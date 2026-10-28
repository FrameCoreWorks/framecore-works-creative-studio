# Roadmap for the development surfaces

Kept by every surface (Cloud Code, Codex, ChatGPT Work). The rules for writing are in [AGENTS.md](../AGENTS.md#current-rules-consolidated-2026-10-24); this file says which way to develop and why. Update the current part when the direction changes, and move what it replaces into the history below.

## FrameCore Open Assets creation, 2026-10-28

The owner authorized building the named companion with Earshot's compatible package structure. The
[build record](research/framecore-open-assets-build-2026-10-28.md) separates source checks, live Work
CLI tests, saved-plugin readback and actual client behavior. Include every fully qualified source;
policy holds and unrun host/category paths remain visible. The existing Studio package is unchanged.
This authorization supersedes the earlier build-pending statements, not their qualification gates.

## Owner-directed media companion scope, 2026-10-27

The owner selected **all asset sources that fully meet the provider requirements**, without a provider-count cap or a small launch shortlist. Follow [Task 1 in the current handover](handover-claude-code-2026-10-27.md#task-1-top-priority-a-keyless-free-media-companion-plugin-openverse-set-aside) and the [qualification rule](research/free-media-providers-2026-10.md#owner-selection-decision-2026-10-27): permitted free/keyless public APIs, enforceable per-asset rights and provider client rules, and successful required media/host tests. Unresolved material conditions remain Unknown and block enabling the affected path; technical download success is not complete qualification. Openverse remains set aside. The owner approved the companion name **FrameCore Open Assets**, identifier `framecore-open-assets` (`CW-20261027-03`); the selection and naming decisions do not start implementation, installation or a release.

## Current direction (2026-10-25, package 1.137.0)

- **State.** Studio 1.137.0 with 37 skills, plus three companion plugins in the same marketplace: Earshot Audio 1.0.8, Voice And Narration 1.0.2 and Brand Kit 1.0.1 (current versions in `.claude-plugin/marketplace.json`). Since 1.122.0 the owner opened bounded tasks: the skill rename (1.127.0), Voice And Narration (1.128.0), the Opus motion gallery (1.129.0), proactive skill search (1.130.0), Brand Kit (1.131.0), the review fixes (1.132.0), opt-in startup style (1.133.0), Cinematography decision cards (1.134.0), the motion delivery folder (1.135.0), the gallery shortlist for storyboards (1.136.0) and, in 1.137.0, dated platform caption specs (Caption Studio), a dated disclosure card (UGC) and fixes for the unstable host cases G14 and OG02. The hosted ChatGPT plugin is updated by the owner from `CHATGPT_UPDATE.md` (last saved 1.126.0; pending since 1.127.0).
- **Latest bounded tasks.** The owner's A-to-Z [review of 2026-10-24](reviews/full-review-2026-10-24.md) is closed (fix status at its end); its reference recommendations 1 to 3 are done (Cinematography, platform caption specs, UGC disclosure). Recommendations 4 to 7 wait for the owner.
- **Budgets.** Measured 2026-10-25: skill descriptions use 7,484 of 7,800 characters and the orchestrator 31,851 of 32,000 bytes, so new capabilities go to companion plugins and depth goes to references inside existing skills (priorities in the review).

Direction, in order of value:

1. **The owner's findings from real use and the review fixes**: reproduce, fix the smallest cause, test before and after.
2. **Companion plugins** for new capabilities, each with its own budget, version guard (`scripts/check_version_bump.py`) and Studio registry entry pinned to its reviewed commit.
3. **References that deepen existing skills** when the owner opens that task (cinematography, platform caption specs and UGC disclosure are done; next in the review: English source versions of the Polish delivery and copy templates, a marketing research method, producer worksheets, story diagnostics).
4. **Cheap evidence on every surface** (unchanged from 2026-10-22, below).
5. **Recommended extensions** (unchanged from 2026-10-22, below).

Not the direction: personal defaults (ready templates are allowed since the owner's decision of 2026-10-27), deleting package paths, or growing a reference without a trigger.

## History (newest first)

### Direction 2026-10-22 (package 1.121.0 to 1.122.0)

- **State.** 1.122.0, 37 skills, 1,552 canonical package files. Development is paused for the owner's real-use tests except for explicit bounded tasks. The current [temporary takeover](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/8a8c78c8b15be8934b32c49c88c30413f185c387/docs/handover-chatgpt-work-2026-10-22-superpowers.md) records the separate hosted state and Claude's unfinished Open Design plan.
- **Latest bounded task completed.** The approved [Superpowers companion integration](superpowers/plans/2026-10-22-studio-companion-implementation.md) is published in 1.122.0 and the existing ChatGPT plugin is updated with its private overlay preserved. Superpowers is first recommended and separately installed; Studio retains creative ownership. Fresh installed-client behavior remains untested; Open Design stays paused.
- **Why the pause matters.** From 1.88.0 to 1.118.0 the package grew by about 330 files, mostly knowledge adapted from outside repositories and articles, while no version since 1.36.0 has been tested in a live client and the 204 planned host cases remain not_run. The owner's verdict on the 2026-10-16 test reel showed the gap: every automatic check passed and the reel was still too quiet for a client. New knowledge is worth less than evidence from real use.

Direction, in order of value:

1. **The owner's findings from real use** (FrameCut, motion, startup in the actual clients): reproduce, fix the smallest cause, test before and after.
2. **Fixes from the 2026-10-16 test reel** (change CC-20261021-02): a marked sound moment must never be silent; acceptance checks locked copy and motion activity for HyperFrames reels; a service reel needs pictures, never a realistic object drawn in code, and its plan names the first-second image and the one big moment.
3. **Room in the startup file.** The orchestrator `SKILL.md` was 16 bytes under its 32,000-byte budget at 1.118.0; move routing detail to references so a found defect can be fixed there. A change to startup text needs the owner's ChatGPT startup check.
4. **Cheap evidence on every surface.** Claude Code runs at most 5 headless cases per gate with the owner's plan; Codex has not run 1.77.0 onwards; ChatGPT Work records sandbox runs separately from installed-client behavior.
5. **Recommended extensions.** Every repository the owner sends is reviewed and added to the registry ([guide](extension-registry.md)). Since 2026-10-22 Studio also proposes one, once and in the user's terms, when it clearly improves a reel (FrameCut and Motion Graphics aim for the strongest result, not the simplest) and installs it only after the user agrees; replies never quote Studio's own files or rules.

Not the direction: new knowledge rounds, ready-made ideas or category lists, personal defaults, deleting package paths, or growing a reference without a trigger.

Open items with a known trigger: OmniVoice's weights licence is unverified; Motion Designer cannot install in Codex (its front matter); the web motion probe has not run on a live script-driven site; the private hosted overlay must be preserved on every update; skill descriptions use about 7,716 of 7,800 characters.

### Account-free creative knowledge (2026-10-21)

The owner explicitly authorizes integrating useful Adobe-derived methods as skills/knowledge without Adobe accounts or services. Follow [the bounded scope](adobe-account-free-2026-10-21.md), preserve existing owners and the full FrameCut storyboard gate, and release repository first, then the same hosted plugin with its private overlay. The full upstream suite is excluded from installation under this profile; this restriction supersedes the generic extension-install convention for this source. No unrelated development is reopened.

### Supplemental creative knowledge, 2026-10-21

The owner requests applying the two reviewed articles as [supplemental knowledge](creative-knowledge-2026-10-21.md). Connect source-bound data storytelling, revision-bound feedback and calibrated creative judgment to the existing owners. Extend current ideation and scoped preference rules rather than adding a parallel workflow. This bounded knowledge release preserves FrameCut onboarding, complete visual boards, correction/acceptance, optional requested samples and final delivery. Native dashboard services and collaborative comment interfaces are not implied by the knowledge.

### Concat-inspired FrameCut development, 2026-10-21

The owner explicitly reopened development to implement all six recommended functional areas from the Concat review inside the existing FrameCut workflow. The [bounded implementation scope](framecut/concat-development-scope.md) preserves original code, current owners and the complete storyboard-review gate. Native composition stills and multi-page boards, precise transactional edits, durable jobs, keyframes and format-specific framing, freeze/variable speed and versioned effects extend the current runtime. No Concat AGPL source is incorporated. The desktop editor, Rust/GPU rewrite and optional model-backed effects remain outside this request. Source-guided exercises and decoded-media checks precede repository publication and the guarded existing-plugin update; fresh-client behavior requires separate evidence.

### Owner testing pause and Claude Code handover, 2026-10-21

Development is paused at 1.115.0 while the owner tests FrameCut, Motion Graphics and other modules. The [2026-10-21 handover](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/8a8c78c8b15be8934b32c49c88c30413f185c387/docs/handover-chatgpt-work-2026-10-21.md) consolidates ChatGPT Work's work since 2026-10-20, the current source and saved-plugin state, executed checks and remaining real-client coverage. It supersedes older instructions to continue the audit or build the Reel Editing Assistant: those authorized tasks have been completed within their recorded scope. Do not start another feature round from this historical roadmap. The next implementation should respond to the owner's actual findings or a new explicit request. This handover changes repository documentation only; no plugin update or release is needed.

### FrameCut foundation, owner request 2026-10-20

The owner opened a development direction for **FrameCut**, a separate selectable welcome mode covering adaptive intake, footage/content analysis, traditional editing, motion, sound and final delivery. Highlights from a talking-head video are one example, not its full scope. The [research and implementation foundation](framecut/README.md) records 31 GitHub candidates, source pins, component decisions, timing/revision contracts and acceptance gates. Research and the executable v1 module now ship in **1.113.0**. The [build report](framecut/build-status.md) distinguishes working sandbox media paths, agent tests, remaining advanced capabilities and fresh-client checks.

Ownership is implemented through the existing `opencut-video-studio` ID, displayed as FrameCut, with Caption Studio, Motion Graphics Workflow and Audio Production Director as specialists. The native FFmpeg adapter follows a bounded Kinocut comparison. The common revision/timing model supports speech highlights, product montages, screen recordings and motion-only work. FrameCut is option 5; existing options 1–4 and complete localized startup remain intact. Preserve the private hosted overlay. The 59-component installer inventory remains the installation authority; research candidates are not automatic dependencies. Current AGENTS.md supersedes the old Reel Editing Assistant work order.

### Owner-directed maintenance, 2026-10-20

ChatGPT Work continues repository development and actual sandbox testing while Claude Code is unavailable. Work directly on `main`, with no working branches, and publish verified changes together with a guarded update of the existing hosted plugin. The separate integrations thread owns permanent tool connections. Preserve its current private overlay, report public and hosted versions separately, and keep private integrations out of the public repository. Record measured failures, fixes and remaining coverage gaps; source validation is not proof of fresh-host behavior.

Written 2026-10-16 by Cloud Code (change CC-20261016-04) at the owner's request, for Codex and ChatGPT Work: which way to develop Studio, what Cloud Code did from 1.70.0 to 1.87.0, and why. Read it after `AGENTS.md` and before the ledger. `AGENTS.md` and the owner's newest decision win over anything here; when one changes, update this file in the same change.

### Owner-directed update, 2026-10-17 (1.88.0)

The owner explicitly requested the full reusable resources from Logo Design Skill and the complete SVG/WebGL/3D Anatomy toolset inside Studio. This authorizes the bounded addition of their engines, technical references, templates and source examples; use examples to study APIs and craft, not as preselected client ideas. The existing static and motion owners remain responsible. Both originals are also optional pinned extensions, installed only on a separate request. Trademark SVGs excluded from upstream MIT are not republished; the logo catalogue and verified local-corpus connection retain reference functionality.

The owner also explicitly requested paired GitHub, hosted-plugin and Codex updates with PoYo preserved. Record saved-package/cache equality separately from fresh-client behavior; 1.87.1 already has that readback evidence. This supersedes the historical not-tracked/not-run distribution status below, not the requirement to test behavior honestly.

### 1. Where Studio stands (1.87.0)

- **A complete working tool in maintenance mode.** Change the package only for a trigger: a defect seen in real use or in a host evaluation, a host, model or generator change, a stale dated fact, or an explicit owner request. Name the trigger in the commit and the ledger and show the case before and after.
- **A general product.** Nothing is tuned to the owner's own rates, tools, clients or photos; what is user-specific is an input at run time. An example the owner shows is studied for its method, never written into the package (owner, 2026-10-15: "extract the essence, not the single example").
- **Motion graphics is the main paid use.** Client reels and Meta ads, built as HyperFrames compositions in Claude Code and, since 1.79.0, in a ChatGPT Work session that has Node.js, FFmpeg, Chromium and npm. Studio keeps the brief, the idea, copy locks, the board plan and the review.
- **A base for a person who chooses and directs.** Studio offers choices, recommends one with a reason, and never decides silently for the user (engines, extensions, directions).

Owner clarification, 2026-10-21: FrameCut follows onboarding and consequential questions, a complete visual storyboard/contact sheets of the entire film, user feedback and corrected-board acceptance, then final rendering and review. Samples are optional on request. This owner-requested correction replaces the 1.114.0 sample-first guidance; shared repository publication precedes the guarded existing-plugin update.

### 2. Direction, in order of value

1. **Fix what real use shows.** Owner reports and host evaluations come first. Reproduce the defect, fix it in the text the model reads (the owning `SKILL.md`, then its reference), add a regression test or host case, and record before and after.
2. **Motion graphics quality.** Continue `https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/8a8c78c8b15be8934b32c49c88c30413f185c387/docs/handover-motion-1.70.md` only when the owner asks: a recorded client reel through the HyperFrames route, starter compositions for the app-or-product and offer jobs (local service done in 1.89.0), lyric timing on a Polish song (an English CC BY-SA song ran in 1.90.1), motion activity inside `acceptance.py`. Open since 1.85.0: run the [web motion probe](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/web-motion-probe/README.md) on a live public site (the Cloud Code container could not reach one).
3. **Recommended extensions.** Every repository the owner sends is reviewed, adapted where it fits, and added to the [registry](../plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.json) by [the maintainer guide](extension-registry.md). Nothing in it has yet been installed into a real host: the highest-value next evidence is one real install per kind (REA in Codex or Claude Code, VoxCPM2 on a GPU machine, Voicebox with its MCP server), recorded in each entry's `observed`.
4. **Evidence in the hosts users actually use.** ChatGPT Work is `not_tracked` (the owner tests and reports); Codex has not run any of 1.77.0 to 1.87.0 (`Codex-Sync: not_run`). A Codex surface adds the most by running the host-eval cases and the extension installs in a real Codex session and recording the results.
5. **Creative quality, measured honestly.** The creative suite passes 7 of 11; the remaining failures are category motifs in two of three directions, a limit known since 1.66. Do not tune the instructions to the suite; a change needs a real defect, and the rubric judge stays advisory.

Not the direction: new skills, ready-made ideas, scenario or category lists, personal defaults, deleting or moving package paths, or growing a reference without a trigger. An idea without a trigger goes to the owner as a one-line note.

### 3. What Cloud Code did, and why

| Version | Change | Why (trigger) |
|---|---|---|
| 1.70.0 to 1.73.0 | HyperFrames as the default for client reels in Claude Code, the reel board system, motion activity check, lyric timing, technique atlas, print-ready PDF, HTML capture without npm | Owner-opened motion round (2026-10-12) and the owner's client sessions |
| 1.74.0 to 1.77.0 | One creative menu; handoffs to the owning skill; no invented claims; files stay in the project; fixes from the owner's evaluation and an external review | Defects reproduced from audits and evaluations |
| 1.78.0 | No page chrome in motion (corner labels, counters, kicker lines) | Owner decision after reviewing motionmaxxing |
| 1.79.0 | HyperFrames installable in a ChatGPT Work session | Owner test: the sandbox ran it while Studio said it could not |
| 1.80.0 | Generated cut-out assets and `asset_check.py` | A production session (lyric video from Gemini assets) |
| 1.81.0 | Eighteen fixes from the owner's technical audit, each with a regression test; no-code route first | Owner's technical audit of 1.80.0 |
| 1.82.0 | Directions that argue differently, brand versus category, effects must earn their place; the eval can no longer be passed by a template | Owner's creativity audit of 1.81.0 |
| 1.83.0 to 1.84.1 | Reconstructing an image in a prompt (model image vs REF, mechanism first, space as relations, measured colours); `image_probe.py --analyze` with accents, black and white points, focus and light maps, sRGB conversion; optics, focus and gaze per figure | Owner's reverse-engineering project knowledge; a host case on his mirror portrait where Studio misread the reflection and the focus |
| 1.85.0 | Web motion probe; recommended-extension registry with REA | Owner request to review morluto/rea and offer native installs |
| 1.86.0, 1.86.1 | Animate, Motion Designer and Meta Ads Designer as pinned extensions; probe cleanup fix | Owner request; CI failure of the 1.86.0 release |
| 1.87.0 | The user chooses a local voice engine (Voicebox, OmniVoice, VoxCPM2, MOSS-TTS, MOSS-TTSD), with a comparison and a recommendation when they do not know | Owner request |

The pattern behind these: reproduce first, change the smallest text the model reads, add a test that fails on the old behaviour, run a host case when behaviour is the point, report what was not run. Details and evidence are in `CHANGELOG.md`, `docs/reviews/` and the ledger.

### 4. Open items with a known trigger

- OmniVoice weights' licence (reported non-commercial) is unverified; Hugging Face was unreachable from the container. Check the model card and update the registry entry and the voice-engine guide.
- Motion Designer cannot install in Codex: its `SKILL.md` front matter does not parse at the reviewed commit. Recheck when upstream changes.
- G09: for a static page Studio read the animation from the source without loading a skill. The probe's value is on script-driven sites; run it there before changing routing.
- Image reconstruction has one real-photo case; the owner's own template (PRISM) filled by Studio has not been tested.
- Skill descriptions are at about 7,773 of 7,800 characters; measure before editing any description.
- FrameCut audit (2026-10-22): the owner decided the board stays a one-time host-managed preview and music ducks lightly under speech by default (1.119.3); per-deliverable caption settings, render speed, per-sequence delivery fingerprints and the receipt's sound blindness still wait. See [the audit](framecut/audit-2026-10-22.md).

### 5. Notes per surface

- **Codex.** A shell host: run `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs` and `bash scripts/check_all.sh` before every push; you can try extension installs for real (record `observed`) and run the motion routes end to end. Releases use `scripts/release.py prepare` then `publish`; never force-push, never delete a package path.
- **ChatGPT Work.** Plugin Creator updates the hosted copy from a pinned commit (`CHATGPT_UPDATE.md`); it only adds and overwrites files. The sandbox runs Python and, when the check finds them, HyperFrames for the session; it cannot run local MCP servers or GPU voice engines. Report findings from real use with the reply, the host and the version, so another surface can reproduce them.
- **All surfaces.** Read the ledger and Git history first, record the baseline SHA, add a ledger entry per change, write `synchronized` only with readback evidence, and keep this roadmap current when the direction changes.

## Owner handover continuation, 2026-10-24

The authorized continuation applies the [28 audited repairs and four reference workflows](audit-repairs-and-handover-2026-10-24.md), preserving 37 owners after bounded mixed-routing measurement. Hallmark is an optional complete native design companion with narrow Studio routing. The [full naming list and five future companion plans](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/8a8c78c8b15be8934b32c49c88c30413f185c387/docs/handover-development-proposals-2026-10-24.md) are ready for owner selection; none is auto-installed or renamed by this proposal.
