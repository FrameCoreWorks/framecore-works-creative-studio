# Declarative motion scenes

[`motion-scenes.mjs`](motion-scenes.mjs) is a dependency-free scene engine. A scene in the [motion contract](../../references/motion-contract-json.md) declares a `kind` and `params`; the engine describes its elements once (`buildScene`) and returns their styles and changing text for any frame (`sceneFrame`). Renderers only apply the result, so the [single-file preview](../single-file-preview/README.md) and the [Remotion kinetic type starter](../../../remotion-video-production/assets/kinetic-type-starter/README.md) show the same picture for the same frame. Motion values come from the contract's `motion` block and [motion craft](../../references/motion-craft.md).

With kinds, a project is mostly JSON: in a host without a shell, Studio writes the contract and embeds it in the preview instead of writing scene code.

## Scene kinds

| Kind | Required params | Optional params | Behaviour |
| --- | --- | --- | --- |
| `line-reveal` | `lines`: copy IDs | `sizes`, `weights`, `align` (`left`, `center`) | Each line rises from its own mask, staggered by `lineStaggerFrames` |
| `item-stagger` | `items`: copy IDs | `connector` (default true), `size`, `weight`, `direction` (`auto`, `row`, `column`), `gap` | Items rise and fade in by `itemStaggerFrames`; a connector grows at constant speed behind them. `auto` lays them out in a row only when the frame is at least 1.3 times wider than high, otherwise in a centred column with a vertical connector |
| `end-card` | `text`: copy ID | `rule` (default true), `size`, `duration` | Settles from 94% scale with the resolve easing; no exit when it is the last scene |
| `counter` | `to` | `from`, `decimals`, `prefix`, `suffix`, `label` (copy ID), `locale`, `duration`, `easing` | The label settles first, then the number counts with tabular figures and holds its final value |
| `quote` | `quote`: copy ID | `attribution` (copy ID), `attributionDelay`, `size`, `align` | The whole quotation enters at once; the attribution follows after the delay |
| `logo-reveal` | `asset`: asset ID with `src` | `width`, `reveal` (`circle`, `wipe`), `duration` | Reveals the supplied mark by clipping only; it is never scaled, skewed or recoloured |
| `device` | `screens`: `[{asset, at}]`, assets with `src`, `width`, `height` | `frame` (`phone`, `window`, `browser`), `url` (copy ID), `transition` (`push`, `fade`, `cut`), `transitionFrames`, `taps`, `focus`, `caption` (copy IDs), `side` (`left`, `right`), `captionSizes`, `captionWeights`, `deviceColor` | Screenshots inside a drawn phone or window; see [device scenes](#device-scenes) |

Every scene exits with a short fade and lift unless it is the last scene or sets `params.exit: false`. `params.exit: 'sweep'` hands over with a vertical line instead: during the scene's last `sweepFrames` (default `exitFrames` + 12) the content fades and slides left over `exitFrames` while a line (`sweepColor`, default the accent) crosses from margin to margin and finishes at the scene end. Start the next scene about 12 frames before that end so it enters behind the line, and end the readable hold before the sweep starts. Sizes are given for a frame whose short side is 1080 pixels and scale with the short side, so 1920 × 1080, 1080 × 1920 and 1080 × 1080 share one type scale. Keep the `copy` list of each scene in sync with its params so the reading-hold check measures the right text.

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

[`examples/all-kinds.motion-score.json`](examples/all-kinds.motion-score.json) uses the six text and logo kinds with an original synthetic example mark; [`examples/app-film.motion-score.json`](examples/app-film.motion-score.json) uses `device` with original screenshots of fictional example data. [`examples/two-statements.motion-score.json`](examples/two-statements.motion-score.json) builds the 2026-10-07 ordinary ChatGPT test brief from two `line-reveal` scenes and a sweep exit, with one copy ID per displayed line. `check-score.mjs` in both starters validates kinds, required params, copy references, logo assets and device screens, and lists the kind in the storyboard table.

Copies of the engine are kept identical: the Remotion starter's `src/motion-scenes.mjs` byte for byte, and the single-file preview's embedded block without `export` keywords. The toolkit validation enforces both.

## Extending

Add a kind only when a recurring brief needs it: describe its elements in `buildScene`, its per-frame styles in `sceneFrame`, its params in `sceneKinds` and in `check-score.mjs`, then add it to the example, the table above and the tests. A one-off scene can still be written as custom code in the GSAP starter or a Remotion component.

## Verification boundary

During package preparation the example rendered in the single-file preview (headless Chromium, `file://`) and in the Remotion starter (stills and a 775-frame H.264 render) in a Linux development container. The starters' three-scene contract rendered pixel-identically to the previous hand-written preview. This does not establish behavior in ChatGPT, Work or a Codex session.
