# Project State

## Purpose

Durable recovery state for one operational chat or project folder.

Keep one Project State. This checkpoint and the [portable state template](../templates/project-state.md) use the same interaction fields; a handoff is a view of that state. Preserve known values and user edits when adapting an older checkpoint.

## Interaction and learning

- interaction_mode: learning | creation | undecided
- pace: quick | deep | user_defined
- entry_context: optional; stage (intent_choice | pace_choice | area_choice | brief | working), last menu actually shown (history only), selected work area, next unresolved choice and pending_choice_groups (purpose and displayed token-to-option mapping for each unresolved group). Remove answered/skipped/replaced groups; brief/working retains no entry tokens unless a new choice was offered. Optional interactive_offers: the kind of stage and the user's answer (accepted, declined or no answer) for an offered interactive version. Use [startup and creative menus](../../workflow-orchestrator/references/startup-and-creative-menus.md); bind tokens only to pending groups, with distinct number/letter namespaces in one response.
- companion_setup: optional; superpowers choice (not_offered | offered | accepted | deferred | declined), availability (unknown | absent | readable | unreadable), observed host/catalog and skill-read evidence, actual persistence scope. Availability is rechecked in a new host; retain an explicit decline/defer without claiming account-wide memory. Missing old fields stay unknown.
- superpowers_support: optional; decision, studio_owner, trigger, selected_skills, support_status (not_applicable | unavailable | loaded | applied), artifact_revision, acceptance_criteria, evidence, next_owner. A read proves loaded, not applied; refresh affected evidence after revision changes. This is part of the same Project State, never a second QA loop.
- learning_context: optional; goal, selected domains, level evidence, optional onboarding context (known/unknown answers, questions asked, one pending question with its displayed token mapping and next action; never a question batch), plan revision, current module/lesson, completed/skipped lessons, strengths, practice needs, constraints, next action, persistence evidence and research_status (not_attempted | incomplete | completed; scope and limitation_disclosed); optional diagnostic_attempt, competency_evidence, assistance_used, review_queue, one pending_practice, feedback_diagnosis and learning_project retain their evidence origins. Missing older fields stay Unknown. Use the [progress card](../../workflow-orchestrator/assets/learning-progress.template.md) for a portable view of this same state.
- campaign_context: optional; audit/strategy/claim revisions, objective and priority offer, selected direction, asset IDs/dependencies, measurement plan, one pending question, blockers and next action; retain evidence origins and actual file access, with missing older fields Unknown. Use the [campaign strategy pack](../../ecommerce-campaign-strategy-director/templates/ecommerce-campaign-strategy-pack.md) as a view of this same state.
- framecut_context: optional; project path/editorial revision, working agreement, stage (intake | storyboard | awaiting_feedback | revising | approved | rendering | delivered), board revision, covered sequences/deliverables, ordered scene-to-panel map and sheet paths, pending feedback, actual user approval message tied to that board revision, optional sample request/status, native board receipt/hash and authored beat coverage, active job ID/request/project hash and last observed status, blockers and next action. Mirror this context in the project brief when using the runtime; keep one source of decisions. Changed creative content reopens board review; a session/view change or technical repair faithful to the accepted design does not. Missing older acceptance stays Unknown. See [FrameCut](../../opencut-video-studio/SKILL.md).
- creative_direction: optional; the chosen direction in one sentence, its lens and mechanism sentence, the defaults set aside, the assets it covers and its revision; later owners execute it instead of proposing new directions

## Checkpoint

- checkpoint_id: initial-setup
- checkpoint_status: active
- updated_utc: replace-me
- last_completed_gate: none
- current_gate: intent_lock
- next_action: define the next safe action

## Blocked Items

- none

## Files Touched

- none

## Decisions

- Memory Cache stores durable recovery state.
- Context stores user-supplied input and reference material.
- Do not repopulate Context from Memory Cache unless the current user explicitly asks for it.

## Loop State

- loop_id: none
- iteration: 0
- max_iterations: 0
- phase: stop
- stop_decision: stop_sufficient
- loop_evidence_refs: none

## Risks

- none recorded

## Safe Resume Point

Read applicable project instructions when available and the host-resolved Studio Studio Core; inspect actual assets before continuing from `checkpoint_id`.

## Recovery Prompt

Use `recovery-prompt.md` as the paste-ready recovery instruction.

Saved state is not permission to push, upload, run providers, run APIs, run global install, or perform destructive actions.
