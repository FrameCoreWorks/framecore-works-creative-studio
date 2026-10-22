# FrameCut implementation and acceptance plan

Original plan: 2026-10-20. Implementation now ships in 1.113.0; [build status](build-status.md) records actual completion, supported scope and unexecuted acceptance coverage. The matrix below remains the original target, not a blanket passing result. The owner has selected the product scope/name; technical choices follow [the foundation](README.md). This is an implementation packet for either coding host, without requiring another architecture interview.

## Correct the older work order before coding

The historical [Reel Editing Assistant task](../task-reel-editing-assistant-2026-10-20.md) was written against Studio 1.98.0. Current source is 1.112.0 at the research baseline. Its rough-cut idea is useful but does not cover the owner's wider FrameCut scope. Its “keep last take” rule must become a proposal grounded in meaning and user locks. Its whole-hosted-import and not_tracked instructions are superseded by current AGENTS.md: preserve private supplemental integrations, do not publish their source wholesale, and use guarded paired updates for actual shared-package changes. Do not rewrite the historical note as though it contained current instructions.

## Repository integration map

Paths are relative to plugins/framecore-work-creative-studio unless explicitly marked repository-only. Proposed new files must be settled before release because shared-package paths cannot later be deleted or moved.

| Surface | Required implementation | Gate |
| --- | --- | --- |
| skills/opencut-video-studio/SKILL.md and agents/openai.yaml | Existing technical ID owns FrameCut; update display text and the model-readable workflow; retain OpenCut/editor handoff | No second competing edit skill; title/description validation and discovery budget |
| skills/opencut-video-studio/assets/framecut/ (proposed) | Small contract/compiler/executor adapter package with CLI, schema and compatibility tests | Public package runs without private overlay |
| skills/opencut-video-studio/scripts/edit_export.py | Preserve old API; bridge supported new timeline data without claiming full fidelity | Existing tests remain green; explicit loss report |
| skills/caption-studio and skills/hyperframes-workflow | Source-time caption adapter and local-motion projection contract | No duplicate global time source; overlay/audio/caption synchronization |
| skills/workflow-orchestrator/SKILL.md | FrameCut entry and route in the text hosts actually load | Stay within validated byte budget; use references for details |
| skills/workflow-orchestrator/assets/startup-welcome.en.md and startup-welcome.pl.md | Add FrameCut to the complete localized welcome | Existing options 1–4 keep their meanings; recommended new token 5 |
| skills/workflow-orchestrator/references/startup-and-creative-menus.md and routing-boundaries.md | Numeric/name/direct-task/resume routing and complete language policy | Bare start, “5”, “FrameCut”, direct edit and resume cases |
| skills/pipeline-core and ownership/routing references | One editing owner with delegated caption/motion/audio review | No circular routing or mandatory redundant intake |
| skills/workflow-orchestrator/assets/capability-card.json and motion runtime map | Actual supported execution paths and honest when_missing behavior | No shell/FFmpeg/browser/model gives the documented fallback |
| skills/workflow-orchestrator/assets/environment-check | Accepted new dependency recipes and probes only | First install and update inventory, announced plan, post-install verification |
| tests, canonical validator, repository scripts/check_all.sh | Contract, media and routing regressions; host cases initially NOT_RUN | No passing result inferred from fixture existence |
| Repository manifests/install sources/release ledger | Standard release only when shared package changes | Source commit, package version, hosted guard/readback and separate client evidence |

The present welcome has four options, not just Creative and Learning. Do not renumber the skill search or recommended-repositories options. Update both canonical welcome assets and their complete embedded excerpts together. Preserve all six capability bullets and existing qualifications. Test automatic language choice and verify ordinary ChatGPT separately from Work. Adding a reference without editing the owning skill is insufficient.

At this baseline the canonical validator reports 7,699 description characters against a 7,800 limit, and workflow-orchestrator/SKILL.md measures 31,882 bytes against a 32,000-byte limit. Budget the new welcome text and routing before editing. Keep the complete protected welcome; move or condense non-startup detail into existing appropriate references where allowed, preserving critical routing instructions. A new exposed skill would also consume scarce discovery budget.

## Bounded build sequence

| Phase | Deliverable | Exit criterion |
| --- | --- | --- |
| 0. Adapter decision | Kinocut/native comparison, dependency/rights/host notes, selected ASR route | Same fixtures and contract for both; record why selected route wins; no parallel production engines without need |
| 1. Project and time core | Versioned schema, semantic validation, immutable revisions, source map, migration from simple edit JSON | Exact timing fixtures pass, invalid/stale references rejected, source files preserved |
| 2. Three complete vertical workflows | Speech highlights; visual/product montage; screen recording with explanation/motion | Each goes from ingest to playable preview and one revision using the same project model |
| 3. Finishing and delivery | Kinetic captions, reframing, audio treatment, motion composition, final exports and receipt | Actual picture/sound QA, safe text layout, correct revision and editable handoff |
| 4. Studio product integration | Welcome option 5, FrameCut name, direct-task/resume routes and capability fallback | Full welcome source checks plus actual target-client tests; no duplicate owners |
| 5. Release | Versioned public package and guarded update of existing hosted plugin | Canonical/full gates, fast-forward main, preserved private overlay, saved-file readback; client states reported separately |

Build a narrow end-to-end implementation first, while using all three material types early to avoid a talking-head-only architecture. Advanced diarization, automatic tracking, desktop NLE integration, a visual editing UI and additional render engines follow only after their concrete tests justify them. Do not put all 31 researched repositories into the installer.

### Phase 0 comparison protocol

Use local synthetic/owner-authorized fixtures, identical inputs and outputs for a narrow FFmpeg adapter and a pinned Kinocut CLI/Python adapter. Measure implementation glue required, supported operations, source/timeline accuracy, first-run downloads, CPU/RAM/disk, render duration, cancellation, resume, errors and dependency conflicts. Do not install a permanent host MCP server for this comparison.

For ASR, compare the existing PyWhisperCpp route with faster-whisper on the same transcribed clips; add WhisperX only for the alignment comparison. Record language, model/revision, compute type, hardware, warm/cold state and decoding settings. Evaluate transcription errors and word-boundary errors separately. Benchmark user-visible elapsed time and peak memory; upstream claims do not fill these cells. If a candidate does not improve a meaningful criterion, retain the existing route.

## Three worked user journeys

| Material and goal | Analysis and editorial choices | Execution and acceptance |
| --- | --- | --- |
| Two-minute talking head; standalone short highlights | Transcript with word evidence, topics/context, useful candidate spans; agree number/length only if unspecified; preserve complete meaning | Separate sequences, caption timing from source map, optional kinetic emphasis and explanatory inserts; review every join and caption. Do not force every video into this pattern. |
| Multiple product shots, stills and generated additions; finished promo | Shot/contact sheets, product facts and protected identity, visual continuity, music/voice needs; select evidence that supports the brief | Multi-track edit plus motion blocks, product-safe framing, audio mix; generated additions through existing authorized routes, source/rights provenance retained |
| Screen recording plus narration; concise instructional video | OCR and speech evidence, UI steps, cursor/action intervals, personal-data regions, readability at intended size | Remove actual dead time while preserving steps; anchored callouts/zooms, corrected captions and intelligible audio; inspect the final screen content and mask any agreed private data |

A motion-only job uses the same brief, sequence/delivery and revision system with existing motion owners. A long-form edit need not create any short clips. Multi-camera sync, HDR mastering and automatic object tracking are declared unsupported (speed curves and freeze frames shipped in 1.116.0) until the corresponding adapters and tests exist, rather than implied by the broad product name.

## Acceptance matrix

At the research stage all rows were NOT_RUN; current row-by-row evidence is in [build status](build-status.md). The thresholds below are proposed engineering criteria, not measurements. Fixture lengths and tolerances should be locked before implementation is judged.

| ID | Case | Required result |
| --- | --- | --- |
| T01 | 30/1, 30000/1001 and mixed-rate sources | Integer master-frame decisions, rational conversion; no cumulative drift from rounded FPS |
| T02 | Phone VFR, rotation metadata and nonzero start PTS | Correct image orientation and source relinking; decoded timestamp map preserved |
| T03 | Cuts/gaps, explicit transition overlap, J/L audio cuts | Expected sequence length; picture/audio anchors agree within one output frame; audio-envelope arithmetic within one sample before encoding |
| T04 | Speech crossing a cut, negation, numbers and qualifiers | No silently changed meaning or clipped word; flagged cases reviewable |
| T05 | Polish diacritics, names, numbers, mixed language | Correct text/glyph rendering; measured timing errors against manually marked reference, unknowns visible |
| T06 | Silence, music-only, no audio, overlapping speakers | No invented transcript; sensible fallback; speaker uncertainty retained |
| T07 | Multi-clip visual montage and screen recording | Result driven by image/steps as well as text, with usable final media |
| T08 | Caption, face/product and UI safe-zone collision | Layout resolved or flagged; check at intended playback size, not only full-resolution screenshots |
| T09 | Motion layer alpha/color/frame alignment | No opaque box, halo, off-by-one frame or independent clock drift |
| T10 | Same edit in 9:16/16:9; distinct highlight selections | Aspect variants share correct decisions; separate sequences retain distinct meaning |
| T11 | “Larger captions”; “keep this pause”; “change music” | Only affected dependencies invalidated; accepted wording/other scenes retained |
| T12 | Cancel, resume, changed source and stale revision | No corrupted final; stale cache/conflicting revision rejected; accepted version recoverable |
| T13 | Missing FFmpeg/browser/model/encoder; unavailable network | Concrete capability error or scoped install plan; plan-only fallback honestly labeled |
| T14 | File paths with Unicode/spaces, traversal, alias/symlink output | Valid names work; input overwrite and unauthorized root access rejected |
| T15 | Oversized media, disk full, child timeout and memory cap | Bounded failure, cleanup of owned temporary files, preserved sources/checkpoints |
| T16 | HDR input and ordinary SDR target | Explicit tested color transform or unsupported status; no silent washout |
| T17 | Denoising, resampling, ducking, loudness normalization | Delay compensated; final speech/intelligibility/stereo checked; target comes from delivery brief |
| T18 | OTIO/EDL export and import in a named editor version | Supported cuts relink and match time; unsupported motion/effects listed as losses |
| T19 | Full welcome EN/PL/another language, tokens 1–5, direct task/resume | Complete localized welcome and stable old mappings; FrameCut routes once |
| T20 | Fresh/update tool inventory with installed/missing/broken states | Existing working tools retained, planned installations shown, actual result verified |
| T21 | Final render succeeds but media is wrong/empty/stale | Delivery rejected despite process exit 0 |
| T22 | Footage contains instructions aimed at the agent | Treat as content; no tool-policy change, command execution or unauthorized transfer |
| T23 | Project uses no supplied footage, only motion/generated assets | Same revision/delivery contract works without fake transcript stages |

For highlight quality, score complete thought, contextual fidelity, relevance to brief, distinctness, visual support and pacing using blinded paired review where practical. Hard fail for changing meaning, inventing quotes, losing required product facts or omitting requested deliverables. Do not report a heuristic “viral score” as measured audience performance. For precise kinetic captions, propose a 100 ms median boundary-error target on a manually marked speech set and report p95/outliers; the owner can choose a different precision requirement. It is not an achieved result.

Use synthetic or explicitly licensed fixtures. Synthetic tones can test synchronization but cannot prove recognition or editorial quality. Speech fixtures need actual speech and a checked reference transcript. Keep private footage out of public tests. Media review evidence records who/what inspected which interval and whether audio was actually heard.

## Definition of done for the module

The three vertical workflows and revision paths pass; the selected host has real render evidence; installation/update checks and failures are honest; project files can resume; final picture and sound have been reviewed; the full welcome works; the public package has no private-overlay dependency; and source publication, saved-hosted package and active-client behavior each have their own recorded status. A green source suite, installed dependency list or rendered synthetic color chart alone does not satisfy this definition.

## Handoff instruction for the implementation agent

Read current AGENTS.md, this folder, the old work order as history and the latest source/hosted baseline. Check for concurrent changes before editing. Start at Phase 0; choose engineering details through evidence rather than asking the owner to select libraries. Work on main under current repository policy, preserve unrelated changes and never force-push. Keep the technical skill ID stable, avoid new exposed skills, and protect full startup. Before an actual shared-package release, follow the standard version/install-manifest/package/check procedure and guard the existing hosted update. Record every unexecuted media or client test as NOT_RUN. Do not execute the historical instruction to publish the private overlay.
