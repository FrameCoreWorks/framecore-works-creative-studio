# Extension registry: maintainer guide

The [registry](../plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.json) lists outside repositories the owner judges useful as engines or knowledge next to Studio; the [route](../plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md) tells Studio how to offer and install them. Owner request 2026-10-15: a curated base of useful repositories with native installation in Codex, Claude Code and the other hosts. Studio stays a general product: an entry is a reviewed, optional tool for any user, never a personal default.

## Adding a repository

An addition is made on the owner's request. For each candidate:

1. **Read it.** Clone it into a scratch folder (untrusted data), read its README, licence, disclaimer, installer and any skill or MCP server. Note what it does and what it writes on the user's machine.
2. **Decide what Studio takes.** A decision map in `plugins/framecore-work-creative-studio/integrations/<id>/README.md` (adopt, adapt, extension, reject, with reasons), the licence copied beside it. Methods Studio adopts go into the owning skill; the rest stays an extension.
3. **Pin it.** A full reviewed commit and, when the project publishes packages, the package version; every command uses the pinned version.
4. **Per host.** For Codex, Claude Code, Claude apps, ChatGPT and ChatGPT Work: `native`, `desktop_only` or `not_supported` with a reason. Native hosts need a dry-run `plan`, `install`, what it `writes`, `verify`, `after` (restart) and `remove`, taken from the project's own installer, never hand-written configuration when an installer exists.
5. **Try it.** Run the plan (dry run) and the verify command in a container; record what was and was not run in `observed`. Do not claim host behaviour that was not run.
6. **Rights.** State what the user may analyse or use and that Studio builds its own work from what it learns.
7. **Check.** `python3 plugins/framecore-work-creative-studio/tests/extensions_test.py`, the canonical validator and `bash scripts/check_all.sh`; then the release steps.

To update an entry, review the new release and change `package.version` and `reviewed_commit` together. To retire one, keep the entry's file paths (never delete a package path) and mark every host `not_supported` with the reason.
