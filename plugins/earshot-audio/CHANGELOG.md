# Changelog

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
