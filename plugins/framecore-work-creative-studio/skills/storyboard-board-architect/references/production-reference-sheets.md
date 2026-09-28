# Production reference sheets and individual frame handoff

Use for a precise character, product, coverage or temporal sheet intended for downstream generation. The board is a visual index; each downstream image/video request still needs its own correctly bound source. Source rationale: [expansion evidence](../../research-evidence/references/reference-audio-expansion-sources.md). The contracts and examples here are Studio design, not a vendor schema.

## Pick the sheet's job

| Purpose | Required differences between panels | Keep out unless requested |
|---|---|---|
| Character reference | Needed view, expression, costume detail | Invented story beats, durations or an arbitrary emotion grid |
| Product reference | Visible face, label, construction or physical state | Invented back label, ingredients, certifications or hidden geometry |
| Coverage comparison | Camera views of the same approved state | Unannounced changes of time, wardrobe, prop position or expression |
| Temporal storyboard | Selected event/moment and shot mapping | New events added just to fill the page |

For humans, use [identity guidance](../../character-design/references/human-identity-workbook.md). For a product, assign the supplied packshot authority over silhouette, closure, label and visible material. Keep an unseen back, underside, cap interior or open state Unknown. If product colour is critical, note whether a colour source is supplied and whether the display/output was inspected; a hexadecimal guess sampled from a shadow is not a verified material specification.

## Give each panel a complete production meaning

Carry panel ID, source revision, purpose, selected view or shot ID, depicted moment, source aliases, protected properties, allowed changes, camera/framing, action/state, light, palette, wardrobe/props where relevant, exact visible copy and review state. Use Unknown or not_applicable instead of invented precision.

Temporal panels additionally carry the selected shot's interval and timing basis. Multiple panels can illustrate one shot; they do not each inherit the full shot duration as extra screen time. A held image can represent a longer shot. A static sheet has no measured tempo, movement quality or lip-sync evidence.

Keep internal IDs separate from visible labels. If the user requests visible timing/action/wardrobe notes, supply the exact strings and associate each with its panel. If the user asks for clean reference images, keep those notes in the companion specification. Never silently replace the requested integrated labelled board with a text-free image and a later overlay; offer a separate typeset assembly only when its workflow is authorized.

## Choose readable geometry

Choose a grid from the actual panel count, image aspect ratios, label length and intended viewing size. For many panels, split sheets by scene or property rather than reducing every face or label to a tiny thumbnail. Maintain consistent scale when comparing proportions; declare scale changes for detail insets.

Keep each image's own target framing distinct from the overall sheet format. A 16:9 sheet may contain vertical 9:16 frames. Do not stretch the frame to fit a landscape cell. Use gutters to make boundaries unambiguous and keep labels outside the protected image region when specified. Percentage canvas coordinates are optional and only introduced on explicit user request.

## Deliver the board and source frames according to the request

Distinguish four artifacts: board specification, generated candidate sheet, selected individual frame, and executed video request. Record only the stages actually reached.

- A requested sheet-only prompt ends with that complete prompt and the needed input roles.
- If individual frames are requested, prefer the accepted originals when available. Cropping a sheet is possible only from an actual image and an authorized edit; it does not recreate missing pixels, fix errors or increase source detail.
- Inspect the selected crop for neighbouring-panel leakage, labels, gutters, missing limbs/product parts, and sufficient usable detail.
- If the crop cannot meet framing or identity requirements, describe the necessary reframe/regeneration instead of stretching it or inventing a high-resolution export.
- Name the actual file/attachment and revision that will be bound to the video request. Panel S03 is a location in the plan until a usable image actually exists.

Use [the sheet manifest](../assets/reference-sheet.template.json) for a multi-panel handoff and [the worked sheet](../assets/reference-sheet-worked-example.md) for the distinction between panels and shots. Pass actual selected stills to Image/Video Prompt owners with source authority and readiness intact.

## Review and repair

Check panel count/order, panel-to-label pairing, exact strings, source identity, product state, camera locks and intended-size readability. A failed panel need not invalidate the chosen story; repair its image or annotation locally. If sequence events or timing are wrong, return those decisions to Sequence. If text is wrong, retain the correct image and identify the exact copy repair scope. Do not certify the whole sheet by inspecting only its most prominent panel.
