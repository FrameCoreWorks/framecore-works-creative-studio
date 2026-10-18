"""Reference breakdown (hyperframes-workflow/assets/reference-breakdown): cuts at their first frame, the cut grid and every output."""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/hyperframes-workflow/assets/reference-breakdown/breakdown.py'
spec = importlib.util.spec_from_file_location('breakdown', TOOL)
breakdown = importlib.util.module_from_spec(spec)
spec.loader.exec_module(breakdown)
np = breakdown.np


class Grid(unittest.TestCase):
    def test_cut_starts_are_the_first_frame_of_the_new_shot_and_debounced(self):
        diff = np.array([0, 0, 20, 30, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0], float)
        self.assertEqual(breakdown.cut_starts(diff, 5, 12), [3, 20])

    def test_a_regular_edit_fits_one_grid_and_reports_the_outlier(self):
        starts = [20, 40, 60, 71, 80, 100, 120]
        grid = breakdown.fit_grid(starts, 30)
        self.assertAlmostEqual(grid['step_frames'], 20, delta=0.05)
        self.assertEqual(grid['outlier_cut_index'], [3])
        self.assertAlmostEqual(grid['bpm_if_step_is_quarter'], 90, delta=0.3)
        self.assertIsNone(breakdown.fit_grid([10, 30, 50], 30))


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'needs FFmpeg')
class Video(unittest.TestCase):
    def test_a_synthetic_edit_is_broken_down(self):
        rng = np.random.default_rng(1)
        frames = []
        for _ in range(8):
            colour = rng.integers(0, 255, 3) // 2
            for f in range(20):
                image = np.zeros((108, 192, 3), np.uint8)
                image[:] = colour
                image[40:60, (f * 4) % 150:(f * 4) % 150 + 30] = 255
                frames.append(image)
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '192x108', '-r', '30', '-i', '-',
                            '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-crf', '12', str(tmp / 'v.mp4')], input=np.stack(frames).tobytes(), check=True)
            self.assertEqual(breakdown.main(['--video', str(tmp / 'v.mp4'), '--out', str(tmp / 'out')]), 0)
            report = json.loads((tmp / 'out/cuts.json').read_text())
            self.assertEqual(report['cuts_frames'], [20, 40, 60, 80, 100, 120, 140])
            self.assertAlmostEqual(report['grid']['step_frames'], 20, delta=0.05)
            self.assertEqual(len(report['segments_moving_area']), 8)
            self.assertTrue(all(0 < s['moving_area'] < 0.3 for s in report['segments_moving_area']))
            for name in ('sheet_0.jpg', 'keyframes.jpg', 'motion-heatmap.jpg', 'transitions/T07.jpg', 'ref/seg08.png'):
                self.assertTrue((tmp / 'out' / name).is_file(), name)
            self.assertEqual(breakdown.main(['--video', str(tmp / 'none.mp4'), '--out', str(tmp / 'x')]), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
