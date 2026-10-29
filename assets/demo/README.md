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
