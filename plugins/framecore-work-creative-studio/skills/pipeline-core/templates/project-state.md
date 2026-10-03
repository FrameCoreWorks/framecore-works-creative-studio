# Project State

Keep one Project State. This portable view and the [durable checkpoint](../assets/project-state.md) use the same interaction fields. Preserve known values and user edits; a handoff does not create a second state store.

- checkpoint_id:
- checkpoint_status:
- updated_utc:

- interaction_mode: learning | creation | undecided
- pace: quick | deep | user_defined
- entry_context: optional; stage (intent_choice | pace_choice | area_choice | brief | working), last menu actually shown (history only), selected work area, next unresolved choice and pending_choice_groups (purpose and displayed token-to-option mapping for each unresolved group). Remove answered/skipped/replaced groups; brief/working retains no entry tokens unless a new choice was offered. Use [startup and creative menus](../../workflow-orchestrator/references/startup-and-creative-menus.md); bind tokens only to pending groups, with distinct number/letter namespaces in one response.
- learning_context: optional; goal, selected domains, level evidence, optional onboarding context (known/unknown answers, questions asked, one pending question with its displayed token mapping and next action; never a question batch), plan revision, current module/lesson, completed/skipped lessons, strengths, practice needs, constraints, next action, persistence evidence and research_status (not_attempted | incomplete | completed; scope and limitation_disclosed); optional diagnostic_attempt, competency_evidence, assistance_used, review_queue, one pending_practice, feedback_diagnosis and learning_project retain their evidence origins. Missing older fields stay Unknown. Use the [progress card](../../workflow-orchestrator/assets/learning-progress.template.md) for a portable view of this same state.
- campaign_context: optional; audit/strategy/claim revisions, objective and priority offer, selected direction, asset IDs/dependencies, measurement plan, one pending question, blockers and next action; retain evidence origins and actual file access, with missing older fields Unknown. Use the [campaign strategy pack](../../ecommerce-campaign-strategy-director/templates/ecommerce-campaign-strategy-pack.md) as a view of this same state.

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
