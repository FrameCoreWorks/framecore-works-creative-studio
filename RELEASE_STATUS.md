# Release status

Source version: **1.12.0**. Date: 2026-10-06. Change ID: `CC-20261006-05` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Motion Graphics Workflow method rewrite, motion craft reference, Remotion and GSAP starters sharing one contract |
| Source checks | PASS: canonical validator; 139 Node + 9 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Starter execution | Container only: Remotion starter rendered 300 frames H.264; GSAP seeks pixel-identical. Full playback review not run |
| Scope | 12 changed and 19 added shared files, 859 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `ad451eea112598af903ae6149cfdc10913af1c85`; [v1.12.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.12.0); workflow 37490293094 succeeded; all 859 GitHub blobs and plugin ZIP hash match local |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.12.0.json), [GitHub publication](verification/github-publication-1.12.0.json) and [bounded scope](verification/scope-1.12.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.11.2, is recorded in [its verification](verification/release-1.11.2.json) and [GitHub publication](verification/github-publication-1.11.2.json).
