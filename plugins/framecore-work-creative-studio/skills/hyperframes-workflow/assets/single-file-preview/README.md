# Single-file motion preview

[`motion-preview.html`](motion-preview.html) is a self-contained, dependency-free template that lets a user watch a motion design without installing anything. It works where there is no shell or renderer: ordinary ChatGPT, ChatGPT Work and Codex alike. Save the file and open it in any current browser; it needs no server, no internet and no libraries.

It is a preview for reviewing motion, timing and readable holds. Its **Export video** button writes a video-only MP4 or WebM file in the user's browser through the [browser video export](../motion-export/README.md). For a render with music and voice-over, or where the browser cannot export, use the [Remotion kinetic type starter](../../../remotion-video-production/assets/kinetic-type-starter/README.md); custom choreography lives in the [GSAP motion starter](../gsap-motion-starter/README.md).

## What the template contains

- The motion contract embedded as JSON in `<script type="application/json" id="motion-score">`, in the same `motion-score.json` format as both starters. The bundled example is the starters' synthetic score.
- Easing presets from [motion craft](../../references/motion-craft.md), implemented as cubic-bezier functions.
- The embedded [scene engine](../motion-scenes/README.md) with a generic DOM renderer. Each scene declares a `kind` and `params`; the engine builds its elements once and sets every style from the frame number alone.
- A player with Play/Pause, Replay, previous and next frame, a frame slider, a frame readout and keyboard control (Space, Left, Right). The playback clock only chooses which frame to draw.
- `window.seekFrame(frame)`, `?frame=140` and `?frames=299,0,140` for exact-frame review and seek comparisons.
- Captions from the contract drawn above the scenes, and playback of `music.src` and `voiceover.src` from files saved next to the HTML file; while audio plays, the audio clock chooses the frame. See [music and voice-over sync](../motion-sync/README.md).
- When the contract declares `formats`, a format menu and `?format=9x16` show each [output format](../motion-scenes/README.md#formats) from the same file.
- An **Export video** button: frame-by-frame MP4 (H.264) where the browser can encode it, otherwise WebM, video only, saved through a download link.
- Review mode (`?review=1`) for the [automated frame review](../motion-review/README.md); it draws the stage at its true size from the top-left corner.

## How Studio delivers it

1. Build the approved contract first and express every scene with a [scene kind](../motion-scenes/README.md). Give each displayed line its own copy ID: a headline set in two sizes is two IDs in one `line-reveal`. Use `params.exit: 'sweep'` for a line-sweep hand-over. Keep exact copy and locks from the contract.
2. **Deliver the template unchanged except the contract.** Copy `motion-preview.html` and replace only the JSON inside `<script type="application/json" id="motion-score">`. Do not rewrite, shorten, reformat or restyle the player, the embedded scene engine or the video export, and do not hand-write a separate renderer: a rewritten preview loses the frame review, the Remotion render and the tested export. When the host can read plugin files and run code, copy the file programmatically and substitute the score block rather than retyping it. When no kind fits a scene, say so, offer the closest kind or parameter, and keep the template.
3. Where Node.js is available, run `node check-preview.mjs motion-preview.html` ([`check-preview.mjs`](check-preview.mjs)): it passes only when everything outside the contract matches the template, the contract passes `check-score.mjs` and every scene declares a kind. Without a shell, state that this check did not run.
4. Keep it self-contained: no external URLs, CDN libraries, fonts or tracking. Use system fonts unless the user supplies a font whose license allows embedding; embedded images must be supplied or approved and are inlined as data URIs, which increases file size.
5. Deliver it with the host's real capability:
   - When the host can create files, write `motion-preview.html` and give the user the file or download link.
   - Otherwise give the complete file in one code block and say: save it as `motion-preview.html` and open it in Chrome, Edge, Firefox or Safari; double-clicking the file is enough.
   - If an interactive preview such as Canvas is actually available in the conversation, the same file may be opened there as an extra; it is never required.
6. Report honestly. Do not say the animation was seen, played or reviewed unless the host actually displayed it. Without that evidence, preview and temporal review stay NOT VERIFIED and the user is asked what they see.
7. For a video file without a renderer, ask the user to press **Export video** and save the file; say that it is video only and that MP4 depends on the browser (otherwise WebM). Do not claim an export happened until the user confirms the file. Where execution is available, render the same score with a runtime starter instead. A screen recording of the preview is not a frame-accurate export.

## Verification boundary

During package preparation the template was opened directly from disk (`file://`) in a headless Chromium in a Linux development container. Frames 0, 20, 100, 140, 180 and 299 were captured and inspected, and frames 127 and 140 were pixel-identical whether opened directly or reached through forward and backward seek sequences. Interactive Play was not exercised automatically. A 2026-10-06 diagnostic in ordinary ChatGPT reported that Canvas was not available in that conversation, so this mode does not depend on Canvas. Behavior in any host remains not verified.
