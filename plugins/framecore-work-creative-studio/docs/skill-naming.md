# Skill display-name standard

Applies to every canonical `skills/<id>/SKILL.md` in FrameCore Works Creative Studio, including compatibility entrypoints. Vendored source snapshots are immutable and are not renamed.

## Rules

- Keep the existing technical ID in lowercase kebab-case. The directory, frontmatter `name`, invocation, links and routing keep this ID.
- Require `agents/openai.yaml` for every canonical skill. Put the user-facing name under `interface.display_name`, never under `metadata`.
- Use English names with one space between words and an uppercase first letter for each ordinary word. A new skill derives its name from its ID (separator hyphens become spaces) unless the owner approves a role name for it; the approved names are listed below and in the validator's map.
- Preserve these spellings: `AI`, `UGC`, `HyperFrames`, `OpenCut`, `FrameCut`. Ordinary names such as `Ecommerce` retain their existing spelling. Add a documented spelling exception in the canonical validator when a future tool or acronym needs one.
- Use a double-quoted string on its own `  display_name:` line directly under `interface`. The field controls UI presentation; it is not an instruction to change skill identity.
- Require `interface.short_description` alongside the display name in every included agent metadata file. Use one double-quoted `  short_description:` string of 25–64 characters that describes the existing skill. OpenAI's [plugin metadata checks](https://developers.openai.com/plugins/deploy/submission-errors#skill-agent-metadata-errors) require a nonempty short description when `agents/openai.yaml` is included.
- Preserve other existing metadata, prompts and invocation policies. Adding the required short description does not require a new starter prompt or policy override. Put any existing invocation policy under `policy.allow_implicit_invocation`.
- New skills must follow this standard before release. `scripts/validate-studio.mjs` checks every canonical root for a present, correctly located, unique and correctly formatted display name and a valid short description. `scripts/package_release.py` runs that gate before packaging. Source checks do not establish registration in an active client.

## Owner-approved role names (2026-10-24)

The owner approved plain role names for the skills, keeping two brand names: **FrameCore Studio Guide** for `workflow-orchestrator` and **FrameCut** for `opencut-video-studio`. FrameMotion, FrameBoard, FrameCheck and FrameShot were rejected because existing products in the same field use them (evidence in the repository's `docs/handover-development-proposals-2026-10-24.md`). Only the displayed name changed: technical IDs, invocations, paths, routing and internal artifact types stay the same, and OpenCut compatibility remains. `scripts/validate-studio.mjs` holds the same map, so a changed name needs the owner's approval and an edit in both places. Older records and vendored snapshots keep the names they were written with.

## Canonical names

| Technical ID | Display name |
|---|---|
| `asset-manifest` | Asset Manifest |
| `audio-production-director` | Audio Production |
| `brief-architect` | Brief Architect |
| `caption-studio` | Caption Studio |
| `character-design` | Character Design |
| `cinematography` | Camera And Light |
| `commercial-video-campaign-director` | Video Campaign |
| `commercial-visual-campaign-director` | Visual Campaign |
| `copy-voice` | Copy Voice |
| `creative-music-video-director` | Music Video |
| `creative-video-producer` | Video Producer |
| `delivery-documentation` | Delivery Pack |
| `ecommerce-campaign-strategy-director` | Sales Campaign Strategy |
| `hipson-adapter` | Hipson Handoff |
| `humanizer` | Copy Polish |
| `hyperframes-workflow` | Motion Graphics |
| `image-prompt-architect` | Image Prompt |
| `instruction-packet-factory` | Task Handoff |
| `marketing` | Brand Strategy |
| `opencut-video-studio` | FrameCut |
| `output-critic-iteration` | Output Review |
| `pipeline-core` | Studio Core |
| `producer-ai-task-builder` | Producer AI Task Builder |
| `reference-pack-curator` | Reference Pack |
| `remotion-video-production` | Remotion Video |
| `research-evidence` | Research |
| `screenplay-story-architect` | Story And Screenplay |
| `static-graphic-design-creator` | Graphic Design |
| `storyboard-board-architect` | Storyboard Board |
| `storyboard-sequence-architect` | Shot Sequence |
| `storytelling` | Story Logic |
| `studio-workstyle-profile` | Workstyle Profile |
| `tool-routing-cost` | Tools And Costs |
| `ugc` | UGC Ads |
| `video-prompt-architect` | Video Prompt |
| `workflow-orchestrator` | FrameCore Studio Guide |
| `workflow-self-improvement` | Studio Retrospective |
