"""The commercial scene kinds in the Python renderer (lower third, bar and line charts, photo hero, word entries and
persistent elements): they render, and text that would be cut stops the render."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
RENDER = PLUGIN / 'skills/hyperframes-workflow/assets/motion-render/render.py'
CRITIQUE = PLUGIN / 'skills/hyperframes-workflow/assets/motion-review/critique.py'
EXAMPLE = json.loads((PLUGIN / 'skills/hyperframes-workflow/assets/motion-scenes/examples/data-and-names.motion-score.json').read_text(encoding='utf-8'))
PHOTO = json.loads((PLUGIN / 'skills/hyperframes-workflow/assets/motion-scenes/examples/photo-and-trend.motion-score.json').read_text(encoding='utf-8'))


def render(contract, *extra, stills='100,320', keep=None):
    with tempfile.TemporaryDirectory() as temp:
        path = pathlib.Path(temp, 'c.motion.json')
        path.write_text(json.dumps(contract, ensure_ascii=False), encoding='utf-8')
        done = subprocess.run([sys.executable, '-B', str(RENDER), str(path), '--stills', stills, '--stills-dir', str(pathlib.Path(temp, 's')), *extra],
                              capture_output=True, text=True, timeout=300)
        summary = json.loads(done.stdout) if done.stdout.strip() else None
        if keep is not None and summary:
            keep.extend(Image.open(p).convert('RGB') for p in summary['stills'])
        return done.returncode, summary, done.stderr


class Kinds(unittest.TestCase):
    def test_the_example_renders_in_both_formats(self):
        for extra in ([], ['--format', '9x16']):
            code, summary, err = render(EXAMPLE, *extra)
            self.assertEqual(code, 0, err)
            self.assertEqual(len(summary['stills']), 2)

    def test_a_name_wider_than_the_frame_stops_the_render(self):
        contract = json.loads(json.dumps(EXAMPLE))
        contract['copy']['name'] = 'Aleksandra Konstantynopolitańczykiewiczówna-Brzęczyszczykiewicz'
        contract['scenes'][0]['params']['nameSize'] = 120
        code, summary, err = render(contract)
        self.assertEqual(code, 4, err)
        self.assertEqual(summary['status'], 'text_overflow')

    def test_a_persistent_line_wider_than_the_frame_stops_the_render(self):
        contract = json.loads(json.dumps(PHOTO))
        contract['copy']['tag'] = 'Bezpłatna dostawa dla każdego zamówienia przez cały październik i listopad'
        code, summary, err = render(contract)
        self.assertEqual((code, summary['status']), (4, 'text_overflow'), err)
        self.assertIn('Bezpłatna dostawa', json.dumps(summary['text_overflow'], ensure_ascii=False))

    def test_an_active_word_wider_than_the_frame_stops_the_render(self):
        contract = json.loads((PLUGIN / 'skills/hyperframes-workflow/assets/motion-scenes/examples/social-captions.motion-score.json').read_text(encoding='utf-8'))
        key = contract['captions'][0]['copy']
        contract['copy'][key] = 'Konstantynopolitańczykiewiczówna'
        contract['captions'][0]['words'] = [[contract['captions'][0]['start'], contract['captions'][0]['end']]]
        contract['tokens']['captions']['size'] = 120
        code, summary, err = render(contract, stills=str(contract['captions'][0]['start']))
        self.assertEqual((code, summary['status']), (4, 'text_overflow'), err)

    def test_a_value_wider_than_its_room_stops_the_render(self):
        contract = json.loads(json.dumps(EXAMPLE))
        contract['scenes'][1]['params']['bars'][0]['value'] = 123456789
        contract['scenes'][1]['params']['valueWidth'] = 2
        code, summary, err = render(contract)
        self.assertEqual(code, 4, err)
        self.assertIn('123', json.dumps(summary['text_overflow'], ensure_ascii=False))



class PhotoChartWords(unittest.TestCase):
    def test_the_example_renders_in_both_formats_without_showing_the_photo_edge(self):
        for extra in ([], ['--format', '16x9']):
            images = []
            code, summary, err = render(PHOTO, *extra, stills='0,130', keep=images)
            self.assertEqual(code, 0, err)
            # The warm photo covers every corner at the start and, pushed in and drifted up, the bottom edge before its exit;
            # an uncovered edge would show the neutral grey of the shaded canvas.
            for image in images:
                for x, y in ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1), (image.width // 2, image.height - 1)):
                    r, _, b = image.getpixel((x, y))
                    self.assertGreater(r, b + 20, (extra, x, y))

    def test_the_mark_stays_in_its_corner_on_every_scene(self):
        images = []
        code, _, err = render(PHOTO, stills='0,200,389', keep=images)
        self.assertEqual(code, 0, err)
        for image in images:
            corner = image.crop((image.width - 86 - 100, 192, image.width - 86, 292)).convert('RGB')
            self.assertGreater(sum(1 for x in range(corner.width) for y in range(corner.height) if (lambda px: px[0] > 190 and 120 < px[1] < 170 and px[2] < 90)(corner.getpixel((x, y)))), 500, "the mark's amber circle")

    def test_a_month_label_wider_than_its_slot_stops_the_render(self):
        contract = json.loads(json.dumps(PHOTO))
        contract['copy']['m1'] = 'styczeń dwa tysiące dwudziestego szóstego roku'
        code, summary, err = render(contract)
        self.assertEqual(code, 4, err)
        self.assertEqual(summary['status'], 'text_overflow')

    def test_the_critique_reports_a_word_wider_than_its_column_without_rendering(self):
        contract = json.loads(json.dumps(PHOTO))
        contract['scenes'][2]['params']['sizes'] = [176, 108]
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'c.motion.json')
            path.write_text(json.dumps(contract, ensure_ascii=False), encoding='utf-8')
            done = subprocess.run([sys.executable, '-B', str(CRITIQUE), str(path), '--no-frames'], capture_output=True, text=True, timeout=120)
        result = json.loads(done.stdout)
        self.assertEqual(done.returncode, 1)
        self.assertTrue(any('przedsprzedaży' in f['message'] and f['severity'] == 'error' for f in result['findings']))
        self.assertTrue(result['verdicts']['text_completeness'].startswith('fail'))

    def test_word_entries_wrap_a_long_line_like_the_browser(self):
        contract = json.loads(json.dumps(PHOTO))
        contract['copy']['offer-2'] = 'w przedsprzedaży do końca tygodnia z darmową dostawą'
        code, summary, err = render(contract, stills='389')
        self.assertEqual(code, 0, err)


if __name__ == '__main__':
    unittest.main(verbosity=1)
