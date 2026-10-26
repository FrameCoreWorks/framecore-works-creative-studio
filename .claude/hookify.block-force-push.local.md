---
name: block-force-push
enabled: true
event: bash
action: block
pattern: git\s+push\b[^;&|\n]*(\s--force\b|\s--force-with-lease\b|\s-[a-zA-Z]*f\b|\s\+[^\s]+)
---

**Force push is forbidden in this repository** (AGENTS.md, current rule 2).

Fetch the latest `main`, rebase your commits on it, rerun the checks and push as a fast-forward: `git push origin HEAD:main`. Never resolve drift with a force push or `reset --hard`.
