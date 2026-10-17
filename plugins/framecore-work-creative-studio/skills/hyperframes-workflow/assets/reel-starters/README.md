# Reel starters

Starter compositions for HyperFrames: a board structure with a persistent frame, continuous motion and slots for the brief's exact copy and photos. A starter is a structure, never an idea: the hook, the words, the photos, the palette, the type and any change to the boards come from the brief and the chosen direction ([reel board system](../../references/reel-board-system.md)).

| Starter | Job | Boards | Length |
| --- | --- | --- | --- |
| [local-service](local-service/index.html) | studio, salon, workshop, clinic | hook claim, three work photos with one-word labels, proof number with its line, the person behind it, booking end card | 24 s |

## Use

1. Create a HyperFrames project (`npx hyperframes init <name> --non-interactive`) or use an existing one, then copy the starter's `index.html` over its `index.html`.
2. Put a licensed display font at `fonts/display.ttf` (a [bundled font](../../../pipeline-core/assets/fonts/README.md) or the client's), set the three colours in `:root`, fill `COPY` with the approved exact copy and `PHOTOS` with relative paths to the client's photos. Empty photo slots render as striped placeholders.
3. Retime `BOARDS` to the approved board plan and the music's beat grid; keep the second accent inside each board so no board holds still for more than about 1.5 s.
4. For 4:5, set 1350 in the viewport meta, the `html, body` height and `data-height`; the layout uses width units and adapts.
5. `npx hyperframes lint`, `npx hyperframes render --quality draft`, then [motion activity](../motion-quality/README.md#motion-activity) and a frame review before delivery.

## Evidence

2026-10-17, Linux container, `hyperframes` 0.8.149, Node.js 22, FFmpeg 6.1, Chromium 1194, placeholder copy and placeholder photos: `lint` 0 errors and 0 warnings; draft renders 1080 x 1920 and 1080 x 1350, 30 fps, 24 s. The first version moved only by a slow drift of a flat gradient and failed motion activity (83 % still, a 4.0 s still on the end card); with a textured field, a stronger push-in and a second accent per board it passed: 9:16 15 % still, longest 1.83 s; 4:5 2 % still, longest 0.17 s. With real photos the push-in reads more strongly; not yet run with a client's material or music.
