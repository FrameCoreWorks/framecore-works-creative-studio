"""Iso Glow kit (hyperframes-workflow/assets/iso-glow) and the band envelope tool it is driven by (motion-sync/audio_envelope.py)."""
import importlib.util
import json
import math
import pathlib
import shutil
import struct
import subprocess
import tempfile
import unittest
import wave

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
SKILL = PLUGIN / 'skills/hyperframes-workflow'
KIT = SKILL / 'assets/iso-glow'
TOOL = SKILL / 'assets/motion-sync/audio_envelope.py'
spec = importlib.util.spec_from_file_location('audio_envelope', TOOL)
envtool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(envtool)


def kick_track(path, bpm=120, seconds=4.0, sr=22050):
    """A 60 Hz thump on every beat over a quiet 3 kHz tone: the bass band must see the beats, not the tone."""
    beat = 60 / bpm
    with wave.open(str(path), 'wb') as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(sr)
        frames = bytearray()
        for i in range(int(seconds * sr)):
            t = i / sr
            since = t % beat
            v = 0.8 * math.sin(2 * math.pi * 60 * t) * math.exp(-since * 9) + 0.2 * math.sin(2 * math.pi * 3000 * t)
            frames += struct.pack('<h', int(max(-1, min(1, v)) * 32000))
        out.writeframes(bytes(frames))


class Envelope(unittest.TestCase):
    def test_smoothing_rises_fast_and_falls_slowly(self):
        env = envtool.envelope([0.0] * 100 + [1.0] * 100 + [0.0] * 100, fps=1, sr=100)
        self.assertEqual(env, [0.0, 0.75, 0.615])   # one frame of silence only takes away the release share

    def test_hits_need_a_jump_and_a_gap(self):
        env = [0.1, 0.1, 0.9, 0.95, 0.4, 0.1, 0.1, 0.8, 0.85, 0.2]
        self.assertEqual(envtool.hits(env, fps=10, rise=0.3, gap=0.3), [0.1, 0.6])

    def test_band_parsing(self):
        self.assertEqual(envtool.band_of(':120'), (None, 120))
        self.assertEqual(envtool.band_of('2000:8000'), (2000, 8000))
        for bad in ('', ':', '120', '800:200'):
            with self.assertRaises(ValueError):
                envtool.band_of(bad)

    @unittest.skipUnless(shutil.which('ffmpeg'), 'needs FFmpeg')
    def test_a_kick_track_gives_one_hit_per_beat_and_injects_into_a_composition(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            kick_track(tmp / 'kick.wav')
            html = tmp / 'index.html'
            html.write_text('<script>\n      /* BEGIN ENVELOPE */\n      const ENVELOPE = null;\n      /* END ENVELOPE */\n</script>\n')
            code = envtool.main([str(tmp / 'kick.wav'), '--out', str(tmp / 'bass.json'), '--inject', str(html)])
            self.assertEqual(code, 0)
            data = json.loads((tmp / 'bass.json').read_text())
            self.assertEqual(len(data['env']), 120)
            self.assertEqual(len(data['kicks']), 8)
            for k, t in enumerate(data['kicks']):
                self.assertLess(abs(t - k * 0.5), 0.07)
            body = html.read_text()
            self.assertIn('const ENVELOPE = {"fps":30', body)
            self.assertNotIn('const ENVELOPE = null', body)
            self.assertEqual(body.count('/* END ENVELOPE */'), 1)
            self.assertEqual(envtool.main([str(tmp / 'missing.wav')]), 1)


class Kit(unittest.TestCase):
    def test_the_example_carries_an_identical_kit_and_the_envelope_markers(self):
        self.assertEqual((KIT / 'iso-kit.js').read_bytes(), (KIT / 'examples/bass-speaker/iso-kit.js').read_bytes())
        page = (KIT / 'examples/bass-speaker/index.html').read_text()
        for needle in ('<script src="iso-kit.js"></script>', '/* BEGIN ENVELOPE */', '/* END ENVELOPE */', "window.__timelines['main']",
                       'data-composition-id="main"', 'IsoKit.demoEnvelope'):
            self.assertIn(needle, page)
        self.assertNotIn('requestAnimationFrame(', page + (KIT / 'iso-kit.js').read_text())
        self.assertIn('Tolga Cohce', (KIT / 'LICENSE.upstream').read_text())

    @unittest.skipUnless(shutil.which('node'), 'needs Node.js')
    def test_the_kernel_projects_isometrically_and_the_demo_envelope_is_deterministic(self):
        script = (KIT / 'iso-kit.js').read_text() + '''
const K = IsoKit.frame(100, 200);
const out = { origin: K.P(0, 0, 0), x: K.D(1, 0, 0), y: K.D(0, 1, 0), z: K.D(0, 0, 1), front: K.FRONT(0, 10, 5),
  a: IsoKit.demoEnvelope(2, 30, 120, 0), b: IsoKit.demoEnvelope(2, 30, 120, 0) };
out.mid = IsoKit.envAt({ fps: 10, env: [0, 1] }, 0.05);
console.log(JSON.stringify(out));'''
        result = json.loads(subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True).stdout)
        self.assertEqual(result['origin'], [100, 200])
        self.assertAlmostEqual(result['x'][0], math.cos(math.pi / 6))
        self.assertAlmostEqual(result['x'][1], 0.5)
        self.assertAlmostEqual(result['y'][0], -math.cos(math.pi / 6))
        self.assertEqual(result['z'], [0, -1])
        self.assertTrue(result['front'].startswith('matrix('))
        self.assertEqual(result['a'], result['b'])
        self.assertEqual(len(result['a']['env']), 60)
        self.assertEqual(result['a']['kicks'], [0, 0.5, 1, 1.5])
        self.assertAlmostEqual(result['mid'], 0.5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
