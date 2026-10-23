# Handover: Claude Code, 2026-10-23 (Studio 1.125.0, earshot-audio 1.0.5)

For the next Claude Code session (another account) and for ChatGPT Work. Read [AGENTS.md](../AGENTS.md) first; its current rules stand. This note lists what was done on 2026-10-22/23, what is verified and what is left.

## State

- `main`: Studio **1.125.0** (tag `v1.125.0`, release commit `b94028c807c3dd59878d1bb8bceeff6121ac0deb`), public plugin **earshot-audio 1.0.5** in `plugins/earshot-audio` (same commit). Marketplace `framecore-works` lists both.
- Session branch `ccr-9d0ac477-rf33kp` equals `main`. No other working branches; branch deletion is the owner's.
- Hosted ChatGPT plugins (Studio and earshot-audio): **pending**. The owner's ChatGPT Work still had an older earshot runtime (it reported `neural_ready`, Earshot 0.3, no `--yes`, no `status --json`).

## What the owner decided on 2026-10-23 (now implemented)

1. **No upload to Gemini.** Upstream's `llm` and `mcp` stay outside; a review in words is written from local readings (`references/written-critique.md`).
2. **Option A:** when the Earshot plugin is listed but its engine is missing, one question with both routes (install Earshot, or Studio's own `sound.py`), nothing run before the answer, the engine that ran is always named.
3. **Effects chosen by listening, as gates:** description from the picture and request, candidates ranked, `match` against confusions (metal, rattle, clang, glass), under about 4 onsets/s, energy in low-mid/mid for phone speakers; rejected candidates reported. The owner chose by ear the hit the gated selection picked (`cut_hit/kick`): `verification/earshot-audio-1.0.4-listening.json`.
4. **Same setup on every host, right after installation** (no extra "Configure Studio" in Claude): Superpowers first, then Earshot in plain words with **full (about 2.6 GB, recommended) / light (about 200 MB) / not now**; the answer is the consent and the plugin plus tier are installed in the same conversation where code runs (ChatGPT Work, Claude Code, Codex). Text: `workflow-orchestrator/references/extensions.md#first-companion-setup`, step 6, with Polish copy.
5. **One Earshot:** the registry entry `earshot` routes every host through the earshot-audio plugin and `runtime.py` (its own pip installation removed); stale 0.3 text fixed; `listen.py` model commands use the plugin-installed engine offline with its cache, refuse `llm`/`mcp`.
6. **Superpowers for Earshot's code:** `writing-plans`, `test-driven-development` (failing onset check per cue before placement code), `systematic-debugging` (install/runtime/render failures), `verification-before-completion` (encoded MP4). In `earshot-audio` SKILL (sections 1 and 2), Motion Graphics SKILL line 8, `superpowers-native-routing.md#sound-with-earshot`, `earshot-native-routing.md`.

## Evidence (Claude Code, Sonnet 5.5 headless unless noted)

- Companion host evals C01-C20 in `tests/host-evals/companion.json`; records in `verification/host-evals/2026-10-2*-companion-*.json`. Before/after pairs: C14, C16, C17, C18, C19, C20.
- Full tier installed in a Claude Code cloud container after the owner allowed `download.pytorch.org`, `*.pytorch.org`, `huggingface.co`, `*.huggingface.co`, `*.hf.co` (Custom network access): `verification/earshot-audio-1.0.3-full-tier.json`. End-to-end films: `verification/earshot-audio-1.0.2-e2e.json`.
- Owner listening: `PASS_REPORTED` for the V3 hit. Everything in ChatGPT, ChatGPT Work and Codex: `NOT_RUN`.

## Left to do

1. **ChatGPT Work (owner, with Plugin Creator):** update earshot-audio to 1.0.5 and Studio to 1.125.0 from commit `b94028c807c3dd59878d1bb8bceeff6121ac0deb` (prompts below), read back, then run the setup test and the full-tier film test below. Record results as `PASS_REPORTED` with the tested client.
2. **Codex:** the local-folder plugin route for earshot-audio is documented but not tested.
3. **Open owner question:** none blocking. Optional idea (not started, needs the owner): a Claude plugin hook to start setup after a manual `/plugin install`; today the installation prompt enters setup.
4. Budgets: `workflow-orchestrator/SKILL.md` was not touched (31,759 of 32,000 bytes).

## Prompts for ChatGPT Work

**1. Update earshot-audio**

```
@plugin-creator

Update my existing earshot-audio plugin (do not create a new one) from
https://github.com/FrameCoreWorks/framecore-works-creative-studio
pinned to commit b94028c807c3dd59878d1bb8bceeff6121ac0deb (tag v1.125.0), folder plugins/earshot-audio.
Write all files of that folder exactly as published, version 1.0.5. Do not delete or rename any path.
After saving, read back from the saved plugin and report the SHA-256 of:
- scripts/runtime.py (expected 1a28b83c7f074a832dad6f959e23e07783b69fb0a67d2b62a809ed1185c11617)
- upstream.json (expected 20d5332d2fd0551ce02d9f6df00920a2ffd356aac42ba7b731807d0b60c90e46)
- skills/earshot/SKILL.md (expected 3d114acb8d9f097d35c16f3a681d753656ad9aed586c772bb199b0fd310c4164)
List any saved files that are not in that folder (for example an older runtime from the 0.1.0 adapter) without deleting them.
Then run `python3 scripts/runtime.py status --json` from the saved plugin and show the output. Install nothing.
```

Expected: all three hashes match; `status` shows `pinned_commit` `591fa3e…`, `full_ready` (not `neural_ready`), `state: unavailable`.

**2. Update Studio**: the Plugin Creator prompt printed by `release.py` (CHATGPT_UPDATE.md), pinned to `b94028c807c3dd59878d1bb8bceeff6121ac0deb`, preserving the private overlay.

**3. Setup test** (new conversation): `@FrameCore Works Creative Studio Skonfiguruj Studio.` Expected: Superpowers first; then Earshot in plain words with 1 Pełny (about 2.6 GB) / 2 Lekki (about 200 MB) / 3 Na razie bez; nothing installed before the answer. Answer `1`: Studio installs the full tier (plan, `--yes`, `fetch-models --yes`) and shows `status --json` with `ready_full`.

**4. Film test** (same conversation, attach the test `logo.mp4`, 6 s, 30 fps, title at 1.2 s, logo lands at 3.0 s): `@FrameCore Works Creative Studio W załączniku jest logo.mp4 (animacja logo, 6 s, 30 fps, bez dźwięku). Napis FRAMECORE wchodzi w 1,2 s, a logo ląduje w 3,0 s. Dodaj dźwięk: whoosh przy wejściu napisu i uderzenie, gdy logo ląduje. Chcę gotowy plik MP4 i sprawdzenie, czy dźwięk trafia w obraz.` Expected: effects from Earshot's bank chosen by listening (z values, rejected candidates), `timeline --cues` on the encoded MP4 with both cues within one frame, the engine named. The test film is also `tests/host-evals/fixtures/companion-logo.mp4`.

## For the next Claude Code session

- Superpowers in a cloud session: `/root/.claude/plugins/synced/.../skills/using-superpowers` (find with `find / -name using-superpowers -type d`). Host evals: `python3 scripts/host_eval.py --suite companion --cases <ids> --with-plugin <superpowers dir> --with-plugin plugins/earshot-audio --write` (paths are made absolute; set `EARSHOT_NATIVE_ROOT` to an empty folder for "engine missing" cases; at most 25 cases per pass, 5 per gate).
- Releases: commit first (clean tree), then `STUDIO_RELEASE_BRANCHES=<session branch> STUDIO_ORIGIN_AGENT=cloud-code STUDIO_COMMIT_TRAILERS=... python3 scripts/release.py prepare <ver> ... --push` and `publish <ver> --change-id ... --wait 3000 --push`; the notes heading must be exactly `# Creative Studio <version>`.
- The Earshot engine in a new container must be reinstalled (`plugins/earshot-audio/scripts/runtime.py install --tier full --yes`, `fetch-models --yes`), with the network hosts above allowed.
