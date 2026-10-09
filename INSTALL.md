# Installation

The complete environment-specific procedures are maintained in these guides:

| Environment | Installation guide | Result |
|---|---|---|
| ChatGPT Work with Plugin Creator | [CHATGPT_INSTALL.md](CHATGPT_INSTALL.md) | Your own private Creative Studio plugin |
| Codex with filesystem access | [CODEX_INSTALL.md](CODEX_INSTALL.md) | One native Studio entry backed by the complete local knowledge bundle |
| Claude Code and the Claude apps | [CLAUDE_INSTALL.md](CLAUDE_INSTALL.md) | The Studio plugin installed from this repository's Claude marketplace |

For an installation request, the assistant reads the guide matching its actual environment and follows that procedure. Host capability checks, source pinning, existing-installation handling, authorization, saving and verification are defined in the selected guide. A repository URL or downloaded archive alone does not establish installation intent or a completed installation.

All 37 modules, references, templates, original sources and the logo stay together. Individual skill folders have cross-folder dependencies and must not be installed in isolation. Existing installations follow [UPDATE.md](UPDATE.md); preserve personal edits and avoid duplicates.

The owner's private hosted-plugin link is not a public installation link. Other users create their own private copies from the public source. Repository updates do not automatically update those copies.

Providers, credentials and connections belong to each user's environment. Studio installation does not authorize paid generation, client-asset uploads or public publication. Optional additional-tool setup is described in the selected guide and [provider setup guide](plugins/framecore-work-creative-studio/docs/provider-setup-guide.md). Studio is complete without those integrations.
