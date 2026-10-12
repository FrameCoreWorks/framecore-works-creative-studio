# Deep research 1 of 3: Gemini (findings extracted 2026-10-12)

Source: the owner's Gemini Deep Research report "Plan Badawczy Motion Graphics" (22 pages, Polish). Not stored here; these are the extracted claims, each to be checked against its primary source before it enters the package. Status: CLAIM (from the report, unchecked), CHECK (verify first), CONFLICT (disagrees with another source or with Studio).

## Music analysis

- CLAIM: beat, downbeat, onset and section are different events and drive different visual levels: section changes the visual language (palette, layout, motion type), downbeats carry cuts and impacts, beats and onsets carry micro accents.
- CHECK: `mir-aidj/all-in-one` (allin1): beats, downbeats, functional segments (intro, verse, chorus, bridge), uses source separation; code MIT; model weights licence to confirm. Report rates it P0 to adapt.
- CHECK: `mjhydri/BeatNet-Plus` (CRNN, particle filtering) tracks the pulse in music without clear drums; licence unclear. P1 optional fallback.
- CLAIM: store a confidence per detection; for rubato, live or ambient music fall back to interpolation and manual markers instead of forcing a grid.

## Sung lyrics

- CLAIM: free transcription (Whisper, WhisperX) hallucinates under dense music and does not respect the supplied text; forced alignment with the supplied text is the right method.
- CHECK: `MahmoudAshraf97/ctc-forced-aligner` (CTC with Wav2Vec2 or MMS), code BSD-2, word splitting, Polish via `--language pol` and `--romanize`. CONFLICT for commercial use: the default MMS model is CC-BY-NC 4.0; a commercially usable wav2vec2 model must replace it.
- CONFLICT: the report ranks `stable-ts` P2 because Whisper "changes the approved text". Its `align()` mode takes the supplied text, and Studio's `lyric_timing.py` keeps the user's spelling regardless; recheck stable-ts align accuracy on singing.
- CLAIM: Demucs vocal separation raises alignment confidence but adds artefacts and can shift short unvoiced consonants; overlapping lead and backing vocals defeat single-track aligners, so the timing data must keep manual overrides.

## Direction to music

- CLAIM: avoid "audio-reactive vibrator" literalism (a flash on every syllable, a scale jump on every beat); use counterpoint (a held shot over the densest moment) on purpose.
- CLAIM: the visual apex (contact, peak of the move) should land on the beat, so the move starts before it; smooth audio-driven parameters with attack and release envelopes.
- CLAIM: event timing error target at most 2 frames (about 66 ms at 30 fps); beyond about 70 ms viewers notice. CHECK against ITU-R BT.1359 and perception research.

## Clock and rendering

- CLAIM: frame index = floor(time x fps_num / fps_den); use rational fps (30000/1001) correctly; standardise audio to 48 kHz and video to constant frame rate before composition; do not mix 44.1 and 48 kHz.
- CLAIM: GSAP `lagSmoothing` breaks frame-by-frame determinism; call `gsap.ticker.lagSmoothing(0)` or drive time manually in custom renderers (HyperFrames seeks a paused timeline; confirm it is unaffected).
- CLAIM: for long renders stream audio with HTTP range requests (Remotion `useWindowedAudioData`) to avoid memory leaks.
- CLAIM: keep the music analysis in one versioned JSON (provenance, model versions, manual overrides) that renderers read without recomputing.

## Tools

- CONFLICT: the report calls Motion Canvas inactive and risky; other sources describe it as MIT and usable. CHECK repository activity.
- CLAIM: Remotion plus GSAP is the strongest DOM route; Studio's default in Claude Code is HyperFrames (HTML plus GSAP), which shares the GSAP concerns.

## Formats

- CONFLICT: bottom interface overlay given as 15 to 20 % of a vertical screen, with TikTok's right-hand column from mid-height; industry guides for Meta Reels cite 35 % bottom. Keep the conservative figure until official pages are checked.
- CLAIM: adapt layout per aspect ratio at composition time; never crop a 16:9 film to 9:16.
