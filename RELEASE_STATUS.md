# Release status

Source version: **1.17.0**. Date: 2026-10-06. Change ID: `CC-20261006-10` (origin: cloud-code).

| Field | Value |
|---|---|
| Change | Automated frame review: preview review mode and review-frames tool with contact sheet |
| Source checks | PASS: canonical validator; 149 Node (+1 opt-in browser test passing) + 12 motion-quality + 12 installer + 4 identity + 8 GEPA pilot + 23 asset tests |
| Tool runs | Container only: starter and all-kinds contracts without findings; broken contract flagged with exit code 1 |
| Scope | 11 changed and 2 added shared files, 869 total; 37 skill IDs |
| GitHub publication | NOT_RUN at source preparation; see the [development ledger](docs/development-ledger.md) for the integrated state |
| Hosted plugin, ChatGPT and Codex | Owner-managed; not tracked by this source release |

See [source verification](verification/release-1.17.0.json) and [bounded scope](verification/scope-1.17.0.json). Source and container checks do not establish host behavior. The 201 planned host cases remain not_run. The previous release, 1.16.0, is recorded in [its verification](verification/release-1.16.0.json) and [GitHub publication](verification/github-publication-1.16.0.json).
