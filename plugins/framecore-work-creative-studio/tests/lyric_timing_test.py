"""Lyric timing (hyperframes-workflow/assets/motion-sync/lyric_timing.py): alignment, interpolation, beats, snapping, exports."""
import importlib.util
import json
import math
import pathlib
import shutil
import struct
import tempfile
import unittest
import wave

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/hyperframes-workflow/assets/motion-sync/lyric_timing.py'
spec = importlib.util.spec_from_file_location('lyric_timing', TOOL)
lt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lt)

LYRICS = "[Zwrotka]\nJo jo, nie nastukałem\nV to dobry chłopak\n\nNa winylu grubić"


def heard():
    # the recogniser mishears and drops words; times in seconds
    return [{'text': 'jo', 'start': 1.00, 'end': 1.20}, {'text': 'jo', 'start': 1.25, 'end': 1.45},
            {'text': 'nie', 'start': 1.60, 'end': 1.75}, {'text': 'nastukalem', 'start': 1.80, 'end': 2.40},
            {'text': 'we', 'start': 3.00, 'end': 3.10}, {'text': 'to', 'start': 3.15, 'end': 3.25},
            {'text': 'chlopak', 'start': 3.60, 'end': 4.10},
            {'text': 'na', 'start': 5.00, 'end': 5.10}, {'text': 'winylu', 'start': 5.15, 'end': 5.60}, {'text': 'grubic', 'start': 5.70, 'end': 6.20}]


class LyricTimingTest(unittest.TestCase):
    def test_lyrics_keep_their_spelling_and_get_times(self):
        lines = lt.read_lyrics(LYRICS)
        self.assertEqual([l['text'] for l in lines], ['Jo jo, nie nastukałem', 'V to dobry chłopak', 'Na winylu grubić'])
        share = lt.place(lines, heard())
        words = {w['text']: w for l in lines for w in l['words']}
        self.assertTrue(words['nastukałem']['matched'])
        self.assertAlmostEqual(words['nastukałem']['start'], 1.80)
        self.assertTrue(words['chłopak']['matched'])
        self.assertFalse(words['dobry']['matched'])           # never heard: interpolated between its neighbours
        self.assertGreaterEqual(words['dobry']['start'], 3.25)
        self.assertLessEqual(words['dobry']['end'], 3.60 + 1e-6)
        self.assertGreater(share, 0.75)
        self.assertEqual(lines[2]['start'], 5.00)

    def test_snapping_moves_close_cuts_to_half_beats_only(self):
        lines = lt.read_lyrics(LYRICS)
        lt.place(lines, heard())
        lt.snap(lines, bpm=120, beat0=0.0, snap_ms=80, lead_frames=1, fps=30)   # half-beat every 0.25 s
        first = lines[0]
        self.assertTrue(first['cut_on_beat'])                  # 1.00 minus one frame lies 33 ms from the half-beat at 1.00
        self.assertLessEqual(first['cut'], first['start'])
        for line in lines:
            self.assertLessEqual(line['cut'], line['start'])
            self.assertEqual(line['cut_frame'], round(line['cut'] * 30))

    def test_exports(self):
        lines = lt.read_lyrics(LYRICS)
        lt.place(lines, heard())
        lrc = lt.to_lrc(lines)
        self.assertTrue(lrc.startswith('[00:01.00]Jo jo, nie nastukałem'))
        self.assertIn('<00:01.80>nastukałem', lt.to_lrc(lines, words=True))
        srt = lt.to_srt(lines)
        self.assertIn('00:00:01,000 --> 00:00:02,400\nJo jo, nie nastukałem', srt)

    def test_a_line_sung_from_zero_never_cuts_before_zero(self):
        for beat0 in (0.1, 0.2):                               # unsnapped and snapped cases both went negative in 1.71.0
            lines = lt.read_lyrics('Start now')
            lt.place(lines, [{'text': 'start', 'start': 0.0, 'end': 0.3}, {'text': 'now', 'start': 0.35, 'end': 0.6}])
            lt.snap(lines, bpm=120, beat0=beat0)
            self.assertGreaterEqual(lines[0]['cut'], 0.0)
            self.assertGreaterEqual(lines[0]['cut_frame'], 0)

    def test_overlapping_neighbours_never_invert_a_word(self):
        lines = lt.read_lyrics('aa bb cc')                     # the recogniser ends "aa" after "cc" starts
        lt.place(lines, [{'text': 'aa', 'start': 1.0, 'end': 1.6}, {'text': 'cc', 'start': 1.5, 'end': 2.0}])
        for w in lines[0]['words']:
            self.assertLessEqual(w['start'], w['end'])
        self.assertTrue(lines[0]['needs_check'])
        self.assertNotIn('squeezed', lines[0]['words'][1])

    def test_ntsc_frame_rate_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / 'lyrics.txt').write_text(LYRICS, encoding='utf-8')
            (root / 'words.json').write_text(json.dumps(heard()), encoding='utf-8')
            lt.main([str(root / 'song.wav'), str(root / 'lyrics.txt'), '--words', str(root / 'words.json'),
                     '--bpm', '120', '--fps', '30000/1001', '--out', str(root / 'out.json')])
            report = json.loads((root / 'out.json').read_text(encoding='utf-8'))
            self.assertEqual(report['fps'], '30000/1001')
            for line in report['lines']:
                self.assertEqual(line['cut_frame'], round(line['cut'] * 30000 / 1001))

    def test_no_match_is_an_error(self):
        with self.assertRaises(ValueError):
            lt.place(lt.read_lyrics('zupełnie inne słowa'), [{'text': 'xyz', 'start': 0, 'end': 1}])

    @unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg is needed for the beat finder')
    def test_cli_with_supplied_words_and_detected_beats(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            rate, bpm, seconds = 22050, 120, 8
            frames = bytearray()
            for n in range(rate * seconds):                 # a click on every beat
                t = (n / rate) % (60 / bpm)
                v = math.sin(2 * math.pi * 1000 * t) * math.exp(-t * 60) if t < 0.05 else 0.0
                frames += struct.pack('<h', int(v * 20000))
            with wave.open(str(root / 'click.wav'), 'wb') as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(bytes(frames))
            (root / 'lyrics.txt').write_text(LYRICS, encoding='utf-8')
            (root / 'words.json').write_text(json.dumps(heard()), encoding='utf-8')
            out = root / 'timing.json'
            code = lt.main([str(root / 'click.wav'), str(root / 'lyrics.txt'), '--words', str(root / 'words.json'),
                            '--out', str(out), '--srt', str(root / 'x.srt'), '--lrc-words', str(root / 'x.lrc')])
            self.assertEqual(code, 0)
            report = json.loads(out.read_text(encoding='utf-8'))
            self.assertAlmostEqual(report['bpm'], 120, delta=2)
            self.assertEqual(report['engine'], 'supplied')
            self.assertEqual(len(report['lines']), 3)


if __name__ == '__main__':
    unittest.main()
