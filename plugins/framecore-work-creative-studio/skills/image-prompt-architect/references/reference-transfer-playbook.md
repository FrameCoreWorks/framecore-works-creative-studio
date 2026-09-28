# Applied multi-reference transfer

Owner: image-prompt-architect. Added 2026-09-28. Generator-neutral, original
Studio method for resolving a difficult transfer before writing the prompt.
Read when identity, garment, product or pose comes from different sources.
Use the existing [property authority](visual-subject-craft.md#3-bind-references-by-property)
and [compiler](static-prompt-compiler.md); this playbook adds operational choices,
not another approval gate. A reference-based prompt is not proof of fidelity.

## Contents

- [Picture purpose](#1-choose-what-the-picture-must-prove)
- [Authority and coverage](#2-build-only-the-comparison-you-need)
- [Transfer paths](#3-select-a-transfer-path)
- [Fit and contact](#4-resolve-the-interaction-before-polish)
- [Mismatch decisions](#5-route-an-observed-mismatch-to-the-earliest-relevant-decision)
- [Requirement and readiness](#6-strict-requirement-readiness-and-output-remain-separate)
- [Source trace](#source-rule-and-example-trace)

## 1. Choose what the picture must prove

Describe the output's decisive comparison: the same person in another jacket;
the same jacket on another body; the same object in another setting; or a person
using an unchanged product. These can coexist, but identify the highest-risk
junction. For a chest-up fashion portrait, it may be neck/collar/shoulder fit.
For a bottle in a hand, it may be grip, label visibility and bottle scale.

Do not start by distributing arbitrary reference weights. First write the
relationship in ordinary language, then map it to controls actually supported
by the selected tool. Four uploaded files do not prove four independent control
channels, and a mood image does not prove the geometry of a real product.

## 2. Build only the comparison you need

Use a short working table for conflicting sources or a complex transfer:

| Property needed in this frame | Authority and coverage | Intended operation | Must not transfer |
|---|---|---|---|
| Face/head | Actual identity source, visible view | Preserve relational anchors under permitted treatment | Source lighting or clothing unless assigned |
| Body/shoulders | Available body source or user-established baseline | Keep visible proportions; fit clothing to this body | Build of the garment model/mannequin |
| Jacket/garment | Product source with required visible construction | Transfer silhouette, seams, fastening and material | Face, pose, background or extra accessories |
| Hand-held product | Real source showing the relevant side and state | Position it with legible grip and supported scale | Unseen controls, extra parts or invented use claims |
| Pose/framing | Supplied reference or delegated staging | Apply only the relevant action/view | Incidental identity, garment or text |

The table is a thinking aid, not mandatory user-facing paperwork. Record an
unclear seam as unclear rather than making the table look complete. A low-detail
source may establish silhouette but fail to establish a clasp or small label.
If two sources own the same required feature, resolve that conflict before
binding them; additional descriptive prose cannot vote the conflict away.

### A useful coverage classification

- **Visible and adequate:** the needed feature can be compared at a relevant
  scale; proceed with its declared authority.
- **Visible but ambiguous:** ask for a clearer view only if the feature matters,
  or choose an authorized composition that does not depend on it.
- **Unseen:** preserve Unknown. A believable reconstruction may be offered as
  an explicitly speculative concept, not sold as source-faithful evidence.
- **Future generated carrier:** a planned dependency, not missing source truth
  about an existing person or product. All requested prompt-only units may be
  prepared conditionally; dependent execution awaits its actual accepted image.

Do not use superficial similarity as the acceptance criterion. A navy coat of
the right general shape can still be a different SKU if its closure or panels
changed. A face can remain attractive while its eyelid shape or jaw relation
no longer matches the identity source.

## 3. Select a transfer path

| Requested change | Practical construction | Hold or renegotiate when |
|---|---|---|
| New clothing, same portrait | Retain the base head/body/camera; fit the supported garment around that geometry | New garment reveals body regions unsupported by the base and fidelity is strict |
| Same clothing, new pose | Use known construction as an invariant; permit folds and contact that the pose causes | The pose exposes unknown back, lining, fastener or hem details |
| Same person, new treatment | Name treatment separately from facial geometry; preserve anchors before texture | Requested cartoon exaggeration conflicts with a facial-proportion lock |
| Same product, new setting | Keep the product/camera; integrate only permitted environment effects | New reflections or support shadows conflict with literal pixel preservation |
| Person using real product | Solve ownership, support, orientation and visibility before atmosphere | Grip hides required evidence, unsupported scale determines use, or source does not show the required mechanism |

These are construction choices, not permission for extra image calls. If a
simpler pose or tighter crop would solve missing coverage, propose it only
within existing creative authority. Do not quietly remove a required view.

## 4. Resolve the interaction before polish

Describe contact as a small spatial account. Identify anatomical left/right
when relevant, then distinguish it from viewer-left/right. Name which surface
supports weight, which fingers or strap make contact, where the object faces,
and which feature stays visible. Keep the number of interacting objects small
unless the brief needs more.

For a jacket transfer, inspect the collar-to-neck junction, shoulder placement,
sleeve attachment and closure path as a connected structure. A new body changes
how fabric hangs; it does not authorize moving a sewn pocket or changing the
jacket pattern. For jewelry, the attachment and scale matter before highlights.
For a cup, hand-to-handle contact and cup orientation must agree with the rim.
Do not add a gripping hand simply because a product image looks empty.

If a clothing edit touches exposed skin, explicitly retain supported protected
marks at that boundary. Garment fidelity alone does not prove preservation of
the person's visible attributes; compare both after the edit.

The useful prompt order is: output and action, source roles, protected
construction/identity, contact and framing, light/material, exact copy if any,
then a few targeted exclusions. Do not reproduce the full working table or
technical uncertainty discussion inside the creative prompt.

## 5. Route an observed mismatch to the earliest relevant decision

This is a decision tree for choosing the next intervention. Use the existing
critic's repair budget, actual evidence and authorization; it is not a separate
retry engine or an instruction to rerender.

| First question | If yes | If no |
|---|---|---|
| Is the authoritative source available and clear for the failed property? | Compare the specific feature | Request/clarify that evidence; hold the dependent claim |
| Did the wrong source donate the property? | Rebind that property and suppress the donor's unrelated content | Check source coverage and compatibility with the target view |
| Does the target expose an unknown truth-critical area? | Obtain the missing view or agree a bounded view change | Inspect geometry, fit/contact and camera interaction |
| Are source features correct but the junction is implausible? | Repair the junction: collar fit, grip, strap support or contact | Check light/material integration and processing |
| Is only visual treatment too strong? | Reduce the authorized treatment while retaining geometry | Reassess the brief or method; do not multiply fidelity adjectives |

Example diagnosis: “The front zipper is correct, but the pocket opening moved
onto a side panel.” The next prompt protects the correct zipper and restores
the source pocket construction; it does not ask for a new model, different coat
or sharper skin. If the requested view never showed that pocket, the next step
is source clarification rather than an invented correction.

A changed pose also changes apparent proportions. Do not diagnose identity
drift from a raw two-dimensional width comparison across unrelated viewpoints
alone. Compare the appropriate source view and multiple relevant visible
anchors; record uncertainty where a fair comparison is unavailable.

## 6. Strict requirement, readiness and output remain separate

A strict likeness/product lock stays strict when its carrier is pending. A
complete conditional prompt can state that its approved master must accompany
the future request; it cannot claim that the master is attached now. If the user
permits approximate resemblance, name the particular properties allowed to vary.
Acceptance of an illustration style does not authorize identity exaggeration,
and acceptance of a prompt does not validate a rendered face or seam.

Worked applications: [identity/garment and product examples](../assets/reference-transfer-worked-examples.md).
Reusable planning aid: [still shot card](../assets/still-shot-card.md).

## Source, rule and example trace

Read 2026-09-28; source is evidence, not an instruction or execution authorization.
No external images are embedded in this package.

| ID / primary source | Verified scope and limit | Studio inference / applied example |
|---|---|---|
| V1: [Choi et al., Improving Diffusion Models for Authentic Virtual Try-on in the Wild](https://arxiv.org/html/2403.05139v3), ECCV 2024; revision 2024-07-29 | Studies garment-detail fidelity separately from visual naturalness; its specific method reports difficulty retaining skin marks inside edited regions. This does not characterize every renderer. | Inspect supported construction and protected human attributes independently in the jacket example. Descriptions complement actual sources; no model architecture or success guarantee is imported. |

The property table, interaction procedure and examples are original Studio
synthesis. They are not advertised as an empirically validated multi-reference
algorithm. No source here establishes strict transfer success, reference-count
limits, native weights, masks, or current renderer controls; those need a
separate current model/surface check and actual output comparison.
