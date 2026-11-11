# DR-01 source-pack portability and evidence boundaries

This is the complete final authored DR-01 research pack, prepared for repository publication on 2026-11-11. The research remains in its original Polish language at the user's request. This English wrapper describes the export; it does not replace or summarize away the report, glossary, recipes, contracts, examples, source ledgers, QA, implementation backlog or review evidence.

Start with [the original reading guide](README.md), then [COMPREHENSIVE-REPORT.md](COMPREHENSIVE-REPORT.md) and [IMPLEMENTATION_HANDOFF.md](IMPLEMENTATION_HANDOFF.md). The [export manifest](EXPORT-MANIFEST.json) maps every source file to an included artifact or explicit exclusion, with original and export SHA-256 values.

## Preservation and transformations

The source inventory contains 74 files. Forty-seven final files are retained; 27 dated backups are excluded. No downloaded full third-party manual, code archive, credential file, host-private configuration or cache was present in this inventory. The pack includes the original research prompt as its specification.

Forty-five retained files are byte-identical copies. Two files have portability-only edits: specialists/craft/VALIDATION.json changes three private absolute path fields to paths relative to this source-pack root; review/INDEPENDENT-REVIEW.md redirects one link to an excluded dated backup to the export manifest, with an explicit Polish annotation. Historical hashes, timestamps, results and evidence labels are untouched. No factual claims, proposals, limits, source access labels or public source URLs were changed.

Public Studio claims retain their researched commit, 4611c9c4ed44579b8a2c0224c9276d955fccd8d6. Pins for other projects remain as originally recorded. No locally read installed file is reclassified as a public GitHub file merely because its name matches. Installed-byte equality and active-runtime status remain whatever the original research actually established.

The original files' statements about non-publication, retained backups or Hipson work describe the original research process. They are historical statements, not claims about this later export. The Hipson source directory and its ledger were not modified.

## Historical review hashes

[REVIEW.md](REVIEW.md), [review/REVIEW-SNAPSHOT.json](review/REVIEW-SNAPSHOT.json), the resumed checks and specialist validation records describe their original snapshots. A review hash is not rewritten to make a transformed export appear historically reviewed. The export manifest supplies a separate byte lineage.

Some earlier specialist hashes may precede later integrated research revisions. That is history, not evidence that the current export bytes passed those older reviews. The final integrated source snapshot, the export's original hashes and the current export hashes must be read as distinct records.

## Repeatable checks

The original verify_research.py was inspected before execution. It uses the Python standard library, resolves files relative to itself, prints its result to stdout and does not run downloaded code, renderers, applications or network requests. The original prompt's hard-coded hash remains valid because the prompt is byte-identical.

Run from a checkout of this directory, with Python 3:

```sh
python3 verify_research.py
python3 verify_export.py
```

The first command repeats the original research's structural, traceability and analytic checks. The historical [VERIFICATION.json](VERIFICATION.json) records the original **43/43** result. A separate fresh run on the export is recorded in [EXPORT-VERIFICATION.json](EXPORT-VERIFICATION.json), labeled as export validation. These are repeated checks of overlapping evidence, not 86 independent tests.

The second command checks current export hashes, inventory closure, relative links, JSON/CSV consistency, privacy-path patterns, example bindings and small analytic invariants. It writes no files. It does not contact external URLs. Its result is not a new native-render certificate. A manifest cannot authenticate itself; the publisher must retain its separately reported SHA-256 and verify the repository commit carrying it.

The following preserved historical utilities have different behavior and are not part of the read-only export check:

- check_links.py performs network HEAD requests and writes LINK-CHECK.json with a backup. It measures transport, not source truth.
- integrate_sources.py rewrites the integrated JSON/CSV ledgers with backups.
- review/review_checks.py writes its result file without creating a backup.

If those utilities are needed later, use a disposable working copy and preserve the published evidence. They were not executed during this export.

## Limits retained

Native rendering, continuous video review, listening, browser-font rendering and cross-platform parity remain **NOT_RUN**. Source videos remain **NOT_VIEWED** where so labeled. The example sidecar still has blocked preflight, unavailable font bytes and no client approval. The code snippets and proposed contracts are research material, not a shipped renderer or an approved integration.

The export reruns document/analytic checks only. Existing external-link transport results remain historical; external endpoints were not rechecked for this publication. All original source URLs are unchanged, and the export introduces no new external source URLs. Relative-link validation checks file existence, not every Markdown anchor or external page section.

No redistribution license is inferred from a tutorial, repository link or accessible asset. The pack preserves its original rights notes. It contains original authored research and the stated small original example asset; it does not bundle third-party source archives, media, font files or full manuals.

## Export bookkeeping

EXPORT-MANIFEST.json records all 74 source dispositions and hashes for the new portability/verifier/result artifacts. The manifest itself is excluded from its own hash list to avoid self-reference. Public artifact count is 51 files: 47 retained source files plus this wrapper, the export verifier, its fresh research-check result and the manifest. The publisher's private inventory, preparation script, full diff and final checker output are not part of the source-pack.

