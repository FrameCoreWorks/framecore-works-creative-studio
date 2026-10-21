# Data-led motion and revision-bound feedback

Use for an animation based on reports or metrics, a real-product walkthrough, a format adaptation, or a correction attached to a board/video moment. These are original Studio working procedures, not new runtime commands or an integration with Claude. Keep the current owner, project and stage. Load only the relevant section.

## Decision and source before design

Reuse the audience, placement, message, duration, brand and supplied materials. Ask only a consequential missing question; a fixed number of questions, scenes or words is not a quality guarantee. Define what the audience should understand or do. Prefer inspectable raw tables, exact customer wording and real product states over an unsupported summary. Do not require additional research for stable craft or repeatedly ask for supplied facts.

For each material number or claim, keep a compact entry in existing research/working notes:

| Field | Record |
| --- | --- |
| Identity | Stable claim ID and exact proposed display text |
| Source | Supplied file/table/query or public document, precise locator, source revision/hash when available, and snapshot/as-of date |
| Meaning | Unit, currency if relevant, population, period, filters, denominator and comparison basis |
| Derivation | Reproducible calculation, exclusions, rounding and missing-data handling |
| Evidence | Verified, contradicted or Unknown; method and actual check result |
| Dependents | Copy IDs, scenes/board panels, formats and accepted artifact revision using it |

Use the existing contract's supported source/claim/copy fields and link to these notes; do not insert invented fields into a closed motion or FrameCut runtime schema. Keep private records in the authorized project store, never the shared plugin. If storage is unavailable, keep a portable session record and say so.

Reconcile totals only across comparable, mutually exclusive groups. Check duplicates, missing rows, period alignment and units. Distinguish percentage-point changes from relative changes. Do not turn correlation, a selected cohort or a small historical sample into a causal or general effectiveness claim. If raw evidence is missing, retain a clearly identified placeholder or omit the claim; do not mark it verified from confident prose.

## Report to complete visual storyboard

1. Research Evidence establishes the claim and its limits; the user chooses the communicative goal where unresolved. An interactive dashboard is optional, never a prerequisite for a short film.
2. Motion Graphics turns the supported finding into a timed visual argument. Choose chart scale, axes, labels and transitions that preserve the comparison. Keep qualifiers readable; check the text and final numbers in the actual frames.
3. Show the whole planned sequence, including setup, evidence, development and ending, with its meaningful intermediate states. Reuse existing board owners. In FrameCut, show every requested format's complete visual contact sheets, collect corrections and obtain acceptance of the current board before final rendering. A video sample is optional on request.
4. Use Motion Graphics for designed animation and FrameCut when footage/mixed-media editing requires it. Reuse the FrameCut working agreement and stage-scoped handoff. Data analysis does not authorize an external connector, upload or automatic refresh.
5. If a source changes, identify affected claims, copy, panels, sound/timing dependencies and deliverables. Recompute before reuse, mark affected evidence stale and return affected creative decisions to board review. Preserve unrelated accepted work. A refreshed data source never silently changes an accepted final; exported MP4 is a fixed artifact.

## Feedback attached to an artifact

Keep a compact note in the existing project revision history or FrameCut pending-feedback record: `feedback_id`, artifact/project revision, panel or scene/event ID, format, frame or time with FPS/timebase when known, exact request, affected property, resolution and verification reference. Optional timecodes cannot replace artifact identity.

- A board comment needs no video. Prefer the panel ID when that is what the user saw.
- With an unambiguous current target, propose/apply only the requested local correction under existing authorization. Inspect its dependent timing/captions/layout before execution; retain copy and brand locks.
- After a split, ripple edit, source replacement or revision change, use verified event/source mappings to relocate the target. Never apply an old absolute timestamp to a different scene. If several targets fit, ask one focused clarification and retain the unresolved note.
- Track pending, needs-clarification, applied and verified separately. Report what changed and which updated evidence was actually inspected. User acceptance is a separate decision; a resolved note is not complete-board approval.
- When the host lacks timeline comments, show the frame/panel and keep the note in chat or an authorized project file. Do not claim a clickable collaborative interface, automatic synchronization or saved comments without actual capability and write evidence.

## Formats and product truth

For each requested format, reconsider reading order, chart labels, line breaks, object placement and safe areas. Use existing format-specific scene parameters and framing. A crop alone cannot establish a readable composition; inspect each board at intended viewing size. Preserve exact copy unless rewriting is authorized and recheck reading time after reflow. No universal eight-word or three-second limit substitutes for the brief and readability check.

For a walkthrough use authorized screenshots/recordings of real states. Accessible source code may establish actual labels, assets and behavior, but does not prove the running screen was captured. Distinguish a faithful reconstruction from recorded interaction, show the control/action/result relationship and never invent a successful click, feature or performance claim. Follow the existing [product-film method](../../hyperframes-workflow/references/product-films.md), including fictional demonstration data and real feature fidelity. Do not execute an app, expose client data or publish a walkthrough merely because source was supplied.

## Sources and capability boundary

Reviewed 2026-10-21. Editorial lead: Ruben Hassid, [Motion](https://ruben.substack.com/p/claude-motion-and-dashboards), 2026-10-14. It motivates this knowledge update; its examples, prompts and sales comparisons are not bundled or treated as performance evidence.

Primary references: Anthropic, [Motion](https://support.claude.com/en/articles/17454997-get-started-with-claude-motion) and [Dashboards](https://support.claude.com/en/articles/17454700-get-started-with-claude-dashboards). The former documents code-based animation and MP4 export; the latter documents inspectable chart queries and last-refresh information. These describe Claude's product, not Studio tools. No reviewed source establishes a Studio-callable Motion/Dashboards API. Verify actual host access before offering any native operation. A supplied CSV is a snapshot unless a real refresh mechanism exists. Plan availability, integrations and pricing are time-sensitive and are deliberately not frozen here.
