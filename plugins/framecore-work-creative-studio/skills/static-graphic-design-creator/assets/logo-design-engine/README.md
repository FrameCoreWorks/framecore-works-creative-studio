# Bundled Logo Design engine

Studio includes the complete reusable toolkit from [Logo Design Skill 1.4.4](https://github.com/kaankiziltug/logo-design-skill/tree/0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134): all nine Python tools, fourteen reference chapters, two templates, the searchable 1,432-record catalogue and all upstream fictional example images. The exact copied files and hashes are in [source provenance](../../../../integrations/logo-design-skill/source-manifest.json). No separate skill installation is needed. `SKILL.source.md` preserves upstream instructions as source material; the containing Studio owner governs routing, user approvals, requested medium and review scope.

## Start from the user's brief

Use this engine for requested SVG/vector logo production, inspection and delivery. It does not select a visual idea or convert a raster request into vector output. For visible-text raster generation, follow the active Studio and user rules. The brief, accepted geometry, exact copy, font rights and requested deliverables remain authoritative. Fictional examples demonstrate techniques; they are not ready-made directions or marks to reuse.

Resolve this directory from the installed skill, then run the adapter using its actual absolute path. Commands below assume this is the working directory; outputs belong in a project outside the installed plugin.

```sh
python3 studio_logo.py probe
python3 studio_logo.py init /absolute/project/logo
python3 studio_logo.py build /absolute/project/logo/presentation-spec.json --out /absolute/project/logo/review-01
python3 studio_logo.py build /absolute/project/logo/presentation-spec.json --out /absolute/project/logo/review-02 --raster required
```

`init` creates a blank presentation specification and guidelines template. Create the requested artwork in the project and fill the brand, brief, success criteria and concept fields from the agreed task. It does not create an invented brand or select a mark. Use absolute input/output paths when running from elsewhere. Existing output directories are refused; create a new revision rather than overwriting approved work.

`build` accepts local, self-contained SVG inputs. It rejects active content, CSS blocks, external assets and file references; this bounded restriction is not a general SVG sanitizer. Review unfamiliar files before invoking native tools. SVGs containing these features can be handled separately after inspection with the native tools, without weakening host security settings.

The build emits:

- Copied input SVGs and a portable presentation specification.
- `concepts.svg`, `preview.html` and `presentation.html` from the upstream tools.
- `audit.json`, marked advisory with visual approval `not_run`.
- Per-concept black, white, mono, square, favicon and app-icon SVG variants. A supplied `concept.avatar` is used for favicon/app-icon geometry, while the master variants retain the symbol.
- With `--raster required`, concept PNG, variant PNGs, favicon ICO, 16/32/48 px icons, Apple touch icon, 192/512 px icons, maskable icon, webmanifest and HTML inclusion snippet.
- `delivery.json` with input/output hashes, actual raster completeness, unresolved checks and the upstream source pin; `tool-log.txt` with native command output.

`--raster off` is the default and performs no render. `optional` preserves useful SVG/HTML even when rendering is unavailable and marks incomplete raster output. `required` fails if a requested raster artifact is missing, even when an upstream command returned success. All outputs remain candidates until actual visual review. Guidelines are a template requiring completion. The presentation tool uses sample context copy for mockups: replace or omit it if exact production copy is required; do not deliver fictional contact details as client facts.

## Host capabilities

| Capability | Requirement | Behavior when unavailable |
| --- | --- | --- |
| Read chapters/templates and catalogue | Readable plugin files | Deliver the brief, technique/geometry instructions and file plan |
| Search, audit, sheets, presentation, SVG export | Python 3.8+ standard library | Do not claim execution; provide the project inputs and native commands |
| PNG and ICO | An existing CairoSVG, rsvg-convert, Inkscape, Chromium-family browser, or macOS Quick Look renderer | The probe reports detection only; an actual render is the proof |
| HTML presentation screenshots and greyscale contact-sheet PNG | Existing Chromium-family browser | Keep editable HTML/SVG; report missing PNG. CairoSVG ignores the upstream sheet's `feColorMatrix`, so the adapter requires a browser for that filter |
| Reference mark gallery | Separately obtained original corpus and a browser | The bundled catalogue still works; no trademark SVG is silently downloaded |

Codex, ChatGPT Work and ordinary ChatGPT use the same package and rules. Inspect actual file, Python and rendering tools exposed in that session. A host name alone does not prove execution support. The adapter performs no package installation, provider generation, uploads or network requests. Quick Look may produce opaque output when its transparency recovery dependency is absent; inspect the actual alpha channel when transparency matters.

## All native tools

Scripts are byte-identical upstream files. Run `python3 scripts/NAME.py --help` for their complete argument sets. Native commands can overwrite their target; always use new project paths. The shared `svglib.py` supplies SVG geometry/colour helpers and is imported by the other eight tools.

| Tool | Purpose | Example, with project paths |
| --- | --- | --- |
| `search_library.py` | Filter marks by type, industry, technique, geometry, colour and subject | Prefer `studio_logo.py search --technique negative-space --limit 6` for honest local-file availability |
| `svg_audit.py` | Heuristic SVG structure, geometry, colour and small-size checks | `python3 scripts/svg_audit.py /project/logo.svg --json` |
| `concept_sheet.py` | Equal-scale symbol/lockup contact sheet | `python3 scripts/concept_sheet.py /project/a.svg /project/b.svg --names A B -o /project/new/concepts.png` |
| `preview_sheet.py` | Size, background, context and comparison sheet | `python3 scripts/preview_sheet.py /project/logo.svg -o /project/new/preview.html` |
| `presentation_board.py` | Editable HTML concept or selected-identity presentation and optional slide PNGs | `python3 scripts/presentation_board.py /project/spec.json -o /project/new/board.html` |
| `render_png.py` | SVG/HTML rendering, transparent PNG where supported, ICO | `python3 scripts/render_png.py /project/logo.svg -o /project/new/logo.png --size 512` |
| `export_variants.py` | SVG, PNG and web-icon delivery variants | `python3 scripts/export_variants.py /project/logo.svg --out-dir /project/new/icons --web-icons` |
| `build_catalog.py` | Rebuild catalogue/statistics/gallery for a local corpus | Use a writable project copy of the engine; put authorized references at `assets/library/svg/`. Never rebuild the installed snapshot |
| `svglib.py` | Shared SVG parser, geometry, bounds, colour and embedding functions | Imported by the tools; not a standalone CLI |

The upstream SVG audit's exit 0 can include `FAIL` findings. Its numerical score is advisory and does not certify originality, geometric fidelity, font rights, render quality, security or production readiness. It approximates curves and does not fully resolve `<use>`, CSS, clipping or stroke bounds. Export recolouring may collapse painted white cutouts; inspect every requested variant.

## Reference library without redistributed trademarks

The catalogue, classifications, statistics and gallery code are bundled. The 1,432 actual company/product SVG marks are explicitly excluded from upstream MIT terms by [TRADEMARKS.md](TRADEMARKS.md). Studio does not republish them or download them automatically. `search` returns pinned source URLs and `local_svg: null` until a corpus is provided. It supports the upstream filters and `--summary`/`--list-values`.

When the user supplies a separately obtained original checkout for legitimate reference study:

```sh
python3 studio_logo.py verify-corpus /absolute/original-logo-design-skill
python3 studio_logo.py search --reference-library /absolute/original-logo-design-skill --type letterform --limit 6
python3 studio_logo.py catalog-check /absolute/original-logo-design-skill
python3 studio_logo.py gallery --reference-library /absolute/original-logo-design-skill --out /absolute/project/private-reference-gallery
```

The verifier matches every SVG against the reviewed commit's hashes in `reference-corpus.json`. It does not grant trademark rights. The gallery reads the original local files through file URLs and copies no mark into Studio or the project. Keep it private and do not ship it with client artwork. The catalogue is technology-heavy and is not a clearance database. Study construction, do not trace or imitate existing marks.

## Knowledge and examples

The [chapter index](references/library-guide.md) documents library filters. Load the relevant chapter for [discovery](references/discovery-brief.md), [principles](references/principles.md), [process](references/process.md), [mark types](references/mark-types.md), [visual techniques](references/visual-techniques.md), [SVG construction](references/svg-construction.md), [typography](references/typography.md), [colour](references/color.md), [identity systems](references/identity-system.md), [redesign](references/redesign.md), [critique](references/critique.md), [testing](references/testing-checklist.md) or [presentation/delivery](references/presentation-delivery.md). All fourteen are available without fetching the original.

Both [guidelines template](templates/brand-guidelines-template.md) and [presentation schema example](templates/presentation-spec.example.json) are preserved. The example's brand, counts and ideas are illustrative data. Use the blank `init` specification for a real brief. [Example images](examples.html) includes every upstream fictional demonstration image and its thumbnail. Their inclusion demonstrates available source material, not an evaluation of visual quality or permission to replace a user's concept with one.

The original is the `logo-design` entry in FrameCore Works Toolbox's catalog, not a Studio extension; these built-in resources need no separate installation.
