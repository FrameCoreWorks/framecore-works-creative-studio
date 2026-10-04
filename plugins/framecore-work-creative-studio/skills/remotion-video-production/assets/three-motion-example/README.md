# Frame-driven Three.js example

Original synthetic geometry demonstrates the [3D runtime card](../../../hyperframes-workflow/references/motion-toolkit-runtime-cards.md) through the existing Remotion owner. It is a teaching fixture, not a client concept or a claim of host rendering capability.

## Contract

- `FrameCoreThree`: 640 × 360, 30 FPS, 180 frames, 6 seconds; final valid frame 179.
- Opening hold [0,24), alignment [24,132), stable final hold [132,180).
- Three separate blocks align into one group with frame-derived rotation and positions.
- Exact titles are in `src/index.tsx`; Arial is an illustrative system font, not a locked brand asset.
- Intentional silence, opaque output; no downloaded model, font, image or texture.

## Authorized local use

Copy this folder to a new authorized project outside the installed plugin before installing or writing outputs. Use an existing compatible project's dependencies when adapting the scene there. For this isolated example, use its lockfile:

```sh
npm ci
npm run typecheck
npm run studio
npm run still
npm run render
```

Studio is a local server; stop it after review. The CLI may download a browser if no compatible browser is available. Prefer an available supported browser through the documented `--browser-executable` option. The example config selects `angle`; confirm GPU/browser support and exact installed CLI flags before a render. Source presence does not establish these capabilities in ChatGPT.

The pinned packages are example compatibility pins, not an instruction to upgrade an existing project. All `@remotion/*` packages and `remotion` must stay on one matching version. React 19 is paired with Fiber 9. Remote rendering, API use, upload and publication are not part of these commands.

## Inspect and adapt

Check frame 0, 24, 90, 132 and 179; direct/backward seeking must preserve positions and rotations. Inspect the encoded video in normal time and check dimensions, FPS, duration and frame count with an available media inspector. The final hold must stay stable. Retain the existing QA budget and record actual evidence in [toolkit acceptance](../../../hyperframes-workflow/templates/motion-toolkit-acceptance.md).

Use `useCurrentFrame()` for render-critical animation. Do not replace it with a cumulative `useFrame()` loop. Adding models or textures requires source/rights records, completion of loading before capture and renewed visual review. New fonts need explicit availability and layout checks.

Three.js and React Three Fiber are MIT; Remotion and its adapters have their own licensing terms. Preserve notices from installed dependencies. The source here is newly authored and contains no upstream template artwork.
