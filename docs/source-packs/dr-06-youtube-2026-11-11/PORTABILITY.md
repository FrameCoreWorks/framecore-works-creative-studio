# DR-06 portable research source pack

This pack preserves the complete final Polish authored research on code-based animated YouTube series. Start with [REPORT.md](REPORT.md), then the [implementation handoff](IMPLEMENTATION_HANDOFF.md), [series bible and workshop](SERIES_BIBLE_AND_WORKSHOP.md), and [independent review](review/REVIEW.md). The original user specification and its digest are preserved byte for byte in PROMPT.md and PROMPT.sha256.

## Preservation and provenance

All 38 retained source files are byte-identical. The 36 excluded files are dated backups, individually listed with their original SHA256 in EXPORT-MANIFEST.json. No final authored report, catalogue, source registry, original format, economics model, contract, benchmark plan, review, or execution disclosure was shortened. No raw third-party manual, downloaded code archive, credential file, or cache was found in this source inventory. No source locator was rewritten; no private absolute host path was detected in retained text. Historical reviews and their evidence concern their original snapshots, not a newly certified implementation.

The actual researched repository pins remain those in [baseline/repositories.json](baseline/repositories.json): Studio `de4c70fb3f372492b75f50ae831cfd7973de8bf7`, Toolbox `adc8094f8e087889e4337c99dd0d267ae1b11a51`, Open Assets `889471fcdbc2216ddc465715eff0e82784d5b8ee`. These are research baselines, not assertions about a later publication commit. Public links and access labels are unchanged; publication did not re-open or revalidate external sources.

## Repeatable checks

From this directory, run `python3 verify_artifacts.py` and `python3 verify_export.py`. Both are read-only standard-library document checkers. The first checks the original research's catalogue consistency, required files, source references, CSV/JSON agreement, prompt digest, review status, local links, and unexecuted benchmark labels. The second checks manifest hashes, file closure, unchanged retained bytes, JSON readability, local Markdown destinations, known private-locator patterns, and explicit evidence limits. EXPORT-VERIFICATION.json records a fresh run on this export separately from historical review evidence. The manifest intentionally excludes its own digest; the publisher records that digest separately.

`build_evidence_index.py` is the original, preserved **mutating index builder**, not a verifier. It rewrites SOURCES.json and EVIDENCE_STATS.json and may create backups. It was inspected but not executed for publication; use it only on a disposable working copy if rebuilding indexes is intended. Rebuilding makes the current manifest stale.

## Evidence limits that remain

The viewing scope is **11 films with sampled static frames, 7 exported transcripts, 0 full watches, and 0 audio listens**. Frame observations and transcript access are described in [VIEWING_LOG.md](evidence/VIEWING_LOG.md); original host screenshots/transcripts are not independently portable audiovisual evidence in this pack. The source review explicitly could not reproduce those host-only observations. Twelve deep-dive cards do not imply twelve complete audiovisual analyses.

The catalogue is a purposeful sample with disclosed missing metadata. Public-source counts do not measure evidential depth. Production type, source-access method, creator claims, technical evidence, and inference remain distinct. Milo's claimed code-rendered workflow has no audited public production repository here. The proposed formats, episode sidecar, continuity fields, adapter rules, and economics are proposals or explicit assumptions, not demonstrated product capability or measured production costs.

All five runtime benchmarks remain **NOT_RUN**. No renderer, model, provider, adapter, lipsync pipeline, cache pipeline, full pilot, or historical project was executed for this export. No native certification, legal clearance, source-truth verification, or audiovisual quality acceptance follows from the document checks. Local link checks cover destination files, not Markdown anchors, external transport, or content accuracy. Pattern scanning is bounded and is not a security certification. An implementation must perform the handoff's actual tests and full audiovisual review before claiming production readiness.
