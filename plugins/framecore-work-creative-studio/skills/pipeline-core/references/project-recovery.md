# Project recovery and cross-host work

Use for a long, interrupted or transferred project. Keep one shared Project State; a handoff and Memory Cache summarize that state rather than creating a second workflow. A resumed session checks actual assets and permissions before continuing from the last accepted artifact.

## Capability and persistence

Inspect the active host’s actual file and storage tools. With no persistent project storage, return the [portable handoff](../../workflow-orchestrator/assets/cross-host-handoff.template.md) or the [Project State template](../templates/project-state.md) when requested. Do not promise that another host receives attachments or settings automatically. Attempt an exact supplied conversation URL with the available web/open tool; mark full, partial or unavailable retrieval and missing media separately.

For a user-requested local recovery store, keep user input in Context/ and compact generated recovery state in Memory Cache/. Reuse existing files, retain the selected checkpoint and preserve user edits. Store goal, artifact/shot IDs, exact selected copy, source revisions, source-map pointers, decisions, open questions, tested evidence, loop stop state and next action. Exclude secrets, full transcripts, hidden reasoning, raw provider responses, signed URLs and bulk media.

## Included utilities

The complete original source is in the [pinned archive](../../../integrations/workflow-kit/workflow-kit-55c8bf1-source.tar.gz). When local persistence is requested and a shell is available, extract this archive into a separate, explicitly chosen scratch/source directory first. The expanded reference mirror contains non-discoverable source names and must not be used as an upstream installation. Then use the extracted source root and an explicit user-project target:

```bash
node <extracted-source-root>/tools/init-memory-cache.mjs --target <user-project>
node <extracted-source-root>/tools/validate-memory-cache.mjs --target <user-project>
```

Do not use --force for an existing recovery store without specific overwrite authorization. The upstream recovery prompt assumes a project-local .agents installation; replace that prompt with the [Studio recovery prompt](../assets/recovery-prompt.md), filling actual installed skill paths or host-resolved names before final validation, and record that local adaptation. For a newly created empty cache, also adapt its initial project-state.md from the [Studio checkpoint template](../assets/project-state.md), using gate IDs such as intent_lock rather than role IDs. Preserve an existing populated state and user edits. The optional upstream installer is a separate user-requested task.

Local semantic index/query utilities use token overlap; they are not model embeddings or cross-host sync. Their default allowlist targets project-local .agents/.codex and Memory Cache, so a plugin-only installation may index just its recovery files. Report that scope honestly. Context and media stay excluded. The source embed mode is only an activation-gated local plan in this release; it does not provide a hosted embedding integration. Verify a future version before describing it differently.

## QA and delivery

When a learning path is active or paused, retain its `learning_context` inside the same Project State and include a concise [Karta postępu](../../workflow-orchestrator/assets/learning-progress.template.md) in a portable handoff. Reuse known onboarding answers and resume the recorded module after checking actual asset access. Keep self-reported completion distinct from reviewed attempts, and preserve the production checkpoint through mode switches. A card cannot activate a provider or restore missing attachments; without verified storage it is user-carried context, not promised memory.

Verify checkpoint ID, last completed gate, actual asset access, pending strict carriers, exact source revisions and next action. A retrieved conversation may contain inaccessible attachments. A successful write is persistence evidence only for that destination. Prefer one short handoff with exact decisions and explicit missing inputs. Follow [integration authority](studio-integration-policy.md) for valid scoped authorization and the user’s Quick/Deep preference.
