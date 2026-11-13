#!/usr/bin/env python3
"""Build the list of package files that Studio releases deleted (1.153.0 Earshot and Open Assets copies, 1.178.0
motion module, 1.179.0 editing and captions module), each with every Git blob SHA-1 it ever shipped with.

The cleanup tool next to the list removes an old copy's leftover file only when its bytes equal one of these shipped
versions, so a file the user changed or added is never touched. Run after a release that deletes package paths:

  python3 scripts/build_removed_files.py
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'plugins/framecore-work-creative-studio'
RELEASES = ('1.153.0', '1.178.0', '1.179.0')
OUT = ROOT / PACKAGE / 'skills/workflow-orchestrator/assets/migration/removed-files.json'


def main():
    removed = {}
    for version in RELEASES:
        for path in json.loads((ROOT / f'verification/scope-{version}.json').read_text())['removed']:
            removed.setdefault(path, version)
    current = {p for p in removed if (ROOT / PACKAGE / p).exists()}
    if current:
        raise SystemExit(f'{len(current)} listed paths exist in the package again: {sorted(current)[:5]}')
    blobs = {p: set() for p in removed}
    log = subprocess.run(['git', 'log', '--all', '--raw', '--no-abbrev', '--no-renames', '--format=', '--', *[f'{PACKAGE}/{p}' for p in removed]],
                         cwd=ROOT, check=True, capture_output=True, text=True).stdout
    for line in log.splitlines():
        if not line.startswith(':'):
            continue
        meta, path = line.split('\t', 1)
        new = meta.split()[3]
        rel = path.removeprefix(PACKAGE + '/')
        if rel in blobs and set(new) != {'0'}:
            blobs[rel].add(new)
    missing = [p for p, b in blobs.items() if not b]
    if missing:
        raise SystemExit(f'no shipped version found for {missing[:5]}')
    data = {
        'schema': 'framecore-removed-files/1',
        'note': 'Package files deleted by Studio releases, with every Git blob SHA-1 they shipped with. Built by scripts/build_removed_files.py.',
        'releases': list(RELEASES),
        # Top folders (two levels) that no longer exist in the package: anything else left there was never Studio's.
        'removed_folders': sorted({'/'.join(p.split('/')[:2]) for p in removed} - {t for t in {'/'.join(p.split('/')[:2]) for p in removed} if (ROOT / PACKAGE / t).exists()}),
        'files': {p: {'removed_in': removed[p], 'blobs': sorted(blobs[p])} for p in sorted(removed)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1) + '\n', encoding='utf-8')
    print(f'{OUT.relative_to(ROOT)}: {len(removed)} files, {sum(len(b) for b in blobs.values())} shipped versions')


if __name__ == '__main__':
    main()
