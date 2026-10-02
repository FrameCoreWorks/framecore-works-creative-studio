# Progress card

- interaction_mode: learning | creation
- learning_status: onboarding | planned | in_progress | paused | completed
- onboarding_context: optional portable view of learning_context; known/unknown/skipped answers, questions asked (count toward the six-question limit), at most one pending question with its displayed token-to-option mapping and next action. Remove answered/skipped/replaced pending questions; never reconstruct a mapping from an old menu or repeat a skipped optional question.
- selected_path / domain_ids:
- independent_outcome:
- level_by_domain: self_reported | observed | unknown; brief evidence
- plan_revision and module_order:
- current_module / current_lesson:
- completed_lessons: lesson ID, learner attempt or self-report, review evidence
- skipped_lessons: skipped does not establish mastery
- strengths: observed or learner-reported, never inferred private traits
- practice_needs:
- diagnostic_attempt: competency, task, observed attempt or learner_reported/Unknown, criteria and plan adjustment; skipped is not assessed
- competency_evidence: competency/criterion, task/context, attempt/evidence reference, origin (observed | learner_reported), help_level, criteria met/unmet/Unknown, performance_state (Unknown | supported | independent_familiar | independent_transfer), next practice; unverified reports retain Unknown
- assistance_used: strongest solution-bearing help per assessed criterion (none | hint | guided | partial_example | worked_example); compare successful tasks without invented mastery scores
- review_queue: competency, reason, relevant future lesson/context and last observed attempt; no reminders or automatic completion
- pending_practice: at most one diagnostic/retrieval/revision/transfer task, criteria, support already supplied and next action; never show its solution before the attempt unless requested
- feedback_diagnosis: observed defect, cause_category (craft | instruction | reference | generator | tool | Unknown), observed/hypothesized basis, evidence gap and correction
- learning_project: optional goal, artifact/revision, related module, dependencies, protected decisions and next learner action; practice alternatives remain separate from production approvals
- next_action:
- constraints: time, budget, available tools, preferred learning form
- project_context: goal, selected concept, exact text locks, accepted asset revisions
- available_assets / missing_assets:
- evidence_to_recheck: dated tool facts or unavailable references
- persistence: conversation_only | user_copied_card | verified_private_save

This card summarizes available context. It is not execution authorization, proof of mastery, actual attachment transfer or automatic memory across hosts. Recheck actual asset access on resume. Keep secrets and unnecessary personal details out; never save the card in the shared plugin. Preserve the project checkpoint when switching modes, and continue without repeating known onboarding answers.

Keep lesson completion, output quality and independence separate. Retain old evidence on an unsuccessful attempt and record the new gap. Missing fields in an older card stay Unknown; continue without migration or repeated onboarding. A copied card retains evidence provenance and does not verify its own performance claims.
