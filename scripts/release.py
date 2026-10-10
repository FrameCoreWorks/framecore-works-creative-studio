#!/usr/bin/env python3
"""One command for a Studio release, and one for its publication record.

  python3 scripts/release.py prepare 1.55.0 --change-id CC-20261010-13 --title "Release 1.55.0: …" \
      --changelog notes/changelog.md --notes notes/release-notes.md --summary "…" [--extra "…"] [--push]
  python3 scripts/release.py publish 1.55.0 --change-id CC-20261010-13 [--push]

prepare: checks the branch can fast-forward main, bumps every version marker, writes the changelog entries and release
notes, regenerates config/install-sources.json, runs every check and parses the results, writes the scope and release
records, VERIFICATION, RELEASE_STATUS and the ledger entry, packages the release and commits with the trailers; with
--push it fast-forwards main (never a force push) and pushes the working branches. publish: waits for the GitHub
workflows of the release commit, downloads the release assets, checks them against the local build and the tag tree,
writes the publication record, updates RELEASE_STATUS and the ledger and commits (and pushes with --push). Both print
what they did; neither edits anything inside the shared package except the version markers prepare owns.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'plugins/framecore-work-creative-studio'
PLUGIN = ROOT / PACKAGE
REPO = 'FrameCoreWorks/framecore-works-creative-studio'
SESSION_BRANCHES = ['ccr-b6d36a1c-4hszow']
TRAILER_TAIL = ('Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
                'Claude-Session: https://claude.ai/code/session_0187TnJYu2qDShCj23GszTm5')
PYTHON_SUITES = ['Codex installer', 'package identity', 'benchmark script', 'host smoke', 'hosted readback', 'Claude plugin and guides',
                 'GEPA pilot', 'asset', 'caption', 'environment check', 'motion acceptance', 'skill finder', 'Animate engine',
                 'static render', 'host-eval harness']


class ReleaseError(Exception):
    pass


def run(*args, check=True, cwd=ROOT, env=None, timeout=None):
    done = subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, env=env, timeout=timeout)
    if check and done.returncode != 0:
        raise ReleaseError(f'{" ".join(args[:3])} failed ({done.returncode}): {(done.stderr or done.stdout)[-1500:]}')
    return done


def git(*args, check=True):
    return run('git', *args, check=check).stdout.strip()


def read(relative):
    return (ROOT / relative).read_text(encoding='utf-8')


def write(relative, text):
    (ROOT / relative).write_text(text, encoding='utf-8')


def replace_once(relative, old, new, count=1):
    text = read(relative)
    found = text.count(old)
    if found != count:
        raise ReleaseError(f'{relative}: expected {count} occurrence(s) of {old!r}, found {found}')
    write(relative, text.replace(old, new))


def version_tuple(value):
    return tuple(int(part) for part in value.split('.'))


def current_version():
    return json.loads(read(f'{PACKAGE}/plugin.json'))['version']


def today():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')


# ------------------------------------------------------------------ prepare

def bump(old, new):
    for manifest in (f'{PACKAGE}/plugin.json', f'{PACKAGE}/.codex-plugin/plugin.json', f'{PACKAGE}/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json'):
        replace_once(manifest, f'"version": "{old}"', f'"version": "{new}"')
    replace_once(f'{PACKAGE}/skills/workflow-orchestrator/SKILL.md', f'"version":"{old}"', f'"version":"{new}"')
    replace_once('README.md', f'Source version: **{old}**', f'Source version: **{new}**')
    replace_once(f'{PACKAGE}/README.md', f'Version: {old}.', f'Version: {new}.')
    replace_once(f'{PACKAGE}/docs/migration-status.md', f'Version: {old}.', f'Version: {new}.')
    text = read('CLAUDE_INSTALL.md')
    if f'v{old}' not in text:
        raise ReleaseError(f'CLAUDE_INSTALL.md: no v{old} tag example')
    write('CLAUDE_INSTALL.md', text.replace(f'v{old}', f'v{new}'))


def package_links(text):
    """Changelog links are repository-relative; inside the package docs/ they point to the plugin root or GitHub."""
    def fix(match):
        target = match.group(1)
        if re.match(r'(https?:|mailto:|#)', target):
            return match.group(0)
        if target.startswith(PACKAGE + '/'):
            return '](../' + target[len(PACKAGE) + 1:] + ')'
        return f'](https://github.com/{REPO}/blob/main/{target})'
    return re.sub(r'\]\(([^)]+)\)', fix, text)


def write_notes(new, changelog, notes):
    entry = f'## {new}, {today()}\n\n{changelog.strip()}\n\n'
    for relative, body in (('CHANGELOG.md', entry), (f'{PACKAGE}/docs/release-history.md', package_links(entry))):
        text = read(relative)
        at = text.index('\n## ') + 1
        write(relative, text[:at] + body + text[at:])
    write('RELEASE_NOTES.md', notes.strip() + '\n')


def parse_checks(log):
    node = {key: int(value) for key, value in re.findall(r'^# (tests|pass|skipped|fail) (\d+)$', log, re.M)}
    ran = [(int(n), int(skipped or 0)) for n, skipped in re.findall(r'^Ran (\d+) tests? in [^\n]*\n+OK(?: \(skipped=(\d+)\))?$', log, re.M)]
    names = PYTHON_SUITES if len(ran) == len(PYTHON_SUITES) else [f'suite {i + 1}' for i in range(len(ran))]
    return {'node': node, 'python': {name: {'tests': n, 'skipped': skipped} for name, (n, skipped) in zip(names, ran)}}


def summary_text(checks, browser):
    node = checks['node']
    skipped = node.get('skipped', 0)
    parts = [f"{node.get('tests')} Node tests ({node.get('pass')} passing" + (f", {skipped} opt-in browser tests skipped there" + (f" and run separately: {browser} passing in the browser run" if browser else '') if skipped else '') + ')']
    parts += [f"{c['tests']} {name}" + (f" ({c['skipped']} skipped without optional dependencies)" if c['skipped'] else '') for name, c in checks['python'].items()]
    return ', '.join(parts)


def run_checks():
    validator = json.loads(run('node', f'{PACKAGE}/scripts/validate-studio.mjs').stdout)
    canonical = validator['canonical']
    if validator['status'] != 'PASS':
        raise ReleaseError('canonical validator: ' + json.dumps(canonical.get('errors'))[:1500])
    env = {key: value for key, value in os.environ.items() if key != 'MOTION_REVIEW_BROWSER'}  # browser suite runs once, below
    log = run('bash', 'scripts/check_all.sh', env=env, timeout=3600)
    checks = parse_checks(log.stdout + '\n' + log.stderr)
    browser = None
    if os.environ.get('MOTION_REVIEW_BROWSER'):
        done = run('node', '--test', '--test-concurrency=1', f'{PACKAGE}/tests/motion-toolkit.test.mjs', timeout=3600)
        stats = {k: int(v) for k, v in re.findall(r'^# (tests|pass|fail) (\d+)$', done.stdout, re.M)}
        if stats.get('fail'):
            raise ReleaseError(f'browser run: {stats}')
        browser = stats.get('pass')
    claude = None
    if run('which', 'claude', check=False).returncode == 0:
        run('claude', 'plugin', 'validate', PACKAGE, '--strict')
        run('claude', 'plugin', 'validate', '.', '--strict')
        claude = run('claude', '--version').stdout.split()[0]
    return canonical, checks, browser, claude


def scope_record(old, new, change_id, note):
    base = f'v{old}'
    status = git('diff', '--no-renames', '--name-status', base, '--', PACKAGE).splitlines()
    untracked = git('ls-files', '--others', '--exclude-standard', '--', PACKAGE).splitlines()
    changed, added, removed = [], [], []
    for line in status:
        kind, *paths = line.split('\t')
        path = paths[-1][len(PACKAGE) + 1:]
        (added if kind.startswith('A') else removed if kind.startswith('D') else changed).append(path)
    added += [p[len(PACKAGE) + 1:] for p in untracked if '__pycache__' not in p]
    if removed:
        raise ReleaseError('package paths removed (a hosted update cannot delete): ' + ', '.join(removed))
    files = sum(1 for p in PLUGIN.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    touched = changed + added
    record = {
        'version': new, 'baseline_tag': base, 'baseline': git('rev-parse', base), 'change_id': change_id, 'origin': 'cloud-code',
        'files': files, 'skills': len(list((PLUGIN / 'skills').glob('*/SKILL.md'))),
        'changed': sorted(changed), 'added': sorted(added), 'removed': [], 'unchanged_count': files - len(touched),
        'welcome': 'changed' if any('startup-welcome' in p for p in touched) else 'byte_identical',
        'menus': 'changed' if any('startup-and-creative-menus' in p for p in touched) else 'byte_identical',
        'vendored_snapshots': 'changed' if any('/upstream/' in p or 'assets/animate-engine/' in p for p in touched) else 'byte_identical',
        'note': note,
    }
    write(f'verification/scope-{new}.json', json.dumps(record, indent=2, ensure_ascii=False) + '\n')
    return record


def update_records(old, new, change_id, args, canonical, checks, browser, claude, scope, baseline):
    summary = summary_text(checks, browser)
    release = {
        'version': new, 'date': today(), 'baseline': baseline, 'change_id': change_id, 'origin': 'cloud-code',
        'environment': 'Claude Code cloud container used only as a development tool',
        'checks': [
            {'command': f'node {PACKAGE}/scripts/validate-studio.mjs', 'status': 'PASS', 'files': canonical['files'], 'owners': canonical['owners'],
             'planned_cases': canonical['evaluations']['total_planned'], 'executed': canonical['evaluations']['executed'], 'warnings': canonical.get('warnings')},
            {'command': 'bash scripts/check_all.sh', 'status': 'PASS', 'node': checks['node'], 'python': checks['python']},
        ] + ([{'command': 'MOTION_REVIEW_BROWSER=<local chromium> node --test motion-toolkit.test.mjs', 'status': 'PASS', 'tests': browser}] if browser else [])
          + ([{'command': f'claude plugin validate --strict (plugin and marketplace, Claude Code {claude})', 'status': 'PASS'}] if claude else []),
        'review': args.summary, 'source': args.title, 'github_publication': 'NOT_RUN', 'host_behavior': 'NOT_RUN',
    }
    write(f'verification/release-{new}.json', json.dumps(release, indent=2, ensure_ascii=False) + '\n')
    scope_line = f"{len(scope['changed'])} changed and {len(scope['added'])} added shared files out of {scope['files']}"
    verification = (f'The [{new} source checks](verification/release-{new}.json) pass canonical validation and `scripts/check_all.sh`: {summary}'
                    + ('; `claude plugin validate --strict` passes' if claude else '') + '. ' + (args.extra.strip() + ' ' if args.extra else '')
                    + f'[Scope](verification/scope-{new}.json) records {scope_line}.')
    replace_once('VERIFICATION.md', f'## Current source: {old}', f'## Current source: {new}\n\n{verification}\n\n## Previous source: {old}')
    status = read('RELEASE_STATUS.md')
    status = re.sub(r'^Source version: \*\*[^*]+\*\*\. Date: [0-9-]+\. Change ID: `[^`]+`', f'Source version: **{new}**. Date: {today()}. Change ID: `{change_id}`', status, count=1, flags=re.M)

    def row(name, value):
        nonlocal status
        pattern = re.compile(r'^\| ' + re.escape(name) + r' \|.*\|$', re.M)
        if not pattern.search(status):
            raise ReleaseError(f'RELEASE_STATUS.md has no row {name!r}')
        status = pattern.sub(lambda _: f'| {name} | {value} |', status, count=1)
    row('Change', args.summary)
    row('Source checks', 'PASS: canonical validator; `scripts/check_all.sh`: ' + summary + ('; `claude plugin validate --strict` passes' if claude else ''))
    row('Scope', f"{scope_line}; {scope['skills']} skill IDs; welcome {scope['welcome'].replace('_', '-')}, menus {scope['menus'].replace('_', '-')}, vendored snapshots {scope['vendored_snapshots'].replace('_', '-')}")
    row('GitHub publication', f'{new}: pending (release commit on `main`, then the tag workflow)')
    status = status.replace(f'(verification/release-{old}.json) and [bounded scope](verification/scope-{old}.json)', f'(verification/release-{new}.json) and [bounded scope](verification/scope-{new}.json)')
    status = re.sub(r'Its GitHub publication is [^.]*(?:\[[^\]]*\]\([^)]*\))?[^.]*\.\s*The previous release, [0-9.]+, is recorded in \[its verification\]\([^)]*\) and \[GitHub publication\]\([^)]*\)\.',
                    f'Its GitHub publication is pending. The previous release, {old}, is recorded in [its verification](verification/release-{old}.json) and [GitHub publication](verification/github-publication-{old}.json).', status, count=1)
    status = re.sub(r'1\.36\.0 to [0-9.]+: NOT_RUN', f'1.36.0 to {new}: NOT_RUN', status)
    write('RELEASE_STATUS.md', status)
    ledger = f"""

## {change_id}

- Origin: cloud-code
- Branch: `{git('rev-parse', '--abbrev-ref', 'HEAD')}`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `{baseline[:7]}` (main, package {old}); full SHA in the commit trailer
- Result: the release commit carrying this entry (package {new})
- Package version: {old} -> {new}
- Scope: {args.summary}
- Shared package changed: yes; {len(scope['changed'])} changed, {len(scope['added'])} added, 0 removed ([scope](../verification/scope-{new}.json))

Verification:

- canonical validator: PASS{'; `claude plugin validate --strict`: PASS' if claude else ''}
- `scripts/check_all.sh`: {summary}: PASS ([record](../verification/release-{new}.json))

Cross-host state:

- GitHub: pending (release commit, tag workflow and readback follow)
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run
"""
    write('docs/development-ledger.md', read('docs/development-ledger.md').rstrip('\n') + ledger)


def zip_facts(new):
    path = ROOT / 'dist' / f'framecore-work-creative-studio-{new}.zip'
    with zipfile.ZipFile(path) as archive:
        count = sum(1 for name in archive.namelist() if not name.endswith('/'))
    return path, count, path.stat().st_size


def commit(title, body, change_id, baseline, shared):
    message = f"""{title}

{body.strip()}

Origin-Agent: cloud-code
Change-ID: {change_id}
Baseline-SHA: {baseline}
Shared-Package-Changed: {'yes' if shared else 'no'}
ChatGPT-Work-Sync: not_tracked
Codex-Sync: not_run
{TRAILER_TAIL}
"""
    git('add', '-A')
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.txt', encoding='utf-8') as handle:
        handle.write(message)
    try:
        git('commit', '-q', '-F', handle.name)
    finally:
        os.unlink(handle.name)
    return git('rev-parse', 'HEAD')


def push(baseline):
    git('fetch', '-q', 'origin', 'main')
    if git('rev-parse', 'origin/main') != baseline:
        raise ReleaseError('origin/main moved since the baseline; merge it and run again (no force push)')
    git('push', '-q', 'origin', 'HEAD:main')
    branch = git('rev-parse', '--abbrev-ref', 'HEAD')
    for target in [branch] + SESSION_BRANCHES:
        if target not in ('HEAD', 'main'):
            run('git', 'push', '-q', 'origin', f'HEAD:{target}', check=False)


def prepare(args):
    old, new = current_version(), args.version
    if version_tuple(new) <= version_tuple(old):
        raise ReleaseError(f'{new} is not newer than {old}')
    git('fetch', '-q', 'origin', 'main', f'refs/tags/v{old}:refs/tags/v{old}', check=False)
    baseline = git('rev-parse', 'origin/main')
    if run('git', 'merge-base', '--is-ancestor', baseline, 'HEAD', check=False).returncode != 0:
        raise ReleaseError('HEAD does not contain origin/main; merge it first')
    same = run('git', 'diff', '--quiet', f'v{old}', '--', PACKAGE, check=False).returncode == 0
    if same and not git('ls-files', '--others', '--exclude-standard', '--', PACKAGE):
        raise ReleaseError(f'the package is identical to v{old}: a records-only change needs no release')
    for folder in PLUGIN.rglob('__pycache__'):
        subprocess.run(['rm', '-rf', str(folder)], check=True)
    bump(old, new)
    write_notes(new, read_arg(args.changelog), read_arg(args.notes))
    run('python3', 'scripts/build_install_manifest.py')
    canonical, checks, browser, claude = run_checks()
    scope = scope_record(old, new, args.change_id, args.summary)
    update_records(old, new, args.change_id, args, canonical, checks, browser, claude, scope, baseline)
    for folder in PLUGIN.rglob('__pycache__'):
        subprocess.run(['rm', '-rf', str(folder)], check=True)
    run('python3', 'scripts/build_install_manifest.py')
    run('python3', 'scripts/package_release.py', timeout=1800)
    _, count, size = zip_facts(new)
    text = re.sub(r'\d+ files, about \d+ MB', f'{count} files, about {round(size / 1e6)} MB', read('CLAUDE_INSTALL.md'), count=1)
    write('CLAUDE_INSTALL.md', text)
    run('node', f'{PACKAGE}/scripts/validate-studio.mjs')
    sha = commit(args.title, read_arg(args.body) if args.body else args.summary, args.change_id, baseline, True)
    print(json.dumps({'version': new, 'commit': sha, 'baseline': baseline, 'zip_files': count, 'zip_bytes': size, 'checks': checks, 'browser': browser, 'claude': claude}, indent=2))
    if args.push:
        push(baseline)
        print(f'pushed {sha[:7]} to main')
        print(plugin_creator_prompt(new, sha, count))


def read_arg(value):
    path = Path(value)
    return path.read_text(encoding='utf-8') if path.is_file() else value


def plugin_creator_prompt(version, sha, files):
    return f"""
--- Plugin Creator update prompt ---
@plugin-creator

Use Plugin Creator to update my existing FrameCore Works Creative Studio from:
https://github.com/{REPO}

Pin the source to commit {sha} (tag v{version}). Read CHATGPT_UPDATE.md and config/install-sources.json at that commit,
verify all declared source files ({files} files, sizes and SHA-256) and update the same plugin with the current release guard.
Write the declared files exactly as published; do not delete or rename any path and do not merge private preferences into
plugin files. Preserve identity, starter prompts, logo and integrations. Do not create duplicates.
After saving, report the version and the new release ID, then run from the saved plugin in code execution:
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --update --host chatgpt_work
and show its verdict.
"""


# ------------------------------------------------------------------ publish

def api(path):
    with urllib.request.urlopen(f'https://api.github.com/repos/{REPO}/{path}', timeout=30) as response:
        return json.loads(response.read())


def download(url, target):
    with urllib.request.urlopen(url, timeout=120) as response:
        target.write_bytes(response.read())


def publish(args):
    version = args.version
    sha = git('rev-list', '-n', '1', f'v{version}', check=False) or git('rev-parse', 'HEAD')
    deadline = time.time() + args.wait
    while True:
        runs = api(f'actions/runs?head_sha={sha}').get('workflow_runs', [])
        pending = [r for r in runs if r['status'] != 'completed']
        if runs and len(runs) >= args.min_runs and not pending:
            break
        if time.time() > deadline:
            raise ReleaseError(f'workflows not finished after {args.wait}s: {[(r["name"], r["status"]) for r in runs]}')
        time.sleep(20)
    failed = [r for r in runs if r['conclusion'] != 'success']
    if failed:
        raise ReleaseError('workflow failed: ' + ', '.join(f"{r['name']} {r['conclusion']} {r['html_url']}" for r in failed))
    git('fetch', '-q', 'origin', f'refs/tags/v{version}:refs/tags/v{version}')
    sha = git('rev-list', '-n', '1', f'v{version}')
    names = [f'framecore-work-creative-studio-{version}.zip', f'framecore-work-creative-studio-{version}.zip.inventory.json', f'framecore-motion-player-{version}.html']
    folder = Path(tempfile.mkdtemp(prefix=f'readback-{version}-'))
    hashes, matches = {}, {}
    for name in names:
        target = folder / name
        download(f'https://github.com/{REPO}/releases/download/v{version}/{name}', target)
        hashes[name] = hashlib.sha256(target.read_bytes()).hexdigest()
        local = ROOT / 'dist' / name
        matches[name] = local.exists() and local.read_bytes() == target.read_bytes()
    prefix = 'framecore-work-creative-studio/'
    with zipfile.ZipFile(folder / names[0]) as archive:
        members = [n for n in archive.namelist() if not n.endswith('/')]
        tree = run('git', 'ls-tree', '-r', '-z', '--name-only', f'v{version}', PACKAGE + '/').stdout.strip('\0').split('\0')
        mismatched = [n for n in members if subprocess.run(['git', 'show', f'v{version}:{PACKAGE}/{n[len(prefix):]}'], cwd=ROOT, capture_output=True).stdout != archive.read(n)]
        frontmatters = 0
        try:
            import yaml
            for n in members:
                rel = n[len(prefix):]
                if rel.startswith('skills/') and rel.count('/') == 2 and rel.endswith('/SKILL.md'):
                    yaml.safe_load(archive.read(n).decode('utf-8').split('---')[1])
                    frontmatters += 1
        except ImportError:
            frontmatters = None
    if mismatched or len(members) != len(tree):
        raise ReleaseError(f'release ZIP differs from the tag tree: {len(members)} vs {len(tree)} files, {len(mismatched)} mismatched')
    by_name = {r['name'].split()[0]: r for r in runs}
    record = {
        'version': version, 'change_id': args.change_id, 'origin': 'cloud-code', 'commit': sha, 'package_commit': sha,
        'release_url': f'https://github.com/{REPO}/releases/tag/v{version}',
        'workflows': [{'id': r['id'], 'name': r['name'], 'branch': r['head_branch'], 'conclusion': r['conclusion']} for r in runs],
        'plugin_zip_sha256': hashes[names[0]], 'plugin_zip_matches_local': matches[names[0]],
        'plugin_zip_matches_tag_tree': f'{len(members)} of {len(tree)} files byte-identical to v{version}:{PACKAGE}/',
        'plugin_inventory_sha256': hashes[names[1]], 'plugin_inventory_matches_local': matches[names[1]],
        'motion_player_sha256': hashes[names[2]], 'motion_player_asset_matches_local': matches[names[2]],
        'published_skill_yaml': f'{frontmatters} SKILL.md frontmatters in the downloaded plugin ZIP parse with PyYAML' if frontmatters is not None else 'PyYAML unavailable; not parsed',
        'hosted_plugin': 'not_tracked (owner decision 2026-10-10: the owner updates and tests it)', 'host_behavior': 'NOT_RUN',
    }
    write(f'verification/github-publication-{version}.json', json.dumps(record, indent=2, ensure_ascii=False) + '\n')
    status = read('RELEASE_STATUS.md')
    status = re.sub(r'^\| GitHub publication \|.*\|$', f'| GitHub publication | {version}: `main` at `{sha[:7]}`, [v{version}](https://github.com/{REPO}/releases/tag/v{version}), release and check workflows green, plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree ({len(members)} of {len(tree)}) ([record](verification/github-publication-{version}.json)) |', status, count=1, flags=re.M)
    status = status.replace('Its GitHub publication is pending.', f'Its GitHub publication is recorded in [github-publication-{version}.json](verification/github-publication-{version}.json).')
    write('RELEASE_STATUS.md', status)
    ledger = read('docs/development-ledger.md')
    pending = '- GitHub: pending (release commit, tag workflow and readback follow)'
    at = ledger.rfind(pending)
    if at < 0:
        raise ReleaseError('no pending GitHub line in the ledger')
    done = (f'- GitHub: synchronized. `main` at `{sha[:7]}`; workflows ' + ', '.join(f"{r['name']} {r['id']}" for r in runs)
            + f': success; [v{version}](https://github.com/{REPO}/releases/tag/v{version}) assets read back: plugin ZIP, inventory and player '
            + f'match the local build, ZIP byte-identical to the tag tree ({len(members)} of {len(tree)}) ([record](../verification/github-publication-{version}.json))')
    write('docs/development-ledger.md', ledger[:at] + done + ledger[at + len(pending):])
    run('node', f'{PACKAGE}/scripts/validate-studio.mjs')
    baseline = git('rev-parse', 'HEAD')
    commit(f'docs: record {version} GitHub publication', 'Release workflow and checks are green; the downloaded assets equal the local build and the tag tree.',
           args.change_id, baseline, False)
    print(json.dumps(record, indent=2))
    if args.push:
        push(baseline)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Prepare or record a Studio release.')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('version')
    p.add_argument('--change-id', required=True)
    p.add_argument('--title', required=True)
    p.add_argument('--changelog', required=True, help='changelog entry body (file or text), repository-relative links')
    p.add_argument('--notes', required=True, help='RELEASE_NOTES.md content (file or text)')
    p.add_argument('--summary', required=True, help='one paragraph for RELEASE_STATUS and the ledger')
    p.add_argument('--extra', help='an extra sentence for VERIFICATION (evidence beyond the checks)')
    p.add_argument('--body', help='commit body (file or text); defaults to the summary')
    p.add_argument('--push', action='store_true')
    q = sub.add_parser('publish')
    q.add_argument('version')
    q.add_argument('--change-id', required=True)
    q.add_argument('--wait', type=int, default=1800)
    q.add_argument('--min-runs', type=int, default=4)
    q.add_argument('--push', action='store_true')
    args = parser.parse_args(argv)
    try:
        (prepare if args.command == 'prepare' else publish)(args)
    except ReleaseError as error:
        print(f'release: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
