# Creative Studio 1.131.0

A new companion plugin, Brand Kit, takes a company website apart into a brand kit and a brand audit.

## What changed

The separate `brand-kit` plugin (install it from this repository's marketplace next to Studio) reads a website you name: a few pages, their stylesheets and styles, with robots.txt honoured. It records colours with their use, font families, logo files, headings, CTAs and a copy sample in `evidence.json`, drafts `brand-kit.json` in Studio's brand kit format with a source ledger, and writes `brand-audit.md` with the visual system and a voice and messaging profile. Values it could not verify, such as font and logo rights, stay `Unknown`. Approved kits are saved as numbered revisions per brand. A menu then hands the next step (new website ideas, ads and Meta Ads, video, brand development, content, a spoken brand voice) to Studio's skills. Studio's extension registry lists it.

## What did not change

Studio's skills, startup, routing, names, paths and the brand kit schema are unchanged.

## Verification limits

The plugin's 46 launcher tests and 6 package tests and Studio's checks passed. One real extraction (pypi.org) ran in a Claude Code cloud container. The skill's audit and direction steps in a host conversation, and fresh ChatGPT, Work, Claude and Codex clients, were not run for this release.
