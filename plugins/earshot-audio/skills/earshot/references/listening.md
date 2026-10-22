# Listening workflows in full

Restated from upstream Earshot 0.4.0 for this plugin. Run every command as `python3 <runtime> run <command> ...`.

## Choosing an asset

1. `rank "<description>" <folder> --top 5`: a shortlist from candidate files.
2. `find <winner> "<one clean instance>" --top 3`: the best moments as trims. `stroke` = one onset until it decays;
   `event` = strokes that belong together (a key's press and release), both starting 5 ms before the attack;
   `window` = a plain stretch for beds. `head` and `tail` say how loud the first 5 ms and the last 10 ms are against the
   trim's peak (-30 dB or lower is clean). `--kind event` or `--kind texture` forces one kind.
3. `describe <winner> --start s --end e`: tags with z, AudioSet classes, attack and decay. One-shots under 0.5 s read
   weakly in AudioSet; only a clearly different class is a warning.
4. `realness <winner> --start s --end e`: on the trim you will use, not the whole multi-take file. Clips up to 6 s use
   thresholds 0.17 / 0.77; longer files the mean of 4 s windows with 0.40 / 0.77. Exact digital zeros alone prove
   nothing.
5. `ab a b --query "..."` with `--a-start --a-end --b-start --b-end` to decide; `match <file> "<claim>" --alts ...` to
   test one claim; `compare <file> --refs <folder>` for palette fit (typicality z at least -1 fits, under -2 is an
   outlier).

## Reviewing a mix or a film

1. `timeline <film or wav> [--video film.mp4] --cues cues.json [--detail low|high]`: events with time, level and
   tag, sections, loudness, beats, picture cuts and sync. Only sync above the printed chance level means anything; a
   cut with no listed hit may still carry a soft whoosh: check the sheet.
2. `sheet <film> -o sheet.png --cues cues.json [--from s --to s]`: open the PNG.
3. `critique <film> [--fast]`: metrics against seven professional launch films (verdict launch-grade, close, needs
   work, not launch-grade) with timed fixes; build a `profile` from the user's own references for other genres.
4. `measure <file> [--music]`: LUFS, true peak, LRA, floor, attack and decay, brightness, bands, tempo and key.

## Numbers

| number | meaning | trust |
| --- | --- | --- |
| LUFS, dBTP, LRA, ms, Hz | measurements | exact |
| z | how a description stands out among a few hundred scored on the same sound | 3+ strong, 2.5-3 plausible, 2-2.5 weak, <2 none |
| p_vs_alts | forced choice among your wordings | only which wording fits best |
| cosine | raw similarity | never a confidence |
| AudioSet (0..1) | per-class tagger probability, up to 8 kHz | broad classes |
| p_real | real or produced vs code-synthesized | evidence, not proof |

## Forge, honestly

The search optimises Earshot's own models: a made sound can out-score real recordings while still sounding wrong.
p_real is easy to fool and typicality rewards the average. Judge by the model-free tone words (bands outside every
reference, tails, lengths), robust re-renders and spectrograms, and ask for a blind, loudness-matched human test before
calling a made sound as good as real.
