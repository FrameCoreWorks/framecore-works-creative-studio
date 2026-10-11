# Method catalog

Read when a task needs more than direct execution: a `reasoning_route`, a
`runtime_route`, or a method beyond the compact check. The runtime rules (CQoT
inside the one review, conditional methods and candidate limits) are in
[inference reasoning methods](inference-reasoning-methods.md); nothing here adds
a review pass, a role or permission.

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
