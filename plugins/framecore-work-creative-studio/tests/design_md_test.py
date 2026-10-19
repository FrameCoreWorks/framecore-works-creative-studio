"""DESIGN.md export and import for the brand kit (pipeline-core/assets/design-md)."""
import contextlib
import importlib.util
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/pipeline-core/assets/design-md/design_md.py'
GUIDE = PLUGIN / 'skills/delivery-documentation/scripts/brand_guide.py'
TEMPLATE = PLUGIN / 'skills/pipeline-core/assets/brand-kit.template.json'
spec = importlib.util.spec_from_file_location('design_md', TOOL)
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)


def kit():
    k = json.loads(TEMPLATE.read_text(encoding='utf-8'))
    k.update({'name': 'Kawiarnia Lipa', 'spelling': 'Kawiarnia Lipa, w Kawiarni Lipa', 'do_not': ['stock smiles', 'red for prices'],
              'legal_lines': ['Ceny brutto'], 'claims': {'approved': [{'text': 'Palimy co tydzień', 'source': 'umowa'}], 'banned': ['najtańsza kawa']}})
    k['colours']['surface_alt'] = {'hex': '#EDE3D1', 'role': 'cards'}
    return k


def run(*args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return dm.main(list(args))


class DesignMd(unittest.TestCase):
    def test_export_writes_tokens_by_role_and_marks_what_is_missing(self):
        md, css, manifest = dm.export(kit())
        for line in ('--bg: #f7f3ec;', '--fg: #1d1d1b;', '--accent: #f2c14e;', '--primary: #1d3b2a;', '--color-surface-alt: #ede3d1;',
                     '--font-display: "Fraunces", serif;', '--font-body: "Inter", sans-serif;'):
            self.assertIn(line, css)
        self.assertEqual(md.count('\n## '), 8)
        self.assertIn('- stock smiles', md)
        self.assertNotIn('{phrases', md)
        self.assertEqual(manifest['schemaVersion'], 'od-design-system-project/v1')
        self.assertEqual(manifest['id'], 'kawiarnia-lipa')
        empty = dm.export({'name': 'X'})[0]
        self.assertIn(dm.UNSTATED, empty)

    def test_round_trip_keeps_colours_roles_and_donts(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            (tmp / 'kit.json').write_text(json.dumps(kit(), ensure_ascii=False), encoding='utf-8')
            self.assertEqual(run('export', str(tmp / 'kit.json'), '--out-dir', str(tmp / 'd')), 0)
            self.assertEqual(run('export', str(tmp / 'kit.json'), '--out-dir', str(tmp / 'd')), 2)   # never overwrites
            self.assertEqual(run('import', str(tmp / 'd/DESIGN.md'), '--out', str(tmp / 'back.json')), 0)
            back = json.loads((tmp / 'back.json').read_text(encoding='utf-8'))
            self.assertEqual(back['name'], 'Kawiarnia Lipa')
            self.assertEqual(back['colours']['accent'], {'hex': '#F2C14E', 'role': 'prices, highlights'})
            self.assertEqual(back['do_not'], ['stock smiles', 'red for prices'])
            self.assertTrue(back['voice']['address'].startswith('{'))       # never guessed from prose
            self.assertEqual(run('import', str(tmp / 'd/DESIGN.md'), '--tokens', str(tmp / 'd/tokens.css'), '--out', str(tmp / 'back.json')), 2)
            guide = subprocess.run([sys.executable, str(GUIDE), str(tmp / 'back.json'), '--out-dir', str(tmp / 'g'), '--draft'],
                                   capture_output=True, text=True)
            self.assertEqual(guide.returncode, 0, guide.stderr)
            self.assertTrue((tmp / 'g/brand-guide.pdf').is_file())

    def test_an_open_design_package_imports_its_tokens_and_antipatterns(self):
        md = '# Acme\n\n## 2. Color\n\n- **Paper:** `#efe7d2` — background\n\n## 9. Anti-patterns\n\n- ❌ No gradients on text.\n- No emoji.\n'
        css = ':root { --bg: #ffffff; --fg: #111111; --accent: #ed6f5c; --font-display: "Playfair Display", serif; --space-1: 4px; }'
        imported = dm.import_design(md, css)
        self.assertEqual(set(imported['colours']), {'background', 'text', 'accent'})
        self.assertEqual(imported['fonts']['headline']['font'], 'Playfair Display')
        self.assertTrue(imported['fonts']['body']['font'].startswith('{'))
        self.assertEqual(imported['do_not'], ['❌ No gradients on text.', 'No emoji.'])
        without_tokens = dm.import_design(md)
        self.assertEqual(without_tokens['colours'], {'paper': {'hex': '#EFE7D2', 'role': 'background'}})


if __name__ == '__main__':
    unittest.main(verbosity=2)
