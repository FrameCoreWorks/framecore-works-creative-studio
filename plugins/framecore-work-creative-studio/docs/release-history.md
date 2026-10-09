# Historical development notes

## 1.42.0, 2026-10-09

New modules from the full review (the repository's docs/reviews/full-review-2026-10-08.md); the welcome and menus are unchanged:

- **Sound for supplied footage.** [`footage.py`](../skills/hyperframes-workflow/assets/motion-sound/footage.py) measures the cuts of a video the user made (ffmpeg scene score, or the user's cut list), takes the moments the user marks and the closing reveal, and writes a sound contract; `sound.py` then designs hits for those moments, composes a music bed fitted to the shots and mixes it with or without the video's own sound, ducking the music under it. The mix reports the same timing status and loudness as for a motion video. A request for sound for one's own reel now gets a plan from measured cuts and one offer to mix the track ([planned case MS06](../evals/motion-sound-cases.json)).
- **Executable captions.** [`captions.py`](../skills/caption-studio/assets/captions/README.md) checks SRT and WebVTT against three profiles (subtitles with the published reading speeds as errors, social captions timed to speech with the same limits as warnings, on-screen text with Studio's readable hold), converts between the formats, builds cues from timed words or segments with natural line and cue breaks, imports them into a motion contract exactly as the sync tool does, and burns them into a supplied video in the renderer's caption style with the audio copied unchanged. The readability reference now separates captions that follow speech from text with no speech.
- **Capability card.** One machine-readable [card](../skills/workflow-orchestrator/assets/capability-card.json) lists what Studio executes itself (render, critique, sound, footage sound, captions, burn-in, player, sync, revision, Remotion), what each tool needs (Python, Pillow, numpy, ffmpeg, Node.js, a browser), what it delivers and what to deliver when a tool is missing, plus the boundary for host and external generators. The orchestrator, the capabilities reference and the role map link it; the validator checks every tool path, owner and requirement (`CAPABILITY_CARD`).
- **Host smoke set.** The repository adds eight short host checks for larger releases with a recording template and a checker; they are outside this package.

## 1.41.0, 2026-10-08

Discovery and depth, from the full review (the repository's docs/reviews/full-review-2026-10-08.md); the welcome and menus are unchanged:

- Skill descriptions lead with what the skill does and name its neighbour for the nearest other job. The 37 descriptions total 7,593 characters, under Codex's 8,000-character listing budget for an unknown context size (they were 10,400), and every one stays a valid YAML scalar.
- Caption Studio gains dated [readability defaults](../skills/caption-studio/references/readability-defaults.md): Netflix's line, duration and reading-speed limits for English and Polish subtitles, Studio's hold rule for burned-in captions, safe-area guidance and the SRT and WebVTT formats; captions for a motion video are imported with the motion sync tool.
- UGC gains [formats, scripts and disclosure](../skills/ugc/references/formats-scripts-and-disclosure.md): speaker types and what each may claim, nine formats, a script skeleton for 15, 30 and 60 seconds, dated platform specifications, platform labels and legal starting points for Poland (UOKiK), the EU (UCPD, AI Act Article 50) and the US (FTC), each with its source and check date.
- Storytelling gains [short-form structures](../skills/storytelling/references/short-form-structures.md): eleven shapes chosen by the asset's job, a "but and therefore" causality check and a beat budget. Cinematography links the shot, lens, blocking and motion vocabulary in video craft.
- Every reference and template is now reached from a skill: the three music-video method references, the thread-link resume procedure, the Hipson and self-improvement templates, the artifact templates and the initial source register. The legacy audio alias keeps its three paths as pointers to the maintained files. The validator fails on an unlinked reference or template (`REFERENCE_REACH`), with a test.
- Learning Mode: the motion and sound domains add easing, readable holds, staggers, sound design for motion, hits and ducking, and a rendered comparison where code runs (always after the paper exercise). A finished quiz or worksheet may be offered once as an interactive check; the text version and its separate answer key stay the deliverable.
- Wording: the role map no longer explains kit installation, tool-routing steps are numbered correctly, Hipson points to Instruction Packet Factory for shared packet fields, and the brand and teacher paragraphs in Marketing and Copy Voice have their own sections.

## 1.40.1, 2026-10-08

- The Motion Graphics Workflow's description in 1.40.0 contained an unquoted colon, so its SKILL.md frontmatter was not valid YAML and a host parsing it strictly could fail to load the skill. The description is quoted again, every skill frontmatter and agent metadata file was parsed with a YAML parser (74 of 74 valid), and the canonical validator now rejects a description that is not a safe YAML scalar (`SKILL_YAML`), with a test for unquoted colons, comments, indicators and broken quotes. Use 1.40.1 instead of 1.40.0.

## 1.40.0, 2026-10-08

Motion graphics becomes a full route, from the full review (the repository's docs/reviews/full-review-2026-10-08.md) and the owner's decisions of 2026-10-08 (the welcome and menus are unchanged):

- A video request that names neither a generator nor coded motion now gets one short choice: prompts for a video generator the user runs elsewhere, or a finished MP4 built from code here, with designed sound on request. The main route table has a row for animated video built from text, logos, screenshots, data or product photos; the product-film route and the commercial video director hand such films to the Motion Graphics Workflow.
- The audio owner and the orchestrator no longer say Studio has no media engine: sound for a motion video built from a contract is designed, mixed and checked by the motion sound engine; songs, lyrics, voice, external tools, licensed tracks and supplied-audio review stay with the Audio Production Director.
- A rendered motion video with its contract is reviewed by the motion workflow's craft critique. The role and route contracts gain a `motion` review modality and four handoffs (orchestrator to motion, motion to QA, and both ways between motion and audio), and the roster describes the motion role as building and rendering, not only planning.
- The motion skill's delivery rules, one 2,138-character paragraph before, are now a short list, and its owners table names this skill for the video's own sound.
- Pipeline Core routes motion graphics from code to the Motion Graphics Workflow whatever the runtime and drops leftover kit installation text; its QA checklist no longer asks for a confirmation ritual.
- Six planned behavior cases cover the motion and sound route (`evals/motion-sound-cases.json`), validated for structure; none is executed.
- Smaller: the reply to an interactive-version offer has a named place in the Project State (`entry_context.interactive_offers`); the workstyle profile shows the pace menu in the user's language; development-status sentences are gone; the README files describe the motion MP4, its sound and interactive answers.

## 1.39.0, 2026-10-08

Checks and tools first, from the full review (the repository's docs/reviews/full-review-2026-10-08.md):

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

From an external audit of the repository by ChatGPT (GPT 6.1 Sol), with each finding reproduced before it was fixed (the repository's docs/audit-2026-10-08-response.md):

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
