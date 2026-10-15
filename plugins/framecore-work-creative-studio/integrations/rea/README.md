# REA: what Studio took and what stays an extension

Source: [morluto / rea](https://github.com/morluto/rea/tree/5e30969cc5f1255d44ec7a1f1ca8dbac0af5e7c4) ("Reverse Engineer Anything"), npm package `rea-agents` 6.5.0, reviewed at commit `5e30969cc5f1255d44ec7a1f1ca8dbac0af5e7c4` on 2026-10-15 at the owner's request. [The original licence](LICENSE) (MIT) retains Copyright (c) 2026 morluto. No REA code is vendored or installed with Studio.

REA reverse engineers software: native binaries with Hopper, Ghidra or IDA, JavaScript and Electron apps, .NET, Android, firmware, network captures, and websites through Chrome's DevTools, as an MCP server, a CLI and an agent skill. It is not about images or prompts; Studio's image reconstruction is a separate method in Image Prompt Architect.

## Decision map

| REA part | Decision | Studio destination or reason |
| --- | --- | --- |
| "See a feature you like, understand how it works, build your own" | Adapt for motion | The [web motion probe](../../skills/hyperframes-workflow/assets/web-motion-probe/README.md) reads a page's motion libraries, tweens and CSS animations; Studio rebuilds the technique, never the code |
| Findings with evidence and unknowns | Adopt in the probe | Every report says what it could not see (a bundled GSAP, canvas or WebGL motion) |
| Website observation through DevTools (`inspect-web-page`, `analyze-web-bundle`) | Not adopted | In the review it refused a public page loading third-party resources and listed a local page's scripts without naming the motion library; the probe reads the library's own state instead |
| Binaries, Electron, .NET, Android, firmware, network captures | Extension | Outside Studio's creative scope; installable natively as a [recommended extension](../../skills/workflow-orchestrator/references/extensions.md) when the user wants it |
| Its MCP server, skill and setup (`setup`, `doctor`, `uninstall`) | Extension, pinned | The registry entry uses REA's own installer at 6.5.0, dry run first, only on an explicit request, in Codex, Claude Code or the Claude desktop app |
| Responsible-use terms (no DRM or licence circumvention, no copying proprietary code or assets) | Adopt | Stated in the registry entry and the probe; Studio learns techniques and builds its own version |

## Evidence

2026-10-15, Linux container, Node.js 22.22: `rea-agents@6.5.0` ran; `setup --dry-run` planned the MCP registration and skill for `claude_code`, `codex` and `claude_desktop` with backups; `doctor` reported the registration missing before setup. REA was not installed into a real host and its MCP tools were not used from an agent session.
