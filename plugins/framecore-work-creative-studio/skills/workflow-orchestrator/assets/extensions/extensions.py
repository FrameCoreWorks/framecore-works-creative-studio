#!/usr/bin/env python3
"""Studio's recommended extensions: outside repositories reviewed as engines or knowledge next to Studio.

  python3 extensions.py list --host codex                 # what can be added in this host
  python3 extensions.py show rea --host claude_code       # what it gives, rights, requirements and the exact commands
  python3 extensions.py show rea --host codex --json

It only reads the registry and, for `show`, checks the local requirements it can (the Node.js version). It installs
nothing: the printed commands are run only when the user explicitly asks, the plan (dry run) first.
Exit codes: 0 shown, 1 unknown extension or host, 2 bad registry.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REGISTRY = Path(__file__).resolve().parent / 'extensions.json'
HOST_FIELDS = {'native': ('plan', 'install', 'writes', 'verify', 'after', 'remove'),
               'desktop_only': ('plan', 'install', 'writes', 'verify', 'after', 'remove'),
               'not_supported': ('reason',)}
ENTRY_FIELDS = ('id', 'name', 'repository', 'reviewed_commit', 'package', 'license', 'kind', 'role', 'gives', 'studio_uses',
                'not_for', 'requires', 'rights', 'hosts', 'observed', 'update')


def load(path=REGISTRY):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    problems = validate(data)
    if problems:
        raise ValueError('; '.join(problems))
    return data


def validate(data):
    """A registry entry is complete, pinned and covers every host; commands carry the pinned version."""
    problems = []
    if data.get('schema_version') != 1 or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(data.get('checked'))):
        problems.append('schema_version 1 and a checked date')
    hosts = data.get('hosts') or []
    seen = set()
    for entry in data.get('extensions') or []:
        where = str(entry.get('id'))
        if not re.fullmatch(r'[a-z0-9_-]+', where) or where in seen:
            problems.append(f'{where}: id must be unique, lowercase')
        seen.add(where)
        for field in ENTRY_FIELDS:
            if entry.get(field) in (None, '', [], {}):
                problems.append(f'{where}: {field} missing')
        if not re.fullmatch(r'[0-9a-f]{40}', str(entry.get('reviewed_commit'))):
            problems.append(f'{where}: reviewed_commit must be a full commit hash')
        if not str(entry.get('repository', '')).startswith('https://'):
            problems.append(f'{where}: repository must be an https URL')
        pinned = f"{(entry.get('package') or {}).get('name')}@{(entry.get('package') or {}).get('version')}"
        for host in hosts:
            spec = (entry.get('hosts') or {}).get(host)
            if not spec or spec.get('status') not in HOST_FIELDS:
                problems.append(f'{where}: host {host} needs a known status')
                continue
            for field in HOST_FIELDS[spec['status']]:
                if not spec.get(field):
                    problems.append(f'{where}: {host} {field} missing')
            for field in ('plan', 'install', 'verify', 'remove'):
                if spec.get(field) and pinned not in spec[field]:
                    problems.append(f'{where}: {host} {field} must use the pinned {pinned}')
            if spec.get('plan') and '--dry-run' not in spec['plan']:
                problems.append(f'{where}: {host} plan must be a dry run')
    return problems


def version_tuple(text):
    found = re.search(r'(\d+)\.(\d+)\.(\d+)', text or '')
    return tuple(int(v) for v in found.groups()) if found else None


def check_requirement(requirement):
    """The local state of a requirement this script can check; the rest are stated, not checked."""
    if requirement.get('tool') != 'node':
        return {'tool': requirement.get('tool'), 'status': 'not_checked', 'note': requirement.get('note')}
    if not shutil.which('node'):
        return {'tool': 'node', 'status': 'missing', 'note': requirement.get('note')}
    try:
        found = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return {'tool': 'node', 'status': 'missing', 'note': 'node does not run; ' + requirement.get('note', '')}
    have = version_tuple(found)
    fits = have is not None and any(have >= version_tuple(low) and (high is None or have < version_tuple(high)) for low, high in requirement['ranges'])
    return {'tool': 'node', 'status': 'ok' if fits else 'unsupported_version', 'found': found, 'note': requirement.get('note')}


def show(entry, host, check=True):
    spec = entry['hosts'][host]
    report = {key: entry[key] for key in ('id', 'name', 'repository', 'reviewed_commit', 'package', 'license', 'kind', 'role',
                                        'gives', 'studio_uses', 'not_for', 'rights', 'observed')}
    report['host'] = host
    report['status'] = spec['status']
    report['steps'] = {k: v for k, v in spec.items() if k != 'status'}
    report['requirements'] = [check_requirement(r) for r in entry['requires']] if check and spec['status'] != 'not_supported' else entry['requires']
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description="List or show Studio's recommended extensions; installs nothing.")
    parser.add_argument('action', choices=['list', 'show'])
    parser.add_argument('extension', nargs='?')
    parser.add_argument('--host', help='codex, claude_code, claude_apps, chatgpt or chatgpt_work')
    parser.add_argument('--registry', default=str(REGISTRY), help=argparse.SUPPRESS)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        data = load(args.registry)
    except (OSError, ValueError) as error:
        print(f'extensions: bad registry: {error}', file=sys.stderr)
        return 2
    if args.host and args.host not in data['hosts']:
        print(f"extensions: unknown host {args.host}; use one of {', '.join(data['hosts'])}", file=sys.stderr)
        return 1
    entries = {e['id']: e for e in data['extensions']}
    if args.action == 'list':
        rows = [{'id': e['id'], 'name': e['name'], 'role': e['role'], 'gives': e['gives'],
                 'status': e['hosts'][args.host]['status'] if args.host else {h: e['hosts'][h]['status'] for h in data['hosts']}} for e in entries.values()]
        if args.json:
            print(json.dumps({'checked': data['checked'], 'policy': data['policy'], 'extensions': rows}, indent=2, ensure_ascii=False))
        else:
            for row in rows:
                status = row['status'] if isinstance(row['status'], str) else ', '.join(f'{h} {s}' for h, s in row['status'].items())
                print(f"{row['id']}: {row['name']} ({row['role']}; {status})\n  {row['gives']}")
        return 0
    if args.extension not in entries or not args.host:
        print('extensions: show needs a known extension and --host', file=sys.stderr)
        return 1
    report = show(entries[args.extension], args.host)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    print(f"{report['name']} ({report['repository']} at {report['reviewed_commit'][:12]}, {report['package']['name']} {report['package']['version']}, {report['license']})")
    print(f"  gives: {report['gives']}\n  Studio uses it for: {report['studio_uses']}\n  not for: {report['not_for']}\n  rights: {report['rights']}")
    print(f"  {args.host}: {report['status']}")
    for key, value in report['steps'].items():
        print(f'  {key}: {value}')
    for item in report['requirements']:
        print(f"  requires {item.get('tool')}: {item.get('status', 'stated')}" + (f" ({item['found']})" if item.get('found') else '') + f" - {item.get('note')}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
