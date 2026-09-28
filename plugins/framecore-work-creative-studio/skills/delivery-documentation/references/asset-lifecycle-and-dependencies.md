# Asset lifecycle and dependency discipline

Use for several related files, reference packs, masters, variants, resumable work or a changed source. For one simple text answer, keep only the useful facts. This is an original Studio workflow, not a DAM integration, storage service or standards-compliance claim. Source checks: 2026-09-28.

## Contents

- [Identify without inventing](#identify-without-inventing)
- [Reference authority](#reference-authority)
- [Revision and change impact](#revision-and-change-impact)
- [Time and media evidence](#time-and-media-evidence)
- [Manifest contract and helper](#manifest-contract-and-helper)
- [Worked recovery](#worked-recovery)
- [Handoff and acceptance](#handoff-and-acceptance)
- [Source basis](#source-basis)

## Identify without inventing

Separate asset identity, revision, location, role and evidence. A filename is a locator; `final` in a name is not an acceptance record. A master is the approved source for a stated downstream purpose, not necessarily the largest file. A proxy can support framing decisions without proving texture, colour or audio quality of the original.

Use a stable project-scoped ID such as `product-front`, then revisions such as `r001`. Keep a simple documented filename convention, for example `harbor_product-front_r003.png`; format/size variants get separate IDs. Do not rename existing user files merely to impose a convention. Do not put confidential personal information into publicly exposed names.

Track planned, present and missing separately. `present` records the operator's declaration that the content is available; the manifest helper does not open or verify it. Preserve an available locator or inline text reference. Leave the hash null unless actually computed; a declared SHA-256 is not proof of inspection. A byte hash can help distinguish file changes, but cannot establish authorship, licensing, truth or aesthetic quality.

Keep provenance as source locator/person/operation plus known limitations. Record rights information actually supplied or verified and the permitted use; unknown stays unknown. Do not infer permission from a public URL, watermark absence or provenance badge. Content credentials and their absence require bounded interpretation. Do not remove metadata or upload materials merely to fill a record.

## Reference authority

Assign each reference a job before using it:

| Role | May govern | Must not silently govern |
|---|---|---|
| Identity | Person/object identity features established by the source | Pose, framing or copied background unless selected |
| Product truth | Shape, label, components, packaging facts | Unsupported benefits or unseen surfaces |
| Wardrobe | Garment construction, pattern and fit references | Wearer's identity or unobserved reverse view |
| Composition | Hierarchy, viewpoint, relative placement | Source person's face or protected copy |
| Lighting/material | Highlight/shadow behaviour and material response | Unrelated product geometry |
| Continuity master | Approved state for a specified sequence | A new timeline, audio track or arbitrary animation |
| Inspiration | A technique or association to reinterpret | Exact duplication, factual authority or execution permission |

One asset may have multiple explicitly selected roles. Conflicting authorities need a decision at the affected property, not a blended average. Keep original files intact; separate proposed crops, masks and derivatives. A screenshot of a reference collection is not automatically the individual source asset a generator needs.

## Revision and change impact

Pin each derivative to the exact revisions used, including selected copy, source image, shot plan and audio master where relevant. Keep historical manifests when revising a project. Replacing a file under an unchanged name still requires a new revision if its content changes. A location-only move with verified unchanged content can keep its revision.

The helper represents one selected revision per asset ID per snapshot. Keep a separate candidate snapshot while a replacement is pending; retain the previously accepted delivery snapshot and its explicit selection. Adopt the candidate only after the applicable checks. Do not replace the selected accepted revision merely because a newer draft exists.

When something changes:

1. Describe the actual delta and affected locks. Preserve the user's authorization scope.
2. Create a new source revision and retain its predecessor in project history.
3. Find direct dependents and then their dependents. Keep unrelated assets outside this set.
4. Mark historical acceptance as belonging to its old input basis. Reassess affected criteria before asserting current acceptance.
5. Rebuild or amend only the artifacts that need it. Record why an affected artifact remains valid when inspection supports that conclusion.
6. Pin the newly used revisions and review the resulting content. Never simply update dependency numbers to make a validator pass.

This is conservative change impact, not proof that every descendant's pixels must change. A label correction might require exact-copy review of poster, motion close-up and captions; a relocated source may need only a location update. When an effect is unknown, keep the affected output pending, not silently approved.

Use [asset change routing](../../workflow-orchestrator/references/asset-change-routing.md) to select the actual creative owner. Delivery records the result; it does not become the author or reviewer for every medium.

## Time and media evidence

For a clip, distinguish source range, placement in a sequence, inspected range and requested range. State units and the actual timebase where known; do not translate frames into seconds without a known rate. OpenTimelineIO's range documentation distinguishes media-relative and parent-relative time, and allows requested source ranges beyond available media for workflows that request new material. Therefore an oversized request is a production gap to classify, not automatic proof of a corrupt file.

Example, explicitly hypothetical: requested segment is 12–18 s, available source is 0–15 s. The 15–18 s tail is not available evidence. Plan an authorized extension, another take or a changed cut; do not report the requested six seconds as an inspected six-second clip. A dissolve may require handles outside the visible cut. An OTIO-style edit description refers to media; it does not imply that the referenced media was delivered. No OTIO exporter is bundled here.

For any property, preserve `requested`, `verified` and `unknown` separately. Verified entries contain a value, method and evidence locator/scope. Requested 48 kHz is not verified 48 kHz; a filename ending `.wav` establishes neither. A user-reported BPM stays a report until inspected through an appropriate method.

## Manifest contract and helper

Use [the blank manifest](../assets/project-manifest.template.json) or [the fictional worked manifest](../assets/project-manifest.example.json). The example declares hypothetical present assets solely to demonstrate the data contract; those media files are not included. Do not copy its acceptance records into real projects.

Required top-level fields: `schema_version: 1`, `project_id`, `assets`, `deliverables`. Each asset contains:

| Field | Contract |
|---|---|
| `id`, `revision`, `kind`, `role` | Nonempty identifiers/text; kind is text, image, audio, video, board or other |
| `state`, `locator`, `sha256` | planned/present/missing; present requires a locator; hash null or 64 hexadecimal characters |
| `depends_on` | Exact `{id, revision}` pairs; one current revision per asset ID in this snapshot |
| `properties` | requested object, verified object, unknown array; each verified value has method and evidence |
| `review` | status not_reviewed/accepted/changes_required; accepted needs reviewed_revision, scope, evidence and a basis matching declared dependencies |
| `provenance` | Nonempty source and rights statements; write Unknown when genuinely unknown |

`deliverables` records `{id, purpose}` with purpose `draft`, `reference` or `final`. Final assets must be present, accepted for their current revision and free of stale dependency chains, planned source dependencies or upstream `changes_required` records. Draft/reference delivery may intentionally include unreviewed material, clearly labelled. Previously accepted content that becomes temporarily missing retains its historical review; selecting that missing asset itself as final still fails. Its existing derivatives may retain acceptance, but any new source-fidelity inspection remains bounded by actual access. The helper checks recorded consistency, not whether the reviewer told the truth or inspected enough.

`depends_on` means inputs actually used to author/produce the artifact. Future execution requirements for a completed prompt specification belong in an optional `planned_inputs` note, not a false claim that future media was used already. That note is informational and not validated by the helper. A complete conditional prompt pack can be accepted as text while future rendering remains pending.

From the plugin root, using a Python 3 environment when available:

```sh
python3 skills/delivery-documentation/scripts/asset_manifest.py check project-manifest.json
python3 skills/delivery-documentation/scripts/asset_manifest.py impact project-manifest.json product-front
```

`check` returns structural errors, stale assets, unready assets and final-delivery issues; exit 1 means the declared final delivery or structure needs correction. `impact` returns transitive descendants of the supplied changed IDs; it does not modify the manifest or media. Unknown IDs and malformed graphs fail explicitly. Cycles, duplicate IDs and missing dependency IDs are invalid. A stale revision is reported even when the affected asset is not selected for final delivery. No network request, upload, generation, deletion, hashing or media inspection is performed by this helper. Run it only when execution is actually available; otherwise apply the same contract manually.

## Worked recovery

The example has `product-front@r002` → `poster@r003` → `portrait@r001` and an independent `lyric@r001`. All are fictional. Imagine the actual product label changes:

- Register `product-front@r003`; the current poster still records `product-front@r002`.
- `check` identifies poster and portrait as stale, even though portrait still points to the unchanged poster revision. The old approval cannot silently travel through that chain.
- `impact ... product-front` returns poster and portrait, excluding lyric.
- Reinspect the source/product truth; ask the static direction/image owner for the narrow repair. Keep selected copy and approved layout locks unless the change affects them.
- Inspect the actual repaired poster, then the portrait adaptation. Record new revisions, dependency basis, review scope and actual evidence. Restore final selection only when those records are true.

If the product is instead temporarily unavailable, keep its metadata and mark it missing. A historical derivative does not disappear, but re-verifying its fidelity may be blocked. Never fabricate the source, hash or review to complete a manifest.

## Handoff and acceptance

Return an actual deliverable list with purpose and status, not a folder-wide wildcard. Distinguish accepted for concept, accepted for exact copy, accepted for temporal continuity and verified for technical delivery. The manifest's single review record summarizes the applicable scopes; detailed records stay linked in evidence. No numerical aggregate score can cancel a failed mandatory requirement.

Include outstanding dependencies, requested/verified/unknown properties and the next action. Honor the host's storage requirements and the user's authorized transfer/publication scope. A manifest is not persistent memory, an upload authorization, a rights certificate, a C2PA validator or a production export.

## Source basis

| Source, checked 2026-09-28 | Supported finding | Applied decision / limit |
|---|---|---|
| [W3C PROV Primer](https://www.w3.org/TR/prov-primer/), §2 and §3.6 | Revision and derivation can be represented separately | Pin source versions; the Studio helper is an original local convention, not PROV compliance |
| [NARA naming guidance](https://records-express.blogs.archives.gov/2017/08/22/best-practices-for-file-naming/) and [Harvard naming guidance](https://datamanagement.hms.harvard.edu/plan-design/file-naming-conventions) | Consistent naming, documented metadata and versions help retrieval | Use a concise scheme; their differing length recommendations are not universal constraints |
| [OpenTimelineIO Time Ranges](https://opentimelineio.readthedocs.io/en/latest/tutorials/time-ranges.html), accessed documentation labelled 0.19.0.dev1 | Source, available and parent-relative ranges have different meanings | Preserve time context and media gaps; no claim of a stable-version adapter |
| [C2PA 2.0 specification](https://spec.c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html), Introduction | Validation concerns bound provenance assertions, not a value judgment about content | A provenance record is not creative or factual acceptance |
| [C2PA 2.4 Security Considerations](https://spec.c2pa.org/specifications/specifications/2.4/security/Security_Considerations.html), §2.3 and security discussion | Complete provenance-manifest removal is possible | Missing credentials alone cannot establish falsification; no C2PA verification is bundled |

Library of Congress PREMIS pages were discovered but their full bodies could not be retrieved during this research. They are not treated as read evidence or as a compliance basis for this implementation.
