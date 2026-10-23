---
name: earshot
description: Hear sound you cannot hear, locally. Use before saying how audio sounds or fits; to choose, trim, compare or verify sound effects, music or ambience; to check a soundtrack or a video's audio against its picture (sync, loudness, mix, a launch-film scorecard); to render a film's sound effects on cue frames from a bank of 252 code-made sounds (sfx, kit, the launch preset), make or fit a sound in code (forge, fit), or build a full soundtrack from real licensed recordings (the real-sound process). Earshot runs on the user's machine; nothing is uploaded.
---

# Earshot: ears and a sound kit for an agent

You cannot hear. Never say how a sound sounds or that it fits without an Earshot reading behind it, and quote the
number ("strong match, z +3.9", "p_real 0.96", "-14.2 LUFS"). Earshot 0.4.0 by Leon Lin (MIT) runs on the user's
machine on CPU; this plugin installs it from one pinned commit and keeps every run local.

`<runtime>` below is this plugin's `scripts/runtime.py`, two folders above this file (`../../scripts/runtime.py`,
not inside this skill folder); `<skill>` is this folder's `real-sound` subfolder. Resolve both
from where the host installed this skill; never copy a path from another machine.

## 1. Readiness and consent (always first)

1. `python3 <runtime> status --json`. Four facts, kept apart: the skill is readable; `light_ready` (no models:
   measure, critique --fast, sfx, kit and the real-sound scripts); `full_ready` with `models_cached` (timeline,
   sheet, describe, match, rank, find, compare, ab, realness, full critique); a task actually completed. `unavailable`
   means not installed here, not "probably works".
2. Missing tier: say in one line what will be written and its size, then install only after the user agrees:
   `python3 <runtime> install --tier light` prints the plan; `--yes` runs it (about 200 MB). Full: `--tier full --yes`
   (about 1.5 GB) and `python3 <runtime> fetch-models --yes` (pinned CLAP and AST, about 1.1 GB). The source is the
   pinned commit, checked file by file; the engine is never updated from upstream `main`.
3. No shell or code execution in this host: give the plan, the exact commands and what each would prove; never
   report a reading that did not run.
4. Ask at most one question per reply: the one that changes the route (own recordings or a search, which film or
   file). Take sensible defaults for the rest (how the sound should feel, its room, its length), say them in one
   line, and let the user correct them.

## 2. Running it

- One command: `python3 <runtime> run <command> ... [--json]`. Allowed: `measure describe match rank find compare ab
  realness timeline sheet critique profile forge fit sfx kit gallery doctor`. Runs are offline.
- Many readings in one task: models take 20-40 s to load per process, so write one short script and run it with
  `python3 <runtime> exec -I my_script.py` (`from earshot import api`, then `api.find(...)`, `api.realness(...)`).
  `exec` is the venv interpreter with the plugin's offline model cache; never call the venv's python directly, which
  would miss that cache and could download the models again.
- Not in this plugin: `llm` (uploads audio to Gemini) and `mcp` (a server). The launcher refuses them, and the
  installation replaces both modules in the engine with a stub that raises an error, so the upload cannot run from Python
  either; API keys are not passed to the engine. `doctor --fetch` is refused too (use `fetch-models`). If someone asks
  for an audio-LLM opinion, say it would upload the audio and offer the local readings instead.
- Errors are one line on stderr with exit 1; a refusal is exit 2.

## 3. Listening

**Choose an asset.** `rank "<description>" <folder> --top 5` shortlists; `find <file> "<one clean hit>" --top 3`
returns trims (a `stroke` or `event` starts 5 ms before the attack; never use a trim marked head cut or tail cut);
`describe <file> --start s --end e` says what the trim sounds like (AudioSet is weak on one-shots under 0.5 s: only
an outright different class such as Speech or Engine is a red flag); `realness` on the exact trim you will use (a
gate only when the user wants real or produced sound; clean professional synthesis also reads as synthesized); `ab
a b --query "..."` with trims to decide between two; `match <file> "<claim>" --alts ...` to test one claim;
`compare <file> --refs <folder>` for palette fit.

**Review a mix or a film.** With the light tier only, check sync from measured onsets: `kit.lock.json`, or onsets
measured in the encoded film's audio against the cue frames, and say `timeline` and `sheet` need the full tier.
With the full tier: `timeline film.mp4 --cues cues.json`: events, sections, loudness, picture cuts and sync
per cut and cue (offset_ms = sound minus picture; trust it only above the printed chance level). `sheet film.mp4 -o
sheet.png --cues cues.json`, then open the PNG: green within a frame, amber within 100 ms, red silent. `critique
film.mp4`: a scorecard against seven professional launch films with timed fixes (a range, not a target; music-led
or speech-led films need a `profile` built from references the user chooses). `measure` for exact LUFS, true peak,
LRA, bands, onsets, tempo and key.

**A review in words.** When the user wants an opinion on a mix or a film ("what sounds cheap", "is it ready"), write it
yourself from local readings: `timeline`, the opened `sheet` PNG, `critique`, `measure` and `describe` or `realness` on
the sounds you judge, then sync, realism, mix, loudness and the cheap tells, each tied to a number, and fixes by
impact. Say it is a review written from readings, not a listening test. Steps and criteria:
`references/written-critique.md`. This replaces upstream's upload to a hosted model: free, no key, nothing leaves the
machine.

**A/B a change.** `ab before.wav after.wav --query "..."` or `--refs`, with trims for multi-take files, then
`timeline` again. Change one thing at a time.

**Reading the numbers.** Measurements (LUFS, dBTP, ms, Hz) are exact. z verdicts: 3 or more strong, 2.5-3
plausible, 2-2.5 weak, under 2 no match; try two or three phrasings when it is borderline. Cosine is never a
confidence. p_real is evidence, not proof, with different thresholds for clips up to 6 s and longer files. Write
queries as source + material + action + character ("a heavy wooden door slamming in a small room"), with realistic
confusions as alternatives.

## 4. Making sound

**A film's effects from the bank (no models).** `kit init --preset launch -o audio/kit.json` for films cut to music
(also `calm` text-led, `crisp` energetic product, `minimal` effects-only). `sfx list --category ui_pop` (0.4 families:
ui_pop, knock, cut_hit, mallet, drip, shutter, reverse_swell, plus new whoosh, riser, swish, glitch and notify
members) and `sfx render <id> -o x.wav --dur 0.8 --apex 0.32` to audition with measured onset, peak and end. Then
`kit render audio/kit.json --out audio/kit` and `kit check audio/kit.json --out audio/kit`; replace a warned take
instead of keeping it. `kit.lock.json` carries each take's measured onset, peak, end and loudness: place hits and
touches by onset, a whoosh by its peak, a riser by its peak or end as its role says. With a music bed, set each
effect against the bed (`kit.bed_level`, `kit.gain_db`, `kit.place`, `kit.space_run` in Python), pull the music down
6-12 dB for 0.3-0.5 s before a big hit and bring it back on it, and report the gains and bed levels. These sounds are
made in code (15 fitted from CC0 recordings with credits); when the brief asks for recorded sound, use section 5.

**Make or fit a sound in code.** `forge <recipe> --refs <real refs> --budget 144 --reps 2 --tone 1.5 --keep 4
--robust 8 --dir <round>` improves a code recipe by listening; `fit <recording> -o recipe.py` turns a recording into
a recipe with knobs. Say plainly that the search satisfies Earshot's own models: judge by the model-free tone
words, robust re-renders and spectrograms, and ask for a blind human test before calling a made sound as good as
real.

## 5. A soundtrack from real recordings (real-sound)

Follow `<skill>/references/process.md` and the prompt briefs in `<skill>/templates/prompts/`. In those files
`{{PY}}` means `python3 <runtime> exec`: fill it in that way, also in briefs handed to other agents, so every
script and every `-m earshot <command>` runs offline from the plugin's cache and through the allowlist.

Steps: cue list from the picture (`templates/cues.json`), brief (`templates/SOUND_BRIEF.md`), recordings, licence
audit, music edit at bar lines (`arrange.py`), design fragments, integrate and QA (`mix.py`, `qa.py --layers`,
`--listen`), five critics and one fixer (`variant.py`), master (-14 LUFS, true peak at most -1.5 dBTP), credits
(`credits.py`), mux (`node <skill>/scripts/mux.mjs`).

**Recordings.** By default use the user's own recordings and the bank. Search and download from Freesound, Mixkit or
Pixabay only when the user asks or accepts that proposal; then download politely and sequentially, record every
file in its manifest, run `audit.py` (policy in `licences.py`, `references/licences.md`; CC0, public domain, CC BY,
Mixkit and Pixabay allowed; NC, ND, SA, Sampling+ and unverified blocked) and `credits.py`, and never commit or
publish downloaded recordings. `audit.py --fetch` re-reads licence pages and is part of that same consent. Nothing is
ever uploaded.

## 6. Handing results to Studio or another owner

Return, for each result: the engine that produced it (this plugin, a pinned Earshot command line, or another tool),
the commands run, WAV paths with SHA-256, `kit.lock.json`, measured onset, peak and end, the readings with their
numbers, and what was not run. FrameCut (or the project's editor) keeps the master timeline: convert a zero-based
frame as `frame * fps_den / fps_num` seconds and place a take at `round(t * rate) - round(anchor * rate)` samples;
Earshot 0.4.0 reads a numeric fps in cue files, so pass seconds with rational FPS kept in the project. The project's
owner keeps the brief, approvals and final review. Details: `references/studio-handoff.md`.

## 7. Limits (say them when they matter)

Taste is not measured: Earshot says what a sound is and how it measures, not whether it is right for the story. No
speech recognition. CLAP hears about 50 Hz to 14 kHz and AST up to 8 kHz. Picture cuts come from a frame-difference
detector: pass cues for animation. Model scores never prove a licence or where a recording came from. Upstream's
full listening workflows: `references/listening.md`.
