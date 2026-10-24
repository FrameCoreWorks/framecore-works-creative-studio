"""Brand guide (delivery-documentation/scripts/brand_guide.py): pages and PDF from a brand kit, nothing invented."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/delivery-documentation/scripts/brand_guide.py'
TEMPLATE = PLUGIN / 'skills/pipeline-core/assets/brand-kit.template.json'
PILLOW = importlib.util.find_spec('PIL') is not None
spec = importlib.util.spec_from_file_location('brand_guide', TOOL)
brand_guide = importlib.util.module_from_spec(spec)
spec.loader.exec_module(brand_guide)

KIT = {'schema_version': 1, 'name': 'Pasieka Lipa', 'version': '1.0', 'spelling': 'Pasieka Lipa; w Pasiece Lipa',
       'colours': {'primary': {'hex': '#1D3B2A', 'role': 'headlines'}, 'accent': {'hex': '#F2C14E', 'role': 'prices', 'cmyk': '0 22 78 5'},
                   'text': {'hex': '#1D1D1B', 'role': 'body'}, 'background': {'hex': '#F7F3EC', 'role': 'backgrounds'}},
       'fonts': {'headline': {'font': 'Fraunces Black', 'licence': 'OFL (bundled)'}, 'script': {'font': 'Brush Pro', 'licence': 'commercial'}},
       'logo': {'files': {'colour': 'logo.png'}, 'min_width_px': 120, 'clear_space': 'the height of the letter L'},
       'voice': {'address': 'Ty', 'tone': ['ciepły'], 'use': ['prosto z pasieki'], 'avoid': ['najlepszy na świecie']},
       'claims': {'approved': [{'text': 'Miód z Beskidów', 'source': 'adres pasieki'}], 'banned': ['leczy']},
       'legal_lines': ['Miód nie jest lekiem.'], 'do_not': ['Nie zmieniaj proporcji znaku.']}


def run(kit, folder, *extra):
    path = pathlib.Path(folder, 'kit.json')
    path.write_text(json.dumps(kit, ensure_ascii=False), encoding='utf-8')
    done = subprocess.run([sys.executable, '-B', str(TOOL), str(path), '--out-dir', str(pathlib.Path(folder, 'guide')), '--date', '2026-10-11', *extra],
                          capture_output=True, text=True, timeout=180)
    return done.returncode, done.stdout, done.stderr


class Pure(unittest.TestCase):
    def test_contrast_and_placeholders(self):
        self.assertAlmostEqual(brand_guide.contrast((255, 255, 255), (0, 0, 0)), 21.0, places=1)
        self.assertAlmostEqual(brand_guide.contrast((255, 255, 255), (255, 255, 255)), 1.0)
        found = brand_guide.placeholders(json.loads(TEMPLATE.read_text(encoding='utf-8')))
        self.assertIn('name', found)
        self.assertIn('claims.approved[0].source', found)

    def test_bundled_font_lookup_by_name(self):
        self.assertEqual(brand_guide.font_file({'font': 'Fraunces Black'}, PLUGIN).name, 'Fraunces-Black.ttf')
        self.assertIsNone(brand_guide.font_file({'font': 'Brush Pro'}, PLUGIN))


@unittest.skipUnless(PILLOW, 'Pillow is not installed')
class Compose(unittest.TestCase):
    def test_a_kit_becomes_pages_and_a_pdf_with_missing_parts_reported(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            Image.new('RGBA', (600, 200), (29, 59, 42, 255)).save(pathlib.Path(temp, 'logo.png'))
            code, out, err = run(KIT, temp)
            self.assertEqual(code, 0, err)
            result = json.loads(out)
            self.assertEqual(result['pages'], 6)
            self.assertEqual(result['fonts_without_sample'], ['Brush Pro'])
            pdf = pathlib.Path(temp, 'guide/brand-guide.pdf').read_bytes()
            self.assertTrue(pdf.startswith(b'%PDF'))
            self.assertEqual(pdf.count(b'/Type /Page\n') + pdf.count(b'/Type /Page\r') + pdf.count(b'/Type /Page '), 6)
            with Image.open(pathlib.Path(temp, 'guide/brand-guide-p1.png')) as cover:
                self.assertEqual(cover.size, brand_guide.PAGE)
                self.assertEqual(cover.getpixel((5, 5)), (247, 243, 236))

    def test_template_placeholders_stop_the_run_unless_draft(self):
        with tempfile.TemporaryDirectory() as temp:
            kit = json.loads(TEMPLATE.read_text(encoding='utf-8'))
            code, _, err = run(kit, temp)
            self.assertEqual(code, 2)
            self.assertIn('--draft', err)
            code, out, err = run(kit, temp, '--draft', '--language', 'pl')
            self.assertEqual(code, 0, err)
            self.assertTrue(json.loads(out)['draft'])

    def test_bad_colour_and_existing_output_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            kit = json.loads(json.dumps(KIT))
            kit['colours']['primary']['hex'] = 'green'
            self.assertEqual(run(kit, temp)[0], 2)
            kit['colours']['primary']['hex'] = '#1D3B2A'
            kit['logo'] = {}
            self.assertEqual(run(kit, temp)[0], 0)
            code, _, err = run(kit, temp)
            self.assertEqual(code, 2)
            self.assertIn('exists', err)


class LongTokenWrapping(unittest.TestCase):
    def test_every_intermediate_token_is_split_without_losing_letters(self):
        import ast
        from types import SimpleNamespace
        tree = ast.parse(TOOL.read_text())
        function = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'wrap')
        unit = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
        namespace = {'keep_together': lambda text: text}
        exec(compile(unit, str(TOOL), 'exec'), namespace)
        for text in ('X'*26 + ' next', 'before ' + 'X'*26 + ' next', 'X'*26, 'X'*26 + ' ' + 'Y'*24):
            lines = namespace['wrap'](text, SimpleNamespace(getlength=lambda s: 10*len(s)), 100)
            self.assertTrue(all(len(line) <= 10 for line in lines), lines)
            self.assertEqual(''.join(lines).replace(' ', ''), text.replace(' ', ''))
        with self.assertRaisesRegex(ValueError, 'glyph'):
            namespace['wrap']('X next', SimpleNamespace(getlength=lambda s: 10*len(s)), 5)


if __name__ == '__main__':
    unittest.main()
