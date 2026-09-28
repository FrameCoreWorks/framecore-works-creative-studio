# Static prompt compiler

Owner: image-prompt-architect. Version: 0.1.0-dev.2. Updated: 2026-09-24. Sources: static-design unified contract, reference/typography/QA assets; Poster Creator ROOT/META; LUMENFRAME; Visual Prompter K15. Stable composition grammar with dynamically mapped generator controls.

## 1. Confirm the kind of output

Distinguish:

- final integrated raster graphic;
- text-free image by explicit choice;
- source-bound image edit;
- prompt for an external target only;
- explicitly requested separate assets/vector/coded artwork;
- production specification rather than an image.

Do not infer a mockup when the user asks for a poster. A photograph of a poster hanging on a wall is not the poster artwork. Do not infer multiple variants, a moodboard or a grid when one finished output is requested. A deliberate collage can be the artwork, but it is not the same as a grid of alternatives.

The instructions that follow target one integrated raster. Separate-assets work requires its own plan and current-asset scope. Do not use that exception as a hidden workaround for difficult text.

### Multiple independent stills

Use this path only when the requested result is several distinct image files. Do not confuse them with:

- one multi-panel board, contact sheet, moodboard, or reference sheet; route its panel layout to `storyboard-board-architect` and let `image-prompt-architect` compile a requested board image;
- one campaign adapted across ratios or channels; campaign direction and format roles belong to `commercial-visual-campaign-director`;
- a causal or time-ordered set of story moments; event order and shot coverage belong to `storyboard-sequence-architect`, which can hand off selected stills for prompt compilation.

If the user’s wording leaves “separate files or one board?” materially unclear, ask that one question before building the output pack. Otherwise resolve the requested count exactly. Give every image a distinct job; decide whether the set is coverage (different useful views/roles of one subject) or progression (deliberate change over time); state only the visual thesis and locks meant to persist, the variations allowed per image, and an anti-duplicate check. Keep the image order or names only when they help downstream use.

For each unit, make a compact card with its ID, unique job, subject/action, composition or camera intent, relevant shared/variable properties, references actually attached to that request, and one acceptance check. Then write a complete standalone prompt for each requested file. Repeat the essential visual facts and any exact copy needed by that prompt; never replace them with “same as the previous image” or rely on an earlier turn, a repeated seed, or unverified cross-request model memory. Do not invent a source asset, carrier, or real product fact.

Separate the continuity requirement, input readiness and observed result. Bind strict locks to a real, property-appropriate source for each independent execution. Text-only/no-carrier continuity is approximate only when that is the requested or explicitly authorized fidelity; a missing carrier never silently downgrades a strict requirement. Request the required source or offer a bounded relaxation for the user's decision.

For a prompt-only set, including explicitly requested layer/asset packs, deliver all requested independently specified units without waiting for a newly generated master. If a unit depends on that future master, put the requirement to supply the approved master in its complete standalone prompt and identify the planned dependency outside it. Mark the unit not ready for execution and the pack unvalidated until that real carrier is accepted and bound; do not pretend it is attached or describe unseen properties as observed facts. This planning allowance does not make an absent existing edit base inspectable or permit invention of unknown real identity/product features. Complete independent units and hold only details that truly depend on missing source evidence.

During actual production, inspect the master or representative initial outputs before expanding dependent generation. Follow any agreed sequential image-acceptance workflow at that execution stage. Do not claim native batching or shared state unless the model and surface are separately verified.

## 2. Inputs required for final compilation

An ordinary brief can carry all necessary inputs; a formal contract file is not required.

- What should be communicated and in what context?
- What concept/layout decisions are selected or explicitly delegated?
- Which exact strings are final, which are mandatory, and which line breaks are protected?
- Which supplied assets govern which properties?
- What format/ratio is intended and what delivery properties are actually needed?
- If a generator is named, what current guidance applies to that version/surface?
- What would a reviewer need to check in the result?

Do not stop for irrelevant unknowns. A concept raster need not know the printing stock. A production master does. If copy is missing but needed, do not compile placeholders into a “ready” prompt.

## 3. Bind references by property

Identify the actual attached source and its role:

| Role | Governs | Does not automatically govern |
|---|---|---|
| Brand/logo | Approved mark geometry, colors or usage rules | Competitor reference layout |
| Product truth | Shape, construction, material, label topology, variant | A new invented feature |
| Identity | Supplied person's/character's visible anchors | Guaranteed exact likeness from text |
| Layout | Approved structural relationships | Copy and claims within the example |
| Style/material | Declared surface or formal attributes | Product identity, text or complete composition |
| Edit source | The current artwork to modify | Permission to redesign all of it |
| Negative reference | What the user wants to avoid and why | A secret new generation source |

Use the actual host-supported reference attachment, not merely an alias in prose. A reference visible in the chat may still need to be bound to the generator request. Do not invent img1/img2 or assert a missing upload exists.

Conflicts must be resolved at the property level. If an old pack shot and a new supplied label differ, ask which governs the label rather than blending them. If the user's request only changes background, protect product/copy/layout.

## 4. Semantic construction order

Resolve all applicable priorities, but do not force eight headings or repeated paragraphs.

1. Final output: asset type, one finished output, intended ratio, communication purpose, first read and viewing mode.
2. Foundation: background field, useful material, palette roles, protected reading areas and negative space.
3. Architecture: focal axis, relative scale, alignment, grouping and attention sequence.
4. Main event: type, sign, object, relation or scene. Protect real assets and describe meaningful geometry.
5. Support: only elements with a navigation, message, proof, recognition or purposeful atmosphere role.
6. Typography: every required string, type behavior, placement, hierarchy and permitted/locked breaks.
7. Integration: color, light, material and local contrast bind the whole; no contradictory process instructions.
8. Finish: optical spacing, crop/safe zones, narrow exclusions and observable checks.

These are priorities inside one prompt and one requested generation, not sequential image calls. A pure typographic poster does not need a pictured hero, fake camera or lighting description. A local edit uses its permitted change first, not a complete redesign disguised as eight stages.

## 5. Exact text construction

Quote the final inventory. Keep language, accents, case, punctuation, figures, qualifiers, addresses and contacts exact. Specify no additional visible text when appropriate. Mentioning a title once with clear role is better than repeating it in contradictory paragraphs.

Do not leave “[headline]”, “lorem ipsum” or alternate slogans in a final prompt. Do not let instruction metadata appear as visible copy. If a slash label was explicitly requested as instruction metadata, distinguish it from artwork text; do not invent a catalog whose entries were never loaded.

Describe typographic behavior: condensed display, open functional sans, controlled contrast, compact but separable uppercase, stable factual block. Do not promise access to a named font or exact editable typography in a raster.

Requiredness and priority are independent. A legal line may be visually secondary and still compulsory. Do not “solve” dense content by deleting it or rendering pseudo-text.

## 6. Model-native translation

Preserve creative invariants across target models. Change only what evidence justifies: structure, control fields, reference carriers, accepted input or a model-specific limitation. Two correct prompts may be similar; artificial difference is not quality.

Separate prose from actual settings. An aspect ratio phrase in text expresses intent; a verified size/aspect setting controls the request when available. A camera number can guide appearance, not guarantee optical metadata.

Do not add universal CFG, steps, seeds, negative fields, reference weights or flags. Some targets do not expose them. JSON/YAML may organize instructions without being an API schema. Label the distinction.

When current mapping is unavailable, provide a conservative natural-language prompt and name the limitation. Do not silently call it optimized for the latest model. API/wrapper questions belong only to a user-raised implementation context.

## 7. Compactness without losing locks

Every clause should create a decision, constrain ambiguity or protect an invariant. Remove duplicated atmosphere and generic quality words. “Senior designer quality”, “award-winning” or “100% anti-slop” does not specify composition.

A complex poster may require a substantial prompt because text, references and relationships matter. Do not reduce it to a subject/style tag list. Conversely, a one-word sign may need only a few paragraphs. Length follows constraint density.

Prefer explicit geometry: “The narrow seam between the two paper panels aligns with the space between the two title words” is operational. “Beautifully integrated typography” is not.

## 8. Scoped edit

Bind the actual source and resolve four distinct parts of an edit before compiling: the requested change, properties that remain protected, any narrowly allowed secondary changes that are physically caused by the requested edit, and observable success checks. A secondary change is not blanket permission to redesign. Name only effects that apply to the supplied material and scene; preserve other source properties. Resolve any overlap or contradiction between the requested change and a protected property before releasing a final prompt.

For background replacement, preserve subject/product geometry, pose, camera, crop, focus and truth. Adapt the new environment to the existing camera and subject rather than silently changing those locks. Allow only relevant physical consequences of the new environment, such as changed reflections, refraction/transmission, contact or cast shadows on the replacement support, environmental color spill, edge integration, or background perspective/scale/depth and processing. These are conditional examples, not a required checklist or universal permission. Match the replacement's horizon, perspective, camera height/lens character, scale/depth, light/exposure, reflected color, support, edge softness, atmosphere, grain and processing as applicable. Keep focus and subject sharpness protected; depth-of-field or atmospheric integration must not silently refocus the subject. Preserve product-local color, SKU, label and exact visible copy unless the user explicitly authorizes a specific change. For glass, chrome, glossy packaging or transparent objects, do not preserve old-environment reflections or transmission as pixel locks when they physically conflict with the new environment. If the user requests both, withhold the contradictory final prompt and ask one focused trade-off question or offer a bounded alternative, such as allowing only the necessary new-environment interactions while preserving product truth, or keeping the original environment.

If a source image is absent, do not claim to have inspected it or issue a source-bound edit prompt as though its pixels were known. Never guarantee that prompt wording will produce pixel-identical protected regions or a successful render. Actual-output inspection remains a separate QA step.

For an exact word replacement, quote the old and new strings as edit instructions and make clear which is final visible copy. Protect other strings without necessarily transcribing the entire poster if the edit source is readable and actually bound.

Do not insert a different concept, modify a face or refresh the palette during a date repair. After editing, inspect both the target and protected properties. Compare with the original approved base when there have been multiple edits; a rejected result is not the new source of truth.

A fresh independent generation must include enough context and actual references to stand alone. “Same as before” is inadequate if the target cannot see the previous request.

## 9. Preflight and delivery

Before release:

- accepted/delegated concept, no unresolved competing directions;
- selected exact copy or deliberate no-copy;
- source role and actual availability established;
- ratio and viewing task compatible;
- attention hierarchy and supporting element jobs explicit;
- material behavior coherent and no unsupported claims;
- syntax/settings supported or transparently conservative;
- one requested artifact, appropriate method and honest review state.

For a new or materially revised static campaign direction, the authorial anti-slop gate in [direction and composition](../../commercial-visual-campaign-director/references/direction-and-composition.md#9-authorial-and-anti-slop-pre-prompt-gate) must have passed before a final prompt is released. Consume that direction-stage decision; do not create a competing checklist or treat prompt syntax as a substitute for concept repair. If the handoff has a material unresolved failure, withhold the final prompt and return the direction for repair. If the gate result is absent, do not assume success: use the same shared gate and criteria once at this boundary, then return to the direction owner if it fails. An unchanged, previously accepted direction used for a narrow mechanical edit may retain its prior decision.

Fix a failed prompt gate. Do not label it final and ask the generator to resolve contradictions.

Return a complete fenced prompt. If explanation is allowed, add a short production note: intended format, copy inventory or reference to its exact lock, first read, safe-area assumptions and the review test. Do not repeat the entire manual.

Prompt-ready is not render-accepted. Generation requires an actual request and tool. A general approval such as “ten kierunek jest dobry” is not automatically permission to spend credits or upload files. A specific “generuj ten plakat” need not be asked again if all relevant requirements and host permissions are satisfied.

## 10. Failure handling

Report tool error, missing capability, usage limit, content-policy refusal and successful-but-defective render as different states. Only report a cause supported by the actual tool or visible evidence.

Preserve the prompt after a technical failure. Do not silently rerun or switch to an external provider. If no inspection route exists, mark QA not run. Do not claim that a Thinking model is the cause merely because it was selected.
