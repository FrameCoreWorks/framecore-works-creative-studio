---
name: narrate
description: Make a voice-over, narration or read of an approved script ("lektor", TTS, read my script) and check that each line fits its scene's time. Runs VoxCPM2 or Voicebox on the user's own computer, or ElevenLabs through the app's connector; applies the project's pronunciation lexicon, measures every take against its limit and hands WAV files and narration.lock.json to FrameCut or Motion Graphics Workflow. Nothing is installed, downloaded, cloned or paid for without the user's yes. Script writing goes to Copy Voice.
---

# Voice And Narration

Turn an approved script into one measured WAV per line. The words come from Copy Voice with their locked facts; the
timing limits come from the board plan or the FrameCut timeline. This skill picks and runs the engine, applies the
pronunciation lexicon, measures each take and hands the files to the mix. It never rewrites the script itself.

`<runtime>` below is this plugin's `scripts/runtime.py`, two folders above this file (`../../scripts/runtime.py`).
Resolve it from where the host installed this skill; never copy a path from another machine. Formats of the cue
sheet, lexicon and lock file: `references/formats.md`.

## 1. Readiness first

Run `python3 <runtime> status --json` before promising anything. Keep the facts apart: this skill is readable;
`voxcpm_version` installed; `weights_cached`; `voicebox` ready; a read actually generated and measured. `unavailable`
means not here, not "probably works". No shell in this host: give the cue sheet, the voice direction and the exact
commands instead, and never report a take that did not run.

## 2. Where local engines run

VoxCPM2 and Voicebox are for the user's own computer: Claude Code or Codex on a desktop or laptop, or Claude Desktop
with Voicebox installed. Their packages and weights are several GB and need a persistent disk and a GPU (VoxCPM2
about 8 GB of VRAM).

When `status` says `"environment": "cloud"`, or the user is in a phone app, a web session, Codex cloud or ChatGPT
Work: advise against installing them and say why in one line (several GB on a temporary disk, usually no GPU, lost
with the session). Offer ElevenLabs through the connector, or the script with voice direction for the user to record
or generate on their own computer. Install there only if the user insists after that warning, with `--allow-cloud`.
Voicebox can never be reached from a cloud environment: its API listens only on the user's own computer.

## 3. Choose the engine

Ask once, when the user has not said: VoxCPM2 (clean 48 kHz sound for paid ads and client voice-overs, Apache-2.0),
Voicebox (a desktop app with several engines inside, no code), or ElevenLabs (cloud, the user's own account and
credits). When the user does not know, describe these three in their language and recommend one for their need and
computer. A user who already uses one keeps it. Never switch engine silently: when the chosen one is not ready, say
so and offer another route.

## 4. Install only with consent

- VoxCPM2: `python3 <runtime> install voxcpm` prints the plan (pinned `voxcpm==2.0.3`, about 3 GB, its own
  environment); run it with `--yes` only after the user agrees. Weights are a second consent:
  `python3 <runtime> fetch-models` prints the plan (about 5 GB from huggingface.co), then `--yes`.
- Voicebox: the user installs the app from its release page; then `status` shows it ready.
- ElevenLabs: the user connects the ElevenLabs connector in their app. No API key is stored or asked for.

## 5. Consent for a voice

Clone a voice only with its owner's recorded permission (the user's own voice, or a speaker who agreed in writing).
Pass that record with `--consent "<who agreed, how, when>"` next to `--reference-wav`; the launcher refuses a clone
without it, and the lock file keeps it. Never imitate a real person, a celebrity or a client's competitor. Mark a
synthetic voice where the platform or the law asks.

## 6. Generate

Prepare `cues.json` (one line per scene, with `max_seconds`) and the project's `lexicon.json` (the project's own words:
brand names, people, numbers read aloud). Keep one lexicon per project; never reuse one client's lexicon for another.

- VoxCPM2: `python3 <runtime> generate --engine voxcpm --cues cues.json --lexicon lexicon.json --out takes/`. A voice
  description goes at the start of a line's text in parentheses, for example `(calm, warm male voice)`.
- Voicebox: `python3 <runtime> generate --engine voicebox --profile <profile id> --language pl --cues cues.json
  --lexicon lexicon.json --out takes/`.
- ElevenLabs: follow `references/elevenlabs-connector.md`. Price the run first, ask before spending credits, name
  the chosen voice, and never retry a generation automatically: each attempt costs credits.

A failed line is recorded as failed and the others are kept. Fix the cause, then regenerate only that line with
`--only <id>`. Errors are one line on stderr with exit 1; a refusal is exit 2.

## 7. Measure and fit

Run `python3 <runtime> measure --cues cues.json --out takes/` after every generation (generate also prints it).
Each line reads `fits`, `over` (with seconds over), `silent`, `missing` or `unreadable`. For a line that is over,
change nothing yourself; offer the user, in this order:

1. shorten the text through Copy Voice, keeping its locked facts;
2. regenerate that line at a faster pace (a pace note in the voice description, or the engine's pace setting);
3. a speed-up of at most 5%: `python3 <runtime> stretch <id> --percent N --cues cues.json --out takes/` prints the
   plan, and `--yes` runs it only after the user agrees (needs FFmpeg).

## 8. Check the pronunciation

A person listens to every take, always; say which names and numbers to listen for. Automatic transcription through
the ElevenLabs connector is optional and needs its own consent, because it uploads the audio and spends credits.
A wrong word goes into the lexicon, then `--only` regenerates that line.

## 9. Hand off

Deliver the WAV files and `narration.lock.json` (engine, model, version, voice source and consent, the text actually
sent, duration, limit, verdict, any stretch, SHA-256, lexicon hash). FrameCut keeps the master timeline; in a motion
film Motion Graphics Workflow's sound step mixes them. Studio keeps the brief, the copy locks and the final review.
Name the engine that produced every take.
