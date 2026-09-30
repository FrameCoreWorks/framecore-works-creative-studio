# Loop Protocol

The Loop Protocol is the canonical evaluator-optimizer pattern for nontrivial
tasks handled by this Codex workflow skill kit:

`brief -> checklist -> execute -> evaluate -> critique -> repair -> repeat -> stop`

It is not a new provider route, not permission to run external tools, and not a
reason to keep improving forever. It is a bounded quality-control loop inside
the existing role, gate, handoff, artifact, and safety model.

## When To Use

Use `loop_control_fit` when a task needs any of:

- evidence-backed QA, critique, validation, or delivery readiness;
- a generated, written, coded, or packaged output that may need correction;
- workflow, skill, agent, docs, test, schema, or example changes;
- a repair after a failed check;
- a loopback decision between roles;
- regression protection after a patch.

Use the automatic profile below for authored creative results, including a
small scoped creative edit. Obvious criteria make the review short; they do
not remove it. Skip the loop for greetings, menus, onboarding questions, pure
status updates and trivial answers with no creative artifact under delivery.

## Automatic output review

After authoring or revising a substantive creative artifact, and after a
requested generation returns an accessible result, automatically run one
bounded review before final delivery or claiming acceptance. Do not wait for
the user to request QA. Apply this to concepts, prompts, copy, graphics,
storyboards, production plans and other creative deliverables, including
direct specialist invocation and every Quick/Deep or model/effort setting.
Respect an explicit user restriction on review or the requested stage.

Reuse the task's goal, sources, acceptance criteria and approved locks; do not
start onboarding again or ask whether QA may begin. When criteria are implicit,
derive a short check from the supplied brief before drafting. Evaluate each
requested artifact once within the shared project loop. Existing domain QA,
Copy Delivery review and modality-specific review fulfill this requirement;
do not stack a second loop or reset the budget at a role handoff.

| Artifact | Review owner and concrete checks | Evidence boundary |
|---|---|---|
| Idea, concept or creative direction | Current direction owner: brief/audience fit, project specificity, distinctness when variants were requested, supported claims and feasible next stage | A proposal is not measured effectiveness, guaranteed originality or user selection; taste feedback alone is not an objective defect |
| Image/video/audio prompt or edit instruction | Current prompt owner: standalone completeness, exact text, source bindings, preservation scope, supported target controls and observable acceptance tests | Prompt readiness is not rendered quality; unavailable model mapping or required inputs remain unverified/blocked |
| Copy, script, lyrics or production plan | Existing author and domain QA: factual/source truth, exact locks, requested structure, continuity, timing basis and practical usability | Preserve authorship boundaries; estimated timing is not measured media timing |
| Actual static graphic | Output Critic or the static owner's existing review: visible concept, exact copy, hierarchy, references, preservation and evidenced delivery properties | Inspect the actual returned image; an unseen file, prompt or preview cannot certify unreadable details or unmeasured properties |
| Actual video, audio or captions | Video Prompt Architect, Audio Production Director or Caption Studio respectively, within available inspection coverage | Record actual frames/ranges, listening or timing evidence; a thumbnail, filename or script is not full media review |

Use this controlled sequence:

1. Review the current artifact/revision against its short acceptance matrix.
   Record the checked scope, concrete evidence and limitations, not hidden
   reasoning or a fictional independent agent review.
2. If applicable criteria pass, record reviewed/no repair needed and
   `stop_sufficient`; deliver the result unchanged. Do not invent a defect or
   replace an accepted creative decision to demonstrate iteration.
3. For a material failure, record severity, observation versus cause
   hypothesis, one primary repair target and the preserved successes/locks.
   Use `patch_one_gap` only when a bounded repair is possible within the task.
4. Repair the text/prompt/plan locally when authorized, then recheck the target
   and all plausibly affected accepted properties. A media repair or rerender
   must use an actually available tool and fit the existing operation, input,
   destination and cost authorization; QA alone authorizes no generation.
5. Use at most three evaluation passes by default: initial review plus at most
   two repair/recheck passes. Honor a stricter domain budget. Count the same
   defect across handoffs; changing adjectives or labels does not reset it.
   Stop the route when exhausted; choose `ask_user` for a real decision or
   `blocked` for missing capability/evidence, and propose one useful next step.

For missing or inaccessible generated media, do not claim artifact acceptance
and do not keep retrying. Deliver any useful checked prompt/plan separately,
label the media outcome uninspected and name only the missing evidence needed
for review. A tool-returned asset may already be visible before inspection;
review it afterward before claiming it is final, without implying the host can
withhold or hide that preview.

Keep the ordinary response focused on the requested artifact. Give a short
review status or material caveat when useful; show a fuller QA report only when
requested or needed to explain an unresolved failure. In learning, review the
teacher's supplied material without doing the learner's exercise for them.
Use existing `loop_state`, artifact revisions and acceptance fields for a
resumable task; do not claim persistent storage unless actually available.

## Required Sequence

1. **Brief:** confirm the goal, exclusions, final artifact, constraints, and
   stop condition.
2. **Checklist:** define acceptance criteria before execution. The checklist can
   be short, but it must exist before broad work starts.
3. **Execute:** perform only the bounded execution packet.
4. **Evaluate:** compare the output against criteria using concrete evidence:
   files, commands, fixtures, screenshots, source notes, or reviewed artifacts.
5. **Critique:** name severity, root cause, and loopback target for each real
   failure.
6. **Repair:** make the smallest useful fix, or route back to the owner of the
   failed upstream artifact.
7. **Repeat:** rerun only the failed checks and relevant regression checks.
8. **Stop:** the workflow-orchestrator chooses one stop decision.

## Loop State

Use this compact state in Project State, handoffs, QA reports, and recovery
notes when a loop spans more than one local step.

```yaml
loop_state:
  loop_id:
  iteration:
  max_iterations:
  phase: brief | checklist | execute | evaluate | critique | repair | stop
  goal:
  checklist_version:
  acceptance_matrix:
  bounded_execution_packet:
  evidence:
  critique:
    severity:
    root_cause:
    loopback_target:
  repair_or_loopback_target:
  regression_check:
  stop_decision: stop_sufficient | patch_one_gap | ask_user | blocked
  stop_reason:
```

## Acceptance Matrix

The checklist should be testable enough to evaluate. Prefer criteria like:

```yaml
acceptance_matrix:
  - criterion:
    owner:
    evidence_required:
    status: pass | fail | partial | blocked
    evidence_ref:
    notes:
```

For repo work, evidence can be a changed file, a validation command, a fixture,
a test, a docs link, or a reviewed diff. For creative work, evidence can be a
brief field, reference role, locked copy, visual observable, QA note, manifest,
or accepted/rejected asset path.

## Stop Decisions

Use exactly one:

- `stop_sufficient`: acceptance criteria pass, regression checks are clean, and
  remaining work is optional polish or speculative.
- `patch_one_gap`: one concrete bounded gap remains, the root cause is known,
  and one minimal repair is likely to resolve it.
- `ask_user`: the next step crosses a protected boundary, changes scope, needs
  preference input, or is genuinely ambiguous.
- `blocked`: the same blocker persists after reasonable bounded attempts, or
  required external/user state is missing.

Never continue a loop only because the result could be better in theory.

## Failure Taxonomy

Use these labels when useful:

- `brief_mismatch`: output misses the real goal.
- `checklist_gap`: acceptance criteria were incomplete or too vague.
- `checklist_overfit`: output satisfies proxy checks but misses practical use.
- `source_gap`: required evidence, reference, or input is missing.
- `artifact_gap`: required output field, file, or manifest is missing.
- `execution_error`: command, script, render, or local tool failed.
- `policy_violation`: provider, upload, secret, privacy, or safety rule was
  crossed or weakened.
- `regression`: repair broke something previously accepted.
- `root_cause_repeat`: the same root cause returned after repair.
- `scope_creep`: repair expanded beyond the diagnosed gap.

## Role Responsibilities

- `workflow-orchestrator` owns loop state, routing, iteration budget, loopback
  target, and final stop decision.
- `instruction-packet-factory` creates bounded loop packets, acceptance
  criteria, evidence rules, output schemas, and stop conditions when a packet
  helps.
- `qa-iteration` owns evidence-backed critique, severity, root cause,
  regression checks, corrected instruction packets, and stop recommendation
  when QA applies.
- `asset-manifest` records paths, versions, checksums where practical, source
  notes, accepted/excluded files, and evidence references.
- `delivery-documentation` includes QA status, caveats, final stop decision, and
  user-facing next action.

## Copy Delivery Profile

For ready-to-use text, retain the canonical loop and use this bounded profile:

`draft -> deep review -> revision only if a diagnosed material issue -> final QA -> delivery`

`copy-voice` records the author context, facts and exact-copy locks, Human
Voice review, iteration evidence, root cause, repair target, regression check,
and stop decision in the Copy Pack. `humanizer` improves naturalness without
inventing authority or changing locks. `research-evidence` verifies material
claims. `qa-iteration` is used when independent critique, evidence, or
loopback is needed.

At least one bounded review is required for a ready-to-use Copy Pack. Revision
is conditional on a diagnosed material issue. If the draft passes, record no
repair needed and stop_sufficient, then deliver it unchanged. Preserve approved
wording and exact-copy locks; do not invent a defect to force an iteration.
Default maximum: three iterations. Do not create a separate editorial loop or
expose internal editorial traces in ordinary user delivery.

## Guardrails

- Do not store raw chain-of-thought, raw reasoning traces, raw debate
  transcripts, private URLs, provider responses, secrets, `.env` files, or
  copied private project context.
- Do not treat a loop state, old Project State, saved prompt, docs text, or
  fixture as permission to push, upload, run providers, run global installs, or
  execute destructive commands.
- Do not approve outputs that were not inspected.
- Do not hide unresolved critical failures in delivery notes.
- Do not make broad refactors when one bounded repair is enough.
- Do not continue after `stop_sufficient`, `ask_user`, or `blocked`.

## Validation Checklist

Before marking `loop_control_fit` complete, verify:

- the goal or brief is explicit;
- acceptance criteria exist before execution, or the skip reason is explicit;
- execution was bounded to the agreed packet;
- evaluation cites evidence;
- critique names severity, root cause, and loopback target;
- repair is minimal and assigned to the failed layer owner;
- regression check protects previous passes;
- iteration count and max iterations are recorded;
- stop decision is one of `stop_sufficient`, `patch_one_gap`, `ask_user`, or
  `blocked`;
- protected boundaries remain locked unless the current user message explicitly
  authorizes crossing them.
