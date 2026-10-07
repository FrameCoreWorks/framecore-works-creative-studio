# Release status

Source version: **1.21.0**. Date: 2026-10-07. Change ID: `CC-20261007-02` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Single-file preview delivered unchanged except its contract, with a `check-preview.mjs` gate; `sweep` exit; clearer contract checks |
| Source checks | PASS: canonical validator; 157 Node (+2 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | check-preview rejects the owner-supplied ChatGPT preview (6 findings) and passes the template-built example; sweep pixel-identical in preview and Remotion; existing contracts unchanged |
| Scope | 16 changed and 2 added shared files, 877 total; 37 skill IDs |
| GitHub publication | NOT_RUN at source preparation; see the [development ledger](docs/development-ledger.md) for the integrated state |
| Owner host report (1.20.0) | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.21.0.json) and [bounded scope](verification/scope-1.21.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.20.0, is recorded in [its verification](verification/release-1.20.0.json) and [GitHub publication](verification/github-publication-1.20.0.json).
