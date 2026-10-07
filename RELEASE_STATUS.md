# Release status

Source version: **1.24.0**. Date: 2026-10-07. Change ID: `CC-20261007-06` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | MP4 first in hosts with code execution, with a frame check at transitions; HTML preview without export; 1.23.0 player-link and no-substitute requirements withdrawn |
| Source checks | PASS: canonical validator; 159 Node (+3 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Owner reports | 2026-10-07 test C: ChatGPT's MP4 clean, its HTML preview different and exporting through MediaRecorder ([report](verification/host-report-2026-10-07-test-c.json)); test A ([report](verification/host-report-2026-10-07-test-a.json)) |
| Scope | 10 changed shared files, 878 total; 37 skill IDs |
| GitHub publication | NOT_RUN at source preparation; see the [development ledger](docs/development-ledger.md) for the integrated state |
| GitHub Pages | Live at <https://framecoreworks.github.io/framecore-works-creative-studio/> since the owner enabled it on 2026-10-07: HTTP 200, byte-identical to the template; a contract opened and exported on the live site in Chromium. Published by workflow 37585412460 (`gh-pages` `52c3af1`) |
| Owner host report (1.20.0 export) | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.24.0.json) and [bounded scope](verification/scope-1.24.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.23.0, is recorded in [its verification](verification/release-1.23.0.json) and [GitHub publication](verification/github-publication-1.23.0.json).
