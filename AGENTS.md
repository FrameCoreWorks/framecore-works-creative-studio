# Repository maintenance

This repository publishes FrameCore Works Creative Studio. The editable plugin is in `plugins/framecore-work-creative-studio/`; preserve vendored `upstream/` snapshots and their provenance.

## Skill names

Follow `plugins/framecore-work-creative-studio/docs/skill-naming.md` for all current and new skills. Keep technical IDs, paths, invocations and routing stable. Every canonical skill requires `agents/openai.yaml` with `interface.display_name`: English words separated by spaces, an uppercase first letter for each word, and preserved AI/UGC/HyperFrames/OpenCut spelling. Also require a nonempty `interface.short_description`, using the repository's validated 25–64 character, double-quoted scalar format. Do not put display metadata under `metadata` or replace a technical ID with a title.

## Repository language and installation documentation

Write maintained repository documentation, operational instructions, comments and general learning-template guidance in English. Preserve localized UI resources, exact-copy teaching examples, multilingual evaluation inputs and historical observed replies in their original language; they are data, not untranslated general guidance. Keep pinned upstream snapshots byte-identical and preserve provenance. Repository language does not fix Studio's response language. Preserve the complete startup content while automatically following each user's language.

Keep README installation sections as links to the complete `CHATGPT_INSTALL.md` and `CODEX_INSTALL.md` procedures. Do not duplicate installation prompts or add a short copy-paste command to README. Keep host selection, capability checks, source pinning, authorization, installation/update handling and verification in those guides. A repository URL identifies source; it does not itself grant installation permission or provide missing host capabilities.

## Protected Studio startup

Preserve the working startup integration as a permanent product contract. `workflow-orchestrator` owns startup and must remain an exposed, readable skill with complete interface metadata. Resolve skill resources from the host's catalog; do not invent a resource URI or treat presence in an archive as proof of registration.

For every sent bare Studio invocation or start request, automatically select the user's response language under `skills/workflow-orchestrator/references/startup-and-creative-menus.md`. Explicit preferences take precedence; otherwise use meaningful user text, actually supplied host language for bare/numeric inputs, then conversation language. Never infer country or hidden host settings, and never require an explicit translation request. English is only a provisional fallback when no signal exists. Keep complete, byte-matched English (`assets/startup-welcome.en.md`) and approved Polish (`assets/startup-welcome.pl.md`) excerpts plus the synchronized language policy near the beginning of `workflow-orchestrator/SKILL.md`, before QA and routing. Copy the matching language excerpt or translate the entire English source for other languages. Preserve all six capability bullets, qualifications, optional materials, structure and numbered options; never reduce startup to modes alone or add another introduction/menu. Localize later menus without changing token mappings. Preserve direct-task/resume handling and repeated-invocation checkpoints; a language change must replace the old-language welcome. The former Polish-default rule is superseded by the owner's automatic-language requirement.

Keep both localized welcome/excerpt, language-policy projection and skill-metadata validation active. After changes to startup, manifests, skill exposure, metadata or packaging, verify ordinary ChatGPT startup separately from Work and record the tested client and reasoning setting. The full-welcome contract is the same at every reasoning setting. Record owner-reported success as `PASS_REPORTED`; source validation and saved-package equality do not establish active-client behavior. A diagnostic that manually inspects plugin files is not a normal startup test.

## Verification and publication

Make focused edits and preserve the user's changes. Run the canonical `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs` check. For a release, synchronize both plugin manifests and current version markers, regenerate `config/install-sources.json` using `python3 scripts/build_install_manifest.py`, and run `python3 scripts/package_release.py`. Preserve unexecuted evaluation status; source checks are not host UI or media tests.

## Paired GitHub and ChatGPT updates

The user requires the existing ChatGPT plugin and this GitHub repository to remain synchronized. For every explicitly requested plugin implementation or update, complete both operations in the same task: verify the repository changes, commit and push them to GitHub, update the existing hosted plugin from the same source, and read back both destinations. This is standing project authorization for the paired update unless the user's current request explicitly limits the work to review, planning or local-only changes. A metadata-only repository correction needs no redundant hosted release when the plugin package is unchanged.

Treat `plugins/framecore-work-creative-studio/` as the shared package. Its version, complete path inventory and file contents must match the saved ChatGPT package. Repository-only maintenance instructions, CI, verification reports and distribution scripts stay outside that package. Preserve plugin identity, audience, assets, prompts, local unrelated settings and vendored provenance. Use the current hosted source as the guarded update baseline; never create a duplicate plugin or overwrite a concurrent edit.

Keep source checks, GitHub publication, saved-plugin readback and active-client behavior as separate evidence, while completing the paired source update together. Record the GitHub commit and hosted release ID. Compare full-package hashes when archive access allows; explicitly record unreadable files or normalization differences instead of calling a partial comparison full byte equality. A failed save, push, release or readback remains an unresolved sync state; report it and continue recovery where authorized. Do not close an update as synchronized merely because one destination succeeded.
