# Declarative motion scenes

[`motion-scenes.mjs`](motion-scenes.mjs) is a dependency-free scene engine. A scene in the [motion contract](../../references/motion-contract-json.md) declares a `kind` and `params`; the engine describes its elements once (`buildScene`) and returns their styles and changing text for any frame (`sceneFrame`). Renderers only apply the result, so the [single-file preview](../single-file-preview/README.md) and the [Remotion kinetic type starter](../../../remotion-video-production/assets/kinetic-type-starter/README.md) show the same picture for the same frame. Motion values come from the contract's `motion` block and [motion craft](../../references/motion-craft.md).

With kinds, a project is mostly JSON: in a host without a shell, Studio writes the contract and embeds it in the preview instead of writing scene code.

## Scene kinds

| Kind | Required params | Optional params | Behaviour |
| --- | --- | --- | --- |
| `line-reveal` | `lines`: copy IDs | `sizes`, `weights`, `align` (`left`, `center`), `entry` (`lines`, `words`), `wordMotion` (`rise`, `pop`), `wordStaggerFrames` (3), `wordEasing` | Each line rises from its own mask, staggered by `lineStaggerFrames`; with `entry: 'words'` every word enters in turn, see [word entries](#word-entries) |
| `item-stagger` | `items`: copy IDs | `connector` (default true), `size`, `weight`, `direction` (`auto`, `row`, `column`), `gap` | Items rise and fade in by `itemStaggerFrames`; a connector grows at constant speed behind them. `auto` lays them out in a row only when the frame is at least 1.3 times wider than high, otherwise in a centred column with a vertical connector |
| `end-card` | `text`: copy ID | `rule` (default true), `size`, `duration` | Settles from 94% scale with the resolve easing; no exit when it is the last scene |
| `counter` | `to` | `from`, `decimals`, `prefix`, `suffix`, `label` (copy ID), `locale`, `duration`, `easing` | The label settles first, then the number counts with tabular figures and holds its final value |
| `quote` | `quote`: copy ID | `attribution` (copy ID), `attributionDelay`, `size`, `align` | The whole quotation enters at once; the attribution follows after the delay |
| `logo-reveal` | `asset`: asset ID with `src` | `width`, `reveal` (`circle`, `wipe`), `duration` | Reveals the supplied mark by clipping only; it is never scaled, skewed or recoloured |
| `device` | `screens`: `[{asset, at}]`, assets with `src`, `width`, `height` | `frame` (`phone`, `window`, `browser`), `url` (copy ID), `transition` (`push`, `fade`, `cut`), `transitionFrames`, `taps`, `focus`, `caption` (copy IDs), `side` (`left`, `right`), `captionSizes`, `captionWeights`, `deviceColor` | Screenshots inside a drawn phone or window; see [device scenes](#device-scenes) |
| `lower-third` | `name`: copy ID | `title` (copy ID), `align` (`left`, `center`), `nameSize` (64), `titleSize` (40), `nameWeight` (700), `titleWeight` (400), `barColor` | A name and an optional title above the bottom edge or the safe area; an accent bar rises at the left (none when centred), then the lines slide up from their masks. One line each: wider text stops the render instead of being cut |
| `line-chart` | `points`: `[{label?, value}]` (copy ID, number; 2 to 12 points) | `min` (0 or the lowest value), `max`, `values` (`last`, `all`, `none`), `height` (0.6 of the safe area), `size` (36), `valueSize` (40), `valueWidth` (4 em), `thickness` (8), `dot` (12), `labelWeight` (500), `lineColor`, `duration` (48), `easing` (`easeInOutCubic`), `locale`, `decimals`, `prefix`, `suffix` | The axis and month or category labels settle, then the line draws from the first point to the last; each point's dot, and its value when shown, appear as the line arrives. Labels are one line in their slot: wider text stops the render |
| `photo-hero` | `asset`: asset ID with `src` (a photo) | `lines` (copy IDs), `sizes` (`[96, 48]`), `weights`, `align`, `focus` `{x, y}` (0.5), `zoom` `[from, to]` (`[1, 1.08]`, each 1 to 2), `zoomEasing` (`linear`), `parallax` (px drift up over the scene, 0), `shade` (0.6; 0 for none), `color` (`#FFFFFF`), `textDelay` (8), `fadeFrames` | The photo covers the frame around `focus` (CSS `object-fit: cover`) and pushes in from `zoom[0]` to `zoom[1]` over the whole scene while drifting up by `parallax`; a shade over the lower 60 % keeps the lines readable, and they rise from their masks above the bottom safe area. It exits with a fade only. The checker warns when the drift is larger than the zoom leaves below the focus |
| `bar-chart` | `bars`: `[{label, value}]` (copy ID, number of zero or more; 1 to 8 bars) | `max`, `size` (44), `valueSize`, `thickness` (36), `gap` (40), `valueWidth` (4.5 em kept for the value), `labelWeight` (500), `barColor`, `duration` (36), `easing`, `locale`, `decimals`, `prefix`, `suffix` | Rows arrive in turn: the label settles, the bar grows from the left on one shared scale and its value counts up at the bar's end, formatted like `counter` |

Every scene exits with a short fade and lift unless it is the last scene or sets `params.exit: false`. `params.exit: 'sweep'` hands over with a vertical line instead: during the scene's last `sweepFrames` (default `exitFrames` + 12) the content fades and slides left over `exitFrames` while a line (`sweepColor`, default the accent) crosses from margin to margin and finishes at the scene end. Start the next scene about 12 frames before that end so it enters behind the line, and end the readable hold before the sweep starts. Sizes are given for a frame whose short side is 1080 pixels and scale with the short side, so 1920 × 1080, 1080 × 1920 and 1080 × 1080 share one type scale. Keep the `copy` list of each scene in sync with its params so the reading-hold check measures the right text.

## Word entries

`line-reveal` with `params.entry: 'words'` brings the lines in word by word, across all lines, every `wordStaggerFrames` (3). `wordMotion: 'rise'` (the default) slides each word up from its own mask; `'pop'` springs it up from 60 % scale with `easeOutBack` and no mask. Words wrap like text and keep the Polish typesetting rules: a one-letter word stays with the next and a number with its unit, as one entering group. The gap between words is 0.28 of the type size in every renderer, so the browser, Remotion and the Python renderer wrap identically. Use it for short, loud lines (a hook, an offer); a long sentence entering word by word reads slower than the same line rising at once.

## Persistent elements

Top-level `persistent` lists elements that stay on screen across scenes, drawn above the scenes and below the captions: `{id, asset | copy, position, from, to}` with `position` `top-left`, `top-right` (default), `bottom-left` or `bottom-right`. They sit inside the side margin and the safe area (or the margin, whichever is larger). An `asset` shows the mark at `width` (160); a `copy` shows a one-line tag at `size` (36) and `weight` (700) on `background` (default the accent; `'none'` for plain text) in `color` (default the background colour), with `radius` (8). An element starting at frame 0 is there from the first frame; otherwise it fades in at `from` and out before `to` with the contract's entry and exit values, unless `to` is the end of the film. Keep a persistent element clear of scene text in every format; the frame review measures it like a caption. [`examples/photo-and-trend.motion-score.json`](examples/photo-and-trend.motion-score.json) keeps a mark in the corner and adds an offer tag from the second scene.

## Device scenes

`device` shows the user's screenshots inside a drawn phone (rounded body and island), window (title bar with three controls) or browser (a window whose title bar holds an address field showing the `url` copy), for [product films](../../references/product-films.md).

- **Screens.** `screens` lists asset IDs in order; every screen after the first has `at`, its start in frames from the scene start. The next screen pushes in (`transition: 'push'`, the default), fades in (`fade`) or cuts (`cut`) over `transitionFrames` (12). Each screenshot fills the screen like CSS `object-fit: cover`; the first one's `width` and `height` set the screen's aspect.
- **Taps.** `taps` is a list of `{at, x, y}`: a finger marker arrives 4 frames before `at`, presses on `at` while a ring in the accent colour spreads, and leaves after 8 frames. `x`, `y` are fractions of the screen. Put the next screen's `at` 3–5 frames after the tap's, so the press causes the change.
- **Camera focus.** `focus` is a list of `{at, scale, x, y, frames}`: from `at` (frames from the scene start) the device eases over `frames` (24) to `scale`, keeping the point `x`, `y` (fractions of the screen, 0.5 is the centre) in place. Keys run in order; use `scale: 1` to return.
- **Caption.** `caption` lists copy IDs set like `line-reveal` lines (`captionSizes` default `[72, 40]`); they rise 10 frames after the scene starts. In landscape the caption takes the `side` half and the device the other; in vertical formats the caption sits above the device.
- **Entry and exit.** The device settles in over `entryFrames` + 10 with the resolve easing and leaves with the scene's exit.

`deviceLayout(scene, score)` and `deviceFrame(scene, score, frame)` compute every size and position in whole pixels, so the preview, the Remotion starter and the [Python renderer](../motion-render/README.md) place the device identically. Screenshots must be data URIs for the preview's browser export, which draws the stage into a canvas.

## Scene backgrounds

Any scene can set `params.background` (a colour): the scene then draws on its own canvas of that colour instead of the contract's background. `params.backgroundWipe` (`left`, `right`, `up`, `down`; default `none`) reveals that canvas from the named side over `params.backgroundFrames` (12) with ease-in-out, so a new colour sweeps over the previous scene. Start the next scene `backgroundFrames` before the previous one ends and give every scene a background, or the base canvas shows between them. This is the signature of the Color block [style](../motion-styles/README.md); [`examples/color-block.motion-score.json`](examples/color-block.motion-score.json) shows it in 16:9 and 9:16.

## Formats

One contract can produce several output formats. `formats` lists variants of the base size, each with an `id`, `width`, `height`, optional `viewing`, and optional `tokens` and per-scene `params` that are merged over the base for that format only:

```json
"formats": [
  {"id": "9x16", "width": 1080, "height": 1920, "viewing": "9:16 full screen on a phone", "params": {"title": {"sizes": [112, 80]}}}
]
```

`resolveFormat(score, id)` returns the contract as seen in that format; `base` or no ID returns the base contract unchanged. Timeline, copy, holds and motion stay shared, so every format is reviewed against the same frames. Use per-format params for what really differs, such as smaller type for long lines in a narrow frame.

`tokens.safeArea` (`{top, bottom}` as fractions of the height) adds top and bottom padding to keep content clear of platform interface elements. The engine has no default: take the values from the target platform's current documentation or the user, and record the source in the contract's decisions.

## Captions and beats

`buildCaptions(score)` and `captionsFrame(score, frame)` draw `score.captions` above the scenes; `beatFrames(score)` returns the beat grid from `score.music`. Both renderers use them, and the [sync tool](../motion-sync/README.md) fills the contract fields.

## Example and checks

[`examples/data-and-names.motion-score.json`](examples/data-and-names.motion-score.json) uses `lower-third` and `bar-chart` with the Product light style, bundled Inter and a 9:16 format with `contentScale`. `lowerThirdLayout(scene, score)` and `barChartLayout(scene, score)` compute their sizes in whole pixels, as `deviceLayout` does, so every renderer places them identically. [`examples/all-kinds.motion-score.json`](examples/all-kinds.motion-score.json) uses the six text and logo kinds with an original synthetic example mark; [`examples/app-film.motion-score.json`](examples/app-film.motion-score.json) uses `device` with original screenshots of fictional example data. [`examples/photo-and-trend.motion-score.json`](examples/photo-and-trend.motion-score.json) uses `photo-hero` with an original synthetic photo, `line-chart` with six months of sales in Polish, a word-by-word offer and two persistent elements, in 9:16 and 16:9. `lineChartLayout`, `lineChartReach` and `lineWords` compute the line, its arrival frames and the word groups the same way in every renderer. [`examples/social-captions.motion-score.json`](examples/social-captions.motion-score.json) shows the `active-word` caption preset in 9:16. [`templates/`](templates/) holds three 9:16 ad templates (offer, product, testimonial) with 4:5 and 1:1 formats and placeholder copy; the [variants tool](../motion-variants/README.md) applies a brand kit and expands them into languages and formats. [`examples/two-statements.motion-score.json`](examples/two-statements.motion-score.json) builds the 2026-10-07 ordinary ChatGPT test brief from two `line-reveal` scenes and a sweep exit, with one copy ID per displayed line. `check-score.mjs` in both starters validates kinds, required params, copy references, logo assets and device screens, and lists the kind in the storyboard table.

Copies of the engine are kept identical: the Remotion starter's `src/motion-scenes.mjs` byte for byte, and the single-file preview's embedded block without `export` keywords. The toolkit validation enforces both.

## Extending

Add a kind only when a recurring brief needs it: describe its elements in `buildScene`, its per-frame styles in `sceneFrame`, its params in `sceneKinds` and in `check-score.mjs`, then add it to the example, the table above and the tests. A one-off scene can still be written as custom code in the GSAP starter or a Remotion component.

## Verification boundary

During package preparation the example rendered in the single-file preview (headless Chromium, `file://`) and in the Remotion starter (stills and a 775-frame H.264 render) in a Linux development container. The starters' three-scene contract rendered pixel-identically to the previous hand-written preview. This does not establish behavior in ChatGPT, Work or a Codex session.
