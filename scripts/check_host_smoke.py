#!/usr/bin/env python3
"""Check host smoke-set records (docs/host-smoke-set.md) for complete, honest fields.

Every verification/host-smoke-*.json except the template must name the plugin version,
date, tester, client and reasoning setting, list the eight cases SM1 to SM8 once each
with an allowed result, and give an observation and evidence for every case that ran.
Exit 0 when all records pass, 1 with the problems listed.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CASE_IDS = [f'SM{n}' for n in range(1, 9)]
RESULTS = {'PASS_REPORTED', 'FAIL_REPORTED', 'PASS_OBSERVED', 'FAIL_OBSERVED', 'PARTIAL', 'NOT_RUN'}
AVAILABILITY = {'yes', 'no', 'unknown'}


def problems(record, name):
    found = []
    if record.get('schema') != 'host-smoke/1':
        found.append(f'{name}: schema must be host-smoke/1')
    template = record.get('template') is True
    if not template:
        if not re.fullmatch(r'\d+\.\d+\.\d+', str(record.get('plugin_version', ''))):
            found.append(f'{name}: plugin_version must be the tested release, for example 1.42.0')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(record.get('date', ''))):
            found.append(f'{name}: date must be YYYY-MM-DD')
        for field in ('tester', 'client', 'reasoning_setting', 'version_read_back'):
            if not str(record.get(field, '')).strip():
                found.append(f'{name}: {field} is empty')
    for field in ('code_execution', 'web_search'):
        if record.get(field) not in AVAILABILITY:
            found.append(f'{name}: {field} must be yes, no or unknown')
    cases = record.get('cases')
    if not isinstance(cases, list) or [c.get('id') for c in cases if isinstance(c, dict)] != CASE_IDS:
        found.append(f'{name}: cases must be SM1 to SM8 in order, once each')
        return found
    for case in cases:
        where = f"{name} {case['id']}"
        result = case.get('result')
        if result not in RESULTS:
            found.append(f'{where}: result must be one of {", ".join(sorted(RESULTS))}')
            continue
        if template:
            continue
        if result == 'NOT_RUN':
            if not str(case.get('notes', '')).strip():
                found.append(f'{where}: a case that did not run needs the reason in notes')
            continue
        if not str(case.get('observed', '')).strip():
            found.append(f'{where}: describe what was observed')
        if not isinstance(case.get('evidence'), list) or not case['evidence']:
            found.append(f'{where}: name the evidence (screenshot, transcript or file with hash)')
        if result == 'PARTIAL' and not str(case.get('notes', '')).strip():
            found.append(f'{where}: name the pass criteria that were not met')
    if not isinstance(record.get('unknown'), list):
        found.append(f'{name}: unknown must be a list')
    return found


def main(argv):
    folder = pathlib.Path(argv[1]) if len(argv) > 1 else ROOT / 'verification'
    paths = sorted(folder.glob('host-smoke-*.json'))
    if not any(p.name == 'host-smoke-template.json' for p in paths):
        print('Missing verification/host-smoke-template.json')
        return 1
    found = []
    for path in paths:
        try:
            record = json.loads(path.read_text())
        except (OSError, ValueError) as error:
            found.append(f'{path.name}: not valid JSON ({error})')
            continue
        if path.name == 'host-smoke-template.json' and record.get('template') is not True:
            found.append('host-smoke-template.json: template must be true')
        if path.name != 'host-smoke-template.json' and record.get('template') is True:
            found.append(f'{path.name}: a filled record must not be marked as the template')
        found.extend(problems(record, path.name))
    for line in found:
        print(line)
    if not found:
        print(f'Host smoke records pass: {len(paths) - 1} filled, template valid.')
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
