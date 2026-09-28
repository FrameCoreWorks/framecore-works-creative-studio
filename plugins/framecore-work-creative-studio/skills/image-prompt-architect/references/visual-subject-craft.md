# Visual Subject Craft: People, Wardrobe, Products, and Photographic Coherence

Status: stable craft reference synthesized for the Creative Studio runtime. This module is generator-neutral. It is not a current model catalog, a camera-metadata guarantee, a legal review, a video-prompt adapter, or permission to execute a provider.

## 1. Scope and retrieval

Read this reference when a prompt materially depends on one or more of the following:

- a realistically photographed person, portrait, model, avatar, group, or person-product interaction;
- identity continuity, a likeness-preserving edit, or several images of the same person;
- wardrobe, fashion, footwear, bags, jewelry, or other body-worn products whose construction must remain true;
- a real commercial product, package, variant, label, mechanism, claim, scale, or buyer-facing asset;
- a staged photographic scene where camera, light, material, contact, or environment integration determines credibility;
- a still image deliberately prepared as a possible image-to-video starting frame.

Do not load it for a purely typographic or abstract graphic with no meaningful photographed subject or product truth. For finished posters and other text-bearing static raster graphics, also follow the existing one-pass integrated-artwork, exact-copy, and reference-binding contracts. This reference adds subject and photographic craft; it does not authorize a text-free background followed by overlays, a second generation stage, compositing, or manual repair.

Use the smallest relevant slices. A portrait prompt does not need the product category library; a pack shot does not need a face dossier. In Quick work, keep the source facts, highest-risk interaction, camera/light logic, and acceptance check concise. In Deep work, expand only the properties that materially affect the asset or interact across references.

## 2. Authority before adjectives

Before writing visual language, establish what is known, where it comes from, and what remains unknown. Separate:

1. **Source-observed truth**: clearly visible in an attached, usable reference or supplied document.
2. **User-declared truth**: explicitly stated as fact or approved direction by the user.
3. **Design choice**: a proposal the user has delegated or selected; it is not product evidence.
4. **Inference**: a plausible interpretation that has not been established as fact.
5. **Unknown / unsupported**: not visible, not supplied, or too ambiguous to trust.

Do not promote inference into factual copy, product construction, identity, or proof. If a missing fact is consequential to the requested output, ask one focused question or state the limitation and narrow the asset. Do not stop for details that cannot affect the crop, task, or acceptance test.

For every high-value prompt, resolve the brief at a useful minimum:

| Decision | Resolve |
|---|---|
| Asset job | What this image must communicate, demonstrate, or preserve |
| Subject truth | Person/character status, product/SKU/variant, wardrobe, and visible invariants |
| Source authority | Which actual asset controls each important property |
| Framing | Shot size, visible area, orientation/ratio, crop, and viewing scale |
| Priority | The first read and the evidence or action that supports it |
| Creative freedom | What may change, what is locked, and what is unknown |
| Acceptance | A small set of visible conditions that can be checked in the render |

Do not claim that listing these fields validates the image. A prompt contract and a visual review are different evidence states.

## 3. Bind references by property

Use the actual supplied images or assets and the authoritative alias map. If an upstream reference-pack contract exists, preserve its aliases, roles, locks, and suppression rules exactly. Do not invent a missing carrier, silently remap an alias, or treat a filename or prose mention as an attached reference.

Assign one primary job to each reference. A reference may contribute secondary evidence only when explicitly useful; it must not become an unbounded style vote.

| Reference role | May govern | Must not silently govern |
|---|---|---|
| Identity | The named person's visible identity anchors | Another person's body, wardrobe, age, or styling |
| Body / proportions | Build, proportions, stance, or scale relationship | Face identity unless it is also explicitly the identity source |
| Garment / accessory truth | Construction, silhouette, material, color, fit, pattern, hardware, label placement | The source model's face/body or a different SKU |
| Product truth | Geometry, variant, material, package, label, controls, visible included parts | Mood, invented functionality, unsupported claims, or hidden surfaces |
| Pose / blocking | Action, limb placement, screen position, contact, and spatial relationships | Face, body build, clothing, or product design |
| Camera / layout | Framing, viewpoint, crop, spatial hierarchy, and negative-space placement | Unapproved copy, brand marks, or product facts |
| Lighting / material | Direction, contrast, reflection character, finish, or atmosphere | Recoloring protected truth surfaces or replacing product identity |
| Style / mood | Selected formal qualities, palette relationships, or treatment | Identity, exact copy, SKU, package, construction, or evidence |
| Edit source | The artwork and properties that are actually being changed | Permission to redesign every other property |

### Property-level conflict protocol

Resolve authority separately for identity, body, pose, wardrobe, product geometry, color, material, label/copy, camera, light, and environment. There is no universally correct single ranking for every image.

- If two references conflict on different properties, bind each property to its proper source and state suppression boundaries.
- If they conflict on the same material property (for example, two different label versions or two different faces), do not average them. Ask which source wins or block only the dependent part of the prompt.
- If a secondary effect must change because a permitted edit changes its cause, name that limited effect as allowed (for example, a new background light can alter glass reflections while the product silhouette and label remain locked).
- Preserve the clean accepted source as the base of an edit. A later attractive but unvalidated output does not automatically become a new master.
- A text description or repeated seed can support resemblance; it is not proof of strict identity or product continuity across independent generations.

### Reference quality and uncertainty

Check resolution, subject size, focus, crop, occlusion, distortion, retouching, lighting/color contamination, view coverage, and whether the source actually reveals the feature needed. Record uncertainty plainly. A single frontal product image does not prove the back, interior, ports, hidden closures, package contents, or internal mechanisms. A single portrait does not prove unseen profile geometry or full-body proportions.

Never strengthen weak reference evidence with more elaborate prompt adjectives. Simplify the requested view or ask for the missing authoritative source.

## 4. Human plausibility: structure, action, and scale

Photographic credibility depends on agreement among identity, anatomy, pose, contact, surface behavior, optics, light, environment, and asset purpose. Detail is downstream of structure: pores, grain, and sharpness cannot fix a wrong face, impossible joint, distorted perspective, or floating hand.

Use this repair and prompt-construction order:

1. identity status and visible identity anchors;
2. skull, face, body, and joint geometry;
3. balance, pose, hand/foot action, and contact;
4. camera distance, perspective, crop, and focus;
5. light direction, exposure, and environment integration;
6. skin, hair, fabric, and accessory behavior;
7. restrained processing and scale-appropriate surface detail.

### Identity and casting

First distinguish an original fictional adult, a user-authorized likeness, and a fictional composite. Use only visible or user-supplied traits. Do not infer sensitive or private attributes from an image, imply that a synthetic person is an actual named individual, or use a celebrity as a shortcut for a new face.

For a reusable realistic identity, choose a small set of relational anchors that can survive angle and expression: face length/width, brow and eye relationship, nose bridge/tip, cheek and midface, mouth/philtrum, jaw/chin, hairline, apparent age, and stable visible marks. Keep body baseline separate from face anchors. Do not use beauty terms such as “perfect,” “flawless,” or “model-like” as identity controls.

Separate stable identity from temporary state:

- **Stable**: face/skull relationships, visible age presentation, natural asymmetry, hairline/base hair characteristics, body baseline, and intentionally supplied stable marks.
- **Controlled state**: expression, gaze, pose, body tension, grooming, and allowed hair styling.
- **Session styling**: wardrobe, accessories, makeup, camera, light, grade, and environment unless expressly locked.

Do not accidentally convert makeup, an expression, a lens distortion, or one outfit into an immutable identity feature. For strict continuity, bind an approved identity carrier to each independent generation and label unvalidated views as uncertain. Change one major axis at a time while the identity is still being validated. Reject a visually attractive render if a major identity anchor or body baseline has drifted.

### Staged validation for reusable multi-view identities

Use this sequence only when the brief needs a reusable identity pack; a one-image task does not require a character-sheet workflow. Keep the last accepted master as primary authority and add views only as the intended asset use requires:

1. Establish or confirm a neutral front master and its visible identity/body anchors.
2. Validate left and right three-quarter views against that master.
3. Add profile views only when needed, after the three-quarter geometry is stable.
4. Add a neutral full-body view when body proportions, garment fit, or movement requires it.
5. Validate only useful, restrained expressions; then test controlled hair/grooming/wardrobe changes.
6. Test environment/light/treatment changes and downstream-specific anchors (for example fashion, e-commerce, talking-avatar, or I2V) after the identity views they depend on have passed.

This is a risk-aware order, not a required number of images or an instruction to create every view. During initial validation vary one major axis at a time: viewpoint/lens; expression; hair/makeup/grooming; wardrobe/body visibility; or lighting/environment/treatment. Combine axes progressively only after the required views are stable.

Apply the evidence labels in [Evidence labels](#evidence-labels): a prompt preflight is not image validation; an unreviewed generated view remains a candidate. Promote a view to a reusable identity anchor only after its actual render has been visually checked against the last accepted master and accepted for the stated use. Record which view and features it validates, its conditions, and its source alias. If a view fails or has unresolved drift, do not use it to build dependent views or replace the master. Return to the last accepted master, preserve passed locks, correct one cause at a time, and recheck. A textual description or repeated seed cannot prove visual continuity. If the image is not actually available for inspection, say so and keep the view unverified. A prompt-only request may still receive the whole planned view set as standalone conditional prompts: carry only established facts, name future source/binding dependencies, and mark dependent execution pending. This does not promote an unseen view, bypass validation during production, or relax strict identity without the user's explicit decision.

For multiple people, give every person a distinct alias, actual identity reference, body/wardrobe ownership, screen position, action, and interaction. Define which hand/prop belongs to whom. Use clear blocking before complex overlap. Do not pool a group into one identity description or allow faces, garments, accessories, or limbs to migrate between people.

### Anatomy and pose as a connected mechanical system

Specify the action, not a generic “natural” or “dynamic” pose. A legible human pose has a support system:

- feet establish the floor plane, stance, and pressure;
- the pelvis and rib cage establish balance and spinal curve;
- shoulders and arms counterbalance the torso;
- the neck and head respond to the torso orientation;
- elbows, wrists, knees, and ankles bend on plausible axes;
- weight shifts create believable compression in the supporting shoe, seat, wall, or garment;
- occlusion makes it clear which limb passes in front and where it connects.

For every visible hand, define its job (rest, point, hold, adjust, apply, operate), visible side, contact points, finger state, wrist angle, and pressure appropriate to the object. A grip must agree with scale, center of mass, friction, product shape, and the feature/label that needs to remain visible. Keep contact shadows and reflections consistent. Avoid hiding all important hands, merged fingertips, impossible thumb placement, floating products, and objects that do not respond to grip.

For feet and full-body work, resolve footwear orientation, sole contact, weight-bearing leg, ground plane, and cast/contact shadow. Do not crop a critical joint, hand, foot, or product detail accidentally. In seated/leaning poses, identify the support surface and visible compression. For crossed limbs, make the overlap order readable.

Keep expressions mechanically coherent: gaze target, eyelid/brow state, cheeks, mouth tension, jaw, and neck should communicate the same intent. A smile may change soft tissue; it must not silently replace the person's jaw or face geometry. Both eyes share a credible gaze/perspective and a catchlight pattern explained by the light setup.

### Human detail budget by framing

| Framing | Prioritize | Do not waste prompt density on |
|---|---|---|
| Beauty macro | visible facial planes, skin zones, cosmetic edge, eye/lip surface, focus plane, controlled highlight | unseen body or wardrobe inventory; universal pores |
| Portrait | relational face geometry, gaze, expression, hairline, neck/shoulder connection, directional skin light | microscopic grit across every surface |
| Chest/waist-up | identity, shoulder/torso posture, hand task, sleeve/cuff, product contact | invisible weave or hidden footwear |
| Three-quarter/full body | proportion, support, limb separation, garment silhouette, shoes, floor contact, camera height | close-up pore description that cannot resolve at scale |
| Environmental/group | silhouette, action, spatial relation, scale, motivated light, set contact, useful identity cues | facial or textile microdetail beyond the final viewing size |

Surface detail must fall away with distance, depth of field, light, motion, and output size. Natural asymmetry is not permission to invent scars, acne, sweat, dirt, fatigue, or damage. Do not replace individual skin with either plastic smoothing or stamped pores. Hair needs a believable hairline, roots, major masses, strand direction, gravity, and only a restrained number of flyaways.

## 5. Wardrobe and worn-product truth

Treat a garment as a constructed object worn by a particular body, not as a color label. At minimum, resolve the facts visible in the intended frame:

- category, silhouette, length, volume, fit/ease, and body relationship;
- fabric family, weight, stiffness/stretch, opacity, finish, and visible-scale structure;
- panels, seams, darts, pleats, collar/neckline, sleeves/cuffs, hem, closure, pockets, and hardware;
- print/logotype placement, scale, orientation, repeat, and color when actually supplied;
- layer order, accessory ownership, and the parts that must remain unobstructed;
- known/unknown views and details.

Large-form truth comes first. A wrong silhouette, garment category, fit, or fabric class is a product failure even when small texture looks plausible. Do not invent unseen lining, back construction, pockets, closures, branding, fit, hardware, or material. Separate styling direction from garment evidence. Never transfer the identity/body of a garment-reference model to the target person.

### Material behavior, not texture labels

Describe physical response only where visible and relevant:

- **Cotton/poplin**: crisp but not rigid folds, a fine weave only at close scale, and mostly matte response.
- **Denim/twill**: directional weave, seam/topstitch structure and firmer folds; distressing only if sourced.
- **Wool tailoring**: dense, controlled drape, shaped lapels, stable shoulders, and restrained surface texture.
- **Silk/satin/fluid synthetics**: gravity-led folds and directional highlights, not metallic mirror glare or melted edges.
- **Knit/jersey**: stretch and recovery around body/joints with rib direction following the panel.
- **Leather/coated surfaces**: edge thickness, finish, grain scale, and localized creasing at flex points.
- **Technical shells, mesh, lace, sequins, fringe, or fine repeats**: treat as high-risk surface structures; define scale, attachment, orientation, transparency, and motion sensitivity only if the source supports them.

Folds should follow support, seam placement, movement, tension, and gravity; they are not decorative wrinkles painted uniformly over the body. Fit must not cling and float at the same time. Layered garments occupy a plausible order and volume. Jewelry, watches, glasses, bags, and shoes need attachment, side/hand ownership, scale, and contact; reject floating straps, duplicated pieces, swapped sides, impossible shoe pairs, or fused accessories.

Choose a fidelity level consistent with the task: exact commercial/catalog truth; controlled campaign representation where the SKU remains recognizable; or explicitly identified concept visualization for a hypothetical product. Never quietly downgrade exact-SKU work to concept art because sources are weak. A pose must reveal the buyer-relevant garment or accessory property; drama that hides the item is not a successful commerce frame.

### Category-specific truth deltas

These are prompts for source inspection, not complete category manuals. Apply only the relevant row and never infer missing facts:

| Category | Lock / inspect | Common false implication to suppress |
|---|---|---|
| Beauty and skincare | Container, applicator, fill/formula appearance, label, variant, plausible amount and application area | Clinical, medical, anti-aging, efficacy, ingredient, or before/after claims not approved for this asset |
| Jewelry and watches | Piece/stone/link count, setting, clasp, dial/markers/hands, finish, scale, and skin attachment | Invented carat, hallmark, certification, movement, duplicate stones, floating or multiplied links |
| Electronics | Housing, screen/bezel, ports, controls, modules, accessories, supplied interface, and scale | Unprovided UI, compatibility, battery, speed, waterproofing, safety, or performance claims |
| Food and beverage | Package/variant, serving/count, preparation state, portion, color, and supplied ingredients | Nutrition/health/origin claims, false freshness, or props implying absent ingredients |
| Home, furniture, and decor | Dimensions/scale source, configuration, silhouette, materials, joinery, modules, hardware, upholstery | Hidden-side invention, impossible room geometry, wrong scale, or extra matching pieces |
| Children's products | Exact included pieces, packaging, supplied age information, scale, and plausible use | Unsupported age suitability, safety certification, developmental outcome, or missing/extra components |
| Supplements and regulated wellness | Exact package, dosage form/count, variant, and approved wording | Medical/therapeutic, physiological, weight-loss, clinical, certification, or transformation claims without current authorization |
| Automotive and industrial | Part/connection geometry, material/finish, supplied dimensions, model/variant fitment, installation context | Unverified compatibility, load/safety rating, compliance, operating condition, or performance |
| Digital products and services | Approved interface/workflow, supplied brand, user-approved metrics and integrations | Invented UI, customer data, outcomes, testimonials, logos, or integrations |
| Pet products | Product geometry, size, fastening/material, packaging, supplied intended use | Veterinary, health, calming, nutrition, safety, or performance claims not approved |

Luxury, marketplace commodities, and general campaigns use the same evidence rules: craft detail or premium staging is not proof of heritage, authenticity, scarcity, rating, certification, or superiority. For channel-specific publication rules, run the current research workflow; this stable craft reference is not a platform-policy source.

## 6. Commercial product truth and claim control

For any real product, preserve exact product/SKU/variant before mood or styling. Identify the asset role and the buyer uncertainty it answers: recognition, scale, material, construction, use, fit, contents, variant difference, trust, or desire. One frame should lead with one primary question and at most a compatible secondary question.

### Product coverage

For each requested visible property, record what source proves it. A useful source can be authoritative for one property and weak for another: approved flat artwork may govern label copy; neutral product photography may govern color/finish; technical data may govern geometry or dimensions. A lifestyle image does not establish hidden product facts.

Before promising a side, macro, interaction, component, mechanism, scale, package, or result, verify that the actual sources cover it. Mark coverage as direct, low-risk/simple inference, or unsupported. A simple rotation of a plain, featureless object may be a limited inference; do not infer hidden labels, ports, contents, mechanisms, ingredients, seams, or legal copy. Ask for a source or revise the shot when high-risk coverage is unsupported.

Lock as applicable:

- exact SKU and variant;
- geometry, proportions, components, controls, hardware, closures, and state;
- color/finish and the source that establishes it;
- material, transparency, internal contents, and supported surface behavior;
- package, labels, logo, exact legible copy, and included-item count;
- dimensions/scale source, use state, and the allowed human interaction;
- explicitly unknown or hidden features.

For a product-human image, define actor position, left/right hand assignment, product orientation/state, contact points and grip, the buyer-relevant feature, and any secondary physical changes allowed. The person must not cover the commercial proof. Simplify a risky gesture rather than compromising anatomy or product truth.

### Claims ledger

Treat visible words and implied proof as controlled facts:

- **User-approved exact copy**: preserve character-for-character unless the user explicitly approves a revision.
- **Supplied claim not yet approved for this asset**: do not place it as final; ask or keep it out.
- **Directly observable form**: may be depicted without turning it into a performance, quality, safety, or quantified claim.
- **Inference**: ask or remove; atmosphere is not evidence.
- **Regulated/high-stakes claim**: require current authorized wording and review by the appropriate owner; do not present this skill as legal approval.
- **Fabricated proof/social proof**: remove.

Never invent a price, discount, scarcity, rating, review, award, bestseller label, certification, warranty, compatibility, safety approval, ingredient, medical/clinical/nutrition/sustainability/performance result, test result, comparison, before/after, testimonial, bundle item, or number. A glossy surface does not prove durability; a laboratory look does not prove efficacy; athletic casting does not prove performance. Do not use visual props or labels to imply what the user has not established.

For any visible text in a static graphic, maintain the existing exact-copy inventory and no-extra-words rule. Keep source-printed product labels distinct from campaign copy; reproduce only supplied/legible/approved text, preserve the actual source asset role, and do not reconstruct unreadable microcopy from guesswork. Do not create an extra slogan, badge, or logo to make the composition feel complete. If the desired visible copy is unknown, stop before final text-bearing prompt compilation and resolve it.

## 7. Camera, composition, light, color, and material coherence

Begin with one visual thesis and the first/second/supporting read. Craft choices must reinforce that message and the product/person role. Avoid piling up unrelated “premium,” cinematic, editorial, and technical cues. A professional image is authored through consequential choices, not adjective count.

### Designed specificity, not a stock placeholder

Make the image feel intentionally art-directed by giving it a concrete visual mechanism: a consequential subject/action, a deliberate camera-to-subject relationship, a motivated light/material interaction, a purposeful environment or negative-space shape, and a clear hierarchy. The mechanism must arise from the brief, selected direction, or user-approved exploration; do not invent a brand story or product benefit.

Reject default filler when it has no stated job: generic influencer casting, a centered packshot with unrelated props, anonymous luxury beige, generic gradients, gratuitous rim lights, floating product geometry, decorative lens effects, random grain, stock-photo smiles, or excessive microtexture. Specificity means better decisions, not more objects. Keep one dominant visual act and let supporting elements prove, contextualize, or deliberately contrast with it. An empty area is useful only if it serves the crop, text hierarchy, or focal balance.

### Composition and viewing scale

Resolve subject occupancy, focal order, camera relation, negative-space job, crop boundaries, and what must stay readable at thumbnail or mobile size. A hero, label, hand action, garment silhouette, and headline cannot all be the primary focus at once. Use contrast, placement, scale, sharpness, color isolation, light, depth, and directional lines to establish hierarchy. Keep truth-critical features inside the useful focus/contrast zone.

Do not crop through eyes, mouth, fingers, wrists, knees, ankles, critical garment edges, controls, closures, labels, or hero product details accidentally. Intentional edge crops should communicate scale or energy. Full-body frames need the footwear/floor relation when it is part of the deliverable; catalog garments need enough outline to judge fit; a still intended as a video start needs space for its anticipated motion.

### Camera and perspective

Specify visible effects, not equipment prestige: camera height, distance impression, viewing angle, subject scale, perspective character, horizon/verticals, focus target, and depth behavior. A wide close camera enlarges near features and limbs; a greater distance with portrait-like compression produces a different relationship. Lens numbers can guide appearance but do not guarantee capture metadata or excuse conflicting geometry.

Choose camera logic for purpose: straight-on for honest geometry/labels, three-quarter for volume, moderate portrait perspective for identity, deliberate wide angle only when spatial energy and its distortion are intentional, overhead for organization/flat lays, macro for a source-supported detail. Keep all visible face/body/product planes consistent with one viewpoint. Never claim a focal length, aperture, sensor, EXIF, resolution, or photographic process as guaranteed output unless the actual workflow supplies verified controls.

### Camera reframing: crop, viewpoint, and newly visible truth

Classify the requested change before writing a prompt. These are different operations:

| Operation | What changes | What can normally remain the same | Main limit |
|---|---|---|---|
| Crop or recompose at a fixed viewpoint | Canvas bounds, scale in frame, or placement; the camera's spatial viewpoint stays fixed | The source projection and already visible surfaces, subject to the actual crop/edit capability | Cropping cannot reveal a surface that was hidden in the source |
| Change camera viewpoint | Camera position/height/distance or viewing angle, potentially with a changed frame | Named identity, product facts, set anchors, and design intent may be protected as semantic properties | Perspective/projection, relative scale, parallax, overlap/occlusion and crop can change; a new view may expose unsupported surfaces |
| Redesign the scene or layout | Objects, blocking, environment, or visual hierarchy beyond the camera change | Only the properties explicitly locked by the user or authoritative references | Do not treat a request for camera reframing as permission for a broad redesign |

For a reframing request, resolve in this order:

1. **Name the camera variable**: angle/view direction, height, distance/perspective, or crop. Do not substitute one for another. If several changes are requested, identify the coupled effects and ask only about a consequential unresolved tradeoff.
2. **Separate locks from scene anchors**: list truth-critical identity/product/person properties separately from background/set elements that should remain recognizable. A semantic anchor such as “the same window remains behind the table” is not a promise that its pixels, outline, or exact placement remain identical under a new viewpoint.
3. **Check view coverage**: determine which sides, labels, anatomy, construction, or environment surfaces the supplied material actually establishes. Textual description can establish user-declared facts; it does not establish that an image was visually inspected. Mark unshown surfaces unknown.
4. **Account for spatial consequences**: a changed viewpoint can alter apparent proportions and distances, reveal or hide objects through parallax and occlusion, change perspective convergence, and require a different crop. Describe the visible target result, not only a camera-motion label. Avoid promising calibrated degrees or exact geometric reproduction unless the real workflow provides and verifies that control.
5. **Choose a feasible preservation contract**: protect semantic identity and stated scene relationships where compatible with the new view; do not promise pixel-identical background preservation from prompt prose alone. If exact pixels are essential, explain that the requirement needs a separately evidenced pixel-preserving method and may conflict with revealing a new viewpoint. Never imply such a method is available or authorized unless it actually is.
6. **Resolve unknowns before release**: when the target view depends on a hidden, truth-critical surface, request an additional source view or offer the bounded alternative of keeping the current viewpoint/crop. Do not invent the unseen side as product/person/environment truth. If the user explicitly authorizes a speculative concept, label the invented area as interpretation rather than verified continuity.

The final acceptance check should name one observable target and one protected invariant (for example, “the requested left-facing silhouette is visible; bottle silhouette, approved front label, and named window/table anchors remain recognizable; no claim of pixel-identical background”). Prompt construction is not proof that the model achieved it. Review the actual output against the source and the declared acceptance check before calling the reframe successful.

Depth of field is a hierarchy tool. Decide what must remain legible together: both eyes, a hand and product, label and container, garment details, or multiple board elements. Do not use shallow focus to hide an unresolved product/pose, and do not call blur “cinematic” without a focal plan.

### Light and environment

Build one explainable light system: motivating source, size/direction, fill or negative fill, background/separation contribution, practicals, exposure priority, white-balance relationship, shadow density/direction, reflections, and contact. Eye catchlights, face shadows, hair highlights, fabric folds, product reflections, floor contact, and background brightness should agree.

Soft light can retain dimensional shape; hard light needs coherent shadow geometry. Use fill to protect important surfaces without flattening them. Add rim/separation light only when a source or deliberate studio setup explains it. Mixed light can be creative, but must not silently corrupt protected skin, brand, garment, or SKU color.

Integrate subjects and objects through perspective, scale, occlusion, contact/cast shadow, reflected color, reflection/transmission, focus, grain, and atmospheric depth. If something reads as pasted in, repair geometry/light/contact before adding surface texture. Props must explain use, scale, audience, or story; remove props that compete or imply an unapproved ingredient, bundle, function, or claim.

### Material and color

For each visible hero material, resolve substance, finish, roughness/gloss impression, opacity/transmission, microstructure at viewing scale, edge/thickness, deformation/drape, and interaction with the actual light/environment. Use property-specific behavior:

- glass/translucent plastic: thickness, tint, transmission, refraction, edge highlights, contents and background continuity;
- metal: finish/brushing direction, environmental reflection shape, and controlled highlight clipping;
- matte/glossy molded material: edge radius, roughness, wall thickness if visible, and reflections that follow geometry;
- paper/packaging: plane/fold/edge logic, coating or print treatment only when supported;
- fabric/skin/hair: use the relevant scale- and construction-specific guidance above.

Assign functional color roles: protected truth colors (SKU, garment, approved mark, skin), background field, supporting neutrals, accent/navigation, and physically plausible reflected color. Do not apply a grade or colored light that redefines a truth color while still presenting the output as an exact catalog view. Strong campaign color casts require a clear campaign framing and protected product recognition.

## 8. Photo-session systems and still-to-video boundary

A multi-image photo session is a designed coverage system, not a stack of unrelated attractive portraits. Identify each asset's unique commercial, narrative, or continuity job. Share only the camera/light/color/identity/product rules that are actually meant to persist, then write a standalone prompt and attach the correct carriers for every independent generation.

For Deep session planning, define the objective, roles/channels, shared visual thesis/capture system, identity and product/wardrobe authority, permitted variation, shot coverage, source attachments, and acceptance checks. Validate clean identity/product masters before high-risk actions, extreme styling, or campaign variations. For Quick single-image work, do not force a session spreadsheet when the image job is already clear.

### Still frame as a possible image-to-video starting point

The image prompt controls one visible instant. It may establish a readable start state compatible with an intended later motion, but it does not encode the entire motion path, timing, duration, camera movement instructions, dialogue, audio, or video-generator syntax. Those belong to a separate video workflow and must not be smuggled into a still-image artifact.

When the user requests an I2V-ready still, define only the visual facts the still can show: starting pose/action phase, visible gaze, hands/joints/silhouette, travel-space direction, stable identity/wardrobe, simple enough occlusion, and a light/environment setup that can plausibly continue. Do not draw a contradictory midpoint and call it a start frame. Keep mouth/jaw/eyes readable for a talking-head source; do not put dialogue on the image. For walking/turning, preserve balance, limb separation, footwear/floor contact when relevant, and open motion space. For product demonstration, keep the correct state, plausible grip, feature visibility, and action path.

Record a compact motion hypothesis only as a planning handoff when useful: visible start state, likely first action, subject/camera direction, moving secondary elements, expected end-state idea, continuity locks, and highest drift risk. Label it as a hypothesis, not a guarantee. The returned image prompt remains a prompt for a single still. Dynamic model instructions must be researched and routed separately by the video-prompt skill.

## 9. Observable anti-artifact and acceptance checks

Replace vague quality claims with observable checks. “Photorealistic,” “perfect hands,” “premium,” “100% human-made,” or “no AI look” are not acceptance evidence by themselves.

### Human and pose checks

- identity anchors and apparent age presentation match the selected authority; styling changes did not replace the person;
- face planes, eye gaze, expression, head/neck/shoulder relation, and body proportions are mutually plausible;
- support leg/seat, weight distribution, joint axes, hand jobs, grip, finger contact, and occlusion can be understood;
- feet meet the floor where expected; object/body contact has plausible pressure and shadow;
- skin, hair, teeth, and detail density fit the crop, light, and final display scale; no uniform pores, plastic smoothing, copy-paste eyes, halos, smeared edges, or invented “imperfections.”

### Wardrobe/accessory checks

- garment category, silhouette, length, fit, layer order, and source-supported construction remain correct;
- folds and stretch follow seams, gravity, pose, and material; repeats follow perspective without turning to moire/noise;
- labels, marks, print, hardware, accessories, and left/right ownership match the source;
- straps, chains, glasses, shoes, bags, and jewelry attach physically and remain stable;
- the pose reveals rather than hides the asset's commercial priority.

### Product/commercial checks

- exact product/SKU/variant is unmistakable at the intended read size;
- geometry, component count, package, label, controls, material, color, state, and supplied contents match their sources;
- every visible side/detail/claim has adequate source coverage or is explicitly a user-approved concept;
- no unapproved words, pseudo-logo, badge, price, discount, review, certification, ingredient, benefit, or comparison appeared;
- contact, scale, product-human interaction, highlight/reflection, transparency, and support surface are physically coherent;
- the asset answers its named buyer question without misleading staging.

### Capture and composition checks

- first read and supporting hierarchy work at thumbnail/mobile scale;
- crop, perspective, horizon/verticals, focus, and depth preserve all truth-critical details;
- one light system explains highlights, shadows, reflections, skin, garment, and set;
- truth colors are preserved for the declared fidelity level;
- subject/product occupies the environment through scale, occlusion, contact, color bounce, focus, and shadow rather than reading as a cutout;
- no excessive sharpening, false microtexture, repeated pattern noise, unexplained haze, halo, doubled edge, melted label, or decorative detail that competes with the message.

### Keyframe-specific checks

- the image depicts one coherent start instant rather than several action phases;
- tracking-relevant face, hands, limbs, garment edges, and product remain readable;
- there is plausible room in the intended motion direction;
- unstable repeated details or foreground crossings do not dominate the first frame;
- no spoken line, video syntax, or motion guarantee has been embedded in the still prompt.

### Evidence labels

Keep these review states distinct:

- **Prompt preflight passed**: the prompt has coherent instructions, source binding, locks, and proposed visible criteria; no image has been validated.
- **Render visually reviewed**: an actual render was received and inspected against the criteria.
- **Accepted for the stated use**: critical invariants pass for the specific channel/asset job; this does not certify another crop, print specification, legal claim, or future version.
- **Not reviewed / insufficient evidence**: no render, low-resolution render, missing source, unreadable text/label, or no reliable comparison. Do not claim quality pass.

Text lint or schema validation cannot prove a render's visual quality. Conversely, an attractive render cannot waive a failed identity, exact-copy, product-truth, or claim check.

## 10. Cause-led correction loop

For a defective render, first report observable evidence, then a likely cause. Keep observation separate from hypothesis. Name one primary failure and one acceptance test for the next iteration; preserve unrelated accepted properties.

Diagnose in causal order:

| Observation | Likely earliest layer | Targeted next test |
|---|---|---|
| Face feels generic or identity drifts | Authority/identity carrier or too many changed axes | Restore source-bound identity and test stable relational anchors in a simpler view |
| Face/body proportions distort | Camera distance, perspective, or anatomy | Correct camera relationship before adding texture detail |
| Hand/product floats or fingers merge | Pose/contact mechanics or occlusion | Simplify grip and specify exact contacts, pressure, and visible side |
| Garment becomes the wrong category/fit | Garment truth and silhouette | Rebind garment source; correct silhouette/fit before weave detail |
| Repeated print/fabric turns into noise | Pattern scale, view size, focus, or surface density | Simplify or enlarge subject; preserve only source-supported repeat and test at target scale |
| Product label/variant mutates | Wrong authority, insufficient source resolution, or unsupported detail | Reattach authoritative product/label source and protect exact visible text; reject if unverified |
| Product seems pasted in | Perspective, support/contact, shared light, reflection, or color bounce | Fix spatial/light integration, not pores or sharpening |
| Reflections contradict geometry | Material-light relationship or competing reference roles | Bind the reflection/light authority and correct one surface interaction |
| Unapproved claims or words appear | Copy/claims inventory and no-extra-words controls | Reconcile exact visible-text ledger and strengthen source-bound suppression; inspect every word |
| Keyframe is hard to animate | Ambiguous start state, overlap, or no motion space | Simplify to one start pose and test silhouette/limb separation and travel space |
| Result looks overprocessed | Post-processing/detail density | Reduce sharpening, haze, fake grain, contrast, and microtexture only after form/light pass |

Change only what is needed for the next test. If the same root cause persists after a controlled attempt, change strategy, return to a clean validated source, ask for a missing reference, or stop and state the limitation. Do not enter open-ended retries, silently spend credits, switch providers, or treat prompt revision as proof of a corrected render.

## 11. Final prompt compilation boundary

Use this module to resolve source truth and visible craft decisions, then compile through the existing prompt architecture and generator mapping workflow. Do not expose this manual or its schemas unless requested; translate only applicable decisions into plain operational instructions.

For a text-bearing static raster, the final image prompt remains one integrated generation request with exact approved text included. It must preserve source roles, suppress unapproved claims and extra words, and state relevant placement/hierarchy/safe-area behavior as supported by the current artifact contract. Do not create a text-free scene first, plan a post-generation overlay, or suggest a separate video/render stage as a workaround.

Prompt preparation and provider execution remain separate. This reference never grants API/wrapper access, uploads, tool execution, or paid generation. Follow the host's current authorization and execution gate. If the user asks for prompt only, stop at the prompt. If the render has not been received, visual-review status is not run.
