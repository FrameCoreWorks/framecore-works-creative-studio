# Motion toolkit runtime cards

Apply only the card required by the [chosen route](motion-toolkit-routing.md). Exact example pins belong to their package manifests; the [source ledger](motion-toolkit-sources.md) records research baselines. Check installed APIs before adapting a different version. These cards are implementation guidance, not a claim that the current host has installed or rendered each tool.

## Three.js through Remotion

**Purpose:** controlled 3D geometry, camera, light and material motion. **Owner:** [Remotion Video Production](../../remotion-video-production/SKILL.md). Start with the original [Three motion example](../../remotion-video-production/assets/three-motion-example/README.md).

- Use `ThreeCanvas` from `@remotion/three` and Remotion's `useCurrentFrame()` / `useVideoConfig()`. Derive transforms from frame values; do not accumulate rotation in React Three Fiber's `useFrame()`.
- Keep all Remotion packages on the same version and check React, React Three Fiber and Three.js peer compatibility. Preserve a working project instead of upgrading it to match a sample.
- A `Sequence` inside the 3D canvas needs `layout="none"`. Distinguish sequence-local frames from explicitly passed master frames.
- Await required models, textures and fonts through the composition's loading contract. An unresolved asset must not produce a silently incomplete frame.
- Keep Remotion's native render path first. Its official Three integration documents `angle` for Chromium OpenGL; verify the actual renderer and host before choosing a flag. CLI configuration and programmatic renderer options are separate surfaces. [Official adapter](https://www.remotion.dev/docs/three)

Review camera framing, clipping, shadow stability and protected geometry at the same frames after different seek orders. A browser 3D preview does not establish encoded-video or GPU availability in another host. Record the exact renderer configuration with render evidence.

## PixiJS 2D scenes

**Purpose:** masks, particles, filters and many independently controlled 2D elements. **Example:** [Canvas toolkit](../assets/motion-toolkit/README.md).

PixiJS v8 initializes in two stages: `new Application()` followed by awaited `app.init(...)`. Use `autoStart: false` and `sharedTicker: false`, then call `app.render()` after setting the full requested state. Use `app.canvas`; do not capture before initialization completes. Fix render dimensions and resolution independently of preview CSS. [Application](https://pixijs.com/8.x/guides/components/application), [ticker control](https://pixijs.com/8.x/guides/components/application/ticker-plugin)

Compute particle positions, opacity, mask bounds and filter uniforms from frame and stable seeds. Avoid accumulated deltas, wall-clock uniforms and frame-dependent random calls. Load and validate resources before capture; font readiness includes the actual required face, not merely a resolved promise. Keep a known baseline state so revisiting an earlier frame clears later effects. Record which renderer supports each shader; WebGL and WebGPU shader programs are not interchangeable.

Use a dedicated scene canvas or a completed composite canvas for export. A DOM label beside a canvas is not part of its encoded pixels. Test transparent areas and filter padding; export must not cut off a glow or inherit stale frame pixels. Dispose only resources owned by the scene. Selected source patterns are attributed in [the adaptation ledger](motion-toolkit-sources.md#pixijs-skills-adaptation).

## D3 data motion

**Purpose:** numeric, chart, hierarchy or geographic geometry in the chosen renderer. **Example:** the data scene in the [Canvas toolkit](../assets/motion-toolkit/README.md).

Use focused modules such as `d3-scale`, `d3-shape` and `d3-interpolate`. For example, `scaleLinear().domain(...).range(...)` maps approved values to coordinates. Compute interpolation progress from the master frame. Keep D3's data functions separate from React-managed DOM and avoid `d3-transition` or timer-driven updates as another clock. [Linear scales](https://d3js.org/d3-scale/linear), [integration guidance](https://d3js.org/getting-started)

Record dataset revision, units, baseline, ordering, missing-value treatment and numeric label rounding. Interpolation must not invent source measurements: distinguish an animated intermediate value from a reported observation. Preserve the approved range across scenes unless the storyboard explicitly explains a change. Precompute or deterministically reconstruct any simulation before seeking; a live force simulation is not inherently seekable. Check identical end values, category identity, axes and readable holds after every seek order.

## Mediabunny Canvas export

**Purpose:** encode supplied Canvas frames and mux the requested compatible media file. Mediabunny does not render arbitrary HTML/CSS or copy separate DOM overlays. In a Remotion project, use the existing native export unless a specific requirement justifies another adapter. **Example:** [Canvas toolkit](../assets/motion-toolkit/README.md).

1. Check actual encoding support with `canEncodeVideo` for the requested codec, dimensions, frame rate and quality configuration; check required audio separately. Use the API signature of the installed pin. Browser codec support, container compatibility and alpha support are separate checks. [Codec checks](https://mediabunny.dev/guide/supported-formats-and-codecs)
2. Create an `Output` with the selected format/target and add a `CanvasSource` video track before `await output.start()`. Declare expected frame rate. [Writing media](https://mediabunny.dev/guide/writing-media-files)
3. For each integer `f` from `0` to `N-1`, await the full scene draw, then await `source.add(f / fps, 1 / fps)`. These values are seconds. Preserve fractional FPS as its exact ratio in configuration. Awaiting writes respects backpressure. Close completed sources and await `output.finalize()` before saving the file. [Canvas source](https://mediabunny.dev/guide/media-sources)

Do not choose a different codec, reduce dimensions, discard required alpha or omit audio silently. Report an unsupported configuration. A memory-backed output consumes memory for the whole file; assess the intended duration and resolution before a larger render. Silence is valid only when declared. Local canvas export does not require microphone or screen-capture permission.

If available, inspect the actual file using `ffprobe -v error -count_frames -show_streams -show_format -of json output.mp4`, substituting its real local filename. Compare width, height, decoded frame count, stream rates, duration, audio and required alpha with the approved contract. A declared frame-rate field or rounded container duration alone is insufficient. Inspect presentation timestamps where needed, then watch the complete result at normal speed. [ffprobe](https://ffmpeg.org/ffprobe.html)

## Manim local clip bridge

**Purpose:** explanatory mathematical or geometric animation. Use an existing discoverable `manim-animation` skill when it is actually available. If absent, keep the bridge as source/contract guidance or execute the example only within an otherwise authorized, capable local environment. Do not install a parallel skill or copy a machine-specific path into the plugin.

The original [Manim example](../assets/manim-motion-example.py) is a starting point; it does not establish runtime readiness. Its declared local baseline is 0.20.1. The separately researched Manim Community 0.21.0 requires Python 3.11 or newer; this is not an instruction to upgrade. Check the selected version's local environment, graphics dependencies and fonts. Use the existing local skill's commands and permissions. TeX-based content needs a functioning TeX setup; do not assume it from the presence of Python. [Version metadata](https://github.com/ManimCommunity/manim/blob/v0.21.0/pyproject.toml)

Use declared scene timing and a fixed seed when randomness is needed. Treat the result as a rendered clip, not a second live clock inside the master composition. Handoff requires editable source, version, actual output/hash, dimensions, FPS, frame count, measured duration, opacity/alpha, audio or declared silence, and mapping to master frames. Inspect the clip before importing it into Remotion or HyperFrames; inspect the assembled sequence again for boundary and timing changes. The existing asset manifest and QA record hold this evidence.

## Lottie import and playback

**Purpose:** reuse an authorized animation asset. Lottie players draw supported animation data; they do not convert arbitrary HTML, GSAP or 3D into Lottie.

- **Lottie JSON:** `lottie-web` accepts animation data and can use Canvas or SVG. Disable autoplay and looping for frame-controlled use. Its `goToAndStop(frame, true)` seeks in frames; `setSubframe(false)` selects authored-frame sampling. The [Canvas toolkit](../assets/motion-toolkit/README.md) supplies an original local JSON example. Await initialization and resource readiness before capture. [lottie-web API](https://github.com/airbnb/lottie-web)
- **dotLottie `.lottie`:** this is a compressed archive which can include several animations and resources. Use an available compatible dotLottie player such as `@lottiefiles/dotlottie-web`, with local WASM/resources and explicit animation selection. Do not pass archive bytes directly as JSON to `lottie-web`. Verify the installed player's frame-control API and rendering completion before building capture around it. [dotLottie Web](https://github.com/LottieFiles/dotlottie-web)
- **Remotion:** use its existing `@remotion/lottie` route for supported JSON when appropriate. Confirm asset features, expressions and deterministic frame behavior; a library integration does not validate every imported asset. [Remotion Lottie](https://www.remotion.dev/docs/lottie/)

Map the master time to the asset's own FPS, trim and frame range explicitly. Define end hold, loop or stop behavior without silently stretching duration. Inspect embedded/external resource references, fonts and rights before loading unfamiliar data; do not automatically fetch remote images, scripts or WASM. Compare selected frames after backward and direct seeks. Record `.lottie` playback separately from the bundled JSON example's evidence.
