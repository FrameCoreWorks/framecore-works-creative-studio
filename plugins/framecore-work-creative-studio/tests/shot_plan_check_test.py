"""The Python shot-plan checker gives the same result as the Node checker (scripts/review-creative-plan.mjs)."""
import copy
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/storyboard-sequence-architect/scripts/check_shot_plan.py'
NODE_TOOL = PLUGIN / 'scripts/review-creative-plan.mjs'
EXAMPLE = json.loads((PLUGIN / 'skills/storyboard-sequence-architect/assets/shot-plan.example.json').read_text(encoding='utf-8'))
spec = importlib.util.spec_from_file_location('check_shot_plan', TOOL)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def mutations():
    def m(fn):
        plan = copy.deepcopy(EXAMPLE)
        fn(plan)
        return plan
    yield 'example', copy.deepcopy(EXAMPLE)
    yield 'gap', m(lambda p: p['shots'][1].update(start_s=4.5))
    yield 'measured without evidence', m(lambda p: p['shots'][0].update(timing_basis='measured'))
    yield 'measured with evidence', m(lambda p: p['shots'][0].update(timing_basis='measured', timing_evidence='edit decision list v3'))
    yield 'dissolve overlap', m(lambda p: (p['bridges'][0].update(type='dissolve', overlap_s=0.5), p['shots'][1].update(start_s=3.5)))
    yield 'sound bridge overlap', m(lambda p: (p['bridges'][0].update(type='sound_bridge', overlap_s=0.5), p['shots'][1].update(start_s=3.5)))
    yield 'overlap eats a shot', m(lambda p: (p['bridges'][0].update(type='dissolve', overlap_s=9), p['shots'][1].update(start_s=-5)))
    yield 'unbound refs', m(lambda p: p['shots'][2].update(bound_refs=['REF-PRODUCT']))
    yield 'all bound', m(lambda p: [s.update(bound_refs=list(s['required_refs'])) for s in p['shots']])
    yield 'complex shot', m(lambda p: p['shots'][0].update(primary_actions=2, camera_moves=2))
    yield 'source too short', m(lambda p: p['shots'][0].update(generation_duration_s=3))
    yield 'duplicate id and unknown', m(lambda p: (p['shots'][1].update(id='S01'), p['shots'][2].update(id='Unknown')))
    yield 'missing bridge', m(lambda p: p['bridges'].pop())
    yield 'duplicate bridge', m(lambda p: p['bridges'].append(dict(p['bridges'][0])))
    yield 'bad bridge type and checks', m(lambda p: p['bridges'][1].update(type='wipe', review_checks=[], relationship=''))
    yield 'bridge not adjacent', m(lambda p: p['bridges'][0].update(to='S03'))
    yield 'wrong end', m(lambda p: p.update(target_duration_s=30))
    yield 'string target', m(lambda p: p.update(target_duration_s='25'))
    yield 'shot not an object', m(lambda p: p['shots'].insert(2, 'S02b'))
    yield 'missing fields', m(lambda p: [p['shots'][3].pop(k) for k in ('id', 'action', 'required_refs')])
    yield 'null id', m(lambda p: p['shots'][4].update(id=None))
    yield 'float counts', m(lambda p: p['shots'][0].update(primary_actions=1.0, camera_moves=-1))
    yield 'strict without refs', m(lambda p: p['shots'][1].update(required_refs=[], bound_refs=[]))
    yield 'not a plan', {'shots': []}


class Parity(unittest.TestCase):
    def test_python_and_node_agree(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('Node.js is not installed here')
        with tempfile.TemporaryDirectory() as temp:
            for name, plan in mutations():
                path = pathlib.Path(temp, 'plan.json')
                path.write_text(json.dumps(plan), encoding='utf-8')
                done = subprocess.run([node, str(NODE_TOOL), 'sequence', str(path)], capture_output=True, text=True, timeout=60)
                self.assertIn(done.returncode, (0, 1), done.stderr)
                self.assertEqual(checker.review_sequence(json.loads(path.read_text(encoding='utf-8'))), json.loads(done.stdout), name)

    def test_the_cli_reports_and_exits_like_the_node_tool(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'plan.json')
            path.write_text(json.dumps(EXAMPLE), encoding='utf-8')
            done = subprocess.run([sys.executable, '-B', str(TOOL), str(path)], capture_output=True, text=True, timeout=60)
            self.assertEqual(done.returncode, 0, done.stderr)
            result = json.loads(done.stdout)
            self.assertEqual((result['status'], result['execution_readiness']), ('structurally_valid_plan', 'blocked'))
            bad = copy.deepcopy(EXAMPLE)
            bad['shots'][1]['start_s'] = 4.5
            path.write_text(json.dumps(bad), encoding='utf-8')
            self.assertEqual(subprocess.run([sys.executable, '-B', str(TOOL), str(path)], capture_output=True).returncode, 1)
            path.write_text('{', encoding='utf-8')
            self.assertEqual(subprocess.run([sys.executable, '-B', str(TOOL), str(path)], capture_output=True).returncode, 2)


if __name__ == '__main__':
    unittest.main(verbosity=1)
