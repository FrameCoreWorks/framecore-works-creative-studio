# Changelog

## 1.0.1 (2026-10-24)

- Final-review minors: a silent take now fails `generate` (exit 1, `silent: <id>`); `stretch` checks the source and FFmpeg before printing its plan; FFmpeg errors read as plain text; an unreadable WAV is reported as `unreadable` instead of a traceback; a leading space before a `(voice description)` keeps it protected; lexicon keys that differ only in case are refused; subprocess output is decoded as UTF-8 with replacement (Windows). Not changed by decision: only `voxcpm` is pinned (its own dependencies, PyTorch included, follow its release), and `status` reports `cloud` or `local` because no reliable signal for an unknown environment exists.

## 1.0.0 (2026-10-24)

- First release: the `narrate` skill and `scripts/runtime.py` for VoxCPM2 and Voicebox on the user's own computer and ElevenLabs through the host connector, with a pronunciation lexicon, per-line measurement, bounded stretch and `narration.lock.json`.
