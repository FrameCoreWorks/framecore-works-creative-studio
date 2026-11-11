# Owner scope: complete YouTube animation and VideoLyrics

Recorded 2026-11-11 from the owner's request. This is a requirements supplement for Claude to assess, not completed new research, an implemented mode or an approved plugin architecture. It remains separate from the independent Deep Research prompts. Their reports are not published by this transfer.

## Desired outcome

FrameMotion needs the professional knowledge to help produce complete, coherent animated works for YouTube: children's cartoons, narrative stories, explainers, songs and music videos. A finished deliverable includes picture, sound, readable text where needed and checked export, rather than an isolated motion demo. A substantial VideoLyrics workflow should combine authored animation/code with generative images/video and edited music. Delivery ready for upload does not authorize publishing to an account.

## Knowledge and decisions to assess

| Area | Practical capability and evidence needed |
|---|---|
| Story and preproduction | Convert intent, audience and duration into a script, beats, shot plan, boards and timed animatic. Identify what each shot communicates; test comprehension and pacing before expensive animation. Reuse current screenplay/storyboard owners where appropriate. |
| Series and character continuity | Maintain a character/style bible, model sheets, proportions, expressions, costume, palette, environment rules and reusable poses. Plan rigs or cutout/vector/3D/generative methods by shot, including acting, staging, silhouettes, eyelines and continuity across revisions. A character-consistency prompt alone is insufficient evidence. |
| Animation craft | Plan poses, timing/spacing, anticipation, overlap, arcs, weight, holds, transitions, camera and depth. Separate shot-local motion from editorial timing; preserve editability and deterministic evaluation where the backend supports it. Explain when drawing, rigging, 3D or generative footage is appropriate and when a hybrid/native operation is required. |
| Dialogue and songs | Work from an approved script/recording, pronunciation and emotional intent. Plan dialogue editing, breaths, mouth/viseme timing when needed, music structure, foley/ambience/SFX and final mix. Track recording or generation rights and actual audio revisions. Do not assume successful transcription proves accurate singing alignment. |
| Children's productions | Define the intended age and understanding level, clear cause/effect, vocabulary, visual readability and pacing. Evaluate story clarity, tone, overstimulation and audio comfort with appropriate human review; avoid a universal retention formula or a claim of educational effectiveness without evidence. Confirm current platform/audience requirements during a real delivery task. |
| Production management | Preserve shot/asset identity, provenance, versions, approvals, dependencies, regenerate-versus-reuse decisions and bounded costs. A changed lyric, voice take, rig or generated shot must invalidate dependent sync/render checks explicitly. |

## Expanded VideoLyrics requirements

1. Treat approved lyrics, sung performance, translations and music timing as versioned inputs. Represent phrase/word/syllable alignment at appropriate precision, with human correction for melisma, pickups, breaths, rubato and overlapping voices; do not derive every word change from beat detection.
2. Choose a visual concept and story/energy progression across intro, verse, chorus, bridge and outro. Synchronize motion to musical meaning as well as beats; decide when lyrics lead, follow, hold or yield to the image. Maintain a usable quiet/resting state.
3. Preserve typography, Polish diacritics, shaping, safe areas, line breaks, contrast and enough reading time. Handle repeats, dense passages and instrumental sections explicitly. Distinguish decorative lyric animation from accessibility captions and from translated subtitles.
4. Combine code-generated type/shapes/compositing with permitted generated plates or shots through explicit media contracts: dimensions, duration, FPS/time basis, color, alpha, crop, motion continuity and provenance. Check generative transitions, flicker, character identity and unintended content; re-generation must be a bounded choice, not an untracked retry loop.
5. Maintain global editorial time in the owning timeline and frame-accurate local animation timing, with explicit sample/frame conversions and duration changes. Avoid duplicate master clocks between FrameCut and FrameMotion. Use existing contracts after inspecting them rather than inventing a parallel schema in this note.
6. Supply a final picture/audio export, an editable project or reconstruction package where supported, source/provenance manifest, caption/lyric sidecars if requested and a QA record. Evaluate full playback and representative transitions in addition to still frames or decode.

## Ownership and evaluation proposed for Claude

Preserve Studio's production coordination, the current story/board/audio/caption owners, Open Assets' acquisition/provenance, FrameCut's editorial timeline and finishing, and FrameMotion's animation/compositing craft. Claude should decide which knowledge FrameMotion must own or reference to work independently without cloning all of Studio. This table is a starting point for that analysis, not a new binding architecture.

Prepare a capability-gap map and the smallest coherent implementation stages, with each proposed operation mapped from manual professional practice to an agent decision, data, backend limits and an observable output. Suggested later acceptance exercises (all **NOT_RUN**): a short character story with dialogue and continuity; an explainer combining diagram/text/voice; a children's song with repeat/verse variation; and a VideoLyrics sequence with Polish text, variable vocal timing, instrumental rests and a generative plate. Test at two aspect ratios where requested, seek frames out of order where deterministic rendering is promised, and inspect/listen to complete results. Record story/art direction judgments separately from technical validity.

Do not install new renderers, run paid generation, publish to YouTube or claim native-app equivalence merely from this scope. The owner has asked to preserve and deepen this capability direction; implementation remains subject to Claude's applicability analysis and the authorized task.
