# Release status

Source version: **1.26.0**. Date: 2026-10-07. Change ID: `CC-20261007-08` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Contract revisions: a change to a delivered video starts from its contract, changes only what was asked, increments `revision`, shows was → is and keeps earlier files; new `revise.mjs` (`diff`, `extend`) |
| Source checks | PASS: canonical validator; 160 Node (+3 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | `extend` on the starter example and on the 2026-10-07 ChatGPT contract; every result passed `check-score.mjs` |
| Scope | 11 changed and 2 added shared files, 880 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `fefe5f6d21ee80f8678de6200cdc3b2fdb8741f3`; [v1.26.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.26.0); workflow 37607283263 succeeded; package tree (880 files), plugin ZIP and player hashes match local |
| Owner reports | 2026-10-07 on 1.25.0: ChatGPT Work delivered the unchanged player template with its contract (check-preview PASS), a valid contract and a clean MP4 ([report](verification/host-report-2026-10-07-work.json)); ordinary ChatGPT delivered a clean MP4 with the same video embedded as its preview ([report](verification/host-report-2026-10-07-test-e.json)). Test D on 1.24.0: ChatGPT delivered a clean MP4 and a valid contract and named the frames it checked ([report](verification/host-report-2026-10-07-test-d.json)); test C: ChatGPT's MP4 clean, its HTML preview different and exporting through MediaRecorder ([report](verification/host-report-2026-10-07-test-c.json)); test A ([report](verification/host-report-2026-10-07-test-a.json)) |
| GitHub Pages | Live at <https://framecoreworks.github.io/framecore-works-creative-studio/> since the owner enabled it on 2026-10-07: HTTP 200, byte-identical to the template; a contract opened and exported on the live site in Chromium. Published by workflow 37585412460 (`gh-pages` `52c3af1`) |
| Owner host report (1.20.0 export) | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.26.0.json), [GitHub publication](verification/github-publication-1.26.0.json) and [bounded scope](verification/scope-1.26.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.25.0, is recorded in [its verification](verification/release-1.25.0.json) and [GitHub publication](verification/github-publication-1.25.0.json).
