# Reference authority and carriers

This reference defines how sequence and board work identify the authority of
uploaded assets and how continuity information is transported to an actual
downstream request. It synthesizes selected Visual Prompter K07/K15/K18,
Video Prompter K09/K14/K15/K18, Storyboard & Reference Board Creator
ROOT/META/K01-K04, and Workflow Kit storyboard contracts/examples. It is
generator-agnostic stable craft; current model input rules must be checked
separately. It is not a claim that any file is attached to a later tool call.

Related contracts: [sequence contract](sequence-contract-and-continuity.md),
[board layout](../../storyboard-board-architect/references/board-layout-and-copy.md),
[delivery and handoffs](../../storyboard-board-architect/references/board-delivery-and-handoffs.md).

## 1. A file can govern one property, not everything

Treat every image, clip, board, document, or written note as a source with a
bounded role. Useful property categories include:

- identity/likeness and which visible details are authoritative;
- product model, packaging, label topology, color, material, and mechanism;
- costume/wardrobe, accessories, and fit;
- location architecture, screen geography, and light;
- composition, crop, angle, or subject placement;
- styling, palette, texture, period, or mood;
- opening/end pose, prop state, or an exact action transition;
- motion cadence, acting reference, camera path, or framing behavior;
- exact copy, dialogue, shot order, duration target, or factual brief.

Never assume an asset owns all properties because it was uploaded first or is
visually compelling. A packshot might govern label layout and silhouette while
a separate art reference governs color treatment. An inspiration image may
inform broad visual principles but must not become logo, identity, or product
truth authority.

## 2. Build an authority map with provenance

For each relevant property, record:

| Attribute | Record |
|---|---|
| Property | The exact fact being controlled |
| Authority | User approval, supplied asset, accepted script/version, or proposal |
| Asset | Human-readable alias/ID that maps unambiguously to an available file |
| Role | Governs, informs, reference-only, edit base, or explicitly suppressed |
| Scope | Which scene, shot, panel, crop, or graphic receives it |
| Preserve | What must remain unchanged or transfer exactly |
| Suppress | Incidental features that must not transfer |
| Conflict | Competing source and specific unresolved property |
| Request binding | Planned, available in chat, bound to this job, or submitted |

Use stable aliases only after resolving them against actual assets. If a user
calls a file `@img3`, retain that alias and its assigned role unless the user
changes it. Do not renumber images based on a new file ordering. A filename,
mention, screenshot of an upload list, or conversation memory does not prove
the file is present in a downstream request. For a future generated carrier,
a planned dependency ID may be recorded separately; explicitly mark it planned
rather than presenting it as a resolved asset alias or existing attachment.

## 3. Resolve conflicts without silently merging

When two sources disagree, identify the conflict by property. Ask the smallest
decision that would change the output. Example: a supplied product packshot
shows a blue cap, while the approved product sheet specifies a white cap. Do
not average the colors or let the latest inspiration image win by default.

Authority can be revised by the user. Record which newer approval supersedes
which older value and where the change propagates. If authority remains
unknown, mark the affected design provisional or avoid showing that detail.
Do not ask about unrelated properties simply because another conflict exists.

Exact copy is a separate authority class: retain exact user-approved strings,
including punctuation, diacritics, numbers, case and language. Layout may
change line breaks only if allowed; never paraphrase or translate a locked
string. A proposed tagline is not approved just because it appears in a
reference. See [board layout and copy](../../storyboard-board-architect/references/board-layout-and-copy.md).

## 4. Continuity has three states, not one promise

Distinguish these concepts in both plans and handoffs:

1. **Continuity requirement:** strict or approximate, per property and shot.
2. **Input readiness:** whether the required source/carrier is available and
   correctly bound to the exact independent request.
3. **Observed result:** whether the output was actually inspected and
   accepted against the contract.

“Strict identity continuity” is a requirement, not proof of readiness. An
attached image can make an input carrier-ready, not guarantee a correct output.
A concept description may permit approximate continuity without a carrier.
After real QA, a shot might still fail or need bounded repair.

### Strict continuity

Use only when preserving a property is materially required: recognizable
person, exact product/SKU, wardrobe, location geometry, object state, starting
frame, or motion continuation. Identify a source that actually represents the
property and attach/bind it to each independent request that relies on it. For
source-video continuation, bind the source clip to the specific operation. For
frame-chained work, pass the accepted frame as the actual next input. Shared
context counts only if the target surface documents and exposes it for that
exact job.

If strict continuity lacks a carrier, preserve the strict requirement and mark
input readiness pending; do not claim repeated text or a seed will achieve it.
Request/bind the source or prepare a conditional plan. Simplification or a change
to approximate continuity requires the user's authorization for that property;
missing evidence is not permission to relax it. The exact model/surface may
impose constraints on reference types; verify current support through research
and the relevant prompt skill.

For prompt-only plans, a master or chained frame that will be generated later
need not exist before all requested cards and independent prompt drafts can be
written. Record it as a planned dependency, state the binding requirement in
each dependent prompt, and mark that prompt not ready for execution until the
real accepted carrier is supplied. Do not call a planned alias an attachment,
invent its unseen properties, or present the pack as continuity-validated.
An existing identity/product/source-edit asset whose pixels are necessary to
know the requested content is different: request that source and hold only the
source-dependent details, while completing independent planning where useful.

### Approximate continuity

Suitable for exploratory work where resemblance, palette, or broad spatial
family is enough. State which properties may drift and which remain locked.
Natural-language descriptions, mood boards, and reused seeds may guide a
family resemblance, but do not provide strict identity, exact layout, or
physical-state continuity.

## 5. A board, keyframe, or shot card is not automatically a carrier

A storyboard board is a designed comparison sheet. Its panel may be tiny,
cropped, labeled, illustrative, or one of several alternatives. The entire
board may contain gutters, typography, arrows, and multiple images that are
not intended to appear in the generated shot. Do not bind the whole sheet as a
single video source and assume the model understands which cell is authoritative.

A keyframe is not a carrier until the selected image itself is available,
approved for that role, and attached/bound to the exact request. A shot card is
text; it can specify intended state but cannot physically transport source
pixels or clip history. A verbal description of a carrier is not the carrier.

For every downstream prompt, produce a carrier check:

| Check | Required answer |
|---|---|
| What property needs continuity? | e.g. identity, product label, entry pose |
| Which source carries it? | resolved alias and source role |
| Is that source actually present in this request? | yes/no/unknown, not intended/mentioned |
| Is it suitable for this property and operation? | evidence or unknown |
| Strict or approximate? | explicit requirement level |
| What happens if absent? | request/bind source or mark pending; relax only with explicit authorization; hold only dependent execution |

One sequence may include both strict and approximate relations. A strict
opening identity might need a portrait carrier, while a noncritical empty
hallway may be a text-only independent shot. Make the requirement local; do
not overburden every request with every reference.

## 6. Source clips, edit bases, and chained frames

For edit, extend, or I2V workflows, distinguish the source of truth from
inspiration:

- **Edit base:** exact image/clip to transform; preserves the aspects the user
  asked to keep.
- **Start/end frame:** actual image bound to a documented operation; it may
  define only a particular boundary.
- **Style/reference asset:** informs scoped properties, not necessarily
  temporal state.
- **Frame-chain carrier:** the accepted terminal frame used to start a new
  independent generation; it must pass drift review first.
- **Reference board:** comparison/context aid, not interchangeable with any of
  the above.

Do not call an image-to-video operation an edit of the board unless the exact
selected board panel is the user's edit base and the desired transformation is
clear. Do not assume an extension follows from a text description; a real
source clip and supported operation are needed.

In a chain, preserve the original approved master as the comparison anchor.
Drift can accumulate if each new frame is compared only to the previous one.
Track what was accepted, what changed, and which exact carrier starts the next
request. If no image/clip tool is available, deliver a binding plan, not a
claim of attached assets.

## 7. Handoff record without false memory

A concise, portable resume record may state project/sequence ID and version,
approved facts, exact text locks, per-property authority, shot IDs, accepted
states, source aliases/roles, actual attachments still available, strict vs
approximate continuity, and unresolved decisions. Do not place credentials,
private absolute file paths, or hidden reasoning in a portable brief.

Never promise that a new chat, model, tool call, plugin or downstream agent
remembers a prior file or output. Repeat the relevant facts and include the
actual carrier in the new request. The record tells the user what must be
re-attached; it does not attach it itself.
