# Sequence contract and continuity

This reference synthesizes selected storyboard and motion-planning knowledge
for the Creative Studio. It is stable craft guidance, not a model-specific
adapter, a measured timing database, or a claim that images/video have been
generated or checked. Provenance scope: selected units from Visual Prompter
K07/K15/K18; Video Prompter K09/K14/K15/K18; Storyboard & Reference Board
Creator ROOT/META/K01-K04; and the pinned Workflow Kit storyboard contracts
plus `examples/storyboard-board`. The runtime rephrases and reconciles
them; it does not reproduce their instructions or templates wholesale.

Related contracts: [reference authority and carriers](reference-authority-and-carriers.md),
[board layout and copy](../../storyboard-board-architect/references/board-layout-and-copy.md),
[board delivery and handoffs](../../storyboard-board-architect/references/board-delivery-and-handoffs.md).

## 1. Define which artifact is being authored

These deliverables answer different questions and should not be collapsed into
one table or image:

| Artifact | Primary question | Typical contents | Does not prove |
|---|---|---|---|
| Sequence / beat map | What changes, and in what order? | beats, scene transition, duration basis, event dependencies | final frame composition, native generator support |
| Shot breakdown / shot cards | How can each moment be covered clearly? | ID, purpose, scale, position, action, camera, start/end state, sound, locks | that shots share context in a later generation job |
| Storyboard / contact board | Which selected moments should be compared on one static page? | chosen panels, their order, image crops, labels, board grid | a full temporal sequence or usable source image per shot |
| Reference board | Which visual properties should collaborators compare? | assets with property authority, selected details, notes | permission to copy every incidental feature in the references |
| Video prompt pack | What should a specific generation operation attempt? | self-contained per-request prompt and bound inputs | that an operation ran or succeeded |

A request can ask for one, several, or all of these. Answer only the scope
requested, but when both sequence and board are requested, state they are
separate outputs and connect them with stable shot IDs and selected moment
labels. A board may omit shots, compress time, or compare alternative
approved designs; disclose its inclusion rule so readers do not mistake it for
complete coverage.

## 2. Read the story or brief as the authority

Use the user's accepted script, treatment, shot order, and corrections as the
source of story truth. Keep known facts distinct from proposed staging. Do not
invent a new beat, reaction, product action, dialogue line, or ending to make
a board more exciting. When the brief is conceptual and invention is
delegated, label proposed story choices before downstream lock-in.

An effective sequence gives each beat a job: establish place or relation,
prepare an action, reveal evidence, change a relationship, hold for audience
comprehension, or land a consequence. Not every project needs a conventional
dramatic arc. Observation, process, essay, mood and music-led work can advance
through attention, duration, contrast, pattern, or a changing visual state.
Do not force conflict, twists, three-act labels, or a fixed beat count.

For each proposed beat, ask:

1. What is visibly or audibly true before it?
2. What causes the change, if change is intended?
3. What can the audience perceive that establishes the beat's function?
4. What state remains after it and enables the next beat?
5. Is the information already communicated elsewhere, or is this repetition
   intentional?

If no meaningful state change is required, name the attention contract: what
the audience is asked to notice, compare, anticipate, or sit with. Stillness
is valid structure when its duration and framing perform a purpose.

## 3. Beat map before camera polish

Build the causal or perceptual order before selecting angles. A compact map
usually needs stable beat IDs, narrative/informational function, visible
event, source authority, relative or approximate timing, and handoff state.
Keep a planned event separate from a camera instruction: “the envelope is
opened” is an event; “hold a locked medium close-up on the hands” is coverage.

Use temporal order honestly:

- **Sequential:** one action enables the next (reach, grasp, lift, open).
- **Simultaneous:** events overlap by design (camera tracks as a person walks;
  rain continues through an exchange).
- **Reaction/hold:** a response follows an observed trigger and needs enough
  time to register.
- **Transition:** an editorial change relocates time/place or viewpoint; do
  not imply it is continuous movement unless it is.

When timing is uncertain, choose among (a) beat order without seconds, (b) a
clearly labelled planning estimate, or (c) one material clarification about
target duration or pace. Do not invent frame-accurate timecodes. Timing inferred
from text is not measured delivery; distinguish estimate, target, and observed
runtime. Ranges should not leave accidental gaps or overlaps, and should allow
for setup, action, comprehension, speech and reaction.

## 4. Create shot cards that can be acted on

Assign stable shot IDs that survive revisions and board pagination (e.g. S01,
S02). Each card should be complete enough for its downstream purpose, not a
miniature prose prompt. Add only material fields:

| Field | Useful question |
|---|---|
| Function | Why is this shot in the sequence? |
| Framing and viewpoint | What scale/side/height shows the needed evidence? |
| Subject/action | What is the one main observable event? |
| Start state | What is in frame before action begins? |
| Camera behavior | Locked, pan, track, push, etc.; what does movement reveal? |
| End state | Where are subject, prop, gaze, camera, and movement at the end? |
| Duration | Target, estimate, or unknown; what is the basis? |
| Sound/dialogue | Only supplied/approved words or a labelled sound intention |
| Continuity | What facts must carry in/out, and which carrier contains them? |
| Acceptance test | What visible criterion would make the shot usable? |

One primary action per short shot is a strong planning default, not a universal
law. Add a secondary action only if both remain legible and feasible. If a wide
shot must establish geography while also proving a tiny label or precise
mechanism, consider separate coverage rather than overloading one frame.

Shot order belongs to the sequence; panel order may be arranged for comparison
or page comprehension. If board order intentionally differs, label it and
retain original shot IDs. Do not silently renumber accepted shots just to fill
a grid.

## 5. Timing as a budget, not a decoration

The audience needs time to parse setup, action, cause, consequence, dialogue,
camera movement, and the terminal state. Each consumes part of the shot's
duration. Identify the dominant information and protect it; a mechanism demo
may favor stable close coverage, while a reaction needs a hold after its
trigger.

Practical planning sequence:

1. Set only the duration the user supplied or approve an estimated target.
2. Allocate time by event complexity and comprehension, not equal slices.
3. Check whether dialogue can be spoken and understood at a plausible pace.
4. Check motion lead-in, contact/reveal, recovery, and terminal hold.
5. Remove false precision and identify any estimate's basis.

If event density does not fit, simplify, lengthen, or split into coverage. Do
not hide impossibility behind words like “fast”, “seamless”, or “fluid”. Never
present a proposed timeline as footage measurement.

## 6. Camera logic and spatial continuity

Select camera decisions to expose story evidence:

1. Purpose and visible information.
2. Distance/scale, angle, height and side.
3. Subject blocking, eyeline, screen direction and contact.
4. Camera path and focus behavior only when materially useful.
5. End composition and relation to the next shot.

Use stable screen direction, geography, left/right ownership, hand/prop side,
entrance/exit and eyelines where these facts affect comprehension. A planned
axis change is valid when a move, neutral framing or subject reorientation makes
it readable. Avoid accidental reversals. Do not add a gratuitous orbit, whip,
push, rack focus or handheld shake to signal generic “cinematic” quality.

For each shot, distinguish subject movement, camera movement, environmental
movement, and optical/editorial change. Pick a lead. Camera behavior should
describe useful relation (starting side, direction, distance/speed, what is
revealed, where it stops) rather than a stack of aesthetic adjectives.

## 7. Continuity is a property-level contract

Track continuity according to the source: identity, costume, product/SKU,
prop ownership and position, hand occupancy, room geography, light/time,
camera axis, screen direction, exact copy/dialogue, sound tail, and start/end
state. Not every story requires every property; include only those that could
break recognition, truth, or action.

Separate **state locks** (must remain invariant) from **transitions** (must
change in a controlled way). For example: “the folder stays red” is a lock;
“Paweł transfers it from counter to shelf between S03 and S04” is a transition.
A coherent shot card names both before and after states when an object moves.
Ownership and physical carrying are different facts; changing one does not
automatically change the other.

Use [reference authority and carriers](reference-authority-and-carriers.md)
for strict/approximate definitions and binding checks. A text-based continuity
note alone does not transport an image, source clip, or shared native context.
Each independent downstream request must receive the required carrier itself,
unless that exact execution surface has verified shared state.

## 8. Revision and acceptance loop

For a continuity change:

1. Name the new fact and its authoritative source.
2. Find every dependent beat/shot/panel and classify direct vs indirect
   dependency.
3. Preserve unrelated actions, copy, composition and approved intent.
4. Revise the smallest set of cards that restores causality.
5. State one observable acceptance test (e.g. “S04 opens with the folder on
   shelf B; S03 and exact line remain unchanged”).

An accepted shot-card plan is still not a render result. If a user supplies
actual frames/video, inspect only what is available and distinguish
observations from inference. When a material failure is reported twice after
controlled corrections, revisit the coverage, carrier, upstream decision, or
sequence structure rather than piling up generic prohibitions.

## 9. Output and handoff

Use plain tables or labelled cards when they improve comparison. A compact
output for a short request may contain an ordered shot list plus timing note;
a complex project may need beat map, detailed cards, continuity state, and
promptability notes. Never expose hidden reasoning or fictional committee
deliberations.

For a board handoff, provide selected shot IDs, panel order, exact labels,
source sequence version, relevant frame/asset selection, and any deliberate
omissions. For video prompt compilation, provide self-contained approved facts,
one request's action, relevant reference roles and attached carrier status,
timing basis, sound/copy locks, operation if known, and acceptance criteria.
See [board delivery and handoffs](../../storyboard-board-architect/references/board-delivery-and-handoffs.md).
