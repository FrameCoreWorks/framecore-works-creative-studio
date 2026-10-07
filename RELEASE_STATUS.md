# Release status

Source version: **1.25.0**. Date: 2026-10-07. Change ID: `CC-20261007-07` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Sound policy for motion deliveries: no code-synthesized audio, silent first, then the user's file, a connected and confirmed provider, or an installed local generator; tested mux command; stale skill sentences removed |
| Source checks | PASS: canonical validator; 159 Node (+3 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | Documented mux kept a click track sample-exact and the video stream byte-identical on the test D MP4 |
| Scope | 10 changed shared files, 878 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `66ec071d417a037bec8efc606d4f0874ba9d75cd`; [v1.25.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.25.0); workflow 37600958954 succeeded; all 878 package files, plugin ZIP and player hashes match local |
| Owner reports | 2026-10-07 on 1.25.0: ChatGPT Work delivered the unchanged player template with its contract (check-preview PASS), a valid contract and a clean MP4 ([report](verification/host-report-2026-10-07-work.json)); ordinary ChatGPT delivered a clean MP4 with the same video embedded as its preview ([report](verification/host-report-2026-10-07-test-e.json)). Test D on 1.24.0: ChatGPT delivered a clean MP4 and a valid contract and named the frames it checked ([report](verification/host-report-2026-10-07-test-d.json)); test C: ChatGPT's MP4 clean, its HTML preview different and exporting through MediaRecorder ([report](verification/host-report-2026-10-07-test-c.json)); test A ([report](verification/host-report-2026-10-07-test-a.json)) |
| GitHub Pages | Live at <https://framecoreworks.github.io/framecore-works-creative-studio/> since the owner enabled it on 2026-10-07: HTTP 200, byte-identical to the template; a contract opened and exported on the live site in Chromium. Published by workflow 37585412460 (`gh-pages` `52c3af1`) |
| Owner host report (1.20.0 export) | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.25.0.json), [GitHub publication](verification/github-publication-1.25.0.json) and [bounded scope](verification/scope-1.25.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.24.0, is recorded in [its verification](verification/release-1.24.0.json) and [GitHub publication](verification/github-publication-1.24.0.json).
