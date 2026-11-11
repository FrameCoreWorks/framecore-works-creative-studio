# FrameCut and FrameMotion: temporary research packet

Read [the current handover](../../handover-framecut-framemotion-2026-11-11.md) first. The owner wants Claude to read the evidence, assess applicability, implement justified work within the applicable scope, preserve useful knowledge in maintained destinations, and then clean temporary handovers/packs from the repository. This packet is input to that judgment, not automatic approval of every proposed design.

## Read in this order

1. [Design](DESIGN.md), [coordinated plan](PLAN.md), [FrameCut plan](FRAMECUT-PLAN.md), [FrameMotion plan](FRAMEMOTION-PLAN.md).
2. [Launch/review-policy proposals](LAUNCH-DECISIONS.md), [knowledge protocol](KNOWLEDGE-PROTOCOL.md), [extraction summary](EXTRACTION-SUMMARY.md).
3. Both craft corpora below, their primary sources and independent reviews.
4. [Review status and evidence boundaries](REVIEW-STATUS.md), then classify each recommendation as applicable, needs adaptation, deferred or rejected before implementation.

| Corpus | Main guidance | Examples and sources |
|---|---|---|
| FrameMotion, 20 cards | [Decision cards](research/motion/decision-cards.md), also [structured JSON](research/motion/decision-cards.json) | [Five studies and rubric](research/motion/worked-studies-and-rubric.md), [curriculum/engine bridge](research/motion/curriculum-and-engine-bridge.md), [24 source records](research/motion/source-ledger.json) |
| FrameMotion, 8 specialist cards | [Advanced compositing and four numerical examples](research/motion-specialist/export/advanced-motion-decision-cards.md) | 13 source records inline; [analytic fixture](research/motion-specialist/verify-calculations.py), [results](research/motion-specialist/calculation-results.json) |
| FrameCut, 22 cards | [Editing compendium, six cases and curriculum](research/editing/applied-editing-compendium.md) | [24 source records](research/editing/source-ledger.json) |
| FrameCut, 8 specialist cards | [FCP/Avid/assistant-editor compendium](research/editing-specialist/compendium.md) | [Three cases](research/editing-specialist/worked-cases.md), [15 source records](research/editing-specialist/source-ledger.json), [analytic fixture](research/editing-specialist/verify-calculations.py), [results](research/editing-specialist/calculation-results.json) |

Totals: **58 cards, 18 example/study sections and 76 source records**. Source records have different access depths and may describe the same document through another locale, version or redirect. They are not 76 completely read independent manuals. Seven specialist example sections have executed arithmetic; no new native-editor, rendering, listening or audience experiment was performed.

The reusable bridge is **creative intent → diagnosis → manual operation → agent decision → supported code/parameters → observed artifact → revision**. Apply contextual judgment rather than universal timing/transition/LUT presets. A valid file does not prove a truthful edit, readable title, correct sound join or pleasing motion.

## Later owner scope

[Complete YouTube productions and VideoLyrics](YOUTUBE-VIDEOLYRICS-SCOPE.md) records the subsequent capability request separately from the completed research corpus and the new independent research tasks. It is a scope input for Claude, not additional verified craft knowledge.

## Portability and provenance

The [export manifest](EXPORT-MANIFEST.json) records source-derived file hashes before and after portability edits. Public owned-source paths and hashes are in [the 477-file inventory](PUBLIC-OWNER-INVENTORY.json). Original private path maps, brand/client materials, raw manuals/archives and local-only receipts are intentionally outside the public packet. Their exclusion is explicit; this is not a complete public copy of private research folders.

Historical planning documents retain their original proposal status. The current handover supplies the owner's subsequent intake/implementation/cleanup workflow. Historical reviewer hashes refer to the snapshots actually reviewed, not automatically to sanitized exports. Local source register/verifier references are historical provenance; this packet's README, extraction summary and review status replace them for portable reading.

To repeat arithmetic without overwriting the recorded motion result, copy each Python fixture into a new temporary directory and run there. The editing fixture prints JSON; the motion fixture writes a new calculation-results.json and deliberately refuses overwrite. These scripts validate equations, not an application's output.

Before cleanup, preserve the useful original guidance, durable source links, decisions, outstanding work and required regression evidence in the maintained plan/owners. Update incoming links to their maintained destinations or commit-pinned history. Do not delete existing Studio runtime/knowledge merely because this packet discusses extraction.
