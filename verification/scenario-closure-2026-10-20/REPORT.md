# FrameCore Works scenario recovery and artifact review

Date: 2026-10-20. Source: `77b316a0cb2907111e9ea54b050fcf314be22f2a`, package **1.111.1**.

Completed **44 scoped artifact exercises: 41 accepted directly and 3 accepted after local artifact repairs**. These are the frozen replacement R01–R43 set plus explicit supporting Storytelling R44. This is a non-blind source-guided review by the resuming assistant, not an independent benchmark or a fresh installed-plugin evaluation. The runtime package was not changed.

## Recovery and evidence limits

Only an early checkpoint survived: 21 execution records (including incomplete R07 and R22), partial media materials and 12 recorded earlier reviews. Missing outputs were rebuilt. Earlier narrative claims of “42 passes plus 2 after fixes” are not treated as recoverable results. R identifiers belong to this reconstructed suite, not to the lost original prompts. Existing execution records and reviewer labels are preserved as history; `final-review.json` states the actual current review method.

The checkpoint's 1505 candidate file hashes match source. The canonical validator passed, as did `bash scripts/check_all.sh`: Node 225 passed / 13 skipped; Python 401 passed / 4 skipped; zero failures. Canonical planned host scenarios retain their original not-run status. There were no paid provider calls. Model token usage and per-case reasoning settings for this resumption are not exposed and are not invented.

The archive contains actual documents, images, PDFs, spreadsheets, renders, project sources, commands, failures, measurements, case findings and a SHA-256 manifest. Generated dependency folders and transient browser/render work directories are excluded. Reproduction requires the versions recorded in the projects and local commands; absolute historical working paths need rebasing.

## Observed repairs

- **R35:** the native extended render had a tiny re-encoding difference in frame 179. The final `E/R35/extended-preserved.mp4` is an explicitly labelled FFmpeg lossless derivative: all 180 original decoded frames are exact and the 60 appended frames equal the last original frame. The native HyperFrames render remains as `extended.mp4`.
- **R40:** initial export paths pointed at absent assets. The rejected export is retained; the corrected portable asset folder passes OTIO roundtrip checks for all three 60-frame clips.
- **R43:** strict lint rejected an audio element without an ID. Adding the ID enabled the render. The wrong-price negative test rejects 89 zł. Exact-copy matching succeeds, but the full fidelity checker still reports `not_verified` because its product/source visual-review flag was not supplied. The encoded frame was separately viewed; this is not a fabricated full-checker pass.

These are repairs to exercise artifacts, not proven defects in Studio instructions. They do not justify a new package release.

## Scope of acceptance

`PASS_SCOPED` means that the listed artifact satisfies the frozen exercise criteria within the stated limits. It does not certify commercial creative quality, print production, actual product behavior or host orchestration. Audio was measured, not listened to. The storyboard PDF is raster: empty text extraction is expected and its three panels were checked visually. OpenCut native UI, external Hipson, paid generation and fresh ChatGPT/Work/Codex sessions were not run. An optional extra DOM capture stalled and was stopped; it is not used as evidence.

| Case | Result | Finding |
| --- | --- | --- |
| R01 | PASS_SCOPED | Byte-identical Polish canonical welcome; no added bytes. |
| R02 | PASS_SCOPED | Brief retains waitlist, EUR 900 and seven days; recommendation and user choice remain explicit. |
| R03 | PASS_SCOPED | Project-only preferences and resumable state; no global settings mutation. |
| R04 | PASS_SCOPED | Real hashes, duplicate fixture and absent portrait identified; rights remain unverified. |
| R05 | PASS_SCOPED | Standalone handoff includes sources, exact copy, protected logo/price and acceptance rules. |
| R06 | PASS_SCOPED | Named Producer alias was read; its audio scope is disclosed and production planning is handed to Instruction Packet Factory. |
| R07 | PASS_SCOPED | Available input files inventoried with hashes; synthetic/raw status and editable fields explicit; no invented final ad. |
| R08 | PASS_SCOPED | 49 $ conflicts with locked 49 €; minimal currency repair, text-only review disclosed. |
| R09 | PASS_SCOPED | Two recorded currency errors distinguished from root-cause hypotheses; targeted pre-export check, no package edit. |
| R10 | PASS_SCOPED | Exhausted two-repair budget retained; unresolved currency blocker is not falsely approved. |
| R11 | PASS_SCOPED | Segments, funnel, creative matrix and measurement plan; unsupported savings excluded. |
| R12 | PASS_SCOPED | Three concrete format plans preserve price, slogan and logo; deliverable is a specification. |
| R13 | PASS_SCOPED | Three contiguous five-second shots plan write, wipe and reuse; product proof is planned, not a claim of filming. |
| R14 | PASS_SCOPED | Four complete posts, one waitlist goal, channel schedule and measurable test; no invented performance. |
| R15 | PASS_SCOPED | Timed 20-second presenter demonstration; no fabricated customer testimonial. |
| R16 | PASS_SCOPED | 30 × EUR 0.20 plus six editing hours: EUR 306, versus EUR 300 local; assumptions and reserve separated. |
| R17 | PASS_SCOPED | Bounded local Hipson packet with sources, exclusions, criteria and handoff; no external execution claimed. |
| R18 | PASS_SCOPED | Ada identity, green sweater and anatomical left-hand prop preserved across three shot plans. |
| R19 | PASS_SCOPED | Six timed intervals total 30 seconds; character choice causes the payoff, with product as a tool. |
| R20 | PASS_SCOPED | Concrete lens, composition, light and physical continuity plan for three feasible shots. |
| R21 | PASS_SCOPED | Overlapping time, switching hands and impossible notebook reveal identified and minimally repaired. |
| R22 | PASS_SCOPED | Actual two-page PNG/PDF storyboard contains three legible panels; XLSX/CSV have three shot rows. Raster PDF requires visual review. |
| R23 | PASS_SCOPED | PCM measurement identifies five pulses and maps five changes; no invented listening or lyrics. |
| R24 | PASS_SCOPED | 14 hours × EUR 50 = EUR 700, plus EUR 70 reserve; optional generation increases total to EUR 776.60. Tax unknown. |
| R25 | PASS_SCOPED | Three copy variants and actual checker transcript retain case, currency, punctuation and contact. |
| R26 | PASS_SCOPED | Concise rewrite preserves locked facts; before/after comparison retained. |
| R27 | PASS_SCOPED | Actual SRT/VTT and six-second MP4; cue timing bounded and earlier visual review of Polish glyphs retained. |
| R28 | PASS_SCOPED | Actual images and colors inspected; product authority separated from style reference and unknown rights. |
| R29 | PASS_SCOPED | Measured color and spatial relationships inform standalone image prompt; product identity is protected. |
| R30 | PASS_SCOPED | Feasible ordered six-second video prompt; constraints and reference identity retained, no provider call claimed. |
| R31 | PASS_SCOPED | Actual SVG, 1080 × 1350 PNG and approximately A4 PDF; exact Polish copy visually reviewed. No PDF/X or press-ready certification. |
| R32 | PASS_SCOPED | Only 2400 accent pixels change within [390,1040,690,1048]; geometry, embedded product/logo and copy remain identical. |
| R33 | PASS_SCOPED | Dated authoritative 40-page/220-g source prevails over older 48-page/210-g source; savings claim remains unknown. |
| R34 | PASS_SCOPED | Native HyperFrames render: 360 × 640, 6 s, 30 fps, 180 frames, audio and reviewed copy. |
| R35 | PASS_AFTER_REPAIR_SCOPED | Seek 2 → 4 → 2 deterministic. Final FFmpeg-derived extension preserves all 180 decoded frames and adds 60 exact last frames; native re-encode retained. |
| R36 | PASS_SCOPED | Original video packets preserved, five measured sound events, zero clipped PCM samples; delivered AAC measurements retained, no listening claim. |
| R37 | PASS_SCOPED | Actual analyzer commands and bounded finite tempo; clipped fixture has 191928 clipped samples, controls have zero. |
| R38 | PASS_SCOPED | Intentional 120-ms PCM delay exceeds detector threshold; repaired PCM equals control and five detected offsets return to zero. |
| R39 | PASS_SCOPED | Actual native Remotion project and render, 360 × 640, 6 s, 30 fps and 180 frames with audio. |
| R40 | PASS_AFTER_REPAIR_SCOPED | EDL/OTIO/CSV export roundtrip retains three 60-frame cuts and hashed assets after fixing relative paths. Native OpenCut UI not run. |
| R41 | PASS_SCOPED | Actual 640 × 360 HyperFrames render; four sampled encoded frames retain complete copy. |
| R42 | PASS_SCOPED | Custom reference profile actually applied; energy advice follows it while true-peak safety remains. Subjective/earshot portion unverified. |
| R43 | PASS_AFTER_REPAIR_SCOPED | New 480 × 480 / 4 s / 24 fps render; exact Polish locks viewed. 89 zł negative rejected; full fidelity checker remains not_verified. |
| R44 | PASS_SCOPED | Explicit supporting Storytelling pass adds causal logic, payoff and continuity notes to R19 without rewriting the screenplay. |

## Files

`plan.json` preserves the 43-case plan. `plan-resumed.json` adds R44. `final-review.json` contains per-case criteria and evidence directories. `measured-results.json`, `checkpoint-artifact-integrity.json`, `source-checks.log` and `source-validator.json` retain checks. `evidence-manifest.json` lists included files and hashes.
