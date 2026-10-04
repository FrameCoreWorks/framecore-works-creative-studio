# Canvas motion toolkit

Three original, synthetic scenes exercise separate capabilities: D3 numeric geometry, PixiJS GPU 2D and Lottie JSON playback. Mediabunny encodes the completed Canvas pixels. This is an editable teaching lab, not an approved brand treatment or an installed host feature.

## Contract and setup

640 × 360 px, 30 FPS, 180 frames, 6 seconds, opaque background and intentional silence. Each scene has an opening hold, motion from frames 24 to 132, and a final hold. System Arial is illustrative; approve and await a suitable font for real work. No external assets, client material, downloaded fonts or provider calls are required.

Copy this entire directory to an authorized project folder before installing anything. Keep `node_modules`, built bundles and rendered media outside the installed plugin. Requires Node.js 20 or newer, npm and a capable browser. Exact direct versions and the dependency graph are recorded in `package.json` and `package-lock.json`.

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm test
npm run build
npm run dev
```

Open the loopback URL printed by the server. It serves only the built example at `127.0.0.1:8766`. Stop it with Ctrl+C. The build uses local dependency files; preview and export do not fetch remote assets. Installation itself downloads dependencies from npm.

## Inspect, seek and export

Select a scene, play or replay it, and scrub the frame control. **Check frame seeking** compares raw Canvas pixel hashes at frames 0, 24, 81, 132 and 179 after direct, sequential and backward rendering. It also requires visible motion. This bounded check does not establish creative quality or every imported asset's behavior.

Choose MP4/H.264 or WebM/VP9 and click **Encode video**, then inspect the encoded preview and download the completed file. Availability is probed for the requested dimensions, FPS and codec. After encoding, the app decodes finalized bytes and checks actual frame count, dimensions, timestamps, duration and absence of audio. Observed contract mismatches report FAIL; unavailable decoding reports NOT VERIFIED while preserving the encoded file for an external inspector. An unsupported format fails visibly; no codec, resolution or audio fallback is silently substituted. Cancellation discards partial output. Memory-backed encoding is intentionally limited to this small example. Review memory use before extending duration or resolution.

```sh
ffprobe -v error -count_frames -show_streams -show_format -of json motion-data.mp4
```

Substitute the actual filename. Require 640 × 360, 180 decoded frames, 30 FPS, six seconds and no audio track. Review actual frames and watch the result. The encoded file has an opaque background; alpha and audio are not implemented in this lab. Check MP4 and WebM separately on each target host.

## Source map

- `timeline.mjs`: pure master-frame state, data, particles and asset-FPS mapping.
- `renderers.mjs`: D3 drawing, stopped Pixi renderer and paused Lottie renderer.
- `lottie-fixture.mjs`: original local animation data; not an archive loader.
- `export.mjs`: awaited frame drawing, timestamped CanvasSource writes and finalization.
- `app.mjs`: preview clock, pixel checks, export and cancellation.
- `timeline.test.mjs`: dependency-free state and mapping checks.

Replace the synthetic data, copy and geometry only under an approved motion contract. Data tween values are intermediate animation values, not additional measurements. This Lottie route supports the bundled JSON fixture; `.lottie` archives require a separate compatible player. Inspect imported references, features, fonts and rights before loading them. Do not add a second timer to D3, Pixi or Lottie.

Use [routing](../../references/motion-toolkit-routing.md), [runtime cards](../../references/motion-toolkit-runtime-cards.md), [sources and license boundaries](../../references/motion-toolkit-sources.md) and [acceptance](../../templates/motion-toolkit-acceptance.md) for real projects. The package includes original source, not vendored third-party library bundles. Dependency licenses and terms remain applicable; preserve notices when distributing a built application.

The Pixi example uses its official `pixi.js/unsafe-eval` compatibility module, whose polyfills avoid generated eval functions. The page retains its restrictive CSP without `unsafe-eval`.
