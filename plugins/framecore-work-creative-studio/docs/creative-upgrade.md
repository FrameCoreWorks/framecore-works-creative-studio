# Creative improvement map, dev.31

The update strengthens existing skills. It adds six applied references to twelve owners, while retaining 37 canonical skill roots, including one compatibility alias. It does not attach a provider or install another set of agents.

| Capability | Resource | Connected owners |
|---|---|---|
| Specific events and creative decisions | [Decision library](../skills/commercial-video-campaign-director/references/creative-decision-library.md) | Commercial Video, Commercial Visual, Static Graphic Design Creator, Creative Video Producer |
| Physical and temporal shot logic | [Shot adjacency](../skills/storyboard-sequence-architect/references/shot-adjacency-workbook.md) | Storyboard Sequence, Cinematography, Video Prompt, Creative Video Producer, Audio Production |
| Preferences with explicit evidence and scope | [Taste learning](../skills/studio-workstyle-profile/references/taste-learning.md) | Studio Workstyle Profile |
| Primary-source evidence and its limits | [Twelve source cards](../skills/research-evidence/references/creative-upgrade-sources.md) | Research Evidence |
| Short routes and a bounded project pilot | [Compact workflow](../skills/workflow-orchestrator/references/compact-routing-and-pilot.md) | Workflow Orchestrator |
| Concrete provider-neutral execution handoff | [Execution contract](../skills/tool-routing-cost/references/execution-adapter-contract.md) | Tool Routing Cost, Creative Video Producer |

## Reusable assets

- [Decision card](../skills/commercial-video-campaign-director/assets/creative-decision-card.json): proposal, evidence, exact user decision and stated reason.
- [Synthetic 25-second sequence](../skills/storyboard-sequence-architect/assets/shot-plan.example.json): edit intervals, entry/exit states, bridges and unresolved strict reference bindings. This illustrates continuity data, not a recommended creative direction.
- [Synthetic scoped taste records](../skills/studio-workstyle-profile/assets/taste-profile.example.json) and [empty profile template](../skills/studio-workstyle-profile/assets/profile.template.json): user/client/project separation, tentative versus explicit evidence, correction and retirement.
- [Project pilot](../skills/workflow-orchestrator/assets/project-pilot.template.json): real selections, correction effort and observed defects; no fabricated success metrics.
- [Execution plan](../skills/tool-routing-cost/assets/execution-plan.template.json): actual input binding, tool/schema verification, scoped authorization, budget, retry state and output inspection.
- [Extended cross-host handoff](../skills/workflow-orchestrator/assets/cross-host-handoff.template.md): selected mechanism, continuity, relevant preferences, execution limits and current evidence.

## Optional declared-data checks

From the plugin root:

```bash
node scripts/review-creative-plan.mjs sequence skills/storyboard-sequence-architect/assets/shot-plan.example.json
node scripts/review-creative-plan.mjs taste skills/studio-workstyle-profile/assets/taste-profile.example.json
```

The first sample is structurally valid but blocked for execution because its references are not bound. That is intentional. A valid plan never establishes actual image quality, authorization, availability or exact identity. The taste checker verifies record structure; it does not infer a person's preferences or perform a persistent write.

## Source discovery repair

The dev.30 host catalog exposed 35 source skills alongside their canonical Studio counterparts. Overlay updates cannot remove old paths. In dev.31 their old source `SKILL.md` paths contain inert Markdown pointers without skill metadata. Original entrypoint bytes are retained under `SKILL.source.md` and in the [complete pinned source archive](../integrations/workflow-kit/workflow-kit-55c8bf1-source.tar.gz). The [manifest](../integrations/workflow-kit/source-manifest.json) records hashes and paths.

Extract the original archive into a separate workspace before using upstream development or installation tools. Do not treat the expanded reference mirror as an installable upstream checkout. Canonical checks scan all skill entrypoints recursively; a refreshed host catalog must be checked separately before claiming host-level removal of the duplicates.

## Evidence and next practical step

[Verification results](creative-upgrade-verification.json) distinguish 43 Node tests, 23 Python tests and two fresh text-use exercises from 167 planned model-evaluation fixtures. No real media or paid provider was used. Real-project validation remains available only when explicitly requested. It is not a prerequisite for plugin development. If the user declines pilots, continue the authorized improvements and report actual structural checks without claiming media-quality evidence.
