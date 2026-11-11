# Anthropic workspace source intake — three repositories

Read-only intake, 2026-11-11; retrieval completed around09:44 UTC. **Purpose: give Claude candidates to assess across the whole workspace, not decide ADD/NO ADD or install anything.** This is separate from DR-01–06 and does not expand the nine-source Creative Studio research queue.

Only this document was created. No repositories were cloned, archives imported, code/hooks installed or run, accounts connected, private materials read, or model/provider calls made. Public GitHub source was fetched through the GitHub connector. No Shared or Claude-owned file was changed.

## Source pins

| Repository | HEAD observed | Commit date reported by connector (UTC) | Intake surface |
|---|---|---|---|
| anthropics/claude-plugins-official | [43fd1f9db0941b2b83cb62268e35970d4a67c202](https://github.com/anthropics/claude-plugins-official/commit/43fd1f9db0941b2b83cb62268e35970d4a67c202) | 2026-11-10 22:01:16 | Code-oriented marketplace plus local and externally sourced plugins |
| anthropics/knowledge-work-plugins | [877a617b435ee2edfb002d9a3703c0a1a03aa1ba](https://github.com/anthropics/knowledge-work-plugins/commit/877a617b435ee2edfb002d9a3703c0a1a03aa1ba) | 2026-11-11 03:16:54 | Cowork-oriented role/workflow plugins, also documented for Code |
| anthropics/skills | [2c5958ecac7cee2b583967a2c4981d0f4a75c579](https://github.com/anthropics/skills/commit/2c5958ecac7cee2b583967a2c4981d0f4a75c579) | 2026-11-06 22:32:28 | Individual skill folders and curated skill-bundle manifests |

These pins identify source reviewed, not installed host versions. External marketplace entries have their own source pins; the marketplace commit alone is not their complete code/dependency audit.

## Ready-to-insert English subsection for handover section11

### Three additional sources for Claude's workspace-wide assessment

Please assess [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/README.md), [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435ee2edfb002d9a3703c0a1a03aa1ba/README.md), and [anthropics/skills](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/README.md) for the **whole Claude workspace**, not only Creative Studio. The first is a Claude Code marketplace; the second supplies Cowork-oriented workplace workflows with a Code route; the third supplies smaller task skills and examples. Treat them as sources to inspect, select, adapt or reject—not a request to install all three.

For useful candidates, identify the actual supported route in Chat/web, mobile, Desktop chat, Code and Cowork separately. Do not infer that a Code hook, local script or MCP configuration works in an ordinary chat merely because all products carry the Claude name. Check current account/plan, organizational permissions, connected tools, filesystem/runtime access and duplication with existing capabilities.

Prefer concise discovery metadata and task-triggered loading of instructions/references. A skill catalog is not free context: metadata, activated bodies, connector schemas/results and background hooks can add cost. Measure practical benefit and task quality rather than promising a token-saving multiplier. The skills author's [progressive-disclosure pattern](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/SKILL.md#L86) is a useful design input, not a measured saving for this workspace.

Return a small shortlist with use case, host, source pin, license, dependencies, overlap, proposed adaptation, files/settings/accounts affected, and a bounded validation plan. Preserve existing user rules, authoritative memory and tool ownership. Check licenses at the selected component level: document skills at the reviewed November6 revision now carry Apache2.0; third-party dependencies retain their own terms, and doc-coauthoring's license remains unclear in this intake.

No ADD/NO ADD decision is predetermined. No installation, account connection, paid run, background hook activation or automatic settings change is authorized by this addition. Keep this workspace assessment separate from DR-01–06 and the existing nine-source Studio queue.

## Differences that matter

| Source | Observed purpose and packaging | What Claude must assess |
|---|---|---|
| Official plugin directory | [README](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/README.md) distinguishes Anthropic-maintained plugins from external partners. [Manifest](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/.claude-plugin/marketplace.json) has317 entries:54 local-path entries and263 external-source objects. | Select individual capabilities. Inspect external pinned source and its license; directory membership does not attest every included server or dependency. Counts are inventory, not review coverage. |
| Knowledge-work plugins | [README](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435ee2edfb002d9a3703c0a1a03aa1ba/README.md) describes role-specific workflows, skills and connectors for Cowork/Code. [Manifest](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435ee2edfb002d9a3703c0a1a03aa1ba/.claude-plugin/marketplace.json) now has123 entries:22 local and101 external-source objects. | Avoid treating the README's older11-plugin description as current scope. Determine whether a workflow is useful without connectors and which external actions it could perform. |
| Skills | [Manifest](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/.claude-plugin/marketplace.json) declares five bundles: document-skills, example-skills, claude-api, academy-guide and discernment-nudge. The skills directory has19 immediate skill folders. | Reuse/adapt a selected contract rather than preload the entire corpus. Scripts and references may assume an execution environment unavailable in the chosen host. |

**Host boundary:** repository documentation establishes Code installation routes, Cowork intent for knowledge-work, and Claude.ai/API skill usage guidance for skills. The skills README's statement about paid-plan availability is an author statement, not an entitlement check for this user. No mobile, current Desktop-chat, browser-chat or organization-policy compatibility was tested. Claude should validate each actual surface and distinguish direct installation, built-in availability, adapted instructions and unsupported execution.

## Representative contracts and concrete caveats

- **Commands versus skills:** the official [example plugin](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/plugins/example-plugin/README.md) describes skill-based model/user invocation and treats commands/ as a legacy layout. Its [manifest](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/plugins/example-plugin/.claude-plugin/plugin.json) is an example contract, not an installed component.
- **A plugin may execute during a session:** [security-guidance hooks](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/plugins/security-guidance/hooks/hooks.json) include SessionStart, prompt/tool and Stop triggers. Targeted reading of [ensure_agent_sdk.py](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/plugins/security-guidance/hooks/ensure_agent_sdk.py) shows a conditional SDK bootstrap using venv/pip. This refutes a blanket assumption that all entries are passive prompt files. The whole security implementation, metrics pipeline and model billing were not audited.
- **Dependencies can float:** the examined [Playwright MCP config](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/external_plugins/playwright/.mcp.json) launches npx with @playwright/mcp@latest. A pinned marketplace snapshot therefore does not guarantee pinned runtime dependencies.
- **Connector descriptions need config checking:** [productivity CONNECTORS.md](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435ee2edfb002d9a3703c0a1a03aa1ba/productivity/CONNECTORS.md) and its README name Microsoft365. The actual [MCP config](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435ee2edfb002d9a3703c0a1a03aa1ba/productivity/.mcp.json) has Slack/Notion/task services, but no Microsoft365 entry and empty Gmail/Google Calendar URLs. Do not promise ready-to-use email/calendar wiring. Endpoint declarations do not authenticate an account; applicable OAuth, account access and admin consent must be established separately.
- **Memory ownership needs adaptation:** [memory-management](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435ee2edfb002d9a3703c0a1a03aa1ba/productivity/skills/memory-management/SKILL.md) uses CLAUDE.md plus a memory/ tree and proposes scanning connected workplace sources to seed it. That pattern must not overwrite existing global/project rules, create competing authoritative memory, or treat this intake as permission to scan mail/chat. Its percentage/line-count goals are design suggestions, not measured workspace results.
- **Document tooling assumes tools:** [DOCX SKILL.md](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/docx/SKILL.md) names npm docx, pandoc, LibreOffice and Poppler and calls for rendered review. Its preinstalled-tool statements describe the intended environment; they do not prove availability on another host. Reuse existing local installations before proposing dependencies.

## License intake, including the November6 change

**Official directory:** [root LICENSE](https://github.com/anthropics/claude-plugins-official/blob/43fd1f9db0941b2b83cb62268e35970d4a67c202/LICENSE) contains Apache2.0. The README directs readers to each plugin's relevant license. The263 external-source entries were not individually license-audited; do not extend the root license to them.

**Knowledge-work:** [root LICENSE](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435ee2edfb002d9a3703c0a1a03aa1ba/LICENSE) contains Apache2.0 text plus an unrelated nonstandard trailing passage. The representative [productivity/LICENSE](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435ee2edfb002d9a3703c0a1a03aa1ba/productivity/LICENSE) contains the standard Apache2.0 form without that trailing passage. This is a source-text observation, not a legal conclusion. Verify the chosen package and its external dependencies before copying or redistribution.

**Skills:** no root LICENSE was present in the inspected root listing; a direct LICENSE fetch returned404. Individual LICENSE.txt files for the following18 folders identify Apache2.0:
academy-guide; algorithmic-art; brand-guidelines; canvas-design; claude-api; discernment-nudge; docx; frontend-design; internal-comms; mcp-builder; pdf; pptx; skill-creator; slack-gif-creator; theme-factory; web-artifacts-builder; webapp-testing; xlsx.

The four office licenses were inspected individually: [docx](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/docx/LICENSE.txt), [pdf](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/pdf/LICENSE.txt), [pptx](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/pptx/LICENSE.txt), [xlsx](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/xlsx/LICENSE.txt). The pinned commit explicitly changes those to Apache2.0; older descriptions of them as proprietary are stale for this revision.

**Unresolved:** doc-coauthoring's directory contains only SKILL.md; LICENSE.txt fetch returned404 and its inspected frontmatter has no license field. Do not infer a blanket grant from neighboring skills. Its reuse terms need clarification before copying/adaptation.

**Third-party assets:** [THIRD_PARTY_NOTICES.md](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/THIRD_PARTY_NOTICES.md) lists distinct terms including BSD components, a GPLv3 FFmpeg build, Pillow terms and OFL fonts. This intake read notice headings/component identifications, not every dependency's full legal history. Apache skill instructions do not erase dependency/asset notices.

## Token-on-demand assessment

The inspected skill-creator section separates always-discoverable metadata, triggered skill bodies and on-demand resources; it also notes scripts can run without loading their entire source into context. That supports selective loading as a design pattern. It does **not** establish zero overhead, availability in every host, identical loading behavior across Chat/Code/Cowork, or a numeric saving. Existing built-in skills may duplicate these examples.

Claude's proposed comparison should report relevance/trigger quality, amount of always-loaded material, activated reference volume, connector/tool output volume, background work and actual task outcomes. Avoid injecting large catalogs into global instructions. Do not modify global instructions, install a plugin or run a benchmark merely to prepare this assessment.

## Access and inspection scope

- Fetched all three root READMEs, marketplace JSONs and root directory inventories; fetched the two present root licenses and inspected declarations/trailers. Root skills LICENSE absence was checked.
- Inventoried official plugins/external_plugins directories; knowledge-work root, productivity/data directories and productivity skill directory; skills root and19 skill folders.
- Representative contracts read: official example README/manifest, security hook JSON and selected bootstrap code sections; Playwright MCP config; productivity README/manifest/MCP/connector notes/memory skill; DOCX skill; skill-creator progressive disclosure section.
- Retrieved18 per-skill license texts and checked declarations/extent; separately verified the doc-coauthoring directory and license absence. Third-party notices received targeted heading/component inspection.
- No exhaustive317/123-plugin code review, external-source traversal, full hook security review, dependency validation, account check, install or runtime test. No third-party source archive or raw manual corpus was copied into the workspace.
