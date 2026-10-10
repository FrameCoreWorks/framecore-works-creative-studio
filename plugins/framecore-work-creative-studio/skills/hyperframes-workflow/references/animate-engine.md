# Animate engine

The [Animate engine](../assets/animate-engine/ENGINE.md) makes short animated films entirely in code: one `<canvas>` drawn and scored procedurally, deterministic frame by frame, rendered to MP4 with a headless browser and FFmpeg. It is bundled unchanged from [cth9191/animate](../../../integrations/animate/README.md) (MIT, version 0.4.0) as one of this skill's runtimes, next to the Python renderer, GSAP, Remotion and HyperFrames. Its own instructions are `ENGINE.md` (the upstream `SKILL.md`, renamed so hosts do not list it as a second skill); where its text says `SKILL.md`, read `ENGINE.md`.

## When to choose it

Recommend it when the look is illustrated or hand-made rather than clean interface motion:

| Need | Why this engine |
| --- | --- |
| An explainer, a history, a timeline or a little story with characters | Story formats (a chronology joined by shape morphs, a mission cut on the beat, a list, a journey with one hero) and a grammar for beats, bridges and the payoff |
| One of its looks: cut paper, crosshatch ink, riso print, sketchbook, manim-style math, pixel art, isometric line art | Each is a style kit with its own rules, palette, motion habits and frame checklist (`styles/<name>/STYLE.md`) |
| A look matched from the user's references | `new-style.md` measures palette, line, texture, motion and cut rhythm and saves a reusable style in the user's project |
| A narrated explainer timed to the words, or cuts on the beats of the user's own track | `tools/voice.mjs` and `tools/beats.mjs` make the voice or the song the clock |
| Several aspect ratios from one piece | Scenes are laid out per format, never cropped |

For kinetic type, interface and product films, data animation and brand motion, keep the contract runtimes (scene kinds, the Python renderer, GSAP, Remotion). For website-to-launch films with HyperFrames' catalog, keep [HyperFrames](hyperframes-engine.md). State the choice in one sentence; the user's explicit runtime wins.

## Where it runs

Codex and Claude Code, or any local project with a shell: Node.js 18 or newer, FFmpeg, and the Studio workspace copy of the engine with its pinned browser driver (Playwright 1.56.1) and a Chromium for it. The [environment check](../../workflow-orchestrator/assets/environment-check/README.md) lists it as `animate_engine` and prints the install commands:

```sh
ENGINE="$HOME/.framecore-studio/workspace/animate-engine"   # after the environment check's install step
node "$ENGINE/tools/build.mjs" pieces/<name>
node "$ENGINE/tools/still.mjs" pieces/<name> 2.25,9.75 look.png --scale 0.5
node "$ENGINE/tools/export.mjs" pieces/<name> --share
node "$ENGINE/tools/review.mjs" pieces/<name>
```

Pieces live in the user's project under `pieces/<name>/`; styles the user makes live in the project's `styles/<name>/`. The workspace copy is replaced on a plugin update: never edit it for one piece, and propose changes to its `craft.md` or a style as notes in the piece's `LOG.md` instead. Voice-over word timing needs Python with `faster-whisper`; without it the engine estimates word times and says so.

In ChatGPT, ChatGPT Work and the Claude apps the engine does not run (no npm workspace or browser driver in the chat sandbox). There, deliver the same idea through the contract and the bundled Python renderer, and use the engine's method files below as craft knowledge.

## How Studio runs it

The engine's flow (intake, story check, look check, storyboard check, build, delivery, learn) fits this skill's method. Studio's rules stay in charge where they differ:

- **Intake.** Ask only what Studio cannot infer, one consequential question at a time, as numbered text when the host has no native choice control. The engine's `intake.md` and its style gallery (`tools/gallery.mjs`) are the source of the questions and the look choice.
- **Approval.** The engine's three check-ins are Studio's storyboard approval: the beat table (story), 2–4 style frames (look) and the board of every beat, each approved as an identified revision before animating. A concrete brief that already settles story or look skips that check-in.
- **Facts.** On-screen claims follow the conditional [Research Evidence](../../research-evidence/SKILL.md) gate and are listed with sources in the piece's `brief.md`, as the engine also requires.
- **The project is the contract.** `piece.json`, `src/`, `brief.md` and `LOG.md` hold the timing, copy and decisions; a revision changes only what was asked and rebuilds. A Studio `.motion.json` contract is not required for this engine.
- **Review.** `review.mjs` (cuts on the beat grid, morph centring, story-arc loudness, dead beats, phone sheet, text cut off or overlapping, loudness) and `textcheck.mjs` are the technical and text-completeness evidence. Then decide [acceptance](../assets/motion-review/README.md) in the four verdicts: technical from the review numbers; fidelity, composition and temporal only from looking at the contact sheets and watching the export. Report the numbers, the weakest shot and what was not verified, such as listening to the score.
- **Sound.** The engine composes its score in code and masters it to about −14 LUFS; a supplied track is used only when the user owns or licensed it. [Motion sound design](motion-sound-design.md) still sets the standard, and the MP4 follows this skill's rule on whether sound is wanted.
- **Providers and assets.** A voice from an ElevenLabs connector runs only when the user has connected it and approves the cost the engine states before the full run; never clone a voice without its owner's consent. Screenshots come only from sites the user owns (`tools/capture.mjs`). Reference media stays local.

## Method files usable everywhere

Even where the engine cannot run, these files are craft knowledge for any motion plan in Studio:

- [Story formats](../assets/animate-engine/grammar/FORMATS.md): eight short-form formats (plot engine × stage × clock) with their invariants, and which are proven.
- [Story rules](../assets/animate-engine/grammar/STORY.md): one constant, colour means one thing, silence before the payoff and loudest on it, the end is the start changed.
- [Frame checklist](../assets/animate-engine/grammar/FRAME.md): what any key frame must hold, in any style.
- [Craft rules](../assets/animate-engine/craft.md): motion, timing, sound and review lessons from finished pieces.
- [Styles](../assets/animate-engine/styles/README.md) and [making a style from references](../assets/animate-engine/new-style.md).

## Honesty

Upstream reports that formats F2 (chronology joined by morphs) and F4 (mission) have each produced a piece that passed every check from the card alone, and F5 (fixed-hero journey) several; the other formats are documented but unproven. Cut paper and crosshatch have carried full pieces; riso, sketchbook, math and pixel one or two; isometric only its demo; a style made from new references is new ground. Say so when choosing one. Studio checked the engine on 2026-10-10 in a Linux container: the riso demo built, exported to MP4 in about a minute and passed its review; the math demo built and rendered stills from a workspace installed with `npm ci`. Codex, Claude Code on the user's machine, macOS and Windows were not run.
