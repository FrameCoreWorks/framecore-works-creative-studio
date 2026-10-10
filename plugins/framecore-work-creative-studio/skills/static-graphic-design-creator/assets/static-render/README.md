# Static compositor

`compose.py` sets exact text on a background and writes the graphic at its exact size: PNG and JPG for screens, a PDF with bleed (and optional crop marks) for print. It is the exact-copy route of [exact-copy compositing](../../references/exact-copy-compositing.md): the background comes from image generation, the user's photo or a flat colour; every word, price, logo and legal line is placed by code, so nothing is misspelt, invented or cropped.

```sh
python3 compose.py promo.static.json --out out/ --formats png,pdf
python3 compose.py promo.static.json --out out/ --formats png --strict   # low contrast is an error
python3 compose.py --presets        # named sizes (dated, provisional)
python3 compose.py --fonts-list     # bundled font names
```

Needs Python 3 and Pillow. Fonts come from [the bundled set](../../../pipeline-core/assets/fonts/README.md), a font folder given with `--fonts`, or a `.ttf`/`.otf` path next to the spec. It prints one JSON summary and writes `<id>.audit.json` beside the outputs.

## The spec

```json
{
  "id": "miod-lipowy-feed",
  "canvas": {"preset": "instagram-feed-portrait", "background": "#F4E9D8"},
  "layers": [
    {"type": "image", "src": "background.png", "fit": "cover", "box": [0, 0, 1080, 1350], "focus": [0.5, 0.4]},
    {"type": "gradient", "box": [0, 700, 1080, 650], "from": "#00000000", "to": "#000000CC", "direction": "down"},
    {"type": "image", "src": "logo.png", "fit": "contain", "box": [856, 64, 160, 64], "focus": [1, 0]},
    {"type": "text", "id": "headline", "text": "Miód lipowy z pasieki w Beskidach", "font": "Fraunces Black", "size": 112,
     "color": "#FFFFFF", "box": [64, 860, 952, 300], "valign": "bottom", "line_height": 1.0, "fit": "shrink", "min_size": 80},
    {"type": "rect", "box": [64, 1190, 330, 96], "fill": "#F2C14E", "radius": 48},
    {"type": "text", "id": "price", "text": "39,90 zł", "font": "Inter Black", "size": 56, "color": "#1D1D1B",
     "box": [64, 1190, 330, 96], "align": "center", "valign": "middle"},
    {"type": "text", "id": "omnibus", "text": "Najniższa cena z 30 dni przed obniżką: 44,90 zł", "font": "Inter Regular", "size": 24,
     "color": "#FFFFFF", "box": [420, 1218, 600, 60], "valign": "middle"}
  ]
}
```

- **Canvas.** `width` and `height` in pixels, or a `preset` (`--presets`). For print give `"print": {"width_mm": 148, "height_mm": 210, "bleed_mm": 3, "dpi": 300, "crop_marks": true}` or a print preset (`a5`, `a4`, `b2`, `poster-50x70`, `business-card-pl`, `rollup-85x200`); layer coordinates are then in the trim's pixels at that resolution (A5 at 300 ppi is 1748 × 2480).
- **Layers**, bottom to top: `image` (`src`, `fit` cover, contain or stretch, `focus` as fractions), `rect` (`fill`, `radius`, `opacity`), `gradient` (`from`, `to`, `direction` down, up, left or right) and `text`. A box is `[x, y, width, height]`. An image, rect or gradient that starts at the top-left corner or is marked `"bleed": true` runs into the bleed.
- **Text.** `text` is the exact copy; `font` a bundled name or a file; `size` in pixels; `color`; `box`; `align` left, center or right; `valign` top, middle or bottom; `line_height` (×size); `tracking` in thousandths of an em; `uppercase`; `max_lines`; `fit: "shrink"` with `min_size` to shrink until it fits; `shadow` `{offset, blur, color}`; `min_contrast` to override the threshold. Headlines from 40 px are balanced so the last line is not a lonely word; `"balance": false` turns it off. A `\n` in the text is a line break the user approved.

## What it guarantees

- **Exact copy.** The text is set as given. Polish typesetting only inserts no-break spaces: a one-letter word stays with the next word, a number stays with its unit, digit groups stay together (`1 299 zł`). The audit lists each layer's text, its lines, font and final size.
- **Nothing cropped.** A word wider than its box, lines taller than the box or more than `max_lines` stop the render with exit code 4 and `"status": "text_overflow"`, naming the layer and the reason; `fit: "shrink"` tries smaller sizes down to `min_size` first. `--allow-overflow` exists for drafts only.
- **No tofu.** A character the font cannot draw stops the render with exit code 4 and `"status": "missing_glyphs"`.
- **Contrast.** For each text layer the weakest tenth of the background right around the letters is measured against the text colour (WCAG ratio). The threshold is 4.5 for text under 48 px and 3.0 from 48 px; the summary reports pass or fail, and `--strict` makes a failure exit code 5 (`low_contrast`).
- **Sharpness.** An image enlarged beyond its pixels is reported with its effective resolution for print.

## Print

The PDF is an RGB raster at the print resolution with the bleed rounded up to whole pixels, plus a 10 mm slug with crop marks when asked. Say so to the print shop. `--icc profile.icc` converts it to CMYK with the profile the print shop names (often FOGRA39 or PSO Coated v3 for coated paper in Poland); without it, the shop converts. Keep text at least 5 mm inside the trim. The PNG and JPG are the trim size without bleed.

## Hosts

Runs wherever Studio can execute Python with Pillow: ChatGPT and ChatGPT Work with code execution, Codex, Claude Code and the Claude apps with code execution. Without code execution, deliver the spec and the background prompt and say the graphic was not composed.
