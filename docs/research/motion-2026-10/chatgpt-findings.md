# Deep research 2 of 3: ChatGPT Deep Research (findings extracted 2026-10-12)

Source: the owner's packet "FCW_MOTION_KNOWLEDGE_RESEARCH 1.0" (12 files, Polish, 48 sources S01 to S48, 20 repository assessments R01 to R20, a proposed `audio_event_map` sidecar schema 0.1.0, synthetic examples, 18 static checks, a handoff with 10 task cards). It was written against Studio 1.66.1, before 1.70.0 and 1.71.0. Not stored here; extracted claims only. Status labels as in `gemini-findings.md`.

## Timing targets (the packet marks them as design goals, not measured facts)

- CLAIM: key cues within 1 frame of their mark (about 33 ms at 30 fps); audio-video offset within 1 frame; drift at most 5 ms per minute after encoder-offset compensation; designated beat hits within 1 frame, offbeat cues not held to it.
- CONFLICT with Gemini: do not assume a 70 ms perception window; set the evaluation window from a benchmark.
- CLAIM: pilot target for word timing, median error at most 100 ms on a spoken or rap fixture; no automatic threshold for melisma.
- CLAIM: a reveal lands on the accent or 1 to 2 frames before the readable point; a tween may start about 150 ms before a downbeat and reach contact or peak scale on the beat, then settle (agrees with Gemini on hitting the apex, not the start).
- CLAIM: rational frame rates (30000/1001) need an exact mapper; rounding seconds to frames per cue accumulates drift over minutes.
- CLAIM: there is no universal -14 LUFS target; keep it an internal profile and check each platform's current guidance.
- CLAIM: "waveform drives text scale every 16 ms" is a local effect at most, never the direction system.

## Contract and data (P0 decisions in the packet)

- CLAIM: one frame-time source of truth; the approved exact lyric text is never altered by import; raw audio events stay separate from render-safe display captions; overlapping singers are never dropped on import.
- CLAIM: measure timing on the final encoded file, not the preview; block unsupported capabilities and uncertain licences; no silent fallbacks.
- CLAIM: cue arbitration: a beat event cannot interrupt words that must stay readable.
- PROPOSAL: an `audio_event_map` sidecar (source sample time, mapped frames, word spans with original character offsets, cue events with provenance), version 0.1.0, explicitly not a replacement for `motion-score.json`.

## Repositories and licences (as the packet assessed them)

| Repo | Use | Code licence | Weights |
| --- | --- | --- | --- |
| librosa/librosa | optional analysis | BSD-3 (verify) | n/a |
| CPJKU/beat_this | beat and downbeat inference | MIT (verified) | Unknown |
| MTG/essentia | method study only | AGPL-3.0 | n/a |
| m-bain/whisperX | guarded aligner for speech, songs only after tests | Unknown until licence review | separate |
| openai/whisper | recognition only, not final sung timing | | |
| facebookresearch/demucs | optional offline stems, not default | verify | separate |
| nomadkaraoke/python-audio-separator | adapter after a model-rights audit | Unknown | Unknown |
| nomadkaraoke/python-lyrics-transcriber | study its correction and edit representation | MIT | n/a |
| Dinoosauro/music-sync | study a manual timeline interface | Unknown | n/a |
| Vincentwei1021/video-shotcraft | adapt methods and templates by own implementation | Apache-2.0 (bundled media separate) | n/a |
| heygen-com/hyperframes-community-skills | review gate per skill | per skill Unknown | n/a |
| tyiannak/pyAudioAnalysis | method reference for regions | | |
| CPJKU/beat_this_live | observe | | |

CONFLICT: Gemini ranks `allin1` P0 and `ctc-forced-aligner` P0; this packet does not list allin1 or ctc-forced-aligner and prefers `beat_this` for beats and downbeats. Both agree that model weights need their own licence check before any commercial default.

## Work packages proposed (FCWG-001 to FCWG-010)

P0: capability registry and audit; strict sidecar contract and migration; rational sample, seconds and frame mapper; exact lyric integrity with singer layers and manual overrides; cue arbitration and semantic hit targeting; renderer parity, audio mux and export QA. P1: beat, onset and downbeat candidates without automatic trust; singing alignment candidates with a manual editor; platform layout and rights profiles. P2: technique atlas and reference tests.
