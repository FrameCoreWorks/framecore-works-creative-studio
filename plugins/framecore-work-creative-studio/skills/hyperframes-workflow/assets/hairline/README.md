# Hairline: isometric line figures from rounded solids, for video

A quiet line drawing on a flat plate: every solid is one silhouette and one crease, corners are round, nothing glows, and **the only highlight is a brighter stroke** on what the story points at. The method comes from [hairline](https://github.com/lucasmarkes/hairline) by Lucas Marques (MIT, notice in [LICENSE.upstream](LICENSE.upstream)), whose figures answer a mouse pointer on a web page. This folder is Studio's own code for **seekable video**: a planned tour takes the place of the pointer, and every value is a function of the timeline time.

Use it for a calm object in an explainer, a product or feature film, an app or developer reel, or an empty state: a shelf, a rack, a stack, a device, a tray. Next to [Iso Glow](../iso-glow/README.md): Iso Glow lights what is live in one accent colour with a glow; Hairline stays monochrome and lets one stroke carry the attention. Without glow it renders fast (the 8 s example: about 35 s in a container without a GPU). The interactive original is the pinned `hairline` [extension](../../../workflow-orchestrator/references/extensions.md), for a user who wants pointer figures on a website.

## Files

- [`hairline-kit.js`](hairline-kit.js): projection (`frame`, 30 degree or 2:1 view), rounded rings (`rrect`, `ringAt`, `hull`, `nearRun`, `path`), rounded solids (`solid`, `put`) and time functions (`easeOut`, `tweenAt`, `springStep`, `springAt`, `stagger`, `falloff`, `tourAt`, `drive`). No dependencies; also loads in Node for tests.
- [`examples/spice-rack/`](examples/spice-rack/index.html): two shelves of spice jars, 1080 x 1920, 8 s. A tour visits four jars; the chosen jar lifts and its lid settles on a spring, its neighbours follow less and later, and a read-out in the corner names it. It runs in HyperFrames (GSAP timeline) and through [`capture-html.mjs`](../motion-export/README.md#hand-written-html-to-mp4-without-npm) (`window.renderFrame(t)`, no network); the folder carries its own copy of the kit.

## Find the figure first

1. **An object, not a diagram.** Something that could stand on a desk: a deploy pipeline might be canal locks, a search a sieve, an archive a drawer. Name it in one line: the object, what happens to it, what the read-out says.
2. **What gives it away.** For each kind of part, two or three features the object really has (a jar: a lid wider than the body, a fill line). A part with none of them is a rounded block, and a row of blocks is nothing in particular.
3. **One variable.** The one number or choice that matters (which one, how far, how fast). The tour sets it.
4. **Rest is the thumbnail.** At rest the figure is already a composition: uneven heights or a lean, never a flat or regular row, and one bright mark where the eye starts. An empty state shows the object holding nothing, still whole.
5. **The tour is a sentence.** Three to six stops, each showing a different answer, then a return to rest; not every part in turn.

## Draw it

- **Rounded solids only.** `solid(P, { x, y, w, d, z, h, r })` gives the hull of the foot ring and the top ring, plus one crease: the near half of the top ring, slightly inset. No vertical corner and no twelve-edge box. `r = w / 2` on a square foot gives a cylinder. A thin plate is a low solid, not a second outline. A tapering part passes a smaller `top`.
- **Bright outside, dim inside.** The silhouette uses the edge colour, creases and details the middle one, guides the receding one, set as tokens (`--plate`, `--hi`, `--edge`, `--mid`, `--lo`). No fills other than the plate, no gradients, glows, shadows or opacity tricks.
- **One highlight.** One bright stroke at rest says where to start; when the tour chooses, the bright moves to the choice and the rest mark gives it up. One highlight may cover the parts of one thing (a jar and its lid), never two places.
- **Honest construction.** Plates are filled with the ground colour, and parts are drawn back to front (lower shelf first; smaller `x + y` first; lower `z` first), so no far edge shows through a near solid. Dashed guides go behind what they belong to.
- **No words in the drawing.** Identity comes from geometry; the name of what is chosen goes to a read-out outside the drawing, a few characters, `rest` at rest. No logos on objects unless the figure is the mark itself, with the owner's permission.
- **Legible small.** The silhouette must read at a quarter of the frame width; past about a hundred solids, or with parts thinner than the stroke allows, it will not.

## Move it

- **Two clocks.** A choice (which part) gets a long ease-out: `tweenAt(t, v0, changes)` runs 0.7 s on cubic-bezier(.32, .72, 0, 1). A position gets a spring, k 100, c 18, m 1: `springAt(t, v0, changes)` is the exact sum of step responses, so it needs no state and seeks correctly. Nothing moves linearly, and constants are not invented without a stated reason.
- **Spread from the choice.** Delay each part by `stagger(i, a)` (45 ms per step) so the answer spreads out from the chosen part instead of running down the list; too long a step reads as a queue.
- **A far end.** `falloff(distance, reach, floor)` clamps every lift and lean; at the strongest setting the figure is still composed and inside the frame.
- **Time only.** Everything is a function of `t` through `renderFrame(t)` and `drive(timeline, D, renderFrame)`. Never `requestAnimationFrame`, timers or `performance.now()` in a composition.

## Make one

1. Copy the example folder, keep the kit copy beside it, and change the object, the rest composition, the tour and the read-out.
2. Render with `npx hyperframes render --quality draft` in a HyperFrames project, or `node <skill>/assets/motion-export/capture-html.mjs index.html --out figure.mp4 --width 1080 --height 1920 --seconds 8`.
3. Check the look on stills before the full render: rest, each tour stop, the frame at a quarter width, and the strongest setting. Answer the [look questions](#look-questions), then run the usual [motion review](../motion-review/README.md) and [motion activity](../motion-quality/README.md) steps.

## Look questions

Yes or no on actual frames; a no is fixed before delivery.

1. Can a stranger say what the object is from the small frame, by pointing at the features named in step 2?
2. Is rest a composition with one bright mark?
3. Does the answer spread from the choice and fall off with distance, not move everything at once or one part alone?
4. Is every solid one silhouette and one crease, with round corners and no vertical corner line?
5. Does nothing show through a near solid?
6. Is exactly one place bright at a time?
7. Does the read-out name the choice in a few characters and say `rest` at rest, outside the drawing?
8. At the strongest setting, is the figure still whole and inside the frame?

## Verification boundary

Verified on 2026-10-26 in a Linux container with Chromium and FFmpeg: the example rendered 240 frames at 1080 x 1920 through `capture-html.mjs` in about 31 to 38 s; two renders matched in content (largest pixel difference 5 of 255, from anti-aliasing, not byte-identical). The HyperFrames render route, the original package and its skills were not run (`NOT_RUN`).
