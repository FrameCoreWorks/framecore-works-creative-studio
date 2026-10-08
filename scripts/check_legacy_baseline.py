#!/usr/bin/env python3
"""Compare the historical legacy suite with its recorded baseline, so a new legacy failure cannot hide among the known ones.

The legacy validator (validate-package.mjs, run through validate-studio.mjs --legacy) and package.test.mjs predate the
conditional research policy and fail by design. This script records exactly which validator errors and which tests fail
(tests/legacy-baseline.json) and fails when the current run differs in either direction: a new error or failure, or a
known one that disappeared. After an intended change, regenerate the baseline with --write and say why in the commit.

  python3 scripts/check_legacy_baseline.py          # compare; exit 0 when identical, 1 on any difference
  python3 scripts/check_legacy_baseline.py --write  # record the current run as the baseline
"""
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'framecore-work-creative-studio'
BASELINE = ROOT / 'tests' / 'legacy-baseline.json'


def current():
    run = subprocess.run(['node', str(PLUGIN / 'scripts/validate-studio.mjs'), '--legacy'], cwd=ROOT, capture_output=True, text=True, check=False)
    try:
        legacy = json.loads(run.stdout)['legacy']
        errors = legacy['report']['errors']
    except (ValueError, KeyError, TypeError) as error:
        raise SystemExit(f'The legacy validator gave no readable report ({error}): {run.stderr.strip()[:500]}')
    tests = subprocess.run(['node', '--test', str(PLUGIN / 'tests/package.test.mjs')], cwd=PLUGIN, capture_output=True, text=True, check=False)
    failing = re.findall(r'^not ok \d+ - (.+)$', tests.stdout, re.M)
    total = re.search(r'^# tests (\d+)$', tests.stdout, re.M)
    if not total:
        raise SystemExit('package.test.mjs gave no test count: ' + (tests.stderr.strip() or tests.stdout.strip())[:500])
    return {'validator_errors': sorted(errors), 'failing_tests': sorted(failing), 'tests': int(total.group(1))}


def main(argv):
    now = current()
    if '--write' in argv:
        BASELINE.write_text(json.dumps({
            'scope': 'Historical legacy suite: validate-package.mjs errors and failing package.test.mjs tests, recorded so that any change is visible. Not a release gate for the current checks.',
            **now}, indent=2, ensure_ascii=False) + '\n')
        print(f"Baseline written: {len(now['validator_errors'])} validator errors, {len(now['failing_tests'])} of {now['tests']} tests failing.")
        return 0
    if not BASELINE.exists():
        raise SystemExit(f'No baseline at {BASELINE.relative_to(ROOT)}; record one with --write')
    known = json.loads(BASELINE.read_text())
    differences = []
    for key in ('validator_errors', 'failing_tests'):
        # Counted as multisets, so a message that starts to appear twice is a difference too.
        new = sorted((Counter(now[key]) - Counter(known[key])).elements())
        gone = sorted((Counter(known[key]) - Counter(now[key])).elements())
        differences += [f'new in {key}: {item}' for item in new] + [f'no longer in {key}: {item}' for item in gone]
    if now['tests'] != known['tests']:
        differences.append(f"package.test.mjs now has {now['tests']} tests, the baseline {known['tests']}")
    if differences:
        print('Legacy suite differs from tests/legacy-baseline.json:')
        print('\n'.join('- ' + line for line in differences))
        print('Fix a new failure, or after an intended change run: python3 scripts/check_legacy_baseline.py --write')
        return 1
    print(f"Legacy suite matches its baseline: {len(now['validator_errors'])} known validator errors, {len(now['failing_tests'])} of {now['tests']} tests failing as recorded.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
