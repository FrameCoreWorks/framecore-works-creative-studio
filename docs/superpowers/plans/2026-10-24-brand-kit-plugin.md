# brand-kit Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (native, chosen for budget: one final review). Steps use checkbox (`- [ ]`) syntax.

**Goal:** A companion plugin `plugins/brand-kit/` that turns a website into evidence, a draft Studio brand kit, an audit with a voice profile, revisions in a local catalog and a direction menu routed to Studio owners.

**Architecture:** Standard-library Python modules behind one launcher `scripts/brandkit.py`; one skill `brand-kit:brand` does interpretation and routing. Kit schema is Studio's `pipeline-core/assets/brand-kit.template.json`.

**Tech Stack:** Python 3.10+ stdlib (`urllib`, `html.parser`, `re`, `json`, `hashlib`, `ipaddress`, `socket`, `urllib.robotparser`), `unittest`.

**Spec:** `docs/superpowers/specs/2026-10-24-brand-kit-plugin-design.md`

## Global Constraints

- Plugin `brand-kit` 1.0.0, display name "Brand Kit", skill `brand-kit:brand`, Apache-2.0.
- Limits: `--pages` default 3, max 8; max 12 stylesheets; 15 s timeout; 3 MB per response; http/https only; private/loopback/link-local refused; robots.txt honoured.
- Catalog root: `--root`, else `BRAND_KIT_ROOT`, else `~/.framecore-studio/brand-kits`; files `<slug>/rev-NNNN.json`, `<slug>/index.json`; never overwrite a revision.
- Kit top-level keys exactly the template's: `schema_version, name, spelling, colours, fonts, logo, voice, claims, legal_lines, do_not`.
- Script never writes tone, claims, licences; unknowns are the string `Unknown`.
- Do not touch Studio's shared package except one `extensions.json` entry (Task 5).

## Review Focus

- Site with no stylesheets or only inline styles: draft still produced, missing roles `Unknown` (test in Task 2/3).
- 3-digit and 8-digit hex, `rgb()` with alpha, uppercase: normalised to lowercase `#rrggbb` (Task 2).
- Brand slug with spaces or `../`: slug sanitised, path stays under root (Task 4).
- Fetch failure or robots disallow on a subpage: recorded in `pages[].status`, run continues (Task 1).
- `diff` of nested dict/list fields: reports dotted paths (Task 4).

---

### Task 1: Safe fetching and page collection (`scripts/site.py`)

**Interfaces — Produces:** `check_url(url:str, resolve=socket.getaddrinfo) -> None` (raises `UnsafeURL`); `fetch(url, opener=None) -> (status:int, content_type:str, text:str)`; `collect(url, pages=3, fetch=fetch, robots=None) -> dict` with keys `pages` (list of `{url,status,html}`), `stylesheets` (list of `{url,status,css}`).

- [ ] Tests `tests/site_test.py`: `ftp://` and `http://127.0.0.1/` and `http://10.0.0.1` raise `UnsafeURL`; `collect` with a stub fetch over fixture `tests/fixtures/home.html` follows nav links only on the same host, caps at `pages`, records a `robots-disallowed` page without fetching it, records an `error` page and continues, gathers `<link rel=stylesheet>` up to 12.
- [ ] Implement; nav links from `<nav>`/`<header>` anchors first, then any same-host anchors.
- [ ] Run `python3 plugins/brand-kit/tests/site_test.py` → OK. Commit.

### Task 2: Evidence parsing (`scripts/style.py`)

**Interfaces — Produces:** `normalise_colour(s) -> str|None`; `parse_css(css, source) -> dict` (`colours`: list of `{hex, use, property, selector, source}`, `variables`: `{name: value}`, `fonts`: list of `{family, selector, source}`, `font_faces`: list); `parse_html(html, url) -> dict` (`meta`, `headings`, `nav`, `ctas`, `copy_sample` ≤ 2000 chars, `logos`, `font_links`, `social`, inline style CSS); `build_evidence(collected) -> dict` aggregating counts: `colours` list of `{hex,count,uses,sources}` sorted by count, `fonts` list of `{family,count,roles}` (roles from selectors: `body`, `heading`, `button`), plus page items, and `method: "static-html-css"`.

- [ ] Tests `tests/style_test.py`: `#ABC`→`#aabbcc`, `#11223344`→`#112233`, `rgb(29, 59, 42)`→`#1d3b2a`, `rgba(0,0,0,.5)`→`#000000`, `hsl(0,100%,50%)`→`#ff0000`; fixture `tests/fixtures/site.css` yields `--brand-green` variable, heading family `Fraunces`, body `Inter`; `parse_html` on fixture finds the header logo img, og:image, the "Zamów online" CTA, nav labels, Google Fonts link, instagram link; empty CSS gives empty lists.
- [ ] Implement with regex over declarations and `html.parser.HTMLParser`. `var(--x)` resolved through variables once.
- [ ] Run tests → OK. Commit.

### Task 3: Draft kit and ledger (`scripts/draft.py`)

**Interfaces — Produces:** `draft(evidence) -> (kit:dict, ledger:list[{field,value,status,evidence}])`; `is_saturated(hex)->bool`, `luminance(hex)->float`.

- [ ] Tests `tests/draft_test.py`: fixture evidence gives `colours.background.hex` light, `colours.text.hex` dark, `primary` = most used saturated with button/link use first; `fonts.headline.font == "Fraunces"`, `licence == "Unknown"`; `logo.files` holds URLs and ledger status `observed` with note `url-not-downloaded`; `voice.tone == []` and ledger `unknown`; kit keys equal template keys (read from `plugins/framecore-work-creative-studio/skills/pipeline-core/assets/brand-kit.template.json`); evidence with no colours → each colour role `{"hex":"Unknown","role":...}`.
- [ ] Implement. Name from `og:site_name`, else title before a separator.
- [ ] Run tests → OK. Commit.

### Task 4: Catalog (`scripts/catalog.py`) and launcher (`scripts/brandkit.py`)

**Interfaces — Produces:** `slugify(s)->str`; `save(kit, brand, root, note='') -> int` (revision number); `list_brands(root)->list`; `show(brand, root, rev=None)->dict`; `diff(a:dict,b:dict)->list[str]` lines `path: old -> new`; `validate(kit)` raises `ValueError` naming missing keys. Launcher subcommands `extract`, `draft`, `save`, `list`, `show`, `diff` with `--json` output where useful.

- [ ] Tests `tests/catalog_test.py`: two brands saved under one root stay in separate folders and `show` returns each unchanged; second save → rev 2, rev 1 bytes unchanged; slug of `"../Kawiarnia Lipa"` is `kawiarnia-lipa`; diff of nested change reports `colours.primary.hex: #111111 -> #222222`; export (rev file) → save under another root → `show` equal (roundtrip); missing key raises. `tests/cli_test.py`: `brandkit.py extract --html fixture --out` then `draft` then `save` via subprocess writes files.
- [ ] Implement. Run tests → OK. Commit.

### Task 5: Skill, references, manifests, packaging, Studio registry

**Files:** `skills/brand/SKILL.md`, `skills/brand/agents/openai.yaml`, `skills/brand/references/audit-template.md`, `skills/brand/references/directions.md`, `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `README.md`, `CHANGELOG.md`, `LICENSE`, `NOTICE`, `tests/package_test.py`; modify `.claude-plugin/marketplace.json`, `scripts/check_all.sh`, Studio `extensions.json` (entry `brand-kit`, like `voice-narration`).

- [ ] `package_test.py`: manifests agree on name/version 1.0.0, display name, marketplace entry; exactly one `SKILL.md`; skill text contains `extract`, `draft`, `save`, `Unknown`, `brand-audit.md`, `references/directions.md`, `references/audit-template.md`, and each Studio owner id named in directions exists in `plugins/framecore-work-creative-studio/skills/`; description ≤ 1024.
- [ ] Write files; skill ≤ 7,000 bytes.
- [ ] Run Studio validator, `bash scripts/check_all.sh --fast`. Commit.

### Task 6: Verify, review, record

- [ ] Offline end-to-end on fixtures; real-site run if network allows (record result or `NOT_RUN`).
- [ ] One final review (superpowers:requesting-code-review); fix findings.
- [ ] Ledger/CHANGELOG entry; Studio release only on coordinator's signal (registry entry changes the shared package).
