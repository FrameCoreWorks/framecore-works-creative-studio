# Studio companion implementation

Owner authorization: implement the approved companion design, publish the repository first, then update the existing ChatGPT plugin. Change ID: CW-20261022-02. Baseline main: b92b45b227dc667934c81080afebcdd3c0163b29. Branch: cw/superpowers-companion-foundation-2026-10-22. Target release: 1.122.0, subject to a fresh main check.

## Contract

Superpowers is the first optional, separately installed companion. Studio keeps all 37 owners, the complete localized welcome, creative approvals, FrameCut's full storyboard and one timeline/QA loop. Discover and read actual installed skills; no bundled Superpowers, account identifiers, automatic installation or new connector. Preserve the hosted private overlay. The owner's explicit implementation request authorizes execution and publication without another design-approval pause.

## Tasks

- [x] Registry: extend the existing reader with `catalog_manual` host status, navigation/verification/refresh/removal guidance and `recommendation_priority: first`. Reject executable installer fields for that status; preserve existing pinned installers and catalog ordering. Add behavioral tests to `tests/extensions_test.py`, observe RED, implement, observe GREEN.
- [x] Workflow: reconcile the hosted native routing reference and 12 cases into public source; link shared authority and QA, the six technical entry points, owner/handoff maps and existing state templates. Add first-configuration guidance in existing references and `extensions.com.openai.onboardingSkill` in both OpenAI manifests, pointing to the existing orchestrator. Installation guides recommend the companion before providers. Preserve descriptions, startup excerpts and the 32,000-byte orchestrator budget. Add focused wiring regressions and exercise bounded source-guided scenarios.
- [x] Review/release: run canonical validation and the complete required suite, inspect unchanged snapshots, obtain one independent whole-branch review, fix material findings with regression evidence, prepare 1.122.0 through the release helper, regenerate inventory and ZIP. Keep fresh installed-client checks explicitly NOT_RUN when unavailable.
- [x] Publication: publish the reviewed tree to the side branch and main with expected-head guards; verify GitHub release assets. Reconcile the current hosted archive against public history, preserve private-only files and overlapping integrations, update the existing plugin with its current release guard, read back the complete saved package. Record actual evidence and remaining limits.

## Interfaces and checks

- `catalog_manual`: required `manual_steps`, `writes`, `verify`, `after`, `remove`; no `plan`/`install` command. Reviewed commit is provenance, not a marketplace version pin. Expose recommendation priority in list/show/catalog JSON and human output.
- Setup: host-triggered setup or explicit installation/first configuration loads the setup section; ordinary bare-name welcome is unchanged. Track choice and availability separately in existing Project State. Installed, declined, deferred and unavailable are not the same state. Never infer a fresh installation from absent project state alone.
- Support receipt: decision, Studio owner, trigger, selected skills, support status, artifact revision, acceptance criteria, evidence, next owner. A successful read is not an executed method/render.
- Source provenance: upstream obra/superpowers at 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b, reviewed 2026-10-22. OpenAI onboarding field documented at https://developers.openai.com/plugins/build/plugins; no corresponding Claude setup field is assumed.

## ReviewFocus

1. Catalog unavailable or a user installs but skills remain unreadable: no false activation or shell fallback.
2. Fresh marketplace/ZIP setup reaches the recommendation; bare invocation preserves the complete welcome.
3. Already installed, declined or deferred: no repetitive offers; no invented cross-chat memory.
4. Accepted FrameCut board with a timing fault: support returns to the same owner/revision without a new intake, sample or QA loop.
5. Raster correction or no-shell host: keep the existing image-edit/plan route; no fictional repository, agent or render.

## Execution notes

The cloud skill resources expose instructions, not an executable local `sdd-workspace` helper. This checklist and the verification records are the execution ledger. The skill's requested one whole-branch reviewer is used; no implementation delegation is needed. Source-guided scenarios are distinct from fresh installed-client tests.

### Observed baseline and focused checks

The unmodified 1.121.0 source-guided setup case recommended earshot/Motion Designer after a tool inventory, with no Superpowers recommendation. The accepted-board timing case proposed a fixed six-frame correction without first distinguishing constant offset from accumulated drift. Other controls retained image editing and full-board acceptance. Five cases were exercised by a fresh-context agent; this is source-guided evidence, not host activation.

Registry RED: five failing tests (unknown catalog status, missing first-priority handling and Superpowers entry). Wiring RED: the onboarding field was absent. After implementation: 21 extension tests pass. Canonical validation initially caught a protected completion-evidence sentence moved out of the entry; restoring that sentence fixed the check. No validator guard was weakened. The entry is within 32,000 bytes and descriptions remain 7,700 characters.

Five source-guided after-cases recommend Superpowers first, retain unverified activation, diagnose constant offset versus drift, preserve raster editing and require the unseen full board without a sample. One response over-inferred render limits from absent shell, so the common contract now explicitly distinguishes shell from other code/render capabilities. These exercises executed no media or installed-host operation. Independent whole-branch review found no Critical/Important issue; its one whitespace finding is fixed. Full release checks follow.

### Completion

Local release checks: 225 Node and 535 Python passes, 25 skips, zero failures; canonical validation PASS. One focused follow-up with Python/render available but no shell correctly retains execution, resolving the observed over-inference. Release source fce01e2fdb9e3faec744e2965eba687f14c3c9d7 is published as v1.122.0; the downloaded ZIP, inventory and player match the build, all 1,552 package files match the tag. The notes-refresh header mismatch was corrected separately without changing package bytes; the original failed run is retained in the publication record alongside the successful correction. The release workflow itself passed the full suite and published the verified assets. Additional source-check runs have their actual observed status in the record.

Existing ChatGPT plugin updated from 1.119.7 to 1.122.0, release pluginrel_6ada1691510c8191876a77b0accd8ce9. Complete readback: 1,604 paths, 1,603 byte-identical to the merged candidate and one JSON-equivalent formatting normalization. All 52 private-only files are byte-preserved. Four installed continuity guards pass. Current-container runtime check is LIMITED (24/59 available); recipes remain preserved, no runtime migration or render was claimed. Fresh ordinary ChatGPT, Work, Codex and Claude behavior stays NOT_RUN. Main and the task branch are synchronized by guarded ref updates; no branch deletion.
