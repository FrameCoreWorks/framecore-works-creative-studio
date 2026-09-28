# Audio evidence and audiovisual handoff

Owner: producer-ai-task-builder. Apply only the sections needed for the requested artifact. This reference adds planning and evidence contracts; it does not add a provider, analysis engine, native control or media-generation capability.

## 1. Resolve the operation and evidence

Use actual available host capabilities within the task's authorization. Read-only local inspection and public research may use tools, including MCP. A remote service that receives private audio is an external transfer; verify that this operation, source and destination are authorized. Preserve authorization already granted. Do not ask again merely because work moved between owners. A prompt request alone authorizes no generation, paid run or upload.

| Evidence state | Permitted conclusions | Boundary |
|---|---|---|
| `user_report_only` | Quote or summarize the user's reported symptom and propose a test | Do not claim to hear it or identify its exact cause |
| `asset_present_not_analyzed` | Confirm the actual file is accessible, if checked | Attachment alone proves no timing, language, quality or musical structure |
| `metadata_only` | Report only properties actually read, such as container, duration or sample rate | Metadata, waveform or file extension does not prove intelligibility, mix quality or section boundaries |
| `inspected_ranges` | State observations within recorded ranges/channels using the actual method | A partial listen, transcript, spectrum or level measurement has a narrower scope than full audiovisual review |

Record source ID/version, method/tool, ranges covered, channels/stems inspected, findings, inference and uninspected scope. A transcription method supports words and its timing evidence, not necessarily music/mix judgments. A loudness measure supports that measure under recorded conditions, not listener preference. Do not claim verified BPM, key, phoneme timing or chorus positions without appropriate actual evidence. If no supported inspection exists, prepare the useful plan or request targeted user observations.

## 2. Keep authorship and review ownership explicit

- Producer owns lyrics, song/music direction, audio triage, sound-cue planning and literal transcript/caption preparation from real sources.
- Copy Voice owns standalone marketing/editorial language and short VO wording; screenplay owns narrative scenes and dialogue. Preserve approved words and route requested wording changes to that owner.
- Sequence owns beat/shot order and timing plans. Video owns picture/motion review, speaker/mouth ownership, audiovisual alignment and caption placement over image. Sampled still frames cannot establish lip-sync.
- Delivery owns requested export specifications, actual file inventory and verified delivery status. A packet is not an export.

For a combined clip, report audio and video findings separately, then test the actual synchronization over the relevant interval. Do not turn separate audio and picture passes into an unperformed combined pass.

## 3. Plan only the necessary audio layers

| Layer | Useful decisions | Acceptance test |
|---|---|---|
| Dialogue / VO | Exact approved words, speaker, pronunciation, intention, pace/pauses, acoustic perspective; voice source/permission when material | Correct words/speaker, intelligible delivery and actual duration when measured |
| Music | Original/authorized source, emotional job, instruments, energy/arrangement, start/end or section intent, treatment under speech | Serves the scene and leaves required speech intelligible; no invented beat map |
| SFX / Foley | Visible cause or intentional editorial cue, source/action, perspective, onset and tail | Sound agrees with contact/event unless an authored offset is specified |
| Ambience / room tone | Location, continuity bed, perspective, entrances/exits | No unintended gaps, jumps or implausible acoustic changes |
| Transition / silence | Narrative role, boundary, fade/tail or intentional hard cut | Intended shift remains understandable and required tails survive |

Choose a lead layer for each moment. Ducking, EQ, dynamics, loudness or peak values are proposed processing intent or sourced targets until actually applied and measured. Do not invent numerical settings to imply engineering. Preserve source audio when locked; if a visual edit changes its causal event, flag the coupled decision instead of silently replacing the soundtrack.

For voice/performance, distinguish a desired delivery from a real recorded or generated voice. Do not promise a particular person's voice, consent, endorsement or phoneme match. For music edits, compare affected regions and their neighbors against the accepted master; a section command does not prove neighboring material stayed unchanged.

## 4. Cue sheet and synchronization

A cue sheet is optional for simple requests. For a timed or multishot handoff include only meaningful fields:

| Field | Contract |
|---|---|
| Cue ID / linked shot IDs | Stable identifiers for each sound event and the dependent picture units |
| Source / role / version | Actual available asset or clearly marked proposed/generated-later cue |
| In/out / offset | Supplied, measured, estimated or unknown; name the clock origin and unit |
| Trigger / relationship | Contact, line, beat, scene boundary, sound bridge, or intended counterpoint |
| Words / speaker | Exact locked script or transcript and correct ownership |
| Treatment / preserve set | Mix priority, fades/tails, allowed changes and protected original material |
| Readiness / acceptance | Missing inputs, capability status and observable retest |

Sequence seconds, source-media time and delivery frames are different clocks. State the conversion basis; never invent FPS/timebase. Do not convert an approximate beat estimate into frame-accurate placement. A target duration is distinct from measured audio length and verified final video runtime.

Track `required_sync`, `input_readiness`, `proposed_relaxation` and `accepted_relaxation` separately. Missing exact-sync capability or source media blocks that requirement's execution; it does not lower the requirement. Suggesting cutaways is an alternative for user acceptance, not proof that exact lip-sync works. A fixed-camera or sustained performance remains fixed through board and prompt stages when approved.

## 5. Transcripts and captions

First establish whether the source is a script, a user-supplied transcript or inspected speech. A script is intended wording, not proof of what was spoken. Preserve exact supplied text where locked; uncertain heard words use a clearly identified unresolved marker outside any claimed final transcript rather than invented speech.

Prepare speaker IDs, literal words, language, timing basis and relevant non-speech cues only when requested and evidenced. Transcription, translation, condensed social captions and exact subtitles are different artifacts; authorize the wording transformation through the actual request. Segmentation and line breaks should preserve locked meaning and words. Do not silently drop fillers, translate, abbreviate or repair names in a verbatim transcript.

For SRT, VTT or another requested format, use that format only when supported by the deliverable. Without timing evidence, return untimed text or an explicitly estimated timing plan, not synchronized final subtitles. Check ordering, end after start, intended overlaps, speaker mapping, language and text equality. Video owns legibility, safe-zone placement and interaction with faces/hands/copy; delivery verifies the actual sidecar or burned-in export and player compatibility when tested.

## 6. Handoff and bounded repair

Send the next owner source revision, exact words, cue/shot links, timing basis, carrier map, required sync, inspected scope, accepted locks, unresolved blockers, operation authorization and the one acceptance test. Mark dependent cue timings, captions, video prompts and exports `review_required` when upstream script, audio length, source take or shot timing changes. Unrelated accepted material stays protected.

Choose one primary cause and one controlled change. Distinguish observed symptom from cause hypothesis. If a second controlled attempt fails for the same reason, reconsider operation, source, timing or structure. Do not automatically rerun a paid service. Acceptance requires the actual revised result and the relevant audio/picture evidence; a clean packet alone only passes planning QA.
