# After Effects craft: think like a professional motion designer

Studio's code motion (HTML, SVG and CSS, GSAP, HyperFrames, Remotion, Canvas and PixiJS, three.js) inherits its vocabulary and its craft from After Effects. Read this before planning a motion piece, when the user uses an After Effects term, and before the final review: plan and judge the piece as an experienced After Effects designer would, then build it in code with the translation table below. It is Studio's own summary of professional practice (Adobe's After Effects guide, School of Motion, Video Copilot, Dan Ebberts' expressions, Disney's principles applied to motion, IBM Carbon and Material motion; sources at the end). Concrete starting values for curves, durations and holds stay in [motion craft](motion-craft.md); where a number here and there differ, motion craft and the user's own rules win. Numbers marked *rule of thumb* are starting points to tune by eye.

## Contents

- [The mindset](#the-mindset)
- [Working stages](#working-stages)
- [Terms and their code form](#terms-and-their-code-form)
- [Curves: the Graph Editor in code](#curves-the-graph-editor-in-code)
- [Weight: anticipation, overshoot, overlap](#weight-anticipation-overshoot-overlap)
- [Stagger and offsets](#stagger-and-offsets)
- [Holds, reading time and frames](#holds-reading-time-and-frames)
- [Effects and how they combine](#effects-and-how-they-combine)
- [Recipes by job](#recipes-by-job)
- [Camera and depth](#camera-and-depth)
- [Design in time](#design-in-time)
- [Pre-delivery check](#pre-delivery-check)
- [Beginner habits and pro habits](#beginner-habits-and-pro-habits)
- [Sources](#sources)

## The mindset

A professional does not "add animation" to a layout. They direct the viewer's eye through time. Every move has a reason (it reveals, connects, emphasises or carries the story to the next beat), every move has weight (it accelerates and decelerates like something with mass), and every beat has one lead action that everything else supports. They plan before they key (brief, concept, styleframes, animatic), block the timing coarsely, spend most of the time shaping speed in the Graph Editor, and only then add effects, motion blur, texture and sound. Motion must work in flat grey boxes before any glow is added; effects never hide weak motion.

When Studio plans a piece, write down, before any code, what a lead designer would: the beat list with one message per beat, the lead action of each beat, the motion language (curves, a duration scale, a stagger, an overshoot policy) and where the eye is at the end of each beat.

## Working stages

| Stage | What a pro does | In Studio |
| --- | --- | --- |
| Brief | Deliverables, length, platforms, ratios, message, mandatory elements, brand limits | the motion brief and copy locks |
| Concept | A visual metaphor; thumbnails | two or three different concepts, each with its named "wow" moment |
| Styleframes | A few finished stills that lock look, type, colour and the final frame | key stills or the board, shown before motion |
| Animatic | Boards timed to the voice or music with temp sound | the timed board or a still-frame preview; fix long shots here |
| Blocking | Key poses with hold or linear keys, timing only | first render of positions and timing, no easing polish |
| Curves | Every move reshaped in the speed graph | named eases from the motion language applied per move |
| Polish | Overlap, follow-through, secondary action, motion blur, texture | the second pass, then the craft critique |
| Sound | Picture and sound designed together, hits on the motion | the motion sound engine or Earshot through Toolbox, cues at frames |
| Render and QC | Frame sweep, safe areas, loudness, codecs | frame sweep with safe lines, `critique.py`, delivery checks |

Studios fix timing before final art: do not polish a scene whose timing has not been seen.

## Terms and their code form

When the user speaks After Effects, answer in their term and build its equivalent.

| After Effects | What it is | Code equivalent |
| --- | --- | --- |
| Composition | Fixed size, fps, duration, background | a fixed-size root with `overflow: hidden` and one paused master timeline (HyperFrames `data-duration`); Remotion `<Composition fps durationInFrames>` |
| Keyframe at frame f | A value at a time | `tl.to(el, {...}, f / fps)`; Remotion `interpolate(frame, [f0, f1], [v0, v1])` |
| Precomp, nesting | A comp used as a layer: groups, reuse, render order | a nested timeline and a wrapper element; Pixi `Container`; three.js `Group` |
| Null, parenting | An invisible controller whose transform children inherit | a wrapper `<div>` or `<g>` carrying the shared move; one config object drives the group |
| Anchor point | The pivot for scale and rotation, set before animating | `transform-origin` (`svgOrigin`, SVG `transform-box: fill-box`); Pixi `pivot`; an offset mesh inside a parent group |
| Separate dimensions | X and Y with their own curves | tween `x` and `y` separately with different eases |
| Hold keyframe | The value jumps at the next key | `tl.set()`; `steps()`; snapping progress |
| Roving keyframe | Even speed along a multi-point path | sample the path by arc length (GSAP MotionPath `autoRotate`, `getTotalLength`) |
| Track matte (alpha or luma) | A layer takes its transparency from another | CSS `mask-image` with `mask-mode: alpha|luminance`, `clip-path`, SVG `<mask>` (luminance) and `<clipPath>`; Pixi `mask`; canvas `destination-in` |
| Mask reveal | An animated cut-out | tween `clip-path: inset(0 100% 0 0)` to `inset(0 0 0 0)`, or `circle()`, `polygon()` |
| Trim Paths | A stroke drawn from start to end | `stroke-dasharray` and `stroke-dashoffset` from the length to 0, with `pathLength="1"`; three.js `Line2` draw range |
| Repeater | Copies with incremental transforms | a generated loop with `--i` or an index; `InstancedMesh` |
| Merge Paths | Boolean shape operations | precomputed compound paths, `fill-rule` |
| Blending modes | Screen, Add, Multiply, Overlay | `mix-blend-mode` with `isolation: isolate` on the group; canvas `globalCompositeOperation` (`screen`, `lighter`, `multiply`); three.js `AdditiveBlending` |
| Adjustment layer | Effects over everything beneath | `filter` on a top wrapper; a post-processing pass |
| Collapse transformations | Render a vector after its transforms so it stays sharp | keep vectors as SVG or redraw at the final scale; never scale a rasterised bitmap up |
| Text animator, range selector | Per-character or per-word properties with an offset | split text into characters, words or lines and tween with `stagger` |
| Expression controls, sliders | Exposed parameters on a controller | a config object, CSS custom properties, Remotion props schema |
| Essential Graphics, MOGRT | A template with editable inputs | a parameterised composition whose text, colours and durations are inputs |
| `wiggle(freq, amp)` | Organic jitter | seeded smooth noise sampled at `t * freq`, scaled by `amp` (never unseeded `Math.random()`) |
| `loopOut("cycle")` | A seamless loop | `phase = (frame % period) / period`; a finite `repeat` |
| `valueAtTime(t - d)` | Delay chains, follow-the-leader | evaluate the same function at `t - i * delay` |
| `linear()`, `ease()` remap | Tie one range to another | a clamped map function (Remotion `interpolate` with `extrapolate: "clamp"`) |
| Markers | Beat and cue points on the timeline | GSAP labels (`tl.addLabel("drop", t)`), beat frames from the music analysis |
| Posterize Time, "on twos" | Each pose held two frames | `frame = Math.floor(frame / 2) * 2` before computing |
| Motion blur | Shutter-based blur of moving layers | sub-frame accumulation: render several samples across the shutter and average (Remotion `<CameraMotionBlur>`) |
| 3D layer and camera | Depth seen through a camera | CSS 3D (`perspective`, `preserve-3d`) or three.js `PerspectiveCamera` |

**The rule underneath all of it:** After Effects evaluates every property at a time; nothing depends on the previous frame. Every visual state in code is a pure function of the frame number: seek one paused timeline, seed all randomness by element index, use finite repeats, no real-time clocks, and wait for fonts and images before the first frame.

## Curves: the Graph Editor in code

- **The speed graph is the feel.** A clean single move is one smooth hump from zero to a peak and back. Longer influence (handle length) makes the start and end slower and the middle faster. Kinks, double humps and hidden extra keys read as stutter.
- **After Effects' default Easy Ease** is about 33% influence with zero speed: `cubic-bezier(0.333, 0, 0.667, 1)`, soft and rarely what a shot needs. Professionals reshape it, commonly to 60 to 85% influence; too much on a long move floats.
- **Naming trap.** After Effects "Easy Ease In" slows the layer *into* a key, which CSS and GSAP call ease-out; "Easy Ease Out" is ease-in. Entrances decelerate (`.out`), exits accelerate (`.in`), moves between rests ease both ends (`.inOut`).
- **The pro asymmetric curve:** leave the first key quickly and land with a long in-influence (75 to 95%). In code that is the `power3.out` to `expo.out` family; [motion craft](motion-craft.md#easing-presets) has the exact presets.
- **Converting a curve** (with speeds `s_out`, `s_in` and the average speed `v = (b - a) / T`): `cubic-bezier(influence_out, influence_out * s_out / v, 1 - influence_in, 1 - influence_in * s_in / v)`. Speed 0 on both sides gives these:

| After Effects ease (influence out / in) | cubic-bezier | GSAP neighbour |
| --- | --- | --- |
| Linear | (0, 0, 1, 1) | `none` |
| 33 / 33 (default) | (0.333, 0, 0.667, 1) | between `sine.inOut` and `power1.inOut` |
| 50 / 50 | (0.5, 0, 0.5, 1) | about `power2.inOut` |
| 66 / 66 | (0.66, 0, 0.34, 1) | `power2.inOut` to `power3.inOut` |
| 80 / 80 | (0.8, 0, 0.2, 1) | `power3.inOut` to `power4.inOut` |
| 90 / 90 | (0.9, 0, 0.1, 1) | `expo.inOut` |

- **Multi-key graphs** (anticipation dip, overshoot and settle) transfer as one GSAP `CustomEase` path with several `C` segments, for example `CustomEase.create("ae80", "M0,0 C0.8,0 0.2,1 1,1")`.
- **Spatial vs temporal.** A curved path (spatial) with a bad speed curve (temporal) wobbles. Give a path its arc with separated X and Y eases (ease X out, Y in) or a motion path, and its feel with the speed curve.

## Weight: anticipation, overshoot, overlap

- **Anticipation:** a small move against the main action first (a button dips before it springs up, a word pulls back before it flies in). It tells the eye where to look.
- **Overshoot and settle:** pass the target and come back. The inertial-bounce idea scales the overshoot by the speed at arrival: a decaying sine `v / ω · sin(ω t) · e^(-decay · t)` (frequency about 3, decay about 5 as a start). In code: `back.out(1.2 to 1.7)`, `elastic.out` for playful marks, Remotion `spring()` with damping. A physical bounce is a series of shrinking parabolic arcs, not a sine. Never stack overshoot and bounce on one property.
- **Follow-through and overlap:** parts keep moving after the body stops; loose parts trail a few frames behind their parent and settle a little later.
- **Secondary action:** a supporting motion (a shadow that scales with a jump, a highlight that sweeps a logo after it lands) that never competes with the lead.
- **Arcs, squash and stretch:** natural motion travels in arcs; stretch along fast travel, squash on impact, keep the apparent volume. Freely on blobs and characters, sparingly on brand marks.
- **Policy, not reflex.** Overshoot is for elements with personality or impact; corporate interface often settles without it. Write the policy into the motion language.

## Stagger and offsets

- Offset related elements instead of starting them together: about 1 to 2 frames between characters, 2 to 4 between words or list items, 4 to 8 between larger blocks (*rule of thumb*). The whole cascade finishes faster than the move itself.
- The order carries meaning: reading order for text, from the centre for a burst, from the touch point for an interface, from the base for growth (bars from the axis).
- In code: GSAP `stagger: { each: 2 / fps, from: "start" | "center" | "end" }` and the position parameter (`"<"`, `">"`, `"-=25%"`); in Remotion `delay = index * k` frames.

## Holds, reading time and frames

- A hold is when the viewer reads. Moving text cannot be read: it must come to rest. Hold each text long enough to read it twice; Studio's house rule is 1 to 1.5 s at least, and the full heuristic is in [motion craft](motion-craft.md#readable-holds). Kinetic type carries about 2 words per second, 3 at most.
- Think in frames, with the frame rate locked to the destination before animating:

| Rate | 1 frame | 6 frames | 12 frames | 24 frames |
| --- | --- | --- | --- | --- |
| 24 fps | 42 ms | 250 ms | 500 ms | 1 s |
| 25 fps | 40 ms | 240 ms | 480 ms | 0.96 s |
| 30 fps | 33 ms | 200 ms | 400 ms | 0.8 s |
| 60 fps | 17 ms | 100 ms | 200 ms | 0.4 s |

- Longer distance or a larger scale change needs a longer move. Holding poses "on twos" gives a hand-made feel on slow moves and judder on fast ones; mix ones and twos on purpose.

## Effects and how they combine

**Render order decides the look.** After Effects renders masks, then effects top to bottom, then transforms. A blur before a scale-up gets scaled with it; on an adjustment layer above, it keeps its radius. A glow before a colour effect is tinted by it; after, it is not. In code the nesting of wrappers sets the same order: an outer element's `filter` applies after the inner transform, and post-processing passes run in their listed order.

**Finishing stack**, top of the master comp (*rule of thumb*): grade, glow or bloom, chromatic aberration or lens distortion, vignette, grain last, so nothing blurs or scales the grain.

| Effect | What pros use it for | Code form |
| --- | --- | --- |
| Glow stack | A tight bright core, a medium halo and a wide faint bloom, often only on chosen colours | duplicated blurred layers with `mix-blend-mode: screen` or stacked `drop-shadow()`; a bloom pass |
| Gaussian, lens, directional blur | Softness and depth; rack focus; speed | `filter: blur()`, SVG `feGaussianBlur`, depth-scaled blur; a short directional smear for speed |
| Fractal noise | Texture, smoke, water, displacement maps, luma mattes; animate Evolution, never the seed | SVG `feTurbulence` with a frame-driven offset; a noise shader with frame time |
| Turbulent or map displacement | Heat haze, liquid type, wobbly lines | `feDisplacementMap` fed by noise; a displacement shader |
| Gradients | Backgrounds and light passes, always with grain | CSS gradients plus a grain overlay |
| Echo, trails | Streaks and smears from past frames | draw earlier states at lower opacity; Remotion `<Trail>` |
| Linear, gradient, shape wipes | Transition primitives; a grey map sets the reveal order | `clip-path`, masks driven by a gradient |
| Particles | Emitters with life, size and opacity over life, turbulence | seeded particle arrays evaluated per frame (PixiJS, canvas) |
| Lens flares | Light accents composited with Screen or Add | additive sprites, kept rare |
| Chromatic aberration, RGB split, glitch | A few frames of channel offsets and slices | offset channel copies; a short burst on a beat |
| Grain | Kills banding and unifies the image | per-frame seeded noise at about 0.5 to 0.8%, last in the stack |

**Banding:** smooth gradients band at 8 bits and again in H.264. Add the light grain last.

## Recipes by job

- **Kinetic typography:** split into characters, words or lines; slide up from a mask line, scale from 0 with a controlled overshoot, expand tracking, blur to sharp, or hit word by word on the beat. Ease the per-character offset; the line must come to rest for its reading time.
- **Logo animation:** line draw (Trim Paths), build from geometric parts, a mask reveal behind a line, morph from a symbol, particle assemble, letter stagger or a 3D extrude to the front. Phases: intro, main reveal, settle, hold (*rule of thumb*: anticipation 200 to 400 ms, reveal 400 to 800 ms, settle 200 to 400 ms, hold 1 to 2 s). Add no glow, shadow or blur the brand guide does not use.
- **Shape morph:** both paths need the same point count and a matching first vertex, or the shape twists. Use a morph tool (GSAP MorphSVG, flubber) rather than raw interpolation.
- **Interface and app motion:** small, fast, functional moves; durations scale with distance and size; related elements move as one group.
- **Data and infographics:** bars grow from the axis, lines draw along x, pies sweep from twelve o'clock, numbers count up with an ease-out so the final value lands softly; stagger series in reading order and hold the final state long enough to read the numbers. Never animate a value through a misleading path (no overshoot below zero or past a meaningful maximum on data that must read exactly).
- **Transitions:** a hard cut in fast, music-driven sections; a whip pan with heavy motion blur and matched colour across the join; a match cut when shots share a form; a mask or shape wipe; a zoom through an element into the next scene; a luma wipe for organic reveals; a push or slide with one shared ease and direction; a glitch of a handful of frames; a morph, the hardest, planned by point count. Transitions run about 0.5 to 1.5 s, the short end in social.
- **Character rigs:** in After Effects DUIK (bones, IK) and Joysticks 'n Sliders (pose blending); in code a hierarchy of groups with pivots at the joints and pose tables blended by frame.

## Camera and depth

- **Push-in** focuses attention: move toward the subject and hold. Studio's house rules: one push per beat, no zoom-out in the middle of a move, moves of about 0.4 to 0.55 s, a close push on typing that holds until the text is sent.
- **Parallax and 2.5D:** two or three depth planes, the camera moves (dolly), the lens does not zoom; foreground moves more than background, and small moves work best.
- **Depth of field:** focus on the subject, blur far planes by depth.
- **Camera rigs:** a camera parented to a null for pans and orbits; camera moves eased and slower than element moves so the frame feels steady.
- **Depth by compositing:** a soft back light, the subject, a blurred multiply contact shadow, a screen or add rim light, haze toward the back.

## Design in time

- **Hierarchy over time:** decide the order in which the viewer notices things and reveal in that order; the most important element moves first or most.
- **One idea per beat**, often one music bar or one sentence of voice-over.
- **Contrast** of value, scale, speed and stillness: a still element among moving ones is a strong focus.
- **Rhythm:** mark the beats first, then snap starts and hits to them; major changes on downbeats, accents on the strongest transients, not a hit on every beat.
- **Negative space** gives motion room to travel and holds room to breathe.
- **Colour:** a limited palette with one accent reserved for the focus.
- **Safe areas:** broadcast title safe about 80 to 90%, action safe about 90 to 93%; vertical social keeps text clear of the top interface and the bottom caption and buttons zone (Studio's 9:16 check lines: top 10%, bottom 20%).
- **One motion language per project:** two or three named curves (enter, exit, move), a frame-based duration scale, one stagger value and an overshoot policy, as brand motion systems such as IBM Carbon (productive and expressive) do. Record it in the motion contract and use it in every scene.

## Pre-delivery check

**Motion:** every move has a reason; no linear keys except mechanical motion; speed curves are clean humps; no floating long eases; no dead frames, and every text has its hold; overshoots settle fully and nothing jitters at rest; fast elements carry motion blur or at least do not strobe; loops are seamless at the loop frame.

**Frame:** text inside the safe areas for every ratio; no banding; clean edges; nothing cut by a mask or the frame by accident; nothing covered by another object.

**Sound and file:** loudness to the target (about -14 LUFS for web, -23 LUFS EBU R128, -24 LKFS ATSC, true peak -1 or -2 dBTP); H.264 yuv420p MP4 with AAC 48 kHz for web (about 8 Mbps at 1080p30 on YouTube); ProRes 422 HQ as a master, ProRes 4444 or a PNG sequence when alpha is needed; the frame rate exactly as composed.

Then run Studio's frame sweep and critique as the motion workflow requires.

## Beginner habits and pro habits

| Beginner | Pro |
| --- | --- |
| Default linear or one-click Easy Ease everywhere | Each curve shaped; asymmetric eases with long landings |
| Everything starts on the same frame | Staggers by a few frames in a meaningful order |
| Animates before designing | Brief, concept, styleframes, animatic first |
| Everything moves all the time | One lead action per beat, the rest quiet or still |
| Text leaves before it is read | Reading holds planned from the word count |
| Pivot left in the middle | Anchor at the physical pivot before animating |
| Dozens of duplicated keys | Controllers, parenting and parameters drive groups |
| Effects hide weak motion | Motion works in grey boxes first; effects at polish |
| Animates the noise seed | Animates Evolution (a continuous offset) |
| Zooms the lens for "3D" | Dollies the camera for real parallax |
| No motion blur | Blur on fast moves, at a 180° shutter |
| Smooth gradients exported clean | Grain last, against banding |
| Overshoot on every element | Overshoot as a policy for elements with impact |
| A different curve style in every scene | One motion language for the whole piece |
| Sound added at the end | Animates to the track and its markers |

## Sources

Paraphrased; checked 2026-11-07. Some pages were read through search summaries where the fetch failed (Adobe's keyframe-interpolation page, Material 3 tokens).

1. Adobe After Effects user guide: keyframe interpolation, speed graph and influence, track mattes, render order, motion blur, Essential Graphics.
2. School of Motion: Graph Editor, the motion design workflow (brief to styleframes to animatic), transitions, text animators.
3. Video Copilot: glow and selective glow, particles and smoke trails, Optical Flares, liquid and displacement looks.
4. Dan Ebberts (motionscript.com): inertial bounce and physical bounce expressions, `loopOut`, `valueAtTime`.
5. Disney's twelve principles as applied to motion design (anticipation, follow-through, arcs, squash and stretch, staging); Issara Willenskomer on interface motion via Adobe.
6. IBM Carbon motion (productive and expressive curves, 70 to 700 ms) and Material motion (durations, decelerate and accelerate curves); Salesforce Kinetics.
7. GSAP documentation: eases, `CustomEase`, `stagger`, the position parameter; easings.net (Penner curves).
8. Remotion documentation: `interpolate`, `spring`, `<CameraMotionBlur>`, `<Trail>`; HyperFrames documentation: deterministic seeking of one paused timeline.
9. MDN and Chrome developers: `mask-mode`, `clip-path`, `stroke-dashoffset`, `mix-blend-mode`, CSS `linear()` easing.
10. Banding and grain guidance (8 versus 16 bpc, 0.5 to 0.8% noise); broadcast safe areas; EBU R128, ATSC A/85; YouTube upload settings; Apple ProRes white paper.
11. Buck studio breakdowns (timing fixed in rough 3D before final shapes); DUIK and Joysticks 'n Sliders documentation.
