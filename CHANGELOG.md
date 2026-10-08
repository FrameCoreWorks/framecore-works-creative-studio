# Changelog

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
