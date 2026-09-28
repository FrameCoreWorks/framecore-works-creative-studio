# Script-to-production handoff

Use when story choices need to travel into production, a storyboard, video
prompting or editorial planning. This is a handoff contract, not a replacement
for those specialties.

## Keep adjacent artifacts distinct

| Artifact | Primary question answered | Not a substitute for |
|---|---|---|
| Pitch/logline | Why this experience, and what decision or audience promise matters? | A complete plot or script. |
| Treatment | How does the film unfold as readable prose? | Exact line-by-line dialogue or a shot list. |
| Beat/sequence map | What events/images/sounds arrive, in what relation? | Scenes that the user requested to be written. |
| Screenplay | What can be performed, seen and heard in the requested format? | A technical timing or model-specific prompt unless explicitly included. |
| Scene card | What is this scene for, what changes or holds, and what must carry? | A formatted script excerpt. |
| Technical script | What timing, action, dialogue, sound, transitions and continuity must production coordinate? | A verified generator payload or approved storyboard image. |
| Storyboard | What does the planned image sequence look like across frames? | A single valid I2V carrier or a sequence of independent prompts. |
| Video prompt | What should the actual selected model operation generate from the bound inputs? | A script, researched capability or rendered/verified output. |

The next stage is conditional. A writer may hand off directly to the user, a
director, storyboard, editorial or a video-prompt specialist. Do not generate
every downstream document for a request that only asked for one.

## Handoff payload, chosen by need

For a short film or ad moving to storyboard/video prompting, preserve only the
fields required to execute the next real operation:

```text
PROJECT / REVISION:
REQUESTED NEXT ARTIFACT:
STORY INTENT:
FORM AND POINT OF VIEW:
AUDIENCE / CHANNEL / DURATION: (known, proposed or unresolved)
LOCKED FACTS, CLAIMS AND EXACT COPY:
CHARACTERS / SUBJECTS:
LOCATIONS AND SPATIAL RELATIONS:
BEATS OR SCENES: (IDs only if useful)
ACTION, ENTRY STATE AND EXIT STATE:
DIALOGUE / VO / SUPERS / SOUND:
CONTINUITY AND REFERENCE CARRIERS ACTUALLY SUPPLIED:
VISUAL OR TONAL ANCHORS:
PRODUCTION CONSTRAINTS / RISKS:
OPEN DECISIONS:
ACCEPTANCE TEST:
```

Do not leave placeholder fields in a final deliverable. Omit irrelevant fields
or mark a real blocker as unresolved. A completed template is not proof of a
production-ready result.

## Timed scripts and technical translation

Write time ranges as planning estimates unless they were measured against an
actual performance, clip or song. A 30-second goal is not a license to make
every action implausibly fast. Estimate from spoken-word pace, breath, visible
handling and transition. If the sequence will not fit, show the cut or duration
tradeoff rather than hiding it in dense phrasing.

Before making a technical script, decide whether it materially helps. It is
usually useful when:

- exact product demonstration or supers must be synchronized;
- a short ad must fit a known duration;
- several independent shots need stable continuity;
- a real editor/generator needs action, source, timing, sound and transitions.

It may be unnecessary for a logline, one-page pitch, exploratory treatment or
single self-contained scene. For each generated unit, specify the facts it
actually receives. A note that shot 3 “matches shot 2” is not a carrier; identify
the real frame, image, clip or confirmed shared context that will be attached.

## Change from script to shots without flattening the story

Keep the story function of each unit, then translate only what the next medium
needs: opening state, readable action, camera/viewpoint intent, end state,
sound, exact speech and continuity. Do not give every line its own close-up or
turn an observational hold into motion for the sake of a prompt.

When a single continuous take is essential, check that physical action, blocking
and duration can happen continuously. When separate generations are needed,
write a complete standalone brief per unit and attach the actual continuity
carrier. Do not infer identity consistency, object state or geography from
repeated adjectives. Keep storyboard cards separate from generator inputs: a
full board can be an overview while each model call needs one correctly framed,
authorized reference asset.

The video-prompt route owns exact current model/surface mapping, prompt form and
supported controls. This reference contributes story intent, not a guessed API
schema. If the selected tool cannot support the story requirement, offer the
smallest truthful creative alternative and disclose the tradeoff.

## Advertising, product and campaign handoff

Before a screenplay draft leaves the story stage, distinguish:

- verified product fact from user hypothesis;
- exact approved copy from new dialogue/VO alternatives;
- claim from dramatic metaphor;
- planned proof image from proof that exists in supplied production media;
- offer/price/CTA that is supplied from one the writer is merely proposing.

A fictional demonstrator is not customer evidence. Do not fabricate a
testimonial, result, certification, comparative statement, price, availability,
logo or contact detail. If proof is not available, rewrite the dramatic action
around a truthful visible property or label the claim pending approval. Keep the
product causal to the story when the brief needs product proof; do not insert it
as a label after the story is complete.

## Worked planning example

Synthetic premise: a night custodian at a community print room has five minutes
to close, but a volunteer is reusing one misprinted page for a hand-cut sign.
The example does not imply a real service or person.

| Unit | Story function | Visible action / sound | Carry into next unit |
|---|---|---|---|
| 01 | Establish the practical closing pressure | Custodian switches off two lights; the printer keeps one status LED glowing. | The remaining page and the closing time matter. |
| 02 | Expose a difference in what “waste” means | Volunteer folds the misprint along a still-readable word, not the crop marks. | Their hands and the page's orientation remain clear. |
| 03 | Let the practical rule meet the chosen use | Custodian reaches for the recycle tray, sees the fold, and puts the tray back. | No speech is necessary unless the user's intended relationship needs it. |
| 04 | End on a small observable choice | The two carry the sign out; the unlit room still shows a faint registration mark. | End state is modest; no forced lesson or twist. |

This is a beat map, not a complete screenplay. To write the script, add the
specific setting, playable actions and any dialogue needed for the chosen tone.
To storyboard it, determine shot scale, screen direction, timing and board
purpose separately. To make a video prompt, bind actual inputs and map the
selected generator first.

## Source note

This reference synthesizes the selected writing and storyboard source
contracts. It is not an official tool schema, and current capability facts
remain out of this evergreen handoff. The source-to-runtime mapping is kept in
the private development audit. These examples are synthetic planning material,
not tested renders.
