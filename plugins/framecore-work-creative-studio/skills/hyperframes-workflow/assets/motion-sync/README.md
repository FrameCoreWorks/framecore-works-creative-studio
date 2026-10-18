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

Audio files must be supplied or licensed for the use; record them in the asset ledger. `sync.mjs` does not detect tempo or align speech: BPM and offset come from [`beats.py`](#analysing-a-supplied-track), the music source or the user, and subtitle timing from the user or a separate tool.

## Adding sound to a delivered video

Studio never delivers toy tones (bare oscillator beeps, untreated noise) as sound. A video is delivered silent first unless the brief asks for sound; then Studio asks once whether sound is wanted and offers these routes:

0. **Studio sound design.** Effects designed for the picture's own events and a composed music bed, rendered at studio standard by [motion sound design](../motion-sound/README.md) (`sound.py plan`, `mix`, `check`): layered synthesis, frame-exact timing, mastered to −14 LUFS. It needs no upload, and a user's track or voice-over from the routes below replaces or joins the composed music.

1. **The user's own file.** The user uploads music or a recorded voice-over. Record it in `music` or `voiceover` (with `bpm` and `offsetMs` for music when known) and mux it into the rendered MP4 without re-encoding the picture, for example `ffmpeg -i video.mp4 -i voice.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -t <duration> out.mp4`. When the sound should start later, insert real silence with `-af "adelay=<milliseconds>:all=1"`; `-itsoffset` only shifts the stream's start time, which some players and editors ignore. For music, follow the rights checks of [Audio Production Director](../../../audio-production-director/SKILL.md); a library or a "royalty-free" label alone does not clear a use.
2. **A voice or music provider such as ElevenLabs.** Only when the provider is actually connected in the conversation (a connector or an API key the user supplied) and the user has confirmed the cost and the terms; never call one from documentation alone. Otherwise give the user what they need to generate it themselves: the exact voice-over text from the contract's copy, its timing as an SRT file built from the captions or scene holds, and voice direction (tone, pace, pronunciation). The user generates the file, uploads it, and route 1 applies.
3. **A local generator** (Codex or the user's computer). Only a tool the user names that is already installed and whose licence allows the use; Studio does not install one unasked.

After muxing, check the encoded file: one audio stream, the expected duration, an unchanged video stream and sync at the first spoken word or beat. In a 2026-10-07 check this command kept a 120 BPM click track sample-exact on a 6-second ChatGPT render (first click at 0.0 ms, and at 1000.0 ms with `adelay=1000`), and left the video stream byte-identical. A Remotion render showed a constant 42.7 ms AAC start delay instead, so measure the file that is delivered.

## Analysing a supplied track

Two unchanged scripts from [kaventro/motion-designer](../../../../integrations/kaventro-motion-designer/README.md) (MIT) read and cut a track the user supplied. They need Python 3 and ffmpeg (`beats.py` uses ffmpeg's `aspectralstats`, available from ffmpeg 5.1), with no Python packages, so they also run in a code-execution sandbox.

```sh
python3 beats.py track.mp3 --json grid.json
python3 music_edit.py track.mp3 grid.json --from-bar 5 --bars 8 --fps 30 --out cut
```

- **`beats.py`** prints the tempo (fitted through the attack of every beat), the beat and bar length, where bar 1 starts and whether that downbeat is clear, then one row per bar: loudness with `drop` and `breakdown` marks, attacks per beat (how busy), brightness, how much of the spectrum is filled, and crest (room for hits). Its last line says whether the track can be a bed under words. `--json` saves the grid; `--sheet sheet.png` draws a spectrogram with bar lines.
- **`music_edit.py`** cuts whole bars from the grid, exact to the frame at `--fps` (pass the contract's frame rate), with 6 ms and 12 ms edge fades, and writes WAV and AAC. It prints which film beat each drop lands on.
- **Into the contract:** use the printed BPM unrounded with `--offset-ms` 0 for a cut that starts on a bar (or bar 1's start in milliseconds for an uncut track): `node sync.mjs motion-score.json --bpm 120.002 --offset-ms 0 --music cut.wav --out synced.motion-score.json`.

Check the result before trusting it: the tempo is what you would tap along to, drops and breakdowns fall 4, 8 or 16 bars apart, and an `uncertain` downbeat means checking that sections start on bar lines (shift bar 1 by one beat when they do not). Cut only on bar lines; never time-stretch or re-pitch, and when the story needs more or less time, change the holds.

**Sound brief.** Before choosing or cutting a track, write one or two sentences in the contract's `audio`: the music's role (in a type-led or explainer video it is a bed under the words: few instruments, no lead melody over text, mixed low; in a product reveal it may lead), the tempo from the pace (calm or editorial about 90–110 BPM, energetic 118–128), an energy level per scene with the biggest lift on the reveal, and a texture that matches the look. The [motion styles](../motion-styles/README.md) suggest a range for each. A bed has `fill` at or under 30% and crest of 12 dB or more in `beats.py`; a track that fails is replaced, not rescued by mixing it lower.

## Example

[`examples/voice-over.srt`](examples/voice-over.srt) is an original three-line voice-over script for the starters' contract.

## Verification boundary

During package preparation, in a Linux development container, the example captions were imported into the starter contract at 120 BPM and reviewed in all three formats without findings. A synthetic 120 BPM click track was rendered through the Remotion starter: the encoded AAC track kept the 0.5-second beat spacing to the sample, with a constant 2050-sample (42.7 ms, about 1.3 frames) start delay from the encoder. Check sync in the target player. Preview audio playback was not exercised, and host behavior is not verified. On 2026-10-07 `beats.py` found 120.002 BPM, bar 1 at 0.250 s with a clear downbeat and the drop at bar 9 in a synthetic 32-second test track with accented downbeats, and `music_edit.py` cut four bars to exactly 240 frames (8.000 s at 30 FPS).

## Lyric timing

[`lyric_timing.py`](lyric_timing.py) gives every word and line of a song its sung time, with the user's lyrics as the truth. A recogniser says when words are sung; the tool aligns its words to the lyric words (a misheard word keeps the correct spelling, Polish letters included), interpolates words it did not hear between their neighbours, finds the beat grid with [`beats.py`](beats.py) and gives each line a board cut one frame before the line, moved to the nearest half-beat when that is within `--snap-ms` (80 ms). Word times stay on the sung syllables for highlights. It writes JSON (lines, words, cuts in seconds and frames, tempo, the share of matched words and the lines to check by ear; `matched` means the recogniser heard that word, not that its time was verified, and unmatched words are interpolated; `--fps` takes rational rates such as `30000/1001`), LRC (`--lrc`, `--lrc-words` with word stamps) and SRT.

```sh
pip install stable-ts                      # recogniser for songs (MIT, archived 2026-05-30); name the model, e.g. Whisper large-v3 (Apache-2.0)
python3 lyric_timing.py song.mp3 lyrics.txt --out song.timing.json --lrc-words song.lrc --srt song.srt
python3 lyric_timing.py song.mp3 lyrics.txt --words words.json  # times from any other tool: [{"text", "start", "end"}]
```

For a dense mix, a vocal stem helps: use one the user supplies or a separator whose model licence allows the job. Demucs code is MIT, but its pretrained weights are for research use only (maintainer, issue 327), so it is not a default for client work. With whisperx the tool currently aligns its own transcription, not the supplied lyrics, then maps the lyrics onto it; stable-ts aligns the supplied lyrics directly. Licence verdicts and the planned changes are in `docs/research/motion-2026-10/chatgpt-delta-findings.md` in the repository.

The user supplies the track and the lyrics and confirms the right to use them. Lines matched at half or less, lines whose heard neighbours overlap so a missing word has no room, and lines whose unheard words would otherwise stretch across an instrumental gap (they are kept beside the next heard word) are listed for a check by ear (`needs_check`); a line sung from 0 s cuts at 0, never before. Recognisers are not bundled: they download models of several hundred megabytes. During package preparation on 2026-10-12 the alignment, interpolation, beat detection on a click track, snapping and exports passed `tests/lyric_timing_test.py`. On 2026-10-18 a real song ran end to end in a Linux container: Brad Sucks, "Total Breakdown" (2:19, CC BY-SA 3.0, from archive.org) with lyrics from Genius, faster-whisper 1.2.1 with the `small` model on CPU, 23 s: 98 % of the lyric words matched, 23 lines, 105 BPM, 9 cuts on a half-beat. Two defects were found and fixed: faster-whisper failed to open the file with PyAV 19 (the tool now decodes with FFmpeg), and one line the singer sang differently from the published lyrics was stretched across a 20 s instrumental break and not flagged (it now sits beside the next heard word, within 0.2 s of what the recogniser heard, and is flagged). Timing was checked against a second recognition pass, not by ear; the tempo is unverified.

Measured on a reference lyric reel (39 s, 84 BPM): its 27 board changes followed the sung words, a median 0.95 s apart; 22 % sat within two frames of a beat and 56 % within two frames of a half-beat. Text arrives with the voice; the beat drives accents (pulses, scale hits, background changes) rather than every cut.

