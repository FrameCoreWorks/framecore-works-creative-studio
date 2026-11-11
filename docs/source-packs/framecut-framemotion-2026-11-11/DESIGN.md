> Portable copy of the earlier planning edition. Read [the packet index](README.md) and the current repository handover for the owner's intake, applicability, implementation and cleanup workflow. Proposals are not automatically approved architecture.

# FrameCut and FrameMotion — knowledge-preserving separation design

Status: **PROPOSAL — PLANNING AND RESEARCH ONLY; NOT APPROVED FOR IMPLEMENTATION.** This extends Claude's November 7–8 plans. The user subsequently authorized actual deep research by separate agent teams. No repository, plugin package, source migration, paid research job or release is created by this document. Claude remains principal architect. The earlier waiver covered the audit, not approval of this architecture; the known Claude OAuth failure has not been retried blindly.

## Intent

Build two independent products that can also serve Creative Studio: FrameMotion understands and executes the craft of motion design; FrameCut understands and executes editorial craft. Both need the reasoning of an experienced practitioner, not merely software terminology or command recipes. Preserve all relevant existing knowledge and capabilities, then deepen and validate the gaps. A successful extraction preserves **intent → human operation → agent decision → code/parameters → final-output review → correction**.

The user's request to isolate all knowledge is interpreted as complete accountable preservation, not indiscriminate publication. Every source gets a destination or an explicit retained/private/licensing/obsolete disposition. Raw manuals, client files, secrets, unlicensed code, obsolete facts and brand preferences do not automatically become public defaults.

## Evidence baseline

- Studio 1.174.1, commit `2942af902909b83441fc4c428d9debd532500c5a`, frozen source under the adjacent audit directory. Recheck main and private release at implementation; these counts do not assert current future HEAD.
- FrameCut owner `skills/opencut-video-studio`: **35 files**. Motion owners `skills/hyperframes-workflow` and `skills/remotion-video-production`: **442 files**. The shared machine inventory covers all **477** with size/hash.
- Source inventories: [integration](EXTRACTION-SUMMARY.md), [motion mapping](EXTRACTION-SUMMARY.md), [cut mapping](EXTRACTION-SUMMARY.md). Supporting rows overlap; do not sum them as distinct knowledge units.
- Existing public/private audit found 55 private additions and two differing manifests; the private FrameCut owner has no replaced files. Seventeen private motion provisioning additions require explicit ownership review. Preserve existing private data; no automatic public promotion.
- Prior audit findings remain open. A copied checker with a false PASS is not a verified release gate. [Prior audit](EXTRACTION-SUMMARY.md).
- Original plans and private historical decisions remain in the local source register, outside this public packet; see EXTRACTION-SUMMARY.md.

## Decisions and assumptions

| ID | Decision | Authority / status |
|---|---|---|
| D01 | Names: FrameCut and FrameMotion; each works standalone and as a Studio companion | Historical user decision, Nov 7–8; reaffirmed by current request |
| D02 | Planning plus actual knowledge research now; no plugin build yet | Current user request and explicit earlier planning-only decision |
| D03 | FrameCut first for implementation; research both in parallel | Proposal, because its owner is smaller; hidden dependencies still require closure |
| D04 | Studio remains the campaign/project orchestrator when it is the caller; a standalone plugin owns its own minimal brief/review | Historical companion direction plus necessary standalone consequence |
| D05 | Copy with provenance first; keep Studio paths/fallback until a separate cutover decision | Existing path protection; no removal authorization |
| D06 | Preserve engine-neutral craft and map only demonstrated engine equivalents | Proposal based on audit API and QC failures |
| D07 | Default canvas/motion-reel and HyperFrames; Remotion optional; original engine locks respected | Historical accepted plan; applicable licensing checked before inclusion/use, no evergreen headcount claim |
| D08 | Initial FrameCut target `plugins/framecut/skills/framecut/`; FrameMotion retains both imported skill-tree names under `plugins/framemotion/` and adds a thin `framemotion` entry | Proposed layout; imported source paths remain untouched in Studio |
| D09 | One canonical owner per knowledge topic; small standalone-required exports may be bundled with source hash/version and generated-update discipline | Proposal; no mandatory third core plugin and no imports into another installation's cache |
| D10 | Existing generic companion major1 plus hashed domain request; preserve stronger FrameCut motion binding | Reuse observed contracts; new operation names/adapters require tests |
| D11 | Host/caller dispatches companions; no recursive companion-to-companion orchestration | Current companion policy; any autonomous child-job proposal is a separate architecture change |
| D12 | Primary documentation establishes feature facts; practitioner accounts establish attributed practice; original examples test our synthesis | Research method, not claim of native-app execution or expert certification |

## Approaches considered

1. **Copy folders and maintain two independent forks.** Fast packaging, but missing caption/font/board dependencies, duplicated contradictory knowledge and drift make this insufficient.
2. **Extract a shared runtime framework first.** Could centralize common code, but creates another install dependency and risks replacing working domain contracts before their real commonality is known.
3. **Incremental domain extraction with explicit local closure and versioned contracts — recommended proposal.** Preserve complete owned trees; localize necessary small components; maintain one canonical topic owner; compare behavior before/after; switch Studio routing only after standalone and companion proof. This fits the already chosen standalone+companion direction and limits unrelated restructuring.

No optional architecture choice in this proposal is recorded as user-approved merely because the user requested a plan.

## Product boundary

| Responsibility | FrameMotion | FrameCut | Studio / other owner |
|---|---|---|---|
| Intention and brief | Motion concept, hierarchy, visual metaphor, animation intent | Editorial premise, selects, scene structure, pacing | Campaign/context and cross-deliverable consistency |
| Time authority | Local composition time from zero, requested rational FPS/frame count | Global edit, source/record time, events, source PTS, audio alignment | Task scheduling; no second master timeline |
| Motion craft | AE concepts, timing/spacing, typography, compositing, 2.5D/3D, responsive/web motion | Basic placement and declared effects; requests complex motion | Brand inputs and copy locks when caller |
| Editorial craft | Motion-sequence rhythm and local sound relationship | Narrative, performance, continuity, trims, split edits, dialogue/music, conform | Broader screenplay/brief where supplied |
| Audio | Cues and motion/music relationship; declared local mix capability | Editorial sound joins, dialogue/music organization and delivery intent | Toolbox/Earshot analysis/model execution; optional supplied results |
| Assets | Consume files plus rights/provenance, create code geometry | Consume footage/audio/stills plus metadata | Open Assets sourcing; no copied asset catalog/model bundle |
| Captions and boards | Needed local rendering subset and resources | Needed local caption/board runtime and resources | Canonical shared component ownership recorded; no missing sibling dependency |
| Knowledge | Canonical motion decision cards | Canonical editorial decision cards | Small versioned cross-domain exports; Studio keeps orchestration knowledge |
| QA | Motion-specific output review and reproducibility | Edit/picture/audio/interchange review | Caller accepts delivery; technical PASS is not creative approval |

FrameMotion is not restricted to vertical social reels. Include brand animation, explainer/data motion, product/3D pieces, titles, compositing, multi-format campaigns, overlays, presentations and web interaction. Support declarations must distinguish implemented exporters from desired formats; SVG/Lottie/Rive/glTF/alpha video are not synonyms for an MP4 export.

FrameCut knows methods from Resolve, Premiere, FCP and Avid without claiming native control or complete feature equivalence. Current limitations such as optical flow, tracking, multicam, managed HDR grading and verified named-NLE import remain explicit until implemented and tested. Knowledge can guide a human handoff where the engine cannot execute.

## Knowledge architecture: preserving judgment

Each product contains five layers, loaded progressively:

1. **Compact entry skill:** recognize task/intention, choose a domain, inspect capabilities, read relevant craft before choosing a tool.
2. **Decision cards:** context and audience; intended effect; diagnosis; alternatives and tradeoffs; manual procedure; supported code mapping; failure mode; review evidence; source/version/date; scope and confidence.
3. **Worked cases:** original positive and wrong alternatives; editable parameters, exact-copy/asset constraints, before/after reasoning and observations. Distinguish calculated examples, source-supported procedures and actual rendered/listened demonstrations.
4. **Evaluation fixtures:** preserve correctness and test transfer to an unfamiliar brief; include deliberately quiet, ambiguous, contradictory and technically-valid-but-wrong examples.
5. **Source/change ledger:** stable claim IDs, source URL/local hash and section, primary/practitioner/local-observation classification, author/rights, import version, supersession and validation state.

A card is not accepted just because its terms occur in a reference file. Routing must cause the relevant material to be read and affect the choice. A reported skill read is not proof the choice was sound; a separate reviewer evaluates rationale and output.

Knowledge states are independent: `IMPORTED_UNVERIFIED`, `SOURCE_SUPPORTED`, `CALCULATION_CHECKED`, `ENGINE_EXERCISED`, `NATIVE_APP_EXERCISED`, `PERCEPTUALLY_REVIEWED`, `USER_ACCEPTED`. None implies the next. A source can be authoritative and still contain outdated or overbroad text. Record conflicts rather than voting by source count.

## Conflicts to resolve explicitly

- Preserve the accepted 1.6-second text-hold heuristic and recordings-first preference as identified defaults with context, not universal empirical standards. Longer text, accessibility, an intentionally quiet piece and an explicit synthesis request may require different choices. The 0.6-second motion preference cannot become compulsory distracting movement on a web page.
- Use the later open-workshop material to explain when cuts, dissolve, bloom, bounce and other techniques are appropriate. Do not turn brand taste into general prohibitions.
- Normal approval uses a displayed revision-bound board receipt. A later recorded one-shot instruction can waive that intermediate approval for its exact scope; self-QA remains. No vague task request is silently converted into waiver or approval.
- Never change a user-locked engine just because the desired look changes. Report a capability gap and propose the alternative.
- A reading-rate formula, loudness target, safe zone, licence threshold, version/API name or legal/platform claim needs a named scope and current evidence. Unlinked Nov 8 assertions are retained as research questions, not shipped facts.
- Bounded defect-driven review stops when the defined checks pass. Conflicting historical minimum/maximum round counts need an explicit policy decision; no mandatory cosmetic rewrite after a pass.

## Contracts and state

Reuse `framecore-task-request/1` and `framecore-task-result/1` from `skills/pipeline-core/assets/companion-contract.schema.json`; validate the selected `$defs`, not the unconstrained root. Proposed provider IDs are `framecut` and `framemotion`. Initial operation vocabulary: `capabilities`, `render`, `review`, `export`; unsupported operations are declared unavailable. These are proposed adapter operations, not current engine CLI commands.

Bind each Studio task to a nonempty task ID, original domain request file hash, source asset hashes, creative revision, requested engine/profile and output specification. Result includes executed commands, actual output hash/size, review evidence, warnings/errors and unexecuted checks. Preserve existing status/readiness semantics; do not introduce a parallel status machine or mark missing review as PASS.

FrameCut's motion request already carries project/sequence/event/deliverable context, local origin zero, duration frames, rational FPS, dimensions/alpha and hashes. Keep `attach-motion --request` and `bind_motion` checks after generic intake. New generic fields do not magically validate domain semantics. Authoring-contract validation belongs to the selected engine adapter.

Studio is authoritative for project-level decisions when caller; standalone entry persists the same minimal principles locally. Engine revision and creative approval revision are distinct. One editor process owns a project revision at a time. Retries are idempotent by task/request identity; changed input invalidates affected evidence. Do not silently rerun a failed companion task in fallback and produce a second accepted output.

## Migration, packaging and rollback

1. Freeze an up-to-date source snapshot and private overlay; generate per-file and per-topic disposition manifests.
2. Preserve imported owner trees in new authorized repositories with notices. Adapt dependencies in explicit reviewed changes, retaining old/new hashes and reasons. Raw private research stays outside distributed packages.
3. Prove standalone operation with Studio physically absent, then companion behavior with Studio present. Resolve resources from each installed package, never machine-specific paths.
4. Introduce Studio entries and explicit transitional selection. A missing companion may use the retained Studio route; failure after execution requires visible recovery choice, not silent rerun.
5. Publish/update only after actual authorization and verified release gates. Each new plugin has its own identity, manifests, source pin, archive hash and private release guard. Existing Studio identity/private overlay is preserved.
6. Remove or replace original paths only in a later explicitly approved cutover. Until then retain the last working Studio route and immutable project/asset receipts. Rollback changes selection, not accepted final files or project schemas in place.

Three manifests means separately validated Agent Plugins/Codex/Claude metadata, not proof of runtime on all hosts. A repository URL is not installation permission. Work must have a demonstrated materialization route that does not rely on unverified GitHub downloads. The current marketplace/prose discrepancy around Toolbox dependencies must be resolved before promising automatic installation.

## Acceptance and staged release

The independent builder check identified two launch-policy ambiguities. [LAUNCH-DECISIONS.md](LAUNCH-DECISIONS.md) supplies concrete recommendations for the minimum host/engine promise and finite review termination, pending architect/user acceptance. These recommendations do not change historical approvals or authorize implementation.

**Preservation:** 100% of owned source paths accounted for; every dependency/test/notice has an explicit disposition; every relevant knowledge topic has a canonical owner and retrieval path. Complete inventory is not complete semantic review.

**Behavior:** existing meaningful tests plus audit regression fixtures pass in the isolated new package. Compare same inputs against the retained implementation at domain events, source map, frame count, alpha, text and audio alignment. Byte equality is appropriate only for deterministic identical outputs; perceptual equivalence must have declared tolerances and human/visual evidence.

**Craft:** cases require reasoned alternatives, a failure diagnosis and a correct revision. Technical and perceptual outcomes stay separate. An unfamiliar quiet title and a meaningful pause must not be damaged by generic speed/retention rules. Quantitative integrity failures cannot be averaged away by an aesthetic score.

**Host:** a proposed full pass has at most 24 single-turn model probes: four surfaces (Codex, Claude Code, GPT Work, ordinary ChatGPT) × two plugins × standalone/Studio mode =16, plus8 negative boundary probes. Record unsupported capabilities honestly; startup/knowledge access on a shell-less surface does not prove render execution. Additional media tests are local source/engine tests, not extra model cases. Any needed follow-ups fit a new explicitly bounded pass, not hidden extra calls.

**Release:** source tests, package readback, installation discovery, actual execution, playback/listening and user acceptance are separate receipts. Critical retained audit false-PASS checks are fixed before they can certify any extracted release. Named-NLE interoperability needs real import/export comparison, not only a valid interchange file.

## Deliverables of this planning/research task

- This proposal and the coordinated [plan](PLAN.md).
- Separate [FrameCut plan](FRAMECUT-PLAN.md) and [FrameMotion plan](FRAMEMOTION-PLAN.md).
- Source inventories, exact ownership maps and integration review.
- Separate expert-research compendia, source ledgers, worked examples and independent specialist reviews, indexed by this packet's `README.md`.
- A handover for Claude. No claim of architect approval, exhaustive expertise, native-app execution or completed plugin extraction.
