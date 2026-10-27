---
name: reference-pack-curator
description: Sort supplied references into canonical sources, mood or style inspiration and exclusions, with aliases and conflicts, before direction or prompts. File inventory goes to Asset Manifest.
---

# Reference Pack

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions. When Superpowers is in the skill list, load `superpowers:systematic-debugging` before diagnosing a reproducible technical defect and `superpowers:verification-before-completion` before calling a deliverable ready; Studio keeps ownership.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


Use this skill to structure references into source authority, aliases, role tags, suppression rules, conflicts, and continuity anchors before direction, character, storyboard, or prompt work.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- The user provides images, links, notes, examples, mood references, or source material.
- Downstream roles need to know what is canonical, inspirational, conflicting, or forbidden.
- Continuity anchors must be protected across image, video, storyboard, or coded-video work.

Do not use this skill to write final prompts, change the brief, or invent reference authority.

For poster rebuilds, packaging, logos, identity or narrow graphic edits, read
[static graphic source authority](references/static-graphic-source-authority.md).
Assign protection per property and preserve the actual current edit source.

## Openverse Reference Base

When the user needs reference or usable images or sounds and has none to supply, search [Openverse](https://openverse.org) first: over 800 million openly licensed images and audio tracks (no video), no key or installation. Where Python runs with internet access, run this skill's `scripts/openverse.py` by its absolute path (resolve it from this skill's folder first, since commands run in the user's working directory): `python3 <skill folder>/scripts/openverse.py "<query>"`, adding `--media audio` for sound; otherwise open `https://api.openverse.org/v1/images/?q=<query>&license_type=commercial,modification` (or `/v1/audio/`) with the host's web tool, and when neither works give the user the `https://openverse.org/search/image?q=<query>&license_type=commercial,modification` link (`/search/audio` for sound). Keep the default filter (commercial use, modification allowed) unless the use is private study. For each chosen work carry its licence, source page and attribution line into the [asset manifest](../asset-manifest/SKILL.md), and say its warnings (share-alike, unknown creator). Openverse does not verify licences: the source page decides before client use. A found work is a reference like any other: tag it canonical, inspiration or excluded here. A failure prints its `error_type`. On a `cloudflare_challenge` (this network is blocked by Openverse's Cloudflare check; never retry the script) or a persistent `server_error` or `timeout`, tell the user plainly what failed, in their words (blocked network or Openverse outage, and which materials could not be fetched), and ask one question with numbered answers: stop here, or continue another way, listing the routes actually available here (the same API URL through the host's own web tool, the search link for the user to pick by hand, another permitted source named as such). Wait for the answer; never switch source silently and never claim Openverse for a work from elsewhere. Report which route delivered each work (owner decision 2026-10-27).

## Inputs

Required:

- `brief_contract`: objective, constraints, audience, and acceptance criteria.
- `raw_references`: files, links, descriptions, screenshots, or source notes.
- `reference_needs`: what downstream roles need from references.

Optional:

- `aliases`: user shorthand for images, people, products, places, or motifs.
- `suppression_rules`: elements to avoid.
- `conflict_notes`: known contradictions between references.

## Outputs

Produce a Reference Pack with:

- canonical references and their roles
- control ownership and attachment requirements for references that must carry strict continuity
- mood, style, example, and exclusion references separated
- aliases and continuity anchors
- suppression rules
- conflicts and resolution notes
- handoff requirements for direction or prompting

## Process

1. Classify each reference by authority, purpose, and permitted control: identity, source, style, motion, performance, audio, or coverage.
2. Separate canonical source from mood or style inspiration.
3. Capture aliases and continuity anchors.
4. Record suppression rules and conflicts clearly.
5. Hand off only the reference meaning, not raw clutter.

## Decision Rules

- Canonical beats inspirational when they conflict.
- If reference authority is unclear, ask or label it as uncertain.
- Keep style inspiration from overriding product, character, or copy requirements.
- For a strict lock, record the alias that must be attached to each affected generation unit. A role tag alone is not a continuity carrier.
- Do not use private references not provided or approved for the task.

## Guardrails

- Do not invent source authority or claim verification that was not performed.
- Do not include private links, credentials, local-only paths, or unapproved personal data.
- Do not write final prompts or direction contracts.
- Do not erase conflicts; document how they should be handled.

## Handoff

Review gate: `reference_authority_fit`.

Hand off to `static-direction`, `motion-direction`, `music-video-direction`, `storyboard-architect`, or prompt roles with:

- `reference_pack`
- `continuity_anchors`
- `reference_roles` and `control_ownership`
- `attachment_requirements`
- `suppression_rules`
- `conflict_notes`
- `reference_gaps`

## QA Checklist

- Canonical, mood, style, and exclusion references are separated.
- Aliases are clear and reusable.
- Conflicts are visible.
- Suppression rules are actionable.
- Reference ownership is explicit enough to prevent style inspiration from overwriting locked source facts.
- Downstream roles can use the pack without reinterpreting raw references.

## View and sheet authority

Use [human identity evidence](../character-design/references/human-identity-workbook.md) when views, orientation or real-person likeness matter, and [production reference sheets](../storyboard-board-architect/references/production-reference-sheets.md) when binding panels to individual sources. Keep unseen geometry Unknown and candidate images distinct from real source evidence.
