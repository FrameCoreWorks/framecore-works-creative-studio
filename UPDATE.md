# Updates and maintenance

- **ChatGPT Work:** [CHATGPT_UPDATE.md](CHATGPT_UPDATE.md), through Plugin Creator and the same existing plugin.
- **Codex:** [CODEX_UPDATE.md](CODEX_UPDATE.md), preserving the actual native entry, complete bundle and personal changes.
- **Fresh installation:** [INSTALL.md](INSTALL.md).

The complete update prompts start with `@plugin-creator` for Work or `$plugin-creator` for Codex. Follow each guide's selection instructions before sending; a copied invocation alone does not confirm tool availability. Codex's native update remains available without Plugin Creator and must preserve the existing local layout.

Pin all source reads to one full commit. Compare actual installed content first. Preserve existing
authorization, identity, user additions and providers. Ask only about material conflicts or changed
scope. A no-op comparison requires no save.

## Maintainer release procedure

1. Keep the canonical plugin under `plugins/framecore-work-creative-studio` and preserve its identity.
2. Synchronize versions and changelog. Preserve starters, logo, source bundles and unrelated modules.
3. Run bounded checks relevant to the change. Rebuild `config/install-sources.json` after final plugin edits.
4. Run `python3 scripts/package_release.py` to validate and package complete plugin/repository ZIPs.
5. Update the hosted plugin separately when requested and read back its saved version and affected source.
6. Commit and push. The release workflow creates a draft, uploads complete archives and inventories,
   verifies asset digests, then publishes the release at that source commit.
7. Verify the immutable tag and published assets. Old tags remain historical snapshots; new installations
   use the current guides.

A GitHub commit does not update hosted or local installations. The local packager and Codex installer
perform no publication or provider operations.
