# Motion quality direction

Use this extension inside the existing code-motion contract, not as another owner, approval gate or mandatory questionnaire. Scale it to the task. A tiny repair keeps its accepted design. A library choice is a starting hypothesis, never client approval.

## Read references as design evidence

For each selected reference, record author/source, model attribution source, time ranges actually inspected, and whether the prompt is original, reconstructed or unknown. Describe composition, type hierarchy, motion paths, pacing, scene continuity, materials and ending in observable terms. Keep source claims separate from your visual observations. Never infer full temporal or audio QA from a contact sheet.

Extract a transferable mechanism, then change subject, composition and narrative to suit the brief. Do not clone a creator's signature layout, brand geometry or music. Popularity and particle count are not quality scores. Consult [research findings](motion-quality-research.md) and the [prompt library](../assets/motion-prompt-library/README.md); load only relevant records.

## Prove the design before expanding it

Within the existing storyboard approval, include one opening, one dense information frame and the ending for nontrivial projects. Use actual copy, available fonts and approved assets at target viewing size. Describe their visual hierarchy and three measurable acceptance criteria. If approval already covers these decisions, do not ask again.

After build authorization, implement a short proof of the hardest transition or central motion mechanism in the selected runtime. Inspect it before expanding the remaining scenes. Use the existing QA budget. A local prototype is not another unrequested deliverable or a license to run external generation.

Keep a concise motion score inside the storyboard:
- focal subject and information revealed by each transformation;
- start, action, readable hold and exit in master frames;
- energy level and the reason for a quiet or busy passage;
- recurring shape, alignment or camera relationship that links scenes;
- sound event, gain and tail, or approved silence;
- exact-copy and asset locks; final resting state or loop seam.

Use variable intensity deliberately. Do not put all text on springs, animate every letter independently, cut on every beat, or add HUD labels, particles, glow and grain to fill empty space. Detail must support the message. Showreel variety is appropriate for a showreel; a product explanation needs a coherent causal sequence.

## Typography and information

Set type on an explicit grid. Specify family, weight, size, line length, tracking, alignment, margins and contrast. Preserve kerning and protected wordmarks. Use a real font file and wait for loading; do not silently substitute it. Test long strings, diacritics and the smallest intended viewing size. Reading holds begin only when the full phrase is legible. Estimate holds from text complexity, then confirm through playback; no universal one-second rule.

Use actual data and sources for data motion. Keep scales stable unless a change is disclosed, preserve units and distinguish illustrative numbers from claims. A statistic increasing smoothly does not make it true. For spatial work, composition and camera continuity matter more than adding geometry.

## Material and sound choices

Add a procedural material only when it supports an approved surface or metaphor. [Optional adapters](../assets/motion-quality/README.md) cover Paper Shaders and Tone.js without installing either. Use one frame authority. Paper's setFrame argument is milliseconds, not a frame index. GPU output may vary; record actual environment and measured tolerance.

Sound design follows the same cue frames as visual impacts: plan it from the contract with the [motion sound tools](../assets/motion-sound/README.md), which design layered effects and a composed bed at studio standard and check the timing. Confirm rights for supplied tracks. Measure peaks and loudness, but reserve audio PASS for actual listening and sync inspection. Silence may be the best direction.

## Review by defects, not effect count

Use the existing [QA record](../templates/motion-qa-record.md). Review at final dimensions and intended viewing scale, then inspect encoded frames around cuts and holds. Compare the complete normal-speed sequence with the motion score. Distinguish static composition, temporal rhythm, audio, export and source readiness. A failed comparison at a scene boundary is a defect; a preference for another palette is not.

Keep the shared first review plus at most two repair passes. Repair the identified scene and neighboring transitions. Preserve passing scenes and approved locks. If essential evidence is unavailable, state the specific limitation and leave that modality NOT VERIFIED.

The existing output reviewer should judge against the predeclared criteria, with a frame/time reference for every material finding. Do not accept the builder's praise as evidence. Where a real independent reviewer is available and warranted, keep its review separate from implementation; roles alone do not prove separate execution. Calibrate subjective judgments with the user's accepted references and explicit counterexamples. A later, more complex iteration is not automatically better; retain the strongest compliant revision within the current budget.

## Review passes and scores

Within the existing review budget, look at the video in these passes (adapted from [kaventro/motion-designer](kaventro-motion-designer-adaptation.md)):

1. **Overview** at about two frames a second: does the story read, and does every result hold long enough?
2. **Transitions** frame by frame from about 0.3 s before to 0.3 s after each cut: flashes, pops, overlaps, mask edges.
3. **Text at full size:** truncation, clipped descenders, alignment, size.
4. **Phone size:** the whole video at 360 px wide (`--stills-width 360` in the [Python renderer](../assets/motion-render/README.md)). What cannot be read there cannot be read in a feed.
5. **Frame 0 and fresh eyes:** frame 0 is the thumbnail most players and feeds show, so it must be a finished frame worth posting. Can someone new to the subject say what it is, what it does, for whom, and where to find it?

Score each stretch from 1 to 10 on hook (the first two seconds), readability, motion, variety, composition, sync and accuracy, and give every score under 8 a finding with a frame reference that would raise it. Scores guide repairs inside the shared budget; they do not extend it.

| You see | Usual fix |
| --- | --- |
| A label or word cut short | reframe, shorten with the user's approval, or choose data that fits; never ship a cut word |
| Descenders cut at the bottom of a mask | a taller mask (about 1.3 times the font size) |
| Text crossed by a moving element | reorder layers or move the path; hold the text until it passes |
| A layer flashing in its end position for one frame | show it at the frame its motion starts |
| A layer popping in or out without motion | give it an entry or tie it to something that moves |
| An action between beats | move it onto the beat; offsets inside a beat are for secondary motion only |
| Fast moves strobing | render with motion blur (`--blur 8`) |
| Banding in dark gradients | flat backgrounds, or dithering at encode time, never per-frame noise |

For a requested model comparison, use [the benchmark packet](../templates/motion-model-comparison.md). Model superiority requires comparable outputs, not provider marketing or selected social examples.
