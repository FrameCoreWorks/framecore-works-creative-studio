# Ad templates and variants

Three 15-second vertical ad templates and a tool that turns one checked contract into a client's branded versions in several languages and formats. Nothing here renders or publishes; it writes contracts and the commands that render them.

## Templates

[`../motion-scenes/templates/`](../motion-scenes/templates/) holds complete storyboards at 1080 x 1920, 30 FPS, 450 frames, each with `4x5` (1080 x 1350) and `1x1` (1080 x 1080) feed formats. Every format passes `check-score.mjs --storyboard` with no warnings, and the renderer reports no text overflow.

| Template | Style | Scenes | For |
| --- | --- | --- | --- |
| `ad-offer` | Sale poster | hook lines, discount counter, three reasons, call to action | a time-limited sale or discount |
| `ad-product` | Product light | product name, three features, rating counter, call to action | one product and its strongest proof |
| `ad-testimonial` | Editorial serif | customer quotation with its author, review count, call to action | a recommendation from a real customer |

The copy is placeholder (`copyStatus: "template-placeholder"`) and `template.replace` lists every copy ID to replace. The approval is `proposed`: a template becomes a contract only after the client's exact text replaces the placeholders, its figures are documented (a rating, a review count, a discount and its terms) and the storyboard is approved. A quotation is the customer's own words used with consent.

## Variants tool

```bash
python3 variants.py templates                                               # list the templates
python3 variants.py brand ad-offer.motion-score.json --brand brand-kit.json --out ad-offer-lipa.motion.json
python3 variants.py expand ad-offer-lipa.motion.json --matrix variants.json --out-dir lipa-variants/
```

- **`brand`** reads a [brand kit](../../../pipeline-core/references/brand-kit.md) and copies its colours into `tokens` (`background`; `foreground` or `text`; `muted` or `secondary_text`; `accent` or `primary`). When the headline font is a [bundled font](../../../pipeline-core/assets/fonts/README.md), it sets `tokens.fontFamily` and declares that family's faces in `fonts`, so the player and the renderer use the same files; a condensed or expanded face is declared only when the kit names it. A font that is not bundled is named in the report: ask the client for the files and their licence and declare them in `fonts`. The report gives the WCAG contrast of each colour against the background and a note when text falls below 4.5:1 or the muted or accent colour below 3:1.
- **`expand`** reads a matrix and writes one contract per variant and a `render-plan.json`:

```json
{
  "formats": ["base", "4x5", "1x1"],
  "variants": [
    {"id": "pl", "language": "pl"},
    {"id": "en", "language": "en", "copy": {"hook-1": "Sale", "hook-2": "until Sunday only", "cta": "Shop now"}},
    {"id": "red", "tokens": {"accent": "#E5322D"}}
  ]
}
```

A variant may replace copy IDs the contract already has, override tokens and set a language; it can never add a copy ID, so no variant shows text the layout was not checked for. Each variant is `copyStatus: "variant-draft"`, and a variant with new text goes back to `approval.status: "proposed"`. The render plan lists a `check-score.mjs --storyboard` command per variant and a [renderer](../motion-render/README.md) command per variant and format. Run the checks first: a longer translation can need a longer hold or a smaller size, which the checker and the renderer's overflow guard report.

Exit codes: 0 written; 2 bad input, an unknown format, an added copy ID, a repeated variant ID, or an output that already exists (nothing is overwritten).

## Order of work

1. Pick a template (or the user's own checked contract) and replace the placeholder copy with the client's exact text.
2. `brand` with the client's kit; fix any contrast note.
3. Check, preview at phone size and get the storyboard approved.
4. `expand` the approved contract into languages and formats; check each variant, get new text approved, then render.
