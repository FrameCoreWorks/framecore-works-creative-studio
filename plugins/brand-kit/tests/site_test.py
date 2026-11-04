"""brand-kit site fetching: URL safety, robots, page and stylesheet collection. No network."""
import pathlib
import sys
import socket
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN / 'scripts'))
import site_fetch as site  # noqa: E402

FIX = pathlib.Path(__file__).resolve().parent / 'fixtures'
HOME = (FIX / 'home.html').read_text(encoding='utf-8')
CSS = (FIX / 'site.css').read_text(encoding='utf-8')


def public(host, *args, **kwargs):
    return [(2, 1, 6, '', ('93.184.216.34', 0))]


class StubFetch:
    def __init__(self, fail=()):
        self.calls, self.fail = [], set(fail)

    def __call__(self, url):
        self.calls.append(url)
        if url in self.fail:
            raise OSError('boom')
        if url.endswith('.css'):
            return 200, 'text/css', CSS
        if 'fonts.googleapis.com' in url:
            return 200, 'text/css', '@font-face { font-family: "Fraunces"; }'
        return 200, 'text/html', HOME


class CheckUrl(unittest.TestCase):
    def test_refuses_unsafe(self):
        for url in ('ftp://example.com/', 'file:///etc/passwd', 'http://127.0.0.1/', 'http://10.0.0.1/',
                    'http://169.254.169.254/latest', 'http:///nohost'):
            with self.assertRaises(site.UnsafeURL, msg=url):
                site.check_url(url, resolve=lambda h, *a, **k: [(2, 1, 6, '', (h or '0.0.0.0', 0))])

    def test_refuses_name_resolving_to_private(self):
        with self.assertRaises(site.UnsafeURL):
            site.check_url('http://intranet.example/', resolve=lambda *a, **k: [(2, 1, 6, '', ('192.168.1.5', 0))])

    def test_unresolvable_name_left_to_a_configured_proxy(self):
        def fail(*a, **k):
            raise OSError('no dns')
        site.check_url('https://lipa.example/', resolve=fail, proxies=lambda: {'https': 'http://proxy:8080'})
        with self.assertRaises(site.UnsafeURL):
            site.check_url('https://lipa.example/', resolve=fail, proxies=lambda: {})
        with self.assertRaises(site.UnsafeURL):
            site.check_url('http://localhost:8000/', resolve=public, proxies=lambda: {'http': 'x'})

    def test_accepts_public(self):
        site.check_url('https://kawiarnialipa.example/', resolve=public)


class ConnectTimeCheck(unittest.TestCase):
    """DNS can answer the pre-check with a public address and the connection with a private one (rebinding)."""

    def serve(self):
        import http.server
        import threading
        server = http.server.HTTPServer(('127.0.0.1', 0), http.server.SimpleHTTPRequestHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return f'http://127.0.0.1:{server.server_address[1]}/'

    def test_a_private_peer_is_refused_even_after_a_public_pre_check(self):
        from unittest import mock
        url = self.serve()
        with mock.patch.object(site, 'check_url'), mock.patch.dict('os.environ', {}, clear=True):
            with self.assertRaisesRegex(site.UnsafeURL, 'non-public'):
                site.fetch(url)

    def test_no_proxy_bypass_still_checks_the_peer(self):
        """A proxy is configured but NO_PROXY sends this host direct: the direct peer is checked."""
        from unittest import mock
        url = self.serve()
        env = {'HTTP_PROXY': 'http://proxy.invalid:8080', 'http_proxy': 'http://proxy.invalid:8080',
               'NO_PROXY': '*', 'no_proxy': '*'}
        with mock.patch.object(site, 'check_url'), mock.patch.dict('os.environ', env, clear=True):
            with self.assertRaisesRegex(site.UnsafeURL, 'non-public'):
                site.fetch(url)

    def test_dns_rebinding_with_no_proxy_is_refused_before_any_request(self):
        import http.server
        import threading
        from unittest import mock
        seen = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                seen.append(self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'INTERNAL')

            def log_message(self, *args):
                pass
        server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        real, calls = socket.getaddrinfo, []

        def rebinding(host, port, *args, **kwargs):
            if host == 'rebind.invalid':
                calls.append(host)
                return real('93.184.216.34' if len(calls) == 1 else '127.0.0.1', port, *args, **kwargs)
            return real(host, port, *args, **kwargs)
        env = {'HTTP_PROXY': 'http://proxy.invalid:8080', 'http_proxy': 'http://proxy.invalid:8080',
               'NO_PROXY': '*', 'no_proxy': '*'}
        with mock.patch.object(site.check_url, '__defaults__', (rebinding, site.urllib.request.getproxies)), \
                mock.patch.dict('os.environ', env, clear=True), mock.patch.object(socket, 'getaddrinfo', side_effect=rebinding):
            with self.assertRaisesRegex(site.UnsafeURL, 'non-public'):
                site.fetch(f'http://rebind.invalid:{server.server_address[1]}/x')
        self.assertEqual(seen, [])

    def test_behind_a_real_proxy_the_proxy_is_the_peer(self):
        """Through a configured proxy the peer is the proxy itself, which may sit on a private address."""
        import http.server
        import threading
        from unittest import mock
        seen = []

        class Proxy(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                seen.append(self.path)
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html>ok</html>')

            def log_message(self, *args):
                pass
        server = http.server.HTTPServer(('127.0.0.1', 0), Proxy)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        proxy = f'http://127.0.0.1:{server.server_address[1]}'
        with mock.patch.object(site, 'check_url'), \
                mock.patch.dict('os.environ', {'HTTP_PROXY': proxy, 'http_proxy': proxy}, clear=True):
            self.assertEqual(site.fetch('http://public.example/')[0], 200)
        self.assertEqual(seen, ['http://public.example/'])


class Collect(unittest.TestCase):
    def run_collect(self, **kw):
        fetch = kw.pop('fetch', StubFetch())
        result = site.collect('https://lipa.example/', fetch=fetch, resolve=public, **kw)
        return result, fetch

    def test_same_host_nav_pages_capped(self):
        result, _ = self.run_collect(pages=2, robots=lambda url: True)
        urls = [p['url'] for p in result['pages']]
        self.assertEqual(urls, ['https://lipa.example/', 'https://lipa.example/menu'])
        self.assertTrue(all('example.org' not in u for u in urls))

    def test_pages_capped_at_eight(self):
        result, _ = self.run_collect(pages=50, robots=lambda url: True)
        self.assertLessEqual(len(result['pages']), 8)

    def test_robots_disallowed_not_fetched(self):
        fetch = StubFetch()
        result, _ = self.run_collect(pages=3, fetch=fetch, robots=lambda url: not url.endswith('/menu'))
        menu = [p for p in result['pages'] if p['url'].endswith('/menu')][0]
        self.assertEqual(menu['status'], 'robots-disallowed')
        self.assertNotIn('https://lipa.example/menu', fetch.calls)

    def test_error_recorded_and_run_continues(self):
        fetch = StubFetch(fail={'https://lipa.example/menu'})
        result, _ = self.run_collect(pages=3, fetch=fetch, robots=lambda url: True)
        statuses = {p['url']: p['status'] for p in result['pages']}
        self.assertTrue(statuses['https://lipa.example/menu'].startswith('error'))
        self.assertEqual(statuses['https://lipa.example/o-nas'], 200)

    def test_bad_links_and_ports_do_not_abort(self):
        html = '<nav><a href="http://[oops">x</a><a href="http://lipa.example:abc/">y</a><a href="/menu">m</a></nav>'
        fetch = lambda url: (200, 'text/html', html)
        result = site.collect('https://lipa.example/', pages=3, fetch=fetch, resolve=public, robots=lambda u: True)
        self.assertIn('https://lipa.example/menu', [p['url'] for p in result['pages']])

    def test_www_and_apex_are_one_site_and_redirect_is_followed(self):
        html = '<nav><a href="https://www.lipa.example/menu">m</a></nav>'
        fetch = lambda url: (200, 'text/html', html, url.replace('://lipa', '://www.lipa'))
        result = site.collect('https://lipa.example/', pages=2, fetch=fetch, resolve=public, robots=lambda u: True)
        self.assertEqual([p['url'] for p in result['pages']], ['https://lipa.example/', 'https://www.lipa.example/menu'])
        self.assertEqual(result['pages'][0]['final_url'], 'https://www.lipa.example/')

    def test_non_html_page_is_not_parsed(self):
        fetch = lambda url: (200, 'application/pdf', '%PDF')
        result = site.collect('https://lipa.example/', pages=1, fetch=fetch, resolve=public, robots=lambda u: True)
        self.assertEqual(result['pages'][0]['html'], '')
        self.assertIn('application/pdf', result['pages'][0]['status'])

    def test_robots_server_error_disallows(self):
        can = site.robots_for('https://lipa.example/', fetch=lambda url: (503, 'text/plain', ''))
        self.assertFalse(can('https://lipa.example/menu'))
        can = site.robots_for('https://lipa.example/', fetch=lambda url: (404, 'text/plain', ''))
        self.assertTrue(can('https://lipa.example/menu'))

    def test_stylesheets_collected_once(self):
        result, _ = self.run_collect(pages=3, robots=lambda url: True)
        urls = [s['url'] for s in result['stylesheets']]
        self.assertIn('https://lipa.example/css/site.css', urls)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertLessEqual(len(urls), 12)


if __name__ == '__main__':
    unittest.main()
