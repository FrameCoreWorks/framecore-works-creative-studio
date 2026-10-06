# Code-based motion graphics

Use this profile for explicitly requested coded motion graphics, kinetic typography, animated diagrams, title systems, brand motion or programmatic video. It extends existing owners and the existing Project State. It does not select a different model, create a new agent, or supply a rendering environment.

For substantive art direction, use [motion quality direction](motion-quality-direction.md) and selectively retrieve the [prompt library](../assets/motion-prompt-library/README.md). Include style frames in the existing storyboard review and a focused motion proof during an authorized build. These refine the current method; they add no owner, separate gate or QA budget.

## Runtime selection

Choosing motion area `8` or loading `hyperframes-workflow` does not select HyperFrames or any other engine. Introduce the work as motion graphics from code; mention a specific engine as selected only when the current contract supports it.

Preserve the user's explicit runtime choice and an established working project. If neither decides the route, recommend the simplest suitable available stack from the brief, visual mechanism, editable-delivery needs, variants, export requirements and verified host capabilities. The user need not name a library. Remotion may be recommended for reusable React/TypeScript compositions and variants; HTML/SVG/Canvas with GSAP may suit lightweight vector or 2D scenes; HyperFrames is one optional HTML-video route. Use the [toolkit decision table](motion-toolkit-routing.md#choose-by-the-required-result) for Three.js/R3F, PixiJS, D3 and other specialized layers.

Before the brief is sufficient, leave the runtime Proposed or Unknown and ask only the next consequential brief question. Do not default to HyperFrames, display a mandatory technical questionnaire, or infer installation from a supported route. Explain the chosen stack briefly when it helps the user understand the deliverable. Keep the existing approval, installation, execution and export boundaries; a recommendation grants none of those permissions.

## Start at the requested stage

Reuse supplied decisions and inspect accessible assets or the existing project. Identify the latest contract revision and actual approval evidence. A build or repair request with an already approved contract continues there. Do not repeat onboarding, rewrite successful scenes or invent approval.

For an unresolved concept, Brief Architect resolves material brief gaps, the appropriate direction owner defines the visual mechanism, and Storyboard Sequence Architect owns timed scenes. Motion Graphics Workflow implements HTML/GSAP or plain seekable HTML/SVG; Remotion Video Production implements React/TypeScript. Creative Video Producer coordinates only when several outputs need it. Audio, copy, references and delivery remain with their existing owners.

Ask only the next consequential missing question under the existing workstyle rules. Learning retains exactly one onboarding question per turn and its exercise/feedback method. Do not import a mandatory grouped questionnaire from an example prompt. A complete brief needs no questionnaire. Optional choices may receive clearly marked proposals; a missing required logo, font or approval blocks only dependent production.

Keep three states explicit: Confirmed, Proposed and Unknown. Use [the contract template](../templates/motion-storyboard-contract.md) as the checklist and keep the contract itself in one [motion contract JSON](motion-contract-json.md) file that the storyboard view, runtimes and review share. The three [stage prompts](../templates/code-motion-stage-prompts.md) are optional instruction packets, not a forced sequence for every small repair.

## 1. Brief, concept and storyboard

Establish audience, purpose, message, duration, dimensions, FPS, intended viewing size, platform or supplied delivery specification, exact copy and asset authority. A CTA, voiceover, hook, camera move or music is optional unless the brief requires it. Do not invent platform safe areas.

Choose one communicative mechanism: what changes, why it expresses the message, and how the opening reaches the ending or a deliberate loop. A restrained sustained state can be appropriate. Specify hierarchy, numeric margins, color values, font/weight/size, image treatment and persistence. Keep unknown brand decisions proposed.

For nontrivial art direction, record Creative DNA and a revisioned Style Lock using the [Motion Designer adaptation](motion-designer-adaptation.md). Reuse an approved style instead of exploring again. Keep these fields inside this motion contract and existing Project State. Recompose each requested aspect ratio and assess its copy/holds independently.

Describe motion by function: direction, transform origin, velocity, acceleration, easing, settling, overlap and hold. Use [motion craft](motion-craft.md) for concrete easing presets, frame durations, staggers, reading holds, beat grids and transition choices, and record the selected values in the contract. Constant-speed motion can be linear. Springs, bounce, 3D and camera moves require a reason; they are not quality defaults.

Inventory assets by stable ID, revision/hash when available, purpose, local availability and authority. Inspiration is not permission to reuse artwork. Protected logos retain geometry, proportions and internal spacing. Animate separate components only when authoritative parts exist and that operation is approved. Record exact copy including diacritics independently of incidental scene code.

For each stable scene ID record purpose, copy/asset IDs, master interval, entry/action/exit state, composition, focal point, motion/easing, persistence, outgoing transition, fully readable hold and audio cue or intentional silence. Define at least three observable, concept-specific acceptance criteria, plus mandatory copy and asset locks.

### Frame authority

- Store positive FPS (with numerator/denominator for rational rates), positive integer N, and duration = N / FPS. Frames are 0 through N-1. Scene and cue intervals use inclusive starts and exclusive ends: [start, end).
- If requested duration × FPS is not an integer, propose a concrete frame count and resulting duration or an alternative FPS. Obtain acceptance before changing locked timing; never silently round it.
- All intervals lie on one master timeline. Intentional transition overlaps are explicit, with blend/layer ownership. The union covers the intended output; sum of overlapping scene lengths is not runtime.
- Readable holds exclude entry/exit motion that prevents reading. Check exact copy at target viewing size. Declare the final hold and whether the final state stays or loops.
- Distinguish designed frame timing from measured media timing. Storyboard frames are a plan until a render is inspected.
- A time exactly equal to duration is outside the encoded frame interval. Sample the final output at N-1. Preserve a declared static background during intentional compositional pauses.

Present the proposed storyboard and ask for approval of its identified revision before first implementation. Existing approval for that same contract satisfies this gate. User edits invalidate only affected decisions; assess consequences to copy, layout, timing and assets.

## 2. Implement the approved contract

Inspect actual files, runtime versions, scripts and user edits first. Preserve an established environment. Otherwise choose the simplest available runtime that can meet preview and frame-export requirements:

| Need | Existing owner and route |
| --- | --- |
| React/TypeScript, reusable props, data-driven variants | Remotion Video Production; new 2D projects can start from the [kinetic type starter](../../remotion-video-production/assets/kinetic-type-starter/README.md) |
| HTML/SVG, GSAP timelines or explicit HyperFrames | Motion Graphics Workflow; new projects can start from the [GSAP motion starter](../assets/gsap-motion-starter/README.md) |
| Small code demonstration with no dependencies | The local [frame starter](../assets/code-motion-starter/README.md); SVG sequence export is not encoded video |
| No filesystem, shell or renderer | Complete contract plus the self-contained [single-file preview](../assets/single-file-preview/README.md) the user opens in a browser; implementation source when requested; execution and export marked NOT VERIFIED |

Check current [runtime evidence](code-motion-evidence.md) and installed APIs before writing adapter-specific code. A model name does not establish available tools. Keep the user's selected model; compare models only through a separately requested controlled evaluation.

Centralize brand tokens, copy, frame ranges, asset paths and render configuration. Use small scene components and shared motion helpers. Preview and export must derive the same visual state from the requested frame. Implement play/pause, replay and exact-frame seeking in applicable previews.

Render-critical state must not depend on wall-clock time, cumulative playback history, uncontrolled CSS animation clocks, asynchronous callbacks that have not settled, or unseeded randomness. A preview clock may choose which frame to request; it must not own the scene state. Assets/fonts must finish loading before capture. Resolve resources locally for export; do not silently replace missing media or typography. Pin the runtime environment and record remaining OS/font/browser/codec variability instead of promising universal byte-identical video.

For Remotion, use the installed frame/configuration APIs and account for sequence-local frames. Pass master-frame values explicitly where cross-scene state needs them. For HyperFrames, follow its current composition and timeline registration contract; seek a paused timeline with explicit endpoints. A plain HTML preview requires a real frame capture and encoding route before it can promise video export. Do not add an experimental frame adapter merely to author a normal composition.

Implement approved audio with timed cues, gain and fades. Missing required audio remains a blocker; deliberate silence is an explicit decision. A local render uses only available, authorized tools. Do not install dependencies, call a provider, upload, publish or deploy from the existence of this profile.

## 3. Inspect, repair and deliver

Use the existing shared QA budget: first review plus at most two repair/review passes, with stricter domain limits preserved. Final review is part of that same loop for the artifact, not a reset. Passing scenes remain unchanged.

Inspect actual output at frame 0, N-1, readable holds, and immediately before/at/after each boundary, clipped to valid frames. Where Node and a local Chrome or Chromium are available, the [automated frame review](../assets/motion-review/README.md) captures these frames and flags text outside the frame, clipped by masks, below WCAG contrast or inside the margins; it does not replace watching the sequence. Check layout, text, asset integrity, clipping, masks, flashes, unintended blanks and jumps. Compare selected states from forward playback, replay, backward seeks and direct seeking. Match semantic state exactly; declare a tolerance only for measured raster differences under recorded rendering conditions.

Watch the entire normal-speed sequence and listen to required audio when capabilities allow. Screenshots do not certify rhythm, motion or sound. Inspect the actual encoded file for dimensions, FPS, frame count, duration and required audio/alpha properties. Record timestamp rounding or codec/container limits explicitly; a preview or SVG sequence does not certify an MP4.

Separate objective defects from preferences. Each defect records criterion, expected/observed result, scene/time/frame, severity, cause and smallest repair. Critical defects include wrong locked copy/identity or unusable output; major defects materially harm message, timing, readability or technical delivery. Optional polish must not rewrite the concept or break locks. A lock-changing repair requires a concrete proposal and approval.

Report project readiness, creative/temporal review, audio inspection and encoded-export readiness separately using [the QA record](../templates/motion-qa-record.md). PASS requires evidence for every applicable mandatory criterion; FAIL means an observed failure; NOT VERIFIED displays an existing Unknown or NOT_RUN state. N/A needs a reason. Do not introduce another shared status machine.

Delivery includes the editable project, available review/final exports, exact commands actually supported, dependencies/versions, locations of tokens/copy/timing/assets, safe-edit notes, unresolved blockers and the reviewed revision. An older render cannot certify newer source. A requested deliverable needs no extra ceremonial delivery approval. Publication and external transfers remain separately scoped operations.

## Optional implementation toolkit

Use [motion toolkit routing](motion-toolkit-routing.md) for Three.js/R3F, PixiJS, D3, Mediabunny Canvas encoding, a discoverable local Manim bridge or supported Lottie imports. Read only the selected [runtime card](motion-toolkit-runtime-cards.md); attach [toolkit acceptance](../templates/motion-toolkit-acceptance.md) to the existing QA record. Tool choice does not change approval, ownership, frame intervals or exact-copy locks. Native Remotion export remains first for Remotion projects.
