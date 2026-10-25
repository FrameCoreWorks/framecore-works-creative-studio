# Structured (JSON) image prompts

Checked 2026-10-25 on the model owners' own documentation unless a row says otherwise. Read when a user asks for a JSON prompt, when a model's own schema is the target (Bria FIBO, Ideogram 4.x), or when a production needs one record that several prompts and edits are compiled from. The [static prompt compiler](static-prompt-compiler.md) still decides content, order, exact text and edits; this card decides the shape.

## What the evidence says

- **Two model families are trained on a JSON caption format and document it:** Bria FIBO (structured captions of about 1,000 words; [repository](https://github.com/Bria-AI/FIBO), [paper](https://arxiv.org/abs/2511.06876)) and Ideogram 4.0 and 4.5 ("trained on captions in this format"; [JSON prompting](https://docs.ideogram.ai/prompting/json-prompting)). For them, matching the official schema exactly is the evidence-backed choice.
- **One family documents a JSON template but says prose works as well:** Black Forest Labs FLUX.2 ("understands both formats equally well"; [prompting guide](https://docs.bfl.ml/guides/prompting_guide_flux2)). Use JSON there for multi-subject or production scenes and automation, prose for quick work.
- **Others read JSON only as text:** OpenAI gpt-image lists "JSON-like structures" among acceptable formats ("use the format that is easiest to maintain"; [prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)); Google's Gemini image guide gives prose formulas and no JSON guidance ([Nano Banana guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)); ByteDance Seedream asks for natural language ([guide](https://docs.byteplus.com/en/docs/ModelArk/1829186)); Qwen-Image's model receives one prose paragraph (JSON wraps only its rewriter's output); Midjourney does not mention JSON and prefers short prompts ([prompt basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics)); CLIP-based Stable Diffusion models read 77 tokens, which braces and keys waste.
- **No controlled test was found** in which JSON beats equally detailed prose on a model not trained on it. Measured gains come from training on complete captions in a fixed field order (FIBO's ablation; a fixed caption order beat a shuffled one in arXiv 2507.05300). Small practitioner tests on Gemini and FLUX.2 found about the same images (secondary). So JSON's value at prompt time is completeness, a fixed order, templating and changing one field at a time, not the braces.

## The rule Studio follows

1. **Keep one internal record** (below) for the asset: it is the source of truth, easy to diff and to change one field.
2. **Compile it for the target model:** into its official JSON schema where one exists (FIBO, Ideogram), into BFL's template or prose for FLUX.2, and into ordered prose (with labelled segments for complex scenes) for every other model. Put size, aspect ratio, seed, count, quality and colour controls into the tool's parameters, never into the prompt text.
3. **Label what you deliver:** "Studio planning record", "Ideogram native JSON", "FLUX.2 JSON template" or "prompt for {model}". Never present a planning record as a model's official syntax ([Image Prompt rule](../SKILL.md)).

## Internal record (field order matters: earlier fields get more weight)

| Field | Holds | Maps to |
| --- | --- | --- |
| `summary` | One sentence: subject, action, setting, medium | Ideogram `high_level_description` (required), FIBO `short_description`, FLUX.2 `scene` |
| `subjects[]` | Per subject: `description`, `count`, `position`, `relative_size`, `pose` or `action`, `expression`, `clothing`, `orientation`, `relationship`, colours | FIBO `objects[]` (at most 5 prominent), FLUX.2 `subjects[]{description, position, action}`, Ideogram `elements[]` with `type: "obj"`, `desc`, optional `bbox` |
| `text[]` | Exact string in double quotes, never translated, with `location` or box, `font`, `size`, `color` | FIBO `text_render[]`, Ideogram `elements[]` with `type: "text"`, Recraft `text_layout[]{text, bbox}` (V3), quoted text in prose elsewhere |
| `background` | Setting and environment | FIBO `background_setting`, FLUX.2 `background`, Ideogram `compositional_deconstruction.background` (required) |
| `composition` | Framing, layout, negative space, where the text zones are | FIBO `aesthetics.composition`, FLUX.2 `composition` |
| `camera` | `angle`, `distance`, `lens`, `depth_of_field`, `focus` (photographic only) | FIBO `photographic_characteristics`, FLUX.2 `camera{angle, lens, depth_of_field}`, Ideogram `style_description.photo` |
| `lighting` | `conditions`, `direction`, `shadows` | FIBO `lighting{conditions, direction, shadows}`, FLUX.2 and Ideogram `lighting` |
| `color_palette` | Names or `#RRGGBB`, each tied to an object | FLUX.2 `color_palette` (hex tied to objects), Ideogram `color_palette` (up to 16, 5 per element), Recraft `controls.colors` (up to 10), FIBO `aesthetics.color_scheme` |
| `style` | `medium`, `art_style` or photographic look, `mood` | FIBO `style_medium`, `artistic_style`, `aesthetics.mood_atmosphere`; FLUX.2 `style`, `mood`; Ideogram `style_description` (`photo` or `art_style`, not both) |
| `use_context` | What the image is for (poster, ad, UI, packaging) | OpenAI guide, FIBO `context` |
| `references[]` | Index, role (identity, style, structure, product) and what to take from it | Reference rules in the static compiler; limits per model (for example Gemini 14, FLUX.2 [pro] 8 at 1 MP) |
| `edit` | `change` (the target and the change) and `preserve` (a short blanket clause) | OpenAI (repeat the preserve list each turn), Gemini, FLUX Kontext, Seedream, Qwen-Image-Edit, FIBO Refine |
| `avoid` | Exclusions | A real negative field where it exists (Recraft V2/V3, FIBO, Qwen; Midjourney `--no`); FLUX.2 has none, so rephrase positively |
| `params` | `aspect_ratio` or `size`, `seed`, `n`, quality | The tool's parameters, never the prompt |

Leave out a field that does not apply; do not write "N/A". Keep nesting to two or three levels, as the official schemas do.

## Native schemas, exactly as documented

**Ideogram 4.x** ([docs](https://docs.ideogram.ai/prompting/json-prompting)): top level `high_level_description` (required; without it the JSON is read as plain text), `style_description` (optional: `aesthetics`, `lighting`, `photo` or `art_style`, `medium`, `color_palette`) and `compositional_deconstruction` (required: `background`, `elements[]`). An element is `{"type": "obj", "desc": …}` or `{"type": "text", "text": "…", "desc": …}`, each with an optional `bbox` `[y_min, x_min, y_max, x_max]` on a 0 to 1000 scale from the top left and an optional `color_palette`. Put the most important elements first (long JSON can lose its last elements; the box holds 10,000 characters in 4.5). With Magic Prompt on, Ideogram rewrites the JSON; turn it off to use it as written.

**Bria FIBO** ([default caption](https://raw.githubusercontent.com/Bria-AI/FIBO/main/default_json_caption.json), paper table 7): `short_description`, `objects[]` (`description`, `location`, `relative_size`, `shape_and_color`, `texture`, `appearance_details`, `relationship`, `orientation`; for people also `pose`, `expression`, `clothing`, `action`, `gender`, `skin_tone_and_texture`; plus `number_of_objects`), `background_setting`, `lighting{conditions, direction, shadows}`, `aesthetics{composition, color_scheme, mood_atmosphere}`, `photographic_characteristics{depth_of_field, focus, camera_angle, lens_focal_length}`, `style_medium`, `text_render[]` (`text`, `location`, `size`, `color`, `font`, `appearance_details`), `context`, `artistic_style`. The API takes a prose `prompt` and/or a `structured_prompt` and returns the structured prompt (field names of the API from a hosting page, secondary); Refine changes only the attributes an instruction names.

**FLUX.2** ([guide](https://docs.bfl.ml/guides/prompting_guide_flux2)): `scene`, `subjects[]{description, position, action}`, `style`, `color_palette`, `lighting`, `mood`, `background`, `composition`, `camera{angle, lens, depth_of_field}`; the guide's product example adds exact-colour and lens values. Earlier content gets more attention; no negative prompt.

## Pitfalls

- **Silent fallback:** Ideogram reads malformed JSON, or JSON without `high_level_description`, as plain text; Magic Prompt rewrites it. Validate the JSON before handing it over.
- **Length:** long JSON loses its tail (Ideogram); CLIP models stop at 77 tokens. Put what matters first.
- **Conflicts:** a hex palette against a style name, `photo` together with `art_style`, a preserve list against the change target. Resolve them in the record before compiling and state the choice.
- **Over-described preservation drifts:** describing in detail what must stay makes models change it (Qwen's rewriter rules). Use a short blanket "keep everything else unchanged" plus position and type.
- **Negative wording:** "no X" fails on FLUX.2 and Midjourney; use a real negative field or a positive description.
- **Text:** quoted, verbatim, in its own language, early, with font, size, colour and place; spell difficult words letter by letter for gpt-image. Code can leak into an image as visible text (secondary, anecdotal): compile to prose for models that are not JSON-native.

## Unknown on 2026-10-25

Controlled JSON-versus-prose tests for gpt-image, Gemini, Seedream, Qwen and FLUX.2; whether Gemini or gpt-image were trained on structured captions; JSON status of FLUX.2 [klein], FLUX.1 Kontext and any newer FLUX; OpenAI's and Recraft's prompt length limits; Ideogram's element limit; Bria's own API page (it did not load; the hosted page was used).
