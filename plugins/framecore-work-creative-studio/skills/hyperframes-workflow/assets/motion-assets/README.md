# Asset check: generated cut-outs

[`asset_check.py`](asset_check.py) checks the stills generated for a motion film before they enter it, and cuts them out when the generator gave no transparency. The method and the generator facts are in [generated cut-out assets](../../references/generated-motion-assets.md). Python 3.8+, Pillow and NumPy; it runs in a code sandbox and in a shell.

```sh
python3 asset_check.py check boombox.png hand.png --screen-px 900 --zoom 1.3
python3 asset_check.py matte neon-white.png neon-black.png --out neon.png
python3 asset_check.py key hand-green.png --out hand.png
```

- **`check`** reports each file as PASS or REPAIR, with the reason and the fix: no real transparency (an opaque file), a painted checkerboard posing as transparency, a green fringe or a dark or bright halo along the alpha edge, and too few pixels for the largest planned size on screen (`--screen-px`) at the largest push-in (`--zoom`).
- **`matte`** computes a difference matte from the same subject generated on pure white and edited to pure black: `alpha = 1 − |white − black| / √(3·255²)` and `colour = black / alpha`. It keeps partial transparency (glass, glow, smoke) that a key cannot. It refuses the pair when the subject moved between the two versions, because their difference then has a colour of its own instead of being the same in every channel.
- **`key`** is a soft chroma key on colour distance (Cb and Cr, so shadows on the screen key too) with despill (green clamped to the larger of red and blue) and a 1 px edge choke, for solid, opaque, non-reflective subjects on `#00FF00` (`--key` for another colour). It refuses a subject with green of its own.

Exit codes: 0 pass, 1 something to repair, 2 input problem (missing or unreadable file, an output that already exists). Outputs are always new files.

Limits: it checks still files, not the composite. Light wrap, grading and the check of edges in the rendered film (peak zoom, 2× crops) are steps of the [method](../../references/generated-motion-assets.md#6-after-the-files-arrive). The checkerboard detector looks for a regular two-tone grid along the image border, and the fringe thresholds are tuned on synthetic tests; a PASS is a lead, and the frames still need a look.

During package preparation (2026-10-14) the tests in `tests/motion_assets_test.py` checked, on synthetic images: a clean cut-out passes and a small one fails against its zoom; an opaque file and a painted checkerboard are reported; a hard key's green rim is reported; the matte recovers a soft glow's alpha within 3 % on average and refuses a subject moved by 25 px; the key cuts a grey subject on green cleanly and refuses one with a green label. It has not run on the assets of a real production yet.
