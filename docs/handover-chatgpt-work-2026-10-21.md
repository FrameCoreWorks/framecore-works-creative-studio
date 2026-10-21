# Handover to Claude Code, 2026-10-21

Origin: ChatGPT Work. Coverage: work completed on 2026-10-20 and 2026-10-21, through the verified publication of 1.115.0. Handover change: `CW-20261021-04`. Repository baseline: `06edb3c92d55f5395cf0a63988a7dd11ad80063a` on `main`.

## Current owner decision

**Pause development. The owner will test FrameCut, Motion Graphics and other Studio modules in actual use.** This document transfers context to Claude Code; it is not an instruction to begin another audit, implement research candidates or finish aspirational features. Resume implementation only for the owner's findings or a new explicit task, and reproduce the concrete issue before changing its smallest cause.

The newest FrameCut direction is onboarding and necessary questions, a complete visual storyboard of the whole reel, user feedback, corrections and acceptance of that board, then final rendering and review. A video sample is optional. This supersedes the sample-first guidance in 1.114.0.

Read current [AGENTS.md](../AGENTS.md), this handover, [release status](../RELEASE_STATUS.md), [the latest ledger entries](development-ledger.md) and the actual Git head before writing. The [2026-10-20 handover](handover-chatgpt-work-2026-10-20.md), older project-book snapshots and original work orders are historical context; their old versions, branch rules, publication rules and unfinished-task statements are not current instructions. Reply to the owner in Polish; maintained repository documentation remains English.

## Verified state at the handover baseline

| Surface | Recorded state |
| --- | --- |
| Repository | `FrameCoreWorks/framecore-works-creative-studio`, `main` at `06edb3c92d55f5395cf0a63988a7dd11ad80063a` before this documentation change |
| Shared package | `plugins/framecore-work-creative-studio/`, version **1.115.0**, 1516 files, 37 canonical skill IDs |
| Release source | `aea1191742f5ae2747610a8a9e8625cfd4217037`, tag [v1.115.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.115.0) |
| Subsequent repository records | `732ae4b` corrects the release-notes heading and records saved-plugin verification; `06edb3c` records verified publication |
| Existing hosted Studio | Plugin `plugins_6ab8e226cbd48191b661cb2ea24d0351`, saved version **1.115.0**, release `pluginrel_6ad871c551e081918f643baaaeb5b3bc` |
| Hosted comparison scope | All 17 affected files verified: 16 byte-identical and the Codex manifest JSON-equivalent after Unicode escaping normalization. App binding checked; complete inventory retains 1565 paths. Private overlay preserved. This is not a claim of whole-package byte equality. |
| Fresh installed clients | 1.115.0 behavior in ordinary ChatGPT, Work, mobile, Codex and Claude remains **NOT_RUN**. Saved-package readback and source-guided dialogues are separate evidence. |
| Owner mobile report | After the earlier hosted-only Sunra MCP removal, the owner said “Działa”: mobile @ invocation is **PASS_REPORTED** for that recovery, not a full FrameCut or 1.115.0 acceptance test. |
| Branches | `main`, `gh-pages`, existing `ccr-b6d36a1c-4hszow`. The ccr head `daab5828bdd4025280ebe2af5f5d5cccacae4a5c` is already an ancestor of main and was preserved. |

These are dated observations. Re-read the current branch and current hosted release before a future change; another authorized surface may have advanced either one.

## Work completed across the two days

### 1. Interrupted audit closed: 1.111.1

Recovered unfinished fixes and retained compatible Claude Code work. The closure corrected exact-copy comparisons that tolerated currency/case/punctuation changes, guarded URL redirects and DNS targets, fixed development-origin attribution, reconciled startup and sound ownership, and strengthened candidate identity records for host evaluations. Audio profiles now use their own measured criteria, and additional media/PDF/font/runtime-probe defects received focused fixes.

The source suite passed with 626 tests passing and 17 skipped; separate browser/render runs executed the 13 omitted browser cases, leaving four Python skips. The saved private plugin was read back across all 1543 files, with one equivalent JSON serialization difference. A private fixture defect was repaired while retaining its connections. No fresh installed-client or paid-provider pass was claimed.

Evidence: [audit closure](reviews/audit-closure-2026-10-20.md), [source results](../verification/closure-2026-10-20/results.json), [publication](../verification/github-publication-1.111.1.json), [hosted readback](../verification/hosted-sync-1.111.1.json).

### 2. Recovered artifact exercises: 44 scoped cases

Rebuilt missing outputs from the surviving checkpoint and completed replacement R01–R43 plus supporting Storytelling R44: **41 PASS_SCOPED and 3 PASS_AFTER_REPAIR_SCOPED**. This was a non-blind, source-guided review, not 44 independent installed-plugin tests. The lost historical report was not reconstructed as if it had survived.

Actual artifacts included documents, sheets, storyboards, graphics, HyperFrames and Remotion renders, captions, audio measurements and limited EDL/OTIO roundtrips. Repairs affected exercise outputs: R35 needed a lossless derivative for exact retained frames, R40 needed portable asset paths, and R43 needed an audio-element ID. These did not establish new package defects. R43's full fidelity checker still reported `not_verified`, despite exact-copy review and a successful wrong-price negative test. Audio was measured rather than subjectively listened to.

The full 816-file archive was saved separately; repository evidence contains the archive record, hashes, measurements and findings, not the complete media archive. Historical absolute working paths may no longer exist. The 1505 candidate-package hashes and 137 retained checkpoint-artifact hashes were verified.

Evidence: [case-by-case report](../verification/scenario-closure-2026-10-20/REPORT.md), [final review](../verification/scenario-closure-2026-10-20/final-review.json), [archive record](../verification/scenario-closure-2026-10-20/archive-record.json). The separate AD01–AD14 source exercises also retain incomplete rubric coverage; they are not a 14/14 host pass.

### 3. Complete installation/update inventory: 1.112.0

Added the owner's complete **59-component** offline inventory to first-install, update and final-installation checks. Evidence distinguishes executable versions, real package payloads/imports, isolated Python environments and model hashes. The former capability-only diagnostic remains available explicitly. Missing-tool installation/repair plans must be disclosed, applicable authorization reused and working versions preserved. The inventory itself installs nothing.

All 59 components passed in the then-current Work environment and from the saved merged candidate. That is bounded installation evidence, not full inference/rendering or proof about another host. The later sandbox snapshots detected 19/59 after the MCP-removal work and 38/59 during 1.115.0. Runtime availability changes across sessions; preserved plugin instructions/configuration do not prove that binaries are still present. Do not invent a universal installation success or reinstall tools merely to make this handover look complete.

Evidence: [inventory notes](../verification/tool-inventory-2026-10-20/README.md), [saved inventory](../verification/tool-inventory-2026-10-20/saved-work-update.json), [1.112.0 publication](../verification/github-publication-1.112.0.json).

### 4. FrameCut research and executable v1: 1.113.0

Published the [research and implementation foundation](framecut/README.md) at `ea6b8b5`: 31 pinned GitHub candidates, component choices, timeline/revision contracts and 23 planned acceptance cases. The owner then authorized implementation. The research candidates did not become automatic dependencies.

FrameCut ships through the existing `opencut-video-studio` owner and welcome option 5. Its native Python-standard-library/FFmpeg runtime supports source analysis, exact frame clocks, immutable revisions, typed edits, locks/undo, captions, overlays/motion, independent audio, render/cache recovery and verified delivery. Caption, motion, audio and project-state specialists share the edit context. A bounded Kinocut comparison supported the native adapter choice; it did not establish superiority over every Kinocut feature.

Executed three media paths: speech/full edit plus highlight, a two-format product montage with animated alpha motion, and screen-recording/motion-only work. Source maps, decoded frames, PCM and cache behavior were measured. Tests exposed and fixed stale anchored audio, locks lost through undo and invalid lock state; formal tests also cover transition handles. Existing PyWhisperCpp and an installed multilingual tiny model produced draft timing; this was not a Polish forced-alignment benchmark.

The original release had 36 FrameCut tests. The build report preserves the T01–T23 PASS/PARTIAL distinctions, unsupported capabilities and client gaps. Do not convert the research acceptance plan into a blanket completed claim.

Evidence: [build status and acceptance matrix](framecut/build-status.md), [build evidence](../verification/framecut-build-2026-10-20/build-summary.json), [fixes](../verification/framecut-build-2026-10-20/fixes.json), [1.113.0 publication](../verification/github-publication-1.113.0.json).

### 5. Owner-requested hosted Sunra MCP removal

The owner reported mobile @ selection trouble and explicitly requested Sunra MCP removal. Public 1.113.0 contained no such configuration. Hosted-only **1.113.1** removed the two MCP configuration files and their binding while preserving the App identity, PoYo, the separate Sunra API route and unrelated runtime recipes. The repository received records/guidance only, without a public-package bump. The owner subsequently reported mobile invocation working; the cause of the original symptom was not proven.

Do not restore the retired MCP files during synchronization. Do not treat this specifically authorized private removal as permission to delete shared-package paths. Evidence: [removal and preservation record](../verification/sunra-mcp-removal-2026-10-21.json).

### 6. FrameCut onboarding and motion handoffs: 1.114.0

Added adaptive novice guidance, brief explanations tied to the material, a reusable working agreement and explicit editorial ownership. Speech and caption languages are separate; translation requires its own timing instead of fabricated source-word alignment. HyperFrames/Remotion choices are explained when useful, without requiring a novice to choose a technical engine first.

Returned motion is bound to its originating request, project/revision context and placement. Checks include actual dimensions, rational FPS, duration/frame count, alpha and stale placement. Unbound legacy returns may preview but require a checked binding for a new final. Delivery readiness is separate from technical PASS: full recorded picture/sound review can support READY; partial/missing review is REVIEW_REQUIRED; failed review is BLOCKED. Review bookkeeping tests do not prove that anybody watched or listened to a real film.

Seven new runtime regressions raised FrameCut coverage to **43 tests**. Five source-guided dialogue exercises were recorded, including two baseline replies that were already useful. There is no fabricated claim that both baseline cases failed. The representative-proof/required-preview direction from this release was superseded by the next owner correction.

Evidence: [audit and dialogue record](../verification/framecut-review-2026-10-21.json), [source verification](../verification/release-1.114.0.json), [saved readback](../verification/hosted-sync-1.114.0.json).

### 7. Complete storyboard before final render: 1.115.0

Implemented the owner's corrected sequence across FrameCut, orchestration, Pipeline Core, storyboard owners, motion handoffs, Project State and Edit Pack guidance. Seventeen shared files changed; none were added or removed. Core media schema and execution behavior stayed unchanged.

The current contract is:

1. Reuse known information and ask only consequential missing questions. A complete brief does not need another onboarding interview.
2. Produce and show **actual visual storyboard/contact-sheet pages covering the entire reel**. A table, placeholders, moodboard or four isolated sample frames is not a completed board. Panel count follows every scene and meaningful action, copy, composition or transition change, including multiple states within one shot. Split into readable pages when necessary.
3. Make panels reviewable with stable scene/panel IDs, time or interval, delivery aspect/composition, exact copy, action/motion, transitions and relevant sound cues. Image-generation tool choice does not waive identity/copy checks.
4. Collect user feedback, apply it and show the corrected complete board. Require acceptance of the current revision. Delegating creative choices does not equal approval of an unseen board.
5. Render the accepted design and perform technical plus full picture/sound review. A faithful technical repair does not require creative reapproval; creative changes reopen board review. Resume an unchanged accepted board without repeating intake or approval.

A video sample is optional on request or an accepted offer. An explicitly requested early sample is a bounded detour that returns to full-board review; sample acceptance is not whole-film acceptance. There is no compulsory preview stage.

The existing Project State/freeform brief carries `framecut_context`: stage, board revision, sequence/deliverable coverage, panel/page references, pending feedback, the actual acceptance message, optional sample status and next action. This is **host orchestration, not a new CLI-enforced creative-approval gate**. CLI authorization and technical verification cannot prove user acceptance. `--mode preview` renders the selected whole sequence; a short sample needs a scoped derived sequence/deliverable while retaining the master.

Five fresh-context source-guided dialogue exercises cover novice intake, a complete delegated brief, revision of an accepted board, an early sample and resuming an accepted board. No new storyboard images or final films were generated for this instruction change. Evidence: [workflow record](../verification/framecut-storyboard-2026-10-21.json).

## Code and ownership map

Paths below are relative to `plugins/framecore-work-creative-studio/` unless otherwise stated.

| Area | Entry point and responsibility |
| --- | --- |
| FrameCut behavior | `skills/opencut-video-studio/SKILL.md`; user workflow and edit ownership |
| Runtime contract | `skills/opencut-video-studio/assets/framecut/README.md` and `schema.json`; implemented behavior takes precedence over aspirational research fields |
| CLI / state | Same directory: `framecut.py`, `fc_core.py`; typed operations, source/timeline clocks, immutable revisions and locks |
| Media / captions / output | Same directory: `fc_media.py`, `fc_captions.py`, `fc_render.py`; ingest/probe/analyze, timed captions, render/cache/mix/verify |
| Startup / routing | `skills/workflow-orchestrator/SKILL.md`; complete localized welcome and stable option mappings |
| Project continuity | `skills/pipeline-core/`; Project State, handoffs and resume context |
| Visual board | `skills/storyboard-sequence-architect/` and `skills/storyboard-board-architect/`; existing `scripts/board_compose.py` under the latter creates PNG pages/PDF without first rendering a video |
| Motion specialists | `skills/hyperframes-workflow/` and `skills/remotion-video-production/`; return checked local-clock assets, FrameCut owns global composition |
| Regression suite | `tests/framecut_test.py` within the shared package; included in repository `scripts/check_all.sh` |

Keep source PTS separate from timeline frames; preserve rational FPS, half-open intervals, source hashes and immutable revisions. Never overwrite originals or accepted finals. Independent audio placement, cuts, variants and separate sequences have different meanings. Analysis heuristics do not establish semantic highlights or authorize automatic removal of pauses/takes.

Advanced tracking, multicam synchronization, speed ramps, reverse/freeze editing, HDR mastering, diarization and native NLE project editing remain outside v1. OTIO is a limited interchange path with explicit losses; native OpenCut/NLE UI import is not certified.

## Verification and release caveats Claude must preserve

- The 1.115.0 local required suite passed: **225 Node + 457 Python = 682 passed**, with 13 Node and 12 Python skips. All **43 FrameCut tests passed**. Counts describe that run, not all possible host behavior.
- Release workflow `39566291015` and source checks `39566290875` passed. All six downloaded release assets were digest-verified; 1516 plugin files and 2184 repository files match source. The local repository ZIP used a different outer checkout-directory prefix, so normalized file content was compared instead of claiming identical ZIP hashes.
- The initial release-description refresh `39566290927` failed on the heading. Repository-only correction `732ae4b` restored the exact `# Creative Studio 1.115.0` prefix; refresh `39567350696` then passed and the release body was read back. Keep failure and recovery distinct.
- [Publication](../verification/github-publication-1.115.0.json), [source verification](../verification/release-1.115.0.json) and [hosted synchronization](../verification/hosted-sync-1.115.0.json) are separate records. The 1565-path hosted package includes a private overlay; public source equality is not its comparison target.
- Continuous subjective playback/listening, real Polish/mixed-language alignment accuracy, all device layouts, paid generators, native editor import and fresh installed-client orchestration remain unverified within the recorded scope. Historical planned host cases stay NOT_RUN.
- Scratch media and runtime installations may disappear. Preserve reproducible source/evidence and check real inputs/runtime when a task resumes; never claim a missing old artifact was reviewed again.

## What to observe during the owner's testing

These are useful observations, not a new autonomous test/development order:

- Does a novice get a useful small choice and a relevant question, while a complete brief goes straight to the full board?
- Does the displayed board explain the entire reel, including changing copy, reveals and transitions, at readable size on the actual client?
- Do feedback, price/text locks, timing changes and accepted-board resumes survive without losing prior decisions or silently rendering an old revision?
- Is a sample optional, and does an early sample return to the full-board process?
- Do mixed footage/motion, caption language/timing, independent audio and final picture/sound review work on actual material?
- Do Motion Graphics and other owners still route ordinary jobs correctly, preserve editable engine projects and deliver viewable results in the owner's client?

For a reported problem, retain the actual host/client and exposed model/reasoning setting, observed package version, request and available input references, expected versus actual behavior, output/timecode or screenshot, reproduction steps and affected locks. Label owner reports PASS_REPORTED where appropriate; do not invent missing settings or confuse a source simulation with a real client run.

## Safe continuation after a concrete new request

Work directly on `main`, preserve concurrent changes, record the actual baseline and use a guarded fast-forward. Do not create extra branches or force-push. Existing `gh-pages` and the merged ccr branch remain untouched. The authenticated GitHub connector was used when direct Git write credentials were unavailable; the remote tree was read back and the identical local patch reconciled without force.

For shared-package changes: implement and verify the repository first, publish the release, then update the **existing** hosted plugin against its current release guard. Merge only the intended shared delta over the current private overlay, preserve private integrations and retired Sunra MCP state, and read back the actual affected files and inventory. Never copy private settings into the public repository or replace the overlay with the public ZIP. A separate owner-directed thread owns permanent private integrations. The hosted orchestrator is near its 32 KB file budget; check merged size when editing it.

Keep technical IDs, complete localized startup, existing option mappings, vendored provenance and permanent shared paths stable. Run the canonical validator and required repository suite for an authorized change. Record origin, change ID, baseline, actual verification and separate per-host states. Do not treat pending features or partial research acceptance rows as authorization to broaden the change.

This handover only updates repository documentation and the owner's pause instruction. **No package version bump, plugin update, integration installation or new product development is part of it.**
