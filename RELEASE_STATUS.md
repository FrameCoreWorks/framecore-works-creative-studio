# Release status

Source version: **1.16.0**. Date: 2026-10-06. Change ID: `CC-20261006-09` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Declarative scene kinds rendered by one engine in the preview and the Remotion starter |
| Source checks | PASS: canonical validator; 148 Node + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Runtime execution | Container only: preview pixel-identical to 1.15.0; all-kinds example rendered in preview and Remotion (775-frame H.264). Full playback review not run |
| Scope | 21 changed and 4 added shared files, 867 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `909c1f020172a3f65740b2339074090fcaf4f225`; [v1.16.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.16.0); workflow 37503394895 succeeded; all 867 GitHub blobs and plugin ZIP hash match local |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.16.0.json), [GitHub publication](verification/github-publication-1.16.0.json) and [bounded scope](verification/scope-1.16.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.15.0, is recorded in [its verification](verification/release-1.15.0.json) and [GitHub publication](verification/github-publication-1.15.0.json).
