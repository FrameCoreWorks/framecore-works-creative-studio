# Caption readability defaults

Checked 2026-10-08. Starting values for planning and caption QA. A distributor's, client's or platform's current specification always wins; record which default or specification a caption plan uses.

## Subtitles: dialogue, translation, accessibility

Netflix's partner guides are the most detailed public subtitle specification:

| Rule | Value | Source |
| --- | --- | --- |
| Lines | At most 2; keep one line unless the text exceeds the character limit | [Netflix Timed Text Style Guide: General Requirements](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617), change log 2022-10-07 |
| Duration of one subtitle | At least 5/6 s (20 frames at 24 fps), at most 7 s | Same |
| Position and breaks | Centred, at the bottom or top; moved to avoid covering on-screen text. Break after punctuation or before a conjunction or preposition; keep article and noun, first and last name, verb and auxiliary together | Same |
| Characters per line | 42 in English and in Polish | [English (USA) guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977), change log 2025-12-19; [Polish guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/216787928), change log 2025-10-17 |
| Reading speed, adult programs | Up to 20 characters per second in English, up to 17 in Polish | Same |
| Reading speed, children's programs | Up to 17 characters per second in English, up to 13 in Polish | Same |

For another language, read that language's guide before using a number; until then its limits are Unknown.

## Captions burned into short-form video

No platform publishes a reading speed for burned-in captions. Captions that transcribe speech follow the speech: keep them within the subtitle reading speeds above as a ceiling, and split a fast passage into shorter cues rather than letting text run ahead of the voice. On-screen text with no speech to follow (supers, titles, motion captions) is read while the viewer watches the picture, so hold it longer: use Studio's [readable hold rule](../../hyperframes-workflow/references/motion-craft.md#readable-holds), the longer of 13 characters per second plus 0.5 s and 0.5 s plus a third of a second per word, at least 1 s. Keep one idea per caption and at most two lines; word-by-word highlighting may move fast only while the whole phrase stays readable. Right-to-left captions align and wrap right to left, keep Latin names and numbers isolated in their own order, use no letter spacing, and highlight by word, never by letter. The [captions tool](../assets/captions/README.md) checks both cases (profiles `social` and `text`) and subtitles (`subtitles`).

Keep captions out of the interface. Per-platform safe areas, sizes, text limits and automatic captions are in the dated [platform caption specs](platform-caption-specs.md) (checked 2026-10-25): Meta's own pages give 14 % at the top, 35 % at the bottom and 6 % at each side for every 9:16 placement, while TikTok's safe zone changes with caption length and YouTube publishes none. Always check the placement's preview before delivery. Studio's craft critique keeps text out of the top 8 % and bottom 14 % of a 9:16 frame as a readability floor for films without platform overlays; leave the platform's deeper bottom margin for anything that will be posted or run as an ad.

## Files

- **WebVTT** ([W3C WebVTT](https://www.w3.org/TR/webvtt1/), Candidate Recommendation Draft of 2026-05-20): the file starts with `WEBVTT`; timings read `00:11.000 --> 00:13.000` with a full stop before the milliseconds, hours only when needed; a blank line separates cues.
- **SRT** (a de facto format without a formal standard): numbered cues, `00:00:11,000 --> 00:00:13,000` with a comma before the milliseconds, a blank line between cues, UTF-8.

The [motion sync tool](../../hyperframes-workflow/assets/motion-sync/README.md) imports both formats into a motion contract's captions, where `check-score.mjs` checks order, overlaps and reading time. Where only Python runs, the [captions tool](../assets/captions/README.md) does the same import, converts between the formats, builds cues from timed words and burns them into a supplied video.
