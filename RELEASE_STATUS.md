# Release status

Source version: **1.30.0**. Date: 2026-10-07. Change ID: `CC-20261007-12` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Product films: `device` scene kind (screenshots in a drawn phone or window, screen transitions, camera focus, caption beside the device), product-film rules, app-film example; frame-review screenshots capture the whole frame |
| Source checks | PASS: canonical validator; 168 Node (+3 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | App-film example: browser review without findings in 16:9 and 9:16; Python renderer within 0.86 grey levels of the browser |
| Scope | 21 changed and 2 added shared files, 892 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `1c2bc1bc3fa0fb00f3f25b93a250609979b30d11`; [v1.30.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.30.0); workflow 37625658353 succeeded; package tree (892 files), plugin ZIP and player hashes match local; GitHub Pages republished the player (workflow 37625658656, byte-identical) |
| Owner review | 2026-10-07: the owner watched the app-film example renders (16:9 and 9:16) and approved them |
| Host testing | Owner decision 2026-10-07: no owner test for each small change; an occasional larger test in ChatGPT Work instead. Host behavior of 1.27.0 is not_run and expected to vary across users' hosts |
| Owner reports | 2026-10-07 on 1.26.0: ChatGPT Work revised the test E contract as asked (only the requested changes, revision 2 approved with the request quoted, `-r2` file names, change list) and rendered a clean 240-frame MP4; the unchanged intro sits about 3 px higher than in revision 1 ([report](verification/host-report-2026-10-07-revision.json)). On 1.25.0: ChatGPT Work delivered the unchanged player template with its contract (check-preview PASS), a valid contract and a clean MP4 ([report](verification/host-report-2026-10-07-work.json)); ordinary ChatGPT delivered a clean MP4 with the same video embedded as its preview ([report](verification/host-report-2026-10-07-test-e.json)). Test D on 1.24.0: ChatGPT delivered a clean MP4 and a valid contract and named the frames it checked ([report](verification/host-report-2026-10-07-test-d.json)); test C: ChatGPT's MP4 clean, its HTML preview different and exporting through MediaRecorder ([report](verification/host-report-2026-10-07-test-c.json)); test A ([report](verification/host-report-2026-10-07-test-a.json)) |
| GitHub Pages | Live at <https://framecoreworks.github.io/framecore-works-creative-studio/> since the owner enabled it on 2026-10-07: HTTP 200, byte-identical to the template; a contract opened and exported on the live site in Chromium. Published by workflow 37585412460 (`gh-pages` `52c3af1`) |
| Owner host report (1.20.0 export) | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.30.0.json), [GitHub publication](verification/github-publication-1.30.0.json) and [bounded scope](verification/scope-1.30.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.29.0, is recorded in [its verification](verification/release-1.29.0.json) and [GitHub publication](verification/github-publication-1.29.0.json).
