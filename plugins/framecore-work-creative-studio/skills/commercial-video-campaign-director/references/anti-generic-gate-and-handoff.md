# Anti-generic gate and campaign handoff

This is a blocking review of a proposed commercial video direction before it is handed to sequence, copy or prompt work. It evaluates the direction's idea logic and evidence, not the quality of pixels, a completed edit, legal compliance or likely campaign performance.

## 1. Evidence-backed gate

Record a concise verdict:

- **PASS:** every material item has a supported answer or an explicitly bounded hypothesis, and the direction can move downstream without inventing facts.
- **REWORK:** the concept is generic, contradictory or underdeveloped but can be repaired from the current brief.
- **BLOCKED:** a missing fact, conflicting lock, unsupported claim or unavailable decision prevents an honest direction. Ask the smallest useful question or offer bounded choices.

Do not score the route numerically or let several small positives conceal one serious truth/feasibility failure. A polished format is not a pass.

| Gate | Passing evidence | Rework/block signal |
|---|---|---|
| Brief fit | The route answers the requested communication job and respects selected concept/format. | Interesting idea unrelated to the actual user request. |
| Specificity | At least one supported product, service, brand, user-supplied context or observable detail changes the idea. | Route could sell any category; unsupported audience pain or differentiator. |
| Authorial mechanism | One clear action, contrast, reveal, ritual, transformation, relationship or structure drives the idea. | Only adjectives, trend names, shot quantity, template or “make it viral”. |
| Motion necessity | A meaningful state, action, relationship, rhythm or sound evolves and is legible over time. | Static key visual with arbitrary camera moves, animated decoration or random cuts. |
| Truth and proof | Product facts, claims, testimonials, authority and visual evidence have named status and source. | Invented result, fake demonstration, false before/after, implied competitor claim or fabricated spokesperson. |
| Human professional craft | Framing, action, camera, light, performance, texture, sound and graphic hierarchy each have an intentional role. | Stock montage, unmotivated orbit/slow motion, generic lens/grade adjectives, “premium” as the entire direction. |
| Distinct routes/assets | Alternatives use materially different mechanisms; requested campaign assets each have a real communication job. | Palette-only variants, one master repeated 1:1, or arbitrary asset matrix. |
| Placement truth | Current constraints are verified for the exact platform, placement, objective and creation path or explicitly left unverified. | Stale limits, universal timing claims, guessing safe zones or turning recommendations into rules. |
| Locks and copy | Exact user-approved copy, product form, brand cue, offer and suppression rules survive. | Unapproved headline, CTA, price, legal line, logo or claim has been silently introduced. |
| Feasibility and handoff | Critical production unknowns and acceptance checks are stated; downstream owner receives only approved intent. | A direction depends on unverified model controls, missing carrier, unavailable footage or an unowned next step. |

Human professional design is not a surface filter. It comes from deliberate selection: one primary idea, a reasoned point of view, controlled hierarchy, motivated movement, observed or sourced details, edit rhythm with purpose, meaningful sound, accurate product handling and an ending that resolves the actual communication job. Do not add ornamental effects or fashionable references to imitate authorship.

## 2. Hard anti-slop loop

When any material gate fails:

1. Name the failed criterion and the concrete evidence that exposes it.
2. Identify the source decision that must change: insight, device, proof, motion, asset job, placement assumption, copy, feasibility or user input.
3. Repair one primary defect first. Preserve already approved locks; do not regenerate the whole concept unless its central mechanism is the defect.
4. State one observable acceptance test for that repair, such as “the first action communicates the supplied use without the voice-over” or “the three placements have different opening actions and distinct jobs.”
5. Re-run the affected gate plus any dependent truth/placement/lock checks.
6. If the same root problem persists, change approach, ask for missing evidence or stop. Never enter an endless rewrite loop or mark prose revisions as proof of render quality.

Do not release a final selected direction or downstream handoff while verdict is REWORK or BLOCKED. You may show clearly labeled exploratory options for selection, but do not imply they are production-approved. An explicit user selection resolves preference, not a factual or technical blocker.

For an actual generated result, pass approved observables and source/attachment context to video-prompt-architect for video/motion and audiovisual review, audio-production-director for audio triage, or output-critic-iteration for a static result. Do not use this pre-prompt gate to claim the produced video passed review.

## 3. Direction contract

Use a compact structured form when useful. Omit irrelevant fields rather than filling every field with ceremony.

~~~yaml
commercial_video_direction:
  status: provisional | selected | locked
  communication_job:
  audience_context:
    status: supplied | observed | researched | hypothesis | unknown
    statement:
  truth_ledger:
    - item:
      status: supplied | approved | observed | researched | hypothesis | unknown
      source_or_owner:
      usage_boundary:
  motion_thesis:
  creative_device:
  why_this_is_specific:
  progression:
    opening_event:
    development:
    proof_or_reveal:
    payoff_or_memory:
  audiovisual_grammar:
    movement:
    camera:
    performance:
    image_language:
    sound_and_silence:
    visible_copy:
  asset_system:
    - asset:
      placement_and_objective:
      communication_job:
      preserve:
      adapt:
      duration_or_format_status: user_supplied | verified | target | unknown
  locks:
    exact_copy:
    product_and_brand:
    references:
    prohibited_changes: []
  research_notes:
    - claim:
      class: requirement | recommendation | observed_example | empirical_finding | inference
      source:
      checked_at:
      scope_and_limit:
  feasibility_unknowns: []
  acceptance_tests: []
  anti_generic_gate:
    decision: PASS | REWORK | BLOCKED
    failed_criterion:
    evidence:
    repair:
    retest:
  handoff:
    sequence_direction:
    copy_voice:
    audio_direction_and_evidence:
    video_prompt:
    modality_review_owner:
~~~

Do not force an ID, version, persistent path, or digest into a conversational brief. If a durable route artifact is explicitly requested and the host can create it, create that artifact before naming its path; compute and verify a digest before reporting one. Without those capabilities, mark path/hash unavailable and keep the current approved intent in conversation. Never simulate persistent memory.

## 4. Bounded handoffs

- **Sequence / shot planning:** pass the selected thesis, progression, intended duration as target or verified constraint, one device, asset jobs, exact locked strings, product/reference roles, preserve/change rules and observable tests. Let the sequence owner decide atomic shots, timing estimates and continuity carriers. Do not pre-write shot cards here.
- **Copy and voice:** pass the communication job, approved fact/claim ledger, exact existing copy, audience/context evidence, desired human voice, CTA state and forbidden wording. The copy owner may propose language but may not promote a claim or overwrite exact user copy.
- **Sonic direction and audio packet:** pass the sound's campaign job, approved copy/voice status, music or recurring sonic motif, source/rights evidence, native-versus-post sound intention, sound-off counterpart and variant continuity to audio-production-director. Its [audio/AV contract](../../audio-production-director/references/audio-evidence-and-av-handoff.md) supplies cue planning and evidence boundaries; it does not imply generated or mixed audio. Narrative dialogue stays with screenplay; standalone copy/short VO wording with Copy Voice; lyrics with Audio Production Director.
- **Video prompt compilation:** pass only the selected direction, requested generator/operation/surface if known, actual available reference carriers, approved sequence if one exists, copy/audio intent, locks and tests. Model syntax, parameters, current capabilities and attachment handling belong to the video-prompt owner and its fresh generator-specific research.
- **Static key visual or campaign graphic:** hand off the shared campaign thesis and visual memory cues to static direction. Do not prescribe poster hierarchy or one identical layout for every medium.
- **Render critique:** provide actual received output plus approved source and criteria to the owner for its modality: video-prompt-architect for picture/motion/AV alignment, audio-production-director for audio, output-critic-iteration for still graphics. Preserve metadata-only, user-report and inspected-range distinctions. If output or required references are unavailable, state which review could not run.

Handoffs are plans, not execution. Selecting a direction alone authorizes no generation, media buying, upload or publishing and establishes no legal claim. Carry a separate existing user authorization for the actual operation, assets and destination; do not discard it or demand reapproval solely because an owner changes. Use only actual capabilities within host/user conditions. Missing carrier or sync capability blocks readiness without changing the required standard; a proposed downgrade requires user acceptance.
