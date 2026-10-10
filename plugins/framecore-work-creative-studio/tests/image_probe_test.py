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


if __name__ == '__main__':
    unittest.main(verbosity=1)
