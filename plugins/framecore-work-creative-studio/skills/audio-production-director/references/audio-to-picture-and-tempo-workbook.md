# Audio-to-picture and tempo workbook

Use this when a film, ad, reel, clip or storyboard needs sound matched to picture, or when the user wants to build visuals around a track. This is a reusable planning method, not an analysis engine or a claim that the uploaded media was heard.

## Choose the clock and direction

Record the source clock first: delivered-file timecode, source clip time, sequence-relative seconds, or frame count/timebase. Convert only when the actual basis is available. Distinguish measured cut points from a rough supplied list, visual estimate, or proposed edit. Preserve the target runtime separately from measured media duration.

- **Picture-first:** examine the real video and audible track if the host has a suitable authorized inspection path. Note coverage and uninspected intervals. If only a board/shot list is available, map that plan and label it as a plan.
- **Music-first:** examine the actual selected song or supplied pulse landmarks. If no song/inspection exists, use the user's BPM, bar/timecode notes, or propose rhythmic ranges marked as estimates. Design the shots to the musical changes rather than pretending they are already synchronized.
- Do not infer BPM from clip length, file name, waveform peaks alone, shot duration, or genre.

## Build one useful synchronization map

For the requested duration, make a compact table only when it helps the edit. Include:

| Time / basis | Picture or shot ID | Visible change | Music / voice / SFX event | Relation and mix note | Evidence |
|---|---|---|---|---|---|
| measured, estimated, proposed, or unknown | exact shot ID or source interval | action, reveal, contact, texture change, performance beat | onset/hold/tail, phrase/section, transient, VO, Foley or silence | align, lead, trail, crossfade, mask, counterpoint, duck only if planned | source and inspection basis |

Choose accents where action, a reveal, a cut, a repeated motif or an expressive pause supports them. A sound bridge may carry over an image cut; a held shot can gain energy through arrangement, performance or texture without a cut. Avoid a metronomic cut on every beat. Leave speech clear and preserve causality between a visible contact and its sound unless a deliberate offset serves the concept.

For a target around 25 seconds with roughly 4–5-second shots, create enough distinct visual events to use the runtime without padding. Let the selected idea determine exact durations and transitions; label timing as provisional until edited. Close the runtime from actual frame/time data once available.

## Give every shot a transition reason

For each adjacent pair, specify one primary connection or an intentional break: shared motion direction, matched shape/scale, a carried texture, a color/lighting relation, an action consequence, sound pre-lap/tail, graphic match, or a deliberate surprise with a readable reset. Record what is preserved (product identity/label/position, person/wardrobe, screen direction, exposure, camera axis) and what is permitted to change. A connection may be purely sonic or spatial; do not use an unrelated beauty shot as connective tissue by default.

## Verify the chosen generator

Use the live source map in [Music provider routing and rights](music-provider-routing-and-rights.md). Check the current UI/API separately; do not present a vendor-specific prompt syntax or track length as current without a dated source. A prompt can request timed arrangement events, but only a real output inspection can establish whether they landed as intended.

## Finish with a practical review

Check that the cue map uses one time basis, every number has an evidence label, no unobserved cue is described as measured, the product/voice/copy remains legible, and the transitions support the chosen emotional movement. Keep planned, generated, inspected, edited, and rights-verified as separate states.
