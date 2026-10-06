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

Every scene exits with a short fade and lift unless it is the last scene or sets `params.exit: false`. Sizes are given for a frame whose short side is 1080 pixels and scale with the short side, so 1920 × 1080, 1080 × 1920 and 1080 × 1080 share one type scale. Keep the `copy` list of each scene in sync with its params so the reading-hold check measures the right text.

## Formats

One contract can produce several output formats. `formats` lists variants of the base size, each with an `id`, `width`, `height`, optional `viewing`, and optional `tokens` and per-scene `params` that are merged over the base for that format only:

```json
"formats": [
  {"id": "9x16", "width": 1080, "height": 1920, "viewing": "9:16 full screen on a phone", "params": {"title": {"sizes": [112, 80]}}}
]
```

`resolveFormat(score, id)` returns the contract as seen in that format; `base` or no ID returns the base contract unchanged. Timeline, copy, holds and motion stay shared, so every format is reviewed against the same frames. Use per-format params for what really differs, such as smaller type for long lines in a narrow frame.

`tokens.safeArea` (`{top, bottom}` as fractions of the height) adds top and bottom padding to keep content clear of platform interface elements. The engine has no default: take the values from the target platform's current documentation or the user, and record the source in the contract's decisions.

## Example and checks

[`examples/all-kinds.motion-score.json`](examples/all-kinds.motion-score.json) uses all six kinds with an original synthetic example mark. `check-score.mjs` in both starters validates kinds, required params, copy references and logo assets, and lists the kind in the storyboard table.

Copies of the engine are kept identical: the Remotion starter's `src/motion-scenes.mjs` byte for byte, and the single-file preview's embedded block without `export` keywords. The toolkit validation enforces both.

## Extending

Add a kind only when a recurring brief needs it: describe its elements in `buildScene`, its per-frame styles in `sceneFrame`, its params in `sceneKinds` and in `check-score.mjs`, then add it to the example, the table above and the tests. A one-off scene can still be written as custom code in the GSAP starter or a Remotion component.

## Verification boundary

During package preparation the example rendered in the single-file preview (headless Chromium, `file://`) and in the Remotion starter (stills and a 775-frame H.264 render) in a Linux development container. The starters' three-scene contract rendered pixel-identically to the previous hand-written preview. This does not establish behavior in ChatGPT, Work or a Codex session.
