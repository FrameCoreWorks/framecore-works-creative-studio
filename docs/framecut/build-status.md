# FrameCut implementation status

## 1.116.0 native development, 2026-10-21

The owner's Concat follow-up extends the current runtime with original implementations of all six recommended areas. The shared frame transform and exact source-time map drive video and actual composition stills; full structural storyboards accept authored semantic moments and produce contact sheets/PDF/coverage receipts. Atomic stable-ID split, trim, move, removal, freeze and parameter updates expose a dry-run impact report. Persisted jobs support status, cooperative cancellation and linked resumption from the same immutable project/source identity. Native transform/gain keys, format-specific crop/zoom/pan, piecewise-linear speed curves and nine versioned declarative picture/audio effects are wired into FrameCut, board, motion and Project State owners.

Native boards retain awaiting-user-review status. The agent must add meaningful action beats and inspect all pages; structural coverage alone does not establish a good creative storyboard. The existing onboarding, consequential questions, user corrections, current-board acceptance and optional sample policy remains authoritative. No desktop editor or Concat code is embedded.

Verification includes synthetic decoded-video, still, audio and lifecycle tests plus a fresh-context source-guided task that splits one clip, preserves all 45 source/animation positions, applies zoom only to the vertical variant, produces nine panels per variant including the requested action moment, and stops for feedback without rendering video. This is sandbox evidence, not a fresh installed ChatGPT/mobile/Codex/Claude client test. Limits: variable-speed audio changes pitch; automatic dead-worker detection requires Linux process identity; cancelled work resumes as a linked job using valid stage caches, not inside an unfinished encoder; native transforms use bounded CPU/Pillow frames. User creative acceptance and real client tests remain separate. Versioned release and hosted-sync records carry actual gate/publication outcomes.

## Historical 1.113.0 foundation

## 1.114.0 orchestration and onboarding follow-up, 2026-10-21

The owner requested another audit focused on uncertain users, light teaching and polished delivery. FrameCut now derives a small choice from the user's material, explains the relevant effect and engine in ordinary language, accepts delegated choices and carries a working agreement across specialists. A representative style proof precedes full finishing when the direction is uncertain; locked styles and small corrections skip it. The full Studio welcome and all 37 skill IDs remain unchanged.

The audit resolved contradictory cutdown routing, added originating-request and actual-media validation for returned motion, separated translation from source-word correction, and exposed delivery readiness separately from technical success. Existing motion bindings without an originating request can still preview but require a checked binding for a new final. Full recorded review, sampled review and failed review have distinct states, with previous review evidence retained.

Evidence: [audit and five dialogue exercises](../../verification/framecut-review-2026-10-21.json). Two baseline replies were already useful; the changes make the guidance explicit rather than claiming both cases failed. Three fresh post-change exercises covered uncertain direction, engine/translation explanation and delegated choices. These are source-guided sandbox conversations, not fresh hosted-client tests. The 43 FrameCut tests include seven new regressions and actual synthetic media/CLI execution. Readiness fixtures test bookkeeping, not subjective watching/listening. No claim of newly installed HyperFrames/Remotion runtimes or real-client film quality is made.


Owner-authorized build on 2026-10-20, following publication of the research at `ea6b8b593dc42a9b255e5177ec3d35796f9dea24`. The executable v1 lives in [the existing editing owner](../../plugins/framecore-work-creative-studio/skills/opencut-video-studio/SKILL.md); its [runtime README](../../plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/README.md) is the implemented contract. The original research contract is architectural guidance where its richer fields exceed v1.

## Delivered behavior

FrameCut is option 5 of the full welcome and the display name of opencut-video-studio, without a new exposed skill. An adaptive interview fills consequential gaps, then source evidence informs editorial decisions. Highlights are one supported job, alongside full edits, visual montages, screen recordings, generated/mixed productions and motion-only compositions. The host makes editorial choices; the CLI does not pretend that silence or a transcript heuristic proves semantic quality.

The runtime ingests immutable hashed media, probes original time bases and timestamps, analyzes scenes/silence/decoded PTS, imports or transcribes speech, validates typed operations, compiles a master timeline and renders preview/final bundles. It supports cuts/gaps/crossfades, constant speed, crop/fit, source-linked and independent audio, fades/ducking/loudness targets, still/video/alpha overlays, titles, sentence/kinetic captions, exact revision snapshots, locks, undo and hash-bound delivery checks. Original files remain unchanged. Caption Studio supplies sidecar QA, Motion Graphics Workflow supplies local-clock motion assets, Audio Production Director supplies sound treatment, and Pipeline Core retains project state. Revision dependency keys preserve unaffected media work.

Native JSON, source relink maps and CSV retain editable decisions. Picture EDL and optional official OpenTimelineIO cover a deliberately limited interchange subset, with explicit losses. Native desktop-editor import is not certified. The legacy edit_export API remains unchanged.

## Component choice

The bounded [adapter comparison](../../verification/framecut-build-2026-10-20/adapter-decision.json) ran pinned Kinocut trim and typed-timeline compilation on a shared synthetic source. It did not benchmark every Kinocut feature. A native standard-library/FFmpeg adapter was selected because FrameCut still needs its own source clock, immutable revisions, ownership and delivery contract, while the narrow executor requires no permanent added runtime. Existing PyWhisperCpp and a verified multilingual tiny model were reused. Actual speech produced draft segments and 22 token-timed words; token times are approximate ASR evidence, not forced alignment. Faster-whisper/WhisperX comparative accuracy work was not required to establish this route and remains NOT_RUN. No new permanent MCP or research-candidate dependency was installed.

## Evidence and fixes

- [36 formal tests](../../verification/framecut-build-2026-10-20/framecut-tests.txt): strict contracts, timing, revisions, media, failures and delivery. Included in the mandatory full repository suite.
- [22 agent contract/recovery checks](../../verification/framecut-build-2026-10-20/agent-contract-after.json), after [observed failures](../../verification/framecut-build-2026-10-20/agent-contract-before.json). Fixed stale anchored-audio cache after a visual move, undo dropping locks and invalid null locks. Added a formal transition-handle regression. [Fix record](../../verification/framecut-build-2026-10-20/fixes.json).
- [Product workflow](../../verification/framecut-build-2026-10-20/agent-product.md): actual two-format montage with stills, video, music and animated alpha overlay. Typography-only revision retained identical source maps and decoded PCM, with 6 cache hits and no rebuilt source stages per format.
- [Speech workflow](../../verification/framecut-build-2026-10-20/speech.json): actual public speech audio, synthetic portrait picture, full edit and vertical kinetic-caption highlight. A clipped-word attempt was blocked and the selection corrected. This does not test an actual talking-head picture or Polish recognition quality.
- [Screen workflow](../../verification/framecut-build-2026-10-20/screen.json): actual encoded synthetic UI capture, removal of waiting while keeping all three steps, anchored explanation and typography revision; 5 cache hits, no rebuilt source stages.
- [Seven fresh-agent routing simulations](../../verification/framecut-build-2026-10-20/agent-routing.json): full Polish/German startup, option 5, direct job, caption revision, numeric context and non-executing fallback. They exposed stale four-option/ownership references, now corrected. These are agent sandbox conversations, not installed-client startup tests.
- [Media measurements](../../verification/framecut-build-2026-10-20/media.json): exact dimensions, frame counts, hashes, technical decoding and loudness. Picture review sampled frames; continuous playback and subjective listening were NOT_RUN. Synthetic tones measure timing, not intelligibility.

A scratch synchronization anomaly replayed temporary files outside the isolated fixture directory. It was separated from module failures and the affected jobs rerun with stable source hashes. No private footage, downloaded speech media or private hosted settings are included in public evidence.

## Original acceptance matrix: actual scope

PASS below means the stated bounded test passed. PARTIAL deliberately does not assert the entire original target.

| Case | Status | Measured scope and remaining coverage |
| --- | --- | --- |
| T01 | PASS | Rational frame/sample arithmetic, 30 and 30000/1001 actual renders, mixed source normalization |
| T02 | PARTIAL | Actual VFR and nonzero-start-PTS renders; phone rotation fixture not run |
| T03 | PASS | Cuts/gaps, explicit overlaps and independently anchored audio, actual PCM placement and duration |
| T04 | PARTIAL | Cut-word/segment blockers and complete-clause repair; blinded semantic highlight review not run |
| T05 | PARTIAL | Unicode/text-path and word-timing contracts; no measured Polish/mixed-language boundary benchmark |
| T06 | PARTIAL | No-audio/music/motion-only paths avoid fabricated transcript; overlapping-speaker accuracy not tested |
| T07 | PASS | Actual product montage and screen workflow, picture samples inspected |
| T08 | PARTIAL | Layout collision blocks final; layouts corrected and sampled; not all device-size/face cases tested |
| T09 | PARTIAL | Alpha motion integration, local time/duration contract and product frames; exhaustive color/halo validation not run |
| T10 | PASS | Product 9:16 and 16:9 variants plus separate speech full/highlight sequences |
| T11 | PASS | Typography revision preserves source maps/PCM; audio/anchor revisions invalidate affected cache; locks survive undo |
| T12 | PASS | SIGINT child cleanup, retry, corrupt cache, source change, stale revision and immutable history |
| T13 | PARTIAL | Missing-tool/timeout/fallback tests; not every browser/model/network combination exercised |
| T14 | PASS | Unicode/spaces, traversal, symlink and overwrite guards |
| T15 | PARTIAL | Bounded subprocess output/time, input limits and cache budget; no OS-level hard memory quota or actual full-disk crash test |
| T16 | PASS | HDR is rejected explicitly; HDR mastering remains unsupported |
| T17 | PARTIAL | Actual mixing/resampling/ducking and measured loudness; no subjective intelligibility review or denoising-delay benchmark |
| T18 | PARTIAL | EDL loss report and official OTIO 0.18.1 write/read; named NLE import NOT_RUN |
| T19 | PARTIAL | Protected welcome source validation and seven agent conversations; fresh installed clients NOT_RUN |
| T20 | PASS/host-scoped | Existing 59-component inventory and its tests retained; saved-package Work update result recorded in the release readback; no other-host installation claim |
| T21 | PASS | Full decode/frame/duration checks plus changed/corrupt/stale output rejection |
| T22 | PARTIAL | Closed typed operations, no shell filter execution, safe text and content-only instruction policy; adversarial live-host footage test NOT_RUN |
| T23 | PASS | Actual no-footage motion-only render with the same revision and delivery contract |

Advanced tracking, multicam synchronization, speed ramps, reverse/freeze operations, HDR mastering, speaker diarization and NLE-native project editing are outside v1. No claim is made that every researched capability or every original aspirational acceptance row is complete. Final creative acceptance requires the requested picture/sound review on the user's material.

## Publication and host status

Use [release status](../../RELEASE_STATUS.md), the versioned source/scope records and the hosted-sync record for exact source commit, package guard and saved-file evidence. Public source and the private hosted overlay are compared with their own scopes. Fresh ordinary ChatGPT, Work, Codex and Claude client behavior is NOT_RUN for this version; saved archive equality and sandbox agents do not establish those results.

Final release-source CI passed: 236 Node tests passed / 2 optional cases skipped; 454 Python tests passed / 8 optional cases skipped, zero failures. All 36 FrameCut tests ran. Strict Claude plugin/marketplace manifest validation passed separately from client behavior. The [final CI and branch record](../../verification/framecut-build-2026-10-20/ci-final.json) includes the corrected release-notes refresh and the preserved existing ccr branch, already merged into main.


## Owner storyboard correction, 1.115.0

The owner clarified that FrameCut must show a sufficiently detailed visual storyboard of the entire reel before final rendering. The previous 1.114.0 entry proposed a representative style proof and required a preview, without requiring acceptance of a full visual board. The owning entry and its routing, storyboard and motion handoffs now follow intake, complete visual sheets, feedback, corrections, current-board acceptance, then final rendering/review. Panel count follows scene and meaningful-state coverage; multiple pages preserve legibility. A video sample is optional on request, including an explicitly requested early exploratory sample that returns to board review.

The existing Project State, runtime brief and Edit Pack retain board revisions, coverage, feedback, acceptance evidence and optional sample status. Creative changes reopen board review; resuming an unchanged accepted board does not. This is host orchestration, not a new CLI-enforced storyboard gate: runtime authorization and technical verification cannot prove user acceptance. Core media behavior/schema are unchanged. The runtime guide no longer implies a compulsory preview and explains that a short sample needs its own scoped sequence/deliverable.

Five fresh-context sandbox dialogue cases exercise novice intake, a complete brief with delegated choices, changes to an accepted board, an early requested sample and resuming an unchanged accepted board. These are source-guided exercises, not installed-client or visual-media tests. See [the workflow record](../../verification/framecut-storyboard-2026-10-21.json) and versioned release records for executed checks. No new paid generation or media-quality certification is claimed.
