# Tool inventory verification, 2026-10-20

Trigger: the owner requested every tool in the supplied Work configuration be checked on initial installation and every plugin update, with missing-tool disclosure before installation.

- Before: the default checker covered 20 public capability entries and exact starter lockfiles; the private overlay had 29 entries. It did not independently verify the full 59-component list.
- After: the complete offline inventory is the default and lifecycle route; the previous diagnostic requires `--capabilities-only`. The inventory does not install or download anything.
- `source-checks.log` and `source-checks.exit`: full required source suite, passed. `validator.json`: canonical package validator, passed.
- `work-update.json`: actual public-candidate update probe, 59/59 passed. `hosted-work-final.json`: actual merged private-candidate final-installation probe, 59/59 passed. These measure the current Work runtime, not a fresh host installation.
- `hosted-candidate-validator.json` and `hosted-candidate-continuity.json`: merged package checks and baseline preservation guards, passed. Private files are not included in this public report.
- Independent review found and verified fixes for incomplete npm entry points, import-only Auto-Editor, ambiguous host traces, isolated Python discovery, failed-probe uncertainty and alternate bundled FFmpeg selection. The private checklist link and private release history were retained by three-way merges.

Model hashes establish installed asset identity; imports and version commands establish bounded installation evidence. Full rendering, model inference, Codex/Claude installation and fresh-client startup remain NOT_RUN. Current reported Work versions do not prove another host or mandate a downgrade.

Saved hosted release: `pluginrel_6ad7c92acb7081919bd776b566bba6b6`. All 1559 archive files match the merged candidate. `saved-work-update.json` repeats the full update inventory from the saved archive: 59/59 passed, no installation. `github-source-readback.json` confirms all 44 changed source blobs at the release commit.
