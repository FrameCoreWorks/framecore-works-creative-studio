# Closure of the interrupted repository audit

Origin: ChatGPT Work. Change ID: `CW-20261020-CLOSURE`. Baseline: `9a028b78bea27d6aac146865dc6c12d29a7329cf` on `main`. The owner requested completion of the earlier audit and unfinished fixes before the next feature task.

## Recovered state

The visible history of the pinned repository-report conversation was inspected, including its expanded work records. The original audit document was recovered. Seven fixes and their regression tests survived as uncommitted files in the earlier workspace; no completed commit, publication or paired hosted update for those fixes was found. The old 43-scenario report was not recovered and is not counted as current evidence. The earlier HyperFrames test archive remains a historical artifact, not a substitute for this run.

The three later Cloud Code commits on `main`, including the Reel Editing Assistant work order, are retained. That feature task is not implemented by this closure. The separate tool-integration thread owns the private hosted additions. Its baseline was version 1.111.0, release `pluginrel_6ad75ceecdac8191a38c95033c107caf`, with 38 hosted-only files and additional changes to shared paths. Private configuration is not copied into this public repository.

## Delta

| Earlier finding | Resolution in this change |
|---|---|
| F1: exact text accepted currency, punctuation and case drift | Preserve symbols and case; normalize only Unicode NFC and whitespace boundaries. Regression cases cover prices, contacts, punctuation, percentages and line wrapping. |
| F2: public URL redirected to a private address | Check every redirect and every numeric address in the connection's DNS answer set; connect to that validated numeric target. Disable environment proxies for this guarded reader and keep HTTPS SNI/certificate verification. Tests use a synthetic transport with real network access forbidden. |
| F3: release records always attributed work to cloud-code | Select the origin once through `STUDIO_ORIGIN_AGENT` and use it consistently in records and commit trailers. Preserve named test-suite summaries and both Node reporters. |
| F4: conflicting startup menus and pace order | Shared policy and Codex installation entry defer to the current four-option welcome and combined work-area/pace selection. Welcome assets are unchanged. |
| F5: supplied-film sound had conflicting owners | Sound design/mixing with code goes to Motion Graphics; the no-code route remains an audio production plan. Standalone audio review stays with the audio owner. |
| F6: source/hosted drift | Prepare the shared release and a guarded patch over the current hosted baseline. Preserve the private overlay; report exact comparison scope in the synchronization record. |
| F7: claimed breadth exceeded retained behavioral evidence | Preserve historical NOT_RUN statuses. Replace unverifiable claims with fresh source, regression and sandbox media results. No blanket claim that all skills were tested end to end in ChatGPT. |
| F8: dirty host-eval candidates were unidentified | Future runs hash the exact package, retain its candidate archive when writing a record, detect changes during the run, and record suite/configuration limits. Historical missing data is not invented; full tool inputs/outputs and effective host reasoning settings remain explicitly unreported. |
| F9: supplied audio profiles still inherited launch-film advice | Validate custom profiles, compare only available metrics, retain the true-peak safety ceiling, and use profile-specific verdicts and recommendations. |
| Additional recovered defects | Bound tempo sampling indices; preserve raw mono amplitude and clipping detection; select the first audio stream consistently; validate PDF Trapped names; use fractional browser glyph metrics; probe cached HyperFrames without npm network access. |
| Smaller instruction defects | Deliver the actual renderer project for its engine; include Motion Graphics in the QA responsibility map; distinguish 5 ms onset alignment from the 10 ms peak tolerance. |

## Verification

Fresh baseline regressions reproduce the defects before applying their implementation fixes. The full source suite passes with 626 tests passing and 17 skipped, across 238 Node tests and 405 Python tests in 47 suites. The skips include opt-in browser checks, the optional GEPA dependency and the intentionally unavailable-OCR scenario on a host where OCR is installed. Detailed results are in [the closure evidence](../../verification/closure-2026-10-20/results.json), with retained source and before-change logs beside it.

Additional browser checks pass 15/15, and the opt-in SVG/WebGL/3D and logo raster checks pass 2/2. This executes all 13 browser/render cases omitted by the main run; four Python skips remain. Publication is recorded separately. The first browser session was interrupted without a final result and is not counted as a pass. Tests that synthesize WAV, MP4 and PDF files establish the measured properties covered by their assertions, not creative quality or client approval.

No paid generation, provider connection test or fresh ordinary-ChatGPT/mobile startup test is part of this run. The 204 planned host cases remain unexecuted in the canonical inventory. A small independent exercise of source instructions is not an installed-client evaluation.

## Handover boundary

Version 1.111.1 is intended to align the public source version with the existing hosted installation after the separate private integration releases. Full public-package equality with the private installation is not claimed: its preserved additions and same-path overlays are explicit. Keep tool credentials and private settings outside the public repository. Begin the next feature task from the existing work order, including its hosted-tool inventory/import step, after the publication and guarded synchronization records are complete.
