---
name: block-push-other-than-main
enabled: true
event: bash
action: block
pattern: git\s+push\b(?!\s+(-u\s+)?origin\s+(HEAD:)?main(\s*$|\s*[;&|)]|\s+\d?>))
---

**Only `main` is pushed to GitHub** (AGENTS.md, current rule 2): no remote branch, not even the `claude/*` branch a cloud session names, no tag pushed by hand and no branch deletion (that is the owner's step).

Use `git push origin HEAD:main` after fetching and rebasing, or `python3 scripts/release.py prepare|publish ... --push` for a release. If the stop hook reports unpushed commits on the session branch, follow CLAUDE.md: `git fetch --prune origin`.
