# Temporary takeover and Superpowers foundation, 2026-10-22

Change: CW-20261022-01. Origin: ChatGPT Work. Owner request: take over temporarily from Claude, inspect repository and hosted plugin, and create a separate branch for the Superpowers companion foundation.

## Current observed state

| Surface | Observation | Evidence scope |
| --- | --- | --- |
| GitHub main baseline | `b92b45b227dc667934c81080afebcdd3c0163b29` | Fresh clone and remote head read; clean starting tree |
| Shared source | 1.121.0; 37 skills; 1,549 canonical package files | Current manifests and canonical validator |
| Latest source work | Pixel effects/Pixel Plugin in 1.121.0; subsequent Claude handover and Open Design plan | Current Git history, changelog, release status and handover |
| Saved hosted Studio | 1.119.7; 1,595 inventory paths | All 16 inventory pages, all 37 entry skill bodies, central Superpowers reference, stored cases and selected routing files read |
| Native Superpowers integration | Reference plus 12 stored cases; six explicit entry links | Workflow Orchestrator, Pipeline Core, Motion Graphics, FrameCut, Remotion and Static Graphic Design; no behavior test inferred |
| Superpowers in this session | Installed/enabled; 15 skills visible; relevant process skills successfully read and used | Current catalog and skill reads, not a fresh-client Studio integration test |
| Working branch | `cw/superpowers-companion-foundation-2026-10-22` | Owner explicitly authorized a separate branch; no main merge or hosted write in this task |

Versions differ legitimately across concurrent work. Neither the 1.118.0 hosted row in `RELEASE_STATUS.md` nor Claude's pre-1.119.0 estimate in the previous handover describes the currently observed saved plugin. This document records a new observation without rewriting historical release evidence. It is not a complete byte comparison of the 1,595 hosted files with public source; other hosted content remains outside this read scope.

The public orchestrator is 31,918 bytes, leaving 82 bytes. The saved hosted one is 32,391 bytes, 391 over the repository limit. The fresh canonical check reports 7,700 aggregate description characters against 7,800. Preserve these budgets when reconciling the native support links; the proposed design addresses the integration point, not an already-applied repair.

No private provider configuration or full hosted package has been copied into this branch. Another owner-directed conversation owns live plugin integration. Re-read its current release before any later update.

## Work left by Claude

Authoritative carry-forward sources:

- [Claude handover](handover-claude-code-2026-10-22.md).
- [Open Design 0.26 implementation plan](superpowers/plans/2026-10-22-open-design-0.26.md), present as a plan with unchecked tasks, not executed by this takeover.
- [FrameCut audit](framecut/audit-2026-10-22.md).

Open Design work includes the registry/privacy/rights update, photosensitivity screening, transcript sanity checks, audio/cover encode checks and bounded motion/caption guidance. It remains separate and paused; the Superpowers request does not authorize silently resuming that queue. Do not run external repository code merely because the plan links to it.

Owner-only or fresh-client checks still include ordinary ChatGPT/Work startup, plain storyboard acceptance questions and proposed direction quality. FrameCut decisions still include caption settings per deliverable, performance, delivery fingerprints and sound coverage in board receipts. Existing source tests and stored scenario inventories do not resolve these product/host questions.

## Foundation delivered on this branch

The [companion design](superpowers/specs/2026-10-22-studio-companion-design.md) defines:

- First installation recommendation, manual host catalog routes, already-installed/declined/unavailable cases.
- Separately maintained Superpowers, no skill extraction or bundling.
- Shared routing and return contract, coverage of all 37 current Studio skills, direct specialist entry points.
- Existing brief, board approvals, master timeline and QA retained by Studio.
- Registry compatibility work, file wiring map, 18 acceptance scenarios and repository-first rollout.

This is a documentation foundation for review. It changes no shared package, source version, welcome, media runtime or hosted release. It does not claim that public routing or new installation behavior has been implemented.

## Verification and branch status

The [verification record](../verification/superpowers-foundation-2026-10-22.json) records canonical PASS and a successful full `scripts/check_all.sh` run: 225 Node tests passed, 13 skipped; 54 Python suites collected 541 tests, with 12 skipped and no failures. Skipped optional browser/dependency/client checks were not independently run. The documentation review confirms all 37 owners are covered once, relative links resolve and the shared package has no diff. Source validation, branch publication and hosted observations remain separate. All 18 new companion behavior scenarios and fresh installed-client behavior remain NOT_RUN at this foundation stage.

At the initial and pre-commit remote reads, `ccr-06247e92-aihwc6` points to `cb431a6`, `ccr-9d0ac477-rf33kp` points to baseline `b92b45b`, and `ccr-b6d36a1c-4hszow` points to `daab582`. All three are already contained in baseline main (ancestry checked). Leave their deletion to the owner. `gh-pages` is the motion-player publication branch and is not a disposable task branch. Recheck remote heads before resuming.

## Resume here

1. Read this takeover, current AGENTS rules and the companion design; check its review status with the owner's actual reply.
2. Re-read main and current hosted plugin before planning implementation. Preserve the other conversation's latest compatible work.
3. With the architecture approved, load Superpowers `writing-plans` and prepare a bounded implementation plan. Use the current skill catalog; installation in one host does not prove another host has it.
4. Continue on this owner-requested branch. Do not apply the older main-only rule or merge the foundation into main without the corresponding scope.
5. Implement and release only the approved companion scope; Open Design and other pending creative/runtime work remain separate.
