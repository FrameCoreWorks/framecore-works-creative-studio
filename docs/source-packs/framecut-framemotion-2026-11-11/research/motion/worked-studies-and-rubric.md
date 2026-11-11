# FrameMotion original worked studies and evaluation rubric

Written 2026-11-11. These are original, fully specified study briefs and predicted failure cases. **No study was rendered, measured, viewer-tested or accepted in this pass.** Numeric values below are proposed fixture choices, not universal craft thresholds. They are designed to teach decisions through comparison.

A future implementation should save the brief, locked inputs, versioned project, render settings, neutral motion specification, output, selected inspection frames and a short critique. Every exercise needs at least one deliberately worse alternative and one context in which that alternative could become appropriate. See decision-cards.md for source-linked factual anchors.

## Study A — A quiet museum title

**Problem.** An exhibition needs an eight-second landscape title that lets visitors absorb a 12-word description. The accepted style is contemplative. The imported short-form rule that a quiet frame should last no longer than 0.6 seconds would undermine this brief.

**Original plan.** 1920×1080, 24 fps, 192 frames, half-open frame intervals. A licensed still photograph occupies the left 58%; title and description occupy the right. Final type is laid out before animation. Frames [0,12) establish the photograph; [12,30) reveal the title as a phrase through a simple screen-space matte; [30,48) reveal the description by line; [48,168) preserve a completely readable composition for five seconds; [168,192) fade the whole composition. No camera movement or mandatory background drift. Sound is optional and follows the approved brief; no automatic synthesized accent.

**Manual study.** Build the still layout in AE, place markers at frames 48 and 168, and preview at likely viewing distance. Compare the proposed quiet hold against a variant with a perpetual 2% scale drift. Use the drift only if it strengthens the viewing experience and preserves reading.

**Neutral-to-code bridge.** The text contract records phrase/line units and a five-second readable interval. The composition has explicit semantic anchors. The adapter uses deterministic visibility and matte coverage, then clamps the post-reveal state. A low motion-activity measurement during the hold is expected; it cannot fail the shot automatically.

**Proposed checks.** The description is fully visible for frames 48–167; all fonts and line breaks match the approved layout; the export contains 192 picture frames; the delivered file plays through the final fade. In a first-view review, the viewer should be able to state the exhibition subject and read the description without chasing moving text.

**Counterexamples and revision.** A noisy festival screen may need a stronger arrival and shorter description. That changes the brief, not the underlying truth of the quiet version. If reading fails, reduce content or lengthen the hold before decorating the background. A user may explicitly authorize a one-shot delivery; internal checks still occur, while no unrequested preview approval is inserted.

**Teaching value.** M01, M09, M10, M11 and M18. It tests whether the agent can reject a contextual imported default for a reason.

## Study B — A product lid with a trustworthy hinge

**Problem.** A six-second product explanation must show that a lid opens from its left edge, while its feature label remains easy to read. A single flat source image has no trustworthy unseen inner surface.

**Original plan.** 1080×1080, 30 fps, 180 frames. Use original geometric proxy shapes, not borrowed product art, for the test. Body occupies x=270–810 and y=330–750. The lid's local hinge is its left boundary. Frames [0,24) establish the closed object; [24,54) open the lid to the authored angle; [54,114) hold the explanation; [114,144) close; [144,180) resolve. Label stays in screen space. The camera remains fixed for the first comparison.

**Manual study.** In AE, set the anchor at the hinge before animating. Parent the lid transform to the body controller. Move the body controller away from the origin and repeat the opening. Test its opacity separately to reveal the fact that parenting and a composited opacity group are different operations. If real depth or unseen surfaces are required, author geometry in a supported engine after checking the engine lock and scope.

**Neutral-to-code bridge.** Lid geometry, hinge pivot and parent transform are explicit. Compose local and parent transforms in the declared order; keep caption placement outside the object's transform tree. A fade is a separate authored operation. A CSS perspective mockup may communicate a diagram but is not claimed to reproduce a physical product render.

**Proposed checks.** In the proxy, the projected hinge point should move by no more than the chosen one-pixel tolerance during rotation when the body is stationary. When the body moves, the hinge follows that parent movement exactly within tolerance. The label remains horizontal and within its safe region. The intended inner face must never be fabricated by stretching an exterior photograph. Inspect occlusion and the moment of contact during closure.

**Counterexamples and revision.** An illustrated paper flap could deliberately bend and overlap. A rigid metal lid should not inherit that follow-through. If the opening feels wrong, diagnose pivot, geometry and timing before adding blur or a camera swoop. A locked Canvas route cannot silently become Blender because the word “realistic” appears in feedback.

**Teaching value.** M06, M07, M08, M13 and M17. It exposes coordinate, inheritance and material assumptions.

## Study C — An honest animated percentage

**Problem.** A dashboard explainer shows progress rising to 100%. The art direction allows a playful arrival, but the data must never imply more than 100%.

**Original plan.** 1600×900, 60 fps, 360 frames. A bar and numeric label represent the same bounded value. Frames [0,30) establish context; [30,150) move from 0 to 100; [150,300) hold the final claim; [300,360) show a concise explanation. A separate decorative frame may elastically settle during [150,180). The actual data, bar length and number remain within [0,100].

**Manual study.** Create separate AE controls for the factual quantity and decorative scale. Inspect the value graph beyond both animation boundaries. Compare a variant that springs the data itself against one that springs only the surrounding graphic. Ask which version communicates the final value without implying a temporary overrun.

**Neutral-to-code bridge.** The quantity is bounded and uses a monotonic authored progress function. The visible integer is derived from that same quantity with an explicit rounding policy. A frame-based adapter specifies both interpolation boundary modes. The installed Remotion audit already exposed the wrong single extrapolate option; the future fixture must retain that failure mode. Decorative spring parameters are not copied numerically from an AE expression.

**Proposed checks.** Evaluate frames -1, 0, 29, 30, 149, 150, 179, 300 and 360, plus all delivered frames. Quantity never leaves its domain; label and bar agree under the chosen rounding rule; frame 150 is exactly the authored final value. Shuffle evaluation order to catch state accumulation. Inspect whether the decorative settle still looks like the bar itself is exceeding its limit.

**Counterexamples and revision.** A chart depicting an actual overshoot should show it truthfully. A value that genuinely decreases cannot be forced into a monotonic curve for neatness. If the bar feels dull, change staging or the surrounding illustration before falsifying the metric.

**Teaching value.** M04, M06, M15 and M20. It separates expressive properties from factual channels.

## Study D — One story across three formats

**Problem.** A 12-second explanation compares “before” and “after” states and identifies two differences. It must work in 1920×1080, 1080×1080 and 1080×1920. Simply cropping the wide version loses the second state.

**Original plan.** 30 fps, 360 frames in every variant. [0,45) establishes the question; [45,105) reveals before; [105,165) reveals after; [165,285) presents the two differences; [285,360) resolves. In landscape, states are side by side with a shared baseline. In square, states occupy upper/lower regions with shorter labels. In portrait, the states appear sequentially in the same focal region, and small retained thumbnails provide context during comparison. The copy may wrap differently; its factual content is unchanged.

**Manual study.** Make three AE compositions with independent layouts and common semantic timing markers. Draw the focal regions at the transition from before to after. Compare the portrait sequential version against a squeezed side-by-side version. Review at actual phone display size, not only a large desktop preview.

**Neutral-to-code bridge.** Semantic slots are question, before, after, difference A, difference B and resolution. Each profile maps slots to layout and motion endpoints. Shared timing does not mean shared coordinates. Protected reading intervals may force a copy reduction or a longer version; the adapter reports that conflict instead of shrinking text below the approved threshold.

**Proposed checks.** Every factual slot exists in all three variants; required labels are neither clipped nor obscured; no motion ends at off-canvas coordinates inherited from landscape. The viewer can identify both differences after one normal-speed viewing. Check eye-trace independently after reflow. Preserve per-variant approval or an explicit waiver; approval of the wide layout does not automatically certify the portrait composition.

**Counterexamples and revision.** A film shot with irreplaceable staging may warrant approved letterboxing. A quick social teaser may intentionally omit detail, but that is a different content variant requiring explicit scope. Do not call it lossless adaptation.

**Teaching value.** M02, M09, M10 and M18. It tests whether format adaptation preserves meaning rather than only pixel bounds.

## Study E — A web diagram with a stable alternative

**Problem.** An interactive product diagram expands a layered assembly on activation. Motion helps explain relationships, but some users prefer less movement. The information must survive both modes.

**Original plan.** Wide layout at 1280×720 and narrow layout at 390×844. A button labeled “Show layers” reveals the same three layer names and relationship arrows. Normal mode uses a proposed 450 ms expansion with a short overlap between parts. Reduced-motion mode changes directly to a stable exploded diagram without large travel. There is no automatic loop. A collapse control preserves access to the description and retains sensible focus.

**Manual study.** Build closed and open still states before animating. Review the reduced-motion state on its own: can a reader explain the assembly without seeing the transition? Then animate only the relationship that benefits from movement.

**Neutral-to-code bridge.** Application state is separate from animation progress. Both modes reach the same information state. Preference changes during a transition resolve to a valid state without leaving hidden content or stale hit targets. A GSAP timeline may animate the presentation, but callbacks are not the only source of state truth. SVG or DOM labeling remains available independently of the animation.

**Proposed checks.** Test keyboard activation, repeated activation, reverse transition, preference changes before and during motion, narrow-screen layout and focus retention. Confirm the three labels exist and are accessible in both modes. If an autoplay variant is later added, separately evaluate its applicable pause/stop/hide obligations. No full WCAG compliance claim follows from passing this exercise.

**Counterexamples and revision.** A lesson demonstrating oscillation may need motion to teach its subject, with a documented essential-motion rationale and suitable controls. An ornamental parallax background does not inherit that rationale. A 1 ms version of the same sweeping movement is not automatically a thoughtful alternative.

**Teaching value.** M01, M07, M15, M18 and M19. It tests semantic equivalence across motion preferences rather than visual sameness.

## Proposed evaluation rubric

Evaluate in two stages. An attractive result cannot compensate for a broken content, rights, delivery or accessibility contract. Conversely, a technically valid render does not establish good craft.

### Stage 1 — Contract checks with evidence

| Check | Evidence required | Failure handling |
|---|---|---|
| Approved intent and revision scope | Brief, engine/profile locks, output requirements, approval or explicit revision-bound waiver | Stop unauthorized changes; preserve internal QA even under a one-shot waiver |
| Source and rights | Asset/font provenance, permissions, required notices, source-to-output mapping | Unknown redistribution rights remain unknown; do not bundle by assumption |
| Picture timeline | Decoded picture duration/frame count, not only container duration; first/last-frame inspection | Detect short video hidden by long audio |
| Layout and content | Exact dimensions, visible text, actual fonts, per-format semantic slot checks | Unsupported format or missing content is not PASS |
| Timing and values | Readable intervals, bounds, boundary frames, rational frame/time arithmetic | Fail broken locks or factual values |
| Transparency and color | Reimported output over test backgrounds, interpretation/transform metadata | Fail unintended fringes, flattening or missing alpha |
| Reproducibility | Pinned inputs/versions; selected frames in shuffled evaluation order | Record tolerance and unexplained differences |
| Web motion behavior | Preference/control/focus scenarios applicable to the actual design | Scope the result; do not extrapolate to complete conformance |
| Export readiness | Real decode/playback in a suitable independent reader | An existing file or a successful process exit is insufficient |

Exact thresholds belong to the project or fixture. A one-pixel pivot tolerance in Study B is a test choice, not a universal professional standard. Unknown, not run, unsupported and not applicable must remain distinct states. A skipped check requires a nonempty reason and its practical consequence.

### Stage 2 — Perceptual review

Score each applicable dimension 0–4: 0 contradicts the brief; 1 repeatedly obstructs understanding; 2 workable with a clear defect; 3 clear and intentional; 4 particularly effective for this brief. Scores are reviewer observations, not scientific measurements.

| Dimension | Review question | Useful evidence |
|---|---|---|
| Hierarchy | Did the intended subject or event attract attention at the right time? | First-view account before explanation |
| Comprehension | Could the viewer recover the intended message? | Retelling or task response, with audience/context recorded |
| Timing | Did preparation, action and recovery feel proportionate to the idea? | Normal-speed playback plus specific frame/time notes |
| Material and causality | Did motion fit attachment, weight, contact and stylization? | Contact/settling comparisons and the declared material hypothesis |
| Typography | Did choreography preserve language and reading? | Actual text/font/script at delivery size |
| Continuity | Did transitions help or deliberately redirect attention? | A/B comparison and stated narrative purpose |
| Restraint and emphasis | Did each added effect earn its place? | Minimal versus embellished comparison |
| Adaptation | Did each format and preference mode preserve the message? | Independent review per variant |

Do not average away a critical defect. Name the one or two changes most likely to improve the stated intent; change one causal factor at a time where practical. Stop when the agreed standard is met. A compulsory number of polish rounds is not evidence of quality. If reviewers disagree, retain their reasons and the audience/task assumptions rather than forcing a universal taste rule.

## Future evidence package naming

Proposed, not created: each study gets brief.md, neutral-spec.json, manual-notes.md, adapter-notes.md, versions.json, render-manifest.json, checks.json, critique.md and licensed-or-original fixture assets. Those belong in an eventual implementation repository only after implementation is authorized. This research directory contains no executable renderer, generated media or package manifest.
