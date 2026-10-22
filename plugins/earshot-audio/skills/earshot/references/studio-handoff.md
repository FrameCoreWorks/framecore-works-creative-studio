# Handing sound to a project's owner

FrameCore Works Creative Studio (or any project with an editor and an approval process) owns the brief, the accepted
storyboard, the master timeline and the final review. Earshot supplies sounds and evidence.

## What to ask for

Project and revision, the owner who asked, the operation, local paths and SHA-256 of the inputs, `fps_num` and
`fps_den`, whether frames count from zero, the source-to-timeline mapping (trims, speed changes), the sample rate, the
cues (id, frame, and whether the sound aligns on its onset, peak or end), the palette and the rights the project allows,
and the acceptance criteria.

## What to return

- The engine that ran (this plugin's pinned runtime, another pinned Earshot command line, or a different tool) and
  the readiness from `status`.
- The exact commands.
- Each WAV with its SHA-256, the `kit.lock.json`, measured onset, peak and end of every take used.
- The placement in samples for each cue and the readings that justify each choice, with their numbers.
- What was not run and why.

## Timing

Zero-based frame `f` at `fps_num/fps_den` is `t = f * fps_den / fps_num` seconds; the take starts at
`round(t * rate) - round(anchor * rate)` samples, where `anchor` is the measured onset, peak or end inside the take.
At 30000/1001 fps, frame 48 is 1.6016 s and frame 90 is 3.003 s. Earshot 0.4.0 reads a numeric fps in a cue file:
pass seconds and keep the rational rate in the project. Resolve a negative start (pre-roll before the film) instead
of cutting the onset. After mixing, check the encoded film with `timeline --cues`, not only the WAV.

## Approvals

An accepted board or edit stays accepted; a technical repair does not reopen it. A new sound the owner did not ask
for goes back to them before it replaces an accepted one. A silent delivery stays silent unless sound was requested.
