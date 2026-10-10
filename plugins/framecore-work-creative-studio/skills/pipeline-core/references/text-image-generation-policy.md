# Static Raster And Text Image Generation Policy

Generated static raster graphics should use the built-in image generation capability actually exposed by the host by default when available.

This is a native chat-window generation path, not an external provider integration, API key requirement, CLI, or paid media-provider workflow.

Visible text in a static raster has two routes. Choose one per deliverable, name it to the user in one sentence, and follow the user's explicit choice. [Exact-copy compositing](../../static-graphic-design-creator/references/exact-copy-compositing.md) sets out when each is the default.

## One pass

Concepts, mood and art-led lettering use the same built-in generation path in one pass, with the text in the image. The prompt must include:

- exact visible copy
- layout hierarchy
- placement and safe margins
- typography direction
- no extra words and no duplicate text constraints

On this route, do not generate a text-free background first and add text later. Inspect every letter of the actual render.

## Exact copy

A client final whose text must be exact (a price, a date, an address, a phone number, a URL or code, a logo, a legal or Omnibus line, small text, body copy beyond a short headline, or print files with bleed) uses a background without text, generated with reserved calm zones, supplied by the user or flat, and the [static compositor](../../static-graphic-design-creator/assets/static-render/README.md), which sets every word in a real font at the exact size and stops instead of cropping. It needs code execution with Python and Pillow. It is a named route, never a silent substitute: without code execution, or when the user prefers one pass, use one pass and inspect the text.

## No image generation

If the current environment does not expose built-in image generation, stop and ask the user how to proceed. Do not silently replace the path with Python-generated artwork, coded SVG, HTML/canvas or other coded artwork. The exact-copy route may still use a supplied photo or a flat background when the user agrees.
