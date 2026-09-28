# Production Task Packet: complete authoring and QA reference

This reference expands the task-builder's decision rules. It is a text-deliverable and evidence-bounded audio-triage contract, not a generation adapter. Read-only research and inspection depend on real host capabilities and task authorization; follow [audio evidence and audiovisual handoff](audio-evidence-and-av-handoff.md) for media evidence, cue sheets, VO, music, SFX and captions. Use only the sections relevant to the user's current request. A packet does not imply that a target model will obey it exactly.

## 1. Intent and deliverable routing

| User's immediate job | Task-builder response |
|---|---|
| “I have an idea for a song” | Shape the idea into a concise song direction or ask one decisive question. Do not force a full production packet if a direction is enough. |
| “Write lyrics” | Clarify only material language/theme/voice constraints; draft original lyrics and label them as new assistant-written copy. Do not borrow protected lyrics or impersonate an artist. |
| “Make an instrumental” | Prepare style, groove, instrumentation, arrangement and listening tests; separate “no lead vocal” from incidental vocal textures if important. |
| “I need a prompt for [named tool]” | Research the current product/surface/model first; compile the complete prompt for that verified target and label any unconfirmed syntax or control. |
| “Change/cover/extend/replace this song” | Identify the source, intended operation, region and preservation priorities. Confirm the current UI supports the specific operation before asserting it. Provide comparison tests for the edited region and neighboring material. |
| “What is wrong with this song?” | Return a standalone review with its evidence scope, findings or labelled hypotheses, and one repair/test; no task packet is required. Determine whether actual audio and an available authorized inspection path exist. Without listening access, use a concise user observation or self-check list without claiming an inspected diagnosis. |
| “Give me a music-video idea” | Route to `creative-music-video-director` unless the user asks for a prompt-ready or operational task packet. |
| “Turn this approved video direction into a prompt” | Preserve direction locks and hand off model-specific prompt compilation to `video-prompt-architect`, after current model/surface research. |
| “Make the singer's mouth match every lyric exactly” | Triage as exact synchronization, not generic music-video generation. Verify a dedicated capability and source media; otherwise explain the boundary and provide a best-effort versus exact-sync decision note. |
| “Lip-sync this existing footage” | Separate dubbing, timing retime, new generated footage and source edit. Do not claim that a music model or general video prompt edits the footage with exact phoneme timing. |
| “Create/render/upload it now” | Record the explicitly requested operations and any existing authorization, then hand execution to the orchestrator. This owner has no bundled execution adapter. If the needed capability or authorization is absent, name that specific gap and provide the usable packet. Do not erase valid user authorization or re-request it solely because the owner changed. |

### Intent mode

- `explore`: the user has a seed, mood, association or reference and wants possibilities. Offer a concrete direction, not a giant questionnaire.
- `decide`: the user is choosing among meaningful routes. Compare only the decision dimensions they need.
- `build`: create the requested lyrics, brief, prompt, task packet or QA checklist.
- `repair`: assess actual evidence or the user's stated failure; preserve approved material and revise one cause.
- `finalize`: remove working notes and deliver the clean, complete artifact plus only essential use instructions.

The output can be shorter than this reference. Completeness means all material decisions and caveats for the task are present, not that every field below is filled.

## 2. Intake and evidence ledger

Before drafting, make a short ledger in working context:

| Field | What belongs here | If missing |
|---|---|---|
| Objective | Desired listener/viewer outcome and why the artifact is needed | Infer only if obvious; otherwise ask one concise question. |
| Task type | Song, lyric, instrumental, revision, music video, sync triage, repair, etc. | Resolve only if it changes the owner or packet. |
| Intended surface | Named current product, model, version, or “not chosen” | Research the user-named target; do not pick a provider on the user's behalf without asking when material. |
| Approved source truth | Exact lyrics, names, voice/artist facts, song/visual locks, audio/video evidence | Mark absent material as absent; never invent it. |
| Reference role | Inspiration, lyric source, sound/mix, identity, visual mood, timing, target edit or critique | Ask only when conflicting authority affects the result. |
| Deliverable language | Language for lyric/prompt/material visible to the listener | Mirror the user unless they specified another language. |
| Rights/consent | User authority for lyrics, source audio, voice/likeness/performance and image/video | Flag a real uncertainty; do not claim legal clearance. |
| Acceptance | How the user will tell whether the result works | Propose one observable criterion when user has not supplied one. |

Keep three evidence layers separate:

1. **Asset exists**: attached, accessible in this conversation/workspace, or absent.
2. **Asset was analyzed**: record user-report-only, present-not-analyzed, metadata-only, or the actual inspected ranges, channels and method. Attachment, a filename and metadata do not prove listening or full-clip analysis.
3. **Fact is verified**: supported by an official current source or direct user confirmation. A title, filename, pasted claim, cached memory or old prompt does not verify BPM, key, section timecodes, model, rights or UI state.

If browsing is disallowed, do not quietly browse. If the user insists on a current factual answer, explain that the fact remains unverified and ask them to provide current official evidence or permit a public-source check. Continue only with stable, clearly marked planning that does not depend on the missing fact.

## 3. Song-direction specification

Construct only relevant dimensions; distinguish direction from hard limits:

### Core

- **Creative premise:** a one-sentence description of the song's specific listener experience, situation or contradiction. Avoid interchangeable adjectives as the only concept.
- **Emotional movement:** starting state, changes (if any), and intended landing. Sustained mood is valid; do not force a build, chorus lift or catharsis.
- **Style reference:** genre or genre blend, optional era, and specific musical traits. Translate named-artist references into non-imitative characteristics. Do not treat broad genre labels as a full arrangement.
- **Groove / tempo:** feel, subdivision, energy, approximate BPM or range only if useful. Say “target” unless exact locking is documented and testable.
- **Sound palette:** primary instruments, texture, register, attack/decay, density, spatial character, and what each major layer contributes. Avoid indiscriminate adjective stacks.
- **Form and arrangement:** intro/verse/chorus/bridge/outro or another structure, section roles, instrumentation/vocal changes, transitions and intended repetition. Use time ranges only when measured or user-approved; otherwise use relative sections or approximate targets.
- **Voice and performance:** vocal type/profile, register, intensity, articulation, phrasing, language, diction, harmony/doubling and relationship to the beat. Do not request cloning or imitation of a real person without verified rights and a supported authorized route.
- **Lyrics:** exact approved block, original draft, or thematic/structural strategy. Separate lyric text from production instructions. Preserve spelling, names and language exactly where locked.
- **Mix / technical intention:** relative priorities like vocal intelligibility, low-end space or restrained reverb. Do not claim mastering, loudness, format or stem export unless the target supports it and current sources verify it.
- **Acceptance test:** one listening test for the primary decision (e.g. hook is understandable on first listen; lead vocal remains intelligible; instrumental has no lead words; edit preserves the accepted chorus identity).

### Write a useful prompt

Place the main outcome first. Then give the most important supporting musical traits, performance, arrangement, lyric handling, exclusions and useful technical targets. Use plain language with causal relations (“the sparse verse makes the close vocal feel exposed”) rather than a stack of disconnected labels. Include a small number of purposeful constraints. Negative constraints should prevent a concrete known failure, not become a wall of “no” statements.

Use exact field labels, section tags or quoted text only when the current product guide supports or illustrates them. A prompt guide example is not proof that tags are a rigid grammar. Lyrics should appear in a separate `Lyrics` section or field when available. User-supplied exact lyrics must not be edited inside a tool-facing prompt. For non-user-provided copyrighted text, do not supply continuation or reproduction; offer a fresh original alternative.

## 4. Task-specific packet patterns

### Original song

Include premise, listener/job, emotional form, sound identity, groove/tempo target, arrangement, vocal profile, lyric strategy or exact approved lyrics, format target, research status, prompt, and one listening checklist. If there are unresolved choices, prefer one decisive question or label a reversible assumption.

### Lyrics / vocal writing

Set language, point of view, subject, relationship, emotional stance, form, level of directness, rhyme/phonetic needs and banned phrases only where they matter. Check that each line is speakable/singable, has a clear role, avoids accidental cliché and stays consistent in perspective. Keep edits trackable if the user gave approved text. Do not name a real singer as a voice target; describe voice characteristics instead.

### Instrumental

State whether all voice is excluded or only lead lyric vocal; define the main instrument roles, rhythmic feel, energy contour, hook/motif, arrangement changes and acceptance test. Do not promise zero incidental voice unless the target can support and the result is checked.

### Cover, remix, extension or section edit

Confirm what must remain recognizable and what is allowed to change. Identify region via a user-selected section or measured evidence; don't infer timestamps. Research current operation names and controls. Prepare a full direction plus a preservation checklist. After the user applies it, compare the changed region and neighboring sections; never promise exact preservation of untouched material.

### Music video / visual performance packet

Carry in approved song-to-image direction, artist/persona facts, identity/reference authority and forbidden substitutions. Describe the video's core visual action, performance behavior, camera relationship, time progression, audio/lyric relationship and continuity only as requested. For every shot/beat, keep source truth and estimated timing distinct. High-level direction stays with `creative-music-video-director`; narrative development, sequence timing and generator-native syntax go to their packaged owners. Don't produce a second, conflicting concept while compiling a prompt.

### Visible singing and exact sync

Separate at least these four cases:

1. A character appears to sing, without exact lyric timing.
2. Generated video is asked to broadly follow a supplied song or lyric mood.
3. Generated mouth movement is expected to match supplied lyrics/phonemes precisely.
4. Existing footage must be re-timed, dubbed or lip-synced to replacement audio.

Only the first two are safely framed as best-effort creative direction absent stronger evidence. Cases 3–4 need a current, purpose-built, verified capability, clear source audio/video, appropriate consent and a test of actual synchronization. If those conditions are absent, preserve the exact-sync requirement and mark its execution readiness blocked. Present a non-exact alternative for the user's decision; adopt it only after the user accepts the relaxation. Do not relabel cutaways or general singing imagery as an exact-sync solution.

### Repair after a weak result

Record: the artifact actually available; the user's target; the observed failure; elements to preserve; likely primary cause; smallest revision; and observable retest. If media is absent, use `user_report_only` and avoid “I can hear/see.” If media exists but cannot be inspected, use `asset_present_not_analyzed`. If an analysis was actually made, identify its narrow scope without claiming a full technical audit. Deliver a complete replacement packet, not only a sentence patch.

## 5. Google Flow Music / Lyria evidence-sensitive notes

This is a historical evidence snapshot, not the live source of truth. Its exact original check date is `Unknown` in the portable package; the external development log is not runtime evidence. Re-run the mandatory research preflight and record the current access date and scope before current claims. Search leads include the [Lyria prompt guide](https://deepmind.google/models/lyria/prompt-guide/), the [Lyria 3.5 model card](https://deepmind.google/models/model-cards/lyria-3-5/), the [Flow Music song workflow](https://support.google.com/flow/answer/17084348?hl=en), and the [Flow Music music-video help page](https://support.google.com/flow/answer/17084421?hl=en).

### Historical notes to recheck

- The snapshot recorded Google Flow Music branding and the older ProducerAI name; names are search leads, not proof of the user's current interface.
- The snapshot recorded Lyria 3.5 for song creation and guidance on genre/blend and era, tempo, instruments, dynamics, vocal character/language, lyrics, and image inspiration. Verify which dimensions the selected current route supports.
- The snapshot recorded product-level song workflows such as prompt creation and, where available, Compose, section edits/Replace, Cover and Extend. Verify current documentation, active control and plan before promising any of them.
- The product interface's supported text/image/audio inputs do not automatically prove each modality is an input to the underlying Lyria model. The model card and app surface are different evidence layers.
- The historical notes recorded a help-page video model selector without a stable exact model name, and differing announcement/marketing descriptions. They establish no present model/version; use `unknown_runtime` until current evidence resolves the selected interface.

### Operational caution

An edit command may alter neighboring musical material. A prompt's BPM, target length, section sequence, lyric spelling, pronunciation, harmony, mix or transition is not evidence of exact output. Audition the actual audio. Use section-specific comparison and protect accepted material; if the edit drifts, change the operation or region rather than stacking more prompt negatives. Apply the same discipline to music-video prompt and visible singing.

Do not preserve stale claims about price, credits, plans, regions, age eligibility, maximum durations, model availability, export, commercial rights, Memories retention or mobile/web parity. Check the current official source and/or ask the user to confirm their selected interface when that detail changes the task.

## 6. Evidence and citation discipline

Use these labels in notes when a product/model statement could be confused with creative advice:

| Label | Meaning | Permitted use |
|---|---|---|
| `official_current` | Current official help/product/model documentation checked for this task and date | State the narrow documented fact and cite it; still qualify account-/region-dependent details. |
| `dated_announcement` | Official release/update statement tied to publication date | Explain what Google announced then; do not silently promote it to current capability. |
| `practitioner_report` | Individual public experience, with date/surface if available | Suggest a QA concern or experiment only; do not assert general behavior. |
| `unknown_runtime` | Conflicting, unnamed, rollout-specific, account-specific or unverified | Ask for the current UI/model or mark the prompt mapping provisional. |
| `local_synthesis` | Conservative production recommendation based on source synthesis | Present as a useful method, not an official provider rule or measured result. |

For fast-changing facts, cite a source close to the claim and note access date. Prefer primary sources. A web result or marketing page cannot prove the user has the feature in their account. If a user explicitly prohibits research, honor it and leave those claims unresolved. Research is not a legal review or rights clearance.

## 7. Packet schema and presentation

Use this schema selectively. A one-prompt request may need only the key, prompt, QA and verification notes; a complex repair can use most fields.

### Production Task Packet

**Task / intent**  
Short description of the requested result, task type, and intent mode.

**Objective**  
What the output should accomplish for the listener/viewer or production.

**Approved source truth**  
Exact supplied material, names, lyrics, audio/video evidence, reference roles and accepted locks. Mark which asset has not been inspected.

**Assumptions / open decision**  
Only reversible assumptions, plus the single decision that blocks the final packet if one exists.

**Rights / consent notes**  
Only material source/voice/likeness permission questions; no legal conclusion.

**Creative direction**  
Song or visual logic, specific and testable. Keep high-level video concept ownership distinct.

**Exact lyric block / lyric strategy**  
Verbatim user-approved copy or newly authored lyrics, in the requested language. Otherwise `N/A`.

**Target interface / evidence status**  
Exact current product and model if known, date and evidence class; unresolved controls marked `verification_required`.

**Copy-ready prompt / task text**  
The complete block to paste. Put only tool-relevant instructions here; no assistant-side caveats that could confuse the target model.

**QA / acceptance test**  
One primary observable listening, lyric, edit or visual check, plus secondary checks only when important.

**Repair path**  
For follow-up: failure evidence → preserved locks → one correction → one retest.

**Next action**  
One user action such as try the packet, confirm a current model label, or return with the resulting audio/video.

Describe the artifact and operation separately. A prepared packet is not generated or mixed media. Use “inspected” only for the recorded actual evidence scope; use “saved” or “uploaded” only when a separate authorized operation really succeeded. Say what remains for the user or a verified execution route to do.

## 8. Bounded iteration and release gate

For each repair cycle:

1. Re-state the one primary failed acceptance test in observable terms.
2. Preserve explicit accepted lyrics, sound traits, persona, source reference, shot or constraint.
3. Identify whether the failure is prompt ambiguity, unsupported capability, rights/consent, missing source material, model drift or an operation mismatch. Don't blame a model when evidence is insufficient.
4. Change one causal input or operation. If the task itself requires multiple dimensions, state which is the controlled primary change and which fields stay fixed.
5. Deliver the entire revised packet and one retest. Keep previous version status truthful.
6. Stop when the user accepts, asks to stop, or the only remaining issue requires an unavailable/unauthorized capability. Do not promise convergence after repeated attempts.

Release gate results:

- `READY`: text is complete and source-safe for the requested purpose; evidence, assumptions and unsupported claims are transparent; the acceptance test is usable.
- `REWORK`: a material ambiguity, factual gap, unapproved lyric, generic or conflicting instruction, missing preservation lock or defective handoff remains. Repair before final handoff.
- `BLOCKED`: a necessary permission, exact source, current model identity or capability cannot be resolved. Give the safe partial work and the one blocker.

Passing this gate means only that the written packet is ready for the user to try. It does not mean the generated output will pass.

## 9. Failure patterns to prevent

- Generic mood adjectives without a musical premise, role or observable arrangement.
- Listing many genres, contradictory tempos, incompatible vocal instructions or conflicting section changes without a priority rule.
- Mixing exact lyrics into prose instructions so the tool rewrites them accidentally.
- Treating `[Verse]`, timestamps, `BPM`, duration or text labels as guaranteed parser syntax without current official evidence.
- Calling any female/male singer “the artist,” inventing artist biography or defaulting to a living performer imitation.
- Claiming the assistant heard a file because it was attached or saw a result from a screenshot description alone.
- Equating an atmospheric performance video with exact lip sync; equating a prompt with editing existing footage.
- Reporting a current model/version based on a cached page, prior announcement or user's recollection.
- Promising that Replace/Cover/Extend preserves everything outside the intended section.
- Adding more adjectives/negative constraints after the same failure without changing a causal control or acceptance test.
- Including every production checklist item even when the user asked for one simple prompt.
- Leaving out the exact content the user needs to paste, then providing only “prompt fragments” in the final handoff.

## 10. Small examples

### Correct evidence distinction

**Safe:** “The current Flow Music Help page exposes a section-replacement workflow. Confirm it is visible in your account before relying on it; review the surrounding bars after applying it.”  
**Unsafe:** “Replace edits only the selected section and leaves the rest untouched.”

### Correct audio honesty

**Safe:** “I have your lyrics and artist notes, but no audio to analyze, so the section map below is provisional.”  
**Unsafe:** “I listened to the track and the second chorus starts at 1:24” when no such analysis occurred.

### Correct sync boundary

**Safe:** “This prompt asks for a singer visibly performing the supplied song. It is not a guarantee of phoneme-accurate lip sync; if exact matching is required, confirm a dedicated sync tool and run an actual sync test.”  
**Unsafe:** “Add a few cutaways and the lipsync is solved.”

### Correct repair

If the user says “the chorus got too big; keep the verse and voice, make only the chorus more intimate,” preserve verse and vocal identity, revise chorus density/arrangement as one change, and test whether the chorus reads more intimate without changing the singer. Do not redesign genre, lyrics, tempo and mix all at once.
