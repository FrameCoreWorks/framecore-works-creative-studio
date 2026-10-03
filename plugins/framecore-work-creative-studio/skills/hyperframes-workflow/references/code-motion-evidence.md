# Code motion: research and implementation evidence

Research date: 2026-10-03. Scope: official documentation read for this integration, not model execution or a visual benchmark. The initiating three-stage example was supplied by the user; the original social-media post/video was not available for inspection. Do not attribute its visual quality to an inspected demonstration.

## Findings adopted

| Source | Supported fact | Application and limit |
| --- | --- | --- |
| [Remotion fundamentals](https://www.remotion.dev/docs/the-fundamentals) | A composition has dimensions, FPS and duration in frames; rendering is expressed through React state at a frame. | Use explicit composition settings and one frame authority. Does not prove any particular generated composition is good. |
| [Remotion animation](https://www.remotion.dev/docs/animating-properties) | Frame-driven interpolation/springs support animation; browser-time CSS transitions can cause rendering flicker. | Keep render state derived from the frame and choose motion by function. |
| [HyperFrames frame adapters](https://hyperframes.heygen.com/concepts/frame-adapters) | Rendering seeks individual states and waits before capture. Custom adapters are experimental and unnecessary for most composition authors. | Use normal composition authoring, not an invented custom-host API. |
| [HyperFrames timeline guidance](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-animation/adapters/gsap-timeline-and-labels.md) | Registered paused GSAP timelines are seek-driven; explicit start/end values help repeatable seeking. | Verify the installed registration/API before using it. |
| [GSAP seek](https://gsap.com/docs/v3/GSAP/Timeline/seek%28%29/) | Timelines can move to a specified position; event suppression affects callbacks. | Scene correctness must not rely on callbacks that seeking can skip. |
| [HyperFrames rendering guide](https://github.com/heygen-com/hyperframes/blob/main/docs/guides/rendering.mdx) | Local rendering has explicit format, quality and FPS settings. | Verify installed CLI options and actual encoded properties; no automatic cloud/render service. |

Links to mutable documentation are retrieval pointers, not pinned dependency versions. Recheck only changed APIs or requirements. This package adds no npm/runtime dependencies and does not silently upgrade an existing project.

## Model evidence and selection

[Anthropic's Opus 5.5 announcement](https://www.anthropic.com/claude-opus-5-5) describes coding improvements and reports a tester's graphics/polish result in a game-building task. This is vendor-reported evidence, not a controlled motion-design evaluation.

[OpenAI's GPT-6 Astra model reference](https://developers.openai.com/api/docs/models/gpt-6-astra) identifies coding and complex reasoning as supported uses. This supports trying the same contract-based workflow with the user's selected coding model, not predicting aesthetic superiority.

No Astra-versus-Opus motion benchmark was performed. Keep model and effort choices with the actual host/user. Do not silently route to another service, hard-code a winning model, infer rendering tools from a model label, or claim the plugin can switch the host's model.

A later authorized comparison should reuse the same brief, authoritative assets, contract, runtime/version, allowed tools and repair budget. Record actual model/settings, completeness, lock adherence, temporal/visual review, export status and resource use. Blind human review of actual outputs can inform taste; generic coding scores cannot replace it. API calls, model trials and paid rendering require their own valid scope.

## Original packaged example

The frame starter is newly authored synthetic geometry and copy with no client/brand media, downloaded font or provider-generated asset. It demonstrates one shared state/render function for preview and SVG-frame export. It is a teaching example, not an approved brand treatment or evidence of encoded-video readiness. Verification belongs in the repository's release report and in a project's own QA record.
