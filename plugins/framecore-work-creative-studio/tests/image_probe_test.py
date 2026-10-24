"""Tests for the raster probe used before reviewing an actual output."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/output-critic-iteration/scripts/image_probe.py'


def probe(image, *args):
    with tempfile.TemporaryDirectory() as temp:
        path = pathlib.Path(temp, 'out.png')
        image.save(path)
        done = subprocess.run([sys.executable, str(TOOL), str(path), '--json', *args], capture_output=True, text=True, timeout=60)
        return done.returncode, json.loads(done.stdout)


class Words(unittest.TestCase):
    def test_numbers_keep_their_sign_decimals_and_per_cent(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('image_probe', TOOL)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.normalise('Promocja -50% — 99,99 zł'), ['promocja', '-50%', '99,99', 'zł'])
        self.assertNotEqual(mod.normalise('-50%'), mod.normalise('50'))


class Reconstruction(unittest.TestCase):
    def test_palette_tones_and_subject_position_are_measured(self):
        from PIL import ImageDraw
        image = Image.new('RGB', (1200, 900), '#F3F2EF')
        ImageDraw.Draw(image).ellipse([400, 300, 640, 780], fill='#B95A40')
        code, report = probe(image, '--analyze')
        analysis = report['analysis']
        self.assertEqual(analysis['palette'][0]['hex'], '#F3F2EF')
        self.assertIn('#B95A40', [c['hex'] for c in analysis['palette']])
        self.assertEqual(analysis['tones']['key'], 'high')
        subject = analysis['subject']
        self.assertEqual(subject['status'], 'measured')
        self.assertEqual(subject['centre_percent'], {'x': 43, 'y': 60})
        self.assertEqual(subject['box_percent'], {'left': 33, 'top': 33, 'right': 54, 'bottom': 87})
        self.assertIn('no colour profile', analysis['colour_basis'])

    def test_a_busy_border_is_not_given_a_false_position(self):
        from PIL import ImageDraw
        image = Image.new('RGB', (400, 300), 'white')
        draw = ImageDraw.Draw(image)
        for x in range(0, 400, 10):
            draw.rectangle([x, 0, x + 4, 300], fill=(30 + x % 200, 90, 160))
        code, report = probe(image, '--analyze')
        self.assertEqual(report['analysis']['subject']['status'], 'not_measured')

    def test_near_identical_shades_merge_and_a_small_accent_is_kept(self):
        # Before 1.84.0 a white field came back as four "colours" (#FEFEFE, #FFFFFF, #FFFEFF, ...) and a small red sign was lost.
        from PIL import ImageDraw
        image = Image.new('RGB', (800, 800), '#FEFEFE')
        draw = ImageDraw.Draw(image)
        for i, shade in enumerate(('#FFFFFF', '#FFFEFF', '#FDFEFD')):
            draw.rectangle([0, 200 * i, 800, 200 * i + 120], fill=shade)
        draw.rectangle([100, 700, 700, 790], fill='#202020')
        draw.rectangle([600, 40, 640, 80], fill='#D8231F')           # 0.25 % of the frame
        analysis = probe(image, '--analyze')[1]['analysis']
        whites = [c for c in analysis['palette'] if c['hex'] >= '#F0F0F0']
        self.assertEqual(len(whites), 1, analysis['palette'])
        self.assertGreater(whites[0]['share'], 0.8)
        reds = [c['hex'] for c in analysis['accents']]
        self.assertTrue(any(int(h[1:3], 16) > 180 and int(h[3:5], 16) < 80 for h in reds), analysis['accents'])

    def test_a_small_white_is_the_white_point_of_a_dark_photograph(self):
        # A small white (a hat) on a dark photograph vanished from the palette before 1.84.0.
        from PIL import ImageDraw
        image = Image.new('RGB', (600, 900), '#2A2A2A')
        ImageDraw.Draw(image).ellipse([300, 500, 340, 530], fill='#F4F4F4')
        tones = probe(image, '--analyze')[1]['analysis']['tones']
        self.assertLessEqual(abs(int(tones['white_point'][1:3], 16) - 0xF4), 4, tones)   # resampling may overshoot a little
        self.assertLessEqual(abs(int(tones['black_point'][1:3], 16) - 0x2A), 4, tones)

    def test_the_focus_map_finds_the_sharp_region_and_the_light_map_the_bright_side(self):
        from PIL import ImageDraw, ImageFilter
        image = Image.new('RGB', (800, 800), (110, 110, 110))
        draw = ImageDraw.Draw(image)
        for x in range(0, 800, 12):
            draw.line([x, 0, x, 800], fill=(40, 40, 40), width=3)
        blurred = image.filter(ImageFilter.GaussianBlur(6))
        blurred.paste(image.crop((400, 400, 800, 800)), (400, 400))  # only the lower right quarter is sharp
        ramp = Image.linear_gradient('L').rotate(-90).resize((800, 800))   # brighter on the left
        lit = Image.composite(blurred, Image.new('RGB', (800, 800), (0, 0, 0)), ramp.point(lambda v: 120 + v // 2))
        analysis = probe(lit, '--analyze')[1]['analysis']
        focus = analysis['focus_grid']
        self.assertGreater(min(focus[r][c] for r in (2, 3) for c in (2, 3)), 2 * max(focus[r][c] for r in (0, 1) for c in (0, 1)), focus)
        self.assertIn('left', analysis['light']['brighter_side'])
        self.assertEqual(analysis['character']['saturation'], 'monochrome')

    def test_warm_and_cool_images_are_told_apart(self):
        warm = probe(Image.new('RGB', (200, 200), (196, 150, 98)), '--analyze')[1]['analysis']['character']
        cool = probe(Image.new('RGB', (200, 200), (98, 140, 196)), '--analyze')[1]['analysis']['character']
        self.assertEqual(warm['temperature'], 'warm')
        self.assertEqual(cool['temperature'], 'cool')

    def test_a_display_p3_file_is_converted_to_srgb(self):
        from PIL import ImageCms
        try:
            p3 = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB'))
        except Exception:
            self.skipTest('no colour management')
        # A profile that only names itself differently stands in for Display P3: the conversion path must run and say so.
        image = Image.new('RGB', (100, 100), (200, 30, 30))
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'p3.png')
            image.save(path, icc_profile=p3.tobytes())
            done = subprocess.run([sys.executable, str(TOOL), str(path), '--json', '--analyze'], capture_output=True, text=True, timeout=60)
        basis = json.loads(done.stdout)['analysis']['colour_basis']
        self.assertTrue(basis.startswith(('embedded', 'converted')), basis)

    def test_paper_grain_over_the_whole_frame_is_not_a_subject(self):
        # Before 1.84.0 a sketchbook texture was "measured" as a subject filling 3-97 % of the width.
        import random
        rng = random.Random(4)
        image = Image.new('RGB', (400, 600), (230, 222, 205))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)
        for _ in range(500):
            x, y = rng.randrange(10, 386), rng.randrange(10, 586)
            draw.rectangle([x, y, x + 3, y + 3], fill=(120, 110, 95))
        self.assertEqual(probe(image, '--analyze')[1]['analysis']['subject']['status'], 'not_measured')


class Probe(unittest.TestCase):
    def test_a_matching_feed_image_has_no_problem(self):
        code, report = probe(Image.new('RGB', (1080, 1350), '#336699'), '--preset', 'instagram-feed-portrait')
        self.assertEqual((code, report['problems']), (0, []))
        self.assertIn('instagram-feed-portrait', report['matching_presets'])
        self.assertEqual(report['ratio'], '4:5')

    def test_a_wrong_ratio_is_a_problem(self):
        code, report = probe(Image.new('RGB', (1080, 1080), 'white'), '--preset', 'story-reel-vertical')
        self.assertEqual(code, 1)
        self.assertIn('ratio 1:1 does not match the target 9:16', report['problems'][0])

    def test_print_resolution_counts_the_bleed(self):
        # A5 with 3 mm bleed at 300 ppi is 1819 x 2551 px; half of that is about 150 ppi.
        code, report = probe(Image.new('RGB', (1819, 2551), 'white'), '--print-mm', '148x210', '--bleed-mm', '3')
        self.assertEqual((code, report['effective_ppi']), (0, 300))
        code, report = probe(Image.new('RGB', (910, 1276), 'white'), '--print-mm', '148x210', '--bleed-mm', '3')
        self.assertEqual(code, 1)
        self.assertIn('below the 300 ppi', report['problems'][0])

    def test_transparency_and_previews(self):
        image = Image.new('RGBA', (400, 200), (0, 0, 0, 0))
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'logo.png')
            image.save(path)
            done = subprocess.run([sys.executable, str(TOOL), str(path), '--json', '--preset', 'story-reel-vertical', '--previews', temp],
                                  capture_output=True, text=True, timeout=60)
            report = json.loads(done.stdout)
            self.assertEqual(report['transparency'], 'used')
            self.assertEqual(report['previews'], ['logo-phone.png', 'logo-thumb.png', 'logo-grey.png', 'logo-safe.png'])
            with Image.open(pathlib.Path(temp, 'logo-phone.png')) as phone:
                self.assertEqual(phone.width, 360)

    def test_ocr_is_reported_as_not_run_without_it(self):
        try:
            import pytesseract  # noqa: F401
            self.skipTest('OCR is installed here')
        except ImportError:
            pass
        code, report = probe(Image.new('RGB', (200, 100), 'white'), '--copy', 'Miód')
        self.assertEqual(report['ocr']['status'], 'not_run')


class AuditImageCases(unittest.TestCase):
    def test_displayed_size_respects_exif_and_preserves_stored_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp)/'rotated.jpg'
            image = Image.new('RGB', (135, 108), 'white')
            exif = Image.Exif(); exif[274] = 6
            image.save(path, exif=exif)
            done = subprocess.run([sys.executable, str(TOOL), str(path), '--size', '108x135', '--json'],
                                  capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stderr)
            report = json.loads(done.stdout)
            self.assertEqual(report['size'], [108, 135])
            self.assertEqual(report['stored_size'], [135, 108])
            self.assertEqual(report['exif_orientation'], 6)
            self.assertEqual(report['format'], 'JPEG')

    def test_rgb_and_grey_png_transparency_is_detected(self):
        for mode, colour, transparent in [('RGB', (255, 0, 0), (255, 0, 0)), ('L', 0, 0)]:
            image = Image.new(mode, (32, 32), colour)
            image.info['transparency'] = transparent
            self.assertEqual(probe(image)[1]['transparency'], 'used')

    def test_exact_inventory_counts_repeated_short_and_numeric_additions(self):
        import importlib.util
        from types import SimpleNamespace
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('probe_inventory', TOOL)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        image = Image.new('RGB', (10, 10), 'white')
        fake = SimpleNamespace(image_to_string=lambda *a, **kw: 'Buy now now 1 x')
        with patch.dict(sys.modules, {'pytesseract': fake}):
            self.assertEqual(mod.ocr_compare(image, 'Buy now')['status'], 'match')
            exact = mod.ocr_compare(image, 'Buy now', exact=True)
            self.assertEqual(exact['status'], 'mismatch')
            self.assertEqual(exact['unexpected_words'], ['now', '1', 'x'])
            self.assertEqual(mod.ocr_compare(image, 'Buy now now 1 x', exact=True)['status'], 'match')


if __name__ == '__main__':
    unittest.main(verbosity=1)
