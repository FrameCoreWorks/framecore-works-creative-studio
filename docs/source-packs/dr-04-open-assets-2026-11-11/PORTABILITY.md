# DR-04 complete source-pack: portability and evidence

This pack preserves the final authored Polish report, both full specialist card documents, catalog JSON/CSV, all 22 own record-metadata descriptions, complete source ledgers, baseline, rights, adapter designs, 20 planned tests, backlog, handoff and independent review. Start with [REPORT.md](REPORT.md), [baseline](baseline/BASELINE.md), [rankings](RANKINGS.md), [handoff](IMPLEMENTATION_HANDOFF.md) and [review](review/REVIEW.md). This wrapper does not replace the research.

## Preservation and adaptations

The frozen source has 64 files: 36 retained final files and 28 excluded dated backups. 30 retained files are byte-identical; 6 have portability-only edits. [EXPORT-MANIFEST.json](EXPORT-MANIFEST.json) accounts for every original path and SHA-256, disposition, export SHA-256 and adaptation. Original paths are workspace-relative, avoiding publication of private absolute host paths. No original was edited.

Changes are limited to the handoff workspace locator; local cache locators in baseline Markdown/JSON; and the same two locators in baseline/sources.json, sources.json and sources.csv. Historical CODE_INSPECTED/READ and 71/71 cache-byte observations remain original evidence. URNs urn:dr04:local-evidence:marketplace-cache and urn:dr04:local-evidence:remote-cache identify non-exported local observations, not fetchable URLs. Reader access is **Unknown / unavailable in this pack**. They are not relabeled as public GitHub observations.

The original 194 unique source locators include two local observations (192 unique HTTP(S) URLs). URNs preserve cardinality, not public accessibility. All HTTP(S) source URLs, baseline pins, provider decisions and test statuses are unchanged. Historical statements about no publication, backups or pending Hipson close describe original research. T-0007 is the research task; publication assignment A-0037 belongs to parent T-0009.

## Pins and ownership

Publication parent: FrameCoreWorks/framecore-works-creative-studio at a0375f5a4ce31e36a1f179307db22a1dd77331ca. It is publication ancestry, not a replacement research baseline.

Research baselines remain Open Assets 0.5.0 at 889471fcdbc2216ddc465715eff0e82784d5b8ee, Studio 1.174.1 at 4611c9c4ed44579b8a2c0224c9276d955fccd8d6, and Toolbox 1.12.0 at adc8094f8e087889e4337c99dd0d267ae1b11a51. Candidate-specific pins remain as researched.

Open Assets owns acquisition, transport and rights/byte evidence; Studio/FrameCut owns production and editorial acceptance; Toolbox/Earshot owns its admitted local audio workflow. Export changes none of those boundaries.

## Separate evidence gates

- **PROVIDER_ELIGIBILITY:** 3 conditional CORE_CANDIDATE, 13 OPTIONAL, 6 MANUAL_REFERENCE_ONLY, 4 REJECTED. These are research classifications, not enabled adapters.
- **ASSET_ELIGIBILITY:** remains per asset, variant, license, use and restrictions. Reading metadata is not clearance or permission to download or redistribute.
- **HOST_READINESS:** every new candidate and record remains **NOT_RUN**. Author test evidence stays historical and scoped to its original host/revision.

There are 26 candidates, 10 deep cards, 22 metadata records and 204 source entries: 196 READ, 6 BLOCKED, 2 INDEXED_EXCERPT. READ is an original access label, not a publication-time fetch or test. Review remains **PASS_WITH_LIMITATIONS / DOCUMENT_REVIEW_ONLY**. Claude has not accepted the architecture.

## Repeatable export verification

Run Python 3 with verify_export.py from this directory. This new standard-library verifier performs read-only hashes/inventory, JSON/CSV, ID/reference, count, relative Markdown file-link, private-path and evidence-gate checks. It does not execute preserved research helpers or providers, contact external URLs, download, render, decode or install. Fresh output is [EXPORT-VERIFICATION.json](EXPORT-VERIFICATION.json); historical [VERIFICATION.md](VERIFICATION.md) remains separate.

The unchanged verify_artifacts.py is the original read-only document checker; source inspected but not run during export. The unchanged assemble_artifacts.py rewrites aggregates and creates backups; preserved as provenance and not executed. Future assembly should occur in a disposable copy followed by fresh checks.

The manifest cannot authenticate itself: its SHA-256 is recorded separately for the publisher. Links are checked for relative-file existence, not all Markdown anchors or remote sections. External availability and rights were not rechecked.

## Redistribution and remaining limits

No binary media, fonts, full imported third-party code/manuals, credentials, private host configuration or caches are included. The 22 records are researchers' selected factual metadata and observations, not media or full third-party responses. Accessibility does not license underlying assets; no blanket third-party reuse license is added.

All 20 planned product tests, native host behavior, download/decode, listening, visual and perceptual checks, and cross-host readiness remain **NOT_RUN**. Architecture acceptance remains **NOT_GRANTED_RESEARCH_HANDOFF**. Export integrity PASS is not runtime PASS.
