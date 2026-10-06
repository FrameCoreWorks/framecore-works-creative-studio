# Release status

Source version: **1.18.0**. Date: 2026-10-06. Change ID: `CC-20261006-11` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Output formats in the motion contract (16:9, 9:16, 1:1 from one timeline) across engine, preview, Remotion starter and frame review; review screenshots drawn at true size |
| Source checks | PASS: canonical validator; 150 Node (+1 opt-in browser test passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | Starter reviewed in three formats (93 frames, 0 findings); base format pixel-identical to 1.17.0; preview and Remotion stills pixel-identical per format. No full per-format video render |
| Scope | 25 changed shared files, 0 added, 869 total; 37 skill IDs |
| GitHub publication | NOT_RUN at source preparation; see the [development ledger](docs/development-ledger.md) for the integrated state |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.18.0.json) and [bounded scope](verification/scope-1.18.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.17.0, is recorded in [its verification](verification/release-1.17.0.json) and [GitHub publication](verification/github-publication-1.17.0.json).
