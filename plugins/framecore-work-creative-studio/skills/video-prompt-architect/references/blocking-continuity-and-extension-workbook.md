# Blocking, continuity and clip-extension workbook

Use this when a moving shot has unclear attention, broken contact, axis drift, an unwanted camera move, or an extension seam. It applies the [video craft reference](video-craft.md) through original worked examples. All examples are planning exercises, not generated clips or inspected assets. They add no connector, model control or execution capability.

## Contents

- [Blocking card and camera decisions](#1-stage-what-must-be-understood)
- [Complete contact shot A](#2-worked-shot-a-make-release-visible)
- [Reusable continuity state contract](#3-continuity-is-a-state-plus-a-real-carrier)
- [Extension tree and complete blueprint B](#4-extension-decision-tree)
- [Picture and sound transitions](#5-picture-continuity-and-sound-continuity-are-separate)
- [One-cause repair table](#6-one-cause-repair-table)
- [Sources and mapping](#7-research-basis-and-source-to-rule-mapping)

## 1. Stage what must be understood

Start with the viewer's required evidence: a face recognizes something, a hand makes contact, an object changes support, or a path stays continuous. Design where bodies, objects and camera must be so that evidence remains visible. A direction such as “dynamic camera” does not specify this relationship.

Use this compact blocking card for a difficult shot:

| Decision | Write a concrete answer |
|---|---|
| Viewer task | The one event or relationship the shot must make readable |
| Opening geography | Subject, destination, active hand/prop and their visible relation |
| Action path | Starting point, travel direction, contact and final support |
| Camera role | What it reveals, follows or preserves; why movement is needed |
| Occlusion risk | Which body/object could hide the decisive event |
| Axis / screen travel | Which side is maintained; any crossing must be intentional and legible |
| Attention handoff | When the viewer should move from face to hand, object or consequence |
| End state | Stable facts needed by a next shot or continuation |

For a single shot, screen direction describes what is visible from its camera. For several shots, also preserve the underlying world geography and performer/prop state. Identical left/right wording cannot repair a camera that has crossed to a different side. Do not invent a new camera angle when the upstream direction locks one.

### Choose motion by its job

| Intended job | Candidate direction | Check before selecting it |
|---|---|---|
| Keep a hand contact legible | Locked frame or restrained following movement | Is contact large enough and unobstructed? |
| Reveal an object behind a foreground edge | A small change of camera position | Does the position change actually reveal the required space? |
| Change emphasis without changing viewpoint | A reframing or focus intention, when appropriate | Will the relevant plane/subject remain readable? |
| Accompany walking | Camera travel related to the subject's path | Do body speed, ground contact and environment movement agree? |
| Let a reaction register | Hold the camera while behaviour changes | Has motion been added only to fill time? |

These are creative alternatives, not native controls. A zoom does not move the camera through space; a dolly does. Avoid requesting several contradictory operations as one “cinematic move.” If the exact surface lacks a needed control, preserve the intent and report feasibility rather than presenting an invented knob.

## 2. Worked shot A: make release visible

**Hypothetical accepted brief:** show a fictional adult placing a plain square card upright in a wooden holder, then withdrawing the hand so the viewer sees the card standing. Requested duration: 6 seconds. No identity reference or named generator; no dialogue or required visible text. This is an original neutral shot design. Duration is a requested target; actual duration/FPS are `Unknown`.

**Blocking choice:** the right hand approaches from screen-right; holder and card remain large enough to see the lower edge. Camera holds on one side of the work surface for the contact and release. A small post-release lateral move is optional only because it can confirm the card stands independently. If the user has locked a fixed camera, omit that move and retain the proof in the same frame.

| Phase | Subject / prop | Camera / attention | Acceptance |
|---|---|---|---|
| Prepare | Card visibly held above the holder, lower edge clear | Stable oblique view of hand and holder | Destination and grip are understandable |
| Place | Lower edge enters the holder; hand still supports it | Keep contact visible | Support transfers before fingers open |
| Release | Fingers separate; hand withdraws sideways | Maintain the same side | No card movement that depends on an invisible hand |
| Settle | Card remains upright, hand out of its silhouette | Hold, or make the optional small reveal | Viewer has time to register independent support |

**Complete generator-neutral prompt — fixed-camera version:**

```text
One continuous close working shot, requested length about six seconds. A fictional adult's right hand holds a plain square cream card just above a small wooden card holder on a work surface. Use a steady oblique camera view that clearly shows the card's lower edge, the holder opening and the fingertips. The hand approaches from screen-right and lowers the card deliberately into the holder. Keep the grip until the lower edge is seated. Then open the fingers, withdraw the hand to screen-right and leave the card standing upright without contact. Hold the settled end state long enough to understand that the holder supports the card.

Keep the camera position and framing constant throughout. Use soft consistent side light so the support and contact shadow remain readable. Preserve the card's shape and the holder's geometry during contact and release. No lettering, new props, cuts, dialogue or visible singing. Quiet room ambience and a small physical contact sound may be planned separately; do not make native audio capability an assumption.
```

**Optional movement variant:** replace only the camera paragraph if movement is authorized and useful: “Hold the camera during placement and release. Once the hand is visibly clear, make a small lateral move toward the holder's front-right side, staying on the established side of the action. End with the holder's support still readable.” This is a different prompt variant, not an additional simultaneous move. Do not include both alternatives in a final prompt.

**Failure and repair:** if the fingers release while the card is still floating, preserve light, prop design and framing; strengthen the support-transfer order and remove the optional camera move. Test actual motion around seating/release. A still showing the final upright card does not prove that the contact sequence succeeded.

## 3. Continuity is a state plus a real carrier

Record required continuity independently from readiness. `strict` remains strict when a required reference is missing; readiness becomes blocked or incomplete. A user's acceptance is needed to relax that requirement, not to inspect an already authorized local asset.

```yaml
continuity_edge:
  source_id_revision: Unknown
  next_request_id: Unknown
  requirement: "strict / approximate / explicitly free"
  protected_properties: []
  actual_carrier_binding: Unknown
  inspected_terminal_range_method: Unknown
  terminal_state:
    body_and_gaze: Unknown
    hand_prop_support: Unknown
    world_geography_and_screen_travel: Unknown
    camera_position_and_motion: Unknown
    light_environment: Unknown
    audio_tail: Unknown
  next_opening_state: Unknown
  operation_surface_verified: Unknown
  readiness: "pending required source/capability checks"
```

This is a planning record, not API payload. Reference names in text do not attach a file. A terminal frame supplies visual state at one instant; it does not establish the preceding speed, sound tail or full path. Use available actual clip evidence for those properties.

## 4. Extension decision tree

1. **What must continue?** If the user wants a genuine temporal continuation, retain that requirement. If they want another related shot, identify it as a new shot. Do not rename the latter “native extension.”
2. **Is the source clip present and bound to the intended operation?** If absent, a conceptual continuation may be drafted, but execution is not ready. A description or remembered ending is not the source.
3. **What was actually inspected?** Metadata establishes only read properties. Frames may support pose/geography. Inspecting a relevant moving interval may support velocity and action phase. Audio needs its own evidence. Report what remains unknown.
4. **Does the exact current surface support the operation and input?** Verify provider documentation when selected. If unverified, return a neutral continuation blueprint. Do not invent a duration extension field, overlap control or frame count.
5. **Can the requested continuation begin from the actual terminal state?** Resolve ongoing action before introducing a new action. Preserve support, gaze, travel, camera and light; allow physically necessary consequences.
6. **How will the seam be checked?** Review the last source interval, the boundary and the first continuation interval in the actual combined moving result. Check picture and audio separately, then together where possible. A single matching frame is insufficient.

If native extension is unavailable, state the concrete alternatives and their limitations: an authorized frame-conditioned next shot, editorial coverage, or a changed plan. Do not silently substitute one for a strict seamless continuation. Carry existing execution authorization; no extra approval is needed merely because the owner changed.

### Worked extension B — finish an action already in progress

**Fictional training scenario, not a current asset inspection:** the example assumes an accepted source clip ends with a performer carrying a plain cup toward an empty shelf. In the hypothetical final moving interval, the cup is upright in the right hand; the body travels screen-left; the camera is stationary; the cup has not reached the shelf. The requested continuation completes placement without replaying the approach. Strict identity, cup and location continuity are required. No real clip is bound here; current model/operation, actual FPS, measured timing and audio are `Unknown`.

**Required before use:** replace the hypothetical state with observations of the actual authorized source; bind that source to a verified extension operation. If inspection reveals a different hand, support or travel state, revise the prompt before calling it ready. Do not claim this blueprint already extends a clip.

**Complete neutral continuation blueprint:**

```text
Continue the bound source clip from its actual terminal action; do not restart the approach. Preserve the accepted performer, wardrobe, plain cup, room, shelf geometry, stationary camera and light direction from the source. The right hand still supports the upright cup as the performer continues toward the shelf in the established screen-left direction. Complete the remaining approach without a cut or a new preparatory pickup. Bring the cup base into contact with the shelf before opening the fingers. Withdraw the right hand while the cup stays upright on the shelf, then settle the body naturally beside it. Keep the established camera side and composition. Do not introduce a second cup, another person, new lettering or dialogue.

Preserve the source's intended sonic perspective only through the actually supported audio route. Any cup contact effect must follow the observed contact; a separate post-audio plan is acceptable only when it fits the authorized workflow. Do not invent music, speech or an audible tail from the visual description.
```

**Review contract:** inspect continuity of cup support, screen travel, performer/location, camera and light at the seam; check that the approach does not restart and the hand releases after contact. Source audio coverage and continuation audio coverage remain separately recorded. A prompt preflight can pass while actual seam quality remains unverified.

**Two distinct repairs:** if the action resets, change the continuation's opening action instruction while retaining the carrier and accepted design. If identity changes despite a correctly bound source, investigate the carrier/operation route; more identity adjectives do not establish strict continuity. After repeated controlled failure, propose a changed structural route and explain any effect on the accepted seamless-continuation requirement.

## 5. Picture continuity and sound continuity are separate

An editorial audio bridge can connect attention across a cut, but it cannot prove a visual extension is seamless. If sound is planned independently, label it as a postproduction decision rather than a native generator feature.

**Original editorial example:** an approved sequence moves from an empty workshop view to a close view of a hand laying down a tool. The director wants anticipation. Let an authorized room activity sound belonging to the upcoming space begin before the picture cut, then retain its perspective consistently after the cut. Do not place the specific tool-contact sound before visible contact unless an intentional sound offset has been approved. The first choice is an editorial J-cut; it is not an exact-sync error or evidence that the generated video has native audio. Exact placement awaits the real edit and sound.

An L-cut can instead let a prior sound continue over a new image. Use only when that tail serves the approved transition. Audio Production Director supplies sound-source/cue details and audio review; this owner reviews their relation to picture. Preserve the exact accepted script from screenplay or Humanizer, and lyrics from Audio Production Director. No new dialogue is required to demonstrate an audio bridge.

## 6. One-cause repair table

| Actual observation or labelled report | First discriminating check | One structural change to test |
|---|---|---|
| Contact hidden by a shoulder | Does blocking obscure the only proof of support? | Move the performer/prop within the accepted camera view before adding a cut |
| Camera motion overwhelms small action | Can the required event be followed at actual playback? | Hold the camera through the critical action |
| Subject reverses screen travel | Did camera side change, or did the body reverse? | Restore the relevant geographic relation; avoid vague “consistent direction” alone |
| Prop floats after release | Which frame/interval loses support? | Make contact-before-release the primary action and simplify competition |
| Extension repeats the source event | Is the prompt describing the whole source rather than its remaining action? | Begin at the observed action phase and remove the replay |
| Seam looks matched in stills but jumps in motion | Was velocity/camera motion actually reviewed? | Match the moving state using the actual source operation; do not certify from stills |
| Sound feels late or detached | Is it causal sound or an authored bridge? | Repair the specific event relation after inspecting combined playback |
| Board requires new angles for a locked shot | Was layout variety confused with shot coverage? | Repeat the approved framing at different temporal states |

For user reports, use “reported” and present a test rather than an observed diagnosis. Picture/motion and AV review stay here; audio triage goes to Audio Production Director without requiring a full task packet; output-critic-iteration owns static-image review. An attractive still is no substitute for motion QA.

## 7. Research basis and source-to-rule mapping

Checked 2026-09-28. All prompts and scenarios above are original local synthesis. These sources support bounded craft principles; neither documents a media-generation interface.

| Primary source / date / scope | Source → rule → example |
|---|---|
| [ARRI interview: Emmanuel Lubezki on Birdman](https://www.arri.com/news-en/emmanuel-lubezki-asc-amc-on-birdman-); 2014-10-22; cinematographer's first-person production account | Camera movement and performance/blocking were developed together for a storytelling purpose → specify why the camera moves in relation to action → A holds during contact and treats the later reveal as a deliberate alternative |
| [Adobe Premiere: J-cuts and L-cuts](https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/perform-j-cuts-and-l-cuts.html); updated 2025-08-22; editorial audio/picture overlap | An incoming sound can precede its image; an outgoing sound can continue under the next image → specify the sound and picture seam independently → the workshop example separates atmosphere anticipation from tool contact |

The ARRI account is not a universal demand for a moving or long-take camera. The Adobe terminology does not imply an editing integration. Current provider limits and controls require new verification for the exact requested surface and operation.
