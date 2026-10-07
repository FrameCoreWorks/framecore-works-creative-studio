# Release status

Source version: **1.32.0**. Date: 2026-10-07. Change ID: `CC-20261007-14` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Motion sound design at studio standard: effects planned from the picture's timing and synthesized in layers, a composed music bed, mastering to -14 LUFS, frame-exact timing check; sound policy updated on the owner's decision |
| Source checks | PASS: canonical validator; 173 Node (+3 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | Three examples mixed: hits within 2 ms, -14.1 to -15.7 LUFS, true peak at most -1.05 dBTP |
| Owner listening | 2026-10-07: music and clicks approved; whooshes too strong, then lowered by 6 to 7 dB |
| Scope | 16 changed and 4 added shared files, 897 total; 37 skill IDs |
| GitHub publication | NOT_RUN: committed locally on `cloud-code/CC-20261007-14-motion-sound`; not pushed |
| Host testing | Owner decision 2026-10-07: no owner test for each small change; an occasional larger test in ChatGPT Work instead. Host behavior of 1.27.0 is not_run and expected to vary across users' hosts |
| Owner review (1.30.0) | 2026-10-07: the owner watched the app-film example renders (16:9 and 9:16) and approved them |
| Owner reports | 2026-10-07 on 1.26.0: ChatGPT Work revised the test E contract as asked (only the requested changes, revision 2 approved with the request quoted, `-r2` file names, change list) and rendered a clean 240-frame MP4; the unchanged intro sits about 3 px higher than in revision 1 ([report](verification/host-report-2026-10-07-revision.json)). On 1.25.0: ChatGPT Work delivered the unchanged player template with its contract (check-preview PASS), a valid contract and a clean MP4 ([report](verification/host-report-2026-10-07-work.json)); ordinary ChatGPT delivered a clean MP4 with the same video embedded as its preview ([report](verification/host-report-2026-10-07-test-e.json)). Test D on 1.24.0: ChatGPT delivered a clean MP4 and a valid contract and named the frames it checked ([report](verification/host-report-2026-10-07-test-d.json)); test C: ChatGPT's MP4 clean, its HTML preview different and exporting through MediaRecorder ([report](verification/host-report-2026-10-07-test-c.json)); test A ([report](verification/host-report-2026-10-07-test-a.json)) |
| GitHub Pages | Live at <https://framecoreworks.github.io/framecore-works-creative-studio/> since the owner enabled it on 2026-10-07: HTTP 200, byte-identical to the template; a contract opened and exported on the live site in Chromium. Published by workflow 37585412460 (`gh-pages` `52c3af1`) |
| Owner host report (1.20.0 export) | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.32.0.json) and [bounded scope](verification/scope-1.32.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.31.0, is recorded in [its verification](verification/release-1.31.0.json) and [GitHub publication](verification/github-publication-1.31.0.json).
