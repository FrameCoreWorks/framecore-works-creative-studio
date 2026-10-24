# Craft rules: type, colour, hierarchy, motion and interface

Brand-agnostic rules a competent designer applies on top of any brand kit: the kit decides *which* colours and fonts, these rules decide *how* they behave. Adapted in English from the `craft/` references of [Open Design](https://github.com/nexu-io/open-design/tree/78d5637cb49da07e81314d1544b5fc6d37c95084/craft) (Apache-2.0), which adapt [refero_skill](https://github.com/referodesign/refero_skill) (MIT, © Refero) and cite their primary sources, and from [anti-slop](https://github.com/miqdadbadjuber/anti-slop) by Miqdad Badjuber (MIT, commit `439a2ef`) for the purpose gate, the liveliness dials, interface patterns, honest placeholders and responsive layout; Studio's own rules win where they differ. Copy has its own catalogue: [AI writing patterns](../../copy-voice/references/ai-writing-patterns.md). The checkable part runs as [`craft_lint.py`](../assets/craft-lint/README.md) on HTML, CSS and SVG.

Numbers are defaults for screen work. Print, video frames and posters seen at a distance scale them (see [Where the numbers change](#where-the-numbers-change)); a brand kit or an explicit brief may override any default, and the override is recorded, not silently applied.

## Contents

- [Purpose before technique](#purpose-before-technique)
- [Machine-made tells](#machine-made-tells)
- [More interface patterns](#more-interface-patterns)
- [Liveliness: three dials](#liveliness-three-dials)
- [Honest content and verification](#honest-content-and-verification)
- [Typography](#typography)
- [Hierarchy](#hierarchy)
- [Editorial hierarchy](#editorial-hierarchy)
- [Colour](#colour)
- [Motion in interfaces](#motion-in-interfaces)
- [Interface states](#interface-states)
- [Accessibility floor](#accessibility-floor)
- [Laws of UX worth naming](#laws-of-ux-worth-naming)
- [Forms](#forms)
- [Responsive layout](#responsive-layout)
- [Right-to-left and mixed scripts](#right-to-left-and-mixed-scripts)
- [Where the numbers change](#where-the-numbers-change)
- [How Studio applies this](#how-studio-applies-this)

## Purpose before technique

These rules are a filter, not a style: they prescribe no colours, fonts or layouts, and they ban no technique. Gradients, glass, badges, card grids and glow are tools; what fails is **technique without purpose**. Before using one, answer "what does this serve?" in one line (a hierarchy, the identity, readability). If the only answer is "it looks modern" or "it looks safe", rework it. Write the one-line reason for every major decision (colour, layout, type, spacing, cards, illustration); a decision whose reason does not fit in one line is revisited.

A piece is done when three things hold: every technique passes this test, it has its own identity (swap the logo and name, and it should still feel like this brand, not like any brand), and it works. Five questions check the last part:

1. **Intentional:** can every visual and copy decision be explained?
2. **Complete:** does every interactive element work, or is it absent?
3. **Content-driven:** does every section exist because the content needs it, not because such pages usually have one?
4. **Resilient:** does it hold in every state, theme, breakpoint and with the keyboard alone?
5. **Evidenced:** is everything presented as fact real and verifiable, or not shown?

Brand direction (the kit, a `DESIGN.md`, references) supplies identity; this filter applies on top of it. When the direction itself asks for a named tell (an indigo gradient, emoji headings), name the element and the rule it meets and ask once whether to keep it; a bold palette or an unusual typeface is identity, not a tell.

## Machine-made tells

These read instantly as default generated output. `craft_lint.py` flags the starred ones; the rest need a look.

**Must fix (P0):**

1. ★ Default Tailwind indigo or violet as the accent (`#6366f1`, `#4f46e5`, `#4338ca`, `#3730a3`, `#8b5cf6`, `#7c3aed`, `#a855f7`) when the brand kit does not name it.
2. ★ A two-stop "trust" gradient: purple to blue, blue to cyan, indigo to pink. A flat surface with an intentional type choice beats it.
3. ★ Emoji as feature icons (✨ 🚀 🎯 ⚡ 🔥 💡 and the like inside headings, buttons, list items or icon slots). Use a monoline SVG at 1.6–1.8 px stroke in the text colour.
4. ★ A system sans (Inter, Roboto, Arial, `system-ui`) hard-coded on display headings when the kit names a display face.
5. ★ A rounded card with a coloured left border: the canonical generated dashboard tile. Drop the radius or the border.
6. ★ Invented metrics: "10× faster", "99.9% uptime", "3× more productive", "zero downtime", or their Polish forms. Use a sourced number or a labelled placeholder (Studio's claim rules apply).
7. ★ Filler copy: lorem ipsum, "feature one / two / three", "placeholder text", "sample content". An empty section is a composition problem, not a copy gap.

**Should fix (P1):**

- ★ ALL CAPS without letter-spacing of at least 0.06em.
- ★ More than about 12 raw hex values outside the token block: the tokens were not used.
- ★ The accent used more than twice on one screen.
- Text over a photo or gradient checked only at its best spot: check the worst spot, or add a scrim.
- ★ Placeholder image services (`unsplash.com` hot links, `placehold.co`, `picsum.photos`, `placekitten.com`).
- The fixed sequence hero → features → pricing → FAQ → CTA with no variation; decorative blobs and waves; perfectly symmetric layouts with no tension.

## More interface patterns

Each is allowed with a written purpose and fails as a default (`craft_lint.py` flags the starred ones):

- **Dose caps:** ★ glass (backdrop blur) on one or two elements, never navbar, cards, modals and sidebar together; ★ glow on one or two focal elements, never cards, buttons, badges, icons, background and borders together; shadows mark elevation, they do not float everything; ★ radius varies by role, not pills everywhere.
- **Decoration:** generic AI icons (sparkle, magic wand, robot, lightning, orb) and an icon set chosen for its recognisable library look instead of the content; ★ an arrow on every button; capsule badges ("AI Powered", "Beta", "New") with no real status behind them; a pill above the headline that repeats the headline; decorative status dots and endless pulses; ★ grid, dot or graph-paper backgrounds; stock or blob illustrations unrelated to the product (use real screenshots or none); a fake terminal window as the hero.
- **Layout templates:** hero plus three or six identical cards; "How it works" always in three numbered steps; a bento mosaic as the default section; a "Trusted by" logo bar under the hero; pricing always in three columns with a "Most popular" card; the four-column Product / Company / Resources / Legal footer; every section the same centred title, subtitle and card grid. Order sections by the product's story.
- **Copy in the interface:** ★ generic CTAs (Get started, Learn more, Discover, Dowiedz się więcej, Odkryj) and ★ buzzwords (AI-powered, next-generation, seamless, innowacyjny, nowej generacji); name the action and the specific benefit.
- **App screens:** the default shell (sidebar, top bar, four stat cards, a chart, a table) chosen before asking what the screen is for; build around the one decision the user makes there. Stat cards with invented numbers and "+12 % this week" deltas without a named period; activity feeds of invented people; charts without a question (put the question in the title: "Failed jobs per hour, last 24 h"); table columns taken from the component (Name, Status, Date, Actions) instead of the field that decides the next move; ★ filler people (John Doe, Jan Kowalski, johndoe@example.com) dressed as data.
- **Theme:** dark by default "because it looks tech". Choose by brand and audience; if both themes ship, both must work.
- **Identity:** never clone a popular product's look (Linear, Vercel, Stripe, Apple) unless the user asks; references inspire, they are not templates.

**Soul:** about 80 % proven patterns and 20 % distinctive choice: one bold visual move (a typeface, a single colour decision, an unexpected proportion), voice in the microcopy ("Start tracking" beats "Get started"), one memorable micro-interaction, one detail only someone who used the product would put there. If someone outside the project can tell from a screenshot whose work it is, it has soul; otherwise it is a template.

## Liveliness: three dials

Removing tells leaves a void, and a model fills a void with its most generic output. Liveliness is added on purpose. Set three dials from the brief or the brand direction and hold them from the first section to the last:

| Dial | 1, calm | 2, balanced | 3, bold | Answers |
| --- | --- | --- | --- | --- |
| **Energy** | public-service calm | product-marketing clarity | agency-portfolio confidence | how hard the design says hello |
| **Rhythm** | uniform, predictable | consistent with a few breaks | asymmetric, mixed compositions | how much sections differ |
| **Motion** | hover states only | reveals and transitions | pinned, choreographed, parallax | how much moves, and why |

Before making, write one line: *"Reading this as: <kind of piece> for <audience>, in a <visual language>, dials E2 / R3 / M1."* With clear direction, infer the dials; when it is ambiguous, ask one decisive question ("closer to calm editorial or experimental agency?"); with no direction and no chance to ask, mark the result a **draft without direction** and use E1 / R1 / M1 rather than a sterile default presented as final. A brand kit or `DESIGN.md` may carry its dials (`Dial: E2 / R3 / M1`).

Levers that turn dials into decisions: **one focal point per screen**; **contrast on purpose** (size, weight, colour); **whitespace as structure**; **one deliberate accent** (none is sterile, everywhere is noise); **one identity motif** (a gesture, pattern or typographic voice repeated so the piece belongs to the brand). For motion in a video, the same dial is set in the [motion workflow](../../hyperframes-workflow/references/motion-craft.md): a "cinematic" piece must actually move, a "static" one must not.

## Honest content and verification

- **Real or labelled.** Every claim, number, testimonial, name, nav item or visual is real, or an explicit placeholder: `[REAL DATA]`, `[LOGO]`, "Your name", "Coming soon", an initial avatar. Never a realistic fake (invented stats, testimonials, team members, ghost links). An empty section beats a fabricated one; no FAQ of template questions.
- **Ask before inventing assets:** logo, people's photos, statistics, testimonial identities and the page structure are confirmed or left as clear placeholders.
- **No dead controls:** ★ every link and button has a real destination or behaviour (a section that exists, a modal that opens and closes with Escape, a toggle, a real URL, a form with feedback), or it is removed or labelled "Coming soon".
- **Verify before delivering:** where the page can run, open it, check the console, and click through every interactive element in every shipped theme and at a phone width; report the evidence element by element ("Book → opens /book, no console errors"; "empty form → validation shown"). Without a way to run it, say so and verify by reading the code; never claim a click that did not happen. Build features in the source, never by patch scripts rewriting files.

## Typography

**Scale.** A multiplicative scale (1.2 or 1.25), at most 6–8 sizes per artifact. Screen defaults: display 48–72 px, H1 32–48, H2 24–32, H3 20–24, body 15–18, small 13–14, caption 11–12.

**Leading.** Display and H1 1.0–1.2; body 1.5–1.6; small 1.5. CJK glyphs fill the em box, so CJK display needs 1.3–1.4 and body 1.7–1.8 at every size, including the biggest cover title; set Latin values only on Latin elements in mixed layouts. Polish and other Latin scripts with tall diacritics (Ś, Ż, Ć) at tight display leading: check that accents do not touch the line above.

**Letter-spacing** (the most skipped rule):

| Context | Tracking |
| --- | --- |
| Body 14–18 px | 0 |
| Small 11–13 px | +0.01 to +0.02em |
| Labels and button text | +0.02em |
| **ALL CAPS at text and label sizes** | **+0.06 to +0.1em, always**; caps at display size in a condensed face (48 px or 4vw and up) may be set tight on purpose |
| Headings 32 px and up | −0.01 to −0.02em |
| Display 48 px and up | −0.02 to −0.03em |

Negative tracking is Latin-only: never on CJK, Arabic, Persian or Urdu (it breaks cursive joining). The 0.06em caps floor follows Bringhurst's 5–10 % of the em.

**Pairing and weights.** At most two typefaces (display and body, or one variable face). Always a fallback chain; never `system-ui` alone on a heading. Most good work uses three weights: read (400–450), emphasise (500–550), announce (590–600); 700+ is rarely needed. Weight should jump between levels, not step.

**Measure.** Body copy 50–75 characters per line (`max-width: 65ch`). Never justify body text on screen.

## Hierarchy

Every surface meets three conditions: **one dominant entry point**, **intentional contrast between levels**, and **recoverable reading order** (a reader can reconstruct the structure without rereading).

Five levers: scale, weight, spacing, tracking and alignment. The dominant element uses at least two in the same direction. Spacing alone can promote an element: an isolated line with generous space reads as display at any size.

- **Flat hierarchy:** levels too close (18/20/22 px), one weight everywhere, uniform gaps. Fix: steps of at least 1.25× or a compensating weight or spacing jump.
- **Noise hierarchy:** everything bold, large or accented. Fix: promote one element and demote the rest, including things that feel important.
- Three working levels (primary, secondary, tertiary). A fourth visible level above the fold is usually a composition problem.
- Semantic and visual roles may differ (an `h1` quieter than a lead paragraph) when reading order stays intact.
- Anti-patterns: the graduated weight ladder (400→500→600→700→800), uniform section spacing, the heading as the only lever, two co-primaries, size-only hierarchy.

## Editorial hierarchy

For long reads, magazines, guides and editorial landings, pacing is authored like a print spread.

| Element | Size | Weight | Tracking | Leading |
| --- | --- | --- | --- | --- |
| Display headline | 56–96 px | light or regular | −0.02 to −0.05em | 1.0–1.1 |
| Standfirst | 18–24 px | regular | 0 | 1.4–1.5 |
| Byline | 12–14 px | regular or medium | +0.02 to +0.04em | 1.5 |
| Body | 16–18 px | regular | 0 | 1.6–1.7, measure 60–70 ch |
| Pull quote | 28–40 px | regular or light, never bold | −0.01em | 1.2–1.3 |
| Caption | 12–13 px | regular | +0.01em | 1.5 |
| Section label | 11–12 px | medium | +0.06 to +0.1em if caps | 1.5 |

Display to standfirst is a jump of at least 1.5× or 24 px. Space carries hierarchy (at least two line-heights around the display). Bold at most twice per 400 words. One pull quote per article, two at most, with no box, border or tint, breaking the column. Alternate dense and spacious sections; uniform padding reads as a template. Rules and dingbats only where they express the publication's identity.

## Colour

| Layer | Share of pixels | Tokens |
| --- | --- | --- |
| Neutrals | 70–90 % | background, surface, text, muted, border |
| One accent | 5–10 % | accent only; never invent a second |
| Semantic | 0–5 % | success, warning, danger |
| Effect | under 1 % | gradients, glows: rarely justified |

- **Accent discipline:** at most two visible accent uses per screen (for example one eyebrow and one CTA). Links and focus rings count.
- **Contrast gates** (★ checked by `craft_lint.py` when a rule sets both colours; compute any other pair with [`contrast_check.py`](../assets/craft-lint/contrast_check.py), never by eye: #555555 on black is 2.82:1 and fails): body text 4.5:1; large text (18 pt ≈ 24 px, or 14 pt bold ≈ 18.5 px) 3:1; UI components against neighbours 3:1. When a brand colour fails on text, use a darker shade for text and keep the bright one for fills.
- **Dark themes:** no pure black or white: about `#0f0f0f` on dark and `#fafafa` on light, text `#f0f0f0` / `#111111`; on dark, hairline borders as `rgba(255,255,255,0.08)`.
- **Name tokens by purpose** (`--accent`, `--success`), never by hue (`--blue-500`).
- Gradients separate hierarchy (header from body, primary from secondary CTA); they do not decorate empty space. For video and art direction, the blue-purple machine palette is covered in [art-style and explainer direction](../../hyperframes-workflow/references/art-and-explainer-motion-direction.md#choosing-the-look).

## Motion in interfaces

This is motion inside a product or page; storytelling motion in a video follows [motion craft](../../hyperframes-workflow/references/motion-craft.md).

- **When it earns its place:** moving through space, time or state (navigation, a container expanding, progress, gesture follow-through). Not to teach a complex system (controlled studies find no gain over static), decorate, signal "premium" or fill silence.
- **Durations:** 50–100 ms instant feedback; 150 ms default state confirmation; 200–300 ms entering UI; 300–500 ms cross-screen; over 500 ms only for staged or platform transitions. Hover-like motion seen often stays at or under 200 ms; mobile runs 20–30 % shorter.
- **Curve or spring:** curves for opacity and colour; springs for position, scale and rotation. Material 3 standard easing is `cubic-bezier(0.2, 0, 0, 1)` (`0.4, 0, 0.2, 1` is the legacy M2 curve).
- **Reduced motion:** every translate, scale, rotate or parallax respects `prefers-reduced-motion`; keep opacity or colour crossfades as the substitute. Animation is never the only signal of a state change.
- **Flashing:** no more than three flashes in any second (WCAG 2.3.1). Rewards (confetti, bursts) fire once; loops cap at 3–5 cycles; motion over 5 seconds needs a pause control; no spinner runs past 60 s.
- Folklore to avoid repeating: "Doherty threshold = 400 ms" (the paper's lowest measured threshold is 300 ms); "skeletons feel 11 % faster" (measured on ribbed progress bars, not skeletons); "Heer & Robertson recommend 300–1000 ms" (they tested 1.25 and 2 s and recommend about one second per stage).

## Interface states

A mockup that shows only the filled-in state is the most common silent failure. Every surface that loads, transforms or accepts data designs five states:

| State | Must contain |
| --- | --- |
| Loading | skeleton or labelled spinner; a "taking longer than expected" note at 15 s |
| Empty | headline, plain explanation, primary action (first use, no results with the query echoed, or cleared) |
| Error | what happened, why if known, what to do; the user's input preserved; severity matched to scope (field, form, section, page, app) |
| Populated | the state usually drawn |
| Edge | 200-character titles, missing optional fields, 10 000 rows, right-to-left content: the layout does not break |

Loading by expected wait: none under 300 ms; subtle 0.3–2 s; skeleton or labelled 2–10 s; determinate bar with cancel 10–60 s; after 60 s stop and offer retry or cancel. Retries back off (immediately, then 2, 4, 8 s); after three, offer support with a copyable error ID.

## Accessibility floor

- Legal floors differ: EU accessibility law (EN 301 549 v3.2.1) and US public-sector rules point to **WCAG 2.1 AA**; WCAG 2.2 adds nine criteria. State the target for the market.
- Touch targets: **24×24 CSS px** is the AA floor (2.5.8); 44×44 is AAA, iOS suggests 44 pt, Material 48 dp.
- ★ Never remove focus outlines without a visible replacement (`:focus-visible`); a focus ring is at least 2 px with 3:1 contrast for AAA.
- Real labels, not placeholders; native elements first (`<button>`, `<a href>`); `<html lang>`; landmarks; alt text (empty for decorative images); no positive `tabindex`. Adding ARIA does not add accessibility: pages with ARIA average more errors.

## Laws of UX worth naming

Use them to decide composition, and cite them correctly:

- **Grouping:** proximity, similarity, common region, uniform connectedness; the item that differs is remembered (Von Restorff), so reserve the strongest contrast for one goal-relevant action.
- **Decisions:** Hick (time grows with options), choice overload (Iyengar & Lepper), anchoring (Tversky & Kahneman, 1974), Pareto, Tesler (complexity is conserved; the system should absorb it).
- **Memory:** chunking (Miller), serial position (first and last are remembered), peak-end (people judge by the peak and the end), Zeigarnik (unfinished tasks pull).
- **Motor and flow:** Fitts (size and distance) plus the platform target floor; goal-gradient (effort rises near the goal); Jakob (users expect your product to work like the others they know).

## Forms

Validate on the first blur after an edit, then live once a field is invalid so the error clears as soon as it is fixed; never on the first keystroke or with red borders at page load (`:user-invalid`, not `:invalid`). On submit, move focus to an error summary. Specific messages ("Date must be DD.MM.YYYY; you entered 5-3-26"), never "Invalid input". Never wipe a field because another one failed. No "retype your email" fields; allow paste. Consequential submissions (legal, financial, data) are reversible, checked or confirmed.

## Responsive layout

For pages and app mockups (a video canvas or a print page is fixed and skips this):

- **States where the content breaks,** not at device widths: usually three (one column, two columns, wide), so tablets and small laptops never get a stretched stack or a crammed grid. Design the narrow state; do not bolt it on as a trailing override.
- **Mobile scale:** a smaller type step or fluid `clamp()` type, section padding about half of desktop, smaller gaps; sections sized to content or `dvh`, ★ not `100vh` (which runs under mobile browser chrome).
- **Grids reflow:** `minmax()`, `auto-fit`, `min-width: 0` on children; no forced 12-column grid on a phone; ★ no fixed widths of 1000 px and more without `max-width`.
- **No horizontal scroll and no clipping:** tables reflow or scroll inside their container, code wraps, images `max-width: 100%`; `overflow: hidden` crops thumbnails, never content.
- **Touch:** targets of about 44×44 px with space between them (24 px is the legal floor, 44 the craft target); every hover-only interaction has a tap equivalent with visible feedback.
- **Navigation:** collapse the desktop row into a bottom bar for a few primary destinations or a labelled menu ("Menu", not a bare hamburger); a fixed bar reserves its height and the safe area so it never hides the last item; sticky headers stay compact.
- **People:** text resizes to 200 % without clipping; the on-screen keyboard never covers the focused field; ★ a viewport meta tag is present.

## Right-to-left and mixed scripts

`dir` with `lang` together; logical CSS properties (`inline-start`, `margin-inline-end`) instead of left and right; isolate mixed runs with `<bdi>` or `dir`, and force `dir="ltr"` on emails, URLs, phone numbers and IBANs. No letter-spacing or italics on Arabic or Hebrew; no lorem ipsum for RTL prototypes. Mirror directional icons, not clocks, media controls or chart x-axes.

## Where the numbers change

- **Print and posters:** sizes in points and by viewing distance (a poster headline seen at 3 m is far above 72 px equivalents); keep the ratios (scale steps, caps tracking, measure, accent share). Print preparation follows [print-ready PDF](../../delivery-documentation/references/print-ready-pdf.md).
- **Video frames and social graphics:** text is read in seconds at phone size; follow [motion craft](../../hyperframes-workflow/references/motion-craft.md) and the channel's safe zones. Caps tracking, accent discipline and hierarchy still hold.
- **Slides:** one primary per slide, three levels at most, accent twice; editorial rules for text-heavy decks.

## How Studio applies this

1. Owners producing styled output (Graphic Design, presentations, landing or app mockups, HTML motion) read the sections their artifact needs: typography, hierarchy and colour almost always; editorial for long reads; motion, states, accessibility and forms for interactive work; right-to-left only when such text appears.
2. Before making, write the one-line Design Read with the three dials; before delivering, the one-line reasons for the major decisions.
3. Where code runs and the artifact is HTML, CSS or SVG, run [`craft_lint.py`](../assets/craft-lint/README.md) inside the [automatic output review](loop-protocol.md#automatic-output-review) and fix P0 findings before delivery; report P1 findings that remain, with the reason.
4. A raster image cannot be linted: look for the same tells in the pixels during review.
5. Nothing here overrides an explicit brand kit, a user's stated choice or exact-copy locks; record the deviation instead.
