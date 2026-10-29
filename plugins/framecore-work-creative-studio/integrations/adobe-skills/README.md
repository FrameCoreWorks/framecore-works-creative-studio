# Adobe skill methods, adapted without an Adobe account

Source: <https://github.com/adobe/skills>, reviewed at `cf077272e02f29873afeb9049740789d7888c388`, 2026-10-21. Root license: Apache-2.0, retained in [LICENSE](LICENSE). Copyright and source attribution remain with the upstream authors. No root NOTICE was present at this pin. Studio's applied reference is an original adaptation; no upstream engine, assets, installer or SKILL.md entrypoint is bundled. Adobe trademarks and proprietary service rights are not granted by the repository's license.

Owner trigger: integrate the reusable free skill knowledge into the existing Studio plugin, with **no Adobe account or integration**. This supersedes the general optional-install convention for this reviewed suite. The [applied reference](../../skills/pipeline-core/references/account-free-creative-production.md) is already bundled and needs no additional installation. Existing Studio owners load its relevant sections; canonical skill IDs and menus stay unchanged.

## Decision map

| Source family at the reviewed pin | Decision | Studio connection and boundary |
|---|---|---|
| Creative Cloud `adobe-create-social-variations`, `adobe-resize-photos-and-videos` | Adapt | Static Design and FrameCut: explicit formats, protected regions, crop/fit/recompose, representative ratio previews, per-output QA. Full film boards remain mandatory. No generative expansion service. |
| `adobe-batch-edit-photos`, `adobe-retouch-portraits` | Adapt | Static Design: representative groups, sample corrections, approved recipe applied to full-resolution originals, exceptions and bounded QA coverage. No Photoshop/Lightroom execution claim. |
| `adobe-fonts`, `adobe-design-from-template`, `adobe-create-pdfs-from-data`, `adobe-design-to-pdf` | Adapt | Static Design and Asset Manifest: actual licensed fonts/specimens, slot mapping and template/mockup rights. No catalog activation, premium template access or proprietary document engine. |
| `adobe-anypdf`, `adobe-anydocx`, `adobe-anypptx`, `adobe-anyexcel`, `adobe-document-review` | Adapt methods; reject mandatory service routing | Research and Delivery: extraction/coverage, exact anchors, conversion versus authoring, review focus and honest annotation/export status. Existing host tools only; no Acrobat prerequisite. |
| `adobe-edit-quick-cut` | Adapt editorial method | FrameCut's inspected source/transcript and timeline. No Adobe API or unsupported semantic-cutting promise. |
| Stardust: extract, audit, direct, spec, prototype, diff, qa, reskin/uplift | Adapt | Ecommerce, Static Design and existing DESIGN.md interchange: current evidence versus target direction, source locks, bounded page inventory and before/after comparison. No upstream CLI, impeccable dependency or new browser engine. |
| Web: page collection, tree, reduction, language/cache evidence | Adapt | Existing permitted research route: structured sources, source language and viewport, readable evidence with coverage. Do not import CDP setup, bot-protection workarounds, session configuration or domain masking. |
| AEM content operations | Adapt generic methods | Website-to-campaign content, metadata, accessibility and evidence-led fixes. EDS paths and AEM-specific schema/deployment assumptions are excluded. |
| Adobe Analytics / Customer Journey Analytics | Adapt supplied-data reasoning | Research and Ecommerce: KPI definitions, comparable periods/segments, movement impact and funnel limitations. No IMS authentication, report calls or segment writes. |
| AEM project management and Workfront | Adapt general handoff/QA discipline | Delivery and Critic: roles, scope, findings, evidence and next steps. No Workfront/Fusion calls, new enterprise planning system or AEM operations. |
| Firefly `run-workflow`, the Creative Cloud `adobe` router and account/service steps | Reject from this route | Account/entitlement-bound services are not transferable skill-only capabilities. No setup, credentials, uploads or paid generation. |
| AEM cloud/6.5-LTS runtimes, App Builder, Commerce scaffolding/migration/review, deployment/migration backends | Reject from this scope | Adobe-specific development and operational stacks do not improve the requested account-free creative workflow. General QA/handoff knowledge is covered above; no enterprise installers or runtime are bundled. |

The marketplace contains multiple suites, not a standalone free creative engine. Method reuse does not certify every upstream skill, reproduce every proprietary operation or make other Studio providers free. Generic existing capabilities are reused instead of duplicating their implementation.

## Installation, rights and evidence

The full upstream suite is not offered for installation: owner decision 2026-10-29 removed it from Studio's recommendations and did not move it to FrameCore Works Toolbox. This does not disable the adapted knowledge already present in Studio. There are no install/remove commands to run, no Adobe connection to configure and no upstream install test pending for this task. A future request to install a distinct account-free upstream tool would need its own dependency review and authorization.

Use only sources, fonts, templates and brand assets with suitable rights. Apache-2.0 applies to the reviewed repository, not arbitrary media used in a project. Studio adaptations deliberately omit mandatory Adobe preference/routing instructions. Verify local source wiring, run Studio's canonical/full checks and distinguish saved-plugin readback from fresh installed-client behavior. Keep current evidence in repository-only verification records; do not claim a service test from a textual scenario.
