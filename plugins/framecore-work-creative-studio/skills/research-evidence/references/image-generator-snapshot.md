# Image-generator families: audited snapshot

Snapshot date: 2026-09-24. Owner: `research-evidence`. Purpose: a dated reference for choosing and prompting current image-generation families, not a live market census or directory, performance ranking, exhaustive census of every endpoint, or guarantee that a model is exposed in this Studio's host.

## How to use this snapshot

When a user names a generator, first identify the exact product/model/version and the surface they actually mean. If the surface is not named, treat the named consumer product as the target; do not interrogate the user about API or wrappers. Ask a narrow clarification only if two plausible versions materially change the prompt. If the user explicitly names an API, third-party service, local UI, or wrapper, map that surface separately. The capability of a model family does not prove that the user's account, a reseller, or this plugin exposes it.

Before delivering a current model-specific prompt, recheck that model's official documentation or release note and search for attributable first-hand practitioner tests dated close to the task. This file provides a starting map and stable distinctions, not permission to skip fresh research. Translate evidence into only the prompt decisions it supports. Never claim a prompt was tested unless that exact prompt and output were actually generated and inspected.

Use these operation labels literally:

- **T2I**: text-to-image generation.
- **I2I/edit**: an existing image is an explicit source to be changed. A product's generic “edit” wording needs an operation-specific source before being classified as such.
- **Reference-led**: one or more images guide identity, style, content, structure, or composition. “Reference image” is not one interchangeable control.
- `documented` means the cited source describes that operation on the named surface. `partial` means the family supports it somewhere but this record cannot establish equivalent behavior across variants/surfaces. `unknown` is not a yes.

## Coverage snapshot

The 19 cards below cover prominent hosted products and model families surfaced in the current official documentation and dated comparative/practitioner searches. Coverage is intentionally a finite, auditable sample, not a claim that these are all commercially available image models or that the list is ranked. Smaller launches, private betas, regional surfaces, model aggregators, research checkpoints, and rapidly changing aliases may be absent. The watchlist records notable surfaced candidates that do not yet meet this snapshot's evidence threshold. No prices, entitlement promises, legal-use conclusions, or plugin execution capability are asserted.

| Family | Variants/identity recorded on 2026-09-24 | T2I | I2I/edit | Reference-led | Evidence status |
|---|---|---:|---:|---:|---|
| Gemini image / Nano Banana | 3.1 Flash Image (Nano Banana 2); 3 Pro Image (Pro); 3.1 Flash Lite Image (Lite); 2.5 Flash Image (earlier) | documented | documented | documented, variant limits | Official API guide; partial practitioner comparison |
| GPT Image | GPT Image 2.5 `sunburst` / `flare`; keep ChatGPT image surface distinct | documented | documented | documented in API guide | Official API guide; user test evidence is predecessor 2.0 only |
| Black Forest Labs FLUX | FLUX.2 Max, Pro, Flex, Dev, Klein; FLUX.1 Kontext is a distinct editing lineage | documented | documented for specified FLUX.2 edit routes; variant-specific | documented for supported FLUX.2 routes | Official family guide; partial platform-mediated practitioner tests |
| Seedream | Seedream 5.0 Pro; older 4.x/5.x names can remain exposed by surfaces | documented | documented | documented in official demo/guidance; exact service controls vary | Official release/guidance; partial user comparison |
| Qwen Image | 2.1; 3.0 and 3.0 Pro API IDs `qwen-image-3.0` / `qwen-image-3.0-pro` | documented | documented | documented, exact reference ranges are surface/version-specific | Official blog/model card/API guide; partial local and API-surface practitioner studies |
| Midjourney | V8.2 default per official version page | documented | documented in web Editor, distinct from initial generation | documented, separate image/style/edit carriers | Current official docs; partial practitioner comparison |
| Ideogram | 4.0 | documented | partial, product/editor functions must be checked by exact operation | documented style/character/reference functions vary by surface | Official release and JSON prompting guide; partial comparison |
| Recraft | V4.1 and V4.1 Flash; Vector/Utility are separate product paths | documented | partial: “Refine” is not a synonym for unrestricted image editing | documented where exact control is exposed; verify version | Official release notes; no qualifying independent current V4.1 test found |
| Krea | Krea 2 / Krea 2 Turbo; model catalog may expose other providers too | documented | unknown for native general I2I in this snapshot | documented style reference/moodboard guidance | Official product/technical sources; one partial platform-mediated user test |
| Meta Muse Image | API identifier `muse-image-1.0`; consumer Meta surfaces may vary by region | documented | documented in API docs | documented in API docs; surface access differs | Official docs; partial single comparative report |
| Microsoft MAI Image | MAI-Image-2.6 and Flash; exact API identifier not established here | documented | documented at product level; exact operation/surface needs fresh check | partial/unknown by exact surface | Official product page; partial test through an intermediary |
| Tencent image generation | Cloud `Hy-Image-3.0` `hy-image-v3`; `Hy-Image-3.5-Preview` `hy-image-v3.5-preview`; separate open-weight `HunyuanImage-3.0` and `HunyuanImage-3.0-Instruct` checkpoints | documented | documented for named Instruct/3.5 routes; not equivalent across names | documented, exact limits differ by route | Current TokenHub docs and separate checkpoint repository; partial open-model user report; no qualifying 3.5 report |
| Reve | Reve 2.1; exact API model identifier not verified | documented | documented at product level | documented by separate References feature; exact surface matters | Official launch/reference docs; partial intermediary comparison |
| xAI Grok Imagine | Image 2.0 `grok-imagine-image-2.0` | documented | documented | documented in current API docs, up to five references there | Official capability/release docs; partial native-app comparison |
| Stability AI / Stable Diffusion | Stable Diffusion 3.5 family; checkpoints differ from hosted services | documented | service/workflow dependent; do not attribute every editing service to the checkpoint | workflow dependent | Official family/service docs; no qualifying current independent 3.5 report found |
| Z-Image | Z-Image foundation model; Z-Image-Turbo checkpoint | documented for public checkpoint | unknown in official checkpoint record used here | unknown | Official model repository; partial user prompt/consistency evidence via a third-party surface |
| Leonardo | Phoenix 1.0 (`phoenix-v1.0`), Phoenix 0.9; Lucid Origin (`lucid-origin`); Leonardo is also a multi-model surface | documented | documented for Phoenix; not established for Lucid Origin in this audit | documented, typed controls differ by model | Official model/API guides; partial Lucid Origin user comparison; no qualifying exact Phoenix 1.0 comparison |
| HiDream | HiDream-O1-Image and separate Dev variant | documented | documented | documented for multi-reference subject personalization | Official repository/model card; partial local Dev report |
| GLM Image | Open checkpoint `zai-org/GLM-Image`; separate hosted Z.AI API model `glm-image` | documented | documented for open checkpoint; not established for hosted API here | documented for open checkpoint, API surface differs | Official repo/API docs; partial practitioner poster study |

## Prompting principles that transfer across families

1. Start from the image's job, not a pile of style adjectives. State the subject, intended viewer response, visual mechanism, focal hierarchy, spatial relationships, environment, and the one or two details that must survive iteration.
2. Separate immutable facts from visual interpretation. Copy, logos, product geometry, identity, and source-of-truth details must be explicitly locked; never let a stylistic reference silently replace brand or product truth.
3. Specify visible text verbatim, in its final language and capitalization. Give the requested line breaks or relative hierarchy only where the target surface can interpret them. Verify spelling, punctuation, count, and placement in the actual output; strong text rendering claims are not a guarantee.
4. Describe composition with observable relationships: where the focal object sits, what overlaps it, how much negative space remains, the reading path, crop, distance, and placement of copy. Do not rely on “professional,” “beautiful,” or “cinematic” to supply missing design decisions.
5. Give each reference one role: identity, product, style, layout, material, or edit source. State what may transfer and what must not. A tool's reference slot, style preset, image prompt, edit canvas, and source-image input are not equivalent.
6. Prefer a small, intentional instruction set. Remove duplicated synonyms, contradictory aesthetics, generic negative lists, and implementation syntax that the selected surface does not accept. Use negative prompts or structured fields only when verified for that exact model/version/surface.
7. Distinguish initial generation, inpainting, global edit, reference-conditioned generation, outpainting, and upscaling. For edits, name the target change, preservation set, allowed physical side effects, and the observable acceptance test.
8. Match the prompt to the target operation, not to a universal template. A text-to-image prompt, an image edit instruction, and a structured API payload have different jobs. Never provide API fields when the user requested a normal prompt and did not name an API.
9. For poster-like work, make text hierarchy and image hierarchy cooperate. Do not ask the image model to solve content strategy, factual claims, typography, production specs, and complex artwork as one undifferentiated sentence.
10. Treat a first output as evidence only for the exact model/surface/settings and task used. Iterate one primary issue at a time and retain accepted elements; do not turn one success, failure, leaderboard score, or anecdote into a universal rule.

## Family cards

### Family: Gemini image / Nano Banana

- **Variants:** `gemini-3.1-flash-image` (Nano Banana 2), `gemini-3-pro-image` (Nano Banana Pro), `gemini-3.1-flash-lite-image` (Lite), and older `gemini-2.5-flash-image`. “Nano Banana” is a product nickname, not proof that app, API, and third-party routes use identical model IDs or settings.
- **Surface and operations:** Google Gemini API guide documents T2I, image editing, and conversational multi-turn image work. The guide distinguishes versions; do not map API behavior automatically to the consumer Gemini app. Lite is not optimized for multi-reference or multi-turn workflows in the guide. Exact reference capacities depend on the current model/version documentation.
- **Prompt guidance:** State the intended final image, use precise spatial and edit instructions, identify each input by role, and separate “change” from “preserve.” For exact visible copy, quote and verify the literal string and line structure. Keep request formatting aligned with the surface rather than injecting API schemas into a chat prompt.
- **Practitioner evidence:** TGK's dated multi-model comparison tested Nano Banana Pro and 2 through WaveSpeed on shared core briefs and reported first outputs; useful but partial, intermediary-mediated, with no incoming references in its controlled text-to-image set and incomplete low-level settings.
- **Unknowns:** Account entitlements, app/API parity, regional availability, exact maximum reference behavior by current version, and any user-specific generation result require fresh verification.
- **Sources:** [Gemini API image generation guide](https://ai.google.dev/gemini-api/docs/image-generation); [TGK multi-model comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: GPT Image

- **Variants:** Official current API model names found in this snapshot: `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare`. Keep the ChatGPT image-generation surface separate from API model identifiers; never promise that a Custom GPT or plugin can select either ID.
- **Surface and operations:** API documentation covers generation, image editing, and reference inputs. Treat supported parameters and quality modes as API-specific. ChatGPT's visible image tool is a separate surface whose currently selectable behavior must be checked in that host.
- **Prompt guidance:** Specify the intended result and exact image-edit target; preserve the user's copy and source-image constraints. Do not emit endpoint fields or assume that model selection, size, output format, or reference limits exist in a normal chat surface.
- **Practitioner evidence:** TGK tested GPT Image 2 (not 2.5), mainly through WaveSpeed, and separately inspected ChatGPT. This is predecessor evidence only, not evidence for the two 2.5 variants. Its controlled core T2I set did not use reference images.
- **Unknowns:** No qualifying practitioner comparison for 2.5 was found in this snapshot. Current ChatGPT model routing, UI parity, account access, and exact controls are unverified here.
- **Sources:** [OpenAI image generation guide](https://developers.openai.com/api/docs/guides/image-generation); [OpenAI models](https://developers.openai.com/api/docs/models); [TGK comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: Black Forest Labs FLUX

- **Variants:** FLUX.2 Max, Pro, Flex, Dev, and Klein have distinct hosted/open-weight or endpoint boundaries. FLUX.1 Kontext is a separate edit-oriented lineage, not a synonym for the FLUX.2 model group.
- **Surface and operations:** The official FLUX.2 overview and API guides document T2I and multi-reference editing for stated routes; controls, reference counts, availability, and licenses vary by variant. The specific FLUX.2 Pro/Max prompting guidance says not to use negative prompts for those targets; do not generalize that advice to every FLUX model. The Klein guide emphasizes descriptive prompts and does not have prompt upsampling.
- **Prompt guidance:** For supported variants, assign reference images explicit roles and map important colors to the objects that should receive them. For complex constraints, use a clear structured description; only use a machine-readable payload when the named surface actually accepts it. Prefer desired positive content over an unsupported negative-prompt block on Pro/Max.
- **Practitioner evidence:** getimg.ai's August 2026 test compared Max/Pro/Klein with shared prompts and prompt enhancement off, but via its commercial surface, one attempt per brief, and without a complete reproducible seed/parameter table. This is partial, not a native BFL benchmark.
- **Unknowns:** Current input limits and edit behavior must be rechecked for the exact variant and endpoint; do not use sibling-version behavior as a substitute.
- **Sources:** [FLUX.2 overview](https://docs.bfl.ai/flux_2/flux2_overview); [FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2); [getimg.ai practitioner comparison](https://getimg.ai/blog/ai-realism-test-comparing-realistic-image-generation-models).

### Family: Seedream

- **Variants:** Seedream 5.0 Pro is the current high-capability variant identified in the July 2026 provider release. Older 4.x or other 5.x variants can remain surfaced by apps/aggregators; verify the exact selected variant rather than assuming the family label means 5.0 Pro.
- **Surface and operations:** Official provider pages demonstrate T2I, editing, multi-reference, and layout/region-level work, but an announcement or demo does not establish identical controls on every ByteDance/third-party surface. No exact API identifier was confirmed in the official pages checked for this snapshot.
- **Prompt guidance:** Give concise design intent, exact copy and clear spatial hierarchy; localize an edit to the named region and explicitly preserve unaffected regions. Treat reference roles and layout constraints as input-specific, not a generic guarantee.
- **Practitioner evidence:** TGK tested Seedream 5.0 Pro through WaveSpeed at a stated 2K JPEG setup using shared core briefs; it is a useful first-output comparison but not a reference-image test or a full parameter-complete replication.
- **Unknowns:** Exact current model IDs, available editing controls, region masks, and account/surface behavior require fresh source checks.
- **Sources:** [Seedream 5.0 Pro](https://seed.bytedance.com/en/seedream5_0_pro); [provider introduction](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro); [TGK comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: Qwen Image

- **Variants:** Qwen-Image 2.1 has official model/API material. Qwen-Image 3.0 and 3.0 Pro appear in the current Alibaba Cloud Model Studio API guide; the Qwen consumer Studio/announcement and hosted API are separate surfaces.
- **Surface and operations:** Official API documentation lists T2I and I2I/edit for 3.0 and 3.0 Pro with 1–3 reference images. The 2.1 model guide describes up to ten references and localized annotation/mask edit workflows. Do not transfer 2.1 controls, reference counts or user findings to 3.0. Check each exact UI/service before compiling API fields.
- **Prompt guidance:** Name the exact edit target, state which image supplies which property, and isolate local changes from preserved composition. Mark and mask controls only where the chosen surface implements them; do not write assumed mask syntax into a plain-language prompt.
- **Practitioner evidence:** Loop Forge's September 23 local 2.1 study covers 26 prompts, multi-source references, and edits; its sampler/seed record is incomplete. NanoGPT's July 23 Qwen-Image 3.0 review describes four poster/text/edit trials, fixed seeds, a 1024-pixel long side, and prompt expansion disabled for some trials, but uses its own service and an 800-character limit. These reports are partial, not universal quality evidence.
- **Unknowns:** Exact parity between Qwen Studio and Model Studio API; prompt expansion defaults; account access; and current 3.0/Pro UI controls require surface-specific rechecks.
- **Sources:** [Qwen-Image 2.1 official guide](https://qwen.ai/blog?id=qwen-image-2.1); [2.1 model card](https://huggingface.co/Qwen/Qwen-Image-2.1); [Qwen-Image 3.0 announcement](https://qwen.ai/blog?id=qwen-image-3.0); [Alibaba Cloud API reference](https://www.alibabacloud.com/help/en/model-studio/qwen-image-generation-and-editing-api-reference); [Loop Forge 2.1 study](https://loopforge.cc/projects/qwen-image-2-1/); [NanoGPT 3.0 review](https://nano-gpt.com/blog/qwen-image-3-review-text-rendering-editing).

### Family: Midjourney

- **Variants:** V8.2 became the default on July 24, 2026 according to Midjourney's current version documentation. Features and reference types changed across versions; do not reuse a V8.1 weight table as a V8.2 fact.
- **Surface and operations:** Official docs distinguish initial image prompts, style references, moodboards, and the web Editor's inpainting/outpainting/retexture tools. These carriers have different intent; an image prompt is inspiration and does not guarantee a copied layout or object.
- **Prompt guidance:** Describe the desired final image instead of issuing an edit command when the input is an inspiration Image Prompt. For Edit Model tasks, state the actual local change and preservation goal. Use only V8.2-supported controls confirmed in current docs; keep weights out unless documented for that version.
- **Practitioner evidence:** TGK tested V8.2 via Midjourney's own web surface, with a first output selected from a four-image batch. It is partial comparative evidence and does not test incoming references in its controlled T2I brief.
- **Unknowns:** Account/UI rollouts and precise version-specific reference weights require current verification.
- **Sources:** [Version documentation](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version); [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts); [Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor); [V8.2 release](https://updates.midjourney.com/version-8-2/); [TGK comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: Ideogram

- **Variants:** Ideogram 4.0 is the release audited here. Older help-center instructions can refer to earlier versions and must not be presented as v4 behavior unless confirmed.
- **Surface and operations:** Official release materials describe T2I and an open model/API path. Style, character reference, and editing features are surface/tool-specific; general I2I equivalence is not established by the version announcement.
- **Prompt guidance:** Ideogram's prompting guide says structured JSON-style prompts can express precise text, layout, and color. Use this structure only on a surface/model that accepts it. Keep the visible copy exact, short enough for the requested use, and separately inspect typography and layout in the actual result.
- **Practitioner evidence:** TGK tested 4.0 through WaveSpeed, using shared briefs and a 2K High JPEG selection. It gives visible first-result limitations and one prompt wording adjustment, but has no incoming references in the controlled T2I set and is not a native UI comparison.
- **Unknowns:** Exact equivalence between JSON guidance, v4 model, and each app/API feature requires checking the current official surface docs.
- **Sources:** [Ideogram 4.0 release](https://ideogram.ai/news/ideogram-4.0/); [Ideogram 4 JSON prompting](https://ideogram.ai/blog/ideogram-4-json-prompting/); [TGK comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: Recraft

- **Variants:** Recraft V4.1 and V4.1 Flash are distinct models; Vector, Utility, and other product modes are not aliases for a single image model.
- **Surface and operations:** Studio and API expose model-specific controls. Provider documentation describes T2I and follow-up “Refine”; do not describe Refine as unrestricted I2I editing. Verify each current reference and edit control against its exact surface.
- **Prompt guidance:** Use a concise design objective and concrete visual relationships. If the task is vector output or utility work, select that specific mode instead of describing a raster-style aesthetic and assuming the model will infer it. Never promise a generated file is an editable vector or press-ready master without checking the output artifact.
- **Practitioner evidence:** No qualifying independent, reproducible current V4.1 or Flash user comparison was located. Recraft's own comparison is vendor-authored, so it is product information, not independent confirmation.
- **Unknowns:** Current reference/edit limits and independently observed result behavior remain open.
- **Sources:** [V4.1 release](https://www.recraft.ai/blog/recraft-v4-1-more-beautiful-by-nature); [V4.1 Flash](https://www.recraft.ai/blog/meet-recraft-v4-1-flash).

### Family: Krea

- **Variants:** Krea 2 and Krea 2 Turbo. Krea's model library can expose third-party families as well; selecting the platform name alone may not identify the underlying model.
- **Surface and operations:** Official Krea 2 materials describe T2I and style references/moodboards. Native, general-purpose I2I editing was not established in the docs checked here; do not infer it from the platform's general editing toolbox.
- **Prompt guidance:** For a series, preserve a compact identity description and change only the shot-specific variables. Keep style-reference influence separate from identity/content constraints, then inspect each output for identity drift. This is a testable workflow hypothesis, not a guarantee.
- **Practitioner evidence:** A September 15 Krea 2 Turbo vs Z-Image Turbo post reports repeated character/scene consistency attempts through OpenMayhem. It is partial: the author is affiliated with the platform, and full prompts/settings are not reproducible from the report.
- **Unknowns:** Which underlying model a UI action selected, native edit behavior, and current in-product model routing require fresh inspection.
- **Sources:** [Krea 2](https://www.krea.ai/krea-2); [technical report](https://www.krea.ai/blog/krea-2-technical-report); [style reference guide](https://www.krea.ai/blog/style-references-krea-2); [community consistency test](https://www.reddit.com/r/ZImageAI/comments/1wh338l/krea_2_vs_zimage_turbo_how_consistent_can_you/).

### Family: Meta Muse Image

- **Variants:** The official model API identifier is `muse-image-1.0`. Meta consumer apps and region-specific rollouts may expose features without displaying the same identifier.
- **Surface and operations:** Official model API docs describe T2I, image edits, multiple references, and multi-turn interaction. The existence of an API feature does not guarantee the same operation in Meta AI app or this plugin host.
- **Prompt guidance:** For text inside images, keep text strings short and explicit, then inspect exact spelling and placement; Meta's docs themselves caution that exact baked-in text can vary. For edits, describe a bounded change and what remains untouched.
- **Practitioner evidence:** TGK's report includes Meta AI on a shared brief, but the actual control path did not expose the precise model/version and had no incoming references in the core T2I test. Treat as a first-result observation only.
- **Unknowns:** Regional availability, exact app/model routing, and parity of reference/edit controls are unverified.
- **Sources:** [Muse Image launch](https://ai.meta.com/blog/introducing-muse-image-muse-video-msl/); [Meta image generation docs](https://dev.meta.ai/docs/image-generation); [TGK comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: Microsoft MAI Image

- **Variants:** MAI-Image-2.6 and MAI-Image-2.6 Flash are listed on the official product page. An exact API identifier was not confirmed in this audit.
- **Surface and operations:** The official page describes generation and controllable image editing, but endpoint availability and precise reference slots require surface-level confirmation. Do not convert product marketing language into unverified parameter names.
- **Prompt guidance:** Treat input reference roles, edit scope, and output layout as separate facts; ask for one missing operation detail only when it changes the prompt. Do not assert a specific number of supported references without a current surface doc.
- **Practitioner evidence:** TGK included MAI-Image-2.6 Preview with a shared T2I set; Astria published a September 13 reference-led fashion test with three references. The latter used an intermediary surface and one output per model, so it is partial evidence for that setup only.
- **Unknowns:** Exact API identifier, current release/status, and native reference/edit parameter limits need current official confirmation.
- **Sources:** [MAI-Image-2.6 product page](https://microsoft.ai/models/mai-image-2-6/); [Astria reference-led test](https://astriaai.github.io/articles/mai-image-2-6-review/); [TGK comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: Tencent Hy-Image

- **Variants:** Cloud service `Hy-Image-3.0` uses `hy-image-v3`; `Hy-Image-3.5-Preview` uses `hy-image-v3.5-preview`. These differ from open-weight `tencent/HunyuanImage-3.0` and `tencent/HunyuanImage-3.0-Instruct`. Do not normalize similar family labels into one endpoint or behavior.
- **Surface and operations:** Current Tencent TokenHub docs date to 2026-09-24. They document cloud 3.0 T2I and up to three reference inputs; 3.5 Preview adds multi-turn editing and has a different reference range on that API. The open Hunyuan repository describes T2I for 3.0 and T2I/I2I for its Instruct checkpoint. This is not proof of parity with TokenHub or a consumer app.
- **Prompt guidance:** For cloud 3.0, state the desired image and, if important, aspect/size intent; verify endpoint size constraints separately. For multi-turn/edit routes, describe current state, exact delta, and preservation set. Do not hard-code request payloads unless API use was requested.
- **Practitioner evidence:** A January 28 HunyuanImage-3.0-Instruct post reports a group-portrait prompt and an input-image edit experiment, but omits reproducible settings and clear per-result surface mapping. No qualifying independent exact-version report was located for Hy-Image-3.5 Preview.
- **Unknowns:** Preview reliability, current cloud account access, parity between checkpoint and cloud backend, and independent failures/results remain unverified.
- **Sources:** [Tencent Hy Image TokenHub guide](https://cloud.tencent.com/document/product/1823/135745); [HunyuanImage 3.0 repository](https://github.com/Tencent-Hunyuan/HunyuanImage-3.0); [Instruct model card](https://huggingface.co/tencent/HunyuanImage-3.0-Instruct); [partial user report](https://www.reddit.com/r/StableDiffusion/comments/1qp44ab/hunyuanimage_30_instruct_with_reasoning_and_image/).

### Family: Reve

- **Variants:** Reve 2.1 is the exact product release found; an exact API model ID was not confirmed.
- **Surface and operations:** Official launch materials describe creation and image editing; a separate official References feature describes reference-led work. Do not combine those into a single proven operation on every surface.
- **Prompt guidance:** Give a direct target and composition/hierarchy; for edits, name the element to change and preserve the rest. Treat high-resolution or layout claims as provider claims unless the user's actual output is checked.
- **Practitioner evidence:** TGK tested 2.1 through WaveSpeed with shared briefs and separately inspected Reve's interface. The reported test run was through the intermediary, lacked references in its core T2I set, and is therefore partial.
- **Unknowns:** Exact model identifier, native reference behavior, UI/API parity, and current output controls require a fresh check.
- **Sources:** [Reve 2.1 launch](https://blog.reve.com/posts/launching-reve-2.1/); [Reve References](https://blog.reve.com/posts/introducing-references/); [TGK comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: xAI Grok Imagine

- **Variants:** Current official API identifier found: `grok-imagine-image-2.0`. Do not assume the consumer app exposes the same image version or settings.
- **Surface and operations:** Current xAI API documentation describes T2I and editing with up to five reference images on that API. Changelog details can alter defaults; avoid storing volatile defaults, sizes, or costs as timeless instructions.
- **Prompt guidance:** State exact visible text, subject relationships, and intended crop. For a reference edit, separate what should change from what must remain; verify the current API's actual input limit only when that exact API is named.
- **Practitioner evidence:** TGK's native Grok test used shared prompts and first outputs, with incomplete internal settings and no incoming reference images in its controlled T2I set. It does not validate the API's five-reference edit behavior.
- **Unknowns:** Chat-app/API parity, account rollout and exact current API defaults need current source/user evidence.
- **Sources:** [xAI Imagine capability guide](https://docs.x.ai/developers/model-capabilities/imagine); [xAI release notes](https://docs.x.ai/developers/release-notes); [TGK comparison](https://theseguysknow.io/best-ai-image-generators/).

### Family: Stability AI / Stable Diffusion 3.5

- **Variants:** SD 3.5 has separately distributed model variants/checkpoints and Stability-hosted services. Do not identify an endpoint, checkpoint, community fine-tune, or app as the same runtime merely because they share “Stable Diffusion” branding.
- **Surface and operations:** Official sources document T2I models and hosted image services. Editing may be provided by a particular service, a community workflow, or another model; do not attribute all such tools to an SD 3.5 checkpoint.
- **Prompt guidance:** Use the documentation of the actual checkpoint and inference pipeline, including supported negative prompts, control adapters, sampler, or scheduler. Do not import a hosted product's controls into a local pipeline or vice versa.
- **Practitioner evidence:** No qualifying current independent SD 3.5 report with exact model, prompt, settings, edit inputs, and output was located in this scoped search. Older family benchmarks and generic diffusion advice are not current 3.5 evidence.
- **Unknowns:** Active checkpoint, UI/pipeline, license/version, editing route, and user's local configuration must be stated before technical instructions.
- **Sources:** [Stability AI Stable Image](https://stability.ai/stable-image); [Stability developer docs](https://platform.stability.ai/docs).

### Family: Z-Image

- **Variants:** Z-Image foundation model and Z-Image-Turbo are distinct checkpoints; the family's separately named edit model is not interchangeable with Turbo.
- **Surface and operations:** Official Turbo repository documents T2I. Native I2I for Turbo was not confirmed in the checked card; do not infer editing from a separate edit model, community ControlNet, or workflow add-on.
- **Prompt guidance:** Keep a prompt descriptive and test the model's language/text handling on the intended surface. For consistency across images, preserve a concise identity description and vary only shot-specific variables, as a bounded experiment rather than a guarantee.
- **Practitioner evidence:** Wiro's 2026-02-24 test gives six prompts, 1024-square outputs, nine steps, guidance 0, and seeds 701–706, including a poster/text task; it ran through Wiro, not the raw local checkpoint. A September 5 OpenMayhem consistency post is another partial third-party observation.
- **Unknowns:** Native editing of Turbo, exact separate edit-checkpoint contract, current hosted controls, and cross-surface reproducibility remain open.
- **Sources:** [Official Z-Image-Turbo repository](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo); [Z-Image project](https://tongyi-mai.github.io/Z-Image-blog/); [Wiro six-prompt test](https://wiro.ai/blog/z-image-turbo-few-step-text-to-image-in-6-prompts/); [OpenMayhem consistency report](https://www.reddit.com/r/ZImageAI/comments/1w85xx4/zimage_turbo_consistency_experiments_in_the/).

### Family: Leonardo Phoenix

- **Variants:** Phoenix 1.0 `phoenix-v1.0`, 0.9, and Lucid Origin `lucid-origin` are different models in the Leonardo platform; the app may expose third-party models too. Verify selected model rather than relying on platform name.
- **Surface and operations:** Phoenix API docs describe T2I plus distinct character, content, style, and I2I guidance. Lucid Origin docs describe T2I with content/style guidance but do not establish a separate I2I field. Do not copy Phoenix reference support to Lucid or vice versa.
- **Prompt guidance:** Assign each reference its true property role. A style reference does not establish exact identity; a content reference does not promise pixel preservation. API controls and limits are not plain chat syntax.
- **Practitioner evidence:** Pipgen's August 2026 test compares Lucid Origin on nine shared prompts with auto-select off and first results retained, but omits seed/resolution and full settings. No qualifying first-hand comparison for exact Phoenix 1.0 was located; Phoenix 1.1 evidence does not transfer to 1.0.
- **Unknowns:** Current app default, in-app/API feature parity, version rollouts, and independent Phoenix 1.0 failure patterns remain unverified.
- **Sources:** [Phoenix product page](https://www.leonardo.ai/phoenix); [Phoenix API guide](https://docs.leonardo.ai/docs/phoenix); [Lucid Origin API guide](https://docs.leonardo.ai/docs/lucid-origin); [Lucid Origin user comparison](https://pipgen.com/ai-image-generators/leonardo/).

### Family: HiDream O1

- **Variants:** `HiDream-ai/HiDream-O1-Image` and the separate `HiDream-O1-Image-Dev` are distinct checkpoints. Do not transfer Dev settings to the full model or older I1/E1 branches.
- **Surface and operations:** Official repository/model card describe T2I, editing from an input image, and multi-reference subject personalization for the stated open checkpoints. This is not a managed hosted UI contract.
- **Prompt guidance:** Separate input images by role; make the edit delta explicit. Treat inference steps, memory, precision, and resolution as pipeline settings dependent on checkpoint/software, not prose tokens.
- **Practitioner evidence:** A May 28 local MLX test used four source prompts and adjusted steps/resolution for the Dev checkpoint. It is partial evidence for that local build, not a universal recommendation.
- **Unknowns:** Current hosted availability, exact surface-specific reference limits, and independent full-checkpoint comparisons remain open.
- **Sources:** [HiDream O1 repository](https://github.com/HiDream-ai/HiDream-O1-Image); [O1 model card](https://huggingface.co/HiDream-ai/HiDream-O1-Image); [local MLX test](https://8bitnand.github.io/blog/local-hidream-o1-vs-gpt-image-nano-banana/).

### Family: GLM Image

- **Variants:** Open checkpoint `zai-org/GLM-Image` and hosted Z.AI API model `glm-image` are separate routes, with separate supported inputs.
- **Surface and operations:** The open checkpoint repository describes T2I and I2I/edit, including style transfer and multi-subject consistency. The Z.AI hosted API documentation checked here describes text-prompt generation; do not attribute open-checkpoint image input support to that API.
- **Prompt guidance:** Use a structured brief with short exact display strings and explicit layout relations for poster/slide tasks. Verify wording and hierarchy in actual output; do not declare text rendering guaranteed based on examples.
- **Practitioner evidence:** A January 2026 first-hand poster/slide report provides prompt examples and describes iterations, but lacks exact checkpoint build, seed, and generation settings. It is useful anecdotal practice, not a controlled model comparison.
- **Unknowns:** Hosted I2I support, current serving version and model routing, reproducibility, and exact text-rendering reliability remain unknown.
- **Sources:** [Official GLM-Image repository](https://github.com/zai-org/GLM-Image); [model card](https://huggingface.co/zai-org/GLM-Image); [Z.AI API docs](https://docs.z.ai/guides/image/glm-image); [poster/slide user report](https://macaron.im/blog/glm-image-poster-slide-prompts).

## Watchlist and evidence gaps

These names appeared in current search, official announcements, model catalogs, or public preference boards, but were not promoted into native prompt adapters during this snapshot because the current model/surface/operation contract and/or useful independent user evidence was not sufficiently audited:

- **Cosmos3 Super Text2Image, Bagel, LongCat Image, Z-Image Edit, and other research/open-model candidates:** public boards or papers surfaced the names, but a board score or paper alone is not a complete end-user surface contract or first-hand prompt study. Search primary model documentation and current first-hand practice before promoting a distinct adapter.
- **Other current hosted products and regional releases:** no claim of comprehensive market coverage. Discover and add them during dated rechecks when they meet the prominence and evidence scope.

The public Artificial Analysis Arena snapshot observed on 2026-09-21 includes millions of pairwise votes and separate text-to-image and image-edit tasks. It can nominate candidates for deeper research; it is not a controlled benchmark, a popularity census, or proof of edit capability. Do not translate rank into a universal “best generator” claim.

## Dated practitioner evidence register

| Source | Date and tested coverage | What it supports | What it does not support |
|---|---|---|---|
| These Guys Know, “We Tested 10 AI Image Generators on Faces, Text and Ads” | Published 2026-08-25; Nano Banana 2/Pro, GPT Image 2, Seedream 5.0 Pro, Midjourney 8.2, Ideogram 4, Reve 2.1, Muse Image, MAI-Image-2.6 Preview, Grok; several runs via WaveSpeed, others via native products | Shared task briefs, some precise settings, visible first-output failures, especially separation of legible text from correct object scale | Not a universal ranking, not 2.5 evidence for GPT Image, not a controlled incoming-reference benchmark, and not full parameter parity across products |
| getimg.ai 17-model realism comparison | Published 2026-08-21; includes FLUX.2 Max/Pro/Klein and Seedream 5.0 Pro via getimg.ai | Single-run observations under shared prompts with enhancement off | Not a native BFL/ByteDance test; no full seed/settings table; not a complete editing study |
| Loop Forge Qwen-Image 2.1 field test | Published 2026-09-23; local RTX 3060 12 GB, 26 prompts, edits and multi-reference examples | Detailed local use cases and visible failure examples | Not every hosted surface; incomplete sampler/seed data; one practitioner's setup |
| NanoGPT Qwen-Image 3.0 review | Published 2026-07-23; four text/edit trials, fixed seeds, specific NanoGPT service limits | Version-specific poster/text and edit observations with some settings | Intermediary prompt-length limits and small sample; not official API or all surfaces |
| Astria MAI Image 2.6 fashion/reference test | Published 2026-09-13; intermediary surface, three references | A concrete reference-led task and output under that service | Not a native Microsoft control test; one output per variant and incomplete reproducibility |
| HunyuanImage-3.0-Instruct post | Published 2026-01-28; group portrait and input-image edit examples | Candidate open-checkpoint prompting/edit observations | Settings and per-result route mapping are incomplete; anecdotal |
| Wiro Z-Image-Turbo comparison | Published 2026-02-24; six prompts, seeds 701–706, 1024-square, nine steps and guidance 0 | Visible poster/text tasks with concrete setup | Wiro-hosted rather than raw local; one user's selected examples |
| Pipgen Leonardo Lucid Origin comparison | Published August 2026; nine shared prompts, auto-select disabled, first outputs retained | Comparative first-output observations for that model/platform | No seed/resolution/full settings; not an exact Phoenix 1.0 test |
| HiDream O1 Dev local MLX comparison | Published 2026-05-28; four source prompts with differing step/resolution settings | Shows why settings materially affect that specific local Dev run | Dev-only partial sample; not a hosted/full-checkpoint adapter |
| Macaron GLM Image poster/slide use | Published January 2026; prompt examples and a small number of iterative trials | Concrete anecdotal text/layout/edit practice | Missing exact model build, seed, and settings; not controlled |
| Krea 2 Turbo vs Z-Image Turbo | Published 2026-09-15; OpenMayhem browser surface | A reported consistency workflow and concrete prompting observations | Author has platform affiliation; missing full prompt/settings; not a controlled native comparison |
| Z-Image Turbo browser consistency experiments | Published 2026-09-05; OpenMayhem surface | Candidate consistency technique with prompts/settings shown | One author's mediated test; no universal identity-lock guarantee or cross-surface result |

Across these reports, test surface, version, prompt formatting, first-output selection, parameters, reference use, and retry policy can differ. Treat cross-model conclusions as local. Reproduce the exact task and surface before turning a finding into a workflow rule.

## Fresh-update checklist

Before changing a card, record the access date; exact name and version; the public user-facing surface; the operation tested/documented; source type; practitioner author/date and reproducibility fields; confidence; conflicting evidence; and resulting runtime change. Preserve old labels as historical rather than rewriting them as “latest.” Retest any rule whose version, endpoint, product UI, or reference controls changed. If a useful independent test is unavailable, preserve the gap. This snapshot's existence does not satisfy the separate video/audio mapping, host retrieval, user-account, fresh-use, or actual-render criteria.
