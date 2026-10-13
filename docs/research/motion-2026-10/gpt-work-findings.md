# GPT Work research packet FCW-MOTION-KNOWLEDGE-RESEARCH-01 (findings extracted 2026-10-13)

Source: the owner's ZIP `FCW-MOTION-KNOWLEDGE-RESEARCH-01` (version 1.0.0-research, dated 2026-10-12, Polish): a compendium of fifteen chapters, a pinned shortlist of 20 repositories, four synthetic case studies, a proposed `motion-sync` sidecar schema 0.1.0 with an example, 14 QA decision cards and an implementation handoff H01 to H14. It read `lyric_timing.py` and `motion-compendium.md` at `1a30607` (1.71.0) and the rest of Studio at a 1.66.1 snapshot. It ran no code, models, renders or listening tests; its claims about Studio code were static readings to be reproduced. The packet itself is not stored in the repository.

## Reproduced and fixed (the trigger for this change)

| Claim in the packet | Reproduction on 1.71.0 | Fix |
| --- | --- | --- |
| A line sung from 0 s gets a negative board cut | `snap` with `beat0` 0.1 gave cut -0.033 s, frame -1; with `beat0` 0.2 it snapped to -0.05 s, frame -2 | the wanted cut is clamped at 0 and a half-beat below 0 is never chosen |
| Interpolation inverts when heard neighbours overlap | heard "aa" 1.0-1.6 and "cc" 1.5-2.0 gave the missing "bb" start 1.6, end 1.5 | the gap closes to zero length instead of inverting, and the line is listed for a check by ear (`needs_check`) |
| `--fps` is an integer, so 30000/1001 is impossible | `type=int` | `--fps` takes a fraction (`30000/1001`); the report records it as text |

Tests: `tests/lyric_timing_test.py` gained three cases (zero start, overlap, NTSC rate); the first two fail on the 1.71.0 code and pass after the fix.

Text corrections in `skills/hyperframes-workflow/references/motion-compendium.md`, which the packet called over-categorical: "forced alignment beats free transcription" now says why known words are aligned and that a full master can align better than a stem (compare both on an excerpt); "no linear moves except constant drifts" now keeps linear motion for mechanical or constant motion by design. The motion-sync README now says that `matched` means the recogniser heard the word, not that its time was verified.

## Checked and already in order

- Meta Reels margins (14/35/6 %): the compendium already calls them a conservative default, not Meta's rule.
- Demucs weights and the WhisperX path: covered by the 1.72.0 caveats from the ChatGPT delta.
- No Studio text recommends madmom models, MMS or other non-commercial weights.
- `beatFrames` in `motion-scenes.mjs` counts beats from absolute time, as the packet recommends keeping.

## Not taken (maintenance mode: no defect seen in use)

These are design proposals without a defect seen in real use; they go to the owner as one-line notes, not as work.

- H02/LT-02: per-word `timestamp_origin` and a verbatim lyric ledger with character spans, occurrence IDs and append-only manual overrides.
- H03: one shared rational clock module for `sync.mjs`, `music_edit.py` (still integer `--fps`) and `lyric_timing.py`.
- H04: the `motion-sync` sidecar schema with a loss report; it is a proposal, not the current score contract.
- H05: fixtures F01 to F14 with independent gold annotations (singing, duet, rubato, 30000/1001 drift).
- H06/H08: optional Beat This and librosa adapters, explicit `--aligner` choice without silent fallback.
- H07: cue `target_phase` and computed pre-roll (contact, apex, reveal, readable).
- H09 to H11: deterministic seek checks, OTIO/ASS/MIDI interchange with loss reports, a waveform marker editor.
- H13/H14: Polish singing and section-label pilots; need licensed data and a benchmark first.
- The memory of `align` grows with lyric words times heard words; measure on a full song before changing it.
