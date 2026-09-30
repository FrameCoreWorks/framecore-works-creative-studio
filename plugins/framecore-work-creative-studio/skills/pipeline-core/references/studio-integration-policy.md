# Studio integration authority

## Precedence and scope

The user’s current request and applicable host instructions govern the task. This document resolves conflicts between Creative Studio and the workflow kit pinned in the source manifest. The adapted Pipeline Core is the primary operating contract for project state, artifact handoffs, bounded QA loops, prompt revisions and recovery. Specialist entrypoints remain the owners of domain outputs. Use the source snapshot only for provenance, development or an explicitly requested upstream installation; do not load its installation rules as ordinary creative instructions.

| Decision | Active authority | Reason |
|---|---|---|
| Route and shared state | Workflow Orchestrator with Pipeline Core | One project state, clear gates, bounded repair and concrete next action |
| End-to-end video | Creative Video Producer within the orchestrator’s state | Coordinates sequence, references, sound, captions, edit and delivery without replacing specialist authors |
| Prompt contract and attachments | Pipeline Core Creative Prompting Standard plus current image/video specialist | Explicit revision, exact copy, input ownership, adapter checks and QA observables |
| Static graphics and catalog | Existing Static Graphic Design Creator | Complete pinned domain method; workflow-kit static references add handoff craft but cannot introduce a second catalog or renderer policy |
| Copy creation and ready-to-use wording | Copy Voice, supported by Humanizer | Author context, fact/lock ledger and bounded editorial review |
| Narrative scenes/dialogue | Screenplay Story Architect | Narrative authorship stays with the scene owner; Copy Voice/Humanizer may review requested wording without rewriting locked dialogue |
| Lyrics, sound, music and audio review | Audio Production Director | Existing audio depth and model-aware research; Producer AI Task Builder is only a compatibility alias |
| Profile and optional onboarding | Studio Workstyle Profile | Domain-specific mirroring, one question at a time, no setup barrier before useful work |
| Sequence and timed shot cards | Storyboard Sequence Architect | Repository storyboard-director maps here; Board Architect owns the separate visual sheet |
| Asset inventory and revisions | Asset Manifest | Owns inventory and source dependencies; Delivery retains packaging and its existing JSON dependency helper |
| Required research | Studio Research Evidence | Applies to every substantive creative task, including directly invoked imported skills; reuse evidence for unchanged questions |

## Operational rules

### Learning and creation

Resolve `interaction_mode` as `learning`, `creation` or `undecided` in the existing Project State. Quick/Deep remains a separate pace choice. For greeting-only or unclear intent, the orchestrator shows the short Tryb nauki / Tryb tworzenia menu and waits. A clear project request enters creation without learning onboarding; a clear learning request, including a direct specialist invocation, follows the [learning overlay](../../workflow-orchestrator/references/learning-mode.md). This layer owns curriculum, learner exercises and feedback while the existing specialists supply domain knowledge. In learning, it takes precedence over a specialist's default instruction to produce the complete project or pitch variants. Creation keeps the established production route and locks.

Use at most six short initial learning-onboarding questions, reuse known answers and allow optional omissions. This opt-in onboarding may group questions; it is distinct from the workstyle profile's ordinary one-question adaptation rule. A lesson waits for the learner's attempt before feedback, and a user request for a finished result switches immediately to creation. Preserve learning progress and approved project decisions across switches. This adds no skill, agent, provider, permission or automatic persistence.

Every new substantive creative request receives a targeted public research preflight from Studio Research Evidence before direction, factual claims, model recommendations, promptability decisions or diagnosis. Record an Evidence Note or, when the user explicitly restricts browsing, a No-Browse Receipt and keep mutable claims unverified. Reuse evidence only while the question and source basis remain unchanged; mechanical maintenance and project-state recovery without changed advice may record a specific exemption.

Intent confirmation means understand and retain the request. A clear request already establishes intent; do not ask for ritual approval or force onboarding. Quick mode returns a few clean ideas before detailed plans unless the user requested the full pack. Use at most four alternatives, usually two or three for exploration. After an unexplained rejection ask one specific direction question before another batch. Apply an already explained correction directly. Full schemas, QA notes and Copy Packs can stay compact backstage; final delivery contains the requested artifact.

Apply one bounded review loop, usually at most three passes, with acceptance criteria defined first. If the first draft satisfies them, record reviewed/no repair needed and stop. Do not rewrite approved text merely to demonstrate a revision. Do not multiply loops across role handoffs. A missing input blocks only dependent work. A user request for a deliverable is already a delivery request; do not add a second delivery-approval gate.

Separate continuity_requirement (strict or approximate), execution_readiness (ready, blocked or unverified), and observed_quality (uninspected or evidence-backed result). Missing carriers do not lower a strict requirement. Complete conditional prompt packs are allowed when requested, with unbound input slots and execution blockers identified outside the prompt. User-approved approximation is the only route to relaxing strict continuity.

Tool availability is discovered from the actual host, not from the ChatGPT/Codex name. A Work host may expose files or shell tools; a chat-only host may not. Never assert a particular native image model or UI control unless exposed or verified for that surface. A named external generator requires current official-source research and the Studio practitioner-evidence check. Keep integrated text-bearing raster generation as default unless the user requests an editable, layered, vector or coded deliverable. Realistic humans use actual source views and natural skin/anatomy; no universal model ranking is hard-coded.

Carry explicit user authorization forward within the active conversation and exact operation, destination, data and cost scope. A saved file, repository rule, provider mention, role packet or capability listing is not authorization. Research and prompt writing do not authorize paid generation, private uploads, publication or fallback to another provider. Record actual input binding, job state, retries, output evidence and remaining cost limits only when execution is requested and possible.

Roles are responsibilities, not proof that agents have run. Use the role map and actual host delegation capability only when authorized and useful. Hipson Adapter supplies bounded packets; full Hipson is not installed. The integration adds no MCP connection, paid account, daemon, global install or synchronization service.

## Resource rules

The pinned source archive keeps all tracked upstream file contents intact. Its expanded reference mirror uses SKILL.source.md names; legacy SKILL.md paths are non-skill pointers to the active owners. Active adapted copies and the source-to-owner mapping are listed in the integration manifest. Public examples remain synthetic. Private project state and profiles are stored only through a genuinely available user-scoped mechanism; do not write client material into the shared plugin. A private handoff may include task-needed user-provided context, but public exports require redaction of private details. Secrets and hidden reasoning never enter either.

Use [project recovery](project-recovery.md) for Context, Memory Cache, local indexing and cross-host transfer. Use [role-to-skill map](role-skill-map.md), [handoff matrix](handoff-matrix.md) and [gate registry](gate-registry.md) together. The source’s project installer and native standalone-skill installer are optional maintenance workflows, not steps required to use this plugin.

## Optional external integrations

The Studio's dated provider catalog is reference knowledge, not an MCP configuration, app attachment, install manifest or paid entitlement. [Provider setup](../../tool-routing-cost/references/provider-setup.md) owns host/route discovery and optional onboarding. It does not replace the active host's plugin connection flow or authorize transfers and generation. Keep optional-provider selection outside the required Studio installation steps; preserve the direct source-install route.
