# Changelog

## 1.0.4, 2026-10-23

Owner report after listening: the landing hit taken from a kit preset had a metallic debris tail. Every effect is now
chosen by listening: a description from the picture and the request, candidates ranked, the pick matched against
likely confusions (metal, rattle, clang), onsets per second and speaker-audible bands measured, and the readings and
rejected candidates reported. A preset's take is a starting point, not a choice.

## 1.0.3, 2026-10-23

Owner decision (option A), after a ChatGPT Work run that found the engine missing and made the sound with
FrameCore Works Creative Studio's own engine without asking: when the engine is missing and the project has its own
sound tools, the readiness question offers both routes (install the light tier, or the project's tools now), runs
neither before the answer, and names the engine that made the sound.

## 1.0.2, 2026-10-23

Defect found in an end-to-end run (Studio, Superpowers and this plugin in Claude Code, light tier): `timeline` and
`sheet` stopped on the missing CLAP model, while the skill listed them as light-tier commands. The skill now lists
measure, critique --fast, sfx, kit and the real-sound scripts as light, moves timeline and sheet to the full tier, and
says how to check sync on the light tier (measured onsets against the cue frames). It also says where `runtime.py`
is (`../../scripts/runtime.py`); the run looked for it inside the skill folder first.

## 1.0.1, 2026-10-23

Owner decision: a free, key-free replacement for upstream's Gemini upload. The skill now writes a review in words
from local readings (timeline, the sheet image, critique, measure, describe and realness), judging sync, realism, mix,
loudness and the cheap tells with each point tied to a number, and says it is not a listening test; steps and criteria
in `references/written-critique.md`. Nothing leaves the machine.

## 1.0.0, 2026-10-22

First public release, at the owner's request: Earshot for every user of this repository's marketplace, built from
upstream `main` (v0.4.0, commit `591fa3e`). Upstream's `earshot` and `real-sound` skills merged into one skill,
`earshot-audio:earshot`; real-sound's scripts, references and templates copied byte for byte; a standard-library
launcher with consented, file-checked installation and an allowlist of local commands (`llm` and `mcp` refused).
Replaces the owner's private ChatGPT adapter (0.1.0, Earshot 0.3.0) as the source.
