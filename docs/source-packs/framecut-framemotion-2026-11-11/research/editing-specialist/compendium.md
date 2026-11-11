# FrameCut specialist: FCP, Avid and assistant-editor decisions

Research date: 2026-11-11 Europe/Warsaw. Eight original decision cards, not implemented FrameCut features. The manual workflows are proposed exercises using documented concepts. No native NLE was opened; no footage was watched, heard, rendered or conformed. Sources and access limits are recorded in source-ledger.json. All agent/data mappings below are **proposals**, not assertions about current APIs. No transport, installer, entitlement or host integration is implied.

## S01 — Preserve editorial attachment, not just vertical position

**Documented basis.** FCP connects clips to primary-storyline content; changing that content can carry its connections. The attachment point is editable. This is a relationship, not simply a fixed video-track coordinate. [Apple: connected clips](https://support.apple.com/en-bh/guide/final-cut-pro/ver7a77ef9e/mac)

**Why / manual workflow.** A label should follow the demonstrated object when the demonstration moves. Inspect the connection frame, move the parent, then try deleting or trimming across it in a disposable duplicate. Compare against a music bed intended to retain its absolute timing. Do not infer ownership from where a rectangle appears.

**Agent mapping.** Represent parent identity, anchor time, local offset and explicit move/delete policy separately from compositing order. Translate into tracks only with a documented flattening policy. Preview the dependent changes before committing.

**Counterexample.** A legal end card belongs to a delivery milestone, not whichever clip happens to sit beneath it. Following the parent would break the fixed duration.

**Artifact check.** Before/after event graph and reference render must show which events followed, stayed or became unresolved. Test a deleted anchor and nested storyline; a matching total duration is insufficient.

## S02 — Roles are a sound classification; stems are a delivery decision

**Documented basis.** FCP roles classify clip function. Its role export can separate or combine roles/subroles, with channel-layout choices. The export settings, not lane appearance alone, determine the delivered grouping. [Apple: roles](https://support.apple.com/en-asia/guide/final-cut-pro/verb71cbcbe/mac), [Apple: role export](https://support.apple.com/en-mk/guide/final-cut-pro/verc9c84cdbc/mac)

**Why / manual workflow.** Assign dialogue, music and effects by listening to actual content. Prepare the recipient's requested stems; document whether narration, production dialogue and localization are separate. Check the intended range and output channel order before export.

**Agent mapping.** Keep semantic role, source channel identity, processing chain and output bus/channel map as distinct fields. Require an explicit stem manifest; never infer a role from track number or filename.

**Counterexample.** A camera clip may contain speech and useful production sound; classifying the whole file as dialogue can omit effects from a music-and-effects delivery. A stereo file may contain two independent microphones.

**Artifact check.** Listen to each stem, check common start/duration and channel labels. Compare the authorized stem recombination with the reference mix under its declared processing conditions; shared nonlinear bus processing can prevent a simple numerical sum from reproducing that mix.

## S03 — A bin is organization; a master clip is a media reference

**Documented basis.** The Media Composer 2025 guide identifies master clips as references to media and distinguishes object types in bins. Avid's NEXIS|EDGE article describes assistant preparation and shared-bin locking in that particular product workflow. [Avid guide, printed 241](https://resources.avid.com/SupportFiles/attach/Media_Composer/Media_Composer_v2025.x_Editing_Guide.pdf), [Avid EDGE](https://www.avid.com/resource-center/avid-nexis-edge-intro)

**Why / manual workflow.** Assistants organize dailies, record source metadata, produce selects and hand over sequence revisions. Preserve the media relationship when renaming a useful select. Make ownership and revision explicit before another editor changes the same sequence.

**Agent mapping.** Separate immutable source identity, human label, selected interval, timeline occurrence and collection membership. Several occurrences may reference one source. Keep revision ownership in the project contract; do not claim that a local JSON lock provides Avid shared-bin interoperability.

**Counterexample.** Two cameras both produce C001.mov; merging records by label silently combines different performances. Duplicating a sequence should not duplicate or overwrite its source files.

**Artifact check.** Rename and duplicate controls must retain source references while new sequence revisions remain distinct. Verify each occurrence resolves to its intended take. Native bin interchange and concurrent native editing remain untested.

## S04 — Synchronization is an evidence-backed relationship

**Documented basis.** Avid documents AutoSync using matching timecode, marked common events, or waveform analysis; angle grouping is a different operation. The indexed guide contains option-dependent batch wording, so this research does not assert one universal batch limit. [Avid guide, printed 492](https://resources.avid.com/SupportFiles/attach/Media_Composer/Media_Composer_v2025.x_Editing_Guide.pdf)

**Why / manual workflow.** Check the slate or another identifiable event; preserve recorder-channel identity and camera scratch sound as distinct sources. Verify synchronization later in the take before trusting the assembly. Only then decide which angle serves the scene.

**Agent mapping.** Store the chosen reference clock, offset, method, supporting events and residual disagreement. Treat an algorithmic match as a candidate. If drift is observed, require an explicit clock/retime model rather than repeatedly changing one offset.

**Counterexample.** Repeated music can yield a convincing but wrong waveform match. A clap aligned at the beginning does not demonstrate the ending is synchronized; sound travel can also complicate the chosen event.

**Artifact check.** Review identifiable start/middle/end events and microphone identity, with measured offsets and playback observations. A correct transcript does not establish lip sync. Native AutoSync, multicam and drift correction are NOT_RUN.

## S05 — Relink is identity plus a clock mapping

**Documented basis.** Avid's relink guidance pairs metadata with source timecode and calls out frame-rate and search restrictions. It recommends testing conform early. These are documented native workflow conditions, not a FrameCut matching implementation. [Avid: relink troubleshooting, updated May 7, 2026](https://kb.avid.com/pkb/articles/en_US/Knowledge/Troubleshooting-relink-No-Clips-Were-Relinked)

**Why / manual workflow.** Test a short edit against the originals during ingest. Compare source starts, selected boundaries, channels and orientation; retain the proxy until the verified original replacement is accepted.

**Agent mapping.** Store original and derivative hashes separately, linked by an explicit derivation record. Match stable source metadata and clock mapping; reject ambiguous candidates instead of choosing the first matching basename. Hash equality is not expected between an original and a transcoded proxy.

**Counterexample.** Matching filename, duration and thumbnail can still select the wrong take. A proxy starting at zero does not share the original's timecode origin.

**Artifact check.** Use a deliberately wrong candidate and verify rejection. Compare several interior edit points, not only endpoints. Record unresolved matches and the native importer version. A successful relink dialog alone is not a conform pass.

## S06 — Trim geometry constrains a decision; it does not choose it

**Documented basis.** Apple describes slip as changing the used source while retaining its slot, and roll as moving a shared cut while preserving combined duration. OTIO separates available, selected, transition-visible and parent-coordinate ranges. [Apple: slip](https://support.apple.com/en-ie/guide/final-cut-pro/ver1632d8e4/mac), [Apple: roll](https://support.apple.com/en-mz/guide/final-cut-pro/ver1632d9ae/mac), [OTIO: ranges](https://opentimelineio.readthedocs.io/en/latest/tutorials/time-ranges.html)

**Why / manual workflow.** Slip to reveal the right action inside an already correct slot. Roll when the switch of attention is wrong but the surrounding timing should stay. Scrub both source handles and play both joins; unused media can contain a blink, slate or incomplete word.

**Agent mapping.** Specify half-open intervals with rational rates and explicit coordinate spaces. Validate requested source coverage including transitions, but separately protect meaningful events and audio relationships. A proposal should explain what new frames reveal and what omitted frames conceal.

**Counterexample.** A valid roll can delete the reaction that motivated the shot. A slip of picture alone can desynchronize speech.

**Artifact check.** Verify arithmetic, source bounds, fixed milestones and sync. Compare alternatives at speed. OTIO permits intentionally unavailable source ranges for some workflows; available-range bounds are a delivery policy, not a universal schema invariant.

## S07 — Interchange has two limits: the format and this adapter

**Documented basis.** Apple's documented DTD here is FCPXML 1.10; it uses rational seconds and warns that structural validity does not guarantee import. FCP7 XML and FCPXML are distinct. Current OTIO documentation separates its core storage adapters from additional plugins. [Apple DTD](https://developer.apple.com/documentation/professional-video-applications/document-type-definition.md), [OTIO adapters](https://opentimelineio.readthedocs.io/en/latest/tutorials/adapters.html)

**Why / manual workflow.** Inventory cuts, layers, transitions, retimes, titles, sound and grades before choosing an export. Agree what stays editable and what may become a rendered replacement. Test the chosen route on a representative short sequence.

**Agent mapping.** Pin format dialect, writer/reader versions and adapter revision; emit a per-element result: preserved, baked, rebuilt, omitted or blocked. Keep the full authoritative project and reference alongside the transfer.

**Counterexample.** An adapter's missing transition support does not prove the XML format lacks transitions. A parser roundtrip can preserve names while destroying the intended picture.

**Artifact check.** Inspect the declared feature matrix below, then import into the actual recipient and compare boundaries, sources and playback. No native roundtrip is certified here.

## S08 — Turnover is an agreement with sound and color

**Documented basis.** Avid's AAF export options include handles and choices affecting audio rendering/channel treatment. FCP can export role-based files. Neither fact establishes a universal interchange preset. [Avid guide, printed 1170](https://resources.avid.com/SupportFiles/attach/Media_Composer/Media_Composer_v2025.x_Editing_Guide.pdf), [Apple role export](https://support.apple.com/en-mk/guide/final-cut-pro/verc9c84cdbc/mac)

**Why / manual workflow.** Ask what the receiving operation needs: source flexibility for sound repair, editable clip levels, clean picture for grading, approved graphics, reference mix and visible timecode. Agree handles and retained effects before consolidation. Keep an untouched turnover revision.

**Agent mapping.** Produce a manifest with sequence revision, rate/timecode origin, media lineage, requested handles, channel map, color-transform ownership and all baked decisions. Separate reference viewing transforms from source encoding. A later picture change needs a new revision and change list, not an overwritten delivery.

**Counterexample.** A reference with a creative look is not necessarily the media a colorist should grade. Flattening dialogue into one stem can remove alternate microphones a mixer needs.

**Artifact check.** Receiver checks missing media, boundary sync, effects and reference agreement. Inspect returned sound/color against the same revision. Delivery completeness, native import success and creative acceptance are separate outcomes.

## Adapter evidence matrix — documentation only

These are selected claims in the linked adapter READMEs, not exhaustive format capabilities, installed versions or successful native tests. Repository main branches are mutable; implementation must pin and revalidate them.

| Route | Documented capability/limit relevant here | Planning consequence |
|---|---|---|
| [CMX3600 adapter](https://github.com/OpenTimelineIO/otio-cmx3600-adapter/blob/main/README.md) | One video track; transitions and linear speed listed supported; nesting and effects unsupported. Reader rate defaults to 24. | Declare rate explicitly; never silently flatten multiple picture layers. |
| [AAF adapter](https://github.com/OpenTimelineIO/otio-aaf-adapter) | Transitions/markers listed read and write; effects unsupported; linear speed read supported, write unsupported. | Do not infer symmetric speed preservation or equate adapter output with Media Composer's native exporter. |
| [FCP7 XML adapter](https://github.com/OpenTimelineIO/otio-fcp-adapter) | Tracks, audio and nesting listed supported; transitions/effects/speed unsupported. | Audit those elements before conversion; XML syntax does not restore them. |
| [FCPX XML adapter](https://github.com/OpenTimelineIO/otio-fcpx-xml-adapter) | Tracks, audio and nesting listed supported; transitions/effects/speed unsupported. | Treat it as a separate route with its own tested loss report. |

## Research boundary

This expands FCP/Avid/interchange knowledge, not native proficiency. Read methods include official indexed excerpts where direct requests failed; the Avid guide was not fully downloaded/read. Current native bin behavior, AAF consolidation details, plugin/effect translation, ScriptSync/PhraseFind, simultaneous collaboration, DF edge cases, VFR conform and sound/color delivery remain exercises to run. No professional qualification or complete editorial curriculum is claimed.
