# Kinetic film kit

Assets for [kinetic launch films](../../references/kinetic-launch-films.md): teasers, trailers, launch and brand films in huge type on a music beat. They work with any runtime Studio builds in (HyperFrames, the GSAP or frame starters, Remotion) and with any music or sound source: supplied, licensed or generated.

| File | What it is |
| --- | --- |
| [`beat-sheets.json`](beat-sheets.json) | Four structure templates in beats: `teaser-24s` (172 BPM), `trailer-45s` (150), `launch-film-48s` (170), `brand-film-36s` (124). Each block has a job, a Studio scene kind or the custom move to build, a ground, the hit on its first beat and a word budget. The brief supplies every word. |
| [`beat_sheet.py`](beat_sheet.py) | Checks a sheet (starts at beat 0, no gaps or overlaps, ends on the last beat, the drop starts a block), prints each block in seconds at the sheet's or the measured tempo, and with `--drop-seconds` the music offset that lands the track's drop on the planned beat. Python 3.8+, no packages. |
| [`sound-kit.json`](sound-kit.json) | Twelve one-shot cues with length, where each is used and a starting prompt for any sound-effects generator, plus fallbacks and a negative prompt. |

## Use

1. Copy the closest template into the project as `beat-sheet.json`, rename its `id`, then adjust blocks and beats to the brief. Fill the words with the copy owner; numbers come from the user.
2. `python3 beat_sheet.py beat-sheet.json` until it prints no errors; show the table for approval with the copy.
3. Measure the track with [`beats.py`](../motion-sync/README.md#analysing-a-supplied-track), then `python3 beat_sheet.py beat-sheet.json --bpm <measured> --drop-seconds <drop>`: start the music at the printed offset (or cut it with `music_edit.py` so the drop lands on the planned beat). A negative offset means the track drops too early for this sheet.
4. Build each block in the contract (`motion-score.json`) with the named scene kind, or a custom scene for the move. Cue each sound from `sound-kit.json` on its block's first beat and on every cut or typed character inside it.

## From phrase to scene

| Phrase | Scene |
| --- | --- |
| Opening hook, a punchy statement | custom word slam, stack or split; `line-reveal` for calmer films |
| "No X. No Y." | custom strike-through on each word |
| A number | `counter`, `bar-chart` or `line-chart` |
| The input that produces the result (a prompt, a tap) | custom typed line with a caret, ending in a push into the drop |
| A product screen | `device` |
| Key art, a product photo | `photo-hero` with a push, a pan and a punch-in on each word |
| A list of features or services | `item-stagger`, or one phrase per feature |
| A quote | `quote` |
| The name | `logo-reveal`, then `end-card` |

Custom moves (whips, zooms through a letter, 3D extruded titles, cut runs, rewinds) are written in the runtime from the brief; [motion craft](../../references/motion-craft.md) and the [technique atlas](../technique-atlas/README.md) hold their timing.
