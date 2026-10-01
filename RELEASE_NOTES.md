# Creative Studio 1.3.1

Repairs the startup instructions after a reported reply containing only the mode choice. Workflow Orchestrator now includes the entire unchanged canonical welcome before other instructions and explicitly rejects a mode-only response. The source validator checks full protected-text integrity and exact excerpt equality. Direct tasks, resume, menus, onboarding and the shared QA budget retain their existing behavior.

Source and supplied-response checks are distinct from active-client observation. Active-client verification remains NOT_RUN unless recorded separately; this release does not claim deterministic control of host skill loading.
