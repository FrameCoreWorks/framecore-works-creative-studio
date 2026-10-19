# Craft lint

[`craft_lint.py`](craft_lint.py) flags machine-made design tells in HTML, CSS and SVG: the checkable part of the [craft rules](../../references/craft-rules.md). Python standard library only, so it runs wherever code runs.

```sh
python3 craft_lint.py page.html
python3 craft_lint.py deck.html styles.css icon.svg --json
python3 craft_lint.py page.html --allow ai-default-indigo     # the brand kit really is indigo
```

| Rule | Level | Fires on |
| --- | --- | --- |
| `ai-default-indigo` | P0 | a hard-coded Tailwind indigo or violet (`#6366f1`, `#4f46e5`, `#4338ca`, `#3730a3`, `#8b5cf6`, `#7c3aed`, `#a855f7`) |
| `purple-gradient` | P0 | a gradient with a purple or indigo stop |
| `trust-gradient` | P0 | a blue-to-cyan gradient |
| `emoji-icon` | P0 | ✨ 🚀 🎯 ⚡ 🔥 💡 and similar inside headings, buttons, list items or `*icon*` elements (emoji in running text are not flagged) |
| `sans-display` | P0 | an `h1`–`h3` or display class hard-coded to Inter, Roboto, Arial, Helvetica or `system-ui` while the page defines a display face (`--font-display` or `@font-face`) |
| `left-accent-card` | P0 | a rule with a 2 px or wider solid left border and a border radius |
| `invented-metric` | P0 | "10× faster", "99.9% uptime", "zero downtime", "3× more productive" and Polish forms such as "10× szybciej" in visible text |
| `filler-copy` | P0 | lorem ipsum, "feature one", "placeholder text", "sample content", "tekst zastępczy", "przykładowa treść" |
| `all-caps-no-tracking` | P1 | `text-transform: uppercase` without letter-spacing of 0.06em (px and rem are converted with the rule's font size; without one, 1 px is accepted) |
| `raw-hex` | P1 | more than 12 hex colours outside the `:root` token block |
| `accent-overuse` | P1 | `var(--accent)` six or more times in the markup (the rule is about two visible uses per screen; the count is an approximation) |
| `placeholder-image` | P1 | placehold.co, picsum.photos, placekitten.com, source.unsplash.com and similar |

Colours defined as custom properties (`--accent: #6366f1`) are the brand's tokens and are never flagged; hard-coded uses are. A finding is a reason to look, not a verdict: when the brief or kit deliberately breaks a rule, pass `--allow ID` and note it in the review. Exit code 1 means at least one P0 finding remains.

It reads source, not pixels: a raster image, a PDF or a rendered video frame is reviewed by eye against the same rules. It does not check contrast (the brand guide tool and Studio's frame review do) or layout.

Adapted from Open Design's `lint-artifact` (Apache-2.0, commit 78d5637), whose rules adapt [refero_skill](https://github.com/referodesign/refero_skill) (MIT). Verified on 2026-10-19 by `tests/craft_lint_test.py`: a page carrying every tell fires each rule once, a clean page with tokens fires none, and an allowed rule is suppressed.
