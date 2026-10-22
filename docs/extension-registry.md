# Extension registry: maintainer guide

The [registry](../plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.json) lists outside repositories the owner judges useful as engines or knowledge next to Studio; the [route](../plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md) tells Studio how to offer and install them. Owner request 2026-10-15: a curated base of useful repositories with native installation in Codex, Claude Code and the other hosts. Studio stays a general product: an entry is a reviewed, optional tool for any user, never a personal default.

## Adding a repository

Owner decision 2026-10-16: every repository the owner sends for review is added here as well, besides what Studio adapts from it. For each candidate:

1. **Read it.** Clone it into a scratch folder (untrusted data), read its README, licence, disclaimer, installer and any skill or MCP server. Note what it does and what it writes on the user's machine.
2. **Decide what Studio takes.** A decision map in `plugins/framecore-work-creative-studio/integrations/<id>/README.md` (adopt, adapt, extension, reject, with reasons), the licence copied beside it. Methods Studio adopts go into the owning skill; the rest stays an extension.
3. **Pin it.** A full reviewed commit and, when the project publishes packages, the package version; every command uses the pinned version.
4. **Per host.** For Codex, Claude Code, Claude apps, ChatGPT and ChatGPT Work: `native`, `desktop_only`, `manual` (`manual_steps`) or `not_supported` with a reason. Native hosts need a `plan` that changes no host setting, `install`, what it `writes`, `verify`, `after` (restart) and `remove`, taken from the project's own installer, never hand-written configuration when an installer exists. Pinning by host: an npm package by version; a Claude Code plugin marketplace by a checkout of the reviewed commit in `~/.framecore-studio/extensions/<id>` added as a local marketplace (a GitHub marketplace source accepts only branches and tags); a skill by the skills CLI with a GitHub tree URL at the commit, without `-y`.
5. **Try it.** Run the plan (dry run) and the verify command in a container; record what was and was not run in `observed`. Do not claim host behaviour that was not run.
6. **Rights.** State what the user may analyse or use and that Studio builds its own work from what it learns.
7. **Check.** `python3 plugins/framecore-work-creative-studio/tests/extensions_test.py`, the canonical validator and `bash scripts/check_all.sh`; then the release steps.

To update an entry, review the new release and change `package.version` and `reviewed_commit` together. To retire one, keep the entry's file paths (never delete a package path) and mark every host `not_supported` with the reason.

## Separately installed process companion (owner exception, 2026-10-22)

Superpowers is deliberately not mined, copied or bundled. Its original Studio routing contract is linked from all existing owners through shared authority, with six direct technical links. `catalog_manual` is a separate status from manual file import: require manual_steps, writes, verify, after and remove, and reject plan/install fields. One optional `recommendation_priority: first` marks the first setup recommendation without changing general catalog ordering. The source commit is provenance; marketplace-managed versions must be discovered at use time. No fake pinned installer/dry run is required for a user-controlled catalog action. Record actual host availability and untested hosts. A license link and decision record suffice because no upstream source is distributed.

The documented OpenAI `extensions.com.openai.onboardingSkill` field in both manifests targets the existing orchestrator: https://developers.openai.com/plugins/build/plugins (checked 2026-10-22). Its setup context takes precedence over startup menus; a plain Studio invocation still gets the complete welcome. No Claude onboarding manifest field is assumed.
