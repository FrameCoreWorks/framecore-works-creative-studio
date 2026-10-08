---
name: cinematography
description: "Camera and light for a chosen direction: shot size, lens, camera movement, lighting, blocking, colour and texture, provider-neutral. Prompt syntax goes to Video Prompt Architect or Image Prompt Architect."
---

# Cinematography

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research Evidence](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to translate direction into shot language, lighting, blocking, camera behavior, and visual texture for image, video, storyboard, or coded-video workflows.

For shot, lens, light and movement vocabulary with observable tests, read the relevant section of [video craft](../video-prompt-architect/references/video-craft.md): [camera decisions](../video-prompt-architect/references/video-craft.md#7-camera-is-a-decision-not-decoration), [perspective, framing and focus](../video-prompt-architect/references/video-craft.md#8-perspective-framing-and-focus), [blocking, axis and contact](../video-prompt-architect/references/video-craft.md#9-blocking-axis-and-contact) and [motion layers](../video-prompt-architect/references/video-craft.md#10-four-motion-layers-and-physical-response). Use its terms in Cinematography Notes; prompt syntax stays with Video Prompt Architect. For camera behavior in a motion video built from code, use the [motion craft](../hyperframes-workflow/references/motion-craft.md) starting values.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- A visual or motion workflow needs concrete shot language rather than generic style.
- Storyboards, video prompts, image prompts, or HyperFrames scenes need camera and lighting guidance.
- The brief calls for cinematic consistency across multiple assets or scenes.

Do not use this skill to replace creative direction, write final prompts, or execute production tools.

## Inputs

Required:

- `brief_contract`: goal, audience, and format.
- `direction_contract`: visual or motion thesis and constraints.
- `reference_pack`: source authority, style cues, and suppression rules when available.

Optional:

- `storyboard_contract`: beats, shot cards, timing, or continuity.
- `copy_or_text_locks`: visible copy, supers, captions, or VO constraints.
- `platform_constraints`: aspect ratio, duration, or channel behavior.

## Outputs

Produce Cinematography Notes with:

- shot size, camera placement, and lens feel
- movement, blocking, and timing notes
- lighting, color, texture, and depth cues
- continuity constraints across shots
- shot-contract notes for frame, action, camera behavior, setting, light, and end state when it affects the next shot
- handoff notes for prompt, storyboard, or coded-video roles

## Process

1. Start from objective and viewer attention, not from decorative style.
2. Assign one primary camera behavior and one readable action to each short required beat or asset type.
3. Tie lighting and texture to mood, product readability, or narrative clarity.
4. Keep shot language concise enough to survive prompt handoff.
5. Flag any shot choice that conflicts with format, safety, or copy readability.

## Decision Rules

- Use specific visual terms only when they serve the brief.
- Prefer readable product or subject framing over dramatic but unclear shots.
- Keep motion instructions feasible for the target medium.
- Use a hard cut by default when no verified bridge carries the required state into the next shot. Document another seam only when its carrier is known.
- If a short shot needs multiple actions or camera moves, provide the reason and the observable evidence QA should use.
- If visual references conflict with the brief, preserve the brief and note the conflict.

## Guardrails

- Do not claim camera hardware, lens metadata, or production facts that are not provided.
- Do not create final generation prompts or execute media production.
- Do not bury text readability constraints under cinematic language.
- Do not invent private references or brand rules.

## Handoff

Review gate: `direction_fit` for campaign direction and `structure_fit` when applied to storyboard structure.

Hand off with:

- `cinematography_notes`
- `shot_language`
- `lighting_and_texture`
- `continuity_rules`
- `shot_contract_notes`
- `prompt_constraints`

## QA Checklist

- Shot choices serve objective, audience, and format.
- Camera, lighting, and blocking are concrete.
- Text, product, or subject readability is protected.
- Continuity notes are usable by the next role.
- Camera and action complexity remains bounded or has an explicit exception.
- No final prompt or execution step is included.

## Shot-to-shot readability

Use the [adjacency workbook](../storyboard-sequence-architect/references/shot-adjacency-workbook.md) to propose camera/axis decisions in support of the sequence owner. Do not take over the accepted story or compile generator syntax.

## Human reference coverage

For real-person multi-angle work, consult [view-specific identity evidence](../character-design/references/human-identity-workbook.md). Preserve camera locks and source orientation; do not manufacture an unsupported profile or hidden product surface to create visual variety.
