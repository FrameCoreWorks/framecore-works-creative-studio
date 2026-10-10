# Development ledger

Repository development metadata. Each integrated change made from ChatGPT Work, Codex, Cloud Code or another authorized surface gets one entry. The ledger is outside the shared runtime package. Git history and current file content remain the authority; an entry records intent, provenance and verification limits.

Entry fields: change ID, origin (`human`, `chatgpt-work`, `codex`, `cloud-code` or another named environment), baseline SHA, result SHA, package version change, scope, whether the shared package changed, verification and cross-host state. Use only `synchronized`, `pending`, `unknown` or `not_run` for cross-host state, and `synchronized` only with readback evidence.

## CC-20261006-01

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-01-conditional-research`
- Baseline: `928199aefdd004d36d1d42e45092d1ce002a0854` (main, package 1.10.1)
- Result: `91f80c96445df0120f2415615b849c1dbd0124b0` (package 1.11.0); work-in-progress parent `36ac03d`
- Package version: 1.10.1 -> 1.11.0
- Scope: conditional, trigger-based research gate (roadmap item 1); offline handling for ChatGPT without search and Codex with network disabled
- Shared package changed: yes; 75 changed files, 0 added, 0 removed ([scope](../verification/scope-1.11.0.json))

Verification:

- canonical validator: PASS
- Node CI set 134, motion-quality 9, installer 12, identity 4, GEPA pilot 8 (3 skipped), asset 23: PASS
- install inventory regenerated; local package build: PASS
- host behavior: not_run; 201 planned cases not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `391fa79` on owner instruction; [v1.11.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.11.0) published by workflow 37453689737; 838 blobs and plugin ZIP hash match ([record](../verification/github-publication-1.11.0.json))
- ChatGPT Work: pending; the owner updates the hosted plugin through ChatGPT Work (hosted plugin was 1.10.1 at publication)
- Codex: pending

Notes:

- Preserved skill IDs, complete welcome, automatic language policy, startup menus and vendored snapshots.
- Version 1.11.0 was chosen because an unpublished 1.10.2 exists outside this repository; that 1.10.2 is not part of this history.
- No search, provider call, rendering or media inspection was performed.

## CC-20261006-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-02-orchestrator-slim`
- Baseline: `41e6bc9e1cb74cb0cca862595196995217291bcb` (main, package 1.11.0)
- Result: `9401d17a11ebdb1aac367efda50f759f4cfedae5` (package 1.11.1)
- Package version: 1.11.0 -> 1.11.1
- Scope: shorter `workflow-orchestrator` entry without behavior change (roadmap item 2)
- Shared package changed: yes; 8 changed, 2 added, 0 removed ([scope](../verification/scope-1.11.1.json))

Verification:

- canonical validator: PASS
- Node CI set 135, motion-quality 9, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- install inventory regenerated; local package build: PASS
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `15b253c` on owner instruction; [v1.11.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.11.1) published by workflow 37458063083; 840 blobs and plugin ZIP hash match ([record](../verification/github-publication-1.11.1.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

Notes:

- Welcome excerpts, language policy and route rows are byte-identical; moved paragraphs are verbatim apart from relative links.
- Host installation and update checks are handled by the owner, per the owner's instruction on 2026-10-06.

## CC-20261006-03

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-03-skill-routing`
- Baseline: `3abbd6dc5ad509c2f9dc1500fe0c41da380a433c` (main, package 1.11.1)
- Result: `aa1d672aa0796344ce7bb664f8a800b50f46142c` (package 1.11.2)
- Package version: 1.11.1 -> 1.11.2
- Scope: routing boundaries for overlapping owners; legacy audio alias explicit-only (roadmap item 3)
- Shared package changed: yes; 16 changed, 0 added, 0 removed ([scope](../verification/scope-1.11.2.json))

Verification:

- canonical validator: PASS
- Node CI set 136, motion-quality 9, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- install inventory regenerated; local package build: PASS
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `40672b9` on owner instruction; [v1.11.2](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.11.2) published by workflow 37460600966; 840 blobs and plugin ZIP hash match ([record](../verification/github-publication-1.11.2.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

Notes:

- Not changed on purpose: pipeline-core, asset-manifest, instruction-packet-factory and storytelling stay automatically available. All 36 other owners read pipeline-core references, and host access to files of a non-injected skill is unverified.
- Prior evidence: the dev.31 host catalog listed 35 entries and hid the two explicit-only owners ([migration status](../plugins/framecore-work-creative-studio/docs/migration-status.md)).

## CC-20261006-04

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-04-no-delete-rule`
- Baseline: `d48e05280eafdd6e036b223db38498f727d8ab6a` (main, package 1.11.2)
- Package version: unchanged (1.11.2)
- Scope: record the no-delete constraint of ChatGPT Work plugin updates in `AGENTS.md` (roadmap item 5 outcome)
- Shared package changed: no

Evidence (owner-run Plugin Creator diagnostic in ChatGPT Work, 2026-10-06, reported to Cloud Code):

- existing plugin `plugins_6ab8e226cbd48191b661cb2ea24d0351`, saved version 1.11.1, current release `pluginrel_6ac4e07da2508191b1627b6f53b82f21`
- `update_plugin` documentation: "This tool cannot delete files"; archive updates overlay the current release and keep omitted files; no full-replacement parameter
- full file listing: 840 files, 394 under `integrations/workflow-kit/upstream/`

Decision:

- Keep `integrations/workflow-kit` unchanged (option 1 of the roadmap item 5 analysis). Removing the 4.36 MB expanded mirror would leave its 394 files in the hosted plugin and break inventory parity without reducing hosted size.
- Retire package files only by stubbing in place; never delete, rename or move package paths.

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `9df70f5` on owner instruction (no release: package unchanged)
- ChatGPT Work: not affected (no package change)
- Codex: not affected (no package change)

## CC-20261006-05

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-05-motion-craft`
- Baseline: `4044cd74448d2c7d48ccd8fc0daaf88ec6eae043` (main, package 1.11.2)
- Result: `327b7e57f49b5f76500d9fef189d47e311132116` (package 1.12.0)
- Package version: 1.11.2 -> 1.12.0
- Scope: Motion Graphics Workflow method rewrite, motion craft reference, Remotion kinetic type and GSAP starters sharing one `motion-score.json`
- Shared package changed: yes; 12 changed, 19 added, 0 removed ([scope](../verification/scope-1.12.0.json))

Verification:

- canonical validator: PASS
- Node CI set 139, motion-quality 9, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- packaged starters run in a development container: Remotion typecheck, contract check and 300-frame H.264 render; GSAP direct, forward and backward seeks pixel-identical
- full playback review, GSAP video encoding and host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `ad451ee` on owner instruction; [v1.12.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.12.0) published by workflow 37490293094; 859 blobs and plugin ZIP hash match ([record](../verification/github-publication-1.12.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

Notes:

- Only new paths were added; no package path was deleted, renamed or moved.
- Starter dependencies are pinned with lockfiles; no `node_modules` or rendered output is in the package.

## CC-20261006-06

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-06-html-preview`
- Baseline: `5769ad9288db76842b56104bc78c8e0407abc247` (main, package 1.12.0)
- Result: `4aa8d0319da54a74c7c0cf9609f71727990aeaf5` (package 1.13.0)
- Package version: 1.12.0 -> 1.13.0
- Scope: self-contained single-file motion preview for hosts without shell or renderer (motion direction 5)
- Shared package changed: yes; 10 changed, 2 added, 0 removed ([scope](../verification/scope-1.13.0.json))

Verification:

- canonical validator: PASS
- Node CI set 140, motion-quality 9, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- template opened via `file://` in headless Chromium; six frames inspected; direct, forward and backward seeks pixel-identical
- interactive Play and host behavior: not_run

Host evidence:

- Owner-run ordinary ChatGPT diagnostic on 2026-10-06: Canvas unavailable in that conversation; the test files were not executed there. The mode was therefore designed not to depend on Canvas.

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `bc631cf` on owner instruction; [v1.13.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.13.0) published by workflow 37492623075; 861 blobs and plugin ZIP hash match ([record](../verification/github-publication-1.13.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261006-07

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-07-motion-contract`
- Baseline: `6c1f8023641a9b1df9ebaba13dda209e8cfe8e17` (main, package 1.13.0)
- Result: `45e0cbfa56c03b70e4f582c904ea7c1a2253a9cf` (package 1.14.0)
- Package version: 1.13.0 -> 1.14.0
- Scope: one motion contract JSON for storyboard, approval and timeline (motion direction 4)
- Shared package changed: yes; 20 changed, 1 added, 0 removed ([scope](../verification/scope-1.14.0.json))

Verification:

- canonical validator: PASS
- Node CI set 142, motion-quality 9, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- packaged starters reinstalled and rerun; strict storyboard check PASS; GSAP and single-file preview frame 140 pixel-identical to the previous release
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `65609d5` on owner instruction; [v1.14.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.14.0) published by workflow 37499901576; 862 blobs and plugin ZIP hash match ([record](../verification/github-publication-1.14.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261006-08

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-08-library-index`
- Baseline: `f507d82bd20bd1848e556e0e10392b6c0c73ebbe` (main, package 1.14.0)
- Result: `7ef7be2c78a6e03af66d15eff995c2074c97f432` (package 1.15.0)
- Package version: 1.14.0 -> 1.15.0
- Scope: motion prompt library brief index and record-specific objectives for 60 blueprints (motion direction 6)
- Shared package changed: yes; 17 changed, 1 added, 0 removed ([scope](../verification/scope-1.15.0.json))

Verification:

- canonical validator: PASS
- Node CI set 145, motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- library validate: 320 entries, 19 brief types, no errors
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `2ddc4e5` on owner instruction; [v1.15.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.15.0) published by workflow 37501244215; 863 blobs and plugin ZIP hash match ([record](../verification/github-publication-1.15.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261006-09

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-09-scene-kinds`
- Baseline: `b5a2f56d3ce1240eb5a1043253566c740da9d260` (main, package 1.15.0)
- Result: `f06456dc3eea6429fe60733534e49cc7c0f5761c` (package 1.16.0)
- Package version: 1.15.0 -> 1.16.0
- Scope: declarative scene kinds rendered by one shared engine in the single-file preview and the Remotion starter (motion direction 7, second round)
- Shared package changed: yes; 21 changed, 4 added, 0 removed ([scope](../verification/scope-1.16.0.json))

Verification:

- canonical validator: PASS
- Node CI set 148, motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- preview frames pixel-identical to 1.15.0; all-kinds example rendered in preview and Remotion (775-frame H.264); packaged Remotion starter reinstalled, typechecked and rendered
- full playback review and host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `909c1f0` on owner instruction; [v1.16.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.16.0) published by workflow 37503394895; 867 blobs and plugin ZIP hash match ([record](../verification/github-publication-1.16.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261006-10

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-10-frame-review`
- Baseline: `f16c18e55c6ac187890e5f35a038dc520a1f669f` (main, package 1.16.0)
- Result: `47baaab0070e37ece2cd163b3a7784732ce6ec55` (package 1.17.0)
- Package version: 1.16.0 -> 1.17.0
- Scope: automated frame review with preview review mode and contact sheet (motion direction 8, second round)
- Shared package changed: yes; 11 changed, 2 added, 0 removed ([scope](../verification/scope-1.17.0.json))

Verification:

- canonical validator: PASS
- Node CI set 149 (+1 opt-in browser test passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- review tool in headless Chromium: starter and all-kinds contracts without findings; broken contract flagged with exit code 1
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `659f31f` on owner instruction; [v1.17.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.17.0) published by workflow 37521316269 (second attempt after a GitHub HTTP 502); 869 package files and plugin ZIP hash match ([record](../verification/github-publication-1.17.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261006-11

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-11-formats` (stacked on the unpushed CC-20261006-10 branch)
- Baseline: `659f31f95aba386a6d253f3fe881dce881930cf1` (CC-20261006-10 head, package 1.17.0)
- Result: `e5e2ee3ef6b4774d07c398b5694dda4155eb29eb` (package 1.18.0)
- Package version: 1.17.0 -> 1.18.0
- Scope: output formats in the motion contract (16:9, 9:16, 1:1 from one timeline) and true-size review screenshots (motion direction 9, second round)
- Shared package changed: yes; 25 changed, 0 added, 0 removed ([scope](../verification/scope-1.18.0.json))

Verification:

- canonical validator: PASS
- Node CI set 150 (+1 opt-in browser test passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- container: starter reviewed in three formats without findings; base format pixel-identical to 1.17.0; preview and Remotion stills pixel-identical per format; no full per-format video render
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `e5cf3c5` on owner instruction; [v1.18.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.18.0) published by workflow 37522878932; 869 package files and plugin ZIP hash match ([record](../verification/github-publication-1.18.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261006-12

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-12-audio-sync`
- Baseline: `d05c38b57376b5482bef552b4a61021d33f62c77` (main, package 1.18.0)
- Result: `3c42040dc5ee3b80a48a2178062782ba74998c58` (package 1.19.0)
- Package version: 1.18.0 -> 1.19.0
- Scope: music beat grid, voice-over caption import, captions and audio in preview and Remotion (motion direction 10, second round)
- Shared package changed: yes; 25 changed, 3 added, 0 removed ([scope](../verification/scope-1.19.0.json))

Verification:

- canonical validator: PASS
- Node CI set 152 (+1 opt-in browser test passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- container: captioned starter reviewed in three formats without findings; uncaptioned output pixel-identical to 1.18.0; click-track render with sample-exact beat spacing and a 42.7 ms AAC start delay; preview audio playback not exercised
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `7e39fd0` on owner instruction; [v1.19.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.19.0) published by workflow 37526607956; 872 package files and plugin ZIP hash match ([record](../verification/github-publication-1.19.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261006-13

- Origin: cloud-code
- Branch: `cloud-code/CC-20261006-13-browser-export`
- Baseline: `a572cb17b5cb7a9dc64d2c74d8da268ec4ae6f0d` (main, package 1.19.0)
- Result: `a9b9545a059e7e7b562ea3c833f6d3a6104a1412` (package 1.20.0)
- Package version: 1.19.0 -> 1.20.0
- Scope: browser video export from the single-file preview and a shell exporter (motion direction 11, second round); owner chose MP4 where possible with WebM fallback, video only
- Shared package changed: yes; 12 changed, 3 added, 0 removed ([scope](../verification/scope-1.20.0.json))

Verification:

- canonical validator: PASS
- Node CI set 155 (+2 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- container (Chromium 1194): VP9 WebM exports read by ffprobe; drawn frames pixel-identical to Remotion; MP4 writer verified with a libx264 stream; browser H.264 not offered by this build
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `bacf565` on owner instruction; [v1.20.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.20.0) published by workflow 37530222815; 875 package files and plugin ZIP hash match ([record](../verification/github-publication-1.20.0.json))
- Ordinary ChatGPT export test, 2026-10-07: PASS_REPORTED by the owner (Android phone browser, reasoning setting not reported): MP4 H.264 `avc1.640028`, 1920 x 1080, 180 frames, 409 kB, plays. The delivered preview had custom controls rather than the unchanged template ([report](../verification/host-report-2026-10-07-browser-export.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-02-template-and-sweep` (stacked on the unpushed CC-20261007-01 report branch)
- Baseline: `cd00f85c5291920e97fb95492ee96be4ff602892` (CC-20261007-01 head, package 1.20.0)
- Result: `658946d350ebe55f4af0ac0a3e8f695c492320d5` (package 1.21.0)
- Package version: 1.20.0 -> 1.21.0
- Scope: preview template kept intact with a check-preview gate, sweep exit, clearer contract checks; owner approved after the 2026-10-07 ChatGPT test analysis
- Shared package changed: yes; 16 changed, 2 added, 0 removed ([scope](../verification/scope-1.21.0.json))

Verification:

- canonical validator: PASS
- Node CI set 157 (+2 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- container: check-preview rejects the owner-supplied ChatGPT preview and passes the template-built example; sweep pixel-identical in preview and Remotion; existing contracts unchanged
- host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `736e279` on owner instruction; [v1.21.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.21.0) published by workflow 37574652135; 877 package files and plugin ZIP hash match ([record](../verification/github-publication-1.21.0.json))
- Ordinary ChatGPT retest on 1.21.0, 2026-10-07: the delivered HTML fails check-preview (hand-written renderer, MediaRecorder export, no template engine or export) although its contract follows 1.21.0 (kinds, sweep exit); its Export video produced no MP4 on the owner device (FAIL_REPORTED); recorded as FAIL_SOURCE_INSPECTION ([report](../verification/host-report-2026-10-07-template-test.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-04

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-04-motion-player`
- Baseline: `1ded66114406a81639c8299ca2a35af990c57d88` (main, package 1.21.0)
- Result: `2673475eb3bb5c4e587f8330f543d34c5b65cfd9` (package 1.22.0)
- Package version: 1.21.0 -> 1.22.0
- Scope: motion player (Open contract), contract-plus-player delivery with a WebCodecs-only export fallback for self-written pages, player release asset and Pages workflow, export CLI hardening; owner approved after the second 2026-10-07 ChatGPT test (the CC-20261007-03 report was first kept local at the owner's request and published later on 2026-10-07 on owner instruction)
- Shared package changed: yes; 13 changed, 0 added, 0 removed ([scope](../verification/scope-1.22.0.json)); repository-only: `.github/workflows/pages.yml`, `scripts/package_release.py`, `scripts/publish_github_release.py`

Verification:

- canonical validator: PASS
- Node CI set 158 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- container: player opens and exports valid contracts and rejects invalid ones; release player byte-identical to the template; Pages steps simulated locally; export CLI races reproduced and fixed
- GitHub Pages: not enabled; host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `4df37e9` on owner instruction; [v1.22.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.22.0) published by workflow 37585412547 with the motion player file; 877 package files, plugin ZIP and player hashes match ([record](../verification/github-publication-1.22.0.json))
- GitHub Pages: workflow 37585412460 created `gh-pages` with the template as index.html; the owner enabled Pages on 2026-10-07 and the site is live (HTTP 200, byte-identical to the template; a contract opened and exported there in Chromium) ([record](../verification/github-publication-1.22.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-05

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-05-player-link`
- Baseline: `54b39e882957a5d5d003a07dd3b47eb1054e1061` (main, package 1.22.0)
- Result: `a1b88b4f444ebc72b8cf134ff96c26bd46f8987b` (package 1.23.0)
- Package version: 1.22.0 -> 1.23.0
- Scope: one clickable player link carrying the contract, `player-link.mjs`, no substitute videos, approval rule for direct build requests; owner approved after test A, declined the in-chat MCP player prototype for now
- Shared package changed: yes; 13 changed, 1 added, 0 removed ([scope](../verification/scope-1.23.0.json))

Verification:

- canonical validator: PASS
- Node CI set 159 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- the one-click link for the test A contract opened and exported on the live player in Chromium; owner: it opened on their device (PASS_REPORTED, [report](../verification/host-report-2026-10-07-test-a.json))
- ChatGPT behavior with the new rule: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `d687f58` on owner instruction; [v1.23.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.23.0) published by workflow 37591516754; 878 package files, plugin ZIP and player hashes match ([record](../verification/github-publication-1.23.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-06

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-06-mp4-first`
- Baseline: `0d5d0de17aa95cf4599c647229df3d8a24744255` (main, package 1.23.0)
- Result: `6631e693797187f0836bb1d70107c4b3e11871ba` (package 1.24.0)
- Package version: 1.23.0 -> 1.24.0
- Scope: MP4-first delivery with a frame check, HTML preview without export, 1.23.0 player-link requirements withdrawn; owner decision after test C ("keep the MP4 download plus an HTML preview; no GitHub Pages link for now")
- Shared package changed: yes; 10 changed, 0 added, 0 removed ([scope](../verification/scope-1.24.0.json))

Verification:

- canonical validator: PASS
- Node CI set 159 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- test C files inspected ([report](../verification/host-report-2026-10-07-test-c.json)); test D on 1.24.0: ChatGPT followed the new steps (MP4 and contract, frames named, no preview export), MP4 clean and contract valid on inspection ([report](../verification/host-report-2026-10-07-test-d.json))

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `ddae453` on owner instruction; [v1.24.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.24.0) published by workflow 37597377168; 878 package files, plugin ZIP and player hashes match ([record](../verification/github-publication-1.24.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-07

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-07-motion-audio-policy`
- Baseline: `5b7bfa19f0fd859ee196f8a9a220e03432a60d5d` (main, package 1.24.0)
- Result: `fcf51229b2c35166a58468d1b1135a71e3fdc31d` (package 1.25.0)
- Package version: 1.24.0 -> 1.25.0
- Scope: sound policy for motion deliveries (no code-synthesized audio; user file, connected and confirmed provider, or installed local generator), tested mux command, stale skill sentences removed; owner request after test D
- Shared package changed: yes; 10 changed, 0 added, 0 removed ([scope](../verification/scope-1.25.0.json))

Verification:

- canonical validator: PASS
- Node CI set 159 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- mux command tested on the test D MP4 with a click track
- owner tests on 1.25.0: ChatGPT Work delivered the unchanged template with its contract (check-preview PASS), a valid contract and a clean MP4 ([report](../verification/host-report-2026-10-07-work.json)); ordinary ChatGPT delivered a clean MP4 and a preview embedding it ([report](../verification/host-report-2026-10-07-test-e.json)); neither asked about sound, the prompt having said "Bez muzyki"
- owner decision: keep the sound rule as it is, without further step-by-step guidance

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `66ec071` on owner instruction; [v1.25.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.25.0) published by workflow 37600958954; 878 package files, plugin ZIP and player hashes match ([record](../verification/github-publication-1.25.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-08

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-08-contract-revisions`
- Baseline: `9f34127aa1d6cfebd2648b84e455bd86458cc79e` (main, package 1.25.0)
- Result: `b011eeb0a37f78726fa56cd6e756d31460388b34` (package 1.26.0)
- Package version: 1.25.0 -> 1.26.0
- Scope: contract revisions (start from the delivered contract, change only what was asked, increment revision, show was -> is, revision-suffixed files) and `motion-revise/revise.mjs` (`diff`, `extend`); owner choice "a" after the 1.25.0 tests
- Shared package changed: yes; 11 changed, 2 added, 0 removed ([scope](../verification/scope-1.26.0.json))

Verification:

- canonical validator: PASS
- Node CI set 160 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- `extend` on the starter example and on the 2026-10-07 ChatGPT contract: every result passed check-score; ChatGPT behavior with the revision rules: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `fefe5f6` on owner instruction; [v1.26.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.26.0) published by workflow 37607283263; 880 package files, plugin ZIP and player hashes match ([record](../verification/github-publication-1.26.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed
- Owner test on 1.26.0 (ChatGPT Work): revision rules followed; PASS_REPORTED ([report](../verification/host-report-2026-10-07-revision.json))

## CC-20261007-09

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-09-render-script`
- Baseline: `45b5548869ac186d963c107386039c3d8316b6ad` (main, package 1.26.0)
- Result: `98702ac093145a300e7360f8fbeb2ebf2395556c` (package 1.27.0)
- Package version: 1.26.0 -> 1.27.0
- Scope: render script delivered with the video and named in `runtime.script`, reused unchanged for revisions; check-score and revise.mjs support; owner choice "a" after the ChatGPT Work revision test
- Shared package changed: yes; 14 changed, 0 added, 0 removed ([scope](../verification/scope-1.27.0.json))

Verification:

- canonical validator: PASS
- Node CI set 161 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- both ChatGPT Work revision-test contracts rendered with one renderer: frames before the change byte-identical; ChatGPT Work behavior with the script rule: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `c0ae6d7` on owner instruction; [v1.27.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.27.0) published by workflow 37612739362; 880 package files, plugin ZIP and player hashes match ([record](../verification/github-publication-1.27.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed
- Owner decision (2026-10-07): small changes are not owner-tested one by one; source checks remain mandatory, an occasional larger ChatGPT Work test replaces per-change tests, and host results may differ between users' environments

## CC-20261007-10

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-10-python-renderer`
- Baseline: `3bda5518b69aa6e1ce025acef3b61085c3bad544` (main, package 1.27.0)
- Result: `65d8bf1d68043f388990c174656fd0b9bcbd92ca` (package 1.28.0)
- Package version: 1.27.0 -> 1.28.0
- Scope: bundled Python renderer (`motion-render/render.py`), a port of the scene engine, copied and run by code-execution hosts instead of their own drawing code; owner choice "a" (then "b", styles)
- Shared package changed: yes; 11 changed, 2 added, 0 removed ([scope](../verification/scope-1.28.0.json))

Verification:

- canonical validator: PASS
- Node CI set 162 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- renderer versus browser engine on three contracts: mean difference at most 0.86 grey levels; repeated renders byte-identical; ChatGPT Work sandbox run: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `748404f` on owner instruction after a failed first release run (bytecode in the install manifest, fixed in `748404f`); [v1.28.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.28.0) published by workflow 37619690244; 882 package files, plugin ZIP and player hashes match ([record](../verification/github-publication-1.28.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-11

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-11-motion-designer-methods`
- Baseline: `662bbbef2bc96e33d2b3b8b5fc1ba2d0ee976b17` (unpublished 1.28.0 on `cloud-code/CC-20261007-10-python-renderer`)
- Result: `7d6e8b7e6000ba4f321ed7d14b5f929a3d3f2d44` (package 1.29.0)
- Package version: 1.28.0 -> 1.29.0
- Scope: methods adapted from kaventro/motion-designer (MIT, `7d0b8bb`): motion styles, motion vocabulary and video types, review passes and scores, renderer motion blur and phone-size stills, retained beats.py and music_edit.py with a sound brief; owner request to compare the repository and implement what is new
- Shared package changed: yes; 14 changed, 8 added, 0 removed ([scope](../verification/scope-1.29.0.json))

Verification:

- canonical validator: PASS
- Node CI set 166 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- styles checked and rendered; beat analysis and bar cut of a click track exact; host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `fe70de9` (which merges the 1.28.0 bytecode fix) on owner instruction; [v1.29.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.29.0) published by workflow 37620623797; 890 package files, plugin ZIP, inventory and player hashes match ([record](../verification/github-publication-1.29.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-12

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-12-device-scenes`
- Baseline: `aadd9e3acfa9f2d2c6a81075af5c1f96b775ec7d` (main, package 1.29.0)
- Result: `776cc317f30d9ee275d57d1cdbb145c2e4b46205` (package 1.30.0)
- Package version: 1.29.0 -> 1.30.0
- Scope: product films (`device` scene kind in the engine, its copies and the Python renderer; product-film rules; app-film example) and the frame-review screenshot fix; owner chose the product-film direction
- Shared package changed: yes; 21 changed, 2 added, 0 removed ([scope](../verification/scope-1.30.0.json))

Verification:

- canonical validator: PASS
- Node CI set 168 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- app-film example reviewed in Chromium without findings; Python renderer within 0.86 grey levels of the browser; host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `1c2bc1b` on owner instruction; [v1.30.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.30.0) published by workflow 37625658353; 892 package files, plugin ZIP and player hashes match; Pages republished byte-identical ([record](../verification/github-publication-1.30.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed
- Owner review: the app-film example renders (16:9, 9:16) approved on 2026-10-07

## CC-20261007-13

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-13-taps-browser-backgrounds`
- Baseline: `bcb35c07aa47abf9c42f84577905fe990661867e` (main, package 1.30.0)
- Result: `e01238c1adb4253ba3ab5a190cdc2e2b4d66712c` (package 1.31.0)
- Package version: 1.30.0 -> 1.31.0
- Scope: device taps, browser frame and per-scene backgrounds with wipes (engine, its copies, check-score, Python renderer, examples); owner order a, b, c
- Shared package changed: yes; 21 changed, 1 added, 0 removed ([scope](../verification/scope-1.31.0.json))

Verification:

- canonical validator: PASS
- Node CI set 170 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- both examples reviewed in Chromium without errors; Python renderer within 0.86 grey levels of the browser; existing contracts byte-identical to 1.30.0; host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `94db9c9` on owner instruction; [v1.31.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.31.0) published by workflow 37629547896; 893 package files, plugin ZIP and player hashes match; Pages republished byte-identical ([record](../verification/github-publication-1.31.0.json))
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-14

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-14-motion-sound`
- Baseline: `94db9c91c19c444501899d9ab07e5cc1629f6e35` (main, package 1.31.0)
- Result: `6fd0189d27b54f85954d44fc0d71f45286057bc0` (package 1.32.0; two earlier work-in-progress commits on the branch)
- Package version: 1.31.0 -> 1.32.0
- Scope: motion sound design (cue planning from the picture's timing, layered synthesis, composed music bed, mastering, timing check) and the owner's sound-policy change (direction A); a CC0 recording library was built first, rejected by the owner for quality and removed before release
- Shared package changed: yes; 16 changed, 4 added, 0 removed ([scope](../verification/scope-1.32.0.json))

Verification:

- canonical validator: PASS
- Node CI set 173 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- three example mixes: hits within 2 ms, -14.1 to -15.7 LUFS, true peak at most -1.05 dBTP; owner listening: music and clicks approved, whooshes lowered; host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `c8ac235` on owner instruction; [v1.32.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.32.0) published by workflow 37641483672; 897 package files, plugin ZIP and player hashes match ([record](../verification/github-publication-1.32.0.json))
- Owner listening: lowered whooshes approved before publication
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261007-15

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-15-sound-refinement`
- Baseline: `ed8b70c5c1007eb739dcb387ee944c93e495b153` (main, package 1.32.0)
- Result: `1ccc65424720bfa94e766e7310743e8d125e2b16` (package 1.33.0); ten earlier commits on the branch record the audit, palettes, owner-rejected knock and snare, candidate sounds, sound direction and the generative engine
- Package version: 1.32.0 -> 1.33.0
- Scope: measured sound audit and fixes; then, on the owner's direction, sound and music designed anew for every video (contract analysis, generated effect recipes, composed music, quality gate, level checks); fixed minor-key chords and a 27 dB levelling error found by owner listening
- Shared package changed: yes; 15 changed, 6 added, 0 removed ([scope](../verification/scope-1.33.0.json))

Verification:

- canonical validator: PASS
- Node CI set 174 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23: PASS
- 20 designs of four examples: no timing failure (worst 1.46 ms); example mixes -14.0 to -14.3 LUFS; owner listening: approved after the landing swoosh fix; host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `1ccc654` on owner instruction; [v1.33.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.33.0) published by workflow 37732160230; plugin ZIP, inventory and player hashes match ([record](../verification/github-publication-1.33.0.json))
- Owner listening: generative renders approved after the landing swoosh fix
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261008-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261007-15-sound-refinement`
- Baseline: `1ccc65424720bfa94e766e7310743e8d125e2b16` (package 1.33.0; main carried test records and the sound test scenario on top)
- Result: `b2d9f6c006117cd078f0b3433cd1b1ae14577aa0` (package 1.34.0)
- Package version: 1.33.0 -> 1.34.0
- Scope: craft critique and a mandatory improvement round (also on delivered frames), measured AAC delivery, recorded user sound choices, owner references; outside the package, a blind motion benchmark kit (docs/motion-benchmark, scripts/motion_benchmark.py, tests)
- Shared package changed: yes ([scope](../verification/scope-1.34.0.json))

Verification:

- canonical validator: PASS
- Node CI set 175 (+3 opt-in browser tests passing), motion-quality 12, installer 12, identity 4, GEPA pilot 8, asset 23, benchmark script 3: PASS
- owner's ChatGPT Work test of 1.33.0 (GPT 6.1 Sol): four videos technically passing, steps 1 to 3 approved by ear, step 4 rejected as a direction; host behavior of 1.34.0: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `b2d9f6c` on owner instruction; [v1.34.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.34.0) published by workflow 37754297112; plugin ZIP, inventory and player hashes match ([record](../verification/github-publication-1.34.0.json))
- Owner decision: no further tests in this series; the Bounce Party direction is rejected
- ChatGPT Work: owner-managed
- Codex: owner-managed

## CC-20261008-03

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-03-intelligent-ui`
- Baseline: `2704f917535c723afe2c039b1cca67e6da0b5422` (main, package 1.34.0)
- Result: `7872bfdea5a30575a197e064fa85d4b579da2972` (adaptation) and the release commit carrying this entry (package 1.35.0)
- Package version: 1.34.0 -> 1.35.0
- Owner decision 2026-10-08: every change ends with a full release commit and push to `main` (a GitHub release follows from the release workflow); this replaces the earlier instruction that excluded publication. The hosted ChatGPT plugin is still updated only on the owner's instruction
- Scope: adaptation of every active module to ChatGPT's native Intelligent UI through one shared presentation policy, short domain routes, a structural validator, mutation tests and planned host scenarios ([record](intelligent-ui-adaptation.md))
- Shared package changed: yes; 17 changed, 4 added, 0 removed ([scope](../verification/scope-1.35.0.json))

Verification:

- canonical validator: PASS
- Node CI set 175 (+3 opt-in browser tests passing), motion-quality 12, presentation 10, installer 12, identity 4, GEPA pilot 8, asset 23, benchmark script 3: PASS ([record](../verification/release-1.35.0.json))
- instruction trace of 17 scenarios: one conflict found and repaired (plain-text request versus the storyboard table); host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `ecf6ed0` on owner instruction; [v1.35.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.35.0) published by workflow 37763045138; plugin ZIP, inventory and player hashes match ([record](../verification/github-publication-1.35.0.json))
- ChatGPT Work: not_run (no hosted update authorized)
- Codex: not_run

## CC-20261008-06

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-03-intelligent-ui`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `0e2d36307465715ff673277bb4631411c611563c` (main, package 1.35.0)
- Result: the release commit carrying this entry (package 1.36.0)
- Package version: 1.35.0 -> 1.36.0
- Scope: Studio offers an interactive version on its own, once per stage after the deliverable, saying whether it is a view in the chat or an HTML file; a decline is remembered for that kind of stage; skipped during onboarding, under a pending learner exercise and for copyable deliverables ([record](intelligent-ui-adaptation.md))
- Shared package changed: yes; 11 changed, 0 added, 0 removed ([scope](../verification/scope-1.36.0.json))

Verification:

- canonical validator: PASS
- Node CI set 175 (+3 opt-in browser tests passing), motion-quality 12, presentation 11, installer 12, identity 4, GEPA pilot 8, asset 23, benchmark script 3: PASS ([record](../verification/release-1.36.0.json))
- instruction trace: two conflicts resolved (one learner decision at a time; the host-capability note); host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `fe9e695`; [v1.36.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.36.0) published by workflow 37770199028; plugin ZIP, inventory and player hashes match ([record](../verification/github-publication-1.36.0.json))
- ChatGPT Work: not_run (hosted update on owner instruction only)
- Codex: not_run

## CC-20261008-07

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-03-intelligent-ui`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `379523918e775c98b1862d04b340d8c1426ebe56` (main, package 1.36.0)
- Result: the release commit carrying this entry (package 1.37.0)
- Package version: 1.36.0 -> 1.37.0
- Scope: fixes from the owner-supplied external audit (ChatGPT, GPT 6.1 Sol, of `e8884d8`), each reproduced first: critique status and exit 3 for uninspected frames, video decoding of review frames only with size, rate and length checks, silent cues reported missing, `extend` moving `sfx` and marking the sound design stale, `mix` refusing it, `plan` keeping user choices; outside the package the benchmark contract pick and video critique, `scripts/check_all.sh` for release and a new checks workflow ([response](audit-2026-10-08-response.md))
- Shared package changed: yes; 14 changed, 0 added, 0 removed ([scope](../verification/scope-1.37.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 187 (+3 opt-in browser tests; 60 passing in the browser run), installer 12, identity 4, benchmark script 5, GEPA pilot 8, asset 23: PASS ([record](../verification/release-1.37.0.json))
- audit reproductions and fix exercises in the container; host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `7a68ea8`; [v1.37.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.37.0) published by workflow 37773432571; checks workflow 37773432695 success; plugin ZIP, inventory and player hashes match ([record](../verification/github-publication-1.37.0.json))
- ChatGPT Work: not_run (hosted update on owner instruction only)
- Codex: not_run

## CC-20261008-08

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-03-intelligent-ui`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `c7202cc284abe29811290b9f1539024c00cc07a3` (main, package 1.37.0)
- Result: the release commit carrying this entry (package 1.38.0)
- Package version: 1.37.0 -> 1.38.0
- Scope: composed music plays on after an early reveal and resolves in the last bar (`endBar` in the music plan, both the recipe composer and the palette bed); contracts planned earlier keep their sound
- Shared package changed: yes; 12 changed, 0 added, 0 removed ([scope](../verification/scope-1.38.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 188 (+3 opt-in browser tests; 61 passing in the browser run), installer 12, identity 4, benchmark script 5, GEPA pilot 8, asset 23: PASS ([record](../verification/release-1.38.0.json))
- measured on an 8 s spot with the reveal at 4 s; color-block rendered before and after and sent to the owner; owner listening: PASS_REPORTED (new ending approved); host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `1d51919`; [v1.38.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.38.0) published by workflow 37775866204; checks workflow 37775866194 success; plugin ZIP, inventory and player hashes match ([record](../verification/github-publication-1.38.0.json))
- ChatGPT Work: not_run (hosted update on owner instruction only)
- Codex: not_run

## CC-20261008-10

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-10-full-review`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `0a6036ce98a7f0f03f43abae7263c9eca8292c5b` (main, package 1.38.0)
- Result: the commit carrying this entry (report only)
- Package version: 1.38.0 (unchanged)
- Scope: the full A-to-Z review the owner asked for ("1a 2b start review"), written as [docs/reviews/full-review-2026-10-08.md](reviews/full-review-2026-10-08.md): 3 high, 16 medium, 24 low and 6 informational findings, a ranked backlog and four owner decisions; no plugin or tool file changed (fixes wait for the owner's choice)
- Shared package changed: no

Verification:

- fresh clone of the baseline: canonical validator PASS; `scripts/check_all.sh` exit 0 (Node 188 pass, 3 browser tests skipped; installer 12, identity 4, benchmark script 5, GEPA pilot 8, asset 23); browser-run motion tests 61/61; legacy suite 134 errors and 20 of 67 tests failing, as before
- `v1.38.0` release ZIP byte-identical to the tag tree (908 files); renderer parity on four examples; sound and critique end to end on one example; host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `0d48e79`; the report and this ledger read back from `origin/main` with identical SHA-256; checks workflow 37800294869 success (the separate legacy job fails by design, as before)
- ChatGPT Work: not_run (package unchanged)
- Codex: not_run (package unchanged)

## Retroactive notes (recorded under CC-20261008-11)

The full review (F-REC-02, F-REC-03) found changes without an entry and one reused Change ID. They are recorded here instead of rewriting history:

- `CC-20261008-01`: `eb180bb` added the 1.33.0 ChatGPT Work sound test scenario; docs only, package unchanged.
- `CC-20261008-03` was used twice: first for the 1.33.0 ChatGPT Work sound test records (`eb252fe`, `dc51e51`, `1334b87`, `436d28c`, `f77a923`), then for the Intelligent UI change released as 1.35.0 (`7872bfd`, `ecf6ed0`, `fff1587`), which the entry above describes.
- `CC-20261008-04`: `173f261` recorded the owner's standing rule in AGENTS.md (push every verified update to `main`); docs only.
- `CC-20261008-05`: `e3db3e2`, `e8884d8`, `0e2d363` recorded the first Intelligent UI host observations for 1.35.0; records only.
- `CC-20261008-09`: `0a6036c` added the full review plan; docs only.

## CC-20261008-11

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-11-checks-and-tools`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `0205fa4d85e37058c94965c4d84b2a4d7ebf432a` (main, package 1.38.0)
- Result: the release commit carrying this entry (package 1.39.0)
- Package version: 1.38.0 -> 1.39.0
- Scope: the checks-and-tools part of the [full review](reviews/full-review-2026-10-08.md), with the owner's decisions of 2026-10-08 (recommended options, welcome unchanged): solo-render sound timing with a status, safe contract embedding, one reading-time rule, the improvement round inside the shared budget, renderer and export notes; outside the package the Codex entry's area count with a test, CI dependencies and `actions/checkout` on Node 24, the release-notes refresh, the legacy baseline, a pixel-parity browser test, README, install guide and records
- Shared package changed: yes; 20 changed, 0 added, 0 removed ([scope](../verification/scope-1.39.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 191 passing of 195 (4 opt-in browser tests; 65 passing in the browser run), installer 13, identity 4, benchmark script 5, GEPA pilot 8, asset 23: PASS ([record](../verification/release-1.39.0.json))
- legacy suite: matches `tests/legacy-baseline.json` (134 validator errors, 20 of 67 tests failing as recorded)
- preview with `</script>` in its copy opened in Chromium (ready, no injected element); host behavior: not_run

Cross-host state:

- GitHub: synchronized; `main` fast-forwarded to `f491647`; [v1.39.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.39.0) published by workflow 37814666113 with the media tests running in CI; checks workflow 37814666417 success, legacy baseline job success; plugin ZIP, inventory and player hashes match ([record](../verification/github-publication-1.39.0.json))
- ChatGPT Work: not_run (hosted update on owner instruction only)
- Codex: not_run

## CC-20261008-12

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-12-motion-route`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `3a9ff867d3cdb24755493dce4f88c42e4ced9bf5` (main, package 1.39.0)
- Result: the release commit carrying this entry (package 1.40.0)
- Package version: 1.39.0 -> 1.40.0
- Scope: motion graphics as a full route from the [full review](reviews/full-review-2026-10-08.md), with the owner's decisions of 2026-10-08 (recommended options; welcome and menus unchanged): the generated-or-coded video choice, a main route-table row, the product-film route and commercial video scope, the audio owner and orchestrator naming the motion sound engine, the `motion` review modality and four handoffs in the role contracts, the motion delivery list and owners table, Pipeline Core routing and kit leftovers, the interactive-offer state field, the workstyle pace menu language, six planned motion and sound cases, README capability text. Kept as is: the area 8 wording in the startup menus reference (pinned startup text)
- Shared package changed: yes; 28 changed, 1 added, 0 removed ([scope](../verification/scope-1.40.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 192 passing of 196 (4 opt-in browser tests; 66 passing in the browser run), installer 13, identity 4, benchmark script 5, GEPA pilot 8, asset 23: PASS ([record](../verification/release-1.40.0.json))
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run

Cross-host state:

- GitHub: pending (release workflow and readback recorded in the next update)
- ChatGPT Work: not_run (hosted update on owner instruction only)
- Codex: not_run

## CC-20261008-14

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-14-yaml-hotfix`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `00aa7553de7e4b8de549c15297ff54d7314174d4` (main, package 1.40.0)
- Result: the release commit carrying this entry (package 1.40.1)
- Package version: 1.40.0 -> 1.40.1
- Scope: hotfix found while preparing 1.41.0. 1.40.0 gave the Motion Graphics Workflow a description with an unquoted colon, so its SKILL.md frontmatter was not valid YAML; the canonical validator read it with a regular expression and passed. The description is quoted; all 74 skill YAML documents were parsed with PyYAML; the validator gains `SKILL_YAML` with a test. 1.40.0 is superseded
- Shared package changed: yes; 9 changed, 0 added, 0 removed ([scope](../verification/scope-1.40.1.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 193 passing of 197 (4 opt-in browser tests; 66 passing in the browser run), installer 13, identity 4, benchmark script 5, GEPA pilot 8, asset 23: PASS ([record](../verification/release-1.40.1.json))
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `434f59a`; release workflow 37839855429, checks 37839855755 and 37839858739, release-notes refresh 37839855439: success; [v1.40.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.40.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (909 of 909), all 37 skill frontmatters parse ([record](../verification/github-publication-1.40.1.json))
- ChatGPT Work: not_run (hosted update on owner instruction only; if 1.40.0 was saved to the hosted plugin, 1.40.1 replaces it)
- Codex: not_run

## CC-20261008-15

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-15-discovery-depth`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `a577173` (main, package 1.40.1, after the 1.40.1 publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.41.0)
- Package version: 1.40.1 -> 1.41.0
- Scope: discovery and depth from the full review (F-PKG-05, F-SKL-02, F-SKL-07, F-PKG-01 to F-PKG-03, F-SKL-05, F-SKL-06, F-SKL-08, F-SKL-10, F-LRN-01, IM1, IM3): trigger-first skill descriptions (37 total 7,593 characters); sourced references for caption readability, UGC formats and disclosure, and short-form structures; every reference and template reached from a skill with the new `REFERENCE_REACH` rule; three legacy alias references replaced by pointers (paths kept); learning topics and rendered comparisons for motion and sound; interactive quiz checks for teachers; wording fixes. Welcome and menus unchanged; F-ORCH-04 stays open because it is protected startup text
- Change ID note: `CC-20261008-13` was reserved for this work on a branch that was never pushed and is not used
- Shared package changed: yes; 54 changed, 3 added, 0 removed ([scope](../verification/scope-1.41.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 194 passing of 198 (4 opt-in browser tests; 66 passing in the browser run), installer 13, identity 4, benchmark script 5, GEPA pilot 8, asset 23: PASS ([record](../verification/release-1.41.0.json))
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `8e39f38`; release workflow 37842914810, checks 37842914841 and 37842918284, release-notes refresh 37842914815: success; [v1.41.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.41.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (912 of 912), all 37 skill frontmatters parse ([record](../verification/github-publication-1.41.0.json))
- ChatGPT Work: not_run (hosted update on owner instruction only)
- Codex: not_run

## CC-20261008-16

- Origin: cloud-code
- Branch: `cloud-code/CC-20261008-16-capability-smoke`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `49d7c39` (main, package 1.41.0, after the 1.41.0 publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.42.0)
- Package version: 1.41.0 -> 1.42.0
- Scope: the review's new modules NM1 (sound for supplied footage: `footage.py` and a footage mode in `sound.py`), NM2 (executable captions: `captions.py` with tests), NM3 (capability card with the `CAPABILITY_CARD` validator rule and links from the orchestrator, the capabilities reference and the role map) and IM2 (host smoke set, template, checker and test, outside the package); MS06 now expects a plan from measured cuts and one offer to mix. Welcome and menus unchanged
- Shared package changed: yes; 18 changed, 5 added, 0 removed ([scope](../verification/scope-1.42.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 196 passing of 200 (4 opt-in browser tests; 67 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, GEPA pilot 8, asset 23, captions 14: PASS ([record](../verification/release-1.42.0.json))
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run; footage sound not listened to by a person

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `3da2cdf`; release workflow 37884503169, checks 37884503184 and 37884505200, release-notes refresh 37884503230: success; [v1.42.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.42.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (917 of 917), all 37 skill frontmatters parse ([record](../verification/github-publication-1.42.0.json))
- ChatGPT Work: not_run (hosted update on owner instruction only)
- Codex: not_run

## CC-20261009-01

- Origin: cloud-code
- Branch: `cloud-code/CC-20261009-01-video-map`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `0e5ac1a` (main, package 1.42.0, after the 1.42.0 publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.43.0)
- Package version: 1.42.0 -> 1.43.0
- Scope: the review's IM4: a dated video-generator snapshot (twelve families, checked 2026-10-09) linked from Research Evidence, its model mapping and the Video Prompt Architect; the capability card's video entry and the knowledge map name it; the validator gains `SNAPSHOT_DATE` with a test. A research subagent started on 2026-10-08 stopped at an API session limit before writing anything; the snapshot was researched and written in this session instead. Welcome and menus unchanged
- Records note (review F-REC-04): tags `v1.0.0` and `v1.1.3` have no release record, and `verification/release-1.0.json` and `verification/release-preparation.json` have no tag; they are historical and left as they are
- Shared package changed: yes; 13 changed, 1 added, 0 removed ([scope](../verification/scope-1.43.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 197 passing of 201 (4 opt-in browser tests; 67 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, GEPA pilot 8, asset 23, captions 14: PASS ([record](../verification/release-1.43.0.json))
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run; no generator was run

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `f15fd5e`; release workflow 37886030856, checks 37886030784 and 37886032855, release-notes refresh 37886030883: success; [v1.43.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.43.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (918 of 918), all 37 skill frontmatters parse ([record](../verification/github-publication-1.43.0.json))
- ChatGPT Work: not_run (hosted update on owner instruction only)
- Codex: not_run

## CC-20261009-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261009-01-video-map` (repository-only follow-up), fast-forwarded into `main` under the owner's standing rule
- Baseline: `d0c6b04` (main, package 1.43.0, after its publication record); full SHA in the commit trailer
- Result: a repository-only commit; the package is unchanged (1.43.0)
- Scope: the owner chose on 2026-10-09 to update the hosted ChatGPT plugin to 1.43.0 with a readback (1a). This session cannot reach ChatGPT Work's Plugin Creator, so the update is prepared for the owner to run there: `scripts/check_hosted_readback.py` compares a readback JSON with `config/install-sources.json` and writes `verification/hosted-release-<version>.json` (verdicts `full_byte_parity`, `path_size_parity`, `mismatch`), with `tests/test_hosted_readback.py` in `scripts/check_all.sh`; CHATGPT_UPDATE.md describes the readback record
- Shared package changed: no

Verification:

- canonical validator: PASS; `scripts/check_all.sh`: PASS (adds 6 hosted-readback tests); package files unchanged

Cross-host state:

- GitHub: this commit on `main`; the package release stays v1.43.0
- ChatGPT Work: pending (update and readback to be run by the owner in ChatGPT Work)
- Codex: not_run

## CC-20261009-03

- Origin: cloud-code, from the owner's ChatGPT Work readback
- Branch: `cloud-code/CC-20261009-01-video-map` (records only), fast-forwarded into `main` under the owner's standing rule
- Baseline: `3022a4e` (main, package 1.43.0); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.43.0)
- Scope: the owner supplied the Plugin Creator readback of the hosted plugin (`hosted-readback-1.43.0.json`, SHA-256 `b7f2bc34...`). `scripts/check_hosted_readback.py` against `config/install-sources.json` at `f15fd5e`: `full_byte_parity`, 918 of 918 paths, sizes and hashes; every readback hash also equals the tag v1.43.0 git blob. No unreadable files. The owner had saved 1.43.0 before the readback; Plugin Creator did not save again because a new save would need 1.43.1
- Shared package changed: no

Verification:

- readback comparison: PASS (`full_byte_parity`) ([record](../verification/hosted-release-1.43.0.json)); canonical validator and `scripts/check_all.sh`: PASS

Cross-host state:

- GitHub: `main` and v1.43.0 synchronized (see CC-20261009-01)
- ChatGPT Work: synchronized. Plugin `plugins_6ab8e226cbd48191b661cb2ea24d0351`, release `pluginrel_6ac87a565d7481918b6a679d5bbdb157`, readback 2026-10-09 06:43 UTC; active-client behavior not_run
- Codex: not_run

## CC-20261009-04

- Origin: cloud-code
- Branch: `cloud-code/CC-20261009-04-hyperframes-engine`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `856601b` (main, package 1.43.0, after the hosted readback record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.44.0)
- Package version: 1.43.0 -> 1.44.0
- Scope: the owner asked on 2026-10-09 for HyperFrames (hyperframes.dev, its Studio app and skills) as the main support for motion graphics and chose 1a (an optional engine in Codex or local shell hosts, installed with a pinned command, its skills not copied into the package) and 2a (the HeyGen catalog only when the user asks and has a HeyGen account). New `hyperframes-workflow/references/hyperframes-engine.md`, checked against heygen-com/hyperframes `3aa68869f7d4cec8b37cdfcb9cd539389b63abed` (CLI 0.8.143, Apache-2.0): when to offer it, installing it, who decides what (Studio keeps intake, approvals, copy, storyboard and review; HyperFrames composes and renders), assets and the HeyGen catalog, evidence. Linked from the Motion Graphics skill and its code-based workflow; capability card entry `hyperframes_engine`; knowledge-map row; a Studio test keeps the engine optional and area `8` engine-neutral. The owner's report of a perfume-shop reel made in HyperFrames Studio is recorded as an owner report about HyperFrames, not a test of this route. Welcome and menus unchanged
- Shared package changed: yes; 11 changed, 1 added, 0 removed ([scope](../verification/scope-1.44.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 198 passing of 202 (4 opt-in browser tests; 67 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, GEPA pilot 8, asset 23, captions 14: PASS ([record](../verification/release-1.44.0.json))
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run; no HyperFrames install or render was run through Studio

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `bfe9dc8`; release workflow 37899173624, checks 37899173622, 37899176172 and 37899178932, release-notes refresh 37899173549: success; [v1.44.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.44.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (919 of 919), all 37 skill frontmatters parse ([record](../verification/github-publication-1.44.0.json))
- ChatGPT Work: pending (hosted update on owner instruction only; 1.43.0 is the saved release)
- Codex: not_run

## CC-20261009-05

- Origin: cloud-code
- Branch: `cloud-code/CC-20261009-05-environment-check`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `8f3598d` (main, package 1.44.0, after its publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.45.0)
- Package version: 1.44.0 -> 1.45.0
- Scope: the owner asked on 2026-10-09 that installing Studio checks the environment for everything its skills use (HyperFrames, Remotion, FFmpeg, Chrome and the rest), whether it is installed and current, tells the user how to install what is missing, and that one command runs the same check. New `workflow-orchestrator/assets/environment-check/` (`check_environment.py`, standard library only; `tools.json` with minimums, newest versions known on 2026-10-09, registry sources and install steps per system; README) reporting tool statuses, capability readiness from the capability card and grouped install steps; it installs nothing. The orchestrator answers environment requests with it before any welcome; its capabilities reference runs it before the first coded render when nothing shows the tools work; the HyperFrames engine reference and the knowledge map link it; `CODEX_INSTALL.md` and `CHATGPT_INSTALL.md` run it after the save. Validator rule `ENVIRONMENT_CHECK` with a Studio test; `tests/environment_check_test.py` (9) in `scripts/check_all.sh`. Welcome and menus unchanged
- Shared package changed: yes; 11 changed, 4 added, 0 removed ([scope](../verification/scope-1.45.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 199 passing of 203 (4 opt-in browser tests; 67 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, GEPA pilot 8, asset 23, captions 14, environment check 9: PASS ([record](../verification/release-1.45.0.json))
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run; the check ran on Linux only

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `2037433`; release workflow 37903762129, checks 37903762077, 37903764562 and 37903767039, release-notes refresh 37903762019: success; [v1.45.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.45.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (923 of 923), all 37 skill frontmatters parse, the environment check runs from the unpacked ZIP ([record](../verification/github-publication-1.45.0.json))
- ChatGPT Work: pending (hosted update on owner instruction only; 1.43.0 is the saved release)
- Codex: not_run

## CC-20261009-06

- Origin: cloud-code
- Branch: `cloud-code/CC-20261009-06-commercial-acceptance`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `32736d1` (main, package 1.45.0, after its publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.46.0)
- Package version: 1.45.0 -> 1.46.0
- Scope: the owner supplied a comparison (PDF and Markdown, 2026-10-09) of a 20 s 1080 x 1920 shop reel with a HyperFrames Studio film and asked for better creative decisions and acceptance in the existing workflow. Traced where the false acceptance came from: the frame review measured only contract copy, the critique reported a frame-checked score of 100 on a video whose word was cut by a mask (pixels look tidy), a contract-only score had no verdict boundary, and nothing audited compositions outside a contract. Changes: `references/commercial-motion.md` (argument before look, key-frame proof, carrier transitions, four verdicts, failure-to-correction table); contract `strategy` and scene `argues`, `assets[].background`, checked by `check-score.mjs` in both starters; `text-audit.mjs` and `text-audit.browser.js` (every visible word, clipping ancestors, holds, transitional cuts, no silent exemptions, `data-text-clip-ok` exceptions, phone-scale sheet), injected into `review-frames.mjs`; critique rules (repeated wipes, photo background, empty first frame in feed films, still stretches four times a second with drift counted as still), `score_scope`, `verdicts`, `pacing`, key frames at full size and phone scale; `acceptance.py` (A technical, B fidelity, C composition with a person's key-frame judgement, D temporal with a recorded viewing); QA record, motion craft, contract, HyperFrames engine reference, SKILL method and guardrail, capability card (`motion_text_audit`, `motion_acceptance`), knowledge map; fixtures and tests (10 Python, 1 contract, 2 browser). Welcome and menus unchanged
- Shared package changed: yes; 19 changed, 13 added, 0 removed ([scope](../verification/scope-1.46.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 200 passing of 206 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, GEPA pilot 8, asset 23, captions 14, environment check 9, motion acceptance 10: PASS ([record](../verification/release-1.46.0.json))
- before/after on the reel's failure cases ([record](../verification/perfua-regression-1.46.0.json)); a 20 s 1080 x 1920 proof rendered and accepted through the whole chain: technical PASS, composition FAIL by Claude's judgement of the key frames, fidelity and temporal NOT VERIFIED
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run; the original reel was not supplied and not re-run; HyperFrames not run

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `9b42385`; release workflow 37913665900 succeeded on attempt 2 (attempt 1 cancelled after 25 minutes in the dependency-install step, before any test ran; re-run once), checks 37913665897, 37913668311 and 37913670804 and release-notes refresh 37913666028: success; [v1.46.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.46.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (936 of 936), all 37 skill frontmatters parse, the text audit runs from the unpacked ZIP ([record](../verification/github-publication-1.46.0.json))
- ChatGPT Work: pending (hosted update on owner instruction only; 1.43.0 is the saved release)
- Codex: not_run

## CC-20261009-07

- Origin: cloud-code, from the owner's instruction of 2026-10-09
- Branch: `cloud-code/CC-20261009-06-commercial-acceptance` (repository-only follow-up), fast-forwarded into `main` under the owner's standing rule
- Baseline: `627760f` (main, package 1.46.0, after its publication record); full SHA in the commit trailer
- Result: a repository-only commit; the package is unchanged (1.46.0)
- Scope: the owner said the session must not ask whether to update the hosted ChatGPT plugin, because he performs that update himself. AGENTS.md records it: after a release, report the hosted state as pending and give the ready update prompt; compare a returned readback with `scripts/check_hosted_readback.py`
- Shared package changed: no

Verification:

- canonical validator and `scripts/check_all.sh`: PASS; package files unchanged

Cross-host state:

- GitHub: this commit on `main`; the package release stays v1.46.0
- ChatGPT Work: pending (owner updates to 1.46.0 in Plugin Creator; 1.43.0 is the saved release)
- Codex: not_run

## CC-20261009-08

- Origin: cloud-code, from the owner's answers of 2026-10-09 ("1 nie 2 nie")
- Branch: `cloud-code/CC-20261009-06-commercial-acceptance` (records only), fast-forwarded into `main` under the owner's standing rule
- Baseline: `7566cc6` (main, package 1.46.0); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.46.0)
- Scope: (1) the original 20 s reel and its composition will not be supplied, so the reel regression stays on the original fixtures of `verification/perfua-regression-1.46.0.json` and the reel itself stays not_verified; (2) the environment check keeps showing install steps only and does not offer to run an installation
- Shared package changed: no

Cross-host state:

- GitHub: this commit on `main`; the package release stays v1.46.0
- ChatGPT Work: pending (owner updates to 1.46.0 in Plugin Creator)
- Codex: not_run

## CC-20261009-09

- Origin: cloud-code, from the owner's report of 2026-10-09
- Branch: `cloud-code/CC-20261009-09-content-routing`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `da78110` (main, package 1.46.0, after CC-20261009-08); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.47.0)
- Package version: 1.46.0 -> 1.47.0
- Scope: in a new ChatGPT thread the owner sent a screenshot of a Facebook post (a truck configurator; ChatGPT moving parts during a PNG cut-out) with the Studio link and got the welcome. Cause: the entry rule sent "Studio-only invocation ... or unclear intent" to the welcome without saying that an attachment or pasted text is content, and the description told every invocation to return the welcome. Now the entry defines a Studio-only invocation as the name or link alone; an invocation with text, a screenshot, an image, a file or pasted material (or right after an unanswered user message) is read first, its intent inferred and routed to the owner, with one numbered line for other readings and at most one targeted question; never the welcome. The description says so; `startup-and-creative-menus.md` has an "Invocation with content" section with the owner's case as the example; `validate-learning-mode.mjs` pins the rule; a Studio test; evaluation case LM25 (202 planned cases). Welcome assets, embedded excerpts and menu text unchanged
- Shared package changed: yes; 11 changed, 0 added, 0 removed ([scope](../verification/scope-1.47.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: Node 201 passing of 207 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, GEPA pilot 8, asset 23, captions 14, environment check 9, motion acceptance 10: PASS ([record](../verification/release-1.47.0.json))
- legacy suite: matches `tests/legacy-baseline.json`; host behavior: not_run (startup with content not tested in ChatGPT)

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `a7cbfc0`; release workflow 37924964208, checks 37924964487, 37924967988 and 37924972219, release-notes refresh 37924964353: success; [v1.47.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.47.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (936 of 936), all 37 skill frontmatters parse ([record](../verification/github-publication-1.47.0.json))
- ChatGPT Work: pending (owner updates to 1.47.0 in Plugin Creator; 1.43.0 is the saved release)
- Codex: not_run

## CC-20261009-10

- Origin: cloud-code
- Branch: `cloud-code/CC-20261009-10-hosts-and-claude`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `a1c4187` (main, package 1.47.0, after its publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.48.0)
- Package version: 1.47.0 -> 1.48.0
- Scope: the owner asked on 2026-10-09 for a fixed set of tools, checked by the validator and split by host (ordinary ChatGPT, ChatGPT Work, Codex, Claude), and for a correct installation path for Claude. The environment check's `tools.json` now has `hosts` (chatgpt, chatgpt_work, codex, claude_code, claude_apps, each with its capability-card profile, install guide and detection trace) and `host_statuses` (observed, check, install, per_project, not_supported); every tool has a status per host, `observed` with the owner's evidence and `not_supported` with the reason. `check_environment.py` gains `--host` (detected from `CLAUDECODE=1`, a `CODEX_` variable, `/mnt/user-data`, `/mnt/data`) and `--matrix [--markdown|--json]`; on a named host an unsupported tool is `not_on_this_host`. The README table is generated and tested. `validate-studio.mjs` requires the five hosts, the five statuses, a status for every tool on every host, evidence or reasons, and the README matrix, and checks that `.claude-plugin/plugin.json` carries the package identity and that no top-level `bin/` exists. New package file `.claude-plugin/plugin.json`; repository-level `.claude-plugin/marketplace.json` (marketplace `framecore-works`, relative source), `CLAUDE_INSTALL.md`, INSTALL and README rows, AGENTS release steps and install-doc list, `tests/test_claude_plugin.py` (6) in `scripts/check_all.sh`. Claude Code facts were read from code.claude.com and claude.com docs on 2026-10-09 (manifest, marketplace, install, CLI, skills, plugins overview and platform support)
- Shared package changed: yes; 11 changed, 1 added, 0 removed ([scope](../verification/scope-1.48.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS for plugin and marketplace
- `scripts/check_all.sh`: Node 201 passing of 207 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, Claude plugin 6, GEPA pilot 8, asset 23, captions 14, environment check 13, motion acceptance 10: PASS ([record](../verification/release-1.48.0.json))
- Claude Code 2.1.295 headless, agent-run: install listed 37 skills; English and Polish welcomes byte-identical to the assets; a pasted question answered without the welcome ([record](../verification/claude-code-startup-1.48.0.json))
- legacy suite: matches `tests/legacy-baseline.json`

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `1aa99e4`; release workflow 37938228957, checks 37938228968, 37938232790 and 37938236302, release-notes refresh 37938228924: success; [v1.48.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.48.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (937 of 937), all 37 skill frontmatters parse ([record](../verification/github-publication-1.48.0.json))
- ChatGPT Work: pending (owner updates to 1.48.0 in Plugin Creator; 1.43.0 is the saved release)
- Codex: not_run
- Claude Code: installed from the GitHub tag v1.48.0 in an isolated configuration (37 skills; Polish welcome byte-identical), agent-run; Claude apps: not_run

## CC-20261009-11

- Origin: cloud-code
- Branch: `cloud-code/CC-20261009-11-required-tools`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `679eecf` (main, package 1.48.0, after its publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.49.0)
- Package version: 1.48.0 -> 1.49.0
- Scope: the owner decided on 2026-10-09 that the required and optional tools are one required set, checked as the final step of installation. `tools.json` drops `optional`, adds imageio-ffmpeg, matplotlib, Manim, the Remotion 3D example and the motion toolkit (17 tools), and a Studio workspace (`~/.framecore-studio/workspace`, `FRAMECORE_STUDIO_WORKSPACE`) where the four starters are installed with `npm ci`. `check_environment.py` checks workspace packages against the starters' pinned versions (`wrong_version`), reports a missing HyperFrames as missing, prints workspace commands with the real plugin path, and adds `--final` (pass, fail, limited, unknown_host; exit 0, 1, 3, 2) and `--workspace`. The validator rejects `optional`, accepts `used_by` and checks each workspace starter's package.json and lockfile. CODEX_INSTALL.md and CHATGPT_INSTALL.md gain "5. Final check of the required tools" (providers move to section 6); CLAUDE_INSTALL.md step 4.3 is the final check; the HyperFrames engine reference says it is installed with Studio. The owner's earlier answer that the check only shows install steps stands: it installs nothing
- Shared package changed: yes; 13 changed, 0 added, 0 removed ([scope](../verification/scope-1.49.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: Node 201 passing of 207 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, Claude plugin 6, GEPA pilot 8, asset 23, captions 14, environment check 14, motion acceptance 10: PASS ([record](../verification/release-1.49.0.json))
- final check on a fully provisioned container: PASS, 17 of 17 ([record](../verification/required-tools-final-check-1.49.0.json))
- legacy suite: matches `tests/legacy-baseline.json`

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `56ea984`; release workflow 37955016470, checks 37955016538, 37955019635 and 37955023474, release-notes refresh 37955016312: success; [v1.49.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.49.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (937 of 937), all 37 skill frontmatters parse, the final check from the unpacked ZIP passes ([record](../verification/github-publication-1.49.0.json))
- ChatGPT Work: pending (owner updates to 1.49.0 in Plugin Creator; 1.43.0 is the saved release)
- Codex: not_run
- Claude Code: not rerun for 1.49.0 (1.48.0 tested)

## CC-20261009-12

- Origin: cloud-code
- Branch: `cloud-code/CC-20261009-12-update-check`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `73a7df2` (main, package 1.49.0, after its publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.50.0)
- Package version: 1.49.0 -> 1.50.0
- Scope: the owner asked on 2026-10-09 that updating the plugin also checks that every required tool is installed and current. `check_environment.py --update` is the final check plus an online newest-version lookup (snapshot when offline); verdict `pass_with_updates` (exit 4) lists newer versions with commands without forcing them; a workspace starter whose lockfile differs from the plugin's is `wrong_version`. Workspace commands replace an existing folder and name the actual workspace. CODEX_UPDATE.md, CHATGPT_UPDATE.md, UPDATE.md and the CLAUDE_INSTALL.md update section end with the update check; `tests/test_claude_plugin.py` checks all install and update guides for `--final` and `--update`; the capabilities reference mentions both checks
- Shared package changed: yes; 12 changed, 0 added, 0 removed ([scope](../verification/scope-1.50.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: Node 201 passing of 207 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, Claude plugin and guides 7, GEPA pilot 8, asset 23, captions 14, environment check 16, motion acceptance 10: PASS ([record](../verification/release-1.50.0.json))
- update check in the provisioned container: `pass_with_updates`; `fail` with a stale starter
- legacy suite: matches `tests/legacy-baseline.json`

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `62a72e0`; release workflow 37960061303, checks 37960061305, 37960066904 and 37960069167, release-notes refresh 37960061468: success; [v1.50.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.50.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (937 of 937), all 37 skill frontmatters parse, the update check from the unpacked ZIP runs ([record](../verification/github-publication-1.50.0.json))
- ChatGPT Work: pending (owner updates to 1.50.0 in Plugin Creator; 1.43.0 is the saved release)
- Codex: not_run
- Claude Code: not rerun for 1.50.0

## CC-20261010-01

- Origin: cloud-code, from the owner's ChatGPT Work readback
- Branch: `main` (records only), fast-forward under the owner's standing rule
- Baseline: `9832e46` (main, package 1.50.0, after its publication record); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.50.0)
- Scope: the owner updated the hosted plugin to 1.50.0 in Plugin Creator and supplied its readback (`hosted-readback-1.50.0.json`, SHA-256 `29591e69...`). `scripts/check_hosted_readback.py` against `config/install-sources.json` at `62a72e0`: `full_byte_parity`, 937 of 937 paths, sizes and hashes; every readback hash also equals the tag v1.50.0 git blob. No unreadable or extra paths
- Shared package changed: no

Verification:

- readback comparison: PASS (`full_byte_parity`) ([record](../verification/hosted-release-1.50.0.json)); canonical validator and `scripts/check_all.sh`: PASS

Cross-host state:

- GitHub: `main` and v1.50.0 synchronized (see CC-20261009-12)
- ChatGPT Work: synchronized. Plugin `plugins_6ab8e226cbd48191b661cb2ea24d0351`, release `pluginrel_6ac93031429c8191ac77687931036628`, readback 2026-10-10; active-client behavior not_run
- Codex: not_run
- Claude Code: not rerun for 1.50.0

## CC-20261010-02

- Origin: cloud-code, from the owner's ChatGPT Work test of 1.50.0
- Branch: `cloud-code/CC-20261010-02-welcome-motion`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `3357085` (main, package 1.50.0, after the hosted readback record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.51.0)
- Package version: 1.50.0 -> 1.51.0
- Scope: the owner reported on 2026-10-10 that in ChatGPT Work the bare invocation gave the complete Polish welcome and a graphic sent with the name was handled as a task (both PASS_REPORTED, [report](../verification/host-report-2026-10-10-startup-1.50.0.json)), and that the welcome says nothing about motion design. The video bullet now reads "Video, motion design and storytelling" / "Wideo, motion designie i opowiadaniu historii" and lists animated graphics and typography. Both welcome assets, their `SKILL.md` excerpts and the protected welcome hashes in `validate-learning-mode.mjs` changed together; six bullets, structure, numbered options and later menus are unchanged. This supersedes the earlier "welcome unchanged" instruction for this one bullet, at the owner's request
- Shared package changed: yes; 10 changed, 0 added, 0 removed ([scope](../verification/scope-1.51.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: Node 201 passing of 207 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, Claude plugin and guides 7, GEPA pilot 8, asset 23, captions 14, environment check 16, motion acceptance 10: PASS ([record](../verification/release-1.51.0.json))
- legacy suite: matches `tests/legacy-baseline.json`

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `6f2bd1a`; release workflow 38031316640, checks 38031316628, 38031318181 and 38031319325, release-notes refresh 38031316649: success; [v1.51.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.51.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (937 of 937), all 37 skill frontmatters parse ([record](../verification/github-publication-1.51.0.json))
- ChatGPT Work: pending (owner updates to 1.51.0 in Plugin Creator; 1.50.0 is the saved release, synchronized)
- Codex: not_run
- Claude Code: not rerun for 1.51.0
