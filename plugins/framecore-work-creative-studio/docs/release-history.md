# Historical development notes

## 1.18.0, 2026-10-06

- Add output formats to the motion contract: `formats` lists variants of the base size (for example 9:16 and 1:1) with optional per-format tokens and scene params; timeline, copy and holds stay shared. `resolveFormat(score, id)` in the scene engine returns the contract for one format.
- The scene engine scales sizes by the frame's short side, so 16:9, 9:16 and 1:1 share one type scale; 16:9 output is pixel-identical to 1.17.0. `item-stagger` gains `direction` (`auto`, `row`, `column`) and stacks vertically with a vertical connector in narrow frames; the end card centres wrapped text.
- Optional `tokens.safeArea {top, bottom}` pads content away from platform interface elements; the engine has no default values.
- The single-file preview gains a format menu and `?format=`; the Remotion starter registers `KineticType-<id>` per format with `render:9x16` and `render:1x1` scripts; the frame review checks every format by default (`--format` limits it) and respects the safe area.
- Fix review screenshots, which were drawn about 8% smaller than the frame in 1.17.0; review mode now renders at true size and matches Remotion stills pixel for pixel.
- `check-score.mjs` validates format IDs, sizes, safe areas and overrides of unknown scenes, and lists the formats in the storyboard.

## 1.17.0, 2026-10-06

- Add `assets/motion-review/review-frames.mjs`: a dependency-free tool that selects the contract's review frames, renders them through the single-file preview with a local Chrome or Chromium, and writes `review.json`, screenshots and a `review.html` contact sheet. Exit code 1 when errors are found.
- Add a review mode to the single-file preview (`?review=1`) that measures settled text in readable holds: outside the frame, clipped by a mask, WCAG 2.x contrast, margins, partial opacity, overlaps and small text in vertical formats. Normal preview output is pixel-identical to 1.16.0.
- Point the skill entry and method to the review before human inspection; it does not replace watching the sequence.
- Tests cover frame selection, preview embedding and HTML escaping; an opt-in browser test (`MOTION_REVIEW_BROWSER`) runs a real review.

## 1.16.0, 2026-10-06

- Add a dependency-free declarative scene engine with six kinds: `line-reveal`, `item-stagger`, `end-card`, `counter`, `quote` and `logo-reveal` (clip-only, never scaled). A scene declares `kind` and `params` in the motion contract; no scene code is needed when a kind fits.
- The single-file preview and the Remotion kinetic type starter now render through the same engine, so both show the same picture for a frame. The preview output is pixel-identical to 1.15.0; the shared engine also removes a 6-frame connector timing difference that the previous hand-written Remotion scene had.
- Add an all-kinds example contract with an original synthetic mark, scene-kind checks in `check-score.mjs` (unknown kind, missing params, copy and logo assets) and the kind in the storyboard table.
- Validation keeps the engine copies identical across the plugin, the Remotion starter and the preview.

## 1.15.0, 2026-10-06

- Add a motion prompt library brief index: 19 common brief types (logo reveal, kinetic statement, product feature, app workflow, social reel, event, quote, data, poll, explainer, lesson, editorial, transitions, music sync, 3D, generative background, end card and others) mapped to two to four original blueprints, a runtime hint, a starter and keep/avoid rules.
- Add `node library.mjs brief` (list, brief ID or free text) with Polish and English matching, including inflected forms.
- Replace the shared family-level objective of 60 original blueprints (brand, editorial, product, social, transitions, typography) with a record-specific objective, also in each prompt's purpose sentence, so search and selection can tell records apart.
- The canonical gate now requires record-specific objectives and an index that points only to existing FrameCore originals.

## 1.14.0, 2026-10-06

- Make `motion-score.json` the single motion contract: storyboard fields (goal, audience, message, concept, runtime state, confirmed/proposed/unknown decisions, acceptance criteria, asset ledger and per-scene focal point, entry, action, exit, transition, persistence and audio) sit beside the existing timeline, copy, tokens and motion values.
- Add approval rules: an approved contract needs evidence for its current revision; a new revision invalidates the old approval.
- Extend the shared `check-score.mjs` with `--storyboard` (require a complete storyboard) and `--markdown` (print the storyboard table for approval), and add `npm run storyboard` to both starters.
- Document the format in `references/motion-contract-json.md` and point the storyboard template, method and skill entry to it. Starter and preview output is pixel-identical to 1.13.0.

## 1.13.0, 2026-10-06

- Add a self-contained single-file motion preview: one HTML file with the embedded motion score, motion-craft easing, one renderer per scene, Play/Pause, Replay, frame stepping, a frame slider, keyboard control and `seekFrame`, with no dependencies, network or server.
- Motion Graphics Workflow now delivers this preview in hosts without shell or renderer, as a file when the host can create files or as one code block with save-and-open instructions. It does not depend on Canvas, which a 2026-10-06 ordinary ChatGPT diagnostic reported as unavailable in that conversation.
- Validation requires the preview to load no external resources and to embed the same contract as the runtime starters.

## 1.12.0, 2026-10-06

- Rewrite the Motion Graphics Workflow entry as one six-step method (stage, storyboard, motion design, runtime, build, review) with real neighbor skills instead of legacy workflow role names; keep the technical ID, review gate and internal handoff type.
- Add `references/motion-craft.md`: easing presets with CSS, GSAP and Remotion equivalents, frame durations, staggers, reading-hold heuristic, beat-grid arithmetic, transition grammar, typography recipes, legibility floors and common defects.
- Add a Remotion kinetic type starter and an HTML/GSAP motion starter. Both read the same `motion-score.json` contract, compatible with the existing score validator, and ship a dependency-free contract check with the reading-hold heuristic. Dependencies are pinned with lockfiles; nothing is installed inside the plugin.
- Verified in a development container: the Remotion starter typechecks and renders a 300-frame H.264 file; GSAP seeks are pixel-identical for direct, forward and backward sequences. Host behavior is not verified.
- Extend toolkit validation and tests to the new starters, including identical contracts across runtimes.

## 1.11.2, 2026-10-06

- Make the legacy `producer-ai-task-builder` alias explicit-only (`policy.allow_implicit_invocation: false`) so it no longer competes with Audio Production Director; explicit invocation still works.
- Add routing boundaries to catalog descriptions of overlapping owners: Storytelling vs Screenplay Story Architect and Storyboard Sequence Architect, Marketing vs Ecommerce Campaign Strategy Director, Brief Architect vs Instruction Packet Factory vs Hipson Adapter, and Pipeline Core vs Workflow Orchestrator.
- Add `ROUTING_BOUNDARY` and `EXPLICIT_ONLY_POLICY` checks with regression tests.
- Keep Pipeline Core, Asset Manifest, Instruction Packet Factory and Storytelling automatically available: 36 other owners read Pipeline Core references, and whether hosts allow reading files of a non-injected skill is unverified.
- Preserve 37 skill IDs, startup, welcome bytes and route tables.

## 1.11.1, 2026-10-06

- Shorten the `workflow-orchestrator` entry from 38.7 KB to about 29 KB and its description from about 800 to under 400 characters, without changing behavior.
- Keep the package identity block, compact version rule, automatic language policy, both complete welcome excerpts, entry sequence and both route tables in the entry.
- Move the full version-reporting procedure and rare routing boundaries verbatim into `references/version-reporting.md` and `references/routing-boundaries.md`, linked with the conditions that require them; merge duplicated entry and menu instructions.
- Add an entry size and description budget and checks that the moved rules and links remain.
- Preserve 37 skill IDs, startup menus, welcome bytes, routes and vendored snapshots.

## 1.11.0, 2026-10-06

- Make the shared research gate conditional: search only when a named tool or model, platform requirement, material public claim, current capability claim, real-world subject or request for inspiration, references or verification makes current sources decision-relevant.
- Keep stable craft on supplied or fictional facts free of searches and of no-research disclaimers; private business claims still require the user's source or omission.
- Handle ChatGPT without search and Codex with network access disabled: no disclosure for untriggered work, one brief limitation and unverified marking for triggered work, no attempt to bypass host restrictions.
- Update 36 skill entrypoints and shared references to the conditional gate; preserve privacy, untrusted-source, no-execution and failure-honesty contracts.
- Reclassify planned cases: 23 `required` with a named `research_trigger`, 126 `not_triggered`; add two planned integration cases for triggered offline research and untriggered restraint. All 201 planned cases remain not_run.
- Validator and regression checks reject a reverted mandatory gate, missing triggers, untriggered cases that expect the research owner and lost offline coverage.
- Preserve the complete welcome, automatic language policy, 37 skill IDs, startup menus and vendored snapshots.

## 1.10.1, 2026-10-04

- Present the existing motion owner as Motion Graphics Workflow while retaining its technical ID, invocation, files and internal handoff types.
- Clarify that creative area 8 chooses a work area, not HyperFrames or another engine.
- Select or recommend a runtime from the brief, working project, delivery needs and verified capabilities; Remotion does not require the user to name it first.
- Preserve all 37 skills, the two-option welcome, motion prompt library, existing approval boundaries and dependencies.

## 1.10.0, 2026-10-04

- Add a provenance-aware motion library: 120 original blueprints, 172 expressly permitted curator starters and 28 creator link records, with category retrieval and optional local search.
- Integrate reference breakdown, style frames, a focused motion proof and a shared visual/audio score into existing HyperFrames and Remotion workflows.
- Add optional injected Paper Shaders and Tone Offline adapters, rational frame helpers and local encoded-file inspection without installing dependencies.
- Record primary research, five viewing cases with actual inspection limits, additional prompt catalogs and a controlled model-comparison packet.
- Preserve the two-option welcome, 37 skill identities, current model, existing engines, provider boundaries, source snapshots and shared QA budget.
- Keep prompt provenance, source checks, adapter mocks, actual inspection, saved-host readback and active-client behavior separate. No claim of measured parity with Claude is made.

## 1.9.4, 2026-10-04

- Remove only option 3 from the complete English and Polish welcome; preserve the introduction, six capability bullets, qualifications and original two modes.
- Keep code-based motion graphics in creative work area 8, including the Creative / Expanded / Motion path and existing runtime descriptions.
- Remove the active startup shortcut and clarify an unmatched startup 3 without selecting motion; honor genuinely pending older menus on actual resume.
- Synchronize embedded welcome copies, protected hashes and existing entry regression fixtures. Preserve other owners, modules, dependencies and provider boundaries.

## 1.9.3, 2026-10-04

- Route plugin version and installation-status questions to the existing entry owner before creative intake.
- Project the current manifest identity into the readable entry and regenerate it during explicit release preparation.
- Require current evidence and distinguish the read package, saved hosted release and newest published release; report unknown or conflicting evidence without guessing from history.
- Add drift, missing/duplicate identity, read-only verification and native-wrapper regression checks.
- Preserve the complete welcome, existing creative routes, all 37 skill identities and provider boundaries.

## 1.9.2, 2026-10-04

- Tighten the existing Artifact Guard adaptation after live text probes: restrict exclusions to reported defects and keep uninspected identity findings unverified.
- Add concise release checks at the three existing retrieval paths; preserve all other runtime owners, menus and budgets.
- Retain the initial 1.9.1 behavior findings separately from subsequent retests; source availability does not prove consistent instruction adherence.

## 1.9.1, 2026-10-04

- Selectively adapt Artifact Guard diagnostic knowledge into Image Prompt Architect, Static Graphic Design Creator and Output Critic.
- Distinguish periodic microtexture, large repeated patches, false detail, intentional patterns and uncertain preview effects.
- Assess photographic plausibility and source preservation separately; compare faces after clothing/background edits.
- Keep optional context-isolation experiments inside the existing reference and repair contracts.
- Preserve the complete startup, all 37 skill identities, motion/teacher/ad modules, upstream sources and provider boundaries.
- Record source provenance and unmeasured visual effectiveness; add no cleaner, provider, universal prompt suffix or extra QA loop.

## 1.9.0, 2026-10-04

- Add optional Three.js/R3F, PixiJS, D3, Mediabunny Canvas export, Lottie JSON playback and a local Manim clip bridge through existing owners.
- Supply original runnable examples with pinned dependency graphs, one frame authority, seeking checks, local encoded preview and decoded-output inspection.
- Add source attribution, runtime cards, bounded acceptance guidance and structural/regression checks.
- Preserve the complete startup, all 37 skill identities, teacher/ad modules, provider gates and pinned upstream sources.
- Keep source, local render, saved-host readback and active-client evidence separate. No automatic engine installation or external generation is introduced.

## 1.8.1, 2026-10-04

- Add a selectable code-based motion graphics shortcut to the complete Polish/English welcome, with supported tools and preview/export availability limits.
- Retain the selected motion area and explicit runtime through pace selection; add creative area 8 while preserving areas 1–7 and both original intents.
- Synchronize embedded welcome copies, shared entry guidance, protected hashes and existing regression checks/fixtures.
- Preserve all six capability bullets, 37 skill identities, existing motion/teacher/ad content, provider boundaries and upstream sources.

## 1.8.0, 2026-10-03

- Add an optional teacher profile for lessons, worksheets, games, quizzes, slide content, classroom guidance, career exploration and teacher documents.
- Supply an original twelve-activity bank, three complete Polish lesson packs with student tasks and teacher keys, and reusable pack/administration templates.
- Align objectives, prerequisites, support, answers and delivery checks; distinguish plans, observations, synthetic data and verified facts.
- Separate classroom-material creation from personal Learning Mode through existing owners and one review budget.
- Preserve 37 canonical skills, startup, menus, provider rules, prior methods and upstream sources.
- Separate content/source verification from actual exports, active-client behavior and untested classroom outcomes.

## 1.7.0, 2026-10-03

- Selectively adapt Meta Ads Designer methods into existing campaign strategy and static-design owners.
- Add proof-led ad structures, observed-versus-inferred competitor analysis and a creative experiment card tied to asset revisions.
- Turn supplied campaign results into bounded hypotheses and next briefs, preserving metric definitions, comparable cohorts and inconclusive outcomes.
- Preserve 37 skill identities, startup, learning, provider gates, pinned sources and one shared review loop.
- Import no provider wrapper, diagnostic code, style catalogue, fixed platform constants or automatic performance verdicts.
- Keep source verification separate from active-host behavior, generated imagery and campaign outcomes.

## 1.6.0, 2026-10-03

- Connect code-based motion graphics through the existing HyperFrames, Remotion, sequence and production owners.
- Add a versioned frame/approval/Style Lock contract, three stage prompts and evidence-bounded review/delivery templates.
- Add an original dependency-free HTML/SVG frame example with shared preview and SVG-sequence export logic.
- Adapt selected Motion Designer Studio methods with pinned source attribution and MIT notices; install no additional engine, provider or owner.
- Preserve startup, learning, exact-copy/asset locks, 37 skill identities and one shared QA budget.
- Recorded source checks and SVG execution are separate from active-client, temporal/audio and encoded-video verification.

## 1.5.0, 2026-10-03

- Connect website evidence, incremental business discovery, positioning, substantiated claims and commerce campaign planning through the existing owners.
- Add staged rollout, campaign asset cards, realistic product/human production guidance and source-aware measurement with inconclusive outcomes.
- Preserve one Project State, one QA loop, integrated static ownership and separate execution authorization.
- Add eight planned campaign cases and focused source-contract regressions; no client media, ad spend or sales-outcome claims.

## 1.4.0, 2026-10-02

- Add diagnostic first practice within the lesson, with no extra onboarding and optional skipping.
- Graduate and fade assistance, honoring full-explanation requests and keeping one pending attempt.
- Track criterion-specific support and independence separately from completion and generated-output quality.
- Revisit earlier skills with retrieval and changed-context transfer tasks in relevant learning sessions.
- Diagnose craft, instruction, reference, generator and tool causes from evidence; insufficient evidence remains Unknown.
- Link exercises through one evolving learning project and preserve evidence in the existing state and handoff.
- Add eight planned scenarios and source-contract regressions; no active-client or educational-outcome claim.

## 1.3.4, 2026-10-01

Automatically selects the full welcome and subsequent menu language from explicit preferences, meaningful user text, actually supplied host language and conversation context. Removes the fixed Polish default and explicit-translation requirement. Embeds complete, protected English and approved Polish texts plus a synchronized language policy before routing; other languages translate the complete English source. Preserves all capabilities, optional materials, numbered choices, checkpoints, direct-task/resume behavior, 37 skill identities, metadata, starters, assets and pinned sources. Native Codex entry and negative source guards follow the same policy. Source checks and isolated source-use observations do not establish active-client behavior.

## 1.3.3, 2026-10-01

Centralizes installation in the complete ChatGPT Work and Codex guides, with README links instead of copy-paste installation prompts. Translates maintained package documentation, general learning-domain guidance and plan/progress labels into English. Preserves the full Polish welcome and its early embedded excerpt, localized UI and starters, exact-copy examples, multilingual fixtures, skill identities, routing, providers, assets and pinned source snapshots. English documentation does not change the user response language. Source and package checks do not establish fresh-account installation or active-client startup behavior.

## 1.3.2, 2026-10-01

Adds the required interface.short_description to fourteen included skill metadata files, including Workflow Orchestrator. Extends the canonical source gate and negative tests to reject missing, blank, mistyped, duplicated, mislocated and out-of-range descriptions. Preserves all 37 IDs, display names, existing starter prompts and invocation policies; every skill instruction body, canonical welcome, menu, onboarding, asset and pinned source is unchanged. The metadata defect is confirmed against current OpenAI package-check documentation. Its role in the reported ordinary-ChatGPT missing-skill behavior remains a diagnosis to verify in the active client; saved-package equality does not prove registration or startup compliance.

## 1.3.1, 2026-10-01

Restores the complete existing startup contract after an owner-reported mode-only reply. Places a synchronized byte-identical welcome excerpt before general review/routing instructions in Workflow Orchestrator, strengthens its bare-invocation trigger, and removes the short-choice ambiguity. The canonical welcome asset, menu wording, onboarding, checkpoints, direct-task/resume routes, 37 IDs, upstream and shared QA budget are unchanged. Adds protected-text and excerpt-integrity checks plus supplied-response negative cases. These checks do not establish that the active ChatGPT client loaded or followed the saved release.

## 1.3.0, 2026-10-01

Implements five conditional quality directions through existing owners: relevant few-shot examples, CRITIC-inspired declared-evidence checks, anchor-based pairwise judging with reversed order, explicitly adopted scoped Reflexion lessons, and an offline official-GEPA development pilot in the repository. Adds eight original teaching cases, a read-only quality helper and source/regression guards. Aligns explained rejection handling, selected static execution and H01/H02/KP02 owner expectations with active policy. Preserves all 37 skill IDs, interface assets/starters, welcome, menus, onboarding, pinned source bundles and the shared initial-review-plus-two-repairs budget. The 183 planned fixtures remain unexecuted. Declared-record checks and a zero-cost synthetic GEPA integration do not establish actual creative improvement, user calibration, active-client behavior or media quality. Publication evidence remains outside the shared package.

## 1.2.10, 2026-09-30

Fixes four audited regressions: lexical exact-copy matching, missing blueprint/operation/music-handoff validation, a grouped-choice example that conflicted with sequential learning onboarding, and missing pending onboarding context in the portable progress card. Adds six source regression tests. Existing routing, skill identities, provider rules, assets, starter prompts, canonical welcome and pinned sources are unchanged. Source checks do not establish installed-client behavior.

## 1.2.9, 2026-09-30

Defines CQoT as Critical-Questions-of-Thought and makes its critical checks part of the existing automatic review. MoE-style selects useful existing specialist responsibilities without claiming separate model or agent execution. CoVe verifies material factual/technical claims with sources or observed tests, reusing the research preflight; comparison and branching are conditional on a real unresolved choice or dependency. Direct and Quick tasks retain one shared review budget and stop unchanged on a pass. Clear goals and observable criteria replace mandatory hidden-CoT narration. Adds source-regression guards for the canonical meaning, shared budget, evidence boundary and owner routes. Preserves identities, assets, pinned sources, welcome, menus, onboarding and starter prompts; source checks do not certify active-client behavior.

## 1.2.8, 2026-09-30

Makes bounded output review automatic for substantive creative results, including ideas, prompts, copy, graphics and production plans, before final delivery. Every existing skill root points to the same profile. Reuses domain QA, preserves a passing draft, caps the initial review plus repairs at three evaluation passes by default and keeps stricter modality budgets. Actual media acceptance requires actual inspection; review never authorizes another generation, upload or paid retry. Welcome, menus, onboarding, technical identities and pinned sources remain unchanged. Source checks are distinct from installed-client behavior.

## 1.2.7, 2026-09-30

Adds a scoped brand-identity profile using existing owners: Marketing for foundations, Static Graphic Design Creator for integrated logo/visual craft and Delivery Documentation for logo/identity guides and actual file packaging. The shared contract and internal Brand Identity Pack carry revisions, selected decisions, acceptance criteria and evidence in one Project State. Sequential intake reuses supplied facts, while logo-only requests skip unrequested stages. Distinguishes concept rasters, reviewed digital assets and verified editable/production masters, including font, colour, variant and export limits. Extends the existing campaign/static learning domains without adding skill roots. Preserves the canonical welcome, menus, provider boundaries, assets, starters and pinned upstream sources. Source checks and bounded source-use tasks do not establish installed-client behavior.

## 1.2.6, 2026-09-30

Aligns durable and portable Project State fields and cross-host handoffs so interaction mode, unresolved choices and learning progress survive an explicitly requested checkpoint. Static-only work keeps concept, copy, text feasibility and prompt compilation in the integrated Static Graphic Design Creator; separate specialists serve separate requested deliverables. Copy delivery requires review and makes revision conditional on a diagnosed material issue, allowing a passing draft to stop unchanged. Existing source guards cover these contracts. Shortens the listing subtitle to the current 30-character package limit. Preserves the canonical welcome, sequential onboarding, all 37 skill identities, assets, prompts, provider boundaries and pinned upstream sources. Source checks and bounded source-use observations do not establish installed-client behavior.

## 1.2.5, 2026-09-30

Makes learning onboarding sequential at every model/effort setting: ask one question about one missing decision, accept a numbered choice or free text, wait for the answer, then ask only the next necessary question. Removes the permissions to batch learning questions from the mentoring method, integration policy and workstyle profile. Reuses voluntary answers, skips known or optional questions and proceeds to the plan and first lesson as soon as enough context is supplied. Keeps the canonical welcome and existing creative entry unchanged. The native Codex wrapper carries the same contract. No stress-test reports or transcripts are added to the shared package.

## 1.2.4, 2026-09-30

Uses one canonical Polish welcome as production text. Every sent Studio-only invocation, including repeated startup in the same conversation, copies the complete identity/capability introduction, optional-material invitation and final creative/learning menu verbatim, without a salutation or added prose. Preserves explicit language requests, concrete-task and actual-resume bypasses, checkpoints and the subsequent creative pace/work-area and learning routes. Native Codex installation points to the same asset. Source checks and bounded source-use observations remain distinct from active-client behavior.

## 1.2.3, 2026-09-30

Simplifies poster and static-graphic format intake: ask print/internet/both only when use is unknown, then describe paper sizes through familiar sheets or digital placement as post/story. Number every option, reuse supplied specifications and avoid mixed paper-code/pixel menus. Exact dimensions remain available for expert requests, prompt compilation and delivery. The shared intake method governs the orchestrator, Brief Architect and static-design owner without changing the pinned upstream source. Format choices do not establish print readiness, renderer controls or generation permission.

## 1.2.2, 2026-09-30

Strengthens the short Studio entry contract across reasoning settings: introduce capabilities and optional materials before the final intent menu, then require creative pace and work-area selections when unresolved. Choice tokens belong only to pending groups; resolved menus expire and simultaneous groups use distinct number/letter namespaces. Offline learning briefly discloses incomplete or unattempted research at the first substantive lesson. Preserves direct briefs, resumed work, learning progress, 37 skill identities, assets, starter prompts and provider boundaries. No stress-test reports or transcripts are added to the shared package. Source-use verification does not establish active-client behavior.

## 1.2.1, 2026-09-30

Restored the full Studio welcome and capability overview. Startup now offers creative/learning intent; a mode-only creative choice leads to quick/expanded pace, the established seven work areas and a relevant brief. Numeric replies bind to the last displayed menu, including older-session order. Concrete briefs bypass redundant selections. The learning curriculum, 37 skill identities, original sources, logo, starter prompts and execution boundaries remain intact. Updated source guards check these entry contracts; planned cases remain unexecuted host specifications. Source checks and a bounded text-only probe do not prove installed-client behavior.

The following notes preserve earlier checkpoints and their evidence limits. Their version numbers, fixture counts, external project paths and pending statuses describe those checkpoints, not the current release. See migration-status.md and the root README for current scope.

Checkpoint dev.7 added cross-cutting intake/reference-authority synthesis. Dev.8 clarified active research and corrected contradictory fixture expectations. The preliminary source map is outside runtime at `Execution/audit/codex-skill-agent-crosswalk.md`; the full Codex knowledge transfer remains incomplete.

Checkpoint dev.9 added a blocking anti-slop review between static direction and final prompt delivery, plus seven targeted fixtures, including valid type-led, maximalist and product-truth directions. Fixtures remain test plans, not passed model behavior.

Checkpoint dev.10 clarified concept states (`needs_selection`, `selected`, `locked`, `not_required`), permitted adaptations and prohibited substitutions within the existing Studio contract. Three planned fixtures cover unresolved selection, adaptation within locks and format/lock conflict. Tests check specification integrity, not executed model behavior. Olga’s independent review of this transfer was not performed in that session. Host behavior and renders were not checked.

Checkpoint dev.11 added two sourced profiles to the existing static-direction owner: business/membership cards and civic/social/political communication. It distinguishes raster concepts from production print files and requires an approved speaker and sourced facts for public communications. S36/S37 were added as planned fixtures with exact-copy/print boundaries and a guard against unsupported claims. This is not a behavior test, legal test, host QA or proof of complete static-design transfer.

Checkpoint dev.12 added a bounded Visual Prompter K07/K09 synthesis to the existing `image-prompt-architect`: staged validation from neutral master to required three-quarter views, profiles only after stabilization and when needed, then purpose-dependent later views; one main change axis at a time; promotion only after inspecting and accepting the actual render for its purpose; rollback to the last accepted master after drift. S38 records this boundary as a planned fixture with missing images. Olga independently accepted source fidelity, fixture, guards/tests and the text-only probe. This does not establish host behavior, identity continuity or render QA, nor complete Visual Prompter/LUMENFRAME transfer.

Checkpoint dev.13 added a bounded LUMENFRAME ROOT/META/K01–K04 transfer to the same owner. Source-to-runtime comparison found no need to duplicate K01, K02 or K04. K03 supplied a procedure distinguishing crop, viewpoint change and redesign; anticipating parallax/occlusion and unknown newly exposed surfaces; and separating semantic continuity from pixel identity. The owner description also covers original still-image prompts without imposing poster copy/layout on images without a communication layout. S39 is a planned fixture with guards. Iga ran a separate synthetic text-only probe; Olga accepted specification/runtime/probe in a read-only review. Before dev.14 the package had 39 static fixtures; all 79 dev.13 cases remain evaluation plans, not passed behavior, renders or host tests.

Checkpoint dev.14 added a bounded synthesis of selected Visual Prompter K15 sections for independent still-image series to the existing `image-prompt-architect`. The compiler distinguishes separate files from boards, campaign-format adaptation and temporal sequences; establishes count, individual image purpose, coverage/progression, shared DNA and allowed differences; and makes each prompt standalone, binding only actually attached carriers. S40 describes three fictional images with approximate text-only continuity and remains planned. Iga ran a synthetic text-only probe; Olga independently accepted the bounded mapping/runtime/fixture/probe with no P0–P2 findings. After dev.14 verification the package had 40 static and 80 total planned fixtures; these are not host-behavior, render-continuity or image-quality tests. Full K15 and broader Visual Prompter/LUMENFRAME transfer remain open.

Checkpoint dev.15 added a bounded Visual Prompter K14 transfer, sections 270–294, 497–514, 542–555 and 593–603, to the existing `image-prompt-architect`. Scoped editing separates the requested change, protected properties, narrowly permitted physical effects of a new environment and observable integration checks. Background replacement preserves geometry, pose, camera, framing, focus and product truth. A conflict between a new environment and exact preservation of old reflections/shadows blocks the final prompt until the user decides. S41/S42 and guards/regressions were added. S41/S42 remain `planned`: Iga’s original probe omitted required research; a separate research-compliant follow-up received focused ACCEPT limited to corrected verification references. Research P2 was resolved only for that follow-up, not a behavior review. The full `verify-build` 19/19 on 2026-09-24 at 08:46:47 UTC establishes local checks, not host behavior or render quality. Broader K14 and full Visual Prompter/LUMENFRAME transfer remain open.

The initial source ledger is neither a complete inventory of the latest generators nor completed deep research. Adding further families requires documentation, examples, conflicts, tests and user sources. Do not supply model parameters from memory.

Structural file validation does not establish retrieval in ChatGPT or Codex. No installation, actual generation or visual model test was performed. New storyboard fixtures are evaluation plans, not model responses or reviewed renders.

For complex creative work, the user may select a model or deeper reasoning setting when the host offers it. The plugin does not control that choice through its manifest or guarantee that the setting alone prevents errors; verification still uses approved locks and acceptance criteria.

Checkpoint dev.16 added one commercial-video campaign-direction owner, two expanded references, ten targeted fixtures and neutral campaign routing before sequence/shot planning and prompt compilation. Platform sources are separated by placement/workflow; current parameters are not stored as universal limits. The anti-generic gate reviews direction and requires a local correction on failure, but is not render QA. Eryk accepted the evidence-attribution correction in a source-note-only review. Olga independently rechecked in read-only mode and accepted four findings concerning attribution, provenance, a single route and M02/M10 guards. Fresh-use, host/retrieval and campaign-render tests were not performed; M01–M10 remain planned.

Checkpoint dev.17 added manual sequential-review rules to the existing workflow-orchestrator only for users explicitly requesting separate assets: one element and candidate at a time, exact-image approval before revision selection, preservation of the previous accepted revision during repair, and stopping when no actual image is available to review. S43 records this as a planned fixture with honest no-output state. Regressions check fixture/guard integration, not model behavior. Full layer planning, a filesystem registry, ZIP export, alpha inspection and automatic assembly remain out of scope.

Checkpoint dev.18 added a separate music-video-direction owner from two distinct skill snapshots and Mira’s role critique. The synthesis supports concrete song-to-image relationships, persona as observable behavior, emotion/energy relationships, selected form, motifs, rhythm and references; deliberate stability and hypnotic forms are valid. It imposes no escalation, climax, symbol count or 25-section export. The orchestrator has exactly one route; M08 sends music-video briefs to that owner, and MV01–MV04 are planned fixtures. This review is not fresh-use, audio analysis, host testing or render QA.

Checkpoint dev.19 added one `producer-ai-task-builder` owner, one expanded reference, one route and seven planned PA01–PA07 cases. It synthesizes ProducerAI Assistant and Workflow Kit without copying the package: text packs for songs, lyrics, instrumentals and edits, plus music-video tasks. Music-video direction, shot cards, video-model prompting and execution remain with separate owners. Current Flow Music research distinguishes model from UI, dated announcements from current sources and practitioner anecdotes from facts; the exact video model remains `unknown_runtime` until confirmed by the current interface/source. PA07 treats exact synchronization as a hard requirement and blocks the prompt until the capability is verified; a best-effort alternative requires user approval. No generation or audio analysis was performed. PA01–PA07 remain planned. Full `verify-build` passed 21/21, package regressions 57/57, inventory 15/15 and skill quick validation 14/14. Olga accepted the bounded ProducerAI packet in an independent source/contract/structural review; this is not a host-behavior or quality test.

Checkpoint dev.20 added bounded interpretation of static-design catalog style labels to the existing `commercial-visual-campaign-director`: S44 permits an explicit reversible brief interpretation without a ritual question; S45 asks about a material retro-period choice and blocks dependent direction; S46 preserves a coherent hybrid brief by assigning separate roles to the grid and linocut illustration; S47 asks whether an unassigned equal-weight style stack means deliberate collision or a role-based system. Validator/regressions protect these four distinct behaviors. S44–S47 are planned specifications, not executed model replies. Dev.20 adds no router, second gate or fixed label limit.

Checkpoint dev.21 clarified explicitly separated assets in the existing `workflow-orchestrator`: a `depends_on` relationship requires reassessment but does not authorize automatic changes to an accepted dependent element. The contract preserves its selected revision and independent assets, requiring a clear user decision before a new repair; relationships are assessed only when actual assets are available. S48/S49 add two planned regression specifications. Full registry, `layer-plan.json`, a filesystem helper, ZIP export, alpha inspection and automatic assembly remain out of scope; fixtures do not establish model behavior.

Checkpoint dev.22 extended the existing `humanizer` with a bounded internal commercial-copy strategy process: audience/channel are tied to offer truth, available proof, justified tension/objection and action; mechanisms are compared instead of synonyms; weak angles are repaired before polishing; and the combined implication of image, headline, proof and CTA is checked. Named frameworks remain optional. S50–S52 are three planned specifications: distinct supported angles, an unproven claim and one exact locked line. Validator/regressions check contract integrity, not model behavior.

Checkpoint dev.23 added 19 dated text-to-image and image-to-image/edit family/product cards to the sole `research-evidence` owner, distinguishing checkpoint, API, consumer surface, references and uncertainty. The ledger separates official sources from dated practitioner tests and includes a watchlist rather than claiming complete market coverage. S53 describes fresh research on a named model without generation authorization and remains `planned`. After the first local run the package had 14 skills, 29 references, 57 files, 495,699 runtime bytes, 53 static fixtures and regressions 65/65; full verify-build and independent PRI-06 review were still pending. The snapshot does not complete video/audio mapping or criterion A.3 for Studio; the project remained unfinished.


## 0.1.0-dev.29 — 2026-09-28

Integrated the exact pinned Static Graphic Design Creator source bundle (34 files; post-transfer SHA-256 verification) as Creative Studio's static-only design owner. Routed campaign-family strategy separately. Replaced the Producer AI Task Builder user-facing role with Audio Production Director and retained the old skill path as a compatibility redirect because overlay updates cannot delete paths. Added current provider/rights references, short-form product motion bridges, realistic human reference capture, per-domain user workstyle schema, supplied-thread retrieval instructions and a portable Codex↔ChatGPT Work handoff. Expanded routing and research requirements and added nine planned fresh-use cases (H17–H25). Canonical validation and the focused structural tests are evidence about this package only; new scenarios are not executed host behavior.

## 0.1.0-dev.28 — 2026-09-28

Deepened the fourteen existing owners using 27 primary-source works, fifteen applied references and original reusable materials. Added declared asset revision/dependency validation and impact calculation, accepted/candidate snapshot discipline, static diagnosis records and a research-to-decision method. Preserved historical files, UI, owner boundaries, current provider research and media evidence requirements. Added twelve planned knowledge scenarios and deterministic asset-helper tests. Publication and actual verification are recorded in the release report; planned fixtures are not executed evidence.

## 0.1.0-dev.30

Integrated Workflow Kit commit 55c8bf19962c7bf7fb43648637ee433d990eb2a9 with 35 source skills mapped into 37 Studio entrypoints. Added 20 owners, shared project/prompt/QA contracts, editing and recovery routes. Resolved overlapping onboarding, audio, storyboard, copy and static-design authority. Preserved all original source files and license. Test evidence and runtime limits are recorded in docs/workflow-kit-integration.md.

## 0.1.0-dev.31 — 2026-09-28

Deepened twelve existing owners through six sourced chapters and reusable decision, sequence, preference, pilot and execution assets. Added a read-only structural sequence/taste checker. Aligned rejection handling: unexplained rejection gets one directional question; an explicit correction is applied directly. Addressed source duplicate discovery by retaining inert old paths and exact original source in a pinned archive. Preserved the complete static-design source bundle and plugin identity/interface. Verification: 43 Node tests, 23 Python tests, two bounded fresh text-use exercises; all passed their stated checks. The 167 planned evaluation fixtures were not executed. See creative-upgrade-verification.json for scope.

## 0.1.0-dev.32 — 2026-09-28

Expanded human identity, production reference sheets, reference capability routing and bidirectional audiovisual planning through five applied chapters, seven reusable assets and eight official-source cards. Repaired strict-identity readiness, audio rejection handling and video-review ownership. Quoted two colon-bearing YAML descriptions for portable parsing. Made pilots explicitly optional and not a development prerequisite. No pilot, fresh-use exercise, generation, paid call or external media upload was performed. Structural validation and source preservation are reported separately from media quality.


## 1.0.0, 2026-09-28

Prepares the existing Studio scope for repository distribution. Preserves all skill instructions, pinned bundles, logo and starters. Adds release-scope documentation and synchronizes current version markers. The 1.0.0 repository wrapper supplied distribution metadata (retired in 1.0.1), installation/update guidance and deterministic ZIP packaging. The owner approved Apache-2.0 for original code and instructions and public GitHub distribution. Hosted publication and GitHub publication are separate operations. Planned evaluations remain planned. See release-1.0.md.

## 1.0.1, 2026-09-29

Replaces registry-based setup with direct source installation through ChatGPT Work or Codex. Adds separate installation/update prompts, a complete source inventory and a native Codex entry backed by the intact Studio bundle. Preserves all 37 canonical skill roots, shared references, source archives, logo and starter prompts. Filesystem installation checks do not prove live host activation.

## 1.1.0, 2026-09-29

Added a dated provider catalog, source evidence, Polish setup guide and private connection-profile template. Extended four existing owners with optional post-install selection and explicit ChatGPT Chat/Work/Codex client, native-app, MCP, CLI and API boundaries. Distinguished Higgsfield consumer credits from Open Higgsfield API billing, captured public-documentation/runtime conflicts, and kept non-generating verification and prompt-only work available. No external provider was installed, authenticated or run. Verification covers package integrity; live provider entitlement and media execution remain untested.

## 1.1.1, 2026-09-29

Standardized all 37 skill display names and synchronized the installed Creative Studio plugin. Source and installed skill-file parity was verified for the updated release.

## 1.1.2, 2026-09-29

Aligned the shared research rule across the operating model and blueprints, added formal music-video and standalone-audio routes, made image routing depend on whether an image is a reference, edit base or review target, and added graph, research-owner and routing regression checks. Updated the installed Creative Studio plugin after the repository change. Structural checks and source readback were run; target-host creative behavior and generated media were not evaluated.

## 1.1.3, 2026-09-29

Corrected canonical route validation to allow an owner to appear in multiple operation-specific rows while keeping exact checks for reference, edit-base and review-target routing. Added explicit contracts for those image operations and fixed the orphaned-resource regression test. Synchronized release markers and the complete install-source inventory. Structural and regression checks pass; the 167 behavior specifications remain planned and were not run against a model.

## 1.2.0, 2026-09-30

Adds optional learning/creation intent to the existing orchestrator, a six-question maximum learning onboarding, a complete personalized curriculum method, fourteen existing-domain learning paths with no-render exercises, adaptive lesson feedback and a portable progress card inside the same Project State. Quick/Deep remains pace. Clear production requests retain their route and do not require learning onboarding. Adds sixteen planned scenarios and source-regression checks; the historical greeting is preserved with a source-guarded effective override. Keeps 37 skill IDs, original snapshots, logo, starter text/order and provider boundaries. Host UI, actual lessons and educational effectiveness require separate observed runs.
