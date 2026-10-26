# Closure of the interrupted repository audit

Origin: ChatGPT Work. Change ID: `CW-20261020-CLOSURE`. Baseline: `9a028b78bea27d6aac146865dc6c12d29a7329cf` on `main`. The owner requested completion of the earlier audit and unfinished fixes before the next feature task.

## Recovered state

The visible history of the pinned repository-report conversation was inspected, including its expanded work records. The original audit document was recovered. Seven fixes and their regression tests survived as uncommitted files in the earlier workspace; no completed commit, publication or paired hosted update for those fixes was found. The old 43-scenario report was not recovered and is not counted as current evidence. The earlier HyperFrames test archive remains a historical artifact, not a substitute for this run.

The three later Claude Code commits on `main`, including the Reel Editing Assistant work order, are retained. That feature task is not implemented by this closure. The separate tool-integration thread owns the private hosted additions. Its baseline was version 1.111.0, release `pluginrel_6ad75ceecdac8191a38c95033c107caf`, with 38 hosted-only files and additional changes to shared paths. Private configuration is not copied into this public repository.

## Delta

| Earlier finding | Resolution in this change |
|---|---|
| F1: exact text accepted currency, punctuation and case drift | Preserve symbols and case; normalize only Unicode NFC and whitespace boundaries. Regression cases cover prices, contacts, punctuation, percentages and line wrapping. |
| F2: public URL redirected to a private address | Check every redirect and every numeric address in the connection's DNS answer set; connect to that validated numeric target. Disable environment proxies for this guarded reader and keep HTTPS SNI/certificate verification. Tests use a synthetic transport with real network access forbidden. |
| F3: release records always attributed work to cloud-code | Select the origin once through `STUDIO_ORIGIN_AGENT` and use it consistently in records and commit trailers. Preserve named test-suite summaries and both Node reporters. |
| F4: conflicting startup menus and pace order | Shared policy and Codex installation entry defer to the current four-option welcome and combined work-area/pace selection. Welcome assets are unchanged. |
| F5: supplied-film sound had conflicting owners | Sound design/mixing with code goes to Motion Graphics; the no-code route remains an audio production plan. Standalone audio review stays with the audio owner. |
| F6: source/hosted drift | Published 1.111.1 on main and saved a guarded patch over hosted 1.111.0. Full hosted archive readback confirms the expected patch and preserves the private overlay; the synchronization record names its exact comparison scope. |
| F7: claimed breadth exceeded retained behavioral evidence | Preserve historical NOT_RUN statuses. Replace unverifiable claims with fresh source, regression and sandbox media results. No blanket claim that all skills were tested end to end in ChatGPT. |
| F8: dirty host-eval candidates were unidentified | Future runs hash the exact package, retain its candidate archive when writing a record (archives dropped 2026-10-26 by owner decision; the hash stays), detect changes during the run, and record suite/configuration limits. Historical missing data is not invented; full tool inputs/outputs and effective host reasoning settings remain explicitly unreported. |
| F9: supplied audio profiles still inherited launch-film advice | Validate custom profiles, compare only available metrics, retain the true-peak safety ceiling, and use profile-specific verdicts and recommendations. |
| Additional recovered defects | Bound tempo sampling indices; preserve raw mono amplitude and clipping detection; select the first audio stream consistently; validate PDF Trapped names; use fractional browser glyph metrics; probe cached HyperFrames without npm network access. |
| Smaller instruction defects | Deliver the actual renderer project for its engine; include Motion Graphics in the QA responsibility map; distinguish 5 ms onset alignment from the 10 ms peak tolerance. |

## Verification

Fresh baseline regressions reproduce the defects before applying their implementation fixes. The full source suite passes with 626 tests passing and 17 skipped, across 238 Node tests and 405 Python tests in 47 suites. The skips include opt-in browser checks, three optional GEPA tests and one Claude CLI validation test because those dependencies were unavailable locally. Detailed results are in [the closure evidence](../../verification/closure-2026-10-20/results.json), with retained source and before-change logs beside it.

Additional browser checks pass 15/15, and the opt-in SVG/WebGL/3D and logo raster checks pass 2/2. This executes all 13 browser/render cases omitted by the main run; four Python skips remain. Publication is recorded separately. The first browser session was interrupted without a final result and is not counted as a pass. Tests that synthesize WAV, MP4 and PDF files establish the measured properties covered by their assertions, not creative quality or client approval.

No paid generation, provider connection test or fresh ordinary-ChatGPT/mobile startup test is part of this run. The 204 planned host cases remain unexecuted in the canonical inventory. A small independent exercise of source instructions is not an installed-client evaluation.

## Handover boundary

Version 1.111.1 aligns the public source version with the existing hosted installation after the separate private integration releases. Full public-package equality with the private installation is not claimed: its preserved additions and same-path overlays are explicit. Keep tool credentials and private settings outside the public repository. The publication and guarded synchronization records are complete. The next feature task starts from its existing work order, including a deliberate review of hosted-tool imports; it was not implemented as part of this closure.

## Publication and saved installation

- Source release: [v1.111.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.111.1), commit `addf23e73400c0e17c3321a7020e98395e8932fc`. The downloaded plugin ZIP and inventory match the local build; all 1505 package files match the tag tree. The player and canonical repository archive match GitHub-reported SHA-256 digests. Exact methods and the corrected release-description workflow are in [the publication record](../../verification/github-publication-1.111.1.json).
- Saved private plugin: release `pluginrel_6ad76a03ef2081919bf42aed344dc562`, version 1.111.1. All 1543 files read back: 1542 exact byte matches and one semantically identical JSON formatting normalization; zero unexpected changes. The 1517 files omitted from the patch remain byte-identical to the previous saved release. [Synchronization record](../../verification/hosted-sync-1.111.1.json).
- A pre-existing test-fixture defect in the private overlay omitted its MCP files. The fixture was repaired without altering connections; all seven affected hosted suites pass (88 tests).
- Remote branches remain `main`, `gh-pages` and the existing `ccr-b6d36a1c-4hszow` session branch. The latter's head `daab5828bdd4025280ebe2af5f5d5cccacae4a5c` is already an ancestor of the release commit. No branch was created or deleted.

The old conversation itself was not repaired or resumed. Its recoverable work is now committed and linked here; the missing historical scenario report is still missing. Fresh-client behavior, paid generation and the optional client reel mix remain outside the completed verification.

## Fourteen handover prompts

All AD01–AD14 prompts received retained source-based responses and a [separate review](../../verification/closure-2026-10-20/source-exercises-review.json). This was explicitly non-blind: the agent accidentally saw automated checks before answering. It is not a 14/14 host pass. Actual outputs include a linted static HTML mockup, color measurements, a copy-checker run and a standalone image prompt. Media/brand-dependent execution was blocked by absent inputs; no input was fabricated.

The review records incomplete rubric coverage in AD02, AD05, AD07 and AD12, an informational short-Polish-text language-label limitation, and an overbroad missing-browser claim corrected by the parent. The model license required by AD12 remains unverified at the author's source. These are bounded exercise findings, not grounds for claiming all installed behavior has passed. No production change was made merely to optimize the non-blind sample answers.
