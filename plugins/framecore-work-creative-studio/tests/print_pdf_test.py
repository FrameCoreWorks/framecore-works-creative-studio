"""Print PDF (static-graphic-design-creator/assets/static-render/print_pdf.py): boxes, output intent, preflight."""
import importlib.util
import json
import math
import pathlib
import shutil
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

    def test_check_walks_forms_vectors_transparency_lines_and_attachments(self):
        try:
            from reportlab.lib.colors import CMYKColorSep
            from reportlab.pdfgen import canvas
        except ImportError:
            self.skipTest('reportlab is optional')
        path, out = self.root / 'vector.pdf', self.root / 'vector-x.pdf'
        sheet = canvas.Canvas(str(path), pagesize=(154 * 72 / 25.4, 216 * 72 / 25.4))
        sheet.beginForm('logo')                                       # RGB hidden inside a form XObject
        sheet.setFillColorRGB(1, 0, 0); sheet.rect(20, 20, 50, 50, fill=1, stroke=0)
        sheet.endForm(); sheet.doForm('logo')
        sheet.setFillColorCMYK(1, 1, 1, 1); sheet.rect(100, 100, 50, 50, fill=1, stroke=0)
        sheet.setFillColor(CMYKColorSep(0, 0.5, 1, 0, spotName='GOLD')); sheet.rect(200, 100, 50, 50, fill=1, stroke=0)
        sheet.setFillAlpha(0.5); sheet.rect(100, 200, 50, 50, fill=1, stroke=0)
        sheet.setLineWidth(0.1); sheet.line(20, 300, 200, 300)
        sheet.save()
        with pikepdf.open(path) as pdf:
            pdf.attachments['manifest.c2pa'] = pikepdf.AttachedFileSpec(pdf, b'claim')
            pdf.save(out)
        code, text = run('check', str(out), '--require', 'x1a', '--json')
        report = json.loads(text)
        problems, notes = ' '.join(report['problems']), ' '.join(report['notes'])
        self.assertEqual(code, 1)
        for expected in ('vector colour in RGB', 'total ink 400.0 %', 'transparency (alpha)', 'line of 0.1 pt',
                         'manifest.c2pa', 'no output intent'):
            self.assertIn(expected, problems)
        self.assertIn('Spot GOLD', notes)
        self.assertEqual(len(report['sha256']), 64)

    @unittest.skipUnless(shutil.which('pdftoppm'), 'pdftoppm (poppler) is needed')
    def test_compare_reports_changes_inside_and_outside_the_region(self):
        from reportlab.pdfgen import canvas
        paths = []
        for index, x_mm in enumerate((20, 20, 60)):
            path = self.root / f'v{index}.pdf'
            sheet = canvas.Canvas(str(path), pagesize=(100 * 72 / 25.4, 100 * 72 / 25.4))
            sheet.rect(x_mm * 72 / 25.4, 50 * 72 / 25.4, 10 * 72 / 25.4, 10 * 72 / 25.4, fill=1)
            sheet.save(); paths.append(str(path))
        self.assertEqual(json.loads(run('compare', paths[0], paths[1])[1])['verdict'], 'SAME')
        code, text = run('compare', paths[0], paths[2], '--region', '15,35,75,55')
        self.assertEqual((code, json.loads(text)['verdict']), (0, 'CHANGED_INSIDE'))
        code, text = run('compare', paths[0], paths[2], '--region', '50,35,75,55')
        self.assertEqual((code, json.loads(text)['verdict']), (1, 'CHANGED_OUTSIDE'))


if __name__ == '__main__':
    unittest.main()
