# Editor craft: think like a professional editor

FrameCut makes editorial decisions the way an experienced editor working in DaVinci Resolve or Premiere Pro makes them, and then expresses them as FrameCut operations. Read this before planning the storyboard of any edit, when a user names an editing term, and before the final review. It is Studio's own summary of editing practice (Murch, Dmytryk, Reisz and Millar, the Resolve and Premiere manuals, broadcast and platform specifications; sources at the end), written for this engine. Numbers marked *rule of thumb* are practitioner starting points to tune by eye and ear, not standards.

The user directs; FrameCut proposes like a good editor in the room: a clear recommendation, the reason in the viewer's terms, and the trade-off.

## Contents

- [How an editor decides](#how-an-editor-decides)
- [Working stages](#working-stages)
- [Terms and their FrameCut form](#terms-and-their-framecut-form)
- [Cutting dialogue and talking heads](#cutting-dialogue-and-talking-heads)
- [Pacing and short-form retention](#pacing-and-short-form-retention)
- [Cutting to music](#cutting-to-music)
- [Transitions](#transitions)
- [Sound for editors](#sound-for-editors)
- [Colour for editors](#colour-for-editors)
- [Delivery and QC](#delivery-and-qc)
- [Beginner habits and pro habits](#beginner-habits-and-pro-habits)
- [What FrameCut cannot do here](#what-framecut-cannot-do-here)
- [Sources](#sources)

## How an editor decides

**Murch's order of priorities for a cut:** emotion (about half of the value), then story, rhythm, eye-trace, the two-dimensional screen plane and finally three-dimensional space. When a cut cannot satisfy all six, give up the lowest first: a viewer forgives a crossed line or a jump in position when the feeling and the story are right, and never forgives the reverse. Use the six as the review questions for every join on the storyboard: does it carry the feeling, does it move the story, does it land in the rhythm, does the eye find the subject where it was already looking, are screen directions consistent, is the space coherent.

**Every cut needs a reason** (Dmytryk): new information, a reaction that matters more than the speaker, the action leaving frame, a beat in the music, compressing time, hiding a flaw. Without a reason, stay on the shot. Prefer cutting in movement, so the motion carries the eye across the join. Staying on a strong shot beats cutting for variety.

**Reasons not to cut:** the performance is still building, the shot is still giving information, or a cut would step on an emotional beat. After a punchline or a reveal, hold a beat before cutting away: too early kills the laugh, too late kills momentum.

**Eye-trace:** if the subject sits on the right third of shot A, put what matters in shot B near the same place. In 9:16, keep faces in the upper-middle band, clear of the platform's interface.

**Continuity or expression, chosen once.** Invisible editing (matched action, eyelines, screen direction, the 180° and roughly 30° rules) suits drama, interviews and corporate work. Expressive editing (jump cuts, smash cuts, match cuts, speed ramps, montage) suits vlogs, ads, music videos and social. Keep the choice consistent: two jump cuts in a smooth piece look like mistakes, a whole jump-cut vlog reads as style.

**Structure for any length:** hook, setup, escalation, payoff, resolution or call to action. For an ad: problem, product, proof, offer, call to action. Whatever the hook promises must pay off, or social viewers leave when the promise drifts.

## Working stages

A pro moves through these stages and does not polish before the structure works. FrameCut follows the same order inside its storyboard gate.

| Editor's stage | What happens | In FrameCut |
| --- | --- | --- |
| Ingest, organise | Checksummed copies, named bins, metadata, proxies | `ingest` (hash, probe, rights, provenance); asset IDs are the bins |
| Selects | Best moments pulled out; for interviews a transcript and a paper edit | `analyze` (scenes, silences, thumbnails), `transcribe` / `import-transcript`, `propose` candidates for review |
| Assembly | Everything in story order, long | first `add_sequence` |
| Rough cut | Structure and story working, temp music | storyboard revision shown to the user |
| Fine cut | Timing to the frame, performance choices, music final | `apply` revisions: trims, splits, `plan-cuts`, keyframes, beats |
| Picture lock | No more timing changes | storyboard acceptance recorded in the project brief |
| Sound | Dialogue edit, room tone, music edit, SFX, mix to spec | buses, ducking, effects; Earshot through Toolbox for checks and SFX |
| Colour | Correct, match, then one look | picture effects (see [colour](#colour-for-editors)) |
| Titles, captions | Final supers spelled and timed | texts, captions, Caption Studio QA |
| QC, delivery | The exported file checked, platform versions | `render --mode final`, `verify`, `review`, per-deliverable framing |

Version every round and keep one consolidated notes round per stage; FrameCut's revisions and `undo` are that history.

## Terms and their FrameCut form

When the user uses an editor's word, answer in that word and do the matching operation. A term with no FrameCut form is in [what FrameCut cannot do here](#what-framecut-cannot-do-here).

| Term | Meaning | FrameCut form |
| --- | --- | --- |
| Timeline / sequence | One arrangement of clips in time | `sequences[]`, integer frames at rational FPS |
| Source in/out, three-point edit | Three of four marks set, the fourth follows | clip `source_in`, `start`, `duration` |
| Four-point edit, fit to fill | All four marks set; the source range is retimed to fill the gap | a constant `speed` equal to the source length divided by the gap length |
| Drop-frame timecode | At 29.97 fps the frame numbers 00 and 01 are skipped every minute except every tenth, so timecode keeps clock time | frames stay exact at `30000/1001`; mark 29.97 timecode as DF (`;`) when reporting it |
| Insert / overwrite | Push later material on, or cover what is there | `move_clip` on each later clip, then the new clip through `set_sequence`; `replace_clip` |
| Lift / extract (ripple delete) | Remove leaving a gap / closing it | `remove_clip` with `ripple: false|true` |
| Blade / razor | Split at the playhead | `split_clip` |
| Ripple trim | Shorten one side and shift everything after | `trim_clip` with `ripple: true` |
| Roll, slip, slide | Move an edit point; change the shown part of the source; move a clip between neighbours | two `trim_clip` operations in one transaction; `replace_clip` with a new `source_in`; `move_clip` plus neighbour trims |
| Handles | Spare source frames beyond the used part | validation refuses transitions without them (`insufficient_handles`) |
| J-cut / L-cut (split edit) | Incoming sound before its picture / outgoing sound under the next picture | mute the base clip's sound and lay the dialogue as an independent `audio` event anchored with an offset |
| Jump cut | Same subject, small change: a visible skip | a split with material removed |
| Punch-in | Digital push to a tighter size | `keyframes` `zoom` 1.1 to 1.3 with `pan_x`/`pan_y`, held (`easing: hold`) on the clip after the cut |
| Cutaway, insert, B-roll | Covering or proving shots over the main audio | a clip over the gap with the voice as an independent audio event, or an `overlays` event |
| Speed ramp | Speed changing over time | `speed_curve` (1/4 to 4) |
| Freeze frame / frame hold | One frame held | `freeze_frame` |
| Fit to fill | Speed a clip to fill a gap | constant `speed` from source length / gap length |
| Adjustment layer | Effects over everything beneath for a time range | not available; apply `effects` per clip |
| Compound / nested clip | Several clips as one | render the part as its own deliverable and ingest it as a clip |
| Dissolve, dip, wipe, slide | Picture transitions | `transition` frames plus `transition_style` |
| Room tone | The recorded "silence" of a place | an independent audio event on the `dialogue` bus under gaps |
| Ducking | Music lowered under speech | `duck_db` on the `music` bus |
| Stems (D, M, E) | Dialogue, music, effects submixes | buses `dialogue`, `music`, `sfx` |
| LUFS, true peak | Loudness and inter-sample peak | deliverable `lufs`; `verify` measures integrated loudness and true peak |
| Safe zones | Areas clear of platform interface | deliverable `safe_top`, `safe_bottom`; captions and supers stay inside |
| Reframe | Re-crop for another aspect ratio | one sequence, several deliverables, `framing` per deliverable |
| EDL / XML / OTIO | Interchange of the edit | `export` (CSV, EDL for plain cuts, `--otio`) |
| Picture lock | Timing frozen | storyboard acceptance; afterwards only sound, colour and text change |

## Cutting dialogue and talking heads

1. **Select by content first.** Build the paper edit from the transcript; fix delivery afterwards. Never change what a speaker means by joining parts of different sentences: negations, numbers and qualifiers must survive.
2. **Silence removal with pads.** Run `plan-cuts` on the `analyze` silences. Its defaults keep 6 frames after the last sound and 3 frames before the next word; a documentary wants looser pads (8 to 12 after), a fast TikTok style tighter ones (*rule of thumb*). Silences shorter than 6 frames stay: they are breathing, not dead air.
3. **Breaths and fillers.** Remove gasps, doubled breaths and fillers that break the meaning; keep a short breath before a new thought in a calm piece, since a film with every breath removed sounds machine-cut. A breath that is merely loud can be lowered 6 to 12 dB instead of cut (*rule of thumb*). Level-based silence detection treats a breath as silence, so listen to the joins.
4. **Cover the cut.** At each jump, choose one: B-roll or a cutaway over the join, a punch-in (alternate between 100% and about 115 to 125%, centred on the eyes, *rule of thumb*), or an honest jump cut in a style that uses them. Check the source resolution: a 1080p source cannot punch in far without softening a 1080p output.
5. **Audio at the join.** FrameCut fades a few milliseconds at every hard cut automatically. Where the background noise jumps, fill the gaps between dialogue clips with room tone; never run one continuous bed under the dialogue, since it doubles the noise already recorded under the voice.
6. **Split edits.** For a conversation or an interview over B-roll, lead the next voice in a few frames before its picture (J) or let the line run over the reaction (L); this makes edited speech feel continuous.

## Pacing and short-form retention

Rhythm is variation, not speed: alternate short and long shots and give a held shot after a fast run. Shorten shots, tighten framing and lift sound toward a climax, then release.

| Format | Typical shot or visual change (*rule of thumb*) |
| --- | --- |
| Feature drama | 3 to 8 s, longer for performance |
| Trailer, action | 0.5 to 2 s |
| Documentary interview | 5 to 15 s on the speaker, B-roll 2 to 5 s per shot |
| Corporate, explainer | 3 to 6 s |
| TV spot (15/30 s) | 1 to 3 s |
| Music video | on beats and bars, 0.5 to 4 s |
| Reels, TikTok, Shorts | a change every 1 to 5 s; the hook in the first 1 to 3 s |

**Short-form:**

- Open on the strongest frame or line, never a logo, a slow fade-in or a greeting; the payoff or question is on screen in frame one.
- Reset attention every few seconds with a new shot, a punch-in, B-roll, a text pop or a sound. 3 to 5 seconds is the common advice; faster is a style to test, not a rule.
- Cover every claim with visual proof.
- For an ad family (15, 30, 60 s), cut the 15 first: it finds the smallest complete version of the idea (*practitioner rule*). Longer versions add context and proof; a 15 is not the 60 trimmed in order.
- Burn in large, high-contrast captions inside the safe zone (Caption Studio owns their style and QA). Many viewers start muted.
- Remove dead air but keep the breaths that give rhythm.
- An ending that flows back into the first frame invites a replay.

These are editing patterns, not a measured virality score; never present them as one.

## Cutting to music

- Run `beats` on the music asset. Put strong picture changes on downbeats (beat one of a bar), shot changes on beats, scene changes on 4- or 8-bar phrase boundaries. Cutting a frame or two early or on an off-beat reads looser and more organic; choose it on purpose.
- `beats` finds the pulse, not the bar: count bars from a strong beat you can hear, and check for half or double tempo. With a `low_confidence` warning, cut by ear.
- **Edit music to length** by removing whole bars or phrases at matching musical points and crossfading over a beat; check that no downbeat doubles at the joint. Avoid stretching music audibly.
- **Hit the ending:** back-time the track (start it earlier) so its real ending lands on the last frame or the logo, instead of fading out a song mid-phrase.
- Vary cut density with the energy of the section: every beat only at peaks or a drop, every two beats for most social edits, every bar (four beats) in calm passages (*practitioner rule*). Cutting on every beat from start to finish reads mechanical; let movement inside the shot land on the beat too.
- Sound can lead picture: start a musical change a few frames before the visual change, or land a hit exactly on the cut.

## Transitions

The hard cut is the default. Every other transition means something; use it for that meaning, and pair a stylised transition with a sound (whoosh, hit) on a beat.

| Transition | Meaning, when | Length (*rule of thumb*) | FrameCut |
| --- | --- | --- | --- |
| Hard cut | Continuous time or a deliberate jump | 0 | no `transition` |
| Short dissolve, a "soft cut" | Softens a jump inside one scene | 4 to 15 frames | `transition` 4 to 15, `dissolve` |
| Dissolve | Time passing, a thematic link, montage softness | 1 to 2 s; longer means more time passed | `dissolve` |
| Dip to black | End of a chapter, a big time jump, an emotional pause | 0.5 to 1.5 s in total | `dip_black` |
| Dip to white | Memory, flash, a bright reveal | 6 to 20 frames | `dip_white` |
| Wipe | Stylised or retro chapter change | 8 to 20 frames | `wipe_left|right|up|down` |
| Slide, push | Energetic change of place or topic, list steps | 8 to 20 frames | `slide_left|right|up|down` |
| Whip pan | Energy, a change of place matched to camera motion | 6 to 12 frames | a short `slide` in the direction of motion plus a whoosh; for a real motion blur, build it in Motion Graphics |
| Zoom, spin, glitch, light leak | Trend, music and social formats, motivated by a beat or a sound | 6 to 15 frames | Motion Graphics builds it as a clip; FrameCut places it |
| Match cut | Ideas linked by shape or movement | 0 | a hard cut planned on the storyboard |

Too many dissolves and decorative transitions are the clearest sign of an amateur edit. A transition needs handles on both clips; FrameCut refuses one without them.

## Sound for editors

Order of work: dialogue edit, dialogue processing (high-pass around 80 to 100 Hz, noise reduction, EQ, compression, de-essing), room tone, music, effects, mix, loudness check.

- **Dialogue is the anchor.** Set it first; fit music and effects around it. Music under speech sits about 15 to 20 dB below the voice; 20 dB is the accessibility-safe gap. In FrameCut set the music event's `gain_db` for the music alone, then `duck_db` about -10 to -15 dB under speech (the engine default of -6 dB is gentle; *rule of thumb*), and listen.
- **Edits need micro-fades and continuous ambience.** FrameCut adds the fades; add room tone where the background jumps.
- **Loudness by destination:**

| Destination | Integrated | True peak |
| --- | --- | --- |
| Social and streaming (YouTube, Spotify normalisation; no official TikTok or Instagram target) | about -14 LUFS | -1 dBTP |
| Podcast | about -16 LUFS | -1 dBTP |
| EBU R128 broadcast | -23 LUFS | -1 dBTP |
| ATSC A/85 (US TV) | -24 LKFS | -2 dBTP |
| Netflix | -27 LKFS, measured on dialogue | -2 dBTP |

Set the deliverable's `lufs`; `verify` measures the result within 1.5 LU and refuses true peaks above -0.5 dBTP. For a platform asking for -1 or -2 dBTP, read the measured `input_tp` in the receipt.

## Colour for editors

Correct before you grade, with scopes rather than a laptop display:

1. Know the source (log, RAW or Rec.709) and convert it once. A LUT made for log footage on Rec.709 material breaks the image; never convert twice.
2. Exposure: blacks just above the floor, highlights below clipping.
3. White balance: neutral greys line up across the RGB parade.
4. Contrast: set black and white points, then shape the mids.
5. Skin: near the vectorscope skin-tone line, judged by eye across different skin tones.
6. Match neighbouring shots before any look.
7. One subtle look over everything, after the correction: a creative LUT is built for balanced Rec.709, so apply it after exposure and balance, often at reduced strength (*rule of thumb*: 50 to 70%); avoid oversaturation, crushed blacks without intent and orange-and-teal on everything.

FrameCut's picture effects (`brightness`, `contrast`, `saturation`, `blur`, `vignette`, `grayscale` and the pixel looks) cover simple corrections and matching per clip. It has no LUTs, curves, colour wheels, qualifiers, windows or scopes: for log footage or a real grade, say so and offer the colour pass in Resolve or Premiere through `export --otio`, or ask for Rec.709 material.

## Delivery and QC

- **Specifications.** Social vertical: 1080×1920, H.264, 30 fps (or the source rate), AAC; about 10 Mbps is a safe middle. YouTube recommends about 8 Mbps at 1080p (12 at high frame rate). Masters: ProRes 422 HQ (about 220 Mbps at 1080p29.97); ProRes 4444 when alpha is needed. Never mix 25 and 29.97 fps without a conversion.
- **Vertical safe zones** (1080×1920, approximate, they differ by source): Reels keep about 210 to 250 px clear at the top and 280 to 310 px at the bottom; TikTok about 130 px top and 480 px bottom, plus about 100 to 150 px on the right for both. Key content between about y 220 and y 1440.
- **Captions:** SRT or WebVTT sidecars; about 42 characters per line, two lines, at most 20 characters per second for adults in English and 17 in Polish (Netflix; Caption Studio's readability defaults own the rules).
- **QC the exported file, not the timeline.** Watch it through and check: flash frames (a clip of one or two frames left by an edit), black or frozen frames, audio pops, dropouts and drift, loudness and true peak, spelling of every super and name, safe zones, exact duration (ads to the frame), frame rate, resolution and audio channels, the first and last frames.

## Beginner habits and pro habits

| Beginner | Pro |
| --- | --- |
| Cuts for variety | Cuts for a reason |
| Opens with a logo or an intro | Opens with the hook |
| Every shot the same length | Varies rhythm, holds the key moment |
| Decorative transitions everywhere | Hard cuts, motivated transitions |
| Music as loud as the voice | Dialogue first, music 15 to 20 dB under |
| Clicks at audio edits | Micro-fades and room tone |
| Ignores loudness | Meters to the platform target |
| A LUT on everything | Converts once, corrects, then a subtle look |
| One export for every platform | Per-platform framing, safe zones and specifications |
| Leaves every "um" or removes every breath | Removes distracting fillers, keeps natural breaths |
| Captions under the platform interface | Captions in the safe zone, readable size, two lines at most |
| Polishes before the structure works | Assembly, rough cut, fine cut, lock, then finishing |
| Watches only the timeline | QCs the exported file |

## What FrameCut cannot do here

Say so plainly and offer the route that exists, instead of approximating silently:

- **Subject-tracked reframing** (Smart Reframe, Auto Reframe), stabilisation, rotoscoping and Magic Mask, multicam and waveform sync: not available. Per-deliverable crops and keyed pans can follow a subject by hand on the storyboard.
- **Optical-flow slow motion** (Speed Warp, Optical Flow): not available; speed changes repeat or skip frames. Pitch: constant speed keeps the voice's pitch; a speed curve shifts pitch with speed, so lay the voice as an independent event when it must stay natural.
- **Colour pipeline** (LUTs, curves, wheels, qualifiers, scopes, log transforms): not available; see [colour](#colour-for-editors).
- **Voice isolation, dialogue levelling, compression and de-essing:** use the high-pass, low-pass and denoise effects, or Earshot through Toolbox for analysis.
- **Downbeat and bar detection:** `beats` gives the pulse only.
- **Adjustment layers and nesting:** per-clip effects, or render a section and ingest it.

## Sources

Paraphrased; checked 2026-11-07. Several books and manuals were read through secondary summaries, noted where that is the case.

1. Walter Murch, *In the Blink of an Eye* (rule of six), via UT Austin RTF wiki, No Film School and Musicbed summaries.
2. Edward Dmytryk, *On Film Editing*, via ProVideo Coalition "Seven rules" and SDSU "When to cut".
3. Karel Reisz and Gavin Millar, *The Technique of Film Editing* (Routledge; Lantern Media History archive).
4. Netflix Sound Mix Specifications and Best Practices v1.5; Netflix Timed Text Style Guides (General Requirements, English (USA), Polish: 42 characters per line, 17 characters per second for adults).
5. EBU R128; ATSC A/85 via TC Electronic; ITU-R BS.2434 (regional loudness and true peak).
6. YouTube Help, recommended upload encoding settings.
7. Apple ProRes white paper (data rates).
8. Adobe Premiere Pro help: J and L cuts, Auto Reframe, Auto Ducking, Morph Cut, skin tones in Lumetri.
9. Frame.io Insider and Workflow Guide (editing stages, Resolve AI tools, Resolve node templates); MixingLight (serial, parallel and layer nodes); Gamut (Resolve colour pipeline); Cullen Kelly on LUTs in a managed pipeline.
10. Videomaker and PremiumBeat (Resolve trim modes, dynamic trim, Scene Cut Detection, timing music, whip pans); Apple Final Cut Pro guide (edit to the beat).
11. FlowingData on James Cutting's shot-length research; Cutting et al. (PMC3485803).
12. WCAG 1.4.7 (background audio 20 dB below speech).
13. auto-editor (default margin around speech); RedShark News (text-based editing, fillers, Remix).
14. FFmpeg wiki `xfade`; GDELT on FFmpeg scene detection.
15. Social specification and safe-zone guides (Poster.ly, Adaptly, True Anthem; vendor figures, approximate).
16. CapCut and Adam Connell on hooks, pattern interrupts and retention (practitioner advice, unverified figures).
