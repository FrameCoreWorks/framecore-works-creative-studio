# Host evaluations in Claude Code

`scripts/host_eval.py` runs Studio in a real host: headless Claude Code (`claude -p`) with the plugin loaded from this source tree, one fresh empty workspace and an isolated configuration per case, later turns resumed in the same session. It complements the [host smoke set](host-smoke-set.md), which a person runs in ChatGPT and ChatGPT Work. A record is evidence for Claude Code on the machine and model that ran it; it does not establish ChatGPT, ChatGPT Work or Claude apps behaviour.

```sh
python3 scripts/host_eval.py --list                     # the cases; runs nothing
python3 scripts/host_eval.py --gate --write             # release-gate subset (5 cases)
python3 scripts/host_eval.py --write                    # the whole suite (21 cases)
python3 scripts/host_eval.py --cases W04,S01 --judge    # chosen cases with the advisory judge
python3 scripts/host_eval.py --suite routing --write    # the Polish routing set (25 cases)
```

## How a case is judged

The suite is [tests/host-evals/suite.json](../tests/host-evals/suite.json). A case is a list of turns, each with deterministic checks: the welcome byte-identical to its asset, no welcome, the language, the number of questions put to the user (outside list items and quoted copy), list items, numbered options, the skills loaded, the files read (`reads_any`, which also accepts a profile reference such as the teacher or brand profile), commands run or not run, text present or absent. Cases with a `source` take the user request and the rubric from the package evals (`plugins/.../evals/*.json`); `prefix` adds the Studio name the way a Claude Code user addresses the plugin. Checks alone decide PASS or FAIL. `--judge` adds a second, cheaper model that grades the reply against the case's rubric; it is advisory and never changes a verdict.

The [routing set](../tests/host-evals/routing.json) (`--suite routing`) holds 25 real-style Polish requests, nine addressed to Studio by name and sixteen not, each checked by the owner the host loaded; `no_skills` marks the wrong side of a known collision (image prompt, product video entry points, supplied-video review, service businesses). It measures routing, not quality: a small task answered well without loading its owner still fails there.

Every record in [verification/host-evals/](../verification/host-evals/) states the package version, source commit, Claude Code version, model, allowed tools, each reply (up to 6,000 characters) with its SHA-256, the skills and tools used, the tokens and the time. A failed case is reviewed before anything is changed: a harness defect is fixed in the harness, a case that does not apply to the host is rewritten with the reason in `host_note`, and a product finding is fixed in the package and rerun. The review is written into the record.

## Plan usage

Runs use the usage of the Claude plan the session runs on; they are not billed separately. Owner decision 2026-10-11 (1a, 2a): runs go ahead without asking, at most 25 cases per pass and 5 for the release gate; the script stops at that limit (`--max-cases` changes it only on the owner's request) and records the cases, tokens and time. `--turn-budget-usd` is only a runaway stop for one turn, passed to Claude Code in its API-price scale.

The dollar figures in the results below, for runs up to 2026-10-11, are what Claude Code reported as the API-price equivalent of the tokens (`total_cost_usd`); they were not charges. Later records carry tokens and time instead.

## Results

| Date | Package | Cases | Result | Usage | Record |
| --- | --- | --- | --- | --- | --- |
| 2026-10-10 | 1.55.0 | 15 | 12 PASS, 3 FAIL: one harness defect (D01), one case not applicable as written (LM01, no Studio name), one product finding (S01, two questions after offering directions) | USD 1.68 | [suite](../verification/host-evals/2026-10-10-1.55.0-suite.json) |
| 2026-10-10 | 1.56.0 candidate | 3 | D01, LM01 (with the Studio name) and S01 PASS after the fixes | USD 0.26 | [rerun](../verification/host-evals/2026-10-10-1.56.0-candidate-LM01-D01-S01.json) |
| 2026-10-10 | 1.57.0 candidate | 2 (new: Q01 offer from given rates, Q02 what to charge) | first run: Q01 hit the turn cap (harness), Q02 stated unsourced market ranges (product finding); after the routing fix and a 20-turn cap both PASS | USD 0.22 + 0.26 | [first](../verification/host-evals/2026-10-10-1.57.0-candidate-Q01-Q02-first.json), [after](../verification/host-evals/2026-10-10-1.57.0-candidate-Q01-Q02.json) |
| 2026-10-11 | 1.63.0 | 25 (routing set) | 23 PASS, 2 FAIL: RT01 and RT08, short requests without the Studio name answered without loading a skill (routing finding); every collision case on the intended side | USD 2.42 | [routing](../verification/host-evals/2026-10-11-1.63.0-routing.json) |
| 2026-10-11 | 1.64.0 candidate | 9 (routing set, cases naming Studio) | 9 PASS on the single route table, the same owners as on 1.63.0 | USD 0.91 | [rerun](../verification/host-evals/2026-10-11-1.64.0-candidate-routing-named.json) |
| 2026-10-11 | 1.65.0 candidate | 4 (new: M02 storyboard only, M03 Veo prompts, M04 MP4 without code execution, M05 three stills) | 3 PASS, 1 FAIL: M04 stayed on the coded route but asked only for a shell instead of naming the motion player route (product finding) | 206,032 tokens, 75 s | [run](../verification/host-evals/2026-10-11-1.65.0-candidate-M02-M05.json) |
| 2026-10-11 | 1.65.0 candidate, M04 reruns | 2 | after two wordings of the fix: one reply passed the check only by naming the contract while promising a render it could not do (not counted), then FAIL; open finding: Studio promises an MP4 before checking that it can run code | 118,405 tokens, 36 s | [second](../verification/host-evals/2026-10-11-1.65.0-candidate-M04-second.json), [third](../verification/host-evals/2026-10-11-1.65.0-candidate-M04-third.json) |
| 2026-10-11 | ChatGPT Work, by the owner | 1 (M04 by hand) | PASS_REPORTED: stayed on the coded route and asked only for the logo; code execution is available there, so the no-code finding above is not covered | not measured | [report](../verification/host-report-2026-10-11-m04-chatgpt-work.json) |
