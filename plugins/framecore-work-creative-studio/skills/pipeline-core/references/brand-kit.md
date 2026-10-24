# Brand kit

One small file per client or brand that every Studio owner reads before making anything for it: colours, fonts and their licences, logo files, tone, words to use and avoid, banned claims and required legal lines. Start from [brand-kit.template.json](../assets/brand-kit.template.json); keep the filled file with the client's project, never in the plugin.

## What it holds

| Field | Use |
| --- | --- |
| `name`, `spelling` | The exact brand name and how it is written (capitals, declension notes such as "w Kawiarni Lipa") |
| `colours` | Named colours with HEX values and their role (`primary`, `accent`, `text`, `background`); the static compositor accepts `brand:primary` wherever a colour goes |
| `fonts` | Roles (`headline`, `body`) with a bundled font name or the client's font file and its licence; the compositor accepts `brand:headline` as a font |
| `logo` | Files and where each is used (colour on light, white on dark, a square mark), minimum size, clear space |
| `voice` | Form of address (Ty or Państwo), tone in three adjectives, words and phrases to use and to avoid |
| `claims` | Approved claims with their source; banned claims |
| `legal_lines` | Required lines: the Omnibus line for reductions, disclaimers, consent text, AI-assistance line |
| `do_not` | What the brand never does (stock smiles, red for prices, all caps) |

## How owners use it

- Static and motion: colours, fonts and logo come from the kit; the compositor resolves `brand:` names with `--brand kit.json`.
- Copy: the voice, spelling, approved and banned claims; the checker's form-of-address finding is resolved by the kit's choice.
- Campaigns and video: the same locks across every asset; a change to the kit is a change for all later assets, not a silent edit of one.

## DESIGN.md for design agents

To take a kit into Open Design or another agent design tool, or to start a kit from a `DESIGN.md` someone supplies, use [`design_md.py`](../assets/design-md/README.md): export writes `DESIGN.md`, `tokens.css` and a manifest from the kit's own values; import fills colours, fonts and don'ts and leaves everything else as placeholders for the user. The shared [craft rules](craft-rules.md) apply on top of any kit.

## Keeping it between conversations

Studio does not store client data. In ChatGPT keep the kit in a Project (as a file or in its instructions); in Claude, in a Project or in a project folder's CLAUDE.md; in Codex or Claude Code, as `brand-kit.json` in the project folder, which AGENTS.md or CLAUDE.md can point to. When no kit exists, ask for the logo, colours and the form of address once and offer to save them as a kit.

## Draft from a website

Use the supplied public URL and a permitted available read/capture route. Bound pages and viewports. Reuse [website evidence](account-free-creative-production.md#website-brand-and-content-evidence); collect accessible DOM/CSS/font declarations, logo sources and actual screenshots only where the host can inspect them.

Keep a dated source ledger beside the project kit: source URL, inspected page/viewport, method, observation, proposal and unresolved status. A declared font stack is not a verified rendered face; CSS colour is different from a pixel sample; a logo URL is not a downloaded asset. Mark font/logo rights, clear space, minimum size and unsupported identity claims Unknown. Website copy is observed wording, not automatically an approved or substantiated advertising claim.

Draft the existing schema in [brand-kit.template.json](../assets/brand-kit.template.json); do not invent required schema fields or put client data in the plugin. Keep the one-line identity and evidence ledger in project notes. Preserve supplied approved locks when the website differs and show the contradiction as a proposed change. Screenshot-only or blocked-page access yields partial observations and Unknown values, never invented DOM, licence or fetch evidence.

Show the compact draft and its sources. Once the user approves saving it (including existing explicit approval), write the real kit to the authorized project location and check it with the existing DESIGN.md/brand-guide route. Missing assets remain missing; a readable draft kit does not prove a completed brand guide.
