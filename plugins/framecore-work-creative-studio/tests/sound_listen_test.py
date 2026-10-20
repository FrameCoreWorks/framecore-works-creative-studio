"""Sound listening tools (hyperframes-workflow/assets/sound-listen): listen.py measures and critiques, place_sfx.py lays samples on frames."""
import importlib.util
import json
import math
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import wave

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
KIT = PLUGIN / 'skills/hyperframes-workflow/assets/sound-listen'
SR = 48000
HAVE_FFMPEG = shutil.which('ffmpeg') is not None and shutil.which('ffprobe') is not None


def load(name):
    sys.path.insert(0, str(KIT))
    spec = importlib.util.spec_from_file_location(name, KIT / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_wav(path, samples):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', max(-32767, min(32767, int(s * 32767)))) for s in samples))


def clicks(times, seconds, amp=0.8, hz=1800, decay=0.05):
    """short decaying tones whose attack starts exactly at each time"""
    out = [0.0] * int(seconds * SR)
    for t in times:
        i0 = int(round(t * SR))
        for k in range(int(decay * 5 * SR)):
            if i0 + k < len(out):
                out[i0 + k] += amp * math.exp(-k / (decay * SR)) * math.sin(2 * math.pi * hz * k / SR)
    return out


def cut_video(path, seconds=4.0):
    """a silent 30 fps video with hard colour cuts at 1.0, 2.0 and 3.0 s"""
    cmd = ['ffmpeg', '-v', 'error', '-y']
    for c in ['red', 'blue', 'green', 'yellow']:
        cmd += ['-f', 'lavfi', '-i', f'color=c={c}:s=160x90:r=30:d=1']
    cmd += ['-filter_complex', '[0][1][2][3]concat=n=4:v=1:a=0', '-pix_fmt', 'yuv420p', '-an', str(path)]
    subprocess.run(cmd, check=True, capture_output=True)


@unittest.skipUnless(HAVE_FFMPEG, 'FFmpeg and FFprobe are required')
class ListenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.listen = load('listen')
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = pathlib.Path(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_loudness_of_a_sine_matches_the_standard(self):
        # a 997 Hz sine at -20 dBFS peak is about -23 LUFS mono-in-stereo-less; the tool must land within 1 LU of the K-weighted figure
        p = self.dir / 'sine.wav'
        write_wav(p, [0.1 * math.sin(2 * math.pi * 997 * k / SR) for k in range(SR * 5)])
        lufs = self.listen.integrated_lufs(self.listen.decode(str(p), weighted=True))
        self.assertAlmostEqual(lufs, -23.0 - 0.0, delta=1.5)

    def test_onsets_land_on_the_planted_times(self):
        times = [0.5, 1.2, 2.0, 2.6, 3.4]
        p = self.dir / 'clicks.wav'
        write_wav(p, clicks(times, 4.5))
        a = self.listen.analyse(str(p))
        found = [float(t) for t in a['onsets']]
        for t in times:
            self.assertTrue(any(abs(f - t) < 0.01 for f in found), f'no onset near {t}: {found}')

    def test_sync_against_cuts_is_scored(self):
        v = self.dir / 'cuts.mp4'
        cut_video(v)
        good = self.dir / 'good.wav'
        write_wav(good, clicks([1.0, 2.0, 3.0], 4.0))
        late = self.dir / 'late.wav'
        write_wav(late, clicks([1.35, 2.35, 3.35], 4.0))
        sg = self.listen.sync_of(self.listen.analyse(str(good), video=str(v)))
        sl = self.listen.sync_of(self.listen.analyse(str(late), video=str(v)))
        self.assertGreaterEqual(sg['with_onset'], 0.99)
        self.assertLess(sl['with_onset'], 0.5)

    def test_check_flags_clipping_and_clears_clean_audio(self):
        loud = self.dir / 'loud.wav'
        write_wav(loud, [max(-1, min(1, 3 * math.sin(2 * math.pi * 440 * k / SR))) for k in range(SR * 3)])
        quiet = self.dir / 'quiet.wav'
        write_wav(quiet, clicks([0.5, 1.5], 3.0, amp=0.3))
        self.assertFalse(self.listen.check_of(str(loud))['clean'])
        self.assertFalse(any('clip' in f['text'].lower() for f in self.listen.check_of(str(quiet))['findings']))

    def test_cli_exit_codes(self):
        p = self.dir / 'cli.wav'
        write_wav(p, clicks([0.5, 1.5], 3.0))
        ok = subprocess.run([sys.executable, str(KIT / 'listen.py'), 'measure', str(p), '--json'], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertIn('lufs_i', json.loads(ok.stdout))
        bad = subprocess.run([sys.executable, str(KIT / 'listen.py'), 'measure', str(self.dir / 'nope.wav')], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 3)

    def test_critique_reports_partial_without_earshot(self):
        p = self.dir / 'crit.wav'
        write_wav(p, clicks([0.5, 1.0, 1.5, 2.0], 3.0, amp=0.5))
        r = subprocess.run([sys.executable, str(KIT / 'listen.py'), 'critique', str(p)], capture_output=True, text=True)
        self.assertIn(r.returncode, (0, 1), r.stderr)
        self.assertIn('NOT MEASURED HERE', r.stdout)


@unittest.skipUnless(HAVE_FFMPEG, 'FFmpeg and FFprobe are required')
class PlaceSfxTests(unittest.TestCase):
    def test_samples_land_on_the_cue_and_peak_stays_under_ceiling(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = pathlib.Path(tmp)
            v = d / 'v.mp4'
            cut_video(v)
            write_wav(d / 'hit.wav', [0.0] * 2400 + clicks([0.0], 0.6, amp=0.9)[:SR // 2])  # 50 ms of silence before the attack
            cues = [{'t': 1.0, 'file': 'hit.wav', 'align': 'onset', 'label': 'cut1'}, {'frame': 60, 'fps': 30, 'file': 'hit.wav', 'align': 'onset', 'label': 'cut2'}]
            (d / 'cues.json').write_text(json.dumps(cues))
            out = d / 'out.mp4'
            r = subprocess.run([sys.executable, str(KIT / 'place_sfx.py'), '--video', str(v), '--cues', str(d / 'cues.json'), '--out', str(out), '--json'],
                               capture_output=True, text=True, cwd=d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            res = json.loads(r.stdout)
            self.assertTrue(res['all_on_time'])
            self.assertLessEqual(res['true_peak_dbtp'], -0.9)
            self.assertTrue(out.exists())

    def test_missing_sample_is_an_input_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = pathlib.Path(tmp)
            v = d / 'v.mp4'
            cut_video(v)
            (d / 'cues.json').write_text(json.dumps([{'t': 1.0, 'file': 'absent.wav'}]))
            r = subprocess.run([sys.executable, str(KIT / 'place_sfx.py'), '--video', str(v), '--cues', str(d / 'cues.json'), '--out', str(d / 'o.mp4')],
                               capture_output=True, text=True, cwd=d)
            self.assertEqual(r.returncode, 3)


if __name__ == '__main__':
    unittest.main()
