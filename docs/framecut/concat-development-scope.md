# FrameCut development scope, 2026-10-21

## Authorization and baseline

The owner explicitly requested implementation of all six recommended Concat-inspired development areas and their Studio orchestration. Baseline: `c700ad256dcf83ec9134c994d1a12f3c4b278f49`, shared package 1.115.0. This request reopens development after the testing pause. Concat `816a8f0e02829a718a2475c3dd4673bea3e5a154` was reviewed as a functional reference; its AGPL code, assets and dependencies are not incorporated or translated. Implementations are original FrameCut code.

## Bounded instruction packet

- Owner: FrameCut (`opencut-video-studio`); existing storyboard, caption, audio and motion owners retain their responsibilities.
- Implement: compact timeline queries and transactional split/trim/move/ripple removal; actual composited stills and complete storyboard coverage; durable job status/cancellation/resumption; keyframe transforms and per-deliverable framing; freeze frames and variable playback speed; a versioned, bounded effect catalogue with executable fixtures.
- Allowed implementation: existing FrameCut runtime and schema, new focused runtime modules, FrameCut tests, storyboard/runtime capability instructions in the existing owning skills, installation metadata, release metadata and repository evidence.
- Preserve: exact master-frame/rational-FPS and source-PTS authority, immutable sources and revisions, locked content, strict failures, full storyboard review before final, optional requested samples, scoped external motion, complete startup/menu and existing skill IDs, private integrations and vendored snapshots.
- Excluded: replacing the editor architecture with Concat, desktop UI, Rust/GPU migration, generative providers, voice cloning, automatic model downloads, optional background-removal/stabilization installations, unrelated integrations.
- Dependency: Pillow, already used by the storyboard compositor, may support native image transforms; capability failures must name the missing dependency, never silently omit an effect.

## Review and execution packet

Verify actual decoded media as well as contracts: split/trim preserve source and animation windows; ripple maps dependents or fails explicitly; failed batches leave state unchanged; stills match the same composition/time as video; boards cover every event and meaningful declared beat; ramps preserve video/audio/caption maps; restart/cancel never publishes a partial final; effects are versioned and unknown effects fail. Run existing FrameCut regressions, targeted new tests, realistic source-guided skill tasks, the canonical validator and the full repository gate. Separate sandbox media evidence from untested fresh-client behavior. Publish the tested repository first, then update and read back the existing plugin while preserving its current private overlay.

Rollback is a selective revert of this change on the current branch. Never force-push or replace newer unrelated work.
