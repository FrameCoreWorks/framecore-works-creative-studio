# Automated frame review

[`review-frames.mjs`](review-frames.mjs) checks a motion contract before a person watches it. It runs where Node.js 20 or newer and a local Chrome or Chromium are available, typically Codex or a local project; it installs nothing and makes no network requests.

```sh
node review-frames.mjs motion-score.json --out review-out
node review-frames.mjs motion-preview.html --out review-out --browser /path/to/chrome
node review-frames.mjs motion-score.json --out review-out --format 9x16
```

A contract with [`formats`](../motion-scenes/README.md#formats) is reviewed in every format by default: `base` plus each format ID. `--format` limits the run to one. Screenshots then go to `frames/<format>/`, every frame record carries its `format`, and the contact sheet has one section per format.

## What it does

1. Selects review frames from the contract: frame 0 and N-1, both sides of every scene boundary, the start, middle and end of every readable hold, sound cues, the start, middle and end of every caption, and uniform samples. The rules match `reviewFrames` in the [motion quality helpers](../motion-quality/README.md).
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

Run it after a build and before presenting a motion review; repair every error and judge every warning within the shared review budget, then rerun. Record the result in the [QA record](../../templates/motion-qa-record.md). Frames outside holds are captured but not measured, because text is meant to move there. Captions are measured whenever they are shown, including overlap with settled scene text.

## Craft critique and the improvement round

[`critique.py`](critique.py) scores a contract and its rendered frames against Studio's craft rubric, so the judgement a motion designer makes by eye becomes numbers any model can act on. It needs Python 3.8+ and Pillow, uses the bundled [Python renderer](../motion-render/README.md), and runs in ChatGPT's code execution as well as in Codex; no browser.

```sh
python critique.py video.motion.json --out critique-r1
python critique.py video.motion.json --video video.mp4 --out critique-r1
```

With `--video` the frames come from the delivered video itself instead of the bundled renderer: use it whenever the video was drawn by a renderer written for the project, so the critique judges what the viewer will see. The video must have the contract's size, frame rate and length (checked with ffprobe; a mismatch is reported, never scaled away), and only the review frames are decoded, so a long or large video does not fill memory.

| Area | Rule (severity) |
| --- | --- |
| readability | every scene's words are held long enough to read: words / 3 per second + 0.4 s, at least 0.8 s (error below 85% of it, warning above) |
| text amount | at most 10 words per scene in a vertical video, 14 in a wide one (warning) |
| pace | a scene with copy lasts at least 1 s; a scene without a second beat lasts at most 6 s or 1.8 times its reading time (warning); equal scene lengths throughout (note) |
| hook | the first readable moment comes within 1.5 s (warning) |
| ending | an end card or logo holds at least 1.5 s (warning); a video without one is noted |
| motion | lines arrive 3 frames to 0.5 s apart (warning) |
| contrast | foreground against background at least 4.5:1 (error) |
| layout | in every hold frame of every format: something is visible, nothing touches the frame edge (error), and in 9:16 nothing sits in the bottom 14% or top 8% where Reels and TikTok draw their interface (warning) |
| composition | in 9:16, a content block shorter than 60% of the height is centred between 30% and 62% of it, so neither half of the frame is left empty (warning) |

The score starts at 100 and loses 15 per error and 5 per warning. Every finding names the scene or frame and a concrete fix, often a ready [`revise.mjs extend`](../motion-revise/README.md) command. `contact-sheet.png` shows every review frame (first and last, both sides of every boundary, hold starts and middles), one section per format; look at it before deciding. `critique.json` holds the result. `status` says what the score covers: `checked` (frames inspected, no errors), `issues` (errors remain; exit code 1), `contract_only` (`--no-frames`: the timing and text rules only, no picture certified) or `incomplete` (frames were asked for but could not be read or drawn here, such as a missing or mismatched video or an SVG mark without `cairosvg`; exit code 3). An incomplete review is never a pass, whatever its score: fix the cause or say in the reply that the picture was not inspected.

**The improvement round is part of every delivery.** After the first render: run the critique, look at the contact sheet, fix every error and every warning (or say in the reply which warning is kept on purpose and why), re-render, and run the critique again. Repeat until no error remains; at least one round is made whenever the first critique has a finding. The reply states the score before and after and what was fixed. A first render is never delivered unreviewed.

## Limits

The browser checks are layout checks on selected frames, and the critique's rules are a floor, not taste: neither judges motion quality, rhythm, timing feel, audio or the encoded export, and they do not replace watching the full sequence. Custom Remotion components outside the scene kinds are not rendered by the preview; review their stills separately. Results depend on the local browser and fonts; record the browser that ran.

## Verification boundary

Until 1.18.0, review screenshots were drawn about 8% smaller than the frame because the headless viewport is shorter than the window; measurements were unaffected. Review mode now renders at true size. In a 1.18.0 check, frame 176 of the starter matched the Remotion still of the same frame pixel for pixel in each of the three starter formats. Until 1.30.0 the screenshots still lost the bottom of the frame (87 pixels in Chromium 1194), which new headless Chrome fills with the page background because the page gets less height than the window; text measurements were unaffected. The tool now measures that difference with a probe page, enlarges the window by it, and the contact sheet shows each screenshot cropped to the frame. On 2026-10-07 every review frame of the app-film example then matched the Python renderer within 0.86 grey levels on average, including the bottom rows.

During package preparation the tool ran in a Linux development container with headless Chromium 1194: the starter contract (31 frames; 93 across its three formats since 1.18.0) and the all-kinds example (53 frames) produced no findings, and a deliberately broken contract produced clipping and out-of-frame errors with exit code 1. Host behavior is not verified.
