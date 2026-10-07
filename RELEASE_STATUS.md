# Release status

Source version: **1.22.0**. Date: 2026-10-07. Change ID: `CC-20261007-04` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | The single-file preview becomes the motion player (Open contract); Studio delivers contracts plus the player instead of whole pages, with a WebCodecs-only export fallback for self-written pages; the player ships with every release and gets a Pages workflow; export CLI hardening |
| Source checks | PASS: canonical validator; 158 Node (+3 opt-in browser tests passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Container runs | Player opens valid contracts, including the second ChatGPT test contract, rejects invalid ones and exports; release player byte-identical to the template; Pages steps simulated locally; existing contracts unchanged |
| Scope | 13 changed shared files, 877 total; 37 skill IDs; repository-only: Pages workflow and release scripts |
| GitHub publication | NOT_RUN at source preparation; see the [development ledger](docs/development-ledger.md) for the integrated state |
| GitHub Pages | Not enabled at source preparation; the owner enables Settings > Pages > Deploy from a branch > gh-pages after the first workflow run |
| Owner host report (1.20.0) | 2026-10-07, ordinary ChatGPT, Android phone browser: browser export produced a playable MP4 H.264 (`avc1.640028`), 1920 x 1080, 180 frames; PASS_REPORTED ([report](verification/host-report-2026-10-07-browser-export.json)) |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.22.0.json) and [bounded scope](verification/scope-1.22.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.21.0, is recorded in [its verification](verification/release-1.21.0.json) and [GitHub publication](verification/github-publication-1.21.0.json).
