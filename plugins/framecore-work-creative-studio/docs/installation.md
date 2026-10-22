# Direct source installation

Install the complete Studio through the assistant in the target environment.

- **ChatGPT Work:** use Plugin Creator to create the user's own private copy from the complete canonical plugin bundle. Preserve all 37 skill roots, source bundles, assets, interface and starter prompts. Update an existing matching plugin rather than duplicating it.
- **Codex:** install a native Studio entry backed by the complete local bundle. Keep the bundle outside native skill discovery so its nested modules and source mirrors do not become duplicate installed skills. Read modules from their canonical locations to preserve relative references.

The repository supplies complete environment-specific installation procedures and source inventories:

- [ChatGPT Work installation](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CHATGPT_INSTALL.md)
- [Codex installation](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CODEX_INSTALL.md)
- [ChatGPT Work updates](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CHATGPT_UPDATE.md)
- [Codex updates](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CODEX_UPDATE.md)

Resolve the requested ref to one full commit before reading guides, inventory and source. Fetch every declared file, including binaries, and verify hashes. Do not install isolated specialist folders or assume that a source read is an installation.

Follow the active host's real save mechanism and existing authorization. Report a concrete unavailable capability without simulating success. After saving, read back the actual result and distinguish file verification from host discovery and behavior. Preserve personal changes on updates and inspect ambiguous saves before retrying.

The author's private plugin link is not a public installation link. Public GitHub source permits creating an independent personal copy; it does not synchronize accounts, private history, provider credentials or later changes. Installation does not activate providers or authorize media generation, private asset uploads or public publication.

## First configuration and companion support

Run the host's plugin setup action after installing from a catalog or ZIP, or ask Studio to configure itself. Both OpenAI manifests point setup to the existing orchestrator; Claude uses the explicit setup request and its actual plugin interface. Follow [first companion setup](../skills/workflow-orchestrator/references/extensions.md#first-companion-setup) before providers or other add-ons. Recommend separately installed Superpowers first when missing and not declined/deferred, explain its technical support, then let the user install it through their host catalog. Already readable skills skip the offer. Missing support does not block Studio; actual activation needs a skill read. The complete bare-name welcome remains unchanged.

## Optional provider setup after saving

After a fresh installation is saved and verified, offer one optional tool-selection question using [the setup method](../skills/tool-routing-cost/references/provider-setup.md). The user may choose existing accounts, request a setup guide, or skip. Read [the user guide](provider-setup-guide.md) for ChatGPT Chat/Work, supported Codex plugins, custom MCP, CLI and API distinctions. Provider setup does not authorize connecting services, importing client files or spending credits. Tool installation follows the separately disclosed plan and its authorization below. On updates preserve private preferences and do not repeat onboarding unless requested or materially needed.

## Required tool inventory at installation and every update

Run the [complete environment check](../skills/workflow-orchestrator/assets/environment-check/README.md) from the saved package with `--final` for installation or `--update` after every update and the actual host. The 59-component runtime catalog includes engines, libraries, models, browser builds and separate Python environments. Report detected versions and evidence; the owner-reported Work versions are references, not a cross-host guarantee. Disclose which missing tools will be installed, where and with what downloads/permissions before executing an authorized plan. Preserve working versions and locks, then rerun. If execution or installation is unavailable, state Unknown or the concrete blocker. A saved plugin does not prove tool availability or render behavior.
