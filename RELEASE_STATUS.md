# Release status

Source version: **1.9.3**. Date: 2026-10-04.

| Field | Value |
|---|---|
| Change | Evidence-based package version reporting in the existing entry owner |
| Source checks | PASS: canonical validator, 121 Node + 12 installer + 4 identity-generation + 23 asset tests |
| Scope | 8 shared files changed; 800 files, welcome assets and all other skill entrypoints byte-identical to 1.9.2 |
| GitHub publication | PASS: `3044bde9facf96472bf4e5da9b9eb4e1266f97bb`, [v1.9.3](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.9.3), workflow 37221734565 succeeded; release plugin ZIP SHA256 matches local |
| Saved hosted plugin/readback | UPDATED: `pluginrel_6ac290c27ef48191b9616c82b49d3beb`; 808 paths/sizes and 796 readable text hashes match, including all changed files |
| Full hosted byte parity | 12 unchanged large/binary files remain unread; full archive download returned HTTP 403 |
| Ordinary ChatGPT | PASS_OBSERVED version 1.9.3, rejection of historical 1.3 and full welcome; read-package scope correct after startup, direct metadata wording remains PARTIAL |
| ChatGPT Work | PASS_OBSERVED version 1.9.3; initial active-version wording too strong, corrected to available-package evidence after a diagnostic question |
| Codex installed files | Managed cache updated to 1.9.3; all 808 files and embedded identity match source |
| Codex active session | Catalog still pointed to the removed 1.9.2 entry; probe reported unavailable evidence. New-rule behavior in a refreshed session remains UNVERIFIED |

See [source checks](verification/release-1.9.3.json) and [bounded scope](verification/scope-1.9.3.json). Publishing a new package does not force existing chats to refresh their loaded skill snapshot. A saved release, an installed/read package and the latest GitHub version are separate evidence layers. The 199 planned host scenarios remain not_run; ad hoc probes are recorded separately.

The [1.9.2 Artifact Guard observations](verification/host-behavior-1.9.2.json) remain partial; this version-reporting change does not alter those instructions or establish visual mitigation efficacy.

See [host probes](verification/host-behavior-1.9.3.json), [saved readback](verification/hosted-release-1.9.3.json) and [GitHub evidence](verification/github-publication-1.9.3.json). Version values were correct in both tested ChatGPT surfaces; precision about saved versus loaded state is not uniformly confirmed. No manual cache mutation or duplicate native installation was performed.
