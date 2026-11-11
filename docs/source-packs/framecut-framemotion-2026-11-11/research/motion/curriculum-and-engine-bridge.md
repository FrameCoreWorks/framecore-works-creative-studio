# FrameMotion learning programme and implementation bridge

Research planning evidence, 2026-11-11. This programme extends the imported FCWM workshop. It is not a replacement for it, a promise of senior mastery, or authorization to build or publish a plugin. The research completed now is the source ledger, twenty decision cards and five original study designs. The practice, render comparisons and expert evaluation below remain **NOT RUN**.

## What has been learned and what still needs evidence

The newly verified material adds precise distinctions that broad style recipes often omit: temporal versus spatial interpolation; material-specific settling; parent transforms versus opacity; compositing order versus organisational nesting; alpha versus luminance coverage; temporal sampling versus optical-flow blur; working color versus display transforms; camera geometry versus a generic scale animation; semantic state versus animation progress.

The imported FCWM archive contributes situated practice: observed user reactions, concrete pacing corrections, preferred sound/engine routes, successful one-shot exceptions, and practical production lessons. Those observations are valuable evidence about those projects. They do not establish universal audience behavior, redistribution rights, current platform limits or tool API truth. The extraction map preserves their provenance and distinguishes inventory from full reading.

The twenty cards are a starting corpus of decisions, not complete motion-design knowledge. Character acting, advanced typography/shaping, simulation, detailed sound-image rhythm, color-critical HDR delivery, complex 3D/material work, procedural geometry, broadcast standards and export-runtime restrictions need separate deeper study. None should be advertised as mastered because an index mentions it.

## Six-stage curriculum with observable exit criteria

| Stage | Practice and source work | Evidence required to advance |
|---|---|---|
| 1. Seeing and describing | Annotate focal regions, key poses, semantic beats and the reason for each move in three licensed/original references from different styles. Compare restrained, energetic and contemplative work. Use M01–M05. | A description that predicts what the viewer should notice, plus a counterexample to each proposed rule; no unsupported “premium” labels |
| 2. Timing and material | Recreate simple movements manually before coding. Vary only one factor: path, speed, pivot, damping, overlap or hold. Use M03–M08 and Study B. | Minimal A/B studies, a graph or frame-position analysis, and a critique explaining why a variant fits a specified material or narrative |
| 3. Language and attention | Compare phrase/word/character treatment, quiet holds and focal handoffs. Use real copy and representative writing systems. Use Studies A and D. | Normal-speed comprehension observations, text integrity checks and a reasoned rejection of at least one attractive but unreadable version |
| 4. Compositing and image formation | Build tiny truth-table fixtures for mattes, alpha, nesting, sampling and color. Verify the same small scene through the intended export/reimport path. Use M11–M17. | Numeric checks where appropriate, inspected images, pinned versions and explicit failed equivalences |
| 5. Authoring systems and adaptation | Implement only the required engine routes, then compare wide/square/portrait and interactive/reduced-motion variants. Use Studies C–E. | Arbitrary-time reproducibility, per-format semantic checks and accessible-state/control evidence, with unsupported routes reported honestly |
| 6. Transfer and critique | Give the agent a new brief that conflicts with a familiar profile default. Require it to choose, justify and demonstrate a different treatment. Obtain independent practitioner critique where available and authorized. | The agent changes its decision for the right reason, preserves locks/rights, and revises the output from concrete critique rather than adding generic polish |

No fixed number of practice rounds proves competence. Use a held-out brief to check transfer: for example, a quiet instructional loop after energetic social studies, or a rigid mechanism after elastic badge studies. A student or agent that only reproduces the training style has not generalized.

## Source-validation workflow

1. Record the claim before searching: technical behavior, aesthetic judgment, historical user preference, measured observation or proposal.
2. Prefer the original creator, official documentation or original research for that claim. A practitioner's explanation of their own work can establish intent and technique; it does not by itself prove universal perception.
3. Read the relevant section and retain URL, title, retrieval date, version/context, supported claim and uncertainty. Do not label a search excerpt as a fully read manual.
4. Compare conflicts instead of voting by domain authority. The Adobe matte page's introductory wording conflicts with its own table; corroboration matters. The current Adobe import page contains historical material, so a current URL is not evidence that every assertion is current.
5. For technical equivalence, make a minimal fixture in the installed version. Documentation supports the proposed test, not a claim that the local renderer passed.
6. For aesthetic judgments, use a target audience/task and counterexample. Preserve disagreement with context instead of converting a preference to UNIVERSAL.
7. For rights and licensing, retain the actual terms applying to the specific asset/version. A tutorial link or a working download is not a redistribution license.
8. Promote evidence in stages: IMPORTED_UNVERIFIED → SOURCE_CHECKED → LOCALLY_REPRODUCED → OUTPUT_REVIEWED. A failed or unsupported case remains visible; promotion is not automatic.

Future research should deliberately seek disconfirming examples: a successful long hold, an effective hard cut, restrained movement with no overshoot, expressive simultaneous action, a flat composition that outperforms 3D, or a useful stylized violation of physical behavior. Each prevents a contextual recommendation from hardening into a simplistic rule.

## Engine bridge: what can be mapped and what needs proof

| Manual concept | Proposed neutral representation | Candidate implementation | Equivalence limit and future evidence |
|---|---|---|---|
| AE temporal curve | Value/time relation with boundary behavior | Canvas evaluator; GSAP curve; Remotion interpolation | Compare sampled position/velocity, not ease names |
| AE spatial path | Geometry plus travel parameter | Canvas/SVG path or engine trajectory | Parameter progress is not automatically distance progress |
| Text animator | Shaped text plus semantic selection units | DOM/SVG/Canvas or native text engine | Wrapping, kerning, ligatures and script behavior require real-font fixtures |
| Parenting/nulls | Transform graph plus separate opacity policy | Matrix graph, DOM transform groups, three.js/Blender objects | AE parent opacity is not inherited; group compositing may differ |
| Precomp/collapse | Explicit render/effect graph and flatten boundaries | Offscreen surfaces or render nodes | Framework component nesting is not a substitute for render-order evidence |
| Track matte | Coverage source/mode/space/inversion | Mask, clipping or compositing operation | Alpha/luminance semantics and transformed bounds differ by adapter |
| Motion blur | Exposure interval and temporal sample policy | Supported renderer integration or explicit subframe evaluation | Static blur, flow estimation and geometric sampling are different operations |
| Color-managed comp | Input/working/view/output interpretation | Engine color pipeline with declared transforms | Hex equality and matched screenshots alone do not establish pipeline parity |
| 2.5D camera | Pose, projection, sensor/FOV assumptions and depth | three.js, Blender or supported 2.5D engine | Match geometry and framing before comparing motion; no unseen geometry from flat images |
| Interactive motion | Semantic state plus optional transition | DOM/SVG/GSAP or another tested web runtime | Video timing does not provide focus, input or accessibility behavior |
| Final export | Explicit format, codec, alpha/color and playback requirements | Capability-checked export route | File extension and process success do not certify a valid deliverable |

The official Blender camera API search result additionally exposes focal length, sensor dimensions, sensor fit, orthographic scale and camera shift as separate properties. That supports a richer mapping than copying one lens number. The full API page could not be fetched, and the installed API was not executed here; property support and coordinate conventions still need a pinned-version test. [Blender Camera API](https://docs.blender.org/api/current/bpy.types.Camera.html).

Canvas motion-reel and HyperFrames remain the accepted default routes in the imported user decisions; Remotion remains optional with its license consideration. This is a preference/routing record, not proof that one renderer can reproduce every card. A locked route requires explicit handling when a needed capability is absent. Blender is a candidate for appropriate geometry and physical scene work, not an automatic replacement for any request using the word “realistic”.

## Actionable future tasks and exact proposed evidence names

These names describe future work and do not create implementation files now.

| Task | Proposed evidence or test | Acceptance |
|---|---|---|
| Preserve knowledge retrieval | tests/knowledge_retrieval_motion_test.py; traces for quiet title, rigid mechanism, matte reveal and reduced-motion web | Required card and relevant profile source are actually consulted; inventory presence alone fails |
| Prove graph semantics | tests/curve_path_boundary_test.py | Independent path/timing changes, intended joins, before/after bounds and correct clamp options |
| Prove attachment semantics | tests/transform_parent_opacity_test.py | Non-origin pivot, parent scale/rotation, screen-space caption and explicit opacity behavior |
| Prove language handling | tests/text_semantics_reading_interval_test.py | Real font/script samples, protected readable interval and infeasible-retime reporting |
| Prove compositing semantics | tests/matte_alpha_render_order_test.py | Coverage truth table, export/reimport alpha, and deliberately different effect/group orders |
| Prove sampling and color | tests/blur_color_pipeline_test.py | Documented sample convergence, controlled patches and pinned transforms; unsupported paths remain unsupported |
| Prove reproducibility | tests/arbitrary_time_render_test.py | Forward/reverse/shuffled-frame agreement under declared tolerances |
| Prove adaptation and web behavior | tests/format_semantics_reduced_motion_test.py | Content preserved per target and preference state; no false full-conformance claim |
| Preserve audited failures | tests/motion_audit_regressions_test.py | Wrong clamp, container/picture mismatch, stale hash/spec, incomplete dimensions, blank skip reason, alpha false results and CSS shorthand crash remain caught |
| Demonstrate craft transfer | studies/A–E with critique records; held-out-study/ | Output reviewed against intent and counterexample; technical PASS alone is insufficient |

Implementation test names are proposals for the eventual owner, not existing source tests. The original local edition keeps exact private mappings and prior audit evidence outside this public packet. See [the portable extraction summary](../../EXTRACTION-SUMMARY.md) and [public owner inventory](../../PUBLIC-OWNER-INVENTORY.json) for shipped paths, baseline hashes and regression concerns. The extraction plan must also establish dependency closure, licenses, notices, fonts, fixtures and standalone behavior before release.

## Boundaries of the completed research

Completed: read-only extraction evidence; primary-source browsing; twenty source-linked decision cards; five original study briefs; measurable and perceptual rubric; explicit uncertainty and a future learning programme. Not completed: new motion renders, AE operation, API runtime comparisons, practitioner interviews, embedded-video review, audience testing, licensing certification, a shipping skill or implementation repository. Existing audit tests retain their original scope and are not relabeled as validation of these new studies.
