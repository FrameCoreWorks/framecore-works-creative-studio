# Response to the repository audit of 2026-10-08

The owner supplied an external audit of `main` at `e8884d8` (package 1.35.0), written by ChatGPT with GPT 6.1 Sol: "FrameCore Studio Audyt Repo 2026-10-08". Each finding was reproduced in a Linux development container before anything was changed. Fixes are released in 1.37.0 (change CC-20261008-07).

| Finding | Reproduced | Verdict | Fix |
|---|---|---|---|
| F01: critique scores 100 and exits 0 when the video cannot be read | Yes: `--video missing.mp4` gave exit 0, score 100, `frames: not_run` | Correct | `status` (`checked`, `issues`, `contract_only`, `incomplete`); frames asked for but not read give `incomplete` and exit 3; the video's size, frame rate and length must match its contract |
| F02: silence counted as a measured hit with 0 ms offset | Yes, by reading `check_hits`: a silent transient window fell back to the expected sample and was marked measured and on time | Correct | A window with no signal above about -80 dBFS is `missing`, not measured, and fails `all_ok`; intentionally silent landings create no cue, so they are unaffected |
| F03: `extend` leaves `sfx` behind and the music fitted to the old length | Yes: a cue after the extended scene stayed at its old frame | Correct; also found that planning again lost the user's fixed choices unless repeated | `extend` moves `sfx` and marks `soundDesign.status` `stale`; `mix` refuses a stale design; `plan` keeps choices recorded as set by the user |
| F04: CI skips current suites | Partly: presentation and benchmark tests were not in CI; motion-quality already ran, imported by `motion-toolkit.test.mjs`; no checks ran on branches or pull requests | Partly correct | `scripts/check_all.sh` used by the release workflow and a new checks workflow on every push and pull request; legacy suite as a separate non-blocking job |
| F05: benchmark takes `meta.json` for the contract | Yes, by reading `find`: the first `.json` alphabetically was used | Correct | `*.motion.json` first, a JSON counts only when it is a contract, several candidates are reported; the delivered video is also judged on its own frames; an incomplete review keeps no score |
| F06: `--video` decodes the whole video into memory | Yes, by reading `VideoFrames`: all frames as RGB, then copied | Correct | Only the review frames are decoded (ffmpeg select) |

Other points of the audit:

- **The rubric measures a minimum, not craft.** Agreed: Bounce Party scored 100 and the owner rejected it. The critique is a floor; concept, choreography and energy remain the owner's review and the blind benchmark's.
- **Music winds down after a mid-video reveal.** Confirmed open in `compose.render_music`; not changed in 1.37.0.
- **"All tests pass" needs scope.** Agreed: current checks and the historical legacy suite (20 of 67 `package.test.mjs` tests failing, 134 `validate-package.mjs` errors, the same as before) are reported separately.
- **Release status still said NOT_RUN for Intelligent UI.** Already updated in 1.36.0 with the partial host report.

Host behavior of the fixes is not verified; they are source and container checks.
