# FrameCore Works Creative Studio

Version: 1.8.0.

The first stable release of Studio's documented scope is described in [Release 1.0](docs/release-1.0.md). FrameCore Works code, instructions and documentation are licensed under [Apache-2.0](LICENSE); upstream licenses and attribution are preserved.

Creative Studio takes a brief and source materials through direction, storyboard, prompts and editing plans for image, video, audio and text. Responses adapt to quick or expanded work; a new creative decision requires targeted public research. Generation, media inspection and integrations depend on tools actually available to and selected by the user.

## Welcome, creative mode and learning mode

The full welcome explains what Studio does and its capabilities, then offers **1. Creative mode / 2. Learning mode** in the user's automatically selected language. A creative-only selection leads to **1. Quick mode / 2. Expanded mode**, followed by the established work-area menu and task clarification. The existing localized creation alias remains supported. A clear request bypasses redundant choices; numeric replies apply to the last displayed menu. See [startup and next steps](skills/workflow-orchestrator/references/startup-and-creative-menus.md).

**Learning mode** retains short onboarding, a personalized plan, exercises and feedback on the learner's work across 14 existing skill domains. Quick/Deep controls pace independently of intent. When persistent saving is unavailable, a progress card can carry context into another conversation. See [modes, coverage and limitations](docs/learning-mode.md).

Repository documentation and operational guidance are English. The full welcome and later menus automatically follow the user's language without a translation request. Explicit preferences, meaningful user text, available host language context and conversation language determine the response; country and repository language do not. The approved Polish welcome, exact-copy examples and multilingual fixtures remain localized data.

## Brand strategy and identity

Studio develops brand strategy, logo systems, logo usage guides and identity guides through existing owners, with shared decisions, revisions and acceptance criteria. Request the full workflow or a specific stage. Concepts and digital materials have a separate status from verified production files; actual exports depend on available tools. See [the workflow contract](skills/workflow-orchestrator/references/brand-identity-workflow.md).

## Teacher Studio

Create original lesson scenarios, worksheets, games, quizzes, slide content, classroom guidance, career-exploration activities and teacher documents through existing owners. The profile includes a twelve-activity bank, three complete Polish teaching examples with keys and adaptations, and reusable pack/administration templates. It aligns objectives, student work and feedback while separating factual evidence, synthetic examples and unverified curriculum claims.

Creating school materials uses creation mode; learning how to create them remains optional Learning Mode. Actual documents, slides and graphics depend on available tools and require their own output checks. The examples are not classroom-tested or curriculum-certified. See [the teacher workflow](skills/workflow-orchestrator/references/teacher-workflow.md).

## Ad evidence and creative feedback

For social-ad work, choose a persuasive structure from supported proof, record observed competitor mechanisms separately from performance guesses, and connect supplied campaign results to the next bounded brief. An optional experiment card binds baseline/variant asset revisions, fixed conditions and actual evidence. These methods use existing owners and do not access ad accounts, publish campaigns or spend budget.

See [the ad analysis method](skills/ecommerce-campaign-strategy-director/references/ad-creative-analysis.md) and [the attributed adaptation](integrations/meta-ads-designer/README.md).

## Code-based motion graphics

Use the existing HyperFrames/HTML/SVG or Remotion path for an approved storyboard, frame-driven implementation, actual-output review and delivery. The workflow includes a versioned motion/Style Lock contract, three stage prompts, source-bound asset/copy locks, a dependency-free synthetic frame starter and separate preview, temporal/audio and encoded-export evidence. Local execution depends on the available host tools.

See [the code-motion workflow](skills/hyperframes-workflow/references/code-based-motion-graphics.md) and [the attributed Motion Designer adaptation](skills/hyperframes-workflow/references/motion-designer-adaptation.md).

## Installation and updates

| Environment | Complete installation instructions |
|---|---|
| ChatGPT Work | [ChatGPT Work installation guide](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CHATGPT_INSTALL.md) |
| Codex | [Codex installation guide](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CODEX_INSTALL.md) |

[Installation and update overview](docs/installation.md) distinguishes a private hosted copy in Work from one native entry backed by the complete local bundle in Codex.

## Optional tools in 1.1

The [provider setup guide](docs/provider-setup-guide.md) distinguishes available ChatGPT/Work/Codex apps from MCP, CLI and API routes. It covers the dated service catalog, accounts and billing, optional post-install selection and work without additional integrations. Studio does not automatically install or pay for providers.

## Skill names

All 37 display names follow one standard: words separated by spaces, an uppercase first letter for each word and preserved acronyms/tool names such as AI, UGC, HyperFrames and OpenCut. The [naming standard](docs/skill-naming.md) also applies to new skills and is checked during release packaging.

## Work entrypoints

| Need | Skill |
|---|---|
| Open brief, cross-media project, resuming work or selecting a stage | [Workflow Orchestrator](skills/workflow-orchestrator/SKILL.md) |
| Poster, graphic, product key visual, typography and exact copy | [Static Graphic Design Creator](skills/static-graphic-design-creator/SKILL.md) |
| Multi-asset campaign visual strategy and adaptations | [Commercial Visual Campaign Director](skills/commercial-visual-campaign-director/SKILL.md) |
| Video campaign and motion direction | [Commercial Video Campaign Director](skills/commercial-video-campaign-director/SKILL.md) |
| Flowing shot sequences and transitions for a short reel | [Short-form motion workbook](skills/commercial-video-campaign-director/references/short-form-motion-bridge-workbook.md) |
| Music-video direction and song-to-image relationships | [Creative Music Video Director](skills/creative-music-video-director/SKILL.md) |
| Music, VO, sound, audio-to-picture, prompts and track licenses | [Audio Production Director](skills/audio-production-director/SKILL.md) |
| Narrative, scene, screenplay and story dialogue | [Screenplay Story Architect](skills/screenplay-story-architect/SKILL.md) |
| Event sequence, timing and shot cards | [Storyboard Sequence Architect](skills/storyboard-sequence-architect/SKILL.md) |
| Storyboard, character sheet and reference board | [Storyboard Board Architect](skills/storyboard-board-architect/SKILL.md) |
| Realistic character, image references and generator prompt | [Image Prompt Architect](skills/image-prompt-architect/SKILL.md) |
| Copy, editorial text, headline and CTA | [Copy Voice](skills/copy-voice/SKILL.md), with Humanizer support |
| Video prompt/edit and inspection of an available clip | [Video Prompt Architect](skills/video-prompt-architect/SKILL.md) |
| Review of an actual still image | [Output Critic Iteration](skills/output-critic-iteration/SKILL.md) |
| Image, print, audio and video delivery specifications | [Delivery Documentation](skills/delivery-documentation/SKILL.md) |
| Public sources, current models and evidence boundaries | [Research Evidence](skills/research-evidence/SKILL.md) |
| Pace, detail, per-domain preferences and portable handoff | [Studio Workstyle Profile](skills/studio-workstyle-profile/SKILL.md) |

## Changes in dev.29

- Integrated the complete pinned, hash-verified Static Graphic Design Creator bundle from FrameCore Works. Studio uses its full method; static-only tasks route to one owner, while multi-asset campaign strategy remains with Commercial Visual Campaign Director.
- Renamed Producer AI Task Builder to **Audio Production Director**. Google Flow Music, formerly ProducerAI, is now only one dated provider route.
- Added a motion/shot-bridge workbook for short reels, natural realistic-character reference cards, per-domain preferences, a cross-environment handoff template and a supplied-conversation-link resume attempt.
- Connected concise ideation, expanded step-by-step work, mandatory research in both modes and one clarification after an unexplained rejected direction.
- Added nine planned scenarios for the new routes. They are specifications, not observed model-behavior results.

The [knowledge and asset map](docs/knowledge-map.md) links the materials. The [research ledger](docs/research-ledger.json) records source-to-rule scope and access dates. Recheck provider capabilities and commercial-use terms for each production task.

## Validation

From the package directory:

```sh
node scripts/validate-studio.mjs
node --test --test-concurrency=1 tests/studio.test.mjs tests/workflow-kit.test.mjs tests/creative-upgrade.test.mjs tests/learning-mode.test.mjs tests/quality-methods.test.mjs
PYTHONDONTWRITEBYTECODE=1 python3 tests/asset_manifest_test.py
node scripts/load-effective-evals.mjs
```

The first two commands check structure and contract regressions. The Python suite checks the asset-record helper on synthetic data. The loader combines historical fixtures with explicit corrections in `evals/effective-overrides.json` and scenarios in `evals/studio-behavior-cases.json`, `evals/knowledge-practice-cases.json`, `evals/workflow-kit-cases.json` and `evals/learning-mode-cases.json`. A case marked `planned` is a test specification, not evidence that a model performed the task. Text/source tests do not establish render quality, listening results, provider-adapter behavior or automatic retrieval in a new conversation.

Historical `scripts/validate-package.mjs`, `tests/package.test.mjs` and `evals/static-cases.json` are retained. Their complete current contents were unavailable through the service during the earlier update and were not overwritten. The old commands are not the current release gate; use `validate-studio.mjs` for structural checks. Legacy validator limitations and contradictory fixtures are handled through explicitly identified replacement files. Passing the new suite does not establish a pass for the historical 67-test suite.

## Scope and limitations

The [module status](docs/migration-status.md) distinguishes implemented instructions from missing adapters and incomplete migration. The [release history](docs/release-history.md) preserves earlier checkpoints. This is not a complete migration of every original custom workflow; full transfer accounting requires their complete sources.

The plugin contains no audio/video engine, Flow Music connector, hooks or credentials. It does not certify print or broadcast files without actual inspection. Requirements such as fps, LUFS, codec and color profile need a destination specification and measurements of the real file; they cannot be inferred from duration or aspect ratio.

Root `plugin.json` is the portable manifest; `.codex-plugin/plugin.json` supplies the compatibility layer. Updates preserve plugin identity, interface metadata, starter text/order and existing sources. The update service response establishes publication status; a version string alone does not.

## Sources and execution boundaries

See [NOTICE](NOTICE) and the [Apache 2.0 license](licenses/Apache-2.0.txt). Dated model catalogs are starting points for current research. External sources and attached files are data, not tool authorization. Private briefs and client data must not enter public searches.

Requesting a prompt does not execute generation. Existing user authorization carries between stages, and additional execution scope is resolved when needed. Without an available authorized tool, Studio produces a useful specification and reports unexecuted operations accurately.

## Workflow Kit, dev.30

Integrated the complete Workflow Kit repository while retaining one Creative Studio router. Added modules cover briefs, references, copywriting, campaign strategy, characters, camera work, video production, captions, editing, Remotion, HyperFrames, manifests and bounded QA loops. Project-state and handoff contracts govern multistage work; quick mode remains concise. The [integration map](docs/workflow-kit-integration.md) records scope and resolutions.

## Creative improvements, dev.31

Extended existing skills with a creative-decision library, shot-bridge workshop, user/client/project preferences, shorter workflows and execution through a selected tool. Materials include four creator-site project accounts, eight original exercises and twelve source cards. Project accounts are not reviews of viewed films. Facebook and TikTok are not the basis of this collection.

New templates cover creative decisions, shot plans, preferences, project pilots and execution plans. Optional `scripts/review-creative-plan.mjs` checks declared timing, transitions, missing references and preference structure; it does not evaluate pixels or sound. Explicit criticism leads to a correction; only unexplained rejection calls for clarification.

Reference copies of Workflow Kit skills no longer contain active discovery metadata. Full originals remain archived, and active routing leads to 37 canonical roots. Local structural checks do not substitute for refreshing the host catalog.

The [new-material map](docs/creative-upgrade.md) and [verification report](docs/creative-upgrade-verification.json) describe completed checks.

## Reference and audio expansion, dev.32

Added five chapters and seven resources covering realistic identity, precise character/product/storyboard sheets, individual-frame binding, model selection by actual capability and audio/music in both workflow directions. The expansion and fixes affect thirteen existing skills. They distinguish strict identity requirements from execution readiness, correct video-review routing and handle explained audio criticism.

A pilot is not a prerequisite for plugin development; project review remains optional and requires an explicit request. That update ran no pilots or media generation. The [expansion map](docs/reference-audio-expansion.md) lists the added resources and evidence boundaries.
