"""The lower-third and bar-chart scene kinds in the Python renderer: they render, and text that would be cut stops the render."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
RENDER = PLUGIN / 'skills/hyperframes-workflow/assets/motion-render/render.py'
EXAMPLE = json.loads((PLUGIN / 'skills/hyperframes-workflow/assets/motion-scenes/examples/data-and-names.motion-score.json').read_text(encoding='utf-8'))


def render(contract, *extra):
    with tempfile.TemporaryDirectory() as temp:
        path = pathlib.Path(temp, 'c.motion.json')
        path.write_text(json.dumps(contract, ensure_ascii=False), encoding='utf-8')
        done = subprocess.run([sys.executable, '-B', str(RENDER), str(path), '--stills', '100,320', '--stills-dir', str(pathlib.Path(temp, 's')), *extra],
                              capture_output=True, text=True, timeout=300)
        return done.returncode, json.loads(done.stdout) if done.stdout.strip() else None, done.stderr


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

    def test_a_value_wider_than_its_room_stops_the_render(self):
        contract = json.loads(json.dumps(EXAMPLE))
        contract['scenes'][1]['params']['bars'][0]['value'] = 123456789
        contract['scenes'][1]['params']['valueWidth'] = 2
        code, summary, err = render(contract)
        self.assertEqual(code, 4, err)
        self.assertIn('123', json.dumps(summary['text_overflow'], ensure_ascii=False))


if __name__ == '__main__':
    unittest.main(verbosity=1)
