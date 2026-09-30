---
name: character-design
description: Use this skill for provider-neutral character design systems, identity anchors, expression sheets, outfit variants, consistency rules, and prompt handoffs.
---

# Character Design

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, run the mandatory [Research Evidence](../research-evidence/SKILL.md) preflight; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to define repeatable character identity systems for static, motion, storyboard, or prompt workflows. It protects continuity before prompts or boards are produced.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- A person, mascot, avatar, creature, or recurring subject must stay consistent across assets.
- Prompting or storyboard roles need identity anchors, pose range, wardrobe, expression limits, or variation rules.
- References contain conflicting character cues that need authority and suppression rules.

Do not use this skill for one-off styling when continuity does not matter.

## Inputs

Required:

- `brief_contract`: objective, audience, and deliverable context.
- `reference_pack`: approved identity references or written character source.
- `continuity_needs`: which features must persist across outputs.

Optional:

- `variant_requirements`: outfit, age, mood, scene, or pose variants.
- `suppression_rules`: features that must not appear.
- `prompt_constraints`: generator-facing limitations or exact wording needs.

## Outputs

Produce a Character System with:

- identity anchors and immutable traits
- proportions, face, hair, wardrobe, expression, and pose rules
- allowed variation ranges
- suppression rules and conflict notes
- prompt handoff notes for `image-prompting`, `video-prompting`, or `storyboard-architect`
- approved identity carrier aliases and their attachment requirements for strict cross-request continuity

## Process

1. Identify canonical character facts and separate them from style inspiration.
2. Define immutable traits before variant traits.
3. Turn visual references into concise continuity language and name the actual reference aliases that can carry strict identity.
4. State what can change by shot, scene, format, or platform.
5. Prepare handoff notes that are concrete enough for prompt authors.

## Decision Rules

- Prefer a few strong identity anchors over a long descriptive inventory.
- If references conflict, prioritize canonical source material and document the conflict.
- Treat wardrobe, props, and expressions as controlled variants unless the brief locks them.
- Preserve the user-required fidelity even when a carrier is missing. Mark execution blocked or conditional until the required identity source can be attached; never silently downgrade strict identity to approximate continuity.
- Keep character design separate from final prompt wording.

## Guardrails

- Do not invent likeness rights, endorsements, biographies, or private identity details.
- Do not execute image or video generation.
- Do not use private reference material unless the user provided it for this task.
- Do not override reference-curator authority.

## Handoff

Review gate: `reference_authority_fit` when resolving identity sources, then `direction_fit` when handed into direction work.

Hand off with:

- `character_system`
- `continuity_anchors`
- `allowed_variants`
- `suppression_rules`
- `prompt_handoff_notes`
- `identity_carrier_aliases`

## QA Checklist

- Immutable and variable traits are separated.
- Canonical references are named or summarized.
- Suppression rules are actionable.
- Prompt handoff notes avoid vague adjectives.
- Strict identity requests identify actual reusable carriers rather than only repeated description.
- The system supports the requested formats without executing generation.

## Human reference capture

For an actual person, use the [human reference capture card](../image-prompt-architect/assets/human-reference-capture-card.md). Ask for useful missing views and expressions instead of inferring unseen anatomy. Preserve natural skin, facial proportions and identity; stylization or beautification requires the requested scope. A reference sheet is an input carrier, not proof that a later generation preserved identity.

## Identity, reference sheets and local repair

Use [the human identity workbook](references/human-identity-workbook.md) for view-specific source evidence, raw realism, orientation, identity sheets and scoped drift repair. Its packet and worked scenarios are conditional aids; do not turn a single portrait into a full intake.
