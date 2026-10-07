# Release status

Source version: **1.23.0**. Date: 2026-10-07. Change ID: `CC-20261007-05` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | One clickable link that opens the motion player with the contract loaded; `player-link.mjs`; no substitute videos; approval rule for direct build requests |
| Source checks | PASS: canonical validator; 159 Node (+3 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | Link for the test A contract opened and exported on the live player in Chromium; Node and Python links byte-identical; player template unchanged |
| Owner reports | 2026-10-07 test A: the one-click link opened the animation on the owner's device (PASS_REPORTED); ChatGPT's own MP4 differed from its contract ([report](verification/host-report-2026-10-07-test-a.json)) |
| Scope | 13 changed and 1 added shared files, 878 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `d687f58f6167adde6b5dfd0475f1ee6d0c59511d`; [v1.23.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.23.0); workflow 37591516754 succeeded; all 878 package files, plugin ZIP and player hashes match local |
| GitHub Pages | Live at <https://framecoreworks.github.io/framecore-works-creative-studio/> since the owner enabled it on 2026-10-07: HTTP 200, byte-identical to the template; a contract opened and exported on the live site in Chromium. Published by workflow 37585412460 (`gh-pages` `52c3af1`) |
| Owner host report (1.20.0 export) | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.23.0.json), [GitHub publication](verification/github-publication-1.23.0.json) and [bounded scope](verification/scope-1.23.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.22.0, is recorded in [its verification](verification/release-1.22.0.json) and [GitHub publication](verification/github-publication-1.22.0.json).
