# DESIGN.md: the brand kit for design agents

[`design_md.py`](design_md.py) converts a Studio [brand kit](../../references/brand-kit.md) to and from `DESIGN.md` with `tokens.css`: the brand contract that [Open Design](https://github.com/nexu-io/open-design) and other agent design tools read before rendering (Markdown prose an agent follows, plus semantic CSS custom properties such as `--bg`, `--fg`, `--accent`, `--font-display`). Python standard library only.

```sh
python3 design_md.py export brand-kit.json --out-dir design/
python3 design_md.py import design/DESIGN.md --tokens design/tokens.css --out brand-kit.json
```

**Export** writes `DESIGN.md` (eight numbered sections: theme and atmosphere, colour roles, typography, logo, voice, claims and legal lines, the brand's don'ts, an agent prompt guide), `tokens.css` and a `manifest.json` in Open Design's `od-design-system-project/v1` shape, so the folder can be added there as a design system. Colours map by role: `background` to `--bg`, `text` to `--fg`, `accent`, `primary`, `surface`, `muted`, `border` to their tokens, anything else to `--color-<name>`; fonts to `--font-display` and `--font-body` with a generic fallback. Only the kit's own values are written: a missing value reads "Not stated in the brand kit", and template placeholders are left out.

**Import** reads colours and fonts from `tokens.css` (or `#hex` colour lines in `DESIGN.md`) and the don'ts from a section named Don'ts or Anti-patterns. Everything else stays a `{placeholder}`: a `DESIGN.md` is prose, and Studio does not guess a form of address, claims, legal lines or font licences from it. [`brand_guide.py`](../../../delivery-documentation/scripts/brand_guide.py) lists the unfilled fields and lays out a guide only as a marked draft until the user fills them.

Neither direction overwrites an existing file. A `DESIGN.md` describing someone else's brand (Open Design ships many for real companies) is a reference for structure, not a kit to work in: Studio does not produce work in another company's identity.

Verified on 2026-10-19 by `tests/design_md_test.py`: a filled kit exports and imports back with the same colours, roles and don'ts; an Open Design-style package imports its tokens; existing files are refused; the imported kit runs through `brand_guide.py --draft`.
