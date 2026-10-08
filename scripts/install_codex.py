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


def frontmatter_name(path):
    """Read the skill identity, not name-like text in its Markdown body.

    Support ordinary YAML scalar names, quoted keys/values and comments.
    Ambiguous or unsupported identity syntax requires review before any write;
    this is deliberately not a general YAML parser.
    """
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    end = next((i for i, line in enumerate(lines[1:], 1)
                if line.strip() in {'---', '...'}), None)
    if end is None:
        raise ValueError('Unterminated skill frontmatter requires review: ' + str(path))
    declarations = []
    for line in lines[1:end]:
        match = re.match(r'^(?:name|"name"|\'name\')\s*:\s*(.*)$', line)
        if match:
            declarations.append(match[1].strip())
    if len(declarations) != 1:
        raise ValueError('Missing, duplicate or unsupported skill name requires review: ' + str(path))
    scalar = declarations[0]
    if scalar.startswith('"'):
        try:
            name, consumed = json.JSONDecoder().raw_decode(scalar)
        except ValueError as error:
            raise ValueError('Unsupported quoted skill name requires review: ' + str(path)) from error
        tail = scalar[consumed:]
        if not isinstance(name, str) or (tail.strip() and not re.fullmatch(r'\s+#.*', tail)):
            raise ValueError('Ambiguous skill name requires review: ' + str(path))
    elif scalar.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'(?:\s+#.*)?\s*", scalar)
        if not match:
            raise ValueError('Unsupported quoted skill name requires review: ' + str(path))
        name = match[1].replace("''", "'")
    else:
        name = re.split(r'\s+#', scalar, maxsplit=1)[0].strip()
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', name):
            raise ValueError('Unsupported skill name requires review: ' + str(path))
    return name


def wrapper(bundle):
    return f'''---
name: {NAME}
description: Use FrameCore Works Creative Studio for learning creative skills or creating briefs, graphics, video, audio, text, reference sheets, storyboards and production handoffs. Route the task through the complete installed Studio knowledge bundle. Do not use for unrelated coding.
---

# FrameCore Works Creative Studio

Use the intact Studio bundle at `{bundle}`. It contains 37 linked modules,
their knowledge, references, templates, original source bundles and logo.

Start by reading `{bundle / 'skills/workflow-orchestrator/SKILL.md'}`.
For a plugin version or installation-status question, reread that entry and
apply its package-version reporting contract before any welcome or creative intake.
Do not infer the installed version from conversation history or the latest release.
For an explicit specialist request, read that module's SKILL.md directly under
`{bundle / 'skills'}` and apply its research and preservation requirements.
Follow relative references from the actual module location inside the bundle,
never from this entry folder. Load only the resources needed for the current task.

The nested modules are reference files read by Codex, not separately installed
personal skills or proof that other agents ran. This native entry preserves the
same creative routing as the hosted plugin. Use the user's language and requested
pace. Resolve learning versus creation through the orchestrator: clear learning
requests use its mentoring overlay, and concrete projects bypass learning intake.
For every sent Studio-only invocation, greeting or startup request, apply the
automatic language policy at the beginning of the orchestrator before answering.
Follow an explicit preference, otherwise meaningful user text; for bare or numeric
inputs use an actually supplied host response/UI language, then conversation
language. English is only a provisional fallback when every signal is absent.
Never infer country or claim access to hidden host settings. Do not require an
explicit translation request. Copy the entire matching embedded English/Polish
welcome or automatically translate the full English source for another language:
`{bundle / 'skills/workflow-orchestrator/assets/startup-welcome.en.md'}`
`{bundle / 'skills/workflow-orchestrator/assets/startup-welcome.pl.md'}`.
Preserve the introduction, all six capability bullets, optional-material invitation,
qualifications and final 1. Creative mode / 2. Learning mode choice in the user's
language. Add no salutation or other text. Repeat the full welcome unchanged while
the language is unchanged; switch the entire response when the language changes.
Preserve project and learning checkpoints. Concrete tasks and actual resume
requests bypass the welcome. Localize later menus without changing reply tokens.
In learning onboarding, ask exactly one question about one missing decision,
accept its numbered option or free text, then wait for the answer. Never show a
question batch; reuse supplied facts and skip known questions. Sufficient context
goes directly to the plan and first lesson at every host reasoning setting.
A mode-only creative choice must show 1. Quick mode / 2. Expanded mode in the user's language;
a pace-only choice shows the complete work-area menu from the orchestrator's
startup and creative menus reference, motion graphics included. These steps apply at every host
reasoning setting. Bind choice tokens only to currently pending displayed groups.
An explicit specialist learning request follows that same overlay. Quick/Deep
remains pace, not the learning/creation choice. Use only available authorized tools.
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
                  if frontmatter_name(p) in declared['entrypoints']]
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
