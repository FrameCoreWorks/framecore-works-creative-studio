# README demo clips

The clips shown in the [repository README](../../README.md#watch-it), plus three earlier renderer examples. They are repository presentation files, outside the plugin package, and are not installed with Studio.

## Renderer examples

These three clips were shown in the README until 2026-10-31. Each MP4 was rendered on 2026-10-29 from Studio 1.153.0 (`0b2e37c`) by the bundled [Python renderer](../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-render/README.md) (`render.py` 1.7.0, Pillow 12, Liberation Sans and the bundled Inter and Archivo fonts) from an example contract, without hand editing. Each GIF is a 12 fps preview of its MP4 made with ffmpeg; the MP4 is the exact render.

| Clip | Contract | Size |
|---|---|---|
| `app-film` | [app-film.motion-score.json](../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-scenes/examples/app-film.motion-score.json) | 1920×1080, 30 fps, 400 frames |
| `social-captions` | [social-captions.motion-score.json](../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-scenes/examples/social-captions.motion-score.json) | 1080×1920, 30 fps, 300 frames |
| `data-and-names` | [data-and-names.motion-score.json](../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-scenes/examples/data-and-names.motion-score.json) | 1920×1080, 30 fps, 420 frames |

The example contracts use synthetic data ("Example data", invented names and prices); they are not client work.

To render them again from the repository root (the renderer never overwrites an existing file):

```sh
A=plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets
python3 $A/motion-render/render.py $A/motion-scenes/examples/app-film.motion-score.json app-film.mp4
ffmpeg -i app-film.mp4 -vf "fps=12,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle" app-film.gif
```

The vertical clip's GIF uses `scale=320:-1`. A different font set changes the picture; the renderer's summary names the font files it used.

## Client chat

`client-chat.mp4` (1920×1080, 30 fps, 543 frames, 18.1 s, no audio) and its preview `client-chat.gif` (800 px wide, 15 fps, infinite loop) open the README section. They were made in a Claude Code cloud session on 2026-10-30 with Studio's Motion Graphics route as a HyperFrames 0.8.149 composition, [`client-chat/index.html`](client-chat/index.html), over eight owner review rounds, and accepted by the owner (PASS_REPORTED). The café, its messages and the reel are staged, not a client testimonial.

The phone is drawn in code. The camera holds each chat beat about 1 to 1.5 s, pushes in close while the creator types, waits on a "typing" bubble, then the reel bursts out of its bubble to fill the frame in three boards and shrinks back before the client's reply. Studio's motion activity and flash checks passed on the MP4. To render again, put the composition in a HyperFrames project with a local `assets/gsap.min.js` and Oxanium 500 and 700 WOFF2 files in `assets/fonts/`, then run `npx hyperframes@0.8.149 render --fps 30 --quality delivery -o client-chat.mp4`.

## Trailer

`trailer.mp4` (1280×720, 30 fps, 40.5 s, no audio) is the owner's own FrameCore Works preview reel, supplied on 2026-10-30 as a 1920×1080, 60 fps master and re-encoded here for the README (H.264, CRF 25). `trailer.gif` is an 8 s, 640 px, 12 fps excerpt from 16 s that links to the MP4.

## Brief to film

`brief-to-film.mp4` (1920×1080, 30 fps, 612 frames, 20.4 s, no audio) and its 800 px, 15 fps preview `brief-to-film.gif`: a handwritten brief becomes four pencil storyboard panels, the camera dives into the first and it becomes the finished ad for an invented bike shop, then pulls back to the grid. Made in a Claude Code cloud session on 2026-10-30 with Studio's Motion Graphics route as a HyperFrames 0.8.149 composition, [`brief-to-film/index.html`](brief-to-film/index.html), and accepted by the owner (PASS_REPORTED). Motion activity and flash checks passed.

## Paper box

`paper-box.mp4` (1080×1920, 30 fps, 354 frames, 11.8 s, no audio) and its 450 px, 15 fps preview `paper-box.gif`: a sheet holding a brief is cut along a dashed line, folds itself into a printed 3D box and unfolds from behind into the FrameCore Works logo. The paper-fold technique follows @x4b47x's paper cut-out film in the Opus 5.5 gallery; nothing was copied. Made on 2026-10-31 as a HyperFrames 0.8.149 composition, [`paper-box/index.html`](paper-box/index.html), in CSS 3D transforms, and accepted by the owner (PASS_REPORTED). Motion activity (24% still) and flash checks passed. On 2026-10-31 the owner found the closing caption hidden behind the unfolded box; the logo now ends smaller and higher, and a sweep of frames every 0.5 s confirmed every text sits fully visible inside the 9:16 safe area (top 10%, bottom 20%) in every hold.

## Chart to title

`chart-to-title.mp4` (1920×1080, 30 fps, 288 frames, 9.6 s, no audio) and its 800 px, 15 fps preview `chart-to-title.gif`: five order bars grow with counting values, then the black bars sink and the tallest, red bar lies down and becomes the owner's name title under a large "+158%". Example data and an invented bakery. Made on 2026-10-31 as a HyperFrames 0.8.149 composition, [`chart-to-title/index.html`](chart-to-title/index.html), and accepted by the owner (PASS_REPORTED). Motion activity and flash checks passed.

The HyperFrames compositions render the same way as the client chat: put the file in a HyperFrames project with a local `assets/gsap.min.js` and the Oxanium WOFF2 files in `assets/fonts/`, then run `npx hyperframes@0.8.149 render --fps 30 --quality delivery -o <name>.mp4`.

