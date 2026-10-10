---
name: pipeline-core
description: 'Shared Studio contracts used by other owners: project state, roles, gates, handoffs, artifact templates, QA loops and delivery discipline. Entry, menus and routing belong to Workflow Orchestrator.'
---

# Pipeline Core

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research Evidence](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill when a task needs Studio's shared workflow contracts in ChatGPT or Codex.

It is the contract layer for roles, gates, handoffs, artifacts, request diagnostics, reasoning routes, Loop Protocol, text-bearing image policy, Humanizer routing, HyperFrames routing, Hipson Adapter routing, and workflow governance.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- A request needs more than one workflow stage or role.
- The task involves brief, references, direction, prompting, QA, delivery, onboarding, or governance.
- The task needs checklist-driven evaluation, critique, repair, regression checks, or a loopback decision.
- The user asks how the kit routes work or what the installed roles do.

Do not use this skill to bypass specialist owners or treat routing as authorization to generate, upload, or replace the user's local preferences.

## Surface Model

- In Codex, Studio runs as a plugin or as one native entry backed by the intact bundle; neither registers project agents or needs project config. Keep a visible Workflow Profile; persist project state only with approval. Role IDs are bounded responsibilities unless the host actually exposes a matching registered agent.
- Where a workspace allows it, Project State may be stored in approved workspace files; role IDs map to registered agents only when the host actually has them.
- On every host, role IDs are bounded responsibilities. Inspect actually exposed file, shell, agent and persistence capabilities. In a chat-only surface keep state in conversation or a handoff. Claim saved files, executed commands or agents only from actual results.
- On either surface, use only capabilities that are actually available. A workflow route never grants provider, upload, API, file-system, or publishing permission.

## Inputs

Required:

- `user_request`: the current task, goal, and any explicit exclusions.
- `workspace_context`: actual installed Skills, visible preferences and accessible artifacts. Include Codex project config only when it exists; use conversation context and user-provided artifacts in ChatGPT.
- `mode`: analyze, plan, edit, generate, review, install, or deliver.

Optional:

- `existing_project_state`: prior gates, handoffs, artifacts, or decisions.
- `local_preferences`: language, tone, QA strictness, display names, and output path.
- `artifact_paths`: brief, reference pack, prompt pack, QA report, or manifests.

## Outputs

Produce one or more of:

- Task Confirmation
- Project State
- Workflow Request Diagnostic
- Loop State
- role route and gate sequence
- reasoning route and runtime route when useful
- handoff notes
- loopback decision
- delivery or governance recommendation

## Process

1. `intent-confirmation` locks goal, exclusions, work mode, expected output, and immediate next step.
2. `workflow-orchestrator` chooses blueprint, only the useful specialist roles (MoE-style responsibility selection), gates, handoffs, conditional reasoning route when useful, and next action. Role selection is not proof of separate agent execution.
3. For nontrivial iterative work, `workflow-orchestrator` activates `loop_control_fit`: brief, checklist, bounded execution, evaluation, critique, minimal repair, regression check, and stop decision.
4. Specialist roles produce contracts, not loose opinions. ChatGPT roles remain temporary and stop after their artifact or handoff is complete.
5. `qa-iteration` reviews produced outputs when assets exist or when evidence-backed critique is needed.
6. `delivery-documentation` packages final notes only after QA or explicit acceptance.

## References

Read only what is needed:

- [references/agent-roster.md](references/agent-roster.md) for role list and responsibilities.
- [references/workflow-operating-model.md](references/workflow-operating-model.md) for stage order and review gates.
- [references/loop-protocol.md](references/loop-protocol.md) for `brief -> checklist -> execute -> evaluate -> critique -> repair -> repeat -> stop`, loop state, repair boundaries, regression checks, and stop decisions.
- [references/workflow-blueprints.md](references/workflow-blueprints.md) for common task routes and loopback boundaries.
- [references/role-skill-map.md](references/role-skill-map.md) for the canonical distinction and mapping between Codex workflow role IDs and supporting public skills on Codex and ChatGPT.
- [references/handoff-matrix.md](references/handoff-matrix.md) for allowed handoffs and required fields.
- [references/gate-registry.md](references/gate-registry.md) for canonical gate names.
- [references/inference-reasoning-methods.md](references/inference-reasoning-methods.md) for compact reasoning routes, runtime route boundaries, candidate limits, and raw trace prohibitions.
- [references/text-image-generation-policy.md](references/text-image-generation-policy.md) for visible text in raster graphics.
- [references/client-projects.md](references/client-projects.md) for the client path from enquiry to acceptance (intake, offer, concepts, revisions, handoff), and [references/brand-kit.md](references/brand-kit.md) for a client's colours, fonts, logo, voice and legal lines.
- [references/prompt-format-and-continuity.md](references/prompt-format-and-continuity.md) for generator-specific prompt fields, independent generation units, continuity carriers, and standalone prompt rules.
- [references/creative-prompting-standard.md](references/creative-prompting-standard.md) for portable image, edit, and video prompt contracts, reference roles, attachment ownership, target verification, rewrite-forward, and adapter evidence.
- [references/humanizer-routing.md](references/humanizer-routing.md) for copy polish routing.
- [references/human-voice-and-copy-delivery.md](references/human-voice-and-copy-delivery.md) for author context, truthful
  Human Voice controls, format-sensitive copy decisions, and the bounded Copy
  Delivery Loop.
- [references/hyperframes-workflow.md](references/hyperframes-workflow.md) for coded-video workflow.

## Decision Rules

- Prefer the smallest route that preserves gates and handoffs.
- Apply CQoT (Critical-Questions-of-Thought) inside the existing output review.
  Use [conditional methods](references/inference-reasoning-methods.md#one-review-conditional-methods)
  for claims, choices or difficult dependencies; do not stack reviews, reset
  repair budgets, force hidden CoT or invent independent expert execution.
- Resolve installed Skills through the active host, not a hard-coded project path. Relative resources belong to the actual Skill directory. Native installation does not supply the repository CLI or register project agents. Map role IDs through [references/role-skill-map.md](references/role-skill-map.md); report missing supporting Skills without inventing or installing them.
- A direct request for one prompt, brief, storyboard, caption plan, review, or other bounded artifact should route to the relevant specialist skill when its inputs are sufficient. Do not start the full pipeline merely because implicit invocation is available.
- Use a multi-stage route when the user explicitly asks for an end-to-end or full workflow, or when the task genuinely spans dependent stages that require shared state, gates, handoffs, or QA.
- An explicit `$pipeline-core` invocation requests governed multi-stage routing, but it does not require irrelevant stages and does not authorize unavailable tools or protected actions.
- Use `loop_control_fit` for nontrivial work that needs QA, correction, validation, delivery readiness, workflow changes, or evidence-backed iteration.
- Use a Workflow Request Diagnostic when the request could be mistaken for install help, a simple prompt, a full creative workflow, QA, delivery, provider execution planning, or workflow improvement.
- Record a compact `reasoning_route` when the task needs decomposition, verification, comparison, a tool loop, branching, or bounded search.
- Prefer public runtime tiers and reasoning effort levels over brittle exact model names when a `runtime_route` is useful.
- Start from a workflow blueprint when the request matches a known pattern, then shrink or expand it based on available artifacts.
- Use role IDs from the public kit. Use local display names only from Codex onboarding config, or user-selected labels in the current ChatGPT conversation.
- Do not skip upstream gates when later roles depend on their artifacts.
- Route standalone commercial/editorial wording or a separately requested Copy Pack through `copy-voice`, use `humanizer` for voice polish when needed, and use `caption-studio` for timing and accessibility. Keep static-only design copy inside `static-graphic-design-creator`, narrative dialogue with screenplay and lyrics with audio.
- Route ready-to-use copy through `copy-voice` with the Human Voice and Copy
  Delivery policy. Use the existing Loop Protocol for at least one bounded
  review. Revise only a diagnosed material issue; when the draft passes, record
  no repair needed and stop_sufficient. Do not create a second editorial loop.
- Route deterministic React/TypeScript video composition through `remotion-video-production`.
- For brand strategy, logo systems and identity guides, use the [brand identity profile](../workflow-orchestrator/references/brand-identity-workflow.md) and its existing-owner stage handoffs. Keep one Project State; route strategy to Marketing, integrated visual work to Static Graphic Design Creator and the requested guide/file package to Delivery Documentation. Do not expand logo-only work into a full brand project.
- For static-only work, `static-direction` routes to `static-graphic-design-creator`
  as the integrated owner of concept, layout, catalog guidance, visible copy,
  text feasibility and prompt compilation. Do not add a second Copy Voice,
  Humanizer or Image Prompt intake for its internal stages. Use shared reference,
  execution, inspected QA and asset/delivery owners only for missing requested
  work. A separately requested copy deliverable or non-static artifact in a mixed
  campaign may use its specialist; pass accepted context and exact-copy locks.
- Route motion graphics from code (kinetic type, animated titles and logos, explainers, app or product films from screenshots or photos, data animation) to `hyperframes-workflow`, which chooses the runtime, renders a finished MP4 where code runs and designs its sound; React/TypeScript compositions go to `remotion-video-production`.
- Route Hipson-style packets through `hipson-adapter` unless the user chooses full Hipson separately.
- Route unresolved product, offer, audience, channel, claim, asset-matrix, or creative-test strategy through `ecommerce-campaign-strategy-director`.
- Route screenplay, treatment, scene, dialogue, pitch, coverage, or narrative-rewrite work through `screenplay-story-architect` before storyboard production.
- Route end-to-end reel, short-form ad, product-video, UGC-video, explainer, cutdown, or mixed video-production work through `creative-video-producer`.
- Route detailed caption timing, styling, safe zones, render handoffs, or caption repair through `caption-studio`.
- Route footage-first or timeline-first OpenCut planning through `opencut-video-studio` when OpenCut is available or the user wants an OpenCut Edit Pack.
- Route text-only music, music-video, visible-singing, lip-sync triage, or named music-provider planning packets through `audio-production-director` without implying provider execution.

## Guardrails

- Use role IDs and surface-appropriate display names from onboarding.
- Do not skip upstream gates.
- Generated static raster graphics should use the native image tool actually exposed by the host by default when available.
- Static raster graphics with visible text must use the native image tool actually exposed by the host in one pass with text included.
- Resolve generator prompt fields and negative handling before producing generator-specific prompts. Do not attach a universal negative-prompt block.
- Treat separately generated images and shots as independent units. Claim strict continuity only when each request has a concrete continuity carrier.
- For image, edit, or video prompting, use a revisioned Creative Prompt Contract when the work has strict locks, multiple requests, target adaptation, or execution readiness needs. Keep the prompt revision, reference roles, attachment plan, continuity carrier, QA observables, and adapter status together.
- Treat one primary action and one primary camera move as defaults for a short video unit. Any exception needs a concrete rationale and evidence that QA can inspect.
- Keep model fields, reference limits, edit modes, audio behavior, and target-specific syntax pending until an official source check confirms the active surface.
- Use rewrite-forward only from an accepted actual output, never from a planned end frame or repeated prose.
- Do not substitute Python-generated artwork, SVG, HTML/canvas, Sharp/composited PNG, or other coded artwork unless the user explicitly asks for coded, vector, template, or editable source output. The exact-copy route of the [text policy](references/text-image-generation-policy.md), named to the user, is not a substitute: it sets exact text on a generated, supplied or flat background.
- Delivery follows QA when generated assets exist.
- Upload, publish, or external delivery requires an explicit current user request.
- Workflow self-improvement creates proposals, not automatic mutations; when implementation is requested, use the self-improvement sufficiency gate to choose `stop_sufficient`, `patch_one_gap`, or `ask_user`.
- Loop Protocol work must record an iteration budget, acceptance matrix, evidence, root cause, minimal repair or loopback target, regression check, and one stop decision: `stop_sufficient`, `patch_one_gap`, `ask_user`, or `blocked`.
- Do not continue a loop only because the result could be better in theory.
- Do not add a hook, CTA, list, heading, emoji, hashtag, question, artificial
  roughness, or generic marketing structure without a confirmed channel, goal,
  audience, legal, timing, or accessibility reason.
- Do not fabricate author experience, testimonials, sources, quotes, metrics,
  results, promises, or user history to make text feel more authentic.
- Never store raw chain-of-thought, raw reasoning traces, raw debate transcripts, provider secrets, signed URLs or `.env` files. Store only task-needed private project context in the authorized user-scoped project or private handoff; shared plugin files and public exports must remain free of private project data.
- A runtime route or model recommendation is not permission to call an API, use an external provider, upload files, run destructive commands, or install routing infrastructure.
- Do not add private project context, secrets, local machine paths, or provider-specific execution dependencies.
- In ChatGPT, do not claim doctor checks, hash checks, repository validation, local file writes, or persistent agent creation unless those capabilities actually ran on an available surface.

## Handoff

Review gate: `workflow_route`.

Hand off with:

- `workflow_blueprint`
- `active_roles`
- `completed_or_existing_artifacts`
- `last_completed_gate`
- `required_handoffs`
- `review_gates`
- `request_diagnostic`
- `reasoning_route`
- `runtime_route`
- `loop_state`
- `loop_evidence_refs`
- `pending_decisions`
- `blocked_items`
- `files_touched`
- `risks`
- `next_role`
- `next_action`
- `recovery_prompt`

## QA Checklist

- A clear request starts the work; one question is asked only when a material choice is open, without ritual approval.
- Selected roles match the task and available inputs.
- Required gates and handoffs are named.
- Reasoning routes are compact, bounded, and do not store raw reasoning traces.
- Runtime routes keep provider/API/upload permissions false unless the current user explicitly asks for the protected action.
- Loop state has checklist-before-execution, evidence-backed evaluation, root cause, minimal repair or loopback target, regression check, and stop decision.
- Ready-to-use text has a Copy Pack status, author context, fact-and-lock
  review, Human Voice review, and bounded Copy Delivery Loop evidence.
- Missing artifacts trigger loopback instead of guesswork.
- The selected route is the smallest sufficient route; a full pipeline is used only when explicitly requested or justified by multi-stage dependencies.
- External delivery or execution is not implied without user instruction.
- Public-neutral boundaries remain intact.

## Studio operating assets

Use [project recovery](references/project-recovery.md) for memory and cross-host transfer. [Artifact schemas](assets/artifact-schemas.json) preserve the kit’s required contract sections; [artifact templates](templates/artifact-templates.md) give their field skeletons. Where a template and an owner's own contract differ, the owner's contract wins: a motion video uses the [motion contract](../hyperframes-workflow/references/motion-contract-json.md), and the Task Confirmation block records intent taken from the request rather than a question to ask. [Studio integration authority](references/studio-integration-policy.md) defines primary owners, staged use and the active exceptions. Intent is captured from a clear request; it is not a mandatory confirmation question. Keep full schemas backstage when a compact answer suffices.

Recovery assets: [checkpoint state](assets/project-state.md) and [paste-ready recovery prompt](assets/recovery-prompt.md). The [upstream onboarding schema](assets/onboarding.schema.json) belongs only to a separately requested project-local installation; ordinary Studio use follows [Studio Workstyle Profile](../studio-workstyle-profile/SKILL.md) with optional, incremental preferences.

## Provider setup state

Use [provider setup](../tool-routing-cost/references/provider-setup.md) for optional post-install choices and host-aware connection planning. Keep directory presence, installed/selected state, authentication, billing, schema and task permission independent. The user's account and tool preferences remain private; shared package defaults contain no personal provider state. An instruction-only Studio install is complete without a provider.
