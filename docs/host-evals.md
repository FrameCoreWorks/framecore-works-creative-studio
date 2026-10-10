# Host evaluations in Claude Code

`scripts/host_eval.py` runs Studio in a real host: headless Claude Code (`claude -p`) with the plugin loaded from this source tree, one fresh empty workspace and an isolated configuration per case, later turns resumed in the same session. It complements the [host smoke set](host-smoke-set.md), which a person runs in ChatGPT and ChatGPT Work. A record is evidence for Claude Code on the machine and model that ran it; it does not establish ChatGPT, ChatGPT Work or Claude apps behaviour.

```sh
python3 scripts/host_eval.py --list                     # the cases; spends nothing
python3 scripts/host_eval.py --gate --write             # release-gate subset (5 cases, about USD 0.6)
python3 scripts/host_eval.py --write --budget-usd 4     # the whole suite (15 cases, about USD 1.7)
python3 scripts/host_eval.py --cases W04,S01 --judge    # chosen cases with the advisory judge
```

## How a case is judged

The suite is [tests/host-evals/suite.json](../tests/host-evals/suite.json). A case is a list of turns, each with deterministic checks: the welcome byte-identical to its asset, no welcome, the language, the number of questions put to the user (outside list items and quoted copy), list items, numbered options, the skills loaded, commands run or not run, text present or absent. Cases with a `source` take the user request and the rubric from the package evals (`plugins/.../evals/*.json`); `prefix` adds the Studio name the way a Claude Code user addresses the plugin. Checks alone decide PASS or FAIL. `--judge` adds a second, cheaper model that grades the reply against the case's rubric; it is advisory and never changes a verdict.

Every record in [verification/host-evals/](../verification/host-evals/) states the package version, source commit, Claude Code version, model, allowed tools, each reply (up to 6,000 characters) with its SHA-256, the skills and tools used, the cost and the time. A failed case is reviewed before anything is changed: a harness defect is fixed in the harness, a case that does not apply to the host is rewritten with the reason in `host_note`, and a product finding is fixed in the package and rerun. The review is written into the record.

## Cost

The owner approved paid runs on 2026-10-10 (decision 2a): about USD 2 to 4 for a full pass and under USD 1 for the release gate. Measured on 2026-10-10 with Claude Code 2.1.296 and `claude-sonnet-5-5`: USD 0.06 to 0.21 per case, USD 1.68 for the 15-case suite. The script stops before a case once `--budget-usd` is spent and caps each turn with `--turn-budget-usd`.

## Results

| Date | Package | Cases | Result | Cost | Record |
| --- | --- | --- | --- | --- | --- |
| 2026-10-10 | 1.55.0 | 15 | 12 PASS, 3 FAIL: one harness defect (D01), one case not applicable as written (LM01, no Studio name), one product finding (S01, two questions after offering directions) | USD 1.68 | [suite](../verification/host-evals/2026-10-10-1.55.0-suite.json) |
| 2026-10-10 | 1.56.0 candidate | 3 | D01, LM01 (with the Studio name) and S01 PASS after the fixes | USD 0.26 | [rerun](../verification/host-evals/2026-10-10-1.56.0-candidate-LM01-D01-S01.json) |
