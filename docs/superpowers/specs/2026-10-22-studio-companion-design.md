# Superpowers as Studio's first recommended companion

Status: approved by the owner for implementation and repository-first publication, followed by the existing ChatGPT plugin update. See the [implementation plan](../plans/2026-10-22-studio-companion-implementation.md).

Owner request: 2026-10-22. Change: CW-20261022-01. Baseline: `b92b45b227dc667934c81080afebcdd3c0163b29`, Studio 1.121.0. Working branch: `cw/superpowers-companion-foundation-2026-10-22`.

## Goal and bounded scope

Recommend the separately maintained **Superpowers** plugin first when installing Studio. Explain its value, let the user install it through their host's plugin interface, then use its actually available skills at the appropriate Studio decision points. Studio retains creative ownership; Superpowers supports requirements clarification, engineering plans, implementation, diagnosis, code review and evidence-based completion.

This is a companion integration, not extraction, rewriting or bundling of Superpowers skills. The owner's current request is an explicit exception to the older repository convention of mining every reviewed repository. It also authorizes this separate working branch, superseding main-only for this task. Other repository rules remain in force.

In scope: the approved architecture, installation/first-configuration behavior, ownership coverage, handoff contract, verification and paired publication. The existing native integration has been inspected and is the compatibility baseline. Open Design remains a separate paused work item.

## Evidence informing the design

- Public source is 1.121.0, with 37 skill roots and 1,549 files in the canonical inventory.
- Readback of the existing hosted Studio on 2026-10-22: 1.119.7, 1,595 inventory paths. This is a separate release line, not evidence that the entire hosted package equals an older public tag.
- The hosted package already has `skills/pipeline-core/references/superpowers-native-routing.md`, 12 cases in `evals/native-superpowers-cases.json`, and direct links in Workflow Orchestrator, Pipeline Core, FrameCut, Motion Graphics Workflow, Remotion Video Production and Static Graphic Design Creator. These are the starting compatibility contract. Stored cases are not executed behavior evidence.
- Superpowers is installed and enabled in this ChatGPT Work account. Its 15 skills are visible. `using-superpowers`, `brainstorming`, `using-git-worktrees` and `verification-before-completion` were read for this task. This proves access in this conversation, not in another account, client or fresh session.
- Public orchestrator: 31,918 bytes against a 32,000-byte limit. Hosted orchestrator: 32,391 bytes. Integration must resolve the budget before release; merely appending the hosted paragraph to public source is unsuitable.
- Sources: [upstream Superpowers README](https://github.com/obra/superpowers/blob/main/README.md), retrieved 2026-10-22; [official Claude listing](https://claude.com/marketplace/plugins/superpowers), checked the same day and explicitly offering Claude Code installation; live installed-plugin catalog and scoped hosted readback; [Claude handover](../../handover-claude-code-2026-10-22.md). Upstream documents official Claude Code and Codex marketplace installation. ChatGPT availability here is separately observed; Claude app availability must be checked in that app.

## Architectural choice

| Approach | Effect | Decision |
| --- | --- | --- |
| One shared companion contract, small links from routing and direct technical entry points | One decision policy and one handoff record; covers specialist calls without repeating procedures | Recommended |
| Full Superpowers instructions repeated in every Studio skill | Competing versions, larger discovery budget, duplicate gates | Reject |
| Copy or fork Superpowers into Studio | Another distribution to maintain, no longer the separately installed companion requested | Excluded by owner scope |

Use the existing hosted reference path as the prospective canonical public contract after comparison. Do not create a second parallel adapter or new Studio skill. Reuse Studio's existing owner map, project state, approval records and QA budget. Adding this companion does not create a new owner, agent, renderer, provider, MCP server or hook in Studio.

## Installation recommendation

1. During explicit Studio installation, after identifying the host and before other add-on recommendations, check whether Superpowers is already available.
2. If available and readable, record that observation and skip the installation offer. The owner's current account takes this route.
3. Otherwise show one short recommendation explaining what it improves. Installation is manual by default, through the user's Plugins/Marketplace interface. A Studio installation request alone does not authorize installation of another plugin.
4. The user can install it, defer or decline. Deferral, refusal or unavailable catalog access leaves Studio usable and installation complete. Do not repeat a declined offer in the same project/session; retain that choice only in actually authorized project/profile storage. Do not infer cross-session persistence.
5. After installation, check the current session's catalog and read the relevant skill. If the session has not refreshed, say activation is unverified and use the host's documented refresh/new-conversation route. Do not claim a loaded method merely because the user reports clicking Install.

Suggested Polish copy, adapted to the actual host:

> Pierwszym polecanym dodatkiem do Studio jest Superpowers. Pomaga doprecyzować wymagania, zaplanować prace techniczne, diagnozować błędy oraz sprawdzać kod i wyniki. Studio nadal prowadzi część kreatywną. Możesz zainstalować Superpowers osobno w katalogu pluginów. Jeśli wolisz, kontynuujemy bez niego.

Use the user's language. This belongs to installation/onboarding context, not the protected bare-name welcome or every creative request. Existing installations get the recommendation only in an appropriate explicit installation/update context, with prior choices respected. The complete localized welcome and menu order remain unchanged.

### Host-specific manual routes

| Surface | Preferred route | Evidence and limit |
| --- | --- | --- |
| ChatGPT / ChatGPT Work | Open Plugins, search Superpowers, inspect the matching listing, add/enable it | Listing installed/enabled and skills readable in this Work session; ordinary ChatGPT and all-account availability untested |
| Codex app | Plugins in sidebar, Superpowers in Coding, add through the listing | Documented by upstream; not exercised here |
| Codex terminal CLI | User opens `/plugins`, searches Superpowers, selects Install Plugin | Documented by upstream; do not paste a CLI command into the app as if equivalent |
| Claude Code | Official marketplace listing; in the interactive terminal CLI the documented command is `/plugin install superpowers@claude-plugins-official` | Documented by upstream; use native UI for other Code surfaces, not an unverified slash-command route |
| Claude apps / Cowork | Search the actual Plugins/Marketplace UI for the official listing and follow that surface's installation controls | Not observed here; do not claim that Claude Code commands, availability or activation apply to these apps |

The upstream listing identity is Superpowers from `obra/superpowers` / Jesse Vincent and Prime Radiant. Availability through a platform's official catalog does not mean the platform authored the plugin. Install independently in each host; no account connection or synchronization between hosts is implied.

Do not clone a repository, install individual skill files, modify configuration, add a marketplace or run shell installers as an automatic fallback when a catalog listing is missing. Recheck the host or continue with Studio. A different installation route requires its own user intent.

### Registry compatibility

The current extension registry assumes pinned external repositories and executable installer plans. Its `manual` status currently means adding files by hand. Neither accurately describes this companion's user-driven marketplace installation.

For implementation, extend that existing schema/reader deliberately to represent a `catalog_manual` installation method with host-specific navigation, `recommendation_priority: first`, a dated source review and observed availability. Keep existing extension entries and command behavior compatible. Do not invent fake plan/install commands to satisfy the schema or mislabel file import as catalog installation. The exact schema change belongs in the implementation plan after design approval.

The reviewed upstream revision is provenance, not a promise that a platform catalog serves that exact revision. Resolve the actual installed skills/version at use time. Explain this narrow exception in the maintainer guide and extension route. A companion card may occupy the first installation recommendation without changing the ordering policy of the general reference catalog.

## Dispatch and return contract

For a matching decision, resolve `superpowers:using-superpowers` and the required skill using the host's actual installed catalog/path, read it, then apply the relevant method within current authorization. Names in this document are semantic identities, not hard-coded tool invocations. Never bake in an account plugin ID, cache version or another host's filesystem path.

| Decision | Superpowers support | Return condition |
| --- | --- | --- |
| Material unresolved requirements or new technical architecture | `brainstorming` | Clarified gap and bounded design; reuse the known brief and real approvals |
| Approved direction needs a multi-step coded build | `writing-plans` | Executable plan bound to the approved revision and acceptance criteria |
| Authorized execution of that plan | `executing-plans`; optionally `subagent-driven-development` when selected and supported | Reviewed changes with evidence; no invented delegation |
| Reproducible rendering, timing, layout, font, audio or tooling fault | `systematic-debugging` | Cause supported by evidence, bounded repair, relevant regression check |
| Meaningful deterministic code behavior | `test-driven-development` | A failing behavioral check before the fix and passing regression afterward where execution is available |
| Substantial code review or received technical review | `requesting-code-review` / `receiving-code-review` | Actual findings tied to code and requirements; verify before changing |
| Substantive completion claim | `verification-before-completion` | Current-revision evidence within the existing domain QA pass |
| Independent bounded technical tasks | `dispatching-parallel-agents` | Only with real delegation tools, authorized scope and useful separation |
| Explicit skill/plugin maintenance or Superpowers diagnosis | `writing-skills` / `diagnosing-superpowers` | Scoped maintenance result; not an ordinary creative-production step |
| Authorized repository isolation and branch completion | `using-git-worktrees` / `finishing-a-development-branch` | Follow the user's branch choice and repository rules; media work alone grants no Git permission |

Greetings, status requests, minor copy changes and routine raster edits do not start a software workflow. Creative dissatisfaction first returns to the creative owner; it is not automatically a software defect. Technical methods never replace actual picture, motion or listening review.

Keep one small record in existing Project State, compatible with the hosted reference:

- `decision`, `studio_owner`, `trigger`, `selected_skills`;
- `support_status`: `not_applicable`, `unavailable`, `loaded` or `applied`;
- `artifact_revision`, `acceptance_criteria`, `evidence`, `next_owner`.

Record catalog/skill-read evidence and capability limitations in `evidence`. A failed read is `unavailable` with the observed error; uncertain availability is stated as unknown, not converted into an installed claim. `loaded` means instructions were read; `applied` requires the relevant method and observable result. One task may use several skills, but keep each decision's receipt scoped. Revalidate affected evidence after an artifact revision changes; unchanged accepted parts stay accepted.

The support result always returns to the original Studio owner and checkpoint. No second brief, master timeline, approval chain, automatic sample render or duplicate QA loop. A valid already-given approval is reused; an unseen storyboard or materially changed design is not silently approved. No cyclic handoffs: once the selected support decision is resolved, continue with Studio; only new evidence or a new decision reopens support.

## Coverage of all 37 Studio skills

Every row inherits the shared decision policy. Direct technical entry points also link to it so a specialist invocation cannot bypass routing. Other skills use the central owner/handoff map; no 37-fold boilerplate is needed.

| Existing skill IDs | Ownership and conditional use |
| --- | --- |
| `workflow-orchestrator`, `pipeline-core` | Central dispatch, availability, state and return. Resolve direct specialist calls as well as top-level workflow requests. |
| `hyperframes-workflow`, `remotion-video-production`, `opencut-video-studio`, `static-graphic-design-creator` | Direct links: motion/code, React compositions, FrameCut timing and coded layout. Retain domain craft and approved assets. Raster edits keep their existing image-edit route. |
| `audio-production-director`, `caption-studio`, `asset-manifest`, `tool-routing-cost` | Timing/render/data faults and tooling plans when technical; audio quality, captions, provenance and spending boundaries remain Studio-owned. Their existing shared-policy links cover independently invoked technical work; avoid redundant boilerplate. |
| `brief-architect`, `reference-pack-curator`, `research-evidence`, `instruction-packet-factory`, `studio-workstyle-profile` | Supply the existing brief, evidence, bounded packet and preferences. Use support only for unresolved consequential requirements or technical workflow design, without restarting intake. |
| `commercial-video-campaign-director`, `commercial-visual-campaign-director`, `ecommerce-campaign-strategy-director`, `creative-video-producer`, `creative-music-video-director`, `marketing` | Strategy and creative direction stay here. Pass bounded technical implementation to the actual production owner, with the same brief and revision. |
| `character-design`, `cinematography`, `screenplay-story-architect`, `storytelling`, `storyboard-sequence-architect`, `storyboard-board-architect` | Characters, story, shots, whole-film boards and creative acceptance remain Studio-owned. Technical board/composition faults may use support through their execution owner. |
| `copy-voice`, `humanizer`, `ugc`, `image-prompt-architect`, `video-prompt-architect` | Copy, voice, performance and prompts stay with Studio. Do not turn writing or generation requests into code plans. Relevant tool failures route to technical diagnosis without replacing approved copy. |
| `output-critic-iteration`, `delivery-documentation` | Existing artifact review and delivery own final quality; completion support checks evidence without adding another QA cycle. |
| `workflow-self-improvement`, `producer-ai-task-builder`, `hipson-adapter` | Preserve explicit-only triggers. Support is conditional on an authorized maintenance or bounded technical task; installation does not activate these skills. |

FrameCut retains: sufficient onboarding and questions, detailed visual storyboard/contact sheets covering the full reel and key state changes, user corrections and current-board acceptance, then final render and review. A sample is optional on request. Source/local/master timing and actual rational FPS remain the authority during repairs.

## Prospective wiring map

Paths below are relative to repository root; `P` means `plugins/framecore-work-creative-studio`.

| Surface | Implementation target after review |
| --- | --- |
| Installation | `CHATGPT_INSTALL.md`, `CODEX_INSTALL.md`, `CLAUDE_INSTALL.md`: first companion recommendation; README continues linking to complete guides |
| Maintainer contract | `AGENTS.md`, `docs/extension-registry.md`: companion exception and current branch scope; retain other release rules |
| Public companion reference | `P/skills/pipeline-core/references/superpowers-native-routing.md`: reconcile the current hosted contract, including native-maintenance wording that must become cross-host aware |
| Shared authority and QA | `P/skills/pipeline-core/references/studio-integration-policy.md` and `loop-protocol.md`: all 37 owners inherit the same support contract and review budget |
| First configuration | Both OpenAI manifests use documented `extensions.com.openai.onboardingSkill` targeting the existing orchestrator; explicit setup routes to companion guidance, including marketplace/ZIP installs. Claude uses explicit setup guidance without an invented manifest field. Bare-name welcome stays unchanged. |
| Central dispatch | `P/skills/workflow-orchestrator/SKILL.md`, its `references/routing-boundaries.md` and `references/extensions.md`, and `P/skills/pipeline-core/SKILL.md`: concise links, no budget overflow |
| Owners and handoffs | `P/skills/pipeline-core/references/role-skill-map.md`, `handoff-matrix.md`, `P/scripts/workflow-kit-routes.json`: same owners, support edges only |
| State and cross-host resume | `P/skills/pipeline-core/templates/project-state.md`, `P/skills/workflow-orchestrator/assets/cross-host-handoff.template.md`: revision-bound support receipt and installation choice without invented persistence |
| Direct technical specialists | Existing six hosted entry points; all other owners inherit the common reference through their existing shared-policy links |
| Registry | `P/skills/workflow-orchestrator/assets/extensions/extensions.json`, `extensions.py`, owning tests: compatible catalog-manual representation and first recommendation |
| Evaluation and release | Existing native cases plus installation/direct-entry cases; canonical validator, required suites, host evals, package inventories and guarded readback |

Never change the pinned workflow-kit/Animate snapshots to wire this integration. Do not add descriptions that breach the 7,800-character aggregate limit. Move necessary detail into existing references and verify links instead of deleting package paths. Read the latest hosted overlay immediately before any future update and preserve unrelated private integrations.

## Acceptance scenarios for implementation

These are acceptance definitions. Source-guided exercises and structural checks are recorded in the implementation verification; fresh installed-client cases remain NOT_RUN.

| ID | Scenario | Required outcome |
| --- | --- | --- |
| SP01 | Fresh Studio installation, companion missing | First add-on offer explains value and manual host route; Studio remains installable |
| SP02 | Already installed and readable | No repeated installation offer; real support resolution |
| SP03 | Decline or defer | Continue Studio; do not repeatedly ask in unchanged scope |
| SP04 | User installed, active session cannot read it | Activation unverified, documented refresh/new session, honest fallback |
| SP05 | Marketplace absent or wrong surface | No invented installer, shell command or cross-host availability claim |
| SP06 | Bare Studio name, Polish and English | Existing full welcome and order; no technical intake or extra companion pitch |
| SP07 | Direct FrameCut or motion request | Shared trigger policy reached even without top-level orchestrator invocation |
| SP08 | Approved board, coded implementation | Preserve acceptance and exact locks; appropriate plan/implementation support |
| SP09 | New reel without a board | Complete visual board and feedback/acceptance before final render; optional sample only |
| SP10 | Six-frame drift at rational FPS | Evidence-based source/local/master diagnosis and affected-boundary verification |
| SP11 | Simple raster or copy correction | Domain route and scoped review, no repository or compulsory software plan |
| SP12 | No execution/render route or no delegation tools | Probe actual capabilities; shell absence alone is not render unavailability. No claimed unavailable render or independent review |
| SP13 | Direct audio/caption/tooling fault | Bounded technical support, original owner receives result |
| SP14 | Revised output after earlier PASS | Evidence scoped to current revision; preserve unaffected accepted work |
| SP15 | Maintenance and explicit-only specialists | No spontaneous self-improvement or external agent dispatch |
| SP16 | Companion removed or changed mid-project | Rediscover when needed, no cached claim of execution; continue independent Studio work |
| SP17 | General extension catalog and existing installers | Existing entries/commands unchanged; first installation recommendation does not force catalog sorting |
| SP18 | Hosted package changed during implementation | Re-read current guard and affected files; reconcile, never overwrite concurrent work |

Run host behavior cases in bounded groups of at most five per gate, recording client, reasoning setting, actual skill reads, output, tokens/time where measurable and untested scope. Source/schema checks alone cannot pass these cases. Separately verify unchanged public welcome, package budgets, all 37 owners, direct entry reachability and no new runtime dependency.

## Rollout result

The owner approved implementation and paired publication. Release 1.122.0 publishes the reconciled shared contract on main before the guarded update of the existing ChatGPT plugin. Both destinations were read back; the private overlay remains private and preserved. See the [implementation plan](../plans/2026-10-22-studio-companion-implementation.md), [publication record](../../../verification/github-publication-1.122.0.json) and [hosted readback](../../../verification/hosted-sync-1.122.0.json). The release number was selected from then-current main, not reserved for the paused Open Design proposal. Fresh installed-client behavior remains a separate unexecuted check.
