# Repository maintenance

This repository publishes FrameCore Works Creative Studio. The editable plugin is in `plugins/framecore-work-creative-studio/`; preserve vendored `upstream/` snapshots and their provenance.

## Skill names

Follow `plugins/framecore-work-creative-studio/docs/skill-naming.md` for all current and new skills. Keep technical IDs, paths, invocations and routing stable. Every canonical skill requires `agents/openai.yaml` with `interface.display_name`: English words separated by spaces, an uppercase first letter for each word, and preserved AI/UGC/HyperFrames/OpenCut spelling. Also require a nonempty `interface.short_description`, using the repository's validated 25–64 character, double-quoted scalar format. Do not put display metadata under `metadata` or replace a technical ID with a title.

## Protected Studio startup

Preserve the working startup integration as a permanent product contract. `workflow-orchestrator` owns startup and must remain an exposed, readable skill with complete interface metadata. Resolve skill resources from the host's catalog; do not invent a resource URI or treat presence in an archive as proof of registration.

For every sent bare Studio invocation or start request, output the full canonical Polish welcome from `skills/workflow-orchestrator/assets/startup-welcome.pl.md` before asking for the work mode. Keep its byte-matched embedded excerpt near the beginning of `workflow-orchestrator/SKILL.md`, before general QA and routing instructions, so startup does not depend on an additional asset read. Never reduce it to modes alone, paraphrase it, or add another introduction/menu. Preserve explicit language requests, direct-task and resume handling, and repeated-invocation checkpoint behavior.

Keep canonical welcome/excerpt and skill-metadata validation active. After changes to startup, manifests, skill exposure, metadata or packaging, verify ordinary ChatGPT startup separately from Work and record the tested client and reasoning setting. The full-welcome contract is the same at every reasoning setting. Record owner-reported success as `PASS_REPORTED`; source validation and saved-package equality do not establish active-client behavior. A diagnostic that manually inspects plugin files is not a normal startup test.

## Verification and publication

Make focused edits and preserve the user's changes. Run the canonical `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs` check. For a release, synchronize both plugin manifests and current version markers, regenerate `config/install-sources.json` using `python3 scripts/build_install_manifest.py`, and run `python3 scripts/package_release.py`. Preserve unexecuted evaluation status; source checks are not host UI or media tests.

## Paired GitHub and ChatGPT updates

The user requires the existing ChatGPT plugin and this GitHub repository to remain synchronized. For every explicitly requested plugin implementation or update, complete both operations in the same task: verify the repository changes, commit and push them to GitHub, update the existing hosted plugin from the same source, and read back both destinations. This is standing project authorization for the paired update unless the user's current request explicitly limits the work to review, planning or local-only changes. A metadata-only repository correction needs no redundant hosted release when the plugin package is unchanged.

Treat `plugins/framecore-work-creative-studio/` as the shared package. Its version, complete path inventory and file contents must match the saved ChatGPT package. Repository-only maintenance instructions, CI, verification reports and distribution scripts stay outside that package. Preserve plugin identity, audience, assets, prompts, local unrelated settings and vendored provenance. Use the current hosted source as the guarded update baseline; never create a duplicate plugin or overwrite a concurrent edit.

Keep source checks, GitHub publication, saved-plugin readback and active-client behavior as separate evidence, while completing the paired source update together. Record the GitHub commit and hosted release ID. Compare full-package hashes when archive access allows; explicitly record unreadable files or normalization differences instead of calling a partial comparison full byte equality. A failed save, push, release or readback remains an unresolved sync state; report it and continue recovery where authorized. Do not close an update as synchronized merely because one destination succeeded.
