# Motion toolkit routing

Use this extension inside the existing [code motion workflow](code-based-motion-graphics.md). It adds implementation choices for an approved storyboard. It does not add a workflow owner, shared state, mode or approval gate. Preserve the current interaction mode, work pace, source locks and remaining QA budget.

## Choose by the required result

| Required result | Tool and responsibility | Existing implementation owner | Starting point |
| --- | --- | --- | --- |
| Typography, simple logo motion, diagrams and lightweight vector scenes | HTML/SVG with frame functions or a paused GSAP timeline; HyperFrames when available | Motion Graphics Workflow | Existing [frame starter](../assets/code-motion-starter/README.md) |
| Many graphic objects, masks, particles, filters or custom 2D effects | PixiJS draws the scene; the project frame selects every visible state | Motion Graphics Workflow, or Remotion Video Production when a React composition is selected from the brief or existing project | [Canvas toolkit](../assets/motion-toolkit/README.md) and [PixiJS card](motion-toolkit-runtime-cards.md#pixijs-2d-scenes) |
| Charts, data diagrams and numeric transitions | D3 computes data geometry and interpolation; Canvas, SVG or React draws it | Keep the chosen Motion Graphics Workflow or Remotion owner | [D3 card](motion-toolkit-runtime-cards.md#d3-data-motion) |
| 3D geometry, materials, lights and camera choreography | Three.js and React Three Fiber through `@remotion/three` | Remotion Video Production | [Three motion example](../../remotion-video-production/assets/three-motion-example/README.md) |
| Procedural material treatment with explicit time | Optional Paper Shaders; selected frame drives milliseconds | Keep the current Motion Graphics Workflow or Remotion owner | [Material adapter](../assets/motion-quality/README.md) |
| Synthesized timed sound accents | Optional Tone.js Offline; cue frames map to seconds | Existing Audio Production Director with the current composition owner | [Sound adapter](../assets/motion-quality/README.md) |
| A video file from an existing Canvas scene | Mediabunny encodes supplied frames and writes a compatible container | Keep the scene's existing implementation owner | [Canvas export card](motion-toolkit-runtime-cards.md#mediabunny-canvas-export) |
| Mathematical or geometric explanations | An available local Manim route renders a clip for the existing composition | Existing discoverable local Manim skill, then the selected Motion Graphics Workflow or Remotion owner | [Manim bridge](motion-toolkit-runtime-cards.md#manim-local-clip-bridge) |
| A supplied animation in Lottie JSON or a dotLottie archive | A compatible player renders the approved asset at an explicit frame | Keep the selected Motion Graphics Workflow or Remotion owner | [Lottie import card](motion-toolkit-runtime-cards.md#lottie-import-and-playback) |

Apply the shared [runtime selection policy](code-based-motion-graphics.md#runtime-selection). The rows describe suitable combinations, not automatic selection or installed availability. Prefer the project's working runtime. Add a library only for an observable requirement it satisfies. A small title does not need a 3D renderer; an existing Remotion scene normally keeps Remotion's export. Combining tools is appropriate when their roles are explicit, for example D3 geometry drawn by PixiJS and encoded by Mediabunny.

## Capability check before implementation

Record the actual host, available file access, shell, browser or preview, package versions, renderer and output access. Discover an existing skill through the host's real catalog before using it. A local Manim skill, shell, GPU or browser encoder available on one computer is not automatically available in ordinary ChatGPT, Work or another Codex session.

Use the example's package manifest and README as its execution contract. Copy it into an authorized project directory before installing dependencies; keep the installed plugin package free of `node_modules`, caches and rendered outputs. Preserve an existing project's lockfile and compatible versions. Missing dependencies require authorized installation; loading this reference or viewing the welcome menu grants none. Do not infer provider activation, upload, deployment or external rendering authorization from a toolkit selection.

If execution is unavailable, provide the requested complete source and edit instructions, and report preview/export as NOT VERIFIED. State the specific missing capability. If a simpler route can satisfy the same approved result, propose it with the relevant tradeoff; do not silently change locked delivery properties.

## One clock and one handoff

Keep integer frame count `N`, positive FPS, frames `0..N-1`, and half-open scene intervals from the existing motion contract. The scene's state is a function of the requested frame, approved assets and fixed configuration. Playback only selects frames. Pixi tickers, GSAP playback, Lottie autoplay, D3 timers and 3D real-time loops must not create competing time authorities.

For an imported clip, explicitly map master frames to clip timestamps and document any FPS conversion or retiming. Await assets, fonts, renderer initialization and the requested frame's completed draw before capture. Recheck forward, replay, backward and direct seeks using [toolkit acceptance](../templates/motion-toolkit-acceptance.md) within the existing [motion QA record](../templates/motion-qa-record.md).

Research Evidence supplies current API/rights evidence; existing copy, storyboard, asset, output-review and delivery owners keep their responsibilities. Record the chosen tool and limitations in the current motion contract and Project State. Do not create an additional registry or state machine.

## Evidence boundary

The reference cards describe supported implementation patterns. Release verification and the actual project's QA record state which paths were executed, on which host and with what result. Bundled source, static checks, a displayed canvas and a completed encoded file are separate evidence. None establishes the others. See [sources and adaptation](motion-toolkit-sources.md).
