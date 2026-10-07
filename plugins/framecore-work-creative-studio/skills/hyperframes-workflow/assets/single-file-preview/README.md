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

## The motion player

The same file is the **motion player**. Its **Open contract** button (or dropping a file on the page) loads any motion contract: pasted JSON or a `.json` file. The player checks that every scene has a known kind and can be drawn, then reloads with the contract carried in the address fragment (`#contract=...`), which browsers never send to a server; reloading keeps it, **Built-in example** clears it. Everything else, including formats and **Export video**, works as for an embedded contract.

The player is available without the plugin:

- **Online:** <https://framecoreworks.github.io/framecore-works-creative-studio/>, published from this template by the repository's Pages workflow once GitHub Pages is enabled for the `gh-pages` branch.
- **As a file:** `framecore-motion-player-<version>.html` in every [GitHub release](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/latest), byte-identical to this template; save it once and open it in a browser.

## How Studio delivers it

1. Build the approved contract first and express every scene with a [scene kind](../motion-scenes/README.md). Give each displayed line its own copy ID: a headline set in two sizes is two IDs in one `line-reveal`. Use `params.exit: 'sweep'` for a line-sweep hand-over. Keep exact copy and locks from the contract; `approval.status` is one of the [contract states](../../references/motion-contract-json.md).
2. **Deliver the contract, not a hand-written page.** In a host without a shell, give the contract as a file named `<id>.motion.json` when the host can create files, otherwise as one JSON code block, and tell the user: open the motion player (link above, or the saved player file), press **Open contract**, choose the file or paste the JSON, then press **Export video** for a video file. Do not write, shorten or restyle a player, scene engine or export of your own except under the fallback in step 4: the 2026-10-07 tests showed that a rewritten page can lose the tested export and always loses the frame review.
3. Deliver a complete HTML file only by copying `motion-preview.html` byte for byte and replacing just the JSON inside `<script type="application/json" id="motion-score">`, done programmatically when the host can read plugin files and run code. Where Node.js is available, confirm it with `node check-preview.mjs motion-preview.html` ([`check-preview.mjs`](check-preview.mjs)): it passes only when everything outside the contract matches the template, the contract passes `check-score.mjs` and every scene declares a kind. If the template cannot be copied exactly, deliver the contract as in step 2 instead.
4. **Fallback for a self-written page.** If a page of your own is still delivered (for example, the user insists on a single HTML file and the template cannot be copied), its Export video must reproduce [`video-export.mjs`](../motion-export/video-export.mjs): WebCodecs `VideoEncoder`, frame by frame from the frame number, with the same codec candidates (H.264 MP4 first, then VP9 and VP8 WebM) and the same MP4 and WebM writers. Never use `MediaRecorder`, `canvas.captureStream` or real-time recording. In the first 2026-10-07 test a page that reproduced `video-export.mjs` exported a playable MP4; in the second, a `MediaRecorder` export on the same phone produced no file. Say in the reply that the page is self-written, that `check-preview.mjs` will not pass it, and offer the motion player route.
5. Keep it self-contained: no external URLs, CDN libraries, fonts or tracking in the contract or the page. Use system fonts unless the user supplies a font whose license allows embedding; embedded images must be supplied or approved and are inlined as data URIs, which increases size. A very large contract may exceed what an address fragment holds; then deliver the HTML file as in step 3.
6. If an interactive preview such as Canvas is actually available in the conversation, the player may be opened there as an extra; it is never required.
7. Report honestly. Do not say the animation was seen, played or reviewed unless the host actually displayed it. Without that evidence, preview and temporal review stay NOT VERIFIED and the user is asked what they see.
8. For a video file without a renderer, the user presses **Export video** in the player and saves the file; say that it is video only and that MP4 depends on the browser (otherwise WebM). Do not claim an export happened until the user confirms the file. Where execution is available, render the same score with a runtime starter instead. A screen recording of the preview is not a frame-accurate export.

## Verification boundary

During package preparation the template was opened directly from disk (`file://`) in a headless Chromium in a Linux development container. Frames 0, 20, 100, 140, 180 and 299 were captured and inspected, and frames 127 and 140 were pixel-identical whether opened directly or reached through forward and backward seek sequences. Interactive Play was not exercised automatically. A 2026-10-06 diagnostic in ordinary ChatGPT reported that Canvas was not available in that conversation, so this mode does not depend on Canvas. Behavior in any host remains not verified.
