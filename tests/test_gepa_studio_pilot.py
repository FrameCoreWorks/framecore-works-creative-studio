import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from gepa_studio_pilot import Budget, BudgetExhausted, StudioAdapter, guard_candidate, read_section, run_pilot, split_cases, validate_config

def config(): return json.loads((ROOT / 'config/gepa-pilot.json').read_text())
def dataset(): return json.loads((ROOT / 'config/gepa-cases.json').read_text())
GEPA_AVAILABLE = importlib.util.find_spec('gepa') is not None


class PilotBoundaries(unittest.TestCase):
    def test_target_and_protected_text_cannot_be_widened(self):
        c = config(); section = read_section(ROOT, c)
        self.assertEqual(guard_candidate({'example_selection': section}, c), section)
        for proposal in [{'welcome': section}, {'example_selection': section + '\n## New menu'}, {'example_selection': section.replace('A locked direction needs no new alternatives.', '')}]:
            with self.assertRaises(ValueError): guard_candidate(proposal, c)
        c['component']['path'] = 'plugins/framecore-work-creative-studio/skills/workflow-orchestrator/SKILL.md'
        with self.assertRaises(ValueError): read_section(ROOT, c)

    def test_holdout_and_ids_remain_separate(self):
        groups = split_cases(dataset()); self.assertEqual([len(groups[s]) for s in ['train', 'validation', 'holdout']], [4, 3, 3])
        d = dataset(); d['cases'][-1]['input'] = d['cases'][0]['input']
        with self.assertRaises(ValueError): split_cases(d)
        d = dataset(); d['cases'] = [x for x in d['cases'] if x['split'] != 'holdout']
        with self.assertRaises(ValueError): split_cases(d)

    def test_external_callbacks_require_approval_and_caps_before_any_call(self):
        c = config(); c['mode'] = 'authorized_external'
        calls = []
        with self.assertRaises(ValueError): run_pilot(c, dataset(), task=lambda *a: calls.append(a), proposer=lambda *a: calls.append(a))
        self.assertEqual(calls, [])
        c = config(); c['budget']['max_cost_usd'] = 1
        with self.assertRaises(ValueError): validate_config(c)
        with self.assertRaises(ValueError): run_pilot(config(), dataset(), task=lambda *a: None)

    def test_call_and_cost_budgets_stop_before_unauthorized_call(self):
        c = config(); c['budget']['max_task_calls'] = 1
        b = Budget(c); cap = b.reserve('task'); b.settle(cap, {'cost_usd': 0})
        with self.assertRaises(BudgetExhausted): b.reserve('task')
        with self.assertRaises(ValueError): b.settle(0, {'cost_usd': 0.01})
        c['budget'].update(max_cost_usd=0.5, task_call_cost_cap_usd=0.4)
        b = Budget(c); cap = b.reserve('task'); b.settle(cap, {'cost_usd': 0.4})
        with self.assertRaises(BudgetExhausted): b.reserve('task')

    def test_invalid_numeric_budgets_fail_closed(self):
        for value in [True, float('nan'), -1, 0]:
            c = config(); c['budget']['max_metric_calls'] = value
            with self.assertRaises(ValueError): validate_config(c)

    @unittest.skipUnless(GEPA_AVAILABLE, 'Install the pinned optional GEPA development dependency')
    def test_hard_gate_failure_or_unknown_has_zero_score_and_no_raw_output(self):
        case = split_cases(dataset())['train'][0]
        for state in ['FAIL', 'Unknown']:
            def task(section, item): return {'cost_usd': 0, 'score': 1, 'hard_gates': {g: state for g in item['hard_gates']}, 'feedback': 'Short scoped finding', 'output': 'RAW RESPONSE MUST BE DISCARDED'}
            a = StudioAdapter(config(), task, None)
            batch = a.evaluate([case], {'example_selection': read_section(ROOT, config())}, capture_traces=True)
            self.assertEqual(batch.scores, [0])
            self.assertNotIn('RAW RESPONSE', json.dumps(batch.outputs) + json.dumps(batch.trajectories))

    @unittest.skipUnless(GEPA_AVAILABLE, 'Install the pinned optional GEPA development dependency')
    def test_missing_gate_cannot_score_as_success(self):
        a = StudioAdapter(config(), lambda *args: {'cost_usd': 0, 'score': 1, 'hard_gates': {}, 'feedback': 'None'}, None)
        with self.assertRaises(ValueError): a.evaluate(split_cases(dataset())['train'][:1], {'example_selection': read_section(ROOT, config())})

    @unittest.skipUnless(GEPA_AVAILABLE, 'Install the pinned optional GEPA development dependency')
    def test_official_engine_pilot_is_zero_cost_proposal_only_and_source_unchanged(self):
        before = (ROOT / config()['component']['path']).read_bytes()
        report = run_pilot(config(), dataset())
        self.assertEqual(report['engine'], 'official gepa.optimize')
        self.assertEqual(report['status'], 'offline_integration_only')
        self.assertEqual(report['cost_usd'], 0)
        self.assertFalse(report['adopted']); self.assertFalse(report['raw_traces_saved'])
        self.assertTrue(report['source_unchanged'])
        self.assertLessEqual(report['calls']['task'], 40); self.assertLessEqual(report['calls']['proposal'], 3)
        self.assertEqual(report['creative_effectiveness'], 'NOT_ESTABLISHED')
        self.assertEqual(before, (ROOT / config()['component']['path']).read_bytes())


if __name__ == '__main__': unittest.main()
