---
name: brand
description: Take a company website apart into a brand kit and a brand audit, then plan the next move. Use when the user pastes their site and wants its colours, fonts, logo, imagery, tone of voice and messaging reverse-engineered, a brand kit or brand book drafted, kits for several brands kept apart with revisions, or ideas for a new website, ads, Meta Ads, video or brand development built on the current brand. Writes Studio's brand kit schema; execution goes to Studio's owners.
---

# Brand Kit

Turn a website into evidence, a draft brand kit in Studio's schema, a written brand audit with a voice profile, and a
numbered menu of directions. The kit format is Studio's `pipeline-core/assets/brand-kit.template.json`; this skill
never invents its own fields. Studio's owners do the creative work for the chosen direction.

`<brandkit>` below is this plugin's `scripts/brandkit.py`, two folders above this file (`../../scripts/brandkit.py`).
Resolve it from where the host installed this skill; never copy a path from another machine.

## 1. Evidence

Ask only for what is missing: the URL, and the goal if the user gave none (the menu in step 5 can wait). Work in the
project folder.

```
python3 <brandkit> extract <url> --pages 3 --out evidence.json
python3 <brandkit> draft evidence.json --out brand-kit.draft.json --ledger brand-kit.sources.json
```

`extract` reads the home page and up to `--pages` same-site pages from the navigation (max 8), their stylesheets and
inline styles, honours robots.txt and refuses private addresses. Report its summary line plainly: a page that is
`robots-disallowed` or `error` was not read. For a page the user saved, or a site that blocks the script, use
`--html page.html --css site.css --base-url <url>`.

No shell in this host: read the page with the host's fetch or browser tool, follow the same rules below and say
which fields could not be measured. Never present a value you did not see.

When a browser tool is available (Playwright, Claude in Chrome, the host's own browser), also take a desktop and a
mobile screenshot of the home page and look at them: logo placement, imagery style, density, photography versus
illustration, motion. A screenshot shows the look; it is not an exact colour value.

## 2. Read the evidence honestly

- A CSS colour is a declared value, not a pixel sample; roles in the draft (`primary`, `accent`, `text`,
  `background`) are inferred from use and count, so check them against the screenshot.
- A declared font family is not a verified rendered face. Font licences stay `Unknown` until the user names them.
- A logo URL is not a downloaded or licensed asset. Clear space, minimum size and a white version stay `Unknown`.
- Website copy is observed wording. It never becomes an approved claim in `claims.approved` by itself.
- Another company's site used as a reference gives technique, never its logo, photos or copy.

## 3. Brand audit and voice

Write `brand-audit.md` in the project folder from `references/audit-template.md`. The voice profile is the core:
form of address, tone in three adjectives with a quoted line for each, phrases the brand uses, what it avoids,
promises it repeats and how its CTAs speak. Build it only from quoted copy in `evidence.json` (headings, CTAs, copy
sample) and the screenshots; when the sample is thin, say so and ask for a few more texts (offer page, emails,
posts). Name contradictions (two palettes, mixed address forms) and gaps (no mark, no white logo, weak CTA) as
findings, not as faults of the user.

## 4. Draft, approve, save

Fill the voice fields of `brand-kit.draft.json` from the audit, keep every unverified value `Unknown`, and show the
user a compact view: name, four colours with roles, two fonts, logo files, voice, the list of `Unknown` fields and
the source ledger. Supplied approved values (an existing kit or brand book) win over the website; show a difference
as a proposed change.

Save only after the user agrees. Then:

```
python3 <brandkit> save brand-kit.json --brand "<Brand name>" --note "from <url>, <date>"
```

Each save is a new numbered revision in the brand's own folder of the catalog (`BRAND_KIT_ROOT`, default
`~/.framecore-studio/brand-kits`); earlier revisions are never overwritten. `list`, `show <brand> [--rev N]` and
`diff <brand> A B` show the catalog; work for a client always names which brand and revision it uses, and two brands
never share a file. When the kit changes, list the outputs made with the earlier revision that need a check. Also
write `brand-kit.json` into the project folder when the user wants Studio's owners to read it from there; in a
cloud session say that the catalog lives on a temporary disk and offer the file for download.

## 5. Choose a direction

Offer the numbered menu in `references/directions.md` in the user's language: new website ideas, ads and Meta Ads,
video ads and reels, brand development, content and social, a spoken brand voice. Recommend one in a sentence based
on the audit's strongest gap. Hand the chosen direction to the Studio owner the reference names, with the kit path,
revision and the audit. If Studio is not installed, give the plan as prose and say that Studio carries the execution.

## Reporting

Keep apart: evidence collected (pages read, method), what was inferred, what the user approved, what was saved
(brand, revision, path). Nothing was published or uploaded; a draft kit is not a finished brand guide.
