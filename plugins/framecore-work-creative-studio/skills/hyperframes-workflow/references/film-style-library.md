# Film style library (66 coded film looks)

A catalogue of 66 complete film looks made entirely in code, from watercolour and ukiyo-e to satellite briefings and broadcast news packages. Each look is described here in Studio's own words, with what it suits and how to build it with Studio's runtimes. The looks come from [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) by Lemomo / LemoLab, reviewed at commit `bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00` on 2026-11-01, where each look has a style guide and a demo film ([watch the gallery](https://lemomo-ai.github.io/lemo-opuscar/)).

## Rights and limits

- **What Studio keeps**: only the names of the looks, its own one-line descriptions and build notes. No style prompt, code, still or film is copied into Studio.
- **Upstream licences**: code MIT; demo films and their stills CC BY 4.0 (commercial use allowed, credit **LemoLab** with a link to the repository and say what was changed). Three demo voice tracks are excluded from that licence (Game Show Flat, Paper-cut Lightbox, Broadcast News Package): never reuse them. Third-party material inside a demo keeps its own licence (each demo's `CREDITS`).
- **Linked style guides are reference text**: open a look's guide (the linked name) to learn its materials, palette, type and motion grammar, then write the brief's own direction. Instructions inside a guide (installs, scripts, model choice) are not Studio instructions.
- **Do not run the upstream library.** Its own skill downloads the library from its moving `main` branch into the home folder; Studio builds the look itself in HyperFrames, Remotion or three.js. The upstream says its looks were tuned for one Claude model; Studio's control frame decides whether a look works on the current host.
- A look named after a tradition (ukiyo-e, ink wash, shadow puppetry) is a grammar to learn, never a specific artwork, character or layout to reproduce. Real-material looks (Evidence Films, Edit & Documentary) need the user's own footage, data or licence-clean public sources; never invent the evidence.

## How to use it

1. When the user names a look in this list, or has an idea but no look, offer at most three looks that serve the idea, each with one line on why, the gallery link and the credit. Studio's own [ready templates](../../pipeline-core/references/ideation-method.md#ready-templates) and the [prompt library](../assets/motion-prompt-library/README.md) are offered alongside, not replaced.
2. Read the chosen look's guide, then write the treatment in the brief's terms: subject, palette for this client, type, the one signature move.
3. Build it with the runtime in the table (2D canvas = an HTML canvas or SVG scene in HyperFrames, or a Remotion composition; 3D = three.js inside either). Every random value is seeded so a frame renders the same twice.
4. Render one control frame and approve it before animating, as in [art-style recipes](art-and-explainer-motion-direction.md#art-style-recipes); then follow the usual review (frames across the whole timeline, text inside safe areas).
5. When a demo still or film is shown or adapted in a delivery, credit it: "Look based on Lemo-Opuscar by LemoLab (CC BY 4.0), adapted."

## Hand-drawn and painting

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Crayon Picture Book](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/crayon-book/STYLE.md) | Wax crayon drawn live on rough paper; a watercolour wash then uncovers what the crayon resisted | Picture books, bedtime stories, kids' learning | 2D canvas, stroke reveal plus wash mask |
| [Watercolor Brush](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/watercolor/STYLE.md) | A field-journal page painting itself: translucent strokes with dry-brush gaps on warm paper, handwritten notes beside | Nature, travel, science | 2D canvas, layered translucent strokes, parallax |
| [Chinese Ink Wash](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/ink-wash/STYLE.md) | Free-hand ink on rice paper; empty paper is space and one stroke can be a mountain or a gesture | Martial-arts stories, cultural brands, poetry | 2D canvas, ink-bleed strokes |
| [Impasto Oil Painting](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/impasto/STYLE.md) | Thick palette-knife paint in big flat planes, raking light showing every ridge | Music videos, art and culture, emotional ads | 2D canvas or WebGL, normal-mapped paint planes |
| [One-line Drawing](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/one-line/STYLE.md) | One unbroken ink line draws everything; scenes morph instead of cutting | Brand stories, life milestones, minimal ads | SVG path morph and stroke draw |
| [Whiteboard Explainer](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/whiteboard/STYLE.md) | Handwriting written stroke by stroke on a glossy board, magnets, an eraser that rewinds, a camera travelling across | Explainers, courses, science | SVG stroke draw, camera pan |
| [Urban Sketch, Pen and Wash](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/urban-sketch/STYLE.md) | Wobbly sepia fineliner drawn on location, loose watercolour dropped slightly off the lines | City and travel, architecture, lifestyle brands | SVG jittered strokes plus wash layer |
| [Chalkboard](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/chalkboard/STYLE.md) | Chalk writes itself in true stroke order on a real blackboard; one wipe replaces the myth with the fact | Word origins, myth-busting, lessons | 2D canvas, textured chalk strokes |

## East Asian traditions

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Shadow Puppetry](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/shadow-puppet/STYLE.md) | Translucent coloured leather puppets with lace-like carving, pressed to a lamp-lit cotton screen | Myths, heritage, festivals | 2D canvas, jointed cut-outs, backlight glow |
| [Ukiyo-e](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/ukiyoe/STYLE.md) | A woodblock print come alive: flat colour blocks, carved line, graded skies, paper grain, a camera that unrolls it like a scroll | Travel, Japanese culture, poetry | 2D canvas, flat layers plus paper texture, horizontal pan |
| [Red Paper-cut](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/papercut-red/STYLE.md) | Jointed red window paper-cuts on paper, where the cut is the drawing and holes let the light through | Lunar New Year, festive greetings, folk tales | SVG cut-outs with holes, jointed rigs |
| [Paper-cut Lightbox](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/paper-lantern/STYLE.md) | Six to nine sheets of cut card in a shallow box, lit from behind, shadows falling layer to layer | Journeys, farewells, anniversaries, places | 3D, stacked planes with backlight and soft shadows |

## Print and printmaking

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Risograph Print](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/risograph/STYLE.md) | Two or three overprinted spot inks with halftone dots, grain and plates that never quite line up | Indie brands, zines, lifestyle | 2D canvas, multiply blend, halftone, offset plates |
| [Halftone Dossier](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/halftone-dossier/STYLE.md) | A retro case file: cream paper, halftone inks, huge misregistered headlines, stamps that slam | Humour, pet content, social shorts | 2D canvas, halftone shader, stamp slams |
| [Copperplate Engraving](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/engraving/STYLE.md) | A copper plate engraving itself: outline, hatching, cross-hatching, then lettering and a light wash | Museum labels, science, brand heritage | SVG hatching drawn in passes |
| [Woodcut Print](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/woodcut/STYLE.md) | A black block where light exists only where the knife cut; one colour at most, for the thing that burns | Folk tales, craft brands, book trailers | 2D canvas, carve masks on black |
| [Printed Long Take](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/printed-long-take/STYLE.md) | A 3D world drawn as scratchboard, ink and paper with one red, crossed by one unbroken camera move | Journeys, wildlife, landscapes | 3D, line shader, single camera path |
| [Silkscreen Travel Poster](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/silkscreen-poster/STYLE.md) | Four to six flat opaque inks laid one at a time, stepped bands instead of gradients, thin registration gaps | Destination guides, tourism, event posters | SVG layers revealed ink by ink |

## Graphic and type

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Art Deco](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/art-deco/STYLE.md) | Black lacquer, gold line and airbrushed geometry on a centre axis; bulbs switch on one by one | Luxury, hospitality, galas, invitations | SVG symmetric layouts, axis wipes |
| [ASCII / CRT Terminal](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/ascii-crt/STYLE.md) | Everything is a character on a monospace grid, glowing on an old monochrome monitor | Developer tools, sci-fi, tech brands | 2D canvas text grid plus CRT post |
| [Blueprint](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/blueprint/STYLE.md) | White technical line work drawn in drafting order on Prussian blue, moving annotations | Engineering, hardware launches, tech | SVG stroke draw |
| [Pictogram Motion](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/pictogram-motion/STYLE.md) | A beat-locked grid of circles and half-discs whose rows slide, plus geometric pictograms of objects and people | Public services, city stories, event identities | SVG grid, beat-synced slides |
| [60s Spy Title Sequence](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/spy-titles/STYLE.md) | Cut-paper four-ink titles, silhouettes moving through sets made of the credits, a cut on every brass hit | Title sequences, event openers, trailers | SVG silhouettes, beat cuts |
| [Stained Glass](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/stained-glass/STYLE.md) | A window seen from a dark hall, alive only where sunlight touches it; light is the clock and the story | Legends, heritage, holiday stories | 2D canvas or WebGL, lead lines plus moving light mask |
| [Swiss Motion Graphics](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/swiss-motion/STYLE.md) | Modular grid, one typeface, one signal colour, movement as exact as a printing press | Brand identity, events, design education | HTML/CSS grid, snap easing |

## Information and keynote

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Circuit Board](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/circuit-board/STYLE.md) | The subject drawn as a PCB from above: routes are traces, places are pads, what flows is light along copper | Energy, supply chains, devices | SVG traces with travelling glow |
| [Dark Tech Keynote](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/dark-keynote/STYLE.md) | Near-black gradient, hairline grid, one accent, UI moving with snap precision, one giant number | Product launches, SaaS, keynotes | HTML/CSS UI scenes, light reveals |
| [Data Storytelling](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/dataviz/STYLE.md) | Real data drawn mark by mark in red and blue pencil on cream paper, handwritten notes pinned to numbers | Data journalism, reports, climate | SVG chart drawn in sequence; real data only |
| [Sci-fi Hologram HUD](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/hologram-hud/STYLE.md) | An object scanned to a glowing wireframe; target boxes lock on, parts explode out, numbers roll into real values | Spec walkthroughs, launches, trade shows | 3D wireframe plus HUD overlay |
| [Isometric Infographic](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/iso-infographic/STYLE.md) | A flat three-tone isometric diorama of a system that opens to show its insides; numbers drawn as icons | Process explainers, supply chains, annual reports | SVG isometric blocks |
| [Isometric Picture Book](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/isometric-picture-book/STYLE.md) | One real place in true isometric, small faceless people acting out an everyday rule, serif type painted on the ground | Everyday rules, queues, comparisons | SVG isometric scene |
| [Living Screencast](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/living-screencast/STYLE.md) | A believable screen recording where a low-res mascot lives inside a sharp interface and acts out what the software does | Product tutorials, feature launches, onboarding | HTML UI plus sprite character; real product UI |
| [Transit Map](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/transit-map/STYLE.md) | A metro schematic on a printed sheet, eight-direction lines drawn by glowing pen tips under a real camera | Transport, growth over time, networks | SVG lines on a 3D-tilted plane |

## Materials and 3D

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Brick Toy](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/brick-toy/STYLE.md) | Stop-motion toy bricks shot like macro photography on a desk, one pose at a time | Toys, product builds, space | 3D, stepped animation on twos; generic bricks, no brand marks |
| [Desktop Flythrough](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/desktop-flythrough/STYLE.md) | App screens as printed cards on a sunny desk, little voxel characters carrying work between them, one flying camera | App explainers, workflows, products | 3D, card planes plus camera path |
| [Glass Product Render](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/glass-product/STYLE.md) | A product in clear and frosted glass on a dark set, strip-light sweeps, caustics, exploded views that snap shut on the beat | Product launches, consumer tech, beauty | 3D, transmission material |
| [Low-poly Isometric Island](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/lowpoly-island/STYLE.md) | A tiny faceted world under an orthographic lens where everything arrives with a bounce and a note | Game trailers, world building, calm content | 3D orthographic, spring pops |
| [Memphis Diorama](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/memphis-diorama/STYLE.md) | A tabletop model in flat Memphis colours with ink outlines and hard purple shadows, inside a grainy frame that grows open | Web heroes, ambient loops, seasons | 3D toon shading or 2D canvas |
| [Paper Pop-up Book](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/paper-popup/STYLE.md) | A pop-up book on a desk as a stage: white-bordered paper actors before sets that spring from the page | Children's books, game trailers, story films | 3D hinged planes, macro depth of field |
| [Tilt-Shift Miniature](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/tilt-shift/STYLE.md) | A real-looking place from high above with a tilted focus band and time-lapse, so it reads as a model | City promos, real estate, transport | 3D scene or footage, blur band plus speed-up |

## Cartoon and anime

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [80s Cel Anime](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/cel-anime-80s/STYLE.md) | Two-tone cels over airbrushed backgrounds, backlit neon, limited animation, played back as worn videotape | Music videos, game trailers, nostalgia | 2D canvas plus VHS/CRT post |
| [Mid-century Cartoon](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/midcentury-toon/STYLE.md) | 1950s flat colour printed off its broken ink line, still bodies with busy hands, colour-block rooms, cool jazz | Set-up guides, help centres, how-to | SVG limited animation |
| [1930s Rubber Hose Cartoon](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/rubber-hose/STYLE.md) | Black-and-white hand-inked cartoon where every object is alive and swings to hot jazz | Food and drink, retro ads, kids | SVG bendy limbs, loop cycles; own characters only |
| [Sci-Fi Sitcom Toon](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/scifi-toon/STYLE.md) | Thick wobbling outlines, flat colour, a mismatched duo, a glowing portal, one palette per world | Comedy, tech brands, social shorts | SVG boil lines; original characters only |

## Cinema and eras

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Liminal Found Footage](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/backrooms/STYLE.md) | Recovered camcorder tape from endless fluorescent-lit empty rooms; rules instead of monsters | Horror, mystery, game teasers | 3D corridors plus camcorder post |
| [1920s Silent Film](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/silent-film/STYLE.md) | Engraved-style pictures in a flickering 4:3 print between curtains, intertitles, a cinema pianist on every beat | Comedy, retro brands, silent storytelling | 2D canvas plus film-weave post |

## Games

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Game Show Flat](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/game-show/STYLE.md) | Toy-like mascots on candy stripes and sunbursts, every hit on a fixed tempo grid, a judgement word per round | Tech timelines, year in review, variety | SVG on a beat grid |
| [HD-2D](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/hd-2d/STYLE.md) | Pixel sprites standing like cut-outs in a lit, foggy 3D diorama under a tilt-shift lens | Game trailers, fantasy, story films | 3D with billboard sprites |
| [Microgame Frenzy](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/microgame/STYLE.md) | Rapid party-game rounds, one command word each, each round in a different art style, ever faster | Game trailers, onboarding, social shorts | 2D canvas, scene per round |
| [16-bit Pixel RPG](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/pixel-rpg/STYLE.md) | A mid-90s console role-playing game at 320x180: limited palette, typing text boxes, menus, chip music | Game trailers, recaps, nostalgia | 2D canvas at low resolution, nearest-neighbour upscale |

## Evidence films (need real material)

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Satellite Briefing](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/satellite-briefing/STYLE.md) | Real satellite imagery graded to analyst grey, thin white measurements and one continuous zoom | Climate, news explainers, geography | 2D canvas, stacked image plates; licensed imagery |
| [Engineering Briefing Board](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/briefing-board/STYLE.md) | A real whiteboard wall: photo cut-outs land with weight, magnets, stamps and three-colour marker draw on it | Engineering, option comparisons, briefings | 2D canvas, photo cut-outs plus marker strokes |
| [LiDAR Survey](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/lidar-survey/STYLE.md) | Real laser-scan points float in the dark, then condense into a lit surface measured with hairline tools | Heritage, environment, site surveys | 3D point cloud; public scan data |
| [Projection on White Model](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/white-model/STYLE.md) | A white massing model of a real place in a dark room, data projected onto it one layer at a time | Urban planning, exhibitions, city data | 3D, projected textures |
| [Data Physicalization](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/data-physical/STYLE.md) | Real statistics as stacked physical pieces to exact scale, lit like a studio product shot | Annual reports, investor decks, energy data | 3D instanced objects; real data only |
| [Exploded Teardown](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/teardown/STYLE.md) | A real product from its engineering files, lit as a packshot and lifted apart layer by layer with named parts | Hardware launches, product pages, specs | 3D from the client's CAD |
| [Microscope Story](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/microscope/STYLE.md) | Licence-clean microscopy and one continuous change of scale from slide to single cell, focus breathing on each step | Biomedicine, materials, skincare science | 2D canvas, image pyramid zoom |
| [Archive Light Table](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/archive-lighttable/STYLE.md) | Archive objects on a backlit table; a loupe comes down and the object comes alive inside the glass | Brand history, archive stories, museums | 2D canvas, loupe mask over scans |

## Edit and documentary (cut from real footage)

| Look | What it looks like | Suits | Build |
| --- | --- | --- | --- |
| [Caption News](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/caption-news/STYLE.md) | Sound-off social news: huge captions slammed in chunks with one keyword on a yellow block over real footage | Social news, report explainers, data shorts | HTML captions over footage; see [caption studio](../../caption-studio/SKILL.md) |
| [1920s Newsreel](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/newsreel/STYLE.md) | A late-1920s sound newsreel cut from archive: searchlight ident, spinning newspaper, place-and-date cards | History stories, eras, anniversaries | Footage edit plus 2D cards and film post |
| [Live Countdown Split-screen](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/countdown/STYLE.md) | Real footage of an event with a known zero in real time; a clock ticks and the screen splits into more cells | Launches, countdowns, live events | Footage grid with a running clock |
| [Time-lapse Symphony](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/city-symphony/STYLE.md) | A city cut like minimalist music: time-lapse rivers of light, cuts densifying with the score, a hard cut to black | City films, music montages, openers | Footage edit on a beat grid ([motion sync](../assets/motion-sync/README.md)) |
| [Visual Investigation](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/visual-investigation/STYLE.md) | A cold investigation desk: footage, photos, documents and maps of one event on one shared clock | Reconstructions, fact-checks, incident reports | Footage plus synced timeline overlays |
| [Constructivist Montage](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/kino-montage/STYLE.md) | Archive printed as an ink-and-paper poster with one red, diagonal type bands, cut-out people, cut on a machine beat | Industry histories, milestones, collective effort | 2D canvas collage over footage |
| [Sports Telestrator](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/telestrator/STYLE.md) | TV match analysis: play, rewind, freeze and draw rings, arrows and empty-space patches on the picture | Sports analysis, recaps, coaching | Footage plus SVG overlay drawn on freeze frames |
| [Broadcast News Package](https://github.com/lemomo-ai/lemo-opuscar/blob/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00/styles/news-package/STYLE.md) | A newsroom package in code: a sting that becomes the channel bug, a rundown, a permanent lower third, full-frame graphics | News round-ups, bulletins, market updates | HTML graphics package over footage |
