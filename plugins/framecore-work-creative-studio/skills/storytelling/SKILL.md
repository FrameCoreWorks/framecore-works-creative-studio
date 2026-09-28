---
name: storytelling
description: Use this skill for provider-neutral narrative structure, story beats, emotional arcs, scene logic, continuity, and multi-shot workflows.
---

# Storytelling

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, run the mandatory [Research Evidence](../research-evidence/SKILL.md) preflight; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to shape narrative logic, story beats, emotional arcs, continuity, and multi-shot dependencies for creative workflows before storyboard or prompt work.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- A request needs story structure rather than only visual styling.
- A campaign, video, storyboard, music video, or character sequence needs a clear arc.
- Multi-shot continuity, tension, reveal, or payoff must be planned.

Do not use this skill to replace the brief, evidence, references, copy locks, or final prompt roles.

## Inputs

Required:

- `brief_contract`: goal, audience, deliverable, and constraints.
- `direction_context`: visual, motion, music-video, or campaign direction when available.
- `story_goal`: what the viewer should feel, understand, or do by the end.

Optional:

- `reference_pack`: motifs, continuity anchors, and suppression rules.
- `copy_or_dialogue`: VO, dialogue, captions, or required text.
- `format_constraints`: duration, scene count, channel, or aspect ratio.

## Outputs

Produce Story Structure Notes with:

- premise and narrative promise
- beats and progression
- tension, reveal, or transformation
- emotional arc and payoff
- continuity dependencies
- handoff notes for storyboard, copy, or prompt roles

## Process

1. Define the narrative job of the asset.
2. Establish the premise before listing scenes.
3. Build beats that escalate or clarify.
4. Tie emotional movement to visible or audible events.
5. Mark dependencies that later roles must preserve.

## Decision Rules

- Keep the story proportional to the format.
- Use conflict, contrast, or curiosity only when it fits the brief.
- If the request is purely informational, prioritize clarity over drama.
- If copy is locked, structure around it instead of rewriting it silently.

## Guardrails

- Do not invent evidence, testimonials, personal claims, or source facts.
- Do not skip references or copy locks when they are required.
- Leave final prompt compilation and media execution with their owners; task-relevant read-only research follows the shared research gate.
- Do not overcomplicate short-form commercial assets with unnecessary plot.

## Handoff

Review gate: `structure_fit`.

Hand off to `storyboard-architect`, `motion-direction`, `music-video-direction`, or `copy-voice` with:

- `story_structure`
- `beats`
- `emotional_arc`
- `continuity_dependencies`
- `copy_dependencies`

## QA Checklist

- Premise and payoff are clear.
- Beats fit the requested format.
- Emotional movement is visible or audible.
- Continuity dependencies are explicit.
- The output supports downstream structure without becoming final prompt text.

## Authorship boundary

Supply structure notes to [Screenplay Story Architect](../screenplay-story-architect/SKILL.md) for authored scenes and dialogue. Do not force escalation, conflict or a payoff when the selected artistic form calls for a sustained mood, observational sequence or another deliberate structure.
