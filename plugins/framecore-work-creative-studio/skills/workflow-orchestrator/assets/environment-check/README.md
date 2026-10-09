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

## How Studio uses it

- **After installation.** The repository's Codex and ChatGPT Work installation guides (`CODEX_INSTALL.md`, `CHATGPT_INSTALL.md`) run it once after the plugin is saved and show the user the result.
- **On request.** "Check my environment", "what is installed", "sprawdź środowisko" and similar requests run it where code runs; Studio answers in the user's language with the capabilities first and the install steps second.
- **Before the first coded render.** Where a task needs FFmpeg, Node.js or a browser and nothing in the conversation shows they work, one run replaces probing tool by tool.
- **No code execution.** Studio cannot check the environment; it gives the install list from `tools.json` for the user's system and says nothing was checked.

## Installing

The check prints commands; it never runs them. Installing changes the user's system and downloads software, so Studio runs an install step only when the user asks for it in a host that allows it, one step at a time, and reruns the check afterwards. In ChatGPT's code execution, installs (where allowed at all) last only for that sandbox session. HyperFrames is installed only on the user's request, as its [engine reference](../../../hyperframes-workflow/references/hyperframes-engine.md) describes; `npx hyperframes@0.8.143 doctor` then checks its own needs in more depth.

## Keeping it current

`tools.json` has a `checked` date. When a tool's minimum changes, a tool is added to a skill, or the newest versions are refreshed, update `tools.json` in the same release; the validator checks that each tool maps to a requirement or capability of the capability card and that every checkable requirement has a tool.
