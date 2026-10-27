# Open Design 0.26.0 Registry Update and Adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the `open-design` extension entry to release 0.26.0 and adopt the delivery mechanics the review found (photosensitivity screening, transcript sanity warnings, encode audio/cover checks, a handful of model-read rules), released as Studio 1.122.0.

**Architecture:** Runtime items are small additions beside existing tools (`motion-quality/`, FrameCut's `fc_media.py`), each driven by a test that fails first. Model-read items are the smallest edits in the owning reference or `SKILL.md`. The registry entry, its integration folder and the release follow the existing pattern (MoneyPrinterTurbo, Pixel Plugin).

**Tech Stack:** Python 3 (numpy, ffmpeg/ffprobe), unittest, Node validator, `scripts/release.py`, `scripts/host_eval.py`.

**Spec:** `https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/8a8c78c8b15be8934b32c49c88c30413f185c387/docs/handover-claude-code-2026-10-22.md`, section "Pending, in this order", item 1. Repository rules: `AGENTS.md` "Current rules".

`P` below means `plugins/framecore-work-creative-studio`.

## Global Constraints

- Work on `main` only; the session branch `ccr-9d0ac477-rf33kp` is pushed equal to `main`. No worktrees, no other branches, no force push.
- Never delete, rename or move a path in `P/`. New paths are permanent.
- Trigger for every change (maintenance mode): the owner's handover item 1 (2026-10-22, Open Design 0.26.0 review). Name it in the ledger and commits.
- `P/skills/workflow-orchestrator/SKILL.md` is not edited (82 bytes of budget left). Skill descriptions are not edited.
- `P/skills/hyperframes-workflow/assets/animate-engine/` is a pinned snapshot: do not touch.
- No code or text is copied from Open Design; methods are written again. Its code is read only, never run. Never use its `curl | sh` installer.
- Release tag `open-design-v0.26.0` = commit `bfee093942f8578c8b6ec7f26862e96f81026a89`.
- SHA-256: `open-design-0.26.0-mac-arm64.dmg` `ff7a1181b83aca664b85b7da0a5df740c99cf34bdce203d5276022ee72946d76`; `open-design-0.26.0-mac-x64.dmg` `f2fc313eb5b62c207621b5f15e83aa135c69a04e9cbae25fce94da2d99c346ee`; `open-design-0.26.0-win-x64-setup.exe` `4c0697a53177753072593b44133f44cca76421a102a4da1b4229d5e643569b00`. Linux only from source at `bfee093`, Node 24, pnpm 10.33.2.
- Flash screening is labelled "screening", never WCAG, Harding or broadcast conformance.
- Commit trailers: `Origin-Agent: claude-code-cloud`, `Change-ID: CC-20261022-08`, `Baseline-SHA: <full SHA>`, `Shared-Package-Changed`, `ChatGPT-Work-Sync`, `Codex-Sync`, plus the session attribution lines.
- Repository text in English.

## Review Focus

1. A video shorter than 1 s, or a single-frame video, given to `flash_check.py`: expect a PASS with the measured length, or exit 2 for fewer than two frames, never a crash. Test in Task 1.
2. A slow full-frame fade from black to white and back (one pair of opposing changes over 2 s) must not count as several flashes: consecutive same-direction changes collapse into one transition. Test in Task 1.
3. A transcript with no words and no segments (silent clip) must give no warnings and no division by zero. Test in Task 2.
4. `inspect-encode.py --audio required` on a video with no audio stream: FAIL recorded in `evidence.json` and exit 1, not an ffmpeg traceback. Test in Task 3.
5. `--cover-time` equal to the duration or negative: rejected before the destination directory is created, so a retry with the same destination works. Test in Task 3.

---

### Task 1: Photosensitivity screening `flash_check.py`

**Files:**
- Create: `P/skills/hyperframes-workflow/assets/motion-quality/flash_check.py`
- Create: `P/tests/flash_check_test.py`
- Modify: `scripts/check_all.sh` (add `python3 "$P/tests/flash_check_test.py"` after `motion_activity_test.py`)
- Modify: `P/skills/hyperframes-workflow/assets/motion-quality/README.md` (one row/paragraph for the tool)
- Modify: `P/skills/hyperframes-workflow/references/runtime-map.md` (row after `motion_activity`)
- Modify: `P/skills/workflow-orchestrator/assets/capability-card.json` (entry `flash_check` after `motion_activity`, same shape; `observed`: what was run in this container)

**Interfaces:**
- Produces: `samples(path, fps=30, size=(64, 114)) -> np.ndarray` (float relative luminance, shape frames×h×w); `measure(frames, fps) -> dict` with keys `seconds`, `fps`, `max_flashes_per_second`, `worst_second_start`, `transitions`; `verdict(report, max_flashes=3) -> list[str]`; `main(argv=None) -> int` (0 PASS, 1 REVISE, 2 unreadable input). Report always carries `"screening": "Photosensitivity screening only; not WCAG, Harding or broadcast conformance."` and, from `main`, `video_sha256`, `verdict`, `problems`.

Constants: `SAMPLE_FPS = 30` (`--fps` accepts 24 to 30, else argparse error), `MIN_DELTA = 0.10`, `DARK_LIMIT = 0.80`, `MIN_AREA = 0.25`, `MAX_FLASHES = 3`.

Algorithm (not determined by the tests alone):
- ffmpeg `fps=N,scale=64:114,format=rgb24` raw frames; sRGB to linear per channel (`c/12.92` if `c<=0.04045` else `((c+0.055)/1.055)**2.4`), `L = 0.2126R + 0.7152G + 0.0722B`.
- For each consecutive pair, a pixel changes significantly when `|ΔL| >= MIN_DELTA` and `min(L_a, L_b) < DARK_LIMIT`. The pair is an `up` (or `down`) transition when at least `MIN_AREA` of pixels change significantly upward (downward).
- Collapse runs of same-direction transitions into one; keep the time of each kept transition.
- Slide a 1 s window over transition times; flashes in a window = `count // 2`. Report the maximum and the start of that window.

- [ ] **Step 1: Write the failing tests** (`unittest`, skip without ffmpeg; frames built with numpy and piped to `ffmpeg -f rawvideo -pix_fmt gray -s 64x114 -r 30 -i - -pix_fmt yuv420p`, in a temp dir; module loaded with `importlib` like `motion_activity_test.py`)
  - `test_fast_full_frame_flicker_is_flagged`: black/white toggled every 3 frames for 3 s (5 flashes/s) → `max_flashes_per_second >= 4`, `verdict` non-empty, `main([path]) == 1`.
  - `test_slow_alternation_passes`: toggle every 15 frames (1 flash/s) → `max_flashes_per_second <= 1`, `main([path]) == 0`.
  - `test_slow_fade_counts_as_one_change_each_way`: linear ramp 0→255 over 1 s and back over 1 s → `max_flashes_per_second <= 1`.
  - `test_small_area_flicker_passes`: fast toggle confined to 10 % of the frame → `max_flashes_per_second == 0`.
  - `test_bright_only_flicker_passes`: fast toggle between grey 235 and 255 (both linear L above 0.80) → `max_flashes_per_second == 0`.
  - `test_report_is_labelled_screening_and_bound_to_file`: `main([path, '--json'])` output has `screening` containing `"not WCAG"` and a 64-hex `video_sha256`.
  - `test_short_and_unreadable_inputs`: a 0.5 s clip → returns 0 or 1 without exception; a text file → `main` returns 2; `--fps 60` → `SystemExit`.
- [ ] **Step 2: Run** `python3 P/tests/flash_check_test.py` → FAIL (file not found on import).
- [ ] **Step 3: Implement** `flash_check.py` in the style of `motion_activity.py` (docstring with usage and limits, argparse, exit codes, `--json`).
- [ ] **Step 4: Run** `python3 P/tests/flash_check_test.py` → all PASS; then `python3 P/tests/motion_activity_test.py` still PASS.
- [ ] **Step 5: Register** in `check_all.sh`, motion-quality README, runtime-map and capability card; run `node P/scripts/validate-studio.mjs` → PASS and `python3 P/tests/runtime_inventory_test.py` → PASS.
- [ ] **Step 6: Commit** `feat(motion-quality): flash_check photosensitivity screening` with the trailers.

### Task 2: Transcript sanity warnings in FrameCut

**Files:**
- Modify: `P/skills/opencut-video-studio/assets/framecut/fc_media.py` (`transcript_import`, `transcribe`, new helpers)
- Modify: `P/tests/framecut_script_test.py` (new test class; follow its existing fixture style)
- Modify: `P/skills/opencut-video-studio/SKILL.md` only if it lists `import-transcript`/`transcribe` outputs: one clause that `warnings` are checks to read, not verdicts.

**Interfaces:**
- Produces: `transcript_warnings(result: dict) -> list[str]`; `model_language_check(model: Path, language: str) -> str | None` (raises the module's `require` error with code `model_language_mismatch` for an English-only model and a language other than `en`/`auto`; returns a warning string for `auto`; else `None`). `transcript_import` result gains `"warnings": [...]` before the fingerprint; `transcribe` calls `model_language_check` before any ffmpeg/ASR work and appends its warning.

Rules (exact values from the spec):
- Music/garbage: tokens = whitespace-split text of `words` if any, else `segments`; warn when more than 20 % of tokens contain `U+FFFD` or a music note (`♪ ♫ ♬ ♩ ♭ ♮ ♯`).
- Micro words: timed words with `end - start < 0.05`; warn when at least 5 and more than 20 % of timed words.
- Repeats: three consecutive segments whose normalized text (casefold, stripped of punctuation and spaces) is identical and non-empty.
- English-only model: file name matches `\.en(\.|$)` (e.g. `ggml-base.en.bin`).

- [ ] **Step 1: Write the failing tests**
  - `test_music_note_transcript_warns`: segments of `"♪ ♪ ♪"` and one real line → one warning mentioning music notes or unreadable characters.
  - `test_micro_word_spans_warn`: 10 words, 6 of 0.02 s → warning; 10 words of 0.3 s → none.
  - `test_three_identical_segments_warn`: `"Thank you."` ×3 consecutive → warning; ×2 → none.
  - `test_empty_transcript_has_no_warnings`: no words, no segments → `warnings == []`.
  - `test_clean_transcript_has_no_warnings_and_fingerprint_is_stable`: same input twice → equal fingerprints, `warnings == []`.
  - `test_english_only_model_with_polish_is_an_error_before_decoding`: `model_language_check(Path('ggml-base.en.bin'), 'pl')` raises with code `model_language_mismatch`; `'auto'` returns a string; `'en'` and `ggml-base.bin` with `'pl'` return `None`. Also `transcribe(...)` with a temp `ggml-base.en.bin` and `language='pl'` raises that code without calling ffmpeg (patch `fc_media.ffmpeg` to fail the test if called).
- [ ] **Step 2: Run** `python3 P/tests/framecut_script_test.py` → new tests FAIL.
- [ ] **Step 3: Implement** the helpers and wire them in.
- [ ] **Step 4: Run** `python3 P/tests/framecut_script_test.py`, `framecut_test.py`, `framecut_audit_test.py`, `framecut_development_test.py` → all PASS.
- [ ] **Step 5: Commit** `feat(framecut): transcript sanity warnings and English-only model check`.

### Task 3: `inspect-encode.py --audio` and `--cover-time`

**Files:**
- Modify: `P/skills/hyperframes-workflow/assets/motion-quality/inspect-encode.py`
- Create: `P/tests/inspect_encode_test.py`; register in `scripts/check_all.sh` after `flash_check_test.py`
- Modify: `P/skills/hyperframes-workflow/assets/motion-quality/README.md` (the two flags)

**Interfaces:**
- Produces: `inspect(video, destination, audio=None, cover_time=None) -> dict`; the dict gains `"failed_checks": [...]`. `evidence.json` gains `"audio_check": {"expected": "required"|"silent", "streams": n, "max_volume_db": float|None, "result": "PASS"|"FAIL"}` and `"cover": {"time": t, "file": "cover.png"}` when requested. CLI exits 1 when `failed_checks` is non-empty (evidence still written), 1 with "Inspection failed" for input errors as today.

Rules: peak from ffmpeg `-af volumedetect -f null -` (`max_volume:` line); `required` passes when an audio stream exists and peak > -80 dB; `silent` passes when there is no audio stream or peak <= -80 dB. `cover_time` must satisfy `0 <= t < duration` (from `format.duration`), checked before `destination.mkdir`; frame extracted with accurate seek (`-ss` after `-i`) to `cover.png`.

- [ ] **Step 1: Write the failing tests** (skip without ffmpeg; fixtures from lavfi `testsrc2` with and without `sine` audio, and `anullsrc` for silent audio)
  - `test_required_audio_passes_with_tone_and_fails_without_stream`
  - `test_silent_passes_for_no_stream_and_for_digital_silence_and_fails_for_tone`
  - `test_cover_time_writes_frame_and_records_it`
  - `test_cover_time_outside_film_is_rejected_before_destination_exists`: `t = duration` and `t = -1` raise `ValueError`; destination does not exist afterwards.
  - `test_cli_exit_code_is_1_when_a_check_fails` (run the script with `subprocess`).
  - `test_default_run_is_unchanged`: no flags → no `audio_check`/`cover` keys, `failed_checks == []`.
- [ ] **Step 2: Run** `python3 P/tests/inspect_encode_test.py` → FAIL.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run** the test → PASS; `bash scripts/check_all.sh --fast` → PASS.
- [ ] **Step 5: Commit** `feat(motion-quality): inspect-encode audio and cover checks`.

### Task 4: Registry entry and integration folder for 0.26.0

**Files:**
- Modify: `P/skills/workflow-orchestrator/assets/extensions/extensions.json` (entry `open-design` only)
- Create: `P/integrations/open-design/README.md` (decision map, MoneyPrinterTurbo format)
- Create: `P/integrations/open-design/LICENSE` (Apache-2.0 text read from the repository at `bfee093`, byte-for-byte)
- Modify: `P/tests/extensions_test.py` (one test pinning the entry)
- Check: `docs/extension-registry.md` for any other file an entry update must touch, and follow it.

Entry changes:
- `reviewed_commit` → `bfee093942f8578c8b6ec7f26862e96f81026a89`; `gives`: "Release 0.26.0".
- Every host's `manual_steps`: release link `open-design-v0.26.0`, the three new SHA-256 values, Linux from source at `bfee093` with Node 24 and pnpm 10.33.2; keep `od mcp install <agent>`, `--print`, `--uninstall`; add "Never use the `curl | sh` installer from its README"; add that registering the MCP server gives the agent write and delete power over Open Design projects (`write_file`, `delete_file`, `delete_project`), and that the daemon stays on 127.0.0.1 (a non-loopback bind needs `OD_API_TOKEN`).
- `requires`: desktop 0.26.0, pnpm 10.33.2.
- `rights`: telemetry on by default (PostHog, privacy-masked replay, conversation and tool content for quality traces, scrubbed and truncated, until Don't share); safety and reliability telemetry cannot be switched off in official builds; motion skills carry their own MIT licences; the five official motion templates are remakes of third-party viral posts and are not Studio's designs.
- `not_for`: add "using Share (uploads project files to OpenDesign's cloud, needs sign-in) with client material unless the client agreed".
- `observed`: 2026-10-22 entry: tag resolved with `git ls-remote` on 2026-10-20, SHA-256 read from the release's `.sha256` assets, code read only; app, MCP server and agent connection not installed or run.

- [ ] **Step 1: Write the failing test** `test_open_design_entry_pins_0_26_0`: `reviewed_commit` equals the full SHA; every `manual` host's steps contain `open-design-v0.26.0`, all three hashes, `--print`, `--uninstall` and `curl | sh`; no host text contains `0.25.0`; `not_for` contains `Share`; `integrations/open-design/LICENSE` starts with `Apache License` and `README.md` exists.
- [ ] **Step 2: Run** `python3 P/tests/extensions_test.py` → FAIL.
- [ ] **Step 3: Fetch the licence** (read-only, e.g. `https://raw.githubusercontent.com/nexu-io/open-design/bfee093942f8578c8b6ec7f26862e96f81026a89/LICENSE`) into the integration folder; read the craft-rules file at `de6d2c0` and `bfee093` and note in the README whether it changed (a change is reported to the owner, not adopted here).
- [ ] **Step 4: Edit** the entry and write the README (decision table: adopted methods with their Studio location, rejected items from the handover's "Rejected" list, "noted for later" items).
- [ ] **Step 5: Run** `python3 P/tests/extensions_test.py` and `node P/scripts/validate-studio.mjs` → PASS.
- [ ] **Step 6: Commit** `feat(extensions): Open Design 0.26.0 entry and decision map`.

### Task 5: Model-read text (smallest edits in the owning files)

**Files and content** (each a sentence or short bullet in an existing section; written in Studio's voice, not quoting Open Design):
- `P/skills/hyperframes-workflow/references/motion-craft.md`: (a) flash and strobe limit: no more than 3 full-frame luminance reversals in any second; beat-driven pulses on full-frame brightness count; text pulses stay at 3 to 6 % scale; screen with `flash_check.py`. (b) The transition is the exit: do not fade the outgoing scene before a covering transition. (c) Right-to-left and complex scripts: mirror reveal direction but keep the film timeline left to right; isolate Latin names and numbers; no tracking and no slant on Arabic; animate by word, not by letter; check shaping in the renderer before promising.
- `P/skills/hyperframes-workflow/assets/motion-sync/README.md`: restraint: a beat envelope drives one or two properties of an accent, never full-frame brightness or every layer.
- `P/skills/caption-studio/references/readability-defaults.md`: right-to-left bullet (alignment, isolated Latin names and numbers, no letter spacing, word-level timing).
- `P/skills/remotion-video-production/references/remotion-implementation-notes.md`: transparent overlay for FrameCut: `--image-format=png --pixel-format=yuva444p10le --codec=prores --prores-profile=4444` for an editor, `--codec=vp9 --pixel-format=yuva420p` for a browser; check flags against the installed Remotion version and confirm with FrameCut's `has_alpha` probe.
- `P/skills/creative-video-producer/SKILL.md`: pilot the first and hardest unit at real size before a batch of generations.
- `P/skills/video-prompt-architect/references/video-craft.md`: a 360 spin as four quarter-turn segments anchored on supplied views.
- `P/skills/opencut-video-studio/SKILL.md`: zero questions is valid when a wrong guess is cheap to fix; after a recommendation offer to just go with it; a finished stage closes with at most three plain next steps drawn from what was made; a local tweak never reopens discovery.
- `P/skills/workflow-orchestrator/references/extensions.md`: a declined or unavailable add-on means the next-best route with its cost named.
- `P/skills/tool-routing-cost/SKILL.md`: a failure is told in one plain sentence with the next step, never provider, path or code.

- [ ] **Step 1: Baseline host evaluation** before editing: `python3 scripts/host_eval.py --suite gaps --cases G13,G14` and `python3 scripts/host_eval.py --suite routing --cases RT22` (3 cases, within the 5-per-gate limit). Record cases, tokens, time and read the replies.
- [ ] **Step 2: Measure** `wc -c` of every file above; make the edits; confirm the orchestrator `SKILL.md` and skill descriptions are byte-unchanged (`git diff --stat`).
- [ ] **Step 3: Run** `node P/scripts/validate-studio.mjs` and `python3 P/tests/knowledge_wiring_test.py` → PASS.
- [ ] **Step 4: After host evaluation**: the same three cases; compare replies (no regression; G14 offers a next step or "go with it"; no file names quoted). Record both runs for the ledger.
- [ ] **Step 5: Commit** `docs(skills): Open Design review rules in owning references`.

### Task 6: Release 1.122.0, publication and records

- [ ] **Step 1:** `bash scripts/check_all.sh` (full) → PASS; `claude plugin validate --strict` on the plugin → PASS.
- [ ] **Step 2:** Re-check `git fetch origin main` equals the baseline (`cb431a6…` or the last own commit); stop and inspect on drift.
- [ ] **Step 3:** `python3 scripts/release.py prepare 1.122.0 --change-id CC-20261022-08 --title ... --changelog ... --notes ... --summary ... --push` (summary names the trigger; nothing edited while it runs). On failure follow the handover trap note (restore only the bumped files, fix, rerun).
- [ ] **Step 4:** `python3 scripts/release.py publish ...` (repeat once if the shell was killed); read back the GitHub release assets as in CC-20261022-06.
- [ ] **Step 5:** Ledger publication commit (GitHub state, ChatGPT Work `pending`, Codex `not_run`), push `main`, push `ccr-9d0ac477-rf33kp` equal to `main`.
- [ ] **Step 6:** `git ls-remote --heads origin`; report branches beyond `main`, `gh-pages` and the session branch with their merge state. Give the owner the regenerated `CHATGPT_UPDATE.md` prompt pinned to the 1.122.0 commit.
