# Handover: FrameCore Works Creative Studio, 2026-10-27 (updated 2026-10-28)

The only current handover. All older handovers were removed on 2026-10-27 at the owner's request; they remain readable in Git history at commit [`8a8c78c`](https://github.com/FrameCoreWorks/framecore-works-creative-studio/tree/8a8c78c8b15be8934b32c49c88c30413f185c387/docs). Read [AGENTS.md](../AGENTS.md) (Current rules) first, then this file, then [the roadmap](roadmap.md) and the top of [the ledger](development-ledger.md).

## Working rules (owner)

- Reply to the owner in Polish; repository files stay in English.
- Commit on `main` and push only `main` (fast-forward, no force push, no remote branch). One change reaches `main` at a time; never run two releases at once. Change IDs `CC-` (Claude Code), `CW-` (ChatGPT Work), `CX-` (Codex) with the trailers listed in AGENTS.md, and a ledger entry per change.
- A change to `plugins/framecore-work-creative-studio/` ships as a release (`python3 scripts/release.py prepare <version> ... --push`, then `publish ... --push`), then the existing hosted ChatGPT plugin is updated with Plugin Creator from `CHATGPT_UPDATE.md` (its private overlay kept). Without Plugin Creator, record the hosted state as `pending`.
- Never delete, rename or move a package path; retire text instead. Budgets: orchestrator `SKILL.md` at most 32,000 bytes (31,665 in 1.150.0), skill descriptions at most 7,800 characters in total (about 7,482 now).
- Do not wait for the owner's manual tests; record untested client behaviour as `NOT_RUN`. Make small decisions with a sensible default and record it; ask only about risky or irreversible steps, accounts, payments and publishing in the owner's name.
- Evidence stays separate: source checks, GitHub publication, saved-plugin readback, host behaviour. Host evaluations run in headless Claude Code (`python3 scripts/host_eval.py`), at most 25 cases per pass and 5 per release gate.
- Claude Code cloud: the stop hook may ask to push the session branch; follow CLAUDE.md (`git fetch --prune origin`, never push it). Hookify rules in `.claude/` block force pushes, pushes of anything but `main` and removal of package paths.

## ChatGPT Work updates without a ZIP, 2026-10-29

Owner rule: hosted updates in ChatGPT Work go through on their own; never ask the owner to attach or upload a ZIP,
and never upload one for him. Work's Plugin Creator takes only a ZIP path in code execution, code execution has no
network, and the GitHub connector writes no files (attempts 2026-10-30). So the model writes each file's connector
text into code execution, one cell checks every hash and builds the ZIP, and `create_plugin`/`update_plugin` take
that archive ([No-ZIP update route](../CHATGPT_UPDATE.md#no-zip-update-route), `CC-20261030-03`). Studio 1.157.0
makes Studio's companion setup install Toolbox and Open Assets in Work; both companions document the same route
(Toolbox 1.2.4 may leave out its 230 KB Earshot hash locks there). First successful hosted run: NOT_RUN. Nothing
needs the owner's Mac.

## Claude Code installs both companions with Studio, 2026-10-30

Owner question: does adding Studio from the marketplace in Claude also install Toolbox and Open Assets? In Claude
Code, yes: Studio's root marketplace entry declares `dependencies: ["toolbox", "framecore-open-assets"]` and the
marketplace now also lists `toolbox` (git-subdir of the Toolbox repository at a pinned commit, like Open Assets),
so one `claude plugin install framecore-work-creative-studio@framecore-works` installs all three (`CC-20261030-04`;
verified in an empty config with Claude Code 2.1.314). The dependencies sit in the marketplace entry, not in the
package's `plugin.json`, so no release was needed and an uploaded copy still loads; tag-pinned installs get it from
the next release tag. The Claude apps (claude.ai, Cowork) are not documented to honour dependencies: there the user
adds the two companions from the same marketplace. When Toolbox or Open Assets publishes a new version, bump its
`sha` and `version` in `.claude-plugin/marketplace.json`.

## Toolbox 1.0.3: owner-approved removal, 2026-10-28

Historical removal record, change `CX-20261028-01`. The owner authorized the full
Toolbox cleanup, verification and publication on main, including deletion of the
15 dedicated reviews despite Toolbox's default retention rule. This supersedes
older proposal-only wording for this list; the broader companion migration is
still planning only.

Removed Toolbox entries: `archify`, `hud`, `linkedin-agent`, `notfair`, `planning-with-files`, `ponytail`, `wondelai-code-craftsmanship`, `wondelai-marketing-cro`, `wondelai-metaskills`, `wondelai-product-innovation`, `wondelai-product-strategy`, `wondelai-sales-influence`, `wondelai-strategy-growth`, `wondelai-systems-architecture`, `wondelai-team-motivation`.

Toolbox baseline `f68470c03f7268f0926cd5446fd100642aa6eb96` had 33 entries.
Catalog **1.0.3** has **17 tools plus its index = 18 entries**. All 30 dedicated
docs/reviews and their active catalog/installation links were removed. The only
managed execution setting found was `PONYTAIL_DEFAULT_MODE` in the repository's
otherwise empty `.claude/settings.json`; that file and Ponytail-specific
CLAUDE instructions were removed. Independent work rules remain. No other local
MCP, hook, alias, wrapper, autostart or dependency for these entries was found.
No user/global installation, account, credential, cache, runtime or data was deleted.

All 17 surviving tool objects and pins are unchanged, including `wondelai-ux-design`
and its shared `wondelai/skills` source / `design-everyday-things` skill, plus
`marketing-skills`, `antislop`, `web-quality-skills`, `ffmpeg-skill` and
`earshot-audio` 1.2.0. The complete retained list, configuration audit, historical
client-leftover checklist and exact existing-plugin update prompt are in
[Toolbox's removal handover](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/main/docs/handover-claude-code-2026-10-28.md).

**New standing Toolbox rule:** new tools/assets/repositories and future entry
updates must demonstrate a concrete, fully justified improvement to FrameCore
repositories, with affected task, benefit and verification recorded in the review.
General usefulness or an unverified promise is insufficient. The retained entries
are not retrospectively invalidated, and this rule authorizes no further removal.

**Studio changes are documentation only:** this handover, roadmap and ledger.
Replace only the stale Toolbox recommendations/status text. Preserve the concurrent
Task 5 reference-file proposal and all independent Studio skills, knowledge,
protected paths, onboarding and architecture. All **1750 tracked files across
Studio's plugin directories** match baseline `9358ac746ee738f33063c5b210dd186c093a37d6`
byte-for-byte; the canonical Studio package remains 1.150.0 with 1598 files/37 owners.
No Studio hosted release is needed for this documentation change.

**Residual matches intentionally preserved:** Studio CHANGELOG and packaged
`docs/release-history.md` retain earlier Ponytail uninstall/evaluation history;
the old owner-reported uninstall fact below remains reported history. The word
“ponytail” in the prompt-example image description is a hairstyle. HUD matches
are graphics/game-interface concepts. None is a live Toolbox connection, so no
protected package bytes are edited for these matches.

**Verification:** Toolbox 37 repository tests + 24 Earshot tests, marketplace,
both portable checks/builds and Claude validation PASS. Its six-file ZIP matches
source and has no removed-tool residue; 82 IDs/aliases/source/config terms were
scanned. Isolated Claude catalog install/list reads 1.0.3; a removed-ID install
fails with Plugin not found after source verification. Isolated Codex file
install/verify PASS, not client activation. Studio canonical validator PASS;
full `bash scripts/check_all.sh` PASS: **1068 passed, 33 skipped, zero failures**.
Skipped optional/dependency/browser checks are NOT_RUN: 11 Node opt-in checks,
3 GEPA checks, 12 print/PDF checks, 6 SVG wordmark checks (missing fontTools), and
1 negative OCR-unavailable check skipped because OCR is installed. This differs
from the earlier host’s 1072/29 aggregate; it does not claim identical case coverage. The first full attempt
failed on the system FFmpeg's missing `ass` filter; the passing run uses the
already-installed FFmpeg 7.1 with libass, existing media Python 3.12 and a canonical
temporary directory. Validators and tests were not changed.

**Synchronization:** Toolbox saved Work update is **pending**; name search and a
complete personal-plugin inventory found no verified editable Toolbox identity.
No duplicate was created. Source/ZIP verification does not prove saved-plugin or
client state. Fresh Work/Codex/Claude invocations and global uninstall audits are
NOT_RUN. Exact main result commits, CI/readback and final independent inspection
are recorded in the completion handover; no remote branch or PR is created.

## ffmpeg-skill review, 2026-10-28

The owner selected `kajisho5/ffmpeg-skill` for Toolbox after the [source comparison and bounded verification](reviews/ffmpeg-skill-2026-10-28.md). Toolbox catalog **1.0.2** added `ffmpeg-skill` version 2.17.3, retained unchanged in catalog **1.0.3**, at `1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff`; [Toolbox commit `f68470c`](https://github.com/FrameCoreWorks/framecore-works-toolbox/commit/f68470c03f7268f0926cd5446fd100642aa6eb96) records the owner-approved entry. This supersedes the review's original pending-catalog recommendation, not its evidence limitations.

The catalog entry makes the original available as an independently installed option for recording alignment/drift correction, multicam preparation and explicit HDR-to-SDR conversion. **Studio routing and execution integration are not yet implemented.** FrameCut currently excludes multicam and requires a tested SDR conform before HDR editing. Preserve its one master timeline, storyboard acceptance and project revision; Earshot and Caption Studio retain their domain ownership. Cuts, captions, basic reframing, sound mixing and loudness already overlap existing tools.

The source contains 42 executable tool contracts, an argparse-derived input schema, capability detection and a local stdio MCP transport exposing 12 core tools by default. That is not evidence of a native Work plugin or active Claude/Codex installation. Audio alignment is not lip-sync certification; crop/contact-sheet tools do not track subjects; dry-run has documented analysis/verification exceptions. Full source hashes remain separate from upstream's sampled file fingerprints. The report records local synthetic checks and untested surfaces explicitly.

Toolbox's catalog package and marketplace were updated; no user skill, FFmpeg engine, model, MCP connection or hosted plugin was installed. The original native installer was tested in an isolated temporary skills directory; the installed 42-tool contract and all 145 payload files were checked. The portable Toolbox archive and an isolated native Codex **catalog-file** install were verified. Actual Claude marketplace installation, fresh Work/Codex/Claude activation and cross-plugin execution remain NOT_RUN; upstream's root `bin/` makes claude.ai / Cowork compatibility unverified. No existing saved personal Toolbox plugin appeared in the owner-plugin listing; do not create a duplicate on that basis. The earlier Workflow Kit proposals and independent-companion architecture remain unchanged.

## Workflow Kit reuse review, 2026-10-28

The owner asked whether the predecessor [Workflow Kit](https://github.com/FrameCoreWorks/framecore-works-codex-chatgpt-workflow-kit) contains useful material to transfer into Studio. This is a review and recommendation, recorded under the owner's standing request to keep Claude's handover current. The proposals below are **not adopted implementation decisions** and do not replace the independent-companion direction in the next section.

### Verified baseline and existing integration

- Workflow Kit main: `55c8bf19962c7bf7fb43648637ee433d990eb2a9`, package 1.1.0; Studio main before this documentation change: `a016cad35d03addc3f17f8c50a26d0f512c0bc43`, package 1.150.0.
- Studio's [source manifest](../plugins/framecore-work-creative-studio/integrations/workflow-kit/source-manifest.json) already pins that exact current upstream commit. There is no newer upstream delta to import at the reviewed heads.
- All **359 tracked upstream files** match the pinned archive and expanded source mirror byte for byte, accounting for the declared `SKILL.source.md` renames. Every source-file SHA-256 and the archive SHA-256 match; no tracked upstream path is missing.
- All **35 source skills** have active-owner mappings: 20 were added and 15 merged during the historical integration. All 105 declared active resources and four supporting resources exist. These are source/integration facts, not proof that a live host loads every resource on every task.
- The [integration record](../plugins/framecore-work-creative-studio/docs/workflow-kit-integration.md) describes the original dev.30/dev.31 integration. Its historical role/handoff totals are not current totals: the current route registry has 21 roles, 53 handoffs and 19 gates. The old 35 discovery entrypoints are deliberately inert; do not register another active copy.

| Valuable predecessor material | Current Studio location/status | Review conclusion |
| --- | --- | --- |
| Brief, source authority, asset traceability and delivery | Brief Architect, Reference Pack Curator, Asset Manifest and Delivery Documentation; mapped methods, templates and references | Already integrated; retain current owners |
| Creative prompt contracts, exact copy, edit preservation and continuity | Pipeline Core plus Image/Video Prompt Architect and their adapted kit resources | Already integrated; current Studio policy wins where the predecessor differs |
| Video production, storyboard, captions, OpenCut, Remotion and HyperFrames | Existing specialist owners and handoffs | Already integrated; no second workflow or controller |
| Bounded QA loops, voice review, instruction packets and retrospectives | Pipeline Core, Copy Voice/Humanizer, Hipson/Instruction Packet and Workflow Self-Improvement | Already integrated; no automatic learning or mandatory revision loop |
| Recovery, compact state and local lookup | Active [project-recovery guide](../plugins/framecore-work-creative-studio/skills/pipeline-core/references/project-recovery.md), adapted checkpoint/recovery templates; original CLI tools in archive | Useful remaining convenience work; recovery itself is already present |
| Artifact fixtures and end-to-end examples | Preserved upstream; active artifact schema links point to their fixtures | Useful for stronger development checks and a few adapted learning examples |

### Bounded candidates, in recommended order

**1. Make project recovery easier to execute.** The owner's overloaded-conversation/handover problem is a concrete trigger. The current guide requires extracting the exact archive into a separate source directory, running the legacy Memory Cache tools and adapting the initial state/recovery prompt for Studio. Consider a small adapter owned by Pipeline Core that initializes, validates and exports the existing Studio state with the actual installed paths. Reuse the existing checkpoint and cross-host handoff instead of introducing another state store or agent. The upstream `tools/context-budget-audit.mjs` supplies a useful size check; it measures bytes in allowed local files, not chat tokens or the chat service's context limit, so it cannot promise to prevent a thread from freezing.

Acceptance if implementation is later opened: resume a synthetic interrupted project in a new session without repeating accepted intake; preserve exact copy, selected assets/revisions, unresolved choices and blockers; identify missing attachments honestly; preserve populated user state; keep Context separate; reject an oversized recovery packet. A host without a shell/persistent filesystem receives a portable handoff. Persistence follows the actual user authorization and available destination, not the predecessor's unconditional approval wording.

**2. Adapt the predecessor's artifact-contract consistency checks.** [Workflow Kit's schema validator](https://github.com/FrameCoreWorks/framecore-works-codex-chatgpt-workflow-kit/blob/55c8bf19962c7bf7fb43648637ee433d990eb2a9/scripts/validate/schemas.mjs) checks required fields against template sections and fixtures. Studio's current `scripts/validate-workflow-kit.mjs` verifies fixture paths and integration structure, but its artifact-schema block only reads the fixtures. An isolated temporary-copy probe confirmed the narrow gap: baseline `validateWorkflowKit` returned zero errors; adding `__review_missing_required_field__` to Task Confirmation's `required_fields`, absent from both template and fixture, still returned zero errors. The same mutation against the upstream schema validator produced `ARTIFACT_SCHEMA_FIELD_MISSING_TEMPLATE` and `EXAMPLE_ARTIFACT_MISSING_FIELD`, with zero baseline findings. Both real repositories were unchanged by the probes. This is missing validation coverage, not a demonstrated failure of a generated client artifact.

Candidate scope: adapt field/template/fixture consistency checks and selected negative prompt/copy cases to the **active Studio contracts**, inside the existing validation path. Keep source snapshots immutable and scope checks to each actual owner; full backstage schemas are not mandatory for a short user-facing answer. Do not copy the predecessor's validators unchanged: `scripts/validate/copy-delivery-contracts.mjs` requires a revision phase, while Studio permits `no repair needed` and an unchanged passing draft; generator/model assumptions and strict continuity/readiness fields also need current-owner review. Acceptance: absent required fields, changed locked copy and missing strict carriers are detected; a passing unchanged draft remains valid. Source fixture checks still do not certify creative quality or active-host behavior.

**3. Reuse a few worked examples when improving teaching or onboarding.** The end-to-end modular desk-lamp example, static campaign walkthrough and video/storyboard examples can support a compact brief -> decisions -> artifact -> review demonstration. They currently serve archival/development purposes, with fixture links in the active schema. Adapt two or three examples only for a concrete learning task or observed usability gap, using existing learning resources. Keep current Studio owners, research rules, image-tool capability discovery and Quick behavior; the legacy example's nine-role route and model-specific wording are not the current product contract. Acceptance: a learner can complete the example with traceable source inputs and a final deliverable; no full fictitious production run is claimed from a planning-only example.

### Material not recommended for direct migration

- Native/project-local installers, `.agents`/`.codex` agent templates and the old onboarding flow: they serve a separate standalone product and would duplicate Studio's installation, startup and ownership.
- The lexical index as a new semantic-memory service: `semantic-memory-index.mjs` uses token overlap, with legacy-path allowlists. It is not embeddings, persistent cloud memory or cross-host synchronization. Keep optional local lookup modest unless a concrete retrieval need appears.
- The old automatic audit CLI as a quality judge: `skill-agent-auditor.mjs` looks under `.agents/skills` and flags missing example/assets/fixture README files and keywords. Porting it literally would create layout-based noise in a plugin with different paths. Studio already has an explicit retrospective owner, change requests and host-evaluation cases.
- Background self-improvement, API activation phrases and legacy mandatory confirmation/revision gates: preserve current scoped authorization, explicit adoption and Studio's bounded review policy.
- A new installable extension entry for the same 35 skills: this is already-integrated predecessor material, not a newly proposed independent companion. The current analysis request does not authorize duplicate installation or a runtime registry edit.

Recommendation: first simplify recovery for long projects; then close the demonstrated contract-validation gap. Worked examples are a smaller follow-up tied to learning needs. No bulk re-import, new skill, archive rewrite, source-pin change, companion migration or hosted release was performed by this review. All three candidates remain proposals for a later explicitly scoped implementation task. Fresh ChatGPT/Codex/Claude behavior was not tested.

## Latest owner decisions: independent companions, 2026-10-28

This section is the current continuation point for Claude Code. The owner asked ChatGPT Work to recover two related conversations, read the complete project knowledge document and publish the latest decisions as this handover. It supersedes older same-repository architecture, separate-Earshot-repository and build-pending statements below **only for this companion architecture task**. Other bounded tasks retain their own status and authorization. Do not restart completed Open Assets research/build/cleanup.

### Accepted architecture and responsibilities

| Product / component | Source and responsibility | Independence |
| --- | --- | --- |
| Creative Studio | [This repository](https://github.com/FrameCoreWorks/framecore-works-creative-studio): creative knowledge, brief and accepted decisions, project state, tool selection, sequencing, cross-plugin dependencies and handoffs, final review | Owns coordination; do not copy entire companion implementations into its creative core |
| FrameCore Open Assets | [Independent repository](https://github.com/FrameCoreWorks/framecore-open-assets): find and download qualified media, preserve source/rights/attribution, verify the actual file | Usable without Studio, Toolbox or Earshot |
| FrameCore Works Toolbox | [Independent repository](https://github.com/FrameCoreWorks/framecore-works-toolbox): reviewed catalog, host-specific installation information, distribution and maintenance of local adapters | Usable without Studio or Open Assets; listing a tool does not install it |
| Earshot Audio | `plugins/earshot-audio/` **inside the Toolbox repository**: FrameCore's own wrapper around the reviewed original Earshot engine | A separately installable plugin, usable without Studio, Open Assets or the Toolbox catalog plugin |

The owner chose separate repositories for Studio, Open Assets and Toolbox, rather than one monorepo containing all three products. Earshot inside the Toolbox repository is an intentional exception to “one plugin per repo”: its independence is an installation/runtime property. Do not create a fourth Earshot repository, merge Earshot into the catalog package or ask the owner to resolve that already settled choice again.

Companions must not require one another to complete their ordinary standalone task. Studio describes any dependencies of the full Studio workflow and checks whether the required installed capability actually exists. Neither an instruction nor a catalog entry proves automatic dependency installation. Keep host-specific dependency/installation behavior explicit and verified; do not assume Claude, Codex and ChatGPT have identical mechanisms or limits.

Future distinct capabilities may follow the independent-companion pattern. This does not mandate a new repo for every small craft fix or authorize extracting established Studio skills. Keep the existing owners, IDs, startup, accepted content and path protection. There is no approved mass migration or deletion from Studio.

### Earshot and installation decisions already settled

- Maintain our own adaptation in Toolbox, with original authorship, licence, reviewed upstream commit and a clear description of FrameCore changes. This is not a wholesale copy of upstream into the repo and not a fork of its engine under new authorship.
- The original engine is [Leon Lin's Earshot](https://github.com/Leonxlnx/earshot), pinned by the current wrapper to `591fa3e028032e6dce56620a20e932e35667e8d8` (0.4.0). Source/engine preparation and model downloads remain outside the catalog/repository and have their own runtime/consent requirements.
- Toolbox follows Studio's installation pattern: root `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, a shared skill source and a separate archive per local plugin. Its Claude marketplace remains a repository-level catalog, outside those plugin archives.
- Open Assets already has the three manifests. Do not add duplicate manifests or recreate its existing plugin.
- Package portability does not certify every third-party catalog entry on Work/Codex, nor install Earshot's engine or models. Record source/package checks, saved deployment, native installation and fresh client behavior separately.

### Source snapshot checked for this handover

These are `OBSERVED_SOURCE` facts from 2026-10-28, not new runtime test results. Refresh the relevant head before subsequent changes.

| Repository / surface | Observed main commit | Source state |
| --- | --- | --- |
| Studio | `d4d82bdda2b86b7455b65a46d3d63e6511f3d503` | Studio 1.150.0; existing in-repo copies Open Assets 0.2.1 and Earshot 1.1.0 remain present |
| Independent Open Assets | `dcb26ae1f779e034a13442bbb4c50075abc8f6d7` | Open Assets 0.2.1; standalone/companion documentation and three manifests |
| Toolbox | `23b84ac8ca1736c152457dc0262d43a1287aa27f` | Catalog 1.0.1 and independent Earshot wrapper 1.2.0; latest commit adds the adapter |

The source split is therefore only partly reflected in Studio: newer companion repositories exist, while this repository still contains earlier companion copies and routing. **Do not infer completed migration, complete cross-repo orchestration or hosted Earshot 1.2.0 activation.** Compare actual contracts and publication records first; do not delete the older copies in this documentation task.

Toolbox's complete Git tree contains 122 files / 614,700 bytes of tracked content: the six-file catalog is 23,013 bytes; the 29-file Earshot wrapper is 347,875 bytes. The marketplace has 32 entries: the catalog, Earshot and 30 pinned external entries (13 Creative, 8 Dev tools and 10 Marketing & growth entries excluding the catalog). These are Git-tree counts, not ZIP/cache/context sizes. No loose image/video/audio assets or model weights appear in that tree. Dependency lockfiles are functional setup records, not unused media.

Four retained reviews (`compound-engineering`, `seo`, `skillspector`, `video-vision`) have status `removed` and no active marketplace entry. They explain earlier removal decisions and stay outside the portable catalog. Toolbox normally retains removed reviews; the owner's dated 1.0.3 exception above completely removes the 15 selected dossiers. The four earlier retained reviews are unaffected and are not evidence that those tools remain active.

Toolbox's [verification record](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/23b84ac8ca1736c152457dc0262d43a1287aa27f/docs/verification.md) reports 37 repository checks and 24 wrapper checks passing. Treat those as `REPORTED_HISTORY`: the present handover did not rerun Toolbox's engine, models or installers. Fresh host activation, engine rendering and full-tier inference remain `NOT_RUN` there. That record says the prior saved Work Earshot 1.1.0 was left unchanged; this session did not perform a new hosted readback. The earlier Open Assets → Earshot 1.1.0 → Studio Work flow does not certify the new independent 1.2.0 adapter workflow.

### Toolbox scope after the owner-approved cleanup, 2026-10-28

The 1.0.3 removal record at the start of this handover supersedes the earlier
proposal-only status for the exact 15 selected entries. The comparison below
contains retained tools only; it is not approval for any further removal or for
implementing the companion migration. Reviews, tests and build helpers remain
repository maintenance; user recordings, outputs and model caches stay separate.

| Area | Retained items / issue to compare | Treatment |
| --- | --- | --- |
| Video | `earshot-audio`, `ffmpeg-skill`, `animate`, `motion-designer`, `video-shotcraft`, `brag`, plus Studio's existing motion/Remotion owners | Match the task to one execution workflow; preserve sound/caption ownership and evidence |
| Graphics, web and text | `logo-design`, `meta-ads-designer`, `hallmark`, `nateherk-design`, `sepia`, `wondelai-ux-design` | Preserve Studio's graphic/copy ownership and accepted results |
| External/local prerequisites | `open-design`, `blender-agent-skills` | Verify host and runtime readiness separately from catalog presence |
| Development | `antislop`, `web-quality-skills` | Keep optional domain-specific use and existing pins |
| Marketing | `marketing-skills` | Preserve the independent marketing capability and existing pin |

Only `wondelai-ux-design` remains from the former Wondelai catalog groups. Its
`wondelai/skills` source, commit and complete skill list are preserved, including
`design-everyday-things`, which was also listed by a removed group. The source
is shared; this task does not alter upstream content or independently integrated
Studio knowledge. The owner's new admission rule requires demonstrated concrete
benefit to FrameCore repositories for new entries and future updates.

### Current authorization and next work

The earlier instruction authorized **publishing the architecture documentation handover**. The new bounded 1.0.3 cleanup is separately authorized and recorded at the start of this file; the following migration-planning limits remain in force. Architecture comparison and a detailed cooperation/migration plan are within the recovered planning scope. It does not authorize implementation of that plan, new releases, companion installation, paid providers, uploads, publication of user media or changes to protected Studio behavior. Earlier completed build/update permissions are not an open-ended migration order.

Next action: compare current Studio and Open Assets integration points with Toolbox Earshot's [generic input/output contract](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/23b84ac8ca1736c152457dc0262d43a1287aa27f/plugins/earshot-audio/skills/earshot/references/handoff.md). Produce a reviewable plan covering:

1. Task → owner → required installed capability → input/output → evidence → host, including missing-capability behavior and standalone use.
2. Open Assets returns a verified local file with source, rights, credits and hash; Studio passes an ordinary local file/source record to Earshot; Earshot returns outputs, input/output hashes, readiness, measurements, timing and explicit unexecuted checks. Studio retains the brief, master timeline and final creative approval.
3. Version compatibility and independent distribution; observed install paths for Claude, Work and Codex; no promise of automatic dependency installation without evidence.
4. Bounded migration of references/ownership and any necessary compatibility paths. Inspect old companion copies before proposing retirement; preserve Studio's protected paths and concurrent work.
5. Source/package checks, standalone tests, cross-plugin provenance/timing tests and fresh-client checks, each with actual scope/cost/authorization. Do not treat decode/measurements as listening or creative acceptance.

Use a small scope/review packet before implementation: problem, owner, allowed paths/sections, exclusions, acceptance, relevant regression checks and rollback. Keep durable checkpoints during substantial work and resume from the next unfinished action; do not repeatedly poll CI or rerun completed tests without new evidence. Never claim to force host compaction or diagnose an application freeze without evidence. Work on `main` only, preserve concurrent changes, and do not repeat settled questions. The private project knowledge document was read in full but is not copied into this public repository.

This handover update changes only this file, the roadmap's current direction and the development ledger. No runtime bytes, manifests, package versions, releases or hosted installations are changed. The commit/ledger identifies the documentation publication separately from all earlier implementation evidence.

## Current state, 2026-10-28

The following paragraphs record the earlier implementation in this repository. The independent-repository snapshot and planning scope above take precedence for continuation; historical build, provider and hosted-state statements are not new instructions.

The owner's follow-up requires complete removal of unqualified providers from Open Assets, without disabled entries or pointers. Open Assets 0.2.1 is now published at `0ec35cf` and saved as `pluginrel_6ae1e793e458819183183bc46e9d9859`; all 61 surviving files and all four deletions were verified by readback. The cleanup record is in [the bounded record](research/open-assets-confirmed-only-2026-10-28.md). It retains fourteen providers/twenty-three observed Work media paths, removes four provider dossiers and the unused NASA audio branch, and leaves Studio/Earshot packages unchanged. Earlier held-provider statements below describe the 0.2.0 baseline, not the current catalogue.

Studio **1.150.0**, Open Assets **0.2.0** and Earshot **1.1.0** are published on main and saved in the existing ChatGPT plugins. Source commits: `ed7f8cc` and `8766407`; tag `v1.150.0`. [Release evidence](../verification/github-publication-1.150.0.json) and [hosted readback](../verification/open-assets-0.2.0-hosted.json) record exact scope, including all 55 preserved private Studio files. The current catalog exposes the updated three skills. Fourteen providers/23 media paths passed actual Work search/download/decode; four sources remain held and NASA audio is disabled. The local Open Assets → Earshot light → Studio provenance flow passed. New-conversation startup, neural listening and Claude/Codex runtime tests remain NOT_RUN; the owner plans those separately. This completes the expanded Task 1 implementation/update scope; remaining product tasks below retain their own authorization requirements.

## State on 2026-10-27

- **Studio 1.149.0** on `main` (tag `v1.149.0`). Companions: Earshot Audio 1.0.9, Voice And Narration 1.0.2, Brand Kit 1.0.1.
- Today's releases: 1.143.0 and 1.145.0 (plugin-dev review fixes, review in `docs/reviews/plugin-dev-skill-review-2026-10-26.md`), 1.144.0 (Openverse reference base), 1.146.0 (motion library first; sound sourcing to Audio), 1.147.0 (ready templates; no-idea directions), 1.148.0 (Openverse failure classes and retries), 1.149.0 (on a blocked or failing Openverse, Studio tells the user and asks whether to stop or continue another way).
- **Hosted ChatGPT plugin:** last saved 1.126.0; `pending` for 1.127.0 to 1.149.0. One Plugin Creator update covers all.
- **claude.ai marketplace:** the repository archive is about 22 MB since the host-eval candidate ZIPs were removed (they had pushed it past claude.ai's 512 MB limit); the owner's re-sync: not confirmed.
- **Ponytail plugin** was uninstalled by the owner (it appended lines to replies and broke the byte-identical welcome).
- **Owner decision 2026-10-27, ready templates:** Studio shows matching ready templates from its libraries first; Studio originals and starters whose source allows copying are used as they are; third-party creator work is linked and adapted, never copied (`pipeline-core/references/ideation-method.md#ready-templates`). A user with no idea gets two or three directions at once.

## Owner-authorized update, 2026-10-28

The owner expanded Task 1 to implementation, full Work media tests and synchronized updates of all three existing plugins. The coordinated release is Studio 1.150.0, Open Assets 0.2.0 and Earshot 1.1.0. Four additional providers qualified; four remain held. Studio routes sourcing through Open Assets and Earshot imports verified local audio with provenance. See `verification/open-assets-0.2.0-work.json` and the dated research update. Later Claude/Codex active-client tests remain NOT_RUN, to be performed separately; older research-only scope below is historical.

## Task 1 (top priority): a keyless free-media companion plugin, Openverse set aside

**Implementation history, not a new work order:** the research, build, coordinated 1.150.0 update and confirmed-only 0.2.1 cleanup below were completed within their recorded scopes. Continue from the independent-companion planning section above; preserve these earlier requests as provenance and do not rerun them merely because they use present-tense wording.

Current owner authorization, 2026-10-28 (`CW-20261028-01`): build **FrameCore Open Assets** using Earshot's
Claude/ChatGPT/Codex package pattern. This supersedes the earlier research-only/build-pending statements below.
The standalone companion is implemented in `plugins/framecore-open-assets`; see the
[build record](research/framecore-open-assets-build-2026-10-28.md). Ten official provider adapters and eighteen
policy dossiers preserve the all-qualified-sources rule; eight candidates remain blocked by unresolved terms
or commercial-use restrictions. Each host/category must run its own search-to-decoded-file verification.
Claude runtime is unavailable in this Work session, so Claude Code/apps results remain NOT_RUN. Studio
1.149.0 and Earshot 1.0.9 are unchanged; Studio's broader Openverse rewiring/release is not part of this
standalone companion creation and must not be inferred from its availability.

Research checkpoint (ChatGPT Work, 2026-10-27, `CW-20261027-01`): [provider research](research/free-media-providers-2026-10.md) covers six categories and 18 live-tested keyless candidates; [HTTP and decoder evidence](../verification/free-media-providers-2026-10-chatgpt-work.json) records 15 successful representative search-to-file paths and three failures. Music, recorded-SFX and policy gaps remain explicit. A follow-up [GitHub mapping](research/free-media-github-solutions-2026-10.md) reviews 31 pinned repositories and adds SFXMint as a conditional synthetic/AI SFX candidate; upstream repository runtimes remain NOT_RUN. Claude Code provider tests are NOT_RUN. The owner has limited this checkpoint to research/tests; no release or Studio rewiring is part of it.

Owner follow-up, 2026-10-27 (`CW-20261027-02`): **include every source that fully satisfies the asset-provider requirements**, not only the earlier launch shortlist. The [qualification rule](research/free-media-providers-2026-10.md#owner-selection-decision-2026-10-27) requires official permitted keyless access, applicable rights/client conditions and the required media/host tests. Mixed-rights catalogues require enforceable per-asset filtering. Unknown conditions and failed or unrun required paths remain pending; a technical PASS is not full qualification. No provider-count cap is approved. **Approved name: FrameCore Open Assets. Technical identifier: `framecore-open-assets`. Implementation authorization: pending.** The naming decision is recorded in `CW-20261027-03`; approval of the name does not authorize a build or release. These decisions supersede the earlier request to choose a small provider list and name, not the research and evidence gates below.

Owner decision 2026-10-27, final:

1. **Set Openverse aside for now.** It is unstable: Cloudflare challenges from cloud hosts (HTTP 403, `cf-mitigated: challenge`) and server errors under load (500, 504, 56 s responses). Upstream issues [#5625](https://github.com/WordPress/openverse/issues/5625) (open since 2026-10-03, also blocks the OAuth token endpoint, no maintainer reply), [#5478](https://github.com/WordPress/openverse/issues/5478) (open since 2025-09, a token does not help, depends on the hosting provider) and [#5649](https://github.com/WordPress/openverse/issues/5649) (timeouts and 502 from many networks). Do not invest further in Openverse access.
2. **Build a companion plugin beside Studio** (like `plugins/earshot-audio` and `plugins/brand-kit`: three manifests, marketplace entry, version guard in `scripts/check_version_bump.py`, registry entry, README, tests). It aggregates free media APIs for images, audio, music, sound effects, graphics and video that **need no registration and no key**. Providers that need a key or account are out of scope (Pixabay, Unsplash, Pexels, Freesound, Jamendo, Smithsonian via api.data.gov, Europeana).
3. **One module per provider, built from that provider's own documentation.** Read its official API documentation, README, terms, rate limits and client rules (for example Wikimedia's User-Agent policy) directly from the provider; record the URL and date read; implement exactly those rules (headers, pacing, caching, hotlinking, attribution format, licence fields, allowed uses); keep each provider's know-how as a reference inside the plugin so any agent on any host uses it the same way. No scraping, no evasion of protections (no CAPTCHA solving, proxy or IP rotation, cookie copying, browser impersonation).
4. **Common contract:** one result shape (provider, id, title, creator, licence, licence URL, source page, file URL, attribution, warnings); commercial-safe licence filter by default (no NC, no ND, SA flagged); failure classes and bounded retries as in Studio's `skills/reference-pack-curator/scripts/openverse.py`; the 1.149.0 rule (tell the user what failed, ask before another route). Downloads are checked to be real media (for example `ffprobe`, image headers), never an HTML error page.
5. **Research first (owner request).** Before building, search thoroughly per category (audio, music, SFX, graphics and illustrations, photos, video) for keyless free media APIs. For each candidate record: official documentation URL, truly keyless or not, licence model and allowed uses, limits and client rules, media formats and download variants, and a live test from ChatGPT Work and from Claude Code. Look beyond the list below: public-domain and government archives (national libraries, space agencies, public broadcasters' open archives), university and museum open-access collections, CC0 libraries for 3D, textures, icons and sound, open music archives. Exclude scraping-only sources, sites whose terms forbid automated access, and anything behind an account. Present every fully qualified source per category and name the gaps (keyless audio and music are expected to be scarce). The owner has approved the all-qualified-sources selection rule and the name FrameCore Open Assets (`framecore-open-assets`); obtain build authorization before implementation.
6. **Rewire Studio away from Openverse** (in the same task, as a Studio release): the Openverse reference base in `skills/reference-pack-curator/SKILL.md`, the pointers added in 1.144.0 (Graphic Design, Image Prompt, Storyboard Board, Cinematography, Character Design, Motion Graphics and its `references/reel-board-system.md`, FrameCut, Audio, Research), the orchestrator's picture rule ("Openverse photos"), the Audio row, the first-configuration line in `skills/workflow-orchestrator/references/extensions.md`, Earshot 1.0.9's Openverse step in `plugins/earshot-audio/skills/earshot/SKILL.md`, the `openverse` registry entry and `integrations/openverse/README.md`. Point them to the companion plugin; keep every file path (retire text, never delete files). Measure the orchestrator budget before editing (about 337 bytes left).
7. **Evidence per host:** test every module with fresh requests from ChatGPT Work and from Claude Code before enabling it; report a provider that fails from a host as such for that host.

Keyless candidates to verify (from quick research on 2026-10-27; not yet checked against the providers' documentation): Wikimedia Commons (images, audio, video; descriptive User-Agent required; answered 429 to bursts in the owner's cloud session), The Met Collection API (CC0 public-domain images), Art Institute of Chicago API (CC0 data, IIIF images), Cleveland Museum of Art Open Access API (CC0), Rijksmuseum (keyless per a secondary source), Library of Congress JSON API, NASA Image and Video Library (images-api.nasa.gov), Internet Archive advanced search (licences vary per item). Keyless audio: Wikimedia Commons and Internet Archive first; report the gap if nothing else qualifies, so the owner can decide whether a free-key source such as Freesound is allowed.

Openverse facts kept for reference: from a Claude Code cloud container (egress via Cloudflare IAD) identical anonymous requests got HTTP 200 JSON on 2026-10-27 11:51 UTC, while the owner's ChatGPT Work test at 10:40 UTC got 403 challenges (cf-ray `a51115ddaab2381e-ORD` images, `a51115f47f8f381e-ORD` audio). Openverse's documentation ties OAuth only to API rate tiers, not to the Cloudflare edge. A CC BY audio file was found and downloaded from Freesound's CDN from the Claude container (verified MP3, 60 s). The owner may still post our evidence to #5625 (a draft comment is in Git history at commit `8a8c78c`, `docs/handover-claude-code-2026-10-27.md`); that is the owner's choice, not this task.

## Task 2: no-idea directions in every area

Owner requirement: a user with no idea gets striking, fitting directions at once, ready templates first. Suite `tests/host-evals/ideas.json` (NI01 Motion, NI02 FrameCut, NI03 poster, NI04 jingle, NI05 UGC, NI06 AI video clip); run `python3 scripts/host_eval.py --suite ideas`.

- Baseline on 1.146.0: 9 of 18 runs passed. After 1.147.0: 8 of 12. Not recorded with `--write`.
- Open failures: NI01 sometimes answered by the orchestrator without loading Motion Graphics (no library read); NI03 and NI04 "a direction never mentions this brief" (read the replies: the harness's `each_mentions` regex may be too narrow, or the direction is generic); NI06 once asked 4 questions.
- Next: read failing replies (wrap `host_eval.run_turn` to print the reply and read paths), separate harness strictness from real defects, fix the smallest cause in the owning `SKILL.md`, record a pass with `--write`.

## Task 3: owner actions to remind (not agent work)

- The old request to update hosted Studio from 1.126.0 through 1.149.0 was superseded by the recorded 1.150.0 save. Verify current state before any new update; ordinary ChatGPT startup remains a separate unrun check for that release.
- Confirm the actually installed Studio version in claude.ai when the owner tests it; do not prescribe the historical 1.149.0 as the new target. Toolbox/Earshot activation has its own evidence requirements above.
- Optionally post the Openverse evidence to #5625.

## Task 4: maintenance follow-ups

- **Links to removed handovers inside the package:** `plugins/framecore-work-creative-studio/docs/release-history.md` and `docs/skill-naming.md` still link to removed `docs/handover-*.md` files on `main`. At the next Studio release, point them to the permalinks at commit `8a8c78c` (as done for the repository docs).
- **Security review** of Studio's executable scripts (security-guidance and pr-review-toolkit plugins): planned, not started.
- **Orchestrator budget:** move detail to references before adding routing.
- **Older open items from the motion 1.70 handover** (check which are done before acting; they follow maintenance mode unless the owner asks): lyric timing on a real song with stable-ts; one recorded client-style HyperFrames reel through the route; starter compositions for app or product and offer (a local-service starter exists); lyric video check with `music-to-video`; a `footage` scene kind for hybrid films in the contract route; push, iris and split transitions only when briefs ask; `motion_activity.py` inside `acceptance.py`; Meta placement facts (Caption Studio's dated card now covers 9:16 safe zones).
- **Companion plans kept as plan only** (from the 2026-10-24 proposals; Voice And Narration and Brand Kit are built, the free-media plugin is Task 1): a publishing and platform pack, and a localization glossary. Not authorized until the owner chooses.

## Task 5: reference files for every Studio skill (plan only, 2026-10-28)

The owner asked (2026-10-25) for a reasoned proposal of reference files for each Studio skill, added to the handover. Nothing below is written yet; each priority group is a bounded task the owner opens before work starts (maintenance mode). Measured on `448de19` (Studio 1.150.0, 37 skills): 2 skills have no reference (`workflow-self-improvement` and the retired `hipson-adapter`) and 10 have one; `hyperframes-workflow` and `pipeline-core` carry the most.

**Why references.** Descriptions are near their limit (7,800 characters in total) and `workflow-orchestrator/SKILL.md` has about 330 bytes left, so neither should grow. A reference costs nothing in those budgets: a model reads it only when the owning `SKILL.md` links it.

**Already done since the 2026-10-24 review** (its recommendations 1, 2, 3, 5 and 6, all in 1.150.0): Cinematography `camera-light-decision-cards.md` (1.134.0); Caption Studio `platform-caption-specs.md` and UGC `disclosure-by-platform-and-market.md` (`ea14dd0`, checked 2026-10-25); Brand Strategy `positioning-and-audience-research.md` and Video Producer `production-worksheets.md` (`78119cb`). Not proposed again.

**Rules for every new reference.**

1. One file in the owning skill's `references/`, linked by one sentence in that skill's `SKILL.md` that says when to read it; never a link from `workflow-orchestrator/SKILL.md`. Skill descriptions stay unchanged.
2. Method, checks and dated facts only; no ready-made ideas, scenarios or category lists, no personal defaults (rates, tools, clients).
3. Facts that change (platform rules, law, specifications) carry a check date, a source per row and Unknown where not verified; refreshes edit the file in place.
4. About 4 to 8 KB, in English; examples stay in the language they demonstrate.
5. A host-eval case in `tests/host-evals/additions.json` shows the gap before and the reference's effect after; run it headless (at most 5 cases per release subset).
6. Each priority group ships as one Studio release with the usual checks; no package path is moved or deleted.

### Priority 1: real gap in a core job

| Skill | Today | Proposed reference | Why (the gap) |
|---|---|---|---|
| `opencut-video-studio` (FrameCut) | `editor-handoff.md` only; `SKILL.md` about 29 KB | `footage-logging-and-selects.md`: log footage, mark selects, a paper edit for interviews, rough-cut review criteria | Its description promises "interview, analyze, edit", but nothing in the skill names logging, selects, a paper edit or a rough cut; every footage-first edit starts there. |
| `storytelling` | `short-form-structures.md` (short form only) | `structure-diagnostics.md`: why a longer story does not work (want, obstacle, change; cause chain; setup and payoff ledger; motifs across a series) | Longer narrative and series work has no diagnosis. Review recommendation 7. |
| `brief-architect` | `client-offer-and-quote.md` only | `brief-gap-diagnosis.md`: find contradictions and missing acceptance criteria, order the one question per round, two short before/after examples | The skill's core job (messy notes into a Brief Contract) is two process lines; the only reference covers quotes. |

### Priority 2: wider reach for non-Polish users and commerce

| Skill | Today | Proposed reference | Why (the gap) |
|---|---|---|---|
| `copy-voice` | Polish copy standard and Polish checker; AI-pattern list in English and Polish | `locale-mechanics.md`: how to check punctuation, quotation marks, numbers, dates and currency for the copy's language, and where to verify; Polish keeps its own standard | Studio follows each user's language, but only Polish has a mechanics standard. |
| `ecommerce-campaign-strategy-director` | 5 references, no listing rules | `marketplace-listing-rules-snapshot.md`: dated main-image, gallery and title rules for the marketplaces a user names, one source per row | The description names marketplaces, but no marketplace rule is recorded anywhere in the package. |

### Priority 3: useful, lower urgency

| Skill | Proposed reference | Why |
|---|---|---|
| `character-design` | `identity-drift-checks.md`: diagnose identity drift across a batch of outputs and choose the smallest repair | Review recommendation 7; continuity rules exist, a diagnosis of drift does not. |
| `reference-pack-curator` | `reference-rights-and-provenance.md`: mark each supplied reference as inspiration only, client-owned, stock under licence or Unknown | Supplied references are sorted by role, not by usage right (Open Assets covers sourced media, not the user's own pack). |
| `tool-routing-cost` | `batch-cost-estimate.md`: estimate a job from takes, pilot, resolution and the provider's current price page | The skill enforces a cost cap but has no method to estimate one. |

### Refresh only, no new file (trigger: a dated fact goes stale)

- `research-evidence`: `image-generator-snapshot.md` (2026-09-24), `video-generator-snapshot.md` (2026-10-09), `channel-specs-snapshot.md` and `marketing-rules-snapshot.md` (2026-10-10); the 90-day rule makes the oldest due by about 2026-12-23.
- `video-prompt-architect` `generator-dialects.md` and `audio-production-director` `music-provider-routing-and-rights.md`: when a generator or provider changes.

### No new reference proposed

- Already deep: `hyperframes-workflow`, `pipeline-core`, `audio-production-director`, `commercial-video-campaign-director`, `commercial-visual-campaign-director`, `creative-music-video-director`, `image-prompt-architect`, `video-prompt-architect`, `screenplay-story-architect`, `storyboard-board-architect`, `storyboard-sequence-architect`, `delivery-documentation`, `output-critic-iteration`, `research-evidence`.
- Done recently: `cinematography`, `caption-studio`, `ugc`, `marketing`, `creative-video-producer` (see above).
- Narrow by design: `asset-manifest`, `humanizer`, `instruction-packet-factory`, `remotion-video-production` (refresh its official sources when Remotion changes), `studio-workstyle-profile`, `static-graphic-design-creator`, `workflow-self-improvement` (explicit-only).
- Budget: `workflow-orchestrator`.
- Retired or alias: `hipson-adapter`, `producer-ai-task-builder`.

**Suggested order.** Priority 1 as one release (three independent files in different skills), then priority 2; priority 3 only when real use shows the need; refreshes when their dates fall due.

## Reference: free media providers that need a key (out of scope for Task 1)

Recorded on 2026-10-27 in case the owner later allows free-key sources: Pixabay (free key, 100 requests per 60 s, commercial use without attribution, self-host images, 24 h cache), Unsplash (free key, 50/h demo and 1,000/h after approval, hotlinking and download tracking required), Pexels (free key, 200/h and 20,000/month; a secondary source says new keys are paused), Freesound (free key, per-sound CC licence), Jamendo (free client id, 35,000 requests/month for non-commercial applications only), Smithsonian Open Access (api.data.gov key), Europeana (free key). Verify every figure against the provider before use.
