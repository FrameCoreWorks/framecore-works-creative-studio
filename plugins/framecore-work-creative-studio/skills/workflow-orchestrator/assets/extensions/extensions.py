#!/usr/bin/env python3
"""Studio's recommended extensions: outside repositories reviewed as engines or knowledge next to Studio.

  python3 extensions.py list --host codex                 # what can be added in this host
  python3 extensions.py show rea --host claude_code       # what it gives, rights, requirements and the exact commands
  python3 extensions.py show rea --host codex --json
  python3 extensions.py list --category tts --host claude_code   # the voice engines a user can choose from
  python3 extensions.py catalog --host claude_code         # every entry with its description and how it installs here

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
               'not_supported': ('reason',),
               'manual': ('manual_steps',),
               'catalog_manual': ('manual_steps', 'writes', 'verify', 'after', 'remove')}
ENTRY_FIELDS = ('id', 'name', 'repository', 'license', 'kind', 'role', 'gives', 'studio_uses',
                'not_for', 'requires', 'rights', 'hosts', 'observed', 'update')
STEP_ORDER = ('plan', 'install', 'verify', 'after', 'remove')


def pin_of(entry):
    """What every command must carry: the package version, the reviewed commit or, for an unversioned download, its SHA-256."""
    package = entry.get('package')
    if package:
        return f"{package['name']}=={package['version']}" if package.get('registry') == 'pypi' else f"{package['name']}@{package['version']}"
    if entry.get('archive'):
        return str(entry['archive'].get('sha256'))
    return str(entry.get('reviewed_commit'))


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
    priorities = {'first': 0, 'second': 0}
    for entry in data.get('extensions') or []:
        where = str(entry.get('id'))
        if not re.fullmatch(r'[a-z0-9_-]+', where) or where in seen:
            problems.append(f'{where}: id must be unique, lowercase')
        seen.add(where)
        priority = entry.get('recommendation_priority')
        if priority is not None and priority not in priorities:
            problems.append(f'{where}: unknown recommendation_priority')
        elif priority:
            priorities[priority] += 1
        for field in ENTRY_FIELDS:
            if entry.get(field) in (None, '', [], {}):
                problems.append(f'{where}: {field} missing')
        archive = entry.get('archive')
        if archive:
            if not str(archive.get('url', '')).startswith('https://') or not re.fullmatch(r'[0-9a-f]{64}', str(archive.get('sha256'))):
                problems.append(f'{where}: archive needs an https url and a SHA-256')
        elif not re.fullmatch(r'[0-9a-f]{40}', str(entry.get('reviewed_commit'))):
            problems.append(f'{where}: reviewed_commit must be a full commit hash')
        if not str(entry.get('repository', '')).startswith('https://'):
            problems.append(f'{where}: repository must be an https URL')
        package = entry.get('package')
        pinned = pin_of(entry)
        npm_pin = bool(package) and package.get('registry') == 'npm'
        for host in hosts:
            spec = (entry.get('hosts') or {}).get(host)
            if not spec or spec.get('status') not in HOST_FIELDS:
                problems.append(f'{where}: host {host} needs a known status')
                continue
            for field in HOST_FIELDS[spec['status']]:
                if not spec.get(field):
                    problems.append(f'{where}: {host} {field} missing')
            if spec['status'] == 'catalog_manual':
                if 'plan' in spec or 'install' in spec:
                    problems.append(f'{where}: {host} catalog_manual cannot contain plan or install')
                continue  # Reviewed source is provenance, not a pin on a marketplace-managed version.
            for field in ('plan', 'install') + (('verify', 'remove') if npm_pin else ()):
                if spec.get(field) and pinned not in spec[field]:
                    problems.append(f'{where}: {host} {field} must use the pinned {pinned}')
            plan = (spec.get('plan') or '').replace('npx -y ', 'npx ')   # npx's own -y only skips its download prompt
            reads_only = any(mark in plan for mark in ('--dry-run', '--list', ' checkout ', 'unzip -l '))
            if plan and (not reads_only or re.search(r'(^|\s)(-y|--yes)(\s|$)|plugin install', plan)):
                problems.append(f'{where}: {host} plan must be a dry run')
            if spec.get('install') and re.search(r'(^|\s)(-y|--yes)(\s|$)', spec['install'].replace('npx -y ', 'npx ')) and package is None:
                problems.append(f'{where}: {host} install must keep the installer\'s own confirmation')
    for priority, count in priorities.items():
        if count > 1:
            problems.append(f'only one {priority} recommendation is allowed')
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
    report = {key: entry.get(key) for key in ('id', 'name', 'repository', 'reviewed_commit', 'archive', 'package', 'license', 'kind',
                                            'role', 'gives', 'studio_uses', 'not_for', 'rights', 'observed', 'recommendation_priority')}
    report['pinned'] = pin_of(entry)
    report['host'] = host
    report['status'] = spec['status']
    report['steps'] = {k: v for k, v in spec.items() if k != 'status'}
    report['requirements'] = [check_requirement(r) for r in entry['requires']] if check and spec['status'] != 'not_supported' else entry['requires']
    return report


def catalog(data, host):
    """Every entry for one host: what it is and does, and how it is added there (the steps, never run here)."""
    rows = []
    for entry in data['extensions']:
        spec = entry['hosts'][host]
        how = {k: spec[k] for k in HOST_FIELDS['catalog_manual']} if spec['status'] == 'catalog_manual' else \
            {k: spec[k] for k in STEP_ORDER if spec.get(k)} if spec['status'] in ('native', 'desktop_only') else \
            {'manual_steps': spec['manual_steps']} if spec['status'] == 'manual' else {'reason': spec['reason']}
        rows.append({'id': entry['id'], 'name': entry['name'], 'repository': entry['repository'], 'pinned': pin_of(entry),
                     'license': entry['license'], 'role': entry['role'], 'category': entry.get('category'), 'gives': entry['gives'],
                     'studio_uses': entry['studio_uses'], 'status': spec['status'], 'how': how,
                     'recommendation_priority': entry.get('recommendation_priority'),
                     'other_hosts': {h: entry['hosts'][h]['status'] for h in data['hosts'] if h != host}})
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description="List or show Studio's recommended extensions; installs nothing.")
    parser.add_argument('action', choices=['list', 'show', 'catalog'])
    parser.add_argument('extension', nargs='?')
    parser.add_argument('--host', help='codex, claude_code, claude_apps, chatgpt or chatgpt_work')
    parser.add_argument('--category', help='only one category, for example tts')
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
    if args.action == 'catalog':
        if not args.host:
            print('extensions: catalog needs --host', file=sys.stderr)
            return 1
        rows = [r for r in catalog(data, args.host) if not args.category or r['category'] == args.category]
        if args.json:
            print(json.dumps({'checked': data['checked'], 'host': args.host, 'policy': data['policy'], 'extensions': rows}, indent=2, ensure_ascii=False))
            return 0
        heading = None
        for row in sorted(rows, key=lambda r: r['category'] or ''):
            if row['category'] != heading:
                heading = row['category']
                print(f"\n[{heading}]")
            print(f"{row['name']} - {row['repository']} ({row['license']}, {row['role']}; {args.host}: {row['status']})")
            print(f"  gives: {row['gives']}\n  in Studio: {row['studio_uses']}")
            if row.get('recommendation_priority'):
                print(f"  recommendation: {row['recommendation_priority']}")
            for key, value in row['how'].items():
                print(f'  {key}: {value}')
            print('  other hosts: ' + ', '.join(f'{h} {s}' for h, s in row['other_hosts'].items()))
        return 0
    entries = {e['id']: e for e in data['extensions'] if not args.category or e.get('category') == args.category or args.action == 'show'}
    if args.action == 'list':
        rows = [{'id': e['id'], 'name': e['name'], 'role': e['role'], 'gives': e['gives'],
                 'recommendation_priority': e.get('recommendation_priority'),
                 'status': e['hosts'][args.host]['status'] if args.host else {h: e['hosts'][h]['status'] for h in data['hosts']}} for e in entries.values()]
        if args.json:
            print(json.dumps({'checked': data['checked'], 'policy': data['policy'], 'extensions': rows}, indent=2, ensure_ascii=False))
        else:
            for row in rows:
                status = row['status'] if isinstance(row['status'], str) else ', '.join(f'{h} {s}' for h, s in row['status'].items())
                print(f"{row['id']}: {row['name']} ({row['role']}; {status})\n  {row['gives']}")
                if row.get('recommendation_priority'):
                    print(f"  recommendation: {row['recommendation_priority']}")
        return 0
    if args.extension not in entries or not args.host:
        print('extensions: show needs a known extension and --host', file=sys.stderr)
        return 1
    report = show(entries[args.extension], args.host)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    package = f", {report['package']['name']} {report['package']['version']}" if report.get('package') else ''
    print(f"{report['name']} ({report['repository']} at {report['pinned'][:12]}{package}, {report['license']})")
    print(f"  gives: {report['gives']}\n  Studio uses it for: {report['studio_uses']}\n  not for: {report['not_for']}\n  rights: {report['rights']}")
    print(f"  {args.host}: {report['status']}")
    if report.get('recommendation_priority'):
        print(f"  recommendation: {report['recommendation_priority']}")
    for key, value in report['steps'].items():
        print(f'  {key}: {value}')
    for item in report['requirements']:
        print(f"  requires {item.get('tool')}: {item.get('status', 'stated')}" + (f" ({item['found']})" if item.get('found') else '') + f" - {item.get('note')}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
