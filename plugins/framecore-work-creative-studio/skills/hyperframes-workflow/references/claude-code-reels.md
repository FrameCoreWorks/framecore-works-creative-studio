# Client reels in Claude Code: the HyperFrames route

Owner decision 2026-10-12: in Claude Code, or another host with a shell, Node.js, FFmpeg and Chrome or Chromium, client reels and ads are built as HyperFrames compositions by default. The bundled contract route (Python renderer, motion player) stays for hosts without a shell and for small JSON jobs. Checked against [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) at commit `86521b94f592bcf0ca86aba63068893cf658af16` (CLI `hyperframes` 0.8.149, Apache-2.0).

## Set up once

- **HyperFrames plugin for Claude Code** (recommended, versioned): `claude plugin marketplace add heygen-com/hyperframes`, then install `hyperframes@hyperframes` and enable auto-update for that marketplace in `/plugin`. Its router is `/hyperframes:hyperframes`; its skills load on demand.
- **Or the pinned CLI** in the project: `npx hyperframes@0.8.149 ...`, with `npx hyperframes skills update` for the core skills.
- `npx hyperframes doctor` checks Node.js, FFmpeg, memory and the browser. When Chrome is not found but a Chromium exists, set `HYPERFRAMES_BROWSER_PATH` to it. HyperFrames sends anonymous usage data; `npx hyperframes telemetry disable` turns it off.
- Installing downloads code from npm and GitHub; it is part of the installation the user asked for, never of a single film.

## Who does what

Studio keeps the decisions; HyperFrames builds. HyperFrames' router calls itself the entry for every video request; inside Studio it is the engine, so its intent interview does not repeat what the brief already settled.

| Stage | Owner |
| --- | --- |
| Brief, offer, exact copy, claims, rights, language | Studio (orchestrator, Copy Voice, Research Evidence) |
| The idea, found before the look | Studio's [ideation method](../../pipeline-core/references/ideation-method.md), carried in Project State |
| Board plan and approval | This skill with the [reel board system](reel-board-system.md) |
| Composition, animation, blocks, render | The HyperFrames skills below |
| Review and acceptance before delivery | This skill: motion activity, visible text, Polish diacritics, safe boxes, sound |

| Job | HyperFrames skill |
| --- | --- |
| Composition structure, timing attributes, tracks, sub-compositions | `hyperframes-core` |
| Motion rules, scene blueprints, transitions, 24 text effects, runtime adapters | `hyperframes-animation` |
| Camera moves, punch-ins, Ken Burns, match and whip handoffs, masks | `hyperframes-keyframes` |
| About 400 ready blocks and components (lower thirds, captions, CTA cards, transitions, UI mock-ups, charts, HUD frames); search before hand-building | `hyperframes-registry` (`npx hyperframes catalog <words>`, `npx hyperframes add <name>`) |
| Palettes, typography, beat planning, design spec | `hyperframes-creative` |
| Mixing: fades, ducking under a voice, effects | `hyperframes-audio` |
| Captions on footage | `embedded-captions` |
| Lyric video, beat-cut slideshow, kinetic promo from a track | `music-to-video` |
| Promo from a product URL, script or brief | `product-launch-video` |
| Explainer from text with no footage | `faceless-explainer` |
| Designed overlays on interview or talking-head footage | `talking-head-recut` |
| Layout conventions, safe boxes, plan and build order | `hyperframes-studio` |
| Music, effects, voice, stock images through HeyGen | `media-use`, only when the user asks and has a HeyGen account |
| CLI loop: init, add, check, snapshot, beats, render | `hyperframes-cli` |

## The production loop

1. **Brief and idea.** Settle the job, the offer, exact copy, format and length; find the idea with the ideation method. Name what is set aside.
2. **Board plan.** Write the reel as boards ([reel board system](reel-board-system.md)): for each, its time range, the one statement, what changes on it and the block or blueprint that builds it. Get the plan approved before building; a direct, complete brief may skip the stop and say so.
3. **Build.** `npx hyperframes init <name>`, search the registry for every named look before writing it by hand (a name the registry lacks: the [technique atlas](../assets/technique-atlas/README.md) says what it is and shows it), one sub-composition per board, the persistent frame (HUD, logo, captions) on its own track. Exact copy is typed from the brief, never generated inside an image or clip.
4. **Check.** `npx hyperframes check` until it has no errors.
5. **Look.** `npx hyperframes snapshot` at each board's middle and last frame; read the PNGs. Fix overflow, contrast, missing glyphs (ą, ć, ę, ł, ń, ó, ś, ź, ż) and anything outside the title-safe box before rendering the film.
6. **Draft render.** `npx hyperframes render --quality draft`, then run [motion activity](../assets/motion-quality/README.md#motion-activity) on the MP4 and declare intended holds with `--hold`. REVISE means rework the still stretch (a new change, a board cut, a camera move), never decorate it with particles.
7. **Delivery render.** `--quality delivery` for each format; when the brief has sound, listen to it before accepting, and answer the [development review](motion-development-review.md).
8. **Deliver.** The MP4 per format, a cover frame (a snapshot whose text reads at thumbnail size), the project folder, and the review record: what was checked, on which frames, and what was not.

Report the HyperFrames version and the skills used. A render warning (for example a media file that failed to load) is a finding to fix or disclose, not noise.

## Evidence

On 2026-10-12 in a Linux container with Node.js 22, FFmpeg 6.1 and Chromium, `hyperframes` 0.8.149 initialised the `kinetic-type` example, passed `lint` with two warnings and rendered it: 1920 x 1080, 30 fps, 450 frames, 15 s; one warning, `media_load_failed`, for a video the example loads from the network. Motion activity on that render: PASS, 35 % still, longest still 2 s. The owner reports client reels built in Claude Code with HyperFrames. No Studio-planned client reel has yet been rendered through this route in a recorded test.
