---
name: copy-voice
description: Write campaign copy, headlines, CTAs, voice-over, supers, caption text and short dialogue lines with locked facts and claims. Polish of existing text goes to Humanizer; narrative scenes to Screenplay Story Architect.
---

# Copy Voice

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research Evidence](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when the workflow needs written copy, voice, captions, supers,
dialogue, product text, campaign lines, CTA variants, or tone polish. Use it
after the brief, audience, claim boundaries, and output format are clear enough
to write without inventing missing facts.

For static graphic headlines, support lines, labels and concept/copy pairing,
read [static graphic copy](references/copy-development-and-human-voice.md).
Keep wording selection separate from typography feasibility and claim evidence.
Use the existing Human Voice review before locking newly written copy; later
polish must not silently change selected words.

## Polish copy and channel limits

For copy in Polish, follow the [Polish copy standard](references/polish-copy-standard.md) (quotes, dashes, no-break spaces, money, dates, time, sentence-case headlines, one form of address) and run the [checker](scripts/pl_copy_check.py) on ready-to-use text where code execution exists: `--fix` applies only typographic fixes, the other findings are decisions. For a named placement, write to the visible length in the [channel specs snapshot](../research-evidence/references/channel-specs-snapshot.md) and check each field with `--channel`. Flag price reductions, paid-content labels, consent text, generated realism and regulated claims in the claim ledger with the [marketing rules snapshot](../research-evidence/references/marketing-rules-snapshot.md). Deliver a multi-field set as a [Copy Pack](assets/copy-pack.template.md). For messages to a client at each project step (questions, offer, concepts, feedback summary, files, payment reminder, request for a testimonial) start from the [client email kit](assets/client-emails.pl.md).

## Teacher materials

For teacher-facing lesson content, worksheets, quizzes, games, explanations, answer keys, rubrics or school communications, use the [teacher profile](../workflow-orchestrator/references/teacher-workflow.md) and [material methods](../workflow-orchestrator/references/teacher-material-methods.md). Own complete original educational text and its content/answer review with Research Evidence inside the same bounded loop. Preserve objectives, prerequisites and supplied facts; do not turn a classroom-material request into Learning Mode or route pedagogical correctness to the static-image critic. Keep student tasks separate from teacher answers.

## Inputs

- Brief, audience, platform, format, language, and desired tone.
- Locked facts, product claims, offer terms, disclaimers, and banned wording.
- Existing copy drafts, hooks, scripts, VO, captions, subtitles, or supers.
- Timing, placement, safe-zone, character-count, or variant requirements.
- Author context: speaker authority, audience, channel, real goal, content
  type, and one confirmed concrete observation, proof point, stake, limitation,
  question, or friction point.
- Handoff target such as prompt pack, storyboard, campaign asset, captions, or
  delivery notes.

## Outputs

- A Copy Pack with final or draft copy grouped by use case.
- Optional variants by audience, platform, length, tone, or funnel stage.
- Claim ledger notes for factual statements that need evidence or approval.
- Human Voice review and Copy Delivery Loop evidence for ready-to-use text.
- Handoff notes for `image-prompting`, `video-prompting`,
  `hyperframes-producer`, `caption-studio`, `qa-iteration`, or
  `delivery-documentation`.

## Process

1. Identify the exact output type, author context, and where the copy appears.
2. Separate locked facts from creative phrasing before writing. Route material
   uncertainty to `research-evidence` instead of inventing proof.
3. Write the smallest useful set of variants. Do not assume a hook, CTA, list,
   heading, emoji, hashtag, question, or promotional structure unless the brief
   or channel calls for it.
4. Keep platform, timing, visual placement, and exact visible-text constraints
   visible.
5. For ready-to-use text, run the bounded sequence `draft -> deep review ->
   revision -> final QA -> delivery` using the existing Loop Protocol. Record
   the Human Voice review, root cause if repaired, regression check, iteration
   count, and stop decision in the Copy Pack.
6. Use `humanizer` for naturalness and voice polish without changing authority,
   facts, or exact locks. Use `qa-iteration` when the review needs independent
   critique, evidence, or a loopback decision.
7. Prepare final handoff notes that preserve exact visible text where required.

## Decision Rules

- If copy contains public facts, statistics, certifications, pricing, or legal
  claims, require an evidence check before final delivery.
- If the user asks for many variants, make a compact matrix instead of a long
  unstructured list.
- If copy will be visible inside a generated image or video prompt, mark exact
  visible text and do not allow later silent rewriting.
- If the brand voice is unknown, ask for a short preference or infer cautiously
  from approved examples.
- If author context cannot be formed without inventing a material fact, ask at
  most one question or use carefully qualified wording.
- Controlled imperfection is off by default. Enable it only for an explicit
  request or confirmed profile in a suitable non-precision channel, and never
  use it to change facts, promises, locks, names, dates, amounts, or respect.

## Guardrails

- Do not invent product claims, offer terms, social proof, awards,
  certifications, medical/legal/financial claims, or customer quotes.
- Do not add provider execution, upload, API-key, or paid-tool instructions.
- Do not override source language unless the user asks for translation.
- Do not hide uncertainty; label copy that depends on missing evidence.
- Keep private names, links, and client details out of public examples.
- Do not fabricate personal experience, client reactions, testing, sources,
  testimonials, quotes, metrics, results, or promises.
- Do not optimize text to conceal AI involvement or imitate a living person's
  distinctive style.

## Handoff

Review gate: `copy_fit`.

Send every ready-to-use Copy Pack through its bounded editorial review. Use
`qa-iteration` when facts, exact visible text, brand tone, compliance, or a
material defect needs independent review. Hand off approved copy to
`image-prompting`, `video-prompting`, `storyboard-board-architect`,
`hyperframes-producer`, `caption-studio`, or `delivery-documentation`
depending on the next artifact.

## QA Checklist

- Copy matches the brief, audience, language, and platform.
- Locked facts and required wording are preserved.
- Claims are either sourced, user-provided, or clearly marked for approval.
- Exact visible text is isolated for image, storyboard, video, or caption use.
- Variants are meaningfully different and not redundant filler.
- The Copy Pack distinguishes `draft` from `ready_to_use`; ready text records a
  completed bounded review with an existing Loop Protocol stop decision. Revise
  only a diagnosed material issue; a passing draft records no repair needed and
  stop_sufficient without changing approved wording.
- No fabricated author experience or unrequested CTA, hook, hashtag, emoji, or
  presentation format was added.
- Handoff target and next review gate are clear.

## Studio text boundaries

Narrative scenes and original dialogue belong to [Screenplay Story Architect](../screenplay-story-architect/SKILL.md); lyrics belong to [Audio Production Director](../audio-production-director/SKILL.md). Review their wording only within the requested scope. Exact user-final text does not require new selection. If a first draft passes the bounded review, record no repair needed and deliver; do not manufacture a rewrite.
