# Iso Glow: isometric line art that lights up, for video

A monochrome hairline drawing on a dark panel; **one accent colour, only on what is live**, and live things glow. The contrast is the whole effect. The look and its rules come from [iso-glow](https://isoglow.dev/) by April Zhu, built on [iso-figure](https://github.com/MrBongoC/ai-iso-skill) by Tolga Cohce (both MIT, notices in [LICENSE.upstream](LICENSE.upstream)). Upstream makes interactive single-file pages; this folder adapts the method to **seekable video**: the same drawing, driven by time and by the soundtrack instead of clicks.

Use it for a hero object, device, building or small city in a reel, an explainer, a product or music video: a loudspeaker that pumps with the bass, an office tower whose floors light in sequence, a machine whose wires carry pulses on the beat. The interactive original is the pinned `iso-glow` [extension](../../../workflow-orchestrator/references/extensions.md), for a user who wants clickable pages.

## Files

- [`iso-kit.js`](iso-kit.js): the projection kernel and helpers (`frame`, `box`, `lit`, `slits`, `defs`, `envAt`, `drive`, `demoEnvelope`). No dependencies; loads in any page.
- [`examples/bass-speaker/`](examples/bass-speaker/index.html): a HyperFrames composition, 1080×1920, 8 s. An isometric loudspeaker whose woofer, dust cap, tunnel and rim glow and pump with a bass envelope, with a ring of air on every hit. It runs as is on a demo envelope at 108 BPM; the folder carries its own copy of the kit so it renders from its own root.
- [`../motion-sync/audio_envelope.py`](../motion-sync/audio_envelope.py): turns the user's track into the per-frame envelope and hits the drawing follows, and writes it into the composition.

## Make one

1. **Name what lights up and why,** before drawing: the woofer follows the bass, the windows follow the chorus, the wire carries the beat. A figure where nothing reacts to the story or the sound is decoration.
2. **Decompose the object into 3 to 8 boxes** and write `(x, y, z, w, d, h)` down first. +x runs down-right, +y down-left, +z up. Put the long, detailed face on FRONT (the `y = max` face, lower left) or SIDE (the `x = max` face, lower right); only the top, front and side ever show.
3. **Draw back to front** (smaller `x + y` first, lower `z` first); paint order is the only depth sort, so every face needs an opaque fill. Put detail on the face planes: `K.FRONT(x, y + d, z + h)` returns a transform whose local u runs along the face and v downward, so plain rects, circles and text land on the face. Texture comes from repetition (`slits` for window grids, ribs and grilles). Never hand-write skewed polygons.
4. **Light it.** `lit(parent, draw)` draws a part twice: grey hairline and an accent copy inside one shared glow filter. Animate only the accent copy's opacity. At least one large element (a woofer, a lit floor band, a sign, a screen) must read as solid accent at phone size: a faint glow was upstream's most common failure.
5. **Drive it from time.** Copy the example, run `python3 audio_envelope.py track.mp3 --start S --duration D --inject index.html` (bass by default; `--band 2000:8000` for hats) and map the envelope to scale, opacity and a small shake in one `drive(timeline, D, t => ...)` update. Hits (`ENVELOPE.kicks`) start one-shot effects such as expanding rings. Everything is a function of the timeline time, so seeking renders the right frame; never use `requestAnimationFrame`, timers or `performance.now()` in a composition.
6. **Check** with the usual [motion review](../motion-review/README.md) and [motion activity](../motion-quality/README.md) steps, then watch it at normal speed with sound: the pump must land on the hits you hear.

## Rules (from upstream, kept)

- One accent colour through tokens (`--accent`, `--line`, `--body`, `--panel`, ...), never a literal hue inside a figure. Pick the accent for the subject: warm amber or sodium for buildings and night scenes, the brand colour when there is one.
- Only what is live gets the accent. If everything glows, nothing does.
- No real company logos, product silhouettes or trademarks on objects or screens; invent signage and glyphs.
- Filters use `filterUnits="userSpaceOnUse"`: a perfectly horizontal or vertical line has a zero-height box and disappears under a default filter region.
- Escape text before writing it into SVG; clip scrolling screen text to its glass with a `clipPath`.
- A light theme drops all glow: lit parts become flat accent fills and strokes.
- Upstream's pages end with a "Made with ISO-GLOW" footer link. A video made with this adapted kit carries no footer or credit on screen unless the user asks; the notices stay in this folder.

## Cost and limits

- Glow is a blur, and blurs are the slowest thing a software renderer draws. In a Linux container without a GPU, a 23-second 1080×1920 HyperFrames render with one CSS `drop-shadow` per lit element took 13 minutes; the 8-second example, with one shared SVG filter on a few lit groups as `lit` draws them, took 1 minute 20 seconds. Keep the shared filter rather than a filter per element, and draft at `--quality draft`.
- Typography over the drawing needs a dark text shadow to stay legible over lit rings.
- The isometric view is fixed. For an orbiting 3D view use the [Anatomy engine](../anatomy-engine/README.md) or the original iso-glow 3D mode.

## Verification boundary

On 2026-10-18 in a Linux container, the example composition passed `hyperframes lint` (0.8.149), rendered 8 s at 1080×1920 in 1 min 20 s and passed motion activity (11 % still); a full-length version of the same speaker with kinetic lyrics, driven by `audio_envelope.py` output on a supplied song, rendered at 1080×1920 and passed motion activity (3 % still). The owner approved that video's look; host behavior in other runtimes is not verified.
