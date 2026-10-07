# Motion contract JSON

One file, `motion-score.json`, carries the storyboard, the approval state and the technical timeline. The same file is presented to the user as a storyboard, approved, read by the runtime starters and the single-file preview, and used for review. This replaces keeping a Markdown storyboard and a separate code timeline in sync by hand. The Markdown [storyboard contract](../templates/motion-storyboard-contract.md) remains the full field checklist and the human-readable view.

## Lifecycle

1. **Draft.** Write the contract with `approval.status: "proposed"`. Keep unknown brand decisions in `decisions.unknown` and proposals in `decisions.proposed`.
2. **Present.** Show the storyboard as a table. In a shell-capable host run `node check-score.mjs motion-score.json --markdown`; elsewhere render the same table in the reply. Do not show raw JSON to a non-technical user unless asked.
3. **Approve.** On the user's explicit approval set `approval.status: "approved"`, `approval.revision` to the current `revision`, and `approval.evidence` to where and when approval was given. A direct request to build a complete brief counts as approval of that revision: use `approved` with evidence quoting the request. Otherwise keep `proposed`. Use only the four listed states; never invent another. Any change to copy, locks, timing or concept increments `revision`, which invalidates the old approval for the affected decisions.
4. **Check.** `node check-score.mjs motion-score.json --storyboard` requires a complete storyboard; without the flag it checks timeline, copy references and reading holds only.
5. **Build and review.** Runtimes read the same file. Review compares the output with `acceptance`, scene `acceptance` and the readable holds.
6. **Revise.** A change to a delivered video starts from its contract and, when it was delivered, its render script; it changes only what was asked, increments `revision`, shows the user what changed (was → is) and renders with the same script, so unchanged parts stay pixel-identical. Files carry the revision in their names. See [contract revisions](../assets/motion-revise/README.md), whose `revise.mjs` lists differences and lengthens or shortens a scene while moving everything after it.

## Fields

Top level:

| Field | Meaning |
| --- | --- |
| `schema_version`, `id`, `revision` | Format version, contract ID and its current revision |
| `approval` | `{status, revision, evidence}`; status is `proposed`, `approved`, `blocked` or `example-not-client-approved`; an approved contract needs evidence for its current revision |
| `stage` | Requested stage: `storyboard`, `build`, `review` or `repair` |
| `goal`, `audience`, `message`, `concept` | What the film must achieve, for whom, the one message and the communicative mechanism |
| `style` | Optional ID of the [motion style](../assets/motion-styles/README.md) whose tokens and motion values were copied into the contract; renderers never read it |
| `runtime` | `{status, value}`; status is `selected`, `proposed` or `unknown`; a work-area choice never selects it. Optional `script`: the plain file name of the render script delivered with the video, such as `video-r2.render.py` |
| `viewing`, `audio` | Intended viewing size or placement, and the audio plan or intentional silence |
| `decisions` | `{confirmed, proposed, unknown}` lists keep the three states explicit |
| `fps`, `totalFrames`, `width`, `height` | Rational FPS `{num, den}`, integer frame count N (frames 0..N-1) and the base size |
| `formats` | Optional output variants `{id, width, height, viewing?, tokens?, params?}`; `params` maps scene IDs to param overrides. Timeline, copy and holds are shared; `base` is reserved for the base size. See [formats](../assets/motion-scenes/README.md#formats) |
| `tokens` | Colours, font family, margin ratio and optional `safeArea {top, bottom}` (fractions of the height, from platform documentation or the user) and caption style `captions {size, weight, color, background, bottom}` used by the code |
| `motion` | Tempo family, entry/exit frames, staggers, easing names and transition set from [motion craft](motion-craft.md) |
| `copy`, `copyStatus` | Exact copy by ID, verbatim; `copyStatus` such as `approved`, `proposed` or `illustrative` |
| `assets` | Asset ledger entries `{id, file, revision, role, authority}`; an empty list when none are used |
| `acceptance` | At least three observable, concept-specific criteria |
| `cues` | Optional sound cues `{id, frame, durationFrames, frequency, gainDb}` for the existing sound adapter |
| `music` | Optional beat grid and track `{bpm, offsetMs, beatsPerBar, src?, volume?}`; `offsetMs` is when the first beat sounds |
| `voiceover` | Optional voice-over track `{src, volume?}` |
| `sfx` | Optional sound cues `{frame, sound, gain?, pan?, params?, event?}` in frame order: `sound` is a [sound design](../assets/motion-sound/README.md#sound-designs) (`whoosh`, `impact`, `boom`, `riser`, `click`, `release`, `tick`, `knock`, `shimmer`), `gain` in dB (at most +6), `pan` from −1 to 1, `params` its design values; written by `sound.py plan` and editable by hand |
| `soundDesign` | Optional `{engine, density, status, seed, direction, music?}` from `sound.py plan`; `direction` records this video's profile (pace, moods, evidence), its choices with reasons and the effects' character; `music` holds the composed bed's `bpm`, `key`, `palette`, `backbeat`, `progression`, `seed`, `energies` per bar and `gain`, and `revealBar` and `revealFrame` when the final reveal is placed on a downbeat |
| `captions` | Optional `{id, start, end, copy}` list in order without overlap; `copy` is a copy ID holding the exact text. See [music and voice-over sync](../assets/motion-sync/README.md) |

Each scene:

| Field | Meaning |
| --- | --- |
| `id`, `purpose` | Stable scene ID and what the scene communicates |
| `kind`, `params` | Optional declarative [scene kind](../assets/motion-scenes/README.md) and its parameters; the scene engine renders it without custom code |
| `start`, `end` | Master-frame interval `[start, end)`; overlaps are intentional transitions |
| `copy` | Copy IDs shown in the scene |
| `holds` | Readable holds `[start, end)` inside the scene |
| `focalPoint`, `entry`, `action`, `exit` | Where the eye goes and how the scene enters, acts and leaves |
| `transition`, `persistence`, `audio` | Link to the next scene, what carries over, and the sound cue or silence |
| `acceptance` | Optional scene-level observable criteria |

The file stays compatible with `validateScore` in [the motion quality helpers](../assets/motion-quality/README.md); extra fields are ignored by runtimes and by that validator.

## Where the tools are

- `check-score.mjs` ships identically in the [Remotion kinetic type starter](../../remotion-video-production/assets/kinetic-type-starter/README.md) and the [GSAP motion starter](../assets/gsap-motion-starter/README.md), with `npm run check` and `npm run storyboard`.
- The [single-file preview](../assets/single-file-preview/README.md) embeds the same JSON.
- Without a shell, follow the same field rules by hand and state that the automatic check did not run.
