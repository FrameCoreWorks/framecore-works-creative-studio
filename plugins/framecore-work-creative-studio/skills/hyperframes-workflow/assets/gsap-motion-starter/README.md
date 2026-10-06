# GSAP motion starter (HTML)

An original, synthetic starter for the HTML route of the [Motion Graphics Workflow](../../SKILL.md): kinetic typography and lightweight 2D scenes built with a paused GSAP timeline. It is a teaching fixture, not a client concept or a mandated style.

## Same contract as the Remotion starter

[`motion-score.json`](motion-score.json) is identical to the [Remotion kinetic type starter](../../../remotion-video-production/assets/kinetic-type-starter/README.md) contract: 1920 × 1080, 30 FPS, N = 300 frames, three scenes, readable holds, exact copy, tokens and motion values from [motion craft](../../references/motion-craft.md). The same storyboard can therefore be implemented in either runtime and reviewed against the same frames. `check-score.mjs` validates the contract without dependencies and prints it as a storyboard with `npm run storyboard`; see [motion contract JSON](../../references/motion-contract-json.md).

## Custom choreography route

This starter shows hand-written GSAP choreography: `main.mjs` draws the example's three scenes in order and does not interpret `kind` or `params`. Use it when a scene needs choreography the [scene kinds](../motion-scenes/README.md) do not cover. For declared kinds use the single-file preview or the Remotion starter, which share the scene engine. This starter draws the base size only and ignores `formats`; for another format, write its choreography against that size or use the shared engine's `resolveFormat`.

## How it stays deterministic

- One GSAP timeline is created paused. Scene visibility, entries and exits are placed at `frame / fps` from the score.
- Playback never runs the timeline clock; it only chooses a frame and calls `seekFrame(frame)`. Scrubbing, replay and capture use the same function.
- `window.seekFrame(frame)` renders exactly one frame and resolves after fonts are ready, so a capture tool can request frames 0..N-1.
- `?frame=140` opens a frame directly; `?frames=299,0,140` replays a seek sequence to compare direct, forward and backward seeks during review.

## Authorized local use

Copy this folder to a new authorized project outside the installed plugin. Requires Node.js 20 or newer for the check and Python 3 for the local preview server.

```sh
npm ci
npm run check
npm run storyboard
npm run preview
```

Open `http://127.0.0.1:8767/index.html` and stop the server when finished. Opening the file directly may block module loading. GSAP 3.15.0 is used under its own [standard no-charge license](https://gsap.com/standard-license); no GSAP source is bundled in this plugin.

## From preview to video

This page is a seekable preview, not an encoder. For video, capture frames 0..N-1 through `seekFrame` with an available capture tool (for example a HyperFrames composition or a headless-browser frame capture) and encode them with an available encoder, or move the approved contract to the Remotion starter. Record the actual capture and encoding route in the QA record.

## Verification boundary

During package preparation the page was served locally and captured in a headless Chromium in a Linux development container at frames 20, 100, 140, 180 and 299; direct seeks to frames 127 and 140 were pixel-identical to the same frames reached through forward and backward seek sequences. No video was encoded from this page. This does not establish behavior in ChatGPT, Work or a particular Codex session.
