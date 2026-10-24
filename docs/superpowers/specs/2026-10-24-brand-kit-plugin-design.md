# brand-kit: a website-to-brand-kit companion plugin beside Studio

Date: 2026-10-24. Status: defaults chosen under the owner's standing rule (small design decisions by sensible default, ask only on direction); awaits the owner's review.

## Intent

The owner (2026-10-24, project thread "Zbuduj brand kit z analizą strony"): grow the proposed brand kit manager into a strong "brand kit + voice" asset. The user pastes their company website; the plugin takes it apart (styles, colours, typography, logo, voice and messaging) into a brand kit, then plans in whichever direction the user picks: new website ideas, ads, Meta ads, brand development.

What already exists in Studio 1.130.0 and stays the single source:

- the kit schema `pipeline-core/assets/brand-kit.template.json` and its guide `pipeline-core/references/brand-kit.md`, including "Draft from a website" (evidence ledger, Unknown values, approval before saving);
- website evidence rules in `pipeline-core/references/account-free-creative-production.md`;
- `ecommerce-campaign-strategy-director/references/website-to-campaign.md`, `workflow-orchestrator/references/brand-identity-workflow.md`, `marketing`, the DESIGN.md exporter.

What is missing: a tool that actually collects the evidence (today the model must read raw HTML/CSS by hand, which is slow and error-prone), a written brand audit with the voice profile, a way back into Studio's owners for the chosen direction, and the manager part of the proposal (per-brand revisions, isolation, diff).

Success: in Claude Code or Codex a user gives a URL and gets, in one pass, `evidence.json` (what was measured, from which page and how), a draft `brand-kit.json` in Studio's existing schema, `brand-audit.md` (identity, palette, type, logo, imagery, voice and messaging, gaps, each with its source or `Unknown`) and a numbered menu of directions that routes to Studio skills. The approved kit is saved as a revision in a local catalog; a second brand never mixes with the first; an old revision stays readable and diffable.

## Decision: separate plugin, not a Studio extension

A separate plugin `plugins/brand-kit/` modelled on `plugins/voice-narration/`. Reasons: Studio is in maintenance mode with permanent package paths; the companion proposal already places the manager outside Studio and requires "no divergent schema", so the plugin reads and writes Studio's template schema and never defines its own. Studio gains only one registry entry in `extensions.json` (the owner's extension rule), as for voice-narration.

## Structure

| Path | Content |
| --- | --- |
| `skills/brand/SKILL.md` | The only skill, `brand-kit:brand` (display "Brand Kit"), with `agents/openai.yaml`. Order: evidence, interpretation, draft, approval, save, direction. |
| `skills/brand/references/audit-template.md` | The `brand-audit.md` outline and the voice profile questions. |
| `skills/brand/references/directions.md` | The direction menu and which Studio owner takes each, with what the kit hands over. |
| `scripts/brandkit.py` | Launcher: `extract`, `draft`, `save`, `list`, `show`, `diff`. Standard library only, Python 3.10+. |
| `scripts/site.py`, `scripts/style.py`, `scripts/draft.py`, `scripts/catalog.py` | Fetch, CSS/HTML parsing, kit drafting, catalog. Each small and testable alone. |
| `tests/` | Offline fixtures (an HTML page and a stylesheet), unit tests, package test; wired into `scripts/check_all.sh`. |
| manifests, `README.md`, `CHANGELOG.md`, `LICENSE` (Apache-2.0), `NOTICE` | As voice-narration. Version 1.0.0. |

## Launcher

- `extract URL [--pages N] [--out evidence.json]` (also `--html FILE` for offline input): fetches the page and up to `N` (default 3, max 8) same-site pages linked from navigation, plus up to 12 linked stylesheets and inline `<style>`. Limits: 15 s timeout, 3 MB per response, http/https only, private and loopback addresses refused, robots.txt honoured, honest user agent. Records per item: value, count, where it came from (URL, selector or property) and `method: "static-html-css"`.
  Collected: colours (hex, rgb(a), hsl normalised to hex, with use: text, background, border, other; CSS custom properties by name), font families with their usage (body, headings, buttons), `@font-face` sources and font services (Google Fonts, Adobe Fonts links), logo candidates (img/svg in header or with "logo" in class/id/alt/src, inline SVG, `og:image`, icons, `apple-touch-icon`), page metadata (title, description, language, OpenGraph), headings h1–h3, navigation labels, button and CTA texts, a bounded copy sample, social profile links. Blocked or failed pages are recorded as such.
- `draft evidence.json [--out brand-kit.draft.json] [--ledger sources.json]`: maps evidence onto the existing template. Roles by rule: background = most used light background colour, text = most used dark text colour, primary and accent = the two most used saturated colours (buttons and links first); headline font = family used by headings, body = family on body/html. Logo files hold URLs, not downloads. Voice fields, claims, legal lines and licences stay placeholders or `Unknown` for the model and the user; the script never writes tone. The ledger lists each kit value with its evidence item and status `observed`, `inferred` or `unknown`.
- `save KIT --brand SLUG [--root DIR] [--note TEXT]`: validates the kit against the template's top-level fields and writes `<root>/<slug>/rev-NNNN.json` plus `index.json` (revision, date, note, SHA-256). Root default `~/.framecore-studio/brand-kits`, or `BRAND_KIT_ROOT`. Never overwrites a revision. `list`, `show SLUG [--rev N]` and `diff SLUG A B` (changed fields by path) complete the manager. Export is the revision file itself; import is `save` of a supplied file.

## The skill

1. Ask for the URL and the goal only if missing. Run `extract`, then `draft`. No shell: read the page with the host's fetch or browser, follow the same evidence rules and say which fields could not be measured.
2. If a browser tool is present (Playwright, Claude in Chrome), take a desktop and a mobile screenshot of the home page and note the visible logo, imagery style and layout; screenshots are evidence of look, not of exact colour values.
3. Interpret: write `brand-audit.md` from `references/audit-template.md`. The voice profile (address form, tone in three adjectives, use/avoid phrases, recurring promises, CTA style) is built from the copy sample and quoted examples. Website claims are observed wording, never approved claims.
4. Show the compact draft, the audit and the Unknowns; the user corrects. Save as a revision only after the user agrees, and also write `brand-kit.json` into the project folder when they want.
5. Directions: offer the numbered menu from `references/directions.md` (new website ideas, ads and Meta ads, video ads and reels, brand development and positioning, content and social, spoken brand voice) and hand the chosen one to the Studio owner it names, with the kit path. If Studio is not installed, give the plan in prose and say that Studio carries the execution.

Rules carried from Studio: a declared font is not a verified rendered face, a CSS colour is not a pixel sample, a logo URL is not a licensed asset; font and logo rights stay `Unknown`; no client data in the plugin; another brand's site used as a reference gives technique, never its assets.

## Out of scope for 1.0.0

Rendered-page colour sampling and full-page crawls, competitor analysis (Studio's `marketing` and the marketing plugin cover it), uploading or publishing anything, a hosted ChatGPT package (ChatGPT has no shell; the skill's no-shell route covers it later).

## Testing

Offline only: fixture HTML and CSS give known colours, fonts, logos, CTAs; tests check parsing, normalisation, role mapping, Unknown handling, URL safety refusals, robots handling with a stubbed fetcher, catalog isolation of two brands, revision immutability, diff output and an export/import roundtrip. Package test checks manifests agree, one skill, the references exist and the skill text keeps its rules. A real-site run is recorded separately as `NOT_RUN` or with its evidence.
