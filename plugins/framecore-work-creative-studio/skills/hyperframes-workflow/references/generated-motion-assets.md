# Generated cut-out assets for motion

A coded film can look photographic instead of drawn when its realistic objects come from stills generated for it, cut out cleanly and animated in code. This reference says when to suggest them, how to ask for them, how to get transparency from each generator, and how Studio checks them before and after compositing.

Evidence: a lyric video built on 2026-10-14 from assets the user generated in Gemini. A hand drawn in code was rejected outright; photographic assets on green made a large quality jump; the remaining defects were a visible acrylic plate behind a neon sign, green and dark fringes on glass, chains and chrome, soft close-ups from about 1376 × 768 sources, and garbled text on a generated cassette.

## 1. When to suggest them

Suggest generated assets after the concept is approved, when the film needs realistic objects, products, props, hands or other body parts, close-up macros, real-looking backgrounds or photographic light effects, and the user has no photos or footage. Do not suggest them for kinetic type, flat or illustrated looks, data animation, or when the user supplied the assets. Never draw realistic objects or hands in code: code draws type, shapes, light and interface, not photographs.

## 2. Plan the list from the storyboard

One asset per scene need, each tied to its scenes: the hero object; separate close-ups of parts that move (a woofer, a cassette, a tape path); props for single sections; a background plate with an open area for text; light effects. Note for each asset which parts will move and its largest size on screen including any push-in, because those set the generation rules. Record the list in the [asset manifest](../../asset-manifest/SKILL.md) with generator and model, transparency method, resolution, moving parts and check status.

## 3. Rules for an animatable asset

- **One object per image**, filling most of the frame, at the highest resolution the tool gives. The source must have at least as many pixels as the asset covers on screen at its largest zoom; otherwise plan a smaller size or a shallower push-in. Do not upscale with an AI model unless the user asks.
- **Straight-on, long-lens view** (no strong perspective) for anything animated in parts: reels that rotate, cones that pump, keys that press, needles that move.
- **Moving parts clean and unobstructed:** circles round, windows without glare, displays blank and unlit (code fills them), nothing covering them.
- **No text on objects** unless it is exact approved copy. Generate a label or logo as its own asset with the brand reference, composite it, and check it letter by letter.
- **No brand names, third-party logos or copies** of a specific real product or someone else's photograph; references inform realism only.
- **Consistency:** reuse the first approved asset as the reference for the next (same light, same rim colour). A second state of an asset (a pressed key, side B) is an edit of the first that changes one thing, with identical framing and scale.
- Realism cues that helped: "real studio product photograph, not a 3D render", the lens and aperture, real materials, slight wear, neutral studio reflections.

## 4. Transparency by generator (checked 2026-10-14)

These are fast-moving product facts: before promising transparency for a named tool, check its current documentation through [Research](../../research-evidence/SKILL.md).

| Generator | Real alpha? | Route |
|---|---|---|
| OpenAI GPT Image through the API (`gpt-image-2.5-flare`, `gpt-image-2.5-sunburst`) | Yes: `background="transparent"` with `output_format` `png` or `webp`; JPEG holds no alpha ([API reference](https://developers.openai.com/api/reference/python/resources/images/methods/generate), [cookbook](https://developers.openai.com/cookbook/examples/multimodal/transparent-image-assets-for-campaigns-and-presentations)) | Ask through the parameter, not only in the prompt, and run `check`: a requested transparent background is not guaranteed |
| ChatGPT, Codex's built-in image tool or another wrapper | Unknown per tool: the wrapper must expose and forward the option | Promise nothing; run `check` on the downloaded file |
| Google Gemini image models (Nano Banana family) | No: a "transparent background" comes back white, black or as a painted checkerboard in an opaque file ([Google AI forum](https://discuss.ai.google.dev/t/transparency-issue-in-image-generation-ui-gemini-2-0-flash-experimental-api/74170)) | Never ask Gemini for transparency; use the white and black matte or, for a solid subject, green |

**By material:**

- **Opaque, matte, no green of its own:** native alpha, or flat `#00FF00` ("no green on the subject, no green reflections, generous margin, sharp edges"), then `asset_check.py key` (soft key on chroma distance, despill, 1 px choke).
- **Glass, ice, chrome, smoke, chains, hair, soft shadows, or a subject with green of its own:** native alpha, or difference matting: generate on pure white `#FFFFFF`, then edit that image to "change only the background to pure black `#000000`, keep everything else identical", and run `asset_check.py matte white.png black.png`. It refuses a pair whose subject moved. A matting model (for example BiRefNet) is another route when a connected provider offers it.
- **Light, neon, sparks, glow, flares:** no alpha. Generate on pure black and composite with a screen or add blend. Ask for the light only: "neon tubes only, no acrylic backing, no wall, no frame, no standoffs". A straight-edged plate cannot be blended away; regenerate it.

## 5. Who generates

Probe the host; never assume. With an image-generation tool the host actually exposes (Codex's built-in image tool, or a connected provider), Studio may generate the assets itself, but only after [Tools And Costs](../../tool-routing-cost/SKILL.md) states the provider, model, approximate number of images, cost and what gets uploaded (reference images may include the client's brand), and the user approves the batch. Otherwise give the user one ready prompt per asset, built with [Image Prompt](../../image-prompt-architect/SKILL.md), and continue when the files arrive.

## 6. After the files arrive

1. `python3 asset_check.py check <files> --screen-px <largest size> --zoom <largest push-in>`: real alpha, no painted checkerboard, no green or dark fringe along the edge, enough pixels. A REPAIR names the fix.
2. Matte or key where needed, then check again.
3. Split into animatable parts, grade into the scene (rim light in the scene's colours, contact shadow, matching grain, a little light wrap at the edge) and animate.
4. **In the rendered film**, at the frames where each asset is largest (the peak of a push-in) and at its first and last frames, crop the edges at 2× and look for fringes, halos, a backing plate or softness. A still that passes can still fail in motion; fix by re-keying, matting, regenerating or reframing, and re-render the range. Report the result in the technical verdict.

The [asset check tool](../assets/motion-assets/README.md) documents the commands and their limits.
