# Board delivery and handoffs

This reference connects sequence plans, static board layouts, image/video
prompt preparation, review, and delivery without implying that an asset moved
between tools. It synthesizes selected storyboard and reference-transfer
units from Custom GPTs 01, 02 and 07 plus the pinned Workflow Kit storyboard
contracts/examples. It is a portable workflow contract, not an API schema or
provider authorization.

Related contracts: [sequence contract](../../storyboard-sequence-architect/references/sequence-contract-and-continuity.md),
[reference authority and carriers](../../storyboard-sequence-architect/references/reference-authority-and-carriers.md),
[board layout and copy](board-layout-and-copy.md).

## 1. Name the state of the deliverable

Use state words precisely. A board workflow may be at any of these states:

1. **Content established:** temporal beats/cards, comparison views, or reference
   properties are selected or explicitly provisional. A sequence is required
   only for a temporal story board.
2. **Board specified:** layout, selected panels, copy and authority are
   documented.
3. **Prompt prepared:** a complete prompt/brief exists for a chosen route.
4. **Generation requested:** user explicitly requested it, and any necessary
   tool conditions are being checked.
5. **Generated:** a tool actually returned an image.
6. **Inspected:** the returned image was viewed against named criteria.
7. **Accepted/revised:** the user or agreed reviewer made an explicit choice.

Never leap from one state to another in wording. A board prompt is not a
board. A generated image is not automatically legible, coherent, editable,
accurate, or approved. A technical check is not a creative-quality pass.

## 2. Sequence-to-board handoff

For temporal story boards, the sequence architect supplies only what the board
needs. Coverage/reference boards can enter directly from their supplied sources
and purpose; they do not need events, timings, a sequence version, or a trip
through the sequence owner. For those boards, substitute panel/source/property
mapping for shot-order fields and omit irrelevant temporal fields.

A temporal sequence-to-board handoff includes:

- sequence/project identifier and source revision;
- stable shot IDs and accepted order;
- selected panels and the inclusion/omission rule;
- concise visual moment for each chosen panel;
- time range/duration only when source and precision are known;
- exact visible strings and approval/line-break status;
- per-property source authority and suppression rules;
- strict/approximate continuity requirements;
- unresolved conflicts and provisional choices.

The board architect may reorder page placement for readability, but must keep
shot IDs tied to the sequence and disclose any page order different from
story order. It may recommend different aspect/proportion from the source
frame, but cannot silently alter the movie's shot timing, camera move, story
event, or text. For a board containing fewer moments than the sequence, say
what is sampled (e.g. hero beats, scene openings, coverage comparison).

Do not require a board before video prompt compilation. The approved shot card
may go directly to the video prompt route. Conversely, a board is useful for
visual comparison but does not automatically supply the action details or
inputs for per-shot prompt compilation.

## 3. Board-to-image prompt handoff

When an image prompt skill receives a board brief, provide a compact, complete
artifact contract: board purpose; resolved format or unknown; panel IDs/order;
each approved moment or selected reference/coverage property; hierarchy and
spacing; exact copy; actual input assets
and property roles; safe-zone/legibility requirements; exclusions; and
acceptance criteria. Keep source-provenance or QA discussion out of the
generator prompt unless a concise instruction is needed to prevent an error.

The prompt compiler owns dynamic model/surface research and current syntax.
Do not hard-code a default generator, output resolution, number of references,
negative prompt field, layout token, or typography guarantee here. Respect the
actual user's named destination and hand back unresolved current capability
claims instead of inventing them. User asks for board image generation only
when that intent is explicit; a request to “make a board prompt” is not
execution permission.

## 4. Board-to-video handoff

An approved board can inform shot selection and visual direction. For every
independent video request, video-prompt-architect still needs its own complete
action, start/end state, camera and sound intent, exact copy/dialogue, and
actual bound input carrier where strict continuity requires one. Provide the
board's shot IDs and source version so the prompt does not silently change
coverage.

Never equate:

- a panel label such as `S03` with the image asset `S03.png`;
- a whole contact sheet with one clean opening frame;
- a selected still with a bound image-to-video source;
- a sequence description with the source clip for extension;
- multiple prompt cards with shared context across independent jobs;
- a planning JSON object with a native provider request.

If the user wants a board frame to serve as a carrier, identify and supply the
actual selected still (not merely the board), confirm it is the correct
approved state, and verify the destination supports that input. If the required carrier is absent, keep a strict requirement strict and report
its readiness as pending; request the carrier or prepare a conditional binding
plan. Use approximate continuity only when already requested or when the user
authorizes that specific relaxation. A missing file alone never grants it. Read
[reference authority and carriers](../../storyboard-sequence-architect/references/reference-authority-and-carriers.md).

## 5. Review and correction loop

Review the artifact the user actually supplied, not a remembered version or
description. Keep separate issue categories:

- sequence/content: missing, invented, reordered, or causally impossible beat;
- board layout: unclear grid, misordered panel, crop, hierarchy, spacing;
- visible copy: exact-text mismatch, unapproved label, unreadable text;
- references: wrong authority, suppressed feature leaked, missing source;
- carrier/handoff: planned file is absent or wrong input was bound;
- production/technical: dimensions, safe area, delivery file, or format
  remains unverified.

For each issue, record the observed evidence and confidence, affected
shot/panel/property, accepted elements that must not change, smallest causal
fix, and observable acceptance test. Fix one main failure at a time unless
coupled dependencies require a named set. After two failed corrections for
the same issue, change the method (e.g. shorter label, alternate layout,
separate copy deck, real carrier, split coverage) rather than accumulating
generic negative instructions.

The reviewer must not state “I checked the image” if only its prompt was
available. A text fixture, hand-authored board, thumbnail, or partial
screenshot has narrower evidence than the full-resolution asset. Record what
was and was not inspected.

## 6. Production delivery and limitations

A useful board delivery note may include:

- artifact status and version;
- intended use and format assumptions;
- sequence source/version and covered shot IDs;
- exact copy deck and unresolved approval status;
- property-level asset roles and files that must be attached downstream;
- safe-area, readability, crop or DTP questions;
- accepted changes, outstanding issues, and test criteria.

Do not call a raster image an editable board, layered source, approved animatic,
print-ready master, or generated production package unless that state is
actually verified. If a DTP handoff is requested, list known dimensions,
safe margins, bleed/profile requirements only when supplied/verified, and
open questions for the operator. Do not invent those values.

Keep the handoff local unless the user explicitly requests upload. Do not
claim file creation, upload, image generation, or install when no tool result
supports it. Do not include private absolute file paths or credentials in a
portable resume summary.

## 7. Compact output forms

### Sequence-to-board spec

```text
BOARD PURPOSE:
SOURCE SEQUENCE / VERSION (temporal only) OR REFERENCE/COVERAGE SOURCES:
LAYOUT BASIS (or unresolved):
PANEL ORDER / COMPARISON GROUPING:
- Panel ID if useful — approved moment or selected property/view — exact label if required
- Panel ID if useful — approved moment or selected property/view — exact label if required
COPY LOCKS / BREAKS:
REFERENCE ROLES / SUPPRESSED FEATURES:
OMISSIONS / PROVISIONAL ITEMS:
ACCEPTANCE TEST:
```

### Independent prompt readiness

```text
REQUEST ID / SHOT ID:
ACTION AND END STATE:
EXACT COPY / DIALOGUE:
CONTINUITY REQUIREMENT PER PROPERTY:
ACTUAL CARRIER / PLANNED CARRIER AND READINESS:
SURFACE SUPPORT VERIFIED / UNKNOWN:
RELAXATION AUTHORIZED BY USER (if any; absence is not authorization):
OBSERVABLE ACCEPTANCE TEST:
```

These forms are optional planning aids, not mandatory output formats and not
provider-native schemas. Use prose or a compact table when that serves the
user better.
