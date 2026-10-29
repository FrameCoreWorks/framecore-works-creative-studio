# Hallmark integration

Reviewed 2026-10-24: [Nutlope/hallmark](https://github.com/Nutlope/hallmark/tree/7ec868225c6caa040558c321ee0fefa0e73f83a8), commit `7ec868225c6caa040558c321ee0fefa0e73f83a8`, source/skill version 2.0.0. [MIT licence](LICENSE). The owner requested analysis, recommendation and complete separate native Codex installation.

| Material | Decision | Boundary |
| --- | --- | --- |
| Task-first page anatomy and first viewport inspection | Adapt | Existing static design owner; reuse approved brief and brand |
| Before/after content and behavior inventory | Adopt method | Preserve copy, links, forms, handlers, routes, IDs and test hooks |
| Hard defects versus taste/finish observations | Adapt | Existing review budget; aesthetics are reasoned advice |
| Full 48 themes, previews, scripts and references | Separate native extension | Complete upstream payload, no thin reimplementation inside Studio |
| Global style bans, forced random theme and repeated intake | Exclude from Studio rules | User intent and approved system govern |
| Together key-triggered generation; Claude edit hook | No automatic activation | Separate explicit authorization and actual host support |

The [native routing contract](../../skills/static-graphic-design-creator/references/hallmark-native-routing.md) connects the optional skill to Studio. The [FrameCore Works Toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox) catalog (entry `hallmark`) records its pinned install route (owner decision 2026-10-29). Hallmark is for coded pages/app screens, not another motion runtime or Studio skill owner.

## Installation and evidence

The native Codex installation uses the complete pinned `skills/hallmark` subtree: 178 files, 6,841,340 bytes. The host's CODEX_HOME-aware skill installer preserves fixtures which upstream's own installer intentionally omits. All 178 upstream payload files matched before compatibility work. Codex rejected upstream agents/openai.yaml because dependencies was a sequence; the installed copy now uses the [narrow Codex metadata replacement](codex-openai.yaml) (dependencies.tools object and singular default_prompt). The other 177 source files remain byte-identical. The [source manifest](source-manifest.json) records both pinned original hashes and the one declared replacement. The first browser smoke also left 11 generated screenshot/cache files under the installed fixture directory; these are explicitly excluded from source-payload parity, so complete current-directory equality is not claimed. They are retained as test evidence. Discovery, executable lint and browser evidence are recorded separately; a filesystem copy alone is not active-host verification.

Upstream `install.mjs --remove` removes **all known harness copies**, even with a harness flag. Do not use it to remove only Codex from a live machine. Prefer the Toolbox entry's agent-scoped removal, or the managing host's removal flow for a CODEX_HOME-specific copy. The installer lifecycle test used an isolated temporary home, never the real user home.

## Rights and data

The 755 Wikimedia entries are metadata, not a uniformly MIT photo library. Verify each chosen image's file page, creator, source and licence; preserve attribution and applicable share-alike terms. Themes' font links retain their own rights. A screenshot is source evidence, not permission to copy a page. No paid generation, private upload, automatic hooks or host configuration edits are implied by installation.

## Verification scope

Pinned source and native payload inspected; upstream reference checker and disposable installer lifecycle run locally. Browser smoke checks use synthetic local fixtures. Fresh Codex discovery is separate from Studio integration behavior; unexecuted clients remain NOT_RUN. Keep observations in the release record current rather than treating upstream showcases as host tests.

## Codex metadata compatibility

Before replacing an existing native agents/openai.yaml, save a dated copy. Use only this integration's codex-openai.yaml for the reviewed 2.0.0 payload; do not change its SKILL.md or runtime resources. A fresh Codex invocation must discover the skill and have no Hallmark metadata-loader warning. This is an installation compatibility override, not a modified upstream release. Re-evaluate it when upstream fixes its schema. Claude's native skill files are unaffected.
