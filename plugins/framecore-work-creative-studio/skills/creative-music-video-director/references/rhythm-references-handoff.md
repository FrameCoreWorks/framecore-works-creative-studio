# Rhythm, review, revision and handoff

This reference keeps music-video direction executable without turning a concept into technical prompt syntax or a mandatory shot list.

## Musical and edit relationship

When musical structure is actually available, select moments where image, action, performance, camera or edit should relate to it. Possible relationships include landing on a beat, anticipatory motion, syncopation, delayed response, a held image over several beats, anti-sync, silence, deceleration or no visual change. Explain the intended effect; do not decorate every beat.

Use section labels or time ranges only when supplied or verified. Mark a user-provided map as supplied, a direct analysis as observed, and a reasoned placement as approximate. If no track analysis exists, use relative terms (opening, later verse, repeated chorus) only when the user provided that structure; otherwise keep rhythm ideas conceptual. Never invent BPM, bars, exact drop points, section order or timecodes.

Editing may be fast, held, mixed, repetitive, sparse or highly synchronized. Cut density can rise, fall, or remain stable. Long holds may create attention, vulnerability, power, observation or tension; they can also fail to communicate. Evaluate the intended viewer experience and perceptible action rather than relying on fixed seconds-per-cut rules. A chorus can intensify, simplify, withhold, repeat or leave the frame unchanged. Promise a payoff only when the selected direction provides a visible cause and result.

## Authorial direction gate

Before handoff, perform a short bounded critique:

1. **Specificity:** Is the central image/action tied to the supplied song, artist or user association? Would swapping these leave the concept unchanged?
2. **Purpose:** Does the camera, setting, performance, symbol and edit each help the intended experience? Remove stock spectacle added without a reason.
3. **Form:** Are any contrast, escalation, movement, motif recurrence or climax requirements being forced by habit? Preserve deliberate repetition, restraint and stillness when they work.
4. **Clarity:** Is the main event or attention path visible? Avoid concepts that need unknown backstory to make sense.
5. **Truth and control:** Are audio observations, artist facts, lyrics, reference authority, timings and locks accurately labelled?
6. **Repair test:** If one material issue remains, name its cause, the smallest correction and one observable acceptance test. Do not hand off a failing direction as finished.

This is a creative-direction check, not a render review. An actual generated clip goes to [video-prompt-architect](../../video-prompt-architect/SKILL.md) for picture/motion and audiovisual alignment, and [audio-production-director](../../audio-production-director/SKILL.md) for audio triage. Carry the actual prompt, carriers, timing, supplied output and inspected-range evidence. A good direction does not certify execution quality.

## Proportionate direction contract

For a handoff, include only applicable fields; do not force an empty field to complete a template:

- `direction_thesis`: central idea, image/action engine and intended viewer effect.
- `song_evidence`: audio, lyrics, map or description actually supplied/verified; uncertainty and estimates remain explicit.
- `chosen_form`: performance, narrative, symbolic/abstract, hybrid, persona/fashion, rhythm-led or another apt form; name the primary engine.
- `visual_world`: spatial, light, material, image and camera rules required for the concept.
- `persona_performance_locks`: approved observable behavior, identity or styling constraints, plus allowed changes.
- `emotional_rhythm_logic`: how viewer experience and musical relation progress, persist or deliberately counterpoint.
- `motif_reference_roles`: meaningful motifs, reference authority/scope, and originality limits.
- `acceptance_and_risks`: one or more observable direction checks and likely failure/correction.
- `open_decisions`: unresolved facts or creative choices that change the next stage.
- `requested_handoff`: target owner and what that owner needs; omit if the user only requested exploration.

### Handoff to `storyboard-sequence-architect`

Pass the selected thesis, supplied/verified song structure, emotional and performance logic, relevant motifs, accepted image rules, timing uncertainty, approved reference roles, continuity locks, and open decisions. The sequence owner determines beat order, shot IDs, duration estimates and actual continuity dependencies. Do not dictate unnecessary shot counts or pretend the direction is already storyboarded.

If the direction locks a sustained composition or fixed camera, preserve it through shot cards and board panels. Distinct time samples may legitimately share framing; vary only approved performance, light or object state. Pass source/version and the actual basis of music timing so a conceptual section map does not become measured timecode downstream.

### Handoff to `video-prompt-architect`

Pass generator-neutral world, observable actions, performer/camera relationship, motion/edit intention, exact approved dialogue/copy if any, style/identity locks, reference assets and roles, scope, acceptance test, and what may simplify. The prompt owner checks the named current generator/model/surface and compiles a feasible prompt. Do not include unverified native syntax or claim that prose creates strict continuity without a bound carrier.

If the user asks for both downstream artifacts, preserve a clear order: direction decision → sequence plan where timing/shot structure is needed → generator-aware prompt. This does not mean the user must receive a long internal handoff or fictional agent dialogue.

For a requested audio/visual production packet, also pass the sonic thesis, exact lyrics/VO status, sources and permissions when known, music-to-action relation, any cue/shot links and required synchronization to Audio Production Director. Use its [audio evidence and audiovisual handoff](../../audio-production-director/references/audio-evidence-and-av-handoff.md); keep proposed timing, observed timing and unknowns distinct. A missing exact-sync capability does not silently authorize approximate singing.

## Focused revision loop

On critique, identify the actual rejection: central idea, image cause, viewer relation, persona behavior, rhythm, reference use, feasibility or a specific visual result. Keep accepted elements and exact locks. Change the smallest upstream decision that can address the cause, not only the prop/location adjective. If the user has only described a render and has not supplied it, do not claim visual inspection; ask for the actual media or state what can be assessed from text alone.
