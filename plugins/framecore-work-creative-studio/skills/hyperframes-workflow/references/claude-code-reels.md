# Client reels in Claude Code: the HyperFrames route

Owner decision 2026-10-12: in Claude Code, or another host with a shell, Node.js, FFmpeg and Chrome or Chromium, client reels and ads are built as HyperFrames compositions by default. The bundled contract route (Python renderer, motion player) stays for hosts without a shell and for small JSON jobs. Checked 2026-11-04 against [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) tag `v0.9.13`, commit `06722eb9b90834beee636d1a9d41cd22452bd7fd` (CLI `hyperframes` 0.9.13, Apache-2.0).

## Set up once

- **HyperFrames plugin for Claude Code** (recommended, versioned): `claude plugin marketplace add heygen-com/hyperframes`, then install `hyperframes@hyperframes` and enable auto-update for that marketplace in `/plugin`. Its router is `/hyperframes:hyperframes`; its skills load on demand.
- **Or the pinned CLI** in the project: `npx hyperframes@0.9.13 ...`, with `npx hyperframes@0.9.13 skills update` for the core skills.
- `npx hyperframes doctor` checks Node.js, FFmpeg, memory and the browser. When Chrome is not found but a Chromium exists, set `HYPERFRAMES_BROWSER_PATH` to it. HyperFrames sends anonymous usage data; set `HYPERFRAMES_NO_TELEMETRY=1` or run `npx hyperframes telemetry disable` before the first command unless the user agreed to it.
- Installing downloads code from npm and GitHub; it is part of the installation the user asked for, never of a single film. When the npm registry is blocked (an egress policy, a closed network), HyperFrames cannot run: write the boards as one HTML page and render it with the [HTML capture](../assets/motion-export/README.md#hand-written-html-to-mp4-without-npm), and say so before the build.

## Who does what

Studio keeps the decisions; HyperFrames builds. HyperFrames' router calls itself the entry for every video request; inside Studio it is the engine, so its intent interview does not repeat what the brief already settled.

| Stage | Owner |
| --- | --- |
| Brief, offer, exact copy, claims, rights, language | Studio (orchestrator, Copy Voice, Research) |
| The idea, found before the look | Studio's [ideation method](../../pipeline-core/references/ideation-method.md), carried in Project State |
| Board plan and approval | This skill with the [reel board system](reel-board-system.md) |
| Composition, animation, blocks, render | The HyperFrames skills below |
| Review and acceptance before delivery | This skill: motion activity, visible text, Polish diacritics, safe boxes, sound |

| Job | HyperFrames skill (0.9.13) |
| --- | --- |
| Composition contract, format, motion, keyframes, look, captions, overlays, sound, storyboard, per-type notes (launch, explainer, music, vertical, data, 3D) | `hyperframes` |
| About 450 ready blocks and components (lower thirds, captions, CTA cards, transitions, UI mock-ups, charts, HUD frames); search before hand-building | `hyperframes-registry` (`npx hyperframes catalog <words>`, `npx hyperframes add <name>`) |
| CLI loop: init, add, check, snapshot, timeline, beats, audio, render | `hyperframes-cli` |
| Music, effects, voice, stock images through HeyGen | `media-use`, only when the user asks and has a HeyGen account |
| Port, rebuild, catalogue style, Figma, live deck | on-demand skills in the [skill map](hyperframes-skill-map.md), with what each requires |

The 0.8.x workflow skills (`product-launch-video`, `music-to-video`, `embedded-captions`, `talking-head-recut` and others) no longer exist; the [skill map](hyperframes-skill-map.md#names-removed-in-v090) says where each job went.

## The production loop

1. **Brief and idea.** Settle the job, the offer, exact copy, format and length; find the idea with the ideation method. Name what is set aside.
2. **Board plan.** Write the reel as boards ([reel board system](reel-board-system.md)): for each, its time range, the one statement, what changes on it and the block or blueprint that builds it. Get the plan approved before building; a direct, complete brief may skip the stop and say so. With the plan, offer [control frames first or full render now](../../workflow-orchestrator/references/studio-contract.md#control-frames-or-full-render) once; with full render, step 5 is Studio's own check, not a stop for the user.
3. **Build.** `npx hyperframes init <name>` (or copy a [reel starter](../assets/reel-starters/README.md) when its job fits the brief), search the registry for every named look before writing it by hand (a name the registry lacks: the [technique atlas](../assets/technique-atlas/README.md) says what it is and shows it), one sub-composition per board, the persistent frame (HUD, logo, captions) on its own track. Exact copy is typed from the brief, never generated inside an image or clip.
4. **Check.** `npx hyperframes check` until it has no errors.
5. **Look.** `npx hyperframes snapshot` at each board's middle and last frame; read the PNGs. Fix overflow, contrast, missing glyphs (ą, ć, ę, ł, ń, ó, ś, ź, ż) and anything outside the title-safe box before rendering the film.
6. **Draft render.** `npx hyperframes render --quality draft`, then run [motion activity](../assets/motion-quality/README.md#motion-activity) on the MP4 and declare intended holds with `--hold`. REVISE means rework the still stretch (a new change, a board cut, a camera move), never decorate it with particles.
7. **Delivery render.** `--quality delivery` for each format; when the brief has sound, listen to it before accepting, and answer the [development review](motion-development-review.md).
8. **Deliver.** The MP4 per format, a cover frame (a snapshot whose text reads at thumbnail size), the project folder, and the review record: what was checked, on which frames, and what was not.

Report the HyperFrames version and the skills used. A render warning (for example a media file that failed to load) is a finding to fix or disclose, not noise.

## Evidence

On 2026-10-17 the [local-service starter](../assets/reel-starters/README.md#evidence) rendered at 9:16 and 4:5 and passed motion activity after a second accent was added to each board; a slow drift of a flat field alone failed it.

On 2026-10-12 in a Linux container with Node.js 22, FFmpeg 6.1 and Chromium, `hyperframes` 0.8.149 initialised the `kinetic-type` example, passed `lint` with two warnings and rendered it: 1920 x 1080, 30 fps, 450 frames, 15 s; one warning, `media_load_failed`, for a video the example loads from the network. Motion activity on that render: PASS, 35 % still, longest still 2 s. The owner reports client reels built in Claude Code with HyperFrames. No Studio-planned client reel has yet been rendered through this route in a recorded test.
