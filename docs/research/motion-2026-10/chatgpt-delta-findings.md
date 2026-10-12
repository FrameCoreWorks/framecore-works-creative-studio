# ChatGPT research delta 1.1 against v1.71.0 (findings extracted 2026-10-12)

Source: the owner's "FCW_MOTION_RESEARCH_DELTA_1.1.md", a read-only reconciliation against tag v1.71.0 that checked licences on primary pages (LICENSE files, model cards, maintainer statements), accessed 2026-10-12. Extracted decisions; labels as in the delta.

## Verdicts on the conflicts

- C1 (70 ms): the 0.07 s figure is `mir_eval`'s beat-evaluation window, not a perception law; ITU-R BT.1359 does not set a 70 ms rule for motion hits. Keep one frame as an engineering target for designated cues; report errors in ms and frames; use separate windows for beat F-measure, word alignment and cue targeting.
- C2: Beat This first (beats and downbeats, code and published weights MIT); All-In-One later for sections only, because its default pipeline runs Demucs.
- C3: stable-ts `align()` uses the supplied text (the Gemini claim confuses transcription with alignment) but the repository was archived on 2026-05-30; add a WhisperX known-text adapter with explicitly named, licensed models; block ctc-forced-aligner's default MMS model (CC-BY-NC-4.0).
- C4: neither 15 to 20 % nor 35 % is a cross-platform rule; record placement, paid or organic, check date and overlay source; TikTok publishes downloadable placement safe zones; Meta's page needs login.
- C5: Motion Canvas is usable MIT code with maintenance risk (stable 3.17.2 of 2024-12-14, alpha 3.18.0 of 2025-02-16, documentation change 2026-07-02), not abandoned.

## Licences (code and default weights)

| Project | Code | Default weights | Commercial by default |
| --- | --- | --- | --- |
| mir-aidj/all-in-one | MIT | author checkpoints MIT, but the default pipeline runs Demucs | no (Demucs weights) |
| CPJKU/beat_this | MIT | published weights MIT (training data caveat) | yes |
| ctc-forced-aligner | BSD-2 | MMS default CC-BY-NC-4.0 | no |
| m-bain/whisperX | BSD-2 | per language; Polish `jonatasgrosman/wav2vec2-large-xlsr-53-polish` Apache-2.0; Whisper large-v3 Apache-2.0 | yes for that named combination |
| jianfch/stable-ts | MIT (archived 2026-05-30) | Whisper large-v3 Apache-2.0 when named | yes for a named model |
| facebookresearch/demucs | MIT (archived 2025-01-01) | pretrained weights for scientific use only (maintainer, issue 327) | no |

Defect in 1.71.0: the motion-sync README recommends `python3 -m demucs` for vocal separation without the weights caveat, and the compendium mentions vocal separation the same way.

## Change requests for lyric_timing.py (LT-01 to LT-06)

- LT-01: explicit `--aligner` and model options, no silent fallback, licence status recorded; WhisperX must align the approved lyric text, not its own transcription.
- LT-02: verbatim lyric ledger with character offsets, line and occurrence IDs, singer IDs, manual overrides that win and are never re-estimated.
- LT-03: statuses per word (observed, interpolated, manual, unresolved); no interpolation across invalid anchors; character length is not sung length.
- LT-04: beat events from a provider (bundled, Beat This, manual) instead of one global BPM; `--snap-policy`; never shift word times to hit the grid.
- LT-05: rational fps (`Fraction`) from absolute sample times; 30000/1001 regression.
- LT-06: versioned output, explicit blocked or lossy statuses, regression fixtures P01 to P10 (bilingual diacritics, repeated chorus, duet, melisma, rap, initial silence, rubato, 30000/1001, locked lyric with a wrong ASR word, offline without models).
