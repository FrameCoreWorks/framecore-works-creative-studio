# Exact-copy compositing

A static graphic can carry its text in two ways. Choose one per deliverable, say which in one sentence, and let the user's explicit choice win.

| Route | Default for | How |
| --- | --- | --- |
| **One pass** | concepts, mood boards, art-led lettering, a short headline that is part of the picture | One integrated generation prompt with the exact copy, as the [text policy](../../pipeline-core/references/text-image-generation-policy.md) describes; inspect every letter of the actual render |
| **Exact copy** | client finals whose text must be right: a price, a date, an address, a phone number, a URL or code, a logo, a legal or Omnibus line, small text, body copy beyond a short headline, print files with bleed | A background without text, then every word, price and logo set by the [static compositor](../assets/static-render/README.md) in a real font at the exact size |

Switch a one-pass deliverable to exact copy when an inspected render misspells a word or a Polish letter, invents text, or cannot hold the copy at a readable size; do not regenerate the same prompt hoping for better letters. Exact copy needs code execution with Python and Pillow; without it, keep one pass and inspect the text.

## Steps

1. **Lock the inputs.** The exact strings (with approved line breaks), the size from the [presets](../assets/static-render/presets.json) or the user's own specification, brand colours, the user's fonts if they have rights to them (otherwise a [bundled font](../../pipeline-core/assets/fonts/README.md)), and the logo as a PNG with transparency. A claim, price or legal line follows the claim ledger and the research gate; the compositor sets text, it does not check that it is true.
2. **Plan the layout first.** Give each text block a box and decide where the picture must stay calm: a band for the headline, a corner for the logo, a strip for the price and the legal line. On a 9:16 placement keep text inside the safe area.
3. **Make the background for that layout.** A generation prompt describes the subject, light and composition and reserves the text zones in plain words ("the lower third is calm, dark and empty for a headline"); it asks for no text, letters, logos, signage or watermarks anywhere. A supplied photo or a flat colour works too. Inspect the background at full size before setting type on it.
4. **Write the spec and compose.** Use `fit: "shrink"` with a sensible `min_size` for headlines of uncertain length; never crop. Read the summary: `text_overflow` or `missing_glyphs` means changing the size, box, font or (with the user) the copy; a failed contrast means a gradient, a scrim, a badge or another colour; a safe-area warning means moving the block.
5. **Look at the result.** Open the PNG at full size and at phone width (about 360 px wide) before delivering; the audit proves the text is complete, not that the design works.
6. **Deliver honestly.** The PNG or JPG at the exact size, the PDF for print with its bleed, the spec (`*.static.json`), the background's source or prompt and the audit. State whether the PDF is RGB or converted with the print shop's profile, and that a raster logo is not a vector master.

## Revisions

Change only what the user asked in the spec, compose again and keep the previous files; name the new ones with a revision suffix (`-r2`). A copy change goes through the same overflow and contrast checks.

## What it does not do

It does not judge taste, check facts, vectorise a logo, embed fonts in an editable layout or produce a CMYK file without a profile. An editable layout for a print shop or an agency (InDesign, Affinity, Figma, Canva) is a separate deliverable that the user asks for.
