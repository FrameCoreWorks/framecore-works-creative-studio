# Earshot Audio

A plugin that gives an AI agent ears and a sound kit, built on [Earshot](https://github.com/Leonxlnx/earshot) by
Leon Lin (MIT). It listens to and measures sound (what a file sounds like, how well it fits a description, the best
moment in a long take, real or synthesized, a second-by-second listening transcript of a film, an annotated sheet, a
launch-film scorecard), renders a film's sound effects on cue frames from a bank of 252 code-made sounds, makes and
fits sounds in code, and builds full soundtracks from real licensed recordings.

It works on its own and next to FrameCore Works Creative Studio, which hands it sound work and keeps the brief,
approvals and final review.

- **Local only.** The engine runs on the user's machine on CPU. Nothing is uploaded; upstream's audio-LLM command and
  MCP server are not part of this plugin.
- **Pinned and checked.** `scripts/runtime.py` installs Earshot v0.4.0 from commit `591fa3e` into
  `~/.framecore-studio/extensions/earshot`, after checking every upstream file against `upstream.json`, and only after
  the user agrees. Models (about 1.1 GB) are a separate, agreed step.
- **Recordings on request.** Downloads from Freesound, Mixkit or Pixabay happen only when the user asks, with
  upstream's licence audit and credits.

Needs Python 3.10+, FFmpeg and FFprobe, and Node for the final mux. Installation with Claude Code follows
[CLAUDE_INSTALL.md](../../CLAUDE_INSTALL.md); the plugin is listed in this repository's marketplace as
`earshot-audio`.
