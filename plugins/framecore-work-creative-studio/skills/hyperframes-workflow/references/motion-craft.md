# Motion craft: concrete starting values

Use this reference when designing or implementing motion, after the brief and storyboard define what must be communicated. The numbers are Studio starting heuristics for a first pass, not platform rules or proof of quality. Adjust them to the approved style, viewing size and actual playback, and record the chosen values in the motion contract. Public standards cited here are named; everything else is craft guidance to verify by watching the result.

## Principles that decide most results

1. **One focal point per moment.** At any frame the viewer should know where to look. Stage secondary elements after the focal element settles, not at the same time.
2. **Motion explains a change.** Every movement should reveal, connect, compare, emphasize or transition. If it does none of these, remove it or make it quieter.
3. **Enter fast, settle slowly.** Entrances use ease-out, exits use ease-in, moves between two rest states use ease-in-out. Linear motion only for constant processes (progress bars, scrolling tickers, rotation that never stops).
4. **Consistent direction and origin.** Keep one direction of progress (left to right or bottom to top for left-to-right languages) and grow elements from a meaningful origin (the button, the data point, the previous element), not from the centre by default.
5. **Contrast in energy.** Alternate active passages with readable rests. A sequence where everything moves all the time reads as noise.
6. **Hold the result.** The final state of each idea needs a readable hold before the next change; the end card needs the longest hold.

## Easing presets

Use the project's installed APIs. Equivalent values across runtimes:

| Purpose | CSS / cubic-bezier | GSAP | Remotion |
| --- | --- | --- | --- |
| Standard entrance | `cubic-bezier(0.33, 1, 0.68, 1)` (ease-out cubic) | `power2.out` | `Easing.out(Easing.cubic)` or `Easing.bezier(0.33, 1, 0.68, 1)` |
| Confident, crisp entrance | `cubic-bezier(0.25, 1, 0.5, 1)` (ease-out quart) | `power3.out` | `Easing.bezier(0.25, 1, 0.5, 1)` |
| Dramatic reveal, fast start and long settle | `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out expo) | `expo.out` | `Easing.bezier(0.16, 1, 0.3, 1)` |
| Move between two rest states | `cubic-bezier(0.65, 0, 0.35, 1)` (ease-in-out cubic) | `power2.inOut` | `Easing.inOut(Easing.cubic)` |
| Exit | `cubic-bezier(0.32, 0, 0.67, 0)` (ease-in cubic) | `power2.in` | `Easing.in(Easing.cubic)` |
| Constant process | `linear` | `none` | `Easing.linear` |

GSAP `power1`–`power4` correspond to quad, cubic, quart and quint curves. For a physical settle in Remotion, `spring({frame, fps, config: {damping: 200}})` gives a smooth approach without overshoot; lower damping adds bounce. Check the installed version's signature before use. Use overshoot or bounce only when the brief calls for playful character, and never on body text.

## Durations in frames

Values for 30 FPS; double them for 60 FPS and scale proportionally for other rates. Shorter values feel snappy and technical, longer values feel calm and premium. Pick one tempo family per project and keep it.

| Element | Typical range at 30 FPS | Notes |
| --- | --- | --- |
| Small label, icon or UI detail entering | 8–12 frames | |
| Headline line reveal | 12–20 frames | Mask reveals read best around 15 frames |
| Hero title or logo resolve | 20–45 frames | Protected logos keep geometry; animate approved parts only |
| Move or scale between rest states | 20–40 frames | Longer distance needs longer duration |
| Scene transition (push, wipe, mask) | 10–20 frames | |
| Dissolve | 6–15 frames | Longer dissolves look unintentional |
| Exit | 60–75% of the entry duration | Exits should not compete with the next entrance |
| Per-word stagger | 2–4 frames | |
| Per-line or per-item stagger | 4–8 frames | |
| Per-letter stagger | 1–2 frames | Only for a short display word, never for sentences |

Keep the total stagger of a group shorter than its own entry duration so the group reads as one gesture.

## Readable holds

A hold begins when the whole phrase is legible, not when its animation starts. Starting heuristic: about 13 characters per second plus 0.5 seconds to settle, with a minimum of 1 second. Example: a 26-character line needs about 2.5 seconds, 75 frames at 30 FPS. A second check counts words: half a second plus a third of a second per word, from the moment the last word has landed and stopped moving (kaventro/motion-designer); use the longer of the two, at least 1 second. `check-score.mjs` and the craft critique (`critique.py`) apply exactly this rule. Increase it for small viewing sizes, dense layouts, secondary languages or data that must be compared. Confirm by watching at the intended size; the heuristic is not a reading standard.

## Vocabulary and signature

Name moves by feel and keep one set per video (adapted from [kaventro/motion-designer](kaventro-motion-designer-adaptation.md)):

| Feel | How | Scene engine |
| --- | --- | --- |
| arrive | ease-out, from below or from what caused it | `entryEasing` (`easeOutCubic`, `easeOutQuart`) |
| settle | a calm landing for panels, cards and end cards | `resolveEasing` (`easeOutExpo`) |
| depart | ease-in, faster than the arrival; last in, first out | `exitEasing` (`easeInCubic`), `exitFrames` about 60–75% of `entryFrames` |
| snap | quick state changes: a list shifting, a value updating | short `entryFrames` (8–12) |
| glide | camera-like moves over 0.8–1.2 s | `easeInOutCubic` (the sweep line) |
| drift | 2–3% movement during a hold so a still frame is not frozen | custom code; the engine holds still |

- **One relay object.** A small element (a dot, a line, a shape from the logo) travels through the video and returns at the end, so the first and last frames rhyme.
- **An accent with one meaning.** The accent marks now or just changed; new values arrive in it. Do not spend it on decoration.
- **One signature per video.** One move or effect the video is remembered by carries more than five. Name it in the brief; [motion styles](../assets/motion-styles/README.md) each name one.
- **Effects mark moments.** A glitch on a cut, a shake on a drop; constant textures stay quiet (film grain at about 8–15% opacity). Effects never hide text that must be read.

## Rhythm and music

- Frames per beat = FPS × 60 / BPM. Example: 120 BPM at 30 FPS = 15 frames per beat; 128 BPM at 30 FPS = 14.0625.
- Compute every cue from the master timeline as `round(beatIndex × FPS × 60 / BPM)` instead of adding rounded beat lengths, so rounding errors do not accumulate.
- Put major events on downbeats or bar starts, and let smaller accents fall between. Cutting on every beat flattens the rhythm: something may move on a beat, but scenes change on bar lines.
- Land the biggest reveal on the music's drop. Put the drop in the beat map first and plan backwards from it; when the story needs more or less time, change the holds, never the music's speed.
- Land the visual impact on the cue frame; start the motion before it so the peak arrives with the sound.
- Leave silence or a sustained note under the final hold when the message needs attention.
- The [sync tool](../assets/motion-sync/README.md) records the grid in the contract, reports where scenes and holds fall on it and imports voice-over subtitles as captions.

## Transition grammar

| Transition | Use when | Avoid when |
| --- | --- | --- |
| Hard cut | Ideas are separate, energy is high, or the beat demands it | The viewer needs to track one object across scenes |
| Match cut or shape continuity | A shape, colour or position carries meaning into the next scene | The shapes do not genuinely relate |
| Mask or wipe | Revealing a new layer of the same idea, or a clear direction of progress | Several wipes in different directions in one sequence |
| Push or slide | Moving through a sequence, list or timeline | The content is not ordered |
| Scale-through or zoom | Going deeper into a detail or pulling out to context | Used as decoration without a deeper or wider subject |
| Morph | One state truly becomes another (before and after, data change) | The two states have unrelated structure |
| Dissolve | Time passing or a soft change of mood | Fast, informational sequences |

Choose two or three transition types per project and repeat them consistently. Consistency is not one wipe everywhere: where scenes belong together, let an element carry the change (a product, a search field, a selection mark); keep a full-frame wipe or mask for a real break. Three or more identical full-frame wipes read as slides, and the critique flags them ([commercial motion](commercial-motion.md#2-prove-the-picture-on-real-frames-first)).

## Video types

Starting shapes for common requests (adapted from kaventro/motion-designer). A social cut of any type runs 15–25 s in 1080 × 1920 and shows its strongest moment in the first two seconds.

| Type | For | Length · format | Scene kinds |
| --- | --- | --- | --- |
| Title or sting | an intro, outro, logo or channel open | 3–10 s · any, often looping | `logo-reveal`, `end-card`, one signature move |
| Kinetic type | a quote, manifesto or announcement | 10–40 s · vertical or square | `line-reveal`, `quote`, a line per beat |
| Explainer | a topic or an idea, often with voice-over | 30–90 s · landscape or vertical | `item-stagger`, `counter`, captions |
| Data video | a statistic or result | 8–30 s · any | `counter`, `item-stagger`; sourced numbers only |
| Feature cards | several features quickly | 15–30 s · vertical or square | `line-reveal` headline per feature, `end-card` |
| Product film | a product's real interface at work | 20–60 s · landscape, square or vertical | `device` with screenshots, `end-card`; see [product films](product-films.md) |
| Overlay on footage | lower thirds, captions, end cards over a recording | the footage's length and format | custom code over the user's footage |

## Typography in motion

- **Line mask reveal:** each line rises from below its own clipping box with an ease-out entrance of 12–18 frames. Reliable default for headlines. A mask about 1.3 times the font size keeps descenders whole; the scene engine's 1.1 is tight, so check `g`, `j`, `p`, `q` and `y` at rest.
- **Word stagger:** words enter 2–4 frames apart with small offsets (about 20–40 px at 1080p) and opacity. Good for short statements.
- **Emphasis:** change colour, weight, underline or scale (about 1.04–1.08) of one key word after the line is readable. Emphasize one idea per line.
- **Counters:** animate integers with tabular figures so width does not jitter; hold the final value and show the unit and source.
- **Voiceover sync:** derive word timing from the actual transcript or audio analysis, not from estimated speech rates, and mark estimates as designed timing.
- Use real font files and wait for them to load. Test the longest string and diacritics at the smallest intended viewing size.

## Layout and legibility

- Starting margins: keep text at least 5–8% of the frame width from the edges. Platform interface overlays and safe zones change; check current platform documentation when the delivery placement is named, and do not invent them.
- Contrast: WCAG 2.x success criterion 1.4.3 asks for 4.5:1 for normal text and 3:1 for large text. Use it as a floor for on-screen text, and check the darkest and brightest frames behind moving text.
- Size: on a 1080 × 1920 vertical frame, body text below about 40 px is hard to read on a phone; headlines usually work from about 80 px. Verify at actual size.
- Use a grid for the whole film and keep recurring elements in the same positions so the viewer learns the layout.

## Common defects to remove before review

- Everything animates at once, or every element uses the same duration and easing.
- Text moves while it should be read, or disappears before its hold ends.
- Bounce or overshoot on serious, corporate or data content.
- Decorative particles, glow, grain or HUD labels filling empty space without meaning.
- Transitions in many different directions with no logic.
- Jitter from fractional positions, unloaded fonts or numbers changing width. Round the resting positions of type to whole pixels; keep fractions for motion only.
- An ending without a stable final frame.
- A few pixels of drift standing in for pacing: drift keeps pixels moving but adds no information, so a long drifting hold is still a still stretch.
- A word cut by a mask, a box or the frame edge while it should be read, including decorative background words; a container that fits does not prove its text fits.
- A photograph's own background showing as a rectangle on a different scene colour.

## Recording the choices

Add the selected tempo family, easing presets, transition set and hold values to the motion contract's motion system so implementation and review use the same numbers. Starters in this package read them from the shared `motion-score.json` format; see [the Remotion kinetic type starter](../../remotion-video-production/assets/kinetic-type-starter/README.md) and [the GSAP starter](../assets/gsap-motion-starter/README.md).
