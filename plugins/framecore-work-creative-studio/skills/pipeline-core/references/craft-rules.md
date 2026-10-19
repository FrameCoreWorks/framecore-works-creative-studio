# Craft rules: type, colour, hierarchy, motion and interface

Brand-agnostic rules a competent designer applies on top of any brand kit: the kit decides *which* colours and fonts, these rules decide *how* they behave. Adapted in English from the `craft/` references of [Open Design](https://github.com/nexu-io/open-design/tree/78d5637cb49da07e81314d1544b5fc6d37c95084/craft) (Apache-2.0), which adapt [refero_skill](https://github.com/referodesign/refero_skill) (MIT, © Refero) and cite their primary sources; Studio's own rules win where they differ. The checkable part runs as [`craft_lint.py`](../assets/craft-lint/README.md) on HTML, CSS and SVG.

Numbers are defaults for screen work. Print, video frames and posters seen at a distance scale them (see [Where the numbers change](#where-the-numbers-change)); a brand kit or an explicit brief may override any default, and the override is recorded, not silently applied.

## Contents

- [Machine-made tells](#machine-made-tells)
- [Typography](#typography)
- [Hierarchy](#hierarchy)
- [Editorial hierarchy](#editorial-hierarchy)
- [Colour](#colour)
- [Motion in interfaces](#motion-in-interfaces)
- [Interface states](#interface-states)
- [Accessibility floor](#accessibility-floor)
- [Laws of UX worth naming](#laws-of-ux-worth-naming)
- [Forms](#forms)
- [Right-to-left and mixed scripts](#right-to-left-and-mixed-scripts)
- [Where the numbers change](#where-the-numbers-change)
- [How Studio applies this](#how-studio-applies-this)

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
- ★ Placeholder image services (`unsplash.com` hot links, `placehold.co`, `picsum.photos`, `placekitten.com`).
- The fixed sequence hero → features → pricing → FAQ → CTA with no variation; decorative blobs and waves; perfectly symmetric layouts with no tension.

**Soul:** about 80 % proven patterns and 20 % distinctive choice: one bold visual move (a typeface, a single colour decision, an unexpected proportion), voice in the microcopy ("Start tracking" beats "Get started"), one memorable micro-interaction, one detail only someone who used the product would put there. If someone outside the project can tell from a screenshot whose work it is, it has soul; otherwise it is a template.

## Typography

**Scale.** A multiplicative scale (1.2 or 1.25), at most 6–8 sizes per artifact. Screen defaults: display 48–72 px, H1 32–48, H2 24–32, H3 20–24, body 15–18, small 13–14, caption 11–12.

**Leading.** Display and H1 1.0–1.2; body 1.5–1.6; small 1.5. CJK glyphs fill the em box, so CJK display needs 1.3–1.4 and body 1.7–1.8 at every size, including the biggest cover title; set Latin values only on Latin elements in mixed layouts. Polish and other Latin scripts with tall diacritics (Ś, Ż, Ć) at tight display leading: check that accents do not touch the line above.

**Letter-spacing** (the most skipped rule):

| Context | Tracking |
| --- | --- |
| Body 14–18 px | 0 |
| Small 11–13 px | +0.01 to +0.02em |
| Labels and button text | +0.02em |
| **ALL CAPS** | **+0.06 to +0.1em, always** |
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
- **Contrast gates:** body text 4.5:1; large text (18 pt ≈ 24 px, or 14 pt bold ≈ 18.5 px) 3:1; UI components against neighbours 3:1. When a brand colour fails on text, use a darker shade for text and keep the bright one for fills.
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
- Never remove focus outlines without a visible replacement (`:focus-visible`); a focus ring is at least 2 px with 3:1 contrast for AAA.
- Real labels, not placeholders; native elements first (`<button>`, `<a href>`); `<html lang>`; landmarks; alt text (empty for decorative images); no positive `tabindex`. Adding ARIA does not add accessibility: pages with ARIA average more errors.

## Laws of UX worth naming

Use them to decide composition, and cite them correctly:

- **Grouping:** proximity, similarity, common region, uniform connectedness; the item that differs is remembered (Von Restorff), so reserve the strongest contrast for one goal-relevant action.
- **Decisions:** Hick (time grows with options), choice overload (Iyengar & Lepper), anchoring (Tversky & Kahneman, 1974), Pareto, Tesler (complexity is conserved; the system should absorb it).
- **Memory:** chunking (Miller), serial position (first and last are remembered), peak-end (people judge by the peak and the end), Zeigarnik (unfinished tasks pull).
- **Motor and flow:** Fitts (size and distance) plus the platform target floor; goal-gradient (effort rises near the goal); Jakob (users expect your product to work like the others they know).

## Forms

Validate on the first blur after an edit, then live once a field is invalid so the error clears as soon as it is fixed; never on the first keystroke or with red borders at page load (`:user-invalid`, not `:invalid`). On submit, move focus to an error summary. Specific messages ("Date must be DD.MM.YYYY; you entered 5-3-26"), never "Invalid input". Never wipe a field because another one failed. No "retype your email" fields; allow paste. Consequential submissions (legal, financial, data) are reversible, checked or confirmed.

## Right-to-left and mixed scripts

`dir` with `lang` together; logical CSS properties (`inline-start`, `margin-inline-end`) instead of left and right; isolate mixed runs with `<bdi>` or `dir`, and force `dir="ltr"` on emails, URLs, phone numbers and IBANs. No letter-spacing or italics on Arabic or Hebrew; no lorem ipsum for RTL prototypes. Mirror directional icons, not clocks, media controls or chart x-axes.

## Where the numbers change

- **Print and posters:** sizes in points and by viewing distance (a poster headline seen at 3 m is far above 72 px equivalents); keep the ratios (scale steps, caps tracking, measure, accent share). Print preparation follows [print-ready PDF](../../delivery-documentation/references/print-ready-pdf.md).
- **Video frames and social graphics:** text is read in seconds at phone size; follow [motion craft](../../hyperframes-workflow/references/motion-craft.md) and the channel's safe zones. Caps tracking, accent discipline and hierarchy still hold.
- **Slides:** one primary per slide, three levels at most, accent twice; editorial rules for text-heavy decks.

## How Studio applies this

1. Owners producing styled output (Static Graphic Design Creator, presentations, landing or app mockups, HTML motion) read the sections their artifact needs: typography, hierarchy and colour almost always; editorial for long reads; motion, states, accessibility and forms for interactive work; right-to-left only when such text appears.
2. Where code runs and the artifact is HTML, CSS or SVG, run [`craft_lint.py`](../assets/craft-lint/README.md) inside the [automatic output review](loop-protocol.md#automatic-output-review) and fix P0 findings before delivery; report P1 findings that remain, with the reason.
3. A raster image cannot be linted: look for the same tells in the pixels during review.
4. Nothing here overrides an explicit brand kit, a user's stated choice or exact-copy locks; record the deviation instead.
