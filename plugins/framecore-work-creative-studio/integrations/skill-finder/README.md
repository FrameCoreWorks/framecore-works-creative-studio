# Skill finder: selective method adaptation

Source: [Vercel / skills](https://github.com/vercel-labs/skills/tree/13e4063a1cf913f5606d57d42ab83a86f5001e04), the `skills` CLI and its `find-skills` skill, observed version 1.7.2, pinned commit `13e4063a1cf913f5606d57d42ab83a86f5001e04`, announced in [Introducing skills, the open agent skills ecosystem](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem). Reviewed on 2026-10-10.

This integration adapts the MIT-licensed `find-skills` method. [The original license](LICENSE) retains Copyright (c) 2026 Vercel, Inc. The upstream skill is not installed or vendored as a second skill, so hosts do not discover it; its CLI is not bundled. Source paths and Git blob hashes are in [the manifest](source-manifest.json). Studio's route is the [skill finder](../../skills/workflow-orchestrator/references/skill-finder.md) with its [search script](../../skills/workflow-orchestrator/assets/skill-finder/find_skills.py).

## Decision map

| Source method | Decision | Studio destination or reason |
| --- | --- | --- |
| Trigger on "how do I do X", "find a skill for X" | Adapt | Welcome option `3` and the orchestrator's entry rule |
| Understand domain and task first | Adapt | One question about what the skill should do |
| Check the leaderboard, then `npx skills find` | Adapt with change | Studio's own skills are matched first; the catalog is read through its search endpoint by a standard-library script, no CLI needed |
| Verify install count, source reputation, stars | Adapt with change | Install count and the catalog's security audits (ath, Socket, Snyk) give a verdict; the whole catalog is searched without an author allowlist, at the owner's request; imitation names are flagged |
| Present name, installs, command and link | Adopt | Plus what the skill does, read from its own `SKILL.md`, and the audit results |
| Install with `npx skills add … -g -y` | Reject `-y`; adapt | Only on an explicit request, in Codex or Claude Code; `DO_NOT_TRACK=1`; the CLI keeps its confirmation |
| CLI telemetry to skills.sh | Opt out | Commands set `DO_NOT_TRACK=1`; the script sends only the search query, the audit request and one GitHub read |
| `npx skills init` when nothing is found | Defer | Creating skills is outside this route |

## Evidence scope

The search (`/api/search`) and audit (`/tele/audit`) endpoints are read from the CLI source; skills.sh does not document them publicly, so they may change without notice and the script treats any failure as `offline` or `unchecked`. Checked on 2026-10-10 against the live catalog from a Linux container: searches returned results with installs and audits, and critical-rated skills were blocked. Behavior in Codex, Claude Code and chat hosts is not run.
