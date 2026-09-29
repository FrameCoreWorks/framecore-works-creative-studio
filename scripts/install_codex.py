#!/usr/bin/env python3
"""Install one native Codex entry backed by an intact Studio bundle. No network."""
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from build_install_manifest import PLUGIN, inventory, verify_source

NAME = 'framecore-work-creative-studio'


def wrapper(bundle):
    return f'''---
name: {NAME}
description: Use FrameCore Works Creative Studio for creative briefs, graphics, video, audio, text, reference sheets, storyboards and production handoffs. Route the task through the complete installed Studio knowledge bundle. Do not use for unrelated coding.
---

# FrameCore Works Creative Studio

Use the intact Studio bundle at `{bundle}`. It contains 37 linked modules,
their knowledge, references, templates, original source bundles and logo.

Start by reading `{bundle / 'skills/workflow-orchestrator/SKILL.md'}`.
For an explicit specialist request, read that module's SKILL.md directly under
`{bundle / 'skills'}` and apply its research and preservation requirements.
Follow relative references from the actual module location inside the bundle,
never from this entry folder. Load only the resources needed for the current task.

The nested modules are reference files read by Codex, not separately installed
personal skills or proof that other agents ran. This native entry preserves the
same creative routing as the hosted plugin. Use the user's language and requested
pace. Do not repeat onboarding for a concrete task. Quick mode gives short ideas;
deep mode develops the project step by step. Use only available authorized tools.
Installation does not connect providers or synchronize ChatGPT memory.
'''


def reject_symlink_chain(path):
    for parent in [path, *path.parents]:
        if parent.is_symlink():
            raise ValueError('Symlink destination: ' + str(parent))


def inside(path, parent):
    return path == parent or parent in path.parents


def check_saved(target, bundle, declared, commit):
    if inventory(bundle) != declared['files']:
        raise ValueError('Saved bundle differs from the verified source')
    expected = wrapper(bundle)
    if (target / 'SKILL.md').read_text() != expected:
        raise ValueError('Native entry has local changes or does not match this bundle')
    receipt = json.loads((target / 'installation.json').read_text())
    if (receipt['source_commit'] != commit or receipt['version'] != declared['version']
            or receipt['bundle_dir'] != str(bundle)
            or receipt['source_files'] != declared['files']
            or receipt['entry_sha256'] != hashlib.sha256(expected.encode()).hexdigest()):
        raise ValueError('Installation receipt does not match the requested source')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['plan', 'install', 'verify'])
    parser.add_argument('--skills-dir', type=Path, required=True,
                        help='Actual native Codex skills location resolved by the host')
    parser.add_argument('--bundle-dir', type=Path, required=True,
                        help='Persistent directory outside every active skill discovery root')
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', args.source_commit):
        raise ValueError('Expected the verified full source commit')
    for path in (args.skills_dir, args.bundle_dir):
        if not path.is_absolute() or '\n' in str(path) or '`' in str(path):
            raise ValueError('Use absolute destination paths without newline or backtick')
        reject_symlink_chain(path)
    skills, bundle = args.skills_dir.resolve(), args.bundle_dir.resolve()
    target = skills / NAME
    reject_symlink_chain(target)
    if inside(bundle, skills) or inside(skills, bundle) or inside(bundle, PLUGIN) or inside(PLUGIN, bundle):
        raise ValueError('Keep the bundle outside discovery roots and outside the source bundle')
    declared = verify_source()
    if args.action == 'verify':
        check_saved(target, bundle, declared, args.source_commit)
        print(json.dumps({'status': 'FILES_VERIFIED', 'version': declared['version'],
                          'files': len(declared['files']), 'host_activation': 'not_observed'}))
        return
    if target.exists() or bundle.exists():
        if target.is_dir() and bundle.is_dir():
            check_saved(target, bundle, declared, args.source_commit)
            print(json.dumps({'status': 'already_up_to_date', 'writes': 0}))
            return
        raise ValueError('Existing or partial installation; inspect it with CODEX_UPDATE.md')
    collisions = [p for p in skills.glob('*/SKILL.md')
                  if re.search(r'^name:\s*["\']?(' + '|'.join(map(re.escape, declared['entrypoints']))
                               + r')["\']?\s*$', p.read_text(), re.M)]
    if collisions:
        raise ValueError('Existing Studio/Workflow Kit skill identities require review: ' + ', '.join(map(str, collisions)))
    if args.action == 'plan':
        print(json.dumps({'status': 'READY', 'writes': 0, 'version': declared['version'],
                          'native_entry': str(target), 'bundle': str(bundle),
                          'modules': len(declared['entrypoints']), 'files': len(declared['files'])}, indent=2))
        return
    skills.mkdir(parents=True, exist_ok=True)
    bundle.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive directory creation prevents replacing an existing installation.
    target.mkdir()
    try:
        bundle.mkdir()
        shutil.copytree(PLUGIN, bundle, dirs_exist_ok=True)
        entry = wrapper(bundle)
        (target / 'SKILL.md').write_text(entry)
        receipt = {'version': declared['version'], 'source_commit': args.source_commit,
                   'repository': declared['repository'], 'bundle_dir': str(bundle),
                   'source_files': declared['files'],
                   'entry_sha256': hashlib.sha256(entry.encode()).hexdigest()}
        (target / 'installation.json').write_text(json.dumps(receipt, indent=2) + '\n')
        check_saved(target, bundle, declared, args.source_commit)
    except Exception:
        print('Partial installation may remain at ' + str(target) + ' and ' + str(bundle)
              + '; inspect actual state before recovery. No existing directory was overwritten.', file=sys.stderr)
        raise
    print(json.dumps({'status': 'INSTALLED_FILES_VERIFIED', 'version': declared['version'],
                      'modules': len(declared['entrypoints']), 'host_activation': 'not_observed'}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        sys.exit(str(error))
