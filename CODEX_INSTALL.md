# Install Creative Studio in Codex

In **Codex**, use `$plugin-creator` and select the matching available skill from completion, then paste the complete prompt below. ChatGPT Work uses `@plugin-creator`; do not assume that the same prefix applies to Codex. Confirm the capability is available rather than treating copied text as proof of activation.

Plugin Creator assists with package checks here. The actual installation remains the native source route below. If Plugin Creator is not available in this host, omit only the invocation line and use the same request; the installer does not require that capability. Do not claim that a connector was enabled.

```text
$plugin-creator

Install FrameCore Works Creative Studio from:
https://github.com/FrameCoreWorks/framecore-works-creative-studio

Use Plugin Creator for package checks when available. Follow the native source-install route
below; do not create a hosted plugin copy or register a plugin catalog. Report unavailable capabilities.
Read CODEX_INSTALL.md and config/install-sources.json. Resolve main once to a full commit and use
that immutable source throughout. Follow this host's actual skill installation rules and inspect
scripts/install_codex.py before execution.

Install one native Creative Studio entry backed by the complete, verified Studio bundle.
Keep all 37 modules and shared resources together. Resolve and show the actual native skills
location and a persistent bundle directory outside every active skill discovery root.
This request authorizes the stated installation; do not repeat approval for unchanged scope.
Check existing Studio plugins, native entries and overlapping Workflow Kit skills in all active
scopes. For existing content use CODEX_UPDATE.md; do not duplicate or overwrite personal changes.

Run plan, install and verify with the same full source commit. Do not copy isolated specialist
folders or add a second orchestrator. Continue in my language. Report saved-file verification
separately from observed host activation. Do not modify unrelated configuration, connect providers,
generate media, upload client assets or publish anything.
```

## Complete bundle and native entry

Studio modules link to sibling skills, shared contracts and pinned sources. A generic skill installer
copying one specialist folder would break these dependencies.

The supplied local helper creates one native skill named `framecore-work-creative-studio`, pointing
to the complete bundle stored **outside skill discovery**. Codex reads the existing orchestrator and
specialists from their original locations. All 37 canonical modules and relative links stay intact.
The modules are supporting instructions, not separately installed personal skills. No provider,
persistent agent roster or project configuration is installed.

This is the same Studio knowledge through a local native entry, not the hosted ChatGPT UI.
Installation does not synchronize history, preferences or provider connections.

## Preflight

1. Resolve main or the requested release to one full commit. Obtain an exact temporary checkout/archive. Read this guide, the inventory and helper from that source.
2. Resolve actual host rules and skill locations. OpenAI documents repository `.agents/skills` and user `~/.agents/skills`; some managed installers use other destinations. Use the observed host location. ChatGPT Work uses CHATGPT_INSTALL.md, not this local helper.
3. Inspect every active scope for an existing Studio entry/plugin or overlapping module identities. The helper checks its selected destination only; the assistant must check other scopes. Existing or ambiguous content routes to [CODEX_UPDATE.md](CODEX_UPDATE.md).
4. Select an empty persistent bundle directory outside **all** discovery roots, such as an application-data folder. Do not write into a user's project unless that scope was requested.
5. Verify the exact source path set and SHA-256 inventory. The helper repeats this check and rejects symlinks, unsafe overlap, partial installations and conflicts.
6. Show native-entry and bundle destinations, then reuse the explicit installation request as authorization. Ask only about unresolved scope/conflicts.

## Install and verify

The assistant fills the placeholders with verified absolute paths. The user need not run commands:

```sh
python3 scripts/install_codex.py plan --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
python3 scripts/install_codex.py install --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
python3 scripts/install_codex.py verify --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
```

Python 3 is required. The helper uses only the standard library, makes no network requests and changes
no global configuration. It saves a receipt next to the native entry and verifies every bundle file.
A byte-identical repeat is read-only `already_up_to_date`. It is not an updater: changed source,
personal edits or partial state require CODEX_UPDATE.md.

On copy failure inspect the actual entry, bundle and receipt before recovery. Partial state is
reported; no existing directory is overwritten or blindly deleted.

Report file verification separately from actual host discovery/invocation. If activation is unobserved,
say so and suggest a new turn or refreshing the skills view. Start with:

```text
Use $framecore-work-creative-studio. Quick mode: give me three short directions for my brief.
```

Mechanism reference, checked 2026-09-29: [OpenAI, Build skills](https://learn.chatgpt.com/docs/build-skills).
Invocation references, checked 2026-09-29: [OpenAI, Package your plugin](https://developers.openai.com/plugins/build/plugins) explicitly distinguishes `@plugin-creator` in Work from `$plugin-creator` in Codex; [Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins) documents Codex `$` skill mentions. A mention does not grant permissions or connect external accounts.
The Work/Codex source-install pattern comes from
[Workflow Kit](https://github.com/FrameCoreWorks/framecore-works-codex-chatgpt-workflow-kit/tree/55c8bf19962c7bf7fb43648637ee433d990eb2a9).
Studio keeps its complete linked bundle rather than copying independent skills.
