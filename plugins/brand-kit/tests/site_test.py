"""brand-kit site fetching: URL safety, robots, page and stylesheet collection. No network."""
import pathlib
import sys
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

    def test_accepts_public(self):
        site.check_url('https://kawiarnialipa.example/', resolve=public)


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

    def test_stylesheets_collected_once(self):
        result, _ = self.run_collect(pages=3, robots=lambda url: True)
        urls = [s['url'] for s in result['stylesheets']]
        self.assertIn('https://lipa.example/css/site.css', urls)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertLessEqual(len(urls), 12)


if __name__ == '__main__':
    unittest.main()
