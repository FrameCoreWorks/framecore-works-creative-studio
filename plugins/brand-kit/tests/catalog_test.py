"""brand-kit catalog: per-brand revisions, isolation, diff, export/import; and the launcher end to end."""
import copy
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN / 'scripts'))
import catalog  # noqa: E402

FIX = pathlib.Path(__file__).resolve().parent / 'fixtures'
TEMPLATE = PLUGIN.parent / 'framecore-work-creative-studio/skills/pipeline-core/assets/brand-kit.template.json'


def kit(name='Kawiarnia Lipa', primary='#111111'):
    data = json.loads(TEMPLATE.read_text(encoding='utf-8'))
    data['name'] = name
    data['colours']['primary']['hex'] = primary
    return data


class Catalog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_slugify(self):
        self.assertEqual(catalog.slugify('../Kawiarnia Lipa'), 'kawiarnia-lipa')
        self.assertEqual(catalog.slugify('Zażółć Gęślą'), 'zazolc-gesla')
        with self.assertRaises(ValueError):
            catalog.slugify('../..')

    def test_non_latin_names_get_a_stable_slug(self):
        slug = catalog.slugify('Яндекс')
        self.assertRegex(slug, r'^brand-[0-9a-f]{8}$')
        self.assertEqual(slug, catalog.slugify('Яндекс'))

    def test_orphan_revision_file_does_not_block_saves(self):
        catalog.save(kit(), 'lipa', self.root)
        (self.root / 'lipa/rev-0002.json').write_text('{}', encoding='utf-8')
        self.assertEqual(catalog.save(kit(), 'lipa', self.root), 3)

    def test_name_change_is_reported(self):
        catalog.save(kit('Acme Inc'), 'acme', self.root)
        self.assertEqual(catalog.name_mismatch(kit('Other Brand'), 'acme', self.root), 'Acme Inc')
        self.assertIsNone(catalog.name_mismatch(kit('ACME, Inc.'), 'acme', self.root))

    def test_brands_isolated(self):
        catalog.save(kit('Lipa'), 'lipa', self.root)
        catalog.save(kit('Dąb', '#222222'), 'dab', self.root)
        self.assertEqual(catalog.show('lipa', self.root)['name'], 'Lipa')
        self.assertEqual(catalog.show('dab', self.root)['name'], 'Dąb')
        self.assertEqual([b['brand'] for b in catalog.list_brands(self.root)], ['dab', 'lipa'])
        self.assertTrue(all(p.parent.parent == self.root for p in self.root.glob('*/rev-*.json')))

    def test_revisions_immutable(self):
        self.assertEqual(catalog.save(kit(), 'lipa', self.root, note='first'), 1)
        first = (self.root / 'lipa/rev-0001.json').read_bytes()
        self.assertEqual(catalog.save(kit(primary='#222222'), 'lipa', self.root), 2)
        self.assertEqual((self.root / 'lipa/rev-0001.json').read_bytes(), first)
        self.assertEqual(catalog.show('lipa', self.root, rev=1)['colours']['primary']['hex'], '#111111')
        self.assertEqual(catalog.show('lipa', self.root)['colours']['primary']['hex'], '#222222')
        index = json.loads((self.root / 'lipa/index.json').read_text(encoding='utf-8'))
        self.assertEqual([r['rev'] for r in index['revisions']], [1, 2])
        self.assertEqual(index['revisions'][0]['note'], 'first')
        self.assertEqual(len(index['revisions'][0]['sha256']), 64)

    def test_diff(self):
        a, b = kit(), kit(primary='#222222')
        b['voice']['tone'] = ['ciepły']
        lines = catalog.diff(a, b)
        self.assertIn('colours.primary.hex: "#111111" -> "#222222"', lines)
        self.assertTrue(any(l.startswith('voice.tone:') for l in lines))
        self.assertEqual(catalog.diff(a, copy.deepcopy(a)), [])

    def test_roundtrip_and_validation(self):
        catalog.save(kit(), 'lipa', self.root)
        exported = self.root / 'lipa/rev-0001.json'
        with tempfile.TemporaryDirectory() as other:
            catalog.save(json.loads(exported.read_text(encoding='utf-8')), 'lipa', other)
            self.assertEqual(catalog.show('lipa', other), catalog.show('lipa', self.root))
        broken = kit()
        del broken['voice']
        with self.assertRaisesRegex(ValueError, 'voice'):
            catalog.save(broken, 'lipa', self.root)
        with self.assertRaises(FileNotFoundError):
            catalog.show('nope', self.root)


class Launcher(unittest.TestCase):
    def run_cli(self, *args, env=None):
        return subprocess.run([sys.executable, str(PLUGIN / 'scripts/brandkit.py'), *args], capture_output=True,
                              text=True, env=env, check=False)

    def test_offline_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = pathlib.Path(tmp)
            r = self.run_cli('extract', '--html', str(FIX / 'home.html'), '--css', str(FIX / 'site.css'),
                             '--base-url', 'https://lipa.example/', '--out', str(t / 'evidence.json'))
            self.assertEqual(r.returncode, 0, r.stderr)
            r = self.run_cli('draft', str(t / 'evidence.json'), '--out', str(t / 'kit.json'),
                             '--ledger', str(t / 'sources.json'))
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads((t / 'kit.json').read_text(encoding='utf-8'))['name'], 'Kawiarnia Lipa')
            env = dict(os.environ, BRAND_KIT_ROOT=str(t / 'kits'))
            r = self.run_cli('save', str(t / 'kit.json'), '--brand', 'Kawiarnia Lipa', env=env)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((t / 'kits/kawiarnia-lipa/rev-0001.json').is_file())
            r = self.run_cli('list', '--json', env=env)
            self.assertEqual(json.loads(r.stdout)[0]['latest'], 1)

    def test_unsafe_url_is_a_clean_error(self):
        r = self.run_cli('extract', 'http://127.0.0.1/', '--out', os.devnull)
        self.assertEqual(r.returncode, 2)
        self.assertIn('non-public', r.stderr)
        self.assertNotIn('Traceback', r.stderr)


if __name__ == '__main__':
    unittest.main()
