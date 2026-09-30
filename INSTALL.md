# Installation

Version: **1.2.10**. Install from this repository through the assistant in your target environment.

| Environment | Copy-paste guide | Result |
|---|---|---|
| ChatGPT Work with Plugin Creator | [CHATGPT_INSTALL.md](CHATGPT_INSTALL.md) | Your own private Creative Studio plugin |
| Codex with filesystem access | [CODEX_INSTALL.md](CODEX_INSTALL.md) | Native Studio skill with the complete local knowledge bundle |

The copyable prompts include the host-specific invocation: `@plugin-creator` in **ChatGPT Work** and `$plugin-creator` in **Codex**. In Work, type `@`, search for **Plugin Creator**, and select it from the menu. In Codex, select the matching available skill from completion. Pasted plain text is not proof of an active selection or available tools. Plugin Creator is required for Work's hosted save; Codex's native helper can operate without it, as described in its guide.

Use the matching guide. Ordinary Chat without creation/save capabilities cannot install the package.
Resolve the requested release, or latest main, to one full Git commit and read all source from that
commit. [config/install-sources.json](config/install-sources.json) declares every plugin file and SHA-256.
A GitHub URL, approval or downloaded ZIP alone is not installation.

All 37 modules, references, templates, original sources and logo stay together. Individual skill
folders have cross-folder dependencies and must not be installed in isolation. Existing installations
follow [UPDATE.md](UPDATE.md); preserve personal edits and do not create duplicates.

The owner's private hosted-plugin link is not a public installation link. Other users create their own
private copies from these public sources. Repository updates do not automatically update those copies.

After installation, give an ordinary brief in your language and choose quick ideas or deeper work.
Providers, credentials and connections belong to each user's environment. Installation does not
authorize paid generation, client-asset uploads or publication.

After installation, optionally choose additional tools using the [provider setup guide](plugins/framecore-work-creative-studio/docs/provider-setup-guide.md). Studio is complete without those integrations.
