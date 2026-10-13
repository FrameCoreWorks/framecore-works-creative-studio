"""Motion technique atlas (hyperframes-workflow/assets/technique-atlas): data shape, lookup, CLI."""
import contextlib
import importlib.util
import io
import json
import pathlib
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/hyperframes-workflow/assets/technique-atlas/atlas.py'
spec = importlib.util.spec_from_file_location('atlas', TOOL)
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)


class TechniqueAtlasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = atlas.load()

    def test_pinned_sources_and_english_only_entries(self):
        self.assertEqual(len(self.data['source']['commit']), 40)
        self.assertEqual(len(self.data['registry']['commit']), 40)
        self.assertIn('MIT', self.data['source']['license'])
        techniques = self.data['techniques']
        self.assertEqual(len(techniques), 637)
        self.assertEqual(len({t['slug'] for t in techniques}), 637)
        for t in techniques:
            self.assertIn(t['family'], self.data['families'])
            for text in [t['name'], t['does'], *t['use_when'], *t['aka'], *t['purposes'], *t['media']]:
                self.assertTrue(text.isascii() or not any('가' <= c <= '힣' for c in text), (t['slug'], text))
            self.assertLessEqual(len(t['registry']), 4)

    def test_pairs_point_at_known_techniques_mostly(self):
        slugs = {t['slug'] for t in self.data['techniques']}
        pairs = [p for t in self.data['techniques'] for p in t['pairs']]
        self.assertGreater(sum(p in slugs for p in pairs) / len(pairs), 0.9)

    def test_lookup_by_brief_names(self):
        self.assertEqual(atlas.find(self.data, 'morph match cut')[0]['slug'], 'morph-match-cut')
        self.assertEqual(atlas.find(self.data, 'Ken Burns')[0]['slug'], 'ken-burns')
        match = atlas.find(self.data, 'match-cut')[0]
        self.assertEqual(match['slug'], 'match-cut')
        self.assertIn('match-cut', match['registry'])
        self.assertEqual(atlas.find(self.data, 'qqqq zzzz xxxx'), [])

    def test_filters_and_cli(self):
        found = atlas.find(self.data, family='transitions', purpose='attention', media='short form', limit=50)
        self.assertTrue(found)
        self.assertTrue(all(t['family'] == 'transitions' and 'attention' in t['purposes'] for t in found))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(atlas.main(['light sweep', '--limit', '1', '--json']), 0)
        self.assertEqual(json.loads(out.getvalue())[0]['slug'], 'light-sweep')
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(atlas.main(['qqqq zzzz xxxx']), 1)


if __name__ == '__main__':
    unittest.main()
