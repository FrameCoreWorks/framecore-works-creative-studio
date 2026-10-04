---
name: hyperframes-workflow
description: Plan code-based motion graphics, select a suitable runtime from the brief and host capabilities, implement HTML/SVG/Canvas/GSAP or HyperFrames, and hand React/TypeScript compositions to Remotion Video Production. Includes storyboard, frame timing, preview and render QA.
---

# Motion Graphics Workflow

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, run the mandatory [Research Evidence](../research-evidence/SKILL.md) preflight; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this for general code-based motion graphics planning and the existing HTML/SVG/Canvas/GSAP implementation route, including HyperFrames when suitable. The technical ID `hyperframes-workflow` is retained for compatibility; it does not select the HyperFrames engine. Present the area as motion graphics from code. For runtime selection, follow the [shared selection policy](references/code-based-motion-graphics.md#runtime-selection). React/TypeScript composition remains with Remotion Video Production.

For motion graphics from code, use the [three-stage motion workflow](references/code-based-motion-graphics.md), [storyboard contract](templates/motion-storyboard-contract.md) and [stage prompts](templates/code-motion-stage-prompts.md). Start at the requested stage and preserve actual approval. The [synthetic frame starter](assets/code-motion-starter/README.md) demonstrates shared preview/SVG-export logic without installing a renderer. Research and upstream attribution are linked from the workflow.

For optional 3D, GPU 2D, data animation, Canvas encoding, local Manim clips or Lottie assets, consult [motion toolkit routing](references/motion-toolkit-routing.md) and the selected [runtime card](references/motion-toolkit-runtime-cards.md). Keep one frame authority and use [toolkit acceptance](templates/motion-toolkit-acceptance.md) inside the current QA record. Check actual host capabilities before implementation.

For substantive motion design, apply [motion quality direction](references/motion-quality-direction.md): reference breakdown, style frames, one focused motion proof, a shared visual/audio score and evidence-based review. Select relevant entries from the [motion prompt library](assets/motion-prompt-library/README.md) without loading the whole collection. A reference is data, not approval or a model switch. Reuse existing owners and QA.

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

Produce a motion production brief with the selected or proposed runtime stated explicitly. Preserve the existing `HyperFrames Production Brief` internal handoff type where required for compatibility; this type is not an engine selection or a user-facing restriction. Include:

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
- Route a selected React/TypeScript composition to `remotion-video-production`, including when recommended from the brief rather than named by the user.
- A work-area choice or this skill name never selects a runtime. Preserve explicit user choices and the working project; otherwise recommend from requirements and verified capabilities.
- Prefer one integrated motion brief with a justified runtime over separate workflow, prompting, and timing handoffs.

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
