# Voice And Narration Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A public `voice-narration` plugin beside Studio that turns an approved cue sheet into one measured WAV per line through VoxCPM2, Voicebox or the ElevenLabs connector, with a lock file for the mix.

**Architecture:** A plugin folder modelled on `plugins/earshot-audio/`: one skill (`voice-narration:narrate`) and a standard-library launcher (`scripts/runtime.py`) split into small modules. VoxCPM2 runs in a pinned venv through a worker script; Voicebox through its local REST API; ElevenLabs only through the host connector, driven by the skill text.

**Tech Stack:** Python 3.10+ standard library (`argparse`, `wave`, `audioop`-free sample math, `urllib.request`, `unittest`); FFmpeg optional; `voxcpm==2.0.3` and `soundfile` inside the venv only.

**Spec:** `docs/superpowers/specs/2026-10-24-voice-narration-plugin-design.md`

## Global Constraints

- Plugin name `voice-narration`, version `1.0.0`, display name `Voice And Narration`; skill technical ID `narrate`.
- `scripts/` imports only the standard library; `voxcpm_worker.py` is the only file that imports `voxcpm`/`soundfile`, and it runs only with the venv interpreter.
- Venv root: `~/.framecore-studio/extensions/voxcpm`, overridable by `--root` or `VOICE_NARRATION_ROOT`.
- Pinned engine: `voxcpm==2.0.3` (reviewed 2026-10-16 at OpenBMB/VoxCPM `cce58a5b59303c9bd63d12f23afe6a49a4a80c59`); model `openbmb/VoxCPM2`.
- Voicebox API: `http://127.0.0.1:17493`, reviewed at jamiepine/voicebox `2bcb98d1a8b6fe05e15fbc1559e3085669e4035d` (v0.5.0).
- `status` never writes; `install` and `fetch-models` write nothing without `--yes`; in a `cloud` environment `--yes` also needs `--allow-cloud`.
- Stretch at most 5%, only with `--yes`. Cloning (`--reference-wav`) refused without `--consent`.
- No ElevenLabs API key, no MCP server, no upload from the scripts.
- Repository docs and code comments in English; never delete, rename or move a path in `plugins/framecore-work-creative-studio/`.
- Branch rule (owner 2026-10-24): one line of work on `main`; before any push fetch `origin/main`, rebase, rerun `bash scripts/check_all.sh`; Task 8 waits for the display-name release and tells the coordinator before pushing.

## Review Focus

- A cue whose text contains a lexicon word inside another word ("Core" in "Hardcore") must not be substituted; only whole words. Test in Task 3.
- A WAV that is entirely silence must measure 0.0 s and verdict `over` never; it is flagged `silent`. Test in Task 4.
- Voicebox answering with a non-WAV body (the audio format is not pinned by its API) must be converted with FFmpeg or the line fails with a one-line reason, never a traceback. Test in Task 6.
- Duplicate cue `id`s or a missing `max_seconds` must stop before any generation with the offending id named. Test in Task 3.
- A cue text with a voice description prefix in parentheses must keep it after lexicon substitution (VoxCPM voice design uses `(description)text`). Test in Task 3.

---

### Task 1: Package skeleton and marketplace entry

**Files:**
- Create: `plugins/voice-narration/plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` (same shapes as `plugins/earshot-audio/`, name `voice-narration`, version `1.0.0`, `"skills": "./skills"` in the Codex manifest, interface `displayName: "Voice And Narration"`, `developerName: "FrameCore Works"`, three default prompts: "Check whether voice generation is ready here.", "Read my cue sheet with VoxCPM2 and measure it.", "Make this voice-over with ElevenLabs.")
- Create: `plugins/voice-narration/LICENSE` (Apache-2.0, copy of root `LICENSE`), `NOTICE` (Voicebox MIT and VoxCPM Apache-2.0 credits with the pinned commits; no code vendored), `README.md`, `CHANGELOG.md` (1.0.0 entry)
- Modify: `.claude-plugin/marketplace.json` (third entry, `source: ./plugins/voice-narration`, version `1.0.0`, category `productivity`)
- Modify: `scripts/check_all.sh` (two lines after the earshot tests: `python3 plugins/voice-narration/tests/runtime_test.py`, `python3 plugins/voice-narration/tests/package_test.py`)
- Test: `plugins/voice-narration/tests/package_test.py`

**Interfaces:**
- Produces: `PLUGIN`, `ROOT` path constants in `package_test.py`, reused by Task 7.

- [ ] **Step 1: Write `test_manifests_agree`** — the three manifests have `name == 'voice-narration'` and one version `{'1.0.0'}`; marketplace entry `voice-narration` has `source == './plugins/voice-narration'`, version `1.0.0`; Codex manifest `interface.displayName == 'Voice And Narration'`.
- [ ] **Step 2: Write `test_no_vendored_engine`** — no file under the plugin matches `*.safetensors`, `*.pt`, `*.bin`, or a directory named `voxcpm`; no file contains `ELEVENLABS_API_KEY` or `mcpServers`.
- [ ] **Step 3: Run** `python3 plugins/voice-narration/tests/package_test.py` — Expected: FAIL (files missing).
- [ ] **Step 4: Create the files listed above.** Create an empty `tests/runtime_test.py` with one `unittest.main()` so `check_all.sh` runs.
- [ ] **Step 5: Run** the package test and `bash scripts/check_all.sh --fast` — Expected: PASS.
- [ ] **Step 6: Commit** `feat(voice-narration): plugin skeleton and marketplace entry`.

### Task 2: Launcher, environment detection and status

**Files:**
- Create: `plugins/voice-narration/scripts/runtime.py`
- Test: `plugins/voice-narration/tests/runtime_test.py` (load module by path like earshot's test; `quiet(fn, *args)` helper)

**Interfaces:**
- Produces: `main(argv: list[str] | None = None) -> int`; `detect_environment(env: Mapping[str, str]) -> str` returning `'cloud'`, `'local'`; `default_root(env) -> Path`; `venv_python(root: Path) -> Path` (Windows `Scripts/python.exe` vs `bin/python`); `status(root: Path, env, probe_voicebox: Callable[[], bool]) -> dict` with keys `environment`, `python`, `venv`, `voxcpm_version` (str or `'unavailable'`), `weights_cached` (bool), `voicebox` (`'ready'|'unavailable'`), `ffmpeg` (bool), `ffprobe` (bool), `gpu` (from `nvidia-smi --query-gpu=name,memory.total --format=csv,noheader` when present, else `'unknown'`).
- Cloud markers: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` set, `CLAUDE_CODE_REMOTE` == `'true'`, `CODEX_SANDBOX` / `CODEX_CLOUD` set. Anything else is `local`.
- Subcommands registered: `status`, `install`, `fetch-models`, `generate`, `measure`, `stretch`. Any other first argument: message `refused: <name> is not a voice-narration command`, exit 2, no subprocess.

- [ ] **Step 1: Tests** — `test_cloud_markers` (each marker → `'cloud'`; empty env → `'local'`); `test_unknown_command_refused` (`main(['mcp'])` returns 2, `subprocess.run` mock not called); `test_status_writes_nothing` (temp root stays empty; `voxcpm_version == 'unavailable'`; `--json` output parses); `test_venv_python_windows_layout`.
- [ ] **Step 2: Run** `python3 plugins/voice-narration/tests/runtime_test.py` — Expected: FAIL.
- [ ] **Step 3: Implement.** Voicebox probe: `GET /health` with 2 s timeout; any error → `unavailable`. Weights cached: `huggingface_hub` cache dir under the root (`<root>/hf-cache/models--openbmb--VoxCPM2/snapshots/*` exists).
- [ ] **Step 4: Run** the test — Expected: PASS.
- [ ] **Step 5: Commit** `feat(voice-narration): launcher, environment detection and status`.

### Task 3: Cue sheet, lexicon and lock file

**Files:**
- Create: `plugins/voice-narration/scripts/formats.py`
- Test: `runtime_test.py` (class `Formats`)

**Interfaces:**
- Produces: `load_cues(path: Path) -> list[Cue]` where `Cue` is a dataclass `id: str, text: str, max_seconds: float, voice_notes: str | None`; raises `CueError(message)` naming the id for duplicate ids, missing/non-positive `max_seconds`, empty text.
- `load_lexicon(path: Path | None) -> tuple[dict[str, str], str | None]` (entries, SHA-256 hex of the file bytes, or `({}, None)`).
- `apply_lexicon(text: str, lexicon: dict[str, str]) -> str` — whole-word, case-insensitive, longest key first, using `(?<!\w)key(?!\w)` with `re.escape`; text inside a leading `(...)` voice description is left unchanged.
- `Lock` with `Lock.load(out_dir: Path) -> Lock`, `lock.set_line(line_id: str, **fields)`, `lock.save()` writing `<out_dir>/narration.lock.json` as `{"version": 1, "lexicon_sha256": ..., "lines": {id: {...}}}`. Line fields: `engine`, `model`, `engine_version`, `voice_source`, `consent`, `text_sent`, `wav`, `sha256`, `duration`, `max_seconds`, `verdict`, `stretch_percent`, `status` (`ok|failed`), `error`.

- [ ] **Step 1: Tests** — `test_whole_words_only` (`{"Core": "kor"}` turns "Core value" into "kor value" and leaves "Hardcore" unchanged); `test_case_insensitive_longest_first` (`{"FrameCore": "frejm kor", "Core": "kor"}` on "framecore" → "frejm kor"); `test_voice_description_kept` (`"(calm male voice)FrameCore"` → `"(calm male voice)frejm kor"`); `test_duplicate_id_named` (CueError message contains the id); `test_missing_max_seconds_named`; `test_lock_roundtrip_keeps_other_lines` (save line a, reload, set line b, both present); `test_lexicon_hash_recorded`.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Implement `formats.py`.**
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** `feat(voice-narration): cue sheet, lexicon and lock formats`.

### Task 4: Measure and stretch

**Files:**
- Create: `plugins/voice-narration/scripts/audio.py`
- Modify: `runtime.py` (`measure`, `stretch` subcommands)
- Test: `runtime_test.py` (class `Measure`; synthetic WAVs written with `wave`)

**Interfaces:**
- Consumes: `load_cues`, `Lock` (Task 3).
- Produces: `spoken_duration(path: Path, threshold_dbfs: float = -50.0) -> float` (seconds up to the last frame above threshold; 16-bit PCM mono or stereo; raises `AudioError` for other sample widths); `verdict(duration: float, max_seconds: float) -> str` in `fits|over|silent` (`silent` when duration is 0.0); `measure_all(cues, out_dir) -> list[dict]` with `id`, `duration`, `max_seconds`, `verdict` or `missing`, `over_by` (rounded to 0.01 s); `stretch(path: Path, percent: float, ffmpeg: str) -> Path` using `atempo=1+percent/100`, writing `<id>.stretched.wav`.
- CLI: `measure --cues F --out DIR [--json]` updates the lock's `duration`/`verdict`; `stretch LINE_ID --percent N --cues F --out DIR [--yes]` — refuses `N > 5` or `N <= 0` (exit 2), prints the plan without `--yes`, refuses with a one-line message when FFmpeg is missing, records `stretch_percent` in the lock.

- [ ] **Step 1: Tests** — `test_trailing_silence_excluded` (1.0 s tone + 0.5 s silence → 1.00 ± 0.02); `test_all_silence_is_silent`; `test_over_by` (2.4 s against 2.0 → `over`, `over_by == 0.4`); `test_missing_file_reported`; `test_stretch_limit_refused` (`--percent 6` → 2); `test_stretch_without_yes_writes_nothing`; `test_stretch_without_ffmpeg_one_line` (`shutil.which` mocked to None).
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Implement** (peak per frame from `array('h')` samples; threshold `32767 * 10**(dbfs/20)`).
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** `feat(voice-narration): measure reads against limits and bounded stretch`.

### Task 5: VoxCPM2 install and fetch-models

**Files:**
- Modify: `runtime.py` (`install voxcpm`, `fetch-models`)
- Test: `runtime_test.py` (class `Install`; `subprocess.run` and `venv.create` mocked)

**Interfaces:**
- Consumes: `detect_environment`, `default_root`, `venv_python` (Task 2).
- Produces: `install_plan(root: Path, environment: str) -> str` (lists root path, `voxcpm==2.0.3`, approx. size "about 3 GB of Python packages including PyTorch"; in cloud the first line is `warning: this is a cloud environment; the files land on a temporary disk and are lost with the session`); `install(root, environment, yes: bool, allow_cloud: bool) -> int`; `fetch_models(root, environment, yes, allow_cloud) -> int` (plan: "about 5 GB of VoxCPM2 weights from huggingface.co"; runs `venv python -c` `huggingface_hub.snapshot_download('openbmb/VoxCPM2', cache_dir=<root>/hf-cache)`; refuses when voxcpm is not installed).

- [ ] **Step 1: Tests** — `test_install_plan_writes_nothing` (no `--yes`: exit 0, root absent, plan contains `voxcpm==2.0.3`); `test_cloud_install_refused_without_allow_cloud` (cloud env + `--yes` → exit 2, nothing written, message names `--allow-cloud`); `test_cloud_plan_leads_with_warning`; `test_install_runs_pinned_pip` (with `--yes`, pip argv ends with `voxcpm==2.0.3`); `test_fetch_models_needs_install_first`; `test_failed_pip_is_one_line` (CalledProcessError → one stderr line, exit 1).
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Implement** (venv via `venv.EnvBuilder(with_pip=True)`; pip `install --upgrade pip` then `install voxcpm==2.0.3 soundfile`).
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** `feat(voice-narration): consented, pinned VoxCPM2 install and weights fetch`.

### Task 6: Generate with VoxCPM2 and Voicebox

**Files:**
- Create: `plugins/voice-narration/scripts/voxcpm_worker.py` (venv only; reads a JSON job file `{model_dir_or_id, cache_dir, jobs: [{id, text, out, reference_wav?, seed}]}`, loads `VoxCPM.from_pretrained('openbmb/VoxCPM2', load_denoiser=False)` once, calls `model.generate(text=..., cfg_value=2.0, inference_timesteps=10, seed=..., reference_wav_path=...)`, writes `soundfile.write(out, wav, model.tts_model.sample_rate, subtype='PCM_16')`, prints one JSON result line per job `{id, status, error?}`; a failed job does not stop the others)
- Create: `plugins/voice-narration/scripts/voicebox.py`
- Modify: `runtime.py` (`generate`)
- Test: `runtime_test.py` (class `Generate`; fake Voicebox on `http.server.ThreadingHTTPServer` at `127.0.0.1:0`; VoxCPM path tested with a fake worker command)

**Interfaces:**
- Consumes: Tasks 2–4.
- Produces: `VoiceboxClient(base_url: str = 'http://127.0.0.1:17493', timeout: float = 600)` with `generate(text: str, profile_id: str, language: str, engine: str | None) -> str` (POST `/generate` JSON, returns `id`), `wait(generation_id: str) -> dict` (reads SSE `GET /generate/{id}/status` until `status` in `completed|failed`), `download(generation_id: str, dest: Path) -> Path` (GET `/audio/{id}`; if bytes do not start with `RIFF`, convert with FFmpeg to 16-bit PCM WAV, else raise `AudioError('voicebox returned non-WAV audio and FFmpeg is missing')`).
- CLI: `generate --engine voxcpm|voicebox --cues F --out DIR [--lexicon F] [--only ID ...] [--language pl] [--profile ID] [--voicebox-engine NAME] [--reference-wav F --consent TEXT] [--seed 42]`. Writes `<out>/<id>.wav`, updates the lock per line (`status ok|failed`, `error`), runs `measure_all` afterwards and prints the measure table. `--engine voicebox` requires `--profile`. `--reference-wav` without `--consent` → exit 2 before any work. `--engine voxcpm` with voxcpm or weights missing → exit 1 with `run: install voxcpm --yes` / `fetch-models --yes` hint. VoxCPM runs with `HF_HUB_OFFLINE=1`, `HF_HOME=<root>/hf-cache`. Voicebox unreachable → exit 1 `voicebox is not running on 127.0.0.1:17493 (it only runs on the user's own computer)`; never falls back to another engine.

- [ ] **Step 1: Tests** — `test_voicebox_roundtrip` (fake server returns id, SSE `completed`, a RIFF body; lock line `ok`, WAV exists, sha256 recorded); `test_voicebox_failed_line_keeps_others` (second cue fails; first stays `ok`, exit 1, lock has `error`); `test_only_regenerates_selected` (`--only b` leaves line a's sha256 unchanged); `test_non_wav_without_ffmpeg_one_line`; `test_clone_needs_consent` (exit 2, no subprocess); `test_voicebox_unreachable_no_fallback` (worker mock not called); `test_voxcpm_worker_jobs` (fake worker prints results; lexicon applied in `text_sent`); `test_voxcpm_missing_hint`.
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Implement** `voicebox.py`, `voxcpm_worker.py`, the `generate` subcommand.
- [ ] **Step 4: Run** — Expected: PASS.
- [ ] **Step 5: Commit** `feat(voice-narration): generate with VoxCPM2 and Voicebox`.

### Task 7: The narrate skill

**Files:**
- Create: `plugins/voice-narration/skills/narrate/SKILL.md`, `agents/openai.yaml` (`display_name: "Voice And Narration"`, `short_description: "Measured voice-overs from local or ElevenLabs engines"` — 25–64 chars, double-quoted), `references/elevenlabs-connector.md`, `references/formats.md`
- Modify: `package_test.py`

**Interfaces:**
- Consumes: CLI from Tasks 2–6 (exact command names and flags).
- Content: the eight behaviour rules of the spec in that order; `<runtime>` resolved as `../../scripts/runtime.py` like earshot; ElevenLabs reference: `creative_list_voices` to pick and name a voice, one `creative_create_flow` per project, `creative_generate_speech` per line, ask before spending credits, never retry automatically, `creative_get_flow_run_status` until done, then save each take locally and run `measure`; optional `creative_transcribe_audio` only with separate consent. Frontmatter description ≤ 1024 chars, triggers on voice-over, narration, lektor, TTS, read my script.

- [ ] **Step 1: Tests** — `test_exactly_one_skill` (`['skills/narrate/SKILL.md']`); `test_skill_rules_present` (contains `status --json`, `--allow-cloud`, `--consent`, `measure`, `narration.lock.json`, `own computer`, `credits`, `Copy Voice`, `FrameCut`); `test_skill_has_no_key_route` (no `API_KEY`, `mcp add`, `.mcp.json`); `test_openai_yaml_format` (display name words capitalised, short description 25–64 chars, double-quoted).
- [ ] **Step 2: Run** — Expected: FAIL.
- [ ] **Step 3: Write the skill and references.**
- [ ] **Step 4: Run** the package test, then `bash scripts/check_all.sh` — Expected: PASS.
- [ ] **Step 5: Live check in this cloud session:** `python3 plugins/voice-narration/scripts/runtime.py status --json` shows `"environment": "cloud"`; `install voxcpm --yes` exits 2 naming `--allow-cloud`. Record the output for the ledger.
- [ ] **Step 6: Commit** `feat(voice-narration): narrate skill`.

### Task 8: Studio registry, link and release (after the display-name release)

**Files:**
- Modify: `plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.json` (entry `voice-narration`, category `tts`, `kind: ["native_plugin", "skill", "cli"]`, same field set as the `earshot` entry, host statuses `claude_code: native`, `codex: manual`, `chatgpt: pending`, plan/install/verify/remove steps; `not_for` states local engines are for the user's own computer)
- Modify: `plugins/framecore-work-creative-studio/skills/audio-production-director/references/local-tts-engines.md` section 3 (one sentence linking the plugin as the generation and measurement route for VoxCPM2, Voicebox and ElevenLabs)
- Modify: release files per AGENTS.md (manifests, marketplace Studio version, version markers, `config/install-sources.json`, `CHANGELOG.md`, `RELEASE_STATUS.md`, `docs/development-ledger.md` with change ID `CC-20261024-NN`)

- [ ] **Step 1:** Confirm with the coordinator that the display-name release is on `origin/main`; `git fetch origin main && git rebase origin/main`.
- [ ] **Step 2:** Run `python3 plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.py list --category tts` before and after the edit; the new entry appears.
- [ ] **Step 3:** Edit the two Studio files; measure the skill-description budget (≤ 7,800 chars total) and `workflow-orchestrator/SKILL.md` (≤ 32,000 bytes) before and after — neither is expected to change.
- [ ] **Step 4:** `python3 scripts/release.py prepare <next minor>`; `python3 scripts/build_install_manifest.py`; `python3 scripts/package_release.py`; `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs`; `bash scripts/check_all.sh` — Expected: all PASS.
- [ ] **Step 5:** Ledger entry: trigger (owner task 2026-10-24), evidence states (`runtime tests PASS`, cloud check PASS, VoxCPM2/Voicebox generation `NOT_RUN`, ElevenLabs `NOT_RUN` unless consented, hosted ChatGPT `pending` with the `CHATGPT_UPDATE.md` prompt).
- [ ] **Step 6:** Tell the coordinator the release is ready; after the go-ahead, `git fetch origin main` again, rebase if moved, rerun `bash scripts/check_all.sh`, then `python3 scripts/release.py publish ... --push` and push the session branch equal to `main`. Run `git ls-remote --heads origin` and report extra branches.
