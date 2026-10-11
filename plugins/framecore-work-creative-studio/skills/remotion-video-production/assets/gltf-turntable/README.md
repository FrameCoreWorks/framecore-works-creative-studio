# Product turntable from a glTF model

A Remotion composition that turns the approved 3D model of a product (glTF or GLB) under studio light, with a soft contact shadow and an optional title: a packshot in motion for a shop, an ad or a product page. Every transform comes from `useCurrentFrame()`, so any frame renders on its own and the render matches the preview.

## Compositions

| ID | Size | Frames |
| --- | --- | --- |
| `ProductTurntable` | 1080 × 1080, 30 FPS | 180 (6 s) |
| `ProductTurntableVertical` | 1080 × 1920, 30 FPS | 240 (8 s) |

Props (`defaults` in `src/index.tsx`, or `--props` on the command line):

| Prop | Default | Meaning |
| --- | --- | --- |
| `model` | `sample-product.glb` | File in `public/`: the approved model of the real product |
| `turns` | 1 | Full turns over the composition; 1 with `settleFrames: 0` loops seamlessly |
| `startAngle` | -30 | Degrees; the side shown on frame 0 |
| `tilt` | 14 | Degrees the camera looks down |
| `background`, `floor` | warm greys | Canvas and floor colours (the brand kit's background and a darker tone of it) |
| `title`, `subtitle` | illustrative | Exact copy; empty strings for none. The title is on screen from frame 0 |
| `textColor`, `fontFamily` | dark brown, Arial | Brand values; a brand font must be installed or loaded by the project |
| `settleFrames` | 12 | The model rises into place over these frames; 0 keeps it still from frame 0 |

The loader waits for the model before any frame is captured (`delayRender`), centres it, stands it on the floor and scales it to a fixed height, so models in any unit frame the same way. A model that fails to load stops the render with its path instead of rendering an empty stage.

## The model

- **Only an approved model of the real product.** Ask for the client's GLB or glTF (from the manufacturer, a CAD export or a photogrammetry scan) with the right to use it. Check its materials and colours against product photos before rendering; a generic or invented model of a real product is not a packshot.
- **Size.** Keep the file under about 20 MB and textures at 2048 px or less; compress large textures before copying the file into `public/`.
- **The sample.** `public/sample-product.glb` is an original synthetic jar made by [`tools/make_sample_glb.py`](tools/make_sample_glb.py) (standard library only, `npm run sample` rewrites it). Its label covers only the front so the turn is visible; it is a placeholder, not a product.

## Run it

Copy this folder to a new authorized project outside the installed plugin, then:

```sh
npm ci
npm run typecheck
npm run still                       # out/frame-45.png
npm run render                      # out/turntable-1x1.mp4
npm run render:vertical             # out/turntable-9x16.mp4
npx remotion render src/index.tsx ProductTurntable out/product.mp4 --props '{"model":"product.glb","title":"…","subtitle":"…"}'
```

WebGL needs a browser that can draw it. Where Remotion's own browser cannot start, pass an installed headless shell with `--browser-executable` and software GL with `--gl=swiftshader` (slower, same picture); `remotion.config.ts` asks for `angle` by default. Remotion needs a company licence for some companies; check its terms before client work.

## Check it

Look at frames 0, the middle and the last at full size and at phone size: the label side faces the camera when it should, nothing is cut by the frame, the title does not overlap the model, and the shadow stays under the product. Watch the whole render once at normal speed; with `settleFrames: 0` and whole `turns`, the last frame should lead back into the first.

## Evidence

Checked on 2026-10-11 in a Linux container with Node.js 22, Playwright's Chromium headless shell and `--gl=swiftshader`: with this lockfile, `npm ci`, `npm run typecheck`, the frame-45 still and a full `ProductTurntable` render (1080 × 1080, 30 FPS, 180 frames by ffprobe); with the same direct pins, stills at frames 0 and 120 and frame 60 of `ProductTurntableVertical`. Not run: GPU rendering, macOS, Windows, a client model.
