> Portable copy of the earlier planning edition. Read [the packet index](README.md) and the current repository handover for the owner's intake, applicability, implementation and cleanup workflow. Proposals are not automatically approved architecture.

# FrameCut Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans after explicit implementation authorization. All checkboxes below are future work, not completed tests.

**Goal:** Isolate the complete FrameCut editorial practice and engine into a standalone plugin that can accept Studio tasks without losing meaning, media integrity, knowledge or review requirements.

**Architecture:** Preserve all35 owner files, localize caption/board/font dependencies, retain the native project and source-map model, and add a thin companion adapter. Canonical editorial knowledge belongs to FrameCut; small motion-facing summaries are versioned exports. Studio source remains intact.

**Tech Stack:** Existing Python/FFmpeg, rational frame/time model, JSON projects, actual caption/board helpers, optional OTIO and optional external tools.

**Spec:** [DESIGN.md](DESIGN.md), [coordination plan](PLAN.md), [extraction evidence](EXTRACTION-SUMMARY.md). Proposed repository `FrameCoreWorks/framecut`; package root `plugins/framecut/`. Neither has been created.

## Global Constraints

- All DESIGN global constraints apply. No source move/delete, new plugin/repo, implementation or publication is authorized yet.
- All35 existing owner files and their source hashes must be retained in the preservation ledger; the157 mapping rows include overlapping support/provenance and are not a feature count.
- Standalone operation must not require Studio or its cache paths. Preserve supplied source media and accepted finals; edits create revisions.
- Existing `framecore-task-request/1`, `framecore-task-result/1`, native project and motion request remain the authority; no second timeline.
- Knowledge of a native NLE feature is distinct from FrameCut capability. Explicitly disclose unsupported color, multicam, tracking, optical-flow and interchange routes.

## Review Focus

1. Source PTS, record frames, display timecode and audio samples disagree under VFR/fractional FPS — C3/C4.
2. Trimming silence removes meaning, a breath, consonant or an intentional reaction — C2/C4.
3. Caption text, numeric dialogue or long board notes disappear while a checker says PASS — C4.
4. A reused motion asset belongs to a stale edit/copy/geometry request — C3 and coordinated I2.
5. A valid EDL/OTIO object loses information when opened in the destination NLE — C5; parser validity is insufficient.

## File responsibilities

| Future path, relative to repository | Responsibility |
|---|---|
| `plugins/framecut/{plugin.json,.codex-plugin/plugin.json,.claude-plugin/plugin.json}` | Independent identity/version/host metadata |
| `plugins/framecut/skills/framecut/SKILL.md` and `agents/openai.yaml` | Editorial entry and domain knowledge routing |
| `plugins/framecut/skills/framecut/assets/framecut/` | All current engine modules/schema/effect manifests, with source-preserving adaptation |
| `plugins/framecut/skills/framecut/scripts/edit_export.py` | Retained legacy exporter dependency |
| `plugins/framecut/skills/framecut/assets/captions/` | Local needed captions runtime; provenance records canonical component owner |
| `plugins/framecut/skills/framecut/assets/board/` and `assets/fonts/inter/` | Board runtime and required font/licence closure |
| `plugins/framecut/knowledge/{index,source-ledger,decisions}.json` | Claim ownership, import history, decision scope and routing |
| `plugins/framecut/knowledge/editorial/` | Source-checked decision cards, not copied manuals |
| `plugins/framecut/examples/editorial/` | Original worked cases and explicitly licensed media fixtures |
| `plugins/framecut/adapters/studio.py` | Generic envelope and domain validation boundary |
| `tests/` and `verification/` | Regression/behavior/host/native-app evidence, kept distinct |

Paths are proposed package layout. Copy/adaptation maps must be reconciled against actual imports before creation. Keep all12 existing effect manifests; extraction does not justify dropping a capability because it is unfamiliar.

### C1: Preserve the complete owner and dependency closure

**Files:** create `knowledge/extraction-manifest.json`, `scripts/check_extraction.py`, `tests/extraction_loss_test.py`; populate package paths above only after authorization.

**Interfaces:** `check_extraction(manifest_path: Path, source_root: Path, target_root: Path) -> list[Issue]`, with each `Issue` containing source ID, rule and path. Manifest record: source path/hash/version; target path/hash; disposition; adaptation reason; canonical owner; rights/notice; tests; retained source/rollback reference.

- [ ] Add tests `test_each_owner_file_accounted_for`, `test_missing_caption_dependency_fails`, `test_board_font_license_required`, `test_unmapped_source_fails`, `test_private_input_not_shipped`, `test_no_external_cache_dependency` with477-source inventory filtered to FrameCut and its explicit support closure.
- [ ] Run `python3 -m unittest discover -s tests -p extraction_loss_test.py`; verify the incomplete staged package fails for the missing path/notice, not an unrelated import.
- [ ] Copy the complete owner, notices and selected local support files; adapt caption/board/font resolvers and legacy exporter paths. Preserve vendor bytes where required and put our wrappers beside them.
- [ ] Run the same tests and `python3 scripts/check_extraction.py --manifest knowledge/extraction-manifest.json --source-root "$STUDIO_SOURCE" --target-root plugins/framecut`. Require zero unmapped owned files, missing runtime resources, missing notices or undeclared private transfers.
- [ ] Review diff and commit the authorized slice. Original Studio path/hash comparison must remain unchanged.

### C2: Turn professional editorial knowledge into usable decisions

**Files:** `knowledge/editorial/*.md`, `knowledge/index.json`, `knowledge/source-ledger.json`, `examples/editorial/`, `tests/knowledge_contract_test.py`, `verification/craft-rubric.json`.

**Interfaces:** each decision card implements the fields in DESIGN; the entry skill selects topic IDs by task intention. The index carries `id`, `owner`, `topics`, `triggers`, `reference`, `version`, `evidence_states`, `capability_limits`; it does not claim an engine feature from topic presence.

- [ ] Add contract tests for each card's source/scope, alternatives, manual operation, supported command or declared gap, counterexample and output review. Require that an unsupported feature has a human/native-NLE handoff, not a fictional CLI command.
- [ ] Incorporate reviewed source research, preserving provenance and English/Polish source examples where appropriate. Cover selects/paper edit, performance, continuity/ellipsis, trims/handles, split edits/dialogue, music structure, sync/proxies, timebases/retime, color/sound, captions and conform.
- [ ] Create original paired exercises: a hesitant answer with meaningful pause; an off-beat cut that preserves a thought; a trim lacking handles; a slip versus roll; a VFR source; a misleading audio crossfade; an interchange-loss case. Keep a separate held-out set.
- [ ] Run `python3 -m unittest discover -s tests -p knowledge_contract_test.py`. Later host probes must show correct material loaded and applied; static phrase presence does not satisfy the craft rubric.
- [ ] Review editorial meaning and source support independently, then commit accepted cards. Label calculations, engine execution, native-app practice and listening separately.

### C3: Standalone intake, revision and approval

**Files:** `skills/framecut/SKILL.md`, existing engine context/project functions under `assets/framecut/`, `references/standalone-workflow.md`, `tests/standalone_state_test.py`.

**Interfaces:** reuse native project, revision and `framecut_context`; standalone entry supplies brief/copy/assets/review locally. Studio input projects these same values; it does not create a competing approval store. Original request hash and accepted creative revision travel with any motion request.

- [ ] Add tests `test_no_studio_import_required`, `test_changed_copy_invalidates_board`, `test_technical_revision_preserves_valid_creative_context`, `test_missing_consent_is_not_approval`, `test_explicit_one_shot_scope_retains_self_qa`, `test_motion_attachment_rejects_changed_brief`.
- [ ] Run `python3 -m unittest discover -s tests -p standalone_state_test.py` against an isolated package path containing spaces and Polish characters.
- [ ] Implement only missing standalone intake/resource/receipt behavior around existing project semantics. Preserve expected errors, revision locks, cancel/resume and atomic edits.
- [ ] Repeat tests with Studio and optional companion paths unavailable. Reopen a saved project and verify source hashes, unresolved feedback and acceptance state survive.
- [ ] Commit the reviewed slice; compare existing edit behavior on shared fixtures before and after extraction.

### C4: Repair inherited false-PASS boundaries before using them as gates

**Files:** local caption/board adapters, current review/delivery checks selected into FrameCut, `tests/{caption_boundary,board_boundary,delivery_evidence,audio_event}_test.py`.

**Interfaces:** validation returns machine errors tied to input/source revision and final output bytes. Technical, visual and audio review states stay independent. The exact copied check API is retained unless an explicit versioned change is reviewed.

- [ ] Add negative fixtures from audit E012/E013/E014/E016/E022 and any imported E001/E004–E008 checks: long clipped notes/header; negative time; literal entities and numeric dialogue; missing onset events;1-second picture with5-second audio; changed spec; same-size same-mtime changed bytes.
- [ ] Require the tests to fail on the inherited defect. Strengthen the onset assertion to require the expected event count before comparing timing.
- [ ] Fix only adopted paths and retain paired passing controls. Do not treat every nonzero exit as the intended rejection.
- [ ] Run existing six FrameCut suites plus relevant caption/export/board tests and the new boundary suites using the canonical media environment and full FFmpeg. Preserve fractional FPS, VFR PTS, half-open ranges and audio-sample mapping.
- [ ] Render supplied/licensed fixtures; inspect cut±1 frames, full dialogue/audio playback, text and receipts. Missing listening or native visual review remains unexecuted. Commit with before/after reproduction evidence.

### C5: Interchange and delivery without false equivalence

**Files:** existing export/handoff paths, `references/nle-interchange.md`, `verification/interchange-matrix.json`, `tests/interchange_loss_test.py`, `examples/editorial/turnover-fixture/`.

**Interfaces:** each export states format/version, cuts retained, transforms/retimes/audio/captions/effects retained or omitted/baked, relink map, source FPS/timecode and handle policy. Unknown fields are not silently marked supported.

- [ ] Define a neutral reference edit with two FPS sources, a dissolve, separated dialogue, markers, caption, retime and motion overlay. Save a reference render/source-map receipt.
- [ ] Add `test_loss_report_lists_unrepresentable_features`, `test_missing_media_does_not_pass`, `test_export_preserves_source_ranges` and run `python3 -m unittest discover -s tests -p interchange_loss_test.py`.
- [ ] Keep current EDL/OTIO capabilities and document actual limits. Add another format only after its behavior is selected and tested; a filename extension is not an implementation.
- [ ] In each available named NLE, import/relink and compare timeline/source ranges plus rendered picture/audio to the reference; record exact app/version and operator steps. Unsupported/unavailable applications stay NOT_RUN.
- [ ] Complete package tests, manifests/notices and isolated fresh-host probes. Final release requires applicable native/perceptual evidence; no promise of four-NLE fidelity from parser success.

## Completion and transition

FrameCut standalone passes before Studio begins selecting it. Then execute I1–I3 in PLAN. The source fallback remains intact; its retirement is a separate decision. Research knowledge may be mature enough to advise on a technique while native execution remains unavailable; both facts must be visible to the user. No checklist item here has been executed as plugin implementation in this planning/research task.
