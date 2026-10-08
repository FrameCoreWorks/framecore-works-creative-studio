# Full review plan: plugin, orchestration, skills and repository

Written 2026-10-08 on the owner's request, before the review starts. Baseline: `main` at `6ce79af`, package 1.38.0, 1168 tracked files, 908 in the shared package, 37 skills, 429 vendored `upstream/` files, 4 workflows, 13 eval suites. The review runs only after the owner switches to the highest reasoning setting and says to start.

## Goal

Find every gap, defect, contradiction and missed opportunity in the plugin and the repository, from A to Z: how Studio is built and published on GitHub, how the orchestrator routes and holds state, how each skill works and connects, how the executable tools behave, and how well tests and records prove what they claim. The result is a ranked list of findings with evidence and a ranked improvement backlog, not a general opinion.

## Rules for the review

- Every finding carries its evidence type: `EXECUTED_CHECK` (reproduced by running something), `OBSERVED_SOURCE` (read in a named file and line) or `INFERENCE` (reasoned, not observed). Unknown stays Unknown.
- Severity: `critical` (breaks startup, installation, publication or user trust), `high` (wrong result or false pass), `medium` (gap, drift, maintainability), `low` (polish).
- Read before judging: no finding from a file name or summary. Findings from earlier audits (docs/audit-2026-10-08-response.md) are rechecked, not copied.
- No paid calls, no uploads, no hosted plugin changes, no host tests on the owner's behalf. Host behavior stays NOT_RUN unless the owner reports it.
- Protected during any fix: startup welcome and its localizations, menu order and tokens, technical IDs, released package paths (never deleted, renamed or moved), vendored snapshots, owner-approved sound and motion references.
- Fixes follow the standing rule in AGENTS.md: verified fixes are released and pushed to `main`. Larger changes (new modules, restructuring) are proposed in the backlog first.

## Phases

### 0. Baseline

Fresh clone of `main`; record SHA, version, release v1.38.0 assets. Run `scripts/check_all.sh`, the browser motion tests and the legacy suite; record every number. Generate an inventory of all tracked files (path, size, hash, kind, in package or not, linked from where).

### 1. Repository and GitHub construction

- Layout: what belongs in the package versus repository-only files; stray, duplicated, generated or oversized files (largest: the 3 MB workflow-kit source archive, banners, logos); `dist/` and `.gitignore`.
- Manifests: both `plugin.json` files, `config/install-sources.json` against the tree, package identity block, version markers in every file that states one.
- Releases: download the v1.38.0 plugin ZIP and its inventory, compare with the tree byte for byte; tags and release history consistency.
- Workflows: release, checks, pages, release-notes refresh; triggers, permissions, pinned actions, what each proves, what is not run in CI (browser tests, sound tests needing numpy and ffmpeg).
- Root documentation: README, INSTALL, CHATGPT_INSTALL, CODEX_INSTALL, UPDATE guides, RELEASE_STATUS, VERIFICATION, CHANGELOG, RELEASE_NOTES, licenses, NOTICE; accuracy against current host procedures (official OpenAI sources, dated).
- Provenance: vendored snapshots byte-identical to their recorded source; license files present.
- Hygiene: secrets scan, private paths, personal data, broken links (also outside the package, which the validator does not cover).

### 2. Packaging and discovery

- All 37 `SKILL.md` frontmatters and `agents/openai.yaml`: names, descriptions, trigger quality and overlap (two skills claiming the same request), length budgets.
- Orphans: package files not reachable from any skill or index; references that link to nothing useful; duplicated rules in several files.
- Size and load cost: largest instruction files, what a host must read for a typical task, instructions that could be shorter without losing rules.

### 3. Orchestration

- Startup: EN and PL welcome, language policy, bare invocation, repeated invocation, resume, direct task bypass.
- Menus and tokens: pending groups, expiry, namespaces, learning onboarding (one question), presentation and interactive offers.
- Routing: the route table against all 37 skills; ambiguous requests; owners that no route reaches; handoff matrix, role map and gate registry against the actual skills.
- Shared state: Project State fields across templates (project-state, handoff, progress card) for drift.
- Cross-cutting rules: research gate, output review loop and budget, authorization, continuity, copy locks, presentation policy. Search for contradictions between files (rules that say always or never about the same thing).
- Instruction trace: walk a sample of each eval family (201 planned cases plus 19 presentation cases) through the instructions and note where the instructions give no answer or two answers.

### 4. Skill-by-skill review

Each skill against one rubric: purpose and trigger, inputs and outputs, method depth and currency, references actually wired, QA and stopping, handoffs in and out, learning overlay, presentation, research triggers, examples, dated claims about tools and models, size. Families:

1. Entry and core: workflow-orchestrator, pipeline-core, brief-architect, hipson-adapter, research-evidence, studio-workstyle-profile, workflow-self-improvement, tool-routing-cost, instruction-packet-factory.
2. Static and image: static-graphic-design-creator, image-prompt-architect, reference-pack-curator, character-design, commercial-visual-campaign-director.
3. Video and story: video-prompt-architect, storyboard-sequence-architect, storyboard-board-architect, cinematography, screenplay-story-architect, storytelling, caption-studio, creative-video-producer, opencut-video-studio, remotion-video-production.
4. Motion: hyperframes-workflow and its assets (scenes, renderer, player, export, revise, review, sound).
5. Audio: audio-production-director, producer-ai-task-builder, creative-music-video-director.
6. Campaigns and copy: commercial-video-campaign-director, ecommerce-campaign-strategy-director, marketing, ugc, copy-voice, humanizer.
7. Delivery and quality: delivery-documentation, asset-manifest, output-critic-iteration.
8. Teaching: the teacher profile and learning mode inside the orchestrator.

### 5. Executable tools

Code review and targeted runs of: the scene engine (JS) and the Python renderer (parity on all examples and formats), player and browser export, single-file preview, critique, sound (synth, recipe, generate, compose, direction, mix, check), revise, review-frames, asset manifest, kinetic and GSAP starters, GEPA pilot, benchmark, installer, packaging and publishing scripts. Look for wrong results, unhandled inputs, false passes, non-determinism, memory and time limits, security of generated HTML, and dependency pins.

### 6. Tests, validators and evals

Coverage map: which rule or tool has a test that would fail if it broke; tests that only check that words exist; the legacy suite (fix, retire as historical, or keep as a separate status); eval suites (realistic inputs, checks that a reviewer can apply, owners still current).

### 7. Records and documentation

CHANGELOG, release history, RELEASE_STATUS, VERIFICATION, ledger and verification JSON consistent with each other and with Git; stale statements; user-facing docs in plain language; host reports filed and linked.

### 8. Currency check

Current official sources only, dated: ChatGPT plugin and skill format, Codex skills, Intelligent UI changes since 2026-10-07, and the named tools and models in the provider catalog whose facts may have changed.

### 9. Gaps and opportunities

What Studio cannot do yet that its users will ask for; weak skills to deepen; connections to add or simplify; modules to merge or split; new tools that would make results depend less on the model (from the benchmark roadmap). Each item with value, effort, risk and what it would change for the user.

## Deliverables

1. `docs/reviews/full-review-<date>.md`: findings ranked by severity with evidence type, location, reproduction and proposed fix.
2. A ranked backlog: quick wins, fixes, improvements, new modules.
3. Separate statuses: source checks, CI, release parity, instruction trace, host behavior (NOT_RUN unless reported).
4. Quick wins fixed and released under the standing rule; larger items proposed for the owner's decision.

## Size and method

About 1170 files, of which the package's instruction text and the motion and sound tools are the bulk. A single session can do it phase by phase in order (0 to 9). With the owner's explicit agreement, phases 1 to 5 can also run as parallel reviewers, each given one phase or skill family and the rules above, with every reported finding verified again before it enters the report.
