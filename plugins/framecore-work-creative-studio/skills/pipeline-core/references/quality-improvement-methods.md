# Conditional quality improvements

These methods extend the existing owners and [single review](loop-protocol.md#automatic-output-review).
They do not change startup, menus, learning intake, reference authority or execution permissions.
Use only the relevant section. Keep the initial evaluation plus at most two repair/rechecks;
honor stricter domain limits. Passing work stops unchanged. No method resets this budget.
Keep summaries and observable findings, never raw reasoning traces.

## Relevant examples

Before an unresolved creative decision, select one to three compatible examples
from the [decision library](../../commercial-video-campaign-director/references/creative-decision-library.md#retrieval-and-few-shot-use).
Match domain, requested stage, problem and hard constraints before superficial style.
Transfer the decision mechanism and its reason, not the example's title, copy,
client facts or aesthetic. A locked direction needs no new alternatives.
If no example fits, proceed without one. Do not force video examples into a
static workflow or expand a narrow edit into exploration. This is bounded
retrieval and few-shot guidance, not a trained retriever or proven creative uplift.

Record only `example_ids`, `fit_reason` and `transferred_decision` when useful.
Do not embed the whole bank in every prompt or expose a worksheet in Quick delivery.

## Tool-backed verification (CRITIC-inspired)

For an objectively checkable requirement, use the available evidence-producing
tool before accepting it. Reuse CoVe and Research Evidence for material claims.
The tool must actually run; its plan, filename or a model's agreement is not evidence.

| Requirement | Appropriate evidence | Limit |
|---|---|---|
| Exact authored copy | Literal comparison with approved strings | Does not certify text rendered in pixels |
| Raster text | Inspect all required text in the actual image; OCR can locate a suspected mismatch | OCR alone remains unconfirmed; compare exact glyphs, punctuation and pairing |
| Dimensions and duration | Probe the actual file, record command/result and revision | Dimensions/duration do not establish composition, timing quality or sound |
| Numbers and units | Calculate from explicit inputs or compare approved attributable source | A correct calculation does not verify its inputs |
| Required element count | Inspect the relevant actual regions/time range | A plan's count does not establish media content |

The packaged read-only helper `scripts/quality-harness.mjs` can compare a declared
contract and evidence record. It does not run OCR, inspect images, listen to audio,
probe files or authenticate a declaration. Its PASS means the supplied evidence
matches the declared contract **within the recorded scope**, not media certification.
Invoke it only if the host exposes local tools; otherwise perform the same bounded
check with genuinely available evidence and mark missing properties Unknown.

Bind each finding to `artifact_revision`, `property`, `expected`, `observed`,
`method`, `locator` and `result`. Stale, missing, partial or contradictory evidence
cannot pass. Check exact copy without silently normalizing spaces or punctuation.
Missing evidence is Unknown, a demonstrated mismatch is FAIL, and neither counts
as success. Feed one material defect and its smallest correction into the existing
review loop. No generation, upload, retry cost or extra critic is authorized here.

## Calibrated pairwise evaluation

Use comparison only for genuinely unresolved alternatives or evaluating a
proposed change. Never create variants of already accepted work to satisfy this method.
Start with the same brief, locks, evidence scope and named criteria for both outputs.
Use the good, bad and borderline [synthetic anchors](../../commercial-video-campaign-director/assets/decision-examples.json)
to state what satisfies a criterion and what remains uncertain. Anchors are teaching
examples, not Kamil's confirmed taste or a claim of measured effectiveness.

1. Apply hard gates first: facts, exact copy, source/identity locks, authorized
   scope, required carrier and honest evidence. A critical FAIL blocks that output;
   Unknown blocks acceptance pending the missing evidence. No average compensates.
2. Present anonymous A/B in comparable form. Judge specificity, causal clarity,
   hierarchy/readability intent and feasible brief fit only where evidence supports
   them. Prefer concise criterion findings to numeric originality scores.
3. Reverse the presentation order, preserving criteria and candidates. Map each
   verdict back to its candidate ID. This is an order check within one evaluation
   pass, not independent expertise or another repair loop. If the results disagree,
   record `order_disagreement` and leave the decision unresolved. Allow a tie.
4. Pin the decision to the reviewed revisions. Record user's actual preference
   separately; do not overwrite it with the judge result. Compare judge decisions
   against actual owner/user decisions before calling the judge calibrated.

Compact record: `candidate_ids`, `revisions`, `hard_gates`, `criteria`,
`anchor_ids`, `ab_verdict`, `ba_verdict`, `decision`, `decision_reason`,
`owner_decision`, `disagreement`, `evidence_scope`. Owner decisions remain
`not_collected` until actually obtained. A same-model order check is not an
independent review. Avoid sharing private outputs with an external judge without
authorization. A plan comparison does not establish rendered quality.

## Controlled Reflexion lessons

The existing [Workflow Self-Improvement](../../workflow-self-improvement/SKILL.md)
owns explicit retrospectives; it does not run as a hidden background learner.
After an evidenced error and successful correction, record
`error → cause hypothesis → tested correction → acceptance result` using its
[lesson template](../../workflow-self-improvement/assets/reflexion-lesson.template.json).
Keep an unproven cause a hypothesis. If correction was not tested successfully,
keep a failure note or proposal, not a confirmed reusable lesson.

Scope every lesson to user/client/project/domain and the specific trigger.
Add evidence revision, applicability, exclusions and adoption decision.
Store real client lessons only through an authorized private project mechanism;
never place them in the shared plugin. No persistence mechanism means session-only.
A successful test does not authorize persistence or instruction edits.
Explicit scoped adoption is required before reuse as a confirmed lesson; otherwise
its status stays proposed. User corrections and current locks take precedence.
Reject stale, unrelated or contradicted lessons; retire rather than erase audit history.
Reuse at most three relevant adopted lessons without new onboarding or a new loop.

## Offline GEPA pilot

GEPA is a development-time optimizer, not a mandatory creative-task step.
The [repository pilot](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/quality-development-1.3.0.md)
uses the official GEPA engine with an adapter that exposes only one allowlisted
instruction section. It generates candidate proposals; it never patches or publishes
the plugin. Its zero-cost offline mode validates integration with synthetic callbacks,
not creative effectiveness or real model optimization.

For a real run, first define the approved model/provider, data boundary, total
cost cap, maximum task/proposal calls, time limit and stop conditions. Use public
or explicitly authorized redacted examples, separate train/validation/holdout,
and forbid private context, secrets and raw reasoning traces. Tool observations and
short error summaries are sufficient reflective feedback. Evaluate serially.

Reject candidate scope expansion and hard-gate failures before any quality score.
Evaluate the selected proposal on untouched holdout and protected regressions,
then compare it with the baseline using the same calibrated criteria. Require
an actual owner decision before adopting a meaningful change. If holdout does
not improve or any protected behavior regresses, retain the baseline. A budget
exhaustion, no useful progress or exhausted task review budget stops the run.
No automatic adoption, source rewrite, new provider dependency or silent escalation.

## Evidence and method limits

Primary sources: [retrieved few-shot examples](https://aclanthology.org/2022.naacl-main.191/),
[CRITIC](https://arxiv.org/abs/2305.11738),
[LLM judge biases](https://arxiv.org/abs/2306.05685),
[Reflexion](https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html),
[GEPA](https://arxiv.org/abs/2507.19457),
[official adapter API](https://gepa-ai.github.io/gepa/guides/adapters/).
Checked 2026-10-01. These papers support their tested methods/tasks, not a blanket
claim of better Studio designs. Studio's creative benefit needs observed outputs
and owner decisions. Distinguish source checks, offline integration, fresh text use,
saved-host equality, active-client behavior and real media QA in release evidence.
