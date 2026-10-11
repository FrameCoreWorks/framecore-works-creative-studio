"""Storyboard compositor (storyboard-board-architect/scripts/board_compose.py): pages, PDF, exact labels, placeholders."""
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/storyboard-board-architect/scripts/board_compose.py'
PILLOW = importlib.util.find_spec('PIL') is not None
spec = importlib.util.spec_from_file_location('board_compose', TOOL)
board_compose = importlib.util.module_from_spec(spec)
spec.loader.exec_module(board_compose)


def compose(board, folder, *extra):
    path = pathlib.Path(folder, 'board.json')
    path.write_text(json.dumps(board, ensure_ascii=False), encoding='utf-8')
    done = subprocess.run([sys.executable, '-B', str(TOOL), str(path), '--out-dir', str(pathlib.Path(folder, 'out')), *extra], capture_output=True, text=True, timeout=120)
    return done.returncode, done.stdout, done.stderr


@unittest.skipUnless(PILLOW, 'Pillow is not installed')
class Compose(unittest.TestCase):
    def board(self, folder, n=6, **extra):
        from PIL import Image
        frames = pathlib.Path(folder, 'frames')
        frames.mkdir(exist_ok=True)
        Image.new('RGB', (900, 1600), (210, 140, 60)).save(frames / 's01.png')
        panels = [{'id': f'S{i + 1:02d}', 'time': f'0:{2 * i:02d}–0:{2 * i + 2:02d}', 'camera': 'MCU', 'action': f'Ujęcie {i + 1}: słoik na stole, światło od okna.'} for i in range(n)]
        panels[0].update(image='frames/s01.png', super='Miód z Beskidów')
        return {'title': 'Storyboard v2', 'subtitle': 'Pasieka · do akceptacji', 'frame': '9:16', 'columns': 6, 'panels': panels, 'notes': 'Założenia: rabat do potwierdzenia.', **extra}

    def test_a_board_becomes_png_pages_and_one_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            code, out, err = compose(self.board(temp), temp)
            self.assertEqual(code, 0, err)
            result = json.loads(out)
            self.assertEqual((result['pages'], result['panels']), (1, 6))
            pdf = pathlib.Path(temp, 'out', 'board.pdf').read_bytes()
            self.assertEqual(len(re.findall(rb'/Type\s*/Page\b', pdf)), 1)
            from PIL import Image
            with Image.open(pathlib.Path(temp, 'out', 'board-p1.png')) as page:
                self.assertEqual(page.size, (1754, 1240))
                # The first frame shows the supplied image (amber).
                r, _, b = page.convert('RGB').getpixel((60 + 100, 170 + 200))
                self.assertGreater(r - b, 80)

    def test_more_panels_flow_onto_more_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            code, out, err = compose(self.board(temp, n=14), temp)
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)['pages'], 3)

    def test_a_missing_image_and_an_existing_output_are_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            board = self.board(temp)
            board['panels'][1]['image'] = 'frames/missing.png'
            code, _, err = compose(board, temp)
            self.assertEqual(code, 2)
            self.assertIn('image not found: frames/missing.png', err)
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(compose(self.board(temp), temp)[0], 0)
            code, _, err = compose(self.board(temp), temp)
            self.assertEqual(code, 2)
            self.assertIn('output exists', err)


class Typesetting(unittest.TestCase):
    def test_one_letter_words_and_numbers_stay_with_their_neighbours(self):
        self.assertEqual(board_compose.keep_together('ręcznie, z dala i w lesie 20 zł'), 'ręcznie, z dala i w lesie 20 zł')


if __name__ == '__main__':
    unittest.main(verbosity=1)
