---
name: ecommerce-campaign-strategy-director
description: 'Sales campaign strategy for a product, store, PDP, marketplace or launch: offer truth, audiences, angles, asset matrix, tests and claim ledger, before creative work. Brand foundations without a commerce goal go to Marketing.'
---

# Ecommerce Campaign Strategy Director

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research Evidence](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to connect product and offer truth to a practical creative campaign plan. It owns strategy and downstream handoff fields, not prompt writing or media execution.

For a company/store URL, website audit, social sales campaign or an end-to-end offer-to-assets request, use [website to campaign](references/website-to-campaign.md). Inspect accessible evidence before asking one material missing question at a time; a complete brief goes directly to the requested stage. Use the [website audit](templates/website-audit.md), existing strategy pack and [asset card](templates/campaign-asset-card.md) only as needed. Apply [campaign production](references/campaign-production.md) to product fidelity, realistic people, truthful UGC and placement handoffs. [Campaign evidence sources](references/campaign-evidence-sources.md) record dated support and current-specification gaps.

For social-ad analysis or proof-led format selection, use [ad creative analysis](references/ad-creative-analysis.md). For supplied campaign results, use [performance feedback](references/creative-performance-feedback.md) to form hypotheses and the smallest next brief. The optional [creative experiment card](templates/creative-experiment-card.md) records observed ads, baseline/variant revisions and results inside the existing campaign state. Reuse known strategy; these tools add no mandatory questions, generation, account access or publication.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- A product, service, online store, PDP, marketplace listing, landing page, or launch needs a campaign route.
- The user needs audience framing, creative angles, an asset matrix, or a testing plan before production.
- Static, motion, UGC, copy, and prompt work need one shared source of truth.

Use a narrower prompting skill when the strategy, claims, audience, channel, and asset role are already locked.

## Inputs

Required:

- `product_or_service_truth`: what is being sold and which facts are confirmed.
- `objective`: launch, conversion, education, retargeting, listing clarity, or another measurable purpose.
- `audience`: known segment, job to be done, trigger, objection, or best available assumption.

Optional:

- offer, price, promotion, proof, approved claims, disclaimers, channels, formats, source assets, references, brand constraints, and prior performance evidence.

## Outputs

Produce an Ecommerce Campaign Strategy Pack containing:

- assumptions and missing evidence
- website/source audit when requested, commercial constraints, brand basis and prioritized opportunities
- product and offer truth
- audience / JTBD snapshot
- campaign thesis and creative angles
- channel and asset matrix
- creative testing plan
- staged rollout, measurement definitions, actual data limits and reporting decisions
- copy and claim ledger
- static, motion, UGC, storyboard, and prompt handoffs
- risks, approvals, QA gates, and next action

Use [templates/ecommerce-campaign-strategy-pack.md](templates/ecommerce-campaign-strategy-pack.md) for standard or full plans.

## Process

1. Inspect the relevant supplied website or evidence within available read-only capabilities; record actual coverage and access limits. Separate confirmed product facts, offer facts, user claims, assumptions, and unknowns.
2. Define the audience trigger, desired progress, objection, anxiety, and proof need.
3. Write one campaign thesis, then derive up to four materially different creative angles.
4. Build a channel and asset matrix with one business role for every proposed asset.
5. Define the first test batch: hypothesis, fixed variables, tested variable, success signal, and failure meaning.
6. Build the claim ledger before downstream use and remove unsupported proof, testimonials, certifications, or performance promises. Copy approval and softer wording do not substantiate factual claims.
7. Prepare bounded handoffs for the roles and skills that will produce direction, copy, storyboards, prompts, QA, and delivery.

## Decision Rules

- Prefer one clear campaign thesis over a list of unrelated concepts.
- Vary one meaningful creative axis at a time in the first test batch.
- Use `commercial-visual-campaign-director` for static direction and `commercial-video-campaign-director` for motion direction.
- Use `commercial-visual-campaign-director` for a shared campaign family; each static-only execution belongs to `static-graphic-design-creator`, including its integrated copy and prompt compilation.
- Use `ugc` and `copy-voice`, with `humanizer` for polish, for creator scripts, proof framing, VO, supers, and CTAs.
- Use `video-prompt-architect` for the selected video unit and `image-prompt-architect` for a separately requested image operation or target adaptation only after product truth, claims, asset role, and acceptance criteria are stable. Do not bypass the integrated static owner for banners or static ads.
- If a user asks for a single prompt and strategy is already complete, hand off instead of expanding the plan.

## Guardrails

- Planning is provider-neutral and does not authorize generation, provider API calls, uploads or publishing. Read-only public research follows the shared Research Evidence gate and the user's boundary.
- Do not invent claims, reviews, certifications, test results, scarcity, endorsements, or customer evidence.
- A matrix or chart shows hypotheses as hypotheses and only sourced numbers; never invented CTR, ROAS, costs or progress ([presentation and interaction](../pipeline-core/references/presentation-and-interaction.md#campaigns-and-qa)).
- Keep private sales data, customer data, credentials, and unpublished client context out of public artifacts.
- Preserve packaging, product count, logos, approved copy, and material details as explicit fidelity locks.
- Static raster work with visible text follows the kit's native one-pass text-image policy when generation is explicitly requested and available.

## Handoff

Review gate: `direction_fit` before creative production begins.

Hand off with:

- `product_offer_truth`
- `audience_jtbd`
- `campaign_thesis`
- `creative_angles`
- `channel_asset_matrix`
- `test_hypotheses`
- `claim_ledger`
- `source_asset_roles`
- `copy_requirements`
- `fidelity_locks`
- `qa_observables`
- `blocked_items`
- `next_role`
- `audit_revision`, `strategy_revision`, `asset_ids`, `destination_map`, `measurement_plan` and relevant `campaign_context`

## QA Checklist

- Every asset has a channel, business role, message, proof need, and acceptance criterion.
- Product and offer facts are separated from assumptions.
- Factual claims have applicable substantiation or are withheld; copy approval is recorded separately.
- Creative angles are meaningfully different and testable.
- The first test batch does not change several strategic variables at once.
- Downstream roles can act without reconstructing the strategy.
- No provider execution or upload is implied.
