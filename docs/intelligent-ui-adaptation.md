# Intelligent UI adaptation

Change CC-20261008-03, branch `cloud-code/CC-20261008-03-intelligent-ui`, baseline `2704f917535c723afe2c039b1cca67e6da0b5422` (package 1.34.0). Written 2026-10-08 on the owner's request: adapt every active Studio module to ChatGPT's native Intelligent UI without a separate plugin, MCP server, app or component system. No version bump, release, publication or hosted plugin update is part of this change.

## 1. Research synthesis

Checked 2026-10-08. The announcement and Help Center pages returned HTTP 403 to direct fetches from the development container, so their content was read through search-indexed excerpts and cross-checked against secondary coverage. Facts below are labelled by source quality.

### Confirmed by official sources (excerpts)

| Claim | Source | Scope and limits | Consequence |
|---|---|---|---|
| GPT-6 composes answers from text, visuals and interactive elements and chooses the arrangement per question; plain text stays an option | [Announcement](https://openai.com/index/gpt-6-for-everyone/), [Help Center](https://help.openai.com/en/articles/20001598-intelligent-ui-in-chatgpt), [release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) | Launched 2026-10-07 | Studio guides the form per stage; it does not build components |
| Examples: side-by-side comparisons, diagrams, charts, buttons, forms, maps, calculators, bill splitters, games, adjustable inputs for learners | Announcement and release notes | Examples, not a component list | Studio names purposes (comparison, experiment, timeline), never a specific component |
| Chat tab only; GPT-6 Sol (Plus, Pro, Business, Enterprise) and Luna (Free, Go); Instant to Extra High; not the Pro reasoning option (Astra); not Voice; not the Work tab; older macOS and Windows desktop apps unsupported | Help Center, [models article](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt), [Business release notes](https://help.openai.com/en/articles/11391654-chatgpt-business-release-notes) | Enterprise depends on admin settings | Work, Codex and Voice always get text; no disclaimer loop |
| Steering: Custom Instructions or an in-conversation request; web setting Personalization, Layout and Visuals, Simple reduces visuals, some may still appear | Help Center | No full off switch documented | An explicit plain-text request binds Studio's own choices |
| Some components (checklists) keep state after a refresh in the same thread; nothing carries across threads | Help Center | Component list not given | No persistence claims; Project State and cards stay the record |
| Connected plugins keep working; no separate usage quota | Help Center | Plugin influence on the form undocumented | Studio guidance is advice to the composing model |
| Rendering is progressive from native streamable components | [Community announcement](https://community.openai.com/t/gpt-6-and-intelligent-ui-in-chatgpt/1404139); described in coverage | | No dependency on a named component |
| Apps SDK custom UI (inline card, carousel, fullscreen, picture-in-picture; `ui/message` follow-ups) is a separate developer mechanism | [UI guidelines](https://developers.openai.com/plugins/concepts/ui-guidelines), [Add UI to your MCP server](https://developers.openai.com/plugins/build/chatgpt-ui) | Needs an MCP server and widget code | Out of scope; its accessibility guidance is reused as design input |

### Secondary coverage only

[Search Engine Journal](https://www.searchenginejournal.com/chatgpt-gpt-6-intelligent-ui/592249/), [TestingCatalog](https://www.testingcatalog.com/openai-rolls-out-gpt-6-with-intelligent-ui-in-chatgpt/) and [explainx.ai](https://explainx.ai/blog/chatgpt-intelligent-ui-gpt-6-interactive-answers-explained-2026) agree on web and mobile availability, the 7-speed bicycle demo, OpenAI's statement that design judgment still needs work, and no API availability. Not relied on for rules.

### Design inferences

- Text in an active skill can steer the composing model as user instructions do (inferred from the Help Center's steering guidance; not documented for plugins).
- The text path is the only form Studio can guarantee on every host, so it carries every decision.

### Unknown

How interactions inside native elements reach the model (every event as a message or not); how much plugin instructions weigh against the host's own choice; per-client mobile availability; accessibility behavior of individual native components; whether Work or Codex will receive the feature.

## 2. Adaptation specification

1. One shared source, `skills/pipeline-core/references/presentation-and-interaction.md`: host basis, form choice, text equivalence, state and action rules, domain adaptations A to F, module coverage for all 37 skills.
2. Reach: the integration authority every skill already reads routes to it; the orchestrator's native-control line routes later stages to it; short domain sentences in learning mode, startup menus, the working contract, Motion Graphics Workflow, Storyboard Sequence Architect, the prompt contract, review and repair, Ecommerce Campaign Strategy Director and Audio Production Director.
3. Protected: canonical welcome and its localization, menu order and tokens, one onboarding question per response, specialist split, one Project State, copy and continuity locks, checkpoints, the QA loop budget, hosts without interactivity.
4. Added validation: `scripts/validate-presentation.mjs` (coverage rows equal the owner roster, every domain route, entry reach, official dated sources with an Unknown list, planned cases), `tests/presentation.test.mjs` (mutation tests), `evals/presentation-cases.json` (17 planned host scenarios, `not_run`).

## 3. Scope package (Hipson Adapter method)

- **User problem:** in ordinary ChatGPT, answers can now be interactive, and Studio had only a rule for choice controls; it could neither use comparisons, experiments or timelines where they help nor protect state from clicks, stale views and implied approvals.
- **Expected behavior:** Studio picks text or a native element per stage, always with an equivalent text path, and keeps decisions in Project State.
- **Allowed files:** the shared reference above; one-sentence routes in the listed domain sources; README section; validator, test and eval files; repository records. No upstream snapshot, no `validate-package.mjs` or `package.test.mjs`, no manifest keys.
- **Protected properties:** as in section 2.3.
- **Acceptance criteria:** every active module covered with a text path; startup byte checks unchanged; canonical validator and all suites pass, except the installer inventory, which is regenerated only at a release; ten required scenarios plus module cases planned.
- **Verification:** canonical validator, Node and Python suites, mutation tests, an instruction trace of the scenarios, host test prompts for the owner.
- **Completion:** committed and pushed on the working branch with host behavior `NOT_RUN`.

## 4. Coverage matrix

| Module | User tasks | Native use, when offered | Text path | State | Change | Check |
|---|---|---|---|---|---|---|
| workflow-orchestrator | Startup, mode, pace and area menus, routing | Choice control mirroring a pending numbered group; the welcome itself stays text | Complete welcome and numbered menus | `pending_choice_groups`, stage, mode, pace | Native-control line now routes later stages to the shared policy; startup menus file: control mirrors pending tokens, expired click asks one clarification; Learning overlay: one-variable experiment, prediction first, click is not evidence | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| pipeline-core | Project State, handoffs, QA loop, prompt contract | Stage tracker for multi-artifact work | Short status list | Project State, revisions | New shared policy; integration authority routes every skill to it; prompt contract keeps the fenced prompt | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| brief-architect | Brief intake and gaps | Form for agreed structured brief fields in creation | One missing question at a time | Brief fields | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| hipson-adapter | Bounded task packets | Scope matrix | Fenced packet | Packet revision | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| research-evidence | Triggered research, evidence notes | Source comparison table; timeline of dated claims; chart of sourced numbers only | Table with links and dates | Evidence Note | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| studio-workstyle-profile | Optional workstyle adaptation | Choice control for the one current question | Numbered options | Profile | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| static-graphic-design-creator | Posters, graphics, design directions | Concept comparison; one-variable type or contrast experiment in learning | Comparison table | Concept status, copy locks | Via concept rule in the working contract | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| image-prompt-architect | Image prompts and edit instructions | Reference-role and readiness checklist beside the prompt | Fenced prompt | Prompt revision | Via prompt contract (shared reference) | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| video-prompt-architect | Video prompts, shot cards, clip review | Shot timeline; readiness checklist | Fenced prompt, timed shot table | Shot cards, revision | Via prompt contract (shared reference) | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| storyboard-sequence-architect | Timed sequences and shot cards | Scene timeline with durations and frames | Timed scene table | Scene IDs, revision | Timeline view, revision and frame impact sentence | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| storyboard-board-architect | Board layout specifications | Layout comparison | Board specification | Board revision | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| hyperframes-workflow | Code-based motion graphics, contract, render, sound | Scene timeline; easing or hold-time experiment in learning | Scene and frame table | Motion contract revision | Storyboard table may be a timeline of the same revision; never an export | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| remotion-video-production | Remotion compositions | Composition timeline | Scene table | Composition revision | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| opencut-video-studio | Edit planning in OpenCut | Cut list timeline | Edit decision list | Edit revision | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| creative-video-producer | End-to-end video coordination | End-to-end stage tracker with dependencies | Checklist | Project State | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| commercial-video-campaign-director | Video campaign ideas and asset jobs | Direction comparison; asset matrix | Tables | Campaign premise, locks | Via concept rule in the working contract | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| commercial-visual-campaign-director | Static campaign systems | Asset role and format matrix | Table | Asset roles | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| ecommerce-campaign-strategy-director | Commerce campaign strategy and tests | Offer and hypothesis matrix without invented metrics | Table | Measurement context | Guardrail: hypotheses and sourced numbers only | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| marketing | Brand foundations, positioning | Positioning and audience comparison | Table | Brand foundations | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| copy-voice | Copy and ready-to-use wording | Side-by-side variants for choosing; the copy itself stays text | Plain copy | Copy IDs, locks | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| humanizer | Naturalness edits of existing text | Before and after comparison | Plain text | Locks | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| screenplay-story-architect | Stories, scenes, dialogue | Beat structure timeline; dialogue stays text | Beat list | Story revision | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| storytelling | Narrative craft | Story arc diagram in learning | Beat list | Learning context | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| character-design | Character directions and continuity | Character direction comparison | Comparison table | Character lock | Via concept rule in the working contract | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| cinematography | Framing, lens, light decisions | Framing or lens experiment in learning; shot comparison | Described values | Shot contract | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| caption-studio | Captions and subtitles | Caption timing timeline; caption text stays text | Timed captions | Caption revision | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| audio-production-director | Music, lyrics, sound packets, audio review | Cue list and song structure timeline; no chart counts as a listen | Cue table, fenced prompts | Audio packet | Timeline allowed; no chart counts as a listen | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| creative-music-video-director | Music video direction | Direction comparison; song section timeline | Tables | Direction lock | Via concept rule in the working contract | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| producer-ai-task-builder | Compatibility alias for audio | Follows audio-production-director | As audio | Audio packet | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| reference-pack-curator | Reference roles for new assets | Reference role table, planned versus attached | Table | Reference roles | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| asset-manifest | Asset inventory and revisions | Inventory and status table from evidence | Table or JSON | Manifest revision | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| delivery-documentation | Delivery requirements and packages | Delivery checklist from measured properties | Checklist | Delivery specification | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| output-critic-iteration | Review and bounded repair | Criteria checklist with evidence per item | Checklist | Review record | Status view from evidence per criterion | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| tool-routing-cost | Tool and provider routes, costs | Route comparison with known and unknown costs | Table | Authorization scope | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| instruction-packet-factory | Instruction packets | None needed; packets are copyable | Fenced packet | Packet revision | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| ugc | UGC scripts and hooks | Hook and script variant comparison | Table | Copy locks | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |
| workflow-self-improvement | Maintainer lessons | None needed | Text | Maintainer lessons | Shared policy through the integration authority; no file change needed | Coverage row and reach: PASS (source); behavior: NOT_RUN |

## 5. Instruction trace of the scenarios

A reading of the instructions against each planned case, not a model run.

| Case | Rules applied | Expected outcome | Conflict found |
|---|---|---|---|
| PI01 short prompt | Choosing the form (copyable), prompt contract | Fenced prompt only | None |
| PI02 three concepts | Concepts, working contract concept states | Comparable fields; pick recorded as `selected`, not approval | None |
| PI03 lesson waits | Learning adaptation, lesson cycle step 5 | One variable, prediction, stop | None |
| PI04 full brief | Learning onboarding, startup menus | Plan and first lesson, no form | None |
| PI05 quiz after expired menu | Expiring groups, startup menus state rules | B is the quiz answer | None |
| PI06 scene fix | Storyboard and motion, revision binding, sequence architect | Revision 4, +60 frames, later scenes shift, others locked | None |
| PI07 stale view | Revision binding | Conflict named, one question | None |
| PI08 Work host | Choosing the form, text equivalence | Same comparison as a table, no disclaimer | None |
| PI09 no renderer | Storyboard and motion, Motion Graphics Workflow delivery | Planning view; contract and player route; no MP4 claim | None |
| PI10 plain text | Choosing the form | Plain text in later turns | Found: Motion Graphics Workflow requires a storyboard table. Repaired: a plain-text request turns Studio's own tables into plain lists with the same fields |
| PI11 to PI17 | Campaigns and QA, other modules, direct invocation, handoff, startup, authorization | As in the case file | None |

## 6. Host test for the owner (NOT_RUN)

Run in ordinary ChatGPT, Chat tab, GPT-6 at any level from Instant to Extra High (not Pro), web client, a new conversation per prompt, with the plugin connected. Record client, reasoning setting, what was rendered and whether you clicked anything. The installed plugin is still 1.34.0, which lacks this policy: these prompts need a later release containing it. Today they give a baseline of 1.34.0.

1. `Hej, od czego zaczynamy?` Expect the complete welcome with all six capability points and the numbered menu 1 and 2; buttons may be added, but the text must be complete.
2. `Zaproponuj trzy kierunki plakatu na festiwal jazzowy w Gdańsku, potem wybiorę jeden.` Expect three directions on the same fields, possibly side by side; then `Biorę drugi.` should be kept in later answers without generating an image.
3. `Chcę zrozumieć easing w motion designie. Ucz mnie krok po kroku.` After onboarding answers, expect one variable at a time and a prediction question before any reveal; clicking alone should not count as your answer.
4. `Napisz prompt do generatora obrazów: ceramiczny kubek na lnianym obrusie, poranne światło, bez tekstu.` Expect one copyable code block, no interactive extras.
5. In a motion project with a storyboard: `W scenie 2 wydłuż zatrzymanie o 2 sekundy. Reszta bez zmian.` Expect a new revision, the 60-frame impact at 30 FPS and the shifted later scenes; a timeline is only a view.
6. `Odpowiadaj tylko zwykłym tekstem. Jak skrócić spot z 30 do 15 sekund?` Expect plain text in this and later answers.
7. The same prompt as 2 in the Work tab. Expect the same content as text without a note about missing interface elements.

## 7. Status

- Source and structure validation: PASS on the branch, except the installer inventory test (16 failures from `config/install-sources.json`, which describes the released 1.34.0 package). In a scratch copy with the manifest regenerated, installer, GEPA and packaging passed; the regeneration is not committed because it belongs to a release.
- Instruction behavior: trace above; no model run.
- Host behavior: NOT_RUN.
- Medium assessment: not applicable (no media produced).
