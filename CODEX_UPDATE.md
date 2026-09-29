# Update an existing Codex installation

In **Codex**, use `$plugin-creator` and select the matching available skill from completion, then paste the complete prompt below. Use it for package checks while preserving the native entry and bundle. If this host does not expose Plugin Creator, omit only the invocation line and use the same update request. The mention does not grant missing tools or permissions.

```text
$plugin-creator

Update my existing FrameCore Works Creative Studio from:
https://github.com/FrameCoreWorks/framecore-works-creative-studio

Use Plugin Creator for package checks when available. Update the existing native installation;
do not create a hosted plugin copy or register a plugin catalog. Report unavailable capabilities.
Read CODEX_UPDATE.md. Locate the actual native entry, receipt and complete bundle, or identify
an older layout. Resolve main once to a full commit and verify its declared inventory.
Compare installed bytes, previous verified source and new source. Prepare the complete change
before writing. Preserve personal additions, projects, provider settings and existing identity.
This request authorizes the update; resolve overlapping personal changes or scope migration with me.
If unchanged, report already_up_to_date without writing. Do not run the fresh installer over
an existing destination.
Keep a private recovery snapshot, recheck drift, apply only intended changes and read back all files.
Preserve the complete linked bundle. Update the native pointer and receipt only after verification.
Report actual saved status separately from activation.
```

For the 1.0.1 layout, `installation.json` next to the native SKILL.md records source identity
and bundle location. Verify it against actual files; it is not permission to overwrite them.

Use a three-way comparison only with a verified prior source. Otherwise report `baseline_unknown`,
show current/source differences and preserve unidentified additions. New upstream content does not
authorize deleting unrelated skills.

Prepare a new verified bundle outside discovery and retain the old one for recovery, then update the
**same** native entry's pointer and receipt. Preserve personal changes to that entry. Recheck current
bytes before mutation and stop on concurrent drift. Never delete an old bundle merely to make the
fresh installer accept a path.

An older plugin-based or individual-skill layout needs an explicit migration of the actual active
entries. Do not create parallel orchestrators or disable unrelated skills. After failed/ambiguous
saving inspect actual state before retry or rollback. No background update, global config rewrite
or provider setup is included.
