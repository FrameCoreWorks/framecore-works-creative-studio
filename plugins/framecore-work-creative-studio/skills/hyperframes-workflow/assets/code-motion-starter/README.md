# Synthetic code-motion frame starter

An original teaching asset for the [motion workflow](../../references/code-based-motion-graphics.md). It has no npm dependencies, external requests, generated/client imagery or copied brand assets. Copy this folder into the authorized project before editing; do not store client content or outputs inside the installed shared plugin.

## Example contract

- ID/revision: synthetic-code-motion / 1; example, not client-approved.
- Concept: scattered blocks align (PLAN), connect (BUILD), then receive a review outline (REVIEW).
- 640 × 360, 30 FPS, N = 180, duration = 6 seconds, frames 0..179.
- SC01 [0,72), SC02 [60,144), SC03 [132,180).
- Crossfades [60,72) and [132,144); all scenes use one timeline.
- Readable text holds [12,60), [72,132), [144,180).
- Motion settles in the final scene at frame 156; final stable hold [156,180).
- Exact illustrative copy: PLAN, BUILD, REVIEW. Font: generic sans-serif, not a locked brand font.
- Intentional silence. Original geometry only; no product or logo approximation.
- Criteria: blocks align by frame 45; connector progresses at constant speed from 72 to 120; final title stays visible through frame 179; scene intervals cover the master without adding overlap duration.

## Files and execution

- [motion.mjs](motion.mjs): centralized example contract, pure frame state and SVG rendering.
- [preview.html](preview.html): play/pause, replay and exact-frame controls.
- [export-svg-frames.mjs](export-svg-frames.mjs): the same renderer writes 180 SVG files and a manifest to a new directory.

With available Python 3 and local-server authorization, run from the copied folder:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open the localhost preview.html page. Stop the server when finished. Direct file opening may block JavaScript module loading. With available Node.js and a requested frame export:

```sh
node export-svg-frames.mjs ./output/svg-review
```

The exporter refuses an existing destination. It may leave partial files after a failure; inspect before choosing a new destination. It does not invoke a provider, install packages, rasterize frames, encode a movie, create audio or certify visual quality.

## Production use and verification

This small example teaches shared frame logic; it is not a general renderer or a mandated visual style. For video, implement the approved project with an available Remotion/HyperFrames capture/encoding path. Verify actual APIs, font/asset readiness and codec settings. Do not assume a stock FFmpeg build accepts SVG input.

Use approved fonts and preserve their terms. Generic-font SVG bytes can be deterministic while rendered glyphs differ by environment. Editable text, dimensions or duration changes require scene/hold/layout rechecks; changing totalFrames alone does not retime the hard-coded example.

Record actual execution and inspection in [the motion QA record](../../templates/motion-qa-record.md). The source example itself carries no PASS for normal-speed playback, audio or encoded export.
