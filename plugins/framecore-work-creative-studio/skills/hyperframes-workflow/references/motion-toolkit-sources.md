# Motion toolkit sources and adaptation

Checked on 2026-10-04. This ledger records source authority and the bounded adaptation; it does not certify installation, render success or host availability. Read [routing](motion-toolkit-routing.md) and only the required [runtime card](motion-toolkit-runtime-cards.md).

## Version and source authority

Package manifests and lockfiles in the examples are the execution pins. An existing project keeps its compatible environment. Current online documentation can move ahead of a pinned version; check that version's source/types before using a newly documented API. Do not update dependencies solely because a newer research baseline appears here.

| Component | Example or research baseline | Primary source and license identification |
| --- | --- | --- |
| Three.js | Example `0.186.0` / upstream r186 | [Three.js](https://github.com/mrdoob/three.js/tree/r186), MIT |
| React Three Fiber | Example `9.8.1` | [React Three Fiber](https://github.com/pmndrs/react-three-fiber), MIT; verify React peer compatibility |
| Remotion and `@remotion/three` | Example `4.0.530`, matching Remotion packages | [Official Three integration](https://www.remotion.dev/docs/three), [Remotion license](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md); separate terms from Three.js |
| PixiJS | Example `8.22.0` | [PixiJS](https://github.com/pixijs/pixijs/tree/v8.22.0), MIT |
| D3 scale module | Example `d3-scale` `4.0.2`; broader D3 research baseline `7.9.0` | [d3-scale](https://github.com/d3/d3-scale/tree/v4.0.2), ISC; [D3 integration](https://d3js.org/getting-started) |
| Mediabunny | Example `1.61.1` | [Mediabunny](https://github.com/Vanilagy/mediabunny), MPL-2.0; [Canvas source](https://mediabunny.dev/guide/media-sources), [codec checks](https://mediabunny.dev/guide/supported-formats-and-codecs) |
| lottie-web | Example `5.13.0`, local JSON playback | [lottie-web](https://github.com/airbnb/lottie-web/tree/v5.13.0), MIT |
| dotLottie Web | Research baseline `0.80.0`; conditional `.lottie` import guidance, not the JSON example's runtime | [dotLottie Web](https://github.com/LottieFiles/dotlottie-web), MIT runtime; asset rights remain separate |
| Manim Community | Existing local example environment `0.20.1`; researched upstream `0.21.0` is not an upgrade instruction | [Manim](https://github.com/ManimCommunity/manim), MIT; [0.21.0 dependency metadata](https://github.com/ManimCommunity/manim/blob/v0.21.0/pyproject.toml) |
| FFmpeg / ffprobe | Use an available local build and record its version/configuration | [ffprobe documentation](https://ffmpeg.org/ffprobe.html), [FFmpeg license/build information](https://ffmpeg.org/legal.html) |

The source license identifiers do not establish permission for imported logos, datasets, fonts, models, music or animation assets. Preserve required notices when redistributing dependencies or adapting third-party source. Inspect applicable dependency/build terms for the actual distribution; the plugin's own license does not replace them.

## PixiJS Skills adaptation

Reference repository: [pixijs/pixijs-skills](https://github.com/pixijs/pixijs-skills/tree/83760c6f53462ca9cecd68055041f5a8c94758ce), commit `83760c6f53462ca9cecd68055041f5a8c94758ce`, dated 2026-10-01. This snapshot identifies its PixiJS baseline as v8.22.0. Its [MIT notice](https://github.com/pixijs/pixijs-skills/blob/83760c6f53462ca9cecd68055041f5a8c94758ce/LICENSE) credits PixiJS, 2026.

| Reviewed pattern | Studio adaptation | Boundary |
| --- | --- | --- |
| Application construction and async initialization | Await initialization, retain fixed render dimensions, use the initialized canvas | No upstream scaffold or global installation |
| Manual rendering and ticker lifecycle | Disable the automatic/shared ticker and render an explicitly requested frame | Do not adopt accumulated realtime deltas for exported motion |
| Resource and scene lifecycle topics | Verify asset/font readiness and release scene-owned resources | Do not broaden execution or external fetching permissions |
| Filter, shader, particle and text topic map | Select only the required effect and check its actual runtime API | No wholesale import of the upstream skill collection or routing rules |

The maintained Studio prose and synthetic examples are original. They use public APIs and selected architectural ideas rather than copying upstream artwork, demos or complete skills. The source repository is credited for its API guidance. If future work copies a substantial upstream portion, retain the corresponding copyright and license text with that portion and record the exact source revision.

## Primary API references

- PixiJS: [Application](https://pixijs.com/8.x/guides/components/application), [ticker lifecycle](https://pixijs.com/8.x/guides/components/application/ticker-plugin).
- D3: [linear scale API](https://d3js.org/d3-scale/linear), [framework integration](https://d3js.org/getting-started).
- Remotion: [Three integration](https://www.remotion.dev/docs/three), [Lottie integration](https://www.remotion.dev/docs/lottie/).
- Mediabunny: [output lifecycle](https://mediabunny.dev/guide/writing-media-files), [media sources](https://mediabunny.dev/guide/media-sources), [format/codec support](https://mediabunny.dev/guide/supported-formats-and-codecs).
- Manim: [Scene](https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html). A rendered clip's properties must be measured after execution.
- Lottie: [JSON player API](https://github.com/airbnb/lottie-web), [dotLottie archive/player description](https://github.com/LottieFiles/dotlottie-web).

## Evidence ownership

Use each example's README for its supported commands, assets, versions and limitations. Release verification reports record the exact source revision and checks actually performed. The [toolkit acceptance template](../templates/motion-toolkit-acceptance.md) attaches current project evidence to the existing motion QA record. A result observed on one host, example, codec or player format applies only to that observed scope.

No new external provider, automatic upload, hosted render service, telemetry permission or native skill installation is introduced by these references. Renderer availability is an observed property of the current session.
