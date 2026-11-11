# DR-03 motion resources: portable source-pack

This pack preserves the complete final authored DR-03 research in its original Polish language, as requested by the user. It is research input for Claude and the implementation owners, not a dependency admission decision, an approved architecture or a tested renderer integration.

## Reading order

1. [REPORT.md](REPORT.md), [REQUIREMENTS.md](REQUIREMENTS.md), [METHODOLOGY.md](METHODOLOGY.md) and the original [PROMPT.md](PROMPT.md).
2. [Baseline and deduplication](BASELINE.md), [candidate JSON](CATALOG.json), [candidate CSV](CATALOG.csv), [full cards](CARDS.md) and [deep dives](DEEP_DIVES.md).
3. [Rankings](RANKINGS.md), [rejections](REJECTIONS.md), [time adapter](TIME_ADAPTER.md) and [test plan](TEST_PLAN.md).
4. [Implementation handoff and backlog](IMPLEMENTATION_HANDOFF.md), [source ledger](SOURCES.json) and [statistics](STATISTICS.json).
5. [Independent review](review/REVIEW.md), [structured review](review/REVIEW.json), [resolution](review/RESOLUTION.md), [spot check](review/LEAD_SPOTCHECK.md) and [original verification](VERIFICATION.md).

The agents/ directories retain the full authored lane cards, knowledge/deep-dive material, candidate records and evidence. The sources/ directory retains baseline inventories, the Toolbox catalog and source records. Repository tree inventories and catalog metadata are evidence, not bundled third-party implementation code.

## Inventory and transformations

The frozen research contains 71 files. This export retains 45 final artifacts and explicitly excludes 26 dated backups. Forty-four retained files are byte-identical. Only review/REVIEW.json changes: its 30 private absolute reviewed_files paths become source-pack-root-relative paths. No review result, evidence status, limitation, source URL, source pin or authored proposal changes.

EXPORT-MANIFEST.json records each original relative path and SHA-256, its inclusion/exclusion, export path/hash and transformation. All exclusions are dated backups; this source inventory contained no downloaded full third-party manuals/code archives, binary assets, credential/host-private files, caches or symlinks. The small authored generator scripts remain as historical research utilities.

The original prompt is byte-identical. The source directory and Hipson ledger remain untouched. Earlier claims about unpublished work, historical progress or local review apply to the original research stage. They do not describe this later publication copy.

## Source and review provenance

The actual researched baseline pins remain:

| Repository | Research pin |
|---|---|
| FrameCoreWorks/framecore-works-creative-studio | 4611c9c4ed44579b8a2c0224c9276d955fccd8d6 |
| FrameCoreWorks/framecore-works-toolbox | adc8094f8e087889e4337c99dd0d267ae1b11a51 |
| FrameCoreWorks/framecore-open-assets | 889471fcdbc2216ddc465715eff0e82784d5b8ee |

All candidate repository pins remain as originally researched. No later publication commit replaces a research pin. Local installation, repository contents and running-session behavior remain distinct; this export creates no equivalence between them.

Historical review and validation claims refer to their original snapshots. Original hashes, if recorded, are not rewritten to make export bytes appear historically reviewed. EXPORT-MANIFEST.json provides separate byte lineage. The parent reported Hipson T-0006 completed with validation V-e5cdc90e9f4244fd818b2b212445729e; this publication worker did not alter or independently query that ledger.

## Supported read-only validation

From a checkout of this directory with Python 3:

```sh
python3 verify_artifacts.py
python3 verify_export.py
```

verify_artifacts.py was fully inspected before execution and copied byte-for-byte. It uses only the Python standard library, resolves paths relative to itself, reads the authored research and prints its result to stdout. It does not run candidate code, applications, renderers, media or network requests. The original prompt hash remains valid.

VERIFICATION.md is historical source evidence. EXPORT-VERIFICATION.json separately records the fresh run on the publication export: artifact integrity PASS, 30 candidates (A=12, B=9, C=9), 12 deep dives and 220 source records. The original checker does not report a numbered total of checks, so none is invented here.

verify_export.py is a new read-only checker for hashes, exact inventory closure, relative links, JSON/CSV fields, record statistics, provenance paths and preserved NOT_RUN status. It does not contact external URLs. The manifest excludes itself from its own hash list; the publisher must retain the separately reported manifest SHA-256 and verify the repository commit.

The preserved agents/runtime/build_records.py, agents/runtime/build_deep_dives.py and agents/knowledge/build_records.py generate and write research documents. They are not verification commands and were not executed during export. Use a disposable working copy if they are needed later; do not overwrite published evidence by running them in this pack.

## Limits preserved

DOCUMENTED, CODE_INSPECTED, the specifically bounded AUTHOR_TEST declarations, DERIVED, Unknown and NOT_RUN retain their original meanings. All 30 candidate execution statuses remain NOT_RUN. The catalog's 220 source records include metadata and failed reads; they are not 220 fully read independent documents. The 205 distinct URLs do not prove comprehensive market coverage.

No candidate installation, asset download/decode, native render, browser-font test, loop/alpha inspection, performance measurement, video viewing or listening was performed for this export. Future test plans remain plans. Rights notes, conflicts, rejections and unknowns remain intact; a library license is not silently promoted into rights for its media assets.

No external source URLs were changed or freshly revalidated. Relative-link checks establish file-target existence, not every anchor or external page section. The pattern-based privacy scan is not an exhaustive security certification.

The public pack has 49 files: 45 retained originals plus this wrapper, verify_export.py, EXPORT-VERIFICATION.json and EXPORT-MANIFEST.json. Private preparation evidence, dated export backups and publication reports remain outside this source-pack. Root is the sole publisher.

