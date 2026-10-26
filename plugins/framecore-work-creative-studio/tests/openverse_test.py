"""Openverse search (reference-pack-curator/scripts/openverse.py): offline parsing, licence filter, warnings and failures."""
import contextlib
import importlib.util
import io
import json
import pathlib
import unittest
import urllib.error
from unittest import mock

TOOL = pathlib.Path(__file__).resolve().parent.parent / 'skills/reference-pack-curator/scripts/openverse.py'
spec = importlib.util.spec_from_file_location('openverse', TOOL)
ov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ov)

REPLY = {'result_count': 2, 'results': [
    {'title': 'Bakery', 'creator': 'InfoMofo', 'license': 'by-sa', 'license_version': '2.0', 'source': 'flickr',
     'url': 'https://example.org/a.jpg', 'attribution': '"Bakery" by InfoMofo is licensed under CC BY-SA 2.0.'},
    {'title': 'Bread', 'creator': None, 'license': 'cc0', 'url': 'https://example.org/b.jpg'}]}


def opener_for(reply, seen):
    def opener(request, timeout):
        seen.append(request.full_url)
        return io.BytesIO(json.dumps(reply).encode())
    return opener


class OpenverseTest(unittest.TestCase):
    def test_commercial_filter_and_warnings(self):
        seen = []
        found = ov.search('bakery', opener=opener_for(REPLY, seen))
        self.assertIn('/v1/images/', seen[0])
        self.assertIn('license_type=commercial%2Cmodification', seen[0])
        first, second = found['results']
        self.assertIn('share-alike', first['warnings'][0])
        self.assertEqual(first['attribution'], REPLY['results'][0]['attribution'])
        self.assertIn('creator unknown', second['warnings'][0])
        self.assertNotIn('creator', second)

    def test_audio_and_any_licence(self):
        seen = []
        ov.search('rain', media='audio', any_licence=True, opener=opener_for({'results': []}, seen))
        self.assertIn('/v1/audio/', seen[0])
        self.assertNotIn('license_type', seen[0])
        ov.search('door', media='audio', licence='cc0,by', opener=opener_for({'results': []}, seen))
        self.assertIn('license=cc0%2Cby', seen[1])
        self.assertNotIn('license_type', seen[1])

    def test_html_or_null_reply(self):
        with self.assertRaises(ValueError):
            ov.search('rain', opener=lambda request, timeout: io.BytesIO(b'<html>'))
        self.assertEqual(ov.search('rain', opener=opener_for({'results': None}, []))['results'], [])

    def test_rate_limit_and_offline_give_a_link(self):
        for error, code in ((urllib.error.HTTPError('u', 429, 'Too Many', {}, None), 2), (urllib.error.URLError('down'), 3),
                            (urllib.error.HTTPError('u', 503, 'Unavailable', {}, None), 3), (ValueError('not JSON'), 3)):
            out = io.StringIO()
            with mock.patch.object(ov, 'search', side_effect=error), contextlib.redirect_stdout(out):
                self.assertEqual(ov.main(['rain', '--media', 'audio']), code)
            reply = json.loads(out.getvalue())
            self.assertTrue(reply['link'].startswith('https://openverse.org/search/audio?q=rain'))


if __name__ == '__main__':
    unittest.main()
