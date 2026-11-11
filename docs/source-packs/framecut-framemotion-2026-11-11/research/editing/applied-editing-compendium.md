# FrameCut applied editing knowledge — research edition

**Date:** 2026-11-11 Europe/Warsaw; retrieval timestamps in `source-ledger.json` are UTC, beginning on November 10. **Status:** primary-source research and original exercise design, not implemented capability, native-editor certification, or demonstrated professional mastery. The 24-source ledger distinguishes page text, indexed excerpts, selected PDF pages and failed access. No film excerpts were watched or heard, no NLE was operated, and no exercise below was rendered. Numerical examples are calculations, not measured results.

This document separates three things: a source-backed technical or practitioner statement; an original proposed editing decision; and the evidence needed to judge that decision. The latter two are our synthesis, not quotations or claims that the named professional endorses FrameCut. A source count measures provenance coverage, not understanding. All proposed creative choices remain hypotheses until tested against footage and a viewer.

## Foundations and decision cards

### C01 — Start with the change in the viewer

**Source basis.** In her original interview, Tatiana Riegel describes retaining first reactions to dailies and evaluating performance within the assembled film. This is her practice, not a quantified universal formula. [Riegel interview](https://www.motionpictures.org/2018/02/tonyas-oscar-nominated-editor-tatiana-s-riegel-makes-scene-work/)

**Decision.** Before choosing a shot, write what the viewer knows before it and what should change afterward. A beautiful close-up that repeats known information may weaken a scene; an imperfect reaction may disclose its emotional turn. Record the intended change in one sentence, identify the exact performance evidence, then compare holding the shot against cutting away.

**Manual → agent.** In an NLE, build alternate short sequences from the same takes. In FrameCut, retain separate candidate sequences and source IDs; annotate the selected join with intent and the rejected alternative. Do not manufacture a virality score or apply Murch percentages as objective weights.

**Counterexample / review.** A safety demonstration may need an unbroken action even when a reaction is more emotive. Review the whole action and ask a new viewer to describe what happened, then whether the proposed emotional change occurred. Clarity and emotional intent are separate observations.

### C02 — Selects and paper edit preserve the evidence

**Source basis.** Nielsen describes spending time observing and selecting before editing to discover the material's rhythm. [Nielsen interview](https://www.motionpictures.org/2021/04/oscar-nominated-editor-mikkel-e-g-nielsen-on-giving-sound-of-metal-its-rhythm-2/)

**Decision.** Make a selects ledger with source interval, exact statement, surrounding context, visual evidence, uncertainty and exclusion reason. A paper edit is a hypothesis about meaning; it cannot establish usable sound boundaries, facial continuity or rights. Put negations, qualifications, names and numerical claims on a protected list before shortening.

**Manual → agent.** Mark ranges/subclips and an assembly in the NLE. FrameCut can ingest, analyze, import/transcribe and propose; preserve raw and approved transcript separately, then connect every chosen range to the source hash and PTS. Review low-confidence ASR against the media before it becomes copy or an edit decision.

**Counterexample / review.** Joining “works” from one answer to “in every case” from another can create a false claim even with perfect waveform joins. Compare the assembly transcript to source context and watch the speaker, not only the words. If speech cannot be heard, mark the paper edit provisional.

### C03 — Eye-trace, reaction and scene geography

**Source basis.** Adair explains intentional reaction selection and establishing the bar's geography in *Blue Moon*. Her choices serve that film's characters. [Adair interview](https://borisfx.com/blog/aotc/art-of-the-cut-blue-moon/)

**Decision.** For each adjacent pair, identify the current focus of attention, the next focus, the gaze direction and what motivates looking there. Do not reduce eye-trace to placing every face at the same coordinate. A controlled attention jump can reveal a threat; an accidental one can hide the main action. Establish spatial relationships when the audience needs them, then spend close-ups on changing information.

**Manual → agent.** Compare outgoing/incoming frames and play the join at speed. Store focus/eyeline notes on storyboard panels; FrameCut can adjust crops or choose a different source range, but cannot infer semantic continuity from a histogram or a structural board.

**Counterexample / review.** A perfectly matched hand position with a different emotional state can feel false. A deliberate axis crossing may be expressive if the scene reorients the audience. Review the join without sound, then with sound, and ask who is looking at whom; record confusion rather than asserting “cinematic.”

### C04 — Continuity, ellipsis and montage have different jobs

**Source basis.** The Academy's teaching guide distinguishes chronological continuity, graphic relationships and montage/time compression. [Academy guide, relevant PDF pages 5 and 9–10](https://www.oscars.org/sites/oscars/files/complet_film_editing_activities_guide.pdf)

**Decision.** Choose whether the sequence promises continuous action, omits time, or makes an argument through juxtaposition. A continuous repair demonstration must not silently omit the essential fastening step. A travel montage may compress hours, but should not imply that footage from two locations depicts one incident. If omission changes the claim, add context or retain the step.

**Manual → agent.** Build a continuity version and a clearly elliptical version. Use source labels and sequence notes to distinguish time/place; FrameCut's clips and gaps execute the order but do not establish the truth of the inferred relationship.

**Counterexample / review.** Alternating two unrelated reactions can imply causation or simultaneity. Review what a viewer infers from the juxtaposition and compare it with the provenance ledger. No cut-density threshold can settle this judgment.

### C05 — Source time and record time are different coordinate systems

**Source basis.** OTIO distinguishes media availability, a selected source span, visible range and the clip's range in its parent. [OTIO 0.18.1 time ranges](https://opentimelineio.readthedocs.io/en/v0.18.1/tutorials/time-ranges.html)

**Decision.** Name the clock beside every number. A source time is where material came from; record time is where it appears. A display timecode is a label, not automatically a PTS or a frame count. Keep master FPS as a rational, intervals half-open, and the inclusive last displayed frame separate from the exclusive out boundary.

**Manual → agent.** Mark source in/out and timeline in/out in the NLE; inspect source and program displays. FrameCut uses source PTS ticks and integer master frames. Its runtime README:45 specifies the conversion from stream-relative seconds using `start_pts` and `time_base`; never use nominal source FPS for VFR. See case W01 for a worked mapping.

**Counterexample / review.** Copying the number 100 from a 1/90000-second clock into a frame field produces a legal-looking but wrong edit. Inspect first/last selected source frames and decoded timestamps, then verify a visible or audible sync event at the mapped record position.

### C06 — Ripple changes downstream time, so inspect dependents

**Source basis.** Adobe documents ripple editing as closing a trim gap and shifting subsequent material. [Premiere Tools panel](https://helpx.adobe.com/premiere/desktop/get-started/tour-the-workspace/tools-panel-and-options-panel.html)

**Decision.** Use ripple when removing duration is intended. Before editing, identify captions, music hits, absolute overlays, connected events and locked end cards that straddle or follow the change. “Delete dead air” is not enough information to choose how those elements move.

**Manual → agent.** In an NLE inspect selected tracks and sync relationships. In FrameCut, dry-run typed `trim_clip` or `remove_clip` with `ripple`; use returned impact, keep stable IDs and resolve `edit_conflict`. A batch should fail atomically rather than partly shifting the film. Recheck the current base revision before saving.

**Counterexample / review.** Removing one second before a music hit while leaving an absolute overlay unchanged moves the meaning of the hit. Compare before/after event maps and the full span through the next protected event; listen to the new join. A shorter total duration alone does not prove success.

### C07 — Roll moves a decision without changing the overall slot

**Source basis.** Adobe defines a roll as changing the common cut while retaining the pair's combined duration. [Premiere rolling edit](https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/perform-rolling-edits.html)

**Decision.** Use a roll when the two shots and fixed sequence length are right but the moment of switching attention is wrong. Consider what the extra outgoing frames reveal and what the removed incoming frames conceal. A roll can preserve a music landmark while changing the reaction timing.

**Manual → agent.** Select both sides of the edit and compare the two frames in the NLE. FrameCut's craft mapping composes two trims in one transaction; adjust source/time fields consistently, respect handles and retain total length. This is not a claim of equivalence with every NLE's multi-track trim selection.

**Counterexample / review.** Delaying a reaction until after its key facial change misses the point even though continuity improves. Compare three candidates around the boundary at full speed and judge the reaction in context, then verify unchanged downstream anchors. Case W02 supplies arithmetic, not an automatic taste rule.

### C08 — Slip the action; slide the slot

**Source basis.** A slip changes the shown source range without moving the clip in the sequence. A slide moves the middle clip and compensates neighboring trims while retaining that clip's source span. [Premiere slip](https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/perform-slip-edits.html), [Premiere slide](https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/perform-slide-edits.html)

**Decision.** If a hand reaches the product too late inside a correctly placed shot, slip. If the entire shot should arrive later while its performance remains intact, slide. Verify both adjacent joins; improving the entrance can damage the exit.

**Manual → agent.** Review the NLE's multi-frame trim view. FrameCut uses replacement with a different `source_in` for a slip and a move plus neighbor trims for a slide. Work in one validated transaction, preserving independent narration unless its move is explicitly intended.

**Counterexample / review.** Slipping synced speech without its audio introduces lip-sync error. Sliding a middle clip with insufficient neighbor handles is infeasible. Review source bounds, two joins, captions and synchronization rather than treating equal duration as proof that nothing else changed.

### C09 — Handles and transitions require real material

**Source basis.** A transition can require media outside a clip's nominal source range; OTIO exposes a distinct visible range. [OTIO time ranges](https://opentimelineio.readthedocs.io/en/v0.18.1/tutorials/time-ranges.html)

**Decision.** First ask what a transition tells the viewer: elapsed time, changed location, a visual analogy, or a deliberate rupture. Then check whether the incoming/outgoing material exists and is suitable. Unused frames containing a slate, blink or camera settle are available technically but may be unusable editorially.

**Manual → agent.** Scrub handles in the source viewer. FrameCut validates overlaps and `insufficient_handles`; do not repair that error by silently repeating frames. Choose a supported style and inspect its actual encoded midpoint. Native storyboard dips are only an approximation of the rendered curve.

**Counterexample / review.** A dissolve may confuse two product states that must be compared exactly; a hard cut can explain them better. Conversely a gentle time passage need not be forced into a hard-cut style. Review meaning, ghosted text/faces, source bounds and audio overlap. Brand transition prohibitions belong to that brand's profile, not universal editorial doctrine.

### C10 — J/L cuts move the audience's attention through sound

**Source basis.** Apple describes separate sound/picture edges with audio still linked; the Resolve editor lesson demonstrates reaction-driven split edits. [FCP split edits](https://support.apple.com/en-my/guide/final-cut-pro/ver1632d82c/mac), [Resolve Editor, printed 185–187](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Editors-Guide.pdf)

**Decision.** Keep the outgoing speaker audible while showing the listener when understanding the response matters. Lead the incoming voice when its sound plausibly motivates a change of attention. Choose the offset from performance and comprehension, not a mandatory number of frames.

**Manual → agent.** Expand/select audio and picture independently, preserving sync. FrameCut mutes the linked base audio and places independent dialogue with an explicit offset; caption sources must reference the dialogue event. Avoid doubling the original voice.

**Counterexample / review.** Introducing an offscreen answer before the question's critical qualifier can imply interruption or a different meaning. Listen across the full exchange and inspect lips where visible. Confirm both voices' source identities, the overlap's intention and correct caption timing.

### C11 — Breaths are part of performance

**Source basis.** The Resolve Editor pacing lesson treats space between soundbites as useful for natural delivery and comprehension. [Editor Guide, printed 46–48](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Editors-Guide.pdf)

**Decision.** Label a pause: breath, thought, hesitation, tension, interruption or expendable waiting. The same measured silence can serve different functions. Keep a preparatory breath when it supports the next thought; attenuate an obtrusive one if shortening it would make the speaker sound unnatural. Preserve the end of consonants and room decay.

**Manual → agent.** Loop the phrase with context and compare uncut/shortened/attenuated versions. `plan-cuts` proposes silence removals with pads and skips certain dependents; it cannot decide meaning. Edit its proposal before applying; record why retained pauses matter.

**Counterexample / review.** Removing hesitation from uncertain testimony may falsely increase confidence. A relentlessly breathless sales read can reduce intelligibility despite fitting the duration. Listening is mandatory for this judgment; waveform inspection and caption counts are supporting evidence, not substitutes.

### C12 — Dialogue continuity includes the space around words

**Source basis.** Fairlight's dialogue chapter addresses clear words and smooth ambience; its layered editing exercises use listening to adjust joins. [Fairlight Guide, printed 82 and 148–151](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fairlight-Audio-Post.pdf)

**Decision.** Diagnose the audible discontinuity before processing: a clipped syllable, abrupt room change, rustle, level mismatch, or a duplicate microphone. Match room tone to the location and perspective. A blanket rule to always add a bed or never use one is too rigid; reason about the ambience already present, edits, overlaps and intended soundscape.

**Manual → agent.** Keep dialogue and production effects identifiable; audition channels/takes separately. FrameCut can position independent sound, fades, gains and basic filters. It does not provide full dialogue restoration or a Fairlight-style mix architecture; a prepared derived asset needs source linkage and measured latency compensation.

**Counterexample / review.** Heavy denoise may remove a rustle while turning speech watery. A tone loop may expose a recurring click. Listen solo for damage, then in the scene for continuity; preserve the untreated source and explain any remaining compromise.

### C13 — Music has phrases, not just a grid

**Source basis.** Fairlight provides a musical grid and phrase crossfades; Nielsen discusses sound as narrative perspective. [Fairlight Guide, printed 208–209](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fairlight-Audio-Post.pdf), [Nielsen interview](https://www.motionpictures.org/2021/04/oscar-nominated-editor-mikkel-e-g-nielsen-on-giving-sound-of-metal-its-rhythm-2/)

**Decision.** Hear the phrase's departure, development and arrival. Put a major reveal where the musical thought supports it, or deliberately against it. A beat marker does not say which beat is the downbeat, whether a pickup precedes the phrase, or whether a fill should complete before a cut.

**Manual → agent.** Mark phrase boundaries by listening. FrameCut `beats` estimates a pulse and confidence; check half/double tempo and add human-verified phrase markers. Independent music keeps its clock when picture is retimed. Compare music edits for repeated attacks, harmonic discontinuity and truncated reverb tails.

**Counterexample / review.** Cutting every half second at 120 BPM can obscure a lyric or make a calm interview feel frantic. In assumed 4/4 with quarter note=120 BPM, a bar is 2 seconds, not 0.5. This arithmetic is not evidence the actual track has that meter or tempo.

### C14 — Multicam begins with synchronization, not angle switching

**Source basis.** Blackmagic's official training separates multicam synchronization and angle editing. [Training hub](https://www.blackmagicdesign.com/products/davinciresolve/training)

**Decision.** Establish each camera and recorder's time basis, matching event, audio-channel identity and drift behavior before making angle decisions. A beginning clap alignment does not prove a long take stays synchronized. Prefer a continuous sound source when changing picture angles; an audible perspective change may be intentional, but should not occur by accident.

**Manual → agent.** A native NLE operator creates and verifies the multicam source, then edits angles with deliberate audio selection. FrameCut currently has no multicamera sync engine. It can ingest a verified conform or separately mapped assets, with offsets/provenance recorded, but must not label this as automatic multicam support.

**Counterexample / review.** Waveform matching may align a repeated musical phrase incorrectly; camera scratch sound may be delayed. Check identifiable events near start, middle and end; document unresolved drift. Then review performance choice and eyelines independently of technical sync.

### C15 — Proxy and relink workflows protect identity

**Source basis.** Adobe provides explicit proxy attachment to full-resolution media. FCP roles and subroles organize audio identity and can use iXML metadata. [Premiere proxies](https://helpx.adobe.com/premiere/desktop/organize-media/ingest-proxy-workflow/attach-proxies-to-full-resolution-media.html), [FCP audio roles](https://support.apple.com/en-lamr/guide/final-cut-pro/verb21791812/mac)

**Decision.** Treat a proxy as a derivative of a specific original, not merely another file with the same name. Preserve source IDs, clocks, channels and the transform used to create it. Camera1/clip001 and Camera2/clip001 are different identities. Organize voice, music and effects by intent; metadata assignment can be wrong.

**Manual → agent.** Attach/relink using a verified identity map and compare proxy/original views. FrameCut retains hashes and relative paths; a future proxy adapter must not replace the original's identity or assume that its timestamps match. Validate the intended audio channel and orientation as well as picture.

**Counterexample / review.** A visually similar take with the same filename can pass a casual thumbnail check. Review source frame identity at several edit points, audio-channel content and exported full-resolution detail. Never deliver a low-resolution derivative merely because the relink dialog says online.

### C16 — VFR and mixed rates need an explicit conform

**Source basis.** FrameCut's current contract uses source PTS and master rational FPS and conforms decoded picture to CFR; HDR is rejected. This is a local implementation claim, not an assertion about every NLE. See frozen runtime README:41–55.

**Decision.** A phone or screen capture's average FPS is insufficient for frame indexing. Decide which master rate the deliverable requires, inspect decoded timestamps, and preserve the source-to-master mapping. Drop-frame timecode changes numbering conventions; it is not a command to discard source frames.

**Manual → agent.** An NLE operator checks source interpretation and sequence settings, then tests the conform with identifiable actions. FrameCut's mapping must be validated against timestamps and the rendered frame sequence, not reconstructed from a rounded decimal frame rate. Record deliberate frame duplication/omission during conform.

**Counterexample / review.** A two-second spot-check can miss end-of-program drift. Inspect distant sync events and source interval endpoints. If timing cannot be established, return a bounded conform requirement rather than changing speed until the last frame approximately matches.

### C17 — Retiming changes both motion and meaning

**Source basis.** FrameCut implements constant/variable speed and freezes, but no optical flow; its variable-speed source audio changes pitch. See owner SKILL:92 and `fc_time.py`/`fc_audio.py`.

**Decision.** Identify what must remain real-time: a spoken claim, demonstration duration, impact, or musical performance. Slow motion can reveal an action; it can also misrepresent a product's operation. Choose speed for the intended effect and state when footage no longer represents elapsed real time.

**Manual → agent.** In the NLE inspect the retime curve, source range and interpolation mode. FrameCut adjusts `speed`, `speed_curve` or `freeze_frame`, then remaps dependents. Keep independent narration untouched where required. An optical-flow result from another tool is a new derived asset, not a hidden upgrade to native FrameCut.

**Counterexample / review.** Holding a speaking face freezes lips while speech continues. Dropped/repeated frames can make a smooth camera pan judder. Inspect difficult motion at delivery speed and frame-by-frame, then listen for pitch/timing damage. Case W04 separates calculated duration from perceived quality.

### C18 — Color is a signal path plus a viewing judgment

**Source basis.** Adobe requires correct source-space identification and interpreting a LUT's output. Resolve's Colorist Guide explicitly says its grading diagram is not a universal operation order. [Premiere clip color](https://helpx.adobe.com/premiere/desktop/correct-color/set-up-color-management/color-management-using-clip-modify.html), [Colorist Guide, printed 8–10 and 46–47](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Colorist-Guide.pdf)

**Decision.** Record input encoding, working space, transforms, look and output space before making an image “more cinematic.” Match the scene's continuity and intended lighting, not every shot's mean brightness. Select a useful reference and identify exceptions; a close-up and wide do not contain the same luminance distribution.

**Manual → agent.** In a color-capable NLE compare reference stills, scopes and adjacent playback. FrameCut's brightness/contrast/saturation primitives are not log conversion, scopes or managed grading. Ask for a verified SDR conform or use a specialist grade, preserving the transform record.

**Counterexample / review.** Double-applying a log transform can clip highlights; forcing a warm practical light to neutral can remove the scene's intention. Validate the exported image in the declared viewing chain. Do not turn the historical “creative LUT=Rec.709, 50–70%” heuristic into a universal rule.

### C19 — Mix for intelligibility and intent, then meter the delivery

**Source basis.** EBU R128's programme target is −23 LUFS; it is not a universal social-media target. [EBU R128](https://tech.ebu.ch/publications/r128)

**Decision.** Establish the foreground and background for each beat. Dialogue need not dominate an intentional silent reaction or music performance; when the words carry the message, test whether they remain understandable on the expected device. Fixed music-to-voice gain differences cannot guarantee this across different spectra and arrangements.

**Manual → agent.** Identify channels, isolate problems, set clip balance, then automate appropriate buses. In FrameCut, separate dialogue/music/SFX events, choose gains/ducking deliberately, and request loudness normalization only against a named spec. Its three buses and basic filters do not imply a full finishing mixer. Inspect the actual encoded audio, including channel assignment and mono playback.

**Counterexample / review.** A mix can pass integrated loudness while one crucial word is masked or mono summing removes an element. Listen to difficult phrases, joins, quiet passages and the complete ending; measure integrated loudness/true peak against the correct spec. Record listening equipment and scope. Never mark `audio_heard=true` from a meter.

### C20 — Caption readability depends on the actual audience and profile

**Source basis.** Netflix's Polish guide distinguishes standard subtitle and SDH requirements; adult standard subtitles allow up to 17 cps, while its SDH section allows 20. These are that delivery's rules. [Polish Timed Text Style Guide, sections 16 and 22](https://partnerhelp.netflixstudios.com/hc/en-us/articles/216787928-Polish-Timed-Text-Style-Guide)

**Decision.** Declare whether the track is verbatim accessibility captioning, translated subtitles, SDH or designed emphasis. Preserve numbers, negation and names. A fast word highlight does not automatically make a dense sentence readable. Choose segmentation from syntax and meaning before visual flourish.

**Manual → agent.** Review sidecars in the target player and the actual composited video. FrameCut projects captions from checked source timing; translations require new phrase/word timing. Check glyphs, entities, punctuation, overlap and occlusion in each aspect ratio. The audit's negative-time and WebVTT exact-copy defects must remain visible in the extraction plan.

**Counterexample / review.** A mathematically compliant caption over a face or critical UI can still fail. A familiar sentence may feel readable only because the editor knows it. Have a fresh reader use the intended viewing size, with audio muted for accessibility assessment where appropriate; retain separate sync and reading observations.

### C21 — Interchange is a negotiated loss budget

**Source basis.** Adobe documents AAF exporter caveats; Apple describes FCPXML as its own transfer format. Neither establishes that FrameCut's current exports survive in those editors. [Premiere AAF](https://helpx.adobe.com/premiere/desktop/render-and-export/export-files/export-aaf-files.html), [FCPXML transfer](https://support.apple.com/en-hk/guide/final-cut-pro/verdbd66ae/mac)

**Decision.** Before exporting, agree which elements must remain editable and which may be baked: cuts, audio channels, retimes, transitions, titles, effects, grading and markers. “XML” alone is not a compatibility contract; FCPXML and legacy FCP7 XML cannot be treated as synonyms.

**Manual → agent.** Supply originals/relink map, edit list, reference movie, captions, sound stems as requested and a loss report. FrameCut has cuts-oriented EDL and optional OTIO, not native FCPXML/AAF authoring. The receiving NLE operator imports in a named version and checks every boundary plus sound/color against the reference.

**Counterexample / review.** A parser roundtrip may retain clip names while an editor loses speed effects or links the wrong take. Compare source/time mapping and output playback; mark each unsupported feature omitted, baked, manually rebuilt or blocked. The historical Avid 2021 excerpt is insufficient to attest current Media Composer interchange.

### C22 — Finish by reviewing the exported film, not the promise

**Source basis.** Resolve's conform lesson uses a reference movie for checking migrated edits. The ASC article describes Murch's real-time approach, but the embedded interview was not watched here. [Colorist Guide, printed 151–153](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Colorist-Guide.pdf), [ASC article](https://theasc.com/post/the-film-book/walter-murch-2-real-time-cuts-image-editing/)

**Decision.** Split review questions: story and meaning; picture continuity; sound; caption/copy; technical delivery. A single pass trying to inspect everything encourages missed details. Sampled frames establish only sampled visual observations. A full audio listen is a different act from a thumbnail review.

**Manual → agent.** Play the encoded deliverable, compare to the accepted board and reference, inspect first/last frames and every known risk interval. FrameCut records reviewer, scope, observations, outcome and picture/audio flags; these are assertions requiring genuine observations. Keep partial work REVIEW_REQUIRED.

**Counterexample / review.** A valid H.264 file can have a wrong final name card or a truncated word. A smooth preview can differ from the final render. Record revision/hash, player/device, intervals inspected, observed issue and next action. Technical PASS never substitutes for creative acceptance.

## Worked original cases — calculated designs, NOT_RUN

These cases are newly authored teaching scenarios. They use no third-party footage and confer no rights to film excerpts cited above. Future runs need real licensed media, before/after renders and an independent reviewer.

### W01 — A source clock that does not start at zero

Assume a source stream has `time_base=1/90000`, `start_pts=900000`; the chosen action starts 2.4 seconds after its stream start. Its source in is `900000 + 2.4×90000 = 1116000` PTS ticks. Put it at master frame 250 in a 25/1 sequence: record start is 10 seconds. A 50-frame clip at speed 1 consumes 2 seconds, or 180000 source ticks; the source interval is `[1116000,1296000)`, record interval `[250,300)`. The last displayed record frame is 299, not 300.

If an independently verified source transient occurs at PTS1170000, it is 0.6 seconds after this source in and should occur 15 master frames after placement, at frame265. This assumes constant speed and exact stated clocks; VFR still requires decoded PTS selection.

**Bad alternative:** treat source-in2.4 as master frame60 or set `source_in=60`. **Review artifact:** mapping ledger, decoded boundary frames, waveform/transient position, and a playback observation. **Pass condition:** mapping agrees with the known event within the declared quantization policy; the reviewer confirms the action is not clipped. No measurement was performed here.

### W02 — Preserve a fixed end card while improving the reaction

Assume 25fps, A occupies `[0,100)`, B `[100,200)`, and the protected card begins at200. The important reaction starts four frames before B's chosen in; however the current cut also leaves A's last line visually unfinished. Compare two independent proposals, not one ambiguous “make it smoother.”

**Roll proposal:** delay the picture cut to110. A becomes110frames; B starts110 with90frames, and its source-in advances10frames at unity speed. The card stays at200. This provides more A but risks losing B's reaction.

**Slip proposal:** retain B's `[100,200)` slot but select a source range4frames earlier, assuming sufficient handles. This preserves the reaction and downstream timing but changes B's end frame. If both decisions are necessary, compose them only after evaluating each effect and source availability.

**Bad alternative:** ripple10frames from B while forgetting to move/reapprove the end card, or slip only the picture of synced dialogue. **Review artifact:** side-by-side edit ledger and three short candidate playbacks. **Evaluation:** editor identifies which version expresses the listener's change without clipping speech; technical reviewer confirms all fields and anchors. Duration preservation alone earns no creative pass.

### W03 — Interview hesitation and a truthful J-cut

An interviewee says, “It usually works… if the room is quiet.” The requested cutdown is shorter. Candidate A removes the pause and condition; B removes part of the waiting but retains the condition and a natural breath; C keeps the full hesitation and covers it with evidence of the room. Choose B only if source listening confirms it preserves the speaker's uncertainty; choose C if the hesitation is the story.

A B-roll shot may begin during the retained line while the independent dialogue continues. The incoming question may lead the return to the interviewer, provided it does not falsely interrupt the condition. Keep the base clip muted if the same voice is already on an independent event; caption the authoritative voice event, not an unrelated visible clip.

**Bad alternative:** cut silence by threshold, place a cheerful music hit over the qualifier, and call the result clearer because it is shorter. **Review artifact:** source/context transcript, protected wording, raw/edited audio, waveform boundaries, and picture+sound variants. **Evaluation:** fresh listener repeats the complete claim and its condition; editor listens for breath/consonant damage and room change. No ASR confidence or LUFS value establishes truthfulness.

### W04 — A 15-second product film with music and slow motion

Assume a commissioned track is verified by listening to have 4/4 meter at quarter note=120BPM. One beat lasts0.5s and one bar2s. A 15s film cannot be described as a whole eight-bar phrase at that rate: eight bars take16s. Options are a musically coherent shorter phrase plus intentional opening/ending space, an authorized different edit, or a revised duration. Do not automatically speed the song to fit.

A real 4-second demonstration retimed uniformly to2× consumes2seconds of record time. A separate voiceover stays unchanged. A speed ramp needs the integrated source-time mapping; its average endpoint speeds alone do not give a reliable duration. A freeze must be clearly designed and cannot stand in for missing captured action.

**Bad alternative:** slice the music at15s mid-syllable or claim the accelerated demonstration occurs in real time. **Review artifact:** phrase markers verified by a listener, source/record map, full music tail and audio-only comparison. **Evaluation:** ending feels complete, product claim remains accurate, no repeated attack or varispeed damage. Tempo detection and frame arithmetic are supporting checks.

### W05 — Match two cameras without erasing the lighting

The owner supplies a warm room wide shot and a close-up encoded with a different camera transform. First identify each source encoding and the delivery space; make a reversible test conform. The close-up's face occupies much more of the image than the wide, so matching whole-frame average luminance is not a valid target. Choose shared subjects and contextual cues, compare contrast/color continuity at the cut, then decide whether a deliberate look improves the scene.

The FrameCut-only route requires supplied verified SDR material or a separate graded return. Record the conform transform and source hashes; do not simulate a log transform with a contrast slider. Review a short sequence containing both angles and the return, not just a pleasing still.

**Bad alternative:** apply a Rec.709 creative LUT to unknown log and again through automatic input conversion, then force every warm wall to gray. **Review artifact:** source tags, signal-flow note, neutral test chart if actually captured, reference stills/scopes and exported comparison. **Evaluation:** reviewer judges consistent scene lighting and preserved highlights/skin detail on a declared display. Numerical equality of histograms is not the goal.

### W06 — A conform that opens successfully but is still wrong

A 25fps master contains plain cuts, independent narration, a variable-speed product shot, a title and a dissolve. In the current frozen FrameCut implementation, any transition, retime or freeze marks the sequence complex: `write_export` withholds both `picture.edl` and `picture.otio` for the whole sequence. It still writes the native project JSON, relink map, shots CSV and loss report. Preserve that authoritative project and provide a reference movie. If the recipient requires a cuts transfer, first agree on a separate simplified or baked derivative; do not imply the existing exporter automatically extracts a supported subset. For the retimed shot, agree whether the receiver needs editability or may use an approved replacement with additional handles. That derivative still needs its own validation and native import comparison; the current export does not faithfully transfer all five element types.

The native-editor operator checks source identity, source/record boundaries, clip order and gaps, then compares picture and audio to the reference. Avid/Resolve/Premiere/FCP each need their own named-version test and supported import route; FCPXML or AAF requires an additional implemented converter/workflow, not renaming the OTIO file.

**Bad alternative:** a successful file import plus matching total duration is declared complete while narration disappears and the retime becomes ordinary playback. **Review artifact:** element preservation matrix, import log, screenshots of unresolved elements and full rendered comparison. **Evaluation:** every element has a documented outcome and every claimed preserved feature is independently inspected. Optional untested features remain NOT_RUN.

## Curriculum, authentic media and evaluation ownership

A practical learning unit must contain: a licensed media manifest; brief/intended viewer change; source selections; proposed edit with rationale; one viable alternative; one intentionally wrong counterexample; before/after project and export; source/record mapping; measured integrity checks; and perceptual review with intervals. **No unit is complete from this document alone.**

| Stage | Practical exercise | Owner of assessment | Evidence required |
|---|---|---|---|
| 1 | Organize footage, source clocks, rights and reversible selects | Assistant editor / technical reviewer | identity map, relink check, exact source ranges |
| 2 | Paper edit preserving context and a protected qualifier | Editorial reviewer plus content owner | source/context comparison and fresh-viewer explanation |
| 3 | Dialogue scene with alternative reactions and eye-trace | Experienced narrative editor | alternate cuts, rationale, continuous playback observations |
| 4 | Four trims and split edits under locked milestones | Editor plus technical reviewer | both joins, source bounds, dependent map and sync observations |
| 5 | Breath, room-tone and music-phrase edit | Dialogue/music editor or qualified listener | solo and contextual listening, naturalness/intelligibility notes |
| 6 | Multicam and proxy/conform identity | Native NLE operator | start/middle/end sync, original/proxy comparison, wrong-take control |
| 7 | Mixed-rate/retime and managed-color return | Conform operator / colorist | declared transforms, mapping and encoded-output review |
| 8 | Caption/accessibility and finishing mix | Language/caption reviewer and mixer | real-player glyph/readability/sync review, mono/listening and metering |
| 9 | Cross-editor turnover | Operator in each named NLE | native project opens, loss matrix, full reference comparison |
| 10 | Unseen complete brief | Independent editor, user as creative owner | original rationale, completed film review, revisions and acceptance |

Use owner-shot material with explicit participant/reuse consent, or a verified training license. Official training media availability does not authorize repackaging it with a public plugin. Store rights, source URL/acquisition date, original checksums, consent/release limits and allowed derivative distribution. Use varied material: overlapping dialogue, quiet testimony, practical instruction, performance music, screen capture, mismatched cameras and a multi-language caption track. Synthetic geometry and tones are useful technical controls but cannot prove performance selection, believable dialogue or taste. Film scenes mentioned in interviews are references to discuss, not assets licensed for these exercises.

A rubric should keep independent columns rather than hide failures in an average:

- **Meaning:** all protected facts survive; unintended implication is a blocker.
- **Editorial intention:** reviewer can identify the chosen attention/story change; a defensible alternative is acknowledged.
- **Picture continuity:** relevant action, geography, eye-trace and source fidelity are reviewed at speed, with intentional violations explained.
- **Sound perception:** intelligibility, joins, room continuity, music phrasing, mono behavior and ending are actually heard. Unheard stays NOT_REVIEWED.
- **Caption/accessibility:** language, exact copy, timing, reading and occlusion are inspected in the actual output/profile.
- **Technical integrity:** dimensions/rate/frames/source hashes/audio channels/loudness meet the declared contract; no stale or preview output is promoted.
- **Interchange:** each preserved element is checked in the actual receiving application. Parser-only checks are a different column.

For subjective columns use **unsupported / plausible / demonstrated in this case / demonstrated on an unseen case**, with evidence and reviewer identity. This is a proposed assessment scheme, not a scientifically validated score or certification. A technical pass cannot compensate for a meaning error or missing listening. The human owner accepts the creative result. The research author cannot independently validate its own editorial taste by writing more rules.

## Corrections, limits and next research

The old knowledge corpus contains valuable practices but also overgeneralizations. Do not turn fixed shot lengths, an obligatory first-frame hook, fixed ducking ratios, a blanket prohibition on continuous ambience, or one LUT node order into universal laws. Preserve each as a contextual hypothesis with a counterexample. The old combined 161-source total does not establish coverage of all editing craft or all editors.

Resolve has substantive selected-page research here; Premiere has targeted official behavior pages; FCP has targeted official pages/indexed content, with some direct requests returning429. Avid remains the thinnest coverage: one historical2021 indexed excerpt, a web-size rejection and a direct403. Its current bins/locking, ScriptSync/PhraseFind, source/record workflow, assistant practice, multicam and AAF/consolidation need further primary reading and an operator's native exercise. No installed versions or commercial entitlements are attested. This edition also does not certify HDR, surround/immersive delivery, broadcast compliance, documentary ethics review or accessibility conformance.

Further research should answer concrete exercise failures rather than expand a bibliography indiscriminately. For every new claim record exact source/version/date, fact versus practitioner preference versus inference, contradiction, applicability and how to falsify it in an artifact. Retain source knowledge privately where appropriate, write original applied guidance, and keep practical validation visibly open.
