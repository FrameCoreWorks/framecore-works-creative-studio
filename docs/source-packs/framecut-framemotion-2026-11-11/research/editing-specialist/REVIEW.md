# Independent review of the FrameCut editing compendium

Reviewer: environment_inventory specialist; 2026-11-11. Reviewed another agent's work, without editing it. Verdict: **useful applied research with one concrete workflow correction required; no native proficiency or interoperability certification**.

## Scope and evidence

Read C01–C22, W01–W06, the curriculum/evaluation sections and the source ledger in:
- [original local research]/research/editing/applied-editing-compendium.md
- [original local research]/research/editing/source-ledger.json

Reviewed content hashes: compendium SHA-256 `605a3a7133bfb607ba853f07bc8d214394b5087e1b49371c54b2c2afba37cabf`; ledger SHA-256 `fe6d29a741013956cc0a701ccb4bef69d1f37208aaccdd56e190f246e8147433`.

Independently checked selected local claims against frozen opencut-video-studio runtime README, SKILL and framecut.py/write_export. Independently read Apple/Avid/OTIO primary material in this specialist's ledger. Recalculated lead W01, W02 and W04 using exact fractions; did not execute its editing workflow, review native output, independently reread all 24 outside sources or verify every local-runtime statement.

## R01 — Correct W06's expectation of a partial basic export (medium)

**Location:** lead compendium W06, line277. It describes a sequence with variable speed and a dissolve, then directs the reader to export supported cuts and the loss report. That suggests the current exporter extracts a supported subset.

**Observed implementation:** [framecut.py:88](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/2942af902909b83441fc4c428d9debd532500c5a/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/framecut.py#L88) sets `complex_edit` for a transition, speed curve, freeze or non-unity speed. At lines105–116 the whole basic EDL/OTIO branch is withheld. The operation still writes native project JSON, relink.json, shots.csv and loss-report.json. The README at line121 confirms that policy.

**Required clarification:** for this mixed sequence, first retain those actual artifacts and the reference. A separately approved simplified or baked derivative is needed before a basic cuts export can be attempted; it is not emitted automatically from the mixed original. This is a documentation correction, not a request to weaken the exporter or implement conversion. No reproduction process or product file was changed.

**Impact:** otherwise an assistant may promise picture.edl/picture.otio that the current workflow intentionally does not produce. The existing C21/W06 warnings about native imports remain valid.

## Arithmetic review

| Lead case | Independent result | Assessment |
|---|---|---|
| W01 source origin | 900000 + 2.4 × 90000 = 1116000 ticks | Correct |
| W01 source duration | 50 / 25 × 90000 = 180000 ticks; exclusive out1296000 | Correct |
| W01 transient | (1170000−1116000)/90000 =0.6s; 250+15=265 | Correct |
| W02 roll | 110+90=200; incoming source-in advances10 at unity speed | Correct for independent baseline proposal |
| W02 slip | Source span starts4 frames earlier; record slot remains100 frames | Correct geometry; preserved reaction still needs real-media review |
| W04 music | 120 quarter-note BPM →0.5s/beat;4/4 →2s/bar;8 bars→16s | Correct under explicit musical assumptions |
| W04 constant retime | 4s source /2 =2s record | Correct |

No arithmetic error found in these checks. W01 correctly leaves VFR decoded-frame selection open. W04 correctly avoids deriving a general speed-ramp duration from endpoint speeds. These are mathematical checks, not perceptual or rendered results.

## Judgment quality and factual restraint

The compendium advances beyond button instructions: it asks what the viewer learns, protects qualifiers and hesitant performance, distinguishes a musical phrase from beat detection, tests sound context, and treats color continuity as a viewing decision. Its counterexamples can falsify a superficially valid edit. The proposed rubric keeps meaning, sound, picture, accessibility and technical evidence separate rather than averaging away a serious failure.

Several important limits are explicit and should survive consolidation: no footage watched/heard, no rendered exercise, no native app operated, no taste inferred from source counts, no Murch percentage scoring, no universal loudness target, no presumed LUT pipeline, and no automatic multicam/HDR claim. C10's independent-dialogue mapping matches the runtime's documented caption-source requirement; C16's source PTS and master rational FPS match README45. C17's variable-speed pitch caveat and C22's review assertions also agree with the inspected contract.

There is no basis here to certify actual editing skill, native Avid operation, sound mixing, color grading or full plugin behavior. This review validates reasoning and selected references, not execution coverage.

## Source coverage: what 24 means

The lead ledger contains24 entries:17 tagged WEB_TEXT_READ,3 targeted downloaded-PDF text reads,2 official indexed bodies with direct429,1 other official indexed text and1 historical Avid excerpt with access limits. The WEB_TEXT_READ category itself includes bounded text extraction/selected sections and the Academy PDF; it must not be summarized as17 entire manuals or sites read.

Resolve evidence is concentrated on selected pages of three version20 books. The PDF page numbers and printed page numbers are separately recorded, which is useful; their complete contents were not reviewed. Interviews establish practitioners' accounts, not universal controlled findings. The ASC video was explicitly not watched. The old Avid2021 excerpt cannot establish current native behavior. Source ledger counts are provenance breadth; they are not function coverage or proof of retained competence.

This specialist adds15 primary entries, including current Avid2025 indexed sections and the2026 relink article, eight cards and three calculated exercises. Counts are additive only as **entries** until canonical URLs/documents are deduplicated across both ledgers. The same underlying article in another locale/version is not necessarily new knowledge. Avid PDF access limits still apply; native-app status remains NOT_RUN.

## Remaining gaps to keep visible

1. Current Avid bin/master/source identity, AutoSync and AAF behavior need versioned native exercises; indexed passages cannot settle all option-dependent behavior. ScriptSync/PhraseFind and shared-storage concurrency remain untested.
2. The lead has no completed licensed-media assessment demonstrating reaction timing, speech preservation, eye-trace, sound continuity or color matching. Its curriculum is a plan for acquiring that evidence.
3. Interchange requires a pinned adapter and named native recipient; README feature matrices are not acceptance tests. Include a wrong-take relink control and mixed-feature loss control.
4. Local FrameCut statements are tied to the frozen revision; standalone extraction must preserve or deliberately revise these semantics. This review did not run its source code or audit every command.
5. No independent source-by-source word-budget or comprehensive factual re-audit was performed for the lead document. Its explicit access limitations should remain attached to any shorter summary.

No other high-impact contradiction was identified within this bounded review. Root owns synthesis and any requested edits; this file does not mark R01 fixed.


## R01 closure — independently verified

At 20261110T232130Z, reread the root-edited W06. It now explicitly states whole-sequence EDL/OTIO withholding for complex edits, names the remaining native JSON/relink/CSV/loss artifacts, and requires a separately agreed simplified or baked derivative before cuts transfer. This agrees with the inspected frozen exporter. **R01 is CLOSED for this document revision.** No product implementation was changed.

Post-correction compendium SHA-256: `bf09aa8ed387e25b0144595a60be2b72b0c9fb3697e92b5637b0fe927bf84fda`. The earlier hash and finding above intentionally retain the reviewed history. Backup of this review before appending closure: `backups/20261110T232130Z/REVIEW.md`. Root also independently reran this specialist’s three-case calculation script and reported exact agreement with its saved JSON; native-editor and perceptual tests remain NOT_RUN.
