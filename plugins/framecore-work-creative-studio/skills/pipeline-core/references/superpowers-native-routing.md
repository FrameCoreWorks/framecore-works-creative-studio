# Native Superpowers support

## Purpose and scope

Use the installed Superpowers plugin as process support inside the existing Studio workflow. Prioritize motion graphics, visual composition/layout and FrameCut. Apply the same routing decision to other Studio tasks when a trigger below matches. Studio owns creative direction, craft, assets and delivery; Superpowers supplies the selected planning, debugging, implementation or verification method. This is a native skill handoff, not an MCP connection or a bundled copy of Superpowers.

At each consequential direction, implementation-plan, repair, review and completion decision, check the trigger table. For a matching trigger, load and use the corresponding available Superpowers skill before making that decision. A mention of the skill is not an invocation. For greetings, unchanged status, menus or a mechanical copy correction, keep the existing short Studio route; do not start a development workflow.

## Discover, select and return

1. Resolve `superpowers:using-superpowers` and the selected skill from the current host's installed skill catalog. Read the entry once per active revision and read each selected skill when needed; reuse already loaded unchanged instructions. Use native skill-reading/invocation tools or the actual installed path. Do not hard-code a cache version, account ID, filesystem location or invocation syntax from another surface.
2. Keep availability distinct from execution: catalog visibility, successful skill read and actual tool results are separate evidence. When a required skill is absent or unreadable, mark support `unavailable` (record unknown availability in evidence), explain the relevant limitation once and continue independent work through the Studio owner. Do not claim Superpowers ran, install it automatically, create a substitute repo or call an external provider.
3. Carry one compact handoff in the existing Project State: `decision`, `studio_owner`, `trigger`, `selected_skills`, `support_status` (`not_applicable`, `unavailable`, `loaded`, `applied`), `artifact_revision`, `acceptance_criteria`, `evidence`, `next_owner`. Record observable decisions/results, not hidden reasoning. `applied` requires the method's relevant checks; `loaded` alone proves only access. Persist only through the task's actually available authorized storage.
4. Return the result to the same Studio owner and checkpoint. Keep one brief, timeline, revision history, acceptance matrix and QA budget. Skill use alone does not create a second agent; independent review requires a real supported dispatch.

## Trigger table

| Decision or symptom | Required native support when available | Scope and return |
|---|---|---|
| A new or materially changed direction has unresolved purpose, constraints or success criteria | `superpowers:brainstorming` | Clarify the actual gap and compare approaches with the Studio owner. Reuse the supplied brief and accepted design. Creative concepts, composition and storyboard stay with Studio. |
| An approved direction needs a multi-step technical implementation plan for coded motion, layout or media tooling | `superpowers:writing-plans` | Specify components, dependencies, exact timing/copy locks, executable checks and review points. A pure edit plan or prompt request stays in Studio's existing artifact; do not manufacture a code project. |
| A technical implementation plan is ready for authorized execution | `superpowers:executing-plans` | Work within the current authorized project and native host. Use `superpowers:subagent-driven-development` only when that execution method is selected and real delegation is supported and permitted. Return reviewed components to their owner. |
| Render/build failure, inconsistent frame timing, clipping, missing fonts, caption collision, audio drift or another reproducible technical defect | `superpowers:systematic-debugging` | Inspect evidence, isolate the failing layer, test one hypothesis and repair the cause. Distinguish an observed defect from an unconfirmed cause. Creative dissatisfaction first needs the domain owner's diagnosis. |
| Implementing or repairing meaningful deterministic code behavior, such as frame mapping, caption bounds, duration or variant generation | `superpowers:test-driven-development` | Use a failing behavioral check, minimal fix and regression check where the host can execute them. Visual taste is evaluated on actual media, not converted into invented unit tests. Preserve existing user code. |
| A substantial code implementation needs review, or code review feedback is received | `superpowers:requesting-code-review` / `superpowers:receiving-code-review` | Review the real implementation against the brief and checks; verify findings before changing code. A client's creative feedback is handled by Studio's relevant owner. |
| About to report a substantive deliverable, repair, render or technical check complete | `superpowers:verification-before-completion` | Require fresh evidence for the current revision and checked scope. Reuse the same completed Studio QA pass; technical success alone does not prove visual or audio quality. |
| Independent bounded technical tasks would benefit from parallel work | `superpowers:dispatching-parallel-agents` | Use only with real host tools, authorized scope and worthwhile review/cost trade-off. Assign separate outputs; FrameCut remains the sole master-timeline owner. |
| Authorized changes to workflow/skill instructions, or an explicit diagnosis of Superpowers behavior | `superpowers:writing-skills` / `superpowers:diagnosing-superpowers` | Use native plugin maintenance and scoped scenario verification. These maintenance routes do not run during ordinary creative production. |

`superpowers:using-git-worktrees` and `superpowers:finishing-a-development-branch` apply only to actual authorized repository work. A media project, plugin invocation or native plugin update is not permission to initialize, clone, modify or push a repository. Native-only/no-repository instructions exclude those steps; use the native artifact/update path and state any unsupported verification honestly.

## Priority workflows

### Motion graphics and coded composition

Motion Graphics owns concept, choreography, visual hierarchy, typography and sound implementation; Remotion Video owns a selected React/TypeScript composition. Use Superpowers to turn the approved design into a concrete build plan, diagnose code/timing/layout defects and verify the result. Preserve the existing engine unless a justified change is authorized. A moving outer container does not establish articulated character performance. Check the promised action, pivots/body parts, timing, readable holds, transitions and sound against actual frames and playback where accessible. A technical PASS or motion metric cannot replace that craft review.

### Layout, typography and static composition

Graphic Design owns layout, hierarchy, exact copy, references and visual choices; Caption Studio owns caption craft, with the motion owner implementing timed composition. Use Superpowers for ambiguous requirements, multi-step coded implementation, reproducible layout faults and completion evidence. Inspect the actual requested sizes and dense/edge frames for overflow, overlaps, font substitution and readability. For a raster edit, preserve the established image-edit route; do not replace it with HTML/SVG, a code repository or a provider solely to satisfy a development procedure.

### Sound with Earshot

Earshot (`earshot-audio:earshot`) chooses, makes and measures the sound; Studio keeps the brief and the review; Superpowers is the method for the code around it (owner request 2026-10-23): `writing-plans` for a soundtrack built in several steps (cue list, selection, mix, master, mux); `test-driven-development` for cue mapping and placement code, with the expected onset per cue frame written as a failing check before the mix; `systematic-debugging` when installation, `runtime.py`, a model load or a render fails, or a cue lands off its frame, reading the actual error and `status --json` before changing anything; `verification-before-completion` before saying a film's sound is done: `timeline --cues` (or measured onsets on the light tier) on the encoded MP4 of the current revision. None of this replaces Earshot's choice by listening or the user's ears.

### FrameCut

FrameCut owns the complete edit, rational FPS, source-to-timeline mapping, revisions and final delivery. Preserve its sequence: sufficient brief, full visual storyboard/contact sheets, feedback and current-board acceptance, final execution and review. A previously accepted unchanged board remains accepted. Technical repairs implementing it do not reopen intake or require duplicate design approval. New creative changes outside that acceptance follow the existing Studio decision gate. A request to make a film does not approve an unseen board. Samples remain optional and require the existing user scope.

For drift or timing defects, use `systematic-debugging` on source timing, component-local timing and master placement before changing offsets. An offset of six frames is `6 / actual_FPS` seconds, with rational FPS retained; never guess FPS or assume a constant correction fixes accumulated drift. Verify speech/caption/animation alignment and affected cut boundaries after repair. All specialists return to the existing FrameCut revision and master clock.

## Authority, permissions and host limits

Current user and host instructions govern both plugins. Apply each imported method only within the requested task, available capabilities and existing authorization. Reuse real approvals for the same unchanged artifact; missing authorization or a genuinely new creative decision remains unresolved. Do not add Git operations, duplicate onboarding, repeated approval rituals, automatic sample renders or additional QA loops merely because a generic development workflow contains them.

Superpowers does not supply renderers, install HyperFrames/Remotion/Blender, grant providers or credentials, or synchronize runtimes. Probe exposed execution/render capabilities; lack of a shell alone does not prove that code execution or rendering is unavailable. Without any available execution/render route, provide a clearly labelled plan or handoff, not a claimed render. No real agent tool means no claimed independent agent review. No hooks or background service are added. Paid generation, external APIs, uploads, publication, deployment, destructive actions and repository writes retain their existing user/host authorization boundaries; naming this plugin does not authorize them.

## Installation and maintenance

Use the [first companion setup](../../workflow-orchestrator/references/extensions.md#first-companion-setup) for explicit installation or first configuration. This routing is the shared public/native contract. Repository maintenance and hosted updates require their own user authorization; follow the repository-first publication order when both are requested, preserving existing private integrations. A saved release proves stored instructions; report separately whether a fresh host session has loaded and exercised them.
