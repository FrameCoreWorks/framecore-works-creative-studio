---
name: creative-video-producer
description: Use this skill to coordinate an end-to-end creative video package for reels, Shorts, TikTok, paid social, product films, UGC-style videos, explainers, music-video routes, cutdowns, and local editing, while preserving provider-neutral planning, QA, and delivery gates.
---

# Creative Video Producer

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, run the mandatory [Research Evidence](../research-evidence/SKILL.md) preflight; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to turn a rough video request and available source material into a production-ready package. It coordinates existing roles and specialist skills; it does not become a permanent agent, media provider, or editing runtime.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- The request spans brief, direction, script, storyboard, keyframes, prompts, audio, captions, editing, QA, and delivery.
- The user wants a complete reel, short-form ad, product video, UGC-style video, explainer, music-video route, or cutdown plan.
- Several creative specialists need one shared production state and acceptance criteria.

Use a narrower skill when the user only needs one prompt, one script, caption repair, or a simple delivery note.

## Inputs

Required:

- `video_goal`: audience effect, business purpose, or story objective.
- `format`: duration, aspect ratio, platform, and required variants.
- `source_truth`: approved product, brand, story, claim, character, and copy locks.

Optional:

- brief, references, footage, images, storyboard, script, VO, music/SFX direction, logo files, edit constraints, delivery targets, and existing QA evidence.

## Outputs

Produce a Creative Video Production Pack containing:

- producer preflight and route decision
- source asset roles and missing decisions
- direction, script, beat map, and shot plan
- keyframe and video-prompt handoffs
- VO, dialogue, supers, captions, music, and SFX plan
- local editing and cutdown plan
- per-shot acceptance criteria
- Creative Prompt Contracts for strict image, edit, or video controls when needed
- manifest fields, QA checklist, loopback targets, and delivery status

Use [templates/creative-video-production-pack.md](templates/creative-video-production-pack.md) for nontrivial work.

## Process

1. Run a preflight: confirm goal, inputs, missing route-changing decisions, defaults, exclusions, and next artifact.
2. Establish brief and reference authority, including source roles, ownership uncertainty, product or story truth, claim locks, and continuity anchors.
3. Choose the primary route: commercial, ecommerce, narrative, UGC, music video, explainer, footage-first edit, or coded video.
4. Add `screenplay-story-architect` when narrative writing must be solved before storyboard and prompt work.
5. Build direction, beat map, shot cards, timing, first/last-frame logic, copy, audio, and caption requirements.
   Route ready-to-use copy, VO, dialogue, supers, and substantive caption
   rewrites through `copy-voice` and the bounded Copy Delivery Loop before
   production handoff.
6. Prepare keyframe and video prompt handoffs with observable acceptance criteria, reference-role ownership, per-request attachment plans, and actual continuity-carrier requirements, without executing external tools.
7. Select a local edit route and define asset bin, timeline events, protected windows, cutdowns, and export targets.
8. Run QA against brief, source truth, continuity, copy, product fidelity, audio, captions, platform constraints, and delivery requirements.
9. Route only the failed layer back for minimal repair, then regression-check dependent outputs.

## Decision Rules

- Use `ecommerce-campaign-strategy-director` before production when product, offer, channel, claim, or test strategy is unresolved.
- Use `screenplay-story-architect` before storyboard when story, treatment, dialogue, or scene logic is weak.
- Use `caption-studio` for detailed caption timing, styling, safe zones, and caption QA.
- Use `opencut-video-studio` for footage-first or timeline-first local edit planning.
- Use `remotion-video-production` for deterministic React/TypeScript compositions, reusable props, data-driven variants, and frame-accurate renders.
- Use HyperFrames skills when the requested runtime is specifically HyperFrames or the route is centered on HTML/GSAP composition.
- For motion graphics from code, coordinate the [shared motion contract and stages](../hyperframes-workflow/references/code-based-motion-graphics.md). Preserve existing runtime/approval decisions; connect direction and sequence only when unresolved. Require separate preview, temporal/audio review and encoded-export evidence without adding another state store or QA loop.
- Critical product, packaging, logo, face, character, claim, CTA, or visible-text shots require sequential QA before the route advances.
- A continuation shot may use rewrite-forward only from an accepted actual output, never from a planned end frame.
- A short cutdown is a re-authored variant, not merely a trim of the master.

## Guardrails

- Planning does not activate providers, APIs, uploads, publishing, global installs, or destructive cleanup.
- Never claim a provider run, local render, timeline edit, or file output unless it actually occurred on an available surface.
- Do not upload local or private source assets without explicit current approval and an available approved route.
- Do not invent licensing, claim approval, voice rights, music clearance, product facts, or source provenance.
- Do not treat a polished script, VO, caption, or super as approved final copy
  until its author context, factual locks, and editorial-loop evidence exist.
- Keep generator-specific prompt formatting in the relevant prompt skill; do not attach a universal negative prompt.
- Preserve source files and accepted finals. Exclude superseded or failed outputs from delivery.

## Handoff

Review gate: `workflow_route`, then `post_execution_fit` when outputs exist.

Hand off with:

- `producer_preflight`
- `primary_route`
- `source_asset_roles`
- `truth_and_continuity_locks`
- `direction_and_story_state`
- `beat_and_shot_plan`
- `copy_audio_caption_plan`
- `keyframe_handoff`
- `video_prompt_handoff`
- `local_edit_plan`
- `cutdown_matrix`
- `shot_acceptance_criteria`
- `manifest_fields`
- `qa_status`
- `loopback_target`
- `next_role`

## QA Checklist

- The route is clear and uses the smallest necessary set of roles and skills.
- Missing decisions are explicit and limited to route-changing questions.
- Source assets, claims, product details, story locks, and continuity anchors are traceable.
- Script, storyboard, prompts, audio, captions, edit, and cutdowns agree on timing and intent.
- Critical shots have observable acceptance criteria.
- Failed outputs have a bounded correction target and do not enter delivery.
- Provider and upload boundaries remain explicit.
- The user can see what is ready, blocked, awaiting approval, or next.

## Studio production entry

Follow [the product-photo-to-reel route](../workflow-orchestrator/references/product-film-end-to-end-route.md) for product-film work. Begin with short researched ideas when selection is pending. [Audio Production Director](../audio-production-director/SKILL.md) owns music, SFX, voice production and media-bounded audio analysis in picture-first or music-first work. Route narrative writing to Screenplay Story Architect and commercial wording to Copy Voice. Edit/runtime selection follows the user’s tools and request.

## Creative quality through production

Coordinate the [decision library](../commercial-video-campaign-director/references/creative-decision-library.md), [shot adjacency](../storyboard-sequence-architect/references/shot-adjacency-workbook.md) and [execution handoff](../tool-routing-cost/references/execution-adapter-contract.md) only at the requested stage. Use one state and one bounded review loop.

## Reference and audio packets

Coordinate [production sheets](../storyboard-board-architect/references/production-reference-sheets.md), [identity evidence](../character-design/references/human-identity-workbook.md) and [audio edit decisions](../audio-production-director/references/audio-edit-and-prompt-workbench.md) when those artifacts are requested. Carry one selected revision through each handoff without reopening accepted creative decisions.
