# Narrative (prose) video prompts

Checked 2026-10-25 on the makers' own guides unless a row says otherwise. Read when compiling a prose prompt for a named video generator. Every video generator reads prose (see [structured video prompts](structured-video-prompts.md) for the planning record); [generator dialects](generator-dialects.md) holds the per-model settings and limits checked on 2026-10-11, and this card adds the order, length and phrasing found on 2026-10-25. Where the two differ, the newer row wins and the dialects card is refreshed.

## Order of sentences (synthesis of the guides and measured evidence)

1. **Shot and style first:** shot size, angle, genre or look (Runway's template, Firefly's formula, LTX, Sora "establish style early").
2. **Subject with two or three identity anchors** (age, wardrobe, one distinctive trait), the same words in every clip of a series (Sora, LTX). Use the generator's own identity tools where they exist (Sora characters, Kling elements, Luma character reference).
3. **Setting and one lighting logic** for the shot (LTX; Sora's three to five palette anchors).
4. **One action with visible verbs, anchored, not scripted** ("takes four steps, pauses, pulls the curtain in the final second"; Sora, LTX, Luma). Fix what must happen (the key action, a contact or reveal, the end state) and describe how the motion feels (weight, speed, rhythm, energy, physical behaviour); leave the in-between movement and secondary motion to the model. Use timed beats only where timing matters (a sync point, a reveal at a set second, the target's own timestamp syntax) or the user asks. A step-by-step list of every move makes the result stiff: the model executes it mechanically, with no room for natural motion (practitioner report 2026-10-30).
5. **One camera move, relative to the subject,** and where it ends (Sora, LTX, Runway).
6. **Audio, each part in its own sentence:** ambience, effects, music or "no score" (Veo, LTX, Sora).
7. **Dialogue last,** one labelled line per speaker with its delivery, in the target's own form.

Present tense; one paragraph for a single shot (LTX explicit). Length: LTX four to eight sentences per shot, Luma two to four. Dialogue: Sora fits one or two short exchanges in 4 s; no maker states words per second (Unknown), so Studio's [prompt record check](../../pipeline-core/assets/prompt-record/README.md) only warns above three words per second.

**Why one action per shot:** measured on many models, prompts with several events drop or reorder them ([MinT](https://arxiv.org/abs/2412.05263)); no model completes more than half of two- to four-event stories ([StoryEval](https://arxiv.org/abs/2412.16211)); later events are suppressed by the opening scene ([TPD](https://arxiv.org/abs/2607.26706)). Split a sequence into shots or clips; Sora notes that two 4 s clips can beat one 8 s clip.

**Image to video:** describe motion and change only, not what the image already shows (Runway, Gemini Omni); keep one continuous take unless a cut is intended (LTX).

**Settings stay settings:** duration, size, resolution and character IDs are parameters ("make it longer" does nothing; Sora).

## Per model

| Generator | Order and length | Camera and action | Dialogue and sound | Several shots in prose | Exclusions | Rewriter | Source (read 2026-10-25) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Veo 3.1 (Vertex AI) | Subject, action, scene, camera angle and move, lens, style, temporal elements, audio, cinematic terms; no required order; more detail, more control | Name framing and movement; for fast action write play by play | Audio in separate sentences; the Vertex guide shows dialogue as a colon cue (`the detective says: …`); effects and ambience apart | Cuts named in prose; no timestamp syntax documented on Vertex | The negative-prompt field as a noun list, without "no" | On by default; `enhancePrompt: false` turns it off (official page seen only as a search excerpt) | [Vertex guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide), [DeepMind guide](https://deepmind.google/models/veo/prompt-guide/) |
| Gemini Omni Flash (`gemini-omni-1.1-flash`; replaces the Veo 3.1 preview in the Gemini API, shut down 2026-10-22) | Scene, camera move, light, mood; very detailed characters and places | Several shots by default: write "a single continuous shot", "No scene cuts" | Audio by default: describe it, "No dialogue" to remove speech | Free prose or `[0-3s]` timecodes | No negative field: write "No …" in the prompt | Unknown | [Omni guide](https://ai.google.dev/gemini-api/docs/omni) |
| Sora 2 | Prose scene, then `Cinematography:`, `Actions:` (beats), `Dialogue:`, `Background Sound:`; shorter clips follow better | One clear camera move and one subject action per shot | Labelled speakers, alternating, short lines; long speeches sync poorly | One block per shot; a timed shot list for exact cuts | Positive specifics ("Avoid signage" in examples) | Unknown | [Sora 2 guide](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) |
| Runway Gen-4, Gen-4.5 | Text to video: `[Camera] shot of [subject] [action] in [environment]. [Details]`; image to video: `The camera [motion] as the subject [action]`; avoid multi-paragraph prompts | Gen-4: one scene per clip; still shot: "the locked-off camera remains perfectly still" | Not covered in the guides read | "X, then Y. Finally Z." or `[00:01]` timestamps paired with prose | Positive phrasing only | Unknown | [Runway Academy](https://academy.runwayml.com/guides/prompting-guide) |
| Kling 3.0 | Setting, subject, action, camera, then dialogue (from the examples); 3 to 15 s | Camera terms in prose; "At the 4th second …" | `Name (tone): line`; Chinese, English, Japanese, Korean, Spanish; any other language is translated to English; a voice bound to an element keeps its tone | Multi-Shot plans cuts from prose; Custom Multi-Shot (`Shot 1, …`) is followed strictly | Unknown | Unknown | [Kling 3.0 guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide) |
| Seedance 2.0 | Subject, action details, scene, light and colour, camera move, style, quality, constraints; events in order; up to 15 s | Shot size and move terms | Dialogue `{…}`, music `（…）`, effects `<…>`, subtitles `【…】`; one dialogue language | `Shot 1 / Shot 2` only: it does not follow timestamps | Explicit constraints ("keep it subtitle-free", "no logo or watermark") | Not found | [Seedance 2.0 guide](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide) |
| Seedance 2.5 | Subject, location, event, genre, camera; up to 30 s | Shot, move, angle vocabulary | `{line}` or `Character's line (emotion): …`; more than 10 languages | 1 s timestamps or `Shot N`, each with picture, camera, action, dialogue, effects | "No subtitles, watermarks, logos, garbled text" | The maker's own optimizer skill | [Seedance 2.5 guide](https://docs.byteplus.com/en/docs/modelark/seedance-2-5-prompt-guide) |
| LTX-2 | Shot, scene, action as a verb sequence, characters (emotion through physical cues), camera, audio; one flowing paragraph, present tense, four to eight sentences | Camera relative to the subject; one light logic | Dialogue in quotes with language and accent; validated in English, French, Spanish, German, Russian | One chronological paragraph; at each cut name the transition and re-establish framing; two to four shots | Not covered; add critical on-screen text in post | Optional enhancer, not for direct API use | [LTX guide](https://docs.ltx.io/api-documentation/implementation-guides/prompting-guide) |
| Luma Ray3 | Subject, action, setting, secondary motion, camera, light; two to four sentences | Mid-action verbs and their consequences | No audio | Unknown | Positive only; avoid vague words such as "vibrant" | Unknown | [Ray3 FAQ](https://lumalabs.ai/learning-hub/ray3-faqs) |
| Wan 2.2 | Full descriptive sentences | Unknown | Unknown | Unknown | Unknown | Prompt extension off unless the flag is set | [Wan 2.2](https://github.com/Wan-Video/Wan2.2) |
| Adobe Firefly video | Shot type, character, action, location, aesthetic | Shot size, angle and motion also in the interface settings: keep them consistent | Not covered | Unknown | Not covered | Unknown | [Firefly video](https://www.adobe.com/learn/firefly/web/create-ai-video-with-text-prompts) |
| MiniMax H3, Pika 2.5 | No official prose guide found; bracketed camera commands for MiniMax are in its API guide ([generator dialects](generator-dialects.md#minimax-h3-hailuo)) | | | | | | secondary only |

## Pitfalls

- **Too many actions** in one shot: events drop or reorder (measured above).
- **Contradictions:** "completely motionless" with an image full of motion blur; several light sources with different logic.
- **Unwanted cuts:** Omni cuts by default; Runway: "continuous, seamless shot" and a longer duration.
- **Unwanted subtitles or text:** Seedance's explicit "no subtitles" line; generated text is unreliable, add copy in post on an [exact layer](exact-layers-in-video.md). Whether quotation marks make Veo draw subtitles is practitioner lore with no Google statement.
- **Negative wording** fails on Runway and Luma; Veo wants nouns in its negative field; Omni and Seedance document explicit "No …" lines. Follow the target.
- **Copying a prompt between models** (LTX warns against it): brackets, labels and timestamp support differ.
- **Re-describing the input image** in image to video.
- **Unsupported dialogue languages:** Kling translates to English; LTX validated five languages; Seedance 2.0 takes one language per prompt.
- **Rewriters change intent** (measured: [VPO](https://arxiv.org/abs/2503.20491)): turn them off when exact wording matters.

## Unknown on 2026-10-25

Veo 3.1's image-to-video page, prompt length limit and whether every variant can turn the rewriter off; Omni Flash's length and rewriter; Runway Gen-4.5 dialogue; official MiniMax, Pika and Wan prose guidance; Kling's negatives and prompt length; dialogue words per second for any model; any measured comparison of prose, labelled prose and JSON on commercial generators.
