# Handover for ChatGPT Work (GPT Astra), 2026-10-20 (package 1.98.0)

## Closure update, 2026-10-20, version 1.111.1

This update supersedes the historical state and hosted-update rule below. The interrupted audit, recovered fixes, source/synthetic-media tests, routing corrections, release provenance and paired publication are complete. The release is `addf23e7`; the existing private plugin is saved as `pluginrel_6ad76a03ef2081919bf42aed344dc562` with all 1543 files read back and its private integrations preserved. See [the closure report](reviews/audit-closure-2026-10-20.md), [publication](../verification/github-publication-1.111.1.json) and [hosted synchronization](../verification/hosted-sync-1.111.1.json).

Task 1 remains fixed at three workflow runs. Tasks 2/2b have retained source and sandbox evidence; fresh ordinary-ChatGPT/client behavior remains NOT_RUN. The missing historical 43-case report is not reused. The 14 prompt exercises are recorded separately with their source-only limits. Optional task 3 still needs an explicit request and client media. Task 4 is the next feature task and has not been implemented. Read the latest owner overrides in AGENTS.md before any new update, especially main-only publication and preserving the hosted overlay.

Cloud Code's weekly limit is spent until Saturday. The owner continues on ChatGPT Work with the GPT Astra model. Read [AGENTS.md](../AGENTS.md), [handover-codex-2026-10-19.md](handover-codex-2026-10-19.md), the latest entries of [development-ledger.md](development-ledger.md) and `git log -10` before writing. Reply to the owner in Polish; direct, no em dashes, facts separated from inferences and unknowns.

## State (facts)

- `main` carries 1.98.0 (`d06ac7d` records the publication; release commit `da84cdd`, tag `v1.98.0`). Release, notes and check workflows were green. ChatGPT Work is `not_tracked`; Codex sync is `not_run`.
- 1.98.0 added earshot (MIT, Leon Lin, pinned `925ebe5`): native listening tools `skills/hyperframes-workflow/assets/sound-listen/listen.py` and `place_sfx.py`, the reference `skills/hyperframes-workflow/references/sound-listening-and-motion-sfx.md`, the registry entry `earshot` (light tier and full tier), `integrations/earshot/`, capability card entries `sound_listen` and `sound_place`, test `tests/sound_listen_test.py` and host-eval case AD14.
- No host test has run on 1.91.0 to 1.98.0 (owner decision). Source checks are not host behavior.

## Task 1: fix the `publish` default

`scripts/release.py publish` waits for `--min-runs` workflow runs on the release commit, default 3. Since releases push only `main` (branch hygiene rule), a release has 3 runs (Refresh current release notes, Publish verified Studio release, Check Studio sources). The previous default exceeded that count, so `publish` waited its full `--wait` and failed unless `--min-runs 3` was passed. Task 1 aligns the default with the three-run release route; an explicit override remains available.

1. Keep the default at 3 at `q.add_argument('--min-runs', ...)` and keep the operational description in sync.
2. Run the canonical validator and `bash scripts/check_all.sh`; this is a non-package change (`Shared-Package-Changed: no`), so no release steps.
3. Commit with the required trailers, add a ledger entry, fast-forward push to `main`.

## Task 2: test in your own sandbox (corrected)

`scripts/host_eval.py` drives the Claude Code CLI (`claude -p`), which ChatGPT Work does not have, so do not run it. Instead test in the ChatGPT Work sandbox: run `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs` and `bash scripts/check_all.sh`, run the new tools on synthetic or owner-supplied media (`sound_listen_test.py`, `listen.py`, `place_sfx.py`), and try the 14 requests in `tests/host-evals/additions.json` (AD01 to AD14) by hand as ordinary ChatGPT Work prompts, checking against each case's rubric. Report results as facts (what ran, what passed or failed, the client and reasoning setting); owner-reported success is `PASS_REPORTED`; nothing you did not run is a pass.

## Task 2b: develop further and check orchestration

Look for defects and inconsistencies in orchestration: routing rows against `routing-boundaries.md`, skill descriptions and the 7,800-character budget, links between owners, capability card against runtime map, registry entries against their hosts, duplicated or conflicting rules. Fix the smallest cause first; list larger design questions for the owner as numbered options.

## Attribution (owner instruction)

Mark your work so the division of labour is visible: commit trailers `Origin-Agent: chatgpt-work`, a ledger entry with origin `chatgpt-work`, and `Co-authored-by` or contributor attribution for the GPT Astra session where the host provides it. Do not reuse `cloud-code` as origin. Change IDs: `CW-YYYYMMDD-NN`. Keep the other trailers from AGENTS.md.

## Task 4 (owner request, after the above): Reel Editing Assistant

See [task-reel-editing-assistant-2026-10-20.md](task-reel-editing-assistant-2026-10-20.md): an analysis of two paid AI reel-editing offers against Studio and a work order for a native assistant (rough cut of raw footage, captions, overlays, style profile).

## Optional task 3 (only if the owner asks)

Lay the earshot bank samples on the Knock Knock reel cuts with `place_sfx.py` and compare with the sound designed by `sound.py` using `listen.py critique` and `ab`. The client's files are not in the repository; the owner must supply them.

## Rules that matter here

- Never delete, rename or move a path in the shared package; retire files with stubs.
- Studio is a general product: nothing personalised to one user.
- Do not commit third-party audio or lyrics; do not download copyrighted songs.
- earshot's audio-LLM critique uploads audio; run it only with the user's own key and an explicit yes.
- Keep the startup welcome byte-identical to its assets.
- Branch hygiene: develop on a local working branch, push only `main` (fast-forward, no force), `gh-pages` and a session branch the host requires.
- After a shared-package release, give the owner only the short Plugin Creator prompt (source commit, no readback) and record ChatGPT Work as `not_tracked`.

## Known limits of the native listening tools

Native band levels, onset density and tempo approximate earshot's (earshot is the reference). The scorecard ranges come from seven SaaS launch films; use `listen.py profile` for other genres. A passing scorecard is not a good film. Neural commands need the `earshot` extension full tier, which does not run in chat sandboxes.
