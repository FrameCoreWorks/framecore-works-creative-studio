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
| `focus-outline-removed` | P0 | `outline: none` or `0` with no `:focus-visible` (or `:focus`) rule anywhere |
| `dead-link` | P0 | links with `href="#"`, an empty `href` or `javascript:` |
| `low-contrast` | P0 | a rule setting both a hex text colour and a hex background below 4.5:1 (3:1 at 24 px, or 18.5 px bold) |
| `glass-overuse` | P1 | `backdrop-filter` on three or more rules |
| `glow-overuse` | P1 | coloured box or text shadows with 10 px or more blur on three or more rules |
| `pill-everything` | P1 | pill radius (500 px and up) on four or more rules |
| `button-arrows` | P1 | an arrow (→ ↗) in three or more buttons or links |
| `generic-cta` | P1 | a button or link reading only Learn more, Get started, Discover, Explore, Try now, Dowiedz się więcej, Odkryj, Zacznij, Sprawdź |
| `buzzword` | P1 | AI-powered, next-generation, seamless, cutting-edge, game-changer, innowacyjny, rewolucyjny, przełomowy, nowej generacji |
| `fake-person` | P1 | John or Jane Doe, Jan Kowalski, Acme, example.com, 123 Main St and their example e-mails in visible text |
| `background-grid` | P1 | two or more gradients with a small `background-size`: a decorative grid or graph paper |
| `viewport-missing` | P1 | a full HTML page with no viewport meta |
| `full-height-section` | P1 | `height` or `min-height: 100vh` (use content height or `dvh`) |
| `fixed-width` | P1 | a width of 1000 px or more with no `max-width` in the rule |
| `headline-length` | P1 | an `h1` over 42 characters or 10 words, or an `h2` over 48 characters (it will not fit two lines at display size on a phone) |
| `index-numbering` | P1 | three or more decorative index numbers (01, 02, 03, Step 1, Krok 1) outside an ordered list |
| `eyebrow-cluster` | P1 | an eyebrow, kicker or section-label element directly above three or more headings (one editorial label is allowed) |
| `micro-label-cluster` | P1 | three or more rules setting tiny tracked capitals (13 px or less, 0.08em or more) |
| `cream-terracotta` | P1 | a hard-coded cream ground together with a hard-coded terracotta colour (brand tokens are not flagged) |
| `mono-prose` | P1 | a monospace font family outside `pre`, `code`, `kbd`, `samp`, tables and `[data-ui]` |
| `table-figures` | P1 | a table whose cells are mostly numbers with no `tabular-nums` and no right alignment |
| `motion-tells` | P1 | `transition: all`, scaling from 0, `animate-bounce`/`ping`/`pulse` or an infinite animation |

A video composition (HyperFrames data attributes or a seekable timeline) is a fixed canvas, so `viewport-missing`, `full-height-section`, `fixed-width` and the eight rules added from taste-skill are skipped there, and so is `accent-overuse`, since the accent rule is per shot and the markup holds every shot; caps at display size (48 px or 4vw and up) are exempt from the tracking rule. Colours defined as custom properties (`--accent: #6366f1`) are the brand's tokens and are never flagged; hard-coded uses are. A finding is a reason to look, not a verdict: when the brief or kit deliberately breaks a rule, pass `--allow ID` and note it in the review. Exit code 1 means at least one P0 finding remains.

It reads source, not pixels: a raster image, a PDF or a rendered video frame is reviewed by eye against the same rules. It checks contrast only where one rule sets both colours as hex; [`contrast_check.py`](contrast_check.py) computes any pair (`python3 contrast_check.py "#777777" "#ffffff"`, `--selftest` recomputes the WCAG reference pairs), and the worst spot of text over an image is checked by eye or with a scrim. Layout is checked only for the static tells above, not rendered.

Adapted from Open Design's `lint-artifact` (Apache-2.0, commit 78d5637), whose rules adapt [refero_skill](https://github.com/referodesign/refero_skill) (MIT), and from the UI, human and mobile rules and the contrast checker of [anti-slop](https://github.com/miqdadbadjuber/anti-slop) (MIT, commit 439a2ef). Verified on 2026-10-19 by `tests/craft_lint_test.py`: pages carrying the tells fire each rule, clean pages and Studio's own video compositions fire none, an allowed rule is suppressed, and the contrast reference pairs recompute exactly. Across every HTML file in the package the linter reports nothing.
