# plugin-dev skill review, 2026-10-26 (package 1.142.0)

Owner-opened bounded task (handover of 2026-10-24, "Plugins, owner 2026-10-26"): run plugin-dev `plugin-validator` and `skill-reviewer` over the Studio plugin and its 37 skills. Read-only review; no package file changed. Baseline `c7031b2`.

## Method and evidence

- `plugin-dev:plugin-validator` over the Studio plugin, the marketplace and the three companion plugins, including `claude plugin validate`.
- `plugin-dev:skill-reviewer` in four batches (10 + 9 + 9 + 9 skills).
- Repository checks on the baseline: `validate-studio.mjs` exit 0; `check_all.sh --fast` PASS.
- The coordinator re-read the main findings in the files (marked **verified** below). The other findings are the reviewers' reports with path:line evidence, not re-read.
- Not run: installed-client loading or triggering (`NOT_RUN`), host evaluations, links inside reference and asset files, script behaviour.

## Plugin validation: PASS

0 critical, 0 important. Manifests agree on name and version (1.142.0; companions 1.0.8, 1.0.2, 1.0.1); `claude plugin validate` passes for the marketplace and all four plugins; 37 valid frontmatters, names match folders, descriptions total 7,468 characters; every skill has `agents/openai.yaml`; no broken SKILL.md links. Minor: `hyperframes-workflow/SKILL.md` is 33,196 bytes (no budget applies to it); the orchestrator has 149 bytes of room; companion plugins have no listing icon. The validator's advice to add an install command to README conflicts with AGENTS.md and is ignored.

Skills listed without a description in the Claude Code skill listing (storytelling, ugc, video-prompt-architect, storyboard-sequence-architect, static-graphic-design-creator and others) all have valid descriptions in their frontmatter: host listing truncation, kept by decision (2026-10-24 review, minor 2).

## Skill findings

### Important

1. **Caption Studio burn-in default contradicts its own dated card** (verified). `caption-studio/SKILL.md:66` keeps 14 % for organic 9:16 posts and `--bottom 0.35` only for paid placements, citing the motion compendium; `caption-studio/references/platform-caption-specs.md:9` (checked 2026-10-25 on Meta Business Help) applies the 14/35/6 % zone to all 9:16 Meta placements, organic Reels included. `hyperframes-workflow/references/motion-compendium.md:27` still says Meta publishes no figure. Trigger: stale dated fact.
2. **Shot Sequence description claims coded-video storyboards** (verified). `storyboard-sequence-architect/SKILL.md:3` "including a motion storyboard for coded video" against `:52` (Motion Graphics authors its own storyboard) and `hyperframes-workflow/SKILL.md:63`. Fix: delete the clause (-47 characters).
3. **Copy Voice client email kit: two instructions** (verified). `copy-voice/SKILL.md:35` uses the kit in the client's language and translates from English; `:39` starts from the Polish kit. Fix: drop the `:39` sentence.
4. **Studio Core ChatGPT metadata presents it as a router** (verified). `pipeline-core/agents/openai.yaml` "Route multi-stage work through gates and QA loops", implicit invocation on, while the description gives routing to the orchestrator. Fix: a non-routing short description such as "Shared project state, gates, handoffs and QA loops".
5. **Motion Graphics description promises sound** (verified). Description "with designed sound" against `hyperframes-workflow/SKILL.md:56` (silent unless the user asks). Fix: "with optional sound" (0 characters). Also `:25` (HyperFrames by default in a shell host) against `:48` ("can be offered", Node 22).
6. **Brand Strategy body claims commerce work** (verified). `marketing/SKILL.md:13` "offer framing … launch kits" against its description "without a commerce goal". Body-only fix.
7. **Visual Campaign description indistinct from Video Campaign.** Suggested: "Shared visual system and format adaptation for a static or mixed campaign family. One static piece goes to Graphic Design." (-1).
8. **Reference Pack overlaps Asset Manifest** (both claim exclusions and continuity carriers; no hand-off). Suggested description in the batch-3 report (about -5).

### Minor (body text, no description cost)

- Copy Voice description claims "short dialogue lines" while `:147` gives dialogue to Story And Screenplay (optional, -22).
- `ecommerce-campaign-strategy-director/SKILL.md:79` sends static direction to Visual Campaign; `:80` and Visual Campaign send a single piece to Graphic Design.
- `static-graphic-design-creator/SKILL.md:35` "the three" against `:37` "normally 2–4" (verified).
- `audio-production-director/SKILL.md:12` "not an automatic audio analyser" against `:8`, `:20` (measured review).
- `pipeline-core/SKILL.md:30` broad trigger against `:124`; `:150` Hipson routing broader than "explicit-only"; `workflow-self-improvement/SKILL.md:32` reads as an implicit trigger.
- `hipson-adapter/agents/openai.yaml` short description does not mention Hipson.
- `studio-workstyle-profile/SKILL.md:39` host list omits Claude Code.
- `delivery-documentation/SKILL.md:20` omits FrameCut's own review of its finals.
- `image-prompt-architect/SKILL.md:10` against `:28`: when a text-bearing raster stays here.
- Name drift: "Board Architect", "Sequence Architect" (`storyboard-sequence-architect:98`, `storyboard-board-architect:47`); "the Motion Graphics" (`output-critic-iteration:12,53`, `delivery-documentation:20`, `creative-video-producer:89`, `commercial-video-campaign-director:24`, `workflow-orchestrator:125` "Motion Graphics's", -2 bytes).
- Polish-first links in `brief-architect/SKILL.md:23` and `delivery-documentation/SKILL.md:36`.

### OK

cinematography, commercial-video-campaign-director, creative-music-video-director, screenplay-story-architect, remotion-video-production, humanizer, research-evidence, tool-routing-cost, producer-ai-task-builder (intentional alias).

## Budget effect of the suggested description edits

-47 (Shot Sequence), -1 (Visual Campaign), about -5 (Reference Pack), 0 (Motion Graphics), optional -22 (Copy Voice): the total falls from 7,468 to about 7,393 of 7,800. The orchestrator edit is -2 bytes.

## Status

Important findings 1 to 8 fixed in 1.143.0 (CC-20261026-07, owner's go-ahead 2026-10-26). The code review of the fix found the same stale caption margin in four more places (the captions tool help and README, the channel specs snapshot, the motion review README and a `critique.py` comment), fixed in the same change. Finding 2 also needed the router side: the Motion Graphics description now names its storyboard, and Shot Sequence hands coded motion over explicitly. Descriptions total 7,507 of 7,800 characters; the orchestrator is unchanged (31,851 bytes).

Host evaluation in headless Claude Code (plan usage, cases RV01 to RV03 in the gaps set):

- RV02 (storyboard for a coded reel): FAIL before (Shot Sequence loaded), FAIL after the first fix, PASS after the router fix; it is the only case that separates before from after.
- RV01 (organic Reel captions) and RV03 (English client email set) pass on the baseline too in their final wording, so they guard against regressions but do not prove the fix; the fix rests on the verified text contradictions. In their first wording RV01 loaded no skill and RV03 was answered directly by the orchestrator, which handles small tasks itself by design.
- Release gate W01, W02, W04, V01, D01: 5/5 PASS.

The minor findings were fixed in 1.145.0 (CC-20261026-14) on the owner's go-ahead, except two that needed no change: Creative Video Producer's Motion Graphics line was already correct, and Delivery's handoff links already tell Studio to use the client's language. Release gate 5/5.
