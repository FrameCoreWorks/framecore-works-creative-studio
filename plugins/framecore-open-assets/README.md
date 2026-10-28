# FrameCore Open Assets

A standalone media-sourcing companion for Claude, ChatGPT Work and Codex, using the same portable
package pattern as Earshot Audio. One shared skill and Python runtime, three synchronized manifests,
and one marketplace entry. It also hands source records to Creative Studio, FrameCut or Earshot.

Search official free APIs without signup or keys, inspect each asset's rights, and save a decoded
file with source, creator, licence, attribution, hash and verification evidence. Public provider
requests leave the executing host; no client media is uploaded. There is no remote MCP server,
paid generation, account setup, browser scraping or Openverse fallback.

## Provider coverage

Fourteen executable providers: Wikimedia Commons, The Met, Cleveland, Rijksmuseum (PDM/CC0 images), Library of Congress (dedicated Gottlieb photographs), NASA (photos/video), LibriVox, Finna, Wellcome, ambientCG, PhyloPic, Poly Haven, SMK and SFXMint. Each provider has its own documented module and rights gate. NASA/LibriVox require item/use-specific review; SA requires deliberate acceptance.

AIC, Internet Archive, ccMixter and Gallica remain held. NASA audio is disabled after oversized test samples and no bounded successful delivery. See [provider details](skills/open-assets/references/provider-index.md). There is no arbitrary provider-count cap. Broad music, recorded SFX and contemporary stock footage remain gaps.

## Installation and capabilities

Use the complete host procedure: [Claude](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CLAUDE_INSTALL.md#framecore-open-assets),
[ChatGPT](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CHATGPT_INSTALL.md#framecore-open-assets), or
[Codex](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/CODEX_INSTALL.md#framecore-open-assets). The plugin itself uses Python's standard
library. Image verification also needs Pillow; audio/video verification needs FFmpeg and FFprobe.
Ask before installing missing dependencies. No model downloads are needed.

The skill is readable in compatible clients; execution requires a shell/code tool and permitted
network. An ordinary chat without those capabilities can plan but cannot claim searches/downloads.
Provider verification is local to the actual host/category/runtime and expires after one day.
No Work test proves Claude Code, Claude apps or Codex behavior.

## Developer checks

Run `python3 tests/runtime_test.py` and `python3 tests/package_test.py` from this plugin directory.
The repository's full check also runs both. Tests cover observed API response shapes, rights gates,
provenance tampering, HTTP blocks/cache/budgets, actual image decoding and package discovery.
No test installs upstream software or makes a provider request. Live CLI tests are recorded
separately in the repository verification directory.

Operational examples and complete input/output/error contracts are in the
[Open Assets skill](skills/open-assets/SKILL.md) and [runtime contract](skills/open-assets/references/contract.md).
Do not save downloaded media, runtime state or credentials inside this package or commit them.
