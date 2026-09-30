# Inference Reasoning Methods

This reference defines public, provider-neutral reasoning routes for FrameCore
workflow work. It is an operating policy inside `pipeline-core`, not a new
agent framework, model router, provider integration, or permission to call an
API.

Contents: [meaning and owners](#canonical-meaning-and-owner-selection),
[conditional methods](#one-review-conditional-methods),
[reasoning route](#reasoning-route-contract), [runtime route](#runtime-route-contract),
[method catalog](#default-methods), [situational methods](#situational-methods),
and [routing rules](#routing-rules).

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

## Reasoning Route Contract

Record a `reasoning_route` inside Project State when a task needs more than
direct execution.

```yaml
reasoning_route:
  task_class:
  complexity: trivial | low | medium | high
  risk: low | medium | high
  reasoning_strategy: direct | decompose | verify | compare | tool_loop | branch | search
  selected_methods:
  candidate_count:
  selection_criteria:
  verification_questions:
  escalation_triggers:
  downgrade_triggers:
  stop_condition:
  raw_trace_storage: forbidden
```

Use `direct` for simple work. Use the smallest stronger route that preserves
the needed gate, handoff, QA, or delivery confidence.

## Runtime Route Contract

When model or runtime choice matters, record a lightweight `runtime_route`.
Prefer tiers and effort levels over brittle exact model names.

```yaml
runtime_route:
  recommended_runtime_tier:
  reasoning_effort: none | minimal | low | medium | high
  runtime_assignment: current_runtime | automation_config | subagent_spawn | unavailable_record_only
  provider_execution_allowed: false
  openai_api_allowed: false
  external_router_adopted_raw: false
```

A runtime recommendation is not permission to call OpenAI API, use external
providers, upload files, run destructive commands, or install routing
infrastructure. Provider execution remains governed by the user’s current
explicit instruction and the public provider-neutral boundary.

## Default Methods

| Method | Public owner roles | Use when | Required output fields |
|---|---|---|---|
| Plan-and-Solve / Least-to-Most | `workflow-orchestrator`, `storyboard-architect`, `instruction-packet-factory` | The task needs decomposition before specialist work. | `reasoning_strategy`, `subtasks`, `next_gate`, `stop_condition` |
| CQoT (Critical-Questions-of-Thought) | Current artifact owner; `qa-iteration` when evidence-led escalation is needed | Every substantive creative artifact needs the compact critical check inside its existing review. | `critical_questions`, `answers_or_gaps`, `required_correction` |
| CoVe | `research-evidence`, `qa-iteration`, `delivery-documentation` | Material factual or technical claims need source- or test-backed verification. | `verification_questions`, `verification_results`, `unresolved_risks` |
| Self-Refine / RCI | `qa-iteration`, `workflow-orchestrator`, target specialist role | A prompt, artifact, or generated output has a diagnosed failure. | `failure_inventory`, `corrected_instruction_packet`, `loopback_target`, `acceptance_test` |
| Best-of-N lite | Direction, copy, prompt, and QA roles | Several plausible strategies, lines, prompts, or routes exist. | `candidate_count`, `selection_criteria`, `selected_candidate`, `rejected_options` |
| ReAct | `research-evidence`, `tool-routing-cost`, `execution-manifest` | Work alternates between reasoning, local checks, tool plans, and observations. | `reason_action_observation_summary`, `tool_boundary`, `next_action` |
| Chain-of-Note / source notes | `reference-curator`, `research-evidence`, `asset-manifest` | Sources, references, or manifests need confidence notes. | `source_notes`, `confidence`, `reference_or_asset_risks` |
| Step-back prompting | `brief-architect`, direction roles | The request is broad, ambiguous, or strategically underspecified. | `generalized_question`, `task_classification`, `specific_route` |
| Meta-prompting / APE-lite | `instruction-packet-factory` | A packet, checklist, or prompt contract needs refinement before specialist work. | `prompt_issue`, `improved_instruction`, `acceptance_criteria` |
| LLM-as-judge / reranking | `qa-iteration`, `workflow-orchestrator` | Candidate outputs need a compact quality decision. | `judge_criteria`, `ranked_candidates`, `decision_reason_summary` |

Default candidate limits:

- Produce one result when one is requested or a direction is already accepted.
- When comparison is justified, use 2 candidates for routine alternatives and
  3 for high-value campaign, storyboard or prompt-pack choices.
- Use 4 only when requested or when the workflow-orchestrator records a
  concrete expected benefit and stop condition. Respect the user's lower limit;
  do not exceed 4 distinct variants without an explicit request for more.
- Candidate count is a text/strategy comparison limit, not paid-generation or
  upload authorization.

## Situational Methods

Use these only when the workflow-orchestrator records why a cheaper route is
insufficient.

| Method | Use when | Guardrail |
|---|---|---|
| ToT-lite | A problem has branching strategic or structural routes. | Limit to 2-3 branches and one selection pass. |
| GoT-lite | Dependencies across references, shots, assets, or manifests matter. | Store a dependency map, not raw reasoning traces. |
| MCTS / tree search | Prompt optimization or route selection needs search over candidates. | Require an eval target, budget, and stop condition. |
| Multi-agent debate | Two specialist roles disagree on a high-impact decision and actual delegation is available and authorized. | Use bounded tasks; distinguish role comparison from executed agents and summarize only findings. |
| PoT / PAL | Computation, schema checks, naming, checksums, or validation need code-like reasoning. | Use local tools only inside approved boundaries. |
| GraphRAG | A durable corpus has many linked entities or references. | Require a defined corpus, source map, and privacy boundary. |
| PromptBreeder / APO-lite | Reusable prompt templates have fixtures or benchmarks. | Do not optimize without an acceptance test or fixture. |

## Routing Rules

The workflow-orchestrator chooses the smallest useful strategy:

1. `direct` for simple tasks.
2. `decompose` for multi-step work using Plan-and-Solve / Least-to-Most.
3. `verify` for material factual or technical claims using CoVe, or evidence-sensitive review using CQoT. The ordinary CQoT output check does not require upgrading a direct task.
4. `compare` for requested or genuinely unresolved multiple candidates using Best-of-N lite and reranking.
5. `tool_loop` for ReAct workflows with local checks or approved tool plans.
6. `branch` for ToT-lite or GoT-lite when linear planning is insufficient.
7. `search` for MCTS/APO-lite only with an explicit budget and acceptance test.

QA rejects a reasoning route when it:

- stores raw reasoning traces;
- adds candidates without a selection criterion;
- continues after the stop condition is met;
- creates a second review loop, restarts a repair budget, forces hidden CoT or
  claims independent experts without executed-agent evidence;
- bypasses provider, upload, Memory Cache, or destructive-command locks;
- treats unverified sources, sidecar output, or old Project State as authority.
