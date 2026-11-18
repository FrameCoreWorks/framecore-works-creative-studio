---
name: block-push-to-main
enabled: true
event: bash
action: block
pattern: git\s+push\b(?=[^;&|\n]*(?:[\s:]main(?=\s|$|[;&|)])|\s--delete\b|\s-d\b|\s--tags\b|\s--mirror\b|\s--all\b|\sv\d|refs/tags/))|git\s+push\s*(?:$|[;&|)\n]|\d?>)
---

**Nothing is pushed to `main` directly** (AGENTS.md, current rule 2, owner 2026-11-18): every change goes on a branch, then a pull request to `main`, green CI and a merge. Tags come from the release workflow after the merge, never by hand, and branch deletion is GitHub's automatic step after a merge.

Push your branch by name, for example `git push -u origin claude/<session-branch>`, then open a pull request. `python3 scripts/release.py prepare|publish ... --push` pushes the current branch the same way.
