"""Tests for scripts/motion_benchmark.py: blind set, scores sheet, key and summary."""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'scripts', 'motion_benchmark.py')
EXAMPLE = os.path.join(ROOT, 'plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-scenes/examples/color-block.motion-score.json')


class MotionBenchmarkTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for run in ('run-a', 'run-b'):
            folder = os.path.join(self.tmp, 'results', run, 'b4-sale')
            os.makedirs(folder)
            shutil.copyfile(EXAMPLE, os.path.join(folder, 'sale.motion.json'))
            with open(os.path.join(folder, 'sale.mp4'), 'wb') as handle:
                handle.write(b'not a real video')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_script(self, *args):
        return subprocess.run([sys.executable, '-B', SCRIPT, *args], capture_output=True, text=True)

    def test_blind_then_summarize(self):
        results, blind = os.path.join(self.tmp, 'results'), os.path.join(self.tmp, 'blind')
        made = self.run_script('blind', results, blind, '--seed', '1')
        self.assertEqual(made.returncode, 0, made.stderr)
        key = json.load(open(os.path.join(blind, 'key.json')))
        self.assertEqual(sorted(entry['run'] for entry in key.values()), ['run-a', 'run-b'])
        videos = sorted(os.listdir(os.path.join(blind, 'videos')))
        self.assertEqual(videos, sorted(code + '.mp4' for code in key))
        self.assertTrue(all('run' not in name for name in videos), 'video names do not reveal the run')
        rows = list(csv.DictReader(open(os.path.join(blind, 'scores.csv'))))
        self.assertEqual(len(rows), 2)
        self.assertNotIn('run', rows[0])
        for row, value in zip(rows, ('4', '2')):
            for criterion in ('concept', 'motion', 'typography', 'pacing', 'sound', 'overall'):
                row[criterion] = value
        with open(os.path.join(blind, 'scores.csv'), 'w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        summary = self.run_script('summarize', results, blind)
        self.assertEqual(summary.returncode, 0, summary.stderr)
        table = json.load(open(os.path.join(blind, 'summary.json')))
        self.assertEqual(sorted(table), ['run-a', 'run-b'])
        self.assertEqual(sorted(t['overall'] for t in table.values()), [2.0, 4.0])
        self.assertTrue(all(t['delivered'] == 1 for t in table.values()))
        self.assertIn('| run-a |', open(os.path.join(blind, 'summary.md')).read())

    def test_refuses_existing_output_and_empty_results(self):
        os.makedirs(os.path.join(self.tmp, 'exists'))
        self.assertNotEqual(self.run_script('blind', os.path.join(self.tmp, 'results'), os.path.join(self.tmp, 'exists')).returncode, 0)
        os.makedirs(os.path.join(self.tmp, 'empty'))
        self.assertNotEqual(self.run_script('blind', os.path.join(self.tmp, 'empty'), os.path.join(self.tmp, 'out')).returncode, 0)

    def test_briefs_are_complete(self):
        briefs = json.load(open(os.path.join(ROOT, 'docs/motion-benchmark/briefs.json')))['briefs']
        self.assertEqual(len(briefs), 8)
        self.assertEqual(len({b['id'] for b in briefs}), 8)
        for brief in briefs:
            self.assertIn('FrameCore Works Creative Studio', brief['prompt'])
            self.assertIn('.motion.json', brief['prompt'])


    def test_contract_is_found_next_to_meta_json(self):
        folder = os.path.join(self.tmp, 'results', 'run-a', 'b4-sale')
        os.rename(os.path.join(folder, 'sale.motion.json'), os.path.join(folder, 'video.motion.json'))
        with open(os.path.join(folder, 'meta.json'), 'w') as handle:
            json.dump({'host': 'test', 'model': 'm'}, handle)
        blind = os.path.join(self.tmp, 'blind')
        self.assertEqual(self.run_script('blind', os.path.join(self.tmp, 'results'), blind, '--seed', '1').returncode, 0)
        key = json.load(open(os.path.join(blind, 'key.json')))
        entry = next(e for e in key.values() if e['run'] == 'run-a')
        self.assertTrue(entry['auto']['delivered_contract'])
        self.assertIn('critique', entry['auto'], 'the contract, not meta.json, was judged')
        # The fake video cannot be read: its review is incomplete and keeps no score.
        self.assertEqual(entry['auto']['video_critique']['status'], 'incomplete')
        self.assertIsNone(entry['auto']['video_critique']['score'])

    def test_meta_json_alone_is_not_a_contract(self):
        folder = os.path.join(self.tmp, 'results', 'run-b', 'b4-sale')
        os.remove(os.path.join(folder, 'sale.motion.json'))
        with open(os.path.join(folder, 'meta.json'), 'w') as handle:
            json.dump({'host': 'test'}, handle)
        blind = os.path.join(self.tmp, 'blind')
        self.assertEqual(self.run_script('blind', os.path.join(self.tmp, 'results'), blind, '--seed', '1').returncode, 0)
        entry = next(e for e in json.load(open(os.path.join(blind, 'key.json'))).values() if e['run'] == 'run-b')
        self.assertFalse(entry['auto']['delivered_contract'])
        self.assertNotIn('critique', entry['auto'])


if __name__ == '__main__':
    unittest.main()
