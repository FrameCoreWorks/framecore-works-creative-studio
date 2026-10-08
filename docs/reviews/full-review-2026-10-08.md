# Full review: plugin, orchestration, skills and repository

Date: 2026-10-08. Change ID: `CC-20261008-10` (origin: cloud-code). Plan: [full review plan](../full-review-plan-2026-10-08.md). Owner instruction: run every phase in one session and fix nothing before this report ("1a 2b start review"). **No file in the plugin or the tools was changed by this review.**

## 1. Baseline and method

| Item | Value |
| --- | --- |
| Source | Fresh clone of `main` at `0a6036ce98a7f0f03f43abae7263c9eca8292c5b` (package 1.38.0) |
| Tracked files | 1168 in the repository, 908 in the shared package, 37 skill IDs, 429 vendored `upstream/` files |
| Release compared | GitHub release `v1.38.0`: plugin ZIP, inventory and `SHA256SUMS` |
| Tools | Node 22, Python 3.13 with numpy, Pillow and ffmpeg, Chromium 1194 (headless), GEPA pilot in a separate virtual environment |
| Not done | No host test, no hosted plugin read or update, no paid call, no upload. Host behavior stays `NOT_RUN` unless the owner reported it earlier. |

Evidence types: `EXECUTED_CHECK` (reproduced by running something here), `OBSERVED_SOURCE` (read at the named file and line), `INFERENCE` (reasoned from the instructions, not observed in a host). Severity: `critical` (breaks startup, installation, publication or trust), `high` (wrong result or false pass that users meet), `medium` (gap, drift, maintainability), `low` (polish). Paths below are relative to `plugins/framecore-work-creative-studio/` unless they start at the repository root (`scripts/`, `.github/`, `verification/`, `docs/`).

## 2. Summary

No critical finding. Three high, sixteen medium, twenty-four low and six informational findings. The source checks, the release parity and the security scan are clean. The weak points cluster in five themes:

1. **The motion and sound engine is an island.** Studio's only end-to-end executable media path (contract, Python renderer, craft critique, designed sound, MP4) grew inside `hyperframes-workflow` from 1.24 to 1.38, but the orchestrator's main route table, the role and route contracts, the QA modality map, the audio owner and the Codex entry still describe the earlier planning-only state. A generic "make a promo video" request never reaches it, the audio owner says Studio has no media engine, and an MP4 is sent for review to the generative-video owner (F-ORCH-01, F-SKL-04, F-ORCH-07, F-SKL-09, F-INST-01).
2. **Checks that can pass without checking.** The sound timing check passes when it could judge no cue (F-TOOL-04), the preview checker passes a file the browser cannot open (F-TOOL-01), and three tools use three different reading-time rules (F-TOOL-02). The same class of problem was fixed for the critique in 1.37.0.
3. **CI proves less than it appears to.** The checks and release workflows have no numpy, Pillow or ffmpeg, so the renderer, critique and sound tests are skipped there (F-CI-01); the release-notes refresh silently does nothing since 1.8.x (F-CI-03); the legacy suite fails by design with no baseline (F-TEST-01); none of the 220 planned behavior cases has been executed (F-TEST-03) and almost none covers motion or sound (F-EVAL-01).
4. **Instruction quality and discovery.** Nine kit-derived skills have generic descriptions without boundaries, the 37 descriptions total 10,400 characters against Codex's 8,000-character listing budget when the context size is unknown (F-PKG-05), six skills are thin single files (F-SKL-02), caption work has no readability defaults (F-SKL-07), and several files give two answers to the same question (F-ORCH-05, F-ORCH-08, F-SKL-09).
5. **Records drift.** A Change ID used for two different changes, four changes without ledger entries, a stale version in `RELEASE_STATUS.md` and one private path in a repository record (F-REC-01 to F-REC-03, F-REPO-01).

## 3. Statuses

| Area | Status | Evidence |
| --- | --- | --- |
| Source checks | **PASS** | `scripts/check_all.sh` exit 0 in 5 min 10 s: Node 191 tests, 188 pass, 3 browser tests skipped, 0 fail; installer 12, identity 4, benchmark script 5, GEPA 8 (3 skipped without the venv; 8 pass in the venv), asset 23. Browser-run motion tests 61/61. Canonical validator PASS, 0 errors, 1 warning (scope note). Numbers equal `RELEASE_STATUS.md`. |
| Legacy suite | **FAIL by design** | `validate-studio.mjs --legacy`: 134 errors; `package.test.mjs`: 47/67 pass, 20 fail. Classified in §6.1; no error points to a current regression. |
| CI | **PASS, partial coverage** | Checks and release workflows green for 1.38.0, but the CI log shows 15 skipped tests against 3 locally (F-CI-01). |
| Release parity | **PASS** | `v1.38.0` plugin ZIP: 908 of 908 files byte-identical to the tag tree; `SHA256SUMS` match. Version markers (both manifests, `config/install-sources.json`, root and plugin READMEs, migration status) all say 1.38.0. |
| Security and hygiene | **PASS with one low finding** | No secret patterns (AWS, GitHub, OpenAI, Slack, Google keys, private keys) in tracked files; one synthetic test address; one private path (F-REPO-01). Hosted player: contract text drawn with `textContent`, review report in a JSON script element, no `innerHTML` or `eval`; no script injection found. |
| Renderer parity | **PASS** | Python renderer against the browser scene engine on all four examples, 137 review frames (§6.2). |
| Instruction trace | **Mixed** | 13 eval cases and 2 probes traced: 8 with one clear answer, 3 with two answers, 1 with no answer (§6.3). This is reading, not host behavior. |
| Host behavior | **NOT_RUN in this review** | Earlier owner reports stay as recorded: menus as tappable cards in ordinary ChatGPT (1.35.0, PASS_REPORTED), browser MP4 export on an Android phone (1.20.0, PASS_REPORTED), sound steps 1 to 3 approved by ear (1.33.0), the 1.38.0 music ending approved by ear, app-film renders approved (1.30.0). |

## 4. Findings

### 4.1 High

**F-ORCH-01. No route chooses between generative video and coded motion graphics.** `OBSERVED_SOURCE`, trace `INFERENCE`.
- Where: `skills/workflow-orchestrator/SKILL.md:114-134` (main route table, no motion row; the motion row is only in the second table at :165, "Motion graphics from code, runtime undecided..."); `skills/workflow-orchestrator/references/routing-boundaries.md`, `references/product-film-end-to-end-route.md` and `skills/commercial-video-campaign-director/SKILL.md` never mention motion graphics; `skills/ecommerce-campaign-strategy-director/SKILL.md:77` sends "motion direction" to the commercial video director.
- Reproduction: trace "Make a 15-second promo video for my app" through the orchestrator. Row :118 ("Open commercial brand/product/service video campaign") wins; the result is a direction and prompts for an external generator. `hyperframes-workflow/references/product-films.md` (the `device` scene kind built for exactly this, with the user's screenshots) is reached only when the user names motion graphics or picks area 8.
- Effect: Studio's one capability that delivers a finished MP4 with designed sound inside the conversation is invisible to most video requests.
- Fix: one routing rule in `routing-boundaries.md` and a row in the main table: when a video could be generated or built from code (text, logos, UI screenshots, data, product shots on flat backgrounds), offer both routes in one short choice; footage-like realism stays generative. Mention coded motion in the product-film route and in the commercial video director's scope. Add evals (F-EVAL-01).

**F-SKL-04. The audio owner does not know the sound engine exists.** `OBSERVED_SOURCE`.
- Where: `skills/workflow-orchestrator/SKILL.md:110` "Audio Production Director has no bundled media engine or provider integration"; `skills/audio-production-director/SKILL.md:10` "it is not a music-generation connector ... or an automatic audio analyser"; no link to `hyperframes-workflow/assets/motion-sound/` anywhere in `skills/audio-production-director/`.
- Effect: a user who asks the audio owner for music or effects for a motion video gets a text packet for an external tool, while Studio can design the effects, compose the bed, mix to -14 LUFS and mux the MP4 itself (owner-approved by ear since 1.33).
- Fix: state the engine's scope in both places (videos with a motion contract, a host with code execution, numpy and ffmpeg) and route motion-video sound to `motion-sound/sound.py`; keep songs, lyrics, voice and external tools with the audio owner.

**F-CI-01. CI skips the renderer, critique and sound tests.** `EXECUTED_CHECK` (CI log of job 113306407999 and local run).
- Where: `.github/workflows/checks.yml`, `.github/workflows/release.yml` (no numpy, Pillow or ffmpeg installed; `release.yml` has `timeout-minutes: 8`).
- Reproduction: the CI log reports 191 Node tests with 15 skipped; locally, with the dependencies, 3 are skipped (the browser tests).
- Effect: a green check says nothing about the most complex code (Python renderer, critique, sound plan, mix and check, video critique). The release gate uses the same script.
- Fix: install pinned numpy and Pillow and the distribution ffmpeg in both workflows; raise the release timeout (the local run takes about 5 minutes with these tests); optionally a Chromium job for the 3 browser tests.

### 4.2 Medium

**F-ORCH-07. Role and route contracts describe the motion engine as a planner.** `OBSERVED_SOURCE`.
- Where: `skills/pipeline-core/references/agent-roster.md` ("hyperframes-producer | Plans coded-video composition workflow | HyperFrames Production Brief"); `scripts/workflow-kit-routes.json` `qa_by_modality` (still, video to `video-prompt-architect`, audio, captions; no rendered-motion entry); `skills/pipeline-core/references/role-skill-map.md:114` ("video motion to Video Prompt Architect"); `skills/output-critic-iteration/SKILL.md` first paragraph (any MP4 to `video-prompt-architect`). No handoff `workflow-orchestrator -> hyperframes-producer`, `hyperframes-producer -> qa-iteration` or between `audio-production` and `hyperframes-producer`; the `motion-direction` role maps only to the commercial video, creative video, cinematography and storytelling skills.
- Effect: a host following the contracts reviews a rendered motion MP4 with the generative-video owner instead of `critique.py`.
- Fix: add a `motion` modality (rendered MP4 with a contract -> `hyperframes-workflow` critique), the missing handoffs, and "rendered MP4 and contract" as the roster artifact; keep `validate-workflow-kit.mjs` in sync.

**F-SKL-09. The motion skill gives two answers for sound, inside one overloaded paragraph.** `OBSERVED_SOURCE`.
- Where: `skills/hyperframes-workflow/SKILL.md:25` (Studio designs effects and composes the bed with `motion-sound/sound.py`) and `:35` (owners table: "Music, sound design or voice -> Audio Production Director"). Line 25 is 2,138 characters and carries the render, critique, delivery, player, sound and revision rules; the next longest line in any `SKILL.md` is 973.
- Fix: split line 25 into a short numbered delivery list; change the table row to "Sound for this video: motion-sound (this skill); songs, lyrics, voice and external audio tools: Audio Production Director".

**F-INST-01. The Codex entry says seven work areas; the menu has eight.** `OBSERVED_SOURCE`.
- Where: `scripts/install_codex.py:103` "a pace-only choice shows the seven work areas". Area 8 (motion graphics) exists since 2026-10-04 (`dd785f4`, `1d089ce`); the wrapper text is unchanged since 1.2.2 (`f5099c8`, 2026-09-30). `tests/test_codex_install.py` does not check the count.
- Effect: the native Codex entry is read before the orchestrator, so Codex gets two answers and may drop area 8.
- Fix: refer to "the work-area menu" without a number; add a test that the wrapper never states a different count than `startup-and-creative-menus.md`.

**F-TOOL-04. The sound timing check passes when it judged nothing.** `EXECUTED_CHECK`.
- Reproduction (fresh clone, 36 s): render `color-block`, `sound.py plan`, `mix --stems stems`, then `python3 sound.py check stems/effects.wav color-block-r2.motion.json` prints `{"cues": 8, "judged": 0, "missing": 0, "max_offset_ms": 0.0, "all_ok": true}` and exits 0. The mix's own `timing_check` judged 1 of 8. All other cues are "masked" (two cues on one frame; landings 133 ms apart measured as swell peaks), and masked cues count as ok.
- Effect: the README is literally accurate ("masked ... reported, not judged"), but a host model reading exit 0 can report "sound timing verified". The README's boundary sentence "every judged hit landed within 2 ms" rests on one hit for this example.
- Fix: return a status (`checked`, `partly_judged`, `not_judged`) as the critique does since 1.37.0 and flag `judged < cues`; better, judge each cue in a solo render (the engine renders any cue from its recipe deterministically), which removes masking.

**F-ORCH-05. The QA budget is bounded in one place and unbounded in another.** `OBSERVED_SOURCE`.
- Where: `skills/hyperframes-workflow/assets/motion-review/README.md:60` "Repeat until no error remains" and `assets/single-file-preview/README.md:32` "run it again until no error remains", against `skills/pipeline-core/references/loop-protocol.md:78` (initial review plus at most two repair passes), `references/motion-quality-direction.md:50` and `references/code-based-motion-graphics.md:73`.
- Fix: keep the mandatory improvement round inside the shared budget; after the second repair, stop and report the remaining errors.

**F-ORCH-02. Capability messaging lags the product.** `OBSERVED_SOURCE`. Owner decision (protected welcome).
- Where: the welcome sound bullet ("musical concepts, lyrics and instructions for audio tools, and planning sound design") and the area 6 and 8 texts ("preview and export depend on available tools") omit that Studio designs and mixes sound and renders a finished MP4 where code execution exists. The root `README.md` "What it includes" omits sound design, the craft critique, the MP4 renderer and interactive presentation.
- Fix: README now; welcome and menu wording only with the owner's approval, keeping all six bullets, structure and tokens.

**F-PKG-01. Three music-video references are never loaded.** `EXECUTED_CHECK` (link graph).
- Where: `skills/creative-music-video-director/references/direction-method.md` (5,938 B), `persona-performance-motifs.md` (4,550 B), `rhythm-references-handoff.md` (6,762 B); `SKILL.md` links only `rhythm-motifs-and-performance-workbook.md`, and nothing else links them.
- Fix: link each from the step where it applies, or replace with a pointer stub if superseded (paths kept).

**F-PKG-04. The package is 14.19 MB, mostly fixed weight.** `EXECUTED_CHECK`.
- Largest files: `integrations/workflow-kit/workflow-kit-55c8bf1-source.tar.gz` 3.06 MB (duplicates the 429-file upstream mirror), `integrations/workflow-kit/upstream/.github/assets/readme-banner.png` 2.38 MB, `assets/logo.png` 1.60 MB, `upstream/.github/assets/social-preview.jpg` 0.22 MB; 50 groups of byte-identical files.
- Constraint: hosted updates cannot delete paths, vendored snapshots stay byte-identical, the logo is protected. Owner decision: accept the size, or allow a lossless recompression of the logo bytes and a provenance-preserving stub for the archive (its hash is recorded in the source manifest).

**F-PKG-05. Skill descriptions overlap and exceed Codex's listing budget.** `OBSERVED_SOURCE` and official source fetched 2026-10-08 (also logged as F-CUR-01).
- Where: nine kit-derived skills start with a generic "Use this skill to/for ..." and name no neighbor: `asset-manifest`, `caption-studio`, `character-design`, `cinematography`, `reference-pack-curator`, `ugc`, `opencut-video-studio`, `remotion-video-production`, `creative-video-producer`. "UGC" appears in five descriptions, captions in `copy-voice` and `caption-studio`, shot language in three. The 37 descriptions total 10,400 characters (mean 281, max 428).
- Source: [Build skills](https://learn.chatgpt.com/docs/build-skills) (the former `developers.openai.com/codex/skills` now redirects there; the page has no date): "front-load the key use case and trigger words, so a host can still match the skill if descriptions are shortened"; Codex's initial skill list uses "at most 2% of the model's context window, or 8,000 characters when the context window is unknown", shortening descriptions first and then omitting skills.
- Fix: rewrite the nine descriptions with the trigger first and one boundary ("not for X; use Y"), bringing the total under 8,000 characters. Metadata validation stays in force. The native Codex install exposes one wrapper entry and is not affected.

**F-SKL-01. Pipeline Core keeps a stale motion rule and kit installation text.** `OBSERVED_SOURCE`.
- Where: `skills/pipeline-core/SKILL.md:129` (coded video only "when the requested runtime is specifically HyperFrames or HTML/GSAP"), `:13` ("the workflow system from this kit"), `:34` (`$skill-installer`, `.framecore/manifest.json`), `:193` ("First move confirms intent before specialist work", against the no-ritual-approval rule).
- Fix: route general motion graphics with an undecided runtime to the Motion Graphics Workflow; replace the kit installation lines with Studio's actual install routes; align `:193` with the integration policy.

**F-SKL-02. Six skills are a single thin file.** `OBSERVED_SOURCE` (opportunity).
- `brief-architect`, `cinematography`, `marketing`, `storytelling`, `ugc`, `instruction-packet-factory`: one `SKILL.md` of about 5 KB, no reference, template or example. `cinematography` does not link `video-prompt-architect/references/video-craft.md`, which holds the shot, lens, light and movement vocabulary. `ugc` has the honesty rules (no fake testimonials) but no hook and format structures (demo, unboxing, problem-solution), platform specifications or advertising disclosure rules. `storytelling` has no short-form structures.
- Fix: link existing material first (cinematography to video craft), then add one sourced reference each for `ugc` and `storytelling`.

**F-SKL-07. Captions have no readability defaults.** `OBSERVED_SOURCE`.
- Where: `skills/caption-studio/SKILL.md:63` ("Set line count, words per beat, reading speed ...") gives no values; `templates/caption-task-pack.md` is a 425-byte skeleton. The only heuristic (about 13 characters per second plus 0.5 s) lives in `hyperframes-workflow/references/motion-craft.md:50` and is not linked.
- Fix: a dated, sourced reference with defaults for subtitles and social captions (characters per line, lines, reading speed, minimum and maximum duration, gaps, platform safe zones, SRT and VTT format rules), with language notes.

**F-CI-03. The release-notes refresh has silently done nothing since 1.8.x.** `EXECUTED_CHECK`.
- Where: `.github/workflows/refresh-release-notes.yml:32-35` reads `publication.source_commit` from `verification/release-<version>.json` and exits 0 with "description refresh skipped" when it is absent. 44 release records lack it, including every release after 1.8.0.
- Effect: edits to `RELEASE_NOTES.md` after a release never reach the GitHub release text, with a green run.
- Fix: read the commit from `verification/github-publication-<version>.json` or from the tag, and fail when neither exists.

**F-TEST-01. The legacy suite fails by design and has no baseline.** `EXECUTED_CHECK`.
- 134 validator errors and 20 failing tests are reported as numbers only (§6.1), and the CI legacy job runs with `continue-on-error`. A new legacy regression would hide among them.
- Fix (owner decision): store the expected error strings and failing test names in a repository-only file and fail on any difference, or retire the suite as historical and stop running it.

**F-TEST-03. No planned behavior case has ever been executed.** `EXECUTED_CHECK`.
- `validate-studio.mjs` reports 201 planned cases (plus 19 presentation cases) and `executed: 0`. Most instruction rules are guarded by text-presence checks (`validate-studio.mjs` 29 `includes` and 25 regex checks, `validate-workflow-kit.mjs` 25 and 12, `validate-presentation.mjs` 9 and 3), which prove that a sentence exists, not that a host follows it. Host evidence exists only as owner reports.
- Fix: a 6 to 8 case smoke set per larger release (startup EN and PL, direct task, motion route, sound route, interactive offer, research unavailable), run by the owner or a Codex CLI session and recorded with the existing host-report schema.

**F-EVAL-01. Behavior evals barely cover motion and sound.** `OBSERVED_SOURCE`.
- Only PI03, PI04, PI06, PI09 (presentation) and WK07 (Remotion against coded HTML) name `hyperframes-workflow`. No case covers the generative-against-coded route choice, rendering an MP4 in a code-execution host, the critique improvement round, sound for a motion video ("no toy tones", ask once), or a contract revision.
- Fix: add five cases with these checks to the existing schema.

### 4.3 Low

| ID | Evidence | Where | Finding | Fix |
| --- | --- | --- | --- | --- |
| F-TOOL-01 | EXECUTED_CHECK | `skills/hyperframes-workflow/assets/motion-review/review-frames.mjs` `previewFor()`; `assets/single-file-preview/check-preview.mjs`; README step 7 | Contract JSON is embedded in `<script type="application/json">` without escaping `<`. Copy text `eksportu </script><h1 id="injected">INJECTED</h1>`: `check-score` PASS, `check-preview` 0 errors, but in Chromium the player never becomes ready and the `<h1>` lands in the page (an `onerror` handler would run in the delivered file). Rare trigger, false pass in the checker. | Escape `<` as `<` when embedding; make `check-preview` fail on `</script` or `<!--` inside the block. |
| F-TOOL-02 | OBSERVED_SOURCE | `gsap-motion-starter/check-score.mjs:55`, `motion-review/critique.py:175`, `references/motion-craft.md:50` | Three reading-time rules: characters/13 + 0.5 s; words/3 + 0.4 s; the longer of characters/13 + 0.5 s and 0.5 s + words/3. "Gotowe do eksportu" needs 1.88 s, 1.40 s and 1.88 s; a 1.5 s hold passes the critique and warns in `check-score`. | One shared rule (the reference's) in both tools. |
| F-TOOL-03 | EXECUTED_CHECK | `assets/motion-render/render.py` | An SVG logo needs `cairosvg` (the all-kinds example exits 2 with a clear message). Whether ChatGPT code execution has it is Unknown; brand marks often arrive as SVG. | Ask for a PNG up front in hosts without a shell. |
| F-ORCH-03 | OBSERVED_SOURCE | `video-prompt-architect/SKILL.md:23`, `workflow-orchestrator/SKILL.md:110`, `references/routing-boundaries.md:17` | Development status in runtime text: "The full Visual Prompter remains in development"; "unsupported module in this preview". | State what is packaged, not internal plans. |
| F-ORCH-04 | OBSERVED_SOURCE | `workflow-orchestrator/references/startup-and-creative-menus.md:35`, root `README.md:13` | Says area 8 is reached via "Creative Mode, Expanded Mode"; the area menu follows either pace. | "after choosing a pace". |
| F-ORCH-06 | OBSERVED_SOURCE | `pipeline-core/references/presentation-and-interaction.md`, `workflow-orchestrator/assets/*template*` | The reply to an interactive-version offer is to be recorded "in the existing Project State", but no state template has a place for it; a decline is easily lost. | Name the place (`entry_context` note). |
| F-ORCH-08 | OBSERVED_SOURCE | `studio-workstyle-profile/SKILL.md:29` | Hardcodes "1. Tryb szybki / 2. Tryb rozbudowany" without "in the selected user language"; the menus reference requires the user's language. | Add the language clause. |
| F-PKG-02 | EXECUTED_CHECK | `workflow-orchestrator/references/thread-link-and-cross-host-resume.md` | Not linked; `capabilities-and-handoffs.md` repeats the rule inline. | Link or stub. |
| F-PKG-03 | EXECUTED_CHECK | `hipson-adapter/templates/{internet-mapping-packet,research-map}.md`, `workflow-self-improvement/templates/{change-proposal,improvement-log}.md`, `pipeline-core/templates/artifact-templates.md`, `research-evidence/references/initial-source-register.md` (6,927 B) | Unreachable from any skill or index. | Link where useful, otherwise stub. |
| F-SKL-03 | OBSERVED_SOURCE | `research-evidence` | A dated image-generator map exists (19 families, 2026-09-24); no video or music map. | See backlog IM4. |
| F-SKL-05 | OBSERVED_SOURCE | `tool-routing-cost/SKILL.md:57-58` | Process numbers step 6 twice. `hipson-adapter` duplicates the packet fields of `instruction-packet-factory` (explicit-only skill). | Renumber; point to one source. |
| F-SKL-06 | OBSERVED_SOURCE | `pipeline-core/references/role-skill-map.md`, `marketing/SKILL.md` | Role map intro still explains kit installation (`$skill-installer`, `.codex/agents/<role>.toml`, which Studio ships only as upstream templates). `marketing` puts the brand-identity paragraph inside "When To Use" before the list. | Trim; move the paragraph. |
| F-SKL-08 | OBSERVED_SOURCE | `producer-ai-task-builder/references/` | The alias keeps three unreachable references: one byte-identical to the audio owner's, two older variants. | Pointer stubs. |
| F-SKL-10 | OBSERVED_SOURCE | `creative-video-producer/SKILL.md`, `copy-voice/SKILL.md:32` | "Use HyperFrames skills when ..." (one skill exists and it chooses the runtime); teacher paragraph inside "## Inputs" before the list. | Reword; move. |
| F-LRN-01 | OBSERVED_SOURCE | `workflow-orchestrator/assets/learning-domains.json` | `editing_motion` has no easing, holds or staggers and does not use `motion-craft.md`; `audio_music` omits motion sound design. Learning cannot use rendered before and after examples where code execution exists. | Add topics and sources. |
| F-CI-02 | EXECUTED_CHECK | all workflows | `actions/checkout` pinned to a build that runs on Node 20 (deprecation warning, forced to Node 24). | Pin a current release SHA. |
| F-REPO-01 | OBSERVED_SOURCE | `verification/hosted-release-1.2.10.json:51` | Contains the owner's local path `/Volumes/Codex/CodexHome/...`. | Replace with a placeholder. |
| F-REC-01 | OBSERVED_SOURCE | `RELEASE_STATUS.md:13` | "Host behavior of 1.27.0 is not_run" while the source is 1.38.0. | Update. |
| F-REC-02 | EXECUTED_CHECK | Git history | `CC-20261008-03` marks both the 1.33.0 sound-test records (`436d28c`, `f77a923` and others) and the Intelligent UI change and 1.35.0 release (`7872bfd`, `ecf6ed0`, `fff1587`). | Note the collision in the ledger. |
| F-REC-03 | EXECUTED_CHECK | `docs/development-ledger.md` | No entry for `CC-20261008-01`, `-04`, `-05`, `-09`. | Add short entries. |
| F-DOC-01 | OBSERVED_SOURCE | `assets/motion-export/README.md` | Browser table omits the owner's Android report (H.264 MP4 exported and played, 2026-10-07, from a page that reproduced `video-export.mjs` in reformatted form). | Add the row with that qualification. |
| F-DOC-02 | OBSERVED_SOURCE | root `README.md:80-88` | "Verify and package" lists only `validate-studio.mjs`, not `scripts/check_all.sh`. | List the full check. |
| F-DOC-03 | OBSERVED_SOURCE | `CHATGPT_INSTALL.md` | Covers installation in ChatGPT Work only; says nothing about using the installed plugin in ordinary chat, where the owner's tests ran and native interactive elements appeared. | One sentence after installation. |
| F-TEST-02 | EXECUTED_CHECK | `tests/motion-toolkit.test.mjs:469` | Renderer parity is tested for kinds, easings and determinism only; pixel parity (§6.2) is not automated. | Add a tolerance test to the browser suite. |

### 4.4 Informational

| ID | Evidence | Finding |
| --- | --- | --- |
| F-RELEASE-OK | EXECUTED_CHECK | `v1.38.0` plugin ZIP identical to the tag tree, 908 of 908 files; checksums match. |
| F-TOOL-OK-01 | EXECUTED_CHECK | Renderer parity on all four examples (§6.2), including `color-block` and `app-film`, which the renderer README does not list. |
| F-TOOL-OK-02 | EXECUTED_CHECK | End to end from a fresh clone (`color-block`): H.264 1920 x 1080, 30 fps, 324 frames; AAC 48 kHz stereo muxed; `plan` refuses to overwrite a revision; critique on the delivered video `checked` (exit 0), without the video `incomplete` (exit 3). |
| F-REC-04 | EXECUTED_CHECK | 64 tags and 63 release records: `v1.0.0` and `v1.1.3` have no record; `release-1.0.json` and `release-preparation.json` have no tag. |
| F-CUR-02 | EXECUTED_CHECK | All nine cited `developers.openai.com` and `learn.chatgpt.com` plugin and skill pages answer 200. `help.openai.com` (including the Intelligent UI article cited by the presentation policy) is not reachable from this environment; a search found no indexed official page naming "Intelligent UI" and a community thread reporting that automatic cards stopped appearing for some users. Currency: Unknown. The policy's text-equivalence rule keeps Studio correct either way. |
| F-CUR-03 | INFERENCE (secondary sources) | No newer OpenAI image model than GPT Image 2.5 (in the 2026-09-24 snapshot); third-party reports date the `gpt-image-1` shutdown to 2026-10-23 and older GPT Image API removal to 2026-12-01 (Studio names none as current). Kling 4.0 unveiled 2026-09-30, rollout in October; Sora's standalone product retired (Studio mentions Sora only as historical input). Google Flow Music is the former ProducerAI ([9to5Google, 2026-04-20](https://9to5google.com/2026/04/20/producerai-becomes-google-flow-music/)); Studio's wording is current. |

## 5. Backlog

Value and effort are estimates (`INFERENCE`). Protected surfaces (welcome, menu order and tokens, technical IDs, released paths, vendored snapshots, approved sound and motion references) stay untouched unless a row says "owner decision".

### 5.1 Quick wins (each under an hour, low risk)

| # | Item | Findings | What changes for the user |
| --- | --- | --- | --- |
| QW1 | Codex entry without the area count, plus a test | F-INST-01 | Codex shows motion graphics in the menu. |
| QW2 | Sound check status and exit code when cues are not judged | F-TOOL-04 | No "timing verified" claim without a measurement. |
| QW3 | Escape `<` when embedding contracts; checker detects it | F-TOOL-01 | A preview with unusual copy opens instead of breaking. |
| QW4 | One QA budget wording in the two READMEs | F-ORCH-05 | No endless repair loop. |
| QW5 | Audio owner and orchestrator name the sound engine; motion owner table fixed | F-SKL-04 (instructions part), F-SKL-09 | Asking for music for a motion video gives a rendered track. |
| QW6 | Wording fixes | F-ORCH-03, F-ORCH-04, F-ORCH-08, F-SKL-05, F-SKL-06, F-SKL-10 | Fewer confusing or internal sentences. |
| QW7 | Workflow fixes | F-CI-02, F-CI-03 | Release notes edits reach GitHub; no deprecation warning. |
| QW8 | Records and docs | F-REC-01 to F-REC-03, F-DOC-01 to F-DOC-03, F-REPO-01 | Accurate status and install guidance. |
| QW9 | Link or stub the unreachable files | F-PKG-01 to F-PKG-03, F-SKL-08 | The music-video method is actually used. |

### 5.2 Fixes (half a day to a day)

| # | Item | Findings | Value | Effort | Risk |
| --- | --- | --- | --- | --- | --- |
| FX1 | CI installs numpy, Pillow and ffmpeg; release timeout raised; optional browser job | F-CI-01 | High | Low | Low |
| FX2 | Motion becomes a first-class route: routing rule and main-table row, product-film route, motion QA modality, handoffs, roster artifact, five evals | F-ORCH-01, F-ORCH-07, F-SKL-01, F-EVAL-01 | High | Medium | Medium (routing change; validators keep contracts consistent) |
| FX3 | Trigger-first descriptions with boundaries, total under 8,000 characters | F-PKG-05 | Medium | Low | Low |
| FX4 | One reading-time rule shared by `check-score` and the critique | F-TOOL-02 | Medium | Low | Low (example contracts may get new warnings) |
| FX5 | Legacy suite: stored baseline or retirement | F-TEST-01 | Medium | Low | Low (owner decision) |
| FX6 | Solo-render timing check for every cue | F-TOOL-04 | Medium | Medium | Low |

### 5.3 Improvements (one to three days)

| # | Item | Findings | Value | Effort | Risk |
| --- | --- | --- | --- | --- | --- |
| IM1 | Deepen thin skills: cinematography links video craft; sourced references for UGC (hooks, formats, platform specifications, disclosure) and short-form storytelling; caption readability defaults | F-SKL-02, F-SKL-07 | Medium to high | Medium | Low; sourced facts need dates and refresh |
| IM2 | Host smoke set per larger release, and one run of the existing blind motion benchmark (`scripts/motion_benchmark.py`, eight briefs, never run so far) | F-TEST-03 | High (trust) | Low code, owner time | Low |
| IM3 | Learning with rendered examples (easing, holds) where code execution exists; interactive quiz adaptation in the teacher profile | F-LRN-01 | Medium | Medium | Low |
| IM4 | Dated video and music generator starting maps like the image map | F-SKL-03 | Medium | Medium | Staleness; needs a refresh date |
| IM5 | Pixel-parity test with a tolerance in the browser suite | F-TEST-02 | Medium | Low | Low |

### 5.4 New modules (proposals for the owner)

| # | Module | Why | Value | Effort | Risk |
| --- | --- | --- | --- | --- | --- |
| NM1 | Sound for supplied footage: build a cue sheet from the user's cut list or a beat grid of the supplied video and render effects and a music bed with the existing engine | H21-type requests ("plan music and sounds for my 25 s reel") get a finished track, not only a text plan; today `sound.py` needs a motion contract | High | Medium to high | Medium (quality on unknown footage; owner listening test needed) |
| NM2 | Executable captions: SRT and VTT from transcript and timing, burned in by the existing renderer, reading-speed check | Captions are the most common short-form request; the renderer already draws captions | Medium to high | Medium | Low |
| NM3 | One machine-readable capability card (what Studio executes per host: render, sound, critique, export) read by the orchestrator, the welcome text and the role contracts | The root cause of theme 1 is that capability statements live in many files and drift | Medium | Medium | Low (protected welcome text changes only with approval) |

### 5.5 Owner decisions needed

1. **Welcome and menu wording** (F-ORCH-02): may the sound bullet and the area 6 and 8 texts say that Studio designs sound and renders MP4 where code execution exists?
2. **Generic video requests** (F-ORCH-01): offer both routes in one short choice, or pick by content type and say why?
3. **Package size** (F-PKG-04): accept, or allow lossless logo recompression and an archive stub?
4. **Legacy suite** (F-TEST-01): stored baseline or retirement?

## 6. Phase notes

### 6.1 Legacy suite classification

About 16 errors come from the mandatory-research policy that became conditional in 1.11.0; 35 are "Missing frontmatter" on the intentional upstream discovery stubs (`CC-20261006-04`); about 70 are fixture expectations tied to the old policy (`research_expectation`, S36 to S49, PA05); one is "Producer task preparation must have exactly one orchestrator route; found 0" (the retired alias). The 20 failing tests map to the same causes.

### 6.2 Renderer parity

Browser frames from `review-frames.mjs` (Chromium 1194, cropped to the stage) against `render.py --stills` at the same frames:

| Example | Frames | Mean difference per example (grey levels) | Worst frame | Pixels differing by more than 48 levels |
| --- | --- | --- | --- | --- |
| two-statements | 24 | 0.16 | 0.28 | at most 0.20% |
| color-block | 31 | 0.12 | 0.17 | at most 0.15% |
| app-film | 29 | 0.28 | 0.87 | at most 0.55% |
| all-kinds (PNG copy of its SVG mark) | 53 | 0.32 | 0.85 | at most 0.59% |

The differences are anti-aliasing at glyph and shape edges; layout and timing match.

### 6.3 Instruction trace

Sampled H21, H25, LM11, PI03, PI05, PI06, PI09, PI16, WK06, WK07, WK13, CM04 and KP12, plus two probes ("make a 15-second promo video for my app"; "add music and sound to the motion video you rendered").

- **One clear answer:** PI09 (no renderer: contract and player link, no invented MP4), PI06 (`revise.mjs extend` moves later scenes and sound cues), PI05 (expired choice group, one clarification), PI16 (full welcome in the user's language), WK13 (research triggered, no-browse receipt when offline), CM04 (no invented testimonial), KP12 (research conflict recorded), WK07 (one locked cut, two runtimes).
- **Two answers:** sound for a rendered motion video (F-SKL-04, F-SKL-09); review of a rendered MP4 (F-ORCH-07); pace menu language (F-ORCH-08).
- **No answer:** the promo-video probe (F-ORCH-01). H21 (a supplied external reel) has one correct answer today, a text plan, because the engine needs a motion contract (NM1).

### 6.4 Skill rubric notes

Strong and current: `research-evidence`, `video-prompt-architect` (named-generator research, no invented syntax), `screenplay-story-architect`, `storyboard-sequence-architect`, `storyboard-board-architect`, `commercial-video-campaign-director` (decision sequence and anti-generic gate), `ecommerce-campaign-strategy-director` (claim ledger, sourced numbers only), `remotion-video-production` (exact pins and lockfiles), the teacher profile. `static-graphic-design-creator` delegates to its pinned upstream method by design. Thin or drifting: see F-SKL-01, F-SKL-02, F-SKL-07, F-SKL-09.

### 6.5 Sources for the currency check (read 2026-10-08)

- [Build skills, learn.chatgpt.com](https://learn.chatgpt.com/docs/build-skills) (fetched; no date on the page).
- [ProducerAI becomes Google Flow Music, 9to5Google](https://9to5google.com/2026/04/20/producerai-becomes-google-flow-music/).
- [Community thread on lost automatic interactive UI](https://community.openai.com/t/has-anyone-else-lost-the-automatic-rich-interactive-ui/1401476) (undated user reports).
- Image and video model status from secondary coverage found by web search; treated as `INFERENCE` and not used for any fix without an official source.
