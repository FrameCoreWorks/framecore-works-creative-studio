#!/usr/bin/env python3
"""Structural check of a shot plan, for hosts that run Python but not Node.

A line-for-line port of reviewSequence in scripts/review-creative-plan.mjs: the same rules, messages and result, so a plan
checked in ChatGPT's Python sandbox gets the verdict it would get in Codex or Claude Code. It reads declared planning
data only: interval gaps, duplicate IDs, missing bridges and unbound references. It never judges pixels, anatomy, taste
or motion.

  python3 check_shot_plan.py shot-plan.json

Prints the JSON result. Exit codes: 0 structurally valid (blockers may remain), 1 invalid plan, 2 unreadable input.
"""
import json
import math
import sys

SCOPE = 'Declared planning data only; no media inspection, taste inference, permissions or provider execution.'
UNDEFINED = object()
BRIDGES = {'cut', 'action_match', 'graphic_match', 'occlusion', 'sound_bridge', 'dissolve'}


def is_object(v):
    return isinstance(v, dict)


def nonempty(v):
    return isinstance(v, str) and len(v.strip()) > 0


def known(v):
    return nonempty(v) and v.strip().lower() not in ('unknown', 'unverified')


def finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def positive(v):
    return finite(v) and v > 0


def integer(v):
    return isinstance(v, int) and not isinstance(v, bool) or (isinstance(v, float) and v.is_integer())


def js(v):
    """Format a value the way a JavaScript template literal would."""
    if v is UNDEFINED:
        return 'undefined'
    if v is None:
        return 'null'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, list):
        return ','.join(js(x) for x in v)
    if isinstance(v, dict):
        return '[object Object]'
    return str(v)


def prop(obj, key):
    """obj?.key: the value, or UNDEFINED when obj is not an object or has no such key."""
    return obj.get(key, UNDEFINED) if isinstance(obj, dict) else UNDEFINED


def same(a, b):
    """JavaScript strict equality for JSON values (objects compare by identity)."""
    if a is UNDEFINED or b is UNDEFINED:
        return a is b
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if isinstance(a, (dict, list)) or isinstance(b, (dict, list)):
        return a is b
    return type(a) is type(b) and a == b


def join(values):
    """Array.join(', '): null and undefined become empty strings."""
    return ', '.join('' if v is None or v is UNDEFINED else js(v) for v in values)


def key_of(a, b):
    return json.dumps([None if a is UNDEFINED else a, None if b is UNDEFINED else b], separators=(',', ':'), ensure_ascii=False)


def review_sequence(plan):
    errors, blockers, review = [], [], []

    def result():
        return {'status': 'invalid_plan' if errors else 'structurally_valid_plan',
                'execution_readiness': 'blocked' if errors or blockers else 'unverified', 'observed_quality': 'uninspected',
                'errors': errors, 'blockers': blockers, 'human_review': review, 'evidence_scope': SCOPE}

    if not is_object(plan) or not isinstance(plan.get('shots'), list) or not plan['shots'] or not isinstance(plan.get('bridges'), list):
        errors.append('A nonempty shot list and a bridge list are required.')
        return result()
    shots, bridges = plan['shots'], plan['bridges']
    target = plan.get('target_duration_s', UNDEFINED)
    if not positive(target):
        errors.append('Target duration must be a positive number of seconds.')
    ids = []
    for shot in shots:
        if not is_object(shot):
            errors.append('Every shot must be an object.')
            continue
        get = lambda k: shot.get(k, UNDEFINED)
        sid = js(get('id'))
        if not known(get('id')) or any(same(seen, get('id')) for seen in ids):
            errors.append('Shot IDs must be known and unique.')
        ids.append(get('id'))
        start, end = get('start_s'), get('end_s')
        if not finite(start) or start < 0 or not finite(end) or end <= start:
            errors.append(f'{sid}: invalid edit interval.')
        if get('timing_basis') not in ('proposed', 'user_supplied', 'measured'):
            errors.append(f'{sid}: timing basis is required.')
        if get('timing_basis') == 'measured' and not known(get('timing_evidence')):
            errors.append(f'{sid}: measured timing requires observed evidence.')
        if not known(get('action')) or not known(get('entry_state')) or not known(get('exit_state')):
            errors.append(f'{sid}: describe an action and entry/exit states.')
        for key in ('primary_actions', 'camera_moves'):
            if not integer(get(key)) or get(key) < 0:
                errors.append(f'{sid}: {key} must be a nonnegative integer.')
        busy = any(finite(get(k)) and get(k) > 1 for k in ('primary_actions', 'camera_moves'))
        if busy and not known(get('complexity_reason')):
            review.append(f'{sid}: simplify the action/camera or document why the complexity is readable.')
        if get('continuity_requirement') not in ('strict', 'approximate'):
            errors.append(f'{sid}: preserve an explicit continuity requirement.')
        required, bound = get('required_refs'), get('bound_refs')
        if not isinstance(required, list) or not isinstance(bound, list):
            errors.append(f'{sid}: reference inventories are required, even when empty.')
            continue
        if any(not known(r) for r in required) or len({json.dumps(r) for r in required}) != len(required):
            errors.append(f'{sid}: required reference aliases must be known and unique.')
        if any(not known(r) for r in bound):
            errors.append(f'{sid}: bound reference aliases must be known.')
        missing = [r for r in required if not any(same(r, b) for b in bound)]
        if missing:
            blockers.append(f"{sid}: unresolved required references: {join(missing)}. Requirement remains {js(get('continuity_requirement'))}.")
        if get('continuity_requirement') == 'strict' and not required:
            blockers.append(f'{sid}: strict requirement lacks a declared source carrier.')
        duration = get('generation_duration_s')
        if 'generation_duration_s' in shot and not positive(duration):
            errors.append(f'{sid}: source clip duration, when supplied, must be positive.')
        if positive(duration) and finite(start) and finite(end) and end - start > duration:
            errors.append(f'{sid}: edit interval exceeds declared source clip duration.')
    first, last = shots[0], shots[-1]
    first_start = first.get('start_s', UNDEFINED) if is_object(first) else UNDEFINED
    if not (finite(first_start) and first_start == 0):
        errors.append('Timeline must start at zero.')
    last_end = last.get('end_s', UNDEFINED) if is_object(last) else UNDEFINED
    if not finite(last_end) or (finite(target) and abs(last_end - target) > 0.000001):
        errors.append('Timeline end must equal target duration.')
    pairs = set()
    for bridge in bridges:
        if not is_object(bridge):
            errors.append('Every bridge must be an object.')
            continue
        b_from, b_to = bridge.get('from', UNDEFINED), bridge.get('to', UNDEFINED)
        index = next((i for i, s in enumerate(shots) if same(prop(s, 'id'), b_from)), -1)
        following = shots[index + 1] if 0 <= index < len(shots) - 1 else UNDEFINED
        if index < 0 or not same(prop(following, 'id'), b_to):
            errors.append('A bridge must join adjacent shot IDs.')
        key = key_of(b_from, b_to)
        if key in pairs:
            errors.append('Duplicate bridge.')
        pairs.add(key)
        if bridge.get('type') not in BRIDGES:
            errors.append(f'{key}: unsupported bridge type.')
        overlap = bridge.get('overlap_s', UNDEFINED)
        if not finite(overlap) or overlap < 0:
            errors.append(f'{key}: overlap must be a nonnegative number.')
        if bridge.get('type') != 'dissolve' and not (finite(overlap) and overlap == 0):
            errors.append(f'{key}: this template permits picture overlap only for a dissolve; audio bridges do not overlap picture intervals.')
        checks = bridge.get('review_checks')
        if not known(bridge.get('relationship')) or not isinstance(checks, list) or not checks or any(not known(c) for c in checks):
            errors.append(f'{key}: state the relationship and observable review checks.')
    for a, b in zip(shots, shots[1:]):
        if not is_object(a) or not is_object(b):
            continue
        bridge = next((v for v in bridges if same(prop(v, 'from'), prop(a, 'id')) and same(prop(v, 'to'), prop(b, 'id'))), None)
        name_a, name_b = js(a.get('id', UNDEFINED)), js(b.get('id', UNDEFINED))
        if bridge is None:
            errors.append(f'{name_a} to {name_b}: missing bridge.')
            continue
        overlap = bridge.get('overlap_s', UNDEFINED)
        a_end, b_start = a.get('end_s', UNDEFINED), b.get('start_s', UNDEFINED)
        if finite(a_end) and finite(b_start) and finite(overlap) and abs(a_end - b_start - overlap) > 0.000001:
            errors.append(f'{name_a} to {name_b}: timeline gap or overlap differs from the declared bridge.')
        if finite(overlap):
            length = lambda s: s.get('end_s') - s.get('start_s') if finite(s.get('end_s')) and finite(s.get('start_s')) else math.nan
            if overlap >= length(a) or overlap >= length(b):
                errors.append(f'{name_a} to {name_b}: overlap consumes an entire shot.')
    if len(bridges) != max(0, len(shots) - 1):
        errors.append('Exactly one picture bridge per adjacent pair is required.')
    review.append('Inspect actual outgoing/incoming media for action phase, screen direction, product state, colour and sound.')
    return result()


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        sys.stderr.write('Usage: python3 check_shot_plan.py <shot-plan.json>\n')
        return 2
    try:
        with open(args[0], encoding='utf-8') as handle:
            plan = json.load(handle)
    except (OSError, ValueError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    result = review_sequence(plan)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    sys.exit(main())
