# Environment check

One command that shows whether the one required set of tools Studio uses is present, what is missing or out of date, and how to install it. It installs nothing. At installation it is the final check: the installation is complete only when it passes.

```sh
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host codex   # final check of an installation
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --online              # newest versions read now
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --matrix              # every tool on every host
```

Run it from the plugin root, or give the full path from anywhere. Options: `--host` names the host, `--workspace DIR` the Studio workspace (default `~/.framecore-studio/workspace`, or `FRAMECORE_STUDIO_WORKSPACE`), `--json` gives a machine-readable report, `--project DIR` also searches that folder's skills for HyperFrames, `--browser PATH` checks a particular Chrome, `--strict` exits 1 when a tool fails.

## The required set

Every tool in [`tools.json`](tools.json) is required; there are no optional tools. Each entry has a minimum where one applies, the newest version known on its check date (`--online` reads the current one from PyPI, npm, nodejs.org, endoflife.date or Chromium's stable channel) and install commands for Linux, macOS and Windows.

- **System:** Python 3.9 or newer, FFmpeg with FFprobe, Node.js 20 or newer with npx (22 for HyperFrames), Chrome or Chromium.
- **Python packages:** Pillow 9 or newer, NumPy 1.22 or newer, CairoSVG (with the Cairo library), imageio-ffmpeg, matplotlib and Manim Community (with Cairo and Pango). A virtual environment keeps them together; run the check with that environment's Python.
- **Studio workspace:** the four starters copied from the plugin into the workspace and installed with `npm ci` from their lockfiles, so every package is at exactly the pinned version: the Remotion kinetic type starter (Remotion, React, TypeScript), the GSAP motion starter, the Remotion 3D example (Three.js, React Three Fiber) and the motion toolkit (PixiJS, d3-scale, Mediabunny, lottie-web, esbuild). The check prints the copy and `npm ci` commands with the plugin's real path.
- **HyperFrames:** its CLI or installed skills (its own Codex or Claude Code plugin, or `npx hyperframes@0.8.143 skills update`). The HeyGen catalog stays off unless the user asks for it.

Each tool is reported as one of these:

| Status | Meaning |
| --- | --- |
| `ok` | Present, at or above the newest known version; a workspace starter has every package at its lockfile version |
| `behind` | Present and working; a newer version exists |
| `below_minimum` | Present but too old for Studio's tools |
| `missing` | Not found, or a workspace starter is not installed or misses packages |
| `wrong_version` | A workspace package differs from the lockfile; run `npm ci` in that folder |
| `not_on_this_host` | On a named host that cannot run it (a chat sandbox for npm or HyperFrames) |
| `unknown` | Found, but its version could not be read |

It then reads the [capability card](../capability-card.json) and marks each capability `ready`, `missing` (with what is missing and what Studio delivers instead) or `unknown` (it depends on something only the host knows, such as network access or the user's browser). Installation commands come last.

## Final check at installation

`--final` decides whether an installation is complete. The required set is every tool the host can run (the matrix below; tools marked `not_supported` for the host are excluded and listed):

| Verdict | Exit code | Meaning |
| --- | --- | --- |
| `pass` | 0 | Every required tool is usable; the installation is complete |
| `fail` | 1 | On Codex or Claude Code, something is missing, too old or of another version; install it with the printed commands and run the final check again |
| `limited` | 3 | In a chat sandbox (ChatGPT, ChatGPT Work, Claude apps) something is missing that the user cannot install there; the plugin is installed, and Studio names these limits and uses the capability card's alternatives |
| `unknown_host` | 2 | The host was not detected; name it with `--host` |

The installation guides (`CODEX_INSTALL.md`, `CHATGPT_INSTALL.md`, `CLAUDE_INSTALL.md`) end with this check and report its verdict.

## Tools by host

The required set, for every host the plugin runs in. The validator checks that every tool has a status for every host, and a test checks that this table equals `check_environment.py --matrix --markdown`.

<!-- BEGIN HOST MATRIX -->
| Tool | ChatGPT | ChatGPT Work | Codex | Claude Code | Claude apps |
| --- | --- | --- | --- | --- | --- |
| Python | observed | observed | install | install | check |
| Pillow (Python imaging) | observed | observed | install | install | check |
| NumPy | check | observed | install | install | check |
| CairoSVG (SVG logos in the renderer) | check | check | install | install | check |
| imageio-ffmpeg (bundled FFmpeg for the renderer) | check | check | install | install | check |
| matplotlib (font fallback for the renderer) | check | check | install | install | check |
| Manim Community (mathematical animation) | check | check | install | install | check |
| FFmpeg | observed | observed | install | install | check |
| FFprobe (comes with FFmpeg) | check | check | install | install | check |
| Node.js | check | check | install | install | check |
| npx (comes with Node.js) | check | check | install | install | check |
| Chrome or Chromium | check | check | install | install | check |
| Remotion kinetic type starter (Remotion, React, TypeScript) | not_supported | not_supported | per_project | per_project | not_supported |
| GSAP motion starter | not_supported | not_supported | per_project | per_project | not_supported |
| Remotion 3D example (Three.js, React Three Fiber) | not_supported | not_supported | per_project | per_project | not_supported |
| Motion toolkit (PixiJS, d3-scale, Mediabunny, lottie-web, esbuild) | not_supported | not_supported | per_project | per_project | not_supported |
| HyperFrames (engine) | not_supported | not_supported | install | install | not_supported |
<!-- END HOST MATRIX -->

- **observed:** the owner reported it working on that host (the evidence is in `tools.json`); the check still runs before a file is promised.
- **check:** may be present in that host's code sandbox; only running the check shows it. Sandbox contents differ between accounts and change over time.
- **install:** the user's own machine (Codex, Claude Code); the check lists the install command when it is missing.
- **per_project:** installed into the Studio workspace with `npm ci`, which needs network once.
- **not_supported:** that host cannot run it; Studio delivers the capability card's alternative (for example the bundled Python renderer instead of Remotion or HyperFrames).

`--host chatgpt|chatgpt_work|codex|claude_code|claude_apps` names the host; by default it is detected from documented traces (`CLAUDECODE=1`, a `CODEX_` variable, `/mnt/user-data`, `/mnt/data`), and ordinary ChatGPT and ChatGPT Work cannot be told apart that way. `/mnt/user-data` also exists in Claude Code cloud sessions, which are recognised first by `CLAUDECODE=1`; pass `--host` when the detection is wrong. On a named host a tool marked `not_supported` is reported as `not_on_this_host`, not as missing.

## How Studio uses it

- **At installation.** The repository's Codex, ChatGPT Work and Claude installation guides (`CODEX_INSTALL.md`, `CHATGPT_INSTALL.md`, `CLAUDE_INSTALL.md`) end with the final check and report its verdict.
- **On request.** "Check my environment", "what is installed", "sprawdź środowisko" and similar requests run it where code runs; Studio answers in the user's language with the capabilities first and the install steps second.
- **Before the first coded render.** Where a task needs FFmpeg, Node.js or a browser and nothing in the conversation shows they work, one run replaces probing tool by tool.
- **No code execution.** Studio cannot check the environment; it gives the install list from `tools.json` for the user's system and says nothing was checked.

## Installing

The check prints commands; it never runs them. Installing changes the user's system and downloads software: the user runs the printed commands, or asks the assistant to run them where the host allows it, and then runs the final check again. In a chat sandbox, installs (where allowed at all) last only for that session, so the final check there can end `limited`. HyperFrames is part of the required set on Codex and Claude Code, as its [engine reference](../../../hyperframes-workflow/references/hyperframes-engine.md) describes; `npx hyperframes@0.8.143 doctor` then checks its own needs in more depth.

## Keeping it current

`tools.json` has a `checked` date. When a tool's minimum changes, a tool is added to a skill, or the newest versions are refreshed, update `tools.json` in the same release; the validator checks that each tool maps to a requirement or capability of the capability card and that every checkable requirement has a tool.
