# Brand Kit

A plugin beside FrameCore Works Creative Studio that takes a company website apart into a brand kit and a brand audit, then plans the next move.

- **What it reads:** the home page and a few pages from its navigation, their stylesheets and inline styles: colours with their use, font families, logo files and icons, page metadata, headings, navigation, CTAs and a copy sample. robots.txt is honoured, pages are bounded and private addresses are refused. With a browser tool the skill also looks at desktop and mobile screenshots.
- **What you get:** `evidence.json` (what was measured and where), a draft `brand-kit.json` in Studio's brand kit format with a source ledger, and `brand-audit.md` with the visual system, a voice and messaging profile, gaps and the fields still `Unknown`.
- **Manager:** approved kits are saved as numbered, never-overwritten revisions, one folder per brand (`~/.framecore-studio/brand-kits` or `BRAND_KIT_ROOT`), with `list`, `show` and `diff`.
- **Next:** a menu of directions (new website ideas, ads and Meta Ads, video, brand development, content, spoken brand voice) handed to Studio's skills.
- **Rules:** CSS values are not pixel samples, declared fonts are not verified faces, a logo URL is not a licence, website copy is not an approved claim. Nothing is published or uploaded.

The skill is `brand-kit:brand`; the launcher is `scripts/brandkit.py` (`extract`, `draft`, `save`, `list`, `show`, `diff`), Python 3.10+ standard library only. Install it from this repository's marketplace next to Studio.
