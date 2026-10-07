# Release status

Source version: **1.20.0**. Date: 2026-10-06. Change ID: `CC-20261006-13` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Browser video export from the single-file preview (MP4 H.264 where the browser can encode it, otherwise WebM; video only) and a matching dependency-free shell exporter |
| Source checks | PASS: canonical validator; 155 Node (+2 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | Chromium 1194: VP9 WebM exports in 16:9 and 9:16 (300 frames, about 42 dB PSNR); drawn frames pixel-identical to Remotion; MP4 writer verified with libx264 H.264; browser H.264 not offered by this build |
| Scope | 12 changed and 3 added shared files, 875 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `bacf565c14c031c298e79b8716f2a9060915f4f5`; [v1.20.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.20.0); workflow 37530222815 succeeded; all 875 GitHub package files and plugin ZIP hash match local |
| Owner host report | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.20.0.json), [GitHub publication](verification/github-publication-1.20.0.json) and [bounded scope](verification/scope-1.20.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.19.0, is recorded in [its verification](verification/release-1.19.0.json) and [GitHub publication](verification/github-publication-1.19.0.json).
