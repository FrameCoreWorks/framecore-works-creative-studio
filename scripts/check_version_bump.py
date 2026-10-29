#!/usr/bin/env python3
"""Fail when the shared package changed on main after its version was already released.

Every package change on main ships as a release, so the hosted plugin, Codex and Claude installs can tell versions apart.
If the tag v<version> of the current plugin.json version exists and the package differs from that tag, the version was
not bumped. Working branches are not checked: there the bump happens at release time.

Companion plugins (every other plugins/<name>/plugin.json) have no tags of their own and ship with Studio's releases.
Each one is compared with the latest Studio release tag: a companion that changed since that tag must carry a newer
version than it had there, so Claude and Codex installs can tell the copies apart. A frozen copy whose only change is
an added DEPRECATED.md keeps its last released version.

  python3 scripts/check_version_bump.py      # exit 0 when released or unchanged, 1 when changed without a bump
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'plugins/framecore-work-creative-studio'


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True)


def companion_errors(root=ROOT):
    """Companions changed since the latest release tag without a version bump."""
    run = lambda *a: subprocess.run(['git', '-C', str(root), *a], capture_output=True, text=True)
    tag = run('describe', '--tags', '--abbrev=0', '--match', 'v*', 'HEAD').stdout.strip()
    if not tag:
        return []
    errors = []
    for manifest in sorted(Path(root).glob('plugins/*/plugin.json')):
        folder = manifest.parent.relative_to(root).as_posix()
        if folder == PACKAGE:
            continue
        old = run('show', f'{tag}:{folder}/plugin.json')
        if old.returncode != 0 or run('diff', '--quiet', tag, 'HEAD', '--', folder).returncode == 0:
            continue
        changed = run('diff', '--name-only', tag, 'HEAD', '--', folder).stdout.split()
        if changed == [f'{folder}/DEPRECATED.md']:  # frozen copy: only the marker was added, the release stays as it was
            continue
        before = json.loads(old.stdout)['version']
        now = json.loads(manifest.read_text(encoding='utf-8'))['version']
        if now == before:
            errors.append(f'{folder} changed after {tag} but is still {now}; bump its version')
    return errors


def main():
    errors = companion_errors()
    for error in errors:
        print(error, file=sys.stderr)
    status = studio_status()
    return 1 if errors else status


def studio_status():
    version = json.loads((ROOT / PACKAGE / 'plugin.json').read_text(encoding='utf-8'))['version']
    tag = f'v{version}'
    if git('rev-parse', '-q', '--verify', f'refs/tags/{tag}').returncode != 0:
        print(f'{tag} is not tagged yet: this commit is its release')
        return 0
    if git('diff', '--quiet', tag, 'HEAD', '--', PACKAGE).returncode == 0:
        print(f'The package is identical to {tag}')
        return 0
    changed = git('diff', '--name-only', tag, 'HEAD', '--', PACKAGE).stdout.split()
    print(f'The package changed after {tag} without a version bump ({len(changed)} files, e.g. {", ".join(changed[:3])}); '
          'release it with a new version.', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
