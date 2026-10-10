# Animate: bundled engine with selective method adaptation

Source: [cth9191 / animate](https://github.com/cth9191/animate/tree/7e5eb56feb2dd573f890e1b7b34748af43d58263), the `animate` Claude Code skill, observed version 0.4.0, pinned commit `7e5eb56feb2dd573f890e1b7b34748af43d58263`. Reviewed on 2026-10-10 at the owner's request to add its skills to the motion graphics module.

[The original license](LICENSE) is MIT and retains Copyright (c) 2026 cth9191. The skill's folder `plugins/animate/skills/animate/` is bundled as [an engine of Motion Graphics Workflow](../../skills/hyperframes-workflow/assets/animate-engine/ENGINE.md): 107 files, each byte-identical to the pinned source, with one rename (`SKILL.md` is `ENGINE.md`, so no host lists it as a second skill). Studio adds only `package.json` and `package-lock.json` beside it, pinning the browser driver its tools load. Paths and Git blob hashes are in [the manifest](source-manifest.json); a test checks every bundled file against them. Studio's route is [the Animate engine reference](../../skills/hyperframes-workflow/references/animate-engine.md).

## Decision map

| Source part | Decision | Studio destination or reason |
| --- | --- | --- |
| Kit (`kit/`): seeded randomness, boiling line, cameras, shape-morph renderer, storyboard, synthesizer, loudness stage | Bundle unchanged | Runs from the Studio workspace copy in Codex and Claude Code |
| Tools (`tools/`): build, tile, still, storyboard, export, review, text check, compare, gallery, frame hash, beats, capture, voice, reference measurement | Bundle unchanged | Same; the environment check installs the workspace and its pinned Playwright with `npm ci` |
| Seven styles with rules, kits, samples and demos; new styles from references | Bundle unchanged | Offered for illustrated or hand-made looks; user styles stay in the user's project |
| Story grammar (`grammar/`), `craft.md`, `intake.md`, `new-style.md` | Bundle and adopt as method | Linked from the reference as craft knowledge on every host |
| Its flow with three check-ins | Adapt | The check-ins are Studio's storyboard approval of identified revisions |
| "Ask with AskUserQuestion" | Adapt | Numbered text unless the host exposes a native choice control |
| Web-check every on-screen claim | Already present | Studio's conditional research gate, sources in `brief.md` |
| "Done is measured" by its review | Adopt with addition | Its numbers are the technical evidence; Studio's four acceptance verdicts still need eyes on the frames and a viewing |
| ElevenLabs voice through a connector | Keep with Studio's provider rule | Only when the user connected it and approved the stated cost |
| Learn step: edit `craft.md` or a style | Adapt | Notes go to the piece's `LOG.md`; the bundled copy is never edited per piece |
| Repository README, `docs/*.png`, plugin wrapper | Not bundled | Presentation only, 5.8 MB |

## Evidence scope

Checked on 2026-10-10 in a Linux container with Node.js 22, FFmpeg 6.1 and Playwright 1.56.1 with its Chromium: the riso demo built, exported 144 frames to MP4 in about a minute and passed its review (cuts and morphs on the grid, story arc, text, dead beats; −14.6 LUFS); the gallery rendered all seven styles; the math demo built and rendered stills from a workspace copy installed with `npm ci`. The source repository's newest Playwright is 1.64.0; Studio pins 1.56.1, the version tested here, and the update check lists the newer one. Codex, Claude Code on a user's machine, macOS, Windows and voice-over timing with faster-whisper were not run.
