# Maintaining the repository

For people who change or package Studio. Users install it with the guides linked from the [README](../README.md).

## Repository layout

| Path | Purpose |
|---|---|
| `CHATGPT_INSTALL.md`, `CODEX_INSTALL.md`, `CLAUDE_INSTALL.md` | Complete environment-specific installation procedures |
| `.claude-plugin/marketplace.json` | Claude plugin marketplace: Studio and its companions |
| `plugins/voice-narration/`, `plugins/brand-kit/` | Companion plugins: measured voice-overs, brand kit from a website (install steps in the guides above) |
| `CHATGPT_UPDATE.md`, `CODEX_UPDATE.md` | Existing-entry updates preserving user changes |
| `config/install-sources.json` | Complete plugin file inventory with SHA-256 hashes |
| `scripts/install_codex.py` | Native Codex entry and intact backing bundle |
| `plugins/framecore-work-creative-studio/` | Canonical portable plugin and compatibility manifest |
| `plugins/framecore-work-creative-studio/skills/` | Active skill entrypoints and supporting material |
| `plugins/framecore-work-creative-studio/integrations/` | Pinned source bundles and provenance |
| `plugins/framecore-work-creative-studio/docs/` | Scope, source mapping and verification history |
| `scripts/package_release.py` | Local ZIP packaging and SHA-256 inventories |
| `LICENSE_STATUS.md` | Approved licensing scope |

## Verify and package

Run from the repository root with Node.js and Python 3 available:

```sh
node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs
bash scripts/check_all.sh
python3 scripts/build_install_manifest.py
python3 scripts/package_release.py
```

`scripts/check_all.sh` runs every current check, the same list as the release and checks workflows; with numpy, Pillow and ffmpeg installed (`requirements-ci.txt` and the system ffmpeg) it also runs the renderer, critique and sound tests, which skip without them. The browser tests run when `MOTION_REVIEW_BROWSER` names a local Chrome or Chromium. `bash scripts/check_all.sh --fast` runs the quick subset (validator, contract and unit tests, without the media determinism suite) for the edit loop; releases use the full list. The historical legacy suite was retired on 2026-10-10; `tests/legacy-baseline.json` keeps its last report as history.

The packager runs structural validation first and writes a plugin ZIP, a complete repository ZIP and their SHA-256 inventories into `dist/`. It makes no network requests, installs nothing and does not publish a release. It excludes Git internals and local build outputs.

The five conditional quality improvements and bounded offline GEPA pilot are described in [Quality development 1.3.0](quality-development-1.3.0.md). They preserve existing owners, UI and one review budget; no automatic prompt adoption or paid execution is introduced.

Current evidence and unverified behavior are recorded in [VERIFICATION.md](../VERIFICATION.md). Planned evaluations are not reported as passed tests. For a larger release, the [host smoke set](host-smoke-set.md) gives eight short checks to run in ChatGPT or Codex and a record that `scripts/check_host_smoke.py` validates; only such runs show host behavior.
