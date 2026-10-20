# Repository maintenance

## Current owner instruction (2026-10-20)

Work directly on `main`; do not create local or remote working branches. After the required checks pass, commit and fast-forward push the completed changes to `main`. This supersedes the older working-branch guidance below. Preserve concurrent work and never force-push.

This development thread owns repository fixes and sandbox testing. A separate owner-directed thread owns permanent supplemental tool integrations in the private hosted plugin. For each shared-package release, update the existing hosted plugin with Plugin Creator when available, using its current release guard and preserving those integrations. Read back the affected files. The hosted version can be newer than the public source version because of its private overlay; record both versions and the actual comparison scope. Do not publish private overlay files or settings to this repository. These instructions supersede the historical `not_tracked` and whole-package equality rules below. Source checks, saved files and fresh-client behavior remain separate evidence.

This repository publishes FrameCore Works Creative Studio. The editable plugin is in `plugins/framecore-work-creative-studio/`; preserve vendored `upstream/` snapshots and their provenance.

## Skill names

Follow `plugins/framecore-work-creative-studio/docs/skill-naming.md` for all current and new skills. Keep technical IDs, paths, invocations and routing stable. Every canonical skill requires `agents/openai.yaml` with `interface.display_name`: English words separated by spaces, an uppercase first letter for each word, and preserved AI/UGC/HyperFrames/OpenCut spelling. Also require a nonempty `interface.short_description`, using the repository's validated 25–64 character, double-quoted scalar format. Do not put display metadata under `metadata` or replace a technical ID with a title.

## Repository language and installation documentation

Write maintained repository documentation, operational instructions, comments and general learning-template guidance in English. Preserve localized UI resources, exact-copy teaching examples, multilingual evaluation inputs and historical observed replies in their original language; they are data, not untranslated general guidance. Keep pinned upstream snapshots byte-identical and preserve provenance. Repository language does not fix Studio's response language. Preserve the complete startup content while automatically following each user's language.

Keep README installation sections as links to the complete `CHATGPT_INSTALL.md`, `CODEX_INSTALL.md` and `CLAUDE_INSTALL.md` procedures. Do not duplicate installation prompts or add a short copy-paste command to README. Keep host selection, capability checks, source pinning, authorization, installation/update handling and verification in those guides. A repository URL identifies source; it does not itself grant installation permission or provide missing host capabilities.

## Protected Studio startup

Preserve the working startup integration as a permanent product contract. `workflow-orchestrator` owns startup and must remain an exposed, readable skill with complete interface metadata. Resolve skill resources from the host's catalog; do not invent a resource URI or treat presence in an archive as proof of registration.

For every sent bare Studio invocation or start request, automatically select the user's response language under `skills/workflow-orchestrator/references/startup-and-creative-menus.md`. Explicit preferences take precedence; otherwise use meaningful user text, actually supplied host language for bare/numeric inputs, then conversation language. Never infer country or hidden host settings, and never require an explicit translation request. English is only a provisional fallback when no signal exists. Keep complete, byte-matched English (`assets/startup-welcome.en.md`) and approved Polish (`assets/startup-welcome.pl.md`) excerpts plus the synchronized language policy near the beginning of `workflow-orchestrator/SKILL.md`, before QA and routing. Copy the matching language excerpt or translate the entire English source for other languages. Preserve all six capability bullets, qualifications, optional materials, structure and numbered options; never reduce startup to modes alone or add another introduction/menu. Localize later menus without changing token mappings. Preserve direct-task/resume handling and repeated-invocation checkpoints; a language change must replace the old-language welcome. The former Polish-default rule is superseded by the owner's automatic-language requirement.

Keep both localized welcome/excerpt, language-policy projection and skill-metadata validation active. After changes to startup, manifests, skill exposure, metadata or packaging, verify ordinary ChatGPT startup separately from Work and record the tested client and reasoning setting. The full-welcome contract is the same at every reasoning setting. Record owner-reported success as `PASS_REPORTED`; source validation and saved-package equality do not establish active-client behavior. A diagnostic that manually inspects plugin files is not a normal startup test.

## Verification and publication

Make focused edits and preserve the user's changes. Run the canonical `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs` check and `bash scripts/check_all.sh`. The historical legacy suite (`validate-package.mjs`, `package.test.mjs`) was retired on 2026-10-10 by owner decision; both are inert stubs and `tests/legacy-baseline.json` is history. `bash scripts/check_all.sh --fast` is the quick edit-loop subset; releases run the full list. For a release, synchronize the plugin manifests (`plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`), the plugin version in the root `.claude-plugin/marketplace.json` and current version markers, regenerate `config/install-sources.json` using `python3 scripts/build_install_manifest.py`, and run `python3 scripts/package_release.py`. Preserve unexecuted evaluation status; source checks are not host UI or media tests.

## Owner product decisions (2026-10-10)

Studio is a general product for any user, not a personal tool: never personalize defaults to one person's rates, tools, clients or teaching context; anything user-specific (rates, VAT status, preferred generators, brand kits) is an input the user supplies at run time. Headless host-evaluation runs use the Claude plan's usage, not separate billing (owner decision 2026-10-11): run them without asking, at most 25 cases per full pass and 5 per release-gate subset, and record cases, tokens and time with every run; a dollar figure from Claude Code is an API-price equivalent, not a cost. The improvement plan in `docs/improvement-plan-2026-10.md` (phases 0 to 5) was completed on 2026-10-11 and closed by the owner on 2026-10-12; its deferred items follow maintenance mode.

## Maintenance mode (owner decision 2026-10-12)

Studio is a complete working tool, and development is in maintenance mode: do not expand or improve it for its own sake. Change the shared package, or add a skill, reference, template, style, scenario or evaluation case, only for a concrete trigger:

- a defect seen in real use (the owner's or a user's report) or in a host evaluation;
- a host, model or generator change that breaks or alters behavior;
- a dated fact that has gone stale (generator maps, dialect cards, platform specifications).

Name the trigger in the ledger entry and the commit, and show that case before and after the change. Make the smallest fix in the text the model actually reads (the owning `SKILL.md`, which single-turn runs load) rather than a new file; every package path is permanent. Creative improvements teach how to build an idea from the brief; they never add ready-made ideas, scenarios or category lists (owner decision 2026-10-11). Studio is a base for work with a person who chooses and directs; do not present it as replacing that judgment. An idea without a trigger goes to the owner as a one-line note, not as work. Repository maintenance (CI, release scripts, records) follows the same rule.

Owner decision 2026-10-12, later the same day: motion graphics is Studio's main paid use, so the owner opened one development round for it, released as 1.70.0, as an explicit exception to maintenance mode. In Claude Code, client reels and ads are built as HyperFrames compositions with HyperFrames' own skills, while Studio keeps the brief, idea, copy locks, board plan and review. Work left from that round is listed in `docs/handover-motion-1.70.md`; it follows maintenance mode unless the owner asks for it.

## Recommended extensions (owner decision 2026-10-16)

Every repository the owner sends for review is also added to the [extension registry](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.json) as a natively installable option, following `docs/extension-registry.md`: pinned to the reviewed commit or package version, with each host's status and its plan, install, verify and remove steps tried in a sandbox. This is the trigger for such an entry under maintenance mode. Studio installs an extension only on a user's explicit request.

## Development provenance

Several surfaces develop this repository: the owner, ChatGPT Work, Codex and Cloud Code. `docs/roadmap.md` says which way to develop Studio and why; keep it current when the direction changes. Before writing, read `docs/roadmap.md`, `docs/development-ledger.md`, `CHANGELOG.md`, `RELEASE_STATUS.md` and current Git history; preserve compatible work from other surfaces and never overwrite it without inspecting its intent. Record the baseline SHA and re-check the branch head before committing or pushing; do not resolve drift with `reset --hard` or a force push.

Treat `main` as protected even without GitHub enforcement. Develop on a local working branch, for Cloud Code `cloud-code/<change-id>-<short-scope>` with change ID `CC-YYYYMMDD-NN`, and integrate through review unless the owner decides otherwise; the branch stays local (see Branch hygiene). Owner decision 2026-10-08: after every update, once the canonical validator and all test suites pass, commit and push it to `main` automatically without asking, as a fast-forward with no force push; when the shared package changed, first complete the release steps below so `main` always carries a released, installable version, then record the GitHub publication. A failed check blocks the push until it is fixed or reported. Commits carry the trailers `Origin-Agent`, `Change-ID`, `Baseline-SHA`, `Shared-Package-Changed`, `ChatGPT-Work-Sync` and `Codex-Sync`. Each integrated change adds a ledger entry with origin, baseline, result, version, scope, verification and per-host state. Write `synchronized` only with readback evidence; otherwise use `pending`, `unknown` or `not_run`.

## Branch hygiene (owner decision 2026-10-19)

Applies to every surface that writes to this repository: Claude Code (local and cloud), Codex (local and cloud) and ChatGPT Work. The owner deleted 80 accumulated remote branches on 2026-10-19; keep the remote at `main`, `gh-pages` and active session branches only.

- Develop on a local working branch (for Cloud Code `cloud-code/<change-id>-<short-scope>`, for Codex `codex/<change-id>-<short-scope>`) and do not push it. Integrate by fast-forwarding `main` after the checks pass: `python3 scripts/release.py prepare|publish ... --push` for a release, `git push origin HEAD:main` for a change that does not touch the shared package.
- Push a working branch only to open a pull request; the repository deletes the head branch after the merge.
- A branch the host itself requires (a Claude Code cloud `ccr-*` branch, a Codex cloud task branch, a ChatGPT Work branch) is the one exception: push only that branch, keep it equal to `main`, and name it in `STUDIO_RELEASE_BRANCHES` so `release.py` updates it. `release.py` never pushes the local working branch.
- Never create a remote branch per release or per change. Never delete `main` or `gh-pages` (`gh-pages` serves the motion player). Never delete a branch another surface is using without the owner; deleting branches is the owner's step.
- Before ending a task, run `git ls-remote --heads origin`. Anything beyond `main`, `gh-pages` and your own session branch goes in your report to the owner, with whether it is merged into `main`.

## Paired GitHub and ChatGPT updates

The user requires the existing ChatGPT plugin and this GitHub repository to remain synchronized. For every explicitly requested plugin implementation or update, complete both operations in the same task: verify the repository changes, commit and push them to GitHub, update the existing hosted plugin from the same source, and read back both destinations. This is standing project authorization for the paired update unless the user's current request explicitly limits the work to review, planning or local-only changes. A metadata-only repository correction needs no redundant hosted release when the plugin package is unchanged.

Owner decision 2026-10-09: the owner performs the hosted ChatGPT Work update himself in Plugin Creator; a session without Plugin Creator access cannot do it. After every release that changes the shared package, do not ask whether to update the hosted plugin. Report the hosted state as pending and give the ready, standalone update prompt based on `CHATGPT_UPDATE.md` (source commit, readback fields). Plugin Creator reads the declared files from the repository at that commit through `config/install-sources.json`, not the release ZIP; the ZIP SHA-256 is reference only (owner correction 2026-10-10). When the owner returns the readback JSON, compare it with `scripts/check_hosted_readback.py` and record the result.

Owner decision 2026-10-10: hosted readback verification is stopped. After a release, give only the short Plugin Creator update prompt (source commit, no readback file), do not ask for or compare a readback or diff, and record ChatGPT Work as `not_tracked`; the owner tests the plugin himself and reports problems. This supersedes the readback steps above and in the paired-update section; `scripts/check_hosted_readback.py` stays available if the owner sends a readback on his own.

Treat `plugins/framecore-work-creative-studio/` as the shared package. Its version, complete path inventory and file contents must match the saved ChatGPT package. Repository-only maintenance instructions, CI, verification reports and distribution scripts stay outside that package. Preserve plugin identity, audience, assets, prompts, local unrelated settings and vendored provenance. Use the current hosted source as the guarded update baseline; never create a duplicate plugin or overwrite a concurrent edit.

Never delete, rename or move a path inside the shared package. ChatGPT Work's `update_plugin` only adds and overwrites files; it cannot delete files or replace the whole package, so a removed or moved path stays in the saved plugin and breaks inventory parity with the repository (confirmed by the owner's Plugin Creator diagnostic on 2026-10-06; see `docs/development-ledger.md`, CC-20261006-04). To retire a file, keep its path and replace its content with an inert pointer or stub, as done for the 35 `integrations/workflow-kit/upstream/.agents/skills/*/SKILL.md` discovery stubs. Package size reductions that depend on deleting paths are not achievable for existing hosted installations.

Keep source checks, GitHub publication, saved-plugin readback and active-client behavior as separate evidence, while completing the paired source update together. Record the GitHub commit and hosted release ID. Compare full-package hashes when archive access allows; explicitly record unreadable files or normalization differences instead of calling a partial comparison full byte equality. A failed save, push, release or readback remains an unresolved sync state; report it and continue recovery where authorized. Do not close an update as synchronized merely because one destination succeeded.
