# Verification evidence

This document records bounded package verification. It is not a certification of every host or generated output.

## Current source: 1.25.0

The [1.25.0 source checks](verification/release-1.25.0.json) pass canonical validation and 218 tests: 159 Node in the CI set (plus 3 opt-in browser tests, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The release adds a sound policy for motion deliveries and a documented mux command, which kept a 120 BPM click track sample-exact and the video stream byte-identical on the test D MP4; `adelay` placed a delayed start exactly, while `-itsoffset` only shifted the stream start. Whether ChatGPT follows the policy is not verified. [Scope](verification/scope-1.25.0.json) records 10 changed shared files out of 878.

## Previous source: 1.24.0

The [1.24.0 source checks](verification/release-1.24.0.json) pass canonical validation and 218 tests: 159 Node in the CI set (plus 3 opt-in browser tests, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The release changes delivery instructions only: MP4 first with a frame check, preview pages without export. It follows the inspection of the 2026-10-07 test C files, where ChatGPT's MP4 was clean and its HTML preview differed from it and exported through MediaRecorder ([report](verification/host-report-2026-10-07-test-c.json)). Whether ChatGPT follows the new steps is not verified. [Scope](verification/scope-1.24.0.json) records 10 changed shared files out of 878.

## Previous source: 1.23.0

The [1.23.0 source checks](verification/release-1.23.0.json) pass canonical validation and 218 tests: 159 Node in the CI set (plus 3 opt-in browser tests, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. A one-click player link built from the 2026-10-07 test A contract opened and exported on the live GitHub Pages player in Chromium, and the owner reported that it opened the animation on their device (PASS_REPORTED; [report](verification/host-report-2026-10-07-test-a.json)). The same report records that ChatGPT's own substitute MP4 differed from its contract. Whether ChatGPT now ends with the link is not verified. [Scope](verification/scope-1.23.0.json) records 13 changed and 1 added shared files out of 878.

## Previous source: 1.22.0

The [1.22.0 source checks](verification/release-1.22.0.json) pass canonical validation and 217 tests: 158 Node in the CI set (plus 3 opt-in browser tests, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. In Chromium 1194 the new motion player opened the `two-statements` example and the contract from the second 2026-10-07 ChatGPT test, rejected invalid input with messages and exported the opened contract; `check-preview.mjs` now names real-time recording as an error; the release's player file is byte-identical to the template. The Pages workflow steps were simulated against a local repository; GitHub Pages itself is not enabled or verified. Concurrent runs exposed and then confirmed fixes for two export CLI races. Existing contracts render pixel-identically to 1.21.0. [Scope](verification/scope-1.22.0.json) records 13 changed shared files out of 877.

## Previous source: 1.21.0

The [1.21.0 source checks](verification/release-1.21.0.json) pass canonical validation and 216 tests: 157 Node in the CI set (plus 2 opt-in browser tests, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The new `check-preview.mjs` rejects the preview delivered in the 2026-10-07 ordinary ChatGPT test (scene engine and video export missing, contract errors, scenes without kinds) and passes the template-built `two-statements` example. The new sweep exit renders pixel-identically in the preview and the Remotion starter; existing contracts are unchanged. Whether ChatGPT now delivers the template unchanged is not verified. [Scope](verification/scope-1.21.0.json) records 16 changed and 2 added shared files out of 877.

## Previous source: 1.20.0

The [1.20.0 source checks](verification/release-1.20.0.json) pass canonical validation and 214 tests: 155 Node in the CI set (plus 2 opt-in browser tests, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. In Chromium 1194 the new browser export drew frames pixel-identical to the Remotion still and exported the captioned starter in 16:9 and 9:16 as VP9 WebM files (300 frames, 10.00 s, about 42 dB PSNR against reference screenshots); the preview's button produced a download. This Chromium build offers no H.264 encoder, so the MP4 writer was verified with a libx264 stream instead (High profile, 300 frames, all decoded in order). Review and preview frames are pixel-identical to 1.19.0. On 2026-10-07 the owner reported a successful export in ordinary ChatGPT on an Android phone browser: an MP4 with H.264 (`avc1.640028`), 1920 x 1080, 180 frames, that plays (PASS_REPORTED; [report](verification/host-report-2026-10-07-browser-export.json)); the delivered preview used custom controls instead of the unchanged template. Desktop browsers, Firefox, Safari, Work and Codex are not verified. [Scope](verification/scope-1.20.0.json) records 12 changed and 3 added shared files out of 875.

## Previous source: 1.19.0

The [1.19.0 source checks](verification/release-1.19.0.json) pass canonical validation and 211 tests: 152 Node in the CI set (plus 1 opt-in browser test, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The new sync tool imported the example voice-over SRT into the starter contract at 120 BPM; the frame review of the captioned contract found no issues in three formats (114 frames). Contracts without captions or music render pixel-identically to 1.18.0. A Remotion render with a synthetic 120 BPM click track kept sample-exact beat spacing in the AAC track, with a constant 42.7 ms encoder start delay. Preview audio playback, full per-format renders and host behavior were not run. [Scope](verification/scope-1.19.0.json) records 25 changed and 3 added shared files out of 872.

## Previous source: 1.18.0

The [1.18.0 source checks](verification/release-1.18.0.json) pass canonical validation and 209 tests: 150 Node in the CI set (plus 1 opt-in browser test, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The starter contract now declares 9:16 and 1:1 formats; the frame review found no issues in any of the three (93 frames). Base-format preview frames are pixel-identical to 1.17.0, and at frame 176 the preview and the Remotion still are pixel-identical in each format. Review screenshots, drawn about 8% small in 1.17.0, are now drawn at true size. Full per-format video renders and playback review were not run. [Scope](verification/scope-1.18.0.json) records 25 changed shared files out of 869. Host behavior is not run.

## Previous source: 1.17.0

The [1.17.0 source checks](verification/release-1.17.0.json) pass canonical validation and 208 tests: 149 Node in the CI set (plus 1 opt-in browser test, run separately and passing), 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The new automated frame review ran in headless Chromium: no findings on the starter contract (31 frames) and the all-kinds example (53 frames), and clipping and out-of-frame errors with exit code 1 on a deliberately broken contract. Normal preview output is pixel-identical to 1.16.0. [Scope](verification/scope-1.17.0.json) records 11 changed and 2 added shared files out of 869. Host behavior is not run.

## Previous source: 1.16.0

The [1.16.0 source checks](verification/release-1.16.0.json) pass canonical validation and 207 tests: 148 Node in the CI set, 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. A declarative scene engine with six kinds now drives both the single-file preview and the Remotion starter. The preview renders the starter contract pixel-identically to 1.15.0; Remotion frames match the earlier render except for a 6-frame connector timing difference that the shared engine removes. The all-kinds example rendered in both, including a 775-frame H.264 file. Full playback review was not run. [Scope](verification/scope-1.16.0.json) records 21 changed and 4 added shared files out of 867. Host behavior is not run.

## Previous source: 1.15.0

The [1.15.0 source checks](verification/release-1.15.0.json) pass canonical validation and 204 tests: 145 Node in the CI set, 12 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The motion prompt library gains a 19-type brief index whose records the canonical gate checks against existing FrameCore originals, and 60 original blueprints receive record-specific objectives; imported records are unchanged. Brief matching was checked with Polish queries including inflected forms. [Scope](verification/scope-1.15.0.json) records 17 changed and 1 added shared files out of 863. All blueprints remain not_run; host behavior is not run.

## Previous source: 1.14.0

The [1.14.0 source checks](verification/release-1.14.0.json) pass canonical validation and 198 tests: 142 Node in the CI set, 9 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The shared `motion-score.json` now carries the storyboard and approval state; the packaged contract passes the strict storyboard check and renders as a Markdown storyboard. Packaged starters were reinstalled and rerun, and frame 140 from the GSAP starter and the single-file preview is pixel-identical to the previous release. [Scope](verification/scope-1.14.0.json) records 20 changed and 1 added shared files out of 862. Host behavior is not run.

## Previous source: 1.13.0

The [1.13.0 source checks](verification/release-1.13.0.json) pass canonical validation and 196 tests: 140 Node in the CI set, 9 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The new single-file preview was opened from disk in headless Chromium without a server or network; six frames were inspected and direct, forward and backward seeks produced pixel-identical frames. Interactive Play was not exercised automatically. An owner-run ordinary ChatGPT diagnostic reported Canvas unavailable in that conversation, so the mode does not depend on it. [Scope](verification/scope-1.13.0.json) records 10 changed and 2 added shared files out of 861. Host behavior is not run.

## Previous source: 1.12.0

The [1.12.0 source checks](verification/release-1.12.0.json) pass canonical validation and 195 tests: 139 Node in the CI set, 9 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The new Remotion kinetic type starter was installed from its lockfile in a development container, typechecked, passed its contract check and rendered a 300-frame 1920 × 1080 H.264 file; the GSAP starter's direct, forward and backward seeks produced pixel-identical frames in headless Chromium. Full playback review and GSAP video encoding were not run. [Scope](verification/scope-1.12.0.json) records 12 changed and 19 added shared files out of 859. Host behavior is not run.

## Previous source: 1.11.2

The [1.11.2 source checks](verification/release-1.11.2.json) pass canonical validation and 192 tests: 136 Node in the CI set, 9 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The legacy audio alias is explicit-only and seven overlapping owners name their neighbors in catalog descriptions; new checks guard both. Automatically available owners drop from 35 to 34 while their combined descriptions grow from 9,134 to 9,644 characters. [Scope](verification/scope-1.11.2.json) records 16 changed shared files out of 840. Host behavior is not run.

## Previous source: 1.11.1

The [1.11.1 source checks](verification/release-1.11.1.json) pass canonical validation and 191 tests: 135 Node in the CI set, 9 motion-quality, 12 installer, 4 identity, 8 GEPA pilot and 23 asset checks. The `workflow-orchestrator` entry shrinks from 38,834 to 29,255 bytes and its description from about 800 to 397 characters. The welcome excerpts, language policy and route rows are byte-identical; the full version procedure and rare routing boundaries moved verbatim to two linked references, guarded by a new budget and reference check. [Scope](verification/scope-1.11.1.json) records 8 changed and 2 added shared files out of 840. Host behavior is not run.

## Previous source: 1.11.0

The [1.11.0 source checks](verification/release-1.11.0.json) pass canonical validation and 190 tests (3 skipped): 134 Node in the CI set, 9 motion-quality, 12 installer, 4 identity, 8 GEPA pilot (3 skipped without the optional dependency) and 23 asset checks. The research gate is now conditional on six named triggers; validators reject a reverted mandatory gate, missing triggers and untriggered cases that expect the research owner. [Scope](verification/scope-1.11.0.json) records 75 changed shared files, 763 unchanged and no added or removed paths; the welcome assets and 441 vendored or upstream files are byte-identical. The planned suite has 201 cases, all not_run. GitHub release, saved-host readback and active-client behavior are not run for this source; see [release status](RELEASE_STATUS.md).

## Previous source: 1.10.1

The [1.10.1 source checks](verification/release-1.10.1.json) pass canonical validation and 170 tests: 131 Node, 12 installer, 4 identity and 23 asset checks. The focused fix retains the `hyperframes-workflow` ID while displaying Motion Graphics Workflow, makes work-area selection independent of engine selection, and allows requirement-led Remotion recommendations. [Scope](verification/scope-1.10.1.json) records 18 changed shared files and 820 byte-identical files. The 320-record library, complete welcome, dependency files and upstream snapshots are unchanged. Publication and actual client behavior are recorded separately in [release status](RELEASE_STATUS.md).

## Previous source: 1.10.0

The [1.10.0 source checks](verification/release-1.10.0.json) pass canonical validation and 169 tests: 130 Node, 12 installer, 4 package identity and 23 asset checks. The nine new Node checks cover score timing, review boundaries, optional adapter scheduling, provenance, retrieval and Polish aliases. The [bounded scope](verification/scope-1.10.0.json) contains 838 package files: 30 added, 14 changed and 794 byte-identical to 1.9.4. Both complete welcome resources, 37 skill identities and vendored snapshots are preserved.

The library contains 120 original not_run blueprints, 172 permitted curator reconstructions and 28 creator link records. An existing local encode was inspected with the new helper: 900 decoded frames and 30 contact-sheet samples. This is not continuous playback or listening evidence. Paper/Tone adapters have mock verification only; no new dependency was installed. No controlled Claude/OpenAI comparison was run. All 199 planned host cases remain not_run. Paired publication and active-client observations are recorded separately in [release status](RELEASE_STATUS.md).

## Previous source: 1.9.4

The [1.9.4 source checks](verification/release-1.9.4.json) pass the canonical validator and 160 existing tests. [Scope checks](verification/scope-1.9.4.json) confirm 808 package paths, 37 skills, 16 changed files and 792 byte-identical files. The welcome changes are exactly deletion of option 3 and its reply token in both languages; motion modules and all other skill entrypoints remain unchanged. Saved-host and active-client evidence is recorded separately in release status. The 199 planned host scenarios remain not_run.

## Previous source: 1.2.10

The [1.2.10 source checks](verification/release-1.2.10.json) passed canonical validation, 78 Node tests, 10 installer tests and 23 asset checks. Six new regression tests cover the four audited defects, including decimal-price boundaries and malformed blueprint sections. All 736 package archive entries match source; 723 unchanged package files match the 1.2.9 baseline byte-for-byte. Thirteen changed paths comprise eight targeted implementation/test files and five version/release files. No skill roots, routing contracts, provider rules, assets, pinned sources, starter prompts or canonical welcome were changed. [GitHub publication](verification/github-publication-1.2.10.json) confirms the source commit, successful workflow, five release assets, matching plugin ZIP digest and all 736 package blob hashes. [Hosted readback](verification/hosted-release-1.2.10.json) confirms all 13 changed files and all 725 readable files byte-for-byte, plus the complete 736-path/size inventory. Eleven unchanged large/binary files lack direct hosted byte readback. Codex automatically fetched 1.2.10; all 736 cached files match source. Installed-client behavior and the 183 planned host cases remain unexecuted.

## Previous source: 1.2.9

The [1.2.9 source checks](verification/release-1.2.9.json) passed canonical validation, 72 Node tests, 10 installer tests and 23 asset checks. Three new regression tests cover conflicting CQoT names, lost shared-budget/evidence rules and unreachable conditional-method routes for direct reviewers and research. The package retains 736 files and 37 skill roots. One fresh source-use prompt task retained the accepted direction and exact copy, produced one requested prompt and did not claim current model-version verification or a guaranteed perfect render. This is source-use evidence, not installed-client observation. The 183 planned host cases remain unexecuted. [GitHub publication](verification/github-publication-1.2.9.json) verifies the published tag, successful workflow, five uploaded assets, matching plugin ZIP digest and all 736 package hashes. [Hosted readback](verification/hosted-release-1.2.9.json) confirms all 15 uploaded files byte-for-byte, the complete path/size inventory and unchanged welcome; 721 omitted files are preserved by the guarded overlay without individual omitted-byte comparison. Active-client behavior remains unverified. Paired publication status is recorded in [release status](RELEASE_STATUS.md).

## Previous source: 1.2.5

The [1.2.5 source checks](verification/release-1.2.5.json) passed canonical validation, fourteen learning source tests, ten installer tests, complete source-manifest verification, package byte checks and preservation checks for the unchanged 734-file/37-skill inventory. The existing learning entry, mentoring method, integration policy and workstyle owner now require one onboarding question per response and wait for its answer, reusing supplied facts and stopping as soon as a useful plan can begin. The canonical welcome is unchanged. The 183 planned host cases remain unexecuted. One fresh sandbox conversation covered four responses: subject choice, one outcome question, an unknown answer leading to one experience question, and a voluntary complete brief leading directly to the requested plan-only output. The first three responses each contained one question, a numbered choice and a free-text alternative. GitHub CI passed 62 Node tests, 10 installer tests and 23 asset checks. [Publication](verification/github-publication-1.2.5.json) records v1.2.5, five verified assets and all 734 package hashes matching source. [Hosted readback](verification/hosted-release-1.2.5.json) verifies all fourteen changed files byte-for-byte, the complete 734-path/size inventory and the unchanged canonical welcome text; the guarded overlay preserved 720 omitted files. Actual installed-client behavior remains unverified.

## Previous source: 1.2.4

The [1.2.4 source checks](verification/release-1.2.4.json) passed canonical validation, fourteen learning source tests, ten installer tests, complete source-manifest verification, package byte checks and preservation checks for the 734-file/37-skill bundle. One new production asset is the single Polish welcome; the existing entry owner copies it verbatim on each sent bare invocation. One fresh sandbox conversation covered three responses: the initial canonical welcome, creative pace menu and identical repeated canonical welcome. This is source-use evidence, not installed-client behavior. The 183 planned host cases remain unexecuted. GitHub CI passed 62 Node tests, 10 installer tests and 23 asset checks. [Publication](verification/github-publication-1.2.4.json) records v1.2.4, five verified assets and all 734 package hashes matching source. [Hosted readback](verification/hosted-release-1.2.4.json) verifies all thirteen changed/new files byte-for-byte and the complete 734-path/size inventory; the guarded overlay preserved 721 omitted files. Actual installed-client behavior remains unverified.

## Previous source: 1.2.3

The [1.2.3 source checks](verification/release-1.2.3.json) passed canonical validation, complete source-manifest verification, package byte checks and preservation checks for the 733-file/37-skill bundle. Ordinary-language format intake is carried by the existing orchestrator, brief and static owners. No executable production code, upstream source, skill identity or platform-specific pixel specification changed. A fresh source-use conversation covered four responses: numbered purpose selection, familiar paper-size explanations, a natural-language A5 choice and a supplied Facebook post bypass. GitHub CI passed 62 Node checks, 10 installer tests and 23 asset checks. [Publication](verification/github-publication-1.2.3.json) records v1.2.3, five verified assets and 733 package file hashes matching local source. [Hosted readback](verification/hosted-release-1.2.3.json) verifies all nine changed files byte-for-byte and the complete 733-path/size inventory; the guarded overlay preserved 724 omitted files. These observations do not prove active-client behavior.

## Previous source: 1.2.2

The [1.2.2 source checks](verification/release-1.2.2.json) passed canonical validation, 48 local Node runner checks, 23 asset checks, 10 installer tests and nine additional installer probes. Two fresh low-reasoning sandbox conversations covered seven responses, including expired-menu clarification and offline-learning disclosure. These are source-use probes, not installed-client observations. GitHub CI passed 62 Node checks, 10 installer tests and 23 asset checks, then published v1.2.2 with five verified assets. The plugin ZIP digest matches the complete local archive. [GitHub publication](verification/github-publication-1.2.2.json) verifies all 733 package file hashes; [hosted readback](verification/hosted-release-1.2.2.json) verifies the 14 changed files byte-for-byte and the complete 733-path/size inventory, with 719 omitted files preserved by the guarded overlay. The package retains 733 files and 37 skill roots; no stress reports or transcripts were added. Active-client behavior remains unverified.

## Previous source: 1.2.1

This update restores the complete welcome and the creative entry sequence. Current deterministic source checks, package inventory, bounded text-only entry probe and paired release readback are recorded in [1.2.1 source checks](verification/release-1.2.1.json). GitHub CI passed all 62 Node tests and published v1.2.1 with five verified assets. All 17 changed/new hosted files are byte-equal to source, and the complete 733-path/size inventory matches; see [publication](verification/github-publication-1.2.1.json) and [hosted readback](verification/hosted-release-1.2.1.json). The probe is an attributed source-use exercise, not observed behavior of a newly installed ChatGPT/Codex client. The 183 planned cases remain unexecuted host specifications.

## Previous source: 1.2.0

The learning-mode source checks are recorded in [1.2.0 verification](verification/release-1.2.0.json). They cover the 37-skill package, mapped learning domains, menu/production-entry instructions, lesson/progress contracts, source-guarded greeting override, existing production checks, native wrapper and complete source inventory. These are deterministic source and filesystem checks, not executed conversations or educational outcome measurements.

The new `learning-mode-cases.json` contributes sixteen planned scenarios. The effective suite contains 183 planned cases; loading and validating them is not running a model. The [1.2.0 hosted readback](verification/hosted-release-1.2.0.json) confirms the existing private plugin was updated: all 22 changed/new files match local source (byte equality, except normalized JSON where recorded), and its complete 732-path inventory matches. This does not confirm a client cache refresh or a running lesson. GitHub commit `65ab9bb8e54a88155acf3316241b79591ecc7983` and release `v1.2.0` are published, with a successful release workflow and five verified assets; see [publication evidence](verification/github-publication-1.2.0.json) and [release status](RELEASE_STATUS.md). The subsequent [source parity check](verification/source-parity-1.2.0.json) confirms byte equality for 721 readable files and path/size equality for all 732 files after matching the host manifest serialization. Seven large text files and four binary files could not be hash-checked because source reads returned HTTP 413 and archive downloads returned HTTP 403; these files were not changed in this update.

The historical [1.1.1 source checks](verification/release-1.1.1.json) and [hosted readback](verification/hosted-release-1.1.1.json) retain their original scope and release attribution.

## Historical evidence

The [1.1.0 source checks](verification/release-1.1.0.json) cover the provider catalog and installation guidance. They do not establish live provider authentication, entitlement, generation or all-host support.

The [dev.31 report](plugins/framecore-work-creative-studio/docs/creative-upgrade-verification.json) records 43 passing Node checks, 23 passing Python checks and two bounded text-use exercises. These are historical observations, not fresh results for 1.0.0.

The dev.33 saved package was checked against the submitted source and its original logo. Its structural validation passed before this release preparation.

## Not executed

- The 183 planned behavioral evaluation specifications, including sixteen learning-mode scenarios.
- Real-client pilots and generated-media quality evaluation.
- External paid-provider integrations.
- New installations across every ChatGPT/Codex surface.
- Automatic cross-host memory synchronization.
- Fresh-session learning/creation behavior, native choice controls and educational effectiveness on the 1.2.0 release.

The presence of fixtures, examples or expected outputs is not recorded as passing execution.
