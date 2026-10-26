# Historical development notes

## 1.145.0, 2026-10-26

Trigger: the owner's plugin-dev review of 2026-10-26 ([review](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/plugin-dev-skill-review-2026-10-26.md)), minor findings, fixed on the owner's go-ahead.

- **Routing wording:** Copy Voice no longer claims dialogue (Story And Screenplay owns it); Sales Campaign Strategy sends a static or mixed family's visual system to Visual Campaign; Audio analyses audio only through its named tools; Hipson routing and the self-improvement trigger stay explicit; Delivery names FrameCut's own review of its finals; Image Prompt says when a text-bearing raster stays there.
- **Consistency:** Graphic Design's direction count, the workstyle host list (Claude Code added), Hipson Handoff's ChatGPT metadata, display names instead of "Board/Sequence Architect" and "the Motion Graphics", and the client intake links lead with the user's language.
- Descriptions total 7,482 of 7,800 characters; the orchestrator is 31,867 bytes. Release gate 5/5 in headless Claude Code (plan usage); Codex and ChatGPT clients: NOT_RUN.

## 1.144.0, 2026-10-26

Trigger: owner decision 2026-10-26 after sending https://openverse.org: Openverse becomes Studio's reference base for images and sound, announced once at first configuration ([decision map](../integrations/openverse/README.md)).

- **[Openverse reference base](../skills/reference-pack-curator/SKILL.md#openverse-reference-base)** in Reference Pack, with Studio's own `openverse.py` (Python standard library, no key): images or audio usable commercially and modifiable by default, or an explicit licence list (`--licence cc0,by`); each work's licence, source page and attribution line for the asset manifest; share-alike and unknown-creator warnings; on a rate limit, an outage or an unexpected reply a JSON error with the openverse.org search link. Openverse has no video.
- **Routing:** every owner that sources pictures or sound points to it: Graphic Design, Image Prompt, Storyboard Board, Cinematography, Character Design (never a real person's identity), Motion Graphics (pictures for service reels, recorded sound), FrameCut (stills, b-roll, ambience, effects), Audio, Research and the orchestrator's picture rule. **Earshot 1.0.9** finds Freesound candidates through Openverse with `license=cc0,by`; its licence and consent policy is unchanged.
- **First configuration** says once, after the startup-style answer, that Openverse is the reference base and nothing is installed.
- Registry entry `openverse` pinned to WordPress/openverse `49f5b60`; NOTICE entry; `openverse_test.py`.
- Host evaluation in headless Claude Code (plan usage): OV01 to OV05 pass ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-26-1.143.0-gaps-OV01-OV02-OV03-OV04-OV05.json)); OV01 and OV02 failed on 1.143.0; OV01 passed 5 of 7 earlier runs while the wording was tightened; release gate 5/5. Claude apps, ChatGPT and ChatGPT Work reach to the API: NOT_RUN; startup check in ChatGPT: NOT_RUN.

## 1.143.0, 2026-10-26

Trigger: the owner's plugin-dev review of 2026-10-26 ([review](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/plugin-dev-skill-review-2026-10-26.md)), important findings 1 to 8, fixed on the owner's go-ahead.

- **Caption safe zone:** Caption Studio, the captions tool's help and README, the motion compendium, the channel specs snapshot and the motion review README now agree with the dated [platform caption specs](../skills/caption-studio/references/platform-caption-specs.md): bottom 35 % for every 9:16 Meta placement, organic or paid; 14 % is a readability floor, not a platform safe zone.
- **Coded-motion storyboards stay with Motion Graphics:** its description names the storyboard, and Shot Sequence no longer claims it and hands coded motion over explicitly.
- **Routing wording:** Copy Voice keeps one client email-kit rule (the client's language, translated from English); Studio Core's ChatGPT metadata no longer presents it as a router; Motion Graphics offers designed sound when wanted and makes HyperFrames the default for client reels on every shell host; Brand Strategy hands offers and product, store or marketplace launches to Sales Campaign Strategy; Visual Campaign and Reference Pack descriptions name their boundaries.
- Descriptions total 7,507 of 7,800 characters; the orchestrator is unchanged. Host evaluation in headless Claude Code (plan usage): new cases RV01 to RV03 pass ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-26-1.142.0-gaps-RV01-RV02-RV03.json)); RV02 failed before the fix, RV01 and RV03 also pass on 1.142.0; release gate 5/5. Fresh ChatGPT and Codex clients: NOT_RUN.

## 1.142.0, 2026-10-26

Trigger: owner decision 2026-10-26 on the open question from 1.140.0: option 2, sample details in mockups.

- **[Honest content](../skills/pipeline-core/references/craft-rules.md#honest-content-and-verification):** a page, app screen or product mockup may fill missing content with plausible samples (product names, menu items and prices, opening hours, interface data) so density and line lengths can be judged. Every sample is listed in the delivery note under "Sample details to confirm" and the mockup carries one small note ("Sample details, to be confirmed"; in Polish "Przykładowe dane do potwierdzenia"). Proof is never a sample: testimonials, ratings, review counts, customer or team names and faces, statistics, awards, partner logos and certifications stay real or labelled placeholders, and a sample never reaches a final asset, ad or published page.
- **Graphic Design** applies the rule to landing, product page and app mockups; the taste-skill decision map records the change. A new lint test keeps the note wording clear of the `filler-copy` rule.
- Host evaluation in headless Claude Code (plan usage): TS01 with its rubric updated passed 3 of 3; the recorded reply lists sample offer items and prices for confirmation, marks the mockup and invents no reviews, ratings or awards ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-26-1.141.0-gaps-TS01.json); before: [1.140.0 record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-26-1.139.0-gaps-TS01.json)). Fresh ChatGPT behavior: NOT_RUN.

## 1.141.0, 2026-10-26

Trigger: owner request 2026-10-26 to study [hairline](https://github.com/lucasmarkes/hairline) (Lucas Marques, MIT) and the owner's choice of option 3: a pinned registry entry, the method restated, and a video kit written for Studio. The repository was read as data at 37d2e78; none of its scripts was run and no file is copied except the licence.

- **[Hairline kit](../skills/hyperframes-workflow/assets/hairline/README.md)** in Motion Graphics: quiet isometric line figures built from rounded solids (one silhouette and one crease, no vertical corner), a brighter stroke as the only highlight, a composed rest with one bright mark, honest paint order and no words in the drawing. A planned tour of three to six stops takes the place of the pointer.
- **`hairline-kit.js`** (Studio's own code, no dependencies): rounded rings, hull and crease; the 30 degree or 2:1 view; and motion as pure functions of time: a 0.7 s ease-out redirected from the current value for choices, exact sums of closed-form spring step responses (k 100, c 18, m 1) for positions, stagger by distance and a clamped falloff. Seeking backwards gives the same values.
- **Example** `examples/spice-rack/`: two shelves of jars, 1080 x 1920, 8 s, with a HyperFrames timeline and `window.renderFrame(t)`; rendered through `capture-html.mjs` in about 35 s without a GPU (no glow); two renders matched in content (largest pixel difference 5 of 255).
- **Wiring:** Motion Graphics routes calm, glow-free isometric line films to the kit and opens its README and example first; capability card entry `hairline_kit`, a runtime-map row, wiring test and `hairline_kit_test.py` (7 tests).
- **Registry:** `hairline` (category motion-graphics) pinned to 37d2e78 through the skills CLI 1.7.2 (hairline-create and hairline-adopt) for Codex and Claude Code; knowledge-only routes for Claude apps and ChatGPT. Decision map and licence in `integrations/hairline/`; NOTICE entry.
- Host evaluation in headless Claude Code (plan usage): new case HL01 (gaps set) passed 3 of 5 at first (one English reply, one answer without reading the kit; [before](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-26-1.140.0-gaps-HL01-before.json)), then 4 of 4 after an explicit file-open instruction ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-26-1.140.0-gaps-HL01.json)). The HyperFrames render route and host install: NOT_RUN.

## 1.140.0, 2026-10-26

Trigger: owner request 2026-10-26 to study [taste-skill](https://github.com/Leonxlnx/taste-skill) (Leonxlnx, MIT) and the owner's choice of option 2: a pinned registry entry plus its methods restated in Studio's own words. The repository was read as data at 12af471; none of its scripts was run and no file is copied.

- **Craft rules:** headline fit and micro-typography (with the Polish no-break space after one-letter words), colour fields and warmth without the generated cream-and-terracotta look, a new section [frame, empty space and pictures](../skills/pipeline-core/references/craft-rules.md#frame-empty-space-and-pictures) (frame, rest versus hole, layout words, claims before layout, picture discipline, drawing the subject, real interface fragments, honest found pictures), one action one name, app screen data, interface furniture and motion honesty.
- **Review:** mockup look passes (one second then five, squint, cover the logo, edges, sameness, phone, fullness, collisions), a fix order and a round record in [review and repair](../skills/output-critic-iteration/references/review-and-repair.md#authored-design-review), without a score. The ideation method's subject inventory now asks for 8 to 12 facts, each also a reference query.
- **Checks:** `craft_lint.py` gains P1 rules `headline-length`, `index-numbering`, `eyebrow-cluster`, `micro-label-cluster`, `cream-terracotta`, `mono-prose`, `table-figures` and `motion-tells` (dose caps, not bans; skipped in video compositions) and more fake-person patterns; `ai_writing_check.py` gains `template-headline` and `interface-furniture` with Polish forms. New tests in `craft_lint_test.py` and `ai_writing_check_test.py`.
- **Graphic Design:** for a landing, product page or app screen mockup it opens the frame rules, writes the claims list and layout words first and runs the look passes on screenshots. Sample details presented as the client's are not adopted (Studio's honest-content rule stays).
- **Registry:** `taste-skill` (category design) pinned to 12af471 through the skills CLI 1.7.2 for Codex and Claude Code (its own marketplaces follow the default branch); manual knowledge-only routes for Claude apps and ChatGPT. Decision map and licence in `integrations/taste-skill/`; NOTICE entry.
- Host evaluation in headless Claude Code (plan usage): new case TS01 (gaps set) failed first (Graphic Design did not open the rules), then PASS after an explicit file-open instruction ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-26-1.139.0-gaps-TS01.json)). The pinned `--list` found the one skill; host install: NOT_RUN. Fresh ChatGPT behavior: NOT_RUN.

## 1.139.0, 2026-10-25

Trigger: owner request 2026-10-25 for a deep web mapping of the ideal JSON prompt structure for images and video, and then the same study for narrative (prose) prompts. Four research passes read the makers' own guides, API references and papers (sources and dates in each card).

- **What the evidence says.** Two image families are trained on a JSON caption format and document it (Bria FIBO, Ideogram 4.x); FLUX.2 documents a JSON template but says prose works as well; gpt-image, Gemini, Seedream, Qwen-Image and Midjourney document prose. No video maker documents a JSON prompt its model reads; real structure exists only as API fields (Kling multi-shot, Sora settings). No controlled test shows JSON beating equally detailed prose on a model not trained on it; JSON's value is completeness, a fixed order and changing one field at a time.
- **Image Prompt:** [structured image prompts](../skills/image-prompt-architect/references/structured-image-prompts.md) (one Studio planning record; Ideogram's and FIBO's schemas exactly as documented; the FLUX.2 template; pitfalls) and [narrative image prompts](../skills/image-prompt-architect/references/narrative-image-prompts.md) (clause order, length, exact text, edits, exclusions and rewriters for eleven model families). Graphic Design now opens the structured card for a JSON prompt; before the fix it answered from memory (host case JP01 failed, then passed twice).
- **Video Prompt:** [structured video prompts](../skills/video-prompt-architect/references/structured-video-prompts.md) (planning record, checks, compile targets per generator) and [narrative video prompts](../skills/video-prompt-architect/references/narrative-video-prompts.md) (sentence order, one action and one camera move per shot backed by measured multi-event failures, dialogue and sound per model, rewriters). The dialects card notes that the Veo 3.1 preview in the Gemini API was shut down on 2026-10-22.
- **[`prompt_record.py`](../skills/pipeline-core/assets/prompt-record/README.md)** checks a record (exact text, Ideogram box scale and colour limits, contiguous shots and durations, dialogue length, speakers, settings in prose, Kling limits) and compiles it to Ideogram native JSON, the FLUX.2 template, Kling custom multi-shot fields, Sora blocks, timestamped prose or plain prose in the narrative order. Standard library only; capability card entry `prompt_record`; 13 tests.
- Host evaluation in headless Claude Code (plan usage): new cases JP01, JV01, NP01 and NV01 PASS ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-25-1.138.0-additions-JP01-JV01-NP01-NV01.json)). No generator was run; fresh ChatGPT behavior: NOT_RUN.

## 1.138.0, 2026-10-25

Trigger: owner request 2026-10-25 to work recommendations 4 to 6 of the [2026-10-24 review](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/full-review-2026-10-24.md#room-for-new-skills-and-richer-references): English source versions of the client templates, a research method for Brand Strategy and production worksheets for Video Producer. Studio is a general product, so a client outside Poland must get a template written for them, not a translation of Polish legal wording.

- **English client templates.** Delivery Pack gains [`handoff-letter.en.md`](../skills/delivery-documentation/assets/handoff-letter.en.md) and [`acceptance-protocol.en.md`](../skills/delivery-documentation/assets/acceptance-protocol.en.md) (an acceptance record with jurisdiction-neutral identifiers and a note that copyright can be assigned only where the law allows); Copy Voice gains [`client-emails.en.md`](../skills/copy-voice/assets/client-emails.en.md). The owners, the client handoff reference, the offer reference and the client-project map pick the version in the client's language and translate any other language from the English one; the Polish files are unchanged.
- **Brand Strategy: [positioning and audience research method](../skills/marketing/references/positioning-and-audience-research.md):** eight questions in order, an evidence ledger whose status (verified, user-stated, inferred, unknown) decides what copy may use, audiences as situations, a tested positioning statement and a message hierarchy built from the ledger. No ready audiences, personas or industry facts.
- **Video Producer: [production worksheets](../skills/creative-video-producer/references/production-worksheets.md):** a schedule from the delivery date backwards with the critical path and review dates, a budget by line with the user's own rates (a line without a rate stays Unknown), six approval gates and what each locks, change control, a risk register and a status report.
- Host evaluation in headless Claude Code (plan usage): new cases EN01, MK01 and VP01 PASS ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-25-1.137.0-additions-EN01-MK01-VP01.json)). Fresh ChatGPT behavior: NOT_RUN.

## 1.137.0, 2026-10-25

Trigger: owner request 2026-10-25 to work items 2 to 4 of the next-steps list: the two dated references the [2026-10-24 review](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/full-review-2026-10-24.md#room-for-new-skills-and-richer-references) recommended, the unstable host cases G14 and OG02, and the roadmap state.

- **Caption Studio: [platform caption specs](../skills/caption-studio/references/platform-caption-specs.md)**, checked 2026-10-25 on the platforms' own pages: Meta's single 9:16 safe zone (top 14 %, bottom 35 %, 6 % each side; bottom 40 % for Reels ads with a disclaimer) with its pixel equivalents, TikTok's caption-dependent safe zone, sizes, lengths and text limits per placement, and the platforms' automatic captions next to burned-in ones. TikTok's overlay pixels, a YouTube Shorts safe zone and several limits stay Unknown. `readability-defaults.md` drops the unconfirmed secondary margins of 2026-10-08 and points to the card.
- **UGC: [disclosure by platform and market](../skills/ugc/references/disclosure-by-platform-and-market.md)**, checked 2026-10-25: the two-place rule (in the content and the platform label) plus a separate AI disclosure; Meta, TikTok and YouTube labels; Poland (UOKiK recommendations 2022 and the March 2025 decisions), the EU (UCPD guidance, DSA Art. 26, AI Act Art. 50 applying since 2 August 2026), the US (16 CFR 255 and Part 465) and the UK (the ASA, CAP and CMA guide of 23 October 2026, read through its landing page and a law-firm summary). It replaces the platform and law notes of 2026-10-08 in `formats-scripts-and-disclosure.md`. Not legal advice; the Unknown list is kept in the card.
- **G14** (a user who does not know the best route): FrameCut waited for footage before naming a route. FrameCut now names the recommended route and one contrasting direction in the first reply even before files arrive. Before: 1 of 6 recorded runs passed (2026-10-22); after: 4 of 4.
- **OG02** (a prompt for another coding agent): the model grepped the 700 KB gallery shard and ran out of turns, or skipped the prompt guide. Motion Graphics now tells it to open the library README's prompt guide with the file tool and then the gallery shortlist, never the shard. After: 4 of 4 runs, the gallery suite 3/3.
- Host evaluation in headless Claude Code (plan usage), recorded: [G14](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-25-1.136.0-gaps-G14.json), [gallery suite](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-25-1.136.0-opus-gallery.json), [PC01 and UD01](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-25-1.136.0-additions-PC01-UD01.json), all PASS. New cases PC01 and UD01 in the additions set. Fresh ChatGPT behavior: NOT_RUN.
- `docs/roadmap.md` current state brought to this release with measured budgets (descriptions 7,484 of 7,800 characters, orchestrator 31,851 of 32,000 bytes).

## 1.136.0, 2026-10-25

Trigger: the open follow-up in the [second-account handover](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/handover-claude-projects-second-account-2026-10-24.md) from 1.129.0: a storyboard-only request for a coded film named the Opus 5.5 gallery but postponed the lookup to the build (host case OG01 failed twice on 2026-10-24).

- Root cause from the recorded runs: the gallery is one 700 KB shard; the model either loaded only the skill and followed no link, or grepped the shard, could not pull usable entries and deferred the read.
- New [gallery shortlist](../skills/hyperframes-workflow/assets/motion-prompt-library/opus-gallery-shortlist.md): six records per brief type (97 in all, about 40 KB) with the mechanism note, the creator, the film link and the prompt link, generated by `node library.mjs shortlist --write` from the shard and the brief index; a Node test fails when it is stale, too large or carries prompt text.
- Shot Sequence now tells the model, for a film built from code, to open the shortlist with the file tool before writing the storyboard, in the same turn, and to credit at most three records under it; Motion Graphics step 2 points to the shortlist instead of the shard; the library README and knowledge wiring link it. No gallery prompt text is added.
- Host evaluation in headless Claude Code (plan usage): before, OG01 FAIL (read nothing, deferred); after, OG01 PASS in three runs, the suite 3/3 ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-25-1.135.0-opus-gallery.json)). OG02 is unstable: it failed once after the change and once on the unchanged 1.135.0 baseline (there by running out of turns), then passed. Fresh ChatGPT behavior: NOT_RUN.

## 1.135.0, 2026-10-24

Trigger: owner request 2026-10-24 (a bounded task): adopt the strongest ideas from a comparison with [social-motion-agent](https://github.com/aievolutionpl/social-motion-agent) (MIT) in the motion module; ideas only, no code or media copied.

- Motion Graphics: `acceptance.py --pack` writes a [delivery folder](../skills/hyperframes-workflow/assets/motion-review/README.md#delivery-folder) only for a film that is not blocked: the exact video and contract that were judged, the evidence, the render script or sources, `manifest.json` with every file's SHA-256 and `HANDOFF.md` with the status, the four verdicts, what was not verified and how to revise. A blocked film is never packaged; the acceptance result now records the contract and video SHA-256.
- Motion sound: [rules for supplied library samples](../skills/hyperframes-workflow/references/sound-listening-and-motion-sfx.md#where-sound-sits-against-the-picture): never at full level, lower under a voice-over, one sound per visual event, the same sample at most twice, the key spoken word left clear.

## 1.134.0, 2026-10-24

- Cinematography gains [camera and light decision cards](../skills/cinematography/references/camera-light-decision-cards.md): shot size, lens feel, angle, movement, light and colour chosen beat by beat, each with a reason and an observable QA test (review recommendation 1 of [the 2026-10-24 review](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/full-review-2026-10-24.md)). The skill description is unchanged.
- Repository: [tests/test_publish_release.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/tests/test_publish_release.py) covers the guard branches of `scripts/publish_github_release.py` (ambiguous release, tag on another commit, release from another source, partial upload on a published or draft release, changed or unexpected assets); deferred item from minor finding 19.

## 1.133.0, 2026-10-24

Trigger: owner request 2026-10-24 (a bounded task): let a user choose at first configuration whether Studio starts guided or plugs into their own workflow.

- New opt-in startup style ([startup style](../skills/workflow-orchestrator/references/startup-and-creative-menus.md#startup-style)). `guided` stays the default and keeps the complete welcome and menus. `workflow` answers a bare invocation with one ready line, keeps "menu" for the full welcome and skips the intent, area and pace menus for a creation request; concrete tasks bypass the welcome in both styles.
- First companion setup asks the style once, before the add-ons ([extensions](../skills/workflow-orchestrator/references/extensions.md#first-companion-setup)).
- The choice is `work_preferences.startup_style` in the workstyle profile; it is saved only with consent through a real per-user mechanism (Claude Code `~/.claude/CLAUDE.md`, Codex `~/.codex/AGENTS.md`, ChatGPT memory or custom instructions), with an honest conversation-only fallback.
- Validator check `STARTUP_STYLE`; host cases ST01 and ST02 in the additions suite (ST01 failed before the change, both pass after).

## 1.132.0, 2026-10-24

- **Fixes from the full review.** Owner instruction 2026-10-24 to fix every finding of the [full review](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/full-review-2026-10-24.md); the fix status is at its end.
- **Companions.** Voice And Narration 1.0.2 needs the script's language for Voicebox instead of defaulting to Polish; Brand Kit 1.0.1 checks each connection's real address against DNS rebinding; Earshot Audio 1.0.8 bounds its fallback download. A companion that changes without a new version now fails `check_version_bump.py`. The install guides and README name Voice And Narration and Brand Kit, and Studio's registry pins both to their fixed commit.
- **Storyboards in any language.** `board_compose.py` keeps the user's text exactly; Polish typesetting and „…” supers apply only to boards with `"language": "pl"`, and `labels` localizes Audio and Super.
- **Clearer owners.** Ad and brand-film scripts are named in Screenplay's description; polish goes to Humanizer, store campaigns to Sales Campaign Strategy, the shared visual system to Visual Campaign, the coded-motion storyboard to Motion Graphics; Claude Code is named in the shared contracts and the startup contract; Polish client templates say to translate and adapt them.
- **Repository.** The repository ZIP leaves out host-eval candidate snapshots (about 490 MB); `check_all.sh` prints validator errors; the release workflow skips a version already released from another commit; `release.py` pushes only `main`; AGENTS.md current rules and the roadmap follow the owner's 2026-10-24 rules; stray `edit*.py` scripts removed.

## 1.131.0, 2026-10-24

- **Brand Kit plugin.** Owner task 2026-10-24 (grow the "Brand kit manager" from the [companion proposals](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/handover-development-proposals-2026-10-24.md#4-future-companion-plugins-plan-only) into a website-to-brand-kit and voice asset; [design](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/superpowers/specs/2026-10-24-brand-kit-plugin-design.md), [plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/superpowers/plans/2026-10-24-brand-kit-plugin.md)). A new public plugin, `plugins/brand-kit` 1.0.0 (skill `brand-kit:brand`), collects bounded, robots-respecting evidence from a company website (colours with their use, font families, logo files, metadata, headings, CTAs, a copy sample), drafts a kit in Studio's own brand kit schema with a source ledger where unverified values stay `Unknown`, writes a brand audit with a voice and messaging profile, keeps approved kits as never-overwritten revisions per brand (`save`, `list`, `show`, `diff`) and offers a direction menu (new website ideas, ads and Meta Ads, video, brand development, content, spoken brand voice) handed to Studio's owners. Studio gains the registry entry `brand-kit`; no path was removed or moved.

## 1.130.0, 2026-10-24

- **Studio looks for a skill when a task needs one.** Owner request 2026-10-24. Besides welcome option `3`, Studio now searches the open skills.sh catalog by itself when a task needs a specific capability that no Studio skill or [recommended extension](../skills/workflow-orchestrator/references/extensions.md) covers. It offers at most three audited candidates once per need and asks one question: use once in this task, install, or continue without ([skill finder, section 6](../skills/workflow-orchestrator/references/skill-finder.md#6-during-a-task)). A declined offer is not repeated.
- **Use a listed skill once without installing it.** `find_skills.py --read owner/repo/skill` reads a `listed` skill's `SKILL.md` at a pinned commit, with its licence. It refuses skills that are not `listed`, contain an instruction override or a download piped to a shell, or are very long. Studio applies only the method and runs nothing from the skill.
- **More hosts.** ChatGPT Work runs the search script in its sandbox (no lasting install there). Ordinary ChatGPT and the Claude apps search through the host's web search and use a skill once only when its audits read low or safe. This replaces the 1.53.0 rule that skipped the search in chat hosts. Two planned evaluation cases (LM28, LM29) were added. Live catalog checks and host runs are `NOT_RUN`.

## 1.129.0, 2026-10-24

- **Opus 5.5 gallery in the motion prompt library.** Owner request 2026-10-24: Studio draws technique from [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) in its video workflow. All 703 entries at commit `92aee2f` become link-only records in [`specimen-opus-gallery.json`](../skills/hyperframes-workflow/assets/motion-prompt-library/specimen-opus-gallery.json), each with a Studio-written mechanism note, brief types and a prompt link pinned to the commit; no creator prompt text or media is copied (the MIT licence covers the compilation, the credits leave each prompt with its creator). Owner decision the same day: the gallery supplies technique after the idea is chosen from the brief, never the idea.
- A brief lookup lists up to three gallery records ranked by the brief's own words; search covers the notes; 16 records carry a `caution` (credential or settings instructions, real people, protected characters). Games and interactive pieces stay opt-in.
- New [prompt guide](../skills/hyperframes-workflow/assets/motion-prompt-library/README.md#writing-a-prompt-for-a-coded-film) for a coded film, written from reading the whole gallery: source of truth, format, idea and first second, beats, motion values, sound, determinism, things to avoid, review.
- Motion Graphics, Remotion and Storyboard Sequence Architect link the gallery and the guide; knowledge wiring, library validation and the canonical validator check the records; registry entry `awesome-opus-videos` (knowledge, manual, nothing to install); repository script `scripts/build_opus_gallery_shard.py` with `--check` for refreshes.
- Headless host evaluation (suite `opus-gallery-pl`, Claude Code, 8 case runs across four records in `verification/host-evals/2026-10-24-1.127.0-opus-gallery*.json`): OG02 (prompt for another coding agent) and OG03 (gallery record with a caution) PASS; OG01 (storyboard-only brief) still FAIL: the model names the gallery but defers the lookup to the build stage. Hosted ChatGPT plugin: `pending`.

## 1.128.0, 2026-10-24

- **Voice And Narration plugin.** Owner task 2026-10-24 (companion choice "Voice and narration" from the [companion proposals](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/handover-development-proposals-2026-10-24.md#4-future-companion-plugins-plan-only); [design](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/superpowers/specs/2026-10-24-voice-narration-plugin-design.md), [plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/superpowers/plans/2026-10-24-voice-narration-plugin.md)). A new public plugin, `plugins/voice-narration` 1.0.0 (skill `voice-narration:narrate`), turns an approved cue sheet into one WAV per line with VoxCPM2 (installed with consent at `voxcpm==2.0.3`, weights fetched separately with consent) or Voicebox on the user's own computer, or ElevenLabs through the host's connector (no API key). It applies a per-project pronunciation lexicon, measures every take against its line's limit, offers a consented speed-up of at most 5% and writes `narration.lock.json` for FrameCut or Motion Graphics Workflow. Local engines are advised against and their install refused without `--allow-cloud` in cloud or phone environments. Studio gains the registry entry `voice-narration` and one paragraph in Audio Production Director's local voice engines guide; no path was removed or moved.

## 1.127.0, 2026-10-24

- **Plain role names for the skills.** Owner decision 2026-10-24 (option "plain role names" on the [naming proposal](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/handover-development-proposals-2026-10-24.md#5-naming-proposal-for-owner-review--not-applied)). Thirty skills get shorter display names (for example Motion Graphics, Audio Production, Shot Sequence, Output Review, Copy Polish, Graphic Design, Brand Strategy); FrameCut stays and `workflow-orchestrator` displays as FrameCore Studio Guide. FrameMotion, FrameBoard, FrameCheck and FrameShot were not used because existing products in the same field carry them. Technical IDs, invocations, paths and routing are unchanged. Catalog descriptions, skill headings, routing tables and maintained references use the new names; the validator's display map and routing-boundary checks and the [naming standard](../docs/skill-naming.md) follow the approved list. Historical records and vendored snapshots keep their original names.

## 1.126.0, 2026-10-24

- Resolve the 28 independently reviewed audit findings with focused regression coverage for captions, image/PDF correctness, quotation/copy validation, wrapping, alternate-format motion acceptance and FFmpeg 9 decoding; the full regression also exposed and fixed FFmpeg 7 crossfade rate metadata.
- Require observed and bound media execution for C17 and ordered red/edit/green evidence for C20; repair portable installer/browser test expectations.
- Add language versions, website-derived draft brand kits, dated platform delivery cards and cross-deliverable accessibility evidence through existing owners.
- Register Hallmark as an optional complete native design companion, with pinned provenance and a narrow Codex metadata adapter. Keep full upstream resources separate from Studio.
- Record 12 source-guided mixed-routing observations and four reference cases, retaining the strict comparison-read failure. Preserve 37 owners and protected startup; publish naming and future companion proposals for owner selection.

## 1.125.2, 2026-10-23

- **Earshot credited to Leon Lin.** Owner decision 2026-10-23: [first companion setup](../skills/workflow-orchestrator/references/extensions.md#first-companion-setup) presents Earshot as Leon Lin's open-source project packaged by FrameCore Works; `earshot-audio` 1.0.7 starts its manifest descriptions with the credit and shows "Earshot (Leon Lin)".

## 1.125.1, 2026-10-23

- **Review fixes (Earshot and Superpowers integration).** Trigger: an independent review on 2026-10-23. `listen.py`'s Earshot bridge always runs offline with the plugin's cache and refuses `doctor --fetch`; `earshot-audio` 1.0.6 fails an installation whose upload stub cannot be applied; setup states what is written and where; the last references to a second Earshot route are removed from the owners and routing references.

## 1.125.0, 2026-10-23

- **One setup offer on every host.** Owner request 2026-10-23. [First companion setup](../skills/workflow-orchestrator/references/extensions.md#first-companion-setup) offers Superpowers, then explains Earshot in plain words and asks full (about 2.6 GB), light (about 200 MB) or not now; the answer is the consent, and the plugin and tier are installed in the same conversation where code runs, with blocked hosts named. [CLAUDE_INSTALL.md](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CLAUDE_INSTALL.md), [CODEX_INSTALL.md](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CODEX_INSTALL.md) and [CHATGPT_INSTALL.md](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CHATGPT_INSTALL.md) end by entering that setup.
- **One Earshot.** The registry entry `earshot` routes every host through the `earshot-audio` plugin and its `runtime.py` (no separate pip installation); stale 0.3 descriptions are corrected ([integration note](../integrations/earshot/README.md)); `listen.py`'s model commands run the plugin-installed engine offline with its cache and without API keys, and refuse `llm` and `mcp`.
- **Superpowers for Earshot's code.** [Sound with Earshot](../skills/pipeline-core/references/superpowers-native-routing.md#sound-with-earshot), the Motion Graphics owner and `earshot-audio` 1.0.5 load `writing-plans`, `test-driven-development`, `systematic-debugging` and `verification-before-completion` for the code around Earshot. Host evals C14, C18, C19 and C20 failed before and pass after.

## 1.124.4, 2026-10-23

- **Effects chosen by listening.** Trigger: the owner's listening report on 2026-10-23 (a preset's landing hit with a metallic debris tail; Earshot read it as 11.8 onsets per second, losing to "metal debris / rattle"). The public `earshot-audio` 1.0.4 skill chooses every effect from a description built from the picture and the request: candidates ranked, the pick matched against likely confusions, onsets per second and speaker-audible bands measured, as gates rather than trade-offs, with readings and rejected candidates reported. The [Motion Graphics owner](../skills/hyperframes-workflow/SKILL.md) and [native Earshot routing](../skills/pipeline-core/references/earshot-native-routing.md) ask for such takes. Host eval C17 failed before and passes after.

## 1.124.3, 2026-10-23

- **A missing Earshot engine is a choice, not a silent fallback.** Trigger: the owner's ChatGPT Work test on 2026-10-23, where earshot-audio was listed without its engine and Work made the sound with `sound.py` without asking. Owner decision (option A): [native Earshot routing](../skills/pipeline-core/references/earshot-native-routing.md), the [Motion Graphics owner](../skills/hyperframes-workflow/SKILL.md) and the public `earshot-audio` 1.0.3 skill ask one question with both routes (Earshot's light tier, about 200 MB, or Studio's own engine), run neither before the answer and name the engine that ran. Host eval C16 failed before and passes after; C09 and C10 still pass.

## 1.124.2, 2026-10-23

- **Earshot light tier described correctly.** Trigger: defect seen in an end-to-end run on 2026-10-23 ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/earshot-audio-1.0.2-e2e.json)). The registry's `earshot` entry no longer lists `timeline` as a light-tier command (it always loads the CLAP model); `timeline`, `sheet` and the full `critique` need the full tier. The public `earshot-audio` plugin 1.0.2 makes the same correction in its skill, says how to check sync from measured onsets on the light tier, and names where `runtime.py` is. Before: 24 turns and two failed `timeline` calls; after: 17 turns, sync within one frame on the encoded film.

## 1.124.1, 2026-10-23

- **Earshot Audio is the second setup recommendation.** Owner request 2026-10-23. The registry entry `earshot` carries `recommendation_priority: second` (the validator accepts `first` and `second`, one of each), and [first companion setup](../skills/workflow-orchestrator/references/extensions.md#first-companion-setup) gains step 6: after Superpowers, load `earshot-audio:earshot` if it is listed, otherwise offer the host's install step once, without running any installer. Host eval: new case C14 (Superpowers only) failed before and passes after; C15 (both plugins) recognises an installed Earshot Audio; C05 now fails only on a Superpowers install command.
- **Install guides.** [CODEX_INSTALL.md](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CODEX_INSTALL.md) and [CHATGPT_INSTALL.md](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CHATGPT_INSTALL.md) gain "Second recommended companion: Earshot Audio"; the [Claude guide](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CLAUDE_INSTALL.md) section is renamed to match and names the folder.
- **Host eval tool.** `scripts/host_eval.py` resolves `--with-plugin` to an absolute path: Claude runs in the case's temporary workspace, so a relative path loaded no companion while the record listed it.

## 1.124.0, 2026-10-23

Trigger: the owner asked to publish Earshot for every user beside Studio, built from upstream `main` and merging upstream's two skills. This repository's marketplace now lists a second plugin, `earshot-audio` 1.0.0 (`plugins/earshot-audio`), built on Earshot v0.4.0 by Leon Lin (MIT, commit `591fa3e`): one skill, `earshot-audio:earshot`, joins listening (describe, match, rank, find, compare, ab, realness, timeline, sheet, critique, measure), making sound (the 252-sound bank with the `launch` preset, kits with measured anchors, forge, fit) and upstream's real-sound process, whose scripts, references and templates are copied byte for byte. A standard-library launcher checks readiness without writing, installs the engine only after the user agrees, from the pinned commit with all 282 files checked, keeps runs offline in its own cache (`exec` for scripts and briefs), refuses `llm` and `mcp`, replaces those two engine modules with a stub and passes no API keys; models are a separate agreed step. Internet recordings are fetched only on request, with upstream's licence audit and credits. Studio's `earshot` registry entry moves to v0.4.0 and names the public plugin as the first route in Claude Code and Codex, the pinned command line staying as the route without it. Evidence: launcher and package tests fail before and pass after; in a Linux container the light tier installed from the pinned commit (40 s), a whoosh rendered with its apex at 0.3205 s for 0.32 s, the launch kit rendered 72 of 72 clean takes, `measure` ran, and upstream's suite passed 773 tests (failures only in the excluded MCP and LLM interfaces and the full tier); the full tier was not run there because the PyTorch index was blocked. Companion cases with Studio, Superpowers and earshot-audio in Claude Code: before 1 of 4, after the fixes C10 to C12 pass and C09 loads Earshot in 2 of 3 runs. A fresh review found five important issues; four were fixed with failing-first tests and one (C11's scope) is the owner's decision. Fresh ChatGPT and Codex behavior is NOT_RUN.

## 1.123.2, 2026-10-22

Trigger: the owner's Earshot handover and the files of the hosted 1.122.1 plugin, whose Earshot routing had never reached the repository; an update from the repository would have overwritten it. Studio now routes sound work to the owner's separate native plugin `earshot-audio` (skill `earshot-audio:earshot`) through `pipeline-core/references/earshot-native-routing.md`, the shared policy and the QA loop, and Motion Graphics, FrameCut, Audio Production Director and Remotion name that skill directly, because a link alone is not read in a single-turn run. Corrections to the hosted version: Claude Code and Codex users without the private plugin keep the pinned `earshot` command-line install (the hosted entry had replaced it with a path inside that plugin), and every fallback names the engine that actually ran; Earshot is local only, with no Gemini upload and no MCP server, as the handover decided (the hosted entry still allowed an upload after consent); the 2026-10-20 decision map and its measured differences stay. The private overlay lines in the same hosted files (motion, engine and media runtimes, session runtimes, app bindings) are not published. The orchestrator is unchanged. Evidence: a source test fails before and passes after; host evaluation in Claude Code without the Earshot plugin (G15) offers Earshot only if available, falls back to Studio's sound tools and keeps audio local; the Studio and Superpowers companion cases still pass 5/5. The pair with Earshot was not run here, because the plugin is not available in this environment; its runtime evidence comes from the owner's ChatGPT Work run and is reported, not rerun.

## 1.123.1, 2026-10-22

Trigger: the owner asked to find and fix the gaps between Studio and the Superpowers companion so the pair works in Claude as well as ChatGPT. Studio's host evaluations ran Claude Code with an isolated configuration and never loaded Superpowers, so the pair had no repeatable test; `scripts/host_eval.py --with-plugin` and the new `companion` suite (eight cases) now run both plugins together. Root cause found with them: a Studio owner used a Superpowers skill only when its own `SKILL.md` named it; the link to the shared routing reference is not read in a single-turn run, and 31 of 37 owners did not mention Superpowers at all. Thirty-six owners now name `superpowers:systematic-debugging` for a reproducible technical defect and `superpowers:verification-before-completion` before a deliverable is called ready, while Studio keeps ownership (the orchestrator routes to them and keeps its byte budget). A second gap, independent of Superpowers but made more frequent by its start-up hook: a request without the Studio name reached Creative Video Producer, which asked up to nine questions and did not send the user's own footage to FrameCut; it now does, with at most one question. Before: FrameCut timing defect 0/3, caption defect 0/1, unnamed footage reel 0/5 (0/2 without Superpowers). After: companion suite 8/8, release gate without Superpowers 5/5, G13 and RT22 pass; G14 stays unstable on unchanged text. Brainstorming wrote no design document in any run. Fresh ChatGPT behavior is NOT_RUN.

## 1.123.0, 2026-10-22

Trigger: the Open Design 0.26.0 review in the 2026-10-22 handover (item 1). Delivery mechanics and a few rules are adopted; no Open Design code or text is copied. `flash_check.py` screens a rendered video for photosensitivity risk: 30 fps sampling (24 to 30), relative luminance, flashes counted as pairs of opposing changes of at least 0.10 with the darker side below 0.80 over a quarter of the frame, REVISE above 3 flashes in any second; it is labelled screening, not WCAG, Harding or broadcast conformance. FrameCut's `transcribe` and `import-transcript` return `warnings` for music notes or unreadable characters above 20 %, word spans under 0.05 s and three identical segments in a row, and an English-only `*.en` model refuses another language before decoding. `inspect-encode.py` gains `--audio required|silent` (volumedetect peak against -80 dB) and `--cover-time` (the exact frame, refused outside the film before anything is written), recorded in `evidence.json`. The `open-design` extension now pins release 0.26.0 (`bfee093`) with installer SHA-256 values, never the `curl | sh` installer, the Share, telemetry, MCP write-tool and loopback warnings, and a decision map with the Apache-2.0 licence in `integrations/open-design`; Studio's adapted craft rules and prompt examples are unchanged upstream. Smallest edits in the owning texts: a flash and strobe limit, "the transition is the exit", right-to-left and complex scripts, beat-envelope restraint, right-to-left captions, transparent Remotion overlays for FrameCut, a pilot before a batch, a 360 spin in quarter turns, FrameCut pacing and closing steps, the next-best route after a declined add-on, plain failure messages. The orchestrator file and skill descriptions are unchanged. A fresh whole-change review found three issues, fixed before release with tests that failed first: a cover recorded although no frame was written, flash screening memory on long films (0.5 GB instead of 2.6 GB for 2 minutes of 720p) and quantized English-only model names. Installer checksums were re-read from the release assets on 2026-10-22. Tests fail before and pass after (`flash_check_test.py`, `inspect_encode_test.py`, new FrameCut and registry cases). Host evaluation in headless Claude Code before and after: G13 and RT22 pass; G14 is unstable on unchanged text (it failed once before and once after). Fresh installed-client behavior is NOT_RUN.

## 1.122.0, 2026-10-22

Trigger: the owner approved Superpowers as the first recommended, separately installed Studio companion and requested repository-first implementation followed by the existing ChatGPT plugin update. Studio now exposes a setup action through the existing orchestrator, recommends manual host-catalog installation before other add-ons, preserves declined/deferred choices and checks readable skills before claiming activation. All 37 owners inherit one native support contract; six technical entry points link directly. Creative direction, full-board acceptance, one master timeline and one QA loop stay with Studio. The registry supports catalog_manual without fake shell installers or marketplace version pins. No upstream skills, accounts or connectors are bundled. Focused regression tests fail before and pass after; five before/after source-guided scenarios and independent review are recorded separately from fresh installed-client behavior, which remains NOT_RUN.

## 1.121.0, 2026-10-22

Trigger: the owner sent Pixel Plugin and asked for its best ideas to be taken into Studio before it was listed. Two read-only analyses (its four skills, and the pixel-mcp engine source) found a thin Aseprite wrapper whose game-development content Studio should not take, plus a few real gaps. FrameCut gains three versioned picture effects for a pixel look on supplied footage: `pixelate` (whole-pixel blocks, box-averaged down and nearest-neighbour up), `posterize` (levels per channel) and `ordered_dither` (a 4x4 Bayer tile pinned to screen coordinates, so it does not crawl on video; error diffusion is deliberately absent). Their defaults leave a clip unchanged, they take 30 to 40 ms per 1080x1920 frame, and the effect fixtures now accept a few painted pixels and a read position. Studio's Animate reference gains a Pixel look section (the engine's own pixel style file stays byte-identical to its pinned source) with hue-shifted colour ramps without pillow shading, colour-count tiers and palette swaps by role, a rule for choosing the dither and keeping it stable on motion, action timing in render frames, and a section on a user's own pixel sprites (whole-number nearest-neighbour scaling). Pixel Plugin itself is listed as a Claude Code extension that needs the user's Aseprite, with its five unverified prebuilt binaries flagged; the engine's own algorithms were found weak in places and are not adopted. Decision map: `integrations/pixel-plugin`. Sandbox tests only (`tests/framecut_pixel_test.py`, failing before); the plugin, Aseprite and its tools were not run.

## 1.120.0, 2026-10-22

Trigger: the owner asked to take the best ideas from MoneyPrinterTurbo for FrameCut. A read-only review of its code (nothing was run) found little editing intelligence to adopt, but three methods that fill real gaps and were verified offline. `align-script` aligns a known script to a timed transcript: the script is the authority on spelling, names and diacritics, the speech on timing; words are matched with case, punctuation and diacritics folded, a word between two matched neighbours is interpolated by its length, a word without anchors stays untimed and is listed, and a script that barely matches the speech is refused, with a coverage report. FrameCut's caption cues now break through Caption Studio's own rules (a finished sentence, punctuation, a clause start or a pause, never after a one-letter word of the brief's language). A caption font that cannot draw a character of the text gives the blocking `font_missing_glyphs` warning, so Polish letters never burn as boxes. The color pipeline idea was checked and is already correct (a known colour measured within two levels of its source). The decision map in `integrations/moneyprinterturbo` records what was adapted, what already existed and what was not adopted. Sandbox tests only (`tests/framecut_script_test.py`, 11 cases, failing before); fresh installed-client behavior is NOT_RUN.

## 1.119.5, 2026-10-22

Trigger: the owner's observations from real use. Asking for storyboard acceptance had quoted the plugin's own FrameCut SKILL.md to the user in ChatGPT, and a user who did not know what was possible got the simplest route with no hint of Studio's kits or installable add-ons. The orchestrator now forbids quoting or naming Studio's files, skills or rules to justify a question, and sends footage that needs a diagram or animation to FrameCut. FrameCut asks for acceptance in plain words about the user's result and aims for the strongest result: it compares Studio's own kits with add-ons from the recommended extensions, recommends one route in the user's terms and offers a missing add-on once, for this project only or kept; one yes covers the plan, install and check, nothing is installed before it, and a declined offer is not repeated. Motion Graphics applies the same check, and the extension route and AGENTS.md now allow proposing an extension, not only installing on request. Evidence: headless Claude Code, plan usage. Case G14 loaded only the orchestrator and gave one simple overlay plan before; after, FrameCut loads and offers two contrasting directions with a trade-off. Case G13 passes before and after: the ChatGPT wording leak does not reproduce in Claude Code, so that fix rests on the owner's screenshot and a guard. Fresh ChatGPT behavior is NOT_RUN.

## 1.119.4, 2026-10-22

Trigger: the owner sent MoneyPrinterTurbo for review, which adds it to the recommended extensions. The entry is pinned to commit 6992380 and the PyPI package `mpt` 1.3.9 and is native in Codex and Claude Code through a virtual environment (not supported in chat hosts). It turns a topic or script into a finished short video with stock footage, voice-over, subtitles and music. Studio keeps the brief, script, claims and review. The decision map and licence are in `integrations/moneyprinterturbo`. Rights notes in the entry: the bundled background songs are described by the author as taken from YouTube videos, so they must not be published; the project's own agent skill is rejected for Studio because it installs without asking and fetches its helper unpinned; its API server listens on all interfaces by default, so only the CLI or the loopback WebUI should be started. Evidence: static review, matching published hashes, the wheel's code identical to the repository, the dry-run plan and a successful install in a fresh virtual environment. The program itself was not run (the container blocked executing the downloaded package), so its CLI and generation are NOT_RUN.

## 1.119.3, 2026-10-22

Trigger: the owner's decisions on the FrameCut audit. Music on the music bus is now lowered 6 dB under speech by default, with smooth ramps that follow the timed transcript (the clip's whole extent when there is no transcript); `duck_db` sets another amount and `0` keeps the music level. Before, a bed under a continuous talking-head cut was ducked through the pauses only when `duck_db` was set, with an abrupt step. The storyboard remains a host-managed preview shown once for acceptance, with another only when the user asks; changes the user did not request still need their approval. Measured on a 6 s talking clip with a music bed: about -6 dB under the words and full level in the pause. See the [audit record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/framecut/audit-2026-10-22.md).

## 1.119.2, 2026-10-22

Trigger: the owner's request to check FrameCut thoroughly. Four independent reviews of 1.119.1 (real media, storyboard and jobs, adversarial robustness, guidance) found defects; each fixed one was reproduced and now has a test that fails on 1.119.1. Captions are no longer switched off by a partial `set_captions`; a spoken word without timing blocks a final instead of vanishing from the captions; `analyze` works on very short clips; linked audio is no longer shifted at 1x; a revision over the read limit can no longer brick a project; hand-edited probe values can no longer reach ffmpeg filter graphs; a preview bundle can no longer be reviewed to READY; file names and notes can no longer forge EDL lines or CSV formulas; a source swapped during a render is not cached; a render lock left by a killed process is reclaimed and SIGTERM cleans up; outputs cannot target the runtime's own files; errors are typed and say what failed. FrameCut guidance, orchestrator routing and stale design documents were corrected. Seven product decisions (runtime enforcement of the storyboard gate, per-deliverable caption settings, render speed and others) and the remaining lower-priority findings are listed in the [audit record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/framecut/audit-2026-10-22.md). Sandbox media evidence only; fresh installed-client behavior is NOT_RUN.

## 1.119.1, 2026-10-21

Trigger: host evaluation G12 on 1.119.0. A Polish request for a shoemaker reel with no photos loaded only the workflow orchestrator and planned a shoe drawn in code, reproducing the owner's 2026-10-16 defect. The orchestrator now sends a service, product or before-and-after reel to Motion Graphics Workflow before the plan, with the picture rule and the first-second test, using the budget freed in 1.119.0. After the fix the same request loads Motion Graphics Workflow, refuses a code-drawn realistic object, offers generated or phone pictures, names a text-only reel as the weaker fallback and opens with a full-frame hook. Evaluation case AD01 now expects English for a bare option number with no language signal, as the automatic-language rule requires. See the [host-evaluation records](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/host-evals/2026-10-21-1.119.0-gaps-G12-after.json).

## 1.119.0, 2026-10-21

Trigger: the owner's verdict on the 2026-10-16 shoemaker test reel ("I would not give this reel to a client; it is not striking and says little"; uneven check mark, weak drawn shoe). Reel plans now apply a stopping test (what fills the screen in the first second, the one big moment, a reason to choose this business) and a picture rule: a service, product or before-and-after reel needs the client's or generated pictures, a realistic object is never drawn in code, and a type-only reel is named as a weaker fallback before building. The rules sit where reel requests actually route (Creative Video Producer, Motion Graphics Workflow, the reel board system and the ideation method); boards keep changing inside themselves and the finished reel is compared with reference reels before delivery. Acceptance of a HyperFrames or hand-written composition binds its text audit to the composition's own SHA-256 (`--composition`), checks the locked copy (`--copy`) and counts a `motion_activity.py` measurement bound to the encoded file's SHA-256 (`--motion-activity`) in the temporal verdict. A landing marked in the motion score is never designed silent. The orchestrator's coordination detail moved verbatim to [routing boundaries](../skills/workflow-orchestrator/references/routing-boundaries.md#coordination-detail), freeing about 930 bytes of the entry skill's budget; startup, the welcome and the routing table are unchanged.

## 1.118.0, 2026-10-21

Owner-requested adaptation of Adobe skill methods without Adobe accounts or services. Connect multi-format variants, batch finishing, local typography/templates, website brand/content evidence, document review, supplied-data reasoning and editorial selection to existing Studio owners. Preserve the full FrameCut board gate, existing skill IDs/startup and private hosted integrations. No Adobe connector, upstream suite installation, proprietary renderer or premium entitlement is added. See [bounded scope](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/adobe-account-free-2026-10-21.md).

## 1.117.0, 2026-10-21

The owner requested supplemental knowledge from the reviewed Motion/Dashboards and Taste articles. Connect source-bound data storytelling and revision-bound panel/frame feedback to existing owners; refine creative judgment, optional diversity exploration and scoped taste applicability. Preserve full visual-board acceptance, exact locks, optional requested samples, startup and private integrations. Primary-source limits distinguish model estimates from measured novelty and Claude product features from Studio capabilities. No new runtime, dashboard service, comment UI or provider integration. See [scope](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/creative-knowledge-2026-10-21.md).

## 1.116.0, 2026-10-21

The owner requested all six recommended Concat-inspired FrameCut features inside the existing workflow. Original native implementations add composited frame previews and complete structural storyboards with authored action beats, transactional stable-ID editing with dry-run impact, durable cancellable/resumable jobs, transform/gain keys and per-format framing, freeze frames and variable speed, and nine versioned declarative effects. Shared source/time maps, revision/source hashes, bounded resources and explicit export losses preserve existing editing contracts. FrameCut, Storyboard Board Architect, Motion Graphics Workflow and Project State instructions are connected to the native commands. Full-board feedback/acceptance still precedes final rendering; samples remain optional on request.

No Concat code or model dependencies are bundled. Variable-speed audio changes pitch; process-death detection is Linux-specific. Sandbox contracts, decoded media and a fresh-context workflow exercise are tested separately from fresh installed-client behavior, which remains NOT_RUN. Private hosted configuration is preserved by a guarded repository-first update. See [scope](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/framecut/concat-development-scope.md) and [implementation status](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/framecut/build-status.md).

## 1.115.0, 2026-10-21

FrameCut now follows onboarding and consequential questions, complete visual storyboard/contact sheets of the entire film, user feedback and corrected-board acceptance, then final rendering and review. Panel count follows actual scene and meaningful-state coverage; readable pages show key images, exact copy, timing, motion, transitions and sound cues. A video sample is optional on request. Carry board revisions, coverage, pending feedback and actual acceptance through the existing project state and stage-scoped storyboard/motion handoffs. Resume unchanged accepted boards without repeating intake or approval. This corrects the prior sample-first workflow and preserves runtime media behavior, welcome and private integrations. See [workflow evidence](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/verification/framecut-storyboard-2026-10-21.json).

## 1.114.0, 2026-10-21

FrameCut gains adaptive onboarding with brief, relevant explanations of effects and HyperFrames/Remotion, a working agreement reused by specialists, representative style proofs and staged finishing. Clarify editing/cutdown ownership and separate translation from source-word correction. Validate returned motion against its originating edit context and actual media; expose delivery readiness separately from technical PASS. Preserve the complete welcome and existing private integrations. See [FrameCut build status](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/framecut/build-status.md) for measured scope.

## 1.113.0, 2026-10-20

FrameCut is now the executable editing mode in the full welcome (option 5), using the existing opencut-video-studio ID. It takes an adaptive brief through source analysis, editable timeline, captions, motion/audio finishing, revisions and verified delivery. The standard-library/FFmpeg runtime provides exact source clocks, immutable revisions, source-bound transcripts, kinetic captions, motion placements, independent audio, cache recovery and explicit interchange losses. Existing caption, motion, audio and project owners share one timeline.

Sandbox agents exposed and verified fixes for stale anchored audio, undo dropping locks and invalid lock state; formal coverage also guards transition handles. Three media workflows, rational/VFR/offset clocks and optional OTIO round-trip have actual evidence. The existing 59-component install/update inventory is retained. Full playback/listening, Polish alignment accuracy, native editor import and fresh installed-client behavior are not certified by these tests. See [FrameCut build status](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/framecut/build-status.md).

## 1.112.0, 2026-10-20

The owner requested a complete first-install and every-update check for the supplied Work tool configuration.

- Add a 59-component inventory with reported reference versions, executable/import/package evidence, isolated Python discovery, and separate Whisper/OCR model hashes.
- Make the complete offline inventory the default, `--final` and `--update` path. Retain the former project capability check behind `--capabilities-only`.
- Disclose missing-tool installation and repair plans before execution, reuse applicable authorization, preserve working versions, and recheck afterward.
- Verify each actual host independently. Shared Work runtime variables no longer identify a client as Codex.
- Add regression coverage for incomplete npm packages, failed probes, isolated environments, model identity and installation-plan behavior.

All 59 components passed installation probes in the current Work environment. Cross-host installs, fresh-client startup, renders and model inference were not run.

## 1.111.1, 2026-10-20

Close the interrupted 2026-10-20 repository audit before the next feature task.

- Exact-copy review preserves currency, punctuation, case and contact details while allowing Unicode NFC and line wrapping.
- Audio analysis keeps mono amplitude, consistently selects the first audio stream, bounds tempo sampling and respects supplied reference profiles.
- Print preflight validates the PDF Trapped name; frame review uses fractional glyph widths; cached HyperFrames probing stays offline.
- Web reach checks redirects and validates the numeric addresses used for each connection, with HTTPS hostname verification preserved.
- Startup, supplied-film audio routing, renderer delivery and QA ownership agree across active instructions.
- Release provenance follows the actual development surface; suite summaries retain their names. Future host evaluations bind results to a content hash and retained candidate archive.
- Version 1.111.1 aligns the public source with the existing private hosted installation after its separate 1.99–1.111 integration updates. Private connections and supplemental runtimes remain preserved, outside the public repository.

Fresh source and sandbox media checks are recorded in verification/closure-2026-10-20. The old 43-scenario report was not recovered and is not treated as fresh evidence. No paid provider generation or fresh-client startup evaluation was performed.

## 1.98.0, 2026-10-20

At the owner's request, earshot (Leon Lin, MIT) joins the recommended repositories and its capabilities are added next to Studio's sound skills. The model-free half is rewritten as Studio tools; the model half and the sound bank stay in the pinned extension:

- **Hear the film.** `sound-listen/listen.py` (NumPy and FFmpeg only) measures loudness, true peak, spectrum, stereo, onsets, tempo and key; lists what sounds when next to the cuts; scores every cut or cue for a sound within 100 ms; audits one sound for clicks, a cut tail, clipping, DC offset and pitch glide; compares two sounds; scores a soundtrack against launch-film ranges with timed fixes (or against the user's own `profile`); draws an annotated sheet. Model commands pass through to the extension when it is installed
- **Place sounds on frames.** `place_sfx.py` aligns the measured attack, peak or end of any sample the user may use to a cue time or frame, mixes with the video's sound or a bed, holds the true peak under a ceiling (also after the AAC encode) and re-renders each sound alone to confirm it sits within 5 ms of its cue
- **Craft in Studio's own words.** `references/sound-listening-and-motion-sfx.md`: the listening loop, where hits sit against a cut, what whooshes, risers, impacts, stings, pops, pop-ins, clicks, typing and zips are made of, and the honest limits
- **Registry.** `earshot` (category audio) pinned to 925ebe5 with a light tier (measurements, `sfx`, `kit`; no models) and a full tier (CPU PyTorch, about 1.1 GB models) for `describe`, `match`, `rank`, `find`, `compare`, `realness`; manual consent for the audio-LLM critique. Native on Codex and Claude Code; not supported in chat sandboxes
- **Wiring.** Motion Graphics runs `listen.py critique` and `sync` after mixing; Audio Production Director reviews supplied audio with numbers first; capability card entries `sound_listen` and `sound_place`, runtime-map rows, wiring test, a new test (`sound_listen_test.py`) and host-eval case AD14 (not run)
- **Limits recorded.** Native band levels, onset density and tempo are approximations of earshot's (earshot is the reference); the scorecard ranges come from SaaS launch films; a passing scorecard is not a good film

## 1.97.0, 2026-10-20

At the owner's request, OpenCreator (krillinai, formerly KrillinAI, Apache-2.0) joins the recommended repositories; nothing from it is bundled:

- **Registry.** `opencreator` added (category video), pinned to release 3.2.8 (commit f4dbed1) with the SHA-256 of the macOS (Apple Silicon and Intel) and Windows installers. It is a desktop app around Codex CLI that translates and dubs videos, generates thumbnails, images, video and voice, and makes stick-figure animations. Manual on Codex, Claude Code and Claude apps (the user installs it on their own computer); not supported in ChatGPT and ChatGPT Work
- **Limits recorded.** Its 108 prompt templates belong to named outside authors and carry no licence, so Studio does not reuse them; downloading other people's videos is outside Studio's scope; media services need the user's own keys and cost money

## 1.96.0, 2026-10-19

At the owner's request, after a 16.7-second Knock Knock reel (children's woodworking classes) was built in Claude Code from two reference reels and approved in four review rounds, Studio records how to make dense kinetic reels and how to keep every scene logical:

- **Dense kinetic reels.** [Dense kinetic reels](../skills/hyperframes-workflow/references/dense-kinetic-reels.md): the structure of a brand showreel (chat or notification hook, the brand's carrier launched by an action, three to five offer boards in kinetic type, a summary in the brand's lettering, payoff in the same chat, logo assembled from its parts), measured cut rates and still shares, and build and sound notes. A blueprint row joins the reel board system
- **Brand first.** Colours, type, characters and objects come from the brand's logo and kit, never from a reference; a reference teaches a mechanism. Tempo follows the audience
- **The carrier.** One element of the logo travels through the boards; when it replaces a letter it is drawn as a vector glyph at the type's weight, larger than the letters and centred with even spacing, never a raster cut-out
- **Scene logic check.** Each object does its real job on its material, seen from the side that shows the result (a drill into a board's face, a saw in its kerf, a hammer on a nail head), with a visible result, and the next board grows out of that result (the camera flies through the bored hole). It is the development review's new question 6, a QA record row, a step before building in Motion Graphics and a check on shot cards in Storyboard Sequence Architect
- **Reading time.** About 0.75 s between short chat messages and at least 0.8 s on the last one before a scene change
- Repository: knowledge-wiring rows (a heading link now counts) and host-eval case AD13 (not run)

## 1.95.0, 2026-10-19

At the owner's request, Upscayl (upscayl/upscayl, AGPL-3.0) joins the recommended repositories with an upscaling route in Studio:

- **Upscaling route.** [Upscaling](../skills/static-graphic-design-creator/references/upscaling.md) in Static Graphic Design Creator: measure the effective resolution with `image_probe.py`, prefer a better source, enlarge the clean image before text and logos are composited, inspect faces, hands and product edges at 100 %, and report the tool, model and factor. Linked from the static owner, the print presets, print-ready PDF delivery, format adaptation and the routing boundaries
- **Model licences.** For paid work, High Fidelity (HFA2k, CC BY 4.0); UltraSharp, Ultramix Balanced and Remacri are non-commercial (CC BY-NC-SA 4.0); Upscayl Standard, Lite and Digital Art have no stated licence and are not used for paid work until confirmed
- **Registry.** `upscayl` added (category image), pinned to release 2.15.0 (commit 4f39acf) with the SHA-256 of the Windows, macOS, AppImage and deb installers; manual on every host, since it is a desktop app that needs a Vulkan graphics card and runs on the user's computer
- Repository: a knowledge-wiring row and host-eval case AD12 (not run)

## 1.94.0, 2026-10-19

At the owner's request, a full audit of the repository and plugin after 1.91.0 to 1.93.0, with every gap it found in how the added knowledge is reached fixed ([audit](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/full-audit-2026-10-19.md), [handover for Codex](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/handover-codex-2026-10-19.md)):

- **New owners.** Landing pages, app screen mockups, HTML pages and slide or pitch deck design go to Static Graphic Design Creator with the craft rules; contrast and accessibility checks to Output Critic with `contrast_check.py` (HTML with `craft_lint.py`); measuring a reference animation to Motion Graphics with reference breakdown; coded lyric and beat-synced videos to Motion Graphics with lyric timing. Routing rows, Polish cues and collision rules added
- **Knowledge wired to its users.** DESIGN.md export is linked from the brand identity profile, Delivery Documentation and the static owner; Pipeline Core lists the shared design tools; prompt examples come after the idea and before a web search; Caption Studio and Creative Music Video Director reach lyric timing; Output Critic judges against the craft rules; the motion review row includes motion activity; the reel starter is offered at build time
- **Conflicts resolved.** The one-pass text rule names the exact-copy compositing exception; motion entry and exit timing agree with motion craft; the Polish dash standard accepts the spaced em dash, one style per text; protected text is reported by the AI writing check, never rewritten; one precedence line chooses among Anatomy, Iso Glow, art-style direction and the Animate engine
- **Fixes.** The Iso Glow example follows the track's length and `audio_envelope.py --inject` sets the composition and music clip duration; lyric timing tries faster-whisper first (the recogniser verified on songs); `accent-overuse` is skipped in video compositions; web reach is told to use the direct route for client URLs; the release status records the right origin
- **Capability card.** Lyric timing, motion activity, HTML capture, the prompt library and technique atlas, the asset manifest, the environment check and web reach added, with runtime-map rows; checked 2026-10-19
- **Registry.** Every recommended repository has a category; `extensions.py catalog` groups by it
- Repository: `tests/knowledge_wiring_test.py` (each integrated reference is linked from its owners), a category test, an extended Iso Glow test, GitHub-exact anchors in the validator, and the host-eval set `additions` (11 cases, not run)

## 1.93.0, 2026-10-19

At the owner's request, a full adaptation of anti-slop (miqdadbadjuber, MIT) and its listing among the recommended repositories:

- **AI writing patterns.** [AI writing patterns](../skills/copy-voice/references/ai-writing-patterns.md) in Copy Voice: the shapes of machine-made copy (empty vocabulary, inflated significance, unproven social proof, weasel attribution, chatbot closers, negative parallelism, forced threes, staccato runs, false ranges, generic CTAs, filler, hedging, emoji and bold habits) with fixes, Polish forms, what not to flag, signs of a human writer and a draft-audit-final loop. Dashes are not banned: Polish typography uses them and the brand decides
- **Writing check.** [`ai_writing_check.py`](../skills/copy-voice/scripts/ai_writing_check.py) finds those patterns in English and Polish and judges clusters (clean, check, cluster), never single tells; Copy Voice, Humanizer and output review use it. Standard library only
- **Craft rules.** New sections: purpose before technique (one-line reasons, five craftsmanship questions), more interface patterns (dose caps for glass and glow, decoration, layout templates, app and dashboard screens, generic CTAs and buzzwords, no cloned products), liveliness with three dials (energy, rhythm, motion) and a one-line Design Read, honest content and click-through verification, and responsive layout. Caps at display size may be set tight
- **Lint and contrast.** `craft_lint.py` gains focus-outline-removed, dead-link and low-contrast (P0) and glass, glow, pill, arrow, generic-CTA, buzzword, fake-person, background-grid, viewport, 100vh and fixed-width rules (P1), skipping page-layout rules in video compositions; [`contrast_check.py`](../skills/pipeline-core/assets/craft-lint/contrast_check.py) computes WCAG contrast with a self-test. Across the package's own HTML the linter reports nothing
- **Registry.** `anti-slop` added, pinned to 439a2ef and installed with the pinned skills CLI (all six skills, nothing written to CLAUDE.md or AGENTS.md); manual elsewhere. A decision map is in `integrations/anti-slop/`. The capability card lists the two new tools
- Repository: `tests/ai_writing_check_test.py` and new cases in `tests/craft_lint_test.py`; NOTICE and README updated

## 1.92.0, 2026-10-19

At the owner's request, a full adaptation of Open Design (nexu-io, Apache-2.0) and its listing among the recommended repositories:

- **Craft rules.** [Craft rules](../skills/pipeline-core/references/craft-rules.md) in Pipeline Core, restated in English from Open Design's craft references (themselves from refero_skill, MIT): machine-made tells, typography (caps tracking, display tracking, CJK leading), hierarchy and editorial hierarchy, colour and accent discipline, interface motion, the five interface states, the accessibility floor, laws of UX, forms, right-to-left text, and where print, video and slides change the numbers. Output review of static graphics, Static Graphic Design Creator and Motion Graphics Workflow apply them
- **Craft lint.** [`craft_lint.py`](../skills/pipeline-core/assets/craft-lint/README.md) flags those tells in HTML, CSS and SVG (default indigo, purple and trust gradients, emoji icons, system-sans display, left-accent cards, invented metrics and filler copy in English and Polish, untracked caps, raw hex, accent overuse, placeholder images); brand tokens are never flagged and `--allow` records a deliberate exception. Standard library only
- **DESIGN.md.** [`design_md.py`](../skills/pipeline-core/assets/design-md/README.md) exports a brand kit to DESIGN.md, tokens.css and an Open Design manifest, and imports colours, fonts and don'ts from a DESIGN.md package, leaving everything else as placeholders for the user
- **Prompt examples.** 87 worked prompts for gpt-image-2, Seedance 2.0 and HyperFrames ([prompt examples](../skills/pipeline-core/assets/prompt-examples/README.md)), verbatim with their licences (CC BY 4.0, Apache-2.0) and credit lines; 19 source templates were left out (no open licence, real people or clubs, third-party franchises or studio styles, imitated company or platform styles, fake phone photos). Image and Video Prompt Architect consult them for structure only
- **Registry.** `open-design` added, pinned to release 0.25.0 (commit de6d2c0): manual install in Claude Code, Codex and the Claude desktop app with the installers' SHA-256, `od mcp install <agent> --print` first, local use free and cloud credits never needed; not supported in ChatGPT and ChatGPT Work. The capability card lists the three new tools
- Repository: `tests/craft_lint_test.py` and `tests/design_md_test.py`; NOTICE and README updated

## 1.91.0, 2026-10-18

At the owner's request, two outside sources implemented in Studio and listed as recommended repositories, and a fourth welcome option:

- **Welcome option 4.** Under the skill-search line, the welcome (English and the approved Polish translation, both byte-checked) now asks whether the user wants to see the GitHub repositories recommended by FrameCore Works. Choosing it shows the [recommended repositories list](../skills/workflow-orchestrator/references/extensions.md#recommended-repositories-list): every registry entry with what it does, what Studio already bundles from it, its licence and how it is installed in the agent the user is in; it installs nothing. `extensions.py catalog --host <host>` prints it. A `4` from a three-option welcome shown before 1.91.0 asks for clarification; a `4` in the work-area menu is still area 4
- **Iso Glow for video.** [Iso Glow kit](../skills/hyperframes-workflow/assets/iso-glow/README.md) in Motion Graphics Workflow: isometric hairline drawing where only what is live glows, adapted from iso-glow (April Zhu, on iso-figure by Tolga Cohce, MIT) for seekable video, with a HyperFrames loudspeaker example driven by the bass. [`audio_envelope.py`](../skills/hyperframes-workflow/assets/motion-sync/audio_envelope.py) measures one band of a supplied track per frame and its hits and writes them into a composition (Python and FFmpeg only)
- **Art-style and explainer direction.** [Art-style and explainer motion direction](../skills/hyperframes-workflow/references/art-and-explainer-motion-direction.md), restated in English from huashu-art-motion (alchaincyf, MIT): camera moves as punctuation with timings, choosing the look and palette, seven explainer grammars, twelve cross-grammar rules, six ways a film goes wrong and shot-list rules; [reference breakdown](../skills/hyperframes-workflow/assets/reference-breakdown/README.md) adapts its breakdown script (cuts at their first frame, the cut grid with BPM candidates, transition sheets, motion heatmaps, keyframes)
- **Registry.** `huashu-art-motion` (commit 8a0d7d7, skills CLI install in Codex and Claude Code) and `iso-glow` (no repository: the archive is pinned by SHA-256, a new `archive` pin the validator checks in every command) added; the capability card lists the two new tools
- Repository: `tests/iso_glow_test.py`, `tests/reference_breakdown_test.py` and catalog/archive cases in `tests/extensions_test.py`; NOTICE, README, the smoke set and the Claude install guide updated

## 1.90.3, 2026-10-18

From the owner-supplied Polish test track (2026-10-18):

- **Lyric timing in Polish, recorded.** A fast Polish rap track with two voices matched 89 % of the lyric words with the default `small` and the automatic retry; lines in order, choruses placed where a separate transcription heard them, one line flagged. The weakest lines were wordplay. Recorded in the motion-sync README; no audio or lyrics stored

## 1.90.2, 2026-10-18

From a model comparison on the same real song (owner choice 2026-10-18), faster-whisper on CPU, share of lyric words matched:

- **`small` is the default recogniser** (98 % in about a minute); the former default `large-v3` matched 72 % in 226 s and `large-v3-turbo` 71 %
- **A weak pass is retried.** The large models skipped whole verses while conditioning on the previous text; a first pass below 90 % is now retried with the other setting and the better pass kept (`large-v3-turbo` then reached 94 %). The report names the model and the setting
- One song is weak evidence; the motion-sync README records the comparison and suggests comparing models on the user's own track when many lines need a check

## 1.90.1, 2026-10-18

From the first end-to-end lyric timing run on a real song (owner request 2026-10-18): Brad Sucks, "Total Breakdown" (CC BY-SA 3.0), faster-whisper `small` on CPU, 98 % of the lyric words matched in 23 s:

- **FFmpeg decoding.** faster-whisper 1.2.1 could not open the track with PyAV 19; `lyric_timing.py` now decodes the audio with FFmpeg and passes the samples
- **No stretch across a gap.** A line sung differently from the published lyrics, after a 20 s instrumental break, had its unheard words stretched across the break and was not flagged. Unheard words now stay beside the next heard word (within 0.2 s of the recogniser here) and the line is flagged for a check by ear; a matched share of half or less is flagged too
- Repository: regression test; no audio or lyrics committed; the tempo was not verified by ear

## 1.90.0, 2026-10-17

At the owner's request, Agent Reach's no-login reading inside Studio:

- **Web reach.** [`web_reach.py`](../skills/research-evidence/assets/web-reach/README.md) in Research Evidence reads public pages (Jina Reader, then a direct fetch), RSS and Atom feeds, public GitHub repositories and YouTube subtitles (with yt-dlp), using only the Python standard library. Every result names its source, retrieval date and route; bot challenges are reported, private and metadata addresses refused, responses capped at 5 MB. Channels that need cookies or a login stay out
- Adapted from [Agent Reach](https://github.com/Panniantong/agent-reach/tree/94f06c1969dfc1834001269d79d3ad0972d9dee6) (MIT); the full CLI stays an optional extension. Works wherever Python has internet access; a chat sandbox without it falls back to the host's search
- Repository: offline tests in `tests/web_reach_test.py`; one live read through Jina Reader in a container; NOTICE updated

## 1.89.1, 2026-10-17

At the owner's request after reviewing [Agent Reach](https://github.com/Panniantong/agent-reach/tree/94f06c1969dfc1834001269d79d3ad0972d9dee6) (1.5.0, MIT):

- **Agent Reach as a recommended extension**, no-login channels only: public web pages (Jina Reader), YouTube metadata and transcripts, RSS, public GitHub and Exa search, installed on request in Codex or Claude Code. Channels that need cookies or a logged-in session (X/Twitter, Reddit, Facebook, Instagram, Xiaohongshu, Boss Zhipin) are rejected: Studio never exports cookies, uses spare accounts or automates a platform against its terms. Research Evidence offers it once when the host's own web tools cannot read a source the decision depends on
- Repository: decision map and licence in `integrations/agent-reach`; not installed or run (owner decision 2026-10-17: no tests this round). The 1.89.0 release was published with all assets; its notes workflow failed on the tag commit because the notes lacked the version heading, fixed in `688ea23`

## 1.89.0, 2026-10-17

At the owner's direction (2026-10-17: motion quality and a slimmer package, no host tests this round):

- **Local-service reel starter.** [`reel-starters/local-service`](../skills/hyperframes-workflow/assets/reel-starters/README.md): a 24 s HyperFrames board structure (hook, three work photos with labels, proof, person, booking end card) with a persistent frame, continuous motion, a second accent per board and slots for exact copy and photos. Rendered at 9:16 and 4:5 in a container; the first version failed motion activity (83 % still) and the fixed one passed (15 % and 2 %)
- **Read less, find more.** Six large references (video craft, image generator snapshot, visual subject craft, learning mode, the production task packet, presentation and interaction) gain a Contents list so a model reads one section
- **Description headroom.** Three explicit-only or legacy skill descriptions are shorter (7,699 of 7,800 characters, from 7,789); routing boundaries unchanged
- Repository: structural test for the starters; roadmap updated

## 1.88.0, 2026-10-17

At the owner's explicit request, bundle the reusable toolsets from [Logo Design Skill](https://github.com/kaankiziltug/logo-design-skill/tree/0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134) 1.4.4 and [Anatomy](https://github.com/wheresryan22/anatomy/tree/e9488296a44211c42701ff71705b7901470ec78f):

- Logo: all nine tools, fourteen references, two templates, catalogue assets and fictional examples; a Studio adapter for project setup, search, SVG audits, review sheets and variant/icon exports. Recognition, optical craft and target-size checks live in the existing static owner. Real-company trademark SVGs are excluded from MIT and are not republished; an explicitly supplied reviewed corpus can be attached with its separate rights status.
- Anatomy: the complete 15-file SVG/WebGL/3D kit, React adapters, rendering/geometry review tools, technical references and source examples. A project initializer, three executable integration fixtures and one deterministic frame bridge connect to the existing HTML capture route. No separate Anatomy installation is required for the bundled code.
- Add both original repositories as optional, pinned extensions with per-host procedures. No native extension is automatically installed. Existing owners, menus, creative decisions, provider boundaries and review budgets stay in place.
- Keep copied source byte-identical with MIT notices and file hashes. Treat upstream audit scores and sampled checks as scoped evidence, not automatic production approval. Record local tests separately from fresh-client behavior.

## 1.87.1, 2026-10-17

Four bounded fixes for defects reproduced in the owner's audit:

- Run the GSAP and Remotion contract validators correctly in paths containing spaces, URL characters or symlinks; keep the two starter validators identical.
- Bind motion QA reports to the exact contract bytes, identity and revision, and bind video critiques to the inspected encoded file. Reject mismatched reports and leave legacy or standalone HTML evidence unverified for a separate contract.
- Add a guarded Studio adapter for Animate caption exports. Captions follow each actual output, including alternative formats and custom filenames; the 107 pinned upstream source files remain unchanged.
- Isolate environment-test browser discovery from machine-wide browser installations while retaining production detection of Chrome outside PATH.

No skill IDs, menus, welcome content, providers or creative workflows change. Version markers, source inventory and release records are refreshed for distribution. PoYo is preserved only in the existing hosted installation as the owner's approved synchronization exception. Source tests and saved-package comparisons do not establish fresh-chat behavior.

## 1.87.0, 2026-10-16

At the owner's request:

- **Choose a local voice engine.** For a voice-over generated on the user's computer, Studio asks which engine to use: [Voicebox](https://github.com/jamiepine/voicebox), [OmniVoice](https://github.com/k2-fsa/OmniVoice), [VoxCPM2](https://github.com/OpenBMB/VoxCPM) or [MOSS-TTS / MOSS-TTSD](https://github.com/OpenMOSS/MOSS-TTS). A user who does not know them gets a comparison (what each is best at, Polish, cloning, voice design, sound, computer, commercial licence) and a recommendation for their need and computer ([local voice engines](../skills/audio-production-director/references/local-tts-engines.md)). Cloning needs the voice owner's permission; engine, model and licence go into the delivery notes
- All five are [recommended extensions](../skills/workflow-orchestrator/references/extensions.md) (category `tts`), pinned and installed only on request: Voicebox from its v0.5.0 release with its MCP server or REST API, OmniVoice and VoxCPM2 from PyPI in their own virtual environment, MOSS-TTS and MOSS-TTSD from their reviewed commits. In chat hosts Studio delivers the script, voice direction and engine settings instead
- Repository: provenance and licences in `integrations/tts-engines`; host case G11 (PASS)

## 1.86.1, 2026-10-16

- The web motion probe no longer fails when the browser is still writing its temporary profile as it exits; its cleanup retries and warns, like the other browser tools (CI run of the 1.86.0 release). 1.86.0's changes are published with this release

## 1.86.0, 2026-10-16

At the owner's request:

- **The original repositories as extensions.** [Animate](https://github.com/cth9191/animate), [Motion Designer](https://github.com/kaventro/motion-designer) and [Meta Ads Designer](https://github.com/aievolutionpl/meta-ads-designer), whose methods Studio already adapts, can now be installed in full and natively from the [recommended extensions](../skills/workflow-orchestrator/references/extensions.md), each pinned to its reviewed commit. In Claude Code, Animate and Motion Designer install as plugins from a checkout at that commit, and Meta Ads Designer as a skill. In Codex, Animate and Meta Ads Designer install as skills; Motion Designer cannot, because its skill's front matter does not parse at that commit. In ChatGPT, ChatGPT Work and the Claude apps, Meta Ads Designer's rule files can be added to a project by hand; the other two need a shell
- A new host status, `manual`, gives the files to add by hand; a plan never changes a host setting, and a skills CLI install keeps its own confirmation
- Repository: every repository the owner sends for review is now also added to the registry (owner decision 2026-10-16, AGENTS.md and the [maintainer guide](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/extension-registry.md))

## 1.85.0, 2026-10-15

At the owner's request, from a review of [morluto/rea](https://github.com/morluto/rea) ([decision map](../integrations/rea/README.md)):

- **How is this web animation built?** The [web motion probe](../skills/hyperframes-workflow/assets/web-motion-probe/README.md) opens a page in a local browser and reads its motion libraries and versions, each GSAP tween (targets, properties, duration, delay, ease, stagger, scroll range; finished entrances kept), every CSS animation and transition with its timing and keyframes, Lottie files, fonts, and optional frames. Studio takes the values and rebuilds the technique in its own runtime; it never copies the site's code, assets or text
- **Recommended extensions.** A curated [registry](../skills/workflow-orchestrator/references/extensions.md) of outside repositories the owner reviewed as engines or knowledge, each pinned, with its rights terms and per-host status (native, desktop only, not supported with the reason) and its own dry-run plan, install, verify and remove commands. Studio installs one only on an explicit request, the plan shown first. The first entry is REA (software reverse engineering: apps, Electron, .NET, Android, websites), installable natively in Codex, Claude Code and the Claude desktop app; not in ChatGPT or ChatGPT Work
- The skill finder names a fitting extension before the open catalog; the Codex and Claude installation guides end with an optional extensions question
- Repository: a maintainer guide for adding repositories ([extension registry](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/extension-registry.md)); host cases G09 (motion read from a page) and G10 (extensions and host status)

## 1.84.1, 2026-10-15

At the owner's request: the reconstruction method states general rules only; two notes naming the single photograph and generator result they were learnt from are removed from the package text. No rule changes.

## 1.84.0, 2026-10-15

Trigger: defects seen in a host evaluation on the owner's real case, a black-and-white mirror portrait from his reverse-engineering project (2026-10-15):

- **Optical effects by their cause.** Studio read the reflected person as "a window onto another world" or "a small portrait in a frame", the result the owner had to correct by hand. The method now describes a mirror as a real reflection (smaller with distance, inside the reflected room, sharing the light, never touching the rim), and the same for glass, water, shadows and lens blur
- **Focus and gaze per figure.** Both runs made the near face the sharpest, the reverse of the photo, and one had both people looking the same way. Studio now states which face is sharp and which soft, each figure's gaze and expression, and the camera's height and lens, and repeats a soft near face in the closing lock
- **The measurement runs when it can.** With a shell available Studio skipped the probe; it now runs it before writing. `image_probe.py --analyze` merges near-identical shades (a white logo was four "colours"), keeps small accents apart (a red sign, a white hat on a dark photograph), gives the black and white points, colour character (monochrome, muted or saturated; warm, neutral or cool), a 4 × 4 focus grid, a 3 × 3 brightness grid with the brighter side, converts Display P3 and other profiles to sRGB, and no longer places a "subject" on paper grain
- **After a generation** Studio checks the usual generator drift first (a profile turned to the camera, a smile, extra headroom, both faces sharp, a tilted object turned flat), seen in the owner's Nano Banana result; a stated length limit is counted with a tool; a handoff for a new conversation; a future REF is named by its label, not the model person's gender
- Repository: before and after records of the mirror case (`verification/host-evals/2026-10-15-1.83.0-reverse-mirror-*.json`); the photo is a third-party image and is not committed. Seven probe tests, six of which fail on the old probe

## 1.83.0, 2026-10-15

At the owner's request, from the knowledge of his reverse-engineering project:

- **Reconstruct an image in a prompt.** Image Prompt Architect analyses a supplied photograph, poster or illustration and writes a prompt that recreates its effect with the user's own person, animal or product: the model image is analysed and never uploaded as a reference, the mechanism comes first, space is described as relations from the viewer's side, colours have roles, the medium stays (an illustration is not turned into a photograph), and a template the user supplies is filled exactly ([reference reconstruction](../skills/image-prompt-architect/references/reference-reconstruction.md))
- **Measured, not guessed.** `image_probe.py --analyze` gives the dominant colour fields in HEX with their share, the tonal range and, on a plain background, where the subject sits in percent of width and height
- **After a generation** Studio corrects in a fixed order (mechanism, then scale, colour and light, then texture) and gives a full corrected prompt for the original references
- Repository: host case G08 (before FAIL, after PASS); the harness can place repository files in a case workspace

## 1.82.0, 2026-10-15

From the owner's creativity audit of 1.81.0 ([decisions](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/creativity-audit-1.81.0-2026-10-15.md)):

- **Directions that argue differently.** The ideation method asks for each direction's conclusion in one sentence; two that could swap places are one direction, whatever their metaphor or reveal order
- **Brand, not only category.** Studio tells apart what fits the category, what uses a true product trait and what only this brand could own; with no brand fact it asks for one or leaves that part open, and never invents one
- **Effects must earn their place.** Every effect, above all one added for "stronger", passes a removal test: if nothing is lost without it, Studio looks for a better event instead
- Repository: the creative evaluation can no longer be passed by a template (the same three coloured squares now fail all 11 briefs), a changed offer, "nie tylko", variant labels or a wrong number of directions; a live run of the creative suite is recorded (7 of 11; the remaining failures are category motifs in two of three directions, a limit known since 1.66)

## 1.81.0, 2026-10-14

Fixes from the owner's technical audit of 1.80.0, each with a regression test ([fixes](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/technical-audit-1.80.0-2026-10-14.md)):

- **Approvals stay honest.** Importing captions into a contract makes a new revision that needs approval again (Python and Node tools); exact copy must appear whole and in order within one frame (10 is not 100, "do not buy" is not "do buy not"); the technical verdict fails a file whose picture or audio runs longer than the contract
- **Exports keep their picture and timing.** HTML capture pads short audio instead of cutting the film to it and checks the encoded frame count; the browser MP4 writer stores composition offsets correctly; extending a scene moves active-word caption timings with it
- **Without code execution** Studio gives the contract and the motion player first, instead of asking to switch on a shell
- **Environment check.** A program that does not run is reported missing; Node.js below HyperFrames' minimum fails the check where HyperFrames runs; printed install commands keep folder names literal; an older HyperFrames on a host that cannot run it is never shown as usable
- **Asset check.** A grey subject moved between the white and black versions is refused; a fully transparent file is not an asset
- Learning mode returns to the complete welcome with all its options
- Repository: publication commits only its records, refuses a dirty tree and stops when a downloaded asset differs; manifest and ZIP share one file rule and are compared after packing; the host-eval harness pairs tool calls with their results, counts questions in lists, keeps usage of finished turns, and stops when an API key is set unless the owner allows it; stronger checks for M04, M05, X02 and X03

## 1.80.0, 2026-10-14

From a production session on 2026-10-14 (a lyric video built from assets the user generated in Gemini) and its handover:

- **Generated cut-out assets.** When a motion film needs realistic objects, products, hands, close-ups or photographic light and nothing is supplied, Motion Graphics Workflow plans one generated still per need from the storyboard, with ready prompts (or, with an approved connected generator, makes them), and never draws realistic objects or hands in code ([generated cut-out assets](../skills/hyperframes-workflow/references/generated-motion-assets.md))
- **Transparency by generator** (checked 2026-10-14): OpenAI's API `background="transparent"` with PNG or WebP; Gemini has no alpha, so white then an edit to black for a difference matte, or flat green for a solid subject; light and neon on black with no backing plate, composited with screen
- **Asset check tool** (`assets/motion-assets/asset_check.py`): `check` (real alpha, painted checkerboard, edge fringe, pixels for the largest zoom), `matte` (difference matte that refuses a moved subject) and `key` (soft chroma key with despill that refuses a subject with green of its own); edges are checked again in the rendered film at peak zoom
- Image Prompt Architect gains the animatable-asset rules; Asset Manifest records generator, transparency method, resolution and moving parts
- Repository: host case G07 in `tests/host-evals/gaps.json` (before FAIL, after PASS)

## 1.79.0, 2026-10-14

From the owner's ChatGPT Work test of 1.78.0 (2026-10-14): the sandbox had Node.js 24, FFmpeg 6.1, Chromium 153 and the npm registry, installed the HyperFrames CLI on request and rendered a 1080x1920 test; Studio had said HyperFrames could not run there.

- **HyperFrames in ChatGPT Work.** Motion Graphics Workflow offers to install the pinned HyperFrames CLI for the session when the check finds Node.js, FFmpeg, Chromium and the npm registry, runs `doctor` and a short test render, then builds client reels there as in Claude Code; the install lasts only for that session
- **Environment check.** On ChatGPT Work, Node.js, npx and Chromium are observed and HyperFrames is installable (`install`), with the session install command; HyperFrames skills without the CLI count as missing there. Ordinary ChatGPT and the Claude apps are unchanged
- Capability card and runtime map: the HyperFrames engine and the visible-text audit are open to a code sandbox whose check finds their needs

## 1.78.0, 2026-10-14

Owner decision after reviewing [motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) (Apache-2.0, idea only):

- **No page chrome.** Motion Graphics Workflow checks plans and frames for the tells of a template film (a small label in a corner, a "02 / 04" counter, a timecode or progress bar, a kicker above a headline, the same left headline beside a card in scene after scene, a headline typed letter by letter) and removes what the idea does not need; a persistent logo, the offer, phone and address stay
- Repository: host case G06 in `tests/host-evals/gaps.json` (passes before and after; after the change the reply states the rule); NOTICE credits the source

## 1.77.0, 2026-10-14

Fixes from an external review of 1.76.0, each reproduced before the change ([decisions](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/argon-review-1.76.0-2026-10-13.md)):

- **Files stay in the project.** The motion renderer reads assets only from the contract's folder and font files only from that folder, the font folders it is given or the bundled fonts; the sound tool reads its WAV inputs only from the contract's folder
- **Offers read right.** Hours and days lines show the quantity with the hourly or daily rate, a discount gets its own line, and no empty payment line appears
- **Right clip, right timing, right check.** Clip review never matches shot S1 to `S10.mp4`; the voice-over budget counts the pause of a standalone dash and of a full stop inside quotes; the OCR copy check keeps signs, decimals and per cent and counts repeated words
- **Versions keep their names.** Exports of `spot.v2.json` no longer overwrite those of `spot.v1.json` (variants, sheet export, prompt pack, edit export, board compositor)
- **Polish copy.** "Ci klienci" is no longer flagged as mixed address; no-break spaces bind only after Polish one-letter words, never after "B" or English "A"
- **UGC disclosure** goes both in the video (on screen and spoken) and at the start of the caption
- Repository: the release job no longer installs the pilot from a Git URL; release branches and trailers come from the environment; CI runs the headless frame-review tests; NOTICE and LICENSE_STATUS list the components added after 1.0.0

## 1.76.0, 2026-10-13

Fixes from the owner's evaluation of 1.75.0 ([record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/evaluation-1.75.0-2026-10-13.md)):

- **No invisible text.** The static compositor stops with `text_overflow` when a text box lies outside the canvas (a price placed off the page rendered nothing and passed); the motion renderer stops when a persistent line or an active-word caption is wider than the frame
- **Offers read right.** Prices entered gross are labelled as gross unit prices; negative hourly or day rates and negative extras are refused
- **A new look needs a new approval.** A brand kit or a variant that changes colours or type puts the contract back to proposed
- **Fonts.** When no Arial or metric-compatible font is installed, the motion renderer says so (`font_warning`); install Liberation Sans for the bundled examples
- Repository: a release refuses a working tree with uncommitted changes, so unrelated drafts never ride along; release counts read both Node test reporters

## 1.75.0, 2026-10-13

Fixes from the gap audit of 1.74.0 (owner's audit in Claude Code, [record](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/reviews/gap-audit-2026-10-13.md)):

- **Work goes to its owner.** Static Graphic Design Creator, Image Prompt Architect, Caption Studio, Humanizer and the legacy audio alias now hand a request outside their scope to the owning skill instead of doing it themselves; "a small task may be done directly" applies only inside the current owner's domain
- **No invented claims.** Copy Voice never says it inserted a no-break space the text does not contain; Humanizer adds no health, comfort or performance claim; planning tool costs never records consent to pay
- **Fewer questions.** The video and image prompt architects ask one question when essentials are missing; after choosing a work area Studio asks one brief question and promises no render before checking the host
- **Right reading.** Asset Manifest reads `haslo.txt` as a slogan, not a password; captions say 14 % from the bottom is for organic posts and paid Reels use 35 %; a single generator prompt goes to Video Prompt Architect first
- **Tools fail clearly.** Missing or unreadable inputs exit 2 with one line in the Polish copy checker (a mistyped path used to pass as "no findings"), motion activity, lyric timing, print PDF check and HTML capture; lyric timing and the static compositor never overwrite an existing file; the frame review finds Playwright's Chromium; a plain environment check no longer prints "FINAL CHECK"; HyperFrames is pinned to 0.8.149 everywhere
- Regression cases in `tests/host-evals/gaps.json` (repository): all five pass in Claude Code after the change

## 1.74.0, 2026-10-13

One creative menu (owner decision, CR-20261013-01):

- **Work areas and pace in one message.** After choosing Creative mode, Studio shows the eight work areas `1–8` and the pace `A. Quick / B. Expanded` together, with a reply such as `8, B`; a bare area number takes Quick mode. Before, three menus came before the first question about the project. A pace given up front shows the areas only; a pace menu still pending from an earlier version keeps its numbers on resume
- **The areas keep their names and order.** The orchestrator now names the eight areas itself; in the first test of the combined menu the model renamed and reordered them because the list lived only in a reference
- Host evaluation in Claude Code: W05 failed on 1.73.0 and passes now; the welcome, skill search and direct-task cases still pass (records in `verification/host-evals/`). The owner's ChatGPT startup check is pending

## 1.73.0, 2026-10-13

Fixes from a client end-card session (owner's retrospective, 2026-10-13):

- **Hand-written HTML to MP4 without npm.** [`capture-html.mjs`](../skills/hyperframes-workflow/assets/motion-export/README.md#hand-written-html-to-mp4-without-npm) renders a canvas, GSAP or DOM composition frame by frame from `window.renderFrame(t)` with a local Chrome or Chromium and FFmpeg, dependency-free, with rational frame rates, format variants and an optional finished mix. The session had Chromium and FFmpeg but a blocked npm registry, so neither HyperFrames nor Remotion could run and Studio had no route; two captures now give identical frames
- **Probe before the runtime.** The motion skill checks Node.js, FFmpeg, the browser and the npm registry before choosing or promising a runtime and says which route it chose; the runtime map and the Claude Code reel route name the capture when npm is unreachable
- **Clean end cards.** After the reveal everything that covered it clears within one beat and no decoration stays unless asked; an addition Studio proposes stays off until the user clearly accepts it
- Retrospective and decisions in `docs/reviews/retro-outro-end-card-2026-10-13.md` (repository); the one-menu start and a "delicate" sound preset are left as owner notes

## 1.72.0, 2026-10-13

Lyric timing fixes, a motion technique atlas, print-ready PDF and shared script patterns:

- **Lyric timing defects fixed.** Found by the GPT Work research packet (FCW-MOTION-KNOWLEDGE-RESEARCH-01) and reproduced on 1.71.0: a line sung from 0 s got a board cut before 0 (frame -1 or -2), and when the recogniser's neighbouring words overlapped, an unheard word between them ended before it started. Cuts now never go below 0, the gap closes instead of inverting and such lines are listed for a check by ear (`needs_check`); `--fps` accepts rational rates such as `30000/1001`. Three new cases in `tests/lyric_timing_test.py`; the first two fail on 1.71.0
- **Motion technique atlas.** [`technique-atlas`](../skills/hyperframes-workflow/assets/technique-atlas/README.md) names 637 motion techniques in English (what each does, when to use it, family, purposes, media, pairings, HyperFrames registry candidates by name for 104), projected from the English card text of gongnyang/awesome-ai-motion (MIT, pinned `1e3c249`) against the registry of HyperFrames 0.8.149; `atlas.py "<name>"` resolves a technique a brief names. Order of use: registry block, then the atlas as vocabulary and preview, then the motion written from the brief; card code is never copied. Linked from the motion skill, the compendium and the Claude Code reel route
- **Compendium wording.** Known words are aligned rather than transcribed, with a full-master versus vocal-stem comparison on dense mixes; linear motion is kept for motion that is mechanical or constant by design; `matched` in lyric timing means heard, not verified
- **Demucs caveat.** The motion-sync README, the lyric timing docstring and the compendium no longer recommend Demucs without saying its pretrained weights are for research use only
- **Print-ready PDF.** `print_pdf.py` (static render) finishes a PDF for print (TrimBox and BleedBox, the printer's ICC output intent without converting colours), preflights it through every page and form XObject (bleed, effective ppi, colour spaces including spot colours, total ink, transparency, hairlines, fonts used, attachments such as C2PA, PDF/X declaration), compares two renders per region, and maps, removes or moves vector blocks in a PDF without its source. [Print-ready PDF](../skills/delivery-documentation/references/print-ready-pdf.md) covers questions for the printer, PDF/X, routes for making the PDF and a check list
- **Shared script and campaign patterns.** One [reference](../skills/pipeline-core/references/script-and-campaign-patterns.md) for scripts, short-form video, campaigns, launches and sales conversations, linked from Pipeline Core, Copy Voice, Marketing and Storyboard Sequence Architect
- Research findings from Gemini, ChatGPT (two reports and a delta against 1.71.0) and GPT Work, with what was taken and what was left as notes for the owner, in `docs/research/motion-2026-10/` (repository)

## 1.71.0, 2026-10-12

Motion graphics knowledge and lyric timing:

- **Motion compendium.** One map of where every part of Studio's motion knowledge lives (Studio references, HyperFrames skills, Remotion's agent skills), plus what the other references did not hold: ad creative for Meta and short-form platforms with dated sources (the message in the first 3 seconds, sound-off design, 9:16 and 4:5, the widely cited Reels margins marked as not confirmed on Meta's pages, length ranges), tools and licences (HyperFrames, GSAP, Remotion, Motion Canvas, Revideo, Lottie, Rive, Manim, Theatre.js), lyric timing by forced alignment, hybrid films with generated images and clips, HyperFrames techniques and transitions by name, the working sequence from style frames to delivery, and a failure-to-fix table ([motion compendium](../skills/hyperframes-workflow/references/motion-compendium.md))
- **Lyric timing.** `lyric_timing.py` gives every word and line of a song its sung time with the user's lyrics as the truth: a recogniser (stable-ts, WhisperX or faster-whisper, installed by the user) or supplied word times, global alignment that keeps the correct spelling, interpolation of unheard words, the bundled beat grid, board cuts snapped to half-beats when close, and JSON, LRC (with word stamps) and SRT ([lyric timing](../skills/hyperframes-workflow/assets/motion-sync/README.md#lyric-timing)). Measured on a reference lyric reel: cuts follow the sung words, beats drive the accents
- Handover updated with the next step: lyric timing on a real song (repository)

## 1.70.0, 2026-10-12

Motion graphics for client reels in Claude Code (owner-requested development round):

- **HyperFrames by default in Claude Code.** In a shell host with Node.js, FFmpeg and a Chromium, client reels and ads are HyperFrames compositions built with HyperFrames' own skills, while Studio keeps the brief, the idea, copy locks, the board plan and the review ([client reels in Claude Code](../skills/hyperframes-workflow/references/claude-code-reels.md)): setup, who does what, a map of the 21 HyperFrames skills (commit `86521b9`, 0.8.149), an eight-step production loop and the first recorded HyperFrames render in a container
- **Reel board system.** One statement per board, a persistent frame, type with one accent, objects instead of decoration, recreated UI, real photos, CTA end cards; motion targets measured on reference reels; twelve ad structures (local service, app, offer, before/after, how it works, social proof, event, recruitment, B2B launch, voice-over explainer, lyric video, hybrid AI footage) with the registry blocks that build them; formats and safe boxes; lyric video, hybrid footage, transitions and still frames ([reel board system](../skills/hyperframes-workflow/references/reel-board-system.md))
- **Motion activity check.** `motion_activity.py` measures still time in a rendered MP4 and returns REVISE above 40 % undeclared still time or a still over 2.5 s; declared holds are excused. It flags the 6-second film reviewed on 2026-10-11 (83 % still) and passes the reference reels; the skill's review step runs it on every render
- Handover for the next surface (repository): `docs/handover-motion-1.70.md`

## 1.66.1, 2026-10-12

Handoff fixes from the full check of skills, orchestration and handoffs ([report](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/full-check-2026-10-12.md)); maintenance mode, every change fixes a confirmed defect:

- **The right reviewer for a coded motion render.** A rendered motion video with its contract is reviewed by the Motion Graphics Workflow (craft critique and frame review) in the shared output-review table, the execution adapter, Delivery Documentation, the commercial video director and asset-change routing; eight texts had sent it to Video Prompt Architect
- **One route table, no contradicting copies.** Route lines in Pipeline Core and the orchestrator's kit now match the table: explainers and coded films to the Motion Graphics Workflow, creator ads to UGC, positioning and channel plans without a priced offer to Marketing, the visual direction of a music video to Creative Music Video Director
- **The contract after approval without code execution.** Motion Graphics Workflow gives the contract in the reply with the player link instead of a hand-written render script; the new handoff case X03 failed before and passes after
- **Which text wins.** When an owner's kit method and its `SKILL.md` disagree on scope, entry, inputs or the next owner, the `SKILL.md` and the route table win; the handoff matrix lists core contracts, accepts handoffs named in an owner's `SKILL.md`, and missing fields are marked unknown, never invented
- **The chosen direction has a place in Project State** (`creative_direction`), so later owners execute it instead of proposing new directions
- **Creative Video Producer uses the specialists' methods** for the motion thesis, shot cards, generator prompts, creator ads and music videos, and keeps dialogue with Screenplay Story Architect; the motion reference agrees with the skill on who finds the idea of an open motion brief
- Small corrections: the captions README names the real `contract` command; a changed reference for a designed piece goes to Static Graphic Design Creator
- **Full check** (repository): connection graph of the 37 skills, handoff contracts read per skill, and 61 host-eval cases including three new multi-turn handoff cases (X01 to X03); open findings are listed in the report

## 1.66.0, 2026-10-11

Building creative directions from scratch in graphics, video and motion:

- **One ideation method, taught rather than stocked.** A shared [ideation method](../skills/pipeline-core/references/ideation-method.md) for open briefs. It keeps no category lists and no ready ideas: Studio works out the category's obvious motif, palette, type, move and claim with five questions and tells the user in one line what it set aside; collects material that belongs to this client only; turns it into events through ten lenses, each with the move of thought it asks for; writes the mechanism in one sentence ("X becomes Y, because Z"); spreads three directions that differ in mechanism and source, at most one using the defaults as the labelled classic; tests them for swap, retell and fit; and records the direction, its lens and mechanism in Project State. A section on building in each medium covers the frame relation of a still, the cause, turn and payoff of video, and the transformation, rule and signature move of motion. One worked derivation in a category outside every test shows the steps
- **The rule sits where directions are made.** A short fresh-directions rule is inline in Static Graphic Design Creator, Commercial Visual Campaign Director and Commercial Video Campaign Director, and the orchestrator's Quick line uses the method, because a rule kept only in a linked reference was not read in single-turn runs. A client name that is itself the category motif counts as a default when pictured literally. Creative Video Producer, Creative Music Video Director and commercial motion link the method; one idea covers every asset of a project
- **Motion finds its idea before its look.** Motion Graphics Workflow proposes transformations invented for the brief before choosing a style. The subject-to-style map now lists the obvious looks, offered at most once as the classic. The motion prompt library, its brief index and the ad templates execute a chosen idea and are no longer a source of directions
- **Creative host-eval set** (repository): eleven Polish briefs, six of them held out in categories no package file names, with a per-direction stock-imagery check that ignores negations, a set-aside check and an advisory rubric. On held-out briefs 1.65.0 passed 0 of 6 and never named what it set aside; the released wording names it in every reply (21 of 21 across two runs) and passed 8 of 11 held-out cases across those runs. An intermediate wording scored 5 of 5 only because its rule listed the categories of the test; it was replaced. The release gate passed 5 of 5 ([results](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/host-evals.md))
- **Harness:** `max_sections_matching` counts stock imagery per labelled direction, negated mentions do not count, and records are never overwritten

## 1.65.0, 2026-10-11

Motion review and generated-video craft:

- **Development review for motion.** Six questions a person answers about a rendered piece beyond the automatic checks: does the idea develop, does the composition change attention and meaning, is there rhythm contrast, is each state caused by the previous one, is there a signature moment, does the ending land. Restraint is not a defect, repairs reopen the failed dimension instead of adding effects, and each answer says whether it rests on playback, frames, a report or nothing ([development review](../skills/hyperframes-workflow/references/motion-development-review.md)); the QA record has a section for it
- **Sound needs a listening.** `acceptance.py` keeps the temporal verdict open when the contract or the file has sound until someone records `--listening heard` and `--sound-review`; an audio stream is not a listening. `clip_review.py` marks smoothness, rhythm, joins and sound UNVERIFIED in its review, because three frames per clip show states only
- **Joining generated clips.** The [continuity workbook](../skills/video-prompt-architect/references/blocking-continuity-and-extension-workbook.md#7-joining-generated-clips) ranks join methods (shared frame, full-frame cover, occlusion, matched geometry, matched motion), gives each join one shared record, separates planned from actual ends, and sets the frame arithmetic of the cut with a worked example
- **Exact layers in video.** Who owns the logo, readable text, interface, product and claims when generated shots meet brand material, and what generation may add around them; damaged generated identity is covered or removed, not overlaid ([exact layers in video](../skills/video-prompt-architect/references/exact-layers-in-video.md))
- **Gemini Omni dialect.** The generator dialects card adds Gemini Omni from Google's API guide (updated 2026-09-23): input tags, several shots by default, settings outside the prompt, no negative-prompt setting, Polish speech not evaluated, and what is unavailable in the EEA, Switzerland and the UK
- **No promise without a renderer.** Motion Graphics Workflow says to check the host's tools before promising an MP4 and to name the motion player route when there is no code execution
- **Four new host-eval cases** (repository): storyboard only, Veo prompts, MP4 without code execution, three stills. On the candidate 3 of 4 pass; M04 remains an open finding: in a session without code execution Studio stayed on the coded route but promised a render instead of naming the motion player route ([results](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/host-evals.md))

## 1.64.0, 2026-10-11

From Phase 5 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md) (routing, persistence and cost), the last phase:

- **One route table with Polish cues.** The entry's two route tables are one: every owner has a row with how Polish users ask ("plakat", "rozpiska ujęć", "teledysk", "wycena"); the three image operation rows keep their exact contracts. [Routing boundaries](../skills/workflow-orchestrator/references/routing-boundaries.md#collisions) settles the known collisions: a designed piece goes to Static Graphic Design Creator even when only its prompt is wanted, a photo or illustration prompt to Image Prompt Architect; product video by what is asked (idea, whole production, coded MP4 or generator prompt); a supplied generated clip to Video Prompt Architect, never the still-image critic; a service business without a priced offer to Marketing, with a priced offer to Ecommerce
- **Polish routing set.** [25 real-style Polish requests](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/tests/host-evals/routing.json), nine naming Studio and sixteen not, run by the host-eval harness (`--suite routing`, new `reads_any` check). On 1.63.0: 23 of 25, every collision on the intended side; the two misses are short requests without the Studio name that the host answered without loading a skill. On the new table the nine named cases pass with the same owners ([results](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/host-evals.md))
- **Lighter entry and runtime references.** The entry is 28,963 of 32,000 bytes (target 29,000). The method catalog (route contracts, default and situational methods, routing rules) left the reasoning reference that every owner links and is read only when a task needs more than direct execution ([method catalog](../skills/pipeline-core/references/method-catalog.md)); the GEPA real-run procedure moved to the repository
- **Change requests as evaluation cases.** Workflow Self-Improvement attaches the failing exchange to a proposal as an eval case in the harness's check vocabulary ([change request](../skills/workflow-self-improvement/assets/change-request.template.json)); a test keeps the vocabulary equal to the harness
- **Hipson Adapter retired to a pointer.** The adapter keeps its ID and explicit-only route and points to Instruction Packet Factory's [Hipson format](../skills/instruction-packet-factory/references/hipson-format.md)
- **Packets for people.** [Print shop, voice talent and freelancer packets](../skills/instruction-packet-factory/references/vendor-packets.md) with a template; prices, rates, terms and rights come from the user
- **Mascots and stylized characters.** A [reference](../skills/character-design/references/mascot-and-stylized-characters.md) for silhouette, shape language, proportions, anchors and keeping a character the same across tools, and a [mascot sheet](../skills/character-design/assets/mascot-sheet.template.md)
- **SVG wordmark.** [`svg_wordmark.py`](../skills/static-graphic-design-creator/scripts/svg_wordmark.py) sets a wordmark as outlined vector paths from a bundled or supplied font with the font's own GPOS kerning and Polish letterforms (locl PLK), in colour, black and white, with PNG renders, a clear-space and small-size preview and a report whose SVG readback finds no live text, raster or links; a missing glyph stops it. Advances match HarfBuzz and the nonzero fill matches the font rasterizer in tests
- **Brand guide PDF.** [`brand_guide.py`](../skills/delivery-documentation/scripts/brand_guide.py) lays out the brand kit as a guide in English or Polish: logo versions, clear space, colours with HEX, RGB and WCAG contrast (CMYK only from the printer), type samples, voice, claims and rules; unfilled template fields stop it unless it is a draft
- **Registered everywhere.** Capabilities `svg_wordmark` and `brand_guide`, a `fonttools` requirement in the environment check and CI, two new Python suites, the plan and the knowledge map

## 1.63.0, 2026-10-11

From Phase 4 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md) (video and story deliverables):

- **One set of timing numbers.** The [short-form timing card](../skills/pipeline-core/references/short-form-timing.md) gives opening targets per placement (YouTube skippable, non-skippable and bumper facts from Google's help page, read 2026-10-11; feed targets marked as craft guidance), Polish and English voice-over rates at calm, standard and fast reads, a word budget per length, reading time for supers and end-card holds; script, storyboard, prompt, caption, audio and producer owners all point to it. [`vo_budget.py`](../skills/copy-voice/scripts/vo_budget.py) checks a script against it (exit 1 when over) and prints the table, and a test keeps the card's table equal to the tool
- **Editor handoff.** [`edit_export.py`](../skills/opencut-video-studio/scripts/edit_export.py) turns an edit decision list into a CMX 3600 EDL, an OpenTimelineIO timeline and a CSV shot list; [editor handoff](../skills/opencut-video-studio/references/editor-handoff.md) gives the import steps for DaVinci Resolve, Premiere Pro and CapCut and says plainly that they were not tested in each application
- **Client templates.** An [AV ad script](../skills/screenplay-story-architect/assets/av-ad-script.template.md) (Screenplay Story Architect now owns ad scripts; Copy Voice keeps voice-over and supers, UGC keeps creator reads), a [concept one-pager](../skills/commercial-video-campaign-director/assets/concept-one-pager.template.md), a [music-video treatment](../skills/creative-music-video-director/assets/music-video-treatment.template.md) and a [creator brief](../skills/ugc/assets/creator-brief.template.md) with usage rights row by row, each ending in an assumptions box; [client projects](../skills/pipeline-core/references/client-projects.md) adds the rule for a client version of a document
- **Files, not only descriptions.** [`board_compose.py`](../skills/storyboard-board-architect/scripts/board_compose.py) lays a storyboard out as PNG pages and one PDF with exact labels in the bundled Inter (Polish no-break rules, nothing cut, placeholders for missing frames); [`sheet_export.py`](../skills/storyboard-sequence-architect/scripts/sheet_export.py) writes a shot list or AV script as XLSX (standard library), CSV and PDF; [`check_shot_plan.py`](../skills/storyboard-sequence-architect/scripts/check_shot_plan.py) is a Python port of the shot-plan checker with the same result as the Node checker; [`prompt_pack.py`](../skills/video-prompt-architect/scripts/prompt_pack.py) exports and checks a prompt pack before credits are spent; [`clip_review.py`](../skills/video-prompt-architect/scripts/clip_review.py) measures returned clips and puts first, middle and last frames on one contact sheet
- **Generator dialects.** The [generator dialects card](../skills/video-prompt-architect/references/generator-dialects.md) translates one shot card into Veo 3.1, Runway Gen-4.5, Kling 3.0, MiniMax H3 and Seedance 2.x phrasing from the makers' guides read 2026-10-11, with the consumer surfaces, a 60-day refresh cadence and provisional use without browsing; it records that Kling 3.0 translates Polish dialogue into English
- **Registered everywhere.** Seven capabilities (`vo_budget`, `edit_export`, `board_compose`, `sheet_export`, `shot_plan_check`, `prompt_pack`, `clip_review`) in the capability card, seven new Python suites in `scripts/check_all.sh` and the release script, and the knowledge map
- **4.5 in part.** Ad-script ownership is settled; Polish trigger terms move to Phase 5.1; merging the eleven video skills into pointer stubs is left to the owner because skill IDs, invocations and routing stay stable

## 1.62.0, 2026-10-11

From Phase 3 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md) (premium motion), last part:

- **Clause-aware caption cues.** When a cue built from timed words must be cut and has no punctuation to cut at, Caption Studio cuts before a word that opens a clause (`and`, `because`, `which`; `i`, `ale`, `że`, `który`), the incoming word included, or at the longest clear pause, so transcripts without commas still break between thoughts ([captions](../skills/caption-studio/assets/captions/README.md))
- **Polish word timing for Animate voice-overs.** The bundled Animate engine stays byte-identical; its voice tool recognises English only. The new [animate-voice](../skills/hyperframes-workflow/assets/animate-voice/README.md) tool sets the word times of a Polish or other-language voice-over in the piece's `voice.json` afterwards: from supplied timings, local faster-whisper with a multilingual model, or a syllable estimate with pauses; matching keeps Polish letters and fills missed words between their neighbours
- **Twenty runnable library records.** [`runnable-snippets.json`](../skills/hyperframes-workflow/assets/motion-prompt-library/README.md#runnable-snippets) turns twenty original records into contracts made only of declared scene kinds; `node library.mjs snippet <ID>` writes one, brief lookups mark records that have one, and a test checks every snippet with the storyboard checker (no warnings) and renders it with the Python renderer
- **glTF product turntable.** A Remotion template turns the client's approved GLB or glTF model under studio light with a contact shadow and a title, in 1:1 and 9:16, loading the model before any frame is captured and fitting it to the frame; it ships with an original synthetic sample jar and its standard-library generator, and rendered in the container to a 180-frame MP4 ([turntable](../skills/remotion-video-production/assets/gltf-turntable/README.md))
- **Registered everywhere.** The capability card (`animate_voice`; the turntable under `remotion_render`), the environment check (a `gltf-turntable` workspace), the runtime map and the motion toolkit inventory with its exact-pin check know the new parts

## 1.61.0, 2026-10-11

From Phase 3 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md) (premium motion), fourth part:

- **Photo hero.** A new `photo-hero` scene kind: an approved photo covers the frame around a focus point, pushes in slowly and can drift up for depth, under a shade that keeps the headline lines readable above the bottom safe area; it exits with a fade only, and the checker warns when the drift would show the photo's edge
- **Line chart.** A new `line-chart` scene kind: 2 to 12 points on one scale, the axis and labels settle, the line draws from the first point to the last and each dot and value appear when the line arrives; labels wider than their slot stop the render
- **Word-by-word entries.** `line-reveal` takes `entry: 'words'`: every word enters in turn, rising from its mask or springing up with the new `easeOutBack` easing (`wordMotion: 'pop'`), with the Polish word groups kept together
- **Persistent elements.** A top-level `persistent` list keeps a logo or a short tag (price, offer, address) on screen across scenes, above the scenes and below the captions, in any corner inside the margin and safe area
- **One geometry everywhere.** `lineChartLayout`, `lineChartReach` and `lineWords` compute the line, its arrival frames and the word groups identically in the three scene-engine copies and the Python renderer (render.py 1.6.0); tests compare them and the rendered pixels with the browser. Contract checks, sound cues, Remotion types and the craft critique know the new kinds; example `photo-and-trend` in 9:16 and 16:9 with an original synthetic photo and mark ([scene kinds](../skills/hyperframes-workflow/assets/motion-scenes/README.md))
- **Critique knows the overlay and the text width.** The craft critique judges layout and composition without the persistent overlay, treats a photo hero as full bleed, and reports any word wider than its column as a layout error from the renderer's own measurement, also with `--no-frames`

## 1.60.0, 2026-10-11

From Phase 3 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md) (premium motion), third part:

- **Ad templates.** Three 15-second 9:16 storyboards with 4:5 and 1:1 formats: offer (Sale poster), product (Product light) and testimonial (Editorial serif). Every format passes the storyboard check with no warnings and renders without overflow; the copy is placeholder and listed for replacement ([ad templates and variants](../skills/hyperframes-workflow/assets/motion-variants/README.md))
- **Brand kit and variants.** `variants.py brand` copies a client's kit colours into a motion contract, declares a bundled headline font's faces and reports WCAG contrast; `variants.py expand` writes one contract per copy, language or token variant (it may only replace existing copy IDs, and new text goes back to proposed) with a check command per variant and a render command per variant and format
- **Active-word captions.** A `captions.tokens.preset` of `active-word` shows whole words in boxes and highlights the spoken one, from per-word frame spans in `caption.words`; the same layout in the three scene-engine copies and the Python renderer, with a pixel parity test. Caption Studio carries word timings into the contract; example `social-captions`
- **Sound tonal balance.** Mastering applies a balanced tone by default (low-mid trimmed, presence and air lifted; `--tone flat` keeps the design), reports a phone-speaker check, and impacts gain a short midrange knock that phones can play ([motion sound](../skills/hyperframes-workflow/assets/motion-sound/README.md))
- **Runtime map.** One host-first map (no code execution, code execution, shell) of every motion capability, checked against the capability card by a test ([runtime map](../skills/hyperframes-workflow/references/runtime-map.md)); the brief index tags each brief type with the scene kinds every renderer runs and a contract that renders as it is

## 1.59.0, 2026-10-11

From Phase 3 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md) (premium motion), second part:

- **Lower third.** A name and an optional title above the bottom edge or the safe area, with an accent bar that rises before the lines slide up from their masks; left-aligned or centred. Text that would be cut stops the render instead
- **Bar chart.** One to eight rows on a shared scale: each label settles, its bar grows from the left and the value counts up at the bar's end, formatted like `counter` (locale, decimals, prefix, suffix); room is kept for the value, and a value too wide for it stops the render
- **One geometry everywhere.** `lowerThirdLayout` and `barChartLayout` compute every size in whole pixels in the three scene-engine copies and the Python renderer; tests compare the layouts, the counted values and the rendered pixels between the browser and the renderer. Contract checks, the sound planner (knocks and ticks on landing) and the Remotion types know both kinds ([scene kinds](../skills/hyperframes-workflow/assets/motion-scenes/README.md))
- **Example** `data-and-names`: a founder's lower third, three sales channels in Polish złoty and an end card in the Product light style with bundled Inter, in 16:9 and 9:16
- **Fonts in reviews.** The frame-review tool embeds contract font files in its preview, so browser screenshots use the same type as the MP4

## 1.58.0, 2026-10-10

From Phase 3 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md) (premium motion), first part:

- **The same typeface in the preview and the MP4.** A motion contract can declare its fonts (`fonts: [{family, weight, file | url | data}]`). The Python renderer (1.5.0) uses exactly those files with the browser's weight matching; the player registers them, waits for them before its review and export, and reports them. A file resolves next to the contract, in `--font-dir` or in the [bundled fonts](../skills/pipeline-core/assets/fonts/README.md); `embed_fonts.py` embeds them for a local preview file, and the published player serves the bundled fonts itself. Contract checks validate the faces
- **Four commercial styles with real fonts.** Sale poster (condensed Archivo, price last), Editorial serif (Fraunces), Product light (Inter, device and counter) and Bold grotesque (Bricolage Grotesque), each with contrast-checked tokens, motion, a signature and a music palette ([styles](../skills/hyperframes-workflow/assets/motion-styles/README.md))
- **Fuller vertical frames.** `tokens.contentScale` (0.5 to 2) enlarges everything authored for the 1080 px short side, set per format (for example 1.25 in 9:16); identical in the three scene-engine copies and the Python renderer, with a parity test
- **Repository only.** The GitHub Pages workflow publishes the bundled fonts next to the player

## 1.57.0, 2026-10-10

From Phase 2 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md), the client business layer. Every rate, VAT status, term and right is the user's input; Studio holds no prices and personalises nothing (owner decision of 2026-10-10):

- **Offers priced from the user's rates.** [Client offer and quote](../skills/brief-architect/references/client-offer-and-quote.md): packages that differ in outcome, revision rounds, timeline, rights in plain words (transfer or licence, fields of use), payment and validity; `quote_calc.py` computes net, VAT or a stated exemption, gross, discount and advance with decimal rounding and writes the offer in Polish or English; it refuses an hourly item without a rate, an exemption without its basis or an advance above 100 %
- **Client intake** in [Polish](../skills/brief-architect/assets/client-intake.pl.md) and [English](../skills/brief-architect/assets/client-intake.en.md), and commercial fields in the Brief Contract (decision maker, budget, deadline, rounds, use, rights, client materials, acceptance)
- **Concept presentation, revision tracker and changes of scope.** Two or three directions in context with a recommendation and a numbered decision; feedback consolidated and classed as a revision, our error (never counted) or a change of scope (quoted before work starts)
- **Client handoff.** Files grouped by use with sortable names, fonts and licences, a [handoff letter](../skills/delivery-documentation/assets/handoff-letter.pl.md) with the agreed rights and a plain AI-assistance line, an [acceptance protocol](../skills/delivery-documentation/assets/acceptance-protocol.pl.md) (protokół odbioru) and a case-study template that uses only the client's consent and figures
- **Brand kit.** One file per client (colours, fonts and licences, logo files, voice, approved and banned claims, legal lines) read by every owner; the static compositor accepts `brand:primary`, `brand:headline` and `brand:logo.white`; where to keep it in ChatGPT, Claude, Codex and Claude Code
- **Client email kit** (questions, offer, concepts, feedback summary, files, payment reminder, testimonial request), a **brand voice guide** template, and **KPIs and budget scenarios** in the campaign pack (client data or labelled assumptions, never invented benchmarks)
- [Client projects](../skills/pipeline-core/references/client-projects.md) maps the path from enquiry to acceptance and which owner makes each document

## 1.56.0, 2026-10-10

From Phase 1 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md) (static graphics and Polish quality) and the first host evaluation run:

- **Exact text for client finals.** A second route for visible text: a background without text (generated with reserved calm zones, supplied or flat) and the new [static compositor](../skills/static-graphic-design-creator/assets/static-render/README.md), which sets every word, price, logo and legal line in a real font at the exact size, writes PNG, JPG and a print PDF with bleed and crop marks, stops instead of cropping a word or drawing a missing glyph, and measures contrast and safe areas. One-pass generation stays the default for concepts; [exact-copy compositing](../skills/static-graphic-design-creator/references/exact-copy-compositing.md) is the default for finals with a price, date, logo, legal line or print files, always named to the user. The text policy and the rules that allowed only one pass now describe both routes
- **Bundled fonts.** Eighteen OFL fonts in six families (Inter, Archivo, Bricolage Grotesque, Fraunces, Anton, Source Serif 4) with the full Polish alphabet and typographic marks, built reproducibly by `scripts/build_fonts.py` from google/fonts `bd8f81d` ([fonts](../skills/pipeline-core/assets/fonts/README.md))
- **Polish copy standard and checker.** Quotes, dashes, no-break spaces, money, dates, time, sentence-case headlines and one form of address ([standard](../skills/copy-voice/references/polish-copy-standard.md)); `pl_copy_check.py` applies only typographic fixes and counts characters against dated channel limits; a Copy Pack template
- **Dated snapshots.** [Channel copy and format limits](../skills/research-evidence/references/channel-specs-snapshot.md) (Google RSA confirmed; Meta, LinkedIn, TikTok, SEO and email from the best available sources, marked as such) and [Polish and EU marketing rules](../skills/research-evidence/references/marketing-rules-snapshot.md) (Omnibus price reductions, paid-content labels, marketing consent under the PKE, AI Act art. 50 from 2 August 2026, green claims from 27 September 2026, health, alcohol and credit claims). Within 90 days each satisfies its research trigger in Quick mode. The claim ledger gains a rules column; Studio drafts compliant wording, counsel decides
- **Image probe.** Measures an actual raster against its placement or print size (ratio, effective ppi with bleed, transparency, sharpness, OCR against the locked copy when installed) and writes phone, thumbnail, greyscale and safe-area previews to look at
- **Format and print presets** and a **direct-production path**: a complete request for a finished graphic gets one direction and the output in one turn
- **Fewer questions.** After offering directions Studio asks one question, which direction, labelling each with its route; route and format come after the choice (found by the host evaluation, case S01)
- **Digit groups stay together** (`1 299 zł`) in the motion engine (all three copies), the Python renderer (1.4.1) and the compositor, with a parity test
- **Repository only.** `scripts/host_eval.py` runs Studio in headless Claude Code against a 15-case suite with deterministic checks and an optional advisory judge ([docs](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/host-evals.md)); the first run on 1.55.0 passed 12 of 15 for USD 1.68 (one harness defect, one case not applicable without the Studio name, one product finding, all resolved and rerun)

## 1.55.0, 2026-10-10

From Phase 0 of [the improvement plan](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/docs/improvement-plan-2026-10.md), after the six-review audit of 1.54.0 (owner decisions 1a, 2a and 3a of 2026-10-10):

- **Text is never cropped silently.** The bundled Python renderer lays out every scene before drawing and stops with exit code 4 and `"status": "text_overflow"` when a word is wider than its column, naming the word, its width and the column; `--allow-overflow` keeps the old behaviour on request. A 200 px "Najnowocześniejszy" in a 9:16 column used to render as "Najnowo" ([renderer notes](../skills/hyperframes-workflow/assets/motion-render/README.md))
- **Polish line breaks.** One-letter words (w, z, i, a, o, u) stay with the next word and numbers stay with their units (10 zł, 5 kg, 30 %), through a non-breaking space applied identically in the scene engine (all three copies) and the Python renderer; a test checks the two agree
- **Composition errors block acceptance.** Critique flags a vertical hold whose content fills less than 10 % of the frame (an error) or 25 % (a warning), once per scene and format; the thumbnail check runs for every feed format; URL text is no longer judged as readable copy. Acceptance now blocks on any critique picture error, not only on selected areas. The colour-block example's 9:16 layout was enlarged and scores 95
- **Sound mixing about 15 times faster.** Ducking and level matching use a running-sum moving average instead of a long convolution: the test mix went from 2 min 34 s to 10.5 s with the same audio
- **Startup texts agree with the three-option welcome.** Three references and two evaluation inputs still described a two-mode welcome; they name all three options now, the orchestrator says a mode menu alone is a failed startup, and the validator rejects a two-option description (`STARTUP_MENU_DRIFT`). The welcome itself is byte-identical
- **Two routing contradictions removed.** Marketing's "when to use" no longer claims ecommerce, product and launch planning, which belong to Ecommerce Campaign Strategy Director; the product-film route applies the conditional research gate instead of mandatory research, as the research skill defines it
- **Validation.** Skill descriptions have a total budget (fail above 7,800 characters, warn above 7,500). The historical `validate-package.mjs` / `package.test.mjs` suite is retired (decision 3a): both paths stay as inert stubs, because a hosted update cannot delete files
- **Repository only.** `scripts/release.py` prepares a release in one command (version markers, notes, manifest, checks, records, package, commit, fast-forward push) and records its GitHub publication; `scripts/check_all.sh --fast` is the edit-loop subset; `scripts/check_version_bump.py` and the checks workflow stop a package change on `main` without a version bump; CI validates the plugin and marketplace with a pinned Claude Code; AGENTS.md records the owner's product decisions (no personalization: rates, tools and preferences are runtime inputs)

## 1.54.0, 2026-10-10

From the owner's request of 2026-10-10 to add the skills of [cth9191/animate](https://github.com/cth9191/animate) to the motion graphics module:

- **The Animate engine joins Motion Graphics Workflow.** Short explainers, histories and little stories drawn entirely in code on one canvas, deterministic frame by frame, in seven illustrated styles (cut paper, crosshatch ink, riso print, sketchbook, manim-style math, pixel art, isometric line art) or a look matched from the user's references; story formats and a story grammar, shape-morph transitions, a score composed in code and mastered for phones, voice-over timed to the words or cuts on the beats of the user's own track, several aspect ratios from one piece, and a measured review (beat grid, story-arc loudness, dead beats, text cut off or overlapping, loudness). The upstream skill folder (version 0.4.0, MIT, commit `7e5eb56`) is bundled byte-identical as `skills/hyperframes-workflow/assets/animate-engine/`, with `SKILL.md` renamed `ENGINE.md` so no host lists it as a second skill; Studio adds only a package pin for Playwright 1.56.1. The [Animate engine reference](../skills/hyperframes-workflow/references/animate-engine.md) says when to choose it and how Studio's approvals, research gate, acceptance verdicts and provider rules apply; its story grammar, frame checklist and craft rules guide motion plans on every host.
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
- **Proved on a full environment.** In a Linux container the whole set was installed (pip in one virtual environment; Cairo and Pango development libraries for Manim; `npm ci` for the four starters; HyperFrames skills) and the final check passed with 17 of 17 tools (the repository's verification/required-tools-final-check-1.49.0.json). HyperFrames' installation guidance now reflects that it is part of the required set; the HeyGen catalog still stays off unless asked for.

## 1.48.0, 2026-10-09

From the owner's request of 2026-10-09: a fixed, validated tool list per host, and a correct installation path for Claude; the welcome and menus are unchanged:

- **Tools by host.** The environment check's `tools.json` now gives every tool (Python, Pillow, NumPy, CairoSVG, FFmpeg, FFprobe, Node.js, npx, Chrome or Chromium, Remotion, GSAP, HyperFrames) a status on each of five hosts: ordinary ChatGPT, ChatGPT Work, Codex, Claude Code and the Claude apps. The statuses are `observed` (owner-reported, with the evidence), `check` (may be in the sandbox), `install` (the user's machine), `per_project` (npm in a project) and `not_supported` (with the reason). `check_environment.py --matrix` prints the list, `--host` names the host (detected by default from documented traces), and on a named host a tool the host cannot run is `not_on_this_host`, not missing. The [README table](../skills/workflow-orchestrator/assets/environment-check/README.md#tools-by-host) is generated from the same data and tested; the validator requires a valid status for every tool on every host and evidence for every `observed` and `not_supported`.
- **Installation in Claude.** The repository is now a Claude plugin marketplace (`.claude-plugin/marketplace.json`, marketplace `framecore-works`), and the package has a Claude manifest (`.claude-plugin/plugin.json`) with the same identity and version. The repository's CLAUDE_INSTALL.md gives the pinned install for Claude Code (`/plugin marketplace add FrameCoreWorks/framecore-works-creative-studio#v1.48.0`, then `/plugin install framecore-work-creative-studio@framecore-works`) and for the Claude apps (Customize > Plugins), verification, updates and the differences from ChatGPT and Codex. The validator checks the Claude manifest's identity; `tests/test_claude_plugin.py` checks the marketplace, the documented naming rules and limits, and runs `claude plugin validate` when Claude Code is installed.
- **Tested in Claude Code 2.1.295:** both manifests pass `claude plugin validate --strict`; a marketplace install lists 37 skills; headless conversations gave the complete English welcome for the bare name, the complete Polish welcome for a Polish greeting, and a direct answer, without the welcome, for a pasted question.

## 1.47.0, 2026-10-09

From the owner's report of 2026-10-09: a new thread with a screenshot and the Studio link got the welcome instead of help.

- **Content is a task, not a startup.** When Studio is invoked together with a screenshot, image, file or pasted text, or right after an unanswered user message in the thread, it reads that content first (including the text inside a screenshot), infers what the user wants (answer the question shown, solve the problem shown, edit or review an image, write a prompt, plan a video, learn a skill), routes to the owning skill and helps at once. With two plausible readings it helps with the likelier one and offers the others in one numbered line; it asks one targeted question only when no useful step is possible. The complete welcome stays for a bare invocation (only the Studio name or link), a greeting, a question about what Studio can do or an explicit menu request. Rules in the Workflow Orchestrator entry, its description and [startup and creative menus](../skills/workflow-orchestrator/references/startup-and-creative-menus.md#invocation-with-content), with a worked example (a Facebook post about ChatGPT moving truck parts during a PNG cut-out).
- A planned evaluation case (LM25) records the owner's report; the learning-mode validator pins the rule and a Studio test checks it. Welcome text and menus are unchanged.

## 1.46.0, 2026-10-09

From the owner's comparison of a 20 s vertical shop reel with a HyperFrames Studio film (2026-10-09); the welcome and menus are unchanged:

- **Argument before look.** A new [commercial motion](../skills/hyperframes-workflow/references/commercial-motion.md) reference: for an advert or promo, Studio derives audience, action, benefit, friction, available evidence and verified claims, weighs a few different concepts internally, and records the chosen one in the contract's new `strategy` (hook with the scene that pays it off, a CTA that closes the action the film showed, rejected concepts with reasons); every scene says which step of the argument it adds (`argues`). `check-score.mjs` (identical in both starters) fails an unverified claim used in the copy, a missing `argues`, a hook without a later payoff and a CTA without the action it closes.
- **Picture proved on real frames.** The opening, first readable, densest and ending frames are saved at full size and phone scale before a film grows; carrier transitions replace a default wipe; photographs match their background or are isolated; pacing comes from information. The craft critique gains rules for repeated full-frame wipes, an opaque photo background on another scene colour, an empty first frame in feed films, and still stretches measured four times a second from the frames, where drift counts as still while appearing content counts as a beat.
- **Every visible word is checked.** New `text-audit.mjs` (with `text-audit.browser.js`) audits any HTML composition (Studio preview, HyperFrames, GSAP): each word's glyphs after fonts and transforms against the frame and every clipping ancestor, the element's own box included. A cut or hidden word in a readable hold fails; during a transition it is `transitional`; `data-layout-ignore` and similar flags never exempt visible text; a deliberate cut needs `data-text-clip-ok` with a reason and a pixel review. It writes a phone-scale contact sheet with cut words outlined. `review-frames.mjs` runs the same audit on every review frame.
- **Four acceptance verdicts.** New `acceptance.py` keeps technical, fidelity, composition and temporal verdicts separate: a valid export never passes the picture, a contract-only score (any number) leaves composition not_verified, composition needs a person's judgement of the key frames, and temporal needs a recorded normal-speed viewing. The critique now states `score_scope` and its own `verdicts`, including that it cannot see text completeness (a word cut by a mask leaves tidy pixels). The QA record has the four verdicts, coverage, exceptions and the stop decision.
- **Regression evidence.** Original fixtures reproduce the reviewed reel's defects (the clipped "TWÓJ WYBÓR" with and without `data-layout-ignore`, lines hidden by a box that fits the frame) and cases that must pass (complete Polish text, a transition mask, a declared exception); a 20 s 1080 x 1920 30 FPS silent proof contract was rendered and accepted through the whole chain. Ten Python tests, a contract test and two browser tests; a before/after record in the repository (verification/perfua-regression-1.46.0.json).

## 1.45.0, 2026-10-09

The owner asked on 2026-10-09 for Studio to check its environment at installation and with one command; the welcome and menus are unchanged:

- **Environment check.** One command, [`check_environment.py`](../skills/workflow-orchestrator/assets/environment-check/README.md), shows what Studio's tools can use where it runs: Python, Pillow, NumPy, CairoSVG, FFmpeg and FFprobe, Node.js and npx, Chrome or Chromium (including Playwright's copies), Remotion and GSAP per project, and HyperFrames' CLI and installed skills. Each tool is `ok`, `behind`, `below_minimum`, `missing`, `not_installed` (optional), `per_project` or `unknown`; each capability of the capability card is `ready`, `missing` (with what Studio delivers instead) or `unknown`; install and update commands follow for Linux, macOS or Windows, grouped into needed, optional and newer versions. Newest versions come from a snapshot dated 2026-10-09 or, with `--online`, from PyPI, npm, nodejs.org, endoflife.date and Chromium's stable channel. It installs nothing.
- **At installation and on request.** The Codex and ChatGPT Work installation guides run it once after the plugin is saved and show the user the result; Studio runs it whenever the user asks what is installed, and once before the first coded render when nothing shows the tools work. Install steps run only when the user asks. In ChatGPT the check describes the conversation's sandbox, not the user's computer.
- The validator checks that `tools.json` covers every checkable requirement of the capability card and maps each tool to a requirement, capability or pinned project file (`ENVIRONMENT_CHECK`), with a Studio test; 9 Python tests cover statuses, minimums, newest versions, per-project packages, HyperFrames skills and that offline runs never open a connection.

## 1.44.0, 2026-10-09

The owner's decision of 2026-10-09 on HyperFrames (1a: an optional engine where a shell exists, installed with a pinned command, not copied; 2a: the HeyGen catalog only on request); the welcome and menus are unchanged:

- **HyperFrames as an optional engine.** A new [engine reference](../skills/hyperframes-workflow/references/hyperframes-engine.md), checked on 2026-10-09 against heygen-com/hyperframes at commit `3aa6886` (CLI 0.8.143, Apache-2.0), says when Studio offers HyperFrames (a shell with Node.js 22, FFmpeg and Chrome, such as Codex or a local project, and a brief that benefits: a launch film from a website, a longer narrated video, word-level captions on footage or a music-driven edit), how it is installed with a pinned version (HyperFrames' own plugin, or its skills by command; never copied into this package), and who decides what: Studio keeps intake, approvals, copy, storyboard and review, HyperFrames composes and renders. Choosing area `8` still never selects an engine.
- **HeyGen catalog only on request.** HyperFrames' `media-use` catalog (music, effects, images, voice, avatars) is used only when the user asks for it and has a HeyGen account; website assets only when the user owns the site or allows it, with each source recorded.
- The Motion Graphics skill, its code-based workflow, the capability card (`hyperframes_engine`, executed externally, shell hosts only) and the knowledge map link it; a test keeps the engine optional and the area-`8` rule intact. No HyperFrames render has been run through Studio; the route is planned, not verified.

## 1.43.0, 2026-10-09

From the full review (the repository's docs/reviews/full-review-2026-10-08.md); the welcome and menus are unchanged:

- **Video-generator snapshot.** A dated [map](../skills/research-evidence/references/video-generator-snapshot.md) of twelve video families checked on 2026-10-09 (Google Veo 3.1 and Gemini Omni, Kling 3.0, Seedance 2.0 and 2.5, Wan 3.0, MiniMax H3, Runway Gen-4.5 and Aleph 2.0, Luma Ray3.2, Grok Imagine Video 1.5, Midjourney Video V1, LTX-2, and Sora as retired since 24 September 2026), with model IDs, operations (text and image to video, first and last frames, references, editing, extension, native audio), limits that shape prompts, multi-model surfaces and a watchlist. Every fact is labelled as read on the maker's page, read through a search summary or secondary. Research Evidence, its model mapping and the Video Prompt Architect start from it and still recheck the exact target before a model-specific prompt.
- The validator checks that each dated generator snapshot states its date and that Research Evidence cites the same date where it links it (`SNAPSHOT_DATE`), with a test.

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
