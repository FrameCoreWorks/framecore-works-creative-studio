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

The installation ends with the [final check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#final-check-at-installation). Studio uses one required set of tools (Python with Pillow, NumPy, CairoSVG, imageio-ffmpeg, matplotlib and Manim; FFmpeg with FFprobe; Node.js with npx; Chrome or Chromium; the five starters installed with `npm ci` in the Studio workspace; HyperFrames); the check decides which of them this host can run.

1. Run `python3 <persistent-bundle-dir>/skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host codex` and show the user the result in their language.
2. `fail`: the installation is not complete. Show the printed commands for the user's system (system packages, the Python packages in one virtual environment, the starters copied into `~/.framecore-studio/workspace` with `npm ci`, HyperFrames' own plugin). The user runs them, or asks the assistant to run them in this host; the check itself installs nothing. Then run the final check again.
3. `pass`: the installation is complete. Report the verdict, the host and the workspace path with the installation result.

Installing these tools does not connect providers, generate media, spend credits or publish anything.

## 6. Offer optional providers after installation

Then read the bundled [provider setup guide](plugins/framecore-work-creative-studio/docs/provider-setup-guide.md) and [setup method](plugins/framecore-work-creative-studio/skills/tool-routing-cost/references/provider-setup.md). Offer one optional question about existing accounts, additional tools, a setup guide or skipping setup. Match the actual host and distinguish native apps from API/MCP/CLI access and billing.

Installation does not connect providers, modify unrelated settings, generate media, spend credits, upload client assets or publish anything. Skipping provider setup leaves the Studio installation complete. On updates, preserve private preferences and do not repeat onboarding unless requested or materially needed.

## References

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills).
- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins).
- [OpenAI: Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins).
- [Pinned Workflow Kit installation pattern](https://github.com/FrameCoreWorks/framecore-works-codex-chatgpt-workflow-kit/tree/55c8bf19962c7bf7fb43648637ee433d990eb2a9).

The mechanism and invocation references were checked on 2026-09-29. Use the observed host's actual installation rules and preserve the complete Studio bundle.
