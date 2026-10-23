# A review in words from local readings

Upstream Earshot can send a mix to a hosted audio model for a second opinion in words. This plugin does the same job
locally: you, the agent already in the conversation, write the review from Earshot's own readings. It is free, needs no
key and nothing leaves the user's machine. You did not hear the sound: every statement rests on a reading you ran, and
you say which.

## 1. Gather the evidence (one script or a few runs)

Run through `python3 <runtime> run ...` (or one `exec` script on `earshot.api`):

1. `timeline <film or mix> [--video film.mp4] --cues cues.json --detail high --json`: events with time, level and
   tag, sections, loudness curve, beat grid, sync per cut and cue with the chance level.
2. `sheet <film or mix> -o sheet.png --cues cues.json`: open the PNG and look at it (frames, sections, labelled events,
   spectrogram, waveform, loudness, sync markers). Zoom a busy stretch with `--from s --to s`.
3. `critique <film or mix> [--video film.mp4] --json`: the scorecard against seven professional launch films, or a
   `profile` the user built for another genre.
4. `measure <file> [--music]`: LUFS, true peak, LRA, noise floor, bands.
5. For any sound you will judge by character: `describe <file> --start s --end e` on that trim, `realness` when real
   versus synthesized matters, and `ab` between a sound and a candidate replacement.

Without the full tier, steps 1 to 4 still run without tags; say that `describe`, `realness` and the tagged events were
not available.

## 2. Write the review

Judge the film or stem as a senior re-recording mixer would, bluntly, praising only what the readings support:

- **sync**: hits, whooshes and accents against the cues and cuts (offset in ms, early or late, only where above the
  chance level); cuts or cues with no sound when the picture needs one, checked on the sheet before calling them silent.
- **realism**: which sounds `describe` and `realness` read as recorded, which as code-made, and whether that suits the
  brief; synthesis is a flaw only where a sound is meant to read as recorded.
- **mix**: masking (two events stacked in the same bands on the sheet), pile-ups, gaps, the music against the effects
  and voice, the stop-down before the big hit.
- **loudness**: integrated LUFS, true peak, LRA against the target and the critique ranges; the loudest moment and
  where it falls.
- **what sounds cheap**: the measurable tells (identical repeats, pure tones where texture is wanted, plain noise
  whooshes, tails cut off, clicks, a riser stacked on a drop), each tied to a reading.

Then list fixes in order of impact, each with its time, what to change and the reading that will show it worked.

## 3. Report it honestly

Start with one line that says this is a review written from Earshot's readings, not a measurement and not a listening
test. Quote the numbers. Mark anything inferred from the sheet rather than measured. Name what was not run. Taste is
the user's: give the evidence and a clear recommendation, and ask them to listen to the changed passages. Verify each
fix after it is made with `timeline` and `ab` on the same stretch.

## Why not an upload

Upstream's audio-LLM command sends a mono 64 kbps copy to Google Gemini and needs the user's own API key. It is outside
this plugin: the launcher refuses it and the installed engine has it removed. The review above covers sync, mix and
loudness from measurements at least as well; character judgements rest on the local models (`describe`, `realness`)
instead of a hosted listener.
