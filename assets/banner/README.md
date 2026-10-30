# README banner

The animated banner at the top of the [repository README](../../README.md). These are repository presentation files, outside the plugin package, and are not installed with Studio.

| File | What it is |
|---|---|
| `creative-studio-banner.mp4` | The render: 1920×1080, 30 fps, 504 frames (16.8 s), H.264, no audio |
| `creative-studio-banner.gif` | README preview made from the MP4 with ffmpeg: 800 px wide, 15 fps, infinite loop |
| `composition/` | The HyperFrames composition that rendered it |

## How it was made

Studio's Motion Graphics route in Claude Code (a cloud session on 2026-10-30), owner-directed in several review rounds:

1. The letters of "Framecore" and "Works" drop from behind the camera and land with an impact shake while the camera rides along the line.
2. The gear flies in, locks into the "o" of "Works" and keeps turning to the end; the camera stays on it for a moment.
3. "Creative" and "Studio" are painted with real brush strokes: each stroke follows the centre line of the lettering in the order a hand writes it (every letter from its top edge down, crossbars and dots added after the word), with a rough bristle edge, and the camera tracks the brush.
4. A small square drops in beside the logo, paints the top bracket, hops down and paints the bottom bracket, with the camera riding close behind it.
5. The square jumps straight on and the camera keeps riding with it while it hops from label to label, left side then right, ten Studio capabilities slam in from top to bottom and each landing leaves a square stamp on the outer edge; then the camera eases back to the whole banner.
6. The gear spins faster and faster, and the camera swings in along an arc and flies through its hole onto plain white, the film's first frame, so the GIF loops without a cut.

Sources:

- Logo layers: the FrameCore Works Creative Studio logo, split by the owner into transparent per-letter layers (2508 px canvas) and cropped here to content; `composition/assets/logo/layers.json` holds each layer's position on the 1254 px logo canvas.
- Label font: [Oxanium](https://github.com/sevmeyer/oxanium) Bold, SIL Open Font License 1.1 (`composition/assets/fonts/OFL.txt`), chosen for its likeness to the logo's "Framecore Works" lettering.
- Brush strokes: the centre lines of the two script words, traced from the logo layers (skeletonized with scikit-image) and stored inline in `composition/index.html` as SVG mask paths.
- Motion technique only, no code or media copied: a logo assembled from parts flying in one by one, after the logo-reveal entries of the Opus 5.5 gallery Studio links to (for example @Mounnna's [slow-reveal logo build](https://x.com/Mounnna/status/2103802871934497266)).

## Render it again

The composition loads GSAP from `assets/gsap.min.js`, which is not stored here. The cloud browser could not reach a CDN, so install it locally first:

```sh
cd assets/banner/composition
npm i --no-save gsap@3.14.2 && mkdir -p assets && cp node_modules/gsap/dist/gsap.min.js assets/
npx --yes hyperframes@0.8.149 lint
npx --yes hyperframes@0.8.149 render --fps 30 --quality delivery -o banner.mp4
ffmpeg -i banner.mp4 -vf "fps=15,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=24:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" banner.gif
```

Without Chrome, set `HYPERFRAMES_BROWSER_PATH` to a Chromium binary. The camera is one continuous move: its keyframes (look point, scale, tilt) are joined by a cubic spline driven by a single tween, so it never stops between shots.
