# Portable extraction evidence

Research baseline: Studio 1.174.1 at public commit `2942af902909b83441fc4c428d9debd532500c5a`. Reconcile with current main before implementing. This summary replaces local-only extraction maps and audit links; it does not pretend to reproduce private source paths or the full audit evidence.

## Owned files and dependencies

The [public owner inventory](PUBLIC-OWNER-INVENTORY.json) preserves every relative path, size and SHA-256 for 35 `opencut-video-studio` files, 412 `hyperframes-workflow` files and 30 `remotion-video-production` files. All 477 hashes and inclusion in the original extraction maps were verified locally. The wider motion map had 875 source rows and the Cut map 157, with overlap; inventory is not semantic review of every sentence.

FrameCut's executable dependency closure includes Caption Studio rendering, storyboard composition, shared fonts and the legacy edit exporter. Motion uses shared fonts and caption/sound helpers too. A standalone release must localize required resources explicitly and prove execution with Studio absent. Preserve source files and licences during initial extraction; do not equate string/import candidates with executed runtime edges.

Retain the current generic `framecore-task-request/1` and `framecore-task-result/1` envelopes, validating the selected schema definitions. Generic intake does not replace FrameCut's stronger motion-request and attach/bind context checks. FrameCut owns global sequence time; FrameMotion owns a local composition starting at zero. The caller dispatches work; do not invent recursive companion calls or a second master timeline.

Private installation overlays were separately inventoried. Their presence does not authorize public copying. Vendor notices, font licences and starter provenance need per-source dispositions, not a blanket assumption that a public repository licence clears every embedded asset.

## Prior audit findings referenced by the plans

These are reported observations from the earlier local audit, not new reproductions performed during this publication. Reproduce against the implementation baseline before fixing; keep failures separate from the research packet's arithmetic checks.

| IDs used in plans | Reported failure to preserve as a regression concern |
|---|---|
| E001 | Short picture stream can be hidden by a longer audio/container duration |
| E002 | Incorrect single Remotion extrapolation option instead of separate left/right behavior |
| E004–E008 | Weak byte identity, stale specification acceptance, wrong dimensions, empty skip justification and inadequate alpha checks |
| E012–E014 | Clipped storyboard text, negative caption timing and literal WebVTT/entity corruption |
| E016 | Numeric dialogue can be omitted from a proposed edit |
| E020 | Four-digit CSS hex color can crash the examined route |
| E022 | Audio-onset test can succeed without a meaningful observed onset |
| E027 | Browser/Python text-check behavior differs |

The current `framecut.py` exporter withholds basic EDL/OTIO for an entire complex sequence containing transitions, speed changes or freezes. It still emits native JSON, relink, CSV and loss information. This is a current behavior to describe accurately, not a request to weaken it. Native NLE roundtrips, source-to-output semantics and perceptual equivalence need their own evidence.

## Historical/private knowledge

The local research read Claude's earlier split plans, workshop lessons and shared knowledge handovers. Useful situated preferences include engine locks, scoped one-shot exceptions and reading holds. Keep them as attributed project/profile evidence where applicable, not universal empirical standards. The full private map and originals remain available to the owner's local Claude/Codex environment; a cloud-only session should record that access limit rather than claim it read them.

The public packet contains original applied guidance and public-source citations sufficient to assess its recommendations. A future complete extraction still needs the local/private intake, rights decisions and executable dependency proof specified by the plans.
