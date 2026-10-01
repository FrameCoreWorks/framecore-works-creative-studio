#!/usr/bin/env python3
"""Proposal-only GEPA integration. Offline mode uses genuine GEPA with synthetic callbacks.

External callbacks are injected by an explicitly scoped developer run; this module
contains no provider integration. It never writes plugin source or raw traces.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import time

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'plugins/framecore-work-creative-studio/skills/pipeline-core/references/quality-improvement-methods.md'
COMPONENT = 'example_selection'


class BudgetExhausted(RuntimeError):
    pass


def read_section(root, config):
    component = config['component']
    if component['path'] != TARGET or component['id'] != COMPONENT or component['heading'] != 'Relevant examples':
        raise ValueError('Only the allowlisted example-selection section may be optimized')
    target = root / TARGET
    if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Unsafe target')
    body = target.read_text()
    match = re.search(r'^## Relevant examples\n(.*?)(?=^## |\Z)', body, re.M | re.S)
    if not match:
        raise ValueError('Target section missing')
    return match.group(1).strip()


def guard_candidate(candidate, config):
    if not isinstance(candidate, dict) or set(candidate) != {COMPONENT}:
        raise ValueError('Candidate changed the component scope')
    value = candidate[COMPONENT]
    if not isinstance(value, str) or not 200 <= len(value) <= config['component']['max_chars']:
        raise ValueError('Invalid candidate length')
    if re.search(r'^#{1,6}\s|ignore.{0,25}(rules|locks|instructions)|override.{0,25}(rules|locks)|raw (reasoning|chain.of.thought)', value, re.M | re.I):
        raise ValueError('Candidate introduces a heading or unsafe override')
    if not all(s in value for s in config['component']['protected_sentences']):
        raise ValueError('Candidate removed protected selection constraints')
    return value


def validate_config(config):
    if config.get('schema_version') != 1 or config.get('mode') not in {'offline_integration', 'authorized_external'}:
        raise ValueError('Invalid pilot mode')
    budget = config['budget']
    for key in ['max_task_calls', 'max_metric_calls', 'max_proposal_calls', 'max_seconds']:
        if not isinstance(budget.get(key), (int, float)) or isinstance(budget[key], bool) or not math.isfinite(budget[key]) or budget[key] <= 0:
            raise ValueError('Invalid budget: ' + key)
    for key in ['max_task_calls', 'max_metric_calls', 'max_proposal_calls']:
        if not isinstance(budget[key], int):
            raise ValueError('Call budgets must be integers')
    for key in ['max_cost_usd', 'task_call_cost_cap_usd', 'proposal_call_cost_cap_usd']:
        if not isinstance(budget.get(key), (int, float)) or isinstance(budget[key], bool) or not math.isfinite(budget[key]) or budget[key] < 0:
            raise ValueError('Invalid cost budget')
    auth = config.get('authorization', {})
    if config['mode'] == 'offline_integration':
        if auth.get('external_execution') is not False or any(budget[k] != 0 for k in ['max_cost_usd', 'task_call_cost_cap_usd', 'proposal_call_cost_cap_usd']):
            raise ValueError('Offline integration permits zero cost and no external execution')
    elif auth.get('external_execution') is not True or not all(isinstance(auth.get(k), str) and auth[k].strip() for k in ['provider', 'model', 'evidence_id']) or budget['max_cost_usd'] <= 0 or budget['task_call_cost_cap_usd'] <= 0 or budget['proposal_call_cost_cap_usd'] <= 0:
        raise ValueError('External run requires actual scoped approval and explicit per-call/total cost caps')


def split_cases(dataset):
    cases = dataset.get('cases') if isinstance(dataset, dict) else None
    if not isinstance(cases, list) or not cases:
        raise ValueError('Missing cases')
    ids, inputs = set(), set()
    groups = {name: [] for name in ['train', 'validation', 'holdout']}
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get('id'), str) or not case['id'] or case['id'] in ids or not isinstance(case.get('input'), str) or not case['input'] or case['input'] in inputs or case.get('split') not in groups or not isinstance(case.get('hard_gates'), list) or not case['hard_gates'] or not all(isinstance(g, str) and g for g in case['hard_gates']):
            raise ValueError('Invalid case or cross-split ID/input leakage')
        ids.add(case['id']); inputs.add(case['input']); groups[case['split']].append(case)
    if not all(groups.values()):
        raise ValueError('Train, validation and untouched holdout are required')
    return groups


class Budget:
    def __init__(self, config):
        self.limits = config['budget']; self.task_calls = 0; self.proposal_calls = 0
        self.cost = 0.0; self.started = time.monotonic()

    def reserve(self, kind):
        if time.monotonic() - self.started >= self.limits['max_seconds']:
            raise BudgetExhausted('Time budget exhausted')
        count = self.task_calls if kind == 'task' else self.proposal_calls
        if count >= self.limits['max_' + kind + '_calls']:
            raise BudgetExhausted(kind + ' call budget exhausted')
        cap = self.limits[kind + '_call_cost_cap_usd']
        if self.cost + cap > self.limits['max_cost_usd'] + 1e-12:
            raise BudgetExhausted('Cannot reserve a call within total cost cap')
        if kind == 'task': self.task_calls += 1
        else: self.proposal_calls += 1
        return cap

    def settle(self, cap, response):
        cost = response.get('cost_usd') if isinstance(response, dict) else None
        if not isinstance(cost, (float, int)) or isinstance(cost, bool) or not math.isfinite(cost) or not 0 <= cost <= cap:
            raise ValueError('Callback failed its pre-agreed cost cap')
        self.cost += cost


def offline_task(section, case):
    # Deliberately artificial integration metric. It is NOT a creative evaluator.
    score = 1.0 if 'Offline integration marker.' in section else 0.5
    return {'score': score, 'hard_gates': {g: 'PASS' for g in case['hard_gates']}, 'feedback': 'Synthetic metric: add the offline marker to exercise proposal acceptance.', 'output': 'Synthetic callback, no model output', 'cost_usd': 0}


def offline_propose(section, feedback):
    return {'text': section + '\n\nOffline integration marker.' if 'Offline integration marker.' not in section else section, 'cost_usd': 0}


class StudioAdapter:
    def __init__(self, config, task, proposer):
        self.config = config; self.task = task; self.proposer = proposer; self.budget = Budget(config)

    def evaluate(self, batch, candidate, capture_traces=False):
        from gepa.core.adapter import EvaluationBatch
        section = guard_candidate(candidate, self.config)
        scores, outputs, summaries = [], [], []
        for case in batch:  # Intentionally serial, including real callback implementations.
            cap = self.budget.reserve('task')
            response = self.task(section, case)
            self.budget.settle(cap, response)
            gates = response.get('hard_gates', {})
            score = response.get('score')
            if not isinstance(gates, dict) or any(gates.get(g) not in {'PASS', 'FAIL', 'Unknown'} for g in case['hard_gates']) or not isinstance(score, (int, float)) or isinstance(score, bool) or not math.isfinite(score) or not 0 <= score <= 1 or not isinstance(response.get('feedback'), str):
                raise ValueError('Invalid evaluator result; missing evidence cannot score as success')
            passed = all(gates[g] == 'PASS' for g in case['hard_gates'])
            scores.append(float(score) if passed else 0.0)
            # Raw model responses/traces are intentionally discarded.
            outputs.append({'case_id': case['id'], 'hard_gates': {g: gates[g] for g in case['hard_gates']}})
            summaries.append({'case_id': case['id'], 'feedback': response['feedback'][:1200], 'hard_gates': outputs[-1]['hard_gates']})
        return EvaluationBatch(outputs=outputs, scores=scores, trajectories=summaries if capture_traces else None)

    def make_reflective_dataset(self, candidate, eval_batch, components_to_update):
        if components_to_update != [COMPONENT]: raise ValueError('Reflective component scope changed')
        return {COMPONENT: eval_batch.trajectories or []}

    def propose_new_texts(self, candidate, reflective_dataset, components_to_update, *, metadata=None):
        if components_to_update != [COMPONENT] or set(reflective_dataset) != {COMPONENT}: raise ValueError('Proposal scope changed')
        cap = self.budget.reserve('proposal')
        response = self.proposer(guard_candidate(candidate, self.config), reflective_dataset[COMPONENT])
        self.budget.settle(cap, response)
        proposed = {COMPONENT: response.get('text')}
        guard_candidate(proposed, self.config)
        return proposed


def run_pilot(config, dataset, *, root=ROOT, task=None, proposer=None):
    validate_config(config)
    groups = split_cases(dataset)
    section = read_section(root, config)
    baseline = {COMPONENT: section}; guard_candidate(baseline, config)
    if config['mode'] == 'offline_integration':
        if task is not None or proposer is not None: raise ValueError('Offline mode uses only bundled zero-cost callbacks')
        task, proposer = offline_task, offline_propose
    elif not callable(task) or not callable(proposer):
        raise ValueError('External mode requires approved explicit serial callbacks')
    from gepa import optimize, ScoreThresholdStopper, NoImprovementStopper
    adapter = StudioAdapter(config, task, proposer)
    stop = lambda state: adapter.budget.proposal_calls >= config['budget']['max_proposal_calls'] or time.monotonic() - adapter.budget.started >= config['budget']['max_seconds']
    result = optimize(seed_candidate=baseline, trainset=groups['train'], valset=groups['validation'], adapter=adapter, max_metric_calls=config['budget']['max_metric_calls'], stop_callbacks=[stop, ScoreThresholdStopper(1.0), NoImprovementStopper(2)], reflection_minibatch_size=2, candidate_selection_strategy='pareto', use_merge=False, run_dir=None, write_agent_state=False, track_best_outputs=False, use_wandb=False, use_mlflow=False, display_progress_bar=False, seed=47, raise_on_exception=True)
    candidate = result.best_candidate
    guard_candidate(candidate, config)
    # Holdout is evaluated only after selection and never fed to the proposer.
    base_holdout = adapter.evaluate(groups['holdout'], baseline)
    candidate_holdout = adapter.evaluate(groups['holdout'], candidate)
    hard_pass = all(all(v == 'PASS' for v in o['hard_gates'].values()) for o in candidate_holdout.outputs)
    improvement = sum(candidate_holdout.scores) > sum(base_holdout.scores)
    unchanged = read_section(root, config) == section
    if not unchanged: raise ValueError('Source drifted during pilot; discard this proposal')
    return {'mode': config['mode'], 'engine': 'official gepa.optimize', 'target': config['component'], 'seed_sha256': hashlib.sha256(section.encode()).hexdigest(), 'candidate': candidate, 'holdout': {'baseline_scores': base_holdout.scores, 'candidate_scores': candidate_holdout.scores, 'hard_gates_pass': hard_pass, 'improved': improvement}, 'calls': {'task': adapter.budget.task_calls, 'proposal': adapter.budget.proposal_calls}, 'cost_usd': adapter.budget.cost, 'source_unchanged': unchanged, 'status': 'offline_integration_only' if config['mode'] == 'offline_integration' else 'proposal_requires_owner_and_regression_review', 'adopted': False, 'protected_regressions': 'NOT_RUN by this optimizer', 'creative_effectiveness': 'NOT_ESTABLISHED', 'raw_traces_saved': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'config/gepa-pilot.json')
    parser.add_argument('--cases', type=Path, default=ROOT / 'config/gepa-cases.json')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if config.get('mode') != 'offline_integration':
        parser.error('CLI supports offline integration only; approved external runs inject callbacks through run_pilot')
    report = run_pilot(config, json.loads(args.cases.read_text()))
    destination = args.output.resolve()
    if destination.is_relative_to((ROOT / 'plugins').resolve()) or destination.exists():
        parser.error('Output must be a new report outside plugin source')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'calls', 'cost_usd', 'source_unchanged', 'adopted']}))


if __name__ == '__main__': main()
