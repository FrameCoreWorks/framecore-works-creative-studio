---
name: hyperframes-workflow
description: Plan, implement, review or repair code-based motion graphics with HTML, SVG, GSAP or HyperFrames, including approved storyboards, deterministic frame state, local previews, render QA and delivery handoffs.
---

# HyperFrames Workflow

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, run the mandatory [Research Evidence](../research-evidence/SKILL.md) preflight; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this when the output is a coded video composition or HTML-to-video production. This is the single public HyperFrames skill: it covers structure, production brief, implementation prompt, GSAP/timeline notes, captions, overlays, render QA, and delivery handoff.

For motion graphics from code, use the [three-stage motion workflow](references/code-based-motion-graphics.md), [storyboard contract](templates/motion-storyboard-contract.md) and [stage prompts](templates/code-motion-stage-prompts.md). Start at the requested stage and preserve actual approval. The [synthetic frame starter](assets/code-motion-starter/README.md) demonstrates shared preview/SVG-export logic without installing a renderer. Research and upstream attribution are linked from the workflow.

For optional 3D, GPU 2D, data animation, Canvas encoding, local Manim clips or Lottie assets, consult [motion toolkit routing](references/motion-toolkit-routing.md) and the selected [runtime card](references/motion-toolkit-runtime-cards.md). Keep one frame authority and use [toolkit acceptance](templates/motion-toolkit-acceptance.md) inside the current QA record. Check actual host capabilities before implementation.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- The requested output is a coded video composition, HTML-to-video sequence, animated title system, captioned scene, or render-ready motion layout.
- A workflow needs scene structure, timing, visual hierarchy, asset needs, and render QA before implementation.
- A production prompt needs implementation-ready scene instructions, component structure, animation timing, and acceptance criteria.
- A motion system needs GSAP-style sequencing, easing, stagger, transition, caption, overlay, or timeline guidance.
- HyperFrames is the coded-video path, not a paid media-provider integration.

Do not use this skill for static raster generation, final delivery packaging, or tool execution without explicit instruction.

## Inputs

Required:

- `brief_contract`: objective, audience, format, and constraints.
- `storyboard_contract`: scenes, beats, timing, or required structure.
- `copy_locks`: exact captions, overlays, titles, labels, or VO text.

Optional:

- `asset_manifest`: source files, approved assets, and exclusions.
- `motion_notes`: timeline, easing, stagger, transitions, camera moves, overlays, and interaction states.
- `implementation_context`: target runtime, component conventions, frame rate, aspect ratio, and renderer limits.
- `delivery_requirements`: output duration, resolution, file type, or manifest needs.

## Outputs

Produce a HyperFrames Production Brief with:

- scene list and timing
- composition size and visual hierarchy
- text and caption timing
- asset needs and source notes
- motion system, timeline, easing, stagger, and transition requirements
- implementation prompt or component brief
- props, layout, state, and reusable variant notes when needed
- render QA checklist
- delivery manifest requirements

## Process

1. Confirm the output is coded video and not a raster graphic replacement.
2. Map scenes, timing, copy locks, composition size, and visual hierarchy before describing animation.
3. Identify required assets, missing inputs, runtime assumptions, and non-goals.
4. Define the timeline: scene starts and ends, entry and exit transitions, easing, stagger, holds, caption timing, and overlay behavior.
5. Convert the structure into an implementation prompt or component brief with clear inputs, props, layout rules, and acceptance criteria.
6. Add render QA checks for blank frames, overlap, readability, clipping, dropped assets, broken animation states, and duration drift.
7. Hand off to production only after the structure, prompt, motion plan, and QA checklist are complete.

For an authorized build or repair in a capable host, implement the approved contract in the actual project, including frame seeking and shared preview/export state. Follow the motion profile for source inspection, fonts/assets, overlaps, readable holds and separate project, temporal-review and encoded-export evidence. A planning-only request still ends at its requested brief or prompt.

## Decision Rules

- If scene structure is missing, route to `storyboard-architect`.
- If copy is not locked, route to `copy-voice` before finalizing captions or visible overlays.
- If source assets are unclear, route to `asset-manifest` or `reference-curator`.
- If the request is deterministic React/TypeScript video rather than HyperFrames, consider `remotion-video-production`.
- Keep coded-video planning provider-neutral and tool-agnostic until the user chooses a runtime.
- Prefer one integrated HyperFrames brief over separate workflow, prompting, and GSAP handoffs.

## Guardrails

- Do not treat HyperFrames as a paid external media-provider path.
- Do not run rendering, install tools, or publish files unless explicitly requested.
- Do not use coded overlays to bypass the one-pass policy for raster graphics with visible text.
- Do not include private paths, unapproved assets, or hidden metadata.
- Do not claim a render succeeded unless a render or visual verification actually ran.
- Do not invent runtime APIs, package versions, or deployment constraints when they were not verified.

## Handoff

Review gate: `structure_fit`.

Hand off to `hyperframes-producer` or `execution-manifest` with:

- `scene_list`
- `timing`
- `copy_locks`
- `motion_system`
- `implementation_prompt`
- `asset_needs`
- `render_constraints`
- `render_qa_checklist`

## QA Checklist

- The plan is clearly coded-video, not static raster generation.
- Every scene has timing and hierarchy.
- Text and captions are readable and timed.
- Asset needs and exclusions are explicit.
- Animation notes include timeline, easing, stagger, and transition intent where relevant.
- The implementation prompt is bounded and does not imply unapproved execution.
- Render QA covers technical and visual failure modes.
