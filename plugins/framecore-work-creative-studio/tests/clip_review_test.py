"""Clip review sheet (video-prompt-architect/scripts/clip_review.py): measured clips checked against the shot plan."""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/video-prompt-architect/scripts/clip_review.py'
READY = shutil.which('ffmpeg') and shutil.which('ffprobe') and importlib.util.find_spec('PIL')


def clip(folder, name, size, seconds, fps, audio=False):
    path = pathlib.Path(folder, name)
    command = ['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', f'testsrc2=size={size}:rate={fps}:duration={seconds}']
    if audio:
        command += ['-f', 'lavfi', '-i', f'sine=frequency=440:duration={seconds}', '-shortest']
    subprocess.run(command + ['-pix_fmt', 'yuv420p', str(path)], check=True)
    return path


@unittest.skipUnless(READY, 'ffmpeg, ffprobe and Pillow are needed')
class Review(unittest.TestCase):
    def test_clips_are_measured_and_checked_against_the_plan(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = pathlib.Path(temp, 'plan.json')
            plan.write_text(json.dumps({'shots': [{'id': 'S01', 'start_s': 0, 'end_s': 2}, {'id': 'S02', 'start_s': 2, 'end_s': 4}]}), encoding='utf-8')
            clips = [clip(temp, 'S01_take2.mp4', '360x640', 2, 30, audio=True), clip(temp, 'S02.mp4', '640x360', 1, 25), clip(temp, 'extra.mp4', '360x640', 1, 30)]
            done = subprocess.run([sys.executable, '-B', str(TOOL), *map(str, clips), '--plan', str(plan), '--aspect', '9:16', '--fps', '30', '--out-dir', str(pathlib.Path(temp, 'review'))],
                                  capture_output=True, text=True, timeout=300)
            self.assertEqual(done.returncode, 1, done.stderr)
            review = json.loads(pathlib.Path(temp, 'review', 'review.json').read_text(encoding='utf-8'))
            first, second, third = review['clips']
            self.assertTrue(review['temporal'].startswith('UNVERIFIED'))
            self.assertEqual((first['shot'], first['findings']), ('S01', []))
            self.assertEqual((first['measured']['frames'], first['measured']['fps'], first['measured']['audio']), (60, 30.0, True))
            self.assertEqual(second['shot'], 'S02')
            self.assertEqual(second['findings'], ['shorter than its shot: 1.0 s for 2 s', 'frame 640 x 360 is not 9:16', '25.0 fps, not 30'])
            self.assertEqual(third['findings'], ['no shot ID from the plan in its file name'])
            from PIL import Image
            with Image.open(pathlib.Path(temp, 'review', 'contact-sheet.png')) as sheet:
                self.assertEqual(sheet.height, 3 * (240 + 28) + 14)

    def test_a_short_shot_id_never_claims_a_longer_one(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = pathlib.Path(temp, 'plan.json')
            plan.write_text(json.dumps({'shots': [{'id': 'S1', 'start_s': 0, 'end_s': 1}, {'id': 'S10', 'start_s': 1, 'end_s': 2}]}), encoding='utf-8')
            clips = [clip(temp, 'S10.mp4', '360x640', 1, 30), clip(temp, 'spot_S1_v2.mp4', '360x640', 1, 30)]
            subprocess.run([sys.executable, '-B', str(TOOL), *map(str, clips), '--plan', str(plan), '--out-dir', str(pathlib.Path(temp, 'review'))],
                           capture_output=True, text=True, timeout=300)
            review = json.loads(pathlib.Path(temp, 'review', 'review.json').read_text(encoding='utf-8'))
            self.assertEqual(sorted(c['shot'] for c in review['clips']), ['S1', 'S10'])

    def test_without_a_plan_clips_are_only_measured(self):
        with tempfile.TemporaryDirectory() as temp:
            path = clip(temp, 'a.mp4', '320x320', 1, 24)
            done = subprocess.run([sys.executable, '-B', str(TOOL), str(path), '--out-dir', str(pathlib.Path(temp, 'r'))], capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 0, done.stderr)
            again = subprocess.run([sys.executable, '-B', str(TOOL), str(path), '--out-dir', str(pathlib.Path(temp, 'r'))], capture_output=True, text=True, timeout=120)
            self.assertEqual(again.returncode, 2)
            self.assertIn('output folder exists', again.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=1)
