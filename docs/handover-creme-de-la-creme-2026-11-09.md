# FrameCore Works: Crème de la Crème
## Screened handover for Claude Opus 5.5

Date: 2026-11-09  
Updated: 2026-11-11; prior additions: Vork under CW-20261110-01 (section 8); Ultra Skills Motion Graphics implementation task under CW-20261110-02 (section 9); Design Canvas knowledge-extraction assessment under CW-20261110-05 (section 10); account-wide Claude token-efficiency report under CW-20261110-07 and workspace methods/tools supplement under CW-20261110-08 (section 11); Cinecode Toolbox qualification and knowledge-extraction tasks under CW-20261110-09 (section 12); Higgsfield reference-guided scene-code proposal under CW-20261110-10 (section 13). Generative Icons/useAnimations reported tests and optional-asset benefit assessment added under CW-20261111-01 (section 14).
Origin: chatgpt-work  
Change-ID: CW-20261109-01  
Status: sections 1–8 and 10–14 are research and assessment tasks with no implementation authorization; section 9 records the owner's separate Motion Graphics implementation task.

**Temporary transfer note, owner instruction 2026-11-10 (CW-20261110-03).** Claude must read this and all older handovers and supporting materials, retain active decisions in maintained project documentation, and tell the owner the plan step by step before implementation. After that intake and presentation, remove this document, all other development handovers and the temporary source pack, repairing incoming links. Follow the [complete intake and cleanup instruction](roadmap.md#temporary-handovers-owner-instruction-2026-11-10); this does not extend the implementation permissions below.

Projects:
- [Creative Studio](https://github.com/FrameCoreWorks/framecore-works-creative-studio)
- [Toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox)

## 1. Owner intent and authorization

Improve Creative Studio's production judgment and output quality by studying useful external repositories, extracting specific techniques, comparing them with the current product, and adapting only demonstrated improvements into existing owners. Adding more plugins is not the goal.

The owner supplied twelve repositories and explicitly asked for duplicates and unsuitable candidates to be removed before this handover. The original queue contains **six sources**, not twelve new integrations. The owner's 2026-11-10 additions bring the current research queue to **nine sources: the original six, Vork (section 8), Design Canvas (section 10) and Cinecode (section 12)**. Design Canvas is a candidate for selective knowledge extraction, not an approved integration. Cinecode has separate Toolbox qualification and knowledge-extraction tasks, not an admitted catalog entry. Cinematic Director, Drama Skills and Claude AI Music Skills are all retained for targeted knowledge extraction. Functional overlap rules out unnecessary parallel workflows, but does not by itself disqualify a useful source of techniques. The six exclusions are retained only as a decision record, so the same work is not proposed again.

The initial task authorized one new handover document in Creative Studio. The 2026-11-10 follow-up authorizes updating this same document to add Vork. Neither scope authorizes changes to other files, either shared package, Toolbox, versions, manifests, dependencies or hosted plugins. Provenance is recorded here instead of modifying the existing development ledger, in accordance with that one-file scope.

For the receiving Claude session, this document authorizes **read-only audit, analysis and recommendations only**. Do not install plugins, skills or dependencies; invoke generation providers or external production API/MCP services; spend credits; upload, publish, deploy, commit or push implementation changes. Present a bounded plan to the owner first. The separately authorized repository save of this handover does not grant Claude implementation or publication permission.

## 2. Verified baseline and evidence limits

| Surface | Inspected baseline |
| --- | --- |
| Creative Studio main | `a0ea8eee553eacdaf74867e515d5caf3b7b66a27`; source package 1.174.1 |
| Toolbox main | `adc8094f8e087889e4337c99dd0d267ae1b11a51`; catalog 1.12.0 |
| Toolbox TasteSkill pin | 2.1.5 at `12af471f627f866411b4bd785b19646d3672784c` |
| Latest published TasteSkill release | [v2.5.1](https://github.com/Leonxlnx/taste-skill/releases/tag/v2.5.1), published 2026-11-07; annotated tag resolves to `f6b76575f949707b4e3c37cd86cb44b0b98643e8` |
| Actual integrations in the owner's Claude session | UNKNOWN; repository files cannot establish which connectors that session exposes |
| Fresh host installation, upstream execution, renders and listening | NOT RUN in this screening |

The screening read repository metadata and complete tree listings, all twelve READMEs, available root licence files, selected relevant skills and code, current FrameCore rules, catalog/reviews, integration decisions and owning Studio instructions. It is **not** a complete security audit of every file, a successful installation test, or proof of production improvement. Retained means a concrete, source-supported reason for deeper analysis; it does not mean approved for installation.

Upstream demonstrations and test descriptions are upstream-reported evidence, not checks executed here. Model capability, price, duration and platform specifications must be reverified against primary documentation when used.

## 3. Screening matrix: all twelve inputs

Pinned links identify the inspected commits. This is a disposition record, not a twelve-repository implementation backlog.

| Source | Licence evidence | Creative Studio disposition | Toolbox disposition |
| --- | --- | --- | --- |
| [HyperFrames](https://github.com/heygen-com/hyperframes/tree/c38ac5438c751094a720c55c68bd15fc6450ec37) | Apache-2.0 | Exclude from this new-source queue: existing runtime route and skill map | NO ADD: no duplicate integration |
| [Remotion Skills](https://github.com/remotion-dev/skills/tree/1af7e69a2a613437d46095924057970a6a7df40d) | No root licence file found in inspected tree; repository licence metadata null | Exclude from this queue: maintain the existing Remotion owner and its official-source refresh route | NO ADD |
| [Claude Animated Shorts](https://github.com/mromidev/claude-animated-shorts/tree/e3b817b6afc6cd413466d43f11ba31209e034bbf) | MIT for code/docs; reference frames explicitly for style study | Exclude: highly project-specific recipe, fixed language/style/audio assumptions, private study references and hardcoded project paths; no demonstrated incremental benefit over existing motion routes | NO ADD |
| [Cinematic Director](https://github.com/wuwangzhang1216/DirectorSKILL/tree/c65ae0d14457053efb1e354c7e7f7e120d97fad1) | MIT | RETAIN: product/macro lighting and symptom-to-repair methods; compare their detail against existing craft | NO ADD now: extract useful deltas without installing a second directing workflow |
| [Drama Skills](https://github.com/zenstory-ai/drama-skills/tree/3d813c30871b4db5f2387d83bdc3a49db8ce7b2b) | MIT; evaluation novel has a separate stated use restriction | RETAIN: targeted continuity/coverage and evaluation-method analysis | NO ADD now: do not install a second production orchestrator |
| [Seedance 2 Storyboard Generator](https://github.com/liangdabiao/seedance2-storyboard-generator/tree/53f749e094374a8215b20edba745e0a6e7af94ca) | No licence file found; README limits contents to learning/reference use | Exclude: reuse permission for the intended adaptation is not established; substantial storyboard/prompt overlap | NO ADD |
| [Shader Skills](https://github.com/gokayfem/shader-skills/tree/a56e7738d3f22698e795f036b4919f0734ab621d) | MIT | RETAIN: procedural GLSL correctness, visual debugging and rendering discipline | Evaluate ADD; not approved and install/benefit evidence still missing |
| [WebGPU Claude Skill](https://github.com/dgreenheck/webgpu-claude-skill/tree/af2319bd01bb7cc881267a9ef42cafdaf5e9029d) | README declares MIT; no root licence file found | Exclude: strong overlap with current threejs-skills covering WebGPU/TSL; README carries mixed r183+/r171+ guidance | NO ADD; licence packaging also needs clarification before reuse |
| [ComfyUI MCP](https://github.com/artokun/comfyui-mcp/tree/707474d24d0d251ba04a1bebdf86620cef2eaa8b) | MIT | REJECT for this round: requires a separately provisioned ComfyUI environment and models; no project-specific advantage demonstrated | NO ADD under current self-contained-entry rules |
| [ElevenLabs Skills](https://github.com/elevenlabs/skills/tree/9763c39a9d7add478b2f2d8229f0caadf5414f5f) | MIT | RETAIN: ANALYSIS ONLY | NO ADD: API-key/provider dependence; inspect existing connector first |
| [Claude AI Music Skills](https://github.com/bitwize-music-studio/claude-ai-music-skills/tree/597d928fb2c8316ee13159771405813174aa01de) | CC0-1.0 | RETAIN: selected music/voice preparation and QC methods only | NO ADD: broad Suno-oriented suite, MCP/hooks/dependency setup, overlap with Audio Production and Earshot |
| [TasteSkill](https://github.com/Leonxlnx/taste-skill/tree/f6b76575f949707b4e3c37cd86cb44b0b98643e8) | MIT; individual photographs retain their own licences | RETAIN: delta-only analysis against methods already adopted | Evaluate UPDATE of existing entry only, after audit, tests and owner acceptance |

“Exclude” is a scope/fit decision, not a claim that a repository is universally poor. Reopen an excluded item only for a new concrete need or changed evidence. Do not re-audit all twelve by default.

### Why existing integrations matter

- HyperFrames already has an owning workflow and [skill map](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/hyperframes-skill-map.md). Remotion has its [production owner](../plugins/framecore-work-creative-studio/skills/remotion-video-production/SKILL.md). This does not claim byte-for-byte inclusion of every current upstream skill.
- Toolbox already lists `pixelfx`, `threejs-skills`, `gl-transitions`, `animate`, `motion-designer`, `huashu-art-motion`, `bang-motion`, `motion-launch-videos`, `stickman-kino` and other motion tools. Category overlap alone does not prove duplication, but another general renderer is not an established gap.
- The existing [TasteSkill decision map](../plugins/framecore-work-creative-studio/integrations/taste-skill/README.md) already records typography, frame/empty space, picture discipline, critique passes and copy methods adapted from 2.1.5. Do not present these as new discoveries.
- Studio already has reference authority, stable shot IDs, continuity states, adjacency checks, audio workbooks and one bounded QA loop. Proposed additions must improve an observed failure in these mechanisms.

## 4. Original research queue: six narrowly scoped sources

### P1: Shader Skills

Inspected version: 2.0.0 at `a56e7738d3f22698e795f036b4919f0734ab621d`.

Read first: [skill](https://github.com/gokayfem/shader-skills/blob/a56e7738d3f22698e795f036b4919f0734ab621d/skills/shader-art-coding/SKILL.md), [bundler/checker](https://github.com/gokayfem/shader-skills/blob/a56e7738d3f22698e795f036b4919f0734ab621d/skills/shader-art-coding/scripts/glsl_tools.py), [verification overview](https://github.com/gokayfem/shader-skills/blob/a56e7738d3f22698e795f036b4919f0734ab621d/README.md#verification).

Useful scope: exact/bounded/approximate distance fields, deformation-safe stepping, diagnostic views, linear-light/tonemapping order, anti-aliasing and temporal filtering, and selecting a minimal rendering model from the intended image. Its procedural scene library and dependency-aware bundler are different from a collection of between-shot transition shaders.

Map to existing Motion Graphics / Remotion instructions and QA. Keep their frame clock and deterministic seeking. Do not create a second VFX orchestrator.

Static inspection of `glsl_tools.py` found local reads/writes and optional invocation of installed `glslangValidator`; no network client in that inspected file. This is not a whole-repository security clearance. Python 3 is needed for its helper; compilation and actual rendering need appropriate tools/graphics support. Hosted compatibility is UNKNOWN until tested.

Toolbox: strongest new-entry candidate here, but the improvement gate is still open. A successful source audit and a meaningful rendered comparison must precede an ADD recommendation. Do not run its paid agent evaluations.

### P1: Drama Skills

Pin: `3d813c30871b4db5f2387d83bdc3a49db8ce7b2b`; release version not verified.

Read first: [storyboard skill](https://github.com/zenstory-ai/drama-skills/blob/3d813c30871b4db5f2387d83bdc3a49db8ce7b2b/skills/short-drama-storyboard/SKILL.md), [review skill](https://github.com/zenstory-ai/drama-skills/blob/3d813c30871b4db5f2387d83bdc3a49db8ce7b2b/skills/short-drama-review/SKILL.md), [evaluation methodology](https://github.com/zenstory-ai/drama-skills/blob/3d813c30871b4db5f2387d83bdc3a49db8ce7b2b/evaluations/README.md).

Study the concrete enforcement details: script-event coverage, visible hand/prop transfers, frozen start frames separated from end states, reference roles and actual versus planned images, revision propagation, and negative controls/held-out cases in evaluation. Determine which of these catches a failure that Studio's current checks miss; the concepts themselves already overlap.

Map to Shot Sequence, Storyboard Board, Character Design, Asset Manifest, Video Prompt and existing Output Critic responsibilities. Do not import its project state, production queue, onboarding or second reviewer loop wholesale.

Toolbox: NO ADD in this round. Source analysis is useful without installing the complete parallel workflow. Use original synthetic test scenes; do not copy the evaluation novel or assume MIT covers every example asset. The English README records an older synchronization date, so verify details against current skill files.

### P1: Cinematic Director, targeted craft extraction

Inspected skill version: 2.1.0 at `c65ae0d14457053efb1e354c7e7f7e120d97fad1`.

Read first: [skill](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/SKILL.md), [product and macro](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/references/product-and-macro.md), [failure diagnosis](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/references/failure-modes.md).

Study material-specific lighting: shaping reflections on glossy objects, bright/dark-field treatment of transparent products, and raking light for matte texture. Also examine how visible symptoms map to likely structural causes, a bounded repair and a recheck. These are useful candidates for deeper craft even though directing and diagnosis already have Studio owners.

Compare against Cinematography's camera/light cards, Video Prompt's video craft, commercial product-film guidance and Output Critic. Keep only a demonstrable missing decision, useful example or stronger acceptance test. Do not import another director, all A–J workflow modes or the named-director style library wholesale.

Treat fixed clip durations, blanket bans on generated text/products and claims that a particular camera/light setup removes generation risk as upstream heuristics, not universal facts. Preserve the brief, verified model capability and actual visual evidence. A locked camera or moving light may reduce one risk; it does not guarantee unchanged product geometry or colour.

Toolbox: NO ADD now. This source stays in the knowledge queue; any later proposal for a separate entry needs a distinct production benefit and its own qualification.

### P0: TasteSkill existing-entry delta audit

Compare `12af471f627f866411b4bd785b19646d3672784c` (2.1.5) with `f6b76575f949707b4e3c37cd86cb44b0b98643e8` (2.5.1). Recheck releases on resume.

Read first: [changelog](https://github.com/Leonxlnx/taste-skill/blob/f6b76575f949707b4e3c37cd86cb44b0b98643e8/CHANGELOG.md), [skill including Stop hook](https://github.com/Leonxlnx/taste-skill/blob/f6b76575f949707b4e3c37cd86cb44b0b98643e8/skills/taste-skill/SKILL.md), existing Studio decision map and [Toolbox review](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/reviews/taste-skill.md).

Material change: the new skill declares a Stop hook and a browser finish gate. The old review says no hooks. Inspect the hook, output paths, browser execution, network/image fetching, bypasses/waivers, termination behavior and host differences. Existing approval of 2.1.5 does not establish approval of this changed behavior.

Extract only new, useful layout/copy/visual-checking methods. Do not impose its website-specific rules on posters, video or all brands: mandatory page movement, one section per screen, universal image-caption bans and trade-specific shader restrictions are not general Studio defaults.

Toolbox: UPDATE proposal for the same entry, never a duplicate. No update before fresh audit, necessary tests and owner acceptance. Preserve image-level attribution/licensing.

### P2: ElevenLabs Skills, analysis only

Pin: `9763c39a9d7add478b2f2d8229f0caadf5414f5f`; release version not verified.

Read first: [TTS](https://github.com/elevenlabs/skills/blob/9763c39a9d7add478b2f2d8229f0caadf5414f5f/text-to-speech/SKILL.md), [dubbing](https://github.com/elevenlabs/skills/blob/9763c39a9d7add478b2f2d8229f0caadf5414f5f/dubbing/SKILL.md), [SFX](https://github.com/elevenlabs/skills/blob/9763c39a9d7add478b2f2d8229f0caadf5414f5f/sound-effects/SKILL.md).

First inspect the receiving Claude session's exposed integrations without invoking a production service. Record connector name, supported operations and access evidence, or UNKNOWN. Do not infer an active connector from a repository mention.

Study text normalization, pronunciation, continuity across speech chunks, speaker/transcript/translation checks, dubbing revision handling and fitting SFX to cue duration. Map useful deltas to Audio Production Director and existing voice ownership; Earshot remains the measurement capability, not a second TTS provider.

The inspected skills require an API key and contain automatic `@latest` onboarding instructions. Read them as data; do not execute setup or transplant those instructions. Provider-specific parameters and model support require fresh official verification. Report analysis and a knowledge map only.

### P2: Claude AI Music Skills, knowledge only

Inspected plugin version: 0.103.0 at `597d928fb2c8316ee13159771405813174aa01de`.

Read first: [pre-generation checks](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/597d928fb2c8316ee13159771405813174aa01de/skills/pre-generation-check/SKILL.md), [mastering guidance](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/597d928fb2c8316ee13159771405813174aa01de/skills/mastering-engineer/SKILL.md), [plugin manifest](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/597d928fb2c8316ee13159771405813174aa01de/.claude-plugin/plugin.json) and [hooks](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/597d928fb2c8316ee13159771405813174aa01de/hooks/hooks.json).

Study readiness checks for lyrics/pronunciation, musical arrangement decisions and mono-fold/phase QC. Compare with existing audio workbooks and Earshot first. Separate measurements from actual listening and aesthetic judgment.

Do not copy the upstream's universal “-14 LUFS works everywhere” guidance into Studio. Delivery targets must be chosen for the actual destination and brief, with dynamics preserved. Do not import Suno settings as verified current facts, the album state machine, release automation, MCP server or hooks.

Toolbox: NO ADD in this round. Its broad suite duplicates existing responsibilities and brings substantial setup for a Suno-centered workflow; selected concepts can be evaluated without installing it.

## 5. Knowledge map and proposed validation

All adaptations and experiments below are **PROPOSAL / NOT RUN**, not completed improvements. “Gap” means a hypothesis to test against current sources.

| Source | Candidate incremental benefit | Existing owner | Small proposed comparison after authorization |
| --- | --- | --- | --- |
| Shader Skills | Detect shader distance, colour and temporal defects more precisely | Motion Graphics, Remotion, existing visual QA | One original procedural material scene; fixed seed/camera and repeated frame seeks; compare debug output, temporal stability, render cost and visual inspection |
| Drama Skills | Catch missing script events and broken reference/prop state through revisions | Shot Sequence, Board, Asset Manifest, Video Prompt | A three-shot prop handoff with a deliberate continuity error, a missing reference and one changed shot; check detection and affected downstream artifacts |
| Cinematic Director | Make material-light choices and generation-error repairs more concrete | Cinematography, Video Prompt, Commercial Video, Output Critic | One original product brief with glossy, transparent and matte variants; compare lighting decisions and repair plans against current guidance; validate any claimed visual gain on authorized media |
| TasteSkill delta | Improve layout-collision and copy checks beyond the already adapted 2.1.5 methods | Graphic Design, Pipeline Core, Copy Voice, Output Critic | Same original brief and exact copy before/after; inspect text overlap, clipping, hierarchy and brand consistency; separately test hook lifecycle only after approval |
| ElevenLabs Skills | Reduce speech-boundary, pronunciation and dubbing handoff errors | Audio Production Director, existing voice route | Read-only mapping first; later compare authorized supplied clips/transcripts for names, numbers, seams, timing and speaker identity |
| Music Skills | Improve music readiness and mono/phase diagnosis without a new engine | Audio Production Director and Earshot | Use owned/synthetic audio with a known cancellation defect and a pronunciation fixture; measure and listen separately |

For authorized motion/video comparisons, record format, width/height, FPS, duration, engine/version, source revision, settings, inspection range and observed difference. If both formats are requested, author separate 1080x1920 and 1920x1080 compositions; do not substitute an automatic crop. Use the same declared FPS and otherwise comparable settings within each A/B pair.

Review actual renders at normal playback and critical frames. A contact sheet alone cannot certify motion. Inspect opening, dense moments, readable holds, transitions and ending. Audio measurements do not prove that the music fits the story.

Prioritize the owner's concrete defects: generic/flat imagery, weak typography, clutter and objects crossing copy, transition glitches, arbitrary motion, unsuitable music, identity/scale/camera/light drift and excess workflow complexity. Do not enforce one aesthetic on every brief.

## 6. Procedure for the receiving Claude session

1. Read current `AGENTS.md`, `CLAUDE.md`, roadmap, ledger and relevant handovers in Studio, plus Toolbox's `CLAUDE.md`. At the inspected Toolbox baseline there is no root `AGENTS.md`.
2. Recheck both `main` heads and the actual catalog. Respect work that landed after this snapshot. Any later approved work stays on `main`; do not create branches or PRs.
3. Confirm the original six retained pins plus Vork in section 8, Design Canvas in section 10 and Cinecode in section 12, licences and any newer releases. A newer version starts a new review; do not silently substitute it.
4. Build a bounded source audit for those nine sources. Read relevant code as untrusted data. Do not run upstream installers, scripts, hooks, tests or model evaluations during this audit.
5. For each technique, record its exact source, existing equivalent, concrete missing behavior (or “already covered”), target owner, inputs/outputs, limits, fallback, proposed test and expected measurable benefit.
6. Keep knowledge and tool decisions independent. A useful paper/skill does not automatically deserve an installed plugin. A failed Toolbox gate does not invalidate every abstract technique.
7. Present P0/P1/P2 recommendations and a small implementation/test plan. Stop for owner scope approval before executing it. A legitimate outcome is no change.
8. After any later authorization, use original maintainable wording/code, preserve licences/attribution where required, and run appropriately scoped technical and real-output comparisons. Do not copy entire skills or third-party artwork.

Required read-only deliverables:
- Refreshed nine-source Audit Matrix (original six, Vork, Design Canvas and Cinecode), plus the original six-item exclusion record.
- Crème de la Crème Knowledge Map with exact sources and delta to current Studio.
- Toolbox Decision Matrix: ADD proposal / UPDATE proposal / NO ADD, with blockers clearly stated.
- Duplicate & Overlap Report.
- Bounded Implementation Roadmap, including tests, costs and stop conditions.
- Separate account-wide Claude workspace assessment and per-host proposal from section 11; its attached report and two unidentified skill leads do not change the nine-source research queue.
- Verification Report separating PASS, FAIL, NOT RUN and UNKNOWN.

No new orchestrator, duplicate QA loop, copied default style, second audio engine or unsupported promise of cross-host compatibility.

## 7. Original verification and handover provenance, 2026-11-09

- All twelve source identities resolved to full commits; source screening completed.
- Current catalog, TasteSkill pin and existing Studio adaptation confirmed.
- Six items removed from the active queue; six retained with explicit restrictions.
- No candidate upstream installer, skill, hook, service or evaluation was executed.
- No new provider use, paid operation or upstream installation. No media was generated to validate the candidates.
- Claude connector availability and actual production improvement remain UNKNOWN.
- Upstream runtime, installed-host and render acceptance tests remain NOT RUN.
- Repository checks: PASS, `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs` and `bash scripts/check_all.sh` both exited 0. Optional checks reported as skipped remain unverified; these are Studio regression checks, not acceptance tests for the six candidates.
- Document checks: PASS, twelve unique pinned source rows, six retained entries, six exclusions, valid relative links and only one new file. Existing tracked files are unchanged.
- Branch inventory before save: only `main` and `gh-pages`; no additional branches created or found.
- Shared-Package-Changed: no.
- ChatGPT-Work-Sync / Codex-Sync: not_run; no hosted update is needed for this repository-only document.
- Only this new handover is in scope. Existing files and Toolbox remain unchanged.

Start on resume by verifying the current inventory, then analyze the original six retained sources, Vork and Design Canvas below and report evidence-backed deltas. The measure of success is better production results with justified complexity, not more integrations.

## 8. Owner addition: Vork, 2026-11-10

Repository: [voyager-so/vork](https://github.com/voyager-so/vork).
Owner instruction: add this repository to Claude's handover for **both Toolbox qualification and Crème de la Crème knowledge extraction**. This is a general 3D/VFX production candidate, independent of the [map companion and Lemo review](handover-map-motion-companion-2026-11-09.md). It is not a map requirement or an approved installation.

This addition expands the active research queue to **seven sources: the original six plus Vork**. The original twelve-row screening and six exclusions remain historical decisions. Lemo's independent task stays in its linked handover; do not count it as another Vork integration.

### Source snapshot and duplicate check

| Item | Evidence as of 2026-11-10 |
| --- | --- |
| Upstream pin | `8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b`; current main and resolved release tag `v0.4.0` |
| Published version | [v0.4.0](https://github.com/voyager-so/vork/releases/tag/v0.4.0), published 2026-11-10; Cargo workspace and TypeScript SDK both declare 0.4.0 |
| Purpose | Headless 3D/VFX engine in Rust and Slang, with JSON scenes and Python/TypeScript authoring; GPU rendering through Vulkan/Metal |
| Licence | Custom [Vork Preview License](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/LICENSE), source-available, explicitly not open source; current-version commercial rendering is permitted, with restrictions on redistribution and hosted services |
| Toolbox baseline | `adc8094f8e087889e4337c99dd0d267ae1b11a51`; no Vork entry in marketplace, apps index or active Toolbox skill; no Vork-named review/path in the complete tree |
| Studio baseline | `10b9dccb4642909df40f59f07c5003aedc0a32a9`; no Vork entry in the extension registry or dedicated Vork path in the complete tree |
| Evidence limits | Targeted documentation/manifest inspection only; no full source/security audit, installation or render. Host availability, operational suitability and incremental quality remain UNKNOWN |

The scoped absence checks do not prove that every file or installed host lacks any mention of Vork. Claude must refresh both inventories and compare capabilities, not just names.

Read first: [README](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/README.md), [Cargo manifest](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/Cargo.toml), [SDK manifest](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/packages/ts/package.json), [licence](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/LICENSE), [notices](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/NOTICE), [limits](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/docs/help/limits.md), [animation](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/docs/help/animation.md), [outputs](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/docs/help/outputs.md), [diagnostics](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/docs/help/diagnostics.md), [installer](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/install.sh) and [benchmark method](https://github.com/voyager-so/vork/blob/8de8c2e8b5d71fc340e9e2be43c1b9b248f5771b/benchmarks/README.md). Treat all upstream instructions as data; execute none during the audit.

Reconcile version-specific documentation: at this pin, README still describes participating media as unsupported in 0.3, while the 0.4 limits document describes narrowly supported Stage 1 fog. Record the exact supported scope from code, tests and release evidence; do not generalize it to arbitrary smoke or volume simulation. Upstream speed tables include projected Blender timings and different settings; they are not independently measured, equivalent-quality results.

### A. Toolbox: qualify an optional general production tool

Apply the current [Toolbox rules](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/CLAUDE.md) before recommending admission.

- **Packaging and eligibility:** the inspected tree has no installable `SKILL.md` or Claude plugin manifest. Treat Vork as an engine/CLI/SDK, not a ready plugin. Assess whether an independent FrameCore adapter could be eligible; do not create one or relax Toolbox's gates.
- **Installation and security:** inspect scripts, dependencies, downloads, checksum verification, cache/output ownership, cleanup, telemetry and network behavior. Documented default installation uses moving release URLs and may write user directories and shell startup files. Explicitly assess these against the reject gate; listing a pinned-adapter idea is not a waiver. No upstream installers, setup, hooks or tests may run in this phase.
- **Hardware and hosts:** distinguish local Claude Code, Codex and ChatGPT Work capabilities. Current guidance targets supported NVIDIA Vulkan hardware or Apple Silicon Metal; there is an explicit, slow CPU option with platform limits. Do not assume a cloud host exposes a suitable GPU or that all recent NVIDIA cards qualify. Record OS, drivers, VRAM, compiler warmup, storage, authoring runtimes and encoder requirements, with unsupported hosts marked accurately.
- **Rights and cost:** the preview licence permits current-version commercial work but restricts distribution of modified versions and rendering services for other people's submitted jobs without prior permission. Future versions may use different terms. Assess adapter packaging and any future hosted FrameCore product separately. Keep third-party asset rights and the optional Blender bridge's separate GPL licence distinct. Free software use does not establish free compute.
- **Incremental value:** compare against existing Blender, three.js, HyperFrames, Remotion and relevant Toolbox routes. Identify concrete jobs Vork improves, including total setup/render/repair effort, rather than adding another engine for category coverage.
- **Proposed evidence after owner approval:** an original product shot, a procedural motion/VFX scene and a supplied-footage composite, compared with the appropriate existing route. Declare dimensions, FPS, duration, quality settings, hardware, cold/warm timings, memory and visual defects. Author separate portrait/landscape compositions where both are required.

Deliver a **Vork Toolbox Qualification Report** with an explicit ADD proposal / NO ADD verdict, any blocking conditions, and whether the existing rules permit an adapter at all. No admission, wrapper, dependency installation or host update is authorized by this handover.

### B. Creative Studio: Crème de la Crème extraction

Evaluate useful techniques independently of Toolbox eligibility. These are research hypotheses, not verified gaps or completed adaptations.

| Candidate knowledge | Existing owner to inspect | Required evidence or proposed comparison |
| --- | --- | --- |
| Compact scene contracts, typed schemas and targeted help for agents | Pipeline Core and Motion Graphics | Compare current scene validation and repair; identify a specific ambiguity or missing contract |
| Preview-to-final iteration with explicit camera/material/light limits | Motion Graphics, Cinematography and Output Critic | Same original shot; show whether a decision or defect diagnosis improves |
| Integer frame identities, rational clocks and evaluated animation state | Motion Graphics and FrameCut | Inspect current timing first; propose fractional-FPS, seeking and shutter-sample boundary checks |
| Structured warnings for omitted effects and fresh completion metadata | Output Critic, Asset Manifest and delivery verification | Show how a successful process exit can still miss a requested effect; propose an incomplete-output/reused-output fixture |
| Separate GPU, cache, encoding and end-to-end timing | Tool Routing Cost and production QA | Distinguish cold setup from warm rendering; compare equivalent outputs rather than headline speed |
| Render passes, alpha/colour conventions and metadata for compositing | FrameCut and Motion Graphics | Map actual import support and conversion/fallback needs for PNG, EXR, ProRes, depth, motion and shadow passes |

For each retained technique, supply the exact source, current equivalent, proven gap or “already covered”, proposed original adaptation, inputs/outputs, limits, fallback and acceptance test. Review relevant implementation and tests before claiming a technique works. No automatic copying of source, shaders, assets or whole instructions; the custom licence is not a permissive-code licence. Useful abstract techniques may justify a knowledge-only outcome even if Toolbox rejects the engine.

### Receiving Claude's next action and provenance

Add one Vork row to the refreshed Audit Matrix, Knowledge Map, Toolbox Decision Matrix, Duplicate & Overlap Report and P0/P1/P2 roadmap. Start with eligibility, licence and environment feasibility, then inspect high-value techniques. Report PASS / FAIL / NOT RUN / UNKNOWN with evidence. Present the bounded proposal before any implementation.

- Change-ID: CW-20261110-01; Origin-Agent: chatgpt-work.
- Baseline-SHA: `10b9dccb4642909df40f59f07c5003aedc0a32a9`.
- Scope: update this existing handover only, by the owner's explicit follow-up.
- Shared-Package-Changed: no; Toolbox catalog and both installed plugins remain unchanged.
- ChatGPT-Work-Sync / Codex-Sync: not_run; no hosted release is required for this document.
- Vork installation, build, tests, rendering and host acceptance: NOT RUN.
- Verification of this documentation update: PASS, canonical Studio validator and full `bash scripts/check_all.sh` both exited 0; optional skipped checks remain unverified. These are Studio regression checks, not Vork runtime acceptance.
- Focused document checks: PASS, only this handover changed, both analysis tracks present, local links resolve and all twelve pinned Vork file links exist at the inspected SHA.
- Branch inventory: only `main` and `gh-pages`; no branch or PR created.

## 9. Owner addition: Ultra Skills motion-effects implementation, 2026-11-10

Source: [Claude Code Animation Prompts: The Full Set](https://www.ultra-skills.com/resources/claude-code-animation-prompts-six-effects?verified=true), Ultra Skills Editorial Team, displayed date 2026-11-05.
Owner request: add this material as an **implementation task for Motion Graphics**. This is an implementation track for the existing Studio owner, separate from the research queue, Toolbox qualification and the map-companion project.

### Scope and authorization

The current handover-maintenance session records this task only; it does not change or publish a runtime. For the receiving Claude development session, the owner has selected implementation of useful, original motion-effect recipes within the existing Motion Graphics workflow, subject to the source-access, rights and overlap checks below. The earlier read-only scope remains in force for sections 1–8; it must not silently downgrade this new task to an optional research link or authorize unrelated candidates.

Use existing project dependencies and local verification where available. New installations, paid services, external production APIs, uploads and deployment require their own explicit scope. Preserve the existing repository release rules for any later shared-package change. A source-access blocker must be reported specifically, not filled with invented effects.

### Source inspection and access boundary

Observed through the rendered public page on 2026-11-10:

- Despite the historical `six-effects` slug, the page now advertises **30 prompts**, numbered across four groups. Do not implement only six based on the URL.
- The preview covers spatial/3D effects (1–14), print/drawing effects (15–21), numeric/information effects (22–24), and interface/typographic effects (25–30).
- The listed stacks include Remotion, React Three Fiber, SVG, CSS and drawing libraries. These are source choices, not new mandatory dependencies for Studio.
- Its examples are portrait, 1080 × 1920 at 30 fps, lasting two or three seconds. Those are examples, not universal output defaults.
- The full prompt bodies and individual reference loops were behind an access-unlock control in this browser, including with the supplied query parameter. Their complete contents, dependency versions and reuse terms are **UNKNOWN**. No signup, subscription, unlock bypass or prompt execution was performed.
- The publisher explicitly does not establish unattended success on the reader's machine. Its example loops do not certify a complete Studio render.

Read the complete material through legitimate existing access or an owner-supplied copy before deriving prompt-specific requirements. Record the access date, actual inventory and any changes from this preview. Do not retrieve hidden gated content or treat `verified=true` as proof of access, licensing or successful testing. Link and credit the source; write original recipes and code, without reproducing its full prompts or bundling its media. Verify permission before any source-text/code/media reuse.

### Implementation work order for Claude

1. **Inventory every source effect.** For each observed prompt, record its identifier, purpose, visual mechanism, timing, inputs, output and source location. Map it to one of: already covered, extend existing, implement missing, or blocked with a concrete reason. Do not silently discard an effect or count an existing capability as a new implementation.
2. **Inspect current owners and reusable assets.** Start with [Motion Graphics](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/SKILL.md), its [brief index](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-prompt-library/brief-index.json), [film styles](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/film-style-library.md), [motion compendium](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-compendium.md), [toolkit routing](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-routing.md) and the existing [Remotion owner](../plugins/framecore-work-creative-studio/skills/remotion-video-production/SKILL.md). Initial source inspection already found product-turntable guidance, split-flap boards, counters, chart and typography recipes. Similar names are an overlap signal, not proof of identical behavior.
3. **Implement reusable mechanisms in the existing workflow.** Prefer extending current recipes/components over new skills or duplicate libraries. Expose editable copy, palette, fonts, assets, camera, timings, easing, duration, dimensions and seed. Define appropriate use, limitations and a simple fallback. Connect selection to brief intent; an effect is not a compulsory style for every film.
4. **Keep execution portable and deterministic.** Reuse the chosen project renderer. Do not reinstall Remotion or HyperFrames, force React Three Fiber on a non-React project, or introduce a second orchestrator, timeline or QA loop. Derive state from the frame clock, seed randomness and resolve fonts/assets before capture. Document any genuinely missing dependency instead of running an unpinned setup command.
5. **Preserve the geographic boundary.** A stylized city, globe or route effect may be a decorative motion recipe. Real location claims, verified A-to-B routing and aerial data belong to the separate [map-companion proposal](handover-map-motion-companion-2026-11-09.md). Do not present illustrative geometry as an actual road, entrance or building, or duplicate that companion inside Motion Graphics.
6. **Validate and connect the result.** Use original synthetic briefs and owned/permitted assets. Produce representative outputs for every newly implemented or materially changed mechanism, with exact copy and readable holds. Check first/last frames, boundaries, repeated and backward seeks, clipping, layering and full playback. Measure duration/FPS/dimensions with actual output evidence. If both aspect ratios are in scope, create separate portrait and landscape compositions. A muted source loop provides no sound-design evidence.
7. **Deliver a reviewable integration.** Return the complete source-effect mapping, changed paths, original implementation/recipes, render evidence, limitations and local/host results separately. Run the canonical validator and applicable repository checks. Record blocked effects and fresh-host checks as UNKNOWN or NOT_RUN; do not call the whole set complete from a catalog or static-source check.

### Provenance and completion boundary

- Change-ID: CW-20261110-02; Origin-Agent: chatgpt-work.
- Baseline-SHA: `f0a42c5004867bd9a8b2d343b98ef9603fd2cc65`; branch `main`.
- Current scope: update this existing handover only, preserving the earlier seven-source research queue and separate Lemo/map task. No Toolbox entry is proposed by this addition.
- Shared-Package-Changed: no. No version, manifest, hosted plugin or installation changed.
- Source evidence: public rendered preview observed; complete gated prompts/reference loops, licence qualification and implementation acceptance remain UNKNOWN / NOT_RUN.
- Documentation checks and publication/readback are reported by the saving task. They do not establish that any Ultra Skills effect has been implemented or rendered in Studio.

### Owner-supplied supporting archive and assessment, 2026-11-10

The owner supplied [11-free-video-effects.zip](source-packs/11-free-video-effects/11-free-video-effects.zip) and asked for the original archive and a separate assessment to be stored together. Read the [inventory, overlap assessment and implementation gaps](source-packs/11-free-video-effects/README.md) before planning. The ZIP contains one Markdown file with eleven short Remotion-oriented effect briefs, not executable components or reference renders. Its author, reuse terms and relationship to Ultra Skills' advertised full 30-prompt set are UNKNOWN; it does not establish access to that complete set.

Prioritize assessment of Frame Break, Headlines and a shared Orbit/Phone Screens component. Compare the remaining mechanisms with existing Studio recipes before adding anything. This is a supplementary source packet for the existing Motion Graphics task, not a Toolbox admission or map-plugin dependency. The archive, assessment and this handover are temporary and follow the cleanup instruction above. No effect from this archive has been implemented or rendered in this saving task.

## 10. Owner addition: Design Canvas, Crème de la Crème assessment, 2026-11-10

Source: [aievolutionpl/design-canvas](https://github.com/aievolutionpl/design-canvas), inspected at [`51a367d8d54b24f756ce6adcec1c8dea1ff98e73`](https://github.com/aievolutionpl/design-canvas/tree/51a367d8d54b24f756ce6adcec1c8dea1ff98e73). Studio comparison baseline: `1eea5ddca4d1f81cb31ffeadad97e7133278bf35`, package 1.174.1.

**Owner request:** Claude should analyze this source and decide whether it contains any specific Crème de la Crème worth extracting for Creative Studio. This is an assessment candidate, not an instruction to import the catalogue, copy the application or adopt its workflow. A conclusion that Studio already covers the useful material is valid. No Toolbox admission, installation, implementation or hosted-plugin update is authorized by this addition; section 9's implementation scope does not extend to it.

### Observed content and limits

- A static HTML/CSS/JavaScript design library for people and agents, with visual boards, style records, assets, a project-kit composer and local Node CLI. It is not an MCP server or a production video renderer.
- The inspected data contains 64 style/theme records, 147 font-family records, 718 icon records and 77 palettes. README's 56 styles and 698 icons are older counts. Font references are not bundled font files, and catalogue size does not establish design quality.
- [Style records](https://github.com/aievolutionpl/design-canvas/blob/51a367d8d54b24f756ce6adcec1c8dea1ff98e73/data/styles.json) include use cases, composition or principles, fonts, palettes, constraints and prompts; some also specify supporting/incompatible directions and CSS tokens. Coverage and field shapes differ across source groups. Trend images can be synthetic illustrations, not implemented components or verified trend predictions.
- [The comparison implementation](https://github.com/aievolutionpl/design-canvas/blob/51a367d8d54b24f756ce6adcec1c8dea1ff98e73/kit.js) reuses a simple layout while changing type, colours, borders and radius. It is not evidence of a complete composition for every style. [CLI export](https://github.com/aievolutionpl/design-canvas/blob/51a367d8d54b24f756ce6adcec1c8dea1ff98e73/tools/design-cli.mjs) does not carry every style-card field into its brief/provenance; inspect the full record when evaluating knowledge transfer.
- The asset catalogue's 23 animation entries are names without keyframes; CLI export rejects them. Liquid Glass techniques and animated SVG assets may merit narrow analysis, but none is established as a deterministic Studio motion component.
- No root licence covering the application's own code/text was found; GitHub licence metadata is null. Third-party assets have distinct rights and varying provenance coverage. [SOURCES.md](https://github.com/aievolutionpl/design-canvas/blob/51a367d8d54b24f756ce6adcec1c8dea1ff98e73/docs/SOURCES.md) and [the source ledger](https://github.com/aievolutionpl/design-canvas/blob/51a367d8d54b24f756ce6adcec1c8dea1ff98e73/data/source-ledger.json) do not establish a blanket licence for the whole repository. Permission to redistribute its own code, prompts and curated text is **UNKNOWN**; recheck before any copying.

### Questions for Claude's selective extraction

| Candidate | Compare against current Studio | Decision to return |
| --- | --- | --- |
| Structured style cards and compatibility relationships | [Graphic Design](../plugins/framecore-work-creative-studio/skills/static-graphic-design-creator/SKILL.md), its existing 200-code catalogue, poster-language guidance and [reference curation](../plugins/framecore-work-creative-studio/skills/reference-pack-curator/SKILL.md) | Does the structure improve selection or prevent incoherent combinations beyond existing guidance? |
| Same-content comparison and visual boards | Existing direction selection, brand-identity boards and output review | Is there a useful original way to help users compare genuinely different compositions, beyond token swaps? |
| Typography/palette curation and contextual examples | Current brand kit, font resources, craft rules and static/motion owners | Which exact pairs or decision rules add value without overriding approved brand choices or creating another broad catalogue? |
| Portable selected-design context with provenance | [Brand Kit](../plugins/brand-kit/README.md) and [Studio's DESIGN.md/token import-export](../plugins/framecore-work-creative-studio/skills/pipeline-core/assets/design-md/README.md) | Is a small mapping or evidence improvement warranted, or is this already covered? Do not assume compatible schemas or token names. |

Treat the Designer OS hierarchy, brand protection, typography and QA material as an overlap check first; Studio already has extensive equivalents. Evaluate selected assets separately from abstract knowledge, verify their original sources/rights and prefer original adaptation of useful mechanisms over copying instructions or generated previews. Do not build a parallel orchestrator, design owner or review loop.

Return a concise per-item map: exact pinned source, current equivalent, concrete gap or **already covered**, recommended disposition (**consider original adaptation / already covered / hold for rights or evidence / omit**), target owner, proposed inputs/outputs, limitations and a meaningful validation example. Explain whether any retained item would improve actual Studio work enough to justify the change. Present the recommendation before implementation; no minimum number of extracted ideas is required.

### Evidence and lifecycle

- Change-ID: CW-20261110-05; Origin-Agent: chatgpt-work; branch `main`.
- Source inspection: README, complete file tree, relevant data/docs, selected implementation and current Studio equivalents. This is not a complete code/security audit.
- The upstream [Workspace regression run](https://github.com/aievolutionpl/design-canvas/actions/runs/42631841863) reports success at the inspected commit; it is upstream CI evidence, not a local integration or production-output test.
- Upstream installation, script execution, browser acceptance, Studio adaptation and renders: **NOT_RUN**. Shared-Package-Changed: no.
- This section is part of the existing temporary handover and follows the roadmap's read, plan, then cleanup instruction. No additional source archive or permanent knowledge library is created by this task.

## 11. Owner addition: account-wide Claude token-efficiency assessment, 2026-11-10

**Owner scope:** assess whether a small shared working policy and supported configuration can reduce unnecessary usage across the owner's whole Claude environment: ordinary Claude chats on web, desktop and phone, Claude Code on desktop/local CLI, and any cloud, Remote Control or Cowork modes actually used. Creative Studio and this repository are only one workload and the temporary transfer location. Do not turn this into a Studio-only optimization, a new Studio runtime feature, or a claim that the account has one shared filesystem or universal plugin host.

Read the complete [owner-supplied research report](source-packs/claude-token-efficiency-2026-11-10/Claude_Token_Efficiency_Research_FrameCore_2026-11-10.md). It is preserved byte-for-byte in its original Polish, dated 2026-11-10; SHA-256: `6479af5450b82da5bf9fe997be24e9fe27e4a7b786332bc3ebd83868da725bb1`. The report is research input and a set of proposals, not an installed configuration or proof of savings on the owner's account. Its cited benchmarks, product versions, issue states and licences need targeted rechecking before reliance. This saving session verified only the native scope documentation linked below, not every report claim.

### Main question and host boundaries

Can the owner maintain a concise common policy, with host-specific implementation where necessary, instead of repeating large instructions and loading irrelevant tools? Identify exactly what can be account-wide, project-specific, machine-wide or session-only, what synchronizes, and what cannot be made global.

| Surface | Required assessment |
| --- | --- |
| Ordinary Claude Chat on web, desktop and phone | Account instructions, project instructions/knowledge, memory, skill availability and tool-access settings; verify which controls the actual account and clients expose. A local terminal wrapper is not a mobile-chat interceptor. |
| Claude Code local CLI and local Code in Desktop | User-level instructions/rules, project overrides, skill/plugin/hook/MCP scopes and measured context; distinguish the Desktop Chat and Code modes. |
| Account-synced skills | Verify supported clients, account login, enablement, precedence and one-way synchronization; syncing a skill does not synchronize arbitrary local hooks, binaries, databases or secrets. |
| Claude Code cloud | Verify the actual remote environment and project restrictions. Do not assume it reads the user's local home directory or has all desktop tools. |
| Phone Remote Control and Cowork, if used | Identify where the session executes, which machine must remain available and which tools/settings it inherits. Keep this separate from a self-contained mobile chat. |

Native documentation checked on 2026-11-10 provides starting points: [account versus project instructions](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features), [Claude Code user/project instruction scope](https://code.claude.com/docs/en/memory), [account-synced skills and their limits](https://code.claude.com/docs/en/skills), and [usage factors, project caching and official usage indicators](https://support.claude.com/en/articles/9797557-usage-limit-best-practices). Recheck the applicable sections against the owner's client versions. Personal account scope must not be confused with Team/Enterprise organization administration. Plan, organization role, enabled features, machines, configuration and actual usage breakdown remain **UNKNOWN** until observed.

### Receiving Claude's work order

1. **Inventory only accessible settings and evidence.** Establish the clients/modes, account and project boundaries, instruction layers, enabled skills/plugins, hooks, MCP tools and any background memory processes. Read bounded configuration/log excerpts; do not expose secrets, full private conversations or client data in this public repository. If a surface is inaccessible, provide an exact owner-side inspection step and mark it UNKNOWN rather than claiming an account audit.
2. **Diagnose actual waste before choosing tools.** Check duplicate instructions, always-loaded documents, repeated full-file reads, verbose tool output, redundant planning/review loops and repeated renders/tests. Preserve mandatory verification. Recommending narrower checks requires a separate reviewed change to the governing policy; this audit does not authorize silently skipping required checks.
3. **Propose a minimal common policy and a scope map.** Give the exact proposed account instruction text, project exceptions and supported Code user-level file/settings changes. Put substantial specialist material behind relevant on-demand skills or references. Avoid three copies of the same policy and a permanent master prompt containing the whole report. Where synchronization is unsupported, state the small manual or host-specific counterpart. The profile is personal workspace configuration, not a new default shipped to every Studio user.
4. **Protect CODE / CREATIVE / MIXED results.** Treat these as proposed routing profiles, not mandatory product modes. Reduce duplication and technical noise while retaining full briefs, exact copy, complete prompts, references, camera/light/motion/timing, sound and production QA. Code or Markdown implementing creative direction is not automatically CODE. No hidden model downgrade, crop replacing a required separate composition, or reduced output quality.
5. **Compare native features first, then optional candidates.** The report discusses Ponytail, ccusage, native LSP/Serena, Context Mode, QMD, RTK and Graphiti; Claude-Mem and Caveman are cautionary comparisons, not defaults. Assess each tool's real host scope, current source/version/licence, incremental benefit, conflicts and operating cost. Do not stack compressors or memory observers by default. Check the [historical Ponytail removal](handover-claude-code-2026-10-27.md#toolbox-103-owner-approved-removal-2026-10-28) and reported welcome interference: fresh assessment is allowed, automatic restoration is not. Nothing here admits a tool to Toolbox.
6. **Design a bounded comparison before a pilot.** Record the baseline, one change at a time, matched tasks/model/effort/cache conditions, completion quality, retries, time and additional model/indexing costs. Separate context size, input/output/cache tokens, API-price equivalents and official subscription usage. Capture other concurrent sessions as a confounder. Do not infer an account-wide savings percentage from compressed log bytes, or promise a percentage before measurement. Propose the smallest informative pilot and its budget first.
7. **Present a reviewable plan in Polish.** Return the host/setting/sync matrix; observed diagnosis versus UNKNOWNs; common policy and exact per-host proposals; optional tool decisions; privacy/licence/cost limits; rollback steps; and a step-by-step sequence explaining what the owner must do versus what the receiving session can actually do. Recommend the best supported option or no change. Configuration, installations, paid evaluations, account modifications and new service uploads require a subsequent explicit instruction.

### Additional report topics, independent of token savings

The supplied report also requests source identification and selective assessment of **Marketing Psychology (marketing-psychology)** and **Chief of Staff (chief-of-staff)**. Preserve this separate marketing/organization track. Their names reportedly came from screenshots of a Microtech.usa reel; those screenshots are not part of this attached report pack. Exact author, repository, version, licence and identity remain **UNKNOWN**. Do not substitute an arbitrary same-named skill.

After identifying actual instructions, compare marketing value with existing campaign/marketing/copy owners and organizational value with existing brief, decision, priority and handoff methods. Return selective knowledge adaptation, optional separate skill or rejection with evidence, required integrations and context overhead. These are not confirmed token-saving tools, Toolbox additions or authorization for messages, calendar changes or other external actions. They do not expand the nine-source Crème de la Crème queue before qualification.

### Owner supplement: methods and tools for the whole Claude workspace, 2026-11-10

**Owner request (CW-20261110-08):** add the supplied screenshot leads and their initial findings to this handover for possible introduction across the whole Claude workspace. Assess ordinary Chat on phone, desktop and web, Code on desktop/local CLI, and other actually used modes from the host matrix above. The target is a practical personal workspace plan spanning coding, research, planning and creative production. Availability when Studio is active does not prove availability elsewhere. This is a planning addition, not an instruction to install all candidates or change the account during handover intake.

| Source | Verified starting point | Receiving Claude's decision |
| --- | --- | --- |
| [Grill Me and Grilling, Matt Pocock](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity) | At the inspected pin, `grill-me` is a manual entry point that invokes `grilling`. The latter explores decisions and their dependencies through question rounds and calls for delegated fact-finding. | Compare an optional user-invoked plan review with selective adaptation of its questioning method. Resolve the dependency; compare with existing planning/brief tools. Propose a bounded trigger, stopping condition and delegation budget. Do not make repeated interviews or subagents mandatory for ordinary requests. This is not itself a demonstrated token-saving tool. |
| [Agent Browser, Vercel](https://github.com/vercel-labs/agent-browser/tree/f423bb090ccdcadd0de587dd77eed3430d93a306) | The README describes a browser automation CLI with compact accessibility snapshots and element references. Its discovery skill loads instructions from the installed CLI; the skill alone is not the browser runtime. | Compare actual available browser tools on matched research and interface-checking tasks before adding another one. Assess supported hosts, browser/session ownership, dependencies, exact-version installation, permissions, credentials, network traffic and removal. A local CLI is not automatically available in ordinary mobile Chat; distinguish remote control from local phone execution. |
| [Find Skills, Vercel](https://github.com/vercel-labs/skills/blob/26dc8e4755a11fea22ed788256c3db50001b013d/skills/find-skills/SKILL.md) | Studio already has a [selective adaptation](../plugins/framecore-work-creative-studio/integrations/skill-finder/README.md) and [discovery route](../plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/skill-finder.md). That is not proof of a separately installed global skill. | Reuse the Studio route where active; assess whether other workspace tasks need a single user-level discovery entry point. Avoid duplicate registrations and repeated catalog searches. Verify candidates by their actual source and behavior, not install counts alone. Discovery must not silently become installation. |
| HyperFrames | Studio already has the [Motion Graphics owner](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/SKILL.md); the screenshots do not establish a new integration or runtime readiness. | Inventory existing skills and executable versions on each host, including work outside Studio. Propose reuse and clear invocation/routing if there is a real gap. Do not add a second render pipeline merely to reproduce an existing capability. |

Read-only source anchors checked on 2026-11-10: `mattpocock/skills` at `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` (both skill files); `vercel-labs/agent-browser` at `f423bb090ccdcadd0de587dd77eed3430d93a306` (README); `vercel-labs/skills` at `26dc8e4755a11fea22ed788256c3db50001b013d` (`find-skills/SKILL.md`). These are source pins, not installation qualifications or a complete security/licence audit. At Toolbox main `adc8094f8e087889e4337c99dd0d267ae1b11a51`, the marketplace, README, active catalog skill and review-path inventory contained no Agent Browser or Grill Me entry. Installed state on the owner's machines remains **UNKNOWN**. Any proposed Toolbox admission must separately follow Toolbox's current eligibility, reject, complete-upstream and demonstrated-improvement rules; a personal workspace proposal does not bypass them.

**Cost/quality reference:** [Your Old Prompts Are Making Claude Worse, Lance Martin, Anthropic, AI Engineer](https://ai.engineer/talks/ys6YQ2yfBpM-your-old-prompts-are-making-claude-worse), with [the original video](https://www.youtube.com/watch?v=ys6YQ2yfBpM) (listed duration 1:04:02). The organizer's published account describes a 90% cost reduction on a particular support-ticket benchmark after jointly changing model, reasoning effort and prompt. It is not evidence that one prompt saves 90% of this owner's subscription allowance. Relevant methods are inherited-instruction audits, cache reuse where controllable, quality-preserving model/effort comparisons, held-out evaluations and bounded optimization. The initial review read the organizer's account and source links, not the complete audiovisual recording; Claude should verify the relevant original chapters before relying on details. Screenshot rankings and promotional wording are leads, not independently reproduced evidence.

Extend the workspace plan with these deliverables:

1. A decision for each source: reuse existing capability, introduce an optional tool, adapt selected knowledge, defer, or reject, with the concrete benefit and evidence gaps. Keep these workspace decisions separate from the nine-source Studio Crème de la Crème queue and from Toolbox admission.
2. An exact per-host proposal: account instructions, project exceptions, user-level Code configuration, supported skill synchronization, on-demand entry points and fallback when the runtime is unavailable. Global availability must not mean loading every workflow into every conversation. Identify settings the receiving Claude can actually change and steps that require the owner.
3. A minimal staged implementation plan in Polish, with exact proposed files/settings, source versions, dependencies, cost, rollback, success criteria and a bounded pilot. Preserve creative output quality and existing authorization. Do not change model/effort silently, import account data into this public repo, or assume API cache controls are exposed in consumer Chat.
4. Compare completed-task quality, retries, latency and measured usage against the current workspace baseline. Separate API-price savings, token counts and subscription indicators; include the optimization process's own cost. Do not launch unattended self-improvement loops or paid benchmarks from a promotional screenshot.

The owner has authorized adding this implementation-oriented assessment to the temporary handover. Actual configuration changes, installation, paid evaluation and deployment still require the subsequent explicit instruction described above. Original report bytes, the separate map/Lemo tasks and the withdrawn offline-app decision remain unchanged. This supplement follows the same intake, step-by-step presentation and cleanup lifecycle as the rest of section 11.

### Authorization, evidence and lifecycle

This addition authorizes preserving the report and preparing analysis/proposals only. No account configuration, global skill, hook, MCP server, model setting, plugin or repository runtime has been changed. No account logs or usage measurements were accessed; no saving was measured. The withdrawn standalone offline-app idea remains excluded, and the CBR Studio video analysis is not added.

Change-ID: CW-20261110-07; Origin-Agent: chatgpt-work; baseline: `2ec907ebed86202e3306cbb3e045101c1931a67b`; Shared-Package-Changed: no. This section and the complete supporting report follow the existing temporary-handover intake, plan and cleanup policy. After intake, keep any personal configuration proposal in an owner-approved private destination, not as a public dump of the account. Do not run the audit instructions embedded in the report as part of this documentation-saving task.

## 12. Owner addition: Cinecode, Toolbox and Crème de la Crème, 2026-11-10

**Owner request:** add [sarpstar/cinecode](https://github.com/sarpstar/cinecode) to both tracks: qualification as a general film/motion-production tool for Toolbox, and selective extraction of useful techniques for Creative Studio. These are independent decisions. This is the ninth source in the current Crème de la Crème research queue. It is not a map-specific dependency, a replacement for the existing render owners, or a revival of the withdrawn standalone offline-app proposal.

### Source and initial evidence

Inspected upstream `main`: [`67f9807112b97ae253d4a5f0eccaccc46c3b2633`](https://github.com/sarpstar/cinecode/tree/67f9807112b97ae253d4a5f0eccaccc46c3b2633), checked on 2026-11-10. The GitHub releases endpoint returned no published releases. The root [LICENSE](https://github.com/sarpstar/cinecode/blob/67f9807112b97ae253d4a5f0eccaccc46c3b2633/LICENSE) is MIT, copyright Sarp Yıldız. This covers the repository code/instructions, not every downloaded font, recording, image or other asset.

The inspected tree has an installable root [SKILL.md](https://github.com/sarpstar/cinecode/blob/67f9807112b97ae253d4a5f0eccaccc46c3b2633/SKILL.md), references, scripts, starters and tests, with no Claude plugin manifest found. The [English README](https://github.com/sarpstar/cinecode/blob/67f9807112b97ae253d4a5f0eccaccc46c3b2633/README.en.md) describes Quick and Film workflows for coded films, ads, explainers, music videos and footage edits. Its stated requirements are Node.js 22+, Python 3.9+, FFmpeg and Chrome/Chromium/Edge, with GPU availability affecting the render path. Source guidance for a host is not proof of a successful installation or finished film there.

At Toolbox main `adc8094f8e087889e4337c99dd0d267ae1b11a51`, no Cinecode entry was found in the marketplace, README, active catalog skill, apps index or complete path inventory. Installed state in any owner environment is **UNKNOWN**.

### A. Toolbox qualification

Assess the complete upstream under Toolbox's current rules and return a separate **ADD / CONDITIONAL / NO ADD** recommendation with evidence. Check root-skill discovery and packaging, dependencies and optional voice/API services, all installs/updates/downloads, hooks and their scope, network/data flows, persistent files, licence provenance, uninstall and actual benefit over the tools already available. Preserve required full-upstream treatment where applicable; do not create a reduced wrapper to evade a reject gate.

**Initial gate finding: NO ADD AS-IS at this pin under the current reject rules.** The README's install clones an unpinned branch into the user's skill directory, and the skill's update route uses an unpinned `git pull`. In addition, the skill declares UserPromptSubmit, Stop and PreToolUse hooks; [scripts/hook.cjs](https://github.com/sarpstar/cinecode/blob/67f9807112b97ae253d4a5f0eccaccc46c3b2633/scripts/hook.cjs) contains an automatic Python-location cache write under `~/.cinecode/python.txt`. The broader toolkit documents keys, formats, taste history and caches under `~/.cinecode/`. The runner's write is a source finding; actual hook registration, activation and effects in each host were not tested. Apply the current reject gate to these findings before proposing admission, and do not assume that pinning the outer marketplace alone resolves upstream installation/update behavior. Recheck a newer upstream explicitly if one exists; any remaining hard rejection must remain visible, not be relabelled as a qualified tool.

A useful production test proposal should compare one bounded film task with the existing Studio route: setup burden, controllability, visual/audio quality, revision effort, render reliability and total measured usage. Distinguish the repository licence from optional providers' costs and asset rights. Do not execute that pilot or an installer during the current source audit. A failed Toolbox gate does not prevent the independent knowledge review below.

### B. Crème de la Crème extraction

Study specific techniques and map each to an existing Studio owner, its current equivalent, a concrete missing behavior, a small proposed change and a test. The following are inspection targets, not claims of demonstrated improvement:

| Technique to inspect | Exact source starting points | Comparison and proposed proof |
| --- | --- | --- |
| Deterministic frames and safe render resumption | `references/engine.md`, `scripts/capture.mjs`, `scripts/make.py` | Compare the READY/renderFrame/captureFrame contract, seeded time and asset-readiness rules with Motion Graphics, HyperFrames and Remotion. Propose repeated/out-of-order frame equality and stale-asset invalidation checks; do not add another engine merely for equivalent behavior. |
| Preview before expensive production | `SKILL.md`, `references/quick-mode.md`, `references/film-mode.md`, `templates/STATE.md` | Compare a compact production card, representative stills, style frame, animatic and draft with existing brief/storyboard/review owners. Reuse approved intent and measure whether earlier review reduces revisions. |
| Changes confined to affected shots | `references/context-protocol.md`, `scripts/brief.py`, `scripts/snapshot.py`, `scripts/handoff.py` | Compare verbatim owner notes, per-shot actions, preserved accepted shots, targeted rerenders and resumable state with current handoff and FrameCut contracts. Verify unchanged-shot identity and complete recovery after a fresh session. |
| Picture, sound and output QA | `references/engine.md`, `references/sound.md`, `scripts/qc.py`, `scripts/scene_check.py`, `scripts/words_check.py`, `scripts/master_audio.py` | Inspect checks for motion, seams/flashes, loops, exact words, readability and audio, then identify genuine gaps. Keep existing Output Critic and audio ownership. Measurements alone do not certify sound design or listening quality. |
| Visual direction and reusable craft | `references/camera-moves.md`, `references/typography.md`, `references/writing.md`, `references/motion-design.md`, `styles/index.json` | Compare camera/type/story/beat techniques with current libraries and trace original provenance before adaptation. Do not copy defaults, examples, third-party artwork or an entire parallel workflow. |
| Bounded context and diagnostic output | `references/context-protocol.md`, `SKILL.md`, `scripts/usage.py`, `scripts/hook.cjs`, `scripts/guard.py` | Compare section-level reads, compact status, contact sheets and file-based continuation with section 11's workspace study. Review delegation, hooks, model choices and fixed thresholds separately; measure end-to-end usage and preserved quality instead of adopting upstream savings claims or forced session changes. |

**Lemo overlap must be checked explicitly.** The inspected `styles/index.json` contains 58 entries: 51 use the Lemo source and seven identify Cinecode as their source. It pins Lemo to `d33bdea74eeecde3922b0fbad227f0d3dc7afe75` and points to `styles/LICENSE-lemo-opuscar`. Studio already has its separately adapted [film-style library](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/film-style-library.md). Compare actual recipes, source revisions and additions; do not treat all 58 as new Studio knowledge. Preserve Lemo's [independent general Toolbox task](handover-map-motion-companion-2026-11-09.md) and do not infer that Cinecode installs or integrates Lemo's complete engine. Its README also credits other sources, so trace those before claiming an original technique.

### Deliverables, limits and lifecycle

Return two clearly labelled outcomes: the Toolbox qualification and the Studio knowledge map, each with blockers, source pins, overlap, proposed tests and the smallest justified next step. Preserve Studio's existing ownership, startup, language behavior, separate 9:16/16:9 compositions when both are requested, and approval boundaries. Cite actual evidence; labels and upstream demonstrations do not prove FrameCore runtime readiness.

Read in this saving session: repository metadata/tree, release list, licence, README installation/requirements/provenance sections, root skill, engine and context references, hook runner and style-index metadata; plus current Toolbox rules and catalog surfaces. This was an initial source inspection, not a full code/security review. Installation, upstream scripts/hooks/tests, media generation, finished-render inspection and account/token measurements are **NOT_RUN**. No upstream assets or code were copied into either plugin or catalog.

Change-ID: CW-20261110-09; Origin-Agent: chatgpt-work; baseline: `2942af902909b83441fc4c428d9debd532500c5a`; Shared-Package-Changed: no. This adds two assessment tasks to the existing temporary handover only. Follow its intake, step-by-step owner plan and cleanup policy; it does not authorize installation, plugin implementation, paid operations or deployment in this saving session.

## 13. Owner addition: Higgsfield reference-guided scenes in code, 2026-11-10

**Owner request and status: PROPOSAL.** Assess a Motion Graphics extension in which approved visual references or graphic assets establish the intended scene before a coding model builds its editable scene, camera, lighting and animation. The owner wants this method to remain usable with suitable current and future models, including the article's Fable 5.2 label, Claude Opus 5.5 and GPT Astra. This is a workflow case study, separate from the nine-repository research queue and Toolbox admissions. It is one option for Claude to compare and recommend, not a prescribed architecture or authorization to implement it now.

### Primary source and factual boundary

Source: [Higgsfield, Fable 5.2 Rendered a Bombay Bazaar at Sunset, Entirely in Code](https://higgsfield.ai/@higgsfield.studio/blogs/a-bombay-bazaar-at-sunset-rendered-entirely-in-code). Read the complete article text in the browser on 2026-11-10; the page displays Nov 9. The link omits the owner's tracking query.

The article reports a six-shot, 21.5-second film. A Seedream 5.0 Pro image guided light, composition and form; its pixels were excluded from the final render. The scene and sound were built in code. The described renderer is a custom browser WebGPU path tracer; the article does not identify Three.js. Treat Three.js as a candidate implementation, not a verified dependency of this film. Image-to-code here means reconstruction guided by a visual target, not demonstrated automatic conversion of an image into accurate 3D geometry.

Reported techniques include a clean master with stable pixel grids/seeds for constrained pan/tilt shots, a separately rendered moving-camera shot with parallax, and rerendering only changed shots. Reported limits include mannequin-like people, absent object motion blur and limited camera translation. Steps 3–6 were reconstructed by the publisher from model reports. These are source claims, not an independently reproduced pipeline or inspected source project.

### Proposed use in Motion Graphics

Investigate whether this approach improves controllable product films, environment shots, stylized cinematic scenes and spatial explainers: once the visual direction is approved, the user should be able to revise a camera move, light, object or timing while preserving accepted parts. Measure that benefit against the current route; do not promise photorealism, lower cost or universal suitability in advance.

Ask Claude to compare two clearly labelled asset policies:

- **Reference-only reconstruction:** generated or supplied images guide the look and spatial design; the final picture is rendered from authored geometry, materials and lighting. Preserve the distinction between visual resemblance and verified dimensional/physical accuracy.
- **Hybrid scene:** permitted supplied/generated images, textures, cutouts or models become declared render inputs where this better serves the brief. This is a FrameCore option to assess, not a claim about the linked film. Record each asset's role, rights, revision and hash; do not describe an output containing those assets as entirely procedurally authored.

Propose a bounded sequence within existing Studio owners:

1. Reuse the brief, exact copy, approved direction, delivery formats and existing storyboard. Define what must stay stable across revisions and which parts of the scene actually need depth or camera translation.
2. Establish a small approved reference/asset set and a scene specification: object identities, scale, spatial relationships, material/light targets, camera/lens, shot timing and allowed changes. Separate visual targets from production assets in the existing manifest.
3. Choose the simplest suitable available render route and build only a proposed test frame or low-cost proxy after the owner authorizes that pilot. Review composition, light, object identity and geometry before committing to detailed animation or a long render.
4. Plan static and animated elements separately, with frame-derived state, asset readiness, recorded seeds and explicit camera limits. Assess the master-based method only for compatible shots; do not treat a crop or pan over a flat master as proof of real translation, parallax or newly revealed geometry.
5. Reuse current motion/audio timing, output review and revision contracts. A requested change should rerender only affected shots while preserving the accepted versions, source files and reproducible settings.
6. Return the editable scene/project, manifest, render settings, measured checks and actually produced outputs through the existing Motion Graphics/FrameCut handoff. When both 9:16 and 16:9 are needed, design and review their compositions separately rather than automatically cropping one into the other.

### Model and framework portability

Keep three responsibilities distinct: the model that generates a visual reference, the model/agent that plans and writes scene code, and the software/hardware that renders it. A coding model name is not a render engine or proof that its host has a GPU. The names above are owner/article examples, not a frozen allowlist or verified API identifiers. Resolve the exact available model/version and host capabilities at execution time; accommodate future models through the same inputs, outputs and checks, without promising that every future model will pass.

Compare with the active [Motion Graphics owner](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/SKILL.md), its [code-based workflow](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/code-based-motion-graphics.md), [generated asset guidance](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/generated-motion-assets.md), and existing HyperFrames/Remotion and reviewed 3D routes. Evaluate Three.js and WebGPU rendering options against those contracts. A custom path tracer is an option requiring a demonstrated gap and justified maintenance cost, not a mandatory new engine. Do not duplicate an existing integration, introduce a second orchestrator or import the article's no-stock/no-3D-package constraints as global Studio rules.

**Existing overlap and constraint:** Studio already plans generated cutouts from storyboards, checks them and animates them in code. Its generated-asset guidance also explicitly rejects drawing realistic objects/hands in code, based on a recorded quality failure. Therefore the reference-only reconstruction proposal needs an explicitly bounded comparison with that established asset route. Identify whether an approved exception would be justified by inspected results; do not silently remove the guard or treat this showcase as overriding it. The possible gap is controlled spatial reconstruction and render strategy, not the general idea of generating graphics before animation.

Use capability checks for image inspection, code execution, file persistence, browser/GPU support, memory limits, render/export tools and real media review. If a host lacks execution or GPU access, describe the attainable planning/handoff result and a suitable already-approved render route. Higgsfield MCP, Seedream, rented GPU compute and any other provider remain optional choices with separate authorization and cost limits. This proposal does not reopen the withdrawn offline standalone application.

### Claude's deliverable and proposed proof

Return a concise gap analysis and recommended implementation plan in Polish, step by step, with affected existing owners/files, alternative routes, inputs/outputs, dependencies, costs, fallback and acceptance criteria. Compare the overlap with Vork, Cinecode and current Studio craft before proposing additional infrastructure. If existing behavior already covers the method, recommend only the specific missing guidance or no change.

Design, but do not execute yet, one bounded pilot using an owner-approved reference and a short scene with one moving subject and one camera move. Compare the candidate with the existing route using the same brief and acceptance criteria. Check reference fidelity, identity/scale, real depth/parallax where requested, temporal stability, motion blur where required, readable exact text, load/VRAM/render budget, reproducibility and revision isolation. Record actual wall time, model usage and compute cost separately; nominal model capability and the linked showcase do not substitute for the test. Sound, if requested, stays with existing audio owners and requires listening as well as measurements. Define a stop condition before adding more detail or extending to a full film.

**Evidence and lifecycle:** article text read: OBSERVED_SOURCE; proposed Studio benefit: untested. Complete video playback/audio review, source-code inspection, image generation, model comparison, GPU benchmark and reproduction: NOT_RUN. No prompts, media, code or assets from the article were imported. Preserve its source link and this factual boundary through Claude's intake, then apply the existing temporary-handover planning and cleanup policy. Change-ID: CW-20261110-10; Origin-Agent: chatgpt-work; baseline: `ee0bae6ae2d6d0db0cff03396a67f18267794e79`; Shared-Package-Changed: no.

## 14. Owner addition: Generative Icons and useAnimations, 2026-11-11

**Status: optional asset-source assessment and comparison proposal.** The owner supplied results from two separate ChatGPT Work tests, then questioned whether ready-made animated icons add value when Opus 5.5 with Studio can already draw and animate elements using available engines. The follow-up `dodaj` authorizes recording the findings and that unresolved product question here. It does not authorize integration, installation, a new benchmark, Toolbox admission or a new rendering engine. These two asset candidates are separate from the nine-source Crème de la Crème queue above; technical usability alone does not establish a production advantage.

**Owner clarification, 2026-11-11 (CW-20261111-02): Claude decides the assessment outcome.** Independently determine whether either library adds value and where it belongs: optional assets, Studio knowledge, a qualified Toolbox proposal, or no adoption. No ADD/NO ADD outcome, preferred library or knowledge-only route is prescribed. Treat the hypotheses and comparison outline below as options to evaluate, not a required development path. Choose the assessment method, explain the decision and evidence limits in Polish, and present any proposed work step by step. This delegates the assessment decision; implementation, installation and new execution still follow the existing authorization boundaries.

### Evidence and source pins

The saving session read both complete reports: `FCW_Generative_Icons_Test_Report_PL.md` and `useAnimations_raport_2026-11-11.md`, dated 2026-11-11, and the owner's pasted summaries. The reports are external-session evidence, not tests rerun here. Preserve their positive results as **PASS_REPORTED**, failures as **FAIL_REPORTED**, and unexecuted cases as **NOT_RUN**. Their original media, logs and ZIPs remain in the owner's test artifacts; they are not imported by this documentation update. A receiving session without access must obtain the relevant evidence before claiming independent verification. The summary below is sufficient for initial assessment, not a substitute for reproducing a result.

| Candidate | Reported source and version | Separate boundaries |
| --- | --- | --- |
| [LottieFiles Generative Icons](https://github.com/LottieFiles/generative-icons) | [Source commit](https://github.com/LottieFiles/generative-icons/tree/1cc0ad00af2cad7ca109cbafa621a7693f0654f7) `1cc0ad00af2cad7ca109cbafa621a7693f0654f7`; CLI/Linux x64 binary 0.1.2 | The CLI actually consumed public catalog 0.1.1, source commit `29a6f9933a8b663a9b5165a7cb0f90fcb5e27679`. Do not merge CLI and asset versions into one pin. |
| [useAnimations](https://useanimations.com/lottie-icons) / [React repository](https://github.com/useAnimations/react-useanimations) | [Source commit](https://github.com/useAnimations/react-useanimations/tree/f7af6f53f6f1a97486ad95756b281a34e9f7c670) `f7af6f53f6f1a97486ad95756b281a34e9f7c670`; react-useanimations 3.1.1; lottie-web 5.13.0 | The public JSON, repository JSON and npm assets matched structurally for the six tested icons. Raw JSON playback and the React component use different player interfaces. |

Both reports identify MIT for the corresponding code and icon artwork. Retain copyright and permission notices in redistributed copies/substantial portions, preserve third-party/font notices and record per-asset provenance. Recheck the selected revision and intended distribution before reuse; MIT is not a blanket licence for unrelated assets or services. No animation files, dependencies or upstream code are bundled here.

### Generative Icons: reported findings

Tested icons: `arrow-right`, `current-location`, `cart`, `check`, `notification-badge`, `partly-cloudy`.

| Check | Reported result and limit |
| --- | --- |
| CLI and local stdio MCP, without login | PASS_REPORTED: six English searches returned identical CLI/MCP lists; 18/18 files for six icons matched byte-for-byte. MCP search/add and invalid-argument/path-boundary responses were exercised. Listing nine tools does not mean all nine were tested. |
| Variants and local control | PASS_REPORTED: 36 samples across six icons, Light/Strong motion and three styles; color, scale, alpha, loop and frame control worked locally. The arrow's Outline/Duotone samples coincide; 36 samples are not 36 distinct appearances. |
| Offline operation | PASS_REPORTED: local WASM/assets/fonts rendered with network calls blocked; a new CLI project could search/add from a prepared cache. This does not establish offline creation/export of new icons. |
| Repeatability | PASS_REPORTED: 9/9 selected PNG frames matched after reversed seek order; 3/3 matched in a new process. Not a second complete MP4 encode, whole-library audit or cross-platform determinism guarantee. |
| Film | PASS_REPORTED: 12 seconds, 1080 x 1920, 60 fps, 720 frames; 88.27 seconds render/encode; 542,497 bytes. Pipeline: dotLottie Web 0.80.0 WASM -> Node with @napi-rs/canvas 0.1.100 -> FFmpeg 7.1.5. H.264/yuv420p MP4 has no alpha; alpha was checked in assets/PNG. |
| Restrictions | Three Polish queries returned no matches; try English semantic queries and inspect relevance. Chromium startup was blocked, so browser playback/HTML and browser-renderer comparison are NOT_RUN. React, iOS/Android, Remotion/HyperFrames integration and full-library validation are NOT_RUN. |

`draft` and `build` still require sign-in to remote Creator MCP according to the report; neither was run. Reported zero paid calls applies to the tested existing-asset/local-tool path, not all features. A temporary local MCP process was closed after testing; no permanent account/global plugin configuration was installed. CLI/MCP expose the same tested assets; their convenience must justify any additional maintained wrapper.

### useAnimations: reported findings

Tested JSON IDs: `arrow-right`, `map-pin`, `shopping-cart`, `checkmark`, `notification`, `sun`.

| Check | Reported result and limit |
| --- | --- |
| Download and control | PASS_REPORTED: six JSON files retrieved without an account/key; raw frame selection, colors, scale and timeline loop/hold behavior worked. No external fonts, images, URLs or expressions were found in these six files; do not generalize to all 300 catalog entries. |
| React interactions | PASS_REPORTED: six interaction modes and a controlled external RAF clock; component 3.1.1 has no public arbitrary-frame/seek API. Internal methods are not a supported integration contract. |
| Offline operation | PASS_REPORTED: raw JSON, React previews and final rendering worked from local resources with HTTP(S) blocked. |
| Pixel repeatability | FAIL_REPORTED for strict equality: 23/24 raw-icon comparisons and 6/15 whole-composition frames matched. The raw failure changed three pixels by at most 1/255; the composition's largest changed area was 490 of 2,073,600 pixels, with a maximum channel difference of 143. Do not describe every difference as at most 1/255 or claim an established root cause. |
| Alpha overlay | FAIL_REPORTED for a universally transparent overlay: the notification icon uses opaque white strokes for a visual cutout. Matching a fixed background can hide them, but does not create genuine alpha for arbitrary backgrounds. |
| Film and portability | PASS_REPORTED: raw JSON + lottie-web produced 12 seconds, 1080 x 1920, 60 fps, 720 frames, about 556 kB, in 73.1 seconds. React did not produce this final MP4. Remotion/HyperFrames and other systems/players remain NOT_RUN. |

The useAnimations report recommends raw JSON with explicit frame selection over the interactive React wrapper for video; Claude should assess that recommendation against the intended route. A controlled RAF history is useful test evidence, but backward/out-of-order film rendering needs a supported seek contract or reconstruction of state. No new adapter is authorized by this observation.

### Product question and existing overlap

**The missing evidence is benefit over Studio-authored motion.** Neither test compared the same brief against Opus 5.5 using the current Studio route, measured model-token savings or proved fewer revisions. The two reported render times used different compositions and environments; they are not a speed ranking of the libraries.

Studio already documents [Lottie import and playback](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-runtime-cards.md#lottie-import-and-playback) and [motion-tool routing](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-routing.md). Preserve the existing master frame clock and owners. Under [companion routing](../plugins/framecore-work-creative-studio/skills/pipeline-core/references/companion-routing.md), external asset sourcing belongs to Open Assets when qualified; asset provenance belongs to the [Asset Manifest](../plugins/framecore-work-creative-studio/skills/asset-manifest/SKILL.md). Consider these existing boundaries before proposing a new catalog, provider or Toolbox tool. No entry in any of those surfaces is added here.

Hypotheses and open questions for Claude's independent assessment:

- Simple arrows, pulses, underlines, counters and bespoke brand motion may be faster and better authored directly in the current engine.
- A matching family of many icons may reduce geometry/motion-design work and improve consistency. Search, licensing, recoloring, timing, QA and dependency costs still count.
- Generative Icons passed the reported local control and sampled repeatability checks; useAnimations has the recorded alpha/repeatability limitations. Different environments prevent a direct ranking. Claude chooses whether to investigate either library further and in what order.
- For each library, independently decide whether assets alone, CLI/MCP tooling, transferable knowledge or no adoption best fits the current architecture and Toolbox qualification rules. Successful CLI/MCP startup is one piece of evidence, not an automatic admission or rejection.
- Potential Crème de la Crème topics include coherent motion families, semantic asset selection, style/color controls, explicit time mapping, alpha diagnostics and bounded reproducibility checks. Claude decides whether any of these add knowledge beyond existing craft; a useful asset collection need not require a skill.

### Claude's comparison plan and deliverable

First return the independently chosen assessment and any proposed next steps in Polish. Claude decides whether a bounded A/B comparison is needed to resolve remaining uncertainty. The following is one possible design, which Claude may adapt or replace; execute new tests only under an explicit later test authorization:

1. Use the same short-film brief, exact copy, palette, format, timeline and acceptance criteria. Include a simple procedural accent and a coherent group of several icons so neither route is favored solely by task selection.
2. A: current Studio + its available engine, with model-authored geometry/motion. B: the same Studio/model/host using a permitted ready-made icon family. Record model/version/effort, renderer and any unavoidable dependency differences. Keep the method usable with future models without assuming equal capability.
3. Record preparation/search/adaptation time, model usage where actually exposed, render time, human corrections, visual quality, family consistency, brand fit, editability, alpha, timing and repeated/out-of-order frames. Separate cold setup from reuse. Token or cost data unavailable to the host remain Unknown; do not estimate them from elapsed time.
4. Compare at equivalent accepted quality and one declared revision budget. Apply the same requested change to each result. Report remaining failures and evidence limits, including cross-host tests not run. If both portrait and landscape are needed, compose them separately.
5. Recommend one of: no change; optional asset-source guidance through existing ownership; or a narrowly justified tool/dependency proposal. Define success/stop criteria before testing. If finding and adapting an asset saves no meaningful effort or harms quality, keep the existing Studio route.

Return source pins, reported-vs-reproduced evidence, overlap, and separate decisions for asset sourcing, Studio knowledge and Toolbox tooling. If further tests are needed, state why and propose their scope; otherwise explain why the available evidence is sufficient for the decision. Do not claim measured production gains without comparative evidence. There is no requirement to re-audit every LottieFiles service or install both libraries merely to finish this assessment.

**Lifecycle and provenance:** follow the existing temporary-handover intake, owner-facing plan and cleanup policy. Preserve relevant decisions and evidence limits before cleanup. The offline standalone-app idea remains withdrawn. Change-ID: CW-20261111-01; Origin-Agent: chatgpt-work; baseline: `46f37c15bfd1c7622f8f23e534d8b07eb0e0e848`; Shared-Package-Changed: no. This saving session changes documentation only; new media tests, performance comparison, integration and hosted-plugin changes are NOT_RUN.
