"""Web reach (research-evidence/assets/web-reach/web_reach.py): offline parsing and the public-URL guard."""
import contextlib
import importlib.util
import io
import pathlib
import unittest
from unittest import mock

TOOL = pathlib.Path(__file__).resolve().parent.parent / 'skills/research-evidence/assets/web-reach/web_reach.py'
spec = importlib.util.spec_from_file_location('web_reach', TOOL)
wr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wr)


class WebReachTest(unittest.TestCase):
    def test_private_local_and_non_http_addresses_are_refused(self):
        for url in ('http://localhost/x', 'http://127.0.0.1/', 'http://169.254.169.254/latest/meta-data', 'http://10.0.0.5/',
                    'http://[::1]/', 'file:///etc/passwd', 'http://printer.local/', 'http://metadata.google.internal/'):
            with self.assertRaises(wr.ReachError, msg=url):
                wr.public_url(url)
        self.assertEqual(wr.public_url('https://93.184.215.14/page'), 'https://93.184.215.14/page')

    def test_bot_challenges_are_recognised(self):
        self.assertTrue(wr.is_challenge('Title: Just a moment...\n\nWarning: This page maybe requiring CAPTCHA'))
        self.assertTrue(wr.is_challenge('Title: Attention Required! | Cloudflare\nRay ID: 12ab'))
        self.assertFalse(wr.is_challenge('Title: Pricing\n\nOur studio offers three packages.'))

    def test_html_becomes_readable_text_without_scripts(self):
        title, text = wr.html_to_text('<html><head><title>Studio</title><style>p{}</style></head><body><h1>Offer</h1>'
                                      '<script>track()</script><p>Three  packages,</p><p>from 900 zł.</p></body></html>')
        self.assertEqual(title, 'Studio')
        self.assertIn('# Offer', text)
        self.assertIn('Three packages,', text)
        self.assertNotIn('track()', text)

    def test_rss_and_atom_feeds(self):
        rss = wr.parse_feed('<rss><channel><title>News</title><item><title>A</title><link>https://e.com/a</link>'
                            '<pubDate>Fri, 16 Oct 2026</pubDate></item></channel></rss>')
        self.assertEqual(rss, {'title': 'News', 'entries': [{'title': 'A', 'link': 'https://e.com/a', 'date': 'Fri, 16 Oct 2026'}]})
        atom = wr.parse_feed('<feed xmlns="http://www.w3.org/2005/Atom"><title>Log</title><entry><title>B</title>'
                             '<link href="https://e.com/b"/><updated>2026-10-16</updated></entry></feed>')
        self.assertEqual(atom['entries'], [{'title': 'B', 'link': 'https://e.com/b', 'date': '2026-10-16'}])
        with self.assertRaises(wr.ReachError):
            wr.parse_feed('<html></html>')

    def test_subtitles_drop_timing_and_rolling_repeats(self):
        vtt = 'WEBVTT\nKind: captions\n\n00:00:00.000 --> 00:00:01.000\nhello <c>world</c>\n\n00:00:01.000 --> 00:00:02.000\nhello world\nnext line\n'
        self.assertEqual(wr.vtt_to_text(vtt), 'hello world\nnext line')

    def test_missing_tools_and_bad_names_fail_with_one_line(self):
        with mock.patch.object(wr.shutil, 'which', return_value=None), \
             mock.patch.object(wr, 'public_url', side_effect=lambda u: u):
            with self.assertRaisesRegex(wr.ReachError, 'yt-dlp is not installed'):
                wr.youtube('https://www.youtube.com/watch?v=x')
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(wr.main(['github', 'not a repo']), 2)
        self.assertIn('expected owner/repo', err.getvalue())


if __name__ == '__main__':
    unittest.main()
