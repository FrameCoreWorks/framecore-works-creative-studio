"""Prompt records (pipeline-core/assets/prompt-record): checks and per-model compilation of image and video planning records."""
import copy
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/pipeline-core/assets/prompt-record/prompt_record.py'
spec = importlib.util.spec_from_file_location('prompt_record', TOOL)
pr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pr)


class ImageRecords(unittest.TestCase):
    def setUp(self):
        self.r = copy.deepcopy(pr.EXAMPLES['image'])

    def test_example_is_clean(self):
        self.assertEqual(pr.check(self.r), ([], []))

    def test_ideogram_output_follows_the_documented_schema(self):
        out = json.loads(pr.compile_ideogram(self.r))
        self.assertEqual(list(out)[0], 'high_level_description')
        els = out['compositional_deconstruction']['elements']
        self.assertIn('background', out['compositional_deconstruction'])
        self.assertTrue(all(e['type'] in ('obj', 'text') for e in els))
        self.assertEqual([e['text'] for e in els if e['type'] == 'text'], ['JAZZ NAD WISŁĄ', '12.07 · 20:00'])
        self.assertFalse('photo' in out['style_description'] and 'art_style' in out['style_description'])

    def test_exact_text_is_kept_verbatim_in_every_target(self):
        for f in (pr.compile_ideogram, pr.compile_flux2, pr.compile_image_prose):
            self.assertIn('JAZZ NAD WISŁĄ', f(self.r))

    def test_flux2_keeps_its_fields_and_warns_about_negatives(self):
        out = json.loads(pr.compile_flux2(self.r))
        self.assertEqual(out['scene'], self.r['summary'])
        self.assertTrue(set(out) <= {'scene', 'subjects', 'style', 'color_palette', 'lighting', 'mood', 'background', 'composition', 'camera', 'text'})
        self.r['avoid'] = ['blurry text']
        self.assertTrue(any('no negative prompt' in w for w in pr.check(self.r, 'flux2')[1]))

    def test_errors_are_found(self):
        self.r['style']['photo'] = 'shot on 35 mm'
        self.r['subjects'][0]['bbox'] = [900, 0, 100, 500]
        self.r['color_palette'] = ['#000000'] * 17
        self.r['summary'] = ''
        errors = pr.check(self.r)[0]
        self.assertEqual(len(errors), 4, errors)

    def test_settings_in_prose_are_flagged(self):
        self.r['composition'] += ', 16:9'
        self.assertTrue(any('params' in w for w in pr.check(self.r)[1]))


class VideoRecords(unittest.TestCase):
    def setUp(self):
        self.r = copy.deepcopy(pr.EXAMPLES['video'])

    def test_example_is_clean(self):
        self.assertEqual(pr.check(self.r), ([], []))

    def test_gaps_and_wrong_total_are_errors(self):
        self.r['shots'][1]['start_s'] = 5
        self.r['shots'][1]['end_s'] = 9
        errors = pr.check(self.r)[0]
        self.assertTrue(any('gaps' in e for e in errors) and any('duration_s' in e for e in errors), errors)

    def test_kling_limits(self):
        self.r['settings']['duration_s'] = 20
        self.r['shots'][1]['end_s'] = 20
        self.assertTrue(any('3 to 15 s' in e for e in pr.check(self.r, 'kling')[0]))

    def test_unknown_speaker_and_long_dialogue(self):
        self.r['shots'][1]['dialogue'][0]['speaker'] = 'customer'
        self.assertTrue(any('not in subjects' in e for e in pr.check(self.r)[0]))
        r = copy.deepcopy(pr.EXAMPLES['video'])
        r['shots'][1]['dialogue'][0]['line'] = ' '.join(['word'] * 20)
        self.assertTrue(any('too long to sync' in w for w in pr.check(r)[1]))

    def test_kling_payload_fields_and_durations(self):
        out = json.loads(pr.compile_video(self.r, 'kling'))
        self.assertTrue(out['multi_shot'])
        self.assertEqual(out['shot_type'], 'customize')
        self.assertEqual([s['duration'] for s in out['multi_prompt']], [4, 4])
        self.assertEqual(sum(s['duration'] for s in out['multi_prompt']), out['duration'])
        self.assertEqual(out['aspect_ratio'], '9:16')

    def test_identity_anchors_repeat_and_sora_blocks(self):
        sora = pr.compile_video(self.r, 'sora')
        for block in ('Cinematography:', 'Actions:', 'Dialogue:', 'Background Sound:'):
            self.assertIn(block, sora)
        self.assertIn('short grey hair', sora)
        stamps = pr.compile_video(self.r, 'timestamps')
        self.assertIn('[00:00-00:04]', stamps)
        self.assertNotIn('{', pr.compile_video(self.r, 'prose'))


class Cli(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True)

    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            good = pathlib.Path(d, 'v.json')
            good.write_text(json.dumps(pr.EXAMPLES['video']))
            self.assertEqual(self.run_tool('check', str(good)).returncode, 0)
            bad = copy.deepcopy(pr.EXAMPLES['video'])
            bad['shots'][0]['end_s'] = 3
            badf = pathlib.Path(d, 'bad.json')
            badf.write_text(json.dumps(bad))
            self.assertEqual(self.run_tool('compile', str(badf), '--to', 'kling').returncode, 1)
            self.assertEqual(self.run_tool('compile', str(good), '--to', 'ideogram').returncode, 2)
            self.assertEqual(self.run_tool('check', str(pathlib.Path(d, 'missing.json'))).returncode, 2)


if __name__ == '__main__':
    unittest.main()
