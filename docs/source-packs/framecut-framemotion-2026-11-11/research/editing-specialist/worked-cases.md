# Three original assistant-editor exercises

Date: 2026-11-11. Invented media and timings; no copyrighted lesson footage is used. Arithmetic was checked using Python fractions in verify-calculations.py; results are in calculation-results.json. Native import, rendering, listening and editorial acceptance are **NOT_RUN**. All intervals below are half-open and speed is unity unless stated.

## W01 — Source, record and handles are three separate questions

**Brief.** Deliver a four-second demonstration excerpt to a finishing editor while leaving modest trim flexibility. Source media contains 500 frames at 25/1 fps and starts at source timecode 10:00:00:00. Select source-frame offsets [100,200); place them at record offsets [250,350) in a sequence whose timecode origin is 01:00:00:00.

**Calculation.** Selection duration = 100 frames = 4 seconds. Source labels run from 10:00:04:00 to the exclusive boundary 10:00:08:00; the last included frame is 10:00:07:24. Record labels run from 01:00:10:00 to exclusive 01:00:14:00; the last included frame is 01:00:13:24. A source event at offset 125 maps to record 275, or 01:00:11:00.

Requesting 12 frames of handles on both sides creates [88,212), 124 frames, 4.96 seconds. Those extra frames are delivery media, not automatically additional timeline duration. If the new file begins at original offset 88, the used section starts at file-relative offset 12; its source-timecode origin must remain separately recorded.

**Transition experiment.** For a deliberately defined 24-frame centered dissolve at the cut, this exercise allocates 12 frames beyond the outgoing cut and 12 before the incoming cut. That allocation is an exercise convention; verify the actual editor/adapter offsets. Our source has the required outgoing extent through offset 212. The incoming source must independently supply its preceding 12 frames. An outgoing endpoint of 496 with the same request would require 508, exceeding this source by eight frames: reject or explicitly redesign, never pretend the requested handle exists.

**Editorial decision.** Twelve available frames of a hand leaving the product may be suitable; twelve frames containing a slate are not. Compare the hard cut with the dissolve and ask whether superimposing two product states confuses the demonstration.

**Artifacts.** Source/record map, first/last selected images, both handle previews, delivered-file origin and reference movie. Pass arithmetic independently from the editor's judgment. OTIO's distinct range concepts motivate this separation; its data model is not proof the requested media was decoded. [OTIO ranges](https://opentimelineio.readthedocs.io/en/latest/tutorials/time-ranges.html)

## W02 — A slip and a roll solve different problems

**Baseline.** At 25/1 fps, shot A occupies record [0,100), using source A [50,150). Shot B occupies record [100,200), using source B [200,300). An end card begins at record 200. Sources extend sufficiently beyond all proposed bounds.

**Proposal 1, slip B by +10 source frames.** Keep B at record [100,200), use B [210,310). Its duration remains 100 frames; the pair remains 200 frames. Source action B=220 now appears at record 110 instead of 120. Later source content enters earlier in the fixed slot. Compare both B joins, not only the action.

**Proposal 2, independently roll the original cut +8 record frames.** A becomes record [0,108), source [50,158); B becomes record [108,200), source [208,300). Durations 108 + 92 = 200. The end card stays at 200. A surviving B event at source 220 remains at record 120. This roll removes B's earlier source frames; it does not slide the retained B performance in record time.

**Meaning constraint.** Suppose the protected reaction is B [205,209). The original shows all four frames. Proposal 1 shows none. Proposal 2 shows only frame 208, losing three frames. Both operations are geometrically valid; neither satisfies the protected-reaction requirement. Consider an earlier B selection, different coverage, or retaining the original. Do not call a successful arithmetic check an improved edit.

**Audio constraint.** If B is synchronized dialogue, evaluate linked sound explicitly. A picture-only slip changes lip synchronization; a picture roll with continuous independent dialogue may be an intended split edit. No blanket rule selects one.

**Artifacts.** Candidate maps, two join comparisons, protected-event survival and picture/sound review. The two proposals start from the same baseline and must not be accidentally compounded. If deliberately compounded, the slip-then-roll B span would be [218,310), a separate candidate. Documented slip/roll semantics are from Apple; all values and judgment constraints here are original. [Slip](https://support.apple.com/en-ie/guide/final-cut-pro/ver1632d8e4/mac), [roll](https://support.apple.com/en-mz/guide/final-cut-pro/ver1632d9ae/mac)

## W03 — A plausible relink followed by a lossy interchange

**Invented ingest record.** Original O is camera A / card 07 / take 03, 24/1 fps, 2400 frames, source timecode 10:00:00:00. Proxy P was created from O with a verified frame-for-frame map, a different resolution and a different file hash. The edit uses P [240,480), ten seconds.

Candidate X has matching lineage and source clock: the same offsets are valid. Candidate Y has the same basename and a similar thumbnail but is another take at 25/1 fps, 2500 frames. Both files last 100 seconds. Matching only filename and duration would accept Y incorrectly. Treating the same 240-frame span as 25fps produces 9.6 seconds; translating ten seconds to 250 frames fixes duration but cannot fix wrong content. A hash mismatch between O and P is expected; a missing derivation relationship is the actual unresolved evidence.

**Separate rational-rate control.** At 30000/1001 fps, 30000 frames last 1001 seconds. At 30/1 they last 1000 seconds. Rounding the rate creates a one-second discrepancy over that frame count. This calculation concerns elapsed time; it does not implement drop-frame timecode numbering.

**Interchange challenge.** Add a second picture layer containing a title, a 24-frame dissolve, a 50% speed segment and labeled independent sound. The CMX3600 adapter's single-picture-track limit demands an explicit layer decision. The documented AAF adapter cannot write linear speed; the documented FCP7/FCPX adapters do not preserve transitions or speed. These are adapter limitations, not claims about everything those native file formats can represent. [CMX3600](https://github.com/OpenTimelineIO/otio-cmx3600-adapter/blob/main/README.md), [AAF](https://github.com/OpenTimelineIO/otio-aaf-adapter), [FCP7 XML](https://github.com/OpenTimelineIO/otio-fcp-adapter), [FCPX XML](https://github.com/OpenTimelineIO/otio-fcpx-xml-adapter)

**Decision.** Preserve the complete project; negotiate editable elements versus approved renders. Supply an identity map, reference movie with declared clock labels, sound manifest and one outcome per element. Do not silently strip the title or make the slow shot play normally. Native FCPXML, native AAF and OTIO JSON are different delivery routes.

**Artifacts / falsification.** Wrong-take candidate must fail matching; legitimate proxy hash difference must not fail lineage validation. Recipient opens the chosen route in a named version, verifies each source/boundary and compares the complete reference. A parser test, equal duration and an online-media status cannot alone pass this exercise. [Avid relink guidance](https://kb.avid.com/pkb/articles/en_US/Knowledge/Troubleshooting-relink-No-Clips-Were-Relinked)
