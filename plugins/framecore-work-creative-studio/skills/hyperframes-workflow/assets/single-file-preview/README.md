# Single-file motion preview

[`motion-preview.html`](motion-preview.html) is a self-contained, dependency-free template that lets a user watch a motion design without installing anything. It works where there is no shell or renderer: ordinary ChatGPT, ChatGPT Work and Codex alike. Save the file and open it in any current browser; it needs no server, no internet and no libraries.

It is a preview for reviewing motion, timing and readable holds. It is not a video export and not a substitute for the [Remotion kinetic type starter](../../../remotion-video-production/assets/kinetic-type-starter/README.md) or the [GSAP motion starter](../gsap-motion-starter/README.md) when a video file is required.

## What the template contains

- The motion contract embedded as JSON in `<script type="application/json" id="motion-score">`, in the same `motion-score.json` format as both starters. The bundled example is the starters' synthetic score.
- Easing presets from [motion craft](../../references/motion-craft.md), implemented as cubic-bezier functions.
- The embedded [scene engine](../motion-scenes/README.md) with a generic DOM renderer. Each scene declares a `kind` and `params`; the engine builds its elements once and sets every style from the frame number alone.
- A player with Play/Pause, Replay, previous and next frame, a frame slider, a frame readout and keyboard control (Space, Left, Right). The playback clock only chooses which frame to draw.
- `window.seekFrame(frame)`, `?frame=140` and `?frames=299,0,140` for exact-frame review and seek comparisons.

## How Studio delivers it

1. Build the approved contract first. Replace the embedded score with the project's score and declare each scene with a [scene kind](../motion-scenes/README.md); no scene code is needed when the kinds fit. Add custom rendering only for a scene no kind covers. Keep exact copy and locks from the contract.
2. Keep it self-contained: no external URLs, CDN libraries, fonts or tracking. Use system fonts unless the user supplies a font whose license allows embedding; embedded images must be supplied or approved and are inlined as data URIs, which increases file size.
3. Deliver it with the host's real capability:
   - When the host can create files, write `motion-preview.html` and give the user the file or download link.
   - Otherwise give the complete file in one code block and say: save it as `motion-preview.html` and open it in Chrome, Edge, Firefox or Safari; double-clicking the file is enough.
   - If an interactive preview such as Canvas is actually available in the conversation, the same file may be opened there as an extra; it is never required.
4. Report honestly. Do not say the animation was seen, played or reviewed unless the host actually displayed it. Without that evidence, preview and temporal review stay NOT VERIFIED and the user is asked what they see.
5. For a video file, move the same score to a runtime starter and render where execution is available. A screen recording of the preview is not a frame-accurate export.

## Verification boundary

During package preparation the template was opened directly from disk (`file://`) in a headless Chromium in a Linux development container. Frames 0, 20, 100, 140, 180 and 299 were captured and inspected, and frames 127 and 140 were pixel-identical whether opened directly or reached through forward and backward seek sequences. Interactive Play was not exercised automatically. A 2026-10-06 diagnostic in ordinary ChatGPT reported that Canvas was not available in that conversation, so this mode does not depend on Canvas. Behavior in any host remains not verified.
