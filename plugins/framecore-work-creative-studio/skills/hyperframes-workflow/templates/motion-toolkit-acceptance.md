# Motion toolkit acceptance attachment

Attach this to the existing [motion QA record](motion-qa-record.md) for a toolkit example or project. Reuse its review pass and statuses: PASS, FAIL, NOT VERIFIED or justified N/A. NOT VERIFIED displays an existing Unknown / NOT_RUN state. This is a reporting worksheet, not a new shared schema, gate or state machine.

## Contract and environment

- Approved motion contract/revision and source revision:
- Selected existing owner and [runtime card](../references/motion-toolkit-runtime-cards.md):
- Actual host/client and available execution surfaces:
- Installed package versions, lockfile revision, OS/browser/renderer:
- Current task's execution/install authorization, when applicable:
- Actual source/output locations and artifact hashes, with no private host paths in published reports:
- Width, height, FPS numerator/denominator, integer `N`, duration `N / FPS`:
- Dataset, exact copy, asset revisions/rights and required fonts:
- Audio: required asset/cue mapping or deliberate silence:
- Requested container/codec, pixel format and alpha requirement:
- Commands actually executed, exit results and evidence locations:

Copy examples into an authorized project directory before installing dependencies. Do not install `node_modules`, rendering caches or generated outputs inside the installed plugin package. Keep example source and produced media separately identifiable.

## Common evidence

| Check | Status | Observed result and exact evidence | Limitation or blocker |
| --- | --- | --- | --- |
| Source/versions correspond to this output | NOT VERIFIED | | |
| Required libraries and renderer exist in this host | NOT VERIFIED | | |
| One frame authority; assets and exact fonts ready before capture | NOT VERIFIED | | |
| Frame 0, N-1, holds and before/at/after boundaries | NOT VERIFIED | | |
| Same selected states after forward, replay, backward and direct seeks | NOT VERIFIED | | |
| Normal-speed playback and required audio reviewed | NOT VERIFIED | | |
| Encoded file dimensions/rates/count/duration match the contract | NOT VERIFIED | | |
| Audio/alpha/container properties satisfy the actual delivery | NOT VERIFIED | | |
| Editable source, output and safe-edit notes delivered | NOT VERIFIED | | |

Record the tested frame order and actual selected frames. Compare semantic state exactly; specify and justify any raster tolerance with renderer conditions. Do not infer full playback or audio quality from stills. `ffprobe` metadata cannot certify visual quality; a displayed preview cannot certify exported media. A failed mandatory check requires a bounded repair, not a relabel as N/A.

## Route-specific evidence

Complete only applicable rows. A route not executed remains NOT VERIFIED; absence of a planned optional route is N/A with that scope reason.

| Route | Minimum discriminating observation | Status and evidence |
| --- | --- | --- |
| Three.js / React Three Fiber / Remotion | Frame-derived transforms; actual Chromium/OpenGL selection; stable camera, lights and geometry; inspected native render | NOT VERIFIED |
| PixiJS | Automatic ticker disabled; deterministic particles/masks/filter state; correct canvas dimensions; no stale pixels after backward seek | NOT VERIFIED |
| D3 | Exact source values, units, categories and final labels; consistent scale/domain; no timer or live simulation drift | NOT VERIFIED |
| Mediabunny | Configuration-specific codec check; N awaited Canvas frames with explicit timestamps/durations; finalized output; independent media inspection | NOT VERIFIED |
| Manim bridge | Actual available local runtime; measured clip properties; explicit master-to-clip mapping; inspected assembly boundaries | NOT VERIFIED |
| Lottie JSON | Actual player/build and local resource readiness; explicit asset-frame mapping; forward/backward/direct seek agreement | NOT VERIFIED |
| dotLottie archive | Compatible player, selected animation and local WASM/resources; same-frame capture observed for this archive | NOT VERIFIED |

## Findings and handoff

- Objective defect, criterion, expected/observed result, scene/frame and severity:
- Smallest repair, unchanged locks and neighboring frames to recheck:
- Existing review pass used / remaining budget:
- Source ready:
- Preview observed:
- Encoded export observed:
- Temporal/audio QA observed:
- Unresolved host, asset, codec or rights limitation:
- Existing owner receiving the next bounded action:

Do not claim all toolkit paths passed from a single example. Source-level checks, live rendering, playback review, host registration and paired release publication have separate evidence owners.
