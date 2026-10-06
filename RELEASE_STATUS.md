# Release status

Source version: **1.19.0**. Date: 2026-10-06. Change ID: `CC-20261006-12` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Music and voice-over sync: beat grid and caption import tool, captions in the engine, preview and Remotion starter, audio playback and mixing, checks and review |
| Source checks | PASS: canonical validator; 152 Node (+1 opt-in browser test passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | Captioned starter reviewed in three formats (114 frames, 0 findings); uncaptioned output pixel-identical to 1.18.0; Remotion click-track render with sample-exact beat spacing and a 42.7 ms AAC start delay. Preview audio playback not exercised |
| Scope | 25 changed and 3 added shared files, 872 total; 37 skill IDs |
| GitHub publication | PASS: `main` fast-forwarded to `7e39fd08320e410d8cc8ff94814b0dd549809d5e`; [v1.19.0](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.19.0); workflow 37526607956 succeeded; all 872 GitHub package files and plugin ZIP hash match local |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.19.0.json), [GitHub publication](verification/github-publication-1.19.0.json) and [bounded scope](verification/scope-1.19.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.18.0, is recorded in [its verification](verification/release-1.18.0.json) and [GitHub publication](verification/github-publication-1.18.0.json).
