# Claude Code instructions

The repository's maintenance rules for every agent are in [AGENTS.md](AGENTS.md); read them before writing. Start with its **Current rules** section: commit on `main`, push only `main` (no remote branch, not even the `claude/*` branch a cloud session names), and the hosted-plugin and evidence rules.

In a Claude Code cloud session the stop hook may report unpushed commits on the session branch. It compares against a stale local `refs/remotes/origin/<session branch>` left by the clone. Once `origin/main` carries your commits, run `git fetch --prune origin` (local only) and leave the branch unpushed.

The hookify rules in `.claude/hookify.*.local.md` block a force push, a push of anything but `main` and removing or moving a shared-package path; they load when the hookify plugin is active. A Bash command that merely contains such text (a heredoc, a test string) is blocked too: write that text with the Write tool.

@AGENTS.md
