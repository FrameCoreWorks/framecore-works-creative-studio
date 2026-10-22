"""Flash check (hyperframes-workflow/assets/motion-quality/flash_check.py): photosensitivity screening of a rendered video."""
import contextlib
import importlib.util
import io
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import numpy as np

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/hyperframes-workflow/assets/motion-quality/flash_check.py'
spec = importlib.util.spec_from_file_location('flash_check', TOOL)
flash = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flash)

WIDTH, HEIGHT, FPS = 64, 114, 30


def encode(path, frames):
    """Encode a list of grey uint8 frames (HEIGHT x WIDTH) losslessly enough for luminance checks."""
    data = np.stack(frames).astype(np.uint8).tobytes()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{WIDTH}x{HEIGHT}', '-r', str(FPS),
                    '-i', '-', '-c:v', 'libx264', '-qp', '0', '-pix_fmt', 'yuv444p', path], input=data, check=True)
    return path


def toggle(seconds, every, low=0, high=255, area=None):
    frames = []
    for index in range(seconds * FPS):
        frame = np.full((HEIGHT, WIDTH), low, np.uint8)
        if (index // every) % 2:
            if area is None:
                frame[:] = high
            else:
                frame[: int(HEIGHT * area), :] = high
        frames.append(frame)
    return frames


def report_for(path):
    return flash.measure(flash.samples(path))


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg is needed')
class FlashCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = pathlib.Path(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def video(self, name, frames):
        return encode(str(self.root / name), frames)

    def test_fast_full_frame_flicker_is_flagged(self):
        path = self.video('fast.mp4', toggle(3, 3))
        report = report_for(path)
        self.assertGreaterEqual(report['max_flashes_per_second'], 4)
        self.assertTrue(flash.verdict(report))
        self.assertEqual(flash.main([path]), 1)

    def test_slow_alternation_passes(self):
        path = self.video('slow.mp4', toggle(3, 15))
        self.assertLessEqual(report_for(path)['max_flashes_per_second'], 1)
        self.assertEqual(flash.main([path]), 0)

    def test_slow_fade_counts_as_one_change_each_way(self):
        up = [np.full((HEIGHT, WIDTH), round(255 * i / (FPS - 1)), np.uint8) for i in range(FPS)]
        path = self.video('fade.mp4', up + up[::-1])
        self.assertLessEqual(report_for(path)['max_flashes_per_second'], 1)

    def test_small_area_flicker_passes(self):
        path = self.video('small.mp4', toggle(3, 3, area=0.10))
        self.assertEqual(report_for(path)['max_flashes_per_second'], 0)

    def test_bright_only_flicker_passes(self):
        path = self.video('bright.mp4', toggle(3, 3, low=235, high=255))
        self.assertEqual(report_for(path)['max_flashes_per_second'], 0)

    def test_report_is_labelled_screening_and_bound_to_file(self):
        path = self.video('label.mp4', toggle(2, 15))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            flash.main([path, '--json'])
        report = json.loads(out.getvalue())
        self.assertIn('not WCAG', report['screening'])
        self.assertRegex(report['video_sha256'], r'^[0-9a-f]{64}$')

    def test_short_and_unreadable_inputs(self):
        short = self.video('short.mp4', toggle(1, 3)[:15])
        self.assertIn(flash.main([short]), (0, 1))
        text = self.root / 'notes.txt'
        text.write_text('not a video')
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(flash.main([str(text)]), 2)
            with self.assertRaises(SystemExit):
                flash.main([short, '--fps', '60'])


if __name__ == '__main__':
    unittest.main()
