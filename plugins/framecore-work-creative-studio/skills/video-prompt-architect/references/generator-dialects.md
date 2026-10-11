# Video generator dialects

How to phrase a prompt for the generators users name most, so one approved shot card becomes the right words for each tool. Read on 2026-10-11 from the makers' own guides where they loaded; a line marked *secondary* comes only from third-party guides and is a lead to check, not a rule. Model identities, versions and operations are in the [video generator snapshot](../../research-evidence/references/video-generator-snapshot.md); this card adds the phrasing.

## How to use the card

- **Fresh check first.** With browsing, reread the named model's guide before a final prompt and note any difference here as a proposed card update. Without browsing, use the card provisionally, say once that the phrasing was last checked on 2026-10-11, and keep the prompt to the parts every model reads the same way (subject, action, setting, camera, light, sound).
- **Refresh cadence.** Recheck a card every 60 days, at a new major version, or when a user's output contradicts it; keep the old line until the new one is confirmed.
- **The user's tool.** The user names the generator and the surface (the maker's app, its API, or a multi-model surface such as Runway, Firefly, Freepik or an aggregator). A hosted model can expose fewer controls than its maker documents; write for the surface the user will paste into.
- **One shot card, many dialects.** Keep the approved shot card neutral (subject, action, camera, light, sound, duration, aspect) and translate it per tool below; [`prompt_pack.py`](../scripts/prompt_pack.py) exports the result and checks it before credits are spent.

## Where users meet these models

| Model | Maker's consumer surface | Also on |
| --- | --- | --- |
| Veo 3.1, Gemini Omni | Gemini app, Flow | Gemini API, Vertex AI, Runway and other multi-model surfaces |
| Kling 3.0 | Kling app and web (kling.ai) | Kling API, aggregators |
| Seedance 2.x | Dreamina | BytePlus ModelArk, Runway |
| MiniMax H3 | Hailuo AI | MiniMax API, open weights |
| Runway Gen-4.5, Aleph | Runway app | Runway API |

A model reached through another surface follows that surface's controls and limits; check them there.

## Google Veo 3.1

- **Structure.** Subject, action and style, then optionally camera position and motion, composition, focus and lens, and ambiance (colour and light). Use "portrait" for faces. Descriptive, clear sentences rather than keyword lists.
- **Sound.** Audio is always generated. Put spoken lines in quotes; describe sound effects explicitly; describe the environment's soundscape for ambience.
- **Settings, not prose.** Aspect ratio `16:9` or `9:16`; duration 4, 6 or 8 s (8 s for extension, reference images, 1080p and 4K); 720p default. People: text to video and extension allow all ages, image to video, interpolation and reference images adults only, and only adults in the EU, UK, Switzerland and MENA.
- **Polish speech.** The guide lists no spoken languages; generate one short quoted Polish line first and listen before writing a whole scene in Polish.
- Source: [Gemini API Veo guide](https://ai.google.dev/gemini-api/docs/veo), read 2026-10-11.

## Runway (Gen-4.5)

- **Text to video.** `[Camera] shot of [subject] [action] in [environment]. [Supporting details]`, with both visual and motion descriptions.
- **Image to video.** The image sets composition, subject, light and style and is the first frame; the prompt describes motion almost only: `The camera [motion] as the subject [action].` Describe visuals only for new elements or a transformation.
- **Phrasing.** Describe what you want to see, not what you don't; concrete, observable words; no contradictions; avoid multi-paragraph prompts. Sequences: "X, then Y. Finally Z." or rough timestamps such as "[00:01]", within the clip length.
- **Fixes.** Unwanted cuts: a longer duration or "Continuous, seamless shot". Less motion: "locked-off camera", "Minimal subject motion only". Longer scenes: start the next clip from the last frame and join them in an editor.
- Source: [Runway Academy prompting guide](https://academy.runwayml.com/guides/prompting-guide), read 2026-10-11.

## Kling VIDEO 3.0

- **Shots.** One shot by default; with Multi-Shot on, the model plans the cuts; Custom Multi-Shot sets each shot's content and duration ("shot 1, profile shot of ..., cinematic handheld"). Total 3 to 15 s, 720p or 1080p.
- **Timing words.** Beats can be placed in prose ("At the 4th second, the camera ...").
- **Dialogue.** Attach every line to its speaker, with tone in parentheses before the line: `Boy (in an excited tone): "..."`. Spoken languages: Chinese, English, Japanese, Korean and Spanish, mixed in one video if needed; **dialogue in another language, Polish included, is translated into English**, so a Polish voice-over must be recorded or generated separately and added in the edit.
- **Consistency.** Bind a subject as an Element (2 to 4 reference images, or a character video); when the Element has a bound voice, do not set its tone again in the prompt.
- Source: [Kling VIDEO 3.0 user guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide), read 2026-10-11. Prompt length limit of 2,500 characters: *secondary*.

## MiniMax H3 (Hailuo)

- **Camera.** Put camera instructions in square brackets right after the description they belong to, for example `[pan]`, `[zoom]`, `[static]`; the guide gives no complete list.
- **References.** Refer to inputs by role and number in plain words: "following the motion in reference video 1; the character's appearance follows reference images 1 and 2". Up to 9 images, 3 videos and 3 audio clips (12 files).
- **Settings.** H3: 4 to 15 s, 768p or 2K; H3 Max: 5 to 15 s, 480p or 768p. Text to video needs an explicit aspect ratio; image to video takes the image's. Prompts up to 7,000 characters.
- Source: [MiniMax video generation guide](https://platform.minimax.io/docs/guides/video-generation), read 2026-10-11. The consumer app is Hailuo AI.

## ByteDance Seedance 2.x (Dreamina)

- **References.** Up to 9 images, 3 videos and 3 audio clips with text (Seed blog, read 2026-10-09). Name each reference's job in the prompt ("the composition of image 1", "the dance from video 2"); the `@image1`-style tags circulating in guides are *secondary*, and the official prompt guide (BytePlus, updated 28 September 2026) did not render here.
- **Shots and sound.** Multi-shot output up to 15 s (2.0) or 30 s (2.5) with joint audio; describe the cut order in sentences and the sound per shot.
- **Real faces.** Media with real faces are restricted on BytePlus; use approved, non-identifying references or the user's own consented material.
- Sources: [Seed blog](https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0) and [BytePlus blog](https://www.byteplus.com/en/blog/dreamina-seedance2-5), via the snapshot.

## Every generator

- **On-screen text.** No generator is the place for exact copy: generate the picture without words and set supers, prices and logos afterwards ([text in images and video](../../pipeline-core/references/text-image-generation-policy.md)).
- **Brand and people.** Only approved references; no real person's likeness or voice without consent; no competitor's ad as a reference.
- **Report honestly.** A prompt is untested until its output was generated and inspected; say which generator, surface and settings the prompt was written for.
