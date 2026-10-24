# Logo Design Skill: bundled engine and optional native extension

Source: [kaankiziltug/logo-design-skill](https://github.com/kaankiziltug/logo-design-skill/tree/0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134), upstream version 1.4.4, commit `0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134`, reviewed 2026-10-17 after the owner supplied the repository. Studio 1.88.0 integrates the complete reusable [engine](../../skills/static-graphic-design-creator/assets/logo-design-engine/README.md) within [Graphic Design](../../skills/static-graphic-design-creator/SKILL.md#logo-concept-and-craft-pass), following the owner’s explicit request for all resources. It adds no new skill owner or installed dependency. The original remains an optional `logo-design` [extension](../../skills/workflow-orchestrator/references/extensions.md).

## Decision map

| Source method or component | Decision | Destination or reason |
| --- | --- | --- |
| Recognition/equity audit before redesign | Adapt | Separate recognized features, observed defects and permitted changes before choosing refresh versus rebuild |
| Brand word mapping, one identifying idea, different mark constructions | Adapt | The static owner's concept pass starts from concrete brief facts and compares distinct mechanisms; no fixed 8–12 or three-concept quota |
| Black-first shape inspection, equal-scale alternatives, recommendation before a kit | Adapt | Compare actual requested concepts and reuse the existing selection checkpoint; do not reopen an approved decision or force a full kit |
| Letter reading, junctions, true negative space, optical balance and reversed weight | Adapt | Explicit craft checks in the static owner; corrections follow observed defects, not compulsory percentages |
| Small-size, silhouette, context and resemblance comparisons | Adapt | Actual target sizes; 16/32 px for requested icons, not a universal logo minimum; no clearance claim |
| All nine Python tools, fourteen chapters, two templates, catalogue metadata and fictional example images | Bundle | Byte-identical source with a Studio adapter for project setup, search, SVG/HTML build, rendering, icon export, corpus verification and a local reference gallery; no separate installation |
| SVG production as a universal default, five-question intake, mandatory two review loops, fixed mockup counts | Reject as Studio defaults | Preserve requested medium, existing single-question intake, direct-production authorization and bounded review |
| Automatic production approval from a numerical SVG score or exit code | Reject | The audit uses heuristics and can exit 0 with FAIL findings; it omits some SVG semantics. Visual and production checks remain separate |
| Third-party trademark SVG corpus | Exclude from redistribution | Upstream expressly excludes 1,432 marks from MIT; preserve the full searchable index and hashes, and read a separately supplied pinned corpus without copying it |
| Fictional example brands and renders | Bundle as reference | All source example images are available in an index; they demonstrate a method and must not become ready-made Studio ideas |

## Rights and limitations

The [MIT licence](LICENSE) covers upstream code and documentation, Copyright (c) 2026 kaankiziltug. The upstream [TRADEMARKS.md](https://github.com/kaankiziltug/logo-design-skill/blob/0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134/TRADEMARKS.md) explicitly excludes the 1,432 reference SVG marks from that licence. Studio bundles 120 byte-identical source files: all reusable tools, chapters, templates, catalogue assets, fictional example images, source workflow and rights notices. It copies no trademark SVG marks. Source-file inventory and hashes are in [source-manifest.json](source-manifest.json). When installing or redistributing the original, retain both root notices. Upstream's skill-only ZIP and folder copy omit them, so the registry calls out that packaging gap.

The library skews toward technology. Its examples and an audit score do not establish originality or measured performance of a model. The standard-library Python scripts can inspect structure without new dependencies; PNG rendering still requires an available renderer. The SVG geometry audit approximates curves and does not fully resolve `<use>`, CSS, clipping or stroke bounds. The exporter can overwrite output files and its recolouring is not a general SVG transformation; preserve originals and inspect exported variants. Run only reviewed local inputs through browser/render tools, following the host's normal file and network boundaries.

## Observed verification

2026-10-17, macOS scratch checkout: upstream `python3 tools/smoke_test.py` passed all its checks, including catalog consistency, SVG audit, search, sheets, SVG/PNG/icon export and ZIP packaging. This is a tool smoke test, not a visual evaluation of the 28 example brands.

Skills CLI 1.7.2 `add https://github.com/kaankiziltug/logo-design-skill/tree/0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134/skills/logo-design --list` found `logo-design` without installation. Claude Code `plugin validate . --strict` passed the local marketplace manifest. Installed-plugin/skill listings were readable and did not contain this extension. Actual native install/remove, new-session invocation and manual uploads in Claude apps, ChatGPT and ChatGPT Work were **not_run**. Host status in the registry describes the supported route, not a completed installation.

## Bundled-engine verification

The Studio adapter was exercised with original synthetic test geometry, preserving source artwork and using new output directories. The Node suite checks every copied hash, catalogue filtering without misleading local SVG paths, blank project setup, the full SVG/HTML pipeline, overwrite refusal, active-content rejection, corpus mismatch and actual PNG/favicon artifacts. The optional raster case uses an existing renderer and is explicitly enabled in the recorded local run; default source CI skips it. A separate scratch run verifies every original corpus SVG against the reviewed pin, checks classification coverage and opens the local-gallery route. No original extension or new dependency was installed.

The adapter does not render raster on `--raster off`; `required` rejects missing raster files even if the upstream tool exits 0. Its delivery manifest hashes inputs and outputs, leaves visual approval unperformed and labels the guidelines as a template requiring completion. This tool evidence does not establish active-chat routing, a model’s design quality or trademark clearance.
