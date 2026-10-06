# Automated frame review

[`review-frames.mjs`](review-frames.mjs) checks a motion contract before a person watches it. It runs where Node.js 20 or newer and a local Chrome or Chromium are available, typically Codex or a local project; it installs nothing and makes no network requests.

```sh
node review-frames.mjs motion-score.json --out review-out
node review-frames.mjs motion-preview.html --out review-out --browser /path/to/chrome
node review-frames.mjs motion-score.json --out review-out --format 9x16
```

A contract with [`formats`](../motion-scenes/README.md#formats) is reviewed in every format by default: `base` plus each format ID. `--format` limits the run to one. Screenshots then go to `frames/<format>/`, every frame record carries its `format`, and the contact sheet has one section per format.

## What it does

1. Selects review frames from the contract: frame 0 and N-1, both sides of every scene boundary, the start, middle and end of every readable hold, sound cues and uniform samples. The rules match `reviewFrames` in the [motion quality helpers](../motion-quality/README.md).
2. Renders each frame through the [single-file preview](../single-file-preview/README.md) in review mode (`?review=1`), which uses the shared [scene engine](../motion-scenes/README.md), so declared scene kinds look as they will in the Remotion starter.
3. In frames that fall inside a readable hold, measures the settled text:

| Check | Severity | Meaning |
| --- | --- | --- |
| `outside-frame` | error | Rendered text leaves the frame |
| `clipped` | error | Text extends beyond a clipping mask while it should be read |
| `contrast` | error | Text contrast is below WCAG 2.x 4.5:1, or 3:1 for large text, against its background |
| `margin` | warning | Text is closer to the edge than the contract's margin ratio (half of it top and bottom), or inside `tokens.safeArea` |
| `hold-opacity` | warning | Text is not fully opaque during a readable hold |
| `overlap` | warning | Two text elements of a scene overlap |
| `small-text` | warning | Vertical formats only: text below 1/48 of the frame height |

4. Writes `review.json`, a `review.html` contact sheet with every frame and its findings, the screenshots and the `preview.html` it used. It refuses an existing output directory. The exit code is 0 without errors, 1 with errors and 2 when setup fails, such as no browser.

## How Studio uses it

Run it after a build and before presenting a motion review; repair every error and judge every warning within the shared review budget, then rerun. Record the result in the [QA record](../../templates/motion-qa-record.md). Frames outside holds are captured but not measured, because text is meant to move there.

## Limits

These are layout checks on selected frames. They do not judge motion quality, rhythm, timing feel, audio or the encoded export, and they do not replace watching the full sequence. Custom Remotion components outside the scene kinds are not rendered by the preview; review their stills separately. Results depend on the local browser and fonts; record the browser that ran.

## Verification boundary

Until 1.18.0, review screenshots were drawn about 8% smaller than the frame because the headless viewport is shorter than the window; measurements were unaffected. Review mode now renders at true size. In a 1.18.0 check, frame 176 of the starter matched the Remotion still of the same frame pixel for pixel in each of the three starter formats.

During package preparation the tool ran in a Linux development container with headless Chromium 1194: the starter contract (31 frames; 93 across its three formats since 1.18.0) and the all-kinds example (53 frames) produced no findings, and a deliberately broken contract produced clipping and out-of-frame errors with exit code 1. Host behavior is not verified.
