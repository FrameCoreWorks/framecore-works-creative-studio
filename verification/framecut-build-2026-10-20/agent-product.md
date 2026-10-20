# FrameCut product montage trial

Result: the stable runtime successfully produced a 9-second still/video/still montage with music and a bounded transparent motion callout, in landscape and vertical. A later revision enlarged only the title and editorial captions. The source edit, motion placement, and decoded audio remained identical.

## Concrete delivery

Final verified project root: `node_modules/stable-test/` within this folder.

- `renders/r13-landscape-final/video.mp4`: 960 × 540, 270 decoded frames, 30/1 fps, 9.0 seconds.
- `renders/r13-vertical-final/video.mp4`: 540 × 960, 270 decoded frames, 30/1 fps, 9.0 seconds.
- `project.json`: native project revision 13, with immutable source hashes and portable relative paths.
- `handoff/r13/`: native project, relink map, shots CSV, picture EDL, and explicit interchange loss report. Named editor import and OTIO were not tested.
- `evidence/final-comparison.json`: machine-measured typography preservation comparison.
- `evidence/r12-r13-landscape-comparison.jpg` and vertical counterpart: actual before/after rendered frame comparisons.
- `evidence/r13-landscape-inspection.jpg` and vertical counterpart: actual decoded final samples including cuts and motion entry/exit.
- Each final bundle has its technical receipt and `review-evidence.json`.

## What ran

Read the installed FrameCut SKILL.md, runtime README, strict contract and related review guidance. Probed capabilities; created original procedural illustrated product PNGs, a moving detail MP4, synthesized WAV music, and an alpha QTRLE callout. Used init, ingest, analyze, apply, compile, motion-request, attach-motion, preview/final render, review, verify, undo and export. No downloads, paid services, uploads, publishing, speech fabrication, runtime modifications or repository edits.

The brief has no speech. “Captions” are editorial product supers implemented as typed `texts` events. Speech-caption projection, ASR, word timing and meaningful SRT/VTT output were deliberately not tested; generated sidecars are empty and caption QA says no_captions.

All CLI commands and stdout/stderr/exit codes are captured in `commands.log` and `logs/`, including the copied early history in the stable root. Fixture generation and orchestration are retained as Python scripts.

## Stable comparison evidence

Revisions 12 → 13 changed only `sequences[0].texts`; within those events only four `size` values changed: title 0.055 → 0.075; three editorial captions 0.033 → 0.05. Audio, clips, duration, FPS, background and overlays stayed equal. Both source-map files were byte-identical.

Both final formats reused six cached stages: three normalized base visuals, assembly, mix, and callout visual. Both receipts have `cache_built: []`. Runtime Python source hashes were recorded before and after; they were unchanged for this pair.

Decoded PCM SHA-256 was identical across both baseline and enlarged deliveries, in both formats:

`e541125d64d1c91e4e1c5ce184010bb42748c2001a0f1eab0b0b702a9e6893d0`

Output measurement: -18.14 LUFS integrated, -4.90 dBTP, 48 kHz stereo AAC. This is measured evidence, not a listen. Decoder output included AAC padding; stream duration and picture duration both measured 9.0 s.

## Actual inspection and repair

Inspected source samples, all 12 initial runtime review frames per format, baseline detail frames, before/after typography comparison frames, and 19 final decoded frames per format: 0, 37, 74, 75, 89, 90, 104, 105, 108, 111, 116, 134, 159, 164, 165, 179, 180, 225, 269. These show the cuts, title fade, ring/leader drawing and fade, and enlarged text without clipping.

Initial landscape detail caption crossed the bottle. Repaired the deliverable caption zone before the typography-only comparison; retained the edit/music. Final observed frames show caption below the bottle. Both formats intentionally contain square footage with black bars.

No continuous playback was watched and no audio was heard. Review records correctly declare `picture_watched: false` and `audio_heard: false`; the scoped outcome passes the sampled-frame/technical criteria only. Real-time pacing, perceived sound quality and listening acceptance remain unassessed.

## Failures and limits

1. Two later invocations initially returned `busy` for an empty `render.lock` despite preceding renders exiting successfully. Exact process scans found no renderer; documented abandoned-lock recovery allowed progress. `ps` itself failed in the sandbox with “fatal library error, lookup self”, so `/proc/*/cmdline` was used. Immediate checks within one render process showed the lock had been removed. The parent contract tester identified the visible-scratch filesystem watcher restoring transient state; moving the intact job under `node_modules/stable-test` eliminated this behavior. No such failure occurred in the final stable pair.
2. Parent runtime changes during the first trial invalidated caches; those preliminary cache receipts are not the conclusive comparison. The final r12/r13 pair used unchanged source hashes and passed.
3. Deliberately replaying an edit against an old revision returned `stale_revision`, as required.
4. PNG/QTRLE inputs emitted `unlabelled_color` warnings. The fictional illustrated SDR samples were visually inspected; no HDR/color-mastering claim is made.
5. Picture-only interchange correctly reports that independent audio, title styling and motion cannot be recreated from its basic EDL. The native project and callout contract retain them.

## Reproduction

Use the installed CLI path recorded in `commands.log`. From `node_modules/stable-test`, `framecut.py verify project.json --bundle renders/r13-landscape-final` and the vertical equivalent verify the final state. The captured revision history, operation JSON and sources reproduce the edit. `final_pair.py` documents the exact baseline/typography/cache comparison sequence; it expects the preserved pre-pair revision 11 and new output folders, so use a fresh copy rather than overwriting the accepted finals.

Stop: sufficient for this bounded CLI editing and revision trial, with audio listening/continuous playback explicitly unreviewed.
