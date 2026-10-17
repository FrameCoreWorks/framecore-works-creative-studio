#!/usr/bin/env python3
"""Web reach: read public sources for research without a login, with the Python standard library.

    python3 web_reach.py read https://example.com/page            # page as readable text
    python3 web_reach.py feed https://example.com/feed.xml         # RSS or Atom entries
    python3 web_reach.py github owner/repo                         # public repository facts and README
    python3 web_reach.py youtube https://www.youtube.com/watch?v=… # title and subtitles (needs yt-dlp)

`read` asks Jina Reader (r.jina.ai) for the page as Markdown and falls back to fetching the page
and stripping its HTML; it reports which route answered and recognises a bot challenge instead of
returning it as content. Every command refuses private, local and metadata addresses, caps the
response size and prints the source URL and retrieval date, so a finding can be cited.

Adapted from Agent Reach (https://github.com/Panniantong/agent-reach, MIT, reviewed at 94f06c1):
the Jina Reader route, the challenge markers and the public-URL guard. Channels that need cookies,
tokens or a logged-in session are deliberately absent: Studio never exports cookies or automates a
platform against its terms. A code sandbox without internet access cannot use this tool; say so
and continue with the host's own search.
"""
import argparse
import datetime
import html.parser
import ipaddress
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UA = 'Mozilla/5.0 (compatible; FrameCoreStudio-research/1.0)'
MAX_BYTES = 5 * 1024 * 1024
BLOCKED_HOSTS = {'localhost', 'local', 'internal', 'lan', 'localdomain', 'home.arpa', 'instance-data',
                 'metadata.google.internal', 'ip6-localhost', 'ip6-loopback'}
BLOCKED_SUFFIXES = ('.localhost', '.local', '.internal', '.lan', '.localdomain', '.home.arpa')


class ReachError(Exception):
    pass


def public_url(url):
    """Accept only http(s) URLs whose host is not private, local or a metadata endpoint."""
    parts = urllib.parse.urlsplit(url.strip())
    if parts.scheme not in ('http', 'https') or not parts.hostname:
        raise ReachError(f'not a public http(s) URL: {url}')
    host = parts.hostname.rstrip('.').lower()
    if host in BLOCKED_HOSTS or host.endswith(BLOCKED_SUFFIXES):
        raise ReachError(f'refused a local or internal host: {host}')
    try:
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            addresses = [ipaddress.ip_address(info[4][0].split('%')[0]) for info in socket.getaddrinfo(host, None)]
        except socket.gaierror as error:
            raise ReachError(f'cannot resolve {host} (no internet access here?): {error}') from None
    for address in addresses:
        if not address.is_global:
            raise ReachError(f'refused a private or reserved address: {host} -> {address}')
    return urllib.parse.urlunsplit(parts)


def fetch(url, accept='*/*'):
    request = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read(MAX_BYTES + 1)
            charset = response.headers.get_content_charset() or 'utf-8'
    except OSError as error:
        raise ReachError(f'could not fetch {url}: {error}') from None
    if len(body) > MAX_BYTES:
        raise ReachError(f'response over {MAX_BYTES} bytes: {url}')
    return body.decode(charset, errors='replace')


def is_challenge(text):
    """A Jina or Cloudflare bot challenge, not the page."""
    sample = text[:4096].casefold()
    jina = 'warning:' in sample and 'requiring captcha' in sample
    challenge = any(m in sample for m in ('title: just a moment...', '## performing security verification',
                                          'title: attention required! | cloudflare', '<title>just a moment...</title>'))
    cloudflare = 'attention required! | cloudflare' in sample and ('ray id' in sample or '/cdn-cgi/challenge-platform/' in sample)
    return (jina and challenge) or cloudflare or (challenge and 'cf-chl' in sample)


class TextFromHtml(html.parser.HTMLParser):
    SKIP = {'script', 'style', 'noscript', 'svg', 'template', 'head'}
    BLOCK = {'p', 'div', 'section', 'article', 'li', 'br', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'footer', 'blockquote'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.title, self.in_title = [], 0, '', False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag == 'title':
            self.in_title = True
        if tag in self.BLOCK:
            self.parts.append('\n')
        if tag in ('h1', 'h2', 'h3') and not self.skip:
            self.parts.append('#' * int(tag[1]) + ' ')

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag == 'title':
            self.in_title = False
        if tag in self.BLOCK:
            self.parts.append('\n')

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif not self.skip:
            self.parts.append(data)

    def text(self):
        joined = re.sub(r'[ \t\r\f\v]+', ' ', ''.join(self.parts))
        lines = [line.strip() for line in joined.split('\n')]
        return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()


def html_to_text(markup):
    parser = TextFromHtml()
    parser.feed(markup)
    return parser.title.strip(), parser.text()


def read(url, route='auto'):
    url = public_url(url)
    tried = []
    if route in ('auto', 'jina'):
        try:
            text = fetch('https://r.jina.ai/' + url, 'text/plain')
            if not is_challenge(text):
                return {'route': 'jina-reader', 'text': text}
            tried.append('jina-reader: bot challenge')
        except ReachError as error:
            tried.append(f'jina-reader: {error}')
    if route in ('auto', 'direct'):
        markup = fetch(url, 'text/html,application/xhtml+xml')
        if is_challenge(markup):
            raise ReachError('the site answered with a bot challenge; read it in a browser or ask the user for the text')
        title, text = html_to_text(markup)
        return {'route': 'direct', 'title': title, 'text': text, 'tried': tried}
    raise ReachError('; '.join(tried) or 'no route')


def local(tag):
    return tag.rsplit('}', 1)[-1]


def parse_feed(xml_text, limit=20):
    root = ET.fromstring(xml_text)
    entries = []
    if local(root.tag) == 'rss':
        channel = root.find('channel')
        title = (channel.findtext('title') or '').strip() if channel is not None else ''
        for item in (channel.findall('item') if channel is not None else [])[:limit]:
            entries.append({'title': (item.findtext('title') or '').strip(), 'link': (item.findtext('link') or '').strip(),
                            'date': (item.findtext('pubDate') or '').strip()})
    elif local(root.tag) == 'feed':
        title = next(((e.text or '').strip() for e in root if local(e.tag) == 'title'), '')
        for entry in [e for e in root if local(e.tag) == 'entry'][:limit]:
            fields = {local(c.tag): c for c in entry}
            link = fields.get('link')
            entries.append({'title': (fields['title'].text or '').strip() if 'title' in fields else '',
                            'link': link.get('href', '') if link is not None else '',
                            'date': ((fields.get('updated') if fields.get('updated') is not None else fields.get('published')).text
                                     if (fields.get('updated') is not None or fields.get('published') is not None) else '')})
    else:
        raise ReachError(f'not an RSS or Atom feed (root element {local(root.tag)})')
    return {'title': title, 'entries': entries}


def github(name):
    match = re.fullmatch(r'(?:https?://github\.com/)?([\w.-]+)/([\w.-]+?)(?:\.git)?/?', name.strip())
    if not match:
        raise ReachError(f'expected owner/repo or a github.com URL: {name}')
    api = f'https://api.github.com/repos/{match[1]}/{match[2]}'
    repo = json.loads(fetch(api, 'application/vnd.github+json'))
    try:
        readme = fetch(api + '/readme', 'application/vnd.github.raw')
    except ReachError:
        readme = ''
    keys = ('full_name', 'description', 'html_url', 'stargazers_count', 'forks_count', 'open_issues_count',
            'default_branch', 'pushed_at', 'archived')
    facts = {k: repo.get(k) for k in keys}
    facts['license'] = (repo.get('license') or {}).get('spdx_id')
    return {'repository': facts, 'readme': readme}


def youtube(url, lang='en,pl'):
    url = public_url(url)
    tool = shutil.which('yt-dlp')
    if not tool:
        raise ReachError('yt-dlp is not installed (pip install yt-dlp); without it read the page with `read` or ask the user for the transcript')
    with tempfile.TemporaryDirectory() as folder:
        command = [tool, '--skip-download', '--write-subs', '--write-auto-subs', '--sub-langs', lang, '--sub-format', 'vtt',
                   '--print-to-file', '%(title)s\t%(channel)s\t%(upload_date)s', str(Path(folder) / 'meta.txt'),
                   '-o', str(Path(folder) / 'video'), url]
        done = subprocess.run(command, capture_output=True, text=True, timeout=180)
        if done.returncode:
            raise ReachError('yt-dlp failed: ' + (done.stderr.strip().splitlines() or ['unknown error'])[-1])
        meta = (Path(folder) / 'meta.txt').read_text(encoding='utf-8').strip().split('\t') if (Path(folder) / 'meta.txt').exists() else []
        subtitles = sorted(Path(folder).glob('video*.vtt'))
        if not subtitles:
            raise ReachError('the video has no subtitles in the requested languages')
        return {'title': meta[0] if meta else '', 'channel': meta[1] if len(meta) > 1 else '', 'uploaded': meta[2] if len(meta) > 2 else '',
                'subtitle_file': subtitles[0].name, 'transcript': vtt_to_text(subtitles[0].read_text(encoding='utf-8'))}


def vtt_to_text(vtt):
    """Subtitle cues as plain text, with the repeated lines of rolling auto-captions removed."""
    lines, last = [], None
    for line in vtt.splitlines():
        line = re.sub(r'<[^>]+>', '', line).strip()
        if not line or line == 'WEBVTT' or '-->' in line or line.startswith(('Kind:', 'Language:', 'NOTE')) or line.isdigit():
            continue
        if line != last:
            lines.append(line)
        last = line
    return '\n'.join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest='command', required=True)
    r = sub.add_parser('read'); r.add_argument('url'); r.add_argument('--route', choices=('auto', 'jina', 'direct'), default='auto')
    f = sub.add_parser('feed'); f.add_argument('url'); f.add_argument('--limit', type=int, default=20)
    g = sub.add_parser('github'); g.add_argument('repo')
    y = sub.add_parser('youtube'); y.add_argument('url'); y.add_argument('--lang', default='en,pl')
    for s in (r, f, g, y):
        s.add_argument('--json', action='store_true')
    args = p.parse_args(argv)
    try:
        if args.command == 'read':
            result = read(args.url, args.route)
        elif args.command == 'feed':
            result = parse_feed(fetch(public_url(args.url), 'application/rss+xml, application/atom+xml, text/xml'), args.limit)
        elif args.command == 'github':
            result = github(args.repo)
        else:
            result = youtube(args.url, args.lang)
    except (ReachError, ET.ParseError, ValueError) as error:
        print(f'web_reach: {error}', file=sys.stderr)
        return 2
    source = getattr(args, 'url', None) or args.repo
    result = {'source': source, 'retrieved': datetime.date.today().isoformat(), **result}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print(f"Source: {source} (retrieved {result['retrieved']}{', via ' + result['route'] if 'route' in result else ''})\n")
        body = result.get('text') or result.get('transcript') or result.get('readme') or ''
        if 'entries' in result:
            body = (result['title'] + '\n' if result['title'] else '') + '\n'.join(f"- {e['date']} {e['title']} {e['link']}".strip() for e in result['entries'])
        if 'repository' in result:
            body = json.dumps(result['repository'], ensure_ascii=False, indent=1) + '\n\n' + body
        print(body)
    return 0


if __name__ == '__main__':
    sys.exit(main())
