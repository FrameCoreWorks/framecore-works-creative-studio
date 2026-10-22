# Handover to the next Claude Code session, 2026-10-22

Origin: Claude Code (cloud) on a Claude Pro plan, session branch `ccr-06247e92-aihwc6`. Baseline: `main` at `684bb43` (package 1.121.0, tag `v1.121.0`, commit `8274d3787debb3dc4b1b04c7d72151bae9089cbb`). The hosted ChatGPT plugin has not been updated since before 1.119.0 (`pending`; the owner does that step in Plugin Creator, with the private overlay preserved).

Read first: [AGENTS.md](../AGENTS.md) "Current rules", [roadmap](roadmap.md), [FrameCut audit](framecut/audit-2026-10-22.md), the latest [ledger](development-ledger.md) entries.

The owner installed the **Superpowers** plugin on their account and wants it used for work on this repository. This handover exists because the session that was running could not see it (a cloud session fixes its skill list at start). Use it, but the repository rules win where they differ: work on `main`, no extra local or remote branches or worktrees, a trigger for every change (maintenance mode).

## Owner decisions this session

- A reply never quotes or names Studio's own files, skills or rules to justify a question (orchestrator and FrameCut text).
- Studio proposes an add-on once, in the user's terms, when it clearly improves the result (FrameCut and Motion Graphics aim for the strongest result, not the simplest); it installs only after the user agrees; a declined offer is not repeated (`AGENTS.md`, `references/extensions.md`).
- The storyboard is a host-managed preview shown once for acceptance; another only when the user asks. The runtime does not enforce it.
- Music on the music bus ducks 6 dB under speech by default, following the timed transcript (`duck_db` overrides, `0` disables).
- For every repository the owner sends: read it first (never run its code), mine the knowledge into Studio's own skills and references, then list it in the extension registry. No code is copied; methods are written again.
- Repository code from outside is read only. The container blocks executing downloaded packages; do not work around it.

## Released this session

1.119.0 reel lessons and orchestrator budget; 1.119.1 reel rules at the orchestrator (host eval G12); 1.119.2 FrameCut audit fixes (24 tests in `tests/framecut_audit_test.py`); 1.119.3 light music ducking; 1.119.4 MoneyPrinterTurbo extension; 1.119.5 plain acceptance question and strongest route (G13, G14); 1.120.0 FrameCut `align-script`, phrase-aware cues, `font_missing_glyphs`; 1.121.0 FrameCut effects `pixelate`, `posterize`, `ordered_dither`, Pixel look section in `references/animate-engine.md`, Pixel Plugin extension.

## Pending, in this order

### 1. Open Design: update the registry entry, then adopt

The registry entry `open-design` still pins v0.25.0 (`de6d2c0`). The newer release is `open-design-v0.26.0`, tag commit `bfee093942f8578c8b6ec7f26862e96f81026a89` (resolved with `git ls-remote`, 2026-10-20, "Share, Review, Refine"). Facts to put in every host's steps, `requires`, `rights`, `not_for` and `observed`:

- Installer SHA-256 (read from the release's `.sha256` assets and matched against the review): `open-design-0.26.0-mac-arm64.dmg` `ff7a1181b83aca664b85b7da0a5df740c99cf34bdce203d5276022ee72946d76`; `mac-x64.dmg` `f2fc313eb5b62c207621b5f15e83aa135c69a04e9cbae25fce94da2d99c346ee`; `win-x64-setup.exe` `4c0697a53177753072593b44133f44cca76421a102a4da1b4229d5e643569b00`. Linux still only from source at `bfee093`, Node 24, pnpm 10.33.2.
- `od mcp install <agent>`, `--print` and `--uninstall` are unchanged since the last review. Never use the `curl | sh` installer in its README.
- Privacy: telemetry is on by default (PostHog, privacy-masked replay, and "conversation and tool content" for quality traces, scrubbed and truncated, until the user picks Don't share); safety and reliability telemetry cannot be switched off in official builds. New in 0.26.0: **Share** uploads project files to OpenDesign's cloud and needs sign-in: add "do not use Share with client material unless the client agreed" to `not_for`.
- Security: its MCP server exposes write tools (`write_file`, `delete_file`, `delete_project` with `confirm:true`, `create_artifact`, `start_run`, `create_project`); registering it gives the user's agent write and delete power over Open Design projects. The daemon listens on 127.0.0.1; a non-loopback bind needs `OD_API_TOKEN`.
- Licence: Apache-2.0 for the code; the new motion skills carry their own MIT licences; the five official motion templates are explicit remakes of viral third-party posts, so Studio must not present them as its own designs.
- Add `integrations/open-design/README.md` (decision map) and a copy of the Apache-2.0 licence, as for the other entries.

What to adopt (none of it is a new creative idea; Studio is deeper on motion craft, so what is left is delivery mechanics and a few rules). Write tests that fail first for every runtime item.

Runtime:
1. `flash_check.py` beside `motion_activity.py` in `skills/hyperframes-workflow/assets/motion-quality/`: photosensitivity screening, labelled as screening and not as WCAG, Harding or broadcast conformance. Sample at 24 to 30 fps, relative luminance with sRGB linearization on a small frame, count significant opposing luminance changes (at least 0.10 relative luminance, the darker side below 0.80, over at least a quarter of the frame) and flag more than 3 flashes in any 1 s window; report the worst second. The existing activity script samples only 6 fps, which is too few.
2. A transcript sanity check in `fc_media.py`, called by `transcribe` and `import-transcript` and returned as warnings (not verdicts): more than 20 % of tokens being music notes or replacement characters, many word spans under 0.05 s, runs of three identical segments, and an English-only model (`*.en`) with a non-English `--language` (an error, before any decoding; with `auto` a warning).
3. `inspect-encode.py`: `--audio required|silent` (ffmpeg `volumedetect`; required needs a stream with peak above -80 dB, silent needs none audible) and `--cover-time` (extract that exact frame; reject a time outside the film), both recorded in `evidence.json`.

Model-read text (smallest edits in the owning files; the orchestrator has 82 bytes of budget left, so none goes there):
- `references/motion-craft.md`: a flash and strobe limit (count luminance reversals; beat-driven pulses on full-frame brightness count; text pulses stay at 3 to 6 % scale), "the transition is the exit" (do not fade the outgoing scene before a covering transition), and right-to-left and complex scripts (mirror reveal direction but keep the film timeline left to right, isolate Latin names and numbers, no tracking and no slant on Arabic, word-level not per-letter animation, check shaping before promising anything). `motion-sync/README.md`: restraint for what a beat envelope drives.
- `caption-studio/references/readability-defaults.md`: the right-to-left bullet.
- `remotion-video-production/references/remotion-implementation-notes.md`: a transparent overlay for FrameCut (`--image-format=png --pixel-format=yuva444p10le --codec=prores --prores-profile=4444` for an editor, `--codec=vp9 --pixel-format=yuva420p` for a browser; check against the installed version and with FrameCut's `has_alpha` probe).
- `creative-video-producer/SKILL.md`: pilot the first and hardest unit at real size before a batch of generations. `video-prompt-architect/references/video-craft.md`: a 360 spin as four quarter-turn segments anchored on supplied views.
- `opencut-video-studio/SKILL.md` and `references/extensions.md`: zero questions is a valid outcome when a wrong guess is cheap to fix; after a recommendation offer to just go with it; a declined or unavailable add-on means the next-best route with its cost named; a finished stage closes with at most three plain next steps drawn from what was made; a local tweak never reopens discovery. `tool-routing-cost`: a failure is told in one plain sentence with the next step, never provider, path or code.

Rejected: the motion templates, the `frame-*` looks, the jury's numeric composite, page capture of other companies' sites, the live-artifact runtime, interface animation corpora, the scroll runtime. Noted for later: a brand-capture tool for the user's own site, an optional motion block in the brand kit, fitting a reference clip's motion to the easing presets.

### 2. The owner's checks that only they can do

- ChatGPT startup (ordinary ChatGPT, then Work) after the orchestrator edits in 1.119.0, 1.119.1, 1.119.5 (record the client and reasoning setting; `PASS_REPORTED` only from the owner).
- Whether the acceptance question is now plain in ChatGPT (G13 does not reproduce the leak in Claude Code), and whether an uncertain user gets directions instead of one simple plan (G14).
- The hosted plugin update with the private overlay (PoYo, the Sunra API route) preserved. The prompt, pinned to 1.121.0: update the existing plugin from `https://github.com/FrameCoreWorks/framecore-works-creative-studio` at commit `8274d3787debb3dc4b1b04c7d72151bae9089cbb` (tag `v1.121.0`), read `CHATGPT_UPDATE.md` and `config/install-sources.json` at that commit, write the declared files as published, delete nothing, then run `check_environment.py --update --host chatgpt_work`. Regenerate the pin from the newest release before giving it.

### 3. Product decisions still waiting for the owner

[docs/framecut/audit-2026-10-22.md](framecut/audit-2026-10-22.md): per-deliverable caption settings, render speed (about 0.1x real time at 1080p), per-sequence delivery fingerprints, the board receipt's blindness to sound. Ideas from the MoneyPrinterTurbo review that were noted, not built: a `plan` command that explains rebuilds, pause tags with sample-accurate voice-over offsets, source-fitness and coverage reports, a needs-input exit code and a spend-approval gate once FrameCut calls a paid provider.

### 4. Branches

Remote branches: `main`, `gh-pages`, the session branch, and `ccr-b6d36a1c-4hszow` (merged into `main`; the owner may delete it).

## Traps found this session

- `skills/hyperframes-workflow/assets/animate-engine/` is a pinned upstream snapshot. `tests/animate_engine_test.py` fails the release if any file in it changes (it failed 1.121.0 once when `styles/pixel/STYLE.md` was edited). Put Studio's own text in `references/animate-engine.md` instead.
- `scripts/release.py prepare` needs a clean tree and bumps files in place. Never edit the repository while `prepare` or `publish` runs. A failed `prepare` leaves the bump uncommitted: inspect `git diff --stat`, restore only those files with `git restore`, fix the cause, run it again. `Baseline-SHA` in a commit trailer must be a real full SHA.
- The background release shell can be killed when the session's worker restarts; `publish` may then need a second run (it is safe to repeat).
- Budgets: `workflow-orchestrator/SKILL.md` 31,918 of 32,000 bytes; skill descriptions about 7,716 of 7,800 characters. Measure before editing either.
- A model-read text edit needs a host evaluation before and after where the behaviour can be observed (`scripts/host_eval.py`, at most 5 cases per gate, record cases, tokens and time); regex checks can be too narrow, so read the replies.
- Evidence stays separate: source tests, GitHub publication, saved-plugin readback and fresh-client behaviour. Nothing run in a container is installed-client behaviour.
