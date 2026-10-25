# Prompt records

One structured planning record per image or video, checked and compiled for the generator that will run it. The record is Studio's own planning object, never a model's API; what reaches a generator is its own form. Why and when: [structured image prompts](../../../image-prompt-architect/references/structured-image-prompts.md) and [structured video prompts](../../../video-prompt-architect/references/structured-video-prompts.md).

```sh
python3 prompt_record.py example image > poster.json      # a filled example to edit
python3 prompt_record.py check poster.json                # errors (exit 1) and warnings
python3 prompt_record.py compile poster.json --to ideogram   # Ideogram 4.x native JSON
python3 prompt_record.py compile poster.json --to flux2      # the FLUX.2 JSON template
python3 prompt_record.py compile poster.json --to prose      # ordered prose for every other image model
python3 prompt_record.py compile film.json --to kling        # Kling custom multi-shot request fields
python3 prompt_record.py compile film.json --to sora         # Sora headed blocks
python3 prompt_record.py compile film.json --to timestamps   # prose with [00:00-00:04] segments (Veo, Runway, Wan)
python3 prompt_record.py compile film.json --to prose        # one paragraph (LTX and as a neutral form)
```

- **Image checks:** a summary, exact text in `text[]`, Ideogram's `bbox` scale and colour limits, `photo` and `art_style` not together, settings kept out of the prose, a FLUX.2 warning for an avoid list, an edit with its change and a short preserve clause.
- **Video checks:** shots that start at 0 and touch without gaps, durations that sum to `settings.duration_s`, one camera move per shot, speakers defined in `subjects[]`, dialogue short enough for the shot (more than three words per second warns), negative wording in actions, settings kept out of the prose, and Kling's limits (at most 6 shots, each at least 1 s, 3 to 15 s in all).
- `compile` refuses a record with errors and prints warnings to stderr. Other generators' notations (Seedance braces and brackets, MiniMax camera brackets, Bria FIBO's schema) are written by hand from the cards.

Standard library only; nothing is sent anywhere. Field names follow the makers' documentation read on 2026-10-25; Kling's multi-shot `duration` per shot is written as an integer like the request's own `duration` (the per-shot type was not stated on the page read). Tests: `tests/prompt_record_test.py`.
