# Project State

## Purpose

Durable recovery state for one operational chat or project folder.

Keep one Project State. This checkpoint and the [portable state template](../templates/project-state.md) use the same interaction fields; a handoff is a view of that state. Preserve known values and user edits when adapting an older checkpoint.

## Interaction and learning

- interaction_mode: learning | creation | undecided
- pace: quick | deep | user_defined
- entry_context: optional; stage (intent_choice | pace_choice | area_choice | brief | working), last menu actually shown (history only), selected work area, next unresolved choice and pending_choice_groups (purpose and displayed token-to-option mapping for each unresolved group). Remove answered/skipped/replaced groups; brief/working retains no entry tokens unless a new choice was offered. Use [startup and creative menus](../../workflow-orchestrator/references/startup-and-creative-menus.md); bind tokens only to pending groups, with distinct number/letter namespaces in one response.
- learning_context: optional; goal, selected domains, level evidence, optional onboarding context (known/unknown answers, questions asked, one pending question with its displayed token mapping and next action; never a question batch), plan revision, current module/lesson, completed/skipped lessons, strengths, practice needs, constraints, next action, persistence evidence and research_status (not_attempted | incomplete | completed; scope and limitation_disclosed). Use the [progress card](../../workflow-orchestrator/assets/learning-progress.template.md) for a portable view of this same state.

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

Read applicable project instructions when available and the host-resolved Studio Pipeline Core; inspect actual assets before continuing from `checkpoint_id`.

## Recovery Prompt

Use `recovery-prompt.md` as the paste-ready recovery instruction.

Saved state is not permission to push, upload, run providers, run APIs, run global install, or perform destructive actions.
