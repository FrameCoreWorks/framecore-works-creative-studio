# Exact layers in video

Generated video is good at light, space, material and motion; it cannot be trusted to keep a logo, a price or an interface exact from frame to frame. When a film mixes generated shots with brand material, decide for each element who owns it before anything is generated.

| Element | Exact owner | What generation may add |
| --- | --- | --- |
| Logo and wordmark | The supplied vector or raster, or a wordmark set as outlines ([`svg_wordmark.py`](../../static-graphic-design-creator/scripts/svg_wordmark.py)) | Depth, light or material around it |
| Text that must be read: supers, prices, dates, claims, legal lines | A real font set in the edit or the motion layer | The scene behind it |
| Interface and real interactions | A screen capture or a faithful layered rebuild | The space outside the screen |
| Product and packaging | The supplied photo or footage, or a verified product layer | Light, staging and movement around it |
| Numbers and claims | Approved text from the copy pack | Nothing |
| An organic or spatial transformation | Generation, when it adds something code cannot | The transformation itself, inspected at both ends |

## Rules

- **Map the protected moments first.** List every interval where a logo, text, interface or product must be exact and the layer that owns it. A start image guides the first frame's appearance; it does not hold the logo for every frame after it.
- **Remove what the generator damaged.** If a generated shot contains a wrong logo, garbled text or a changed product, cover or remove it. A correct logo laid over a wrong one leaves both visible as soon as anything moves.
- **Exact layers belong to the shot.** They are lit, masked, occluded and moved with it, not stuck on top.
- **Leave it out when covering fails.** If the damaged element cannot be covered cleanly, generate the plate without it and build those moments in code ([Motion Graphics Workflow](../../hyperframes-workflow/SKILL.md)) or in the edit.
- **Check the export, not the plan.** Compare the composite with the source: spelling, geometry, colour, the readable hold and the final frame.

For stills the same split is the [exact-copy route](../../pipeline-core/references/text-image-generation-policy.md).
