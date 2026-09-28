# Installation

Version: **1.0.0**. Use the published `v1.0.0` tag for the pinned installation below. This document is installation guidance, not a record of installation in your environment.

## Codex and ChatGPT desktop marketplace

This repository contains `.agents/plugins/marketplace.json`, pointing to `./plugins/framecore-work-creative-studio`.

Add the pinned repository source:

```sh
codex plugin marketplace add FrameCoreWorks/framecore-works-creative-studio --ref v1.0.0
codex plugin marketplace list
```

Alternatively, from an extracted repository directory:

```sh
codex plugin marketplace add .
```

In a supported ChatGPT desktop client, restart the app, open the Plugins Directory, select **FrameCore Works Creative Studio**, and install the plugin. Inspect the displayed version. Connecting provider accounts is a separate user action.

Source: [OpenAI, Package your plugin](https://developers.openai.com/plugins/build/plugins), read 2026-09-28. Marketplace support varies by surface; adding a source is not evidence that installation succeeded.

## ChatGPT web and mobile

GitHub publication does not itself create a public Plugins Directory listing. A universal GitHub-URL installer for every web/mobile account is **Unknown**. Use an installation/import option actually provided by that account, or an accessible published directory listing. A private owner-only plugin link is not advertised as a public install link.

If Plugin Creator is available and creating a personal copy is explicitly requested, supply the packaged plugin ZIP through its supported creation workflow. Check for an existing installation first. Creation of a copy is separate from synchronizing or updating the original owner's plugin.

## First use and tool connections

Give a brief in your own language. Choose quick ideas or deeper development as needed. Reference files should be attached using the active host's supported mechanism.

Fal, image/video generators, audio services, editors and MCP/API integrations are optional tools supplied by the user. The package contains no authentication material. A prompt request does not authorize paid generation, uploading client files or publication.

Keep the complete plugin directory together. Its skills refer to one another and to shared resources; copying one skill folder alone is not the supported installation path for this package.
