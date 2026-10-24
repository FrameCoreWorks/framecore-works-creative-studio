"""Bounded, polite fetching of a public website: URL safety, robots.txt, pages and stylesheets."""
import ipaddress
import socket
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser

USER_AGENT = 'FrameCoreBrandKit/1.0 (+https://github.com/FrameCoreWorks/framecore-works-creative-studio)'
TIMEOUT = 15
MAX_BYTES = 3 * 1024 * 1024
MAX_PAGES = 8
MAX_STYLESHEETS = 12


class UnsafeURL(ValueError):
    pass


def check_url(url, resolve=socket.getaddrinfo):
    """Refuse anything but http(s) to a host that resolves only to public addresses."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ('http', 'https'):
        raise UnsafeURL(f'only http and https are fetched: {url}')
    if not parts.hostname:
        raise UnsafeURL(f'no host in {url}')
    try:
        infos = resolve(parts.hostname, parts.port or (443 if parts.scheme == 'https' else 80))
    except OSError as exc:
        raise UnsafeURL(f'cannot resolve {parts.hostname}: {exc}') from exc
    for info in infos:
        address = ipaddress.ip_address(info[4][0].split('%')[0])
        if not address.is_global:
            raise UnsafeURL(f'{parts.hostname} resolves to a non-public address ({address})')


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    """GET one URL; returns (status, content type, text). Raises OSError or UnsafeURL."""
    check_url(url)
    opener = urllib.request.build_opener(_SafeRedirect())
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,text/css,*/*'})
    with opener.open(request, timeout=TIMEOUT) as response:
        data = response.read(MAX_BYTES + 1)[:MAX_BYTES]
        charset = response.headers.get_content_charset() or 'utf-8'
        return response.status, response.headers.get_content_type(), data.decode(charset, errors='replace')


def robots_for(url, fetch=fetch):
    """Return a can_fetch(url) function for the site; an unreadable robots.txt allows everything."""
    parts = urllib.parse.urlsplit(url)
    parser = urllib.robotparser.RobotFileParser()
    try:
        status, _, text = fetch(f'{parts.scheme}://{parts.netloc}/robots.txt')
        parser.parse(text.splitlines() if status == 200 else [])
    except (OSError, UnsafeURL):
        parser.parse([])
    return lambda target: parser.can_fetch(USER_AGENT, target)


class _Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.nav, self.other, self.stylesheets = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('nav', 'header'):
            self.depth += 1
        elif tag == 'a' and a.get('href'):
            (self.nav if self.depth else self.other).append(a['href'])
        elif tag == 'link' and 'stylesheet' in (a.get('rel') or '').lower().split() and a.get('href'):
            self.stylesheets.append(a['href'])

    def handle_endtag(self, tag):
        if tag in ('nav', 'header') and self.depth:
            self.depth -= 1


def links(html, base):
    parser = _Links()
    parser.feed(html)
    absolute = lambda hrefs: [urllib.parse.urldefrag(urllib.parse.urljoin(base, h))[0] for h in hrefs]
    return absolute(parser.nav), absolute(parser.other), absolute(parser.stylesheets)


def _same_site(url, root):
    a, b = urllib.parse.urlsplit(url), urllib.parse.urlsplit(root)
    return a.scheme in ('http', 'https') and a.hostname == b.hostname


def _get(url, fetch, resolve, robots):
    if robots is not None and not robots(url):
        return 'robots-disallowed', ''
    try:
        check_url(url, resolve=resolve)
        status, _, text = fetch(url)
        return status, text
    except (OSError, UnsafeURL) as exc:
        return f'error: {exc}', ''


def collect(url, pages=3, fetch=fetch, resolve=socket.getaddrinfo, robots=None):
    """Fetch the start page, up to `pages` same-site pages (navigation first) and their stylesheets."""
    check_url(url, resolve=resolve)
    if robots is None:
        robots = robots_for(url, fetch)
    limit = max(1, min(int(pages), MAX_PAGES))
    queue, seen, result = [url], set(), {'start_url': url, 'pages': [], 'stylesheets': []}
    sheets = []
    while queue and len(result['pages']) < limit:
        current = queue.pop(0)
        if current in seen:
            continue
        seen.add(current)
        status, html = _get(current, fetch, resolve, robots)
        result['pages'].append({'url': current, 'status': status, 'html': html})
        if not html:
            continue
        nav, other, css = links(html, current)
        queue.extend(u for u in nav + other if _same_site(u, url) and u not in seen and u not in queue)
        sheets.extend(s for s in css if s not in sheets)
    for sheet in sheets[:MAX_STYLESHEETS]:
        status, css = _get(sheet, fetch, resolve, robots if _same_site(sheet, url) else None)
        result['stylesheets'].append({'url': sheet, 'status': status, 'css': css})
    return result
