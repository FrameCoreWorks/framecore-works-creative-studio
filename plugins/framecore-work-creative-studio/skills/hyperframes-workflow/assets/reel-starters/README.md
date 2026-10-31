# Reel starters

Starter compositions for HyperFrames: a board structure with a persistent frame, continuous motion and slots for the brief's exact copy and photos. A starter is a structure, never an idea: the hook, the words, the photos, the palette, the type and any change to the boards come from the brief and the chosen direction ([reel board system](../../references/reel-board-system.md)).

| Starter | Job | Boards | Length |
| --- | --- | --- | --- |
| [local-service](local-service/index.html) | studio, salon, workshop, clinic | hook claim, three work photos with one-word labels, proof number with its line, the person behind it, booking end card | 24 s |
| [phone-chat](phone-chat/index.html) | app, service or creator reel told as a chat | a phone drawn in code (titanium frame, island, side buttons, glass, home bar), a chat that types and pops with auto-scroll, a shot-list camera with readable holds, a media bubble whose content takes over the frame and closes back onto it, end line | 14 s |

## Use

1. Create a HyperFrames project (`npx hyperframes init <name> --non-interactive`) or use an existing one, then copy the starter's `index.html` over its `index.html`.
2. Put a licensed display font at `fonts/display.ttf` (a [bundled font](../../../pipeline-core/assets/fonts/README.md) or the client's), set the three colours in `:root`, fill `COPY` with the approved exact copy and `PHOTOS` with relative paths to the client's photos. Empty photo slots render as striped placeholders.
3. Retime `BOARDS` to the approved board plan and the music's beat grid; keep the second accent inside each board so no board holds still for more than about 1.5 s.
4. For 4:5, set 1350 in the viewport meta, the `html, body` height and `data-height`; the layout uses width units and adapts.
5. `npx hyperframes lint`, `npx hyperframes render --quality draft`, then [motion activity](../motion-quality/README.md#motion-activity) and a frame review before delivery.

## Phone chat

The phone is drawn in code, with no maker's logo or exact device. Fill `COPY` (contact, status, messages `m1` to `m5`, the takeover headline, the end line) and edit `SCRIPT`: each line has a time `t`, a sender (`them`, `me`) and, for typed replies, `typeFrom`. Give a short line about 0.75 s of reading time and typing about 0.045 s per character. The camera is the `shot(start, move, x, y, scale, roll)` list: keep a hold of 1 to 1.5 s after every move, keep chat shots at a scale up to 2.1 so the whole screen width stays in the frame, and do not zoom out in the middle of a move. The takeover follows [content that pops out of its container](../../references/dense-kinetic-reels.md#build-notes-hyperframes). The chat and the people in it are a staged scene the client approves, never real testimonials, and never a named messenger's interface.

## Evidence

2026-10-17, Linux container, `hyperframes` 0.8.149, Node.js 22, FFmpeg 6.1, Chromium 1194, placeholder copy and placeholder photos: `lint` 0 errors and 0 warnings; draft renders 1080 x 1920 and 1080 x 1350, 30 fps, 24 s. The first version moved only by a slow drift of a flat gradient and failed motion activity (83 % still, a 4.0 s still on the end card); with a textured field, a stronger push-in and a second accent per board it passed: 9:16 15 % still, longest 1.83 s; 4:5 2 % still, longest 0.17 s. With real photos the push-in reads more strongly; not yet run with a client's material or music.

`phone-chat`, 2026-10-30, Linux container, `hyperframes` 0.8.149, Node.js 22, Chrome headless shell 1243, Inter Bold as the display font, placeholder copy, GSAP from a local copy because the CDN was blocked in that container: `lint` 0 errors and 0 warnings; draft render 1080 x 1920, 30 fps, 14 s; motion activity PASS (22 % still, longest still 2.5 s); [text audit](../motion-review/README.md#visible-text-audit) PASS at 1.9, 4.9, 7.6, 9.5 and 13.6 s with two declared exceptions (earlier lines scrolled under the chat header). Built from the phone and camera of the README chat animation (2026-10-30); not yet run with a client's copy or music.
