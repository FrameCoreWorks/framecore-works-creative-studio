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
