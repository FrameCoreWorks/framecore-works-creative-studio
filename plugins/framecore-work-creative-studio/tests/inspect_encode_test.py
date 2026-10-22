"""Encode inspection (hyperframes-workflow/assets/motion-quality/inspect-encode.py): audio presence and cover-frame checks."""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/hyperframes-workflow/assets/motion-quality/inspect-encode.py'
spec = importlib.util.spec_from_file_location('inspect_encode', TOOL)
inspect_encode = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inspect_encode)


def encode(path, audio=None, seconds=2):
    args = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'testsrc2=size=160x90:rate=25:duration={seconds}']
    if audio:
        args += ['-f', 'lavfi', '-i', f'{audio}:duration={seconds}' if audio.startswith('sine') else f'{audio}', '-t', str(seconds), '-shortest']
    args += ['-pix_fmt', 'yuv420p', path]
    subprocess.run(args, check=True)
    return path


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'ffmpeg and ffprobe are needed')
class InspectEncodeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(cls.tmp.name)
        cls.root = root
        cls.mute = encode(str(root / 'mute.mp4'))
        cls.tone = encode(str(root / 'tone.mp4'), 'sine=frequency=440')
        cls.silence = encode(str(root / 'silence.mp4'), 'anullsrc=r=48000:cl=stereo')

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def out(self, name):
        return self.root / name

    def evidence(self, folder):
        return json.loads((folder / 'evidence.json').read_text())

    def test_required_audio_passes_with_tone_and_fails_without_stream(self):
        self.assertEqual(inspect_encode.inspect(self.tone, self.out('req-tone'), audio='required')['failed_checks'], [])
        self.assertEqual(self.evidence(self.out('req-tone'))['audio_check']['result'], 'PASS')
        result = inspect_encode.inspect(self.mute, self.out('req-mute'), audio='required')
        self.assertEqual(result['failed_checks'], ['audio'])
        check = self.evidence(self.out('req-mute'))['audio_check']
        self.assertEqual((check['streams'], check['result']), (0, 'FAIL'))

    def test_silent_passes_for_no_stream_and_for_digital_silence_and_fails_for_tone(self):
        self.assertEqual(inspect_encode.inspect(self.mute, self.out('sil-mute'), audio='silent')['failed_checks'], [])
        self.assertEqual(inspect_encode.inspect(self.silence, self.out('sil-zero'), audio='silent')['failed_checks'], [])
        self.assertEqual(inspect_encode.inspect(self.tone, self.out('sil-tone'), audio='silent')['failed_checks'], ['audio'])

    def test_cover_time_writes_frame_and_records_it(self):
        inspect_encode.inspect(self.mute, self.out('cover'), cover_time=1.2)
        self.assertTrue((self.out('cover') / 'cover.png').is_file())
        self.assertEqual(self.evidence(self.out('cover'))['cover'], {'time': 1.2, 'file': 'cover.png', 'result': 'PASS'})

    def test_cover_time_outside_film_is_rejected_before_destination_exists(self):
        for name, time in (('cover-end', 2.0), ('cover-negative', -1)):
            with self.assertRaises(ValueError):
                inspect_encode.inspect(self.mute, self.out(name), cover_time=time)
            self.assertFalse(self.out(name).exists())

    def test_cover_near_the_end_is_written_or_fails_never_claimed(self):
        result = inspect_encode.inspect(self.mute, self.out('cover-near-end'), cover_time=1.99)
        written = (self.out('cover-near-end') / 'cover.png').is_file()
        self.assertTrue(written or 'cover' in result['failed_checks'])
        self.assertEqual(self.evidence(self.out('cover-near-end'))['cover']['result'], 'PASS' if written else 'FAIL')

    def test_cover_time_is_checked_against_the_video_not_longer_audio(self):
        longer = str(self.root / 'longer-audio.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=size=160x90:rate=25:duration=2',
                        '-f', 'lavfi', '-i', 'sine=frequency=440:duration=3', '-pix_fmt', 'yuv420p', longer], check=True)
        with self.assertRaises(ValueError):
            inspect_encode.inspect(longer, self.out('cover-past-video'), cover_time=2.5)
        self.assertFalse(self.out('cover-past-video').exists())

    def test_cli_exit_code_is_1_when_a_check_fails(self):
        run = subprocess.run([sys.executable, str(TOOL), self.mute, str(self.out('cli')), '--audio', 'required'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertTrue((self.out('cli') / 'evidence.json').is_file())

    def test_default_run_is_unchanged(self):
        result = inspect_encode.inspect(self.tone, self.out('plain'))
        self.assertEqual(result['failed_checks'], [])
        evidence = self.evidence(self.out('plain'))
        self.assertNotIn('audio_check', evidence)
        self.assertNotIn('cover', evidence)


if __name__ == '__main__':
    unittest.main()
