# Narrative (prose) image prompts

Checked 2026-10-25 on the model owners' own guides unless a row says otherwise. Read when compiling a prose prompt for a named image model, which is the right form for every model without a native JSON schema (see [structured image prompts](structured-image-prompts.md)). The [static prompt compiler](static-prompt-compiler.md) decides content, locks, exact text and edits; this card decides the order, length and phrasing per model.

## Order of clauses (synthesis of the guides and measured evidence)

1. **Summary sentence:** medium or format, main subject, action ("A flat vector poster of …", "A photorealistic close-up of …"). Ideogram asks for the whole image "as if someone glanced at it for two seconds" first; FLUX.2 "pays more attention to what comes first"; measured: CLIP-style encoders read under 20 tokens effectively ([Long-CLIP](https://arxiv.org/abs/2403.15378)) and over-weight the first sentence ([2602.22419](https://arxiv.org/abs/2602.22419)). **Exception: OpenAI gpt-image** orders scene or background first, then subject, details and constraints.
2. **Purpose** in one clause (ad, packaging, interface mockup, infographic): OpenAI and Gemini ask for it.
3. **Subject details next to their noun:** identity anchors, materials, textures, exact counts ("three", not a plural). Measured: multi-subject prompts drop subjects and bind colours to the wrong object ([Attend-and-Excite](https://arxiv.org/abs/2301.13826)).
4. **Secondary subjects, one sentence each, with position** (left, right, foreground).
5. **Setting.**
6. **Composition and camera:** shot size, angle, lens, depth of field as look cues (OpenAI: camera specs "may be interpreted loosely").
7. **Lighting and mood.**
8. **Style and finish:** medium, palette (hex codes tied to objects on FLUX.2), texture. Describe medium, era and technique rather than naming living artists.
9. **Exact text block:** each string in double quotes, with placement, typeface description, size and colour; letter by letter for difficult words on gpt-image; short strings on Midjourney.
10. **Constraints as positive states** ("an empty street", "sharp focus throughout"), or the model's own exclusion mechanism where it exists.

**Length:** about 30 to 80 words by default (FLUX.2 calls it "usually ideal"; Ideogram 3.0 may ignore words after about 150). Midjourney prefers short prompts. Models with language-model text encoders (gpt-image 2, Gemini, Qwen-Image 2.0, Ideogram 4.5, Recraft V4) accept long prompts; split complex ones into short labelled segments or lines (OpenAI). Every added detail reduces variety (measured: [2406.08482](https://arxiv.org/abs/2406.08482); Midjourney: "fewer details mean more variety, but less control").

**Edits:** name each input by index and role ("Image 1: product photo; Image 2: style reference", Ideogram `@img_1`); one imperative change with a specific noun, no pronouns; repeat the preserve clause every turn ("keep everything else exactly the same"); text as `Replace "OLD" with "NEW", same font and colour`; one change per turn.

## Per model

| Model | Order and length | Exact text | Edits | Exclusions | Rewriter | Source (read 2026-10-25) |
| --- | --- | --- | --- | --- | --- | --- |
| OpenAI gpt-image (2, 1.5) | Scene or background, subject, key details, constraints; state the use; labelled segments for complex requests; no stated limit | Quotes or capitals with font, size, colour, place; letter by letter for hard words; medium or high quality for small text | "Change only X, keep everything else the same", the preserve list repeated each turn; inputs by index | State exclusions and invariants explicitly ("no watermark, no extra text") | Through the Responses API the prompt is revised automatically and returned as `revised_prompt`: read it back | [prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) |
| Google Gemini image (Nano Banana family) | Describe the scene, not keywords: "A photorealistic [shot] of [subject], [action], set in [environment]", then light, angle, lens; purpose and audience | Exact text, its font style and the overall design; Pro for text-heavy work | "Keep everything else exactly the same, preserving style, lighting and composition"; several turns is the recommended way; up to 14 references | Positive states ("an empty, deserted street") | Unknown | [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation), [prompting post](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/) |
| FLUX.2 | Subject, action, style, context; first words weigh most; 30 to 80 words | Quotes with place, style, size, colour; hex as "color #xxxxxx" tied to an object | Imperative change sentence; say how each reference is used; up to 8 references (API) | None supported: phrase positively | Unknown | [FLUX.2 guide](https://docs.bfl.ai/guides/prompting_guide_flux2) |
| FLUX.1 Kontext | Imperative edits ("Change", "Remove", "Replace"), one at a time; name the subject instead of a pronoun; 512 tokens (secondary) | `Replace '…' with '…'` | Keep identity features named ("same face, hairstyle, expression") | Unknown | Unknown | [Kontext](https://docs.bfl.ai/kontext/kontext_image_editing) |
| Ideogram 3.x, 4.x | Summary, subject, pose, secondary elements, setting, light, framing, finish; 3.0 about 150 words; 4.5 up to 10,000 characters but focused is easier | `text that reads "…"`; a logo reads best with one icon and one or two lines | 4.5 with references: the prompt is an edit instruction; `@img_1` | Negative prompt in 3.0 only, never contradicting the main prompt | Magic Prompt rewrites and can translate; on by default; turn it off for literal adherence | [prompt structure](https://docs.ideogram.ai/prompting/prompt-structure) |
| Midjourney (V8.2 default) | Short and simple; subject, medium, setting, light, colour, mood, composition; exact numbers; parameters at the end | Double quotes, Latin script, short phrases | Edit Model phrasing: Unknown | `--no`; "no cake" may still give a cake | None; `--raw` removes default styling | [prompt basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics) |
| Seedream 4.x | Coherent sentences: subject, action, environment, then style, colour, light, composition; concise | Double quotes | Clear target, no pronouns; say what stays; "replace the character in Image 2 with the one from Image 1, in the style of Image 3" | Unknown | Unknown | [Seedream guide](https://docs.byteplus.com/en/docs/ModelArk/1829186) |
| Qwen-Image, Qwen-Image-Edit | Rewriting recommended; edits "may become unstable" without it; 2.0 takes about 1,000 tokens | Quotes; best in Chinese | Short directives; inputs by order or position | `negative_prompt` | Official rewriter (opt-in); some hosts enable it by default | [Qwen-Image](https://github.com/QwenLM/Qwen-Image) |
| Recraft V4 | Short phrases in the examples; 10,000 characters | `text_layout` in V3 only | Prompt describes the filled area | `negative_prompt` in V2 and V3 only | Optional paid enhance call | [Recraft docs](https://www.recraft.ai/docs/llms-full.txt) |
| Adobe Firefly | At least three words; subject, descriptors, keywords; do not write "generate" or "create" | Unknown | Unknown | Unknown | Unknown | [Firefly prompts](https://helpx.adobe.com/firefly/web/work-with-images/generate-images/writing-effective-text-prompts.html) |
| Stable Diffusion (CLIP models) | Natural language; CLIP sees 77 tokens and uses under 20 well: essentials first | Short, in quotes (secondary) | Unknown | `negative_prompt` | None | [Long-CLIP](https://arxiv.org/abs/2403.15378); the SD 3.5 guide returned 404 |

## Pitfalls

- **Keyword soup** ("girl, umbrella, oil painting"): Gemini and Seedream ask for sentences. Midjourney and Firefly accept short phrases; there the failure is a long list.
- **Chatty instructions** ("Show me a picture of …") on Midjourney; "generate" or "create" on Firefly.
- **The tail is lost:** CLIP's short window, Ideogram 3.0's 150 words, Kontext's limit. Essentials first.
- **Negative wording** brings the object in. Positive states, or the real exclusion field.
- **Contradicting styles** ("photorealistic flat vector") and quality filler ("8K", "masterpiece"): OpenAI says camera and light terms steer realism better.
- **Rewriters change intent:** Ideogram Magic Prompt, OpenAI's `revised_prompt`, Qwen's and Recraft's enhancers add details, shift who is shown or translate (measured: [2504.11104](https://arxiv.org/abs/2504.11104), [2512.04981](https://arxiv.org/abs/2512.04981)). Turn them off for exact copy or a locked brief, or read the revised prompt back.
- **Drift over many edits:** repeat the preserve clause; on Gemini, restart with a full description when it drifts.

## Unknown on 2026-10-25

Whether Gemini rewrites prompts internally and its and gpt-image's length limits; the current Stable Diffusion 3.5 guide (404) and its T5 limit; Midjourney V8's edit phrasing; Seedream's exclusions; Firefly's text and edit guidance; Recraft V4's prose formula. The clause order above is a synthesis, not a measured optimum for closed models.
