# Inference Reasoning Methods

This reference defines public, provider-neutral reasoning routes for FrameCore
workflow work. It is an operating policy inside `pipeline-core`, not a new
agent framework, model router, provider integration, or permission to call an
API.

Contents: [meaning and owners](#canonical-meaning-and-owner-selection),
[conditional methods](#one-review-conditional-methods),
[candidate limits](#candidate-limits) and [records and catalog](#records-and-catalog).

Use these methods only when they materially improve quality, safety, or
recoverability. Give a clear goal, constraints and observable acceptance criteria;
do not require a model to reveal or narrate hidden reasoning or force a CoT
script at every model/effort setting. Store compact decision summaries and
contract fields only. Do not store raw chain-of-thought, raw reasoning traces, raw debate transcripts,
private URLs, provider responses, secrets, `.env` files, or copied private
project context.

## Canonical meaning and owner selection

CQoT means **Critical-Questions-of-Thought** in Studio. It tests assumptions,
brief fit, reference and exact-copy locks, feasibility, evidence and possible
regressions. Quality gates and brief-completeness checks remain separate
acceptance criteria, not alternative expansions of this name. This is an
operating method, not a claim of measured effectiveness.

MoE-style means selecting only the useful specialist responsibilities through
the existing role-to-skill map. It does not change the model's neural
architecture, start separate models or prove an independent expert reviewed an
artifact. Use the current runtime unless actual delegation capability and task
authorization exist; record executed agents only from returned evidence.

## One review, conditional methods

Use CQoT as a compact check inside the existing [automatic output review](loop-protocol.md#automatic-output-review),
including Quick and direct-specialist tasks. Check only the dimensions relevant
to the artifact, with up to three critical questions per pass; a compound
question may cover related locks. Do not turn these checks into user onboarding
questions or expose an internal debate. Reuse the shared loop ID, reviewed
revision, evidence, evaluation count and stop decision across owners.

| Need | Method selection within the current task |
|---|---|
| Routine authored idea, prompt or copy | Relevant specialist plus CQoT in the existing review; direct execution remains valid |
| Material factual or current technical claim | Add CoVe: check the claim against attributable sources or observed tests; reuse relevant Research Evidence preflight and leave missing evidence Unknown |
| Several requested or unresolved plausible directions | Add Best-of-N lite with explicit selection criteria; do not invent alternatives to an accepted direction or automatically run paid generations |
| Dependent production stages | Add Plan-and-Solve / Least-to-Most for the bounded handoffs |
| Diagnosed material defect | Use Self-Refine / RCI as the repair step, then recheck affected locks in the same loop |
| Actually authorized tool work | Use ReAct summaries of action and observed result; a plan is not an executed observation |
| Linear planning cannot resolve a concrete conflict or dependency | Use bounded ToT-lite or GoT-lite; record the reason and stop condition before branching |

Method names do not add review passes, roles, mandatory reports or permission.
CoVe is claim verification, not a second general creative review. A question
answered by the same model without evidence does not establish factual truth
or independent verification. Passing work stops unchanged; missing media
evidence remains uninspected. The shared limit is the initial evaluation plus
at most two repair/recheck passes, honoring stricter domain limits. No method
or handoff resets this budget. Record concise findings and necessary evidence,
not private reasoning.

## Candidate limits

- Produce one result when one is requested or a direction is already accepted.
- When comparison is justified, use 2 candidates for routine alternatives and
  3 for high-value campaign, storyboard or prompt-pack choices.
- Use 4 only when requested or when the workflow-orchestrator records a
  concrete expected benefit and stop condition. Respect the user's lower limit;
  do not exceed 4 distinct variants without an explicit request for more.
- Candidate count is a text/strategy comparison limit, not paid-generation or
  upload authorization.

## Records and catalog

Use [conditional quality improvements](quality-improvement-methods.md) for relevant
few-shot examples, tool-backed verification, calibrated comparison and explicitly
requested Reflexion lessons. These extend the current method selection and one
review; they add no routine intake or critic.

When a task needs more than direct execution, record a compact `reasoning_route`
in Project State (and a `runtime_route` when the runtime matters) and choose
from the [method catalog](method-catalog.md): the route contracts, default and
situational methods and the routing rules. Read it only then; ordinary work
needs nothing beyond this page.
