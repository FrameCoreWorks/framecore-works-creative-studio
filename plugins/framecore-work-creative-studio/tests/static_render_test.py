"""Tests for the exact-copy static compositor and the bundled fonts."""
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageFont

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/static-graphic-design-creator/assets/static-render'
FONTS = PLUGIN / 'skills/pipeline-core/assets/fonts'
MOTION = PLUGIN / 'skills/hyperframes-workflow/assets/motion-render/render.py'
POLISH = 'ĄĆĘŁŃÓŚŹŻąćęłńóśźż„”–…€ '


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compose = load(TOOL / 'compose.py', 'compose')


def run(spec, folder, *extra):
    path = pathlib.Path(folder, 'design.static.json')
    path.write_text(json.dumps(spec, ensure_ascii=False), encoding='utf-8')
    done = subprocess.run([sys.executable, str(TOOL / 'compose.py'), str(path), '--out', str(pathlib.Path(folder, 'out')), *extra],
                          capture_output=True, text=True, timeout=120)
    return done.returncode, json.loads(done.stdout.strip().splitlines()[-1])


def text(id, value, **rest):
    layer = {'type': 'text', 'id': id, 'text': value, 'font': 'Inter Bold', 'size': 64, 'color': '#111111', 'box': [40, 40, 1000, 400]}
    layer.update(rest)
    return layer


class Fonts(unittest.TestCase):
    def test_every_bundled_font_matches_its_record_and_licence(self):
        manifest = json.loads((FONTS / 'fonts.json').read_text(encoding='utf-8'))
        self.assertEqual(len(manifest['families']), 6)
        files = 0
        for family in manifest['families']:
            licence = (FONTS / family['folder'] / 'OFL.txt').read_bytes()
            self.assertEqual(hashlib.sha256(licence).hexdigest(), family['licence_sha256'])
            self.assertIn(b'SIL OPEN FONT LICENSE VERSION 1.1', licence.upper())
            self.assertNotIn(b'Reserved Font Name "', licence)
            for item in family['files']:
                data = (FONTS / item['file']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), item['sha256'], item['file'])
                files += 1
        present = sorted(p.relative_to(FONTS).as_posix() for p in FONTS.rglob('*.ttf'))
        self.assertEqual(present, sorted(i['file'] for f in manifest['families'] for i in f['files']))
        self.assertEqual(files, 18)

    def test_every_font_has_the_polish_letters_and_typographic_marks(self):
        for path in sorted(FONTS.rglob('*.ttf')):
            font = ImageFont.truetype(str(path), 40)
            self.assertEqual(compose.missing_glyphs(font, POLISH), [], path.name)

    def test_names_resolve(self):
        index = compose.font_index([])
        for name in ('Inter Bold', 'Archivo Condensed ExtraBold', 'Fraunces Black', 'Anton', 'Source Serif 4 Regular', 'Bricolage Grotesque Bold'):
            self.assertTrue(compose.resolve_font(name, index, PLUGIN).is_file(), name)


class Typesetting(unittest.TestCase):
    def test_polish_rules_keep_short_words_numbers_and_units_together(self):
        self.assertEqual(compose.keep_together('Kup w sklepie 1 299 zł i 5 kg'), 'Kup w sklepie 1 299 zł i 5 kg')

    def test_the_rules_match_the_motion_renderer(self):
        motion = load(MOTION, 'motion_render')
        for sample in ('Pracuj z nami w Krakowie', 'Rabat 30 % i 10 zł', 'a b c d', 'Ósma o 8 min', 'Tylko 1 299 zł', '12 000 osób, 1 2345'):
            self.assertEqual(compose.keep_together(sample), motion.keep_together(sample), sample)


class Compose(unittest.TestCase):
    def test_exact_copy_at_exact_size_with_an_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            spec = {'id': 'post', 'canvas': {'preset': 'instagram-feed-portrait', 'background': '#F5EFE6'},
                    'layers': [text('headline', 'Wyprzedaż do −30% w sobotę', size=96, box=[64, 64, 952, 400]),
                               text('price', '1 299,00 zł', font='Anton', size=120, box=[64, 900, 952, 200], align='right')]}
            code, summary = run(spec, temp, '--formats', 'png,jpg,pdf')
            self.assertEqual(code, 0, summary)
            self.assertEqual(summary['size'], [1080, 1350])
            with Image.open(pathlib.Path(temp, 'out/post.png')) as image:
                self.assertEqual(image.size, (1080, 1350))
            self.assertEqual([t['set_as'] for t in summary['texts']], ['Wyprzedaż do −30% w sobotę', '1 299,00 zł'])
            self.assertEqual(summary['texts'][1]['lines'], ['1 299,00 zł'])
            self.assertTrue(pathlib.Path(temp, 'out/post.audit.json').is_file())
            self.assertTrue(all(c['pass'] for c in summary['contrast']))

    def test_a_word_wider_than_its_box_stops_the_render(self):
        with tempfile.TemporaryDirectory() as temp:
            spec = {'id': 'story', 'canvas': {'width': 1080, 'height': 1920},
                    'layers': [text('headline', 'Najnowocześniejszy', size=200, box=[90, 300, 600, 600])]}
            code, summary = run(spec, temp)
            self.assertEqual(code, 4)
            self.assertEqual(summary['status'], 'text_overflow')
            self.assertIn('Najnowocześniejszy', json.dumps(summary, ensure_ascii=False))
            self.assertFalse(pathlib.Path(temp, 'out/story.png').exists())

    def test_shrink_fits_the_copy_without_dropping_a_word(self):
        with tempfile.TemporaryDirectory() as temp:
            spec = {'id': 'story', 'canvas': {'width': 1080, 'height': 1920},
                    'layers': [text('headline', 'Najnowocześniejszy', size=200, min_size=40, fit='shrink', box=[90, 300, 600, 600])]}
            code, summary = run(spec, temp)
            self.assertEqual(code, 0, summary)
            self.assertTrue(summary['texts'][0]['shrunk'])
            self.assertLess(summary['texts'][0]['size'], 200)
            self.assertEqual(summary['texts'][0]['lines'], ['Najnowocześniejszy'])

    def test_a_character_the_font_lacks_stops_the_render(self):
        with tempfile.TemporaryDirectory() as temp:
            spec = {'id': 'x', 'canvas': {'width': 800, 'height': 400}, 'layers': [text('t', 'Привет', box=[20, 20, 760, 300])]}
            code, summary = run(spec, temp)
            self.assertEqual(code, 4)
            self.assertEqual(summary['status'], 'missing_glyphs')

    def test_print_pdf_has_bleed_and_the_png_the_trim(self):
        with tempfile.TemporaryDirectory() as temp:
            spec = {'id': 'flyer', 'canvas': {'preset': 'a5', 'background': '#204060'},
                    'layers': [{'type': 'rect', 'box': [0, 0, 1748, 600], 'fill': '#F2C14E'},
                               text('title', 'Koncert w parku', color='#FFFFFF', size=160, box=[150, 800, 1448, 600])]}
            code, summary = run(spec, temp, '--formats', 'png,pdf')
            self.assertEqual(code, 0, summary)
            self.assertEqual(summary['size'], [1748, 2480])
            pdf = next(f for f in summary['files'] if f['file'].endswith('.pdf'))
            self.assertEqual(pdf['size'], [1820, 2552])  # 3 mm at 300 ppi is 35.4 px, rounded up to 36
            self.assertIn('3 mm bleed', pdf['note'])
            self.assertIn('RGB raster PDF', pdf['note'])
            self.assertTrue(pathlib.Path(temp, 'out/flyer.pdf').read_bytes().startswith(b'%PDF'))

    def test_low_contrast_is_reported_and_strict_makes_it_an_error(self):
        with tempfile.TemporaryDirectory() as temp:
            spec = {'id': 'pale', 'canvas': {'width': 800, 'height': 400, 'background': '#FFFFFF'},
                    'layers': [text('t', 'Ledwo widać', color='#EEEEEE', size=40, box=[20, 20, 760, 300])]}
            code, summary = run(spec, temp)
            self.assertEqual(code, 0)
            self.assertFalse(summary['contrast'][0]['pass'])
            code, summary = run(spec, temp, '--strict')
            self.assertEqual((code, summary['status']), (5, 'low_contrast'))

    def test_text_outside_the_story_safe_area_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            spec = {'id': 'story', 'canvas': {'preset': 'story-reel-vertical', 'background': '#102030'},
                    'layers': [text('top', 'Nowość', color='#FFFFFF', box=[100, 40, 880, 200]),
                               text('middle', 'Sprawdź', color='#FFFFFF', box=[100, 900, 880, 200])]}
            code, summary = run(spec, temp)
            self.assertEqual(code, 0, summary)
            self.assertEqual(summary['warnings'], ['top: text reaches outside the placement safe area'])

    def test_every_preset_has_a_size(self):
        presets = json.loads((TOOL / 'presets.json').read_text(encoding='utf-8'))
        self.assertEqual(presets['checked'], '2026-10-10')
        for name, item in presets['sizes'].items():
            self.assertTrue('px' in item or 'mm' in item, name)


if __name__ == '__main__':
    unittest.main(verbosity=1)
