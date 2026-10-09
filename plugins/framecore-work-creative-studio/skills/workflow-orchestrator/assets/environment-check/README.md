# Environment check

One command that shows what Studio's tools can use in this environment, what is missing or out of date, and how to install it. It installs nothing.

```sh
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py            # dated snapshot of newest versions
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --online   # newest versions read now
```

Run it from the plugin root, or give the full path from anywhere. Options: `--json` for a machine-readable report, `--project DIR` to look for per-project packages (Remotion, GSAP) and project skills in that folder, `--browser PATH` to check a particular Chrome, `--strict` to exit 1 when a required tool is missing or below its minimum.

## What it checks

[`tools.json`](tools.json) lists every program and library the bundled tools and optional engines use: Python, Pillow, NumPy, CairoSVG (optional, for SVG logos), FFmpeg and FFprobe, Node.js and npx, Chrome or Chromium, Remotion and GSAP (per project), and HyperFrames (optional engine, its CLI and installed skills). Each entry has a minimum, the newest version known on its check date, where `--online` reads the current newest version (PyPI, npm, nodejs.org, endoflife.date, Chromium's stable channel) and install commands for Linux, macOS and Windows.

Each tool is reported as one of these:

| Status | Meaning |
| --- | --- |
| `ok` | Present, at or above the newest known version |
| `behind` | Present and working; a newer version exists |
| `below_minimum` | Present but too old for Studio's tools |
| `missing` | A required tool is not found |
| `not_installed` | An optional tool or engine is not found |
| `per_project` | Installed per project with `npm install`; the starter's pinned version is shown |
| `unknown` | Found, but its version could not be read |

It then reads the [capability card](../capability-card.json) and marks each capability `ready`, `missing` (with what is missing and what Studio delivers instead) or `unknown` (it depends on something only the host knows, such as network access or the user's browser). Installation commands come last, grouped into what is needed, what is optional and what could be updated.

## Tools by host

The fixed list of tools Studio's tools use, for every host the plugin runs in. The validator checks that every tool has a status for every host, and a test checks that this table equals `check_environment.py --matrix --markdown`.

<!-- BEGIN HOST MATRIX -->
| Tool | ChatGPT | ChatGPT Work | Codex | Claude Code | Claude apps |
| --- | --- | --- | --- | --- | --- |
| Python | observed | observed | install | install | check |
| Pillow (Python imaging) | observed | observed | install | install | check |
| NumPy | check | observed | install | install | check |
| CairoSVG (SVG logos in the renderer) | check | check | install | install | check |
| FFmpeg | observed | observed | install | install | check |
| FFprobe (comes with FFmpeg) | check | check | install | install | check |
| Node.js | check | check | install | install | check |
| npx (comes with Node.js) | check | check | install | install | check |
| Chrome or Chromium | check | check | install | install | check |
| Remotion (per project) | not_supported | not_supported | per_project | per_project | not_supported |
| GSAP (per project) | not_supported | not_supported | per_project | per_project | not_supported |
| HyperFrames (optional engine) | not_supported | not_supported | install | install | not_supported |
<!-- END HOST MATRIX -->

- **observed:** the owner reported it working on that host (the evidence is in `tools.json`); the check still runs before a file is promised.
- **check:** may be present in that host's code sandbox; only running the check shows it. Sandbox contents differ between accounts and change over time.
- **install:** the user's own machine (Codex, Claude Code); the check lists the install command when it is missing.
- **per_project:** installed into a project folder with `npm install`, which needs network.
- **not_supported:** that host cannot run it; Studio delivers the capability card's alternative (for example the bundled Python renderer instead of Remotion or HyperFrames).

`--host chatgpt|chatgpt_work|codex|claude_code|claude_apps` names the host; by default it is detected from documented traces (`CLAUDECODE=1`, a `CODEX_` variable, `/mnt/user-data`, `/mnt/data`), and ordinary ChatGPT and ChatGPT Work cannot be told apart that way. `/mnt/user-data` also exists in Claude Code cloud sessions, which are recognised first by `CLAUDECODE=1`; pass `--host` when the detection is wrong. On a named host a tool marked `not_supported` is reported as `not_on_this_host`, not as missing.

## How Studio uses it

- **After installation.** The repository's Codex, ChatGPT Work and Claude installation guides (`CODEX_INSTALL.md`, `CHATGPT_INSTALL.md`, `CLAUDE_INSTALL.md`) run it once after the plugin is saved and show the user the result.
- **On request.** "Check my environment", "what is installed", "sprawdź środowisko" and similar requests run it where code runs; Studio answers in the user's language with the capabilities first and the install steps second.
- **Before the first coded render.** Where a task needs FFmpeg, Node.js or a browser and nothing in the conversation shows they work, one run replaces probing tool by tool.
- **No code execution.** Studio cannot check the environment; it gives the install list from `tools.json` for the user's system and says nothing was checked.

## Installing

The check prints commands; it never runs them. Installing changes the user's system and downloads software, so Studio runs an install step only when the user asks for it in a host that allows it, one step at a time, and reruns the check afterwards. In ChatGPT's code execution, installs (where allowed at all) last only for that sandbox session. HyperFrames is installed only on the user's request, as its [engine reference](../../../hyperframes-workflow/references/hyperframes-engine.md) describes; `npx hyperframes@0.8.143 doctor` then checks its own needs in more depth.

## Keeping it current

`tools.json` has a `checked` date. When a tool's minimum changes, a tool is added to a skill, or the newest versions are refreshed, update `tools.json` in the same release; the validator checks that each tool maps to a requirement or capability of the capability card and that every checkable requirement has a tool.
