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

    def form_pdf(self, path, content, inner, matrix=None):
        with pikepdf.new() as pdf:
            leaf = pdf.make_stream(inner, Type=pikepdf.Name.XObject, Subtype=pikepdf.Name.Form,
                                   BBox=[0, 0, 200, 200], Resources=pikepdf.Dictionary())
            parent = pdf.make_stream(b'/Leaf Do', Type=pikepdf.Name.XObject, Subtype=pikepdf.Name.Form,
                                     BBox=[0, 0, 200, 200], Matrix=matrix or tool.IDENTITY,
                                     Resources=pikepdf.Dictionary(XObject=pikepdf.Dictionary(Leaf=leaf)))
            page = pdf.add_blank_page(page_size=(300, 300))
            page.TrimBox = [10, 10, 290, 290]
            page.BleedBox = [0, 0, 300, 300]
            page.Resources = pikepdf.Dictionary(XObject=pikepdf.Dictionary(Fm0=parent))
            page.Contents = pdf.make_stream(content)
            pdf.save(path)

    def test_nested_forms_inherit_colour_and_line_width(self):
        path = self.root / 'inherit.pdf'
        self.form_pdf(path, b'/DeviceCMYK cs 0.05 w /Fm0 Do',
                      b'1 1 1 1 scn 20 20 50 50 re B')
        code, output = run('check', str(path), '--json')
        report = json.loads(output)
        self.assertEqual(code, 1)
        self.assertEqual(report['pages'][0]['thinnest_line_pt'], 0.05)
        self.assertEqual(report['pages'][0]['vector_tac_max'], 400)
        self.assertIn('total ink 400', ' '.join(report['problems']))

    def test_form_state_does_not_escape_and_q_Q_restores(self):
        path = self.root / 'restore.pdf'
        self.form_pdf(path, b'0.1 w /Fm0 Do 10 10 m 50 50 l S',
                      b'q 0.01 w Q 5 w')
        report = json.loads(run('check', str(path), '--json')[1])
        self.assertEqual(report['pages'][0]['thinnest_line_pt'], 0.1)

    def test_stroke_reports_minimum_scale_bound_including_shear(self):
        for matrix, expected in (([0.01, 0, 0, 100, 0, 0], 0.01),
                                 ([1, 0, 10, 1, 0, 0], 0.099),
                                 ([2, 0, 0, 2, 0, 0], 2),
                                 ([0, 0, 0, 1, 0, 0], 0)):
            with self.subTest(matrix=matrix):
                path = self.root / 'scale.pdf'
                self.form_pdf(path, b'/Fm0 Do', b'0 0 m 100 0 l S', matrix)
                report = json.loads(run('check', str(path), '--json')[1])
                self.assertAlmostEqual(report['pages'][0]['thinnest_line_pt'], expected, places=3)

    def test_declared_bleed_cannot_extend_outside_media(self):
        path = self.root / 'boxes.pdf'
        self.form_pdf(path, b'', b'')
        with pikepdf.open(path) as pdf:
            page = pdf.pages[0]
            page.TrimBox = [0, 0, 300, 300]
            page.BleedBox = [-10, -10, 310, 310]
            bad = self.root / 'outside.pdf'
            pdf.save(bad)
        code, output = run('check', str(bad), '--json')
        report = json.loads(output)
        self.assertEqual(code, 1)
        self.assertIn('MediaBox', ' '.join(report['problems']))
        self.assertEqual(report['pages'][0]['bleed_mm'], 0)
        for trim, bleed in (([20, 20, 280, 280], [30, 10, 290, 290]),
                            ([280, 20, 20, 280], [0, 0, 300, 300])):
            with pikepdf.open(path) as pdf:
                pdf.pages[0].TrimBox = trim
                pdf.pages[0].BleedBox = bleed
                pdf.save(bad)
            self.assertEqual(run('check', str(bad), '--json')[0], 1)

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
        self.assertEqual(report['declared']['Trapped'], '/False')

    def test_trapped_is_a_pdf_name_with_a_valid_value(self):
        src, finished = self.root / 'source.pdf', self.root / 'finished.pdf'
        page_pdf(src, 'CMYK', (10, 20, 30, 0))
        run('finish', str(src), '--trim-mm', '148x210', '--out', str(finished))
        cases = ((pikepdf.Name('/True'), False), (pikepdf.Name('/False'), False),
                 (pikepdf.Name('/Unknown'), False), (pikepdf.Name('/False_'), True),
                 (pikepdf.String('/False'), True), (pikepdf.String('False'), True),
                 (False, True), (0, True), (None, False))
        for value, invalid in cases:
            with self.subTest(value=repr(value)):
                path = self.root / 'variant.pdf'
                with pikepdf.open(finished) as pdf:
                    if value is None:
                        del pdf.docinfo['/Trapped']
                    else:
                        pdf.docinfo['/Trapped'] = value
                    pdf.save(path)
                report = json.loads(run('check', str(path), '--min-ppi', '1', '--json')[1])
                self.assertEqual(any('Trapped' in p for p in report['problems']), invalid, report)
                x1a = json.loads(run('check', str(path), '--require', 'x1a', '--min-ppi', '1', '--json')[1])
                self.assertEqual(any('Trapped' in p for p in x1a['problems']),
                                 invalid or value is None or str(value) == '/Unknown', x1a)

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

    @unittest.skipUnless(shutil.which('pdftoppm'), 'pdftoppm (poppler) is needed')
    def test_blocks_remove_and_move_inside_a_scaled_form(self):
        src = self.root / 'outlined.pdf'
        with pikepdf.new() as pdf:                                    # a generator-style page: one form at 0.1 scale
            form = pdf.make_stream(b'0 0 0 1 k 200 500 300 300 re f 0 1 1 0 k 1000 500 300 300 re f',
                                   Type=pikepdf.Name.XObject, Subtype=pikepdf.Name.Form, BBox=[0, 0, 2835, 2835],
                                   Matrix=[0.1, 0, 0, 0.1, 0, 0], Resources=pikepdf.Dictionary())
            page = pdf.add_blank_page(page_size=(100 * 72 / 25.4, 100 * 72 / 25.4))
            page.Resources = pikepdf.Dictionary(XObject=pikepdf.Dictionary(Fm0=form))
            page.Contents = pdf.make_stream(b'q /Fm0 Do Q')
            pdf.save(src)
        stream = json.loads(run('blocks', str(src))[1])['streams'][1]
        self.assertEqual(stream['stream'], 'Fm0')
        self.assertEqual([b['box_mm'] for b in stream['blocks']], [[7.06, 71.78, 17.64, 82.36], [35.28, 71.78, 45.86, 82.36]])
        same, removed, moved = (self.root / n for n in ('same.pdf', 'removed.pdf', 'moved.pdf'))
        run('move', str(src), '--stream', 'Fm0', '--blocks', '1', '--out', str(same))
        self.assertEqual(json.loads(run('compare', str(src), str(same))[1])['verdict'], 'SAME')
        run('remove', str(src), '--stream', 'Fm0', '--blocks', '0', '--out', str(removed))
        self.assertEqual(json.loads(run('blocks', str(removed))[1])['streams'][1]['blocks'][0]['colour'], '0 1 1 0 k')
        self.assertEqual(run('compare', str(src), str(removed), '--region', '5,70,20,84')[0], 0)
        run('move', str(src), '--stream', 'Fm0', '--blocks', '1', '--dx-mm', '10', '--dy-mm', '-5', '--out', str(moved))
        box = json.loads(run('blocks', str(moved))[1])['streams'][1]['blocks'][1]['box_mm']
        self.assertEqual(box, [45.28, 66.78, 55.86, 77.36])
        self.assertEqual(run('compare', str(src), str(moved), '--region', '33,64,58,85')[0], 0)
        with self.assertRaises(SystemExit):
            run('remove', str(src), '--stream', 'Fm9', '--blocks', '0', '--out', str(removed))


if __name__ == '__main__':
    unittest.main()
