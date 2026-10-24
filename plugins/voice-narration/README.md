# Voice And Narration

A plugin beside FrameCore Works Creative Studio that turns an approved script into voice-over files measured against each scene's time.

- **Engines:** VoxCPM2 (installed by the plugin into its own environment, only after you agree) and Voicebox (the desktop app you install) run on your own computer. ElevenLabs runs in the cloud through your app's ElevenLabs connector; no API key is stored.
- **Where:** local engines belong on your own computer (Claude Code or Codex on a desktop or laptop, Claude Desktop). In a phone app or a cloud session the plugin advises against installing them and offers ElevenLabs or a script with voice direction instead.
- **What you get:** one WAV per line, a per-project pronunciation lexicon, a measurement against each line's limit, and `narration.lock.json` for FrameCut or Motion Graphics Workflow.
- **Rules:** nothing is installed, downloaded or paid for without your yes; a voice is cloned only with its owner's recorded consent.

The skill is `voice-narration:narrate`; the launcher is `scripts/runtime.py` (`status`, `install voxcpm`, `fetch-models`, `generate`, `measure`, `stretch`). Install it from this repository's marketplace next to Studio.
