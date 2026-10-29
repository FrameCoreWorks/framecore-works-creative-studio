#!/usr/bin/env python3
"""Check a companion's framecore-task-result/1 before Studio uses it: shared schema, companion registry, output bytes.

Re-hashes every declared output and records each one as not_reviewed; it never opens media or judges quality.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[2] / 'pipeline-core' / 'assets'
SCHEMA = ASSETS / 'companion-contract.schema.json'
REGISTRY = ASSETS / 'companion-registry.json'
TYPES = {'object': dict, 'array': list, 'string': str, 'boolean': bool, 'null': type(None)}


def _is(value, name):
    if name == 'integer':
        return isinstance(value, int) and not isinstance(value, bool)
    if name == 'number':
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, TYPES[name])


def schema_errors(value, rule, root, path='result'):
    """The JSON Schema keywords the shared contract uses; an empty list means the value conforms."""
    errors = []
    if '$ref' in rule:
        rule = root['$defs'][rule['$ref'].rsplit('/', 1)[-1]]
    if 'anyOf' in rule:
        if all(schema_errors(value, r, root, path) for r in rule['anyOf']):
            errors.append(f'{path}: matches no allowed shape')
        return errors
    if 'const' in rule and value != rule['const']:
        errors.append(f'{path}: expected {rule["const"]!r}')
    if 'enum' in rule and value not in rule['enum']:
        errors.append(f'{path}: {value!r} not in {rule["enum"]}')
    if 'type' in rule:
        names = rule['type'] if isinstance(rule['type'], list) else [rule['type']]
        if not any(_is(value, n) for n in names):
            return errors + [f'{path}: expected {"/".join(names)}']
    if isinstance(value, str):
        if len(value) < rule.get('minLength', 0):
            errors.append(f'{path}: too short')
        if 'pattern' in rule and not re.fullmatch(rule['pattern'].lstrip('^').rstrip('$'), value):
            errors.append(f'{path}: does not match {rule["pattern"]}')
    if _is(value, 'number') and 'minimum' in rule and value < rule['minimum']:
        errors.append(f'{path}: below {rule["minimum"]}')
    if isinstance(value, dict):
        errors += [f'{path}: missing {k}' for k in rule.get('required', []) if k not in value]
        for key, sub in rule.get('properties', {}).items():
            if key in value:
                errors += schema_errors(value[key], sub, root, f'{path}.{key}')
    if isinstance(value, list) and 'items' in rule:
        for i, item in enumerate(value):
            errors += schema_errors(item, rule['items'], root, f'{path}[{i}]')
    return errors


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def check(doc, base):
    errors = []
    def fail(code, detail):
        errors.append({'code': code, 'detail': detail})
    root = json.loads(SCHEMA.read_text(encoding='utf-8'))
    for problem in schema_errors(doc, root['$defs']['result'], root):
        fail('SCHEMA', problem)
    if errors:
        return {'status': 'FAIL', 'errors': errors, 'ledger_entry': None}
    provider = doc['provider']
    companion = json.loads(REGISTRY.read_text(encoding='utf-8'))['companions'].get(provider['plugin'])
    capability = (companion or {}).get('capabilities', {}).get(provider.get('capability'))
    if not capability:
        fail('UNKNOWN_PROVIDER', f'{provider["plugin"]}/{provider.get("capability")} is not a registered companion capability')
    elif provider.get('operation') not in capability['operations'] + capability.get('separate_tools', []):
        fail('UNKNOWN_PROVIDER', f'{provider.get("operation")!r} is not a {provider["plugin"]}/{provider["capability"]} operation')
    notes = []
    reviewed = (companion or {}).get('reviewed', {}).get('version')
    if capability and reviewed and provider.get('version') != reviewed:
        notes.append(f'{provider["plugin"]} {provider.get("version")} ran; Studio reviewed {reviewed}')
    outputs = []
    for item in doc['outputs']:
        path = Path(item['path'])
        path = (path if path.is_absolute() else base / path).resolve()
        if not path.is_file():
            fail('OUTPUT_MISSING', str(path))
            continue
        try:
            actual, size = sha256(path), path.stat().st_size
        except OSError as exc:
            fail('OUTPUT_UNREADABLE', f'{path}: {exc}')
            continue
        if actual != item['sha256']:
            fail('HASH_MISMATCH', f'{path}: declared {item["sha256"]}, actual {actual}')
            continue
        if item.get('bytes') is not None and item['bytes'] != size:
            fail('SIZE_MISMATCH', f'{path}: declared {item["bytes"]} bytes, actual {size}')
            continue
        outputs.append({'path': str(path), 'sha256': actual, 'bytes': size,
                        'media_kind': item.get('media_kind'), 'review': 'not_reviewed'})
    entry = {'task_id': doc['task_id'], 'provider': provider, 'status': doc['status'],
             'placeable': doc['status'] in ('succeeded', 'partial') and bool(outputs) and not errors,
             'readiness': doc['readiness']['state'], 'outputs': outputs, 'warnings': doc['warnings'],
             'errors': doc['errors'], 'unexecuted_checks': doc['unexecuted_checks'], 'intake_warnings': notes}
    return {'status': 'FAIL' if errors else 'PASS',
            'scope': 'Contract shape, registered provider and output bytes only; no media inspection or quality review.',
            'errors': errors, 'ledger_entry': None if errors else entry}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='cmd', required=True)
    one = sub.add_parser('check', help='check one result file')
    one.add_argument('result')
    one.add_argument('--base', help='folder the companion ran in; relative output paths resolve against it '
                     '(default: the folder holding the result file)')
    one.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    path = Path(args.result)
    try:
        doc = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        print(f'companion_intake: cannot read {path}: {exc}', file=sys.stderr)
        return 2
    report = check(doc, Path(args.base).resolve() if args.base else path.resolve().parent)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(report['status'])
        for error in report['errors']:
            print(f'  {error["code"]}: {error["detail"]}')
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
