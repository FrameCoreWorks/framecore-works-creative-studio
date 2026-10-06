# Declarative motion scenes

[`motion-scenes.mjs`](motion-scenes.mjs) is a dependency-free scene engine. A scene in the [motion contract](../../references/motion-contract-json.md) declares a `kind` and `params`; the engine describes its elements once (`buildScene`) and returns their styles and changing text for any frame (`sceneFrame`). Renderers only apply the result, so the [single-file preview](../single-file-preview/README.md) and the [Remotion kinetic type starter](../../../remotion-video-production/assets/kinetic-type-starter/README.md) show the same picture for the same frame. Motion values come from the contract's `motion` block and [motion craft](../../references/motion-craft.md).

With kinds, a project is mostly JSON: in a host without a shell, Studio writes the contract and embeds it in the preview instead of writing scene code.

## Scene kinds

| Kind | Required params | Optional params | Behaviour |
| --- | --- | --- | --- |
| `line-reveal` | `lines`: copy IDs | `sizes`, `weights`, `align` (`left`, `center`) | Each line rises from its own mask, staggered by `lineStaggerFrames` |
| `item-stagger` | `items`: copy IDs | `connector` (default true), `size`, `weight` | Items rise and fade in by `itemStaggerFrames`; a connector grows at constant speed behind them |
| `end-card` | `text`: copy ID | `rule` (default true), `size`, `duration` | Settles from 94% scale with the resolve easing; no exit when it is the last scene |
| `counter` | `to` | `from`, `decimals`, `prefix`, `suffix`, `label` (copy ID), `locale`, `duration`, `easing` | The label settles first, then the number counts with tabular figures and holds its final value |
| `quote` | `quote`: copy ID | `attribution` (copy ID), `attributionDelay`, `size`, `align` | The whole quotation enters at once; the attribution follows after the delay |
| `logo-reveal` | `asset`: asset ID with `src` | `width`, `reveal` (`circle`, `wipe`), `duration` | Reveals the supplied mark by clipping only; it is never scaled, skewed or recoloured |

Every scene exits with a short fade and lift unless it is the last scene or sets `params.exit: false`. Sizes are given for a 1080-pixel-high frame and scale with the contract height. Keep the `copy` list of each scene in sync with its params so the reading-hold check measures the right text.

## Example and checks

[`examples/all-kinds.motion-score.json`](examples/all-kinds.motion-score.json) uses all six kinds with an original synthetic example mark. `check-score.mjs` in both starters validates kinds, required params, copy references and logo assets, and lists the kind in the storyboard table.

Copies of the engine are kept identical: the Remotion starter's `src/motion-scenes.mjs` byte for byte, and the single-file preview's embedded block without `export` keywords. The toolkit validation enforces both.

## Extending

Add a kind only when a recurring brief needs it: describe its elements in `buildScene`, its per-frame styles in `sceneFrame`, its params in `sceneKinds` and in `check-score.mjs`, then add it to the example, the table above and the tests. A one-off scene can still be written as custom code in the GSAP starter or a Remotion component.

## Verification boundary

During package preparation the example rendered in the single-file preview (headless Chromium, `file://`) and in the Remotion starter (stills and a 775-frame H.264 render) in a Linux development container. The starters' three-scene contract rendered pixel-identically to the previous hand-written preview. This does not establish behavior in ChatGPT, Work or a Codex session.
