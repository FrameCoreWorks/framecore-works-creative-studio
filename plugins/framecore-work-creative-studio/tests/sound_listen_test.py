"""Sound listening tools (hyperframes-workflow/assets/sound-listen): listen.py measures and critiques, place_sfx.py lays samples on frames."""
import importlib.util
import json
import math
import os
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
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

    def test_the_earshot_bridge_uses_the_plugin_engine_offline_and_refuses_uploads(self):
        # One Earshot (owner request 2026-10-23): the bridge runs the earshot-audio engine with its own model cache,
        # offline and without API keys, and refuses llm and mcp as the plugin's launcher does.
        root = self.dir / 'earshot'
        exe = root / 'venv/bin/earshot'
        exe.parent.mkdir(parents=True)
        exe.write_text('#!/bin/sh\n')
        (root / 'cache').mkdir()
        calls = []
        real = self.listen.subprocess.call
        self.listen.subprocess.call = lambda cmd, env=None: calls.append((cmd, env)) or 0
        try:
            with mock.patch.dict(os.environ, {'EARSHOT_NATIVE_ROOT': str(root)}):
                self.assertEqual(self.listen.delegate('describe', ['a.wav'], str(exe)), 0)
            self.assertEqual(self.listen.delegate('llm', ['a.wav'], str(exe)), 2)
            self.assertEqual(self.listen.delegate('mcp', [], str(exe)), 2)
        finally:
            self.listen.subprocess.call = real
        self.assertEqual(len(calls), 1)
        cmd, env = calls[0]
        self.assertEqual(cmd, [str(exe), 'describe', 'a.wav'])
        self.assertEqual(env['EARSHOT_HOME'], str(root / 'cache'))
        self.assertEqual(env['EARSHOT_OFFLINE'], '1')
        self.assertNotIn('GEMINI_API_KEY', env)
        self.assertNotIn('llm', self.listen.EARSHOT_COMMANDS)
        self.assertIn('earshot-audio', open(KIT / 'listen.py', encoding='utf-8').read())

    def test_the_earshot_bridge_never_goes_online(self):
        # Review 2026-10-23: without a cache folder, or with an engine elsewhere, the bridge must still run offline
        # with the plugin's cache, and `doctor --fetch` (a model download) is refused as the launcher refuses it.
        exe = self.dir / 'elsewhere/bin/earshot'
        exe.parent.mkdir(parents=True)
        exe.write_text('#!/bin/sh\n')
        calls = []
        real = self.listen.subprocess.call
        self.listen.subprocess.call = lambda cmd, env=None: calls.append((cmd, env)) or 0
        try:
            self.assertEqual(self.listen.delegate('describe', ['a.wav'], str(exe)), 0)
            self.assertEqual(self.listen.delegate('doctor', ['--fetch'], str(exe)), 2)
        finally:
            self.listen.subprocess.call = real
        self.assertEqual(len(calls), 1)
        env = calls[0][1]
        self.assertEqual(env['EARSHOT_OFFLINE'], '1')
        self.assertTrue(env['EARSHOT_HOME'].endswith('.framecore-studio/extensions/earshot/cache'), env['EARSHOT_HOME'])

    def test_critique_reports_partial_without_earshot(self):
        p = self.dir / 'crit.wav'
        write_wav(p, clicks([0.5, 1.0, 1.5, 2.0], 3.0, amp=0.5))
        r = subprocess.run([sys.executable, str(KIT / 'listen.py'), 'critique', str(p)], capture_output=True, text=True)
        self.assertIn(r.returncode, (0, 1), r.stderr)
        self.assertIn('NOT MEASURED HERE', r.stdout)

    def test_mono_amplitude_peak_and_loudness_are_not_attenuated(self):
        p = self.dir / 'mono-reference.wav'
        write_wav(p, [0.5 * math.sin(2 * math.pi * 997 * k / SR) for k in range(SR * 5)])
        x = self.listen.decode(str(p))
        self.assertAlmostEqual(float(abs(x).max()), 0.5, delta=0.0001)
        self.assertAlmostEqual(self.listen.true_peak_dbtp(str(p)), -6.02, delta=0.1)
        # Mono energy must not be doubled merely to represent it with two columns.
        self.assertAlmostEqual(self.listen.integrated_lufs(self.listen.decode(str(p), weighted=True)), -9.03, delta=0.3)
        clipped = self.dir / 'mono-clipped.wav'
        write_wav(clipped, [max(-1, min(1, 3 * math.sin(2 * math.pi * 440 * k / SR))) for k in range(SR)])
        self.assertIn('clipping', [f['kind'] for f in self.listen.check_of(str(clipped))['findings']])

    def test_first_audio_stream_is_used_even_when_second_is_default(self):
        first, second = self.dir / 'first.wav', self.dir / 'second.wav'
        write_wav(first, [0.1 * math.sin(2 * math.pi * 997 * k / SR) for k in range(SR * 3)])
        write_wav(second, [0.8 * math.sin(2 * math.pi * 220 * k / SR) for k in range(SR * 3)])
        p = self.dir / 'two-audio-streams.mka'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(first), '-i', str(second),
                        '-map', '0:a:0', '-map', '1:a:0', '-c:a', 'pcm_s16le',
                        '-disposition:a:0', '0', '-disposition:a:1', 'default', str(p)], check=True, capture_output=True)
        self.assertAlmostEqual(float(abs(self.listen.decode(str(p))).max()), 0.1, delta=0.0001)
        self.assertAlmostEqual(self.listen.true_peak_dbtp(str(p)), -20.0, delta=0.1)
        self.assertAlmostEqual(self.listen.integrated_lufs(self.listen.decode(str(p), weighted=True)), -23.0, delta=0.3)
        m = self.listen.measure_of(self.listen.analyse(str(p)))
        self.assertEqual(m['audio_stream_index'], 0)
        self.assertEqual(m['audio_stream_count'], 2)
        self.assertEqual(m['source_channels'], 1)

    def test_tempo_grid_rounding_stays_inside_flux(self):
        flux = self.listen.np.zeros(1206)
        flux[::100] = 1.0
        bpm, beats = self.listen.tempo_of(flux)
        self.assertEqual(bpm, 120.0)
        self.assertTrue(beats)
        self.assertTrue(all(0 <= t < len(flux) * self.listen.HOP / SR for t in beats))

    def test_custom_profile_does_not_use_launch_loudness_or_labels(self):
        p = self.dir / 'quiet-reference.wav'
        write_wav(p, [0.01 * math.sin(2 * math.pi * 997 * k / SR) for k in range(SR * 5)])
        a = self.listen.analyse(str(p))
        m = self.listen.measure_of(a)
        ref = self.listen.ref_from_profile({'metrics': {'lufs_i': {'min': -44.0, 'median': -43.0, 'max': -42.0}}})
        c = self.listen.critique_of(a, m, None, ref)
        rows = {r['key']: r for r in c['rows']}
        self.assertEqual(rows['lufs_i']['status'], 'ok')
        self.assertEqual(rows['lra']['status'], 'n.a.')
        self.assertNotIn('launch', c['verdict'])
        self.assertEqual(c['tips'], [])
        high = dict(m, lufs_i=-30.0, true_peak=0.5)
        bad = self.listen.critique_of(a, high, None, ref)
        self.assertEqual(next(r for r in bad['rows'] if r['key'] == 'true_peak')['status'], 'high')
        actions = ' '.join(bad['actions'])
        self.assertIn('-43', actions)
        self.assertNotIn('-14 LUFS', actions)
        self.assertNotIn('launch', actions)

    def test_invalid_profiles_are_input_errors(self):
        invalid = [None, {}, {'metrics': {}}, {'metrics': {'unknown': {'min': 0, 'median': 1, 'max': 2}}},
                   {'metrics': {'lufs_i': {'min': -10, 'median': -20, 'max': 0}}},
                   {'metrics': {'lufs_i': {'min': -20, 'median': float('nan'), 'max': 0}}},
                   {'metrics': {'lufs_i': {'min': -20, 'median': -10, 'max': float('inf')}}},
                   {'metrics': {'lufs_i': {'min': -20, 'max': 0}}},
                   {'metrics': {'lufs_i': {'min': False, 'median': 1, 'max': 2}}}]
        for profile in invalid:
            with self.subTest(profile=profile), self.assertRaises(self.listen.InputError):
                self.listen.ref_from_profile(profile)
        with self.assertRaises(self.listen.InputError):
            self.listen.profile_of([])
        p = self.dir / 'invalid-profile.json'
        p.write_text(json.dumps({'metrics': {}}))
        wav = self.dir / 'profile-cli.wav'
        write_wav(wav, clicks([0.5], 1.0))
        result = subprocess.run([sys.executable, str(KIT / 'listen.py'), 'critique', str(wav), '--profile', str(p)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)


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
