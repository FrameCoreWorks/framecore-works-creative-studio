# Art-style and explainer motion: direction rules

Adapted in English from [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) by alchaincyf (MIT, reviewed at commit `8a0d7d7`), a skill whose rules come from films its author made and judged. This page keeps the direction method; Studio's own runtimes, review and delivery stay in charge. The original skill (36 implemented art-style scenes, parameterized explainer clips, its own gates, docs mostly in Chinese) is the pinned `huashu-art-motion` [extension](../../workflow-orchestrator/references/extensions.md). The numbers below are starting points measured on reference films, not quotas: a better design wins, checked by watching at normal speed.

## Contents

- [Camera: punctuation, not decoration](#camera-punctuation-not-decoration)
- [Camera moves and their timings](#camera-moves-and-their-timings)
- [Choosing the look](#choosing-the-look)
- [Explainer grammars](#explainer-grammars)
- [Rules that hold across grammars](#rules-that-hold-across-grammars)
- [Six ways a film goes wrong](#six-ways-a-film-goes-wrong)
- [Shot list before code](#shot-list-before-code)
- [Art-style recipes](#art-style-recipes)
- [Breaking down a reference](#breaking-down-a-reference)

## Camera: punctuation, not decoration

Before every camera move, answer three questions: where should the viewer look now, and can they read it at this framing; is this move a transition or an accent; what did the previous shot's camera do.

- **If it reads, hold.** When the picture moves by itself (live footage, a line being drawn, a curve growing) or the viewer is reading, the camera stays. Long holds in an explainer are correct, not dead time.
- **Transitions are slow, accents are fast.** A slow push leads the eye to the next detail, a glide moves between things, a pull-out gives the whole picture or closes a section. Snap pushes, slams and whips are accents: reveals, reversals, key numbers and jokes, few enough to count.
- **Go in, come back.** After pushing in, pull out, glide away or cut to another framing. Never three pushes in a row. One full-frame image per shot is where "cut, push, cut, push" happens most: a 102-second explainer with about 48 pushes, all inward, was judged "far too many zooms, too fast, not smooth at all".
- **One rhythm for the whole film fails.** A steady slow push on every shot read "exactly like a slide deck"; a quick push on every shot read too fast. Same disease: every shot has the same move. Let the camera follow the section's emotion: steady when explaining, faster only at turns and peaks. In a music video: slow push and drift in verses, faster in the chorus, pull-out in the break, transition peaks on the beat.
- **Still is not the same as good.** Something must keep happening in the picture: things moving, footage moving, something new revealed, the camera guiding the eye. Slow and moving are different axes.
- **Art-style scenes are an exception: the painting must stay alive.** Each scene has one main action plus two looping motifs (stars turning, water rippling, smoke rising); the camera may drift slowly. "Transitions between still pictures" loses what made the reference work.

## Camera moves and their timings

| Move | Use | Starting value | Ignore the value when |
| --- | --- | --- | --- |
| Hold | reading, the picture moves itself, silence after a joke | as long as the voice needs | — |
| Slow push | lead the eye to a detail, nudge the emotion | 0.6–1.5 s, sine in-out, push until the target reads (often 10–40 %) | a push of 2× or more may take 2 s; on music, follow the beat |
| Pull-out | back to the whole, "where it is", end of a section | 0.8–2 s, fast start, long settle | scale journeys (cell to planet) take their own time |
| Glide | from one thing to the next on the same wall or desk; follow a moving thing | 0.5–0.9 s, sine in-out; along a line 1.3–1.8 s | following an object: match its speed |
| Snap push | accent: reveal, reversal, key number | 0.25–0.35 s, 18–32 % closer, then hold | kinetic type and music-cut sections: it is the main grammar there |
| Whip | sudden change of attention, comic timing | 0.26–0.30 s with motion blur | — |
| Slam | a big word, number or stamp landing | 0.17 s, scale 1.55 → 0.94 → 1.0 | at most once per shot; not on every cut |
| Hard cut / jump closer | change framing without a move: reaction close-up | 0 frames | — |
| Drift | ambient shots, living art scenes, lyrical music-video sections | 1–4 % per second | **in an explainer, a few percent of drift on every shot reads as a slide deck** |

How much the count matters depends on the form. Explainers (science, finance, whiteboard, investigation desk): accents at most a third of the shots, no three pushes in a row, more than about eight pushes a minute deserves a look. The first 3 seconds of a short-form hook may be dense. Kinetic type and music cuts follow the beat, so push counts do not apply. Story and comedy live on holds and hard jump cuts. Art-style journeys care whether the painting is alive, not how often the camera pushes.

## Choosing the look

The look serves the content: first see what material exists and what the section must make clear.

- **Real material is the main picture.** Screenshots, photos, footage, original text and the product's own output go full frame or close to it, scaled proportionally with key UI uncropped; code explains, labels and moves the camera. Draw or generate a page only where no material exists. A long technical film made almost entirely of generated imagery "looked bad".
- **Pick the grammar by what is being explained** (table below).
- **One look and one palette for the whole film, to the last frame.** People, animals and props use the same brushwork: vector shapes inside a Monet-style video "did not match". A clean, consistent film that is slightly slide-like beats a collage that changes style every shot.
- **Avoid the generated default palette:** blue-purple gradients, deep-purple starfields, neon cyan-violet glow and purple frosted glass read instantly as machine-made. Use them only when the user asks or the subject needs them (a named cyberpunk palette, Starry Night), and say why. A flat navy (hue around 210°) is a deliberate single colour, not this.
- **A palette is 3 to 6 colours:** background, surface, main ink, secondary ink and one or two accents; an accent points at one thing per shot. Decide light or dark once and stay there; no gradient backgrounds or neon outer glow; build depth from paper texture, grain or two flat tones. With real material, take one or two accents from it.
- **A new direction gets three options with different compositions,** not three recolours of one frame. A named style does not waive this.

## Explainer grammars

Choose per section; a film may change grammar between sections, never inside one.

| The section is about | Use | Avoid | Why |
| --- | --- | --- | --- |
| a concept or mechanism | 3Blue1Brown-style transformation (derivation, formulas) or Kurzgesagt-style flat shapes across scales | an investigation desk with no real documents | mechanisms are explained by transformation and scale |
| news, events, history with screenshots and quotes | Vox-style investigation desk: clippings, red lines, highlighter | flat cartoon (weakens credibility) | the viewer must see the source |
| a personal story, mishap or joke | storytime: reaction close-ups, holds, jump cuts | launch-keynote UI (brings its own good-news mood) | the joke lives in the pause |
| a list, stages, one strong line | kinetic typography | transformation (nothing to transform) | the information is structure, not image |
| a product, tutorial steps, features | keynote UI: screenshot full frame and push to the part being described | transformation | one thing per screen; nouns and numbers lead |
| numbers, growth, comparison | finance charts: axes, then data, then one highlight | one big number (only when there is a single number) | needs axes and units that hold up to scrutiny |
| a step-by-step argument | whiteboard: a pen draws as the voice speaks, pull out at the end | a full-screen swap | one line said, one line drawn |

With real screenshots, use keynote UI (clean, tutorial) or the investigation desk (argument, evidence). A section with a single number gets no chart: count it up and land it on the word that says it.

## Rules that hold across grammars

1. **The camera depends only on time; the scene is redrawn for the camera.** Pushes, pans and journeys are one world canvas seen through different cameras, so a 60× zoom stays sharp.
2. **Zoom logarithmically:** every frame scales by the same factor; linear interpolation starts slow and ends violently. To fly through a round opening of radius r, the zoom must reach the distance from its centre to the farthest screen corner divided by r.
3. **Land the reveal on the beat or the word.** The frame where the new picture appears falls on the bar line; a counter lands when the voice says the number (start = word time − count duration); whiteboard writing starts about 0.5 s after its phrase.
4. **Structure, then data, then annotation;** one annotation per shot.
5. **One focus per moment:** one thing enters, the rest holds; main word to secondary text at least 3:1; the background one step lower in saturation, contrast and line weight.
6. **Enter slowly, leave fast, then hold:** entries 0.3–0.4 s, exits about 0.18 s; a landed number holds at least 0.5 s, a punchline at least 0.9 s.
7. **Move on events,** as in the camera section. Numbers and big words land on objects in the film's world (a screen, a price tag, a blackboard), not on a separate solid-colour title card: blind viewers read such cards as "a slide was inserted".
8. **Two frame rates:** the camera smooth, elements stepped (paper, highlighter and typing on twos at 12 fps; characters at 24 fps). Everything smooth looks corporate; everything stepped wobbles.
9. **Colour is a concept:** one colour per idea, no more than three or four semantic colours.
10. **Transitions go between breaths and topics,** never mid-sentence.
11. **Review logic and figures, not only looks:** "rose 8.7 times" versus "rose to 8.7 times its value"; a counter restarting from zero after expanding; ratios that cannot be computed from the chart.
12. **Data changes how it appears, never what it is:** bars start at zero or the axis says otherwise; invented data is marked as illustrative in every shot, real data never.

## Six ways a film goes wrong

Check before starting and again before delivery.

1. **Paged slide deck:** fixed header and page numbers, bullets fading in, the same camera move on every shot, ending on a centred quote card. → Remove the frame, one picture event per shot, varied moves that come back out, end on an action of the hero or the main object.
2. **Copied demo:** compositions, characters or assets from an example go into the film. → Learn the method; redesign composition and objects for the subject.
3. **No concrete object:** an abstract idea shown only as words and icons. → Every shot names a concrete thing and what it does; a row without an object is not ready.
4. **Dead background, empty frame:** a large flat or starfield background that never changes while a small patch moves, or a frame with no subject. → The subject fills at least half the frame, the background changes with the content, the hero is in every shot; a blank mid-film stretch over 0.3 s is a defect.
5. **Drawing what exists as material.** → Put the real screenshot, photo or footage full frame.
6. **Machine-made look:** the default blue-purple palette; a different style every shot; code-drawn chibi people and white-shell robots; coins and particles with faces. → One look and palette locked before the shot list; people either as generated frames that pass review or only hands and backs.

Studio's [motion activity](../assets/motion-quality/README.md) and [frame review](../assets/motion-review/README.md) measure stills, motion and layout; the six failures above still need a look at the frames and one viewing at normal speed.

## Shot list before code

Lock three lines first: the look (one sentence for the whole film), the palette (3–6 values) and characters (none, hands and backs only, or a named frame library). Then one row per shot: time, the object in the picture (a noun), what it does (a verb), the camera move, on-screen text (eight words or fewer, may be empty) and the method. The first 3 seconds are a small concrete scene (hands or an object doing something tied to the topic), not a title; one concrete example runs through the whole film; shots last 2 to 6 seconds; text-led shots stay under 30 %; neighbouring shots change composition, never style. Studio's [shot-plan check](../../storyboard-sequence-architect/SKILL.md) and storyboard owner hold this table.

## Art-style recipes

Upstream keeps one card per art style with its parameters, motif motion, signature transition and known limits (36 implemented: cave painting, Egyptian, Greek, Roman, Gothic, Renaissance, Impressionism, Monet, Seurat, Van Gogh-era post-impressionism, Art Nouveau, Cubism, Bauhaus, Pop, 8-bit, ray-traced, Klimt, Munch, Kusama, Dalí, constructivism, Hopper, Ghibli, vaporwave, Kirby, rubber hose, shadow puppets, Rembrandt, Haring, Matisse, Rick and Morty-style and South Park-style flat cartoons, Dunhuang murals and more; 17 research cards are not yet implementations). When a film uses a painter's or tradition's look:

- Learn the visual language (brushwork, colour, light, form, space) from several different works, then test it on the new subject. A famous painting's people, objects and layout are not a template.
- A studio such as Ghibli or Pixar is a film-level art direction, not one filter: name the scope first.
- **Render one frame first, approve it, then animate it.** Four routes: (A) everything drawn in code with a style renderer, for precise control and many styles; (B) generated layers on a green screen that keep the original frame's coordinates, moved by code, when the look is beyond code; (C) a video model from first and last frame (the same frame for both) for organic whole-painting motion without precise control; (D) a mix, with code owning the timeline.
- Determinism: every random value is seeded, so the same time renders the same pixels twice.
- Public-domain originals (for example open-access museum collections) can be studied and redrawn; anything else is a reference for technique only.

## Breaking down a reference

To recreate a mechanism from a reference animation the user may study, measure before writing code: [reference breakdown](../assets/reference-breakdown/README.md) finds the cuts and their beat grid, makes a 15-cell contact sheet for each transition (the mechanism is only visible there), a per-segment motion heatmap (what moves inside each "still" scene, which a first look always underestimates) and the last clean frame of each segment as the composition map. Take reference frames just before a transition starts, not the prettiest frame. A model listening to the soundtrack is a candidate only: verify tempo and accents with [`beats.py`](../assets/motion-sync/README.md#analysing-a-supplied-track). Recreating means learning the mechanism and applying it to new subject matter, never copying the frames.
