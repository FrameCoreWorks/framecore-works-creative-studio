# Eleven video effects: temporary source pack and assessment

Date: 2026-11-10. Assessment by ChatGPT Work for FrameCore Works; Change-ID: `CW-20261110-03`.
Inspected Studio baseline: `8ee1e061caab9c58eed96b8eaa6de6bd8fd7c0ba`, package 1.174.1.

This folder preserves the owner-supplied [original ZIP](11-free-video-effects.zip) unchanged, with an independent assessment. It supports [the Motion Graphics implementation task](../../handover-creme-de-la-creme-2026-11-09.md#9-owner-addition-ultra-skills-motion-effects-implementation-2026-11-10). It is a temporary transfer packet: Claude must read it, preserve the needed findings and present the plan, then remove this folder and the development handovers under the [owner's cleanup instruction](../../roadmap.md#temporary-handovers-owner-instruction-2026-11-10).

## Contents and provenance

| Item | Observed evidence |
| --- | --- |
| Archive | `11-free-video-effects.zip`, 1,809 bytes, supplied by the owner and published at the owner's request |
| Archive SHA-256 | `70a9da67f79262ec04fcd5b57729ae63776522773ea5dfd2aadecda7d8f31e8b` |
| Only member | `11-video-effects.md`, 4,119 uncompressed bytes |
| Member SHA-256 | `cda6b51a278ac051945c8317016b13590779ebcfa45b60a95bc7ba6ad1c65f14` |
| Actual material | Eleven short effect descriptions, suggested uses and natural-language prompts targeting an existing Remotion project |
| Not supplied | Implementation code, components, project configuration, lockfiles, tests, reference reel, video loops, fonts or other media |
| Original author, source URL, licence and redistribution terms | UNKNOWN; the archive contains no attribution, source link or licence declaration |
| Relationship to Ultra Skills | UNKNOWN. The supplied archive does not identify its publisher or prove that it is an excerpt of the advertised 30-prompt collection. Keep that web preview and this eleven-item source distinct. |

The archive's claim that its examples were made in code is a source claim, not a reproduced result. This assessment is FrameCore's own analysis; the included source text is not represented as FrameCore-authored or automatically covered by the repository's licence. Resolve source rights before copying prompts, code or media into distributed plugin content. Write original production recipes and retain appropriate attribution.

## Assessment against existing Studio capabilities

**Recommendation:** useful as a compact scene catalogue and a source of combinations to evaluate; limited incremental value as technical documentation. It is not a ready renderer, plugin or eleven implemented effects. Atlas entries and references establish documented mechanism overlap, not acceptance of these exact scenes.

The table paraphrases visual intent. Existing atlas IDs refer to the [technique atlas](../../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/technique-atlas/atlas.json); the [After Effects craft reference](../../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/after-effects-craft.md) and [motion compendium](../../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-compendium.md) provide additional overlap.

| Source effect | Visual idea | Existing overlap and proposed value |
| --- | --- | --- |
| 01 Orbit | Moving, rotating phone with a fast feed and attached label | `camera-orbit`, `ui-scroll` and product-film guidance cover parts. Evaluate one reusable device scene shared with Phone Screens. |
| 02 Vertigo | A retreating camera stretches a corridor around a constant-size subject | Existing `dolly-zoom` explicitly couples camera distance and field of view. The source omits that implementation detail; treat this as a scene variant. |
| 03 Zoom-through | A rapid move through a foreground tile into the next grid | Existing `zoom-through`. Define transition duration, layering and landing readability before considering an extension. |
| 04 Headlines | A wall in perspective with neighboring headline columns moving in opposite directions | `ui-scroll` supplies a related mechanism. A configurable multi-column layout with reading holds is a worthwhile composition to assess. |
| 05 Paper Cut | A paper layer lands with a bounce, followed by word impressions timed to speech | `stamp-impact`, typography and existing timing guidance cover much of it. Add texture and voice alignment only where the current recipe is insufficient. |
| 06 Charts | Two staggered waves of growing bars | Existing `bar-grow`. A decorative wave is not evidence for a growth claim; require data, scale and labels for factual charts. |
| 07 Phone Screens | A centered phone feed, expanding rings and side labels | Shares the device/feed core with Orbit. Prefer parameters and presets within one component over a second device system. |
| 08 Frame Break | A character crosses a poster boundary as its surface breaks into tiles | `shatter` and `shatter-transition` cover fragments. Character segmentation, front/back occlusion and coordinated breakout add the most useful composition-level question. |
| 09 Pullback | A close view opens upward to reveal a complete card board | `crane-tilt` and camera guidance cover related movement. Evaluate framing and readable final scale as an existing-mechanism variant. |
| 10 Glitch | Brief channel separation and displaced horizontal strips | RGB split/glitch already appear in craft guidance. Specify intensity and restoration; avoid another duplicate effects catalogue. |
| 11 Typewriter | Terminal text, cursor and per-character sound cues | `terminal-run`, `typewriter` and `typing-input` already cover related motion. Assess sound-event alignment and readable pacing rather than naming this a new capability. |

## Suggested integration plan

1. Compare the exact target scenes with the current owners and reusable assets. Prioritize **Frame Break**, **Headlines**, then **one device component for Orbit and Phone Screens**. This is a review priority, not proof that those components are absent or must be added.
2. Use [Motion Graphics](../../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/SKILL.md) for selection, composition and review, with the existing [toolkit routing](../../../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-routing.md). The source naturally targets the [Remotion owner](../../../plugins/framecore-work-creative-studio/skills/remotion-video-production/SKILL.md); HyperFrames requires an original equivalent using the selected project's supported tools. A prompt is not portable executable code.
3. Keep FrameCut as the consumer of resulting clips where applicable; this packet does not create eleven native FrameCut effects. It has no Toolbox admission requirement and no dependency relationship with the map companion.
4. Define editable copy, typography, colours, asset inputs, camera, easing, duration, dimensions, seed and sound cues. Derive state from the frame clock and resolve assets before capture. The source's six-frame and eight-frame transitions need an explicit master FPS and duration in seconds. Match speech to an actual timing source, not guessed word intervals.
5. For a dolly zoom, specify distance/FOV compensation. For a breakout, specify the character mask and occlusion order. For a factual chart, specify the actual dataset and scale. Use separately composed portrait and landscape layouts when both are requested.
6. Under the existing task authorization, implement only demonstrated gaps using original code/recipes and existing dependencies. Installations, paid services and other restricted actions retain their separate authorization requirements. Do not run upstream setup instructions merely because a source recommends them.

## Verification and limits

- Archive inventory, CRC and both SHA-256 values: checked locally; one Markdown member, no executable project.
- Static comparison: the supplied eleven briefs were compared with the cited Studio atlas, craft, routing and owner documentation.
- Rendering, playback, sound review, fresh-host behavior and exact-scene acceptance: **NOT_RUN**. No source prompt was executed, no dependency installed and no plugin changed by this archive-saving task.
- Proposed acceptance: representative renders for every new or materially changed mechanism; first/last frames and boundaries; repeated and backward seeks; layer/occlusion checks; copy readability; actual media duration/FPS/dimensions; sound alignment; full playback and format-specific review.
- Repository regression checks for the saving task are recorded in the [development ledger](../../development-ledger.md#cw-20261110-03). Those checks do not demonstrate that these eleven effects work.
