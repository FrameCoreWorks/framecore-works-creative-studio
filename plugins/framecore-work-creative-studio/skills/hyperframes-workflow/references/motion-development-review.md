# Development review for motion

Read when judging a rendered or sampled motion piece beyond the automatic checks. The critique measures emptiness, legibility and pacing; this review asks whether the idea develops. It is a person's judgement (Studio's or the user's), written into the [QA record](../templates/motion-qa-record.md) and carried into the composition and temporal verdicts of [`acceptance.py`](../assets/motion-review/README.md#acceptance-in-four-verdicts).

## Seven questions

1. **Idea.** Does the one mechanism the contract names communicate and grow, or does the time between the hook and the end only repeat it?
2. **Composition.** Do scale, framing, hierarchy and figure and ground change where the eye goes and what it means? A colour swap alone usually leaves the composition where it was.
3. **Rhythm.** Is there contrast between fast and held, tension and release, suited to the brand? Even busyness is as flat as even stillness.
4. **Cause.** Does each new state come out of the previous one (its shape, material or action), or does a transition hide an unrelated scene?
5. **Signature.** Is there one moment someone could describe afterwards, beyond a bigger version of the default move?
6. **Physical logic.** Does every object do its real job on its material, seen from the side that shows the result (a drill into a board's face, a saw in its kerf, a hammer on a nail head), with a visible result (chips, the off-cut, the hole), and does the next board grow out of that result? A tool moving beside its material, or an action seen from a side that hides it, fails here even when the motion is smooth (the [scene logic check](dense-kinetic-reels.md#scene-logic-check-run-it-on-the-storyboard-and-again-on-the-frames) in [dense kinetic reels](dense-kinetic-reels.md)).
7. **Ending.** Does the end land, settle and stay readable, with the exact logo, offer and call to action?

## Diagnose, then repair

- Name the main weakness, the interval where it shows and what the viewer misses there. Findings come from inspected frames or a viewing, never from the contract alone.
- Restraint is not a defect. A single sustained move or a long hold passes when it carries tension, communicates and resolves as the brief asks. No number of effects, beats or cuts is a target.
- Repair the dimension that failed: give the mark or element a new role, recompose its relation to the type and the field, or give the new state a consequence in timing. More particles, extra cuts or easing tweaks do not fix an idea that does not develop.
- Example: in a 10-second vertical piece whose middle only scales the same mark up and swaps its colours, the idea stalls between 3 and 7 s. A repair lets the mark become the frame that reveals the product photo, or opens its counter onto the offer; adding sparkles does not.
- One repair round for the main weakness, inside the shared review budget. When the seven questions have no material gap, stop: a clean result needs no extra round.

## What the answers rest on

- Key frames at full size and phone scale can answer questions 1, 2, 5, 6 and 7 for what is visible. Questions 3 and 4, and the motion half of question 6, need a normal-speed viewing: frames show states and their order, not smoothness, rhythm or sync.
- Mark each answer as seen in playback, seen in frames, reported by someone else, or unknown. An unknown answer stays open in the QA record and never counts as a pass.
- With sound, rhythm and the ending are judged with the sound on. A waveform or an audio stream in the file is not listening; record the listening in `acceptance.py` with `--listening heard`.
