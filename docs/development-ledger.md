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

## CC-20261010-03

- Origin: cloud-code, from the owner's correction
- Branch: `main` (records only), fast-forward under the owner's standing rule
- Baseline: `a7de875` (main, package 1.51.0, after its publication record); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.51.0)
- Scope: the owner noted on 2026-10-10 that Plugin Creator updates the hosted plugin from the repository files, not from a release ZIP. AGENTS.md now says the hosted-update prompt follows `CHATGPT_UPDATE.md` (source commit, `config/install-sources.json`, readback fields) and that the ZIP SHA-256 is reference only
- Shared package changed: no

Verification:

- canonical validator and `scripts/check_all.sh`: PASS

Cross-host state:

- GitHub: `main` and v1.51.0 synchronized (see CC-20261010-02)
- ChatGPT Work: pending (owner updates to 1.51.0 in Plugin Creator; 1.50.0 is the saved release, synchronized)
- Codex: not_run

## CC-20261010-05

- Origin: cloud-code, from the owner's ChatGPT Work readback
- Branch: `main` (records only), fast-forward under the owner's standing rule
- Baseline: `941cbf2` (main, package 1.51.0); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.51.0)
- Scope: the owner updated the hosted plugin to 1.51.0 in Plugin Creator from the repository at `6f2bd1a` and supplied its readback (`hosted-readback-1.51.0.json`, SHA-256 `10924def...`). `scripts/check_hosted_readback.py` against `config/install-sources.json` at v1.51.0: `full_byte_parity`, 937 of 937 paths, sizes and hashes; every hash equals the tag v1.51.0 git blob; no unreadable or extra paths. The update check there gave `limited` (exit 3). Plugin Creator's own test run failed one environment-check test because HyperFrames was detected; that is a false positive of the detection, fixed in CC-20261010-04
- Shared package changed: no

Verification:

- readback comparison: PASS (`full_byte_parity`) ([record](../verification/hosted-release-1.51.0.json)); canonical validator and `scripts/check_all.sh`: PASS

Cross-host state:

- GitHub: `main` and v1.51.0 synchronized (see CC-20261010-02)
- ChatGPT Work: synchronized. Plugin `plugins_6ab8e226cbd48191b661cb2ea24d0351`, release `pluginrel_6ac9ec10cdfc819180bd853fa5ecefaa`, readback 2026-10-10; the new welcome in the client not_run
- Codex: not_run

## CC-20261010-04

- Origin: cloud-code, from the owner's ChatGPT Work update to 1.51.0
- Branch: `cloud-code/CC-20261010-04-hyperframes-detect`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `aea24a8` (main, package 1.51.0, after the hosted readback record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.52.0)
- Package version: 1.51.0 -> 1.52.0
- Scope: in ChatGPT Work's sandbox the update check reported HyperFrames skills, and Plugin Creator's test run failed one environment-check test that expects HyperFrames to be absent. Cause: the check matched skill folders named `hyperframes*`, so Studio's own `hyperframes-workflow` counted as HyperFrames (reproduced in this container: `ok` for that skill alone). The check now skips Studio's own skill names and folders inside the Studio plugin; a new test covers Studio's skill alone (`missing`) and the real `hyperframes` skill (`ok`); the named-host test runs with a temporary HOME, CODEX_HOME and XDG_CONFIG_HOME. Which test failed in Plugin Creator's sandbox was not reported; inference: the named-host test, the one that read the real home
- Shared package changed: yes; 9 changed, 0 added, 0 removed ([scope](../verification/scope-1.52.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: Node 201 passing of 207 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, Claude plugin and guides 7, GEPA pilot 8, asset 23, captions 14, environment check 17, motion acceptance 10: PASS ([record](../verification/release-1.52.0.json))
- legacy suite: matches `tests/legacy-baseline.json`

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `139bf5b`; release workflow 38037299317, checks 38037299299, 38037300877 and 38037302331, release-notes refresh 38037299295: success; [v1.52.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.52.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (937 of 937), all 37 skill frontmatters parse ([record](../verification/github-publication-1.52.0.json))
- ChatGPT Work: pending (owner updates to 1.52.0 in Plugin Creator; 1.51.0 is the saved release, synchronized)
- Codex: not_run
- Claude Code: not rerun for 1.52.0

## CC-20261010-06

- Origin: cloud-code, from the owner's ChatGPT Work readback
- Branch: `main` (records only), fast-forward under the owner's standing rule
- Baseline: `00913ab` (main, package 1.52.0, after its publication record); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.52.0)
- Scope: the owner updated the hosted plugin to 1.52.0 in Plugin Creator from the repository at `139bf5b` and supplied its readback (`hosted-readback-1.52.0.json`, SHA-256 `0d40a785...`). `scripts/check_hosted_readback.py` against `config/install-sources.json` at v1.52.0: `full_byte_parity`, 937 of 937 paths, sizes and hashes; every hash equals the tag v1.52.0 git blob; no unreadable or extra paths. Update check there: `limited` (exit 3). HyperFrames reported `ok` from what Plugin Creator called a genuine HyperFrames plugin in the sandbox; the detected path was not reported, so whether HyperFrames is really usable there is Unknown. Plugin Creator's package test run: 310 passed, 10 skipped, 0 failed, including all 17 environment-check tests
- Shared package changed: no

Verification:

- readback comparison: PASS (`full_byte_parity`) ([record](../verification/hosted-release-1.52.0.json)); canonical validator and `scripts/check_all.sh`: PASS

Cross-host state:

- GitHub: `main` and v1.52.0 synchronized (see CC-20261010-04)
- ChatGPT Work: synchronized. Plugin `plugins_6ab8e226cbd48191b661cb2ea24d0351`, release `pluginrel_6aca03c7f9fc8191b2739b27ad44ab41`, readback 2026-10-10; the 1.51.0 welcome in the client not_run
- Codex: not_run

## CC-20261010-07

- Origin: cloud-code, from the owner's decisions of 2026-10-10
- Branch: `main` (records only), fast-forward under the owner's standing rule
- Baseline: `ed69076` (main, package 1.52.0); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.52.0)
- Scope: the owner closed the current ChatGPT Work test round: the sandbox cannot run every tool, so the full required set (HyperFrames CLI included) is a Codex or Claude Code matter, and `limited` in Work is accepted as correct. Owner decision 1a: the environment check should report a tool that the host marks `not_supported` as `not_on_this_host` even when its files are found (today HyperFrames skills found in Work's sandbox give `ok`), with a note that the files are present but the engine does not run there; this is deferred to the next release that changes the shared package, without a separate hosted update. The welcome with motion design (1.51.0) stays not_run in the client; a Codex test is not scheduled
- Shared package changed: no

Deferred to the next package release:

- `check_environment.py`: on a host where a tool is `not_supported`, report `not_on_this_host` whatever the detection found, and keep the found paths in the note; add a test

Cross-host state:

- GitHub: `main` and v1.52.0 synchronized
- ChatGPT Work: synchronized at 1.52.0 (release `pluginrel_6aca03c7f9fc8191b2739b27ad44ab41`)
- Codex: not_run

## CC-20261010-08

- Origin: cloud-code, from the owner's request of 2026-10-10
- Branch: `cloud-code/CC-20261010-08-skill-finder`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `e06a7a5` (main, package 1.52.0, after the owner decisions record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.53.0)
- Package version: 1.52.0 -> 1.53.0
- Scope: the owner asked to adapt Vercel's skill finder (`find-skills`, announced with the open skills ecosystem on 2026-01-20) as a separate welcome option: describe what a skill should do, get Studio's own matching skill first, and in Codex and Claude Code the open skills.sh catalog; search and describe, install only on an explicit request there; the whole catalog, no author allowlist. The welcome gains option 3 ("Looking for a specific skill?" / "Szukasz konkretnego skilla (umiejętności)?") and the reply line "1, 2 or 3"; the six bullets and later menus are unchanged; a `3` answering a pre-1.53.0 two-option welcome still asks for clarification. New: `references/skill-finder.md`, `assets/skill-finder/find_skills.py` (search, three security audits, verdicts listed/caution/unchecked/blocked, `--describe`; install commands with `DO_NOT_TRACK=1`, never `-y`; unsafe catalog names rejected), capability `skill_search`, provenance in `integrations/skill-finder/` (MIT, commit `13e4063`, blob hashes; the upstream skill is not vendored, so hosts do not discover it), evaluation cases LM26 and LM27. Deferred decision 1a: a tool marked `not_supported` for the host is `not_on_this_host` even when its files are found. The orchestrator entry was compacted by four sentences to stay within its 32,000-byte budget
- Shared package changed: yes; 18 changed, 6 added, 0 removed ([scope](../verification/scope-1.53.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: Node 201 passing of 207 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, Claude plugin and guides 7, GEPA pilot 8, asset 23, captions 14, environment check 18, motion acceptance 10, skill finder 7: PASS ([record](../verification/release-1.53.0.json))
- live catalog reads from the container; Claude Code 2.1.296 headless, agent-run: welcomes byte-identical, option 3 flow and catalog search as specified, nothing installed ([record](../verification/claude-code-skill-finder-1.53.0.json))
- legacy suite: matches `tests/legacy-baseline.json`

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `b8c0ee0`; release workflow 38060791402, checks 38060791405, 38060793430 and 38060795520, release-notes refresh 38060791403: success; [v1.53.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.53.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (943 of 943), all 37 skill frontmatters parse ([record](../verification/github-publication-1.53.0.json))
- ChatGPT Work: pending (owner updates to 1.53.0 in Plugin Creator; 1.52.0 is the saved release, synchronized)
- Codex: not_run
- Claude Code: agent-run headless tests PASS (not the owner's client)

## CC-20261010-09

- Origin: cloud-code, from the owner's request of 2026-10-10
- Branch: `cloud-code/CC-20261010-09-animate-engine`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `de64d58` (main, package 1.53.0, after its publication record); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.54.0)
- Package version: 1.53.0 -> 1.54.0
- Scope: the owner asked to add the skills of https://github.com/cth9191/animate to the motion graphics module. The upstream skill folder (version 0.4.0, MIT, commit `7e5eb56`, 107 files: story grammar, craft rules, intake, kit, tools, seven styles with samples and demos, templates, an example) is bundled byte-identical as `skills/hyperframes-workflow/assets/animate-engine/`, with `SKILL.md` renamed `ENGINE.md` so no host lists a second skill; Studio adds `package.json` and `package-lock.json` pinning Playwright 1.56.1 (the version whose Chromium could be tested here; 1.64.0 is newest). Not bundled: the repository README, `docs/*.png` (5.8 MB) and the plugin wrapper. New reference `references/animate-engine.md` (when to choose it, where it runs, how Studio's approvals, research gate, four verdicts, sound and provider rules apply, method files usable on every host, upstream's honesty about proven formats and styles); links from the motion SKILL.md and runtime selection; capability `animate_render`; required tool `animate_engine` (fifth workspace starter, `npm ci` and `npx playwright install chromium`; not supported in chat hosts), so the required set has 18 tools; provenance in `integrations/animate/` with every file's Git blob hash; test `animate_engine_test.py`. The plugin ZIP grows from about 10 MB to about 13 MB (1057 files)
- Shared package changed: yes; 12 changed, 114 added, 0 removed ([scope](../verification/scope-1.54.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: Node 201 passing of 207 (6 opt-in browser tests; 70 passing in the browser run), installer 13, identity 4, benchmark script 5, host smoke 6, hosted readback 6, Claude plugin and guides 7, GEPA pilot 8, asset 23, captions 14, environment check 18, motion acceptance 10, skill finder 7, Animate engine 4: PASS ([record](../verification/release-1.54.0.json))
- the engine in this container: riso demo exported and passed its review; gallery of seven styles; math demo from an `npm ci` workspace; final check 18 of 18 ([record](../verification/required-tools-final-check-1.54.0.json))
- legacy suite: matches `tests/legacy-baseline.json`

Cross-host state:

- GitHub: synchronized. `main` fast-forwarded to `62e8689`; release workflow 38064652836, checks 38064652846, 38064654420 and 38064656432, release-notes refresh 38064652786: success; [v1.54.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.54.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1057 of 1057), all 37 skill frontmatters parse ([record](../verification/github-publication-1.54.0.json))
- ChatGPT Work: pending (owner updates to 1.54.0 in Plugin Creator; 1.52.0 is the saved release, synchronized; 1.53.0 was not saved)
- Codex: not_run
- Claude Code: not rerun for 1.54.0 (1.53.0 agent-run)

## CC-20261010-10

- Origin: cloud-code, from the owner's ChatGPT Work readback
- Branch: `main` (records only), fast-forward under the owner's standing rule
- Baseline: `09236b9` (main, package 1.54.0, after its publication record); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.54.0)
- Scope: the owner updated the hosted plugin to 1.54.0 in Plugin Creator from the repository at `62e8689` and supplied its readback (`hosted-readback-1.54.0.json`, SHA-256 `23906a39...`). `scripts/check_hosted_readback.py` against `config/install-sources.json` at v1.54.0: `mismatch`; 1055 of 1057 paths, sizes and hashes match (also the tag's git blobs), no missing, extra or unreadable paths. `skills/tool-routing-cost/SKILL.md` is 7486 bytes saved against 6714 in the source, `skills/tool-routing-cost/references/provider-setup.md` 10192 against 7131. Neither file changed in the repository since 1.41.0 and the 1.52.0 readback had both identical, so the change was written during this save; its content and origin are Unknown until the owner inspects it. The PNG and JavaScript files of the Animate engine were saved byte for byte
- Shared package changed: no

Verification:

- readback comparison: `mismatch` (2 files) ([record](../verification/hosted-release-1.54.0.json)); canonical validator and `scripts/check_all.sh`: PASS

Cross-host state:

- GitHub: `main` and v1.54.0 synchronized (see CC-20261010-09)
- ChatGPT Work: not synchronized; release `pluginrel_6aca6426a5ac8191bd2458f5d3718152` saved at 1.54.0 with two files differing from the source; resolution pending
- Codex: not_run

## CC-20261010-11

- Origin: cloud-code, from the owner's decision of 2026-10-10
- Branch: `main` (records only), fast-forward under the owner's standing rule
- Baseline: `472c2e9` (main, package 1.54.0); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.54.0)
- Scope: the owner stopped hosted readback verification: no readback, no diff of the two differing `tool-routing-cost` files, no hosted-release comparison. After a release Studio's maintainers give only the short Plugin Creator update prompt; the owner updates and tests the plugin himself. AGENTS.md records the decision; RELEASE_STATUS marks ChatGPT Work `not_tracked`
- Shared package changed: no

Cross-host state:

- GitHub: `main` and v1.54.0 synchronized
- ChatGPT Work: not_tracked (owner decision); last readback 1.54.0 with two files differing, left as they are
- Codex: not_run

## CC-20261010-12

- Origin: cloud-code, from the owner's request for a full re-analysis and improvement plan
- Branch: `main` (records only), fast-forward under the owner's standing rule
- Baseline: `cb5eb72` (main, package 1.54.0); full SHA in the commit trailer
- Result: a records-only commit; the package is unchanged (1.54.0)
- Scope: six independent read-only reviews of package 1.54.0 (entry and orchestration, static and visual, video and story, motion graphics with renders and audio measurements, copy/marketing/audio/research/delivery, infrastructure). Their findings are combined in [the improvement plan](improvement-plan-2026-10.md): diagnosis with evidence, six phases with files and effort, owner decisions
- Shared package changed: no

Cross-host state:

- GitHub: `main` and v1.54.0 synchronized
- ChatGPT Work: not_tracked (owner decision)
- Codex: not_run

## CC-20261010-13

- Origin: cloud-code
- Branch: `cloud-code/CC-20261010-13-phase0`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `6b65c18` (main, package 1.54.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.55.0)
- Package version: 1.54.0 -> 1.55.0
- Scope: Phase 0 of the improvement plan: the renderer stops on a word wider than its column (exit 4, text_overflow) instead of cropping it; one-letter Polish words and numbers with units are kept on one line identically in the scene engine and the renderer; critique flags empty vertical frames and acceptance blocks on any critique picture error; sound mixing about 15 times faster with identical audio; startup texts and two routing descriptions corrected; a total skill-description budget; the legacy suite retired as inert stubs; scripts/release.py, check_all.sh --fast and a version-bump guard in CI
- Shared package changed: yes; 31 changed, 0 added, 0 removed ([scope](../verification/scope-1.55.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 207 Node tests (201 passing, 6 opt-in browser tests skipped there and run separately: 70 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 14 caption, 18 environment check, 15 motion acceptance, 7 skill finder, 4 Animate engine: PASS ([record](../verification/release-1.55.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `c29edde`; workflows Check Studio sources 38086330773, Check Studio sources 38086329203, Publish the motion player to GitHub Pages 38086327115, Refresh current release notes 38086327138, Check Studio sources 38086327134, Publish verified Studio release 38086327137: success; [v1.55.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.55.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1057 of 1057) ([record](../verification/github-publication-1.55.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261010-14

- Origin: cloud-code
- Branch: `cloud-code/CC-20261010-14-phase1`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `acd36ae` (main, package 1.55.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.56.0)
- Package version: 1.55.0 -> 1.56.0
- Scope: Phase 1 of the improvement plan: an exact-copy route for static finals (a background without text plus the new compositor that sets copy, price, logo and legal lines in real fonts, PNG/JPG and print PDF with bleed, stopping on overflow or missing glyphs, checking contrast and safe areas), 18 bundled OFL fonts with Polish coverage, a Polish copy standard and checker with dated channel limits, dated channel-spec and PL/EU marketing-rule snapshots with a rules column in the claim ledger, an image probe with review previews, format and print presets, direct production, one decision after offering directions, digit groups kept together in motion text; repository: the host-eval harness and its first two runs
- Shared package changed: yes; 22 changed, 41 added, 0 removed ([scope](../verification/scope-1.56.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 207 Node tests (201 passing, 6 opt-in browser tests skipped there and run separately: 70 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 14 caption, 18 environment check, 15 motion acceptance, 7 skill finder, 4 Animate engine, 13 static render, 6 Polish copy check, 5 image probe, 6 host-eval harness: PASS ([record](../verification/release-1.56.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `bd37781`; workflows Check Studio sources 38089077489, Check Studio sources 38089075846, Refresh current release notes 38089074521, Check Studio sources 38089074474, Publish the motion player to GitHub Pages 38089074396, Publish verified Studio release 38089074438: success; [v1.56.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.56.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1098 of 1098) ([record](../verification/github-publication-1.56.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261010-15

- Origin: cloud-code
- Branch: `cloud-code/CC-20261010-15-phase2`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `1171a36` (main, package 1.56.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.57.0)
- Package version: 1.56.0 -> 1.57.0
- Scope: Phase 2 of the improvement plan, the client business layer with every rate, VAT status, term and right as user input: offers and a quote calculator, client intake and commercial Brief Contract fields, concept presentation, revision tracker and changes of scope, client handoff with a handoff letter, AI-assistance line and acceptance protocol, a brand kit read by every owner and the compositor, a client email kit, a brand voice guide, KPI and budget scenarios; pricing questions route to Brief Architect and never get unsourced market rates (host-eval Q02 finding)
- Shared package changed: yes; 17 changed, 16 added, 0 removed ([scope](../verification/scope-1.57.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 207 Node tests (201 passing, 6 opt-in browser tests skipped there and run separately: 70 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 14 caption, 18 environment check, 15 motion acceptance, 7 skill finder, 4 Animate engine, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 6 host-eval harness: PASS ([record](../verification/release-1.57.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `1698b4b`; workflows Check Studio sources 38090459304, Check Studio sources 38090457119, Refresh current release notes 38090455681, Publish verified Studio release 38090455727, Check Studio sources 38090455675: success; [v1.57.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.57.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1114 of 1114) ([record](../verification/github-publication-1.57.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261010-16

- Origin: cloud-code
- Branch: `cloud-code/CC-20261010-16-phase3`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `784432c` (main, package 1.57.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.58.0)
- Package version: 1.57.0 -> 1.58.0
- Scope: Phase 3 of the improvement plan, first part: contract-declared fonts used by both the player and the Python renderer (1.5.0) with browser weight matching, font embedding for local previews and the bundled fonts on the published player; four commercial motion styles with bundled fonts and music palettes; tokens.contentScale for fuller vertical frames in every engine copy and the renderer
- Shared package changed: yes; 22 changed, 2 added, 0 removed ([scope](../verification/scope-1.58.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 209 Node tests (202 passing, 7 opt-in browser tests skipped there and run separately: 72 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 14 caption, 18 environment check, 15 motion acceptance, 6 motion fonts, 7 skill finder, 4 Animate engine, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 6 host-eval harness: PASS ([record](../verification/release-1.58.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `cd0b9bd`; workflows Check Studio sources 38092012755, Check Studio sources 38092011379, Refresh current release notes 38092009285, Publish the motion player to GitHub Pages 38092009306, Check Studio sources 38092009354, Publish verified Studio release 38092009295: success; [v1.58.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.58.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1116 of 1116) ([record](../verification/github-publication-1.58.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261011-01

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-01-scene-kinds`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `40a63d8` (main, package 1.58.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.59.0)
- Package version: 1.58.0 -> 1.59.0
- Scope: Phase 3 of the improvement plan, second part: lower-third and bar-chart scene kinds in the three scene-engine copies and the Python renderer with shared whole-pixel layouts, overflow stops for names and values, contract checks, sound cues and Remotion types; a data-and-names example in 16:9 and 9:16; contract fonts embedded in frame-review previews
- Shared package changed: yes; 20 changed, 2 added, 0 removed ([scope](../verification/scope-1.59.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 210 Node tests (203 passing, 7 opt-in browser tests skipped there and run separately: 73 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 14 caption, 18 environment check, 15 motion acceptance, 6 motion fonts, 3 motion kinds, 7 skill finder, 4 Animate engine, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 6 host-eval harness: PASS ([record](../verification/release-1.59.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `5ff4c65`; workflows Check Studio sources 38110198117, Check Studio sources 38110196274, Publish the motion player to GitHub Pages 38110194396, Refresh current release notes 38110194448, Check Studio sources 38110194403, Publish verified Studio release 38110194440: success; [v1.59.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.59.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1118 of 1118) ([record](../verification/github-publication-1.59.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261011-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-02-phase3-rest`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `71d63aa` (main, package 1.59.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.60.0)
- Package version: 1.59.0 -> 1.60.0
- Scope: Phase 3 of the improvement plan, third part: three 9:16 ad templates with 4:5 and 1:1 formats, a brand-kit and batch-variants tool for motion contracts with a contrast report, the active-word caption preset in every renderer with word timings from Caption Studio, a balanced mastering tone with a phone-speaker check and a midrange knock on impacts, and a host-first runtime map checked against the capability card, with brief types tagged by renderable scene kinds
- Shared package changed: yes; 32 changed, 8 added, 0 removed ([scope](../verification/scope-1.60.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 214 Node tests (207 passing, 7 opt-in browser tests skipped there and run separately: 77 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 15 caption, 18 environment check, 15 motion acceptance, 6 motion fonts, 3 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 6 host-eval harness: PASS ([record](../verification/release-1.60.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `db84e1e`; workflows Check Studio sources 38113162969, Check Studio sources 38113161417, Refresh current release notes 38113160365, Publish the motion player to GitHub Pages 38113160489, Check Studio sources 38113160391, Publish verified Studio release 38113160404: success; [v1.60.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.60.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1126 of 1126) ([record](../verification/github-publication-1.60.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261011-03

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-03-phase3c`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `0baa423` (main, package 1.60.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.61.0)
- Package version: 1.60.0 -> 1.61.0
- Scope: Phase 3 of the improvement plan, fourth part: photo-hero and line-chart scene kinds, word-by-word line entries with an easeOutBack spring, and persistent elements across scenes, in the three scene-engine copies and the Python renderer (render.py 1.6.0) with shared layouts, contract checks, sound cues and Remotion types; a photo-and-trend example in 9:16 and 16:9; the craft critique judges layout without the overlay and reports text wider than its column
- Shared package changed: yes; 24 changed, 1 added, 0 removed ([scope](../verification/scope-1.61.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 215 Node tests (208 passing, 7 opt-in browser tests skipped there and run separately: 78 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 15 caption, 18 environment check, 15 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 6 host-eval harness: PASS ([record](../verification/release-1.61.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `c56c5df`; workflows Check Studio sources 38115335628, Check Studio sources 38115333653, Refresh current release notes 38115332460, Publish the motion player to GitHub Pages 38115332373, Check Studio sources 38115332454, Publish verified Studio release 38115332521: success; [v1.61.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.61.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1127 of 1127) ([record](../verification/github-publication-1.61.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261011-04

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-04-phase3-end`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `171b0cb` (main, package 1.61.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.62.0)
- Package version: 1.61.0 -> 1.62.0
- Scope: Phase 3 of the improvement plan, last part: clause-aware caption cues, Polish and other-language word timing for Animate voice-overs beside the unchanged engine, twenty original library records as runnable scene-kind contracts with a builder and checks, and a Remotion glTF product turntable template with a synthetic sample model, registered in the capability card, environment check, runtime map and toolkit inventory
- Shared package changed: yes; 21 changed, 12 added, 0 removed ([scope](../verification/scope-1.62.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there and run separately: 79 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 15 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 6 host-eval harness: PASS ([record](../verification/release-1.62.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `4082c18`; workflows Check Studio sources 38126952768, Check Studio sources 38126951361, Refresh current release notes 38126949736, Publish verified Studio release 38126949774, Check Studio sources 38126949765: success; [v1.62.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.62.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1139 of 1139) ([record](../verification/github-publication-1.62.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261011-05

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-05-phase4`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `778e27e` (main, package 1.62.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.63.0)
- Package version: 1.62.0 -> 1.63.0
- Scope: Phase 4 of the improvement plan: a shared short-form timing card with a voice-over budget tool, EDL, OTIO and CSV editor handoff with step lists, client templates for ad scripts, one-pagers, music-video treatments and creator briefs, executable storyboard, shot-list, prompt-pack and clip-review tools with a Python port of the shot-plan checker, and generator dialect cards for five video models, registered in the capability card, checks and knowledge map
- Shared package changed: yes; 28 changed, 21 added, 0 removed ([scope](../verification/scope-1.63.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there and run separately: 79 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 15 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 6 host-eval harness: PASS ([record](../verification/release-1.63.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `797bcba`; workflows Check Studio sources 38130986221, Check Studio sources 38130984377, Refresh current release notes 38130982726, Publish verified Studio release 38130982730, Check Studio sources 38130982733: success; [v1.63.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.63.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1160 of 1160) ([record](../verification/github-publication-1.63.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261011-06

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-06-phase5-routing`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `520a96b` (main, package 1.63.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.64.0)
- Package version: 1.63.0 -> 1.64.0
- Scope: Phase 5 of the improvement plan, the last phase: one entry route table with Polish cues and settled collisions, a 25-case Polish routing set in the host-eval harness (23 of 25 on 1.63.0, the nine named cases unchanged on the new table), the entry at 28,963 bytes with the method catalog and GEPA procedure out of runtime references, change requests carrying eval cases, Hipson Adapter retired to a pointer, packets for print shops, voice talent and freelancers, a mascot reference and sheet, an SVG wordmark tool and a brand guide PDF tool
- Shared package changed: yes; 22 changed, 11 added, 0 removed ([scope](../verification/scope-1.64.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there and run separately: 79 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 15 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark, 5 brand guide, 9 host-eval harness: PASS ([record](../verification/release-1.64.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `5de353a`; workflows Check Studio sources 38134055178, Check Studio sources 38134053862, Refresh current release notes 38134052026, Publish verified Studio release 38134052025, Check Studio sources 38134052030: success; [v1.64.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.64.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1171 of 1171) ([record](../verification/github-publication-1.64.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261011-07

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-07-eval-limits`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `af39dd9` (main, package 1.64.0); full SHA in the commit trailer
- Result: the commit carrying this entry (repository only)
- Package version: 1.64.0 (unchanged)
- Scope: owner decision 2026-10-11 (1a, 2a): host-eval runs use the Claude plan's usage, not separate billing. `scripts/host_eval.py` drops the dollar budget and records cases, tokens and time; it runs at most 25 cases per pass and 5 for the release gate (`--max-cases` only on the owner's request); `--turn-budget-usd` stays as a per-turn runaway stop. AGENTS.md, `docs/host-evals.md` and the improvement plan say so; earlier dollar figures are labelled as Claude Code's API-price equivalents, not charges
- Shared package changed: no

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: PASS, with 12 host-eval harness tests (3 new: case limits for every suite and the gate, token totals from every model, no dollar total computed)
- no host-eval run was made for this change

Cross-host state:

- GitHub: synchronized. `main` at `6a4c492`, read back with `git ls-remote`; workflow Check Studio sources 38140207485: success
- ChatGPT Work: not affected (package unchanged)
- Codex: not_run

## CC-20261011-08

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-08-motion-review`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `ac85601` (main, package 1.64.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.65.0)
- Package version: 1.64.0 -> 1.65.0
- Scope: A development review for motion with six questions and evidence labels, a recorded listening required for the temporal verdict when there is sound, clip review marking temporal criteria unverified, ranked methods and frame arithmetic for joining generated clips, an exact-layer table for brand material in generated video, a Gemini Omni section in the generator dialects card from Google's guide, a rule to check tools before promising an MP4, and four host-eval cases (3 of 4 pass; M04 open)
- Shared package changed: yes; 18 changed, 2 added, 0 removed ([scope](../verification/scope-1.65.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there and run separately: 79 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark, 5 brand guide, 12 host-eval harness: PASS ([record](../verification/release-1.65.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `d41d537`; workflows Check Studio sources 38147965974, Check Studio sources 38147964123, Refresh current release notes 38147963000, Check Studio sources 38147962971, Publish verified Studio release 38147962952: success; [v1.65.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.65.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1173 of 1173) ([record](../verification/github-publication-1.65.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261011-09

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-09-m04-report`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `19c9646` (main, package 1.65.0); full SHA in the commit trailer
- Result: the commit carrying this entry (repository only)
- Package version: 1.65.0 (unchanged)
- Scope: the owner ran host-eval case M04 by hand in ChatGPT Work (decision 2c) and sent a screenshot: Studio stayed on the coded route and asked only for the logo, stating the assumed 9:16, 1080 x 1920, 6-second plan; recorded as PASS_REPORTED for that host ([report](../verification/host-report-2026-10-11-m04-chatgpt-work.json)). The no-code-execution finding from Claude Code stays open; the reply did not ask about sound (minor)
- Shared package changed: no

Verification:

- canonical validator and `scripts/check_all.sh --fast`: PASS
- the report is the owner's screenshot as read here; the package version was not visible in it

Cross-host state:

- GitHub: synchronized. `main` at `63e24a1`, read back with `git ls-remote`
- ChatGPT Work: not_tracked (owner decision 2026-10-10); this report is the owner's own test
- Codex: not_run

## CC-20261011-10

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-10-m04-full-path`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `63e24a1` (main, package 1.65.0); full SHA in the commit trailer
- Result: the commit carrying this entry (repository only)
- Package version: 1.65.0 (unchanged)
- Scope: the owner reworded M04 so that no logo is expected and ran it in ChatGPT Work: Studio delivered a 6-second 1080 x 1920 MP4 and the project ZIP in one turn (reported 60 FPS, no sound, frame check 90/100); recorded as PASS_REPORTED ([report](../verification/host-report-2026-10-11-m04-full-path-chatgpt-work.json)). The video was not inspected here; the reply did not state that the file was not yet watched
- Shared package changed: no

Verification:

- canonical validator and `scripts/check_all.sh --fast`: PASS
- the report is the owner's screenshot as read here

Cross-host state:

- GitHub: synchronized. `main` at `d626509`, read back with `git ls-remote`
- ChatGPT Work: not_tracked (owner decision 2026-10-10); this report is the owner's own test
- Codex: not_run

## CC-20261011-11

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-11-klos-inspection`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `d626509` (main, package 1.65.0); full SHA in the commit trailer
- Result: the commit carrying this entry (repository only)
- Package version: 1.65.0 (unchanged)
- Scope: the owner sent the MP4 from the ChatGPT Work M04 run. Probed and inspected frame by frame (no normal-speed viewing): 1080 x 1920, 60 fps, 360 frames, 6.000 s, silent; copy exact with correct diacritics; motion only until 1.33 s, then a still frame for 78 % of the runtime although the reported frame check was 90/100. Development review from frames: REVISE ([report](../verification/host-report-2026-10-11-m04-full-path-chatgpt-work.json))
- Shared package changed: no

Verification:

- canonical validator and `scripts/check_all.sh --fast`: PASS
- frame evidence only; the temporal verdict stays not verified

Cross-host state:

- GitHub: pending until the push is read back
- ChatGPT Work: not_tracked (owner decision 2026-10-10); this report is the owner's own test
- Codex: not_run

## CC-20261011-12

- Origin: cloud-code
- Branch: `cloud-code/CC-20261011-12-creative-directions`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `60f1012` (main, package 1.65.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.66.0)
- Package version: 1.65.0 -> 1.66.0
- Scope: A shared ideation method with no category lists or ready ideas (the obvious worked out and set aside, ten lenses with their moves of thought, a one-sentence mechanism, three directions differing in mechanism and source, swap, retell and fit tests, building in each medium, one worked derivation outside every test), a short fresh-directions rule inline in the graphic, visual-campaign and video-campaign owners and the orchestrator, a name rule for names that are the category motif, motion that finds its transformation before its style, the prompt library, brief index and ad templates repositioned as execution only, and an eleven-case creative host-eval set with six held-out briefs
- Shared package changed: yes; 23 changed, 1 added, 0 removed ([scope](../verification/scope-1.66.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there and run separately: 79 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark, 5 brand guide, 14 host-eval harness: PASS ([record](../verification/release-1.66.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `bc78e66`; workflows Check Studio sources 38180751455, Check Studio sources 38180749654, Refresh current release notes 38180748016, Publish verified Studio release 38180748019, Check Studio sources 38180748060: success; [v1.66.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.66.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1174 of 1174) ([record](../verification/github-publication-1.66.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261012-01

- Origin: cloud-code
- Branch: `cloud-code/CC-20261012-01-m04-prompt`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `62b80a9` (main, package 1.66.0); full SHA in the commit trailer
- Result: the commit carrying this entry (repository only)
- Package version: 1.66.0 (unchanged)
- Scope: at the owner's request the M04 host-eval prompt is replaced by the no-logo wording he used in ChatGPT Work (the old one implied the user had a logo). One run on 1.66.0: PASS, read by hand; the reply states it cannot render without code execution and names the Studio player route ([record](../verification/host-evals/2026-10-12-1.66.0-suite-M04.json))
- Shared package changed: no

Verification:

- canonical validator and `scripts/check_all.sh --fast`: PASS
- host eval M04: 1 case, 70,427 tokens, 34 s; single run in headless Claude Code

Cross-host state:

- GitHub: pending until the push is read back
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261012-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261012-02-maintenance-mode`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `4d910be` (main, package 1.66.0); full SHA in the commit trailer
- Result: the commit carrying this entry (repository only)
- Package version: 1.66.0 (unchanged)
- Scope: owner decision 2026-10-12: Studio is a complete working tool and development moves to maintenance mode. AGENTS.md gains the rule (changes only for a defect seen in use or in a host evaluation, a host or model change, or a stale dated fact; the trigger named and shown before and after; the smallest fix in the text the model reads; creative improvements teach rather than add ready-made ideas, from the owner's decision of 2026-10-11). The October improvement plan is marked closed, its deferred items under the same rule
- Shared package changed: no

Verification:

- canonical validator and `scripts/check_all.sh --fast`: PASS

Cross-host state:

- GitHub: pending until the push is read back
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261012-03

- Origin: cloud-code
- Branch: `cloud-code/CC-20261012-03-full-check`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `3144dd5` (main, package 1.66.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.66.1)
- Package version: 1.66.0 -> 1.66.1
- Scope: Fixes for confirmed defects from the full check: coded motion renders reviewed by the Motion Graphics Workflow in eight texts, route lines in Pipeline Core and the orchestrator kit aligned with the single route table, the contract and player link after approval without code execution, SKILL.md and route table over kit methods, the handoff matrix as core contracts with unknown fields never invented, a creative_direction field in Project State, Creative Video Producer using the specialists' methods, the motion reference aligned with the skill, and two small corrections; plus the full-check report and three multi-turn handoff cases
- Shared package changed: yes; 24 changed, 0 added, 0 removed ([scope](../verification/scope-1.66.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there and run separately: 79 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 7 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark, 5 brand guide, 14 host-eval harness: PASS ([record](../verification/release-1.66.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `60b0bcd`; workflows Check Studio sources 38212164623, Check Studio sources 38212162139, Refresh current release notes 38212160407, Check Studio sources 38212160295, Publish verified Studio release 38212160455: success; [v1.66.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.66.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1174 of 1174) ([record](../verification/github-publication-1.66.1.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261012-04

- Origin: cloud-code
- Branch: `cloud-code/CC-20261012-04-motion-1.70`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `9e46aa7` (main, package 1.66.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.70.0)
- Package version: 1.66.1 -> 1.70.0
- Scope: HyperFrames as the default engine for client reels in Claude Code with a map of HyperFrames' 21 skills and an eight-step production loop, a reel board system with twelve ad structures, formats and safe boxes, lyric video, hybrid AI footage, transitions and still frames, and a motion activity check that sends long undeclared stills back for rework
- Shared package changed: yes; 11 changed, 4 added, 0 removed ([scope](../verification/scope-1.70.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there and run separately: 79 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 7 suite 6, 8 suite 7 (3 skipped without optional dependencies), 23 suite 8, 16 suite 9, 18 suite 10, 17 suite 11, 6 suite 12, 8 suite 13, 9 suite 14, 7 suite 15, 4 suite 16, 5 suite 17, 14 suite 18, 6 suite 19, 5 suite 20, 8 suite 21, 5 suite 22, 4 suite 23, 4 suite 24, 4 suite 25, 2 suite 26, 2 suite 27, 2 suite 28, 5 suite 29, 5 suite 30, 4 suite 31, 14 suite 32: PASS ([record](../verification/release-1.70.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `fc582b3`; workflows Check Studio sources 38233850260, Check Studio sources 38233846498, Refresh current release notes 38233844592, Check Studio sources 38233844530, Publish verified Studio release 38233844575: success; [v1.70.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.70.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1178 of 1178) ([record](../verification/github-publication-1.70.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261012-05

- Origin: cloud-code
- Branch: `cloud-code/CC-20261012-05-motion-compendium`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `31ae7df` (main, package 1.70.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.71.0)
- Package version: 1.70.0 -> 1.71.0
- Scope: A motion compendium (knowledge map, ad creative with dated sources, tools and licences, lyric timing, hybrid generated media, techniques and transitions by name, working sequence, failure fixes) and lyric_timing.py (supplied lyrics aligned to recognised word times, interpolation, beat grid, half-beat snapped board cuts, JSON, LRC and SRT)
- Shared package changed: yes; 10 changed, 3 added, 0 removed ([scope](../verification/scope-1.71.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there and run separately: 79 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 7 suite 6, 8 suite 7 (3 skipped without optional dependencies), 23 suite 8, 16 suite 9, 18 suite 10, 17 suite 11, 6 suite 12, 8 suite 13, 9 suite 14, 7 suite 15, 4 suite 16, 5 suite 17, 14 suite 18, 6 suite 19, 5 suite 20, 8 suite 21, 5 suite 22, 4 suite 23, 4 suite 24, 4 suite 25, 2 suite 26, 2 suite 27, 2 suite 28, 5 suite 29, 5 suite 30, 4 suite 31, 5 suite 32, 14 suite 33: PASS ([record](../verification/release-1.71.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `d6ef990`; workflows Check Studio sources 38238123408, Check Studio sources 38238120827, Refresh current release notes 38238116880, Check Studio sources 38238116873, Publish verified Studio release 38238116885: success; [v1.71.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.71.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1181 of 1181) ([record](../verification/github-publication-1.71.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261012-07

- Origin: cloud-code
- Branch: `cloud-code/CC-20261012-07-claude-install`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `1a30607` (main, package 1.71.0)
- Result: the commit carrying this entry
- Package version: 1.71.0 (unchanged)
- Scope: Claude installation from the shell after the owner's desktop attempt of 2026-10-12: CLAUDE_INSTALL.md gains a paste prompt, host detection (`command -v claude`; no `/plugin` in the desktop app's Code tab), the latest-release tag, an inventory step with the `@synced` copy from claude.ai and routes (a) and (b), one confirmation and a report; README links the prompt; UPDATE.md anchor; host-evals.md lists the desktop installation cases CI-01 to CI-05 (not_run); a guide test
- Shared package changed: no (repository documentation and tests only)

Verification:

- canonical validator: PASS; `scripts/check_all.sh` (full list): PASS; source checks only, the desktop cases CI-01 to CI-05 are not run

Cross-host state:

- GitHub: pending until the push is read back
- ChatGPT Work: not_tracked (owner decision 2026-10-10); no hosted change needed, the package is unchanged
- Codex: not_run

## CC-20261013-01

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `53fc97d` (main, package 1.71.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.72.0)
- Package version: 1.71.0 -> 1.72.0
- Scope: Release 1.72.0 finishes change CC-20261012-06, whose release run on another Claude account stopped before it was pushed (its lyric-timing fixes, changelog and release were lost and redone here), and adds CC-20261013-01: the two lyric_timing.py defects named by the GPT Work packet FCW-MOTION-KNOWLEDGE-RESEARCH-01 (negative cut for a line sung from 0 s; inverted interpolation between overlapping heard words), reproduced on 1.71.0 by new tests that fail there and pass now, rational --fps; a 637-technique English atlas projected from gongnyang/awesome-ai-motion (MIT, 1e3c249) with HyperFrames 0.8.149 registry candidates and a lookup tool, requested by the owner; compendium wording the packet found over-categorical; plus the branch's print-ready PDF tools, Demucs caveat and shared script and campaign patterns. Research findings and the proposals left as owner notes are in docs/research/motion-2026-10/gpt-work-findings.md.
- Shared package changed: yes; 21 changed, 8 added, 0 removed ([scope](../verification/scope-1.72.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 216 Node tests (209 passing, 7 opt-in browser tests skipped there), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 7 print PDF (7 skipped without optional dependencies), 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 8 lyric timing, 4 technique atlas, 14 host-eval harness: PASS ([record](../verification/release-1.72.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `49ee13e`; workflows Check Studio sources 38363546063, Refresh current release notes 38363543541, Check Studio sources 38363543607, Publish verified Studio release 38363543525: success; [v1.72.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.72.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1189 of 1189) ([record](../verification/github-publication-1.72.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261013-02

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `52e785f` (main, package 1.72.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.73.0)
- Package version: 1.72.0 -> 1.73.0
- Scope: Release 1.73.0 carries CC-20261013-02, fixes from the owner's retrospective of a client end card made on 2026-10-13 with 1.72.0: a dependency-free HTML-to-MP4 capture for shell hosts whose npm registry is blocked (the session had Chromium and FFmpeg but no route), a runtime probe in step 4 of the motion skill, and clean end-card rules; the one-menu start (startup contract) and a delicate sound preset are left as owner notes.
- Shared package changed: yes; 14 changed, 1 added, 0 removed ([scope](../verification/scope-1.73.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 218 Node tests (210 passing, 8 opt-in browser tests skipped there and run separately: 81 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 7 print PDF (7 skipped without optional dependencies), 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 8 lyric timing, 4 technique atlas, 14 host-eval harness: PASS ([record](../verification/release-1.73.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `b21ddb0`; workflows Check Studio sources 38370062798, Refresh current release notes 38370060248, Check Studio sources 38370060284, Publish verified Studio release 38370060322: success; [v1.73.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.73.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1190 of 1190) ([record](../verification/github-publication-1.73.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261013-03

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `8a61b15` (main, package 1.73.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.74.0)
- Package version: 1.73.0 -> 1.74.0
- Scope: Release 1.74.0 carries CC-20261013-03, the owner-adopted change request CR-20261013-01: after a mode-only creative choice the eight work areas and the A/B pace appear in one message; the orchestrator names the areas in order. Host eval W05 in Claude Code failed on 1.73.0 and passes now; W01, W02, W04 and D01 pass; the owner's ChatGPT startup check is pending.
- Shared package changed: yes; 14 changed, 0 added, 0 removed ([scope](../verification/scope-1.74.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 218 Node tests (210 passing, 8 opt-in browser tests skipped there), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 7 print PDF (7 skipped without optional dependencies), 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 8 lyric timing, 4 technique atlas, 14 host-eval harness: PASS ([record](../verification/release-1.74.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `38e3a4d`; workflows Check Studio sources 38373014268, Refresh current release notes 38373008704, Check Studio sources 38373008689, Publish verified Studio release 38373008625: success; [v1.74.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.74.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1190 of 1190) ([record](../verification/github-publication-1.74.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261013-04

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `99eefe9` (main, package 1.74.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.75.0)
- Package version: 1.74.0 -> 1.75.0
- Scope: Release 1.75.0 carries CC-20261013-04: 18 of 19 findings of the owner's gap audit of 1.74.0 fixed (skill handoffs, invented claims, one-question intake, clear tool errors, no overwrites, Playwright browser discovery, pinned HyperFrames); GAP-16 not reproduced. Host evals G01-G05 in tests/host-evals/gaps.json pass in Claude Code after the change.
- Shared package changed: yes; 34 changed, 0 added, 0 removed ([scope](../verification/scope-1.75.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 218 Node tests (210 passing, 8 opt-in browser tests skipped there and run separately: 81 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 8 motion kinds, 9 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 14 static render, 7 print PDF, 6 Polish copy check, 5 image probe, 8 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 14 host-eval harness: PASS ([record](../verification/release-1.75.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `1eb2194`; workflows Check Studio sources 38405591085, Refresh current release notes 38405586080, Check Studio sources 38405586323, Publish verified Studio release 38405586129: success; [v1.75.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.75.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1190 of 1190) ([record](../verification/github-publication-1.75.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261013-06

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `bc6756b` (main, package 1.75.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.76.0)
- Package version: 1.75.0 -> 1.76.0
- Scope: Release 1.76.0 carries CC-20261013-06: findings F01 to F06 and the release parser from the owner's evaluation of 1.75.0 fixed with tests (text outside the canvas, persistent and active-word overflow, gross labels, negative rates, approval after a look change, dirty-tree guard, Node 24 counts); F07 is an Arial font dependency, now reported by the renderer and skipped with a reason in tests.
- Shared package changed: yes; 18 changed, 0 added, 0 removed ([scope](../verification/scope-1.76.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 218 Node tests (210 passing, 8 opt-in browser tests skipped there and run separately: 81 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 2 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 5 image probe, 10 quote calculator, 5 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 2 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 14 host-eval harness: PASS ([record](../verification/release-1.76.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `938ef63`; workflows Check Studio sources 38438498414, Refresh current release notes 38438494248, Publish verified Studio release 38438494259, Check Studio sources 38438494261: success; [v1.76.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.76.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1190 of 1190) ([record](../verification/github-publication-1.76.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261013-07

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `e7ef587` (main, package 1.76.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.77.0)
- Package version: 1.76.0 -> 1.77.0
- Scope: Release 1.77.0 carries CC-20261013-07: defects from an external review of 1.76.0 reproduced and fixed with tests (path containment in the motion renderer and sound tool, quote lines, clip matching, voice-over pauses, OCR numbers, multi-dot output names, Polish address and no-break spaces, UGC disclosure), release and CI hardening, and complete third-party notices; findings that did not reproduce or need an owner decision are recorded in docs/reviews/argon-review-1.76.0-2026-10-13.md.
- Shared package changed: yes; 26 changed, 0 added, 0 removed ([scope](../verification/scope-1.77.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 218 Node tests (210 passing, 8 opt-in browser tests skipped there and run separately: 81 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 2 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 6 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 14 host-eval harness: PASS ([record](../verification/release-1.77.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `d48c049`; workflows Check Studio sources 38513621823, Check Studio sources 38513618824, Refresh current release notes 38513618861, Publish verified Studio release 38513618830: success; [v1.77.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.77.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1190 of 1190) ([record](../verification/github-publication-1.77.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261014-01

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `9cefe9c` (main, package 1.77.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.78.0)
- Package version: 1.77.0 -> 1.78.0
- Scope: Release 1.78.0 carries CC-20261014-01: after reviewing the motionmaxxing repository the owner chose one adoption, a page-chrome check in Motion Graphics Workflow's review (corner labels, counters, timecodes, progress bars, kickers, repeated slide layouts), with the ad's logo, offer, phone and address kept; host case G06 passes before and after, and after the change the reply states the rule.
- Shared package changed: yes; 9 changed, 0 added, 0 removed ([scope](../verification/scope-1.78.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 218 Node tests (210 passing, 8 opt-in browser tests skipped there and run separately: 81 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 2 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 6 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 14 host-eval harness: PASS ([record](../verification/release-1.78.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `7f1a984`; workflows Check Studio sources 38523051484, Refresh current release notes 38523049189, Publish verified Studio release 38523049171, Check Studio sources 38523048957: success; [v1.78.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.78.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1190 of 1190) ([record](../verification/github-publication-1.78.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261014-02

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `f48268c` (main, package 1.78.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.79.0)
- Package version: 1.78.0 -> 1.79.0
- Scope: Release 1.79.0 carries CC-20261014-02: the owner's ChatGPT Work test (2026-10-14, PASS_REPORTED) showed the sandbox installs the HyperFrames CLI on request and renders; ChatGPT Work's tool statuses, the capability card, the runtime map, Motion Graphics Workflow and the environment check now offer that session install instead of ruling it out. Ordinary ChatGPT and the Claude apps are unchanged.
- Shared package changed: yes; 17 changed, 0 added, 0 removed ([scope](../verification/scope-1.79.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 218 Node tests (210 passing, 8 opt-in browser tests skipped there and run separately: 81 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 2 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 6 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 14 host-eval harness: PASS ([record](../verification/release-1.79.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `7310046`; workflows Check Studio sources 38543752451, Refresh current release notes 38543750854, Publish verified Studio release 38543750755, Check Studio sources 38543750799: success; [v1.79.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.79.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1190 of 1190) ([record](../verification/github-publication-1.79.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261014-03

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `35834a7` (main, package 1.79.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.80.0)
- Package version: 1.79.0 -> 1.80.0
- Scope: Release 1.80.0 carries CC-20261014-03: from a 2026-10-14 production handover, Motion Graphics Workflow plans generated cut-out assets for realistic objects, hands and light instead of drawing them in code, with a transparency route per generator (checked 2026-10-14) and a new asset check tool (check, difference matte, chroma key) used before compositing, plus an edge check in the rendered film; host case G07 fails before and passes after. A clip-level automatic edge audit and a motion-contract field for generated assets are left for a later trigger.
- Shared package changed: yes; 12 changed, 4 added, 0 removed ([scope](../verification/scope-1.80.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 218 Node tests (210 passing, 8 opt-in browser tests skipped there and run separately: 81 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 2 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 16 caption, 18 environment check, 17 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 6 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 7 motion assets, 14 host-eval harness: PASS ([record](../verification/release-1.80.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `8eba8c0`; workflows Publish verified Studio release 38573157444, Check Studio sources 38573158950, Check Studio sources 38573157367, Refresh current release notes 38573157239: success; [v1.80.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.80.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1194 of 1194) ([record](../verification/github-publication-1.80.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261014-04

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `dcb0aa9` (main, package 1.80.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.81.0)
- Package version: 1.80.0 -> 1.81.0
- Scope: Release 1.81.0 carries CC-20261014-04: all 18 findings of the owner's technical audit of 1.80.0 and the two earlier asset findings fixed with regression tests (publication integrity, manifest and ZIP rule, environment check runnability, Node minimum, literal paths and host normalization; MP4 composition offsets, exact copy order, caption approval, audio length, word retiming, playback length; harness questions, tool results, billing guard and partial usage; learning-mode welcome; asset shift and empty files). Live runs: gate 5/5; stronger M04 and X03 checks found the no-code route skipped, fixed in SKILL.md, then passed.
- Shared package changed: yes; 24 changed, 0 added, 0 removed ([scope](../verification/scope-1.81.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 219 Node tests (211 passing, 8 opt-in browser tests skipped there and run separately: 82 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 6 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 17 caption, 22 environment check, 19 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 6 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 9 motion assets, 18 host-eval harness: PASS ([record](../verification/release-1.81.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `0341238`; workflows Check Studio sources 38633232673, Refresh current release notes 38633229119, Publish the motion player to GitHub Pages 38633229101, Publish verified Studio release 38633229160, Check Studio sources 38633229141: success; [v1.81.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.81.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1194 of 1194) ([record](../verification/github-publication-1.81.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261015-01

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `e9343c2` (main, package 1.81.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.82.0)
- Package version: 1.81.0 -> 1.82.0
- Scope: Release 1.82.0 carries CC-20261015-01: from the owner's creativity audit of 1.81.0, the creative evaluation gains a directions check (exact count, each about the brief, no near copies) and offer facts, fixes 'nie tylko' and variant labels, so a template answer no longer passes; the ideation method adds argument, brand and removal tests. Live creative run 7 of 11; the remaining failures are category motifs, a known limit recorded without tuning on the suite. Media evidence and comparative studies stay owner decisions.
- Shared package changed: yes; 9 changed, 0 added, 0 removed ([scope](../verification/scope-1.82.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 219 Node tests (211 passing, 8 opt-in browser tests skipped there and run separately: 82 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 6 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 17 caption, 22 environment check, 19 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 6 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 9 motion assets, 21 host-eval harness: PASS ([record](../verification/release-1.82.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `6b93b04`; workflows Check Studio sources 38688538676, Refresh current release notes 38688536035, Publish verified Studio release 38688536015, Check Studio sources 38688535974: success; [v1.82.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.82.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1194 of 1194) ([record](../verification/github-publication-1.82.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261015-02

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `2a700cc` (main, package 1.82.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.83.0)
- Package version: 1.82.0 -> 1.83.0
- Scope: Release 1.83.0 carries CC-20261015-02: at the owner's request, Image Prompt Architect gains a reference reconstruction method generalized from his reverse-engineering project (model image versus REF, mechanism first, spatial relations, colour roles, medium kept, user template filled exactly, ordered corrections), and the image probe gains --analyze for a measured palette, tones and subject position. Host case G08 fails before and passes after.
- Shared package changed: yes; 11 changed, 1 added, 0 removed ([scope](../verification/scope-1.83.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 219 Node tests (211 passing, 8 opt-in browser tests skipped there and run separately: 82 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 6 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 17 caption, 22 environment check, 19 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 8 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 9 motion assets, 21 host-eval harness: PASS ([record](../verification/release-1.83.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `f6f95f6`; workflows Check Studio sources 38747613973, Check Studio sources 38747609373, Refresh current release notes 38747609720, Publish verified Studio release 38747609588: success; [v1.83.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.83.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1195 of 1195) ([record](../verification/github-publication-1.83.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261015-03

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `d030bf8` (main, package 1.83.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.84.0)
- Package version: 1.83.0 -> 1.84.0
- Scope: Image reconstruction fixes from a host evaluation on the owner's mirror portrait: optical effects described by their cause, focus and gaze per figure, the probe run whenever code runs, and image_probe --analyze with merged shades, accents, black and white points, colour character, focus and brightness grids, sRGB conversion and no subject on texture.
- Shared package changed: yes; 12 changed, 0 added, 0 removed ([scope](../verification/scope-1.84.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 219 Node tests (211 passing, 8 opt-in browser tests skipped there and run separately: 82 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 6 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 17 caption, 22 environment check, 19 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 14 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 9 motion assets, 21 host-eval harness: PASS ([record](../verification/release-1.84.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `3f0e3d1`; workflows Check Studio sources 38764537942, Refresh current release notes 38764534394, Publish verified Studio release 38764534743, Check Studio sources 38764534661: success; [v1.84.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.84.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1195 of 1195) ([record](../verification/github-publication-1.84.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261015-04

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `7f490d1` (main, package 1.84.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.84.1)
- Package version: 1.84.0 -> 1.84.1
- Scope: At the owner's request the reconstruction method keeps general rules only; two provenance notes naming the single example are removed from the package text, with no rule change.
- Shared package changed: yes; 9 changed, 0 added, 0 removed ([scope](../verification/scope-1.84.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 219 Node tests (211 passing, 8 opt-in browser tests skipped there and run separately: 82 passing in the browser run), 13 Codex installer, 4 package identity, 5 benchmark script, 6 host smoke, 6 hosted readback, 8 Claude plugin and guides, 6 release helper, 8 GEPA pilot (3 skipped without optional dependencies), 23 asset, 17 caption, 22 environment check, 19 motion acceptance, 6 motion fonts, 10 motion kinds, 10 motion variants, 7 skill finder, 4 Animate engine, 5 Animate voice, 15 static render, 7 print PDF, 6 Polish copy check, 14 image probe, 11 quote calculator, 6 voice-over budget, 4 edit export, 4 storyboard compositor, 4 sheet export, 2 shot plan check, 2 prompt pack, 3 clip review, 5 SVG wordmark (5 skipped without optional dependencies), 5 brand guide, 4 motion activity, 9 lyric timing, 4 technique atlas, 9 motion assets, 21 host-eval harness: PASS ([record](../verification/release-1.84.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `047e810`; workflows Check Studio sources 38769656353, Refresh current release notes 38769653446, Publish verified Studio release 38769653256, Check Studio sources 38769653339: success; [v1.84.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.84.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1195 of 1195) ([record](../verification/github-publication-1.84.1.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261015-05

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `7f83820` (main, package 1.84.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.85.0)
- Package version: 1.84.1 -> 1.85.0
- Scope: From the owner's request to review morluto/rea: a web motion probe that reads a page's motion libraries, tweens, CSS animations and frames; a curated extension registry with REA pinned at rea-agents 6.5.0, per-host status and dry-run, install, verify and remove steps, installed only on an explicit request; skill-finder, orchestrator and install-guide hooks and a maintainer guide.
- Shared package changed: yes; 12 changed, 8 added, 0 removed ([scope](../verification/scope-1.85.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 221 Node tests (212 passing, 9 opt-in browser tests skipped there and run separately: 84 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 22 suite 11, 19 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 6 suite 17, 4 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 6 suite 22, 14 suite 23, 11 suite 24, 6 suite 25, 4 suite 26, 4 suite 27, 4 suite 28, 2 suite 29, 2 suite 30, 3 suite 31, 5 suite 32 (5 skipped without optional dependencies), 5 suite 33, 4 suite 34, 9 suite 35, 4 suite 36, 9 suite 37, 21 suite 38: PASS ([record](../verification/release-1.85.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `26e03d5`; workflows Check Studio sources 38815524853, Refresh current release notes 38815522353, Publish verified Studio release 38815522411, Check Studio sources 38815522363: success; [v1.85.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.85.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1203 of 1203) ([record](../verification/github-publication-1.85.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261016-01

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `edfef8a` (main, package 1.85.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.86.0)
- Package version: 1.85.0 -> 1.86.0
- Scope: Animate, Motion Designer and Meta Ads Designer added to the extension registry, each pinned to its reviewed commit with per-host routes tried in a sandbox home; a manual host status; every repository the owner sends is now added to the registry.
- Shared package changed: yes; 14 changed, 0 added, 0 removed ([scope](../verification/scope-1.86.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 221 Node tests (212 passing, 9 opt-in browser tests skipped there and run separately: 84 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 22 suite 11, 19 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 8 suite 17, 4 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 6 suite 22, 14 suite 23, 11 suite 24, 6 suite 25, 4 suite 26, 4 suite 27, 4 suite 28, 2 suite 29, 2 suite 30, 3 suite 31, 5 suite 32 (5 skipped without optional dependencies), 5 suite 33, 4 suite 34, 9 suite 35, 4 suite 36, 9 suite 37, 21 suite 38: PASS ([record](../verification/release-1.86.0.json))

Cross-host state:

- GitHub: pending (release commit, tag workflow and readback follow)
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261016-02

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `4d8f1c3` (main, package 1.86.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.86.1)
- Package version: 1.86.0 -> 1.86.1
- Scope: The web motion probe retries the cleanup of its temporary browser profile instead of failing (CI failure of the 1.86.0 release); publishes the 1.86.0 extension entries.
- Shared package changed: yes; 8 changed, 0 added, 0 removed ([scope](../verification/scope-1.86.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 221 Node tests (212 passing, 9 opt-in browser tests skipped there and run separately: 84 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 22 suite 11, 19 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 8 suite 17, 4 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 6 suite 22, 14 suite 23, 11 suite 24, 6 suite 25, 4 suite 26, 4 suite 27, 4 suite 28, 2 suite 29, 2 suite 30, 3 suite 31, 5 suite 32 (5 skipped without optional dependencies), 5 suite 33, 4 suite 34, 9 suite 35, 4 suite 36, 9 suite 37, 21 suite 38: PASS ([record](../verification/release-1.86.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `9d9427b`; workflows Check Studio sources 38854210262, Publish verified Studio release 38854207558, Refresh current release notes 38854207589, Check Studio sources 38854207522: success; [v1.86.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.86.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1203 of 1203) ([record](../verification/github-publication-1.86.1.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261016-03

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `30246c9` (main, package 1.86.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.87.0)
- Package version: 1.86.1 -> 1.87.0
- Scope: Voicebox, OmniVoice, VoxCPM2, MOSS-TTS and MOSS-TTSD as pinned voice-engine extensions the user chooses from, with a comparison and recommendation in Audio Production Director when the user does not know them.
- Shared package changed: yes; 11 changed, 7 added, 0 removed ([scope](../verification/scope-1.87.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 221 Node tests (212 passing, 9 opt-in browser tests skipped there and run separately: 84 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 22 suite 11, 19 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 9 suite 17, 4 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 6 suite 22, 14 suite 23, 11 suite 24, 6 suite 25, 4 suite 26, 4 suite 27, 4 suite 28, 2 suite 29, 2 suite 30, 3 suite 31, 5 suite 32 (5 skipped without optional dependencies), 5 suite 33, 4 suite 34, 9 suite 35, 4 suite 36, 9 suite 37, 21 suite 38: PASS ([record](../verification/release-1.87.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `23c895f`; workflows Check Studio sources 38857297467, Publish verified Studio release 38857294991, Refresh current release notes 38857295118, Check Studio sources 38857295117: success; [v1.87.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.87.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1210 of 1210) ([record](../verification/github-publication-1.87.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261016-04

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `f46de00` (main, package 1.87.0); full SHA in the commit trailer
- Result: the commit carrying this entry; no release (repository documentation only)
- Package version: 1.87.0 (unchanged)
- Scope: owner request 2026-10-16: `docs/roadmap.md` for Codex and ChatGPT Work (direction in order of value, what Cloud Code did from 1.70.0 to 1.87.0 and why, open items, notes per surface); `AGENTS.md` points every surface to it
- Shared package changed: no

Verification:

- canonical validator and `scripts/check_all.sh --fast`: PASS

Cross-host state:

- GitHub: pushed to `main` and the working branch
- ChatGPT Work: not_tracked (no package change)
- Codex: not_run

## CX-20261017-01

- Origin: codex
- Branch: `codex/four-audit-fixes`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `5902098` (main, package 1.87.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.87.1)
- Package version: 1.87.0 -> 1.87.1
- Scope: Fix the four reproduced audit defects: motion-score CLI entry paths, stale motion QA reports, Animate caption output paths and machine-dependent browser tests.
- Shared package changed: yes; 20 changed, 1 added, 0 removed ([scope](../verification/scope-1.87.1.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 222 Node tests (213 passing, 9 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 9 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21 (7 skipped without optional dependencies), 6 suite 22, 14 suite 23, 11 suite 24, 6 suite 25, 4 suite 26, 4 suite 27, 4 suite 28, 2 suite 29, 2 suite 30, 3 suite 31, 5 suite 32, 5 suite 33, 4 suite 34, 9 suite 35, 4 suite 36, 9 suite 37, 21 suite 38: PASS ([record](../verification/release-1.87.1.json))

Cross-host state:

- GitHub: synchronized package commit `90ec991`, tag v1.87.1; source-check and release workflows PASS. Downloaded plugin ZIP, inventory and player match the build; all 1211 source files match the tag ([publication](../verification/github-publication-1.87.1.json)). The release-notes refresh rejected the heading prefix; the repository-only follow-up corrects that one line.
- ChatGPT Work: synchronized, saved release `pluginrel_6ad3630b000c8191ab2725003b5b7302`; all 1211 source files match except the approved PoYo bindings and documented JSON layout normalization; two PoYo files preserved ([readback](../verification/hosted-sync-1.87.1.json)).
- Codex: synchronized managed cache 1.87.1, all 1213 files byte-identical to the saved plugin; fresh-chat behavior not_run.

## CX-20261017-02

- Origin: codex
- Branch: `codex/logo-design-assimilation`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `08a45bf` (main, package 1.87.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.88.0)
- Package version: 1.87.1 -> 1.88.0
- Scope: Owner-requested full reusable Logo Design resources and complete Anatomy SVG/WebGL/3D toolkit, integrated into the existing owners with project adapters, runtime checks, tests, source hashes and optional original extensions.
- Shared package changed: yes; 17 changed, 248 added, 0 removed ([scope](../verification/scope-1.88.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 237 Node tests (226 passing, 11 opt-in rendering/browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 12 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21 (7 skipped without optional dependencies), 6 suite 22, 14 suite 23, 11 suite 24, 6 suite 25, 4 suite 26, 4 suite 27, 4 suite 28, 2 suite 29, 2 suite 30, 3 suite 31, 5 suite 32, 5 suite 33, 4 suite 34, 9 suite 35, 4 suite 36, 9 suite 37, 21 suite 38: PASS ([record](../verification/release-1.88.0.json))

Cross-host state:

- GitHub: synchronized package commit `221cd75`, tag v1.88.0; source-check and release workflows PASS. Downloaded plugin ZIP, inventory and player match the build; all 1459 source files match the tag ([publication](../verification/github-publication-1.88.0.json)).
- ChatGPT Work: synchronized, saved release `pluginrel_6ad370a5bd6c81919a6917dbab9f1853`; all 1459 source files match except the approved PoYo bindings and documented JSON layout normalization; two PoYo files preserved ([readback](../verification/hosted-sync-1.88.0.json)).
- Codex: synchronized managed cache 1.88.0, all 1461 files byte-identical to the saved plugin; fresh-chat behavior not_run.

- Additional verification: Anatomy browser 5/5, final Logo adapter 11/11 with PNG/icons; Olga confirmed the avatar-export P2 fixed. The release workflow passed on the final committed tree: 238 Node tests (227 pass, 11 skipped) and 38 Python suites, including the added regression. New Anatomy MP4 export not_run after automatic approval review rejected the requested file write.

## CC-20261017-01

- Origin: cloud-code
- Branch: `cloud-code/CC-20261017-01-slim-and-motion`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `40552d8` (main, package 1.88.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.89.0)
- Package version: 1.88.0 -> 1.89.0
- Scope: A local-service reel starter for HyperFrames (rendered at 9:16 and 4:5, motion activity PASS after a reproduced FAIL), contents lists for six large references, and description headroom (7,699 of 7,800). No host tests this round by owner decision.
- Shared package changed: yes; 18 changed, 3 added, 0 removed ([scope](../verification/scope-1.89.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 12 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 14 suite 24, 11 suite 25, 6 suite 26, 4 suite 27, 4 suite 28, 4 suite 29, 2 suite 30, 2 suite 31, 3 suite 32, 5 suite 33, 5 suite 34, 4 suite 35, 9 suite 36, 4 suite 37, 9 suite 38, 21 suite 39: PASS ([record](../verification/release-1.89.0.json))

Cross-host state:

- GitHub: pending (release commit, tag workflow and readback follow)
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261017-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261017-01-slim-and-motion`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `688ea23` (main, package 1.89.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.89.1)
- Package version: 1.89.0 -> 1.89.1
- Scope: Agent Reach added to the recommended-extension registry for its no-login channels only, with a decision map and a one-line offer in Research Evidence; not installed or run by owner decision. Records that 1.89.0 was published and its notes workflow failure was fixed in 688ea23.
- Shared package changed: yes; 9 changed, 2 added, 0 removed ([scope](../verification/scope-1.89.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 12 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 14 suite 24, 11 suite 25, 6 suite 26, 4 suite 27, 4 suite 28, 4 suite 29, 2 suite 30, 2 suite 31, 3 suite 32, 5 suite 33, 5 suite 34, 4 suite 35, 9 suite 36, 4 suite 37, 9 suite 38, 21 suite 39: PASS ([record](../verification/release-1.89.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `4a8ed51`; workflows Check Studio sources 39048604253, Refresh current release notes 39048601299, Publish verified Studio release 39048601336, Check Studio sources 39048601327: success; [v1.89.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.89.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1464 of 1464) ([record](../verification/github-publication-1.89.1.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261017-03

- Origin: cloud-code
- Branch: `cloud-code/CC-20261017-03-web-reach`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `ac55391` (main, package 1.89.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.90.0)
- Package version: 1.89.1 -> 1.90.0
- Scope: web_reach.py adapts Agent Reach's no-login reading (pages, feeds, public GitHub, YouTube subtitles) into Research Evidence with the standard library, a public-URL guard and cited results.
- Shared package changed: yes; 10 changed, 3 added, 0 removed ([scope](../verification/scope-1.90.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 12 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 9 suite 37, 4 suite 38, 9 suite 39, 21 suite 40: PASS ([record](../verification/release-1.90.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `15af7d0`; workflows Check Studio sources 39059393654, Refresh current release notes 39059391681, Publish verified Studio release 39059391686, Check Studio sources 39059391683: success; [v1.90.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.90.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1467 of 1467) ([record](../verification/github-publication-1.90.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261018-01

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-lyric-timing-real-song`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `bd00d0c` (main, package 1.90.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.90.1)
- Package version: 1.90.0 -> 1.90.1
- Scope: First end-to-end lyric timing run on a real CC BY-SA song (98 % of words matched); FFmpeg decoding replaces PyAV for faster-whisper, and unheard words no longer stretch across instrumental gaps.
- Shared package changed: yes; 10 changed, 0 added, 0 removed ([scope](../verification/scope-1.90.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 12 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 10 suite 37, 4 suite 38, 9 suite 39, 21 suite 40: PASS ([record](../verification/release-1.90.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `2bba3ac`; workflows Check Studio sources 39104946785, Publish verified Studio release 39104944819, Check Studio sources 39104944796, Refresh current release notes 39104944759: success; [v1.90.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.90.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1467 of 1467) ([record](../verification/github-publication-1.90.1.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261018-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-02-turbo-default`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `03844a4` (main, package 1.90.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.90.2)
- Package version: 1.90.1 -> 1.90.2
- Scope: Lyric timing defaults to faster-whisper small (98 % on a real song versus 72 % for the former large-v3) and retries a pass below 90 % with the other conditioning setting.
- Shared package changed: yes; 10 changed, 0 added, 0 removed ([scope](../verification/scope-1.90.2.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 12 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 4 suite 38, 9 suite 39, 21 suite 40: PASS ([record](../verification/release-1.90.2.json))

Cross-host state:

- GitHub: synchronized. `main` at `1b665f5`; workflows Check Studio sources 39137123783, Publish verified Studio release 39137121903, Refresh current release notes 39137121983, Check Studio sources 39137121782: success; [v1.90.2](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.90.2) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1467 of 1467) ([record](../verification/github-publication-1.90.2.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261018-03

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-03-polish-song`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `f36af73` (main, package 1.90.2); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.90.3)
- Package version: 1.90.2 -> 1.90.3
- Scope: Lyric timing result on an owner-supplied Polish rap track recorded (89 % of words matched with the default and the retry); documentation only.
- Shared package changed: yes; 8 changed, 0 added, 0 removed ([scope](../verification/scope-1.90.3.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 12 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 4 suite 38, 9 suite 39, 21 suite 40: PASS ([record](../verification/release-1.90.3.json))

Cross-host state:

- GitHub: synchronized. `main` at `f255ae5`; workflows Check Studio sources 39150821873, Refresh current release notes 39150819693, Publish verified Studio release 39150819648, Check Studio sources 39150819662: success; [v1.90.3](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.90.3) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1467 of 1467) ([record](../verification/github-publication-1.90.3.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261018-04

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-recommended-repos`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `6ffb604` (main, package 1.90.3); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.91.0)
- Package version: 1.90.3 -> 1.91.0
- Scope: Welcome option 4 lists the GitHub repositories FrameCore Works recommends with descriptions and per-agent installation; Iso Glow kit with audio_envelope.py (from iso-glow) and art-style and explainer direction with a reference breakdown (from huashu-art-motion) in Motion Graphics Workflow; both repositories added to the extension registry.
- Shared package changed: yes; 22 changed, 12 added, 0 removed ([scope](../verification/scope-1.91.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 14 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 6 suite 38, 3 suite 39, 4 suite 40, 9 suite 41, 21 suite 42: PASS ([record](../verification/release-1.91.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `4022e05`; workflows Check Studio sources 39160001050, Check Studio sources 39159999079, Publish verified Studio release 39159997773, Refresh current release notes 39159997788, Check Studio sources 39159997765: success; [v1.91.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.91.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1479 of 1479) ([record](../verification/github-publication-1.91.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261019-01

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-recommended-repos`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `f1a063e` (main, package 1.91.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.92.0)
- Package version: 1.91.0 -> 1.92.0
- Scope: Full adaptation of Open Design: craft rules with craft_lint.py, DESIGN.md export and import for the brand kit, 87 licence-filtered prompt examples for gpt-image-2, Seedance 2.0 and HyperFrames, and open-design in the recommended repositories.
- Shared package changed: yes; 16 changed, 10 added, 0 removed ([scope](../verification/scope-1.92.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 14 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 6 suite 38, 3 suite 39, 9 suite 40, 3 suite 41, 4 suite 42, 9 suite 43, 21 suite 44: PASS ([record](../verification/release-1.92.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `92f7836`; workflows Check Studio sources 39203858328, Check Studio sources 39203856162, Refresh current release notes 39203853733, Publish verified Studio release 39203853794, Check Studio sources 39203853724: success; [v1.92.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.92.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1489 of 1489) ([record](../verification/github-publication-1.92.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261019-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-recommended-repos`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `28a1487` (main, package 1.92.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.93.0)
- Package version: 1.92.0 -> 1.93.0
- Scope: Full adaptation of anti-slop: AI writing patterns in English and Polish with ai_writing_check.py, the purpose test, liveliness dials, interface patterns, honest content and responsive layout in the craft rules, new craft_lint.py rules, contrast_check.py, and anti-slop in the recommended repositories.
- Shared package changed: yes; 18 changed, 6 added, 0 removed ([scope](../verification/scope-1.93.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 14 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 6 suite 38, 3 suite 39, 12 suite 40, 3 suite 41, 6 suite 42, 4 suite 43, 9 suite 44, 21 suite 45: PASS ([record](../verification/release-1.93.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `c84cd22`; workflows Check Studio sources 39213179014, Check Studio sources 39213175064, Refresh current release notes 39213172406, Publish verified Studio release 39213172411, Check Studio sources 39213172404: success; [v1.93.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.93.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1495 of 1495) ([record](../verification/github-publication-1.93.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261019-03

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-recommended-repos`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `beaba73` (main, package 1.93.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.94.0)
- Package version: 1.93.0 -> 1.94.0
- Scope: Full audit after 1.91.0 to 1.93.0: new owners for page mockups, decks, contrast checks, reference animations and lyric videos; added knowledge linked from every skill that uses it; four rule conflicts resolved; Iso Glow example follows the track length; capability card completed; knowledge wiring test and an additions host-eval set.
- Shared package changed: yes; 39 changed, 1 added, 0 removed ([scope](../verification/scope-1.94.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 15 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 6 suite 38, 3 suite 39, 12 suite 40, 3 suite 41, 6 suite 42, 4 suite 43, 9 suite 44, 2 suite 45, 21 suite 46: PASS ([record](../verification/release-1.94.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `c8f9ab8`; workflows Check Studio sources 39236647785, Check Studio sources 39236643547, Refresh current release notes 39236640871, Publish verified Studio release 39236640868, Check Studio sources 39236640908: success; [v1.94.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.94.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1496 of 1496) ([record](../verification/github-publication-1.94.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261019-04

- Origin: cloud-code
- Branch: local working branch, fast-forwarded into `main` under the owner's standing rule
- Baseline: `7606617` (main, package 1.94.0)
- Result: the commit carrying this entry (package unchanged, 1.94.0)
- Package version: none
- Scope: remote branch cleanup and its cause. The owner deleted 80 merged or superseded remote branches by hand (78 merged into `main`; `claude/plugin-cloud-update-vzrtk5` and `cloud-code/CC-20261007-03-second-test-report` superseded, heads `2e5cc5a` and `a82f1ee`) and enabled automatic deletion of merged pull request branches. `scripts/release.py` no longer pushes the local working branch, only `main` and `STUDIO_RELEASE_BRANCHES`. Audit and Codex handover updated.
- Shared package changed: no

Verification:

- `git ls-remote --heads origin`: `main`, `gh-pages`, `ccr-b6d36a1c-4hszow`; 126 version tags; GitHub Pages answers 200
- `tests/test_release.py`: PASS; canonical validator: PASS

Cross-host state:

- GitHub: synchronized once this commit is on `main`
- ChatGPT Work: not_tracked (no package change)
- Codex: not_run

## CC-20261019-05

- Origin: cloud-code
- Branch: local working branch, fast-forwarded into `main` under the owner's standing rule
- Baseline: `fdd81a9` (main, package 1.94.0)
- Result: the commit carrying this entry (package unchanged, 1.94.0)
- Package version: none
- Scope: branch hygiene rule for every surface (Claude Code local and cloud, Codex, ChatGPT Work) in AGENTS.md; a root CLAUDE.md that imports AGENTS.md so Claude Code loads the same rules; pointer in the Codex handover
- Shared package changed: no

Verification:

- canonical validator: PASS; `scripts/check_all.sh --fast`: PASS

Cross-host state:

- GitHub: synchronized once this commit is on `main`
- ChatGPT Work: not_tracked (no package change)
- Codex: not_run

## CC-20261019-06

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-recommended-repos`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `36b4948` (main, package 1.94.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.95.0)
- Package version: 1.94.0 -> 1.95.0
- Scope: Upscaling route in Static Graphic Design Creator with model licences for paid work, and Upscayl 2.15.0 in the recommended repositories with pinned installers.
- Shared package changed: yes; 14 changed, 1 added, 0 removed ([scope](../verification/scope-1.95.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 15 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 6 suite 38, 3 suite 39, 12 suite 40, 3 suite 41, 6 suite 42, 4 suite 43, 9 suite 44, 2 suite 45, 21 suite 46: PASS ([record](../verification/release-1.95.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `8bebc64`; workflows Check Studio sources 39251333111, Check Studio sources 39251330269, Refresh current release notes 39251330422, Publish verified Studio release 39251330481: success; [v1.95.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.95.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1497 of 1497) ([record](../verification/github-publication-1.95.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261019-07

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-recommended-repos`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `578cca6` (main, package 1.95.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.96.0)
- Package version: 1.95.0 -> 1.96.0
- Scope: Dense kinetic brand reels: structure, carrier from the logo, scene logic check, chat reading time and brand-first colours, learned from the owner-approved Knock Knock reel.
- Shared package changed: yes; 13 changed, 1 added, 0 removed ([scope](../verification/scope-1.96.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 15 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 6 suite 38, 3 suite 39, 12 suite 40, 3 suite 41, 6 suite 42, 4 suite 43, 9 suite 44, 2 suite 45, 21 suite 46: PASS ([record](../verification/release-1.96.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `20ba378`; workflows Check Studio sources 39262224725, Refresh current release notes 39262220707, Publish verified Studio release 39262220508, Check Studio sources 39262220610: success; [v1.96.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.96.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1498 of 1498) ([record](../verification/github-publication-1.96.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261020-01

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-recommended-repos`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `2c4a146` (main, package 1.96.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.97.0)
- Package version: 1.96.0 -> 1.97.0
- Scope: OpenCreator 3.2.8 added to the recommended repositories with pinned installers and recorded licence limits.
- Shared package changed: yes; 8 changed, 0 added, 0 removed ([scope](../verification/scope-1.97.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 15 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 6 suite 38, 3 suite 39, 12 suite 40, 3 suite 41, 6 suite 42, 4 suite 43, 9 suite 44, 2 suite 45, 21 suite 46: PASS ([record](../verification/release-1.97.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `8cf6527`; workflows Check Studio sources 39375214807, Refresh current release notes 39375212542, Publish verified Studio release 39375212578, Check Studio sources 39375212539: success; [v1.97.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.97.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1498 of 1498) ([record](../verification/github-publication-1.97.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261020-02

- Origin: cloud-code
- Branch: `cloud-code/CC-20261018-01-recommended-repos`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `daab582` (main, package 1.97.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.98.0)
- Package version: 1.97.0 -> 1.98.0
- Scope: Native listening tools (measure, sync, critique, check, sheet, profile, place samples), earshot registry entry with light and full tier, sound craft reference, wiring
- Shared package changed: yes; 14 changed, 7 added, 0 removed ([scope](../verification/scope-1.98.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 6 suite 7, 8 suite 8 (3 skipped without optional dependencies), 23 suite 9, 17 suite 10, 23 suite 11, 24 suite 12, 6 suite 13, 10 suite 14, 10 suite 15, 7 suite 16, 15 suite 17, 11 suite 18, 5 suite 19, 15 suite 20, 7 suite 21, 2 suite 22, 6 suite 23, 6 suite 24, 14 suite 25, 11 suite 26, 6 suite 27, 4 suite 28, 4 suite 29, 4 suite 30, 2 suite 31, 2 suite 32, 3 suite 33, 5 suite 34, 5 suite 35, 4 suite 36, 11 suite 37, 6 suite 38, 8 suite 39, 3 suite 40, 12 suite 41, 3 suite 42, 6 suite 43, 4 suite 44, 9 suite 45, 2 suite 46, 21 suite 47: PASS ([record](../verification/release-1.98.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `da84cdd`; workflows Refresh current release notes 39393458837, Publish verified Studio release 39393458942, Check Studio sources 39393458904: success; [v1.98.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.98.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1505 of 1505) ([record](../verification/github-publication-1.98.0.json))
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CC-20261020-03: handover for ChatGPT Work (GPT Astra)

- Origin: cloud-code; baseline `d06ac7d`; package unchanged (1.98.0)
- Scope: `docs/handover-chatgpt-work-2026-10-20.md` (release.py `--min-runs` default, additions host-eval run, optional earshot sample demo)
- Verification: canonical validator
- GitHub: pending until pushed
- ChatGPT Work: not_tracked (owner decision 2026-10-10)
- Codex: not_run

## CW-20261020-01: publish workflow count and additions preflight

- Origin: chatgpt-work (Codex shell)
- Branch: `codex/CW-20261020-01-publish-default`, local only
- Baseline: `881dcb55b7f09b0f0866d1ffa8a46a71025443b5` (main, package 1.98.0)
- Result: the commit carrying this entry; package unchanged (1.98.0)
- Trigger: the owner requested tasks 1 and 2 of `docs/handover-chatgpt-work-2026-10-20.md`; the main-only release creates three workflow runs while `publish` waited for four.
- Scope: change the `publish --min-runs` default to 3, synchronize the handover's description, attempt the additions host-eval suite and record its actual prerequisite failure.
- Shared package changed: no; no release or hosted update is required.

Verification:

- CLI argument check with publication stubbed (no GitHub mutation): baseline default 4; candidate default 3; explicit `--min-runs 5` remains 5. Three finished runs now satisfy the default count. This is a local argument check, not a new release publication.
- Canonical validator: PASS.
- `bash scripts/check_all.sh`: PASS, exit 0. Node: 238 total, 225 passed, 13 skipped, 0 failed. Python: 47 suites, 392 total, 381 passed, 11 skipped, 0 failed. Conditional skips include the unavailable Claude CLI, browser checks, optional GEPA dependency and optional print tooling; they are not behavior passes.
- Shared-package diff: empty; plugin version remains 1.98.0.
- Additions host eval: `python3 -B scripts/host_eval.py --suite additions --write` exited 2 with `host_eval: Claude Code (claude) is not installed`. AD01 to AD14: NOT_RUN, zero model calls, zero tokens, USD 0. No response or tool trace exists to evaluate `reads_any` or `skills_any`; routing defects remain Unknown. No package repair is justified by this attempt.
- Requested host: headless Claude Code; requested model: runner default `claude-sonnet-5-5`. Actual host version, model and reasoning setting: not_run. Running this script from Work would still test Claude Code, not GPT Astra. [Preflight record](../verification/host-evals/2026-10-20-1.98.0-additions-preflight.json).

Cross-host state and next step:

- GitHub publication target: `main`, fast-forward only; baseline rechecked before commit. The remote readback is reported separately after pushing this commit.
- ChatGPT Work: not_tracked; shared package unchanged.
- Codex: not_run (installed-plugin behavior); repository source checks above ran in the Work shell.
- Run additions on a host with authenticated Claude Code and available usage or an owner-authorized API key within the handover's budget. Record client, reasoning setting, tokens, time and cost; review actual failures before changing routing.
- Remote branch inventory before publication: `main`, `gh-pages`, and the existing `ccr-b6d36a1c-4hszow` session branch. That session branch is already an ancestor of the baseline `main`; preserved for its owning session.
- Correction (same entry): task 2 no longer asks ChatGPT Work to run `host_eval.py` (it needs the Claude Code CLI); it tests in its own sandbox, develops further, reviews orchestration and marks its commits `Origin-Agent: chatgpt-work`.

## CC-20261020-05: work order for a native Reel Editing Assistant

- Origin: cloud-code; package unchanged (1.98.0)
- Scope: `docs/task-reel-editing-assistant-2026-10-20.md` (analysis of two paid offers against Studio, work order for ChatGPT Work), pointer in the ChatGPT Work handover
- Verification: canonical validator
- GitHub: pending until pushed; ChatGPT Work: not_tracked; Codex: not_run

- Addendum CC-20261020-05: the work order now starts with an inventory of all editing tools, including those the owner attached to the plugin in another thread (not visible in `origin/main` at `4a11e2d`), and binds them into one pipeline.

- Addendum CC-20261020-05 (owner clarification): the other thread's tools exist only in the hosted ChatGPT plugin; the work order tells ChatGPT Work to compare the saved plugin with the repository, import hosted-only files with provenance and not to run a repository update over them before that.

## CW-20261020-CLOSURE

- Origin: chatgpt-work
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `9a028b7` (main, package 1.98.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.111.1)
- Package version: 1.98.0 -> 1.111.1
- Scope: Recovered text, audio, PDF, renderer and offline-probe fixes; redirect safety; consistent routing and release provenance; retained regression evidence.
- Shared package changed: yes; 25 changed, 0 added, 0 removed ([scope](../verification/scope-1.111.1.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 test_codex_install, 4 test_package_identity, 5 test_motion_benchmark, 6 test_host_smoke, 6 test_hosted_readback, 8 test_claude_plugin (1 skipped; see the suite log for reasons), 7 test_release, 8 test_gepa_studio_pilot (3 skipped; see the suite log for reasons), 23 asset_manifest, 17 captions, 24 environment_check, 26 motion_acceptance, 6 motion_fonts, 10 motion_kinds, 10 motion_variants, 7 skill_finder, 15 extensions, 11 animate_engine, 5 animate_voice, 15 static_render, 8 print_pdf, 2 reel_starters, 8 web_reach, 6 pl_copy_check, 14 image_probe, 11 quote_calc, 6 vo_budget, 4 edit_export, 4 board_compose, 4 sheet_export, 2 shot_plan_check, 2 prompt_pack, 3 clip_review, 5 svg_wordmark, 5 brand_guide, 4 motion_activity, 11 lyric_timing, 6 iso_glow, 13 sound_listen, 3 reference_breakdown, 12 craft_lint, 3 design_md, 6 ai_writing_check, 4 technique_atlas, 9 motion_assets, 2 knowledge_wiring, 22 test_host_eval: PASS ([record](../verification/release-1.111.1.json))

Cross-host state:

- GitHub: synchronized at released source `addf23e7`, tag `v1.111.1`. Release/source workflows passed; description correction `97c2eff1` passed and was read back without changing the assets. [Publication record](../verification/github-publication-1.111.1.json).
- ChatGPT Work saved plugin: synchronized, release `pluginrel_6ad76a03ef2081919bf42aed344dc562`; full 1543-file readback passes with one JSON formatting normalization and the private overlay preserved. [Record](../verification/hosted-sync-1.111.1.json). Fresh-client behavior: not_run.
- Codex: not_run

## CW-20261020-CLOSURE-PUBLICATION

- Origin: chatgpt-work; baseline `addf23e73400c0e17c3321a7020e98395e8932fc`; shared package unchanged (1.111.1).
- Trigger: the release and source workflows passed, but the description refresh rejected the root release-notes heading. Align that heading with its existing exact contract and add the verified source/tag record required by the description refresh. No tag or package replacement.
- Verification: downloaded plugin ZIP and inventory match the build; all 1505 ZIP files match the tag tree; GitHub asset digests match the player and canonical repository build. [Publication record](../verification/github-publication-1.111.1.json) preserves the original failed description run and the exact comparison method.
- Hosted plugin: already saved as 1.111.1 with a full archive readback; detailed synchronization record follows in the closure metadata commit. Fresh-client behavior and Codex installation: not_run.
- Description workflow: corrective run `39431106485` passed. API readback equals the corrected notes, with all asset IDs/digests and release identity unchanged. The original failed run remains recorded.

## CW-20261020-CLOSURE-RECORDS

- Origin: chatgpt-work; baseline `97c2eff13a4b8fefabad4b0ed9a49c0b7403989a`; shared package unchanged (1.111.1).
- Result: close publication and saved-plugin records, retain hosted affected-suite logs, correct the local skip explanation (one Claude CLI validation and three GEPA tests), and update the historical handover. Source-only prompt exercises are separately labelled and do not turn canonical host cases into passes.
- Verification: canonical validator PASS; all publication/readback comparisons above; repository-only metadata changed after the tested release. No paid provider calls or installed-client behavior claim.
- GitHub: this metadata commit follows the published release as a fast-forward on main. Hosted plugin is already synchronized; no redundant saved-plugin release for these root-only records. Codex installation: not_run.
- Branch inventory: main, gh-pages and the existing ccr-b6d36a1c-4hszow; ccr head daab5828 is an ancestor of the release. No new remote branches.
- Next work: Reel Editing Assistant remains the explicit next feature task, including careful hosted-only tool import review. Optional client reel mixing requires the owner's request and files.

## CW-20261020-SCENARIO-RECOVERY

- Origin: chatgpt-work; baseline `77b316a0cb2907111e9ea54b050fcf314be22f2a`; main-only, fast-forward publication.
- Trigger: the owner requested completion of the interrupted broad scenario review and a durable report/evidence archive. Only the early checkpoint survived; the claimed later 42+2 result was not recovered and is not evidence.
- Result: the commit carrying this entry. Shared package unchanged, version 1.111.1; no hosted update or private-overlay mutation.
- Scope: complete the replacement R01–R43 artifact exercises and explicit supporting Storytelling R44. Same-assistant, non-blind source-guided review: 41 PASS_SCOPED, 3 PASS_AFTER_REPAIR_SCOPED (R35 exact-frame extension, R40 relative export paths, R43 audio ID). These repair exercise outputs, not proven Studio instruction defects. [Report](../verification/scenario-closure-2026-10-20/REPORT.md) and [case findings](../verification/scenario-closure-2026-10-20/final-review.json).
- Evidence: full 816-file archive saved separately and verified by ZIP CRC plus every manifest hash; [archive record](../verification/scenario-closure-2026-10-20/archive-record.json). Public repository contains the report, frozen criteria, summary, measurements and source-check logs, not the complete media archive. All 137 recorded checkpoint-artifact hashes match. All 1505 candidate-package hashes match the baseline.
- Verification: canonical validator PASS; `bash scripts/check_all.sh` exit 0: Node 225 passed / 13 skipped, Python 401 passed / 4 skipped, zero failures. Real HyperFrames and Remotion renders, portable OTIO roundtrip, PCM/media measurements and selected frame inspection are recorded separately from source checks.
- Limits: fresh ChatGPT/Work/Codex behavior NOT_RUN; native OpenCut UI, paid providers and subjective audio listening NOT_RUN. R43 full fidelity checker remains not_verified while its wrong-price negative is detected. Optional extra DOM capture did not complete and is not evidence. Existing canonical host-evaluation statuses are unchanged.
- GitHub: publication target is main, guarded against the baseline; final publication readback is reported after the commit. ChatGPT Work saved package: prior synchronized 1.111.1 state is unchanged; no new hosted-state comparison. Codex installed behavior: not_run.
- Branch inventory: main, gh-pages and existing ccr-b6d36a1c-4hszow at daab5828, already merged into baseline main; no new branches and no branch deletion.

## CW-20261020-TOOL-INVENTORY

- Origin: chatgpt-work
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `d76de7f` (main, package 1.111.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.112.0)
- Package version: 1.111.1 -> 1.112.0
- Scope: Owner-requested 59-component first-install and every-update inventory; pre-install disclosure, isolated runtime/model evidence and independent host verification.
- Shared package changed: yes; 12 changed, 3 added, 0 removed ([scope](../verification/scope-1.112.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 test_codex_install, 4 test_package_identity, 5 test_motion_benchmark, 6 test_host_smoke, 6 test_hosted_readback, 8 test_claude_plugin (1 skipped; see the suite log for reasons), 7 test_release, 8 test_gepa_studio_pilot (3 skipped; see the suite log for reasons), 23 asset_manifest, 17 captions, 24 environment_check, 21 runtime_inventory, 26 motion_acceptance, 6 motion_fonts, 10 motion_kinds, 10 motion_variants, 7 skill_finder, 15 extensions, 11 animate_engine, 5 animate_voice, 15 static_render, 8 print_pdf, 2 reel_starters, 8 web_reach, 6 pl_copy_check, 14 image_probe, 11 quote_calc, 6 vo_budget, 4 edit_export, 4 board_compose, 4 sheet_export, 2 shot_plan_check, 2 prompt_pack, 3 clip_review, 5 svg_wordmark, 5 brand_guide, 4 motion_activity, 11 lyric_timing, 6 iso_glow, 13 sound_listen, 3 reference_breakdown, 12 craft_lint, 3 design_md, 6 ai_writing_check, 4 technique_atlas, 9 motion_assets, 2 knowledge_wiring, 22 test_host_eval: PASS ([record](../verification/release-1.112.0.json))

Cross-host state:

- GitHub: synchronized. Release source `e4bae6cfbab2a91715af9817e717d23753cdf4af`, published v1.112.0. Publication workflow passed; plugin, inventory and player asset digests match the local build, and all 1508 plugin files match the tag tree. Separate source workflow: still running at this readback (extra browser/GEPA coverage) ([record](../verification/github-publication-1.112.0.json)).
- ChatGPT Work: synchronized, saved version 1.112.0 / `pluginrel_6ad7c92acb7081919bd776b566bba6b6`; all 1559 files match the merged candidate, preserving private 1.111.2 integrations. Saved-package update probes pass 59/59. Fresh-client behavior not_run ([record](../verification/hosted-sync-1.112.0.json)).
- Codex: not_run

Publication follow-up preserves the executable bit of `scripts/check_all.sh` (unchanged file content). Remote branch `ccr-b6d36a1c-4hszow` is already merged into main and remains untouched under the owner-controlled deletion policy.

## CW-20261020-02: FrameCut research and implementation foundation

- Origin: chatgpt-work; baseline `45cab60d12f98663ce17fdc08cc753d5bfeef1cd`; main-only, fast-forward publication under current AGENTS.md.
- Trigger: the owner requested deep Internet/GitHub research and a proper foundation for FrameCut, a broad editing-and-motion mode with adaptive intake and finished-media delivery.
- Before: a historical Reel Editing Assistant work order against 1.98.0, separate editing/motion capabilities and no current FrameCut architecture or component-selection record.
- After: [foundation](framecut/README.md), research on 31 repositories with observed commits/license metadata, exact-time and revision contracts, integration map, three vertical workflows and 23 planned acceptance cases. Recommend extending the existing editing owner, preserving other craft owners, and testing a narrow Kinocut adapter before adoption. Proposed welcome token 5 preserves existing options 1–4. The module and menu are not implemented by this change.
- Shared package changed: no; version remains 1.112.0. No new runtime dependency, private-overlay publication, skill mutation or hosted release.
- Verification: canonical validator PASS; full `bash scripts/check_all.sh` exit 0, Node 225 passed / 13 skipped, Python 422 passed / 4 skipped, zero failures. Document links, 31 unique 40-character source pins, 23 planned cases and worked timing arithmetic checked. [Evidence](../verification/framecut-foundation-2026-10-20/checks.json) and full logs distinguish source checks from unexecuted FrameCut tests.
- GitHub: published as `ea6b8b593dc42a9b255e5177ec3d35796f9dea24` after the owner explicitly authorized publication and implementation. The earlier rejected attempt remains in the historical foundation evidence. Git had no write credentials; the authenticated GitHub connector published the identical tree `ad518ce5ba4897848daee32736dfccbde58a7e5e` with a guarded fast-forward. Local unpublished duplicates were reconciled by rebase, without changing their content. ChatGPT Work saved package: unchanged, no synchronization required for these repository-only documents. FrameCut media/client behavior in Work, ordinary ChatGPT, Codex and Claude: NOT_RUN.
- Branch inventory before publication: main, gh-pages and ccr-b6d36a1c-4hszow. The latter's daab5828 head is already an ancestor of main; preserved, with no new branches.

## CW-20261020-03

- Origin: chatgpt-work
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `ea6b8b5` (main, package 1.112.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.113.0)
- Package version: 1.112.0 -> 1.113.0
- Scope: Owner-requested FrameCut editing mode: adaptive intake, source analysis, exact editable timeline, captions/motion/audio, immutable revisions and verified delivery; welcome option 5 and single-owner orchestration.
- Shared package changed: yes; 26 changed, 8 added, 0 removed ([scope](../verification/scope-1.113.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 test_codex_install, 4 test_package_identity, 5 test_motion_benchmark, 6 test_host_smoke, 6 test_hosted_readback, 8 test_claude_plugin (1 skipped; see the suite log for reasons), 7 test_release, 8 test_gepa_studio_pilot (3 skipped; see the suite log for reasons), 23 asset_manifest, 17 captions, 24 environment_check, 21 runtime_inventory, 26 motion_acceptance, 6 motion_fonts, 10 motion_kinds, 10 motion_variants, 7 skill_finder, 15 extensions, 11 animate_engine, 5 animate_voice, 15 static_render, 8 print_pdf, 2 reel_starters, 8 web_reach, 6 pl_copy_check, 14 image_probe, 11 quote_calc, 6 vo_budget, 4 edit_export, 36 framecut, 4 board_compose, 4 sheet_export, 2 shot_plan_check, 2 prompt_pack, 3 clip_review, 5 svg_wordmark, 5 brand_guide, 4 motion_activity, 11 lyric_timing, 6 iso_glow, 13 sound_listen, 3 reference_breakdown, 12 craft_lint, 3 design_md, 6 ai_writing_check, 4 technique_atlas, 9 motion_assets, 2 knowledge_wiring, 22 test_host_eval: PASS ([record](../verification/release-1.113.0.json))

Cross-host state:

- GitHub: published source `50f7357e550c877869b70a2551da7790f2610ecc`, v1.113.0 and six digest-verified assets; 1516/1516 plugin ZIP files match the tag tree. Authenticated connector fast-forwarded main with an expected-head guard; local duplicate reconciled by rebase. [Publication](../verification/github-publication-1.113.0.json).
- ChatGPT Work: synchronized saved release `pluginrel_6ad7e42f10f0819194506d3275c23ae0`, all 1567 files equal the merged candidate. Private integrations retained. Saved validator, 36 FrameCut tests and 59/59 installation probes pass. [Readback](../verification/hosted-sync-1.113.0.json). Fresh clients NOT_RUN.
- Codex: not_run

- Publication follow-up: corrected the repository-only release-notes heading after the refresh job exposed its exact format requirement. This does not change the shared package or require another hosted release. The original source/full gates remain the evidence for unchanged executable code.

## CW-20261021-01: owner-requested Sunra MCP removal

- Origin: chatgpt-work; baseline `96f8e97a160c22dcd1d359cf708aedaa7c58013b`; main only.
- Trigger: the owner could not select Studio with @ on a phone and explicitly requested removal of Sunra MCP from the repository and saved plugin. The relationship between MCP configuration and the mobile symptom is not proven.
- Before: public source 1.113.0 has no tracked Sunra configuration. The private installation contains portable and compatibility MCP configuration plus instructions requiring its preservation.
- After: saved plugin 1.113.1, release `pluginrel_6ad843091764819193d01632b1c263ee`; both MCP files and their manifest binding removed. Routing, setup instructions and the continuity check respect the retirement. PoYo, the separate Sunra API route, App identity and all local runtime recipes remain preserved. No credentials or private configuration were published.
- Public package changed: no; source version remains 1.113.0. Repository-only update guidance and records distinguish the newer private overlay. No redundant public release.
- Verification: all 12 changed files and the retained App binding match readback; full inventory confirms exactly two removals, 1565 retained files, no additions. Source and candidate canonical validation pass. Connection retirement and unrelated App-loss checks pass; motion/media/engine preservation checks pass within the authorized removal scope. Full repository suite passed: 225 Node tests passed, 13 skipped; 450 Python tests passed, 12 skipped.
- Runtime inventory: 19 of 59 components detected, 40 missing in this current sandbox; earlier supplemental runtime/cache paths are absent. This change preserves their plugin configuration and restoration recipes. No runtime reinstall or paid provider call was performed.
- GitHub: this records-only commit is published with an expected-head guard; the final commit is reported after readback. Mobile @ invocation and other fresh clients: NOT_RUN; service search still returns no FrameCore match.
- Evidence: [removal and preservation checks](../verification/sunra-mcp-removal-2026-10-21.json).

## CW-20261021-02

- Origin: chatgpt-work
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `1628bc0` (main, package 1.113.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.114.0)
- Package version: 1.113.0 -> 1.114.0
- Scope: Owner-requested FrameCut audit: novice onboarding with light teaching, reusable working agreement, staged finishing, clear cutdown ownership, checked motion returns and separate delivery readiness.
- Shared package changed: yes; 16 changed, 0 added, 0 removed ([scope](../verification/scope-1.114.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 test_codex_install, 4 test_package_identity, 5 test_motion_benchmark, 6 test_host_smoke, 6 test_hosted_readback, 8 test_claude_plugin (1 skipped; see the suite log for reasons), 7 test_release, 8 test_gepa_studio_pilot (3 skipped; see the suite log for reasons), 23 asset_manifest, 17 captions, 24 environment_check, 21 runtime_inventory, 26 motion_acceptance, 6 motion_fonts, 10 motion_kinds, 10 motion_variants, 7 skill_finder, 15 extensions, 11 animate_engine, 5 animate_voice, 15 static_render, 8 print_pdf (8 skipped; see the suite log for reasons), 2 reel_starters, 8 web_reach, 6 pl_copy_check, 14 image_probe, 11 quote_calc, 6 vo_budget, 4 edit_export, 43 framecut, 4 board_compose, 4 sheet_export, 2 shot_plan_check, 2 prompt_pack, 3 clip_review, 5 svg_wordmark, 5 brand_guide, 4 motion_activity, 11 lyric_timing, 6 iso_glow, 13 sound_listen, 3 reference_breakdown, 12 craft_lint, 3 design_md, 6 ai_writing_check, 4 technique_atlas, 9 motion_assets, 2 knowledge_wiring, 22 test_host_eval: PASS ([record](../verification/release-1.114.0.json))

Cross-host state:

- GitHub: source `120a865f3c079fc700ecb9ea06eb661de03ec4a8`, tag v1.114.0 and six digest-verified release assets published. 1516 plugin ZIP files match the source tree. [Publication](../verification/github-publication-1.114.0.json).
- ChatGPT Work: synchronized saved 1.114.0, release `pluginrel_6ad8572ec58081919c4301f651d0b0c8`. All changed files verified; generated Codex manifest has equivalent Unicode escaping. Complete inventory remains 1565 paths; App/runtime integrations and Sunra MCP retirement preserved. [Readback](../verification/hosted-sync-1.114.0.json). Fresh-client behavior NOT_RUN.
- Codex: not_run

- Audit details: [five dialogue exercises and runtime before/after evidence](../verification/framecut-review-2026-10-21.json). The two baseline conversations were already helpful; no fabricated failure or statistical improvement claim. Seven executable regressions cover returned motion and review state. The owner subsequently reported mobile @ working on 1.113.1 (PASS_REPORTED), separately from this release.

## CW-20261021-03

- Origin: chatgpt-work
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `f5b9205` (main, package 1.114.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.115.0)
- Package version: 1.114.0 -> 1.115.0
- Scope: Owner-requested FrameCut workflow: adaptive onboarding, full-film visual storyboards/contact sheets, user feedback and corrected-board acceptance before final rendering; video samples optional on request.
- Shared package changed: yes; 17 changed, 0 added, 0 removed ([scope](../verification/scope-1.115.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 test_codex_install, 4 test_package_identity, 5 test_motion_benchmark, 6 test_host_smoke, 6 test_hosted_readback, 8 test_claude_plugin (1 skipped; see the suite log for reasons), 7 test_release, 8 test_gepa_studio_pilot (3 skipped; see the suite log for reasons), 23 asset_manifest, 17 captions, 24 environment_check, 21 runtime_inventory, 26 motion_acceptance, 6 motion_fonts, 10 motion_kinds, 10 motion_variants, 7 skill_finder, 15 extensions, 11 animate_engine, 5 animate_voice, 15 static_render, 8 print_pdf (8 skipped; see the suite log for reasons), 2 reel_starters, 8 web_reach, 6 pl_copy_check, 14 image_probe, 11 quote_calc, 6 vo_budget, 4 edit_export, 43 framecut, 4 board_compose, 4 sheet_export, 2 shot_plan_check, 2 prompt_pack, 3 clip_review, 5 svg_wordmark, 5 brand_guide, 4 motion_activity, 11 lyric_timing, 6 iso_glow, 13 sound_listen, 3 reference_breakdown, 12 craft_lint, 3 design_md, 6 ai_writing_check, 4 technique_atlas, 9 motion_assets, 2 knowledge_wiring, 22 test_host_eval: PASS ([record](../verification/release-1.115.0.json))

Cross-host state:

- GitHub: synchronized source `aea1191742f5ae2747610a8a9e8625cfd4217037`, published v1.115.0. Release workflow 39566291015 and source checks 39566290875 passed. All six downloaded assets verified; 1516 plugin files and 2184 repository files match the source tree. The repository ZIP differs from the local ZIP only in its checkout-directory prefix; normalized content is verified. Description-refresh correction `732ae4b` passed workflow 39567350696 and release-body readback. [Publication](../verification/github-publication-1.115.0.json).
- ChatGPT Work: synchronized saved 1.115.0 / `pluginrel_6ad871c551e081918f643baaaeb5b3bc`, after repository source `aea1191742f5ae2747610a8a9e8625cfd4217037` was published and read back. All 17 affected files verified (16 byte-identical, Codex manifest JSON-equivalent); App binding and all 1565 paths preserved, including private integrations and Sunra MCP retirement. [Readback](../verification/hosted-sync-1.115.0.json). Fresh-client behavior NOT_RUN.
- Codex: not_run


Publication follow-up: the description-refresh workflow initially rejected the release-notes heading because it expects the exact `# Creative Studio 1.115.0` prefix. The repository-only correction changes that heading and retains the release tag/assets; the failure and corrected run are recorded separately. The shared package is unchanged and needs no second hosted update. Git write credentials were unavailable; the authenticated connector published the tested identical tree with a guarded fast-forward. Local preparatory commits were reconciled to that remote tree without changing source content.

Final branch inventory: `main`, `gh-pages`, and existing `ccr-b6d36a1c-4hszow` at `daab5828bdd4025280ebe2af5f5d5cccacae4a5c`. The latter is already merged into main and remains untouched. No branches created or deleted.

## CW-20261021-04: Claude Code handover and owner testing pause

- Origin: chatgpt-work.
- Baseline: `06edb3c92d55f5395cf0a63988a7dd11ad80063a`, `main`; result: the documentation commit carrying this entry.
- Trigger: the owner paused development to test FrameCut, Motion Graphics and other modules, and requested a repository handover to Claude covering work since yesterday.
- Scope: [2026-10-20 to 2026-10-21 handover](handover-chatgpt-work-2026-10-21.md), current pause instruction in AGENTS.md and roadmap discoverability. Consolidates audit/scenario recovery, tool inventory, FrameCut releases, private MCP retirement, source and saved-plugin verification, outstanding client limits and continuation rules.
- Shared package changed: no. Public and last verified saved versions remain 1.115.0; no release, integration installation or hosted update is part of this documentation task.
- Verification: canonical validator PASS; full `bash scripts/check_all.sh` PASS, 225 Node tests passed / 13 skipped and 457 Python tests passed / 12 skipped across 49 Python suites. All 43 FrameCut tests passed. No test code added. Reviewed 27 handover relative links and nine explicit code-map paths; all resolve. `git diff --check` PASS; no shared-package diff.
- GitHub: publish this documentation commit directly to main with an expected-head guard, then read back the identical tree. The final commit SHA is reported after publication.
- ChatGPT Work: existing saved 1.115.0 / `pluginrel_6ad871c551e081918f643baaaeb5b3bc` remains unchanged; its affected-file readback is in the prior release record. No new installed-client test.
- Codex and Claude: no installation or fresh-client test in this handover task; NOT_RUN remains NOT_RUN.
- Owner testing is the next step. Do not automatically resume old work orders or implement partial research acceptance rows.
- Branch inventory: main and gh-pages plus existing `ccr-b6d36a1c-4hszow` at `daab5828bdd4025280ebe2af5f5d5cccacae4a5c`, already merged into main; preserve it. No new branch or deletion.

## CW-20261021-05

- Origin: chatgpt-work
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `c700ad2` (main, package 1.115.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.116.0)
- Package version: 1.115.0 -> 1.116.0
- Scope: Owner-requested native FrameCut development: composited full storyboards, transactional editing, durable jobs, keyframes/framing, freeze/speed ramps and versioned effects, with existing onboarding and storyboard approval orchestration preserved.
- Shared package changed: yes; 19 changed, 17 added, 0 removed ([scope](../verification/scope-1.116.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 test_codex_install, 4 test_package_identity, 5 test_motion_benchmark, 6 test_host_smoke, 6 test_hosted_readback, 8 test_claude_plugin (1 skipped; see the suite log for reasons), 7 test_release, 8 test_gepa_studio_pilot (3 skipped; see the suite log for reasons), 23 asset_manifest, 17 captions, 24 environment_check, 21 runtime_inventory, 26 motion_acceptance, 6 motion_fonts, 10 motion_kinds, 10 motion_variants, 7 skill_finder, 15 extensions, 11 animate_engine, 5 animate_voice, 15 static_render, 8 print_pdf (8 skipped; see the suite log for reasons), 2 reel_starters, 8 web_reach, 6 pl_copy_check, 14 image_probe, 11 quote_calc, 6 vo_budget, 4 edit_export, 43 framecut, 20 framecut_development, 4 board_compose, 4 sheet_export, 2 shot_plan_check, 2 prompt_pack, 3 clip_review, 5 svg_wordmark, 5 brand_guide, 4 motion_activity, 11 lyric_timing, 6 iso_glow, 13 sound_listen, 3 reference_breakdown, 12 craft_lint, 3 design_md, 6 ai_writing_check, 4 technique_atlas, 9 motion_assets, 2 knowledge_wiring, 22 test_host_eval: PASS ([record](../verification/release-1.116.0.json))

Cross-host state:

- GitHub: synchronized. Release source `047d65ce6feae54bb97592e80e40efe1b899c1db`, tag `v1.116.0`; workflows 39595390264, 39595390287 and 39595390330 succeeded. Six downloaded assets verified; 1533 plugin files and 2209 repository files match the source tree. Source CI: 236 Node passes / 2 skipped, 481 Python passes / 8 skipped; all 63 FrameCut tests ran. Strict Claude manifest validation passes in CI. [Publication](../verification/github-publication-1.116.0.json).
- ChatGPT Work: synchronized at saved-package level. Source `047d65ce6feae54bb97592e80e40efe1b899c1db`; hosted 1.116.0 / `pluginrel_6ad8a7f7bbac8191b9f207b9e39a4ee9`. All 36 updated paths are byte-identical to the candidate retaining seven existing private overlays; all 1582 paths retained as expected. App binding unchanged; retired Sunra MCP paths absent. [Readback](../verification/hosted-sync-1.116.0.json). Fresh installed-client behavior remains NOT_RUN.
- Codex: not_run

## CW-20261021-06

- Origin: chatgpt-work
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `342759e` (main, package 1.116.0); full SHA in the commit trailer
- Result: `868bc6ac3dec179141e292c0097c6e0fb52d01cf` (package 1.117.0); this documentation-only follow-up records publication and saved-plugin verification
- Package version: 1.116.0 -> 1.117.0
- Scope: Owner-requested supplemental motion/data/taste knowledge: source-bound visual arguments, revision-bound feedback, evidence-led creative judgment and scoped preferences connected to existing owners, preserving FrameCut full-board acceptance and private integrations.
- Shared package changed: yes; 18 changed, 1 added, 0 removed ([scope](../verification/scope-1.117.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 test_codex_install, 4 test_package_identity, 5 test_motion_benchmark, 6 test_host_smoke, 6 test_hosted_readback, 8 test_claude_plugin (1 skipped; see the suite log for reasons), 7 test_release, 8 test_gepa_studio_pilot (3 skipped; see the suite log for reasons), 23 asset_manifest, 17 captions, 24 environment_check, 21 runtime_inventory, 26 motion_acceptance, 6 motion_fonts, 10 motion_kinds, 10 motion_variants, 7 skill_finder, 15 extensions, 11 animate_engine, 5 animate_voice, 15 static_render, 8 print_pdf (8 skipped; see the suite log for reasons), 2 reel_starters, 8 web_reach, 6 pl_copy_check, 14 image_probe, 11 quote_calc, 6 vo_budget, 4 edit_export, 43 framecut, 20 framecut_development, 4 board_compose, 4 sheet_export, 2 shot_plan_check, 2 prompt_pack, 3 clip_review, 5 svg_wordmark, 5 brand_guide, 4 motion_activity, 11 lyric_timing, 6 iso_glow, 13 sound_listen, 3 reference_breakdown, 12 craft_lint, 3 design_md, 6 ai_writing_check, 4 technique_atlas, 9 motion_assets, 2 knowledge_wiring, 22 test_host_eval: PASS ([record](../verification/release-1.117.0.json))

Cross-host state:

- GitHub: synchronized. Source `868bc6ac3dec179141e292c0097c6e0fb52d01cf`, tag `v1.117.0`; source and publication workflows succeeded. Six downloaded assets verified against their digests and checksums; 1534 plugin files and 2223 repository files match the source tree. [Publication](../verification/github-publication-1.117.0.json).
- ChatGPT Work: synchronized at saved-package level. Hosted 1.117.0 / `pluginrel_6ad8b55506248191b140981560a9921a`. All 19 updated paths compared: 18 byte-identical; the Codex manifest has service-normalized formatting and identical parsed JSON. Eight existing private overlays preserved; complete 1583-path inventory as expected. App binding unchanged; omitted-file sizes unchanged. [Readback](../verification/hosted-sync-1.117.0.json). Fresh installed-client behavior remains NOT_RUN.
- Codex: not_run

Supplemental knowledge verification: [two fresh-context source-guided tasks](../verification/creative-knowledge-2026-10-21.json) passed within their textual scope, with raw artifacts retained and independent arithmetic/event mapping checks. This is not fresh installed-client behavior or visual-media QA.

Branch inventory at publication: only `main`, `gh-pages` and pre-existing `ccr-b6d36a1c-4hszow` (`daab5828bdd4025280ebe2af5f5d5cccacae4a5c`, already merged into source `868bc6a`). No branch created or deleted.

## CW-20261021-07

- Origin: chatgpt-work
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `7459f77` (main, package 1.117.0); full SHA in the commit trailer
- Result: `a25d8ea202853f5bdbc9121336c136569d98bf04` (package 1.118.0); this documentation-only follow-up records publication and saved-plugin verification
- Package version: 1.117.0 -> 1.118.0
- Scope: Owner-requested Adobe-derived skill knowledge without Adobe accounts or services: format variants, batches, local fonts/templates, website and document evidence, supplied-data reasoning and editorial selection connected to existing owners.
- Shared package changed: yes; 19 changed, 3 added, 0 removed ([scope](../verification/scope-1.118.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 test_codex_install, 4 test_package_identity, 5 test_motion_benchmark, 6 test_host_smoke, 6 test_hosted_readback, 8 test_claude_plugin (1 skipped; see the suite log for reasons), 7 test_release, 8 test_gepa_studio_pilot (3 skipped; see the suite log for reasons), 23 asset_manifest, 17 captions, 24 environment_check, 21 runtime_inventory, 26 motion_acceptance, 6 motion_fonts, 10 motion_kinds, 10 motion_variants, 7 skill_finder, 15 extensions, 11 animate_engine, 5 animate_voice, 15 static_render, 8 print_pdf (8 skipped; see the suite log for reasons), 2 reel_starters, 8 web_reach, 6 pl_copy_check, 14 image_probe, 11 quote_calc, 6 vo_budget, 4 edit_export, 43 framecut, 20 framecut_development, 4 board_compose, 4 sheet_export, 2 shot_plan_check, 2 prompt_pack, 3 clip_review, 5 svg_wordmark, 5 brand_guide, 4 motion_activity, 11 lyric_timing, 6 iso_glow, 13 sound_listen, 3 reference_breakdown, 12 craft_lint, 3 design_md, 6 ai_writing_check, 4 technique_atlas, 9 motion_assets, 2 knowledge_wiring, 22 test_host_eval: PASS ([record](../verification/release-1.118.0.json))

Cross-host state:

- GitHub: synchronized. Source `a25d8ea202853f5bdbc9121336c136569d98bf04`, tag `v1.118.0`; source and publication workflows succeeded. Six downloaded assets verified against digests/checksums; 1537 plugin files and 2234 repository files match source. [Publication](../verification/github-publication-1.118.0.json).
- ChatGPT Work: synchronized at saved-package level. Hosted 1.118.0 / `pluginrel_6ad8e429a09881918b92de48cd768fc7`; 21 updated files byte-identical; the Codex manifest has service-normalized formatting and identical parsed JSON. 9 existing private overlays preserved. Complete 1586-path inventory as expected, App binding unchanged and omitted-file sizes unchanged. [Readback](../verification/hosted-sync-1.118.0.json). Fresh installed-client behavior remains NOT_RUN.
- Codex: not_run

Account-free knowledge verification: [two fresh-context source-guided tasks](../verification/adobe-account-free-2026-10-21.json) passed within their textual scope. Raw replies and independent geometry, timing and growth checks are retained. No Adobe services were invoked; installed-client retrieval and new media quality remain NOT_RUN.

The description-refresh workflow exposed an incorrect release-notes heading in the source commit (run `39632355483`). This documentation-only follow-up corrects it to the workflow’s required `# Creative Studio 1.118.0`; the package and hosted release stay unchanged.

Branch inventory at publication: only `main`, `gh-pages` and pre-existing `ccr-b6d36a1c-4hszow` (`daab5828bdd4025280ebe2af5f5d5cccacae4a5c`, already merged into source `a25d8ea`). No branch created or deleted.

## CC-20261021-01

- Origin: cloud-code
- Branch: `main` (session branch `ccr-06247e92-aihwc6` kept equal to it)
- Baseline: `5a3645a` (main, package 1.118.0); full SHA in the commit trailer
- Result: the commit carrying this entry; no release (repository documentation only)
- Package version: 1.118.0 (unchanged)
- Scope: owner request 2026-10-21 after the repository analysis: AGENTS.md opens with one consolidated "Current rules" section (development state, branches, releases and the hosted plugin with its private overlay, evidence, budgets); the superseded dated sections moved word for word to `docs/agents-history.md`; CLAUDE.md points to the current rules; the roadmap opens with the current direction and keeps the earlier text as history
- Shared package changed: no

Verification:

- canonical validator: PASS; no test reads AGENTS.md or the roadmap

Cross-host state:

- GitHub: pushed to `main`
- ChatGPT Work: no package change
- Codex: not_run

## CC-20261021-02

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `657bff9` (main, package 1.118.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.119.0)
- Package version: 1.118.0 -> 1.119.0
- Scope: Trigger: the owner's verdict on the 2026-10-16 shoemaker test reel. Reel plans apply a stopping test and a picture rule where reel requests route; acceptance binds HyperFrames/hand-written compositions (--composition, --copy, --motion-activity bound to the encoded file); a marked landing is never silent; the orchestrator's coordination detail moved verbatim to routing-boundaries.md (about 930 bytes freed, startup unchanged). Before/after: motion_acceptance_test (3 errors on 1.118.0, OK), motion_sound_marked_test (fails on 1.118.0, OK).
- Shared package changed: yes; 21 changed, 1 added, 0 removed ([scope](../verification/scope-1.119.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 15 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22, 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 4 suite 32, 4 suite 33, 2 suite 34, 2 suite 35, 3 suite 36, 5 suite 37 (5 skipped; see the suite log for reasons), 5 suite 38, 4 suite 39, 11 suite 40, 6 suite 41, 13 suite 42, 3 suite 43, 12 suite 44, 3 suite 45, 6 suite 46, 4 suite 47, 9 suite 48, 2 suite 49, 2 suite 50, 22 suite 51: PASS ([record](../verification/release-1.119.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `bc6d4eb`; workflows Check Studio sources 39674902113, Refresh current release notes 39674898850, Publish verified Studio release 39674899003, Check Studio sources 39674898901: success; [v1.119.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.119.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1538 of 1538) ([record](../verification/github-publication-1.119.0.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261021-03

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `37267d2` (main, package 1.119.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.119.1)
- Package version: 1.119.0 -> 1.119.1
- Scope: Trigger: host evaluation G12 on 1.119.0 reproduced the owner's 2026-10-16 reel defect at the orchestrator. The orchestrator now loads Motion Graphics Workflow for service/product/before-and-after reels with the picture rule and first-second test; G12 meets its checks after the fix. AD01 expects English for a bare option number. Host-eval pass: 7 case runs, about 632k tokens, 241 s.
- Shared package changed: yes; 7 changed, 0 added, 0 removed ([scope](../verification/scope-1.119.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 15 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22, 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 4 suite 32, 4 suite 33, 2 suite 34, 2 suite 35, 3 suite 36, 5 suite 37 (5 skipped; see the suite log for reasons), 5 suite 38, 4 suite 39, 11 suite 40, 6 suite 41, 13 suite 42, 3 suite 43, 12 suite 44, 3 suite 45, 6 suite 46, 4 suite 47, 9 suite 48, 2 suite 49, 2 suite 50, 22 suite 51: PASS ([record](../verification/release-1.119.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `24c964f`; workflows Check Studio sources 39679845948, Publish verified Studio release 39679842301, Refresh current release notes 39679842154, Check Studio sources 39679842104: success; [v1.119.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.119.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1538 of 1538) ([record](../verification/github-publication-1.119.1.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-01

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `705f0b7` (main, package 1.119.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.119.2)
- Package version: 1.119.1 -> 1.119.2
- Scope: Trigger: the owner's request to check FrameCut thoroughly. Four independent reviews found defects in 1.119.1; the fixed ones were reproduced and have tests that fail on 1.119.1 (captions, timing, analysis, audio shift, revision size, probe validation, readiness, export injection, cache, locks, signals, paths). Seven product decisions and lower-priority findings are in docs/framecut/audit-2026-10-22.md.
- Shared package changed: yes; 17 changed, 1 added, 0 removed ([scope](../verification/scope-1.119.2.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 15 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22, 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 24 suite 32, 4 suite 33, 4 suite 34, 2 suite 35, 2 suite 36, 3 suite 37, 5 suite 38 (5 skipped; see the suite log for reasons), 5 suite 39, 4 suite 40, 11 suite 41, 6 suite 42, 13 suite 43, 3 suite 44, 12 suite 45, 3 suite 46, 6 suite 47, 4 suite 48, 9 suite 49, 2 suite 50, 2 suite 51, 22 suite 52: PASS ([record](../verification/release-1.119.2.json))

Cross-host state:

- GitHub: synchronized. `main` at `c9e24c9`; workflows Check Studio sources 39730215243, Check Studio sources 39730214055, Refresh current release notes 39730213955, Publish verified Studio release 39730213991: success; [v1.119.2](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.119.2) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1539 of 1539) ([record](../verification/github-publication-1.119.2.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-02

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `96bfb7d` (main, package 1.119.2); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.119.3)
- Package version: 1.119.2 -> 1.119.3
- Scope: Trigger: owner decisions on the FrameCut audit. Music is lowered 6 dB under speech by default, following the timed transcript with smooth ramps; the storyboard stays a one-time host-managed preview. Measured about -6 dB under words and full level in pauses.
- Shared package changed: yes; 11 changed, 0 added, 0 removed ([scope](../verification/scope-1.119.3.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 15 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22, 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 4 suite 33, 4 suite 34, 2 suite 35, 2 suite 36, 3 suite 37, 5 suite 38 (5 skipped; see the suite log for reasons), 5 suite 39, 4 suite 40, 11 suite 41, 6 suite 42, 13 suite 43, 3 suite 44, 12 suite 45, 3 suite 46, 6 suite 47, 4 suite 48, 9 suite 49, 2 suite 50, 2 suite 51, 22 suite 52: PASS ([record](../verification/release-1.119.3.json))

Cross-host state:

- GitHub: synchronized. `main` at `30e2f73`; workflows Check Studio sources 39735186246, Refresh current release notes 39735183320, Check Studio sources 39735183396, Publish verified Studio release 39735183349: success; [v1.119.3](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.119.3) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1539 of 1539) ([record](../verification/github-publication-1.119.3.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-03

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `e7587bf` (main, package 1.119.3); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.119.4)
- Package version: 1.119.3 -> 1.119.4
- Scope: Trigger: the owner sent MoneyPrinterTurbo for review. Registry entry pinned to 6992380 and mpt 1.3.9, native in Codex and Claude Code, with a decision map, licence and rights notes. Static review, hashes, dry-run plan and install ran; the program itself was not run.
- Shared package changed: yes; 8 changed, 2 added, 0 removed ([scope](../verification/scope-1.119.4.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 15 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22, 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 4 suite 33, 4 suite 34, 2 suite 35, 2 suite 36, 3 suite 37, 5 suite 38 (5 skipped; see the suite log for reasons), 5 suite 39, 4 suite 40, 11 suite 41, 6 suite 42, 13 suite 43, 3 suite 44, 12 suite 45, 3 suite 46, 6 suite 47, 4 suite 48, 9 suite 49, 2 suite 50, 2 suite 51, 22 suite 52: PASS ([record](../verification/release-1.119.4.json))

Cross-host state:

- GitHub: synchronized. `main` at `e057a83`; workflows Check Studio sources 39746912599, Publish verified Studio release 39746909345, Check Studio sources 39746909218, Refresh current release notes 39746909073: success; [v1.119.4](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.119.4) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1541 of 1541) ([record](../verification/github-publication-1.119.4.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-04

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `45b4bf7` (main, package 1.119.4); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.119.5)
- Package version: 1.119.4 -> 1.119.5
- Scope: Trigger: the owner observations from real use. Replies no longer quote Studio files or rules; FrameCut and Motion Graphics aim for the strongest result and offer a missing add-on once, installed only after the user agrees. G14 before/after recorded; ChatGPT behavior NOT_RUN.
- Shared package changed: yes; 10 changed, 0 added, 0 removed ([scope](../verification/scope-1.119.5.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 15 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22, 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 4 suite 33, 4 suite 34, 2 suite 35, 2 suite 36, 3 suite 37, 5 suite 38 (5 skipped; see the suite log for reasons), 5 suite 39, 4 suite 40, 11 suite 41, 6 suite 42, 13 suite 43, 3 suite 44, 12 suite 45, 3 suite 46, 6 suite 47, 4 suite 48, 9 suite 49, 2 suite 50, 2 suite 51, 22 suite 52: PASS ([record](../verification/release-1.119.5.json))

Cross-host state:

- GitHub: synchronized. `main` at `5a49560`; workflows Check Studio sources 39759930750, Publish verified Studio release 39759927082, Refresh current release notes 39759927029, Check Studio sources 39759927015: success; [v1.119.5](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.119.5) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1541 of 1541) ([record](../verification/github-publication-1.119.5.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-05

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `910cf08` (main, package 1.119.5); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.120.0)
- Package version: 1.119.5 -> 1.120.0
- Scope: Trigger: the owner asked for the best ideas from MoneyPrinterTurbo. Three methods adapted and verified offline: align-script (script spelling, speech timing, coverage report), caption cues through Caption Studio cut rules, and the blocking font_missing_glyphs warning. Tests fail before and pass after; no code copied.
- Shared package changed: yes; 13 changed, 2 added, 0 removed ([scope](../verification/scope-1.120.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 15 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22, 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 11 suite 33, 4 suite 34, 4 suite 35, 2 suite 36, 2 suite 37, 3 suite 38, 5 suite 39 (5 skipped; see the suite log for reasons), 5 suite 40, 4 suite 41, 11 suite 42, 6 suite 43, 13 suite 44, 3 suite 45, 12 suite 46, 3 suite 47, 6 suite 48, 4 suite 49, 9 suite 50, 2 suite 51, 2 suite 52, 22 suite 53: PASS ([record](../verification/release-1.120.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `0ba0c81`; workflows Check Studio sources 39765309990, Refresh current release notes 39765306211, Publish verified Studio release 39765306361, Check Studio sources 39765306195: success; [v1.120.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.120.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1543 of 1543) ([record](../verification/github-publication-1.120.0.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-06

- Origin: cloud-code
- Branch: `ccr-06247e92-aihwc6`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `9263bb2` (main, package 1.120.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.121.0)
- Package version: 1.120.0 -> 1.121.0
- Scope: Trigger: the owner sent Pixel Plugin and asked to mine it first. Added FrameCut effects pixelate, posterize and ordered_dither, Pixel look guidance in the Animate reference and a pixel-plugin registry entry; the plugin itself was not run.
- Shared package changed: yes; 12 changed, 6 added, 0 removed ([scope](../verification/scope-1.121.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there and run separately: 85 passing in the browser run), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 15 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22, 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 11 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 11 suite 43, 6 suite 44, 13 suite 45, 3 suite 46, 12 suite 47, 3 suite 48, 6 suite 49, 4 suite 50, 9 suite 51, 2 suite 52, 2 suite 53, 22 suite 54: PASS ([record](../verification/release-1.121.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `8274d37`; workflows Check Studio sources 39771713217, Refresh current release notes 39771710670, Publish verified Studio release 39771710772, Check Studio sources 39771710650: success; [v1.121.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.121.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1549 of 1549) ([record](../verification/github-publication-1.121.0.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CW-20261022-01

- Origin: chatgpt-work
- Trigger: the owner's 2026-10-22 request for temporary takeover from Claude and a separate branch establishing a Superpowers companion integration.
- Branch: `cw/superpowers-companion-foundation-2026-10-22`, explicitly requested; no merge into main.
- Baseline: `b92b45b227dc667934c81080afebcdd3c0163b29`
- Result: the commit carrying this entry; repository-only foundation for owner review.
- Package version: 1.121.0 unchanged. Shared package changed: no.
- Scope: [takeover](handover-chatgpt-work-2026-10-22-superpowers.md), [proposed architecture](superpowers/specs/2026-10-22-studio-companion-design.md), dated branch exception, roadmap and verification evidence. Superpowers remains separately installed, first recommended during Studio installation; all 37 owners have a defined support boundary. Public routing and installation changes are not implemented in this foundation.
- Parallel work: saved native Studio 1.119.7 already contains a Superpowers reference, 12 stored cases and six direct entry links. Read without modification; private overlay stays private. Claude's Open Design plan remains unexecuted here.

Verification:

- Canonical validator: PASS, 37 owners and 1,549 package files; description budget warning at 7,700/7,800 characters.
- Full `bash scripts/check_all.sh`: exit 0; Node 225 passed, 13 skipped, zero failures; Python 54 suites / 541 collected, 12 skipped, zero failures. Skips and host limits remain explicit in the [record](../verification/superpowers-foundation-2026-10-22.json).
- Spec self-review and focused documentation checks: all 37 owners exactly once, relative links resolve, shared-package diff empty.
- New companion behavior scenarios: 18 proposed, NOT_RUN. Fresh installed-client behavior: NOT_RUN. Source verification does not establish host behavior.

Cross-host state:

- GitHub: synchronized on the dedicated branch. Foundation commit `734fd72a1c5ee3b71f8699e6735f662bd4b17082` was read back from the remote; its complete tree matches the verified local tree. Main remains at the inspected baseline. See the [branch publication record](../verification/superpowers-foundation-publication-2026-10-22.json).
- ChatGPT Work: not_run for a new release; the existing hosted package was inspected only, and the installed Superpowers process skills were used in this conversation.
- Codex: not_run for installed-client integration.
- Branch hygiene: the three existing `ccr-*` branches are already contained in baseline main; preserved for the owner. `gh-pages` preserved.

## CW-20261022-02

- Origin: chatgpt-work
- Branch: `cw/superpowers-companion-foundation-2026-10-22`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `b92b45b` (main, package 1.121.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.122.0)
- Package version: 1.121.0 -> 1.122.0
- Scope: Owner-approved Superpowers companion: first manual catalog recommendation, existing-orchestrator setup, shared native routing and revision-bound support; Studio keeps creative ownership and approvals.
- Shared package changed: yes; 26 changed, 3 added, 0 removed ([scope](../verification/scope-1.122.0.json))

Verification:

- canonical validator: PASS
- `scripts/check_all.sh`: 238 Node tests (225 passing, 13 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6 (1 skipped; see the suite log for reasons), 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 21 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 11 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40, 5 suite 41, 4 suite 42, 11 suite 43, 6 suite 44, 13 suite 45, 3 suite 46, 12 suite 47, 3 suite 48, 6 suite 49, 4 suite 50, 9 suite 51, 2 suite 52, 2 suite 53, 22 suite 54: PASS ([record](../verification/release-1.122.0.json))

Cross-host state:

- GitHub: synchronized. Release source `fce01e2fdb9e3faec744e2965eba687f14c3c9d7`, tag v1.122.0; all 1,552 package files match downloaded tag assets. Notes-only CI correction `a2c09584b51a23d8d2d5db32cffbaf220216b492` leaves package bytes unchanged. Release workflow PASS; additional source checks retain their observed status in [publication](../verification/github-publication-1.122.0.json).
- ChatGPT Work: synchronized, 1.122.0 / `pluginrel_6ada1691510c8191876a77b0accd8ce9`; complete 1,604-file readback, 52 private-only files preserved, 27 intentional public-path overlays retained; [record](../verification/hosted-sync-1.122.0.json). Current-container runtime LIMITED (24/59); fresh installed-client behavior NOT_RUN.
- Codex: not_run

- Process: Superpowers planning, execution, debugging, source-guided verification and one independent whole-branch review used. No Critical/Important review findings. First setup and routing tested at source level; no claim of automatic cross-host installation or active-client execution.
- Branches: main and the explicitly requested task branch carry the release; the three pre-existing ccr branches are ancestors of baseline main and were preserved. gh-pages was preserved.

## CC-20261022-08

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `62e84ca` (main, package 1.122.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.123.0)
- Package version: 1.122.0 -> 1.123.0
- Scope: Trigger: the Open Design 0.26.0 review (handover item 1). Adds photosensitivity screening (flash_check.py), FrameCut transcript sanity warnings and an English-only model check, inspect-encode audio and cover checks, the open-design registry entry at 0.26.0 with its decision map and licence, and the smallest rule edits in the owning texts. A fresh review's three important findings were fixed with failing-first tests before release.
- Shared package changed: yes; 24 changed, 5 added, 0 removed ([scope](../verification/scope-1.123.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 22 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 13 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 22 suite 56: PASS ([record](../verification/release-1.123.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `cecf8f0`; workflows Check Studio sources 39808288102, Publish verified Studio release 39808284692, Refresh current release notes 39808284682, Check Studio sources 39808284458: success; [v1.123.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.123.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1557 of 1557) ([record](../verification/github-publication-1.123.0.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-10

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `de072bf` (main, package 1.123.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.123.1)
- Package version: 1.123.0 -> 1.123.1
- Scope: Trigger: the owner asked to find and fix the gaps between Studio and Superpowers in Claude as well as ChatGPT. A companion host-eval suite runs both plugins; 36 owners now name the Superpowers skills they must load, and Creative Video Producer sends the user's own footage to FrameCut with at most one question. Companion suite 8/8 after (C01 0/3, C07 0/1, C08 0/5 before).
- Shared package changed: yes; 44 changed, 0 added, 0 removed ([scope](../verification/scope-1.123.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 24 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 13 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 26 suite 56: PASS ([record](../verification/release-1.123.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `56c125e`; workflows Check Studio sources 39856722004, Publish verified Studio release 39856719117, Check Studio sources 39856719159: success; [v1.123.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.123.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1557 of 1557) ([record](../verification/github-publication-1.123.1.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-11

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `53208e5` (main, package 1.123.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.123.2)
- Package version: 1.123.1 -> 1.123.2
- Scope: Trigger: the owner's Earshot handover. The hosted 1.122.1 Earshot routing is ported to the repository with the skill named in four owners, the pinned command-line route kept for Claude Code and Codex, and no Gemini or MCP; private overlay lines are not published.
- Shared package changed: yes; 16 changed, 2 added, 0 removed ([scope](../verification/scope-1.123.2.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 25 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 13 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 26 suite 56: PASS ([record](../verification/release-1.123.2.json))

Cross-host state:

- GitHub: synchronized. `main` at `81b0d51`; workflows Check Studio sources 39864985622, Publish verified Studio release 39864982723, Check Studio sources 39864982736: success; [v1.123.2](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.123.2) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.123.2.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261022-14

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `0f64d9c` (main, package 1.123.2); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.124.0)
- Package version: 1.123.2 -> 1.124.0
- Scope: Trigger: the owner asked to publish Earshot for every user beside Studio. The marketplace lists earshot-audio 1.0.0 (Earshot v0.4.0, upstream earshot and real-sound merged, pinned and checked installation, local only); Studio's registry and routing point to it first.
- Shared package changed: yes; 11 changed, 0 added, 0 removed ([scope](../verification/scope-1.124.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 8 suite 6, 7 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 25 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 13 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 15 suite 56, 6 suite 57, 26 suite 58: PASS ([record](../verification/release-1.124.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `4979658`; workflows Check Studio sources 39903007019, Refresh current release notes 39903004798, Publish verified Studio release 39903004797, Check Studio sources 39903004845: success; [v1.124.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.124.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.124.0.json)); the notes refresh failed on the tag and passed after the notes-only fix `1312795`
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261023-02

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `1f96dc6` (main, package 1.124.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.124.1)
- Package version: 1.124.0 -> 1.124.1
- Scope: Owner request 2026-10-23: first configuration offers earshot-audio second, after Superpowers (registry recommendation_priority second, first companion setup step 6), and the Codex and ChatGPT install guides gain an Earshot Audio section; host_eval resolves --with-plugin to an absolute path. Host eval C14 failed before and passes after; C15 and C05 pass.
- Shared package changed: yes; 11 changed, 0 added, 0 removed ([scope](../verification/scope-1.124.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 9 suite 6, 9 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 27 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 13 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 15 suite 56, 7 suite 57, 27 suite 58: PASS ([record](../verification/release-1.124.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `bcfd726`; workflows Check Studio sources 39921509942, Refresh current release notes 39921507020, Check Studio sources 39921506954, Publish verified Studio release 39921506956: success; [v1.124.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.124.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.124.1.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261023-03

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `9e483b1` (main, package 1.124.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.124.2)
- Package version: 1.124.1 -> 1.124.2
- Scope: Defect seen in an end-to-end run on 2026-10-23: Earshot's timeline and sheet need the CLAP model, but the registry and earshot-audio 1.0.1 listed them as light-tier commands. The registry text and earshot-audio 1.0.2 are corrected; on the light tier sync is checked from measured onsets. After the fix the run took 17 turns instead of 24 and stayed within one frame.
- Shared package changed: yes; 9 changed, 0 added, 0 removed ([scope](../verification/scope-1.124.2.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 9 suite 6, 9 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 28 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 13 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 15 suite 56, 8 suite 57, 27 suite 58: PASS ([record](../verification/release-1.124.2.json))

Cross-host state:

- GitHub: synchronized. `main` at `15ae48a`; workflows Check Studio sources 39929047508, Publish verified Studio release 39929045021, Refresh current release notes 39929045127, Check Studio sources 39929045092: success; [v1.124.2](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.124.2) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.124.2.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261023-04

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `ef7382b` (main, package 1.124.2); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.124.3)
- Package version: 1.124.2 -> 1.124.3
- Scope: Owner's ChatGPT Work test on 2026-10-23: with earshot-audio listed but its engine missing, Work made the sound with Studio's sound.py without asking. Owner decision (option A): Studio and earshot-audio 1.0.3 ask one question with both routes, run neither before the answer and name the engine that ran. Host eval C16 failed before and passes after.
- Shared package changed: yes; 10 changed, 0 added, 0 removed ([scope](../verification/scope-1.124.3.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 9 suite 6, 9 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 29 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 13 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 15 suite 56, 9 suite 57, 27 suite 58: PASS ([record](../verification/release-1.124.3.json))

Cross-host state:

- GitHub: synchronized. `main` at `c55acad`; workflows Check Studio sources 39937471623, Refresh current release notes 39937467906, Publish verified Studio release 39937467894, Check Studio sources 39937467913: success; [v1.124.3](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.124.3) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.124.3.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261023-05

- Origin: cloud-code
- Branch: `main`
- Baseline: `2e6809b` (main, package 1.124.3)
- Result: this commit (verification record only)
- Package version: 1.124.3 (unchanged); earshot-audio 1.0.3 (unchanged)
- Scope: Earshot full tier verified in Claude Code at the owner's request, after the owner allowed the PyTorch and Hugging Face hosts in the environment: install --tier full and fetch-models from the pinned commit, timeline and sheet on an encoded MP4, and an end-to-end run where Studio's request was served by earshot-audio's kit and timeline, within one frame ([record](../verification/earshot-audio-1.0.3-full-tier.json)).
- Shared package changed: no

Cross-host state:

- GitHub: synchronized after push
- ChatGPT Work: pending (hosted earshot-audio still runs an older runtime.py per the owner's report)
- Codex: not_run

## CC-20261023-06

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `8d06086` (main, package 1.124.3); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.124.4)
- Package version: 1.124.3 -> 1.124.4
- Scope: Owner's listening report on 2026-10-23: a preset's landing hit had a metallic debris tail. Earshot-audio 1.0.4 and Studio choose every effect by listening, with candidates ranked, a match against likely confusions, onsets per second and speaker-audible bands as gates, and the readings reported. Host eval C17 failed before and passes after.
- Shared package changed: yes; 10 changed, 0 added, 0 removed ([scope](../verification/scope-1.124.4.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 9 suite 6, 9 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 30 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 13 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 15 suite 56, 10 suite 57, 27 suite 58: PASS ([record](../verification/release-1.124.4.json))

Cross-host state:

- GitHub: synchronized. `main` at `358d40f`; workflows Check Studio sources 39947711723, Refresh current release notes 39947708597, Check Studio sources 39947708731, Publish verified Studio release 39947708811: success; [v1.124.4](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.124.4) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.124.4.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261023-07

- Origin: cloud-code
- Branch: `main`
- Baseline: `48526d8` (main, package 1.124.4)
- Result: this commit (verification record only)
- Package version: 1.124.4 (unchanged); earshot-audio 1.0.4 (unchanged)
- Scope: the owner listened to three landing hits on the test film and chose V3 (`cut_hit/kick`), the take the gated selection of earshot-audio 1.0.4 picked by itself in host eval C17 ([record](../verification/earshot-audio-1.0.4-listening.json)). PASS_REPORTED.
- Shared package changed: no

Cross-host state:

- GitHub: synchronized after push
- ChatGPT Work: pending
- Codex: not_run

## CC-20261023-08

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `76c93ee` (main, package 1.124.4); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.125.0)
- Package version: 1.124.4 -> 1.125.0
- Scope: Owner request 2026-10-23: the same first configuration on every host (Superpowers, then Earshot in plain words with a full or light choice installed in the same conversation; install guides enter it), one Earshot route through the earshot-audio plugin (registry pip installation removed, stale 0.3 text corrected, listen.py runs the plugin's engine offline and refuses llm and mcp), and Superpowers as the method for the code around Earshot (earshot-audio 1.0.5). Host evals C14, C18, C19 and C20 failed before and pass after.
- Shared package changed: yes; 18 changed, 0 added, 0 removed ([scope](../verification/scope-1.125.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 10 suite 6, 9 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 31 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 14 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 15 suite 56, 11 suite 57, 27 suite 58: PASS ([record](../verification/release-1.125.0.json))

Cross-host state:

- GitHub: synchronized. `main` at `b94028c`; workflows Check Studio sources 39958758990, Refresh current release notes 39958755867, Check Studio sources 39958755189, Publish verified Studio release 39958755077: success; [v1.125.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.125.0) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.125.0.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261023-09

- Origin: cloud-code
- Branch: `main`
- Baseline: the 1.125.0 publication record commit
- Result: this commit (handover only)
- Package version: 1.125.0 (unchanged); earshot-audio 1.0.5 (unchanged)
- Scope: [handover](handover-claude-code-2026-10-23.md) for the owner's next Claude Code account and ChatGPT Work: state, owner decisions of 2026-10-23, evidence, remaining work and the ChatGPT Work update and test prompts.
- Shared package changed: no

Cross-host state:

- GitHub: synchronized after push
- ChatGPT Work: pending
- Codex: not_run

## CC-20261023-11

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `85e3d02` (main, package 1.125.0); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.125.1)
- Package version: 1.125.0 -> 1.125.1
- Scope: Independent review on 2026-10-23: listen.py bridge always offline and refuses doctor --fetch; earshot-audio 1.0.6 fails an install whose upload stub cannot be applied; setup states what is written; last second-route references removed. Main gate W01 W02 W04 V01 D01 pass.
- Shared package changed: yes; 15 changed, 0 added, 0 removed ([scope](../verification/scope-1.125.1.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 10 suite 6, 9 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 31 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 15 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 16 suite 56, 11 suite 57, 27 suite 58: PASS ([record](../verification/release-1.125.1.json))

Cross-host state:

- GitHub: synchronized. `main` at `19e2776`; workflows Check Studio sources 39975763356, Refresh current release notes 39975758062, Publish verified Studio release 39975758057, Check Studio sources 39975758201: success; [v1.125.1](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.125.1) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.125.1.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CC-20261023-16

- Origin: cloud-code
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `eb52671` (main, package 1.125.1); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.125.2)
- Package version: 1.125.1 -> 1.125.2
- Scope: Owner decision 2026-10-23: Earshot keeps its name and is plainly credited to Leon Lin in the setup copy and in earshot-audio 1.0.7 manifests.
- Shared package changed: yes; 9 changed, 0 added, 0 removed ([scope](../verification/scope-1.125.2.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 238 Node tests (227 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 10 suite 6, 9 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 17 suite 10, 24 suite 11, 21 suite 12, 29 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 31 suite 18, 11 suite 19, 5 suite 20, 15 suite 21, 8 suite 22 (8 skipped; see the suite log for reasons), 2 suite 23, 8 suite 24, 6 suite 25, 14 suite 26, 11 suite 27, 6 suite 28, 4 suite 29, 43 suite 30, 20 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 4 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 5 suite 40 (5 skipped; see the suite log for reasons), 5 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 15 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 16 suite 56, 12 suite 57, 27 suite 58: PASS ([record](../verification/release-1.125.2.json))

Cross-host state:

- GitHub: synchronized. `main` at `9e69674`; workflows Check Studio sources 39988809212, Publish verified Studio release 39988806127, Refresh current release notes 39988806086, Check Studio sources 39988806082: success; [v1.125.2](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.125.2) assets read back: plugin ZIP, inventory and player match the local build, ZIP byte-identical to the tag tree (1559 of 1559) ([record](../verification/github-publication-1.125.2.json))
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run

## CX-20261024-01

- Origin: codex
- Branch: `main`, fast-forwarded into `main` under the owner's standing rule
- Baseline: `40c1745` (main, package 1.125.2); full SHA in the commit trailer
- Result: the release commit carrying this entry (package 1.126.0)
- Package version: 1.125.2 -> 1.126.0
- Scope: Owner-authorized 28 audit repairs, four reference workflows and pinned optional Hallmark integration; measured routing and full naming/companion proposals retain 37 owners. Regression-discovered crossfade compatibility and test isolation corrected; private hosted overlay preserved separately.
- Shared package changed: yes; 60 changed, 5 added, 0 removed ([scope](../verification/scope-1.126.0.json))

Verification:

- canonical validator: PASS; `claude plugin validate --strict`: PASS
- `scripts/check_all.sh`: 239 Node tests (228 passing, 11 opt-in browser tests skipped there), 13 suite 1, 4 suite 2, 5 suite 3, 6 suite 4, 6 suite 5, 10 suite 6, 9 suite 7, 8 suite 8 (3 skipped; see the suite log for reasons), 23 suite 9, 20 suite 10, 24 suite 11, 21 suite 12, 34 suite 13, 6 suite 14, 10 suite 15, 10 suite 16, 7 suite 17, 31 suite 18, 11 suite 19, 5 suite 20, 17 suite 21, 12 suite 22, 2 suite 23, 8 suite 24, 8 suite 25, 17 suite 26 (1 skipped; see the suite log for reasons), 12 suite 27, 6 suite 28, 4 suite 29, 44 suite 30, 21 suite 31, 26 suite 32, 17 suite 33, 10 suite 34, 5 suite 35, 4 suite 36, 2 suite 37, 2 suite 38, 3 suite 39, 6 suite 40, 6 suite 41, 4 suite 42, 8 suite 43, 8 suite 44, 11 suite 45, 6 suite 46, 15 suite 47, 3 suite 48, 12 suite 49, 3 suite 50, 6 suite 51, 4 suite 52, 9 suite 53, 2 suite 54, 2 suite 55, 16 suite 56, 12 suite 57, 34 suite 58: PASS ([record](../verification/release-1.126.0.json))

Cross-host state:

- GitHub: pending (release commit, tag workflow and readback follow)
- ChatGPT Work: pending (guarded hosted update and affected-file readback required)
- Codex: not_run
