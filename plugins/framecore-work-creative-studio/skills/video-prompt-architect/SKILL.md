---
name: video-prompt-architect
description: Write a video-generator prompt for a clear brief, approved shot card or requested edit (text-to-video, image-to-video, references, extensions), researched for the named model, or review a supplied clip. Coded motion goes to Motion Graphics Workflow.
---

# Video Prompt Architect

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Apply the conditional [public research gate](../research-evidence/SKILL.md) before committing to substantive direction or prompt work. Without a named generator, write a model-agnostic prompt and search only when another trigger applies; verify material public facts. The deeper model-mapping requirements below apply whenever a generator is named.

Own the video craft and prompt-compilation stage. Produce a complete, usable
artifact for the user's actual request. Do not turn every task into a full
production questionnaire or a parade of fictional specialists.

This module owns generator-aware video prompt compilation. The package also
contains initial music-video direction, screenplay development, sequence/shot
planning, and static storyboard/reference-board specification modules; their
approved artifacts can be consumed here without silently revising upstream
decisions. Direction modules are initial synthesis, not evidence of
target-host behavior or creative quality. Audio Production Director supplies
music/audio text packets and conditional evidence-bounded audio triage; it has
no bundled generation connector. A motion video Studio builds from code, with its designed sound, belongs to the
[Motion Graphics Workflow](../hyperframes-workflow/SKILL.md), not to a generator prompt.

## Start from the request

Use the language of the conversation. Technical prompts default to English
unless the user asks otherwise; exact dialogue, visible copy, names, and
pronunciation remain in the requested target language. Never translate or
rewrite locked text without permission.

Do not repeat the welcome or mode menu after the user has supplied a task.
Quick mode means fewer visible decisions, not weaker fact checks or quality
gates. Deep exploration is for unresolved concepts, campaigns, strict
continuity, product proof, dialogue/performance, or repeated failure. Ask only
the next question that materially changes the result.

For a usable brief, resolve only the missing facts that affect the requested
artifact:

- what the audience should understand, feel, or do;
- what is visible and what changes;
- which exact generator or delivery target is requested, if any;
- what operation and source material are actually available;
- important duration, aspect, channel, copy, identity, product, or continuity
  locks;
- whether speech or sound is essential; and
- what observable result would count as success.

Do not ask whether the user uses an API or wrapper unless they explicitly
introduce that context. Do not require answers to fields already clear from the
brief. If a critical source fact is missing, ask for it or label the proposal
as conceptual rather than inventing it.

## Route the work

1. Separate creative intent from execution details. The creative contract holds
   objective, source truth, action, camera, performance, sound, locks, and
   acceptance criteria. The execution contract holds the verified model,
   version, surface, operation, input bindings, supported controls, and
   authorization state.
2. Classify the operation and the way context reaches it. Distinguish T2V,
   I2V, reference-conditioned generation, source-video edit, V2V, extension,
   first/last-frame interpolation, presenter/lip-sync, and any verified native
   multishot mode. Also distinguish text-only, attached references, a bound
   source clip, a chained approved frame, and shared context limited to one
   verified job.
3. Decide whether the requested unit is one continuous shot, an explicitly
   supported native multishot job, or several independent shots. Do not imply
   that several prompts share identity, setting, or history.
4. If the user gave a script or board, preserve its approved premise, shot
   order, copy, identity, product, wardrobe, and stated intent. If it conflicts
   with feasibility, explain the smallest proposed correction; do not silently
   rewrite it. For sequence/shot authoring, route to
   [storyboard-sequence-architect](../storyboard-sequence-architect/SKILL.md);
   for static board layout and copy, route to
   [storyboard-board-architect](../storyboard-board-architect/SKILL.md). A board
   image or card is not automatically a bound carrier for a video request.
5. Read only the relevant sections of
   [video craft](references/video-craft.md). Its sections cover temporal
   causality; shot load; camera and perspective; blocking and contact;
   continuity carriers; dialogue and sound; identity, wardrobe, product truth,
   UGC and short form; I2V and edit operations; QA; examples; and handoff.
6. For difficult blocking, contact, camera/action coordination, continuity or
   clip extension, read the relevant worked case and reusable state template in
   [blocking, continuity and extension](references/blocking-continuity-and-extension-workbook.md).
   Its prompts are generator-neutral exercises; actual carrier binding and
   provider controls still need verification.

## Current generator mapping and fact checks

When a generator is named, actively search the web before presenting the
prompt as adapted to that generator, unless the user explicitly asks not to
browse. Check the exact current model/version and surface where possible.
Prioritize the provider's current official documentation for supported
operations, inputs, controls, limits, and syntax. Then consult original,
attributable practitioner experiments for practical behavior, failures, and
workarounds. Separate official claims, user observations, reproduced tests,
and inference. Compare conflicting evidence and cite the source for current
claims.

Do not equate the consumer UI, API, and third-party wrapper. Do not invent
native syntax, seeds, negative-prompt fields, frame counts, duration limits,
reference counts, or controls. The existence of a feature in one surface does
not prove it exists in another. Do not call one forum post a verified best
practice.

If browsing is unavailable, disclose that live mapping did not happen. Either
return a clearly labelled generator-neutral prompt, or a provisional
adaptation limited to evidence already present in the conversation. Do not
claim it is current or generator-verified. Respect an explicit no-web request;
state the resulting uncertainty rather than fabricating freshness.

Use the shared [research-evidence](../research-evidence/SKILL.md) workflow
for every substantive video task and expand it to current model mapping when
the user names a generator. Do not research unrelated models to fill space.
For a broad question about which video generator to use, or to identify a named
one and its surface, start from the dated
[video-generator snapshot](../research-evidence/references/video-generator-snapshot.md)
and refresh the exact target before writing its prompt; a retired model such as
Sora gets an explanation and a current alternative.

## Build a feasible prompt

Make the action legible as a transition:

opening state -> trigger or preparation -> primary action -> contact or reveal -> consequence -> settled ending

Use only the beats the shot needs. Sequential causes stay in order. Allocate
time among preparation, action, speech, camera movement, reaction, and viewer
comprehension. When too many difficult elements compete, simplify, extend the
duration, or propose separate coverage; do not hide infeasibility under more
adjectives.

Choose camera movement for evidence and meaning. Define a useful starting
position, side, distance, direction, speed, subject relation, and ending
composition when material. Keep the decisive face, contact, product, or
mechanism visible at an appropriate scale. Separate subject, camera,
environment, and optical/editorial motion, then choose a clear lead. Describe
physical response only to the detail supported by the brief and references.

Assign references authority by property: identity, product/SKU, garment,
location, composition, style, camera, motion, audio, or opening/ending state.
For each strict continuity lock, confirm a real carrier is attached to every
independent request that needs it. A text reminder or reused seed is not a
strict carrier. Track the required continuity level separately from carrier
readiness and observed outcome. If the carrier is absent, keep the strict
requirement and mark that request not ready. Request the source or propose a
relaxation/shot-plan change; apply a weaker requirement only when the user accepts it.

Keep product demonstrations and commercial claims truthful. Do not invent
product mechanics, contents, results, testimonials, ownership history, prices,
labels, or endorsements. A visually plausible result is not evidence that a
product performs that way.

For dialogue, establish speaker ownership, exact words, intention, timing
estimate, mouth visibility, listener reaction, and acoustic perspective.
[Screenplay](../screenplay-story-architect/SKILL.md) owns narrative scenes and
dialogue; [Copy Voice](../copy-voice/SKILL.md) owns standalone marketing/editorial
copy and short VO wording; [Audio Production Director](../audio-production-director/SKILL.md)
owns lyrics and audio direction. Consume their accepted text without another
writing pass. Return necessary wording changes to the relevant owner.
Keep approved copy locked. If it cannot fit naturally, propose
more time, a split, VO, or an alternate line for approval.

Sound follows visible or intentional editorial causes. Separate dialogue,
VO, diegetic effects, ambience, score, and mix perspective. Only describe
native audio controls after verifying them for the exact model/surface/
operation; otherwise provide a separate post-audio plan.

Use [audio evidence and audiovisual handoff](../audio-production-director/references/audio-evidence-and-av-handoff.md)
for cue sheets, transcripts/captions, timing basis, sonic continuity and evidence
states. This owner reviews video, motion and audiovisual alignment; Audio Production Director
owns audio triage. For captions, preserve supplied/transcribed words and test
placement and readability over the actual picture. Do not certify sync from
isolated stills, or a whole mix from metadata or a partial listen.

## Hard anti-slop loop

Anti-slop is a set of visible design decisions, not a style phrase or appended
negative list. Before returning a final generator-specific prompt, run this
loop and repair any material failure:

1. **Specificity:** identify the detail, tension, behavior, product truth, or
   visual mechanism that belongs to this brief. If any generic subject could
   replace it without loss, strengthen the concept rather than decorating it.
2. **Authorship:** verify that camera, light, sound, setting, and gesture have
   reasons. Remove stock spectacle (unmotivated orbit, neon, particles, speed
   ramps, dramatic score, or generic “cinematic” language) unless this brief
   earns it.
3. **Hierarchy and feasibility:** keep one dominant action and purpose per
   shot; make the causal spine, viewer attention, and end state understandable.
   Reduce competing motion, hidden dependencies, or detail that the framing
   cannot show.
4. **Human voice and performance:** dialogue must sound speakable, socially
   plausible, and specific to the relationship. Do not fabricate experience,
   testimonial, emotion, accent, or identity; do not insert filler to simulate
   authenticity.
5. **Truth and continuity:** verify exact copy, claims, product/character
   facts, reference authority, carrier coverage, and preservation rules.
6. **Surface correctness:** remove unsupported syntax, false limits, and
   unverified model claims. Distinguish prompt readiness from authorization to
   execute.
7. **Acceptance test:** state concrete observable criteria for a future render.
   A preflight pass is not a render pass.

If a material gate fails, do not label the prompt final. Make the smallest
revision that addresses it, then rerun all affected gates. Do not force three
creative directions for a precise brief; if directions are requested, make
them differ by idea and mechanism, not palette alone.

## Prompt and result output

Follow the requested deliverable. A final prompt should be standalone and
complete, not a patch referring to an earlier draft or chat. Include only
assets actually intended for that exact request; use neutral attachment labels
the user can map to files. Use a separate negative field only when the
selected surface exposes it and current evidence confirms it.

When useful, deliver two compact layers:

1. the complete prompt or clearly labelled neutral blueprint; and
2. a short production note with operation, duration/aspect if known, source
   assets and their roles, locks, unresolved controls, and acceptance tests.

If structured JSON/YAML is requested, label whether it is a planning
representation or a verified native schema. Never present a convenient
planning object as API payload.

Writing a prompt does not generate a video. If the user explicitly requests
generation, use only an actually exposed, permitted host capability. If none
is available, state that and provide the prompt. Never claim a provider ran,
an asset was uploaded, or a result exists unless the tool confirms it.

Resolve authorization by operation, input assets and destination. Preserve a
user's existing authorization through handoffs; do not ask for it again solely
because the owner changed. A new paid run, upload or publication must fit that
scope and actual host conditions. Read-only research and local inspection are
not external generation, and MCP/API are transports rather than permissions.

## Analyze a supplied clip and revise

Diagnose a render only after receiving the actual video or usable frames/audio.
A description of a missing clip is a report, not an inspection. State what
was actually visible/audible and what was not checked. A thumbnail cannot
prove continuity or lip-sync; sampled frames cannot prove the entire motion.

Record source revision, method, inspected time ranges and audio/picture coverage.
Metadata, user observations and actual playback have different evidence scope.
For upstream revisions, mark dependent prompts, cues, captions and exports
`review_required` until their affected locks and timing are checked. Preserve
approved constant framing and sustained performance; a board handoff must not
introduce new camera angles merely to create panel variety.

For each iteration, change one principal cause. Record:

- the observed problem and its evidence level;
- the exact point/beat/region where it occurs;
- what accepted elements must remain unchanged;
- one structural correction; and
- a concrete pass/fail test for the next render.

Return a complete clean prompt for the requested operation. Inspect the new
result against that test when it is supplied. After two controlled failures
with the same symptom, change the structural approach, source/carrier,
coverage, or verified operation instead of accumulating bans or spending
automatically. Preserve the accepted upstream creative direction unless the
evidence shows it is the cause.

## Integrated workflow contracts

Use [the integrated workflow-kit method](kit/method.md) for this owner’s artifact fields, bounded review and downstream handoffs. Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) for precedence and the single active route. Preserve this owner’s domain craft and the user’s requested stage.

## Revisioned prompt handoff

For strict locks, several requests, target adaptation or execution readiness, use [Creative Prompting Standard](../pipeline-core/references/creative-prompting-standard.md) and its [contract template](../pipeline-core/templates/creative-prompt-contract.md). Bind each request to its actual attachments, exact copy, source revisions and required continuity. Keep requirement, readiness and inspected outcome separate; a planned end frame cannot be an accepted carrier. Final prompts stay complete and standalone, each in its own fenced block.

## Compile and inspect adjacent shots

Consume the sequence owner’s [adjacency contract](../storyboard-sequence-architect/references/shot-adjacency-workbook.md). Preserve action phase and actual carriers per request. A planned pair has no inspected smoothness result; review actual neighbouring clips when available.

## Reference-frame readiness

Use [reference capability routing](../tool-routing-cost/references/reference-capability-routing.md) and the [individual-frame handoff](../storyboard-board-architect/references/production-reference-sheets.md) when a character/product sheet supplies a proposed video source. Bind an actual selected image to the supported input; the panel name alone is not a carrier.
