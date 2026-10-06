---
name: brief-architect
description: Use this skill to convert messy notes, user requests, source material, and scattered constraints into a structured Brief Contract for a Codex or ChatGPT workflow.
---

# Brief Architect

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research Evidence](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to convert scattered intent into a Brief Contract that downstream roles can trust. It turns ambiguous requests into objective, audience, deliverables, constraints, exclusions, unknowns, and acceptance criteria.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

For a poster or static graphic, follow [ordinary-language format choices](../workflow-orchestrator/references/intake-and-reference-authority.md#format-choices-in-ordinary-language): ask only missing use (print/internet/both), then familiar paper size or post/story placement, with numbered options. Reuse exact supplied dimensions. Do not expose a mixed paper-code/pixel menu or make technical knowledge a prerequisite for the brief.

## When To Use

For brand strategy, logo or identity-guide briefs, follow the [brand identity profile](../workflow-orchestrator/references/brand-identity-workflow.md). Preserve exact brand-name spelling, real offer, audience, practical goal, intended uses, retained assets and requested scope. Reuse supplied facts and ask exactly one missing question per response; never show the internal pack as a questionnaire or expand a logo-only request into full brand strategy.

Use this skill when:

- The user request is messy, partial, broad, or mixed with source material.
- A creative, campaign, prompt, storyboard, coded-video, or delivery workflow needs a stable brief before specialist work starts.
- The next role needs clear constraints, assumptions, success criteria, or exclusions.

Do not use this skill to create strategy, references, final copy, prompts, QA reports, or delivery manifests.

## Inputs

Required:

- `raw_context`: the user's request, notes, source material, or pasted constraints.
- `expected_output`: the artifact or decision the user expects next.
- `excluded_scope`: anything the user explicitly does not want.

Optional:

- `audience`: buyer, viewer, internal reviewer, client, or platform context.
- `brand_or_subject_notes`: approved terminology, product facts, tone, or visual constraints.
- `deadline_or_format`: size, duration, channel, file type, or delivery condition.

## Outputs

Produce a Brief Contract with:

- objective and desired outcome
- audience and use context
- deliverables and formats
- constraints, exclusions, and non-goals
- known facts, assumptions, and unknowns
- acceptance criteria for the next gate

## Process

1. Separate facts from assumptions and user preferences.
2. Collapse duplicate or conflicting asks into one clear objective.
3. Identify missing inputs that would change the target or deliverable.
4. Preserve user wording for locked names, claims, or required copy.
5. Produce a compact contract that a downstream role can use without rereading the whole conversation.

## Decision Rules

- If the missing information is minor, proceed with a labeled assumption.
- If the missing information changes audience, deliverable, budget, legal claims, or delivery location, ask one concise question.
- Keep creative ideas out unless the user explicitly asked for ideation at the brief stage.
- Do not turn an unresolved conflict into a hidden assumption.

## Guardrails

- Do not invent product claims, testimonials, metrics, brand facts, or source authority.
- Do not include private data, secrets, local-only paths, or customer-specific examples from outside the request.
- Do not skip directly to prompt generation or execution.
- Do not overwrite upstream intent-confirmation decisions.

## Handoff

Review gate: `brief_completeness`.

Hand off to `reference-curator` or `workflow-orchestrator` with:

- `brief_contract`
- `reference_needs`
- `constraints`
- `unknowns`
- `acceptance_criteria`

## QA Checklist

- The objective is singular and testable.
- Deliverables and exclusions are explicit.
- Assumptions are labeled.
- Unknowns are separated from blockers.
- Acceptance criteria can be checked by a later role.
- No strategy, final prompt, generated output, or delivery action is included.
