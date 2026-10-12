"""Motion activity (hyperframes-workflow/assets/motion-quality/motion_activity.py): still time in a rendered video."""
import importlib.util
import pathlib
import shutil
import subprocess
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/hyperframes-workflow/assets/motion-quality/motion_activity.py'
spec = importlib.util.spec_from_file_location('motion_activity', TOOL)
activity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(activity)


def encode(path, source, seconds):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f"{source}{':' if '=' in source else '='}size=360x640:rate=30:duration={seconds}",
                    '-pix_fmt', 'yuv420p', path], check=True)


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg is needed')
class MotionActivityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(cls.tmp.name)
        cls.moving = str(root / 'moving.mp4')
        cls.still = str(root / 'still.mp4')
        cls.mixed = str(root / 'mixed.mp4')
        encode(cls.moving, 'testsrc2', 4)
        encode(cls.still, 'color=c=0x223344', 4)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cls.moving, '-i', cls.still, '-filter_complex',
                        '[0:v][1:v]concat=n=2:v=1[v]', '-map', '[v]', '-pix_fmt', 'yuv420p', cls.mixed], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_moving_video_passes(self):
        report = activity.measure(activity.samples(self.moving))
        self.assertLess(report['still_share'], 0.1)
        self.assertEqual(activity.verdict(report), [])

    def test_still_video_fails_on_share_and_length(self):
        report = activity.measure(activity.samples(self.still))
        self.assertGreater(report['still_share'], 0.9)
        problems = activity.verdict(report)
        self.assertEqual(len(problems), 2)

    def test_still_tail_is_found_and_a_declared_hold_excuses_it(self):
        report = activity.measure(activity.samples(self.mixed))
        self.assertGreaterEqual(report['longest_still_seconds'], 3.5)
        self.assertGreaterEqual(report['longest_still_ends_at'], 7.5)
        self.assertTrue(activity.verdict(report))
        held = activity.measure(activity.samples(self.mixed), holds=[(4.0, 8.0)])
        self.assertEqual(activity.verdict(held), [])

    def test_cli_exit_codes(self):
        self.assertEqual(activity.main([self.moving]), 0)
        self.assertEqual(activity.main([self.still, '--json']), 1)


if __name__ == '__main__':
    unittest.main()
