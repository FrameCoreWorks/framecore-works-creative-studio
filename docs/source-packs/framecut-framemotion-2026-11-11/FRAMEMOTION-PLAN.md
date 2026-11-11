> Portable copy of the earlier planning edition. Read [the packet index](README.md) and the current repository handover for the owner's intake, applicability, implementation and cleanup workflow. Proposals are not automatically approved architecture.

# FrameMotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans after explicit implementation authorization. Future steps are not claimed executed.

**Goal:** Isolate complete motion-design knowledge, engines, examples and evaluation into FrameMotion, supporting independent creative work and exact Studio/FrameCut handoffs.

**Architecture:** Keep the two complete imported motion trees and their provenance, add a small intention-led entrypoint, localize dependencies, and preserve existing engine authoring contracts. New knowledge is decision-oriented and progressively loaded. Optional engines/exports remain explicit capabilities; no universal replacement timeline.

**Tech Stack:** Existing Canvas/DOM/GSAP/HyperFrames, optional React/Remotion, existing Python/JS motion tools and proposed pinned motion-reel1.3.0 vendor layer after rights/runtime review.

**Spec:** [DESIGN.md](DESIGN.md), [coordination plan](PLAN.md), [motion extraction](EXTRACTION-SUMMARY.md). Proposed repository `FrameCoreWorks/framemotion`; package root `plugins/framemotion/`. Neither is created by this task.

## Global Constraints

- All DESIGN constraints apply; planning/research does not authorize plugin building, source removal or publishing.
- Preserve all442 owned motion files plus explicit fonts/caption/reference/test/provenance closure. The875 mapped sources and44 starter archive members are inventory, not runtime/rights approval.
- Preserve current engine locks and exact copy. Source examples/FCWM brand preferences do not become universal product rules.
- Normal approved-board path and explicit scoped one-shot waiver are distinct; self-QA always remains. A request to make a film is not approval of an unseen board.
- Canvas/motion-reel and HyperFrames are the accepted planned default routes; Remotion is optional with current applicable licence evidence. No hidden engine fallback.
- FrameMotion owns local composition time; FrameCut owns global edit time. Reuse existing score/authoring contracts and versioned domain bindings.

## Review Focus

1. Same values and endpoints hide different velocity/path/render-order behavior across engines — M2/M3.
2. Alpha, precomp isolation, parenting or color interpretation changes the final image — M3/M5.
3. Duration/FPS/aspect change destroys readable hold, deterministic seek or partial-render joins — M3/M4.
4. Brand taste or motion-activity thresholds override an intentionally quiet/accessibility brief — M2/M4.
5. Copied fonts, captions, vendor notices or a private Linux provisioning overlay are unavailable standalone — M1/M6.

## Proposed file responsibilities

| Future path relative to repository | Responsibility |
|---|---|
| `plugins/framemotion/{plugin.json,.codex-plugin/plugin.json,.claude-plugin/plugin.json}` | Independent identity/version and host metadata |
| `plugins/framemotion/skills/framemotion/{SKILL.md,agents/openai.yaml}` | Thin intent/capability/knowledge entrypoint |
| `plugins/framemotion/skills/{hyperframes-workflow,remotion-video-production}/` | Complete imported motion implementations/references; internal engine routing by explicit plugin identity |
| `plugins/framemotion/knowledge/{index,source-ledger,decisions}.json` | Canonical source, scope, retrieval and conflict records |
| `plugins/framemotion/knowledge/motion/` | Professional decision cards and code-equivalence boundaries |
| `plugins/framemotion/engines/motion-reel/{vendor,adapter}/` | Unchanged licensed candidate and separately reviewed integration |
| `plugins/framemotion/resources/{fonts,captions}/` | Necessary standalone resources with provenance and local resolution |
| `plugins/framemotion/examples/{craft,brand-kits,format-variants}/` | Neutral examples; FCWM example isolated and rights checked |
| `plugins/framemotion/adapters/` | Studio/FrameCut envelopes and engine-specific authoring validation |
| `tests/`, `verification/` | Executable, visual, host and source-review evidence kept distinct |

Do not publish private research/source-film archives inside these paths. Retained research pointers live in private development records; shipped facts are properly sourced original distillations. Direct external links/import candidates in the extraction map require real closure testing before a package is accepted.

### M1: Freeze complete knowledge and executable preservation

**Files:** `knowledge/extraction-manifest.json`, `scripts/check_extraction.py`, `tests/extraction_loss_test.py`, imported trees and integration notices.

**Interfaces:** same manifest/checker contract as C1, implemented locally or reused as a development tool with pinned provenance; it is not a mandatory runtime framework.

- [ ] Add `test_all_442_owner_files_accounted_for`, `test_missing_font_notice_fails`, `test_integration_provenance_travels_with_vendor`, `test_no_unlicensed_film_archive_shipped`, `test_private_overlay_is_not_required`, `test_external_resource_closure`.
- [ ] Run `python3 -m unittest discover -s tests -p extraction_loss_test.py` on an intentionally incomplete staged target and inspect expected missing-resource failures.
- [ ] Copy complete owner trees, required resources and notices. Preserve vendor pins/bytes. Classify every research file/archive member as copy/adapt/distill/private/exclude-with-reason; no silent omission.
- [ ] Run `python3 scripts/check_extraction.py --manifest knowledge/extraction-manifest.json --source-root "$STUDIO_SOURCE" --target-root plugins/framemotion`; then isolated import/link/resource checks with Studio absent.
- [ ] Review and commit the authorized slice, recording old/new hashes for adaptations. Original Studio remains unchanged.

### M2: Build experienced-creator knowledge routing

**Files:** `skills/framemotion/SKILL.md`, `knowledge/motion/*.md`, index/source/decisions ledgers, `tests/knowledge_contract_test.py`, `verification/craft-rubric.json`.

**Interfaces:** decision cards/index use DESIGN's common fields. `knowledge/decisions.json` distinguishes hard constraints, user locks, profile defaults, source-supported technical facts, practitioner judgment and scoped exceptions. It is not a universal aesthetic score.

- [ ] Add schema/content checks for source links, explicit why/when, manual procedure, supported code mapping, non-equivalence, counterexample and review. Require negative examples for each high-risk mapping.
- [ ] Incorporate reviewed new research and complete existing AE/motion/FCWM practice with a conflict ledger. Cover hierarchy, timing/spacing/graphs, type/shaping, overlap/physical logic, compositing, sampling, 2.5D/3D/camera, color, sound and broad formats/web.
- [ ] Create separate routing cases for AE-language request, unfamiliar branded piece, quiet title, changing data values, long multilingual type, web interaction and partial correction. Explicitly load expert references on direct Remotion/HyperFrames routes.
- [ ] Run `python3 -m unittest discover -s tests -p knowledge_contract_test.py`. Later host evaluation must show the material influenced decisions, not merely that a file was read.
- [ ] Independently review source facts and counterexamples; commit accepted knowledge with honest evidence states. Preserve a held-out case set.

### M3: Local engines and verifiable manual-to-code equivalence

**Files:** imported runtime/resource resolvers, `engines/motion-reel/adapter/`, `tests/{engine_isolation,deterministic_seek,craft_equivalence}_test.py` and existing relevant Node tests.

**Interfaces:** each adapter exposes a capability record and frame-based deterministic render entry around its real authoring contract; no fictional shared renderer API is imposed on all engines. Declare coordinate system, FPS/time origin, alpha convention, color interpretation, supported effects and unavailable features.

- [ ] Add fixtures: parent translation with child opacity independent; changed anchor under rotation; matte inversion; precomp-style isolated versus flattened operation; before/after-range interpolation; fast moving thin element and fractional sampling; multilingual text shaping.
- [ ] Run adapter tests against existing implementations; unsupported equivalence must be reported explicitly. Correct E002 with real supported Remotion left/right extrapolation options and separate controls.
- [ ] Localize fonts/captions and package-root discovery. Keep motion-reel vendor unchanged; wrap synthesis, partial renders and failure propagation according to user scope. Do not download engines/models on import.
- [ ] Compare deterministic frames under sequential/shuffled/reverse seeks, full versus partial renders and FPS changes. Inspect actual composited edges on dark/light backgrounds; document color/blur differences rather than hiding them with loose thresholds.
- [ ] Run existing motion-toolkit/runtime/quality, anatomy/animate, kinetic, fonts/assets/kinds/variants and relevant sound suites. Preserve implementation-specific limits and commit the verified slice.

### M4: Revision-bound creative workflow and broad-format delivery

**Files:** `references/standalone-workflow.md`, existing score/approval adapters, `references/format-delivery.md`, `tests/{approval_revision,format_adaptation,partial_render}_test.py`, `tests/web_accessibility.test.mjs`.

**Interfaces:** creative receipt binds displayed board/spec/asset/copy hashes and either explicit approval or a scoped one-shot instruction reference. Reuse existing project/score structures; output variants reference the same source intention but their own layout/temporal solution.

- [ ] Add tests `test_unseen_board_not_auto_approved`, `test_one_shot_scope_does_not_remove_self_qa`, `test_new_copy_invalidates_acceptance`, `test_locked_engine_not_switched`, `test_quiet_brief_not_forced_to_drift`, `test_reading_window_survives_duration_change`.
- [ ] Implement missing standalone intake and revision binding; caller-provided Studio locks remain authoritative. A generic bare menu choice cannot override explicit constraints.
- [ ] Author one neutral piece in16:9,9:16 and1:1, plus a reduced-motion web variant; compare composition/readability and preserved message rather than center-cropping everything.
- [ ] Verify partial-range boundaries, audio cues and joins against full output at rational frame boundaries. Exporter claims require an actual artifact; unimplemented Lottie/Rive/glTF/alpha routes remain unavailable.
- [ ] Run the new tests and review actual variants. Commit without changing defaults in Studio.

### M5: Bind QA to final bytes and creative intent

**Files:** adopted quality helpers, `qa/evidence_manifest.py`, `tests/{qa_evidence,alpha_boundary,duration_boundary}_test.py`, existing craft lint/encode/flash review adapters.

**Interfaces:** `bind_evidence(inputs: list[Artifact], contract: Artifact, output: Artifact, observations: list[Check]) -> EvidenceReceipt`; hashes always bind current bytes/spec. Separate technical, visual, audio, accessibility and user verdicts; missing evidence never becomes PASS.

- [ ] Add negative fixtures for E001/E004–E008/E020/E027 where reused: short picture with long audio, same-size restored-mtime change, changed spec/dimensions, empty skip reason, palette transparency/alpha silhouette, CSS #abcd, browser/Python type mismatch.
- [ ] Run each on inherited code and confirm the particular false PASS/crash; pair it with a valid control.
- [ ] Fix adopted boundaries before enabling them as release gates. Preserve renderer differences as investigated compatibility issues; do not simply weaken tolerance to pass.
- [ ] Inspect first/last frames, scene boundaries±1, extrema, full-resolution type/edges, contact sheets and real-time playback; listen when audio exists. Record profile-specific intentional holds and unresolved subjective feedback.
- [ ] Commit after negative fixtures fail correctly and positive controls pass. Technical success alone cannot approve a concept or client delivery.

### M6: Standalone and companion release candidate

**Files:** independent manifests/install guides/source inventory, `adapters/{studio,framecut-request}.py`, `tests/standalone_smoke_test.py`, `verification/host-matrix.json`.

**Interfaces:** use I1–I3 in PLAN. Engine capability, plugin identity, generic envelope and domain authoring contract are separate pieces.

- [ ] Build an isolated package with no Studio/private runtime mounted; test actual selected default engine, captions/fonts and truthful optional-engine absence.
- [ ] Execute caller-mediated FrameCut motion request with exact local time/FPS/frame count/alpha, then test stale-context rejection. No recursive companion invocation.
- [ ] Verify metadata/discovery independently on supported hosts. Work packaging/materialization is actually tried through its available route, not assumed from ZIP size or a GitHub URL.
- [ ] Execute the bounded host matrix and export original neutral media with evidence. Separate source, package readback, actual host runtime and independent artifact inspection.
- [ ] Publish only after explicit authorization and architect review, retaining Studio fallback and a verified rollback. No old path retirement is included.

## Completion boundary

The standalone product must retain knowledge, reachable references, working resources, correct outputs and truthful limits. Deeper knowledge is accepted after source and applied review; neither a source count nor a successful render establishes senior-level judgment across arbitrary briefs. This task delivers the plan and research, not these future plugin implementations.
