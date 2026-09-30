
# Output Critic Iteration

Read [Studio integration authority](../../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to review produced outputs against the brief, references, prompts, copy locks, expected observables, and acceptance criteria. It decides accept, fix, rerun, loop back, or exclude.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- Generated, edited, coded, written, or packaged outputs need quality review.
- The workflow needs a delivery allowlist or rejection list.
- Defects require corrected instructions, rerun guidance, or loopback to an upstream role.

Do not use this skill to approve unchecked, uncertain, or rejected assets for delivery.

For static graphics, read [static graphic review](references/static-graphic-review.md)
and the material diagnosis only when an observed defect calls for it. One
incorrect required string or protected-property drift blocks acceptance;
prompt completeness is not evidence of rendered quality.

## Inputs

Required:

- `brief_contract`: objective, constraints, and acceptance criteria.
- `reference_pack`: authority, continuity anchors, and suppression rules when relevant.
- `produced_outputs`: files, prompts, renders, copy, or artifacts to review.
- `expected_observables`: what must be visible, readable, accurate, or structurally present.

Optional:

- `prompt_pack`: prompts or implementation instructions used to create outputs.
- `asset_manifest`: file list and source traceability.
- `copy_locks`: exact text, VO, captions, labels, or legal wording.

## Outputs

Produce a QA / Iteration Report with:

- accepted assets and delivery allowlist
- excluded assets and rejection reasons
- defects grouped by severity
- root cause, loopback target, regression check, and stop recommendation when Loop Protocol applies
- corrected instruction packets or rerun guidance
- prompt-contract checks for text layout, edit preservation, continuity carriers, target verification, and adapter evidence when prompt work is reviewed
- Human Voice and Copy Delivery checks for author context, factual honesty,
  exact copy locks, channel fit, useful structure, controlled-imperfection
  status, and completed editorial-loop evidence when ready-to-use text is reviewed
- loopback target when upstream work must change
- residual caveats

## Process

1. Compare outputs against brief, references, copy locks, expected observables, and the reviewed prompt contract when one exists.
2. Separate objective failures from taste preferences.
3. Decide accept, fix, rerun, loop back, or exclude for each asset.
4. Write corrected instructions only for the smallest necessary change.
5. For Loop Protocol work, name root cause, regression check, and one stop recommendation: `stop_sufficient`, `patch_one_gap`, `ask_user`, or `blocked`.
6. Produce a clear allowlist for `delivery-documentation`.
7. For ready-to-use text, reject a Copy Pack that lacks author context, fact and
   lock review, a completed bounded review with repair only for a diagnosed
   material issue, or a bounded stop decision. A passing draft needs no rewrite.

## Decision Rules

- Reject assets with incorrect required text, broken continuity, missing subject, hidden defects, or untraceable source.
- Use loopback when the prompt, brief, reference pack, or direction was the real failure point.
- Accept with caveat only when the caveat is visible and safe for the user.
- Do not request reruns without explaining what must change.
- For prompt work, reject missing exact text locks, unbounded edit changes, planned-only continuity carriers, unverified target-specific assumptions, and adapter semantic drops before execution readiness.
- Separate a target limitation from a prompt, source, direction, or storyboard defect before choosing a loopback.
- Do not continue a loop only because the result could be better in theory.
- Treat a hook, CTA, list, heading, emoji, hashtag, question, or polished
  formula as a conditional choice. Reject it only when it is unjustified by the
  confirmed channel, goal, audience, legal, timing, or accessibility need.
- Reject fabricated personal experience, sources, testimonials, quotes,
  metrics, results, or promises in final copy.

## Guardrails

- Do not approve assets that were not inspected.
- Do not hide defects to preserve momentum.
- Do not deliver rejected or uncertain assets.
- Do not initiate media generation, uploads or publishing from this review method. Use actually available, authorized inspection tools to review the supplied artifact and report their coverage.
- Do not change approved copy or source facts during QA.

## Handoff

Review gate: `post_execution_fit`.

Hand off to `delivery-documentation` with:

- `accepted_assets`
- `excluded_assets`
- `QA status`
- `root_cause`
- `prompt_contract_checks`
- `continuity_checks`
- `adapter_checks`
- `human_voice_checks`
- `copy_delivery_loop_checks`
- `loopback_target`
- `regression_check`
- `stop_recommendation`
- `caveats`
- `allowlist`

Loop back to the responsible upstream role when defects require rework.

## QA Checklist

- Each reviewed output has a status.
- Rejections include concrete reasons.
- Acceptance criteria were applied consistently.
- Corrected instructions target the real failure.
- Prompt-contract and adapter findings are explicit when they affect acceptance or rerun scope.
- Loop recommendations include severity, root cause, regression check, and stop decision when iteration applies.
- Delivery allowlist contains only accepted assets.
