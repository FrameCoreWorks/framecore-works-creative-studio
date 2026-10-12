"""Print PDF (static-graphic-design-creator/assets/static-render/print_pdf.py): boxes, output intent, preflight."""
import importlib.util
import math
import json
import pathlib
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/static-graphic-design-creator/assets/static-render/print_pdf.py'
try:
    import pikepdf  # noqa: F401
    from PIL import Image, ImageCms
    spec = importlib.util.spec_from_file_location('print_pdf', TOOL)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
except ImportError:
    tool = None

DPI = 100  # small pages keep the test fast; limits are passed to match


def page_pdf(path, mode, colour, mm=(154, 216), dpi=DPI):
    size = tuple(math.ceil(v / 25.4 * dpi) for v in mm)
    Image.new(mode, size, colour).save(path, resolution=dpi)


def run(*argv):
    out = StringIO()
    with redirect_stdout(out):
        code = tool.main(list(argv))
    return code, out.getvalue()


@unittest.skipUnless(tool, 'pikepdf and Pillow are needed')
class PrintPdfTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_finish_sets_centred_boxes_and_check_passes(self):
        src, out = self.root / 'a5.pdf', self.root / 'a5-print.pdf'
        page_pdf(src, 'CMYK', (10, 20, 30, 0))                       # 148 x 210 trim plus 3 mm bleed
        code, _ = run('finish', str(src), '--trim-mm', '148x210', '--bleed-mm', '3', '--out', str(out))
        self.assertEqual(code, 0)
        code, text = run('check', str(out), '--min-ppi', str(DPI - 1), '--json')
        report = json.loads(text)
        self.assertEqual(report['verdict'], 'PASS', report['problems'])
        page = report['pages'][0]
        self.assertAlmostEqual(page['trim_mm'][0], 148, delta=0.1)
        self.assertAlmostEqual(page['bleed_mm'], 3, delta=0.1)
        self.assertEqual(page['images'][0]['colour'], 'CMYK')

    def test_check_finds_missing_boxes_low_resolution_rgb_and_heavy_ink(self):
        rgb, heavy = self.root / 'rgb.pdf', self.root / 'heavy.pdf'
        page_pdf(rgb, 'RGB', (200, 30, 30))
        code, text = run('check', str(rgb), '--require', 'cmyk', '--json')
        problems = ' '.join(json.loads(text)['problems'])
        self.assertEqual(code, 1)
        for expected in ('TrimBox', 'ppi effective', 'RGB', 'output intent'):
            self.assertIn(expected, problems)
        page_pdf(heavy, 'CMYK', (255, 255, 255, 255))
        code, text = run('check', str(heavy), '--min-ppi', '1', '--json')
        self.assertIn('total ink 400.0 %', ' '.join(json.loads(text)['problems']))

    def test_output_intent_and_too_small_page(self):
        src, out, icc = self.root / 'p.pdf', self.root / 'p-print.pdf', self.root / 'srgb.icc'
        icc.write_bytes(ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
        page_pdf(src, 'RGB', (255, 255, 255))
        code, _ = run('finish', str(src), '--trim-mm', '148x210', '--icc', str(icc), '--condition', 'Test sRGB', '--out', str(out))
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(run('check', str(out), '--min-ppi', '1', '--json')[1])['output_intent'], 'Test sRGB')
        with self.assertRaises(SystemExit):
            run('finish', str(src), '--trim-mm', '160x220', '--out', str(self.root / 'x.pdf'))

    def test_check_reports_a_font_that_is_not_embedded(self):
        try:
            from reportlab.pdfgen import canvas
        except ImportError:
            self.skipTest('reportlab is optional')
        path = self.root / 'text.pdf'
        sheet = canvas.Canvas(str(path), pagesize=(154 * 72 / 25.4, 216 * 72 / 25.4))
        sheet.setFont('Helvetica', 12); sheet.drawString(72, 72, 'Print'); sheet.save()
        report = json.loads(run('check', str(path), '--json')[1])
        self.assertEqual(report['pages'][0]['fonts'], [{'font': '/Helvetica', 'embedded': False}])
        self.assertIn('font /Helvetica is not embedded', ' '.join(report['problems']))


if __name__ == '__main__':
    unittest.main()
