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
| `text-cut`, `text-hidden` | error | From the [visible-text audit](#visible-text-audit): any visible text in the stage, not only contract copy, has a word cut or hidden by a mask, its own box or the frame (reported as `transitional` outside holds) |
| `ignore-flag`, `font-not-loaded` | warning, error | A visible text carries an audit-exempting flag; a declared web font did not load |

4. Writes `review.json`, a `review.html` contact sheet with every frame and its findings, the screenshots and the `preview.html` it used. It refuses an existing output directory. The exit code is 0 without errors, 1 with errors and 2 when setup fails, such as no browser.

## How Studio uses it

Run it after a build and before presenting a motion review; repair every error and judge every warning within the shared review budget, then rerun. Record the result in the [QA record](../../templates/motion-qa-record.md). Frames outside holds are captured but not measured, because text is meant to move there. Captions are measured whenever they are shown, including overlap with settled scene text.

## Visible-text audit

[`text-audit.mjs`](text-audit.mjs) checks that every visible word is complete, in any HTML composition: Studio's preview, a HyperFrames or GSAP composition, or hand-written HTML. It runs the in-page [`text-audit.browser.js`](text-audit.browser.js), which `review-frames.mjs` also injects, so a contract review covers every visible text in the stage too.

```sh
node text-audit.mjs composition.html --out audit-r1 --times 1,4.5,9,14.5,19 --holds 0.6-3,3.4-7.6
node text-audit.mjs composition.html --out audit-r1 --times 1,4.5,9 --seek 'window.__timelines.main.seek(T, false)'
node text-audit.mjs video.motion.json --out audit-r1        # a Studio contract: its review frames and holds
```

- **Seeking.** It seeks Studio's preview (`seekFrame`), HyperFrames' `window.__timelines` (and shows only the clips whose `data-start`/`data-duration` cover the time), a global GSAP timeline or web animations; `--seek` takes any expression with `T` (seconds) and `F` (frame). A page with nothing to seek gives `not_verified`, never a pass, when several times were asked for.
- **What counts as visible.** Every text node under the root (`[data-composition-id]`, `--root`, or the body) that is displayed, visible, not transparent and above 2% opacity, including decorative words. Fonts are awaited first.
- **What is measured.** Each word's glyph boxes after transforms, against the frame and every clipping ancestor: `overflow` hidden, clip, scroll or auto on either axis (the element's own box included) and `clip-path: inset()`. A word under 98% visible is cut; a word or line fully hidden while others of the same element show is hidden. Empty ascent space above a tight line-height is not counted as ink. Masks and other clip-path shapes are noted for pixel review, not measured.
- **Holds.** Errors count only in readable holds, from `--holds`, the contract, or inferred: a sample whose text geometry is unchanged 0.2 s later is held. A word cut during a transition is reported as `transitional` and passes.
- **No silent exemptions.** `data-layout-ignore`, `data-layout-allow-overflow`, `data-layout-allow-occlusion` and `data-layout-allow-overlap` do not exempt visible text; they add an `ignore-flag` warning. A deliberate cut needs `data-text-clip-ok="<reason of at least 12 characters>"` on the element itself; it is listed as an exception that needs a pixel review.
- **Output.** `text-audit.json` (every sample, every visible text with its words, issues and exceptions) and `text-audit.html`, a contact sheet at phone scale (360 px wide) with cut words outlined and each screenshot linked at full size. Exit code 0 pass, 1 errors, 2 setup problem.

[`fixtures/`](fixtures/README.md) holds the reviewed reel's defect and the cases that must pass.

## Acceptance in four verdicts

[`acceptance.py`](acceptance.py) turns the evidence into four separate verdicts, as [commercial motion](../../references/commercial-motion.md#3-accept-in-four-separate-verdicts) defines them: A technical (ffprobe against the contract), B fidelity (copy found verbatim in audited frames, no unverified `strategy.claims` in the copy, asset authorities, a person's source comparison), C composition (text audit or frame review in holds, plus `--composition-review` from a person who judged the key frames; a contract-only or incomplete critique leaves it not_verified) and D temporal (pacing samples plus a recorded normal-speed viewing).

```sh
python acceptance.py video.motion.json --video video.mp4 --critique critique-r2/critique.json --review review-r2/review.json \
  --text-audit audit-r2/text-audit.json --composition-review pass --playback watched --source-review pass --temporal-review pass --note "owner, phone, 2026-10-09"
```

Overall `accepted` needs all four to pass; `deliverable_with_limits` lists what was not verified; `blocked` names the failure (exit codes 0, 3, 1). It never infers a viewing or a comparison that was not recorded.

## Craft critique and the improvement round

[`critique.py`](critique.py) scores a contract and its rendered frames against Studio's craft rubric, so the judgement a motion designer makes by eye becomes numbers any model can act on. It needs Python 3.8+ and Pillow, uses the bundled [Python renderer](../motion-render/README.md), and runs in ChatGPT's code execution as well as in Codex; no browser.

```sh
python critique.py video.motion.json --out critique-r1
python critique.py video.motion.json --video video.mp4 --out critique-r1
```

With `--video` the frames come from the delivered video itself instead of the bundled renderer: use it whenever the video was drawn by a renderer written for the project, so the critique judges what the viewer will see. The video must have the contract's size, frame rate and length (checked with ffprobe; a mismatch is reported, never scaled away), and only the review frames are decoded, so a long or large video does not fill memory.

| Area | Rule (severity) |
| --- | --- |
| readability | every scene's copy is held long enough to read, by the [motion craft](../../references/motion-craft.md#readable-holds) rule that `check-score.mjs` also uses: the longer of 13 characters per second + 0.5 s and 0.5 s + a third of a second per word, at least 1 s (error below 85% of it, warning above) |
| text amount | at most 10 words per scene in a vertical video, 14 in a wide one (warning) |
| pace | a scene with copy lasts at least 1 s; a scene without a second beat lasts at most 6 s or 1.8 times its reading time (warning); equal scene lengths throughout (note) |
| hook | the first readable moment comes within 1.5 s (warning) |
| ending | an end card or logo holds at least 1.5 s (warning); a video without one is noted |
| motion | lines arrive 3 frames to 0.5 s apart (warning) |
| contrast | foreground against background at least 4.5:1 (error) |
| layout | in every hold frame of every format: something is visible, nothing touches the frame edge (error), and in 9:16 nothing sits in the bottom 14% or top 8% where Reels and TikTok draw their interface (warning) |
| composition | in 9:16, a content block shorter than 60% of the height is centred between 30% and 62% of it, so neither half of the frame is left empty (warning) |
| hook | in a vertical, feed or advert film, the first frame is empty, though it is the thumbnail (warning) |
| pace from frames | four times a second, a stretch where nothing appears and under 1.5% of the frame changes counts as still; drift therefore counts as still. A still stretch longer than the copy's reading time plus 1.5 s (2 s without copy; plus 1.5 s in the last scene) is a warning |
| transitions | three or more boundaries with the same full-frame wipe, mask, slide or sweep (warning) |
| integration | an asset with an opaque `background` on a scene of another colour: its rectangle will show (warning) |

The score starts at 100 and loses 15 per error and 5 per warning. Every finding names the scene or frame and a concrete fix, often a ready [`revise.mjs extend`](../motion-revise/README.md) command. `contact-sheet.png` shows every review frame (first and last, both sides of every boundary, hold starts and middles), one section per format; look at it before deciding. `critique.json` holds the result. `status` says what the score covers: `checked` (frames inspected, no errors), `issues` (errors remain; exit code 1), `contract_only` (`--no-frames`: the timing and text rules only, no picture certified) or `incomplete` (frames were asked for but could not be read or drawn here, such as a missing or mismatched video or an SVG mark without `cairosvg`; exit code 3). An incomplete review is never a pass, whatever its score: fix the cause or say in the reply that the picture was not inspected. `score_scope` says what the number covers, and `verdicts` keeps the picture separate: `layout` is not_verified without frames, `text_completeness` is never checked here (a word cut by a mask leaves tidy pixels, so only the text audit sees it), and `temporal_playback` stays not_verified because this tool never watches the video. `pacing` lists each scene's longest still stretch, and `keyframes/` holds the opening, first readable, densest and ending frames at full size and phone scale (`-phone.png`).

**The improvement round is part of every delivery.** After the first render: run the critique, look at the contact sheet, fix every error and every warning (or say in the reply which warning is kept on purpose and why), re-render, and run the critique again. At least one round is made whenever the first critique has a finding, and at most two repair rounds follow the first review, as in the shared [loop protocol](../../../pipeline-core/references/loop-protocol.md): when an error remains after the second repair, stop and deliver with that error named, not hidden. The reply states the score before and after and what was fixed. A first render is never delivered unreviewed.

## Limits

The browser checks are layout checks on selected frames, and the critique's rules are a floor, not taste: neither judges motion quality, rhythm, timing feel, audio or the encoded export, and they do not replace watching the full sequence. Custom Remotion components outside the scene kinds are not rendered by the preview; review their stills separately. Results depend on the local browser and fonts; record the browser that ran.

## Verification boundary

Until 1.18.0, review screenshots were drawn about 8% smaller than the frame because the headless viewport is shorter than the window; measurements were unaffected. Review mode now renders at true size. In a 1.18.0 check, frame 176 of the starter matched the Remotion still of the same frame pixel for pixel in each of the three starter formats. Until 1.30.0 the screenshots still lost the bottom of the frame (87 pixels in Chromium 1194), which new headless Chrome fills with the page background because the page gets less height than the window; text measurements were unaffected. The tool now measures that difference with a probe page, enlarges the window by it, and the contact sheet shows each screenshot cropped to the frame. On 2026-10-07 every review frame of the app-film example then matched the Python renderer within 0.86 grey levels on average, including the bottom rows.

During package preparation the tool ran in a Linux development container with headless Chromium 1194: the starter contract (31 frames; 93 across its three formats since 1.18.0) and the all-kinds example (53 frames) produced no findings, and a deliberately broken contract produced clipping and out-of-frame errors with exit code 1. Host behavior is not verified.
