#!/usr/bin/env python3
"""Check declared asset records and compute change impact. Never opens media."""
import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path


def text(value):
    return isinstance(value, str) and bool(value.strip())


def refs(value):
    return (isinstance(value, list) and all(isinstance(x, dict)
            and text(x.get('id')) and text(x.get('revision')) for x in value))


def validate(data):
    errors, delivery_errors = [], []
    index = {}
    def fail(code, detail):
        errors.append({'code': code, 'detail': detail})
    def result(stale=(), unready=()):
        return {'status': 'FAIL' if errors or delivery_errors else 'PASS',
                'scope': 'Declared manifest consistency only; no file or media inspection.',
                'errors': errors, 'stale_assets': sorted(stale), 'unready_assets': sorted(unready),
                'delivery_errors': delivery_errors}
    if not isinstance(data, dict):
        fail('SCHEMA', 'Manifest must be an object')
        return result()
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        fail('SCHEMA_VERSION', 'Expected integer 1')
    if not text(data.get('project_id')):
        fail('PROJECT_ID', 'Expected a nonempty project ID')
    if not isinstance(data.get('assets'), list) or not isinstance(data.get('deliverables'), list):
        fail('SCHEMA', 'assets and deliverables must be arrays')
        return result()
    for number, item in enumerate(data['assets']):
        label = f'asset[{number}]'
        if not isinstance(item, dict):
            fail('ASSET', label + ' must be an object')
            continue
        if not all(text(item.get(k)) for k in ('id', 'revision', 'kind', 'role')):
            fail('ASSET_FIELDS', label)
            continue
        label = item['id']
        if label in index:
            fail('DUPLICATE_ID', label)
            continue
        index[label] = item
        if item['kind'] not in ('text', 'image', 'audio', 'video', 'board', 'other'):
            fail('KIND', label)
        if item.get('state') not in ('planned', 'present', 'missing'):
            fail('STATE', label)
        if 'locator' not in item or (item['locator'] is not None and not text(item['locator'])):
            fail('LOCATOR', label)
        if item.get('state') == 'present' and not text(item.get('locator')):
            fail('PRESENT_LOCATOR', label)
        digest = item.get('sha256')
        if 'sha256' not in item or (digest is not None and
                (not isinstance(digest, str) or not re.fullmatch('[a-fA-F0-9]{64}', digest))):
            fail('DIGEST', label)
        dependencies = item.get('depends_on')
        if not refs(dependencies):
            fail('DEPENDENCIES', label)
        elif len({x['id'] for x in dependencies}) != len(dependencies):
            fail('DUPLICATE_DEPENDENCY', label)
        prop = item.get('properties')
        if (not isinstance(prop, dict) or not isinstance(prop.get('requested'), dict)
                or not isinstance(prop.get('verified'), dict)
                or not isinstance(prop.get('unknown'), list)
                or not all(text(x) for x in prop.get('unknown', []))):
            fail('PROPERTIES', label)
        else:
            for key, value in prop['verified'].items():
                if (not isinstance(value, dict) or 'value' not in value or value['value'] is None
                        or not text(value.get('method')) or not text(value.get('evidence'))):
                    fail('VERIFIED_EVIDENCE', label + ':' + key)
            if set(prop['verified']) & set(prop['unknown']):
                fail('PROPERTY_CONFLICT', label)
        provenance = item.get('provenance')
        if not isinstance(provenance, dict) or not all(text(provenance.get(k)) for k in ('source', 'rights')):
            fail('PROVENANCE', label)
        review = item.get('review')
        if not isinstance(review, dict) or review.get('status') not in ('not_reviewed', 'accepted', 'changes_required'):
            fail('REVIEW', label)
        elif review['status'] == 'accepted':
            if review.get('reviewed_revision') != item['revision']:
                fail('REVIEW_REVISION', label)
            if (not isinstance(review.get('scope'), list) or not review['scope']
                    or not all(text(x) for x in review['scope']) or not text(review.get('evidence'))):
                fail('REVIEW_EVIDENCE', label)
            basis = review.get('basis')
            if not refs(basis) or not refs(dependencies):
                fail('REVIEW_BASIS', label)
            elif sorted((x['id'], x['revision']) for x in basis) != sorted((x['id'], x['revision']) for x in dependencies):
                fail('REVIEW_BASIS', label)
            if item.get('state') == 'planned':
                fail('REVIEW_AVAILABILITY', label)
    # Do not operate on malformed graphs.
    if errors:
        return result()
    children = {key: set() for key in index}
    remaining = {key: 0 for key in index}
    stale = set()
    unready = {key for key, item in index.items() if item['state'] == 'planned'
               or item['review']['status'] == 'changes_required'}
    for key, item in index.items():
        for dependency in item['depends_on']:
            parent = dependency['id']
            if parent not in index:
                fail('MISSING_DEPENDENCY', key + ' -> ' + parent)
                continue
            children[parent].add(key)
            remaining[key] += 1
            if dependency['revision'] != index[parent]['revision']:
                stale.add(key)
    if errors:
        return result(stale)
    ready = deque(key for key, count in remaining.items() if count == 0)
    visited = 0
    while ready:
        parent = ready.popleft()
        visited += 1
        for child in children[parent]:
            if parent in stale:
                stale.add(child)
            if parent in unready:
                unready.add(child)
            remaining[child] -= 1
            if remaining[child] == 0:
                ready.append(child)
    if visited != len(index):
        fail('DEPENDENCY_CYCLE', 'Dependency graph must be acyclic')
    selected = set()
    for selection in data['deliverables']:
        if (not isinstance(selection, dict) or not text(selection.get('id'))
                or selection.get('purpose') not in ('draft', 'reference', 'final')):
            fail('DELIVERABLE', 'Expected {id, purpose: draft|reference|final}')
            continue
        key = selection['id']
        if key in selected:
            fail('DUPLICATE_DELIVERABLE', key)
        selected.add(key)
        if key not in index:
            fail('UNKNOWN_DELIVERABLE', key)
            continue
        if selection['purpose'] == 'final':
            item = index[key]
            for condition, code in [(item['state'] != 'present', 'NOT_PRESENT'),
                                    (item['review']['status'] != 'accepted', 'NOT_ACCEPTED'),
                                    (key in stale, 'STALE_DEPENDENCY'),
                                    (key in unready, 'UNRESOLVED_INPUT')]:
                if condition:
                    delivery_errors.append({'id': key, 'code': code})
    return result(stale, unready)


def impact(data, changed):
    report = validate(data)
    if report['errors']:
        return {'status': 'FAIL', 'errors': report['errors'], 'affected_assets': []}
    index = {item['id']: item for item in data['assets']}
    unknown = sorted(set(changed) - set(index))
    if unknown:
        return {'status': 'FAIL', 'errors': [{'code': 'UNKNOWN_CHANGED_ID', 'detail': unknown}], 'affected_assets': []}
    children = {key: set() for key in index}
    for key, item in index.items():
        for parent in item['depends_on']:
            children[parent['id']].add(key)
    seen = set(changed)
    queue = deque(changed)
    while queue:
        for child in children[queue.popleft()]:
            if child not in seen:
                seen.add(child)
                queue.append(child)
    return {'status': 'PASS', 'scope': 'Potential change impact; no files changed.',
            'changed_assets': sorted(set(changed)), 'affected_assets': sorted(seen - set(changed))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    check = sub.add_parser('check')
    check.add_argument('manifest')
    affected = sub.add_parser('impact')
    affected.add_argument('manifest')
    affected.add_argument('changed_ids', nargs='+')
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
        report = validate(data) if args.command == 'check' else impact(data, args.changed_ids)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        report = {'status': 'FAIL', 'errors': [{'code': 'INPUT', 'detail': str(error)}]}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
