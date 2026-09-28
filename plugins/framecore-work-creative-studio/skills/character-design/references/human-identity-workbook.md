# Human identity and believable reference sheets

Use for a recurring person, a real-person likeness, or a requested human reference sheet. Read only the relevant sections. Character Design owns identity decisions; Reference Pack Curator owns source authority, Board owns the sheet, Image Prompt owns final image instructions, and Video Prompt owns motion continuity. Source support and limits are recorded in [the expansion evidence](../../research-evidence/references/reference-audio-expansion-sources.md).

## Establish what the source can prove

Separate three cases before describing the person:

| Case | Anchor | Unknown or variable |
|---|---|---|
| Actual person | Supplied original photos and explicit current corrections | Unseen anatomy, back of hair, teeth, marks hidden by clothing |
| Fictional photoreal person | User-selected master image and chosen design facts | New angles remain design proposals until selected |
| Stylized existing character | Approved character proportions, medium, face and costume | Photographic realism is not automatically the goal |

Record a small number of discriminating visible traits: overall face proportions, eye spacing/shape, eyelids, nose, mouth, jaw, hairline, asymmetry and any clearly visible mark relevant at the target scale. Do not infer ethnicity, medical history, personality or a biography. A source description cannot substitute for opening an accessible source image.

Keep the user's required fidelity separate from available evidence and execution readiness. Missing profile views do not turn a strict identity requirement into approximate continuity. Preserve strict as the requirement, identify the missing surface/view, and mark the affected request blocked or conditional. Still produce useful planning that does not depend on invented anatomy.

## Capture only the missing evidence

Use the existing [capture card](../../image-prompt-architect/assets/human-reference-capture-card.md). Select views by the planned camera and action, rather than requiring a universal photo count.

| Planned output | Useful source | Reason |
|---|---|---|
| Frontal portrait | Sharp front view with a relaxed expression | Establish face proportions without an extreme expression |
| Turn toward either side | Three-quarter view on the corresponding side | Reveal cheek, jaw, ear and hair relationships |
| True profile | Actual relevant profile | A frontal photo does not establish the nose/chin silhouette |
| Smile or visible speech | Required smile/open-mouth expression | Teeth and changing mouth shape are otherwise unresolved |
| Low/high angle | Corresponding view only if it matters | Avoid inventing the underside of the jaw or top of the head |
| Full-body continuity | Wider reference of posture, proportions and required outfit | A face crop does not establish height, build or garment construction |

Keep framing and lighting reasonably comparable where possible; use clear inputs rather than filters or beauty retouch. Do not prescribe one focal length as a biometric guarantee. If sources conflict because of expression, perspective, age, grooming or lighting, record that possible cause and resolve only the conflict affecting the output. Never average two people's faces into a new identity.

Label orientation explicitly: subject-left, subject-right or viewer-left/right. A selfie may be mirrored; record orientation as Unknown until the image or user resolves it. Do not flip a mark, text, parting or asymmetry merely to fill a symmetrical grid.

## Preserve raw realism without caricaturing skin

Keep visible natural texture, facial asymmetry, age cues, ordinary highlights and the supplied grooming. Avoid inventing pores, scars, fatigue, dirt or exaggerated wrinkles as shorthand for authenticity. Match the amount of detail to viewing scale and focus. Preserve coherent eye moisture, eyelid contact, hair edges and neck/ear transitions; extra sharpening cannot repair wrong facial geometry.

If the brief requests a different environment or light, distinguish the permitted appearance change from an identity change. Warmer illumination can change visible colour without authorizing a different complexion. An expression may move cheeks and eyelids without authorizing slimmer cheeks or larger eyes. Keep requested illustration or 3D styling intact.

## Build the sheet in two layers of authority

1. Inventory the supplied source aliases, actual availability, useful views and property authority.
2. Specify only needed panels, with one main comparison purpose per panel.
3. Keep a neutral anchor visible or separately attached when useful; preserve its actual revision.
4. Separate identity views from costume options and expression options when one crowded sheet would confuse them.
5. Mark new generated views as candidates. They do not become evidence about the real person simply because they look plausible.
6. If the user has requested an acceptance sequence, carry forward only the exact accepted candidate. Do not claim acceptance from silence.
7. Bind the selected individual asset to each downstream request. A sheet title or filename does not attach it to a generator.

Use the [identity packet](../assets/identity-packet.template.json) for multi-request work and the [worked scenarios](../assets/identity-worked-scenarios.md) when deciding what to ask or preserve. For one portrait, keep these decisions in a short handoff rather than exposing the entire packet.

## Diagnose the smallest cause of drift

| Symptom in an inspected output | Check first | Repair scope |
|---|---|---|
| Similar person, wrong jaw or eye spacing | Identity source binding and competing faces | Restore the actual identity source; narrow the edit to face geometry |
| Correct face, wrong glasses or costume | Which source owns each accessory and garment | Rebind wardrobe/accessory properties without redesigning the face |
| Front view works, profile changes identity | Missing profile evidence versus candidate invention | Obtain the useful source or retain the strict unresolved constraint |
| Skin looks waxy | Smoothing, light response and texture at actual display size | Repair skin rendering while protecting facial geometry and colour intent |
| Different identity in one panel | Individual panel source and revision | Replace only the failed panel; inspect the sheet again for consistency |

Do not diagnose an unseen output from its filename. Treat user-reported defects as reports until the media can be inspected. Model selection follows [reference capability evidence](../../tool-routing-cost/references/reference-capability-routing.md); no named generator is permanently best for all humans.
