#!/usr/bin/env python3
"""Fail when the shared package changed on main after its version was already released.

Every package change on main ships as a release, so the hosted plugin, Codex and Claude installs can tell versions apart.
If the tag v<version> of the current plugin.json version exists and the package differs from that tag, the version was
not bumped. Working branches are not checked: there the bump happens at release time.

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


def main():
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
