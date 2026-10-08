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

No platform publishes a reading speed for burned-in captions. Viewers read while they watch the picture, so start slower than subtitle limits: use Studio's [readable hold rule](../../hyperframes-workflow/references/motion-craft.md#readable-holds), the longer of 13 characters per second plus 0.5 s and 0.5 s plus a third of a second per word, at least 1 s. Keep one idea per caption and at most two lines; word-by-word highlighting may move fast only while the whole phrase stays readable.

Keep captions out of the interface. Check the platform's current overlay or preview before delivery: Meta's ad tools draw the safe areas on the artwork, and TikTok publishes overlay files per placement, whose safe area changes with caption length and ad format. Widely used working margins for 9:16 Reels ads are 14% at the top, 35% at the bottom and 6% at each side; they come from secondary sources and were not confirmed on a Meta page on 2026-10-08. Published TikTok bottom margins range from about 240 to over 700 px on 1080 x 1920, so no single number is reliable. Studio's craft critique keeps text out of the top 8% and bottom 14% of a 9:16 frame; leave the deeper bottom margin for ads with a call-to-action button.

## Files

- **WebVTT** ([W3C WebVTT](https://www.w3.org/TR/webvtt1/), Candidate Recommendation Draft of 2026-05-20): the file starts with `WEBVTT`; timings read `00:11.000 --> 00:13.000` with a full stop before the milliseconds, hours only when needed; a blank line separates cues.
- **SRT** (a de facto format without a formal standard): numbered cues, `00:00:11,000 --> 00:00:13,000` with a comma before the milliseconds, a blank line between cues, UTF-8.

The [motion sync tool](../../hyperframes-workflow/assets/motion-sync/README.md) imports both formats into a motion contract's captions, where `check-score.mjs` checks order, overlaps and reading time.
