# Type and format workbench

Owner: commercial-visual-campaign-director. Added 2026-09-28. Applied, original
Studio methods for translating an accepted concept and exact copy into usable
hierarchy and requested adaptations. Read when line breaking, information
pairing, small-format reading or a changed ratio requires a concrete decision.
The existing [typography](typography.md) and [adaptation](format-adaptation.md)
references supply the fundamentals; this file adds worked operations, not a
new style catalog or a promise that raster typography is deterministic.

## Contents

- [Copy relationships](#1-turn-copy-into-a-reading-contract)
- [Typographic choices](#2-select-a-typographic-behavior-through-a-useful-comparison)
- [Exact breaks](#3-construct-breaks-without-rewriting)
- [Adaptation and feasibility](#4-adapt-the-relationship-before-the-decoration)
- [Three inspections](#5-three-different-inspections)
- [Reading repairs](#6-choose-the-next-design-response-to-a-reading-failure)
- [Web accessibility scope](#7-bounded-digital-accessibility-check)
- [Source trace](#source-rule-and-example-trace)

## 1. Turn copy into a reading contract

Read the exact strings first, then decide their relationships. A copy item can
be secondary in attention and still compulsory. Mark whether an amount belongs
to a specific product, whether a condition limits the headline, and whether a
name can be broken without changing its recognition. Never separate item and
price just to obtain a balanced column.

For a difficult text-bearing design, create a small internal map:

| Item | Exact source string | Reading role | Must remain paired with | Break permission |
|---|---|---|---|---|
| Title | User-final or selected wording | Entry | Its concept mechanism | Locked breaks or allowed reflow |
| Support | User-final or selected wording | Meaning/qualification | The claim it qualifies | As authorized |
| Practical facts | Each date/place/price preserved | Retrieval | Correct event/item/condition | As authorized |
| Mark | Actual brand asset or exact supplied wording | Recognition | Its approved use | Never redraw from this table |

This extends the existing copy lock; it does not create new text approval.
If exact text is unreadable in a source, keep that item unresolved. If the user
asks only for copy, return to Copy Voice rather than building this design map.
For a complete directed brief, the map can remain internal.

## 2. Select a typographic behavior through a useful comparison

Start from what the text must do. Compare one meaningful variable at a time
in planning, without automatically generating variants:

| Reading problem | Useful design decision | Check that prevents a superficial solution |
|---|---|---|
| Short cultural title needs character | Let spacing, scale or a repeated structural gesture embody the selected concept | The complete word still has its intended reading; facts remain separate |
| Long functional headline runs out of width | Reconsider territory and authorized breaks before extreme compression | Name/qualifier remains together; letters retain distinguishable forms |
| Several dates/prices need retrieval | Align by semantic group and keep item-value association explicit | A row cannot be read against a neighboring price |
| Two languages need distinct but equal access | Give each its own approved block and consistent role | No translation is shortened or hidden to fit the primary language |
| Thin display forms disappear at use size | Increase suitable weight/scale or change the territory if authorized | A zoomed screenshot is not the only evidence of legibility |
| A face or bright material defeats the headline | Adjust the permitted image/type relationship | Making all text equally larger does not destroy the second read |

Do not specify a different font for every line. A named family is a direction
unless its actual font file, coverage and rights are verified for the output.
A required editable type master belongs to the existing production handoff.

## 3. Construct breaks without rewriting

Keep the original string separately from its displayed line arrangement.
Evaluate candidate breaks for name integrity, amount/condition pairing,
syntax, reading rhythm and collision with adjacent artwork. A line break is
not permission to add a hyphen, replace a dash, lowercase a title, abbreviate a
venue or drop a conjunction. If the user locks a break that will not fit, show
the specific geometry conflict and ask about that break only.

For a line containing a date and time, the notation itself is part of the
copy. A decorative divider that looks similar to the approved separator is
still a changed character. For Polish text, inspect actual accents and the
shape distinction between letters; do not accept approximate word silhouettes.

## 4. Adapt the relationship before the decoration

Describe the invariant in one sentence. Example: a half-turn is made visible
by two opposed semicircular paper planes, while the title remains upright and
intact. The shapes may move around the type; the word must not become mirrored
just because rotation is the motif.

For each requested format, choose among the following operations in order of
what the accepted brief allows, not as an automatic series of edits:

1. **Safe crop:** works only if the actual content bounds, protected relations
   and required information fit the new window.
2. **Uniform scale or clean padding:** possible only when authorized and useful
   at the final viewing size. Padding does not authorize invented scenery.
3. **Recomposition:** change grouping, territories or scale relationships while
   retaining the selected mechanism and all copy.
4. **Content or method decision:** if mandatory content cannot be read within
   the fixed constraints, propose the smallest user-approved change or a
   typesetting/multipage handoff. Do not hide words or create a QR escape hatch.

### A concrete feasibility counterexample

In a fictional 1600-by-1000 raster, suppose the entire required content and
mechanism occupy a centered region 820 pixels wide and 760 pixels high. A
centered 1000-by-1000 crop can contain that region without scaling it. That is
not proof of final readability, but it disproves a blanket claim that every
horizontal-to-square conversion needs a redesign. If required content instead
spans 1400 pixels at locked scale and only cropping is allowed, no 1000-pixel
crop contains its full horizontal extent. Ask about the actual incompatible
constraint. Without bounds or a source, the result is Unknown.

Those are synthetic dimensions illustrating geometry, not platform templates,
official safe areas or instructions to introduce canvas coordinates into a
creative prompt. Use coordinates only when explicitly requested or required by
the chosen deterministic production task.

## 5. Three different inspections

| Inspection | What it answers | What it cannot certify |
|---|---|---|
| Reduced/thumbnail view | Which element wins first attention and whether the mechanism survives | Exact small text or final technical compliance |
| Intended use size | Whether the necessary reading and item pairing work in context | Hidden glyph detail beyond the supplied resolution |
| Detail/source comparison | Whether each required glyph, logo edge and protected property matches | Audience response, conversion or untested other formats |

For prompt-only work these are prospective tests. For actual art, perform only
what the available file and viewing information permit. A text transcription
can help compare strings, but a matching transcript alone does not prove the
letters are visually readable or correctly paired.

## 6. Choose the next design response to a reading failure

Use this tree to choose the design layer. Repair logging, version selection and
retry limits remain with the existing output critic and delivery owners.

- **Wrong supplied wording in the brief:** resolve copy authority before layout.
- **Right wording, wrong glyph in a real raster:** a supported scoped edit may
  fit; protect all other strings and compare the actual result.
- **Right glyphs, wrong first read:** change the allowed hierarchy or competing
  image relationship, not the offer's facts.
- **Right hierarchy, excessive content density:** test grouping and available
  territory; if fixed constraints still fail, change the agreed deliverable.
- **Correct single format, broken adaptation:** recover the defining relation
  and copy pairing in the new layout; palette matching alone is insufficient.
- **Reference unavailable:** keep source-specific correctness unverified;
  continue only the independent design judgments the available evidence allows.

A new format can be complete as a standalone prompt without a rendered master
if the approved direction and copy are sufficiently specified. Pixel-matching
an existing design is a different requirement and needs the actual source.

## 7. Bounded digital accessibility check

For web content within WCAG's scope, SC 1.4.3 uses 4.5:1 for ordinary text and
3:1 for qualifying large text, with defined exceptions. Evaluate the relevant
foreground/background and presentation; do not round a failing result upward
or infer compliance from palette names. A raster prompt cannot guarantee a
ratio. These web criteria do not establish print readiness or whole-artifact
accessibility. Source V5 below supplies the applicable details.

SC 1.4.5 generally favors real text where the technology can provide the desired
presentation, with exceptions for customizable or essential text images. For
a web destination, consider an equivalent text presentation or the appropriate
production handoff within agreed scope. This is not permission to replace a
requested integrated poster with HTML or an unrequested text overlay. Source
V6 below is about web accessibility, not a ban on graphic posters.

## Source, rule and example trace

All three pages were opened and read on 2026-09-28. Publication/update dates
were not established from the inspected passages and remain **Unknown**.
The following are narrow source summaries; the workbench and worked design are
original Studio synthesis, not reproduced institutional examples.

| ID / primary source | Bounded evidence | Application in this package |
|---|---|---|
| V4: [Getty, Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) | Describes visual weight, focal emphasis and the viewer's path as distinct design relationships. | Inspect first read and continuing scan separately in the half-turn adaptations; no universal grid follows. |
| V5: [W3C WAI, Understanding SC 1.4.3 Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) | Explains applicable text-contrast thresholds, their scope and measurement caveats. | Apply the bounded check above when relevant; the examples make no measured contrast claim. |
| V6: [W3C WAI, Understanding SC 1.4.5 Images of Text](https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html) | Explains adjustable text and exceptions for images of text. | Distinguish a raster poster from its web presentation and authorized production needs. |

Reusable tools: [copy/format card](../assets/copy-and-format-card.md) and
[two complete original adaptations](../assets/half-turn-adaptation-example.md).
No typography engine, font availability, brand rights, platform safe area or
raster-text success rate was verified by this research.
