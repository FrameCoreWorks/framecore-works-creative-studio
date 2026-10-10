# Changelog

## 1.57.0, 2026-10-10

From Phase 2 of [the improvement plan](docs/improvement-plan-2026-10.md), the client business layer. Every rate, VAT status, term and right is the user's input; Studio holds no prices and personalises nothing (owner decision of 2026-10-10):

- **Offers priced from the user's rates.** [Client offer and quote](plugins/framecore-work-creative-studio/skills/brief-architect/references/client-offer-and-quote.md): packages that differ in outcome, revision rounds, timeline, rights in plain words (transfer or licence, fields of use), payment and validity; `quote_calc.py` computes net, VAT or a stated exemption, gross, discount and advance with decimal rounding and writes the offer in Polish or English; it refuses an hourly item without a rate, an exemption without its basis or an advance above 100 %
- **Client intake** in [Polish](plugins/framecore-work-creative-studio/skills/brief-architect/assets/client-intake.pl.md) and [English](plugins/framecore-work-creative-studio/skills/brief-architect/assets/client-intake.en.md), and commercial fields in the Brief Contract (decision maker, budget, deadline, rounds, use, rights, client materials, acceptance)
- **Concept presentation, revision tracker and changes of scope.** Two or three directions in context with a recommendation and a numbered decision; feedback consolidated and classed as a revision, our error (never counted) or a change of scope (quoted before work starts)
- **Client handoff.** Files grouped by use with sortable names, fonts and licences, a [handoff letter](plugins/framecore-work-creative-studio/skills/delivery-documentation/assets/handoff-letter.pl.md) with the agreed rights and a plain AI-assistance line, an [acceptance protocol](plugins/framecore-work-creative-studio/skills/delivery-documentation/assets/acceptance-protocol.pl.md) (protokół odbioru) and a case-study template that uses only the client's consent and figures
- **Brand kit.** One file per client (colours, fonts and licences, logo files, voice, approved and banned claims, legal lines) read by every owner; the static compositor accepts `brand:primary`, `brand:headline` and `brand:logo.white`; where to keep it in ChatGPT, Claude, Codex and Claude Code
- **Client email kit** (questions, offer, concepts, feedback summary, files, payment reminder, testimonial request), a **brand voice guide** template, and **KPIs and budget scenarios** in the campaign pack (client data or labelled assumptions, never invented benchmarks)
- [Client projects](plugins/framecore-work-creative-studio/skills/pipeline-core/references/client-projects.md) maps the path from enquiry to acceptance and which owner makes each document

## 1.56.0, 2026-10-10

From Phase 1 of [the improvement plan](docs/improvement-plan-2026-10.md) (static graphics and Polish quality) and the first host evaluation run:

- **Exact text for client finals.** A second route for visible text: a background without text (generated with reserved calm zones, supplied or flat) and the new [static compositor](plugins/framecore-work-creative-studio/skills/static-graphic-design-creator/assets/static-render/README.md), which sets every word, price, logo and legal line in a real font at the exact size, writes PNG, JPG and a print PDF with bleed and crop marks, stops instead of cropping a word or drawing a missing glyph, and measures contrast and safe areas. One-pass generation stays the default for concepts; [exact-copy compositing](plugins/framecore-work-creative-studio/skills/static-graphic-design-creator/references/exact-copy-compositing.md) is the default for finals with a price, date, logo, legal line or print files, always named to the user. The text policy and the rules that allowed only one pass now describe both routes
- **Bundled fonts.** Eighteen OFL fonts in six families (Inter, Archivo, Bricolage Grotesque, Fraunces, Anton, Source Serif 4) with the full Polish alphabet and typographic marks, built reproducibly by `scripts/build_fonts.py` from google/fonts `bd8f81d` ([fonts](plugins/framecore-work-creative-studio/skills/pipeline-core/assets/fonts/README.md))
- **Polish copy standard and checker.** Quotes, dashes, no-break spaces, money, dates, time, sentence-case headlines and one form of address ([standard](plugins/framecore-work-creative-studio/skills/copy-voice/references/polish-copy-standard.md)); `pl_copy_check.py` applies only typographic fixes and counts characters against dated channel limits; a Copy Pack template
- **Dated snapshots.** [Channel copy and format limits](plugins/framecore-work-creative-studio/skills/research-evidence/references/channel-specs-snapshot.md) (Google RSA confirmed; Meta, LinkedIn, TikTok, SEO and email from the best available sources, marked as such) and [Polish and EU marketing rules](plugins/framecore-work-creative-studio/skills/research-evidence/references/marketing-rules-snapshot.md) (Omnibus price reductions, paid-content labels, marketing consent under the PKE, AI Act art. 50 from 2 August 2026, green claims from 27 September 2026, health, alcohol and credit claims). Within 90 days each satisfies its research trigger in Quick mode. The claim ledger gains a rules column; Studio drafts compliant wording, counsel decides
- **Image probe.** Measures an actual raster against its placement or print size (ratio, effective ppi with bleed, transparency, sharpness, OCR against the locked copy when installed) and writes phone, thumbnail, greyscale and safe-area previews to look at
- **Format and print presets** and a **direct-production path**: a complete request for a finished graphic gets one direction and the output in one turn
- **Fewer questions.** After offering directions Studio asks one question, which direction, labelling each with its route; route and format come after the choice (found by the host evaluation, case S01)
- **Digit groups stay together** (`1 299 zł`) in the motion engine (all three copies), the Python renderer (1.4.1) and the compositor, with a parity test
- **Repository only.** `scripts/host_eval.py` runs Studio in headless Claude Code against a 15-case suite with deterministic checks and an optional advisory judge ([docs](docs/host-evals.md)); the first run on 1.55.0 passed 12 of 15 for USD 1.68 (one harness defect, one case not applicable without the Studio name, one product finding, all resolved and rerun)

## 1.55.0, 2026-10-10

From Phase 0 of [the improvement plan](docs/improvement-plan-2026-10.md), after the six-review audit of 1.54.0 (owner decisions 1a, 2a and 3a of 2026-10-10):

- **Text is never cropped silently.** The bundled Python renderer lays out every scene before drawing and stops with exit code 4 and `"status": "text_overflow"` when a word is wider than its column, naming the word, its width and the column; `--allow-overflow` keeps the old behaviour on request. A 200 px "Najnowocześniejszy" in a 9:16 column used to render as "Najnowo" ([renderer notes](plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-render/README.md))
- **Polish line breaks.** One-letter words (w, z, i, a, o, u) stay with the next word and numbers stay with their units (10 zł, 5 kg, 30 %), through a non-breaking space applied identically in the scene engine (all three copies) and the Python renderer; a test checks the two agree
- **Composition errors block acceptance.** Critique flags a vertical hold whose content fills less than 10 % of the frame (an error) or 25 % (a warning), once per scene and format; the thumbnail check runs for every feed format; URL text is no longer judged as readable copy. Acceptance now blocks on any critique picture error, not only on selected areas. The colour-block example's 9:16 layout was enlarged and scores 95
- **Sound mixing about 15 times faster.** Ducking and level matching use a running-sum moving average instead of a long convolution: the test mix went from 2 min 34 s to 10.5 s with the same audio
- **Startup texts agree with the three-option welcome.** Three references and two evaluation inputs still described a two-mode welcome; they name all three options now, the orchestrator says a mode menu alone is a failed startup, and the validator rejects a two-option description (`STARTUP_MENU_DRIFT`). The welcome itself is byte-identical
- **Two routing contradictions removed.** Marketing's "when to use" no longer claims ecommerce, product and launch planning, which belong to Ecommerce Campaign Strategy Director; the product-film route applies the conditional research gate instead of mandatory research, as the research skill defines it
- **Validation.** Skill descriptions have a total budget (fail above 7,800 characters, warn above 7,500). The historical `validate-package.mjs` / `package.test.mjs` suite is retired (decision 3a): both paths stay as inert stubs, because a hosted update cannot delete files
- **Repository only.** `scripts/release.py` prepares a release in one command (version markers, notes, manifest, checks, records, package, commit, fast-forward push) and records its GitHub publication; `scripts/check_all.sh --fast` is the edit-loop subset; `scripts/check_version_bump.py` and the checks workflow stop a package change on `main` without a version bump; CI validates the plugin and marketplace with a pinned Claude Code; AGENTS.md records the owner's product decisions (no personalization: rates, tools and preferences are runtime inputs)

## 1.54.0, 2026-10-10

From the owner's request of 2026-10-10 to add the skills of [cth9191/animate](https://github.com/cth9191/animate) to the motion graphics module:

- **The Animate engine joins Motion Graphics Workflow.** Short explainers, histories and little stories drawn entirely in code on one canvas, deterministic frame by frame, in seven illustrated styles (cut paper, crosshatch ink, riso print, sketchbook, manim-style math, pixel art, isometric line art) or a look matched from the user's references; story formats and a story grammar, shape-morph transitions, a score composed in code and mastered for phones, voice-over timed to the words or cuts on the beats of the user's own track, several aspect ratios from one piece, and a measured review (beat grid, story-arc loudness, dead beats, text cut off or overlapping, loudness). The upstream skill folder (version 0.4.0, MIT, commit `7e5eb56`) is bundled byte-identical as `skills/hyperframes-workflow/assets/animate-engine/`, with `SKILL.md` renamed `ENGINE.md` so no host lists it as a second skill; Studio adds only a package pin for Playwright 1.56.1. The [Animate engine reference](plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/animate-engine.md) says when to choose it and how Studio's approvals, research gate, acceptance verdicts and provider rules apply; its story grammar, frame checklist and craft rules guide motion plans on every host.
- **The required set has 18 tools.** The environment check adds `animate_engine`, a fifth Studio workspace starter installed with `npm ci` and `npx playwright install chromium`, for Codex and Claude Code; chat hosts mark it not supported. Capability `animate_render`; provenance in `integrations/animate/` with every file's Git blob hash, checked by a new test.

## 1.53.0, 2026-10-10

From the owner's request of 2026-10-10 to adapt Vercel's skill finder, and the deferred environment-check correction (decision 1a):

- **Skill finder, option 3 of the welcome.** The welcome now ends with three options: "3. **Looking for a specific skill?** — describe what it should do, and I will check whether I have something like it; in Codex and Claude Code I will also search the open skills.sh catalog." (Polish: "Szukasz konkretnego skilla (umiejętności)?"), and "Enter **1**, **2** or **3**." After `3` Studio asks what the skill should do and recommends its own matching skill first. In Codex and Claude Code, when Studio does not cover the need or alternatives are asked for, `find_skills.py` searches the whole skills.sh catalog, reads each candidate's security audits (ath, Socket, Snyk) and its own description, and gives a verdict (`listed`, `caution`, `unchecked`, `blocked`); install commands set `DO_NOT_TRACK=1`, never use `-y`, and run only on an explicit request; a `blocked` skill gets none. In ChatGPT, ChatGPT Work and the Claude apps Studio matches its own skills and gives the skills.sh link. The method is adapted from Vercel's MIT-licensed `find-skills` with provenance in `integrations/skill-finder/`. The six capability bullets and the later menus are unchanged; a `3` answering a two-option welcome shown before 1.53.0 still asks for clarification.
- **Tools a host cannot run are reported as such even when found.** In a chat sandbox, HyperFrames skills found there were reported `ok`; a tool marked `not_supported` for the host is now `not_on_this_host`, with the found files named in its note.
- Two planned evaluation cases (LM26, LM27) cover skill search in ChatGPT and Codex.

## 1.52.0, 2026-10-10

From the owner's ChatGPT Work update to 1.51.0, where the environment check reported HyperFrames skills and one package test failed:

- **HyperFrames detection no longer counts Studio's own skill.** The check looked for skill folders named `hyperframes*`, so Studio's `hyperframes-workflow` (its guide to HyperFrames, not HyperFrames itself) counted as installed HyperFrames wherever Studio's skills sit in a scanned skills folder. The check now skips Studio's own skill names and folders inside the Studio plugin. A new test covers both cases (Studio's skill alone: `missing`; the real `hyperframes` skill: `ok`), and the host test now runs with a temporary home so skills installed on the testing machine cannot change its result.
- The welcome, menus and all 37 skill IDs are unchanged.

## 1.51.0, 2026-10-10

From the owner's report of 2026-10-10 that the startup welcome says nothing about motion design:

- **The welcome names motion design.** The video bullet of the complete welcome now reads "Video, motion design and storytelling" (Polish: "Wideo, motion designie i opowiadaniu historii") and lists animated graphics and typography. The six capability bullets, qualifications, optional materials, structure and numbered options are otherwise unchanged; the English and Polish assets, the excerpts in `workflow-orchestrator/SKILL.md` and the protected welcome hashes in `validate-learning-mode.mjs` changed together. Later menus and their token mappings are unchanged.
- The owner's ChatGPT Work test of 1.50.0 is recorded: the bare invocation gave the complete Polish welcome, and the invocation sent with a graphic was handled as a task without the welcome (PASS_REPORTED).

## 1.50.0, 2026-10-09

From the owner's request of 2026-10-09: an update also checks that every required tool is installed and current; the welcome and menus are unchanged:

- **Update check after every plugin update.** `check_environment.py --update --host <host>` ends every update guide (Codex, ChatGPT Work, Claude, and UPDATE.md). It checks the whole required set again, reads the newest versions online (the dated snapshot when offline), and compares each Studio workspace starter with the updated plugin: a starter installed from the previous version's lockfile is `wrong_version`, and its printed command replaces the folder and runs `npm ci`. Verdicts: `pass`, `pass_with_updates` (everything works; newer versions listed with their commands, exit 4), `fail` (missing, too old or a stale starter), `limited` (chat sandbox), `unknown_host`. Newer versions are listed, not forced, because system packages often lag their newest release. The check still installs nothing.
- Workspace commands now replace an existing starter folder instead of copying into it, and name the actual workspace when `--workspace` is used. The capabilities reference mentions both checks; a repository test checks that every installation guide ends with `--final` and every update guide with `--update`.
- Tested in the provisioned container: the update check gave `pass_with_updates` (newer Python, FFmpeg, Node.js and Chromium online) and `fail` once a starter's lockfile differed from the plugin's.

## 1.49.0, 2026-10-09

From the owner's decision of 2026-10-09: required and optional tools are one required set, checked as the final step of installation; the welcome and menus are unchanged:

- **One required set of tools.** Every tool Studio uses is required; nothing is optional any more. The set: Python 3.9 or newer with Pillow, NumPy, CairoSVG, imageio-ffmpeg, matplotlib and Manim Community; FFmpeg with FFprobe; Node.js 20 or newer with npx (22 for HyperFrames); Chrome or Chromium; the four starters (Remotion kinetic type, GSAP motion, Remotion 3D, motion toolkit) copied into the Studio workspace (`~/.framecore-studio/workspace`) and installed with `npm ci` from their lockfiles, every package at exactly the pinned version; and HyperFrames. `tools.json` lists all 17 with their host statuses, install commands for Linux, macOS and Windows (the workspace commands carry the plugin's real path) and newest versions.
- **Final check at installation.** `check_environment.py --final --host <host>` ends every installation guide (Codex, ChatGPT Work, Claude): `pass` (complete), `fail` on Codex or Claude Code (something missing, too old or a workspace package of another version, with the commands to fix it; run again until it passes), `limited` in a chat sandbox (installed, with the tools that sandbox lacks named), `unknown_host`. Tools a host cannot run are listed as not on this host and do not count. The check still installs nothing. New statuses `wrong_version` and `not_on_this_host`; the validator rejects an optional tool and checks each workspace starter's package.json and lockfile.
- **Proved on a full environment.** In a Linux container the whole set was installed (pip in one virtual environment; Cairo and Pango development libraries for Manim; `npm ci` for the four starters; HyperFrames skills) and the final check passed with 17 of 17 tools ([record](verification/required-tools-final-check-1.49.0.json)). HyperFrames' installation guidance now reflects that it is part of the required set; the HeyGen catalog still stays off unless asked for.

## 1.48.0, 2026-10-09

From the owner's request of 2026-10-09: a fixed, validated tool list per host, and a correct installation path for Claude; the welcome and menus are unchanged:

- **Tools by host.** The environment check's `tools.json` now gives every tool (Python, Pillow, NumPy, CairoSVG, FFmpeg, FFprobe, Node.js, npx, Chrome or Chromium, Remotion, GSAP, HyperFrames) a status on each of five hosts: ordinary ChatGPT, ChatGPT Work, Codex, Claude Code and the Claude apps. The statuses are `observed` (owner-reported, with the evidence), `check` (may be in the sandbox), `install` (the user's machine), `per_project` (npm in a project) and `not_supported` (with the reason). `check_environment.py --matrix` prints the list, `--host` names the host (detected by default from documented traces), and on a named host a tool the host cannot run is `not_on_this_host`, not missing. The [README table](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#tools-by-host) is generated from the same data and tested; the validator requires a valid status for every tool on every host and evidence for every `observed` and `not_supported`.
- **Installation in Claude.** The repository is now a Claude plugin marketplace (`.claude-plugin/marketplace.json`, marketplace `framecore-works`), and the package has a Claude manifest (`.claude-plugin/plugin.json`) with the same identity and version. [CLAUDE_INSTALL.md](CLAUDE_INSTALL.md) gives the pinned install for Claude Code (`/plugin marketplace add FrameCoreWorks/framecore-works-creative-studio#v1.48.0`, then `/plugin install framecore-work-creative-studio@framecore-works`) and for the Claude apps (Customize > Plugins), verification, updates and the differences from ChatGPT and Codex. The validator checks the Claude manifest's identity; `tests/test_claude_plugin.py` checks the marketplace, the documented naming rules and limits, and runs `claude plugin validate` when Claude Code is installed.
- **Tested in Claude Code 2.1.295:** both manifests pass `claude plugin validate --strict`; a marketplace install lists 37 skills; headless conversations gave the complete English welcome for the bare name, the complete Polish welcome for a Polish greeting, and a direct answer, without the welcome, for a pasted question.

## 1.47.0, 2026-10-09

From the owner's report of 2026-10-09: a new thread with a screenshot and the Studio link got the welcome instead of help.

- **Content is a task, not a startup.** When Studio is invoked together with a screenshot, image, file or pasted text, or right after an unanswered user message in the thread, it reads that content first (including the text inside a screenshot), infers what the user wants (answer the question shown, solve the problem shown, edit or review an image, write a prompt, plan a video, learn a skill), routes to the owning skill and helps at once. With two plausible readings it helps with the likelier one and offers the others in one numbered line; it asks one targeted question only when no useful step is possible. The complete welcome stays for a bare invocation (only the Studio name or link), a greeting, a question about what Studio can do or an explicit menu request. Rules in the Workflow Orchestrator entry, its description and [startup and creative menus](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/startup-and-creative-menus.md#invocation-with-content), with a worked example (a Facebook post about ChatGPT moving truck parts during a PNG cut-out).
- A planned evaluation case (LM25) records the owner's report; the learning-mode validator pins the rule and a Studio test checks it. Welcome text and menus are unchanged.

## 1.46.0, 2026-10-09

From the owner's comparison of a 20 s vertical shop reel with a HyperFrames Studio film (2026-10-09); the welcome and menus are unchanged:

- **Argument before look.** A new [commercial motion](plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/commercial-motion.md) reference: for an advert or promo, Studio derives audience, action, benefit, friction, available evidence and verified claims, weighs a few different concepts internally, and records the chosen one in the contract's new `strategy` (hook with the scene that pays it off, a CTA that closes the action the film showed, rejected concepts with reasons); every scene says which step of the argument it adds (`argues`). `check-score.mjs` (identical in both starters) fails an unverified claim used in the copy, a missing `argues`, a hook without a later payoff and a CTA without the action it closes.
- **Picture proved on real frames.** The opening, first readable, densest and ending frames are saved at full size and phone scale before a film grows; carrier transitions replace a default wipe; photographs match their background or are isolated; pacing comes from information. The craft critique gains rules for repeated full-frame wipes, an opaque photo background on another scene colour, an empty first frame in feed films, and still stretches measured four times a second from the frames, where drift counts as still while appearing content counts as a beat.
- **Every visible word is checked.** New `text-audit.mjs` (with `text-audit.browser.js`) audits any HTML composition (Studio preview, HyperFrames, GSAP): each word's glyphs after fonts and transforms against the frame and every clipping ancestor, the element's own box included. A cut or hidden word in a readable hold fails; during a transition it is `transitional`; `data-layout-ignore` and similar flags never exempt visible text; a deliberate cut needs `data-text-clip-ok` with a reason and a pixel review. It writes a phone-scale contact sheet with cut words outlined. `review-frames.mjs` runs the same audit on every review frame.
- **Four acceptance verdicts.** New `acceptance.py` keeps technical, fidelity, composition and temporal verdicts separate: a valid export never passes the picture, a contract-only score (any number) leaves composition not_verified, composition needs a person's judgement of the key frames, and temporal needs a recorded normal-speed viewing. The critique now states `score_scope` and its own `verdicts`, including that it cannot see text completeness (a word cut by a mask leaves tidy pixels). The QA record has the four verdicts, coverage, exceptions and the stop decision.
- **Regression evidence.** Original fixtures reproduce the reviewed reel's defects (the clipped "TWÓJ WYBÓR" with and without `data-layout-ignore`, lines hidden by a box that fits the frame) and cases that must pass (complete Polish text, a transition mask, a declared exception); a 20 s 1080 x 1920 30 FPS silent proof contract was rendered and accepted through the whole chain. Ten Python tests, a contract test and two browser tests; a before/after [record](verification/perfua-regression-1.46.0.json).

## 1.45.0, 2026-10-09

The owner asked on 2026-10-09 for Studio to check its environment at installation and with one command; the welcome and menus are unchanged:

- **Environment check.** One command, [`check_environment.py`](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md), shows what Studio's tools can use where it runs: Python, Pillow, NumPy, CairoSVG, FFmpeg and FFprobe, Node.js and npx, Chrome or Chromium (including Playwright's copies), Remotion and GSAP per project, and HyperFrames' CLI and installed skills. Each tool is `ok`, `behind`, `below_minimum`, `missing`, `not_installed` (optional), `per_project` or `unknown`; each capability of the capability card is `ready`, `missing` (with what Studio delivers instead) or `unknown`; install and update commands follow for Linux, macOS or Windows, grouped into needed, optional and newer versions. Newest versions come from a snapshot dated 2026-10-09 or, with `--online`, from PyPI, npm, nodejs.org, endoflife.date and Chromium's stable channel. It installs nothing.
- **At installation and on request.** The Codex and ChatGPT Work installation guides run it once after the plugin is saved and show the user the result; Studio runs it whenever the user asks what is installed, and once before the first coded render when nothing shows the tools work. Install steps run only when the user asks. In ChatGPT the check describes the conversation's sandbox, not the user's computer.
- The validator checks that `tools.json` covers every checkable requirement of the capability card and maps each tool to a requirement, capability or pinned project file (`ENVIRONMENT_CHECK`), with a Studio test; 9 Python tests cover statuses, minimums, newest versions, per-project packages, HyperFrames skills and that offline runs never open a connection.

## 1.44.0, 2026-10-09

The owner's decision of 2026-10-09 on HyperFrames (1a: an optional engine where a shell exists, installed with a pinned command, not copied; 2a: the HeyGen catalog only on request); the welcome and menus are unchanged:

- **HyperFrames as an optional engine.** A new [engine reference](plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/hyperframes-engine.md), checked on 2026-10-09 against heygen-com/hyperframes at commit `3aa6886` (CLI 0.8.143, Apache-2.0), says when Studio offers HyperFrames (a shell with Node.js 22, FFmpeg and Chrome, such as Codex or a local project, and a brief that benefits: a launch film from a website, a longer narrated video, word-level captions on footage or a music-driven edit), how it is installed with a pinned version (HyperFrames' own plugin, or its skills by command; never copied into this package), and who decides what: Studio keeps intake, approvals, copy, storyboard and review, HyperFrames composes and renders. Choosing area `8` still never selects an engine.
- **HeyGen catalog only on request.** HyperFrames' `media-use` catalog (music, effects, images, voice, avatars) is used only when the user asks for it and has a HeyGen account; website assets only when the user owns the site or allows it, with each source recorded.
- The Motion Graphics skill, its code-based workflow, the capability card (`hyperframes_engine`, executed externally, shell hosts only) and the knowledge map link it; a test keeps the engine optional and the area-`8` rule intact. No HyperFrames render has been run through Studio; the route is planned, not verified.

## 1.43.0, 2026-10-09

From the [full review](docs/reviews/full-review-2026-10-08.md) (IM4); the welcome and menus are unchanged:

- **Video-generator snapshot.** A dated [map](plugins/framecore-work-creative-studio/skills/research-evidence/references/video-generator-snapshot.md) of twelve video families checked on 2026-10-09 (Google Veo 3.1 and Gemini Omni, Kling 3.0, Seedance 2.0 and 2.5, Wan 3.0, MiniMax H3, Runway Gen-4.5 and Aleph 2.0, Luma Ray3.2, Grok Imagine Video 1.5, Midjourney Video V1, LTX-2, and Sora as retired since 24 September 2026), with model IDs, operations (text and image to video, first and last frames, references, editing, extension, native audio), limits that shape prompts, multi-model surfaces and a watchlist. Every fact is labelled as read on the maker's page, read through a search summary or secondary. Research Evidence, its model mapping and the Video Prompt Architect start from it and still recheck the exact target before a model-specific prompt.
- The validator checks that each dated generator snapshot states its date and that Research Evidence cites the same date where it links it (`SNAPSHOT_DATE`), with a test.

## 1.42.0, 2026-10-09

New modules from the [full review](docs/reviews/full-review-2026-10-08.md) (NM1 to NM3, IM2); the welcome and menus are unchanged:

- **Sound for supplied footage.** [`footage.py`](plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-sound/footage.py) measures the cuts of a video the user made (ffmpeg scene score, or the user's cut list), takes the moments the user marks and the closing reveal, and writes a sound contract; `sound.py` then designs hits for those moments, composes a music bed fitted to the shots and mixes it with or without the video's own sound, ducking the music under it. The mix reports the same timing status and loudness as for a motion video. A request for sound for one's own reel now gets a plan from measured cuts and one offer to mix the track ([planned case MS06](plugins/framecore-work-creative-studio/evals/motion-sound-cases.json)).
- **Executable captions.** [`captions.py`](plugins/framecore-work-creative-studio/skills/caption-studio/assets/captions/README.md) checks SRT and WebVTT against three profiles (subtitles with the published reading speeds as errors, social captions timed to speech with the same limits as warnings, on-screen text with Studio's readable hold), converts between the formats, builds cues from timed words or segments with natural line and cue breaks, imports them into a motion contract exactly as the sync tool does, and burns them into a supplied video in the renderer's caption style with the audio copied unchanged. The readability reference now separates captions that follow speech from text with no speech.
- **Capability card.** One machine-readable [card](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/capability-card.json) lists what Studio executes itself (render, critique, sound, footage sound, captions, burn-in, player, sync, revision, Remotion), what each tool needs (Python, Pillow, numpy, ffmpeg, Node.js, a browser), what it delivers and what to deliver when a tool is missing, plus the boundary for host and external generators. The orchestrator, the capabilities reference and the role map link it; the validator checks every tool path, owner and requirement (`CAPABILITY_CARD`).
- **Host smoke set (outside the package).** [Eight short checks](docs/host-smoke-set.md) for a larger release (startup in English and Polish, a direct task, the video route choice, the code route, sound, the interactive offer and research that cannot run), a [recording template](verification/host-smoke-template.json) and `scripts/check_host_smoke.py`, which `scripts/check_all.sh` tests.

## 1.41.0, 2026-10-08

Discovery and depth, from the [full review](docs/reviews/full-review-2026-10-08.md) (the welcome and menus are unchanged):

- Skill descriptions lead with what the skill does and name its neighbour for the nearest other job. The 37 descriptions total 7,593 characters, under Codex's 8,000-character listing budget for an unknown context size (they were 10,400), and every one stays a valid YAML scalar.
- Caption Studio gains dated [readability defaults](plugins/framecore-work-creative-studio/skills/caption-studio/references/readability-defaults.md): Netflix's line, duration and reading-speed limits for English and Polish subtitles, Studio's hold rule for burned-in captions, safe-area guidance and the SRT and WebVTT formats; captions for a motion video are imported with the motion sync tool.
- UGC gains [formats, scripts and disclosure](plugins/framecore-work-creative-studio/skills/ugc/references/formats-scripts-and-disclosure.md): speaker types and what each may claim, nine formats, a script skeleton for 15, 30 and 60 seconds, dated platform specifications, platform labels and legal starting points for Poland (UOKiK), the EU (UCPD, AI Act Article 50) and the US (FTC), each with its source and check date.
- Storytelling gains [short-form structures](plugins/framecore-work-creative-studio/skills/storytelling/references/short-form-structures.md): eleven shapes chosen by the asset's job, a "but and therefore" causality check and a beat budget. Cinematography links the shot, lens, blocking and motion vocabulary in video craft.
- Every reference and template is now reached from a skill: the three music-video method references, the thread-link resume procedure, the Hipson and self-improvement templates, the artifact templates and the initial source register. The legacy audio alias keeps its three paths as pointers to the maintained files. The validator fails on an unlinked reference or template (`REFERENCE_REACH`), with a test.
- Learning Mode: the motion and sound domains add easing, readable holds, staggers, sound design for motion, hits and ducking, and a rendered comparison where code runs (always after the paper exercise). A finished quiz or worksheet may be offered once as an interactive check; the text version and its separate answer key stay the deliverable.
- Wording: the role map no longer explains kit installation, tool-routing steps are numbered correctly, Hipson points to Instruction Packet Factory for shared packet fields, and the brand and teacher paragraphs in Marketing and Copy Voice have their own sections.

## 1.40.1, 2026-10-08

- The Motion Graphics Workflow's description in 1.40.0 contained an unquoted colon, so its SKILL.md frontmatter was not valid YAML and a host parsing it strictly could fail to load the skill. The description is quoted again, every skill frontmatter and agent metadata file was parsed with a YAML parser (74 of 74 valid), and the canonical validator now rejects a description that is not a safe YAML scalar (`SKILL_YAML`), with a test for unquoted colons, comments, indicators and broken quotes. Use 1.40.1 instead of 1.40.0.

## 1.40.0, 2026-10-08

Motion graphics becomes a full route, from the [full review](docs/reviews/full-review-2026-10-08.md) and the owner's decisions of 2026-10-08 (the welcome and menus are unchanged):

- A video request that names neither a generator nor coded motion now gets one short choice: prompts for a video generator the user runs elsewhere, or a finished MP4 built from code here, with designed sound on request. The main route table has a row for animated video built from text, logos, screenshots, data or product photos; the product-film route and the commercial video director hand such films to the Motion Graphics Workflow.
- The audio owner and the orchestrator no longer say Studio has no media engine: sound for a motion video built from a contract is designed, mixed and checked by the motion sound engine; songs, lyrics, voice, external tools, licensed tracks and supplied-audio review stay with the Audio Production Director.
- A rendered motion video with its contract is reviewed by the motion workflow's craft critique. The role and route contracts gain a `motion` review modality and four handoffs (orchestrator to motion, motion to QA, and both ways between motion and audio), and the roster describes the motion role as building and rendering, not only planning.
- The motion skill's delivery rules, one 2,138-character paragraph before, are now a short list, and its owners table names this skill for the video's own sound.
- Pipeline Core routes motion graphics from code to the Motion Graphics Workflow whatever the runtime and drops leftover kit installation text; its QA checklist no longer asks for a confirmation ritual.
- Six planned behavior cases cover the motion and sound route (`evals/motion-sound-cases.json`), validated for structure; none is executed.
- Smaller: the reply to an interactive-version offer has a named place in the Project State (`entry_context.interactive_offers`); the workstyle profile shows the pace menu in the user's language; development-status sentences are gone; the README files describe the motion MP4, its sound and interactive answers.

## 1.39.0, 2026-10-08

Checks and tools first, from the [full review](docs/reviews/full-review-2026-10-08.md):

- The sound timing check no longer passes without measuring. The mix now judges every cue in a solo render, with the seed it has in the mix, so no neighbouring sound can mask a hit: on color-block 8 of 8 cues are judged instead of 1, and on all four examples every hit lands within 0.15 ms of its frame. Every timing summary carries `status` (`checked`, `partly_judged`, `not_judged`, `missing` or `by_construction`); `sound.py check` on a whole effects track exits 3 when cues sat too close together to be judged, as the craft critique does for frames it could not see.
- Copy containing `</script>` or `<!--` no longer breaks the HTML preview. The contract is embedded with every `<` written as `\u003c`, and `check-preview.mjs` rejects a raw one; before, the checker passed a file the browser could not open.
- One reading-time rule. `check-score.mjs` and the craft critique both use the motion-craft rule: the longer of 13 characters per second plus 0.5 s and 0.5 s plus a third of a second per word, at least 1 s. Before, the two tools disagreed by up to half a second on the same line.
- The improvement round stays inside the shared budget: at most two repair rounds after the first review, and an error left after the second is named in the reply.
- The renderer guide says an SVG logo needs `cairosvg` and to ask for a PNG up front where no shell is available; the export guide records the owner's Android H.264 report.
- Outside the package: the native Codex entry no longer says "seven work areas" (the menu has had eight since area 8 was added) and a test guards the count; CI installs ffmpeg, numpy and Pillow, so the renderer, critique and sound tests run there too (15 tests were skipped before), with `actions/checkout` on Node 24; the release-notes refresh reads the publication record (it had skipped silently since 1.8.x); the historical legacy suite is compared with its recorded known failures (`tests/legacy-baseline.json`) instead of being reported as numbers; a browser test compares the Python renderer with the browser engine pixel by pixel; README, install guide and records corrected.

## 1.38.0, 2026-10-08

- The music no longer winds down for the rest of a video whose final reveal comes early. When more than 1.5 bars and 3 s remain after the reveal (an end card held for half the video, as in the owner's Bounce Party test), the composed music marks the reveal with a cymbal, plays on at full energy, eases in the bar before the last, leads home and resolves in the last bar (`soundDesign.music.endBar`). Measured on an 8 s spot with the reveal at 4 s: the level from 4 to 7 s stays within 0.5 dB of the build-up instead of falling 13 dB. A reveal near the end resolves on the reveal as before.
- Contracts planned before 1.38.0 keep their sound until planned again; among the bundled examples only color-block changes.

## 1.37.0, 2026-10-08

From an external audit of the repository by ChatGPT (GPT 6.1 Sol), with each finding reproduced before it was fixed ([response](docs/audit-2026-10-08-response.md)):

- The craft critique no longer reports a pass for a picture it did not see. `status` says what the score covers (`checked`, `issues`, `contract_only`, `incomplete`); frames that were asked for but could not be read, including a missing video or one whose size, frame rate or length differs from its contract, give `incomplete` and exit code 3.
- `--video` decodes only the review frames instead of the whole video, so a long or large video no longer fills memory.
- `sound.py check` reports a cue with no sound in its window as `missing` and fails, instead of counting silence as a hit on time.
- `revise.mjs extend` moves the sound cues (`sfx`) with the picture and marks the sound design stale; `sound.py mix` refuses a stale design, and `sound.py plan` keeps the choices the user fixed when planning again.
- Outside the package: the motion benchmark takes the `*.motion.json` contract (never `meta.json`) and also judges the delivered video's own frames; one check script (`scripts/check_all.sh`) now drives the release workflow and a new checks workflow on every push and pull request, including the presentation and benchmark tests, with the historical legacy suite as a separate, non-blocking status.

## 1.36.0, 2026-10-08

- Studio offers an interactive version on its own, on the owner's request after the first Intelligent UI test. When a static answer would be easier to understand by exploring it (a storyboard or shot list, a timing or easing choice, directions to compare, a campaign matrix, a lesson concept with a cause and effect), it ends with one short, optional offer that names what the user could do, and says whether it would be a view in the chat or an HTML file (which a phone may not show inside the chat). One offer per stage, never instead of the answer and never during onboarding or under a pending learner exercise; a decline is remembered for that kind of stage; accepting builds from existing material and authorizes no new generation.
- Two new planned scenarios (an offer after a storyboard, a declined offer not repeated) and a mutation test for the rule.

## 1.35.0, 2026-10-08

- Presentation and interaction for ChatGPT's Intelligent UI. One shared policy (`pipeline-core/references/presentation-and-interaction.md`), reached by every skill through the integration authority, decides per stage between text and a native element (comparison, one-variable experiment, timeline, form, chart) and always keeps an equivalent text path. Interactions are views of the existing Project State: only real events count, resolved choice groups expire, a stale view never overrides a newer revision, and a selection never authorizes paid generation, upload or publication. Short adaptations in learning, concepts, storyboard and motion, prompts, campaigns and QA, and audio. The startup welcome, menus, onboarding and locks are unchanged.
- `scripts/validate-presentation.mjs` in the canonical validator, `tests/presentation.test.mjs` and 17 planned host scenarios in `evals/presentation-cases.json` (not run).
- How ChatGPT renders these answers is not verified in a host yet.

## 1.34.0, 2026-10-08

- Craft critique and a mandatory improvement round, to make results depend less on the model. `motion-review/critique.py` scores a contract and its frames against a numeric rubric (reading time per scene, words per scene, pace, a hook within 1.5 s, the end card, line stagger, contrast, frame edges, the 9:16 interface zones and composition balance), gives a concrete fix for every finding (often a `revise.mjs extend` command) and writes a contact sheet per format. With `--video` it judges the delivered video's own frames, for videos drawn by a renderer written for the project. Every delivery now runs it, fixes errors and warnings (or says why a warning stays), re-renders and reports the score before and after.
- `sound.py mix` measures the delivered AAC itself: when encoding raised the true peak above -1 dBTP it trims the master and muxes again, and the summary reports the file's own loudness and true peak, so no extra loudness pass is needed.
- Every sound choice the user fixes (`--set lead`, `landing`, `transition`, `impact`, `accent`, `key`) is recorded in the contract as set by the user.
- Owner references in the motion guidance: accepted and rejected videos as calibration, including the rejected Bounce Party direction from the 2026-10-08 ChatGPT Work test.
- Found by the owner's four-step ChatGPT Work test with GPT 6.1 Sol (all four delivered and passed the technical checks; steps 1 to 3 approved by ear, step 4 rejected as weak motion design).

## 1.33.0, 2026-10-08

- Sound and music are designed anew for every video, on the owner's direction. Studio analyses each motion contract (style, motion tempo and easing, canvas colour, scene kinds, taps, pacing and the brief's English or Polish words) into a pace and six moods, then `generate.py` designs a new sound for every role (transition, landing, press, release, tick, impact, boom, riser, accent: its kind, material resonances, key-tuned pitches, band paths, layers) and `compose.py` composes new music (a progression from a grammar of harmonic functions, Euclidean rhythms with swing, a motif, instruments designed within the families the style allows, a drum kit designed as recipes, an ending). Nothing is picked from finished sounds or stored loops.
- Recipes: a JSON layer language (`recipe.py`) that the generators write, the contract keeps (`soundDesign.recipes`, `soundDesign.music.recipe`) and the host model or a person can read and edit; `sound.py analyze` prints the profile and what was designed with reasons, `--variation` designs the same video anew and `--set` fixes a palette, key or kind of sound.
- A quality gate redesigns any sound that is close to one pure tone (a toy beep or a hollow one-note drum), and a test holds every role at its approved level.
- From a measured audit of 1.32.0: the final reveal now lands on a downbeat of the music (tempo fitted inside the style's range), the music resolves on the tonic and rings out instead of being cut off, the low end is lighter, music dips briefly under hits, a true-peak limiter keeps loudness at -14 LUFS (one example had been 1.7 dB short), the bass carries harmonics for phone speakers, and a music stem is written.
- Fixes: minor-key progressions played two chords outside the key; a landing swell was levelled about 27 dB too loud (owner listening); the knock and snare the owner found flat and empty are no longer part of designed sound.

## 1.32.0, 2026-10-07

- Motion sound design at studio standard. `motion-sound/sound.py` plans a sound track from the motion contract with the picture's own timing (lines, items, captions and cards landing, taps and releases, screen pushes, sweeps, canvas wipes, counter steps, camera moves, the final reveal), renders it with `synth.py`, masters it to -14 LUFS under -1 dBTP and muxes it into the MP4 without touching the picture.
- `synth.py` designs every sound in layers: whooshes from moving-filtered noise that last as long as the move and travel with it, impacts with a falling sub and a bright transient, a boom, risers, modal clicks, ticks and knocks, bell accents tuned to the key, and a shared room. A music bed is composed to the video's length: four chords, pad, bass, arpeggio and drums, with energy following the scenes and tempo and key from the style.
- Timing is checked on every mix: transients within 2 ms of their frames, whooshes on their measured peaks; the contract gains `sfx` (with `params`) and `soundDesign`, validated by `check-score.mjs`.
- The sound policy changes on the owner's decision: Studio may design sound and music with code at studio standard and never delivers toy tones. A CC0 recording library tried first was rejected by the owner for quality and never released. The owner approved the music and clicks; whooshes were lowered by 6 to 7 dB after listening.

## 1.31.0, 2026-10-07

- Taps: `device` scenes take `taps` (`{at, x, y}`). A finger marker arrives 4 frames before the tap, presses on it while a ring in the accent colour spreads, then leaves; with the next screen 3–5 frames later, the viewer sees what caused the change.
- Browser frame: `frame: 'browser'` draws a window whose title bar holds an address field with the `url` copy, for web apps.
- Scene backgrounds: any scene can set `params.background` and wipe it in from a side (`backgroundWipe`, `backgroundFrames`), so a new colour sweeps over the previous scene. This makes the Color block style's signature buildable; `examples/color-block.motion-score.json` shows it.
- The engine copies, `check-score.mjs` and the Python renderer support all three; existing contracts render byte-identically in the Python renderer.

## 1.30.0, 2026-10-07

- Product films: a new `device` scene kind shows the user's screenshots inside a drawn phone (rounded body and island) or window (title bar and controls). Screens change with a push, fade or cut; a camera focus eases in on a point of the screen and keeps it in place; a caption sits beside the device in landscape and above it in vertical formats. Every size is computed in whole pixels, so the preview, the Remotion starter and the Python renderer place it identically.
- `references/product-films.md` adapts the product-film rules of kaventro/motion-designer to screenshots: real features and fictional data, the device always in frame, one action per beat with a hold, captions beside the device, and App Store guideline 2.3.4. `examples/app-film.motion-score.json` uses original screenshots with example data, in 16:9 and 9:16.
- `check-score.mjs` validates device scenes (frame, transition, screen assets with `src`, `width` and `height`, increasing `at`).
- Frame review fix: new headless Chrome gave the page 87 pixels less than the window and filled the bottom of every screenshot with the background. `review-frames.mjs` now measures the difference, enlarges the window and crops screenshots to the frame in the contact sheet; text measurements were never affected.

## 1.29.0, 2026-10-07

- Adapted from [kaventro/motion-designer](https://github.com/kaventro/motion-designer) (MIT, commit `7d0b8bb`), with provenance in `integrations/kaventro-motion-designer/`.
- Seven motion styles (Brand-native, Meadow, Warm ink, Midnight, Field guide, Paper and ink, Color block) in `motion-styles/styles.json`, mapped to contract tokens and motion values with a signature move each. When the brief leaves the look open, Studio offers two or three; the user's brand values always win. The contract records the choice in an optional `style` field.
- Motion craft gains a vocabulary by feel, one relay object, an accent with one meaning, one signature per video, scenes changing on bar lines, the drop on the biggest reveal, a word-based reading-hold check, a descender note for masks and a table of video types.
- Review gains five passes (overview, transitions, text, phone size at 360 px, frame 0 and fresh eyes), seven scores with a pass mark of 8 inside the existing budget, and a failure catalogue.
- The Python renderer adds motion blur (`--blur`, subframes over a 180-degree shutter; holds stay sharp) and phone-size stills (`--stills-width`).
- `beats.py` and `music_edit.py`, retained unchanged, detect the tempo, bar 1 and drops of a supplied track and cut it to whole bars exact to the frame; a sound brief guides the music's role, tempo and texture. Generated music, synthesized sounds and voice models were not adopted.

## 1.28.0, 2026-10-07

- New bundled Python renderer, `motion-render/render.py`: a port of the scene engine (all six scene kinds, easings, holds, lift and sweep exits, captions, safe areas and formats) drawn with Pillow and encoded by ffmpeg as H.264 without audio. `--check-dir` saves the frames for the pre-delivery check; fonts resolve from `tokens.fontFamily` or are chosen with `--font` and `--font-bold`.
- With code execution, Studio copies the renderer byte for byte as `<id>.render.py` and runs it instead of writing its own drawing code, so videos look the same across users, sessions and revisions. An own renderer is written only when the bundled one cannot run, and the reply says so.
- Checked against the browser engine at the review frames of three contracts (16:9 and 9:16, with captions): mean difference below one grey level; repeated renders byte-identical.

## 1.27.0, 2026-10-07

- With code execution, the render script is delivered with the video as `<id>.render.py` (or the language used) and named in the contract's new optional `runtime.script`. It takes the contract and the output path as arguments and reads every visual value from the contract.
- A revision re-runs the previous render script unchanged on the new contract, so unchanged parts stay pixel-identical; the script changes only when the request needs something it cannot draw, and that change is listed too. Without the script, Studio asks for it once, otherwise writes a new one and says that unchanged parts may differ by a few pixels. This follows the 2026-10-07 ChatGPT Work revision test, whose re-written renderer moved unchanged text by about 3 px.
- `check-score.mjs` accepts `runtime.script` only as a plain file name; `revise.mjs` gives it the new revision suffix.

## 1.26.0, 2026-10-07

- Revisions start from the delivered contract. When the user asks to change a video, Studio loads its `.motion.json`, changes only what was asked, increments `revision`, lists what changed (was → is), renders with the same renderer and font, and names the new files with the revision so earlier versions are kept.
- New `motion-revise/revise.mjs`: `diff` lists every changed value between two revisions; `extend` lengthens or shortens one scene and moves later scenes, holds, captions, cues and the total length by the same number of frames, preserving overlaps, refusing empty results and never overwriting a file. It then names descriptive text fields that mention frames or seconds so they can be rewritten.
- The contract lifecycle gains a sixth step, Revise.

## 1.25.0, 2026-10-07

- Studio never synthesizes music, sound effects or voice with code for a motion delivery; the rendered MP4 stays silent until the user chooses a real source. After delivery it asks once whether sound is wanted and offers three routes: the user's own file muxed into the MP4; a voice or music provider such as ElevenLabs only when it is actually connected and the cost and terms are confirmed, otherwise the voice-over text, SRT timing and voice direction for the user to generate it; or a local generator the user names that is already installed and licensed.
- Document a mux command that keeps the picture untouched and delays sound with real silence (`adelay`) instead of `-itsoffset`; a 2026-10-07 check kept a 120 BPM click track sample-exact and the video stream byte-identical.
- Remove stale 1.22.0 sentences from the motion skill entry that forbade the hand-written MP4 renderer used since 1.24.0. The tone-cue helper is marked as a sync-test tool whose tones are never delivered.

## 1.24.0, 2026-10-07

- In hosts with code execution but no shell, Studio now delivers the rendered MP4 as the main result, with the contract as `<id>.motion.json`. This matches the owner's decision after the 2026-10-07 tests, in which ChatGPT rendered and delivered MP4 files itself.
- Before delivery the frames at every scene boundary, hold start and transition are checked for overlapping, clipped or off-frame text, and the reply names the frames checked; a render without this check overlapped two statements on 2026-10-07.
- An HTML preview is optional and for watching only: no Export video button and no `MediaRecorder`, because the MP4 is the video file and a `MediaRecorder` export failed on the owner's phone. Only the byte-for-byte template keeps its tested export.
- The 1.23.0 requirements for a one-click player link and against rendering the MP4 directly are withdrawn. The motion player, its GitHub Pages site and `player-link.mjs` remain available, and the player is the route when no code can run.

## 1.23.0, 2026-10-07

- Studio now ends a motion delivery in hosts without a shell with one clickable link that opens the motion player with the animation already loaded: the player address plus `#contract=` and the contract as base64url JSON, computed with code execution. The `.motion.json` file is attached as well; the paste panel is only the fallback when no code can run. A link of this form opened the animation on the owner's phone on 2026-10-07.
- Add `assets/single-file-preview/player-link.mjs`, which builds the same link from a contract in Node; its output is byte-identical to the documented Python expression.
- Studio no longer renders a substitute video with code other than the plugin's renderers; the player's Export video is the reference export. A substitute MP4 in the 2026-10-07 test differed from its own contract and overlapped two statements.
- A direct request to build a complete brief is recorded as `approval.status: "approved"` with evidence quoting it; `check-score.mjs` says so when the status is invalid.

## 1.22.0, 2026-10-07

- The single-file preview becomes the motion player: **Open contract** loads a motion contract from pasted JSON, a `.json` file or a dropped file, checks that every scene has a known kind and can be drawn, and carries it in the address fragment, which is never uploaded. Formats and Export video work as before.
- In hosts without a shell, Studio now delivers the contract (`<id>.motion.json` or one JSON code block) and sends the user to the motion player, instead of a whole HTML page. Two ordinary ChatGPT tests on 2026-10-07 showed that a model rewrites the 48 KB template rather than copying it, losing the tested export; a complete HTML file is now delivered only as a byte-for-byte copy with its contract replaced.
- Fallback: when a self-written page is still delivered, its export must reproduce `video-export.mjs` (WebCodecs, frame by frame, H.264 MP4 first); `MediaRecorder` and real-time recording are not allowed. In the first 2026-10-07 test such a reproduced export produced a playable MP4; the second test's `MediaRecorder` export produced no file.
- Every GitHub release adds `framecore-motion-player-<version>.html`, byte-identical to the template, and a new Pages workflow publishes the same file to the `gh-pages` branch for <https://framecoreworks.github.io/framecore-works-creative-studio/> once GitHub Pages is enabled.
- `export-video.mjs` waits for the player to finish loading instead of reading the page mid-navigation, and a busy temporary profile no longer fails an export; both were found by running four exports at once.
- Existing contracts render pixel-identically to 1.21.0.

## 1.21.0, 2026-10-07

- Studio now delivers the single-file preview unchanged except its embedded contract: every scene is declared with a scene kind, each displayed line gets its own copy ID, and the player, scene engine and video export are never rewritten or replaced by a hand-written renderer. This follows the 2026-10-07 ordinary ChatGPT test, whose export worked but whose preview was rewritten by hand.
- Add `assets/single-file-preview/check-preview.mjs`: passes only when a delivered preview matches the template outside the contract, the contract passes `check-score.mjs` and every scene declares a kind.
- Add the `sweep` exit (`params.exit: 'sweep'`, optional `sweepFrames` and `sweepColor`): the content fades and slides left while a vertical line crosses the frame and finishes at the scene end, so the next scene enters behind it. Add the `two-statements` example built from the test brief.
- `check-score.mjs` reports `params.exit` and `sweepFrames` errors, requires `schema_version` 1 when present and explains that `audio` is text, with audio files in `music` and `voiceover`.
- Existing contracts render pixel-identically to 1.20.0.

## 1.20.0, 2026-10-06

- Add browser video export: `assets/motion-export/video-export.mjs` draws each frame of the single-file preview into a canvas through an SVG foreignObject image, encodes it with WebCodecs and writes MP4 (H.264) when the browser can encode it, otherwise WebM (VP9 or VP8), with dependency-free muxers. Video only.
- The single-file preview gains an Export video button with progress and a download link named per format; its controls now wrap on narrow screens.
- Add `assets/motion-export/export-video.mjs`: the same export from a shell with a local Chrome or Chromium over the DevTools pipe, without dependencies.
- The toolkit validation keeps the preview's embedded export identical to `video-export.mjs`; tests cover both muxers and an opt-in real export.
- Review and preview frames are pixel-identical to 1.19.0.

## 1.19.0, 2026-10-06

- Add `assets/motion-sync/sync.mjs`: records a beat grid (BPM, first-beat offset, beats per bar) in the motion contract and reports where every scene, hold and caption falls on it, with the nearest beat as a proposal; imports SRT or WebVTT voice-over subtitles as captions with exact text in the copy ledger. It writes a new revision and never moves approved timing.
- Add `music`, `voiceover` and `captions` to the contract. The scene engine gains `beatFrames`, `buildCaptions` and `captionsFrame`; captions cut on exact frames above the scenes and respect the safe area.
- The single-file preview draws captions and plays music and voice-over files saved next to it, with the audio clock driving the frame; the Remotion starter renders captions and mixes both files from `public/`.
- `check-score.mjs` validates music, voice-over and captions and warns about captions shorter than the reading heuristic; the storyboard shows scene starts as bar.beat and lists the captions. The frame review captures and measures captions.
- Contracts without these fields render pixel-identically to 1.18.0.

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

Replaces README installation prompts with links to complete ChatGPT Work and Codex procedures. Translates maintained package documentation and learning guidance into English while preserving localized startup/menu resources, exact copy, multilingual fixtures, routing and pinned sources. Adds a permanent English authoring and installation-documentation policy to repository maintenance instructions.

## 1.2.10, 2026-09-30

Fixes four audited regressions: lexical exact-copy matching, missing blueprint/operation/music-handoff validation, a grouped-choice example that conflicted with sequential learning onboarding, and missing pending onboarding context in the portable progress card. Adds six source regression tests. Existing routing, skill identities, provider rules, assets, starter prompts, canonical welcome and pinned sources are unchanged. Source checks do not establish installed-client behavior.

## 1.2.9, 2026-09-30

Defines CQoT as Critical-Questions-of-Thought and makes its critical checks part of the existing automatic review. MoE-style selects useful existing specialist responsibilities without claiming separate model or agent execution. CoVe verifies material factual/technical claims with sources or observed tests, reusing the research preflight; comparison and branching are conditional on a real unresolved choice or dependency. Direct and Quick tasks retain one shared review budget and stop unchanged on a pass. Clear goals and observable criteria replace mandatory hidden-CoT narration. Adds source-regression guards for the canonical meaning, shared budget, evidence boundary and owner routes. Preserves identities, assets, pinned sources, welcome, menus, onboarding and starter prompts; source checks do not certify active-client behavior.

## 1.2.8, 2026-09-30

Makes bounded output review automatic for substantive creative results, including ideas, prompts, copy, graphics and production plans, before final delivery. Every existing skill root points to the same profile. Reuses domain QA, preserves a passing draft, caps the initial review plus repairs at three evaluation passes by default and keeps stricter modality budgets. Actual media acceptance requires actual inspection; review never authorizes another generation, upload or paid retry. Welcome, menus, onboarding, technical identities and pinned sources remain unchanged. Source checks are distinct from installed-client behavior.

## 1.2.5, 2026-09-30

Makes learning onboarding sequential at every model/effort setting: ask one question about one missing decision, accept a numbered choice or free text, wait for the answer, then ask only the next necessary question. Removes the permissions to batch learning questions from the mentoring method, integration policy and workstyle profile. Reuses voluntary answers, skips known or optional questions and proceeds to the plan and first lesson as soon as enough context is supplied. Keeps the canonical welcome and existing creative entry unchanged. The native Codex wrapper carries the same contract. No stress-test reports or transcripts are added to the shared package.

## 1.2.4, 2026-09-30

Uses one canonical Polish welcome as production text. Every sent Studio-only invocation, including repeated startup in the same conversation, copies the complete identity/capability introduction, optional-material invitation and final 1. Tryb kreatywny / 2. Tryb nauki menu verbatim, without a salutation or added prose. Preserves explicit language requests, concrete-task and actual-resume bypasses, checkpoints and the subsequent creative pace/work-area and learning routes. Native Codex installation points to the same asset. Source checks and bounded source-use observations remain distinct from active-client behavior.

## 1.2.3, 2026-09-30

Simplifies poster and static-graphic format intake: ask print/internet/both only when use is unknown, then describe paper sizes through familiar sheets or digital placement as post/story. Number every option, reuse supplied specifications and avoid mixed paper-code/pixel menus. Exact dimensions remain available for expert requests, prompt compilation and delivery. The shared intake method governs the orchestrator, Brief Architect and static-design owner without changing the pinned upstream source. Format choices do not establish print readiness, renderer controls or generation permission.

## 1.2.2, 2026-09-30

Strengthens the short Studio entry contract across reasoning settings: introduce capabilities and optional materials before the final intent menu, then require creative pace and work-area selections when unresolved. Choice tokens belong only to pending groups; resolved menus expire and simultaneous groups use distinct number/letter namespaces. Offline learning briefly discloses incomplete or unattempted research at the first substantive lesson. Preserves direct briefs, resumed work, learning progress, 37 skill identities, assets, starter prompts and provider boundaries. No stress-test reports or transcripts are added to the shared package. Source-use verification does not establish active-client behavior.

Repository-only installer now reads the actual frontmatter identity, recognizes quoted names/keys and trailing comments, and requires review for ambiguous syntax before writes. Installation guidance carries the current release number.

## 1.2.1, 2026-09-30

- Restores the complete Studio welcome, capability overview and optional asset invitation.
- Uses 1. Tryb kreatywny / 2. Tryb nauki at startup, keeping Tryb tworzenia as an alias.
- Restores quick/expanded pace selection and the established seven creative work areas after a mode-only choice.
- Binds numeric replies to the last menu actually shown; preserves explicit decisions, older-session numbering and direct-task bypass.
- Keeps the learning method, existing owners, pinned sources, identity, assets and execution limits; adds focused source regression checks.

## 1.2.0, 2026-09-30

- Adds optional Tryb nauki / Tryb tworzenia intent routing while keeping Quick/Deep as pace.
- Adds bounded onboarding, a personalized curriculum, learner practice and feedback across fourteen supported creative areas, with explicit limits and no-render options.
- Keeps progress in the shared Project State and adds a portable card and immediate mode switching.
- Reuses all 37 existing skill identities and preserves production routes, provider authorization, pinned sources, logo and starter prompts.
- Adds sixteen planned scenarios, a guarded historical greeting override, source-regression checks and release-workflow coverage of the active test suites.
- Source, hosted save and GitHub publication status are recorded separately in RELEASE_STATUS.md.

## 1.1.1, 2026-09-29

- Standardizes all 37 skill display names with spaces and initial capitals, preserving AI, UGC, HyperFrames and OpenCut.
- Adds 14 missing display metadata files, moves Copy Voice and Tool Routing Cost metadata into the supported interface/policy fields, and normalizes Workflow Self Improvement.
- Adds a naming standard and a release gate for future skills.
- Preserves technical IDs, routing, skill instructions, existing starter text, policies, integrations and original source snapshots.

## 1.1.0, 2026-09-29

- Adds a dated catalog of creative services, source evidence and a Polish setup guide.
- Distinguishes ChatGPT Chat/Work and Codex clients, directory apps, custom MCP, CLI and direct API.
- Separates Higgsfield consumer-account billing from Open Higgsfield API and records unresolved live-tool/documentation conflicts.
- Adds optional post-install tool selection to the full installation prompts and README shortcuts; keeps setup optional and private on updates.
- Preserves all 37 modules, original source bundles, logo, selected repository banner and starter prompts. No provider installation or media pilot.

## Documentation follow-up, 2026-09-29

- Adds `@plugin-creator` to copyable Work installation/update prompts and `$plugin-creator` to their Codex equivalents, including both README installation prompts.
- Documents menu selection, host availability checks and the difference between selecting a capability and granting access.
- Keeps Codex's native complete-bundle installation independent of Plugin Creator. Hosted plugin version and published 1.0.1 archives are unchanged; these corrected guides are on main.

## 1.0.1, 2026-09-29

- Replaces registry-based installation with direct source installation in ChatGPT Work and Codex.
- Adds four copy-paste installation/update guides, a complete hashed source inventory and a local Codex installer.
- Preserves the complete linked bundle, 37 canonical modules, original sources, logo and starter prompts.
- Adds a release workflow that publishes verified packages after upload.

## 1.0.0, 2026-09-28

First stable release of the documented Studio scope. See [release status](RELEASE_STATUS.md).

- Establishes a bounded release scope for the existing 37-entrypoint creative studio.
- Adds repository distribution metadata (retired in 1.0.1), installation/update guidance and reproducible local release packaging.
- Preserves all existing skill instructions, references, original source bundles and the owner-provided logo.
- Retains actual verification history and identifies unexecuted evaluations.
- Separates repository distribution from hosted ChatGPT plugin publication and external provider setup.

Detailed development changes remain in the plugin's [release history](plugins/framecore-work-creative-studio/docs/release-history.md).

- Licenses FrameCore Works original code, instructions and documentation under Apache-2.0 with preserved upstream notices.
