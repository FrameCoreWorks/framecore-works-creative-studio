# earshot-audio: a public plugin beside Studio

Date: 2026-10-22. Status: approved in conversation section by section; this spec awaits the owner's review.

## Intent

The owner wants Earshot available to every Studio user, not only in their private ChatGPT plugin, and built out from the original repository rather than a thin adapter: "merge them and make earshot new plugin from repo master". Success: a user of Claude Code (and later Codex and ChatGPT) installs `earshot-audio` from this repository's marketplace next to Studio, and Studio's sound work uses it with honest evidence, locally, without MCP or Gemini.

Owner decisions in this conversation:

- One new plugin built from upstream `main`, merging upstream's two skills (`earshot` and `real-sound`) into one entry skill.
- Engine installed from a pinned upstream commit into an isolated environment, not bundled.
- Recordings from the internet (Freesound, Mixkit, Pixabay) only when the user asks or accepts, with upstream's licence checks.
- From the Earshot handover (2026-10-22): local CLI and Python only; no MCP server, no Gemini or other audio-LLM upload.

## Upstream

- Repository: <https://github.com/Leonxlnx/earshot>, MIT, Copyright (c) 2026 Leon Lin.
- Pin: tag `v0.4.0`, commit `591fa3e028032e6dce56620a20e932e35667e8d8`, tree `d6f2dbc43f7b38b2147cfd04bbd7aa9055701f1a`, 282 tracked files, `requires-python >=3.10`. Released 2026-10-22: bank 0.4 (252 sounds), the `launch` kit preset mixed against the music bed, the rebuilt `fit`, no new dependencies. The earlier review pinned 0.3.0 (`925ebe5`).
- Upstream skills: `skills/earshot/SKILL.md` (listening, forge, sfx, kit; documents MCP and `llm`) and `skills/real-sound/` (SKILL.md, five references, ten scripts, templates and ten prompt templates, 396 KB).

## Structure

New plugin directory `plugins/earshot-audio/`, listed in `.claude-plugin/marketplace.json` beside Studio, with `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` and `plugin.json` (so the owner's existing private ChatGPT `earshot-audio` can later be updated from this source). Plugin version starts at 1.0.0 and is independent of the engine version.

| Path | Content |
| --- | --- |
| `skills/earshot/SKILL.md` | The only skill, `earshot-audio:earshot`. Written in this repository's words from upstream's two skills, without the MCP and `llm` sections. Three parts: listening (describe, match, rank, find, compare, ab, realness, timeline, sheet, critique, measure, profile), making sound (sfx, kit with the `launch` preset, forge, fit, gallery) and a soundtrack from recordings (the real-sound process). Readiness, installation consent, honest reporting and the Studio handoff come first. |
| `skills/earshot/references/` | Upstream real-sound references copied byte for byte (`process.md`, `design-format.md`, `licences.md`, `sound-design.md`, `troubleshooting.md`) plus this repository's `listening.md` (upstream's listening loops restated) and `studio-handoff.md`. No file named `SKILL.md` below the skill root. |
| `skills/earshot/real-sound/` | Upstream `scripts/` (analyze, arrange, audit, credits, licences, master, mix, qa, variant, mux.mjs) and `templates/` (including `prompts/`) copied byte for byte. |
| `scripts/runtime.py` | The launcher (below). |
| `upstream.json` | Repository, tag, commit, tree, licence, and the SHA-256 of all 282 upstream files plus the list of files copied into the plugin. |
| `LICENSE`, `NOTICE`, `README.md`, `CHANGELOG.md` | MIT text from upstream; attribution; plugin description; history. |

Excluded: MCP configuration of any kind, the `llm` command, keys, upstream's reference films and media, Studio's private overlay.

## Launcher (`scripts/runtime.py`)

Standard library only, Python 3.10+.

- `status [--json]`: interpreter, venv path, installed engine commit, tier readiness (`light_ready`, `full_ready`, `models_cached`) and FFmpeg/FFprobe. Never installs or downloads. Missing or broken pieces report `unavailable`.
- `install --tier light|full [--yes]`: without `--yes` prints the plan (what is written, where, approximate size) and exits 0 without writing. With `--yes`: obtains the source at the pinned commit by `git` (fetch of the exact commit, checked against the recorded tree) or, without `git`, the GitHub archive of the commit; either way every file is checked against `upstream.json` before anything is installed; a mismatch stops with nothing installed. Creates the venv in `~/.framecore-studio/extensions/earshot` (or `--root`, `EARSHOT_NATIVE_ROOT`) and installs the engine with `--no-deps`, then the light dependencies (numpy, scipy, soundfile, soxr, librosa, pyloudnorm, scikit-learn, pillow, matplotlib) or, for full, also CPU PyTorch and transformers. The `mcp` and `llm` extras are never installed.
- `fetch-models [--yes]`: the pinned CLAP and AST snapshots (~1.1 GB), separately and only with consent.
- `run <command> [args...]`: runs `earshot` from the venv with model caches in offline mode. Allowed commands: `doctor` (never `--fetch`), `measure`, `describe`, `match`, `rank`, `find`, `compare`, `ab`, `realness`, `timeline`, `sheet`, `critique`, `profile`, `forge`, `fit`, `sfx`, `kit`, `gallery`. Global options before the command (`--threads N`) are parsed so the real command is checked. `llm`, `mcp` and anything not listed are refused before a process starts, exit 2.
- `python <script> [args...]`: runs a real-sound script from the plugin with the venv interpreter and `-I`.

## Behaviour (skill text)

1. Check readiness with `status` before promising a result; skill visible, light ready, full ready and a completed task are separate facts.
2. Install only after the user's yes, stating what is written and its size (light about 200 MB, full with models about 3 GB); never update the engine from `main`.
3. Many analyses in one task: one short Python script on `earshot.api`, so models load once.
4. real-sound: by default the user's recordings and the bank; searching and downloading from Freesound, Mixkit or Pixabay only on request or an accepted proposal; every download passes upstream's licence policy (`licences.py`, `audit.py`), gets a manifest entry and a credit; disallowed licences are dropped. Nothing is uploaded.
5. Handoff to Studio: WAV paths with SHA-256, `kit.lock.json`, measured onset, peak and end, the commands run. FrameCut keeps the master timeline and frame-exact conversion (rational FPS); Studio keeps brief, board acceptance and final review.
6. Every result names the engine that produced it; model scores do not replace listening or prove licences.

## Studio changes (release 1.124.0)

- Registry entry `earshot`: the public plugin as the first route for every host with code execution (install from this marketplace), the pinned CLI kept as the route without the plugin, pin moved to v0.4.0 in both.
- `earshot-native-routing.md` and the owner lines already naming `earshot-audio:earshot` stay; text updated where it says the plugin is private.

## Tests (written to fail first)

- Launcher, offline: pin and per-file check (a changed file stops the install), refusal of `llm` and `mcp` also after `--threads`, `status` writes nothing, `install` without `--yes` writes nothing, a broken venv is `unavailable`.
- Package: exactly one `SKILL.md`; copied real-sound files byte-identical to the pin; manifests consistent; marketplace lists both plugins with the right versions.
- Real run in the container, recorded with what was not run: light install from the pinned source; `sfx render` with a requested apex and the measured apex; `kit init --preset launch` and `kit check`; `measure` on a sample film; the full tier and `describe` or `match` when time and disk allow, otherwise `NOT_RUN`. Upstream's own test suite once, as information.
- Studio with Earshot in Claude Code: the companion harness with `--with-plugin plugins/earshot-audio` (and Superpowers): whoosh and hit on frames, choosing among candidate files, a refused Gemini upload, recordings only on request. Before and after.

## Publication

`scripts/release.py` covers Studio only. earshot-audio 1.0.0 is published by its marketplace entry and manifests on `main`, validated by its own tests (added to `scripts/check_all.sh`) and `claude plugin validate --strict` on both plugin directories; its `CHANGELOG.md` holds its history. Studio 1.124.0 goes through `release.py` as usual, carrying both. One ledger entry covers the pair. The owner receives a prompt to update the private ChatGPT `earshot-audio` from this source; hosted state stays `pending` until then.

## Out of scope

MCP, Gemini or any audio upload, automatic upstream updates, upstream's reference films, running upstream's suite in GitHub Actions.
