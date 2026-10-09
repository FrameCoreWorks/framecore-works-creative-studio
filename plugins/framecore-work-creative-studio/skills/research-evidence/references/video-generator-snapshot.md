# Video-generator families: audited snapshot

Snapshot date: 2026-10-09. Owner: `research-evidence`. Purpose: a dated starting map for identifying a named video generator, the operations it documents and where to recheck it before a model-specific prompt. It is not a ranking, a price list, a complete census or evidence that a model is exposed in the user's account or in this Studio's host. Music, song and voice generators are mapped separately in [music provider routing and rights](../../audio-production-director/references/music-provider-routing-and-rights.md).

## How to use this snapshot

When a user names a video generator, identify the exact product, version and surface they mean (the maker's app, its API, or a multi-model surface such as Runway, Adobe Firefly or an aggregator). Treat the named consumer product as the target when the surface is not named; ask one narrow question only when two plausible versions would change the prompt. A model hosted on another surface can expose fewer controls than its maker documents.

Before delivering a current model-specific prompt, recheck that model's official page. This file supplies identities, operation distinctions and leads, not permission to skip fresh research. Never say a prompt was tested unless that exact prompt was generated and its output inspected.

Operation labels:

- **T2V**: text to video. **I2V**: an image as the first frame.
- **First-last**: a start and an end frame, with the motion between them generated.
- **Reference-led**: images, clips or voice samples guide identity, style or sound without being the first frame.
- **V2V edit**: an existing video is changed (restyle, replace, relight, reframe).
- **Extension**: a generated clip is continued.
- **Native audio**: speech, effects or music generated with the picture.

`documented`: the maker's page read on 2026-10-09 states it. `docs via search`: the maker's page states it according to a search summary, but the page did not load here. `secondary`: only news, aggregator or third-party pages say so. `unknown` is not a yes. Sora appears only as a retired target.

## Coverage snapshot

| Family | Variants and IDs recorded 2026-10-09 | T2V | I2V | First-last | Reference-led | V2V edit | Extension | Native audio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Google Veo | `veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview`, `veo-3.1-lite-generate-preview` (Gemini API); Veo 3 (`veo-3.0-*`) deprecated | documented | documented | documented (3.1, 3.1 Fast) | documented, up to 3 images (3.1, 3.1 Fast) | unknown | documented (3.1, 3.1 Fast) | documented |
| Google Gemini Omni | Gemini Omni Flash (May 2026), `gemini-omni-1.1-flash` (27 August 2026) | documented | documented | documented (1.1) | documented: images, up to 3 s of video, voice references | documented, by conversation | documented (1.1), to 40 s | secondary |
| Kling (Kuaishou) | Video 3.0 and Video 3.0 Omni (5 February 2026); API IDs `kling-v3`, `kling-v3-omni` | documented | docs via search | docs via search | documented | docs via search (Omni) | unknown | documented |
| ByteDance Seedance | Seedance 2.0 (12 February 2026; BytePlus `dreamina-seedance-2-0-260128`, Fast and Mini variants), Dreamina Seedance 2.5 (BytePlus, 6 August 2026) | documented | documented | unknown | documented | documented | documented (2.0) | documented (2.0) |
| Alibaba Wan | `wan3.0-video`, `wan3.0-video-prime` (Model Studio) | documented | documented | documented | documented | unknown | unknown | docs via search |
| MiniMax | `MiniMax-H3`, `MiniMax-H3-Max` | documented | documented | documented | documented: images, videos, audio | documented (H3) | unknown | documented (H3) |
| Runway | `gen4.5`, `aleph2` (Aleph 2.0), `gen4_turbo`, `act_two` | documented | documented | unknown | unknown | documented (Aleph 2.0) | unknown | unknown |
| Luma | Ray3.2 | documented | documented | documented, up to 16 keyframes | unknown | documented (Modify Video, Reframe) | unknown | documented: none for T2V and I2V |
| xAI Grok Imagine | `grok-imagine-video-1.5`; `grok-imagine-video` for edits | documented | documented | documented (first, last, mid frames) | documented: up to 14 images, 3 voice samples | documented | documented | secondary |
| Midjourney | Video V1 (18 June 2025) | through an image | documented | unknown | unknown | unknown | documented | unknown |
| Lightricks LTX | LTX-2 (open weights, 6 January 2026), LTX-2.3 (5 March 2026) | secondary | secondary | unknown | unknown | unknown | unknown | secondary |
| OpenAI Sora | Retired: the Sora 2 models and the Videos API were removed from the API on 24 September 2026 with no replacement | retired | retired | retired | retired | retired | retired | retired |

## Family cards

### Google Veo

Gemini API model codes `veo-3.1-generate-preview` and `veo-3.1-fast-generate-preview` (preview, January 2026) and `veo-3.1-lite-generate-preview` (March 2026); Veo 3 (`veo-3.0-generate-001`, `veo-3.0-fast-generate-001`) is marked deprecated. Veo 3.1 and 3.1 Fast document T2V, I2V, first and last frame interpolation, up to three reference images and extension by 7 s up to 20 times (input up to 141 s at 720p, output up to 148 s); Lite documents T2V and I2V only. Clips are 4, 6 or 8 s at 24 fps, 720p by default, 1080p and 4K at 8 s (no 4K for Lite), 16:9 or 9:16; audio is always generated. The guide puts speech in quotes and describes effects and ambience explicitly. Vertex AI (Gemini Enterprise Agent Platform) uses different IDs such as `veo-3.1-generate-001`. Sources: [Gemini API Veo guide](https://ai.google.dev/gemini-api/docs/veo), read 2026-10-09.

### Google Gemini Omni

Gemini Omni Flash, introduced with Google I/O in May 2026 as the first Omni model: any combination of text, images, audio (voice references at launch) and video in, video out, edited by conversation, with a SynthID watermark ([Introducing Gemini Omni](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/)). Gemini Omni 1.1 Flash (`gemini-omni-1.1-flash`, 27 August 2026) adds scene extension in 10 s steps to 40 s, first and last frame generation, up to 3 s of reference video, 360p drafts, 720p standard and 1080p or 4K as upscaled output, in the Gemini API, AI Studio, the Gemini Enterprise Agent Platform and Flow ([Gemini Omni 1.1 Flash](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/)). Synchronized audio output is reported by secondary sources; the Google pages read here do not state it. Read 2026-10-09.

### Kling

Kuaishou's press release of 5 February 2026 launched Video 3.0 and Video 3.0 Omni: clips up to 15 s, native speech in English, Chinese, Japanese, Korean and Spanish with several accents, a multi-shot storyboard in Omni, and reference videos and images for consistent characters; early access for Ultra subscribers first ([press release](https://www.prnewswire.com/news-releases/kling-ai-launches-3-0-model-ushering-in-an-era-where-everyone-can-be-a-director-302679944.html), read 2026-10-09). Kling's API pages list `kling-v3` and `kling-v3-omni`, with 4K output, first and last frames in multi-shot generation and reference video in Omni according to search summaries; the pages did not load here. Kling 4.0: see the watchlist.

### ByteDance Seedance

Seedance 2.0, launched 12 February 2026: joint audio and video generation with two-channel audio, from text combined with up to 9 images, 3 video clips and 3 audio clips, up to 15 s of multi-shot output, extension with continuous shots and editing of clips, characters, actions and storylines ([Seed blog](https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0), read 2026-10-09). On BytePlus ModelArk, `dreamina-seedance-2-0-260128` and Fast and Mini variants are listed according to search summaries of the API reference. Dreamina Seedance 2.5, available on BytePlus from 6 August 2026: clips up to 30 s, up to 50 multimodal references, secondary editing of timestamps and characters; BytePlus is not available in the United States, and media with real faces are restricted ([BytePlus blog](https://www.byteplus.com/en/blog/dreamina-seedance2-5), read 2026-10-09). Also on Runway as `seedance2`, `seedance2_fast`, `seedance2_mini` and `seedance2_5`.

### Alibaba Wan

`wan3.0-video` combines T2V, I2V from a first frame or first and last frames, and reference-based generation, up to 30 s at 480p, 720p or 1080p; `wan3.0-video-prime` is the faster variant ([Model Studio model page](https://www.alibabacloud.com/help/en/model-studio/wan3-0-video), updated 28 September 2026, read 2026-10-09). The Wan3.0 guide describes generated dialogue, music and effects according to a search summary; the model page read here does not state audio output. Secondary sources report a public beta from 6 August and general availability from 24 August 2026, with closed weights.

### MiniMax

`MiniMax-H3`: T2V, I2V with first and/or last frame, reference generation from images, videos and audio, and editing; 4 to 15 s; 768p, with 2K by regeneration. `MiniMax-H3-Max`: faster, 5 to 15 s, 480p or 768p ([API guide](https://platform.minimax.io/docs/guides/video-generation)). The open-source post of 3 August 2026 lists 24 fps, native 32 kHz stereo audio, up to 9 images, 3 videos and 3 audio clips as references, and weights on Hugging Face (`MiniMaxAI/MiniMax-H3`) under the MiniMax H3 Community License ([MiniMax News](https://www.minimax.io/news/minimax-h3-open-source)). The consumer app is Hailuo AI. Read 2026-10-09.

### Runway

Runway's API lists `gen4.5` (T2V and I2V, 2 to 10 s, available since 10 February 2026), `aleph2` (Aleph 2.0, video-to-video editing, since 2 June 2026), `gen4_turbo` (I2V) and `act_two` (performance to video). `gen3a_turbo` and `gen4_aleph` were retired on 30 July 2026. Runway is also a multi-model surface: the same API lists Veo 3.1, Gemini Omni Flash, Seedance 2.x, Wan 3.0, MiniMax H3, Grok Imagine Video 1.5 and others, whose exposed controls may differ from the makers' own ([models](https://docs.dev.runwayml.com/guides/models/), [changelog](https://docs.dev.runwayml.com/api-details/api_changelog/), read 2026-10-09). Gen-4.5 audio output is not stated.

### Luma

Ray3.2, "our newest and most versatile video model": T2V and I2V in 5 or 10 s clips with up to 16 keyframes, Modify Video (restyle footage while keeping motion and timing, up to 20 s at 24 fps) and Reframe to other aspect ratios; 360p drafts to 1080p, HDR and EXR export; no native audio for T2V and I2V, while Modify Video and Reframe keep the original audio ([Luma Ray](https://lumalabs.ai/ray), no date on the page, read 2026-10-09). Earlier Ray3 and Ray3.14 remain on partner surfaces such as Adobe Firefly.

### xAI Grok Imagine

`grok-imagine-video-1.5`: T2V and I2V, up to 14 reference images, first, last and mid-video frame pinning, up to 3 voice references, up to 15 s; `grok-imagine-video` edits an existing video with a prompt; extension continues from a last frame ([xAI video generation guide](https://docs.x.ai/docs/guides/video-generations), read 2026-10-09). Generated sound is reported by secondary sources; the guide read here does not state it.

### Midjourney

Video V1, announced 18 June 2025: image to video only, from a Midjourney image or an uploaded start frame, automatic or manual motion prompts, high or low motion, four 5 s videos per job, extension by about 4 s up to four times ([announcement](https://updates.midjourney.com/introducing-our-v1-video-model/), read 2026-10-09). Audio is not mentioned. The current help page did not load.

### Lightricks LTX

Secondary sources only: LTX-2 released with open weights on 6 January 2026 (synchronized audio and video, local inference, a license free for research and for companies under USD 10 million annual revenue), LTX-2.3 on 5 March 2026 (portrait video, cleaner audio). Check the model card and license before recommending it.

### OpenAI Sora

OpenAI's deprecations page records that developers were notified on 24 March 2026 that `sora-2`, `sora-2-pro`, their dated snapshots and the Videos API would be removed from the API on 24 September 2026, with no replacement ([deprecations](https://developers.openai.com/api/docs/deprecations), read 2026-10-09). Secondary sources date the Sora app's closure to 26 April 2026. Treat a Sora request as historical: explain the retirement and offer a current target.

## Surfaces that host many models

- **Runway** exposes its own models and third-party ones through one API (see its card).
- **Adobe Firefly** offers the Firefly Video Model and partner models; Adobe's help pages list Veo 3.1 and 3.1 Fast (with audio), Runway Gen-4 and Gen-4.5, Luma Ray2 to Ray3.14, Kling 3.0 and Seedance 2.0 on some surfaces, and note that prompts and references for some partner models go to their makers (search summary of [Adobe help](https://helpx.adobe.com/firefly/web/create-mood-boards/firefly-boards/partner-models-to-generate-videos.html)).
- Aggregators such as fal, Replicate or OpenRouter host many families; an aggregator listing is not the maker's documentation.

## Watchlist and evidence gaps

- **Kling 4.0:** third-party pages report a limited preview from late September 2026 and a full release planned for October; others found no Kuaishou announcement, model card or API document. No primary source on 2026-10-09.
- **HappyHorse 1.0 and 1.1:** listed on Runway (`happyhorse_1_0`) and in Alibaba Model Studio's migration table (`happyhorse-1.1-i2v`); the developer's identity is disputed in secondary sources.
- **Tencent HunyuanVideo 1.5:** open weights (Apache 2.0) reported for November 2025, 720p, 5 to 10 s; no Tencent page was read.
- **Pika:** no primary page found; version claims conflict.
- **Adobe Firefly Video Model:** current version and limits not read on an Adobe page.
- **Moonvalley Marey** and other licensed-data models: not checked in this snapshot.

## Fresh-update checklist

1. Open the maker's model page or changelog for the exact version and surface; record the date.
2. Confirm each operation the prompt relies on (I2V, first-last, references, edit, extension, audio) on that page, not on a sibling version or a host surface.
3. Recheck limits that shape the prompt: clip length, resolution, aspect ratio, reference counts and real-face rules.
4. Note retirements: Veo 3, Runway Gen-3 and Gen-4 Aleph, and Sora are gone or going.
5. Record what was read and when in the evidence note; update this snapshot only with sourced facts and a new snapshot date.
