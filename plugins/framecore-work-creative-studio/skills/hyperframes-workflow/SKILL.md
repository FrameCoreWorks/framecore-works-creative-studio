---
name: hyperframes-workflow
description: Plan, build and review motion graphics from code - kinetic typography, animated titles and logos, explainers, data and product animation. Chooses the runtime from the brief and host capabilities, implements HTML/SVG/Canvas/GSAP or HyperFrames, hands React/TypeScript to Remotion Video Production, and covers storyboard, frame timing, motion craft, preview and render QA.
---

# Motion Graphics Workflow

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research Evidence](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.

The technical ID `hyperframes-workflow` is kept for compatibility. It does not select the HyperFrames engine: present this area as motion graphics from code and choose the runtime from requirements. Use the user's working language; keep exact copy and requested prompt language separate.

## Method

Start at the requested stage and reuse supplied decisions, approvals and the existing project. The full method is the [code-based motion workflow](references/code-based-motion-graphics.md); this entry summarizes its order.

1. **Stage and inputs.** Identify whether the request is a concept, storyboard, build, repair or review. Confirm it is time-based motion, not a static raster graphic. Collect what exists: brief, exact copy, assets, brand tokens, runtime and delivery needs. Ask only the next consequential missing question.
2. **Concept and storyboard.** Define one communicative mechanism, the scenes on one master frame timeline with readable holds, and exact copy and asset locks in one [motion contract JSON](references/motion-contract-json.md) file, using the [storyboard contract](templates/motion-storyboard-contract.md) as the field checklist. When several aspect ratios are needed, declare them as [formats](assets/motion-scenes/README.md#formats) of the same contract instead of separate projects. Present it to the user as a storyboard table, not raw JSON. Keep Confirmed, Proposed and Unknown explicit. Present the identified revision for approval before the first build; existing approval of the same revision is enough.
3. **Motion design.** Apply [motion craft](references/motion-craft.md) for easing, durations, staggers, holds, rhythm and transitions, and [motion quality direction](references/motion-quality-direction.md) for references, style frames and a focused motion proof. Record the chosen values in the contract's motion system. With music or voice-over, use the [sync tool](assets/motion-sync/README.md) for the beat grid and captions. When inspiration helps, match the brief in the library's [brief index](assets/motion-prompt-library/brief-index.json) and select at most three records from the [motion prompt library](assets/motion-prompt-library/README.md).
4. **Runtime.** Preserve an explicit user choice or a working project; otherwise recommend the simplest suitable available stack using the [runtime selection](references/code-based-motion-graphics.md#runtime-selection) and the [toolkit routing table](references/motion-toolkit-routing.md#choose-by-the-required-result). React/TypeScript compositions go to [Remotion Video Production](../remotion-video-production/SKILL.md).
5. **Build.** Only when authorized and capable: implement the approved contract with every visual state derived from the requested frame, shared preview and export state, loaded fonts and assets, and no wall-clock or unseeded randomness. Declare scenes with the [scene kinds](assets/motion-scenes/README.md) where they fit, so the contract alone drives the preview and the Remotion render; write custom scene code only for the rest. Start from a starter when no project exists: the [GSAP motion starter](assets/gsap-motion-starter/README.md) for HTML, the [Remotion kinetic type starter](../remotion-video-production/assets/kinetic-type-starter/README.md) for React/TypeScript, or the dependency-free [frame starter](assets/code-motion-starter/README.md). Both runtime starters read the same `motion-score.json` contract.
6. **Review and deliver.** Where Node and a local Chrome or Chromium exist, run the [automated frame review](assets/motion-review/README.md) first and repair its errors. Inspect actual output at frame 0, N-1, readable holds and both sides of each boundary, watch the full sequence when possible, and inspect the encoded file. Use the [QA record](templates/motion-qa-record.md) within the shared review budget, then deliver the editable project, exports actually produced and remaining limits.

In a host without shell or renderer, finish with one clickable link that opens the [motion player](assets/single-file-preview/README.md#how-studio-delivers-it) with the contract loaded: `https://framecoreworks.github.io/framecore-works-creative-studio/#contract=` plus the contract as compact UTF-8 JSON in base64url without padding, computed with code execution, never typed; attach the `<id>.motion.json` file too. Every scene declares a scene kind. The user watches there and presses Export video for a video-only MP4 or WebM file ([browser video export](assets/motion-export/README.md)). Do not render a substitute video with code other than the plugin's renderers. Never hand-write a player, renderer or export; a complete HTML file is delivered only as the template copied byte for byte with its contract replaced. If a self-written page is unavoidable, its export must reproduce `video-export.mjs` (WebCodecs, frame by frame), never `MediaRecorder` or real-time recording. Mark preview and export NOT VERIFIED until someone has actually watched the file. The optional [stage prompts](templates/code-motion-stage-prompts.md) are instruction packets, not a mandatory sequence.

## Owners around this skill

| Need | Owner |
| --- | --- |
| Story, scene order or timed shot cards are unresolved | [Storyboard Sequence Architect](../storyboard-sequence-architect/SKILL.md) |
| Captions, overlays, titles or VO text are not locked | [Copy Voice](../copy-voice/SKILL.md) |
| Source assets, revisions or rights are unclear | [Asset Manifest](../asset-manifest/SKILL.md) or [Reference Pack Curator](../reference-pack-curator/SKILL.md) |
| React/TypeScript composition, reusable props or data-driven variants | [Remotion Video Production](../remotion-video-production/SKILL.md) |
| Music, sound design or voice | [Audio Production Director](../audio-production-director/SKILL.md) |
| Several video outputs need coordination | [Creative Video Producer](../creative-video-producer/SKILL.md) |

## Guardrails

- A work-area choice or this skill's name never selects a runtime, installs tools or authorizes rendering, uploads or publishing.
- HyperFrames is a coded-video path, not a paid media-provider integration.
- Do not use coded overlays to bypass the one-pass policy for raster graphics with visible text.
- Do not invent runtime APIs, package versions, platform safe zones or render results; check installed versions and current documentation when a named tool's behavior matters.
- Do not claim a render, playback or audio review that did not actually happen.
- Keep private paths, unapproved assets and hidden metadata out of deliverables.

## Handoff

Review gate: `structure_fit`. The workflow role `hyperframes-producer` maps to this skill and `execution-manifest` to the existing manifest owners. Keep the internal `HyperFrames Production Brief` handoff type for compatibility; it is not an engine selection. Hand off with:

- `scene_list` and `timing` on the master frame timeline
- `copy_locks` and `asset_needs`
- `motion_system` with the chosen easing, durations, staggers, holds and transitions
- `runtime` stated as selected, proposed or unknown
- `implementation_prompt` or component brief
- `render_constraints` and `render_qa_checklist`

## QA checklist

- The plan is time-based motion, not static raster generation.
- Every scene has a frame interval, focal point, readable hold and transition.
- Motion values come from the recorded motion system and serve the message.
- Text is readable at the intended viewing size for the full hold.
- Assets, fonts and exclusions are explicit; locks are preserved.
- Preview, temporal review, audio and encoded export are reported separately, with NOT VERIFIED where evidence is missing.
