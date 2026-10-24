# Creative Studio 1.128.0

A new companion plugin, Voice And Narration, makes and measures voice-overs.

## What changed

The separate `voice-narration` plugin (install it from this repository's marketplace next to Studio) takes an approved script with a time limit per line and returns one WAV per line. It runs VoxCPM2 or Voicebox on your own computer, or ElevenLabs through your app's ElevenLabs connector. It applies the project's pronunciation lexicon, measures each take against its limit, and writes `narration.lock.json` for FrameCut or Motion Graphics. Nothing is installed, downloaded, cloned or paid for without your yes. In a cloud session or a phone app it advises against the local engines and offers ElevenLabs or a script handoff. Studio's extension registry lists it, and Audio Production Director's voice engine guide points to it.

## What did not change

Studio's skills, startup, routing, names and paths are unchanged.

## Verification limits

The plugin's 48 launcher tests and 6 package tests and Studio's checks passed. Status and the cloud install refusal were checked in a Claude Code cloud container. Real VoxCPM2 and Voicebox generation, an ElevenLabs read, and fresh ChatGPT, Work, Claude and Codex clients were not run for this release.
