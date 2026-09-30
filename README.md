# FrameCore Works Creative Studio

![FrameCore Works Creative Studio](assets/creative-studio-banner.png)

Source version: **1.2.0**. [Repository](https://github.com/FrameCoreWorks/framecore-works-creative-studio) · [Installation](INSTALL.md) · [Release status](RELEASE_STATUS.md).

Creative Studio supports creative direction and production planning across image, video, audio and text. Work can begin with a brief, a product photo, a character reference, an existing clip, a script or a concrete correction.

## Learning or creation

Choose **Tryb nauki** for a personal learning plan, short lessons, exercises and feedback, or **Tryb tworzenia** to produce a project. A clear request enters the appropriate mode directly. Quick/Deep remains a separate pace preference. Learning covers the existing creative domains, offers exercises without rendering, and uses a portable progress card when persistent storage is unavailable. See [learning mode and limits](plugins/framecore-work-creative-studio/docs/learning-mode.md).

## What it includes

- Quick mode: concise creative directions before detailed production work.
- Deep mode: collaborative development from research and concept through references, storyboard, prompts and editing plans.
- Product and character continuity, realistic reference capture and precise reference sheets.
- Static Graphic Design Creator methods for composition, typography, exact copy and graphic design.
- Music, voice and sound planning in relation to pictures, or picture planning around existing audio.
- Asset records, revisions, scoped preferences and portable handoffs between environments.
- Consistent skill display names, with a [standard for future additions](plugins/framecore-work-creative-studio/docs/skill-naming.md).
- 37 canonical skill entrypoints: 35 specialist routes, the orchestrator and a retained audio compatibility alias.

The package supplies instructions, knowledge, templates and local verification helpers. Generation, media inspection and editing require the user's available tools and authorization. No credentials, paid-provider account, persistent memory service or automatic cross-environment synchronization is bundled.

## Install through ChatGPT Work or Codex

Use the prompt for your environment. The assistant reads the exact source and performs the supported installation. You do not need to add a registry or run installation commands yourself.

### ChatGPT Work

Open **Work**, type `@`, search for **Plugin Creator**, and select it from the menu. Paste the prompt below with that selection attached. If pasting leaves `@plugin-creator` as plain text, select Plugin Creator through the menu before sending; the text alone is not proof that its tools are available.

```text
@plugin-creator

Use Plugin Creator to install my private FrameCore Works Creative Studio from:
https://github.com/FrameCoreWorks/framecore-works-creative-studio
Read CHATGPT_INSTALL.md and config/install-sources.json first. Pin main to one commit and verify
all declared files. Install the complete 37-module bundle with its shared resources and logo.
If my copy already exists, follow CHATGPT_UPDATE.md and update that same entry without duplicating
it or overwriting conflicting personal changes. Use the actual save workflow and verify the result.
This request authorizes installation. Continue in my language. Do not connect providers or publish
my copy publicly. If saving is unavailable, explain the concrete blocker instead of claiming success.

After the Studio save succeeds, read the bundled docs/provider-setup-guide.md and
skills/tool-routing-cost/references/provider-setup.md. Offer one optional question about additional
tools, existing accounts or skipping setup. Match the actual host and distinguish native apps from
API/MCP/CLI and their billing. Do not connect a provider or spend credits from this install request.
```

### Codex

In **Codex**, use `$plugin-creator` and select the available matching skill from completion. Paste the prompt below. This is the documented Codex invocation, while Work uses `@plugin-creator`. If this Codex host does not expose Plugin Creator, omit only the invocation line and use the same native installation request; the local installer does not depend on Plugin Creator.

```text
$plugin-creator

Install FrameCore Works Creative Studio from:
https://github.com/FrameCoreWorks/framecore-works-creative-studio
Use Plugin Creator for package checks when available. Follow the native installation below;
do not create a hosted plugin copy or register a plugin catalog. Report unavailable capabilities.
Read CODEX_INSTALL.md and config/install-sources.json first. Pin main to one full commit.
Inspect the local installer, resolve and show the actual native skills location and persistent
bundle directory, then run plan, install and verify. Keep the complete 37-module bundle together
outside skill discovery and install its native Studio entry. This request authorizes installation.
Check existing entries across scopes; follow CODEX_UPDATE.md for conflicts or updates rather than
duplicating or overwriting personal changes. Continue in my language. Do not connect providers,
change unrelated configuration or publish anything. Report actual saved-file verification and
whether host activation was observed.

After the Studio save succeeds, read the bundled docs/provider-setup-guide.md and
skills/tool-routing-cost/references/provider-setup.md. Offer one optional question about additional
tools, existing accounts or skipping setup. Match the actual host and distinguish native apps from
API/MCP/CLI and their billing. Do not connect a provider or spend credits from this install request.
```

[Installation details](INSTALL.md) · [Updates](UPDATE.md) · [Full Studio documentation](plugins/framecore-work-creative-studio/README.md).
Invocation syntax checked on 2026-09-29 against [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins) and [ChatGPT's Plugin Creator selection steps](https://learn.chatgpt.com/docs/build-plugins).
ChatGPT Work creates the user's own private plugin. Codex installs the same Studio knowledge through a native local entry. Availability of actual image, video, audio and research tools depends on the user's environment.

## Optional creative tools

Read the [provider setup guide](plugins/framecore-work-creative-studio/docs/provider-setup-guide.md) for a dated catalog of creative apps and host-specific API/MCP/CLI routes. Studio offers one optional choice after installation; no provider is required. Higgsfield consumer-account access and Open Higgsfield API billing are separate. Availability, account authorization and permission to generate are checked independently.

## Repository layout

| Path | Purpose |
|---|---|
| `CHATGPT_INSTALL.md`, `CODEX_INSTALL.md` | Direct source installation prompts and contracts |
| `CHATGPT_UPDATE.md`, `CODEX_UPDATE.md` | Existing-entry updates preserving user changes |
| `config/install-sources.json` | Complete plugin file inventory with SHA-256 hashes |
| `scripts/install_codex.py` | Native Codex entry and intact backing bundle |
| `plugins/framecore-work-creative-studio/` | Canonical portable plugin and compatibility manifest |
| `plugins/framecore-work-creative-studio/skills/` | Active skill entrypoints and supporting material |
| `plugins/framecore-work-creative-studio/integrations/` | Pinned source bundles and provenance |
| `plugins/framecore-work-creative-studio/docs/` | Scope, source mapping and verification history |
| `scripts/package_release.py` | Local ZIP packaging and SHA-256 inventories |
| `LICENSE_STATUS.md` | Approved licensing scope |

## Verify and package

Run from the repository root with Node.js and Python 3 available:

```sh
node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs
python3 scripts/build_install_manifest.py
python3 scripts/package_release.py
```

The packager runs structural validation first and writes a plugin ZIP, a complete repository ZIP and their SHA-256 inventories into `dist/`. It makes no network requests, installs nothing and does not publish a release. It excludes Git internals and local build outputs.

Current evidence and unverified behavior are recorded in [VERIFICATION.md](VERIFICATION.md). Planned evaluations are not reported as passed tests.

## Licensing

FrameCore Works original code, instructions and documentation are licensed under [Apache-2.0](LICENSE). Both pinned upstream bundles retain Apache-2.0 and their notices. See [licensing scope](LICENSE_STATUS.md) and [NOTICE](NOTICE).
