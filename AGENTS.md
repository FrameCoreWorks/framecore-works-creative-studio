# Repository maintenance

This repository publishes FrameCore Works Creative Studio. The editable plugin is in `plugins/framecore-work-creative-studio/`; preserve vendored `upstream/` snapshots and their provenance.

## Skill names

Follow `plugins/framecore-work-creative-studio/docs/skill-naming.md` for all current and new skills. Keep technical IDs, paths, invocations and routing stable. Every canonical skill requires `agents/openai.yaml` with `interface.display_name`: English words separated by spaces, an uppercase first letter for each word, and preserved AI/UGC/HyperFrames/OpenCut spelling. Do not put display metadata under `metadata` or replace a technical ID with a title.

## Verification and publication

Make focused edits and preserve the user's changes. Run the canonical `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs` check. For a release, synchronize both plugin manifests and current version markers, regenerate `config/install-sources.json` using `python3 scripts/build_install_manifest.py`, and run `python3 scripts/package_release.py`. Preserve unexecuted evaluation status; source checks are not host UI or media tests.

GitHub publication and updating an existing hosted plugin are separate operations. Use the current hosted source as the baseline, preserve identity and metadata, and verify saved files after an authorized update.
