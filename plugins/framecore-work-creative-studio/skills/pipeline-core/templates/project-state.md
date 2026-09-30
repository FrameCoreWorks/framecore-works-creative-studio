# Project State

- interaction_mode: learning | creation | undecided
- pace: quick | deep | user_defined
- entry_context: optional; stage (intent_choice | pace_choice | area_choice | brief | working), last menu actually shown (history only), selected work area, next unresolved choice and pending_choice_groups (purpose and displayed token-to-option mapping for each unresolved group). Remove answered/skipped/replaced groups; brief/working retains no entry tokens unless a new choice was offered. Use [startup and creative menus](../../workflow-orchestrator/references/startup-and-creative-menus.md); bind tokens only to pending groups, with distinct number/letter namespaces in one response.
- learning_context: optional; goal, selected domains, level evidence, optional onboarding context (known/unknown answers, questions asked, one pending question with its displayed token mapping and next action; never a question batch), plan revision, current module/lesson, completed/skipped lessons, strengths, practice needs, constraints, next action, persistence evidence and research_status (not_attempted | incomplete | completed; scope and limitation_disclosed). Use the [progress card](../../workflow-orchestrator/assets/learning-progress.template.md) for a portable view of this same state.

- workflow_blueprint:
- active_roles:
- completed_or_existing_artifacts:
- last_completed_gate:
- required_handoffs:
- review_gates:
- request_diagnostic:
- reasoning_route:
- runtime_route:
- loop_state:
- loop_evidence_refs:
- pending_decisions:
- blocked_items:
- files_touched:
- risks:
- next_role:
- next_action:
- recovery_prompt:
