---
name: marketing
description: 'Brand strategy and positioning, audiences, values and voice, and general campaign or channel planning without a commerce goal. Store, product or offer campaigns go to Ecommerce Campaign Strategy Director.'
---

# Marketing

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research Evidence](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to plan campaign-level positioning, offer framing, audience fit, asset matrices, channel adaptation, launch kits, and campaign QA without locking final creative execution too early.

For a website/store-led commercial campaign, use the [website-to-campaign profile](../ecommerce-campaign-strategy-director/references/website-to-campaign.md). Supply only missing brand foundations to the existing Ecommerce Campaign Strategy Director's pack: source-based diagnosis, positioning, buying situations, differentiation/proof and voice. Reuse accepted strategy, inspect accessible website facts before questioning and ask one material missing question per response. Do not create duplicate plans or expand brand-only work into a campaign.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## Brand strategy and identity

For brand strategy or identity foundations, use the [brand identity profile](../workflow-orchestrator/references/brand-identity-workflow.md). Produce a Brand Strategy with sourced/user-supplied facts, proposed positioning, audience/use situations, differentiation and proof limits, values, voice principles and the visual direction basis. Reuse known inputs and ask exactly one missing question per response. Hand the strategy revision and selected direction to Static Graphic Design Creator. Do not force campaign-only CTA, launch or asset-matrix fields into brand-only work. For campaign work, use the method below.

## When To Use

Use this skill when:

- A request needs campaign logic before visual direction, copy, storyboard, or prompts.
- The user asks for ecommerce, product, launch, social, creator, or promotional workflow planning.
- Offers, audiences, channels, claims, or asset variants need structure.

Do not use this skill to invent evidence, write final copy, produce final prompts, or execute media tools.

## Inputs

Required:

- `brief_contract`: objective, audience, deliverables, constraints, and acceptance criteria.
- `offer_or_subject`: product, service, idea, event, or asset focus.
- `channel_context`: ecommerce, social, email, marketplace, video, static campaign, or mixed rollout.

Optional:

- `proof_points`: verified claims, benefits, objections, or differentiators.
- `reference_pack`: positioning, competitor, style, or source references.
- `copy_constraints`: required CTA, legal wording, tone, or banned claims.

## Outputs

Produce a Marketing Plan with:

- audience and offer framing
- campaign thesis and message hierarchy
- asset matrix and channel variants
- CTA system
- proof and claim boundaries
- launch or rollout notes
- QA criteria for downstream creative roles

## Process

1. Clarify what the campaign must make the audience do or understand.
2. Separate verified claims from speculative messaging.
3. Map asset variants to channel jobs.
4. Define CTA and message hierarchy before visual execution.
5. Hand off to direction, copy, or storyboard roles.

## Decision Rules

- Keep claims evidence-backed or label them as assumptions.
- Prefer channel-specific variants over generic reuse.
- If audience or offer is unclear, route back to `brief-architect`.
- If proof is missing, avoid strong performance or outcome claims.

## Guardrails

- Do not fabricate testimonials, metrics, guarantees, certifications, or reviews.
- Do not execute media generation or choose external providers.
- Do not turn marketing strategy into final prompt language.
- Do not use private customer examples unless supplied for the task.

## Handoff

Review gate: `direction_fit` when passed into creative direction.

Hand off to `static-direction`, `motion-direction`, `copy-voice`, or `storyboard-architect` with:

- `campaign_thesis`
- `audience_offer_fit`
- `asset_matrix`
- `message_hierarchy`
- `claim_boundaries`

## QA Checklist

- Audience, offer, and channel are aligned.
- Claims are supported or labeled.
- Asset matrix matches the requested rollout.
- CTA system is clear.
- Downstream roles receive constraints, not vague inspiration.
