# Reconstructing an image in a prompt

Use this when the user gives an image (a photograph, a poster, an illustration) and asks for a prompt that recreates its effect, often with their own face, character, animal or product put in. The method is adapted, in general form, from the owner's reverse-engineering project knowledge (2026-10-15). It analyses an image; it never copies a protected work or a person.

## 1. Three roles of an image

| Role | Where it is used | What comes from it |
|---|---|---|
| Model image | In the conversation, during the analysis and later comparisons | A written description of the composition, palette and every property the effect depends on |
| REF | In the generator, uploaded by whoever runs the prompt | Only the agreed features of a person, animal, product or object |
| Result | In the conversation after a generation | The differences, and the basis for a corrected prompt |

The model image never takes a REF number and is never asked for as a generator upload. Two model images merged into one scene with one person's photo mean a single REF 1. The REF of a future user may not exist yet: say what it is the source of, and never describe their face, hair, age or colouring from the person in the model image, and refer to them by their REF label or as "they", not with the model person's gender. A feature not visible in their photo cannot be promised.

Map the REF roles before the analysis, for example: one person in a new scene (REF 1: face, hair, body proportions; clothing, pose, setting, light and framing come from the model image); a person and an animal (REF 1 and REF 2, each with its own features, scale and contact described). The user decides which features transfer.

## 2. Find the mechanism first

Name what the effect cannot lose: a hand wrapped over an invisible edge is not a hand lying beside a white rectangle; a face half covered by translucent paint is not a face placed between letters. Then pick the medium profile from the image itself, without turning an illustration into a photograph or a flat poster into a 3D render:

| Profile | Describe | Do not impose |
|---|---|---|
| Realistic person | identity from REF, anatomy, pose, skin, hair, clothing, light; framing, position, scale, perspective, contact, occlusion | a full figure or an uncovered face where the image crops or hides it |
| Poster or flat graphic | hierarchy, exact lettering, colours, shapes, negative space; 2D layout, axes, margins, alignment, layer order | a camera, lens, depth of field or 3D perspective that is not part of the effect |
| Product | geometry, proportions, construction, materials, label, colour roles; orientation, visible faces, contact | invented accessories or construction |
| Animal | species and look from REF, coat, proportions, pose, behaviour; body, paws, head, contact | human anatomy or clothing unless agreed |
| Illustration | line, shapes, level of simplification, palette, shading; graphic relations and conventional space | skin pores, photographic optics, physical realism against the medium |
| Hybrid (a photographic poster) | each layer's own properties and how the layers meet | photographing the whole poster as a paper mock-up when it is a flat finished design |

When the effect is optical (a mirror, glass, water, a shadow, a lens blur), describe its physical cause, because a generator builds what the words say. A person seen in a mirror is a reflection: their image lies as far behind the glass as they stand in front of it, so a person farther from the mirror than the camera looks smaller, sits inside the reflected room with space around them, shares the scene's light and perspective, and never touches or leans on the rim; the reflected wall is another part of the room, so its marks do not run straight across the rim. "A window onto another world" or "a portrait inside a frame" builds a framed print, so use such words only when the image really is that (the owner's mirror portrait, 2026-10-15).

## 3. Describe the space as relations

- Frame edges and what each one crops; positions and sizes against width and height; distances, points of contact and the direction of forces; what is in front of what and what hides part of a figure; the empty space, not only the filled one; the hand, wrist and forearm as one continuous limb; the difference between the figure's pose and the camera's perspective.
- Coordinates from the viewer's side: x from the left, y from the top, and never mix shares of width and height. "The person's left hand" is the anatomical side; say which one you mean.
- For each figure, which way the face turns and the eyes look (to the viewer's left or right, up or down, at the camera or past it), its expression, and how the gazes relate (towards each other, away from each other, the same way). Look again before writing it: a reversed gaze breaks the image as much as a wrong pose.
- Camera: its height against the subject (looking up, level, down), its distance, and the lens the perspective shows (converging lines, how large near things look against far ones, how compressed the background is), stated as an approximation.
- For a group of repeated elements (hands, objects), keep an internal record per element: where it enters the frame, start and end, length, axis, rotation, gesture, crop, neighbours and what covers what. Carry their real irregularity (unequal gaps, angles, scales) into the prompt; do not turn it into a fan, an even row or one vanishing point, and do not ask for every finger to be clear where the image overlaps them.
- A partly hidden figure: give the width of the visible part against the frame, its vertical extent, the visible side of the face and the edge that covers it. Do not add a shoulder or a torso the image does not show.
- Focus per element: say which face, hand or object is sharp and which is soft, and how soft. Do not assume the nearest face is the sharp one; generators make it sharp unless told otherwise, so a soft near face and a sharp far one must be stated in the body and again in the closing lock.
- Surface and finish as seen: soft contours, tonal range, lifted blacks, rough cut edges, local blur, print texture. Do not add "clean high-resolution studio photograph" to a soft image, and do not claim a historic technique you cannot confirm.
- Merging several model images, or changing the ratio, is a new agreed composition with chosen elements kept faithfully, never a 1:1 copy.
- When a needed property is ambiguous (a gesture, a count of overlapping limbs, a word), ask one concrete question instead of inventing precision.

## 4. Colours with roles, measured when possible

When a shell or code execution is available, run the [image probe](../../output-critic-iteration/scripts/image_probe.py) before writing the analysis; do not estimate what you can measure. `image_probe.py image.jpg --analyze` gives the colour fields with near-identical shades merged, small accents (a red sign, a white hat) apart from them, the black and white points, the tonal range, the colour character (monochrome, muted or saturated; warm, neutral or cool), a 4 × 4 focus grid (sharpest cell 100: compare cells that hold similar subjects, such as two faces), a 3 × 3 brightness grid with the brighter side as a lead for the light's direction, and, on a plain background, where the subject sits in percent of width and height. A colour profile such as Display P3 is converted to sRGB first. These are the stored file's values; light and compression shape them, and a screenshot adds its own. The measurement supports the look at the image; it does not replace it. Give each colour a role (background, fabric, shadow, light, glass) instead of a bare list of codes. Without a measurement write approximations ("warm off-white background, approximately #F3F2EF"). Keep an agreed palette through later corrections unless a result gives a reason to change it. Keeping a REF person's identity does not carry over the model person's skin or hair colour; resolve such a conflict in the text (for a monochrome effect: the REF identity rendered in greyscale).

## 5. Write the prompt

Settle the direction, medium, REF map and any conflicting requirement before writing; never leave the generator to choose between contradictory variants. The prompt is a standalone instruction for one image: no placeholders, no A/B alternatives, nothing that depends on the conversation. Fill every part with what this task needs and leave out fields that do not apply. Name an absence only when it protects the effect.

Format: narrative prose for the named generator by default ([the compiler](static-prompt-compiler.md) and the model's current guidance). When the user supplies their own structured template, fill it exactly: keep its headings, order, ornaments and limits (length, one line), adapt only the content to this image, and never invent a template of your own for them. When the user says they work with a template but has not given it, ask for it. With a length limit, count the characters with a tool where one is available and give the count; otherwise say the length is an estimate.

Before giving it, check it against the image, not only for complete headings: nothing opposite to the model image ("all clearly separated" against overlap, a radial cluster against an irregular group, a full face against a narrow reveal, studio sharpness against a soft finish), the REF roles, the count of figures, the ratio, the palette and the spatial relations, and that someone with only the prompt and the declared REF could produce the scene. This checks the prompt, not a generation.

## 6. After a generation

Compare what is visible: framing, count and arrangement, pose, gestures and contact, palette, light, materials, style, lettering and the agreed identity. A different person or animal from the REF is not an error when that swap was the aim. Fix first what breaks the mechanism (the wrong side of the frame, a missing occlusion, a wrong gesture, swapped references), then scale, colour and light, then texture. Keep settled decisions; do not solve one problem by changing the whole scene. Tell apart a missing analysis, a conflict in the text and a correct instruction the generator ignored. Generators drift towards their defaults: a profile turns towards the camera, a serious face smiles, a tight crop gains headroom, both faces come out sharp, an object held at an angle turns flat to the camera, a hand on an edge becomes a simple grip. Check these first and restate the ones that drifted as concrete, positive positions (the owner's Nano Banana result of the mirror portrait, 2026-10-15). Give a full corrected prompt for the original REF, not an edit instruction for the previous result, and never state a percentage of likeness without a method that was actually applied.

When the user moves the work to a new conversation, give a short handoff: the model image's role, the REF map, the agreed mechanism, palette, format and limits, and the current full prompt.

## Rights and people

Reconstructing composition, light, colour and finish is analysis. Do not promise a 1:1 copy of a recognisable photograph or artwork for publication, and do not put a real person's face in without that person's photo supplied as REF by someone entitled to use it. Text, logos and trademarks in the model image are reproduced only when the user owns them or the task is clearly private study.
