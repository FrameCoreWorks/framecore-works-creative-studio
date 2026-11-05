# GPT Image 2.6 and animated GIFs

Checked 2026-11-05 against OpenAI's [announcement](https://openai.com/index/introducing-images-2-6/) (2026-11-04), the [image generation guide](https://developers.openai.com/api/docs/guides/image-generation) and the model pages for [Flare](https://developers.openai.com/api/docs/models/gpt-image-2.6-flare) and [Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst). Recheck before quoting a limit or a price: these are dated facts. No render was made for this page; host and output behavior is NOT_RUN.

## What changed

| Fact | Detail |
| --- | --- |
| Where | ChatGPT and Codex (all subscription tiers; desktop, mobile, web) and the API. |
| API models | `gpt-image-2.6-flare` (fast iteration; as little as about 6 s at `quality: low`; better layout for posters and product images) and `gpt-image-2.6-sunburst` (more detail, steadier characters, products and brand details across edits at `medium` or `high`). The 2.5 pair stays documented. |
| ChatGPT and Codex | No documented Flare or Sunburst selector. Never promise a variant, a frame count or a size in a chat surface. |
| Speed | OpenAI states 50% faster than before. |
| `complexity` | `low`, `medium`, `high`; default `high`; no separate fee. It sets how much the model plans before rendering; `quality` (`low` to `max`, or `auto`) sets rendering detail. Use `low` for a focused edit (background, a sign), `medium` or `high` for dense text, complex layouts or many related objects. Higher can add latency and unwanted changes: compare on the task. |
| Markup edits | `POST /v1/images/edits` with a `markup` annotation layer (2.5 and 2.6). It applies to the first input image; other images are references. Each of the image and the layer is at most 16,777,216 pixels, the layer at most 50 MB. Not combined with `mask` or `prompt_rewriter`. The prompt names the change inside the mark, what stays unchanged, and asks to remove the mark from the result. |
| SVG | `output_format: "svg"` on generations only, `n: 1`; no streaming, partial images, compression or `prompt_rewriter`; an SVG is not an edit input. The API renders a raster reference (its `quality` applies) and authors static vector paths from it: no scripts, external resources or embedded rasters. Fits icons and flat illustrations; still check exact text and logo geometry. |
| Price | The same token rates as 2.5 (2026-11-05): text input $5, cached $1.25; image input $8, cached $2; image output $30 per 1M tokens. SVG also bills the authoring model's tokens. Markup has no extra fee. |

## Animated GIFs

**When a GIF here fits.** A short loop of one small action: a mascot or character (wave, blink, double take, victory dance that returns to the start pose), a sticker, a reaction or meme, a product shot turned into a loop, or an animated storyboard to test character movement before video production. It is not a route for sound, exact on-screen copy, timed typography, long or narrative motion or real camera moves: those stay with [Motion Graphics](../../hyperframes-workflow/SKILL.md) (coded motion, which can also export a GIF) or [Video Prompt](../../video-prompt-architect/SKILL.md) (a video generator).

**API contract.** `output_format: "gif"` on `POST /v1/images/generations` only; the edit endpoint does not return GIFs.

| Field | Values | Default |
| --- | --- | --- |
| `frame_count` | 2 to 64 | 9 |
| `frame_duration_ms` | 20 to 2000, rounded to 10 ms | 200 |
| `size` | `auto`, or per-frame `WIDTHxHEIGHT` in multiples of 16 | `auto` |

Loop length = `frame_count` x `frame_duration_ms` (the defaults give 1.8 s). Frames, frame size and `n` share the model's pixel budget: on a limit error reduce frames, frame size or `n`, or use `size: auto`. No streaming, partial images, custom compression or `prompt_rewriter`; `frame_count` and `frame_duration_ms` are only for GIF output. Save the decoded `b64_json` as `.gif`. Unknown on 2026-11-05: whether a generation request can take the user's artwork as an input for a GIF; in ChatGPT and Codex, start from the uploaded artwork and describe the motion.

**Prompt.** Describe the subject, the motion and the loop, in that order:

1. The subject and its locks: the same character, outfit, product and background in every frame (from the user's artwork or REF when given).
2. A fixed camera and framing unless the brief asks for a move.
3. The action as beats from the start pose to the end, with clear, small changes between frames.
4. The loop: the last frame leads smoothly back into the first.
5. The style and light, then the exclusions the brief needs (no captions, labels, borders, logos unless required).

Keep one action per GIF; a loop of 6 to 12 frames reads well and keeps drift low.

**Sprite-sheet route.** OpenAI's partner examples (OpenArt) ask for one sheet instead: "a single animation sprite sheet for a seamless looping GIF ... exactly 6 sequential frames arranged in a precise 3-column by 2-row grid, read left-to-right then top-to-bottom. Every panel has identical dimensions", a fixed camera, the same character and background, incremental motion, the sixth frame leading back to the first, and no captions, panel labels, borders or gutters. Use it on any image model or surface that returns a still, or when the user wants to edit single frames. Assemble the sheet where a shell is available (here a 3 x 2 grid at 8 fps):

```bash
ffmpeg -i sheet.png -vf "untile=3x2,setpts=N/(8*TB),split[a][b];[a]palettegen[p];[b][p]paletteuse" -loop 0 loop.gif
```

**Review before delivery.** Extract every frame (`ffmpeg -i loop.gif frame_%02d.png`) and look at them: identity, outfit and background stay the same, motion advances without jumps, the seam from the last to the first frame is smooth, nothing is cut at the edge, and any required text is whole and legible in every frame. Count the frames (`ffprobe -count_frames`) to confirm an animation, not a still. Report what was checked; a GIF that was not inspected is NOT_RUN.

## Third-party surfaces

Aggregators can expose other names or ranges (for example a five-level reasoning setting instead of the three `complexity` levels). Follow the schema of the surface actually used and never copy OpenAI field names into a chat prompt.
