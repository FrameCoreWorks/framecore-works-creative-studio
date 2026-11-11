# FrameMotion: advanced compositing decision cards

Research supplement, 2026-11-11. These are proposed knowledge and review requirements for planning a standalone plugin, not an implemented renderer or plugin. Studio `workflow-orchestrator` and `research-evidence` supplied the research method. This supplement does not replace the host's full extraction inventory.

Evidence labels: D = directly read primary documentation; P = original practitioner account read; S = original synthesis/proposed procedure; C = locally checked calculation. No AE/Blender UI operation, render, export, browser-font test, or creator video playback was performed. Mathematical verification establishes the stated model, not app parity or professional mastery.

Acceptance scope: eight decisions, each with intent, manual workflow, agent mapping, limitation, negative case and observable review; original numerical examples; source provenance and contrary evidence. Links S01–S13 resolve in the source ledger below. Conditions and examples are deliberately bounded.

## 1. A pivot is not an absolute position

Intent: keep a logo fixed while relocating its rotation pivot; attach a label to a moving parent.

Human AE workflow: D: inspect Anchor Point and Position separately; use the anchor tool for pivot changes and a null for a common transform. Parenting makes child transforms parent-relative and does not transfer opacity. Expression point conversions distinguish layer, composition and world coordinates. [S01], [S02]

Agent mapping: S: declare coordinate basis, units, pixel aspect, pivot and parent for each object. For the bounded 2D case, compose `M_parent × T(position) × R × S × T(-anchor)`. Preserve the world matrix when reparenting by solving the new local matrix against the inverse parent. Mark singular transforms as unsolvable without a policy.

Non-equivalence: a CSS wrapper's opacity and layout behavior are not AE parenting. A 3D world coordinate is not already a screen pixel. Negative scales and skew need explicit decomposition rules.

Negative case: copying the parent's position onto the child while retaining a local offset applies the offset in the wrong basis; adjusting the anchor alone makes the artwork jump.

Output review: proposed: compare a fiducial before/after pivot relocation, rotate through 0/90/180 degrees, and fade the parent. Check both geometry and intended opacity inheritance. Example A supplies a numeric fixture.

## 2. A precomposition is a rendering boundary

Intent: preserve a logo's detail while retaining a particular blur, matte and blend interaction.

Human AE workflow: D: decide whether nesting should flatten the group. Collapse can combine nested transforms; continuous rasterization changes transform/effect ordering. A mask, effect or layer style on a collapsed precomp can restore an isolated rendering stage; an internal adjustment layer can force flattening and cropping. [S03]

Agent mapping: S: represent both transform nodes and raster/composite nodes. Mark the resolution, clip region, backdrop and filter space at every raster boundary. A transform-only group is insufficient. Treat the graph, rather than the layer names, as the portable knowledge.

Non-equivalence: CSS isolation has defined backdrop behavior, but is not an implementation of AE Collapse Transformations. Default grouping and isolated blending are distinct in W3C compositing. [S10] Chris Zwar explicitly bounds his render-order explanation to Classic 3D; do not transfer it wholesale to another renderer. [S13]

Negative case: a 20-pixel blur before a 4× enlargement produces a different visible radius from a 20-pixel blur afterward. Enabling collapse to cure softness may change the approved appearance.

Output review: proposed: compare blurred edges, matte extents, nested blend behavior and crossings with outside 3D layers at maximum scale. Record which boundary caused each difference.

## 3. Transparent edges have a color representation

Intent: deliver a soft-edged logo that composites cleanly on changing backgrounds.

Human AE workflow: D: inspect alpha interpretation and the matte color through Interpret Footage; judge edges over more than the preview's black background. Straight and premultiplied files can share alpha values but differ in RGB. Incorrect interpretation can retain a fringe. [S04]

Agent mapping: S: retain `alpha_mode`, color space and any matte information with the asset. Use one explicit representation at each processing boundary. For black-associated data, recover straight color as `rgb/alpha` only where alpha is meaningfully nonzero; use an explicit zero-alpha policy. Premultiply again where required. Nonblack matte removal needs the corresponding matte model, not blind division.

Non-equivalence: alpha correctness does not establish that the RGB transfer function is correct. Source-over combines premultiplied contributions; an export setting cannot repair RGB already damaged upstream. [S10]

Negative case: multiplying associated RGB by alpha twice darkens edges. Treating unassociated RGB as already associated can brighten edges or exceed valid display values.

Output review: proposed: composite on dark, light and saturated backgrounds; inspect soft edges and zero-alpha pixels; reimport the exported file under its declared interpretation. Example B predicts specific wrong values. No such round trip was executed here.

## 4. Linear working data, display preview and output conversion are separate

Intent: blend illuminated graphics predictably and preserve the approved appearance through delivery.

Human AE workflow: D: establish input interpretation and project working space before judging color; decide on linearization early. AE distinguishes linearizing the working space from using gamma 1.0 only for layer blending. An output profile specifies the working-to-output conversion; display/output simulation is another stage. [S05]

Agent mapping: S: preserve a color-transform graph: source encoding → working encoding/primaries → operations → delivery transform, with a separate preview branch. Record alpha handling alongside it. Numeric RGB equality is meaningful only when both representations match.

Non-equivalence: the same hex string does not prove equal light or appearance. A browser screenshot is not evidence that an HDR or scene-referred pipeline matches AE. W3C's sRGB transfer equations support the bounded SDR arithmetic in Example B, not every application's blending defaults. [S11]

Negative case: baking a display transform into an intermediate and then applying it again on delivery; or changing linearization after color choices and expecting identical graphics.

Output review: proposed: compare tagged reference patches, soft blends and highlights in the intended playback path; reimport the exported file. Distinguish a numerical conversion error from an uncalibrated display difference. Blender-specific mapping remains Unknown; see access gap G01.

## 5. Motion blur is a time interval, not a single blurred image

Intent: make fast graphic movement readable without changing its intended timing.

Human AE workflow: D: enable the relevant layer and composition blur controls, then choose shutter angle, phase and sampling. AE's layer switch does not add blur to movement already inside footage; pixel-motion estimation is a separate operation. [S06]

Agent mapping: S: evaluate and composite the complete scene at each subframe across the exposure interval, then integrate those scene images using a declared weighting in the intended color representation. Accumulating layers separately before compositing requires explicit restrictions on time-varying alpha, occlusion and background; it is not a general substitute. Declare how samples outside a clip are resolved and whether random state is deterministic. The original calculation below uses uniform exposure and constant velocity, not AE's actual adaptive sampler.

Non-equivalence: a spatial blur cannot reproduce arbitrary acceleration, rotation, occlusion or changing geometry. Optical flow reconstructs motion from frames; it is not the same evidence as a known animation trajectory.

Negative case: integer-frame-only evaluation makes additional samples identical. A centered shutter crossing a scene cut contaminates the first frame if the sampler simply reads the previous shot.

Output review: proposed: inspect the fastest translation, rotation and occlusion, plus clip boundaries; compare shutter phase against tracked reference points. Check for stepping and double edges at delivery size. Do not judge sampling solely from one stationary frame.

## 6. A camera-facing card is not a solid object

Intent: choose the simplest scene representation that supports the required camera movement.

Human AE workflow: D: a conventional layer switched to 3D remains a plane with additional spatial controls; geometry options can supply depth for supported content. Inspect the selected renderer and actual object type before promising volume. [S07]

Agent mapping: S: use a plane and a camera for a photographed card; use actual geometry when the move reveals sides, thickness or changing silhouette. Store camera projection, focal units, sensor assumptions, handedness, near/far conventions and output pixel aspect. Exported camera numbers need a coordinate conversion, not merely matching field names.

Non-equivalence: parallax establishes depth relationships but does not invent a photographed object's hidden surfaces. A screen-space billboard, world-oriented plane and mesh produce different silhouettes under orbit. This is an original modeling distinction, not a verified Blender mapping.

Negative case: a product card works for a modest lateral move, then becomes implausibly thin as the camera passes its edge. Replacing that failure with a scale animation preserves neither perspective nor occlusion.

Output review: proposed: review front, three-quarter and near-edge views; inspect intersections, contact shadows and occlusion. Example C's pinhole calculation checks a necessary perspective relation, not a full lens match. Select the representation using the most revealing approved shot.

## 7. A font name is not a reproducible text layout

Intent: preserve a title's spacing and silhouette across an AE design and agent-rendered variants.

Human AE workflow: D: distinguish metrics, optical and manual kerning; tracking and manual pair adjustments can accumulate. Preserve leading, text stroke/fill order and the actual face selection. [S08]

Agent mapping: S: bind a font file identity and axis settings, language, shaping features, kerning policy, line breaks, baseline, leading and per-span styling. Measure rendered glyph bounds after loading fonts, then position the title. Record whether editability or an exact approved outline takes priority. A temporary outline comparison can diagnose differences without replacing the editable source.

Non-equivalence: an AE optical-kerning decision does not directly specify CSS pair adjustments. CSS font synthesis controls exist, but preventing synthesis does not prove the right face loaded or that rasterization matches. [S12]

Negative case: a substitute face passes a family-name check while a Polish diacritic clips; a browser fallback changes a line break halfway through captured output.

Output review: proposed: compare Polish diacritics, ligatures, tight pairs, multiline text and extreme variable axes at actual delivery size. Check frozen loading state and exported frames, not just a DOM measurement. Measure glyph edges/bounds separately from overall title position; antialiasing tolerance needs an agreed reference.

## 8. Duration and aspect revisions change different dependencies

Intent: shorten a graphic and adapt its canvas while protecting the entrance, exit and essential copy.

Human AE workflow: D: use protected time regions for fixed-duration animation. Update source markers explicitly when needed; nested markers do not automatically refresh after source changes. Adobe documents audio and some 3D/CINEWARE caveats. [S09]

Agent mapping: S: separate entrance, elastic content/hold and exit; use a piecewise time mapping with a declared minimum duration. Solve layout independently using margins, text reflow, focal point and overlap constraints. Keep both full source and variant dependency records.

Non-equivalence: protected timing does not decide what content to remove, reframe a shot or make longer copy readable. Scaling the whole canvas is not layout adaptation. A time warp should not silently stretch narration, springs or beat synchronization.

Negative case: requesting a two-second version with 1.25 seconds of entrance and 1 second of exit leaves negative elastic time. The correct response is a creative tradeoff, not an inverted time segment.

Output review: proposed: inspect segment boundaries, complete entrance/exit motion, reading time, audio synchronization and every changed text wrap. Validate all accepted aspect ratios separately. Example D gives both a valid duration reduction and an impossible case.

## Original worked examples

### A. Relocate a pivot without moving a point (C)

Hypothetical 2D logo: 400×200 local pixels; anchor `A=(200,100)`; position `P=(960,540)`; scale `S=(1.5,0.75)`; rotation 30°. Coordinates use x-right/y-down and the numeric matrix `R=[[cos,-sin],[sin,cos]]`, which appears clockwise on that display. There is no parent, skew, camera or pixel-aspect correction.

The declared model is `q=P+R S(p-A)`. Choose new anchor `A'=(0,100)`. To keep every point fixed, solve `P'=P+R S(A'-A)`.

`A'-A=(-200,0)`; scaled difference `(-300,0)`; rotated difference `(-259.807621,-150)`; thus `P'=(700.192379,390)`.

For the local test point `p=(400,100)`, the original screen position is `(1219.807621,690)`. Under the new anchor and compensated position it remains `(1219.807621,690)`. Changing only the anchor yields `(1479.615242,840)`, a jump of `(259.807621,150)`.

Decision: compensate in the transformed basis, then pass the local transform through the parent chain. The fixture proves this affine equation. It does not prove that an AE anchor gesture, CSS transform-origin or a particular scene library exposes identical parameters.

### B. Diagnose an edge and a transfer-function error separately (C)

Hypothetical edge in linear-light RGB: straight foreground `F=(0.8,0.2,0.1)`, alpha `a=0.25`; opaque background `B=(0.1,0.3,0.5)`.

The stored black-associated foreground is `Fp=aF=(0.2,0.05,0.025)`. Correct source-over is `Fp+(1-a)B=(0.275,0.275,0.4)` with alpha 1. This is original arithmetic using the source-over mechanism in [S10].

If an importer mistakenly treats `Fp` as straight and multiplies it again, the result becomes `(0.125,0.2375,0.38125)`. If straight `F` is instead read as already associated, the result is `(0.875,0.425,0.475)`. Thus changing alpha metadata is only justified when it matches the data; it is not a generic visual correction.

Now isolate color encoding using a different test: 50% white over opaque black. Linear blending yields linear `(0.5,0.5,0.5)`; applying the sRGB transfer function gives encoded channels `0.735356983`, approximately code value 188 in full-range 8-bit. Averaging the already encoded endpoints gives 0.5, approximately 128; decoding 0.5 yields only `0.214041140` linear light. Transfer equations follow [S11]. Alpha is not gamma-encoded in this fixture.

Decision: first establish associated versus unassociated data, then establish the working encoding. A visually dark fringe can have either cause. These are analytic fixtures, not measured codec samples; quantization, subsampling and display transforms are excluded.

### C. Exposure and perspective mini-fixtures (C)

At 30 fps with shutter angle 180° and phase −90°, exposure lasts `180/(360×30)=1/60 s`, centered on the frame: `t±1/120 s`. A point traveling 900 px/s spans 15 px during exposure. At 24 fps with the same angle it spans 18.75 px; keeping the same angle does not preserve pixel blur length. These are constant-velocity, uniform-shutter deductions from [S06], not measured AE sampling.

For an abstract pinhole camera, projected width is `f_px×world_width/depth`. With `f_px=1200`, width 200 units and depth 1000, width is 240 px; at depth 1500 it is 160 px. A lateral 100-unit camera shift causes projected displacements of 120 and 80 px respectively for the two depths. The 40-px difference is parallax. This self-contained model excludes lens distortion and does not map millimeters to any application's camera without sensor and fit conventions.

### D. Protect animation duration; redesign spatial layout (C)

Original: 300 frames at 30 fps, entrance 30 frames and exit 24. Elastic middle =246. New total =180; remaining middle =126, so its output-time scale is `126/246=0.512195122`. Mapping output frame coordinate `n` to source coordinate:

- `0≤n<30`: `u=n`.
- `30≤n<156`: `u=30+(n-30)×246/126`.
- `156≤n≤180`: `u=276+(n-156)`.

Boundaries map `30→30`, `156→276`, `180→300`; actual sampled output frames are 0–179. A 48-frame request is impossible with these 54 protected frames: reject or renegotiate protection. These are original timing fixtures, not a claim to reproduce every AE responsive-time edge case.

Spatial revision: an original 1920-wide design has 96-pixel margins (5%). A 1080-wide variant with the same percentage margins has 54-pixel margins and 972 usable pixels. A hypothetical measured title is 1100 pixels wide at the approved type size; uniform fitting would require `972/1100=0.883636364` scale, about 11.64% smaller type. That arithmetic does not approve the reduction. A deliberate line break may preserve hierarchy better, and changes its animation bounds. No font was actually measured; 1100 is the stated hypothetical input.

## Source ledger

All sources accessed 2026-11-11. Adobe dates are page-reported update dates, not proof of a particular installed version. URLs were opened and relevant body passages read. W3C draft status is retained; no draft is treated as proof of browser conformance. Brief summaries and original derived examples are used instead of copied tutorials.

| ID / source | Publication or update | Evidence and bounded claim | Where inspected |
|---|---|---|---|
| S01 [Adobe: Layer properties](https://helpx.adobe.com/after-effects/using/layer-properties.html) | 2026-01-21 | D, vendor manual: pivot/transform semantics; parenting excludes opacity | Anchor point; Parent and child layers |
| S02 [Adobe: Expression language reference](https://helpx.adobe.com/after-effects/using/expression-language-reference.html) | 2026-05-05 | D, vendor manual: point/vector and layer/comp/world conversions differ | Layer space transforms, toComp/fromComp/toWorld |
| S03 [Adobe: Precomposing, nesting, and pre-rendering](https://helpx.adobe.com/after-effects/using/precomposing-nesting-pre-rendering.html) | 2026-01-21 | D, vendor manual: render order and collapse boundary conditions | Render order and collapsing transformations |
| S04 [Adobe: Importing and interpreting footage items](https://helpx.adobe.com/after-effects/using/importing-interpreting-footage-items.html) | 2026-03-27 | D, vendor manual: alpha representations and import interpretation | Alpha channel interpretation; Set alpha interpretation |
| S05 [Adobe: Color management](https://helpx.adobe.com/after-effects/using/color-management.html) | 2026-03-27 | D, vendor manual: working linearization, blend-only setting, output conversion | Linearize working space; Assign an output color profile; output simulation |
| S06 [Adobe: Assorted animation tools](https://helpx.adobe.com/after-effects/using/assorted-animation-tools.html) | 2026-05-11 | D, vendor manual: shutter interval, sampling, layer/internal-motion distinction | Motion blur; Advanced composition settings |
| S07 [Adobe: 3D layers](https://helpx.adobe.com/after-effects/using/3d-layers.html) | 2026-01-21 | D, vendor manual: planar layers versus additional geometry capabilities | 3D layers overview |
| S08 [Adobe: Formatting characters and the Character panel](https://helpx.adobe.com/after-effects/using/formatting-characters-character-panel.html) | 2025-11-21 | D, vendor manual: optical/metrics/manual spacing and stroke order | Spacing; Specify kerning; Text fills and strokes |
| S09 [Adobe: Add responsive design to your graphics](https://helpx.adobe.com/after-effects/using/responsive-design.html) | 2026-03-27 | D, vendor manual: protected regions and documented retiming caveats | Nested compositions; Export a composition with protected regions |
| S10 [W3C: Compositing and Blending Level 1](https://www.w3.org/TR/compositing-1/) | 2024-03-21 Candidate Recommendation Draft | D, primary technical specification: source-over and isolation model | §§5.1, 8.1–8.2 |
| S11 [W3C: CSS Color Module Level 4](https://www.w3.org/TR/css-color-4/) | 2026-11-03 Candidate Recommendation Draft | D, primary technical specification: sRGB and linear-sRGB conversion | §§10.2–10.3; sample conversion code |
| S12 [W3C: CSS Fonts Module Level 4](https://www.w3.org/TR/css-fonts-4/) | 2026-11-04 Working Draft | D, primary technical specification: synthesized-face controls | §2.8 font synthesis |
| S13 [Chris Zwar: Binning it – Understanding layer rendering order in After Effects](https://www.provideocoalition.com/binning-it-understanding-layer-rendering-order-in-after-effects/) | 2021-10-11 | P, original practitioner article: render-order treatment explicitly limited to Classic 3D | Article text; embedded video not watched |

## Access gaps and independent challenge

G01: Blender: the official [color-management manual](https://docs.blender.org/manual/en/latest/render/color_management.html) and [Alpha Convert manual](https://docs.blender.org/manual/en/latest/compositing/types/color/alpha_convert.html) could not be fetched by the web tool (HTTP 402). Versioned 3.3 color and 4.5 alpha routes also failed. One direct read-only request to the official 4.5 color page returned HTTP 403. No payment, alternate provider or access bypass was used. Search excerpts were treated as leads only. Therefore this supplement makes no verified AE→Blender node, color configuration or API-parity claim. Reopen the relevant official manual before adding such a mapping.

Challenges resolved by narrowing the claim: collapse is not just sharpness; parent is not a group-opacity node; linear-blend-only is not whole-pipeline linearization; internal footage motion is not layer-transform motion; protected time is not spatial responsiveness; a font family name is not exact shaping; a planar layer is not a solid. The creator account is first-hand but its embedded demonstration was not inspected, so it corroborates scope and motivation, not measured outcomes.

Remaining unknowns: actual AE/Blender versions and renderer selections; pixel-exact interoperability; all actual visual test results; font/render backend parity; output-codec tagging and round-trip behavior; recipient-specific delivery tolerances. Proposed tests require representative fixtures and visual inspection in the real production path. Documentation acquisition is not experiential mastery.

Planning consequence: S: FrameMotion needs recipes keyed by intent plus an explicit operation graph, coordinate/color/time contracts and revision tests. A catalog of effect names or a universal AE-to-CSS button translation would lose decisive behavior. The plugin should expose a bounded alternative when parity is unknown, and let the user approve the observed result.

[S01]: https://helpx.adobe.com/after-effects/using/layer-properties.html
[S02]: https://helpx.adobe.com/after-effects/using/expression-language-reference.html
[S03]: https://helpx.adobe.com/after-effects/using/precomposing-nesting-pre-rendering.html
[S04]: https://helpx.adobe.com/after-effects/using/importing-interpreting-footage-items.html
[S05]: https://helpx.adobe.com/after-effects/using/color-management.html
[S06]: https://helpx.adobe.com/after-effects/using/assorted-animation-tools.html
[S07]: https://helpx.adobe.com/after-effects/using/3d-layers.html
[S08]: https://helpx.adobe.com/after-effects/using/formatting-characters-character-panel.html
[S09]: https://helpx.adobe.com/after-effects/using/responsive-design.html
[S10]: https://www.w3.org/TR/compositing-1/
[S11]: https://www.w3.org/TR/css-color-4/
[S12]: https://www.w3.org/TR/css-fonts-4/
[S13]: https://www.provideocoalition.com/binning-it-understanding-layer-rendering-order-in-after-effects/
