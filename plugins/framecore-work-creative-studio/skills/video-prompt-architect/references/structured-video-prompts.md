# Structured (JSON) video prompts

Checked 2026-10-25 on the makers' own guides unless a row says otherwise. Read when a user asks for a JSON video prompt, when a shot plan has several shots, speakers or references, or when one plan must be compiled for several generators. The phrasing per generator stays in [generator dialects](generator-dialects.md); this card decides the shape and how it is compiled.

## What the evidence says

- **No video maker's guide documents a JSON prompt that its model reads.** Google Veo ([prompt guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide), [DeepMind guide](https://deepmind.google/models/veo/prompt-guide/)), OpenAI Sora 2 ([cookbook guide](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide)), Runway ([text to video](https://help.runwayml.com/hc/en-us/articles/42460036199443-Text-to-Video-Prompting-Guide)), Seedance 2.0 and 2.5 ([2.0 guide](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide), [2.5 guide](https://docs.byteplus.com/en/docs/ModelArk/2607689)), Alibaba Wan ([guide](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt)), LTX ([guide](https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide)), MiniMax ([guide](https://platform.minimax.io/docs/guides/video-generation)) and Higgsfield describe prose, labelled blocks, shot lists, timestamps or bracket notations. A third-party claim that Seedance 2.5 "requires JSON" is not in its official guide. Pika's and Luma's prompt guides were not read: Unknown.
- **Real structure exists only as API fields:** Kling's multi-shot (`multi_shot`, `shot_type`, `multi_prompt[{index, prompt, duration}]`, up to 6 shots, each at least 1 s, durations summing to the total; [Kling API](https://kling.ai/document-api/api/video/3-0-omni/text-to-video)) and Sora's `seconds`, `size`, `characters` and `input_reference`. The prompt inside each field is still a plain string.
- **Measured evidence is weak:** one practitioner test on Veo 3 Fast (four scenarios, first takes, no seed control) found no real difference on simple scenes and easier editing with JSON on complex ones (secondary). No peer-reviewed comparison exists.
- **What the guides agree on is content, not syntax:** one camera move and one clear action per shot (Sora), contiguous timestamps without gaps (Seedance 2.5, Runway, Veo, Wan), the same words for a character in every shot (Sora), labelled speakers with short lines (a 4 s shot fits one or two short exchanges, Sora), audio in its own sentences or block (Veo, Sora), positive phrasing instead of "no" (Veo, Runway, Seedance), and duration, size and audio as settings, not prose (Sora: asking for them in prose does nothing).

## The rule Studio follows

1. **Keep one internal record** per film (below): the approved shot card in a fixed shape, easy to diff and to change one shot.
2. **Compile it per generator:** settings into the API or app controls; the prompt into the generator's own notation from [generator dialects](generator-dialects.md) and the table below. Do not send the raw JSON as the prompt string.
3. **Label the output:** "Studio planning record", "Kling multi_prompt payload" or "prompt for {model}". A planning record is never presented as a model's schema.

## Internal record

| Field | Rule | Grounded in |
| --- | --- | --- |
| `target` | Generator, surface (app, API, aggregator) and mode (text, image, first and last frame, reference, extend, edit) | Each maker's capability page |
| `settings` | `duration_s`, `aspect_ratio`, `resolution`, `audio`, `seed`: compiled to parameters, never prose | Sora guide; Kling settings; Veo 3.1 page |
| `references[]` | `id`, kind (image, video, audio), role (first frame, last frame, character, style, voice, motion) and the label the generator expects (`<<<image_1>>>`, "Image 1", `<FIRST_FRAME>`, Sora `characters`) | Kling; Wan; Seedance; Gemini Omni; Sora |
| `summary` | One sentence for the whole clip | Seedance 2.5 opens with one; Veo's formula |
| `style` | Medium, film look, grade, three to five palette anchors | Sora; Veo; Wan stylization |
| `subjects[]` | `id` and identity anchors (age, hair, wardrobe, distinctive traits, voice), repeated word for word in every shot | Sora; LTX; Veo |
| `setting` | Location, time of day, weather, atmosphere | Veo; Wan; LTX |
| `lighting` | Sources, quality, direction; the same logic across cuts | Sora; Veo |
| `shots[]` | `index`, `start_s`, `end_s`, framing and angle, lens, one `camera_move`, one main action (or a short ordered `beats` list), `dialogue[]`, `sfx[]`, `transition_in` | Sora; Runway, Veo, Wan and Seedance timestamps; Kling shot limits |
| `dialogue[]` | `speaker`, `line`, `delivery` (emotion, tone, speed), `language`; short lines | Sora; Wan voice formula; Seedance 2.5; Kling speaker binding |
| `audio` | Ambience, effects, music (or explicitly none) | Veo; Sora; Wan; Seedance |
| `on_screen_text[]` | Normally empty: exact copy goes on an [exact layer](exact-layers-in-video.md) after generation | Studio rule; Seedance offers text templates and no-subtitle phrases |
| `avoid[]` | Compiled per model: Veo negative-prompt nouns, positive rephrasing for Runway and Seedance, in-prompt negatives where Kling allows them | Veo; Runway; Seedance; Kling |
| `end_frame` | Optional last-frame composition | Veo first and last frame; MiniMax; Luma keyframes |

Checks before compiling: shots start at 0 and touch without gaps or overlaps, their durations sum to `settings.duration_s`, each shot has one camera move, dialogue fits the shot (a short exchange per few seconds), every subject's anchors are the same words in every shot, and nothing in `summary` or `shots` asks for a setting ("make it 10 seconds", "16:9").

## Compile targets

| Generator | Compile the record to |
| --- | --- |
| Veo 3.1 | Prose in the order cinematography, subject, action, context, style and ambiance; optional `[00:00-00:02]` segments for several shots; audio in separate sentences; exclusions as negative-prompt nouns |
| Sora 2 | A prose scene, then headed blocks `Cinematography:`, `Actions:` (bullets), `Dialogue:` (labelled speakers), `Background Sound:`; for an exact cut, a timed shot list; `seconds`, `size`, `characters` and `input_reference` as API fields |
| Runway Gen-4.5 | Visual and motion description in prose, rough timestamps within the clip; positive phrasing only |
| Kling 3.0 | One prompt string, or custom multi-shot: `multi_prompt[{index, prompt, duration}]` (API) or `shot n, …` in the app; speaker and tone before each line; Polish dialogue is translated to English by the model, so record it separately |
| Seedance 2.x | One-sentence summary, the plot, then a timeline without gaps; the official notation: dialogue in `{}`, sound effects in `<>`, music in `（）`, subtitles in `【】`; bind subjects to images (`<Subject_1>@<Image_1>`); positive constraints ("no subtitles") |
| Wan | Entity, scene and motion, then light, shot size, angle, lens and camera move; several shots as `Shot 1 [0-3 s] …`; voice as line plus emotion, tone, speed |
| LTX | One flowing paragraph in the present tense, about four to eight sentences; no shot list or numbered beats unless each cut is also described in prose; dialogue in quotes |
| MiniMax H3 | Prose with camera commands in square brackets after the description they belong to |

Dialogue formatting conflicts between models (quotes for LTX and Sora, braces for Seedance); use the target's own form and never paste a prompt written for another model (LTX warns against it).

## Pitfalls

- Too many beats or camera moves in one shot; a timestamp too short for the action (Runway: half a second does not fit a walk).
- Timeline gaps or durations that do not add up (Seedance 2.5, Kling).
- Dialogue longer than the shot can hold; long speeches do not sync (Sora).
- Conflicting traits between shots change a character's identity (Sora); conflicting geography between cuts (LTX).
- "No" and "don't" wording (Veo, Runway, Seedance).
- Settings written as prose (Sora).
- Raw JSON in a prompt field: braces and keys are read as text. No primary report was found of a model speaking keys aloud or showing them on screen, but compile to the generator's notation anyway.
- Platform churn: the Sora app closed on 2026-04-26 and the Veo 3.1 preview in the Gemini API was shut down; recheck the generator before a final prompt.

## Unknown on 2026-10-25

Whether any video model was trained or tuned on JSON prompts; the full text of Google's "ultimate prompting guide for Veo 3.1" (read through re-publications); Gemini Omni's stance on JSON; Pika's and Luma's prompt guides; Kling 4.0's API fields; official guidance on dialogue length per second for Seedance and Kling; the Sora Videos API shutdown date (secondary only); a seed-fixed JSON-versus-prose benchmark.
