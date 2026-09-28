# Production boundaries and handoff

Owner: delivery-documentation. Stable synthesis from static, audio and video deliverable/QA contracts. Current platform/export requirements are verified for the actual destination when material; this reference supplies no universal codec, rate or loudness defaults.

## Name the deliverable honestly

| State | What is available | What it does not prove |
|---|---|---|
| Prompt | Ready instruction with necessary locks | That a generator ran or produced a good image |
| Concept raster | Visual proposal or presentation composition | Final text accuracy, editing structure or prepress readiness |
| Reviewed digital raster | Actual file checked for its intended digital use | Editable type, vector outlines or print separations |
| Production handoff | Complete specification and source inventory | That a DTP operator completed the master |
| Production master | Actual specified editable/print deliverable, separately validated | Guaranteed printer outcome without applicable proofing |
| Audio/video plan | Script, cue sheet, shot plan or export specification | That audio/video was generated, mixed, synchronized or exported |
| Inspected audio/video | Actual source and documented reviewed ranges/method | A full-clip, all-channel or audiovisual pass when only a subset was checked |
| Verified media export | Actual output with required properties checked against its specification | Editorial acceptance, complete playback or destination compatibility unless separately tested |

Do not call a raster “print-ready” because it looks sharp or is saved as PDF. A PNG may lack alpha; a transparent-looking checkerboard may be painted. A vector-looking logo is not a vector asset.

## Compact production specification

For an ordinary final prompt, a short note is enough:

- target format/ratio and channel;
- exact approved copy or the current copy-lock ID;
- intended first read and practical information order;
- protected source assets and permitted adaptation;
- safe-area assumptions and known constraints;
- remaining inspection or production checks.

Do not add unexplained measurement precision. If the safe zone was a design assumption, label it as such. A platform or printer specification must come from the actual current source.

## DTP handoff

When editable typography, final font files, QR/barcodes, dielines, exact separations or press output are required, specify:

1. approved content inventory with exact strings and breaks;
2. actual logo/product/image sources and their governing properties;
3. concept and layout invariants;
4. known trim/format and intended use;
5. typography references/files and rights status if known;
6. required color/profile/spot-ink behavior where supplied;
7. unresolved bleed, safe zones, stock, finishing and printer requirements;
8. proofing and acceptance responsibilities.

Unknown is preferable to a guessed bleed/profile. Do not invent universal 3 mm bleed, CMYK settings or a 300-DPI claim for all work. Resolve them with the real production route.

Effective PPI equals pixel dimension divided by physical length in inches on each axis. A metadata tag does not add pixels. Enlarging a source can change apparent sharpness without establishing true detail.

Required QR and barcodes need deterministic construction and scanning against the actual destination/data. Do not claim a generated pattern works. Do not silently add a code as an alternate route around copy density.

## Separate assets and explicit code/vector requests

If the user expressly asks for layered assets or an editable/coded design, record a different deliverable. Define the assembly plan, current asset, dimensions, relationship to other elements and where exact copy belongs. Protect approved versions and name remaining manual work.

Do not present a collection of parts as a finished integrated poster. Do not use this route automatically when the original request was one-pass raster generation.

## Campaign package

List actual variants, the shared mechanism and the layout changes. Each requested format has its own reading/technical review. An asset manifest should record real file paths or IDs, version, role, approval state and unresolved checks. Hashes can establish file identity, not design quality.

Package only actual accepted outputs and necessary source/specification files. Do not invent download links or imply that an archive exists before creation. Keep rejected drafts out of a final-delivery archive unless specifically requested.

## Audio/video delivery specification

Use [audio evidence and audiovisual handoff](../../audio-production-director/references/audio-evidence-and-av-handoff.md) for cue IDs, text/voice ownership, timing basis, inspected scope and source revision. Delivery assembles these contracts; it does not silently rewrite scripts, retime scenes, re-master sound or treat an untimed transcript as synchronized subtitles.

Record each material property with `requested_value`, `verified_value`, evidence/method and unresolved status. Use `Unknown` when no value is established; omit irrelevant properties. A requested value is not a verified property of a file.

| Property group | Fields to carry when relevant | Verification boundary |
|---|---|---|
| Destination and purpose | Placement, aspect, duration target, version/language | Verify current destination requirements only for the exact requested surface |
| Picture | Pixel dimensions, frame rate/timebase, frame count, container/codec, color/alpha needs | Read actual media or authoritative export settings; extension and perceived smoothness prove none of these |
| Audio | Sample rate, channels/layout, codec, bit depth if applicable, loudness/peak requirements, stems | Distinguish requested target, metadata and actual measurement; no universal mastering default |
| Timing and sync | Measured runtime, start offset, source clock, cue/shot alignment, tails and end state | Report actual measured/inspected ranges; a planned exact duration is not a verified export duration |
| Words and captions | Exact script/transcript, language, speaker IDs, sidecar vs burned-in, requested format | Distinguish script from spoken result; verify text/timing/playback only when actually checked |
| Editability and sources | Project file, linked media, fonts, stems, clean plates, licenses when provided | A rendered MP4 or mixdown is not an editable project or separate stems |
| Review and acceptance | Owner, evidence scope, defects, accepted version, outstanding checks | Separate technical probing, listening, picture review, sync review and user acceptance |

For a media package, inventory only real files and their purpose: picture master, alternate aspect/version, clean video, audio mix, available stems, captions, copy deck or project sources as requested. Do not create or imply every item. Mark `specified`, `created`, `inspected`, `accepted` and `delivered` separately. Delivering a cue sheet does not complete a request for a rendered film; report the precise missing capability or pending operation.

When tools are actually available and the user's task authorizes their use, check the export's relevant metadata, readability/playback and affected sync boundaries. Record which checks ran. A tool reading frame count or audio duration does not constitute a full playback/listening review. Report uninspected intervals and unsupported checks without inventing a pass.

For exact-runtime work, compare requested duration with measured media duration using its actual timebase and any specified tolerance. Do not invent a tolerance or infer FPS. Verify caption ordering, intended overlaps, words and speaker assignment; runtime/player compatibility is only verified after the relevant test. Route picture/motion failures to video-prompt-architect and audio failures to audio-production-director with the source and evidence.

If a script, audio take, shot duration or accepted master changes, mark dependent cue sheets, captions, prompts and exports `review_required`. Update only affected dependencies and preserve accepted unrelated files. A previous pass applies to its specific source/version and inspected scope.

## Resume sheet

For a long task or new conversation, supply a compact transferable summary:

- current objective and stage;
- approved concept, exact copy and source locks;
- selected output/version actually available;
- open issue and next test;
- files needed to continue;
- authorization boundary.

A resume sheet records existing operation authorization and its scope; it does not create permission or bypass a real host requirement for fresh activation. Do not invent a need to reconfirm merely because a handoff occurred. It also does not create persistent memory or live task tracking.

## Release gate

Before saying “done”, confirm the requested artifact exists, the relevant checks were actually run, limitations are visible and the user can use the result. Distinguish structural validation from host behavior and actual creative-output review.

Packaging does not itself authorize upload, external publication, marketplace installation or team notification. If the user already requested and authorized a specific operation, preserve that scope and use only the actual supported route; do not add a duplicate confirmation. Missing capability, destination or materially different spend/transfer needs an explicit resolution rather than a fabricated successful delivery.
