"""Bounded, polite fetching of a public website: URL safety, robots.txt, pages and stylesheets."""
import http.client
import ipaddress
import socket
import urllib.error
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


def check_url(url, resolve=socket.getaddrinfo, proxies=urllib.request.getproxies):
    """Refuse anything but http(s) to a host that resolves only to public addresses.

    Behind a configured proxy that resolves names itself, an unresolvable name is left to the proxy;
    literal private addresses and localhost are still refused."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ('http', 'https'):
        raise UnsafeURL(f'only http and https are fetched: {url}')
    if not parts.hostname:
        raise UnsafeURL(f'no host in {url}')
    if parts.hostname == 'localhost' or parts.hostname.endswith('.localhost'):
        raise UnsafeURL(f'{parts.hostname} resolves to a non-public address (loopback)')
    try:
        infos = resolve(parts.hostname, parts.port or (443 if parts.scheme == 'https' else 80))
    except OSError as exc:
        if proxies().get(parts.scheme):
            try:
                ipaddress.ip_address(parts.hostname)
            except ValueError:
                return
        raise UnsafeURL(f'cannot resolve {parts.hostname}: {exc}') from exc
    for info in infos:
        address = ipaddress.ip_address(info[4][0].split('%')[0])
        if not address.is_global:
            raise UnsafeURL(f'{parts.hostname} resolves to a non-public address ({address})')


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _check_peer(conn):
    """Refuse a connection whose actual peer is not public: the name may resolve differently than at check_url."""
    host = conn.sock.getpeername()[0]
    address = ipaddress.ip_address(host.split('%')[0])
    if not address.is_global:
        conn.close()
        raise UnsafeURL(f'{conn.host} connected to a non-public address ({address})')


class _CheckedHTTPConnection(http.client.HTTPConnection):
    def connect(self):
        super().connect()
        _check_peer(self)


class _CheckedHTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        super().connect()
        _check_peer(self)


class _CheckedHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(_CheckedHTTPConnection, req)


class _CheckedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_CheckedHTTPSConnection, req, context=self._context)


def _proxied(scheme):
    """True when a configured proxy resolves names for this scheme (its own address is then the peer)."""
    return bool(urllib.request.getproxies().get(scheme))


PAGE_TYPES = ('text/html', 'application/xhtml+xml')
SHEET_TYPES = ('text/css', 'text/plain')
FETCH_ERRORS = (OSError, ValueError, LookupError, http.client.HTTPException)


def fetch(url):
    """GET one URL; returns (status, content type, text, final URL after redirects)."""
    check_url(url)
    handlers = [_SafeRedirect()]
    if not _proxied(urllib.parse.urlsplit(url).scheme):
        handlers += [_CheckedHTTPHandler(), _CheckedHTTPSHandler()]
    opener = urllib.request.build_opener(*handlers)
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,text/css,*/*'})
    try:
        response = opener.open(request, timeout=TIMEOUT)
    except urllib.error.URLError as exc:
        if isinstance(exc.reason, UnsafeURL):
            raise exc.reason
        if not isinstance(exc, urllib.error.HTTPError):
            raise
        return exc.code, exc.headers.get_content_type() if exc.headers else '', '', url
    with response:
        data = response.read(MAX_BYTES + 1)[:MAX_BYTES]
        charset = response.headers.get_content_charset() or 'utf-8'
        try:
            text = data.decode(charset, errors='replace')
        except LookupError:
            text = data.decode('utf-8', errors='replace')
        return response.status, response.headers.get_content_type(), text, response.geturl()


def robots_for(url, fetch=fetch):
    """Return a can_fetch(url) function: a missing robots.txt allows everything, a server error allows nothing."""
    parts = urllib.parse.urlsplit(url)
    parser = urllib.robotparser.RobotFileParser()
    try:
        status, _, text, *_ = fetch(f'{parts.scheme}://{parts.netloc}/robots.txt')
    except FETCH_ERRORS + (UnsafeURL,):
        status, text = 404, ''
    if isinstance(status, int) and status >= 500:
        return lambda target: False
    parser.parse(text.splitlines() if status == 200 else [])
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


def _absolute(base, hrefs):
    out = []
    for href in hrefs:
        try:
            url = urllib.parse.urldefrag(urllib.parse.urljoin(base, href.strip()))[0]
            urllib.parse.urlsplit(url).port  # raises on a malformed port
        except ValueError:
            continue
        out.append(url)
    return out


def links(html, base):
    parser = _Links()
    parser.feed(html)
    return _absolute(base, parser.nav), _absolute(base, parser.other), _absolute(base, parser.stylesheets)


def _host(url):
    host = urllib.parse.urlsplit(url).hostname or ''
    return host[4:] if host.startswith('www.') else host


def _same_site(url, roots):
    return urllib.parse.urlsplit(url).scheme in ('http', 'https') and _host(url) in {_host(r) for r in roots}


def _get(url, fetch, resolve, robots, types):
    """(status, text, final URL); the text is empty when the page was not read or is not of an expected type."""
    if robots is not None and not robots(url):
        return 'robots-disallowed', '', url
    try:
        check_url(url, resolve=resolve)
        status, content_type, text, *final = fetch(url)
    except FETCH_ERRORS + (UnsafeURL,) as exc:
        return f'error: {exc}', '', url
    if status != 200:
        return status, '', url
    if content_type and content_type not in types:
        return f'skipped: {content_type}', '', url
    return status, text, (final[0] if final else url)


def collect(url, pages=3, fetch=fetch, resolve=socket.getaddrinfo, robots=None):
    """Fetch the start page, up to `pages` same-site pages (navigation first) and their stylesheets."""
    check_url(url, resolve=resolve)
    if robots is None:
        robots = robots_for(url, fetch)
    limit = max(1, min(int(pages), MAX_PAGES))
    queue, seen, roots = [url], set(), [url]
    result = {'start_url': url, 'pages': [], 'stylesheets': []}
    sheets = []
    read = lambda: sum(1 for p in result['pages'] if p['status'] != 'robots-disallowed')
    while queue and read() < limit and len(result['pages']) < limit * 4:
        current = queue.pop(0)
        if current in seen:
            continue
        seen.add(current)
        status, html, final = _get(current, fetch, resolve, robots, PAGE_TYPES)
        page = {'url': current, 'status': status, 'html': html}
        if final != current:
            page['final_url'] = final
            roots.append(final)
            seen.add(final)
        result['pages'].append(page)
        if not html:
            continue
        nav, other, css = links(html, final)
        queue.extend(u for u in nav + other if _same_site(u, roots) and u not in seen and u not in queue)
        sheets.extend(s for s in css if s not in sheets)
    for sheet in sheets[:MAX_STYLESHEETS]:
        status, css, _ = _get(sheet, fetch, resolve, robots if _same_site(sheet, roots) else None, SHEET_TYPES)
        result['stylesheets'].append({'url': sheet, 'status': status, 'css': css})
    return result
