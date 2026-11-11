# Reel starters

Starter compositions for HyperFrames: a board structure with a persistent frame, continuous motion and slots for the brief's exact copy and photos. A starter is a structure, never an idea: the hook, the words, the photos, the palette, the type and any change to the boards come from the brief and the chosen direction ([reel board system](../../references/reel-board-system.md)).

| Starter | Job | Boards | Length |
| --- | --- | --- | --- |
| [local-service](local-service/index.html) | studio, salon, workshop, clinic | hook claim, three work photos with one-word labels, proof number with its line, the person behind it, booking end card | 24 s |
| [phone-chat](phone-chat/index.html) | app, service or creator reel told as a chat | a phone drawn in code (titanium frame, island, side buttons, glass, home bar), a chat that types and pops with auto-scroll, a shot-list camera with readable holds, a media bubble whose content takes over the frame and closes back onto it, end line | 14 s |
| [frame-break](frame-break/index.html) | a person, mascot or product steps out of its own poster | intact poster with a kicker, the break (the character crosses the frame border while the poster face cracks into tiles around it) with the headline, end line | 8.5 s |
| [headline-wall](headline-wall/index.html) | news, press, reviews or many claims at once | a perspective wall of headline cards with neighbouring columns running in opposite directions; the wall stops for each reading hold while one headline comes forward flat; end line | 9 s |
| [device-showcase](device-showcase/index.html) | an app or a feed shown on a phone | one phone drawn in code with a running feed, in two modes: `orbit` (the camera circles the phone, labels stay facing the viewer) or `screens` (the phone holds the centre, rings pulse behind it, labels pop at its sides); headline, two labels, end line | 8.5 s |

## Use

1. Create a HyperFrames project (`npx hyperframes init <name> --non-interactive`) or use an existing one, then copy the starter's `index.html` over its `index.html`.
2. Put a licensed display font at `fonts/display.ttf` (a [bundled font](../../../pipeline-core/assets/fonts/README.md) or the client's), set the three colours in `:root`, fill `COPY` with the approved exact copy and `PHOTOS` with relative paths to the client's photos. Empty photo slots render as striped placeholders.
3. Retime `BOARDS` to the approved board plan and the music's beat grid; keep the second accent inside each board so no board holds still for more than about 1.5 s.
4. For 4:5, set 1350 in the viewport meta, the `html, body` height and `data-height`; the layout uses width units and adapts.
5. `npx hyperframes lint`, `npx hyperframes render --quality draft`, then [motion activity](../motion-quality/README.md#motion-activity) and a frame review before delivery.

## Phone chat

The phone is drawn in code, with no maker's logo or exact device. Fill `COPY` (contact, status, messages `m1` to `m5`, the takeover headline, the end line) and edit `SCRIPT`: each line has a time `t`, a sender (`them`, `me`) and, for typed replies, `typeFrom`. Give a short line about 0.75 s of reading time and typing about 0.045 s per character. The camera is the `shot(start, move, x, y, scale, roll)` list: keep a hold of 1 to 1.5 s after every move, keep chat shots at a scale up to 2.1 so the whole screen width stays in the frame, and do not zoom out in the middle of a move. The takeover follows [content that pops out of its container](../../references/dense-kinetic-reels.md#build-notes-hyperframes). The chat and the people in it are a staged scene the client approves, never real testimonials, and never a named messenger's interface.

## Frame Break, Headlines and Device showcase

Three original recipes from the 2026-11-11 research intake (scene ideas compared with an owner-supplied list of eleven effect briefs and the Ultra Skills preview; no prompt or code copied). Each draws every frame from one clock (`draw(t)`), so any seek gives the same picture, and every number that shapes the film sits at the top of its script: `COPY`, colours in `:root`, the display font, frame and character boxes, `SEED`, the times `T` and the holds.

- **Frame Break.** Put a poster cropped to the frame ratio in `POSTER` and the character as a PNG cut-out with real alpha in `CUTOUT` (the client's photo, cut out; never a figure drawn in code to look real). Order back to front: the frame's void, the poster face, the tiles, the border, the character, the copy. Until the break the character is masked to the frame; from the break it is drawn in front of the border, and the poster face is replaced by the same picture as tiles, of which those near `BREACH` fly out (`SEED` fixes the crack).
- **Headlines.** `CARDS` fill the wall as texture and may run past the frame; only `hero0` and `hero1` must be read, flat and in the safe area, during `HOLDS`. Column travel is the integral of a speed that eases to zero in each hold, summed on a fixed 1/240 s grid, so the wall truly stands still while a headline is read.
- **Device showcase.** One phone component for both modes: set `MODE`. Posts in `COPY.posts` (and optional screen images in `SHOTS`) run as the feed. In `orbit` the labels ride on the side of the phone that faces the camera; in `screens` the rings grow by size, not by scale, so their line stays thin.

## Evidence

2026-10-17, Linux container, `hyperframes` 0.8.149, Node.js 22, FFmpeg 6.1, Chromium 1194, placeholder copy and placeholder photos: `lint` 0 errors and 0 warnings; draft renders 1080 x 1920 and 1080 x 1350, 30 fps, 24 s. The first version moved only by a slow drift of a flat gradient and failed motion activity (83 % still, a 4.0 s still on the end card); with a textured field, a stronger push-in and a second accent per board it passed: 9:16 15 % still, longest 1.83 s; 4:5 2 % still, longest 0.17 s. With real photos the push-in reads more strongly; not yet run with a client's material or music.

`phone-chat`, 2026-10-30, Linux container, `hyperframes` 0.8.149, Node.js 22, Chrome headless shell 1243, Inter Bold as the display font, placeholder copy, GSAP from a local copy because the CDN was blocked in that container: `lint` 0 errors and 0 warnings; draft render 1080 x 1920, 30 fps, 14 s; motion activity PASS (22 % still, longest still 2.5 s); [text audit](../motion-review/README.md#visible-text-audit) PASS at 1.9, 4.9, 7.6, 9.5 and 13.6 s with two declared exceptions (earlier lines scrolled under the chat header). Built from the phone and camera of the README chat animation (2026-10-30); not yet run with a client's copy or music.

`frame-break`, `headline-wall`, `device-showcase` (both modes), 2026-11-11, macOS, `hyperframes` 0.8.149: `lint` 0 errors and 0 warnings. In a desktop browser at 1080 x 1920 with GSAP 3.14.2 and Inter Bold, the timeline was sought every 0.5 s across the whole film: every visible copy element sat inside the 9:16 safe area (top 10 %, bottom 20 %) with no overflow, each hold lasted at least 1.5 s (Frame Break: kicker 0.9–3.0 s, headline 3.4–6.4 s, end line 6.9–8.5 s; Headlines: each hero 1.6 s with the wall stopped; Device showcase: headline 0.4–2.4 s, each label 1.8 s), and seeking 5 → 1 → 5 s gave the same feed position. Key frames were looked at (intact poster, the break with the character over the border, headline, end card; the wall and a hero; both device modes) and fixed where needed (headline clear of the frame, no tile seams before the break, thin rings). Rendered video, measured duration/FPS with ffprobe, motion activity, a client's material and sound: NOT_RUN (the render was blocked in that session's sandbox).
