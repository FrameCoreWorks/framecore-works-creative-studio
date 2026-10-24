# Creative Studio 1.130.0

Studio now looks for a skill in the open skills.sh catalog when a task needs something its own skills do not cover.

## What changed

Besides welcome option 3, Studio searches skills.sh by itself when a task needs a specific capability that no Studio skill or recommended extension covers. It offers at most three audited candidates once per need and asks one question: use once in this task, install, or continue without. A declined offer is not repeated. Using a skill once reads a listed skill's `SKILL.md` at a pinned commit, with its licence; Studio applies only its method and runs nothing from it. Skills that are not listed, contain an instruction override or pipe a download to a shell are refused. ChatGPT Work runs the search script in its sandbox without a lasting install; ordinary ChatGPT and the Claude apps search through the host's web search.

## What did not change

Startup, the welcome, routing, skill names and paths are unchanged; no path was removed. Installation still needs the user's answer, never uses `-y`, and is never offered for a blocked skill.

## Verification limits

The canonical validator and the full check suite passed, and `find_skills.py --read` is covered by stand-in tests. The live skills.sh catalog was unreachable from the container (proxy 403), so live catalog behaviour is not run, and ChatGPT, Work and Codex clients were not run. The hosted ChatGPT plugin update is pending.
