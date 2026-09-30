# Workflow Blueprints

For brand strategy, a logo system, Logo Guide or Identity Guide, use the [brand identity profile](../../workflow-orchestrator/references/brand-identity-workflow.md). Reuse this kit's existing roles/gates: brief and research as needed, then `static-direction` with Marketing for foundations and Static Graphic Design Creator for integrated logo/visual craft, inspected `qa-iteration` where applicable, and `delivery-documentation` for the requested guide/package. Keep stage artifacts and selection status in one Project State; a logo-only request skips the unrequested stages.

Use these blueprints as starting routes. The workflow-orchestrator may shorten or expand them, but it must preserve required gates, handoffs, and missing-artifact loopbacks.

## Shared Research Preflight

Every new substantive creative route includes `research-evidence` before direction, factual claims, model recommendations, promptability decisions, or diagnosis. It produces an Evidence Note or an explicit No-Browse Receipt. Honor an explicit user no-browse boundary and mark mutable claims unverified. Reuse prior evidence only while the question and source basis remain unchanged within the active project. Include the `evidence_fit` gate on each substantive route; mechanical maintenance and project-state recovery without changing advice may record a specific exemption.

## Minimal Planning Route

Use for small planning requests, first-install smoke tests, and tasks where the user needs a clean brief or delivery note without the full creative pipeline.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `brief-architect`
4. `delivery-documentation` when a final summary or package note is needed

Required gates:

- `intent_lock`
- `workflow_route`
- `brief_completeness`
- `delivery_fit` when delivery documentation is produced

Boundary: stop at planning unless the user asks for references, direction, prompt packs, execution, QA, or delivery packaging.

## Static Campaign Or E-Commerce Graphic

Use for posters, banners, product graphics, paid/social creative, marketplace images, and static campaign assets.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `research-evidence`
4. `brief-architect`
5. `reference-curator`
6. `static-direction`
7. `tool-routing-cost` only when execution is explicitly requested
8. `asset-manifest` when outputs exist and an inventory is requested or needed for delivery
9. `qa-iteration` for actually accessible outputs
10. `delivery-documentation` for the requested handoff

For static-only work, `static-direction` uses `static-graphic-design-creator` as the integrated owner of concept, layout, visible copy, text feasibility and prompt compilation. Keep these internal stages in that owner; do not add a second Copy Voice, Humanizer or Image Prompt intake. Reuse an existing brief and accepted references rather than repeating intake. In a mixed campaign, use `copy-voice` only for a separately requested Copy Pack and `image-prompting` for a separate non-static artifact. Carry approved context and exact-copy locks to those owners.

Required gates:

- `intent_lock`
- `workflow_route`
- `evidence_fit`
- `loop_control_fit`
- `brief_completeness`
- `reference_authority_fit`
- `direction_fit`
- `copy_fit` when copy is used, checked within the integrated static owner
- `promptability_fit`, checked within the integrated static owner
- `asset_manifest_fit` when outputs exist
- `post_execution_fit`
- `delivery_fit`

Special rule: static raster graphics with visible text must use the native image tool actually exposed by the host in one pass with final copy included.

## Video Campaign Or Storyboard

Use for video ads, motion concepts, shot lists, social video, storyboard sequences, and video prompt packs.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `research-evidence`
4. `brief-architect`
5. `reference-curator`
6. `motion-direction`
7. `storyboard-architect`
8. `copy-voice` when VO, supers, captions, or dialogue are needed
9. `video-prompting`
10. `tool-routing-cost` only when execution is explicitly requested
11. `asset-manifest` when outputs exist
12. `qa-iteration`
13. `delivery-documentation`

Required gates:

- `intent_lock`
- `workflow_route`
- `evidence_fit`
- `loop_control_fit`
- `brief_completeness`
- `reference_authority_fit`
- `direction_fit`
- `structure_fit`
- `copy_fit` when copy is used
- `promptability_fit`
- `asset_manifest_fit` when outputs exist
- `post_execution_fit`
- `delivery_fit`

Loopback: if the storyboard lacks timing, camera intent, or continuity, return to `storyboard-architect` before prompting.

## Artist-led Music Video

Use for a music-first visual concept, artist persona/performance direction, or a music video whose primary outcome is the song and artist rather than a commercial product campaign.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `research-evidence`
4. `brief-architect`
5. `reference-curator`
6. `music-video-direction`
7. `storyboard-architect` when a timed sequence or shot cards are requested
8. `audio-production` when music, sound, VO, lyrics, rights or audio review is in scope
9. `copy-voice` when non-lyrical copy, captions or presentation text matters
10. `video-prompting` when a video prompt is requested
11. `qa-iteration` when a concrete artifact or prompt is ready for review
12. `delivery-documentation` when a delivery packet is requested

Required gates:

- `intent_lock`
- `workflow_route`
- `evidence_fit`
- `brief_completeness`
- `reference_authority_fit`
- `direction_fit`
- `structure_fit` when a sequence is produced
- `promptability_fit` when a video prompt is produced
- `post_execution_fit` when media or a concrete artifact is reviewed
- `delivery_fit` when delivery documentation is produced

Boundary: the music-video owner develops song/persona image logic; screenplay authorship, timed shot cards, audio planning, prompt compilation, execution and media review remain with their mapped owners.

## Standalone Audio Planning Or Review

Use for an audio task packet, music/sound/VO/lyrics planning, track-rights research, or review of supplied audio when no larger visual route owns the task.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `research-evidence`
4. `brief-architect` when scope or delivery context needs structure
5. `reference-curator` when supplied audio, source material or reference authority matters
6. `audio-production`
7. `qa-iteration` when an actual audio asset or completed packet is explicitly reviewed
8. `delivery-documentation` when a portable packet or delivery note is requested

Required gates:

- `intent_lock`
- `workflow_route`
- `evidence_fit`
- `brief_completeness` when a brief is produced
- `reference_authority_fit` when references are used
- `post_execution_fit` when a concrete artifact or supplied media is reviewed
- `delivery_fit` when delivery documentation is produced

Boundary: Audio Production Director creates text-based planning/review artifacts and can inspect media only through actually available, task-authorized tools. The route does not imply audio generation or provider execution.

## Storyboard Board Artifact

Use when the user needs a board/panel artifact for planning or review, not only a text storyboard.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `brief-architect`
4. `reference-curator`
5. `motion-direction` or `music-video-direction`
6. `storyboard-architect`
7. `storyboard-board-architect`
8. `image-prompting` when the board will be generated as an image
9. `qa-iteration`
10. `delivery-documentation`

Required gates:

- `intent_lock`
- `workflow_route`
- `loop_control_fit`
- `brief_completeness`
- `reference_authority_fit`
- `direction_fit`
- `structure_fit`
- `storyboard_board_fit`
- `promptability_fit` when image prompting is used
- `post_execution_fit`
- `delivery_fit`

Special rule: if the board is a static raster graphic with visible labels, lock final text before image prompting.

## HyperFrames Coded Video

Use when the output is a coded video composition, animation, caption system, website-to-video concept, or render-ready HyperFrames plan.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `brief-architect`
4. `reference-curator`
5. `motion-direction`
6. `storyboard-architect`
7. `copy-voice` when captions, titles, VO, or overlays matter
8. `hyperframes-producer`
9. `asset-manifest` when rendered or source assets exist
10. `qa-iteration`
11. `delivery-documentation`

Required gates:

- `intent_lock`
- `workflow_route`
- `loop_control_fit`
- `brief_completeness`
- `reference_authority_fit`
- `direction_fit`
- `structure_fit`
- `copy_fit` when copy is used
- `execution_manifest_fit`
- `asset_manifest_fit` when outputs exist
- `post_execution_fit`
- `delivery_fit`

Boundary: HyperFrames is a coded-video workflow path, not a paid media-provider integration.

## Remotion Coded Video

Use when the output is a deterministic React/TypeScript video composition, reusable template, data-driven variant system, captioned programmatic video, or locally rendered Remotion artifact.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `brief-architect`
4. `reference-curator`
5. `motion-direction`
6. `storyboard-architect`
7. `copy-voice` when captions, titles, VO, or overlays matter
8. `execution-manifest` supported by `remotion-video-production`
9. `asset-manifest` when source or rendered assets exist
10. `qa-iteration`
11. `delivery-documentation`

Required gates:

- `intent_lock`
- `workflow_route`
- `loop_control_fit`
- `brief_completeness`
- `reference_authority_fit`
- `direction_fit`
- `structure_fit`
- `copy_fit` when copy is used
- `execution_manifest_fit`
- `asset_manifest_fit` when outputs exist
- `post_execution_fit`
- `delivery_fit`

Boundary: the skill may plan or implement local Remotion work when the active environment supports it. It does not activate hosted rendering, uploads, external providers, or dependency installation by itself.

## Prompt Pack Without Execution

Use when the user wants prompts, structured instructions, or a ready-to-run pack, but does not ask Codex to execute external tools.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `brief-architect`
4. `reference-curator` when visual, factual, or continuity references matter
5. direction role as needed
6. `copy-voice` when text quality matters
7. `image-prompting` or `video-prompting`
8. `qa-iteration`
9. `delivery-documentation`

Required gates:

- `intent_lock`
- `workflow_route`
- `loop_control_fit` when a draft/output is reviewed
- `brief_completeness`
- `reference_authority_fit` when references are used
- `direction_fit` when direction is used
- `copy_fit` when copy is used
- `promptability_fit`
- `post_execution_fit`
- `delivery_fit`

Boundary: stop before `tool-routing-cost` unless the current user request explicitly asks for execution planning.

## Document Or Text Workflow

Use for structured notes, written documents, delivery text, research-backed text, summaries, and workspace documentation tasks.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `brief-architect`
4. `research-evidence` when factual support is needed
5. `copy-voice` when wording, tone, or readability matters
6. `qa-iteration` when there is a concrete draft or output to review
7. `delivery-documentation`

Required gates:

- `intent_lock`
- `workflow_route`
- `loop_control_fit` when a draft/output is reviewed
- `brief_completeness`
- `evidence_fit` when research is used
- `copy_fit` when copy is produced or polished
- `post_execution_fit` when a draft/output is reviewed
- `delivery_fit`

Boundary: this path produces local text artifacts by default. Upload, publishing, or external delivery requires an explicit user request.

## QA And Delivery Only

Use when assets or artifacts already exist and the user asks for review, polish, packaging, or delivery notes.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `asset-manifest` when files or versions need traceability
4. `qa-iteration`
5. source role loopback when fixes are needed
6. `delivery-documentation`

Required gates:

- `intent_lock`
- `workflow_route`
- `loop_control_fit`
- `asset_manifest_fit` when assets exist
- `post_execution_fit`
- `delivery_fit`

Loopback: if QA identifies a source-instruction issue, return to the role that owns the failed artifact instead of patching delivery notes around the problem.

## Workflow Self-Improvement Review

Use only when the user explicitly asks for retrospection or when the local opt-in report-only review recipe is enabled.

Route:

1. `intent-confirmation`
2. `workflow-orchestrator`
3. `workflow-self-improvement`
4. optional `qa-iteration` only when routed by the orchestrator
5. user approval before any workflow mutation

Required gates:

- `intent_lock`
- `workflow_route`
- proposal review by the user before adoption

Boundary: this blueprint produces retrospective logs and change proposals only. It does not mutate workflow files, upload files, run providers, or create hidden daemons.
