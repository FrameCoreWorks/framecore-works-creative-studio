# Handover for ChatGPT Work (GPT Astra), 2026-10-20 (package 1.98.0)

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

## Task 2: run the additions host-eval suite

`python3 scripts/host_eval.py --suite additions` (14 Polish requests AD01 to AD14; AD14 is the sound check of a finished reel). The owner approved paid runs within about USD 1 per release-gate subset and USD 2 to 4 per full pass; record the cost with the run. Report which cases fail and why (`reads_any` and `skills_any` show whether the host reached the right file or owner). Fix routing or wiring defects with the smallest change; a fix to the shared package needs the release procedure in the Codex handover. Record the tested client and reasoning setting; `PASS_REPORTED` only for owner-reported success.

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
