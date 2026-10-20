# Environment check

Use `check_environment.py` at the first installation, after **every** plugin update, on an environment request, and when a new/reset runtime invalidates previous observations. The complete inventory is [runtime-tools.json](runtime-tools.json): 59 individually checked components from the owner's 2026-10-20 list. The supplied versions are a **reported working Work configuration**, not newest releases, minimum versions or a mandate to downgrade other installations.

```sh
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host chatgpt_work --json
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --update --host codex --json
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host claude_code --json
```

Use `--host claude_apps` for an actual Claude app code sandbox, not Claude Code; `--host chatgpt` is ordinary ChatGPT. A product name does not establish execution, network, install permissions, OS or architecture. Without an executable environment, report **Unknown / not checked**, give the planned list and do not invent results. A saved plugin package and its tools' current installation state are separate facts. Work sandbox installs may need restoring in a later session.

## Final check at installation

1. Run the complete inventory in the target environment. `ok` means the named installation evidence passed, not that a full creative job/render/inference ran. Each record includes the detected version, location/environment, reference comparison and evidence level. npm packages require real payload in addition to metadata; Python packages must import; binaries execute a version command; models match their pinned public asset hash.
2. Present a short list in the user's language: **confirmed installed**, **missing**, **broken**, **Unknown**, then **tools planned for installation**. Name each tool's purpose, environment, downloads and permissions. Do not say it has been installed from this plan. A different working version is listed separately and is not automatically replaced.
3. Reuse existing authorization when it covers the disclosed tool installation. A check-only request does not authorize installation. If only the plugin save was authorized, ask once for the concrete missing-tools plan. Do not ask again after that scope is authorized. Do not connect paid providers or publish client files as part of tool setup.
4. Before executing the plan, resolve actual OS, architecture, interpreter ABI and package availability. Prefer existing managed runtime restore mechanisms when present; otherwise use the isolated recipes below. Keep working environments and project lockfiles intact. If a target build cannot be installed, name that blocker and a compatible alternative for the user to choose; do not silently substitute a different engine.
5. Rerun the complete check after installation. Report what actually passed and what remains blocked. Installation is complete only when the required components have installation evidence. A pass is **not** proof of host skill routing, an end-to-end render or subjective media quality.

| Verdict | Exit code with `--final`, `--update` or `--strict` | Meaning |
| --- | --- | --- |
| `pass` | 0 | All 59 components have installation evidence; no detected Remotion family conflict |
| `fail` | 1 | Shell host has missing, broken or unverified components |
| `unknown_host` | 2 | Supply the actual host; it was not established |
| `limited` | 3 | Sandbox inventory is incomplete; name the findings and installation capability/blocker |

`limited` does not mean tools are categorically impossible in Work or Claude apps. No component is excluded merely because of the host's product name. Models and Python wrappers are separate rows. Whisper tiny must be multilingual; `tiny.en` is not a substitute. Tesseract, pytesseract and Polish tessdata_fast are separate checks. FFmpeg, FFprobe and the imageio fallback are separate rows. Animate's browser and the browser for other renders are separately reported.

## Update check after a plugin update

`--update` repeats exactly the full installation inventory, **offline by default**. Recheck even if the previous version passed: sessions, caches, interpreter environments or model files may have changed. Show only missing/broken items as installation/repair candidates. Unknown identity or a failed probe needs verification first. Preserve working versions; explain differences from the reported configuration and inspect project lockfiles before an upgrade. Remotion packages with inconsistent versions require compatibility review, not automatic replacement.

Do not confuse installing the plugin with installing engines or launching an npm download. The checker never invokes an installer, fetches a model, starts inference or runs a paid provider. It does not run `npx` to fetch an absent package. `--online` is retained only for the explicit legacy diagnostic (`--capabilities-only --online`); it is not part of normal updates.

## Discovery and isolated environments

- The active Python and discoverable managed Python environments are checked separately. Manim and Blender interpreter rows are tied to environments that import those engines. `--python-env /absolute/path/to/python` can be repeated. `FRAMECORE_PYTHON_ENVS`, `FRAMECORE_MANIM_PYTHON`, `FRAMECORE_BLENDER_PYTHON` and `FRAMECORE_MANIM_PREFIX` also identify actual environments. Never install bpy into an incompatible active Python just because the plugin runs there.
- `--node-root /absolute/path/to/node_modules` can be repeated. The project, Studio workspaces, declared Node module roots, managed motion caches and global npm root are inspected without installation. The selected path is reported; other detected versions are retained in the record. npm-file evidence does not certify a browser import or rendering.
- Use `--workspace DIR` / `FRAMECORE_STUDIO_WORKSPACE` for project environments. `FRAMECORE_MEDIA_HOME` and `FRAMECORE_MOTION_HOME` identify existing managed caches. `FRAMECORE_ANIMATE_ROOT` identifies an installed Animate source tree. Runtime paths may vary by platform: pass an explicit path when discovery cannot see one.
- `--browser`, `CHROME_PATH` and `HYPERFRAMES_BROWSER_PATH` select the other-render browser. `FRAMECORE_ANIMATE_BROWSER` selects Animate's browser; Playwright's reported executable path is also checked. Version output proves an executable installation, not driver/browser render compatibility.
- `FRAMECORE_WHISPER_MODEL` points to the multilingual GGML tiny file. `FRAMECORE_TESSDATA_POL` points to `pol.traineddata`; `TESSDATA_PREFIX` points to a tessdata directory. Hash mismatches are Unknown and preserved, not automatically deleted or replaced.

## Installation recipes

These are plans for the assistant to resolve against the actual host, not commands executed by the checker. Inspect existing managed runtime installers first and use their read-only status before any restore.

| Components | Installation route |
| --- | --- |
| Python libraries | Create a dedicated venv with a compatible interpreter, then install the catalog's distribution and reported version there. Keep Blender bpy in its compatible Python environment; keep Manim and native dependencies together. Pass the resulting interpreter to the check. |
| Python runtimes | Use an available user-managed interpreter tool such as uv or Micromamba, respecting host permissions; do not replace the host's Python. The reported setup uses 3.12.14 general, 3.12.15 Manim and 3.13.16 bpy. Verify wheels/ABI before downloads. |
| npm libraries and HyperFrames | Use a dedicated project/runtime directory and compatible Node; install a coherent set from its reviewed lockfile or explicit catalog pins. Use `npm ci` only for a verified matching lockfile. Do not overwrite a project lockfile or run an unqualified `npx` probe. |
| Animate | Restore the existing managed engine when available, or copy bundled pinned Animate source into a new workspace; install its pinned Playwright dependency and that driver's browser under the installation authorization. Preserve existing edited source. |
| FFmpeg/FFprobe, ImageMagick, Inkscape, Tesseract, Cairo/Pango, LaTeX/dvisvgm, Typst | Use the host OS package manager or a managed toolchain appropriate to OS/architecture. List admin/download requirements. System repository versions may differ from Work's reported versions; verify the actual installation. |
| Auto-Editor / DeepFilterNet | Use the official release matching the platform or the existing managed runtime. Do not confuse a Python wrapper with the standalone executable. Preserve and verify the executable's version. |
| Whisper tiny / Polish OCR data | Download the exact public asset URL in the catalog only under installation authorization, verify SHA-256, then expose its local path to the checker. A hash mismatch is a blocker. |

Sources: [Manim installation](https://docs.manim.community/en/stable/installation/uv.html), [official bpy distribution](https://pypi.org/project/bpy/), [PyWhisperCpp](https://github.com/absadiki/pywhispercpp), [Tesseract data files](https://tesseract-ocr.github.io/tessdoc/Data-Files.html). Source review: 2026-10-20. These references explain installation requirements; they do not establish successful installation on another host.

## Retained project capability diagnostic

`--capabilities-only` runs the older `tools.json` diagnostic for the capability card and exact starter lockfiles. It remains useful for a particular copied project; it is **not** the complete installation/update inventory. Its optional `--online` query reads registry versions. `--matrix` below is that legacy project's host guidance, not measured runtime availability. Normal/default checks use the complete catalog above.

## Tools by host

<!-- BEGIN HOST MATRIX -->
| Tool | ChatGPT | ChatGPT Work | Codex | Claude Code | Claude apps |
| --- | --- | --- | --- | --- | --- |
| Python | observed | observed | install | install | check |
| Pillow (Python imaging) | observed | observed | install | install | check |
| NumPy | check | observed | install | install | check |
| CairoSVG (SVG logos in the renderer) | check | check | install | install | check |
| fontTools (font outlines) | check | check | install | install | check |
| imageio-ffmpeg (bundled FFmpeg for the renderer) | check | check | install | install | check |
| matplotlib (font fallback for the renderer) | check | check | install | install | check |
| Manim Community (mathematical animation) | check | check | install | install | check |
| FFmpeg | observed | observed | install | install | check |
| FFprobe (comes with FFmpeg) | check | check | install | install | check |
| Node.js | check | observed | install | install | check |
| npx (comes with Node.js) | check | observed | install | install | check |
| Chrome or Chromium | check | observed | install | install | check |
| Remotion kinetic type starter (Remotion, React, TypeScript) | not_supported | check | per_project | per_project | check |
| GSAP motion starter | not_supported | check | per_project | per_project | check |
| Remotion 3D example (Three.js, React Three Fiber) | not_supported | check | per_project | per_project | check |
| Remotion glTF product turntable | not_supported | check | per_project | per_project | check |
| Motion toolkit (PixiJS, d3-scale, Mediabunny, lottie-web, esbuild) | not_supported | check | per_project | per_project | check |
| Animate engine (procedural canvas films, Playwright) | not_supported | check | per_project | per_project | check |
| HyperFrames (engine) | not_supported | install | install | install | not_supported |
<!-- END HOST MATRIX -->
