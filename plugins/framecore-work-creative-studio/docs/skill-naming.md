# Skill display-name standard

Applies to every canonical `skills/<id>/SKILL.md` in FrameCore Works Creative Studio, including compatibility entrypoints. Vendored source snapshots are immutable and are not renamed.

## Rules

- Keep the existing technical ID in lowercase kebab-case. The directory, frontmatter `name`, invocation, links and routing keep this ID.
- Require `agents/openai.yaml` for every canonical skill. Put the user-facing name under `interface.display_name`, never under `metadata`.
- Use English names with one space between words and an uppercase first letter for each ordinary word. Replace separator hyphens with spaces. Preserve the existing words and order.
- Preserve these spellings: `AI`, `UGC`, `HyperFrames`, `OpenCut`. Ordinary names such as `Ecommerce` retain their existing spelling. Add a documented spelling exception in the canonical validator when a future tool or acronym needs one.
- Use a double-quoted string on its own `  display_name:` line directly under `interface`. The field controls UI presentation; it is not an instruction to change skill identity.
- Require `interface.short_description` alongside the display name in every included agent metadata file. Use one double-quoted `  short_description:` string of 25–64 characters that describes the existing skill. OpenAI's [plugin metadata checks](https://developers.openai.com/plugins/deploy/submission-errors#skill-agent-metadata-errors) require a nonempty short description when `agents/openai.yaml` is included.
- Preserve other existing metadata, prompts and invocation policies. Adding the required short description does not require a new starter prompt or policy override. Put any existing invocation policy under `policy.allow_implicit_invocation`.
- New skills must follow this standard before release. `scripts/validate-studio.mjs` checks every canonical root for a present, correctly located, unique and correctly formatted display name and a valid short description. `scripts/package_release.py` runs that gate before packaging. Source checks do not establish registration in an active client.

## Canonical names

| Technical ID | Display name |
|---|---|
| `asset-manifest` | Asset Manifest |
| `audio-production-director` | Audio Production Director |
| `brief-architect` | Brief Architect |
| `caption-studio` | Caption Studio |
| `character-design` | Character Design |
| `cinematography` | Cinematography |
| `commercial-video-campaign-director` | Commercial Video Campaign Director |
| `commercial-visual-campaign-director` | Commercial Visual Campaign Director |
| `copy-voice` | Copy Voice |
| `creative-music-video-director` | Creative Music Video Director |
| `creative-video-producer` | Creative Video Producer |
| `delivery-documentation` | Delivery Documentation |
| `ecommerce-campaign-strategy-director` | Ecommerce Campaign Strategy Director |
| `hipson-adapter` | Hipson Adapter |
| `humanizer` | Humanizer |
| `hyperframes-workflow` | HyperFrames Workflow |
| `image-prompt-architect` | Image Prompt Architect |
| `instruction-packet-factory` | Instruction Packet Factory |
| `marketing` | Marketing |
| `opencut-video-studio` | OpenCut Video Studio |
| `output-critic-iteration` | Output Critic Iteration |
| `pipeline-core` | Pipeline Core |
| `producer-ai-task-builder` | Producer AI Task Builder |
| `reference-pack-curator` | Reference Pack Curator |
| `remotion-video-production` | Remotion Video Production |
| `research-evidence` | Research Evidence |
| `screenplay-story-architect` | Screenplay Story Architect |
| `static-graphic-design-creator` | Static Graphic Design Creator |
| `storyboard-board-architect` | Storyboard Board Architect |
| `storyboard-sequence-architect` | Storyboard Sequence Architect |
| `storytelling` | Storytelling |
| `studio-workstyle-profile` | Studio Workstyle Profile |
| `tool-routing-cost` | Tool Routing Cost |
| `ugc` | UGC |
| `video-prompt-architect` | Video Prompt Architect |
| `workflow-orchestrator` | Workflow Orchestrator |
| `workflow-self-improvement` | Workflow Self Improvement |
