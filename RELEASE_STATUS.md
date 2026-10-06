# Release status

Source version: **1.14.0**. Date: 2026-10-06. Change ID: `CC-20261006-07` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | One motion contract JSON for storyboard, approval and timeline; storyboard check and Markdown rendering |
| Source checks | PASS: canonical validator; 142 Node + 9 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Runtime execution | Container only: packaged starters rerun; GSAP and preview frame 140 pixel-identical to the previous release |
| Scope | 20 changed and 1 added shared files, 862 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `65609d524a7e18c292f79e4a60922b1b66787067`; [v1.14.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.14.0); workflow 37499901576 succeeded; all 862 GitHub blobs and plugin ZIP hash match local |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.14.0.json), [GitHub publication](verification/github-publication-1.14.0.json) and [bounded scope](verification/scope-1.14.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.13.0, is recorded in [its verification](verification/release-1.13.0.json) and [GitHub publication](verification/github-publication-1.13.0.json).
