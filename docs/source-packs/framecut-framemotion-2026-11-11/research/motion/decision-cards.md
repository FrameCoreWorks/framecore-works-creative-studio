# FrameMotion applied motion craft: decision cards

Research evidence, 2026-11-11 Europe/Warsaw. Planning directory retains its 2026-11-10 name. This is a source-grounded working curriculum, not a claim of senior practitioner mastery, a shipping skill, or validated renderer parity.

The factual anchors below are newly checked primary-source material. The manual exercises, engine-neutral contracts, adapter designs and checks are original proposals for later implementation and expert review. None of these examples was rendered in this research pass. Imported FCWM preferences remain separate: reading time, quiet-frame limits, recorded-sound preference, engine choices and approved one-shot exceptions are documented in the extraction analysis. A historical brand preference is not a scientific law.

Use a card by naming the intended audience effect, making a minimal manual study, expressing the required behavior without tool vocabulary, selecting a supported implementation, and reviewing the actual output. The counterexample is part of the card: an agent that always applies the named technique has not learned the decision.

## M01 — Stage one primary change

**Intent.** Make the audience notice the intended event before they inspect decoration.

**Verified anchor.** IBM treats staging as a way to avoid competing actions; this is professional brand guidance, not a universal ban on simultaneous motion. [IBM Design — Classic principles](https://www.ibm.com/design/language/animation/classic-principles/).

**Manual procedure.** Block three still poses first: before, decisive change, resolved state. In AE, solo the information-bearing layers, animate the decisive event, then restore supporting layers individually. Compare the added layer against the unadorned version.

**Engine-neutral decision.** Record primary_subject, intended_takeaway, decisive_interval and secondary_actions. Give each secondary action an explicit supporting role.

**Code mapping, proposed.** Proposed adapter: independent named tracks with a priority annotation; schedule decoration after the decisive interval or reduce its salience. Priority is an editorial constraint, not a renderer feature.

**Counterexample.** A crowd, celebration or deliberately chaotic montage may need multiple simultaneous events. The task is then to stage an overall pattern, not mechanically serialize every object.

**Output check.** At delivery size and normal speed, ask a fresh viewer what changed first and what mattered. Record their answer before explaining the intent. A screenshot or number of moving layers cannot certify hierarchy.

**Future contrast fixture.** Three simultaneous equally bright reveals versus a staged version; retain the version with the clearer intended takeaway, not automatically the quieter one.

## M02 — Carry attention across a cut or transformation

**Intent.** Reduce unnecessary visual searching when the next shot completes the previous idea.

**Verified anchor.** The practitioners describe eye-trace using focal placement and attention cues across a sequence. [School of Motion — Eye Tracing in Animation](https://schoolofmotion.com/blog/eye-tracing-animation).

**Manual procedure.** Mark the likely focal point on the last useful frame of shot A and first useful frame of B. Try a matched position, then a deliberate shift. Preview the cut without overlays; judge whether the shift clarifies or interrupts the idea.

**Engine-neutral decision.** Store focal regions, not just object centers. Record whether the transition promises continuity, contrast or a reveal.

**Code mapping, proposed.** Proposed adapter: composition landmarks in normalized coordinates plus per-format overrides. A debug overlay may display the focal path, but it must never become delivered artwork.

**Counterexample.** A surprise, threat or change of viewpoint may depend on a discontinuity. Always matching the center can make a sequence inert or spoil a reveal.

**Output check.** Watch the transition without pausing. Ask where attention went and whether the next fact was missed. Treat this as a viewing observation, not measured eye tracking.

**Future contrast fixture.** A wide shot with the subject at right followed by a label at left; compare an intentional lead cue, a matched placement and an abrupt reveal.

## M03 — Separate where an object travels from when it travels

**Intent.** Give path shape and timing independent creative control.

**Verified anchor.** AE distinguishes spatial interpolation from temporal interpolation. [Adobe — Keyframe interpolation](https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/animation-keyframes/keyframe-interpolation.html).

**Manual procedure.** First draw the route through the required positions. Then inspect timing in the Graph Editor while keeping that route fixed. Compare an even traversal, a pause near a landmark and a fast exit.

**Engine-neutral decision.** Represent trajectory p(u) separately from progress u(t). State whether u measures a curve parameter or traveled distance.

**Code mapping, proposed.** Proposed implementation: x,y = path(progress(time)). For constant travel speed on a curved path, add an arc-length lookup or equivalent evaluation; a linear Bezier parameter is not assumed to be constant distance.

**Counterexample.** A reveal mask may intentionally accelerate through a sharp curve. Constant speed is not always the desired result, and smoothing the route can erase a designed corner.

**Output check.** Inspect positions at equal time steps and play the shot. Verify the object reaches landmarks at the specified beats without an accidental kink or unexplained stop.

**Future contrast fixture.** Same curved path with two timing functions; same timing with two path shapes. Tests should demonstrate that changing one does not silently rewrite the other.

## M04 — Shape speed for the action, not for an easing label

**Intent.** Communicate weight, urgency or restraint through arrival and departure.

**Verified anchor.** AE exposes velocity and influence; GSAP CustomEase accepts custom curve data. Neither source says that a named easing is inherently polished. [Adobe — Speed](https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/speed-between-keyframes/speed.html); [GSAP — CustomEase](https://gsap.com/docs/v3/Eases/CustomEase/).

**Manual procedure.** Inspect the speed graph around each contact or arrival. Adjust the entry, peak and settling portion while watching the whole phrase. Compare a hard stop, a controlled deceleration and a continuous pass-through.

**Engine-neutral decision.** Specify initial/final position, duration and intended boundary velocity. If adjacent segments should flow, require compatible velocity at their join.

**Code mapping, proposed.** Proposed adapter: sample the intended motion at normalized times and compare both position and finite-difference velocity. A shared easing name is insufficient evidence of equivalent curves.

**Counterexample.** A mechanical latch or a comedic snap can require a discontinuity. Imposing smoothness everywhere can remove force and precision.

**Output check.** Plot and inspect the join, then view at actual speed. Reject a hidden pause caused by easing both halves to zero when the object should pass through.

**Future contrast fixture.** Two segments meeting at a waypoint: stop-and-go versus continuous travel. Preserve both as distinct authored choices.

## M05 — Use anticipation only when it explains the next action

**Intent.** Prepare the viewer for a meaningful action without adding a compulsory flourish.

**Verified anchor.** IBM includes anticipation in its applied animation principles; its restrained treatment is a brand choice. [IBM Design — Classic principles](https://www.ibm.com/design/language/animation/classic-principles/).

**Manual procedure.** Make the main action understandable without a lead-in. Add a small preparatory pose or directional cue only if it improves causality. Compare the action with and without that cue at full speed.

**Engine-neutral decision.** Declare preparation, action and recovery as optional semantic phases. Explain what the preparation predicts.

**Code mapping, proposed.** Proposed adapter: phase-local tracks with explicit start/end values; preparation may change pose or emphasis without translating the entire object backward.

**Counterexample.** An urgent error alert, a tiny utility transition or a sudden surprise may be weakened by anticipation. A reverse movement can also imply the wrong direction.

**Output check.** Ask whether the preparatory pose predicts the correct event. Check that it does not consume the reading interval or create a false affordance.

**Future contrast fixture.** An opening panel preceded by a hinge cue, contrasted with a pointless whole-panel backward slide.

## M06 — Choose overshoot or bounce from material behavior

**Intent.** Make settling behavior consistent with the object and contact event.

**Verified anchor.** Ebberts distinguishes decaying oscillation from ballistic bounces whose intervals change; these are different motion models. [Dan Ebberts — Realistic Bounce and Overshoot](https://www.motionscript.com/articles/bounce-and-overshoot.html).

**Manual procedure.** Identify the equilibrium or contact plane before animating. For an elastic settle, inspect excursions around equilibrium. For bouncing contact, inspect each impact and subsequent flight rather than stretching a generic oscillation.

**Engine-neutral decision.** Record material hypothesis, contact rule, incoming velocity and resting state. Decide whether the motion is stylized or physically motivated.

**Code mapping, proposed.** Proposed adapter: select an oscillator or piecewise contact trajectory explicitly. Calibrate against the incoming motion; do not paste a damping value between unrelated solvers.

**Counterexample.** A flat data bar or sober legal title should usually not suggest rubber or collision. A playful graphic may intentionally exaggerate physics, but that is an authored exception.

**Output check.** Inspect contact frames and playback. Look for penetration, unexplained energy gain, a velocity jump at handoff or an object that never settles within its allotted time.

**Future contrast fixture.** An elastic badge and a dropped hard token use different trajectories. A single reused bounce preset should fail the material-intent review.

## M07 — Let follow-through preserve a lead action

**Intent.** Communicate connected parts and delayed response without making the scene feel desynchronized.

**Verified anchor.** IBM discusses overlap; Remotion supplies frame-based spring evaluation. These establish concepts and an API, not a ready-made expressive rig. [IBM Design — Classic principles](https://www.ibm.com/design/language/animation/classic-principles/); [Remotion — spring()](https://www.remotion.dev/docs/spring).

**Manual procedure.** Animate the leading part first. Add a delayed response to one dependent part, then adjust its recovery. Temporarily hide the follower to see whether the main action still reads.

**Engine-neutral decision.** Describe lead/follower relationships, delay, relative amplitude and final alignment. Keep relationship timing separate from layout coordinates.

**Code mapping, proposed.** Proposed adapter: follower local time = global time minus an authored delay, with its own settling parameters. Use a solver only where that response is intended.

**Counterexample.** Rigid manufactured parts that are bolted together should not wobble independently. A label may need to stay stable while its illustrated object moves.

**Output check.** Verify final alignment, intended attachment and a clear lead. An absence of clipping does not prove the overlap feels plausible.

**Future contrast fixture.** A flexible tag following a box versus a rigid handle moving with it; prevent automatic spring insertion on both.

## M08 — Put pivots and coordinate spaces into the specification

**Intent.** Make movement appear attached to the right structure.

**Verified anchor.** AE transforms operate around anchors; parenting changes transform relationships without inheriting opacity. [Adobe — Layer properties](https://helpx.adobe.com/after-effects/desktop/work-with-layers/layer-properties/layer-properties.html).

**Manual procedure.** Place the hinge or attachment anchor before animating. Parent to a null when a group needs a shared movement. Test parent translation, rotation and scale separately, then change the parent's opacity to expose assumptions.

**Engine-neutral decision.** Store local geometry, pivot, parent identity, world transform and opacity policy separately.

**Code mapping, proposed.** Proposed adapter: explicit transform composition with local-to-world conversion. A DOM wrapper may be useful but its opacity behavior must be handled independently; copying AE parenting into a fading wrapper can change the image.

**Counterexample.** A screen-space caption should not inherit a camera/object rotation. Attaching every nearby graphic to the object may destroy legibility.

**Output check.** Overlay the intended pivot and verify that it remains fixed during a hinge motion. Repeat with a non-origin parent and nonuniform scale. Compare child visibility when parent opacity changes.

**Future contrast fixture.** A lid pivots at its edge while a caption stays upright and readable; use this to catch transform-order and accidental opacity inheritance.

## M09 — Animate the reading unit that carries the meaning

**Intent.** Support language instead of treating every glyph as an interchangeable particle.

**Verified anchor.** AE text selectors can target characters, words or lines; selection can include or exclude spaces. [Adobe — Animating text](https://helpx.adobe.com/after-effects/desktop/animating-text/text-animation/animating-text.html).

**Manual procedure.** Set the final typography and line breaks first. Compare a phrase reveal, a word reveal and a character reveal. Preserve a stable final state before the next competing event.

**Engine-neutral decision.** Declare the semantic unit, order, whitespace policy, shaping requirements and final readable interval.

**Code mapping, proposed.** Proposed adapter: shape text before choosing animation units. Do not assume JavaScript string indices equal visible characters or that splitting into spans preserves kerning and connected scripts. Adapter support must be tested for each required writing system.

**Counterexample.** A logotype may benefit from individual letter choreography. A sentence explaining a complex claim often suffers when letters arrive too slowly or move independently.

**Output check.** Review at final size with actual fonts and language. Inspect ligatures, combining marks, right-to-left order, line wraps and clipping. Ask a reader to repeat the message after one viewing.

**Future contrast fixture.** Use Polish diacritics, a long translated title and a connected-script sample where supported; unsupported shaping is an explicit limitation, not a silent fallback.

## M10 — Protect comprehension time during retiming

**Intent.** Preserve the moment when information can actually be read.

**Verified anchor.** AE responsive time protects specified temporal regions while stretching others. This mechanism does not choose the right reading duration. [Adobe — Responsive design](https://helpx.adobe.com/after-effects/desktop/motion-graphics/add-responsive-design/responsive-design.html).

**Manual procedure.** Mark entry, fully readable state and exit separately. Protect the required readable interval, then shorten the surrounding movement. Preview with the full amount of text and actual competing imagery.

**Engine-neutral decision.** Store readable_start/readable_end independently from layer visibility and animation duration. Imported FCWM's accepted 1.6-second minimum belongs to its profile; longer text or a different audience may need more.

**Code mapping, proposed.** Proposed adapter: retiming constraints preserve semantic intervals and report infeasibility when the target is too short. Never quietly compress a locked hold to hit a requested duration.

**Counterexample.** A one-word flash used as texture may not promise full reading; a safety instruction cannot inherit that treatment. Long stillness can be intentional and should not be rejected by a global motion-activity threshold.

**Output check.** Measure the interval after the text settles and before it is occluded, blurred or displaced. Confirm comprehension at normal playback; metadata alone cannot establish it.

**Future contrast fixture.** A short label and a two-line explanation receive different holds; a duration reduction must either preserve both or explicitly request a content/timing tradeoff.

## M11 — Specify matte meaning and its coordinate frame

**Intent.** Reveal the intended area without reversing coverage or detaching it from the subject.

**Verified anchor.** Adobe's explicit table and W3C masking agree on alpha coverage; alpha and luminance masking are not interchangeable. [Adobe — Track Mattes and Traveling Mattes](https://helpx.adobe.com/after-effects/desktop/work-with-transparency-and-compositing/work-with-track-mattes-and-traveling-mattes/track-mattes-and-traveling-mattes.html); [W3C — CSS Masking Module Level 1](https://www.w3.org/TR/css-masking-1/).

**Manual procedure.** Create a simple black/white/transparent test matte before the artistic one. Confirm normal versus inverted mode. Move the fill and matte independently, then together, to establish whether the reveal belongs to the screen or object.

**Engine-neutral decision.** Record mask source, alpha/luminance mode, inversion, coordinate space and combination operation.

**Code mapping, proposed.** Proposed adapter: compute a coverage field and combine it with the source alpha. A colored opaque image behaves differently under alpha and luminance modes; do not infer mode from its appearance.

**Counterexample.** A stationary screen-space window is correct for some reveals; forcing every mask to follow the object changes the idea.

**Output check.** Verify known 0%, partial and full coverage patches, then inspect feathering and transformed bounds. An all-transparent output must fail even if rendering succeeded.

**Future contrast fixture.** Opaque black, opaque white and transparent white patches distinguish alpha from luminance. Note: Adobe's introductory sentence conflicts with its table; the contradictory wording is not imported.

## M12 — Treat transparency as a delivery contract

**Intent.** Keep soft edges clean when an asset is reused over a different background.

**Verified anchor.** Adobe identifies straight/premultiplied interpretation mismatch as a cause of edge artifacts. [Adobe — Importing and interpreting footage items](https://helpx.adobe.com/after-effects/desktop/work-with-footage-items/import-and-interpret-footage-items/importing-interpreting-footage-items.html).

**Manual procedure.** Inspect the alpha channel separately and composite the asset over dark, light and saturated backgrounds. Correct source interpretation before adding edge treatments.

**Engine-neutral decision.** Record alpha representation, matte/background assumptions, color encoding and intended delivery codec/container separately.

**Code mapping, proposed.** Proposed adapter: declare where RGB is associated with alpha and where conversion occurs. Use a known half-covered color patch to test the complete import-render-export-import path.

**Counterexample.** A deliberately opaque video needs no invented transparency. Removing a real colored rim because it resembles a fringe can damage the design.

**Output check.** Reimport the delivered file in an independent reader. Inspect translucent edges and verify that intended empty pixels remain transparent. A checkerboard screenshot is insufficient evidence of encoded alpha.

**Future contrast fixture.** A soft orange disc over black, white and blue backgrounds should preserve edge color; a mismatched-alpha variant should visibly fail.

## M13 — Use precomposition to control evaluation, not only tidiness

**Intent.** Choose which operations happen before or after grouping and transformation.

**Verified anchor.** AE render order depends on layer type and collapse settings; nesting can alter effects and 3D interactions. [Adobe — Precomposing, nesting, and pre-rendering](https://helpx.adobe.com/my_en/after-effects/desktop/work-with-compositions/precomposing-and-nesting/precomposing-nesting-pre-rendering.html).

**Manual procedure.** Build a minimal comparison with one vector, one mask and one effect. Compare the effect inside versus outside the precomp, then compare collapsed and uncollapsed transforms at a larger scale.

**Engine-neutral decision.** Describe the render graph explicitly: generate, mask, effect, transform, composite. Mark where an intermediate image is flattened.

**Code mapping, proposed.** Proposed adapter: translate the required graph into offscreen surfaces or renderer nodes. A React component, SVG group or canvas save/restore is not evidence of AE precomp equivalence.

**Counterexample.** Flattening may be desirable for a graphic treatment or performance. Keeping everything live can change the intended blur, blending or occlusion.

**Output check.** Inspect edge resolution, effect radius, blend interaction and 3D ordering after scale changes. Keep a small comparison render as evidence of the chosen semantics.

**Future contrast fixture.** A blurred masked vector enlarged after nesting versus before blur; the two are intentionally different and must not collapse to one generic group operation.

## M14 — Choose blur from exposure and readability

**Intent.** Make motion coherent while preserving the information the audience needs.

**Verified anchor.** AE blur uses shutter timing and samples; Remotion's temporal-sampling component warns about color effects. Matching nominal angles does not prove matching images. [Adobe — Assorted animation tools](https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/assorted-animation-tools/assorted-animation-tools.html); [Remotion — CameraMotionBlur](https://www.remotion.dev/docs/motion-blur/camera-motion-blur).

**Manual procedure.** First review the motion without blur. Add blur, inspect the fastest section and adjust exposure timing or sampling only after the trajectory is correct. Keep a crisp comparison for titles and thin details.

**Engine-neutral decision.** Store exposure interval, phase, sample strategy and which layers may blur. Distinguish transform blur from optical-flow processing of footage.

**Code mapping, proposed.** Proposed adapter: evaluate deterministic scene state at subframe times and integrate the selected samples, subject to engine support. Do not describe a static directional blur as equivalent temporal sampling.

**Counterexample.** A restrained information graphic may benefit from crisp movement. Blur can hide an accidental jump while making small text unreadable.

**Output check.** Compare high-speed edges, thin lines, colors and text at delivery size. Increase samples until the relevant result stabilizes; record cost and remaining artifacts.

**Future contrast fixture.** A fast diagonal thin bar and a moving title reveal sampling gaps, color changes and unreadable streaks. No renderer equivalence is certified by this research.

## M15 — Make arbitrary-time evaluation reproducible

**Intent.** Ensure an agent can revise or render any frame without replay-dependent surprises.

**Verified anchor.** GSAP seek preserves play/pause state and suppresses callbacks by default. [GSAP — seek()](https://gsap.com/docs/v3/GSAP/Timeline/seek()/).

**Manual procedure.** In an authored timeline, jump directly to the middle, scrub backward and replay from the start. Compare the same frame after each route. Identify effects driven by accumulated state or callbacks.

**Engine-neutral decision.** Define scene_state(time, immutable_inputs, seed), including assets, font readiness and external-data snapshots.

**Code mapping, proposed.** Proposed adapter: make visible state a function of time; do not rely on skipped callbacks to create objects or populate text. Freeze randomness and initialize the scene before seeking. A paused timeline plus seek is necessary in some adapters but not sufficient.

**Counterexample.** An interactive simulation may deliberately depend on user history. It then needs a recorded input/state history for reproducible export, not a false claim of pure time evaluation.

**Output check.** Render frames in forward, reverse and shuffled order and compare within a declared pixel tolerance. Distinguish expected nondeterministic rendering noise from undeclared state dependence.

**Future contrast fixture.** A callback-created label should reveal why a direct seek can differ from sequential playback; use it as a negative test, not a production pattern.

## M16 — Separate working color from display appearance

**Intent.** Keep compositing and lighting predictable across tools and outputs.

**Verified anchor.** Three.js distinguishes color textures from data textures and requires color conversions; the Blender manual excerpt describes scene-linear processing. [Three.js — Color management](https://threejs.org/manual/pages/color-management.html); [Blender 5.1 Manual — Color Spaces](https://docs.blender.org/manual/en/5.1/render/color_management/color_spaces.html).

**Manual procedure.** Use a small reference scene with neutral ramps, saturated patches and a soft composite. Record input interpretation, working space and view/output transform before adjusting lights or grades.

**Engine-neutral decision.** Carry color-space and transfer-function metadata with assets and intermediate images. Specify the intended viewing/output condition.

**Code mapping, proposed.** Proposed adapter: configure color inputs, non-color maps, working calculations and one deliberate output conversion. A matching hex string in two applications is not proof of a matching displayed result.

**Counterexample.** A stylized blend may intentionally use a different compositing treatment. Preserve the declared look rather than imposing a physically motivated workflow blindly.

**Output check.** Compare a controlled patch chart through export and reimport; inspect clipping, altered saturation and double conversion. Record tool versions and transforms with the result.

**Future contrast fixture.** Color albedo versus a normal/data texture through identical-looking loader code should expose why interpretation matters. Blender full-page access and runtime parity remain unverified.

## M17 — Use 2.5D camera movement to reveal relationships

**Intent.** Create depth or scale without camera motion becoming the subject.

**Verified anchor.** AE camera geometry affects framing; its aperture changes depth of field without changing exposure. [Adobe — Cameras, lights, and points of interest](https://helpx.adobe.com/after-effects/desktop/work-with-layers/camera-layer/cameras-lights-points-interest.html).

**Manual procedure.** Arrange depth planes in a static camera view first. Move the camera just enough to reveal their relationship, then test the shot without depth of field. Keep the intended subject in focus when adding it.

**Engine-neutral decision.** Specify camera pose, projection, sensor/field-of-view assumptions, focus target and the semantic reason for the move.

**Code mapping, proposed.** Proposed adapter: convert coordinate systems and camera parameters explicitly. CSS perspective, AE zoom and a Blender lens number are not portable substitutes without matching geometry and projection.

**Counterexample.** A flat diagram may become less understandable when perspective distorts scale. A camera move cannot manufacture the unseen sides of a flat source image.

**Output check.** Inspect parallax order, occlusion, frame edges and subject legibility. Compare matched framing before judging motion. Do not let blur hide missing geometry or incorrect depth order.

**Future contrast fixture.** Three cards at different depths with a small lateral move and a fixed label; reject cardboard edge exposure or misplaced focus if those contradict the intent.

## M18 — Adapt composition to the format instead of cropping blindly

**Intent.** Preserve the argument of the image across wide, square, vertical and web layouts.

**Verified anchor.** Adobe responsive time is a temporal tool; it does not establish a complete spatial adaptation strategy. [Adobe — Responsive design](https://helpx.adobe.com/after-effects/desktop/motion-graphics/add-responsive-design/responsive-design.html).

**Manual procedure.** Create separate composition views for the target formats. Reassign subject scale, text measure and focal handoff while preserving the same story beats. Judge each at its real display size.

**Engine-neutral decision.** Store semantic anchors, required relationships, minimum readable sizes and per-format overrides. Distinguish reflow, reframing and alternate choreography.

**Code mapping, proposed.** Proposed adapter: solve layout for each viewport/profile, then derive motion endpoints from that layout. Do not animate toward coordinates computed for a different aspect ratio.

**Counterexample.** An intentionally fixed cinematic composition may be letterboxed, if that delivery choice is approved. Reflowing everything can break a carefully staged reveal.

**Output check.** Verify all required content, safe regions from the actual destination specification, line breaks and interaction targets per format. Rewatch eye-trace after layout changes.

**Future contrast fixture.** A two-column wide comparison becomes a sequential vertical reveal; a numeric crop-success test alone must not certify the adaptation.

## M19 — Design a meaningful reduced-motion mode

**Intent.** Keep state changes understandable when nonessential motion is disabled.

**Verified anchor.** WCAG 2.3.3 is AAA and concerns interaction-triggered motion; 2.2.2 is Level A and separately covers qualifying automatic motion and updates. [W3C — Understanding SC 2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html); [W3C — Understanding SC 2.2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html).

**Manual procedure.** Identify the information conveyed by each interaction. Design a stable-state alternative that preserves that information. Test keyboard use, preference changes and pause/stop behavior where applicable.

**Engine-neutral decision.** Separate state transition from its animation. Record whether motion is essential, decorative or informative and document the reasoning.

**Code mapping, proposed.** Proposed adapter: honor reduced-motion preference and expose suitable controls. Switch to a clear state change or another tested treatment; do not merely shorten a large parallax movement.

**Counterexample.** A motion demonstration may need motion to explain its subject, but the essential exception needs an actual rationale. Reducing motion does not remove unrelated accessibility obligations.

**Output check.** Run preference-on/off and dynamic-preference scenarios. Ensure no content disappears, no focus is lost and paused animation does not prevent access to information. This is a scoped motion check, not a WCAG conformance claim.

**Future contrast fixture.** An animated expanding diagram must offer the same labels and relationships in a stable layout; an autoplay loop needs its applicable control behavior tested.

## M20 — Bound values that represent facts

**Intent.** Keep expressive motion from changing the apparent data or allowed state.

**Verified anchor.** Remotion interpolation has separate left/right extrapolation settings; a spring can overshoot unless configured or constrained. [Remotion — interpolate()](https://www.remotion.dev/docs/interpolate); [Remotion — spring()](https://www.remotion.dev/docs/spring).

**Manual procedure.** Separate the decorative container from the factual value. Inspect the graph before and after the active interval, not just at its endpoint. Keep labels truthful during settling.

**Engine-neutral decision.** Annotate quantities as bounded, categorical or decorative. Specify the allowed domain and whether intermediate values are meaningful.

**Code mapping, proposed.** Proposed adapter: use extrapolateLeft/extrapolateRight explicitly for bounded interpolation and verify pre/post frames. Apply expressive spring motion to a separate visual property when it would otherwise imply a value above the real maximum.

**Counterexample.** A deliberately elastic shape can exceed its final size. Clamping all motion would remove that expression; only the factual or constrained channel needs the bound.

**Output check.** Evaluate before start, at boundaries, at peak and after end. Check both the numeric state and its visible representation. The audited single extrapolate option must remain a negative fixture.

**Future contrast fixture.** A 100% progress value must never display 107% because its container bounces; a decorative badge may still overshoot.

## Evidence boundaries

No aesthetic recommendation here overrides the approved brief or a profile-specific decision. IBM's restraint, FCWM's punchy timing and a contemplative museum film may legitimately differ. The manual procedures are exercises, not a promise that every menu, API or runtime is installed. Actual adapter acceptance requires pinned versions and output comparison.

Source access is recorded individually in source-ledger.json. Blender color evidence is an official search excerpt because the full page could not be opened. Embedded practitioner videos and source project files were not reviewed. The Adobe matte contradiction is retained as a source-quality warning; the source's explicit table is corroborated against W3C. Historical claims elsewhere on current Adobe pages were not adopted merely because the domain is official.

The cards deliberately avoid declaring equivalence between AE parenting and DOM opacity groups, AE collapsed precomps and React nesting, camera lens parameters across coordinate systems, spring parameters across solvers, optical-flow blur and transform sampling, or video animation and accessible interactive behavior. These are separate capabilities to prove.
