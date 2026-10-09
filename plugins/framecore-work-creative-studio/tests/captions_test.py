"""Tests for skills/caption-studio/assets/captions/captions.py: files, limits, building, contract import and burn-in."""
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/caption-studio/assets/captions/captions.py'
EXAMPLE = PLUGIN / 'skills/hyperframes-workflow/assets/motion-sync/examples/voice-over.srt'
SYNC = PLUGIN / 'skills/hyperframes-workflow/assets/motion-sync/sync.mjs'
STARTER = PLUGIN / 'skills/hyperframes-workflow/assets/gsap-motion-starter/motion-score.json'

spec = importlib.util.spec_from_file_location('captions', TOOL)
captions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(captions)


def cue(start, end, text):
    return {'start_ms': start, 'end_ms': end, 'text': text}


def have_media():
    try:
        import PIL  # noqa: F401
    except ImportError:
        return False
    return bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))


class Files(unittest.TestCase):
    def test_srt_and_webvtt_round_trip(self):
        cues = captions.read_cues(EXAMPLE)
        self.assertEqual(len(cues), 3)
        vtt = captions.write(cues, 'vtt')
        self.assertTrue(vtt.startswith('WEBVTT\n\n00:00:00.600 --> 00:00:03.800\n'))
        self.assertEqual(captions.parse(vtt), cues)
        srt = captions.write(cues, 'srt')
        self.assertTrue(srt.startswith('1\n00:00:00,600 --> 00:00:03,800\n'))
        self.assertEqual(captions.parse(srt), cues)

    def test_styling_settings_and_headers_are_dropped(self):
        text = 'WEBVTT\n\nNOTE a comment\n\n00:01.000 --> 00:02.500 align:start\n<b>Bold</b> {\\an8}words\nsecond line\n'
        self.assertEqual(captions.parse(text), [cue(1000, 2500, 'Bold words\nsecond line')])

    @unittest.skipUnless(shutil.which('node'), 'Node.js not available')
    def test_contract_import_matches_the_motion_sync_tool(self):
        script = (f"import {{parseSubtitles, importCaptions}} from {json.dumps(SYNC.as_uri())};"
                  f"import fs from 'node:fs';"
                  f"const score = JSON.parse(fs.readFileSync({json.dumps(str(STARTER))}, 'utf8'));"
                  f"const cues = parseSubtitles(fs.readFileSync({json.dumps(str(EXAMPLE))}, 'utf8'));"
                  f"const out = importCaptions(score, cues, {{replace: true}});"
                  f"console.log(JSON.stringify({{captions: out.score.captions, copy: out.score.copy, warnings: out.warnings}}));")
        node = json.loads(subprocess.run(['node', '--input-type=module', '-e', script], capture_output=True, text=True, check=True).stdout)
        score = json.loads(STARTER.read_text())
        result, warnings = captions.import_captions(score, captions.read_cues(EXAMPLE), replace=True)
        self.assertEqual(result['captions'], node['captions'])
        self.assertEqual(result['copy'], node['copy'])
        self.assertEqual(warnings, node['warnings'])


class Limits(unittest.TestCase):
    def codes(self, cues, **kw):
        report = captions.check(cues, **kw)
        return report['errors'], report['warnings']

    def test_subtitle_limits_are_errors(self):
        long_line = 'x' * 43
        errors, _ = self.codes([cue(0, 2000, long_line)], profile='subtitles', language='pl')
        self.assertTrue(any('43 characters' in e for e in errors))
        errors, _ = self.codes([cue(0, 2000, 'a\nb\nc')], profile='subtitles')
        self.assertTrue(any('3 lines' in e for e in errors))
        errors, _ = self.codes([cue(0, 1000, 'Dwadzieścia znaków to za dużo')], profile='subtitles', language='pl')
        self.assertTrue(any('characters per second; at most 17 for pl (adult)' in e for e in errors))
        errors, _ = self.codes([cue(0, 1000, 'Twenty characters ok')], profile='subtitles', language='en')
        self.assertEqual(errors, [])
        errors, _ = self.codes([cue(0, 700, 'Hi')], profile='subtitles')
        self.assertTrue(any('5/6 s' in e for e in errors))
        errors, _ = self.codes([cue(0, 7500, 'A long hold')], profile='subtitles')
        self.assertTrue(any('at most 7 s' in e for e in errors))
        errors, _ = self.codes([cue(0, 2000, 'One'), cue(1500, 3000, 'Two')], profile='subtitles')
        self.assertTrue(any('overlaps' in e for e in errors))

    def test_children_and_unknown_languages(self):
        errors, _ = self.codes([cue(0, 1000, 'Czternaście zn')], profile='subtitles', language='pl', audience='children')
        self.assertTrue(any('at most 13' in e for e in errors))
        errors, warnings = self.codes([cue(0, 1000, 'Ein Satz mit sehr vielen Zeichen')], profile='subtitles', language='de')
        self.assertEqual(errors, [])
        self.assertTrue(any('Unknown' in w for w in warnings))

    def test_social_limits_warn_and_text_uses_the_hold_rule(self):
        errors, warnings = self.codes([cue(0, 1000, 'Dwadzieścia znaków to za dużo')], profile='social', language='pl')
        self.assertEqual(errors, [])
        self.assertTrue(any('characters per second' in w for w in warnings))
        _, warnings = self.codes([cue(0, 1500, 'Gotowe do eksportu')], profile='text')
        self.assertTrue(any('reading it needs about 1.88 s' in w for w in warnings))
        self.assertAlmostEqual(captions.reading_seconds('Gotowe do eksportu'), 1.8846, places=3)

    def test_line_ending_on_a_one_letter_polish_word_is_flagged(self):
        _, warnings = self.codes([cue(0, 3000, 'Zobacz, co masz w\nportfelu')], profile='social', language='pl')
        self.assertTrue(any('ends on "w"' in w for w in warnings))

    def test_flicker_gap(self):
        _, warnings = self.codes([cue(0, 2000, 'One'), cue(2030, 4000, 'Two')], profile='social', fps=30)
        self.assertTrue(any('flicker' in w for w in warnings))


class Building(unittest.TestCase):
    def words(self):
        out, t = [], 0.3
        for w in 'Spokojny portfel to aplikacja, która pomaga planować wydatki bez stresu. Zobacz, ile możesz zaoszczędzić w tym miesiącu i w kolejnych.'.split():
            d = 0.18 + 0.04 * len(w)
            out.append({'word': w, 'start': round(t, 3), 'end': round(t + d, 3)})
            t += d + 0.06 + (0.5 if w.endswith('.') else 0)
        return out

    def test_social_cues_fit_one_line_and_break_naturally(self):
        cues = captions.build_from_words(self.words(), profile='social', language='pl')
        report = captions.check(cues, profile='social', language='pl')
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['warnings'], [])
        self.assertTrue(all('\n' not in c['text'] and len(c['text']) <= 42 for c in cues))
        self.assertEqual([c['text'] for c in cues][-2:], ['Zobacz, ile możesz zaoszczędzić', 'w tym miesiącu i w kolejnych.'])
        for a, b in zip(cues, cues[1:]):
            self.assertTrue(b['start_ms'] - a['end_ms'] == 0 or b['start_ms'] - a['end_ms'] >= 67)

    def test_subtitle_cues_use_two_balanced_lines(self):
        cues = captions.build_from_words(self.words(), profile='subtitles', language='pl')
        self.assertEqual(captions.check(cues, profile='subtitles', language='pl')['errors'], [])
        self.assertEqual(cues[0]['text'], 'Spokojny portfel to aplikacja,\nktóra pomaga planować wydatki bez stresu.')

    def test_segments_are_split_when_too_long(self):
        cues = captions.build_from_segments([{'start': 0, 'end': 6, 'text': 'Ten segment ma zdecydowanie zbyt wiele słów, aby zmieścić się w dwóch liniach napisów na ekranie telefonu.'}], 'pl')
        self.assertGreater(len(cues), 1)
        self.assertEqual(cues[0]['start_ms'], 0)
        self.assertEqual(cues[-1]['end_ms'], 6000)
        self.assertTrue(all(len(line) <= 42 for c in cues for line in c['text'].split('\n')))

    def test_command_refuses_to_overwrite_and_reports_check(self):
        with tempfile.TemporaryDirectory() as temp:
            words = pathlib.Path(temp, 'words.json')
            words.write_text(json.dumps({'words': self.words()}, ensure_ascii=False), encoding='utf-8')
            out = pathlib.Path(temp, 'out.srt')
            run = subprocess.run([sys.executable, str(TOOL), 'build', '--words', str(words), '--to', 'srt', '--out', str(out), '--language', 'pl'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)['check'], 'PASS')
            again = subprocess.run([sys.executable, str(TOOL), 'build', '--words', str(words), '--to', 'srt', '--out', str(out)], capture_output=True, text=True)
            self.assertEqual(again.returncode, 2)
            self.assertIn('already exists', again.stderr)


class Contract(unittest.TestCase):
    def test_import_keeps_exact_text_and_shifts_overlaps(self):
        score = {'fps': {'num': 30, 'den': 1}, 'totalFrames': 90, 'copy': {'title': 'Hi'}, 'captions': []}
        result, warnings = captions.import_captions(score, [cue(0, 1000, 'One'), cue(900, 2000, 'Two'), cue(2900, 4000, 'Three'), cue(3500, 3600, 'Gone')])
        self.assertEqual(result['captions'][:2], [{'id': 'caption-1', 'start': 0, 'end': 30, 'copy': 'caption-1'}, {'id': 'caption-2', 'start': 30, 'end': 60, 'copy': 'caption-2'}])
        self.assertEqual(result['copy']['caption-3'], 'Three')
        self.assertEqual(result['captions'][2]['end'], 90)
        self.assertTrue(any('overlaps' in w for w in warnings))
        self.assertTrue(any('after the last frame' in w for w in warnings))
        with self.assertRaises(ValueError):
            captions.import_captions(result, [cue(0, 500, 'x')])


@unittest.skipUnless(have_media(), 'Pillow, ffmpeg and ffprobe are needed for burn-in')
class BurnIn(unittest.TestCase):
    def test_captions_appear_only_inside_their_cues_and_audio_is_kept(self):
        from PIL import Image, ImageChops
        with tempfile.TemporaryDirectory() as temp:
            src, out = os.path.join(temp, 'src.mp4'), os.path.join(temp, 'out.mp4')
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=0x204060:size=540x960:rate=30:duration=3', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=3',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', src], check=True)
            srt = os.path.join(temp, 'c.srt')
            pathlib.Path(srt).write_text('1\n00:00:01,000 --> 00:00:02,000\nTwoje wydatki pod kontrolą\n', encoding='utf-8')
            summary = captions.burn(src, captions.read_cues(srt), out)
            self.assertEqual(summary['frames'], 90)
            self.assertEqual(summary['frames_with_captions'], 30)
            streams = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', out], capture_output=True, text=True, check=True).stdout.split()
            self.assertEqual(sorted(streams), ['audio', 'video'])

            def frame(path, t):
                png = os.path.join(temp, f'{os.path.basename(path)}-{t}.png')
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', path, '-frames:v', '1', png], check=True)
                return Image.open(png).convert('RGB')
            band = (0, 700, 540, 860)  # the caption sits above the bottom 14%
            inside = ImageChops.difference(frame(src, 1.5).crop(band), frame(out, 1.5).crop(band)).getbbox()
            outside = ImageChops.difference(frame(src, 0.5).crop(band), frame(out, 0.5).crop(band))
            self.assertIsNotNone(inside)
            self.assertLess(max(band[1] for band in outside.getextrema()), 24)


if __name__ == '__main__':
    unittest.main()
