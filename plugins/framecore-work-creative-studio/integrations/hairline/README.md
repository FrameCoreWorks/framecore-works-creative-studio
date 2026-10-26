# hairline: decision map

Reviewed 2026-10-26 at [`37d2e78`](https://github.com/lucasmarkes/hairline/tree/37d2e78dcb333ab30c3338e28ed4a690364ea014) (package `@lucasmarkes/hairline` 0.5.1, MIT, Copyright (c) 2026 Lucas Marques, [licence](LICENSE)) after the owner sent the repository and chose option 3: a registry entry, the method restated, and a seekable video kit written for Studio. The repository was read as data; none of its scripts was run. No file of it is copied except the licence.

| Part | Decision | Where in Studio |
| --- | --- | --- |
| Ten drawing rules (fixed hit areas, stagger by distance, clamped reach, the stroke as the only highlight, a designed rest, honest paint order, sleeping loops, two clocks, rounded solids, no words in the figure) | adapted for video: the pointer becomes a planned tour; hit testing and sleeping loops have no video equivalent and are dropped | [Hairline kit README](../../skills/hyperframes-workflow/assets/hairline/README.md), sections Draw it, Move it and Look questions |
| Concept method (an object, not a diagram; the features that give it away; one variable; rest as the thumbnail; empty states; the tour as a sentence) | adapted | [Hairline kit README](../../skills/hyperframes-workflow/assets/hairline/README.md#find-the-figure-first) |
| Drawing kernel (`kernel.js`, `Cam`, `rings`, `prism`, springs and tweens on the frame loop) | not copied; rewritten | [`hairline-kit.js`](../../skills/hyperframes-workflow/assets/hairline/hairline-kit.js): Studio's own rounded rings, hull and crease, and pure functions of time (closed-form spring step responses summed, ease-out redirected from the current value) |
| The 33 package figures and the two example figures | not adopted | Studio's example is an original object (a spice rack); a figure is designed per brief |
| `look.mjs`, `validate.mjs`, `read.mjs`, `build.mjs`, `bench.html` | not adopted | Studio checks frames through its motion review and the look questions; the original stays available through the extension |
| `hairline-adopt` (a supplied SVG rebuilt as a figure) | not adapted | available through the extension; the rule that a logo belongs to its owner is kept in the kit README |
| Website, shadcn registry, CI, golden parity files | not adopted | not method |

Registry entry: `hairline` in [extensions.json](../../skills/workflow-orchestrator/assets/extensions/extensions.json). The pinned skills CLI listed both skills on 2026-10-26; no host installation was run.
