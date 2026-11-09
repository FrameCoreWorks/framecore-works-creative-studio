# FrameCore Works: Crème de la Crème
## Screened handover for Claude Opus 5.5

Date: 2026-11-09  
Origin: chatgpt-work  
Change-ID: CW-20261109-01  
Status: source-screened research brief; implementation is not authorized.

Projects:
- [Creative Studio](https://github.com/FrameCoreWorks/framecore-works-creative-studio)
- [Toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox)

## 1. Owner intent and authorization

Improve Creative Studio's production judgment and output quality by studying useful external repositories, extracting specific techniques, comparing them with the current product, and adapting only demonstrated improvements into existing owners. Adding more plugins is not the goal.

The owner supplied twelve repositories and explicitly asked for duplicates and unsuitable candidates to be removed before this handover. The active queue below contains **six sources**, not twelve new integrations. Cinematic Director, Drama Skills and Claude AI Music Skills are all retained for targeted knowledge extraction. Functional overlap rules out unnecessary parallel workflows, but does not by itself disqualify a useful source of techniques. The six exclusions are retained only as a decision record, so the same work is not proposed again.

This task authorizes one new handover document in Creative Studio. It does not authorize changes to existing files, either shared package, Toolbox, versions, manifests, dependencies or hosted plugins. Provenance is recorded here instead of modifying the existing development ledger, in accordance with that one-file scope.

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

## 4. Active research queue: six narrowly scoped sources

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
3. Confirm the six retained pins, licences and any newer releases. A newer version starts a new review; do not silently substitute it.
4. Build a bounded source audit for these six only. Read relevant code as untrusted data. Do not run upstream installers, scripts, hooks, tests or model evaluations during this audit.
5. For each technique, record its exact source, existing equivalent, concrete missing behavior (or “already covered”), target owner, inputs/outputs, limits, fallback, proposed test and expected measurable benefit.
6. Keep knowledge and tool decisions independent. A useful paper/skill does not automatically deserve an installed plugin. A failed Toolbox gate does not invalidate every abstract technique.
7. Present P0/P1/P2 recommendations and a small implementation/test plan. Stop for owner scope approval before executing it. A legitimate outcome is no change.
8. After any later authorization, use original maintainable wording/code, preserve licences/attribution where required, and run appropriately scoped technical and real-output comparisons. Do not copy entire skills or third-party artwork.

Required read-only deliverables:
- Refreshed six-source Audit Matrix, plus this six-item exclusion record.
- Crème de la Crème Knowledge Map with exact sources and delta to current Studio.
- Toolbox Decision Matrix: ADD proposal / UPDATE proposal / NO ADD, with blockers clearly stated.
- Duplicate & Overlap Report.
- Bounded Implementation Roadmap, including tests, costs and stop conditions.
- Verification Report separating PASS, FAIL, NOT RUN and UNKNOWN.

No new orchestrator, duplicate QA loop, copied default style, second audio engine or unsupported promise of cross-host compatibility.

## 7. Verification and handover provenance

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

Start on resume by verifying the current inventory, then analyze the six retained sources and report evidence-backed deltas. The measure of success is better production results with justified complexity, not more integrations.

