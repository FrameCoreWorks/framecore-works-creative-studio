# Release status

Source version: **1.13.0**. Date: 2026-10-06. Change ID: `CC-20261006-06` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Self-contained single-file motion preview for hosts without shell or renderer |
| Source checks | PASS: canonical validator; 140 Node + 9 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Preview execution | Container only: opened from disk in headless Chromium; six frames inspected; seeks pixel-identical; interactive Play not run |
| Scope | 10 changed and 2 added shared files, 861 total; 37 skill IDs |
| GitHub publication | NOT_RUN at source preparation; see the [development ledger](docs/development-ledger.md) for the integrated state |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.13.0.json) and [bounded scope](verification/scope-1.13.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.12.0, is recorded in [its verification](verification/release-1.12.0.json) and [GitHub publication](verification/github-publication-1.12.0.json).
