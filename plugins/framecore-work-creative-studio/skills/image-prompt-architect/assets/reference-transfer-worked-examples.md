# Worked transfers: source roles become complete prompts

Original synthetic teaching cases, 2026-09-28. These are not generated images,
real user assets, benchmark results or descriptions of files inspected during
this build. In each hypothetical case, the stated inputs have been supplied and
inspected. For a real request, confirm its own assets and facts before using
this pattern. Reference numbers below are local prose aliases, not native
syntax or evidence of attachment. The actual tool must receive those images.

## Example A: identity from a portrait, construction from a jacket

**User-authorized task:** edit the garment only in a 4:5 waist-up portrait.
Preserve the person's face/head, hair, visible body proportions, pose, crop,
background and lighting. The second image supplies a front view of an unbranded
slate-blue canvas jacket on a mannequin. It clearly shows a short standing
collar, one central zip and two symmetric slanted welt pockets. These are
fictional source facts for this exercise. The portrait is frontal enough that
no unseen jacket-back construction is required.

| Input | Governs | Suppressed |
|---|---|---|
| Reference 1: accepted portrait base | Identity, visible body, pose, camera, existing scene | Existing garment is the permitted replacement |
| Reference 2: garment photo | Jacket silhouette, collar, zip, pockets, material and color | Mannequin body, background, camera and lighting |

**Decision:** source-bound edit; fit changes and fabric folds at the body's
contact points are allowed, while sewn construction stays fixed. No identity
pack, extra style source, new pose or text is needed.

```text
Edit Reference 1 to replace only the person's existing upper garment with the jacket shown in Reference 2. Return one vertical 4:5 waist-up portrait with the same person, pose, camera viewpoint, crop, background and lighting as Reference 1.

Reference 1 is the sole authority for the person's recognizable face and head, eye shape and spacing, nose, mouth, jaw, hair, expression, gaze and visible body proportions. Keep those relationships intact. Reference 2 supplies only the jacket, not the mannequin's body, the setting or the photographic treatment.

Reproduce the source jacket's slate-blue canvas, short standing collar, single central zip and two symmetric slanted welt pockets. Preserve the source collar shape, zip path, pocket construction, sleeve attachment and visible seam placement. Fit the jacket to the existing shoulders and torso of Reference 1. Allow only the folds and contact adjustments needed to dress that unchanged body; keep the neck-to-collar junction plausible and the visible zip continuous.

Integrate the jacket into the existing light with coherent fabric shading and appropriate matte canvas response. Keep the person's face and the useful visible jacket structure readable at the source's focus level. Preserve the jacket's source color character under that light. Add no new seams, pockets, fasteners, accessories, logos or visible wording. The result should read as the same accepted portrait with a different, source-faithful garment.
```

**Prospective checks:** face/eye/head relationships match Reference 1; mannequin
proportions have not transferred; each jacket feature matches Reference 2;
collar/shoulder joins are plausible; pose, frame and background remain protected.
A matching blue shade does not compensate for invented pockets. None of these
checks has been performed on a render here.

**If the source differs:** do not keep the fictional color or construction just
because this example names it. Replace the full prompt with the real observed
source facts. If the actual brief needs the unknown back, request that view or
agree a different composition before claiming source-faithful transfer.

## Example B: transparent product with a new support

**User-authorized task:** replace a white sweep and support behind a fictional
clear bottle with a warm-grey plaster field and pale matte stone. The actual
hypothetical edit base shows a black closure and a cream label carrying only
`NURT`. Bottle geometry, camera, framing, focus, label design and this exact word
are locked. Only physical interactions caused by the new surroundings may
change. No person, extra product, liquid, ingredient or marketing claim is added.

**Decision:** preserve the product view; replace the setting to fit its existing
projection. Change only relevant old-environment reflections/transmission and
the support shadow. A new viewpoint would expose unsupported surfaces and is
outside this instruction.

```text
Edit the supplied bottle photograph. Replace only the white studio background and its support surface with a quiet warm-grey plaster background and a pale matte stone support. Preserve the original bottle silhouette, proportions, closure, fill state, camera position, viewpoint, framing, scale and product focus.

Keep the black closure and the cream label's geometry, placement, colors and printed design unchanged. The label's only visible wording is exactly "NURT". Preserve that word character-for-character, at its existing size and hierarchy. Do not add any other words, logos, badges, contents or props.

Fit the new surroundings to the existing camera and bottle. Keep the resting plane believable and the bottle grounded by a coherent contact shadow. Adapt only the glass reflections, transmission of the new background and local edge integration that must change because the setting has changed. The glass should remain visibly transparent with source-faithful thickness and contour; it must not become opaque or acquire a painted outline. Preserve the label's readable surface and the product's established local colors while keeping the reflection pattern consistent with the new environment.

Return one revised product image in the original aspect ratio. Keep every unrelated product feature and compositional relationship intact. The required change is the new background and support with their necessary physical interactions, not a redesign of the bottle or its label.
```

**Prospective checks:** NURT remains exact; bottle and closure construction match
the base; the new support agrees with camera and contact; no old white-sweep
fragment is embedded in a transparent area; no invented contents or claims.
If literal old-reflection pixels must also stay unchanged, this is a conflict
to resolve, not a reason to quietly change the preservation contract.

## How these examples connect to evidence

They implement the original Studio procedures in
[reference transfer](../references/reference-transfer-playbook.md) and
[capture/material construction](../references/capture-and-material-recipes.md).
Those references contain the source-to-rule map and evidence limits. No source
photograph, protected layout, native generator control or empirical success claim
has been copied into these examples. A complete prompt still needs a supported,
authorized route and actual output inspection before acceptance.
