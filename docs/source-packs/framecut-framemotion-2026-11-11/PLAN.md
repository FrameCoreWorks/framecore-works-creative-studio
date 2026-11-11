> Portable copy of the earlier planning edition. Read [the packet index](README.md) and the current repository handover for the owner's intake, applicability, implementation and cleanup workflow. Proposals are not automatically approved architecture.

# FrameCut and FrameMotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans only after implementation is authorized. This document is a planning deliverable, not an instruction to start building.

**Goal:** Extract complete, independently usable motion and editorial knowledge/capabilities into FrameMotion and FrameCut, retaining reliable Studio companion workflows.

**Architecture:** Use incremental domain extraction with local dependency closure and existing versioned contracts. Preserve Studio source during transition. Maintain one canonical owner per knowledge topic and explicit versioned exports for standalone consumers.

**Tech Stack:** Existing Python/FFmpeg and JSON FrameCut project; existing motion Canvas/DOM/GSAP/HyperFrames/Remotion and packaged engines; pinned source/rights manifests; no new mandatory framework.

**Spec:** [DESIGN.md](DESIGN.md). All target paths and interfaces below are proposals for architect review.

## Global Constraints

- Planning and source research are authorized; product implementation, new repositories/plugins, source moves and publishing are not started.
- Baseline Studio1.174.1 commit2942af902909b83441fc4c428d9debd532500c5a; freeze latest accepted source again before building.
- Preserve every existing Studio path, vendored snapshot, licence and private overlay. No mandatory dependency on another plugin installation.
- Host/caller dispatches companions; retain current generic major1 and stronger domain binding. No second master timeline.
- Repository-maintained text is English; user summary is Polish. FCWM brand/private material is not a public default.
- Existing installations/models are reused. No API spend, uploads or paid research implied by the plan.
- Claude is principal architect; cross-provider approval remains pending after earlier OAuth401. Codex checks below are supplemental, not a substitute approval.

## Review Focus

1. A standalone render with Studio/private overlays absent must still find captions, fonts and board runtime — owned by C2/M3.
2. A changed request, asset, copy or duration must invalidate stale acceptance and output — C3/M4 and I2.
3. A technically valid artifact with lost words, missing picture or bad alpha must fail — C4/M5.
4. A quiet/accessible or explicit one-shot brief must preserve the user's intent and scoped permissions — C3/M2/M4.
5. A host without execution capability must report its limit, not fabricate an installed/rendered result — I3.

## Work packages and dependencies

| Phase | Deliverable | Dependencies | Gate |
|---|---|---|---|
| R | Current knowledge extraction + deeper source research + independent challenge | Existing docs/source | Source claims, examples, contradictions and gaps reviewed |
| A | Architect-reviewed design and exact ownership/contract choices | R | Claude review and user implementation instruction |
| C | Standalone FrameCut | A | C1–C5 in FRAMECUT-PLAN |
| M | Standalone FrameMotion | A; can follow C to reuse lessons | M1–M6 in FRAMEMOTION-PLAN |
| I | Studio compatibility and cross-domain handoff | C and M | I1–I3 below |
| D | Independent distribution and transitional routing | I | Actual package/host receipts; no source retirement |
| X | Optional retirement of old Studio implementations | Stable transition and separate user scope | Exact path list, rollback and guarded readback |

Research for both domains proceeds in parallel now. Implementation order FrameCut→FrameMotion is a proposal, not a claim that FrameCut has no dependencies.

### I1: Define and test the adapter boundary

**Files:** future `plugins/<provider>/adapters/studio.py`, `contracts/domain-request.schema.json`, `tests/companion_adapter_test.py`; Studio existing `skills/pipeline-core/assets/companion-{contract.schema,registry}.json` and `skills/delivery-documentation/scripts/companion_intake.py`.

**Interfaces:** `validate_request(request: dict, domain_path: Path) -> ValidatedRequest`; `emit_result(request: ValidatedRequest, outputs: list[Artifact], checks: list[Check], state: str) -> dict`. `ValidatedRequest` preserves the original file digest plus task/provider/operation and domain revision; `Artifact` has role/path/hash/size; `Check` retains actual state/evidence and unexecuted reason. Reuse exact generic schema field names in implementation; these Python type labels are adapter design, not existing source APIs.

- [ ] Add fixtures for standalone/Studio origin, stable task ID, correct hash, wrong task/provider, changed parameters, missing review and partial/blocked result.
- [ ] Run `python3 -m unittest discover -s tests -p companion_adapter_test.py`; assert expected failures identify missing adapter behavior.
- [ ] Implement envelopes around current engines; validate selected schema definitions and domain request, not only generic root JSON.
- [ ] Run the same tests; require every output resolves inside the declared project root and matches its reported bytes. Keep output initially not_reviewed.
- [ ] Commit the reviewed slice only under the authorized repository workflow; no public release yet.

### I2: Preserve FrameCut–FrameMotion binding

**Files:** FrameCut `skills/framecut/assets/framecut/fc_render.py`, FrameMotion `adapters/framecut-request.py`, both `tests/motion_handoff_test.py`; caller routing documentation.

**Interfaces:** keep existing motion request/context checks. FrameCut owns global time; FrameMotion consumes local frames0…N−1 and returns exactly the requested FPS/geometry/alpha with original request and authoring-contract digests.

- [ ] Write `test_request_roundtrip_keeps_local_origin`, `test_changed_copy_rejects_old_motion`, `test_retime_does_not_silently_fit`, `test_missing_alpha_rejected`, `test_unchanged_context_technical_revision_allowed` using real current domain request output.
- [ ] Run the tests against adapters before implementation and capture the failing reason.
- [ ] Implement caller-mediated dispatch and selected-engine contract validation, retaining `attach-motion --request` after generic intake.
- [ ] Render an original neutral overlay, attach it, revise duration and prove stale attachment is rejected; compare final frame ranges and composited alpha.
- [ ] Review source/receipt diffs and commit the slice. No companion invokes another implicitly.

### I3: Transition routing and host evidence

**Files:** Studio existing registry/routing/extension metadata and preserved owner SKILL entrypoints; future `tests/companion_selection_test.py`, `verification/host-matrix.json`, per-plugin install guides.

**Interfaces:** discovery returns actual readable host skill identity/capability/version or an explicit missing/unreadable state. Selection returns one provider per job; failure after a job starts does not silently choose another.

- [ ] Add tests for absent/compatible/newer-reviewed/incompatible companion, duplicate skill IDs, wrong private instance, no execution tools and failure after job start.
- [ ] Preserve default Studio path until explicit transitional selection is made; record chosen provider and request hash before execution.
- [ ] Run `python3 -m unittest discover -s tests -p companion_selection_test.py`; require no duplicate output or hidden install/download.
- [ ] Execute the bounded24-case host matrix from DESIGN, recording source-read trace, commands, bytes where accessible, and honest unknowns. Reuse permitted existing environments.
- [ ] Review source, saved package and actual host behavior separately. Publish new identities only under explicit implementation/release scope; guarded updates never overwrite another plugin's private overlay.

## Knowledge acquisition and transfer acceptance

The research outputs are input to R, not completed implementation. Each claim has source and evidence level; each decision card states intent/manual operation/code mapping/counterexample/review. A second specialist challenges at least the high-risk claims and worked calculations. Source support does not prove native operation, render fidelity, listening or judgment on unseen material.

Before copying new research into a shipped skill, assign stable topic IDs, remove duplicated/contradictory authority, verify rights and current version-sensitive facts, route the entrypoint to the relevant cards, and add a held-out applied evaluation. Maintain unfamiliar briefs outside the examples used to write the cards.

## Review and completion records

The original local edition retains `PLAN-REVIEW-LOG.md`, `SOURCE-REGISTER.json`, `RESEARCH-INDEX.md` and `verify_plan.py`; those local-only records are not shipped in this portable packet. See REVIEW-STATUS.md here. The verifier checks existence, hashes/inventories, complete owner mapping, evidence labels and document links. It cannot prove the proposed code works or certify professional expertise.

The deliverable is complete when both plans, researched knowledge and their reviews are available with explicit limits. The implementation remains unstarted. Claude receives a self-contained handover; no message is sent into his sessions without authorization.
