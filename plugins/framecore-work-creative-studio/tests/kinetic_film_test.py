"""Kinetic film beat sheets (hyperframes-workflow/assets/kinetic-film/beat_sheet.py)."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
KIT = PLUGIN / 'skills/hyperframes-workflow/assets/kinetic-film'
TOOL = KIT / 'beat_sheet.py'
spec = importlib.util.spec_from_file_location('beat_sheet', TOOL)
beat_sheet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beat_sheet)


def sheet(**overrides):
    base = {'id': 'test', 'bpm': 120, 'beats': 16, 'drop_beat': 8,
            'blocks': [{'start': 0, 'end': 8, 'job': 'charge'}, {'start': 8, 'end': 16, 'job': 'drop'}]}
    base.update(overrides)
    return base


class BeatSheetTest(unittest.TestCase):
    def test_every_bundled_template_is_valid(self):
        data = json.loads((KIT / 'beat-sheets.json').read_text())
        self.assertGreaterEqual(len(data['templates']), 4)
        for template in data['templates']:
            with self.subTest(template['id']):
                self.assertEqual(beat_sheet.check(template), [])

    def test_seconds_follow_the_tempo(self):
        plan = beat_sheet.timing(sheet())
        self.assertAlmostEqual(plan['beat_seconds'], 0.5)
        self.assertAlmostEqual(plan['duration'], 8.0)
        self.assertAlmostEqual(plan['blocks'][1]['start_s'], 4.0)
        faster = beat_sheet.timing(sheet(), bpm=240)
        self.assertAlmostEqual(faster['blocks'][1]['start_s'], 2.0)

    def test_gap_overlap_and_length_are_errors(self):
        gap = sheet(blocks=[{'start': 0, 'end': 6}, {'start': 8, 'end': 16}])
        self.assertTrue(any('gap' in e for e in beat_sheet.check(gap)))
        overlap = sheet(blocks=[{'start': 0, 'end': 10}, {'start': 8, 'end': 16}])
        self.assertTrue(any('overlap' in e for e in beat_sheet.check(overlap)))
        short = sheet(beats=20)
        self.assertTrue(any('ends at beat 16' in e for e in beat_sheet.check(short)))
        late = sheet(blocks=[{'start': 2, 'end': 16}], drop_beat=2)
        self.assertTrue(any('beat 0' in e for e in beat_sheet.check(late)))

    def test_drop_must_start_a_block(self):
        self.assertTrue(any('drop' in e for e in beat_sheet.check(sheet(drop_beat=5))))

    def test_music_offset_puts_the_drop_on_the_planned_beat(self):
        plan = beat_sheet.timing(sheet(), drop_seconds=10.0)
        self.assertAlmostEqual(plan['music_offset'], 6.0)
        self.assertEqual(plan['warnings'], [])
        early = beat_sheet.timing(sheet(), drop_seconds=3.0)
        self.assertTrue(any('earlier' in w for w in early['warnings']))

    def test_cli_prints_json_and_fails_on_errors(self):
        out = subprocess.run([sys.executable, '-I', str(TOOL), str(KIT / 'beat-sheets.json'), '--template', 'teaser-24s', '--json'],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        plan = json.loads(out.stdout)
        self.assertEqual(plan['id'], 'teaser-24s')
        self.assertAlmostEqual(plan['duration'], 68 * 60 / 172, places=3)
        with tempfile.TemporaryDirectory() as tmp:
            bad = pathlib.Path(tmp) / 'bad.json'
            bad.write_text(json.dumps(sheet(drop_beat=5)))
            out = subprocess.run([sys.executable, '-I', str(TOOL), str(bad)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 1)
            self.assertIn('drop', out.stdout + out.stderr)
        missing = subprocess.run([sys.executable, '-I', str(TOOL), str(KIT / 'beat-sheets.json'), '--template', 'nope'],
                                 capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)


if __name__ == '__main__':
    unittest.main()
