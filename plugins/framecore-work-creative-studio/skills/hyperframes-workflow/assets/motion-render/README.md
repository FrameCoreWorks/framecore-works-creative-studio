# Python motion renderer

[`render.py`](render.py) renders a [motion contract](../../references/motion-contract-json.md) to an MP4 in a Python sandbox, such as the code execution in ChatGPT or ChatGPT Work. It is a Python port of the [scene engine](../motion-scenes/README.md): the same seven scene kinds (including `device` screenshots in a phone, window or browser, with taps), per-scene backgrounds and wipes and params, easings, entries, holds, lift and sweep exits, captions, safe areas and formats. It needs Python 3.8 or newer, Pillow and ffmpeg (on `PATH` or from the `imageio-ffmpeg` package). SVG logos also need `cairosvg`; otherwise supply a PNG of the same mark.

```sh
python render.py video.motion.json video.mp4 --check-dir video-check
python render.py video.motion.json video-9x16.mp4 --format 9x16
python render.py video.motion.json --stills 0,78,93 --stills-dir stills
```

- **Output.** H.264 in yuv420p at the contract's exact size, frame rate and frame count, without an audio track; an existing file is never overwritten. It prints one JSON line with the renderer version, frames, size, the font files used, the encoder and the files written.
- **Frame check.** `--check-dir` saves the first and last frame, both sides of every scene boundary, every hold start and the middle of every sweep, for the frame check before delivery.
- **Fonts.** `tokens.fontFamily` is resolved to font files on the machine: Arial, Helvetica and `sans-serif` use Arial or a metric-compatible substitute (Liberation Sans, Arimo), then DejaVu Sans. Weights of 600 and above use the bold file. `--font` and `--font-bold` choose files explicitly, for example a font the user supplied. Record the files from the summary, because a different font changes the picture.
- **Logos and images.** PNG, JPEG and WebP files or data URIs are drawn directly. An SVG logo needs the `cairosvg` package; where it is not installed (as may be the case in a hosted Python sandbox, Unknown until tried) the render stops with a clear message. Ask for a PNG of the mark up front when the user supplies only an SVG and no shell is available.
- **Determinism.** The same script, contract and font files give byte-identical frames.

## Fonts

A contract that declares `fonts` ([{family, weight, file or data}]) is rendered with exactly those files, using the browser's weight matching, so the [player](../single-file-preview/README.md) preview and the MP4 set the same type. A `file` is looked up next to the contract, in each `--font-dir`, then in Studio's [bundled fonts](../../../pipeline-core/assets/fonts/README.md); when the renderer runs from a copied `<id>.render.py`, pass `--font-dir <plugin>/skills/pipeline-core/assets/fonts`. A local player file cannot load fonts from disk, so embed them first: `python3 embed_fonts.py video.motion.json video.preview.motion.json`. Without `fonts`, `tokens.fontFamily` is resolved from system fonts as before. The summary's `fonts` lists the files used.

## Text that fits

Before any frame is drawn, the renderer lays out every scene and stops with exit code 4 and `"status": "text_overflow"` when a word is wider than its column, which would otherwise be cropped (a 200 px "Najnowocześniejszy" in a 9:16 column became "Najnowo"). The message names the word, its width and the column; reduce the size, shorten the copy or split the line in the contract and render again. `--allow-overflow` renders anyway, only for a deliberate crop that the review then records. Both renderers share two typesetting rules: a one-letter word (a, i, o, u, w, z) never ends a line, and a number stays with its unit ("90 zł", "10 kg", "50 %"), through no-break spaces in the copy.

## How Studio uses it

With code execution, Studio copies `render.py` byte for byte as `<id>.render.py`, runs it on the contract, inspects the check frames and delivers the MP4, the `.motion.json` and the `.render.py`. The contract records `runtime.value` as the summary's renderer and font files and `runtime.script` as the script's file name. A [revision](../motion-revise/README.md) runs the same script on the new contract. Only when the script cannot run (no Pillow or ffmpeg, an unsupported asset) does Studio write its own renderer with the same rules, and it says so.

## Verification boundary

During package preparation, in a Linux development container with Pillow 12 and Liberation Sans, frames rendered by this script were compared with the browser scene engine (headless Chromium 1194) at the review frames of three contracts: the `two-statements` example, the `all-kinds` example with a PNG copy of its mark, and the starter contract with imported captions in 16:9 and 9:16. The mean difference stayed below one grey level per pixel and side-by-side frames showed the same layout and timing. Two renders gave byte-identical frames, and both contracts of the 2026-10-07 ChatGPT Work revision test kept every frame before the change byte-identical. The script has not been run in a ChatGPT or ChatGPT Work sandbox.
