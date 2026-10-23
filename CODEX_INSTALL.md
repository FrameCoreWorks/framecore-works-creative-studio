# Install Creative Studio in Codex

This is the complete native direct-source procedure for the assistant performing a user-requested installation in Codex with filesystem access. ChatGPT Work installations follow [CHATGPT_INSTALL.md](CHATGPT_INSTALL.md).

## 1. Confirm intent and host capabilities

1. Use the user's explicit installation request as authorization for the described local Studio installation. Do not ask again for unchanged scope. A bare repository link without installation intent is source context; clarify the intended action before writing an installation.
2. Resolve the actual Codex host, filesystem access and supported skill locations. Use Plugin Creator for package checks when available; its documented Codex invocation is `$plugin-creator`, selected from completion. Pasted text alone does not establish availability.
3. The native helper below does not depend on Plugin Creator. If that capability is absent, report it and continue with the supported local route. Do not create a hosted plugin copy, register a plugin catalog or claim a connector was enabled.
4. Continue in the user's language, including the complete startup welcome and later menus. Apply the automatic language policy in Workflow Orchestrator; English repository documentation and localized examples do not set a fixed response language.

## 2. Pin and verify the complete source

Source repository: <https://github.com/FrameCoreWorks/framecore-works-creative-studio>.

1. Resolve the requested release or, by default, `main` once to a full immutable Git commit. Obtain an exact temporary checkout/archive. Use the same commit for this guide, source reads and [config/install-sources.json](config/install-sources.json).
2. Fetch every declared file, including binary assets and pinned source archives. Verify the complete path set and SHA-256 hashes. Inspect [scripts/install_codex.py](scripts/install_codex.py) before execution. Python 3 is required; the helper uses only the standard library and makes no network requests.
3. Keep all 37 modules, references, templates, shared resources, source bundles and the logo together. A generic installer copying one specialist folder breaks cross-folder dependencies.

## 3. Resolve destinations and existing content

1. Follow the observed host's actual skill-installation rules. OpenAI documents repository `.agents/skills` and user `~/.agents/skills`; managed installers may use other destinations. Do not assume a path merely from the client name.
2. Inspect every active scope for an existing Studio plugin, native entry or overlapping Workflow Kit skills. The helper checks only its selected destination. For existing, changed, partial or ambiguous content, follow [CODEX_UPDATE.md](CODEX_UPDATE.md); preserve personal edits and avoid duplicates.
3. Select a persistent bundle directory outside **every** active skill-discovery root. Do not place the bundle in a user's project unless that scope was requested. A transient checkout is preparation, not a persistent installation destination.
4. Show the resolved native-entry and bundle destinations, then proceed under the existing installation authorization. Ask only about material unresolved scope or conflicts.

## 4. Install one entry and verify

The helper creates one native skill named `framecore-work-creative-studio` backed by the complete bundle outside skill discovery. Codex reads the original orchestrator and specialists from their canonical locations; the nested modules remain supporting instructions, not separately installed personal skills. This preserves relative references and avoids a second orchestrator.

The assistant fills these placeholders with verified absolute paths and the same full source commit. The user does not need to run the commands:

```sh
python3 scripts/install_codex.py plan --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
python3 scripts/install_codex.py install --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
python3 scripts/install_codex.py verify --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
```

1. Run `plan`, inspect the destinations and source checks, then run `install` and `verify` sequentially.
2. The helper repeats inventory checks, rejects symlinks, unsafe overlaps, partial installations and conflicts, saves a receipt next to the entry and verifies every bundle file. A byte-identical repeat reports read-only `already_up_to_date`. Changed source or personal edits require the update guide.
3. On a copy failure, inspect the actual entry, bundle and receipt before recovery. Report partial state; never blindly delete or overwrite an existing installation.
4. Report saved-file verification separately from actual host discovery/invocation. If activation is unobserved, say so; a new turn or refreshing the skills view may be needed. Check an ordinary Studio invocation when the host permits it, preserving the full canonical welcome contract.

This installs the same Studio knowledge through a local native entry. It does not install the hosted ChatGPT UI, a provider, a persistent agent roster or unrelated project configuration, and it does not synchronize history, preferences or connections.

## 5. Final check of the required tools

The installation ends with the [complete runtime check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#final-check-at-installation). It checks all 59 components in `runtime-tools.json`, including isolated interpreters, models, CLI tools and motion libraries. Work's reported versions are references, not proof of another host or mandatory downgrades.

1. Run `python3 <plugin>/skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host codex --json` from the saved bundle in the actual target environment. Supply additional `--python-env` or `--node-root` paths for installations outside discovery.
2. Show confirmed tools and the concrete missing/broken/Unknown list in the user's language. Before installation, state which tools will be installed, their purpose, target environments and download/admin requirements. Reuse authorization that already covers that plan; otherwise ask once for that concrete scope. A check alone authorizes no installation.
3. Preserve working versions and locks. Install only the disclosed missing components with compatible OS/architecture/Python environments where authorized and supported, then rerun the full check. `pass` confirms installation evidence. `fail`, `limited` or `unknown_host` leaves an explicit incomplete setup; `limited` does not mean Work/Claude is incapable of installation. Without execution, report Unknown rather than simulated success.

Plugin saving, tool installation and end-to-end creative behavior are separate results. No providers, generation, client-asset upload or publication is included in tool setup.

## First recommended companion: Superpowers

Before providers or other add-ons, follow [first companion setup](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#first-companion-setup). Check whether Superpowers is already readable. Otherwise recommend it once: it supports requirements, technical plans, debugging, code review and verification while Studio keeps creative direction, boards and production ownership. The user installs it separately through the actual host Plugins/Marketplace interface; use the registry's host-specific manual steps. The upstream identity is obra/superpowers, Jesse Vincent / Prime Radiant. An official catalog listing does not mean the platform authored it.

Skipping, declining, unavailable catalog access or unverified activation leaves Studio usable. Do not install automatically, clone as a fallback, connect an account, or repeat a known decline/defer. Recheck actual readable skills after installation; saved files or the user's click do not prove activation. Preserve choices on ordinary updates. Catalog/ZIP installations can run the host's setup action where available, or explicitly ask Studio to configure its companion support. This setup path is separate from the complete bare-name welcome.

## Second recommended companion: Earshot Audio

After Superpowers, [first companion setup](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#first-companion-setup) offers once the sound companion `earshot-audio` (folder `plugins/earshot-audio` in this repository; Earshot 0.4.0 by Leon Lin, MIT): local listening and measuring, sound effects on cue frames and soundtracks from licensed recordings. Skip the offer when `earshot-audio:earshot` is already readable; Studio works without it.

1. Install it only when the user accepts. Take the folder from the same pinned commit as Studio and keep it whole: its skill calls `scripts/runtime.py` two folders up and checks the engine against `upstream.json`. Where Codex shows a plugin route for a local folder, add `plugins/earshot-audio` (it carries `.codex-plugin/plugin.json`); this route is not yet tested here, so check that the skill is readable afterwards.
2. Without that route, install the same pinned engine through the registry: `python3 <persistent-bundle-dir>/skills/workflow-orchestrator/assets/extensions/extensions.py show earshot --host codex`, then its plan, install and verify steps. Studio's sound routes call that engine.
3. Installing the plugin writes no engine. `python3 <earshot-audio>/scripts/runtime.py status --json` reports readiness; `install --tier light|full --yes` and `fetch-models --yes` run only after the user agrees, from the pinned commit with every file checked. Nothing is uploaded; its `llm` and `mcp` commands are refused.
4. Remove: the host's plugin controls or delete the copied folder, and `~/.framecore-studio/extensions/earshot` if the user wants the engine gone.

## 6. Offer optional providers after installation

Then read the bundled [provider setup guide](plugins/framecore-work-creative-studio/docs/provider-setup-guide.md) and [setup method](plugins/framecore-work-creative-studio/skills/tool-routing-cost/references/provider-setup.md). Offer one optional question about existing accounts, additional tools, a setup guide or skipping setup. Match the actual host and distinguish native apps from API/MCP/CLI access and billing.

Installation does not connect providers, modify unrelated settings, generate media, spend credits, upload client assets or publish anything. Skipping provider setup leaves the Studio installation complete. On updates, preserve private preferences and do not repeat onboarding unless requested or materially needed.

## 7. Offer recommended extensions (optional)

After the providers question, Studio may offer its [recommended extensions](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md): outside repositories the owner reviewed as engines or knowledge. Run `python3 <persistent-bundle-dir>/skills/workflow-orchestrator/assets/extensions/extensions.py list --host codex` and ask one optional question. Install one only when the user explicitly asks, with its pinned dry-run plan first, then its install and verify commands, and a restart. Skipping leaves the installation complete.

## References

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills).
- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins).
- [OpenAI: Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins).
- [Pinned Workflow Kit installation pattern](https://github.com/FrameCoreWorks/framecore-works-codex-chatgpt-workflow-kit/tree/55c8bf19962c7bf7fb43648637ee433d990eb2a9).

The mechanism and invocation references were checked on 2026-09-29. Use the observed host's actual installation rules and preserve the complete Studio bundle.
