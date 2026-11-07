"""Editor-craft additions to FrameCut: transition styles, audio micro-fades at hard cuts, a silence cut plan and a beat grid."""
import array
import copy
import math
import shutil
import sys
import tempfile
import unittest
import wave
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / 'skills/opencut-video-studio/assets/framecut'
sys.path.insert(0, str(RUNTIME))
from fc_core import FrameCutError, apply_operations, validate  # noqa: E402
from fc_media import ffmpeg, ingest  # noqa: E402
from fc_render import render  # noqa: E402
from fc_board import preview_frame  # noqa: E402
from fc_editor import beat_grid, plan_silence_cuts  # noqa: E402
from framecut import project_init  # noqa: E402


def synthetic():
    return {'schema_version': 1, 'id': 'test', 'revision': 1, 'assets': {'a': {'path': 'a.mp4', 'sha256': 'a' * 64, 'kind': 'video',
            'probe': {'time_base': '1/1000', 'clock': {'num': 1, 'den': 1000}, 'start_pts': 0, 'duration': 20, 'has_audio': True}}},
            'analyses': {}, 'sequences': [{'id': 'main', 'fps': {'num': 30, 'den': 1}, 'duration': 300, 'clips': [
                {'id': 'take', 'asset': 'a', 'start': 0, 'duration': 300, 'source_in': 0}]}],
            'deliverables': [{'id': 'wide', 'sequence': 'main', 'width': 160, 'height': 90}], 'locks': []}


class Contracts(unittest.TestCase):
    def two_clips(self, style):
        p = synthetic()
        p['sequences'][0]['duration'] = 105
        p['sequences'][0]['clips'] = [{'id': 'one', 'asset': 'a', 'start': 0, 'duration': 60, 'source_in': 0},
                                      {'id': 'two', 'asset': 'a', 'start': 45, 'duration': 60, 'source_in': 5000,
                                       'transition': 15, 'transition_style': style}]
        return p

    def test_transition_style_needs_a_transition_and_a_known_name(self):
        validate(self.two_clips('wipe_left'))
        with self.assertRaises(FrameCutError):
            validate(self.two_clips('star_wipe'))
        p = synthetic()
        p['sequences'][0]['clips'][0]['transition_style'] = 'dip_black'
        with self.assertRaises(FrameCutError):
            validate(p)

    def test_silence_plan_pads_speech_and_ripples_from_the_end(self):
        p = synthetic()
        # A trailing silence that runs to the clip end is cut whole: no next word needs a pre pad.
        silences = [{'start': 2.0, 'end': 4.0}, {'start': 6.0, 'end': 6.2}, {'start': 8.0, 'end': 10.0}]
        plan = plan_silence_cuts(p, 'main', silences, pre_pad=3, post_pad=6, min_cut=6)
        cuts = plan['cuts']
        self.assertEqual([(c['start'], c['end']) for c in cuts], [(246, 300), (66, 117)])
        self.assertEqual(plan['skipped'][0]['reason'], 'shorter_than_min_cut')
        result, _ = apply_operations(p, plan['operations'])
        seq = result['sequences'][0]
        self.assertEqual(seq['duration'], 195)
        self.assertEqual(sum(c['duration'] for c in seq['clips']), 195)
        self.assertEqual([c['start'] for c in seq['clips']], [0, 66])
        self.assertEqual(plan['removed_frames'], 105)
        self.assertEqual(p['sequences'][0]['duration'], 300)

    def test_silence_plan_never_cuts_a_timed_word(self):
        p = synthetic()
        p['analyses']['a'] = {'words': [{'text': 'tak', 'start': 3.0, 'end': 3.3}]}
        plan = plan_silence_cuts(p, 'main', [{'start': 2.0, 'end': 4.0}], pre_pad=3, post_pad=6, min_cut=6)
        self.assertEqual(plan['cuts'], [])
        self.assertEqual(plan['skipped'][0]['reason'], 'overlaps_timed_word')


def click_track(path, bpm, seconds=12, rate=22050, offset=0.25):
    period = 60 / bpm
    samples = array.array('h', [0]) * int(seconds * rate)
    t = offset
    while t < seconds - 0.05:
        start = int(t * rate)
        for i in range(int(0.03 * rate)):
            samples[start + i] = int(20000 * math.exp(-i / (0.004 * rate)) * math.sin(2 * math.pi * 1500 * i / rate))
        t += period
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(samples.tobytes())


class Media(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory()
        cls.source = Path(cls.shared.name) / 'source.mp4'
        ffmpeg(['-f', 'lavfi', '-i', 'testsrc2=s=160x90:r=30:d=5', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=5',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(cls.source)])

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copy2(self.source, self.root / 'source.mp4')
        self.p = project_init(self.root / 'project.json', 'test')
        self.p['assets']['a'] = ingest(self.root, 'source.mp4', 'a')
        self.p['deliverables'] = [{'id': 'wide', 'sequence': 'main', 'width': 160, 'height': 90}]
        self.p['authorization'] = 'Synthetic local regression render'

    def tearDown(self):
        self.tmp.cleanup()

    def styled(self, style):
        self.p['sequences'] = [{'id': 'main', 'fps': {'num': 30, 'den': 1}, 'duration': 45, 'clips': [
            {'id': 'clip', 'asset': 'a', 'start': 0, 'duration': 30, 'source_in': 0},
            {'id': 'next', 'asset': 'a', 'start': 15, 'duration': 30, 'source_in': 61440, 'transition': 15, 'transition_style': style}]}]

    def test_wipe_and_slide_previews_match_the_render(self):
        from PIL import Image, ImageChops, ImageStat
        for style in ('wipe_left', 'slide_up'):
            self.styled(style)
            render(self.p, self.root, 'wide', style)
            preview_frame(self.p, self.root, 'wide', 21, style + '.png')
            ffmpeg(['-i', str(self.root / style / 'video.mp4'), '-vf', "select='eq(n,21)'", '-frames:v', '1', str(self.root / (style + '-decoded.png'))])
            with Image.open(self.root / (style + '.png')) as a, Image.open(self.root / (style + '-decoded.png')) as b:
                difference = ImageStat.Stat(ImageChops.difference(a.convert('L'), b.convert('L'))).mean[0]
            self.assertLess(difference, 8, style)

    def test_dip_to_black_reaches_black_mid_transition(self):
        from PIL import Image, ImageStat
        self.styled('dip_black')
        render(self.p, self.root, 'wide', 'dip')
        ffmpeg(['-i', str(self.root / 'dip/video.mp4'), '-vf', "select='eq(n,22)'", '-frames:v', '1', str(self.root / 'mid.png')])
        preview_frame(self.p, self.root, 'wide', 22, 'mid-preview.png')
        for name in ('mid.png', 'mid-preview.png'):
            with Image.open(self.root / name) as image:
                self.assertLess(ImageStat.Stat(image.convert('L')).mean[0], 40, name)

    def test_hard_cut_gets_an_audio_micro_fade(self):
        self.p['sequences'] = [{'id': 'main', 'fps': {'num': 30, 'den': 1}, 'duration': 60, 'clips': [
            {'id': 'one', 'asset': 'a', 'start': 0, 'duration': 30, 'source_in': 0},
            {'id': 'two', 'asset': 'a', 'start': 30, 'duration': 30, 'source_in': 40960}]}]
        render(self.p, self.root, 'wide', 'cut')
        ffmpeg(['-i', str(self.root / 'cut/video.mp4'), '-vn', '-ac', '1', '-ar', '48000', '-f', 's16le', str(self.root / 'audio.pcm')])
        samples = array.array('h', (self.root / 'audio.pcm').read_bytes())
        rms = lambda values: math.sqrt(sum(v * v for v in values) / len(values))
        cut = 48000
        self.assertLess(rms(samples[cut - 48:cut + 48]), rms(samples[cut - 4800:cut - 2400]) * 0.6)

    def test_beat_grid_finds_tempo_and_phase(self):
        for bpm in (120, 96):
            path = self.root / f'click{bpm}.wav'
            click_track(path, bpm)
            grid = beat_grid(path, fps=30)
            self.assertAlmostEqual(grid['bpm'], bpm, delta=1.5)
            period = 60 / bpm
            for beat in grid['beats'][2:-2]:
                phase = (beat - 0.25) / period
                self.assertLess(abs(phase - round(phase)) * period, 0.03, (bpm, beat))
            self.assertEqual(grid['beat_frames'][3], round(grid['beats'][3] * 30))
            self.assertGreater(grid['confidence'], 0.6)

    def test_beat_grid_flags_music_without_a_pulse(self):
        ffmpeg(['-f', 'lavfi', '-i', 'sine=frequency=440:duration=8', str(self.root / 'tone.wav')])
        grid = beat_grid(self.root / 'tone.wav')
        self.assertLess(grid['confidence'], 0.3)
        self.assertTrue(grid['warnings'][0].startswith('low_confidence'))


if __name__ == '__main__':
    unittest.main()
