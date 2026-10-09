# Dynamic model mapping and evidence

Owner: research-evidence. Version: 0.1.0-dev.3. Updated: 2026-09-24. Procedure adapted from selected source packages and corrected to separate historical knowledge, current documentation, observed results and user-specific availability. For image discovery, start with the dated [image-generator snapshot](image-generator-snapshot.md) and then recheck the named target; the snapshot is neither an exhaustive market census nor a permanently current catalog.

## Why an adapter exists

A visual or motion intention is not yet a native request. Different versions and surfaces can accept different references, durations, edit modes, aspect controls, audio, negative prompts or structured settings. A family name alone does not establish these.

Preserve a model-independent creative core: subject, mechanism, exact text/dialogue, source locks, spatial relationships, action and acceptance criteria. Map only the interface-dependent layer. Do not manufacture stylistic differences between prompts merely to prove they were “optimized”.

## Resolve identity without an infrastructure interview

Use the user's supplied name and context. A normal “prompt for FLUX” request concerns the user-facing target unless another surface is named. Ask only a materially necessary version choice. Do not introduce API versus wrapper questions unprompted.

If the user explicitly gives an API, third-party platform, local graph, screenshot or wrapper, record that surface. Its controls may differ from the model author's app. Do not transfer endpoint syntax into a normal chat prompt.

Brand nickname, provider, model and version are separate. Similar names are not proof of equivalence. Do not silently change a requested older version to a newly announced model.

## Mapping procedure

1. Define the task: generation, edit, reference-led composition, continuation, video shot, dialogue, or production handoff.
2. Locate the model author's documentation, release notes, product page or model card. Check version and date.
3. Read the relevant prompting and reference/input sections. A search-result title is not enough for detailed syntax.
4. Identify supported input carriers, controls and documented limitations on the named surface.
5. Check release changes that could invalidate a stored rule.
6. For every named-generator task, actively search for attributable first-hand practitioner use in addition to owner documentation. Look for both useful results and failures; record exact setup, model/version, surface and uncertainty. If no credible or sufficiently detailed report is found, record that gap rather than filling it with general impressions.
7. Compile a conservative request, using only controls actually confirmed for that surface.
8. State a material uncertainty and the next verification action, rather than hiding it in confident phrasing.

Do not demand an exhaustive market survey for one named-model prompt. A requested broad compendium is different and needs a scoped inventory plus coverage table.

### Additional requirements for video adapters

Map each exact operation separately: T2V, I2V, reference-conditioned video,
first/last-frame input, native multishot, source-video edit, V2V, extension,
motion transfer, presenter/lip-sync, and audio generation are not aliases for
one another. For the named version and surface, establish what the input
actually carries into the job, what timing or shot structure is supported,
whether dialogue/audio is native or separate, which controls are documented,
and which conditions are only reported by users.

Keep three decisions independent in the adapter record: creative intent,
context transport, and shot construction. Do not infer cross-shot memory from
one prompt, infer strict continuity from a reference name, or treat a source
frame as evidence that an edit/extension operation exists. A feature may be
available on one surface and absent on another. Search current official
documentation first, then compare attributable user experiments that show
their exact setup and failure evidence. Leave unsupported syntax and limits
unknown; do not fill them with sibling-model behavior.

Where the user asks for current best practices, provide the concise rule that
changes the prompt and its evidence boundary. Include failed or contradictory
user reports when they alter the recommendation. Never describe a prompt as
tested unless the exact request and output were actually produced and inspected.

## Adapter record

Keep this internal unless the user requests technical detail:

- family and exact model/version;
- surface and task;
- date checked and supporting sources;
- input types/reference carrier actually available;
- supported parameter names, values and limits only where verified;
- prompt structure or wording guidance;
- exact text, image identity, motion/audio and edit preservation risks;
- unsupported assumptions removed;
- remaining UI/account check;
- planned acceptance test and actual test status.

Values may be Unknown. Never infer a field from a sibling model. Text-based “8K” or “120fps” does not establish output dimensions or frame rate. A reference alias is not an upload.

## Evidence classes

| Class | Meaning | Appropriate use |
|---|---|---|
| Official documentation | Published contract/guidance for a stated scope | Parameters and supported operations within that scope |
| Official demonstration/announcement | Vendor-selected claims and examples | Discovery and hypotheses, not guaranteed performance |
| Provider-authored model card/paper | Model description, released artifact or reported evaluation | Technical context with stated version and limits |
| User-supplied account/UI evidence | Actual visible settings or behavior for this user | That account/surface at the observed time |
| First-hand community experiment | A person reports results and, ideally, inputs/outputs/settings | Failure patterns and candidate experiments |
| Secondary commentary | Summary or opinion | Leads, not native syntax authority |
| Local craft synthesis | A design or prompting method authored for this package | Practical reasoning, not a vendor feature |
| Local execution evidence | Actual recorded call and inspected output | That run under those conditions, not universal success |

A README that says “verified” is inherited evidence until its source or test is rechecked. A repeated claim across ten tutorials does not become ten independent confirmations.

## Community evidence protocol

Prefer reports with model/version, surface, prompt, source inputs, settings, output and an explicit comparison. Note missing variables. A beautiful image without its actual prompt and input is inspiration, not a reproducible recipe.

One observation can motivate a bounded test. Do not turn it into a mandatory universal rule such as “always use 30 steps” or “English is always better”. Distinguish a host's prompt rewriting from model behavior. A local LoRA result does not establish the hosted base model's capability. The practitioner search is a required evidence lane, not proof that every user technique generalizes; clearly identify anecdote, reproducible comparison, and unknown separately.

If first-hand evidence conflicts with official documentation, retain both: documentation may define a supported operation, while the report exposes reliability under a specific setup. Do not claim either establishes a guaranteed creative outcome.

## Useful research outputs

For one task: a concise finding that changes the prompt, a complete prompt and one relevant limitation.

For a compendium: scope/date; source register; per-family/version/surface mapping; stable craft; known failure patterns; examples labeled tested/untested; contradiction log; update triggers; remaining gaps. Count actual coverage, not links collected.

For image family, operation, version, surface and evidence boundaries checked on 2026-09-24, consult the [audited image-generator snapshot](image-generator-snapshot.md). For video families, operations and retirements checked on 2026-10-09, consult the [video-generator snapshot](video-generator-snapshot.md). Its cards distinguish T2I, I2I/edit and reference-led operations; a missing field is not support. Recheck any material current claim, and add a newly surfaced family only after applying the same source, practitioner-evidence and uncertainty controls.

No absolute “complete know-how of every model” promise. State the market/date boundary and unverified families. Maintain old-version guidance as historical when useful, never silently current.

## Prompt-language policy

English is the Studio's technical-prompt default, not a universal scientific claim about model quality. Follow the user's explicit preference and relevant documented language support. Preserve exact visible text and dialogue in their approved target language. Do not translate a title as an adapter operation.

## Execution and privacy

Reading public docs does not authorize a provider run. Mapping can be completed without paid calls or uploads. Respect current host/user restrictions on providers, API keys, wrappers and activation. Do not write activation phrases into a resume sheet as if they renew themselves.

Never put a confidential script, client contact data or unreleased product image into a public search query. Generalize the research question. If private input is required for a future service operation, obtain appropriate explicit authorization and use the actual designated route.

Do not diagnose an account entitlement problem by patching a prompt. Confirm what the tool actually reports before recommending a fix.

## Fallbacks and stop conditions

If browsing is prohibited or unavailable, use stable craft and omit unsupported native settings. Label target-specific currency unverified. If a required capability cannot be established, provide a useful planning artifact or ask a narrow question; do not fabricate an adapter.

If a source only describes a new release, do not invent exact UI access. If the host exposes no model selector, do not claim the plugin selected a particular backend. Follow active host policy, including any user-required native image target when it is actually selectable.

Stop researching once the material decision is supported, or report the specific unresolved evidence. Research is meant to improve the artifact, not indefinitely delay it.
