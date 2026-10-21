# Creative Studio 1.119.0

Lessons from the owner's 2026-10-16 test reel, applied as one small maintenance release.

- Reel plans test stopping power (first second, one big moment, a reason to choose the business) and require pictures for service, product and before-and-after reels; a type-only reel is offered only as a named, weaker fallback.
- Acceptance for HyperFrames and hand-written compositions: `--composition` (text audit bound to the composition's SHA-256), `--copy` (locked copy), `--motion-activity` (measurement bound to the encoded file).
- Sound design keeps a landing the motion score marks audible.
- The workflow orchestrator's coordination paragraphs moved verbatim to `references/routing-boundaries.md#coordination-detail`; startup and routing table unchanged. ChatGPT startup should be rechecked by the owner.

Before and after: `tests/motion_acceptance_test.py` (3 errors on 1.118.0, OK now), `tests/motion_sound_marked_test.py` (fails on 1.118.0, OK now); host-eval G12 records from 2026-10-16 show the reel request routing to Creative Video Producer and the orchestrator, where the rules now live.
