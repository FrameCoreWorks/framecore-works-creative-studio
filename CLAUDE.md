# Claude Code instructions

The repository's maintenance rules for every agent are in [AGENTS.md](AGENTS.md); read them before writing. Start with its **Current rules** section: commit on `main`, push only `main` (no remote branch, not even the `claude/*` branch a cloud session names), and the hosted-plugin and evidence rules.

In a Claude Code cloud session the stop hook may report unpushed commits on the session branch. It compares against a stale local `refs/remotes/origin/<session branch>` left by the clone. Once `origin/main` carries your commits, run `git fetch --prune origin` (local only) and leave the branch unpushed.

@AGENTS.md
