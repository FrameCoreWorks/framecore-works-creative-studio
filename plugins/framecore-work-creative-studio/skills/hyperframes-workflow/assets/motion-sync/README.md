# Music and voice-over sync

[`sync.mjs`](sync.mjs) ties a motion contract to music and voice-over. It is dependency-free (Node.js 20 or newer) and uses the shared [scene engine](../motion-scenes/README.md), so keep it next to `motion-scenes` when copying it into a project.

```sh
node sync.mjs motion-score.json --bpm 120 --offset-ms 0 --beats-per-bar 4
node sync.mjs motion-score.json --bpm 120 --music track.wav --captions voice-over.srt --voiceover voice-over.wav --out synced.motion-score.json
```

## What it does

- **Beat grid.** `--bpm`, `--offset-ms` (when the first beat sounds, from frame 0) and `--beats-per-bar` become `music` in the contract. The tool prints where every scene start, hold start and caption falls on the grid: bar and beat, the nearest beat frame and the offset in frames. Beats are computed from the master timeline as in [motion craft](../../references/motion-craft.md#rhythm-and-music), so rounding never accumulates; non-integer frame rates such as 30000/1001 work.
- **Captions.** `--captions` reads SRT or WebVTT. Each cue's exact text goes into `copy` as `caption-1`, `caption-2` and so on (`--prefix` changes the name), and `captions` holds its frame interval `[start, end)`. Styling tags are dropped and line breaks kept. Overlapping cues are shifted to start when the previous one ends, cues past the last frame are skipped, and every adjustment is reported. Existing captions are only replaced with `--replace`.
- **Audio files.** `--music` and `--voiceover` record file names in `music.src` and `voiceover.src`; optional `volume` is from 0 to 1.

Without `--out` it is a dry run. With `--out` it writes a new file, never overwriting one, and increments `revision`: the earlier approval no longer covers the result, so present the storyboard again. It never moves scenes or holds; the offsets it reports are proposals for the next revision, and putting only major events on downbeats is a choice, not a rule.

## Where the sync shows up

- `check-score.mjs` validates `music`, `voiceover` and `captions` (order, no overlap, existing copy, frames inside the timeline) and warns when a caption is shorter than the reading heuristic. The storyboard (`--markdown`) shows each scene start as bar.beat and lists the captions.
- The scene engine draws captions above the scenes, cut on their exact frames, with optional `tokens.captions` `{size, weight, color, background, bottom}`; a `tokens.safeArea` bottom is respected.
- The [single-file preview](../single-file-preview/README.md) plays `music.src` and `voiceover.src` from files next to it; while audio plays, the audio clock chooses the frame.
- The [Remotion kinetic type starter](../../../remotion-video-production/assets/kinetic-type-starter/README.md) renders the captions and mixes both files from its `public/` folder.
- The [frame review](../motion-review/README.md) captures the start, middle and end of every caption and measures caption text whenever it is shown.

Audio files must be supplied or licensed for the use; record them in the asset ledger. The tool does not detect tempo or align speech: BPM, offset and subtitle timing come from the music source, the user or a separate tool.

## Example

[`examples/voice-over.srt`](examples/voice-over.srt) is an original three-line voice-over script for the starters' contract.

## Verification boundary

During package preparation, in a Linux development container, the example captions were imported into the starter contract at 120 BPM and reviewed in all three formats without findings. A synthetic 120 BPM click track was rendered through the Remotion starter: the encoded AAC track kept the 0.5-second beat spacing to the sample, with a constant 2050-sample (42.7 ms, about 1.3 frames) start delay from the encoder. Check sync in the target player. Preview audio playback was not exercised, and host behavior is not verified.
