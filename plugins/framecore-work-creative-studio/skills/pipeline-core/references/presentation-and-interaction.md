# Presentation and interaction

Owner: Pipeline Core, under [Studio integration authority](studio-integration-policy.md). Every Studio skill applies this one source when it chooses how a response is presented. It decides the form of a stage's answer (text, comparison, interactive experiment, form, chart or another element the host actually composes) and how an interaction may change Project State. It adds no skill, agent, state store, MCP server, app, component system, manifest key or tool. Domain owners keep their craft; this file only adds how their output is shown.

Contents: [host basis](#host-basis), [choosing the form](#choosing-the-form), [offering an interactive version](#offering-an-interactive-version), [text equivalence](#equivalent-text-path), [state and actions](#interaction-state-and-actions), [domain adaptations](#domain-adaptations), [module coverage](#module-coverage).

## Host basis

Checked 2026-10-08 against OpenAI's announcement, Help Center article, release notes and developer documentation. Some official pages could be read only through search-indexed excerpts; recheck before relying on a detail that changes behavior.

| Finding | Source | Scope and limits | Consequence for Studio |
|---|---|---|---|
| ChatGPT can compose an answer from text, visuals and interactive elements (buttons, forms, charts, side-by-side comparisons, diagrams, maps, small tools), choosing the form per question; plain text stays an option | [GPT-6 and Intelligent UI for everyone](https://openai.com/index/gpt-6-for-everyone/), [Intelligent UI in ChatGPT](https://help.openai.com/en/articles/20001598-intelligent-ui-in-chatgpt) | Launched 2026-10-07 in the Chat tab; GPT-6 Sol (Plus, Pro, Business, Enterprise) and Luna (Free, Go), Instant to Extra High reasoning; Enterprise depends on admin settings | Studio may ask for a form per stage; the host composes it. Studio never builds or promises a specific component |
| Not in the Work tab, not in Voice, not at the Pro reasoning option, not in older macOS and Windows desktop apps; models for Work and Codex are unchanged | Help Center and release notes as above | Availability can change | Work, Codex, Voice and older clients receive the text path without a disclaimer |
| Built from a fixed library of native, streamable components rendered progressively; OpenAI says design judgment still needs work | Announcement, as reported in launch coverage | Component list is not published | Do not name or depend on a particular component |
| Users steer it through Custom Instructions or a request in the conversation; on the web, Personalization, Layout and Visuals, Simple reduces visuals, and some may still appear | Help Center | No documented full off switch | An explicit plain-text request is binding for Studio's own choices; do not argue with the host's rendering |
| Some components, such as checklists, keep their state when a thread is refreshed; state does not carry across threads | Help Center | Which components persist is not listed | Never claim persistence; Project State and the progress card remain the record |
| Connected plugins keep working; no separate usage quota | Help Center | How plugin skill instructions weigh against the host's own choice is not documented | Studio instructions are guidance to the composing model, not control |
| Apps SDK and MCP custom UI (cards, carousels, fullscreen, picture-in-picture; follow-up messages through `ui/message`) are a different, developer-built mechanism | [UI guidelines](https://developers.openai.com/plugins/concepts/ui-guidelines), [Add UI to your MCP server](https://developers.openai.com/plugins/build/chatgpt-ui) | Requires an MCP server and widget code | Out of scope: Studio ships no server or widget. Its accessibility guidance (contrast, alt text, text resizing, UI only when it improves the workflow) informs what Studio asks for |
| HTML or code artifacts and the motion preview template are files Studio writes | Studio's own tools | Separate from native UI | Never the default replacement for a native element; offered as an optional downloadable version |

Unknown: how a click, slider move or form submission inside a native element reaches the model (whether every event becomes a message), how much a plugin's instructions influence the host's choice, which elements are available on each mobile client, and the accessibility behavior of individual native components. Design inference, not fact: textual guidance in the active skill can steer the composing model as user instructions do. In the owner's first test of 1.35.0 (2026-10-08, ordinary ChatGPT on a phone), menus appeared as tappable cards with the same numbers, a storyboard stayed a static table, and a request for more interactivity produced a self-contained HTML animatic that the phone did not display inside the chat.

## Choosing the form

Decide per stage, from the user's goal, the current stage, the type of data, the decision being made, what the host actually offers in this response, and cost and complexity. One primary presentation per response is the default; add another element only when the stage needs it.

Prefer a native element, where the host offers one, for:

- comparing two to four directions on the same fields;
- showing the effect of one parameter (hold time, easing, type size, contrast, tempo);
- causal learning, where the learner predicts and then sees the result;
- sequences and timelines (scenes, shots, beats, cues, lesson steps);
- decisions on structured data (asset status, campaign matrix, route costs that are known).

Stay with text for:

- copyable deliverables: prompts, copy, scripts, lyrics, packets, code and exact strings, always in their established fenced or plain form;
- short answers and a single obvious fix;
- content that gains nothing from interaction;
- an explicit request for plain text (it holds until the user changes it, and Studio's own tables, such as a storyboard table, then become plain lists with the same fields);
- any host that does not compose native elements, including Work, Codex and Voice.

Apart from the offer below, do not mention whether the host can render interface elements unless the user asked for something interactive that cannot be shown; then say so once, in one sentence, and give the text path. Do not repeat that note in later turns. Never describe an element as shown, saved or clickable unless the host rendered it.

### Offering an interactive version

Studio offers interactivity instead of waiting to be asked (owner decision 2026-10-08). When a stage's result would be easier to understand by exploring it, and the answer itself stayed text or static, end the response with one short, optional offer of an interactive version that names what the user could do with it, for example: "Chcesz wersję interaktywną? Oś czasu, na której klikasz ujęcia, odtwarzasz animatik i zmieniasz czas każdego ujęcia." Good candidates are a storyboard, sequence or shot list, a timing, easing or rhythm choice, directions to compare, a campaign or asset matrix, and a lesson concept with a visible cause and effect.

- One offer per stage, after the complete deliverable; it never replaces the deliverable or blocks the next step, and it is not a consent question.
- Name the benefit (what can be explored or decided), not the technology.
- Say which form it would take: an interactive view inside the chat where the host composes one, or a self-contained HTML file to open in a browser, which a phone may not display inside the chat. Where the host composes native elements, prefer the view in the chat and offer the file as the downloadable option.
- When other choices are pending in the same response, give the offer its own token namespace.
- Skip it for copyable deliverables, short answers, a single fix, an explicit plain-text request, the startup welcome and menus, a learning onboarding question, a response that ends with a pending learner exercise or question (the learner keeps one decision at a time; present the experiment interactively as the exercise itself, or offer it after feedback), and an answer that is already interactive.
- Record the reply in the existing Project State for that kind of stage: after a decline or no answer, do not offer it again for the same kind of stage unless the user asks; after a yes, similar later stages may go straight to the interactive form.
- Accepting builds the view or file from material that already exists. New image, video or audio generation, uploads and publication still need their own request.
- A file follows the existing rules: self-contained with no network requests, built from the current revision, and labelled as a preview, not a rendered video or a measured result.

Startup is unchanged: a bare invocation or greeting returns the complete canonical welcome as text, in the selected language, ending with its numbered menu. A host choice control may accompany a pending numbered group with the same tokens and meaning; it never replaces the welcome, shortens it or adds a menu. Learning onboarding keeps exactly one question per response; a form may carry only that one question.

## Equivalent text path

Every native element has a text equivalent that carries the same decision: the comparison as a short table or list with the same fields, the experiment as two or three described values with the predicted and observed effect, the timeline as a timed table with scene IDs, the form as one question or the numbered options. The text path is complete on its own; the user never needs the element to continue. Reply tokens stay valid whether the user clicks or types. Charts show only real numbers with their source; a projection is labelled as a projection with its assumptions.

Accessibility follows from this: meaning never depends on colour or position alone, every visual comparison names its fields in words, and anything shown as an image or diagram has a text description in the response.

## Interaction state and actions

All decisions live in the existing Project State and its `pending_choice_groups`; the interface is a view, never a second store.

- **Real events only.** Interpret only what actually arrives in the conversation: the user's message, or a message or value the element sends into it. A slider moved without a resulting message, or a view the user only opened, is not a choice. If an element's result is not visible to Studio, ask for the value in one short question.
- **Five separate layers.** Keep exploration (trying values, opening a view), a working change (an edit to the current draft), a selection or approval (the user's explicit choice of an exact item), an execution order (a request to generate, render, upload or publish) and a confirmed result (an observed output) apart. Exploration never becomes selection; selection never becomes execution; execution never counts as a result until the output is observed.
- **Selection is not authorization.** Choosing a concept, route or prompt does not authorize paid generation, an upload, an external provider or publication. Carry an authorization the user already gave for that exact operation; do not ask a ritual consent question when it exists.
- **Expiring groups.** A choice group expires when it is answered, skipped by a concrete request or replaced. A later click or number on an expired group asks one clarification instead of reopening it. A quiz answer belongs to its pending quiz and never selects from an old menu.
- **Revision binding.** Every view of a draft, storyboard, motion contract, prompt or matrix names the revision it shows. A choice made on an older view is applied to the newer revision only when the changed fields do not conflict; otherwise name the conflict and ask one question. A stale view never overrides a newer revision.
- **View versus content.** Sorting, filtering, zooming or switching a comparison layout changes nothing. A substantive edit (time, copy, order, asset) updates the contract and its revision, and propagates to its dependencies.
- **Persistence.** Do not claim that an element's state is saved. Within a thread some elements may keep state after a refresh; nothing carries across threads. Use the progress card or handoff for continuity.

## Domain adaptations

### Learning

Use the existing [lesson cycle](../../workflow-orchestrator/references/learning-mode.md#lesson-cycle): goal, explanation, example, attempt, feedback, transfer. An interactive experiment varies one variable at a time (hold time, easing, type hierarchy, contrast, rhythm) with the others fixed. Ask for the learner's prediction before the reveal, and wait for it. A click, a slider position or opening a view is not an attempt and not mastery; competency evidence still needs the learner's own decision, explanation or work. A quiz element keeps the attempt before feedback. One onboarding question per response and existing checkpoints stay unchanged; a complete brief goes straight to the plan and first lesson.

### Concepts

Compare at most four directions, usually two or three, on the same fields: idea, mechanism, visual character and constraint. Label each item's evidence level: description, sketch, reference or actual asset. Opening or expanding a direction is exploration; the choice goes to Project State as `selected` only on the user's explicit pick, and it is not approval of copy or production. The concept states in the [working contract](../../workflow-orchestrator/references/studio-contract.md#concept-selection-and-preservation) apply unchanged.

### Storyboard and motion

Use existing scene IDs and the existing contract (shot cards, the [motion contract](../../hyperframes-workflow/references/motion-contract-json.md)). A timeline view shows each scene's start, duration and copy from the current revision. A change to time, copy or order updates the contract and its revision; a view change does not. Show the dependency impact of a change in units the production uses, for example 2 s at 30 FPS is 60 frames, and which later scenes shift. Preview and render use the same revision. A native element is a planning view, not a video: it does not export an MP4 or replace the renderer, and without a renderer no export is claimed.

### Prompts and references

Show the exact prompt text, each reference's role, the scope of a change, locks, missing inputs and readiness. Separate a planned reference ("the product photo, to be attached") from an attached file Studio has actually received. The final prompt always stays a standalone fenced code block that can be copied; any table or checklist around it is supplementary.

### Campaigns and QA

Use matrices for audience, message, format and asset roles; hypotheses are labelled as hypotheses with how they would be measured. Never show invented CTR, ROAS, costs, reach or progress; unknown numbers stay Unknown. QA status comes from evidence: criteria passed, failed or uninspected for the exact version reviewed. A progress view counts only observed completions.

### Other modules

Apply the rule to each role's own output rather than copying the motion pattern. Evidence fits the medium: a waveform or loudness chart is not a listen, a still is not motion, a layout description is not a rendered board. Audio cue lists and song structures may be shown on a timeline; lyrics and prompts stay copyable text.

## Module coverage

Every active skill reads this file through the integration authority. The table gives each module's main use; anything else follows the general rule above.

| Module | Useful native form, when offered | Text path | State it touches |
|---|---|---|---|
| workflow-orchestrator | Choice control mirroring a pending numbered group; the welcome itself stays text | Complete welcome and numbered menus | `pending_choice_groups`, stage, mode, pace |
| pipeline-core | Stage tracker for multi-artifact work | Short status list | Project State, revisions |
| brief-architect | Form for agreed structured brief fields in creation | One missing question at a time | Brief fields |
| hipson-adapter | Scope matrix | Fenced packet | Packet revision |
| research-evidence | Source comparison table; timeline of dated claims; chart of sourced numbers only | Table with links and dates | Evidence Note |
| studio-workstyle-profile | Choice control for the one current question | Numbered options | Profile |
| static-graphic-design-creator | Concept comparison; one-variable type or contrast experiment in learning | Comparison table | Concept status, copy locks |
| image-prompt-architect | Reference-role and readiness checklist beside the prompt | Fenced prompt | Prompt revision |
| video-prompt-architect | Shot timeline; readiness checklist | Fenced prompt, timed shot table | Shot cards, revision |
| storyboard-sequence-architect | Scene timeline with durations and frames | Timed scene table | Scene IDs, revision |
| storyboard-board-architect | Layout comparison | Board specification | Board revision |
| hyperframes-workflow | Scene timeline; easing or hold-time experiment in learning | Scene and frame table | Motion contract revision |
| remotion-video-production | Composition timeline | Scene table | Composition revision |
| opencut-video-studio | Cut list timeline | Edit decision list | Edit revision |
| creative-video-producer | End-to-end stage tracker with dependencies | Checklist | Project State |
| commercial-video-campaign-director | Direction comparison; asset matrix | Tables | Campaign premise, locks |
| commercial-visual-campaign-director | Asset role and format matrix | Table | Asset roles |
| ecommerce-campaign-strategy-director | Offer and hypothesis matrix without invented metrics | Table | Measurement context |
| marketing | Positioning and audience comparison | Table | Brand foundations |
| copy-voice | Side-by-side variants for choosing; the copy itself stays text | Plain copy | Copy IDs, locks |
| humanizer | Before and after comparison | Plain text | Locks |
| screenplay-story-architect | Beat structure timeline; dialogue stays text | Beat list | Story revision |
| storytelling | Story arc diagram in learning | Beat list | Learning context |
| character-design | Character direction comparison | Comparison table | Character lock |
| cinematography | Framing or lens experiment in learning; shot comparison | Described values | Shot contract |
| caption-studio | Caption timing timeline; caption text stays text | Timed captions | Caption revision |
| audio-production-director | Cue list and song structure timeline; no chart counts as a listen | Cue table, fenced prompts | Audio packet |
| creative-music-video-director | Direction comparison; song section timeline | Tables | Direction lock |
| producer-ai-task-builder | Follows audio-production-director | As audio | Audio packet |
| reference-pack-curator | Reference role table, planned versus attached | Table | Reference roles |
| asset-manifest | Inventory and status table from evidence | Table or JSON | Manifest revision |
| delivery-documentation | Delivery checklist from measured properties | Checklist | Delivery specification |
| output-critic-iteration | Criteria checklist with evidence per item | Checklist | Review record |
| tool-routing-cost | Route comparison with known and unknown costs | Table | Authorization scope |
| instruction-packet-factory | None needed; packets are copyable | Fenced packet | Packet revision |
| ugc | Hook and script variant comparison | Table | Copy locks |
| workflow-self-improvement | None needed | Text | Maintainer lessons |
