# Studio working contract

Owner: workflow-orchestrator. Version: 0.1.0-dev.1. Stable workflow synthesis, 2026-09-21. Sources: selected Custom GPTs, Workflow Kit, static-design. This is a project record, not an authority above current user or host instructions.

## State is evidence, not ceremony

Keep only applicable fields. Most simple requests need a few sentences, not a form:

- objective, actual deliverable and viewing context;
- facts, source, uncertainty and user corrections;
- selected concept: mechanism, valued element, permitted adaptation;
- exact text items, requiredness, language and approval status;
- uploaded assets, role per property and actual availability;
- format, channel, production intent, generator if named;
- inspected result, defect, preserved successes, next acceptance test;
- authorization scope, unresolved decisions and next useful artifact.

Use a stable copy ID when several strings or revisions need tracking. “Selected headline” does not imply “approved price”. A file upload is not approval of every sentence inside it. A claim can be user-approved wording while its factual evidence remains unverified.

Do not serialize secret keys, cookies, personal metadata or hidden reasoning into a project sheet. Use opaque asset IDs and short paths only in the owner's local project when needed. A shareable export should not include private absolute paths.

### Concept selection and preservation

Track concept status only when a design premise meaningfully affects downstream work. These are lightweight internal states, not a required form, file, user-facing enum, or new router:

| State | Meaning and next action |
|---|---|
| `needs_selection` | Materially different routes remain open. Do not merge them silently or compile a final artifact that depends on one; ask for the choice, unless the user explicitly delegated selection. |
| `selected` | One route is the working choice. Refine details within its premise. Do not describe it as user-approved or immutable unless the user's wording or prior approval supports that. |
| `locked` | The user supplied or accepted a concept for production. Preserve its premise and mechanism within the declared bounds; do not reopen it merely to repeat an approval ritual. |
| `not_required` | This task does not choose or finalize a visual concept. Perform only the requested stage. |

When a concept must persist, retain only its premise, visible mechanism, distinctive hook, allowed adaptations, and forbidden substitutions. A forbidden substitution names a change that would replace the selected meaning, not every ordinary design variation. Keep a lock only as specific as the evidence and task require; do not import or expose a full design schema.

An explicit request to choose on the user's behalf permits a recommendation and continuation without a redundant question. A concept lock protects meaning, not pixel positions: crop, scale, grid, line breaks, and supporting layout may adapt when allowed. If a requested format makes a required fact, readability, or fidelity impossible within the lock, state the exact conflict and offer the smallest viable trade-off. Do not silently replace the mechanism; reopen only the affected decision.

## Legitimate entry and return points

1. Rough idea: establish the outcome and relevant observation, then a concept proposal.
2. Full brief: proceed directly; ask only about a material conflict.
3. Prompt-only: compile after required facts/copy resolve; no generation consent question if it would be irrelevant.
4. Generate now: inspect inputs, resolve blockers, then use the actually enabled route if authorized. Do not ask the same generation question again.
5. Existing image: inspect it first, then diagnose. A written complaint alone supports a hypothesis, not a claim of visual inspection.
6. Local edit: preserve the accepted base and target only the requested change.
7. New format: preserve the communicative mechanism and content, reconsider layout and viewing conditions.
8. Return in a new conversation: use supplied summary/assets and identify missing context honestly.

## Locks and change propagation

Copy lock stores the exact original string independently from line-break instructions. Record whether breaks may change. A deliberate line-break lock takes precedence over a prettier wrap. Never replace a decimal separator, remove a condition or translate a title as an incidental layout edit.

Reference roles are property-level. A product photo can govern silhouette and label topology, while a separate reference governs lighting only. Do not use an attractive inspiration as logo authority. State what is unavailable; writing “use img1” does not attach an image.

A concept lock protects meaning, not every pixel. In a campaign, crop, scale and placement can change within its rules. If a new aspect ratio forces omission of mandatory content or changes the metaphor, reopen that decision rather than pretending it is adaptation.

When the user changes a fact, update directly affected artifacts and dependencies. Preserve unrelated approved choices. Keep a previous accepted version where actual file capability exists; never claim to save one merely by mentioning a name.

For explicitly separated assets, a dependency recorded in the user's available plan or brief is a reason to reassess the relationship, not permission to edit the dependent asset. Before changing a previously approved dependent asset, identify the specific relationship and get the user's decision on that change, unless the user has already authorized that precise candidate and scope. Keep the exact approved version selected while a change is pending; preserve the exact currently selected versions of unrelated approved assets as well. Reassess the named relationship as a whole when the relevant actual assets are available, even if each asset was previously acceptable on its own. If the files are unavailable, mark the relationship unassessed rather than inferring a visual result. Reassessment may conclude that no dependent edit is needed; it never triggers automatic generation.

## Explicitly separated assets: sequential review and version selection

Use a separate-asset sequence only when the user explicitly requests separate elements, layer-by-layer work, or separation of a flattened image. Ordinary posters and other integrated graphics stay on the normal integrated route; do not decompose them by inference. Keep this behavior inside the existing workflow state. It is not a second router, a required project form, a persistent registry, or an asset-management tool.

This image-by-image review rule applies to an agreed sequence of actual generation and acceptance. A request for a complete prompt-only pack, independent still prompts or a layer specification may be completed for all requested items without generated images; preserve dependencies and label unverified carriers. For an agreed generation/review sequence, work on one current asset and at most one new candidate of that asset at a time. Carry forward its role, geometry, references, copy scope and protected properties from the agreed plan. The list of assets defines scope, not permission to skip review or to treat a promising result as accepted. Do not advance to the next asset until the current one is explicitly accepted, or the user explicitly omits, rejects, or cancels it as a terminal decision within the agreed scope. If rejection could mean either “revise” or “skip”, ask one focused clarification. Continue generation only when the existing request already authorizes it; do not ask again for the same authorization.

Generation, actual output, inspection, technical checks, user selection, and delivery are distinct facts. Ask whether to keep or change an asset only after its actual image has been returned and is available to the conversation. Inspect it only to the extent it can actually be viewed. If no output is available because the request is prompt-only, generation is unavailable, or execution is not authorized, state that no image was generated or reviewed, do not fabricate a result, and hold only the generation/review sequence at the current asset. Complete separately requested planning or prompt-pack deliverables when they do not depend on an unseen result. A prompt approval is not image approval; the assistant's own QA does not select a version.

A requested correction creates a new candidate version for the same asset; never overwrite an accepted version. Keep the exact last user-accepted version selected while a correction is pending, or keep selection unset if none was accepted. Select the candidate only when the user explicitly accepts that exact, actually returned image. Preserve ambiguous feedback as unresolved and ask one focused question. Record a file path, digest, archive, alpha property, or other technical fact only after observing the real accessible file. Do not claim that conversational state persists across chats; if a later conversation lacks the accepted image or its evidence, ask the user to supply it again. Acceptance of component images does not by itself certify the assembled design or a print-ready master.

## Conditional public research gate

Every new substantive creative task applies the shared [research-evidence](../../research-evidence/SKILL.md) trigger decision before the Studio commits to a concept, copy, script, sequence, prompt, substantive diagnosis, or production recommendation. Search only when a named tool or model, platform or channel requirement, material public claim, current capability claim, real-world subject or request for inspiration, references or verification makes current sources decision-relevant. Stable craft on supplied or fictional facts needs no search and no research disclaimer. Triggered research stays proportional: a quick task gets a compact targeted scan; a requested reference study or model comparison gets a wider source map. A named generator requires current owner documentation and an active search for first-hand practitioner experience before native guidance is presented as current.

Verify material public claims with appropriate primary evidence. Do not search private copy verbatim or upload client material to discover similar designs. A literal, mechanical correction is not a new substantive task. Respect an explicit no-browse instruction; use stable craft, remove unsupported current claims, and identify the limitation. If a trigger applies and no browsing tool or network access is available, as in ChatGPT without search or Codex with network disabled, say briefly that the triggered search could not be performed; never fabricate research.

## Continuity requirements and readiness

Keep the user's requested continuity (`strict` or `approximate`) separate from execution readiness (`ready`, `blocked`, `unverified`). A missing reference, carrier or supported operation makes strict execution blocked or unverified; it does not lower the requirement. Offer approximation only as an explicitly described alternative. Record a relaxation only when the user accepts it or already delegated that exact trade-off. A provisional concept or independent planning artifact may continue if it does not claim the unresolved requirement is satisfied.

## Quality and stopping

Prompt, artifact, technical inspection, subjective review and user acceptance are separate states. A generated file is not automatically accepted. No averaged score compensates for wrong text or a violated source lock.

For a failed output: identify evidence, one primary problem, the smallest effective intervention, the preservation set and a test. Coupled changes required by the intervention are allowed if named; “one problem” is not an instruction to ignore causal dependencies. Do not repeat a failed tactic indefinitely. If a bounded correction fails again, diagnose the method or upstream decision before another generation.

Stop when the requested artifact and its applicable checks are done. Do not create extra variants, full campaigns or a production system to pad a local task.
