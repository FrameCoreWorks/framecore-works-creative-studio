"""The repository's hookify rules block what AGENTS.md forbids and let the allowed pushes through."""
import re
import unittest
from pathlib import Path

RULES = Path(__file__).resolve().parents[1] / '.claude'
NAMES = ('block-force-push', 'block-push-other-than-main', 'block-shared-package-path-removal')


def pattern(name):
    text = (RULES / f'hookify.{name}.local.md').read_text(encoding='utf-8')
    # hookify compiles the frontmatter pattern with re.IGNORECASE and uses re.search
    return re.compile(re.search(r'^pattern: (.+)$', text, re.M).group(1), re.IGNORECASE)


def blocked(command):
    return [n for n in NAMES if pattern(n).search(command)]


class HookifyRules(unittest.TestCase):
    def test_allowed(self):
        for command in ('git push origin HEAD:main', 'git push origin HEAD:main 2>&1 | tail -1', 'git push -u origin main',
                        'git fetch -q origin main && git push origin HEAD:main', 'rm -f verification/host-evals/x.zip',
                        'git diff --stat plugins/framecore-work-creative-studio/', 'grep -rn rm plugins/framecore-work-creative-studio'):
            with self.subTest(command=command):
                self.assertEqual(blocked(command), [])

    def test_blocked(self):
        for command in ('git push --force origin HEAD:main', 'git push -f origin main', 'git push origin +HEAD:main',
                        'git push --force-with-lease origin main', 'git push -u origin claude/session-branch',
                        'git push origin v1.143.0', 'git push origin --delete gh-pages', 'git push',
                        'git rm plugins/framecore-work-creative-studio/skills/ugc/SKILL.md',
                        'git mv plugins/framecore-work-creative-studio/a plugins/framecore-work-creative-studio/b',
                        'rm -rf plugins/framecore-work-creative-studio/skills/x'):
            with self.subTest(command=command):
                self.assertNotEqual(blocked(command), [])


if __name__ == '__main__':
    unittest.main()
