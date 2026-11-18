# Claude Code instructions

The repository's maintenance rules for every agent are in [AGENTS.md](AGENTS.md); read them before writing. Start with its **Current rules** section: work on a branch, open a PR, merge on green CI (owner 2026-11-18), and the hosted-plugin and evidence rules.

In a Claude Code cloud session, push the session branch by name and open a pull request to `main`; merge it on green CI (AGENTS.md, current rule 2). GitHub deletes the branch after the merge. If the stop hook still reports unpushed commits after the merge, it compares against a stale local `refs/remotes/origin/<session branch>`: run `git fetch --prune origin` (local only).

The hookify rules in `.claude/hookify.*.local.md` block a force push, a direct push to `main` (and hand-pushed tags or deletions) and removing or moving a shared-package path; they load when the hookify plugin is active. A Bash command that merely contains such text (a heredoc, a test string) is blocked too: write that text with the Write tool.

@AGENTS.md
