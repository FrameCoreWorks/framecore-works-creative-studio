# README demo clips

The clips shown at the top of the [repository README](../../README.md#see-it-in-30-seconds). They are repository presentation files, outside the plugin package, and are not installed with Studio.

Each MP4 was rendered on 2026-10-29 from Studio 1.153.0 (`0b2e37c`) by the bundled [Python renderer](../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-render/README.md) (`render.py` 1.7.0, Pillow 12, Liberation Sans and the bundled Inter and Archivo fonts) from an example contract, without hand editing. Each GIF is a 12 fps preview of its MP4 made with ffmpeg; the MP4 is the exact render.

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
