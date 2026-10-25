# Platform caption specs (dated card)

Checked 2026-10-25 on the platforms' own pages unless a row says otherwise. Platform interfaces and ad specs change; refresh a row older than about three months, or at once when a platform announces a change. A client's, distributor's or platform's current specification always wins. Reading speeds, line lengths and file formats are in [readability defaults](readability-defaults.md).

## Safe areas for burned-in captions and on-screen text

| Placement | Keep free of text and logos | Notes | Source |
| --- | --- | --- | --- |
| Instagram Reels, Facebook Reels, Instagram and Facebook Stories, any 9:16 video in Meta feeds | Top 14 %, bottom 35 %, 6 % on each side | One safe zone for all 9:16 Meta placements. Reels ads that carry a disclaimer: keep the bottom 40 % free. On screens taller than 9:16 Meta may zoom (cropping outside the safe zone) or letterbox | [Meta Business Help, safe zones](https://www.facebook.com/business/help/980593475366490); [Instagram Reels ads guide](https://www.facebook.com/business/ads-guide/update/video/instagram-reels) |
| Instagram feed at 1:1 or 4:5 | "Keep the bottom and side edges free" | No percentages published: Unknown | [Meta Business Help, safe zones](https://www.facebook.com/business/help/980593475366490) |
| TikTok (organic and ads) | Depends on the video shape, the caption length and added formats; a longer caption makes the safe zone smaller | Pixel values exist only in TikTok's downloadable overlay files (In-Feed standard, with anchor, right-to-left), which were not read: Unknown. Check the real caption in TikTok's ads preview | [In-Feed ads specs](https://ads.tiktok.com/resources/help/article/tiktok-auction-in-feed-ads); [TopView](https://ads.tiktok.com/resources/help/article/tiktok-reservation-topview) |
| YouTube Shorts | Unknown: YouTube publishes no safe zone | Third-party figures (for example a 900 x 1160 px safe box) are not YouTube's and are not used | [Shorts definition](https://support.google.com/youtube/answer/12779649?hl=en) |

On a 1080 x 1920 frame Meta's percentages are about 269 px at the top, 672 px at the bottom and 65 px at each side, leaving a box of about 950 x 979 px from y = 269 to y = 1248 (on 1440 x 2560: about 358, 896 and 86 px). This is arithmetic on Meta's figures, not a published pixel spec.

Working rule where a platform publishes no numbers (inference, not a platform spec): use Meta's 9:16 zone as the common box for every vertical placement, keep captions centred and away from the right edge, where the action buttons sit (Meta's 6 % side margin is narrower than that column), and check the actual placement's preview before delivery. Studio's craft critique (top 8 %, bottom 14 %) is a readability floor for films without platform overlays, not a platform safe zone.

## Sizes, length and text limits

| Placement | Format | Length | Text fields | Source |
| --- | --- | --- | --- | --- |
| Instagram Reels ads | 9:16, 1440 x 2560 recommended, 4 GB | 0 s to 15 min | Primary text 44 characters recommended; video captions optional but recommended | [ads guide](https://www.facebook.com/business/ads-guide/update/video/instagram-reels) |
| Facebook Reels ads | 9:16, 1440 x 2560, 4 GB | No maximum | Primary text 40 characters | [ads guide](https://www.facebook.com/business/ads-guide/update/video/facebook-facebook-reels) |
| Instagram Stories ads | 9:16, 1440 x 2560, 4 GB | 1 s to 60 min | Primary text 125 characters | [ads guide](https://www.facebook.com/business/ads-guide/update/video/instagram-story) |
| Facebook Stories ads | 9:16, 1440 x 2560, 4 GB | 1 s to 3 min | Primary text 125, headline 40 characters | [ads guide](https://www.facebook.com/business/ads-guide/update/video/facebook-story) |
| Facebook feed video ads | 4:5, 1440 x 1800, 4 GB | 1 s to 241 min | Primary text 50 to 150, headline 27 characters | [ads guide](https://www.facebook.com/business/ads-guide/update/video/facebook-feed) |
| Instagram feed video ads | 9:16 at 1080 x 1920 recommended; a 4:5 size was not stated | 1 s to 60 min | Primary text 125 characters | [ads guide](https://www.facebook.com/business/ads-guide/update/video/instagram-feed) |
| TikTok In-Feed ads (not Spark) | 9:16 recommended, at least 540 x 960 (TikTok's creative guidance: at least 720p), 500 MB | Up to 10 min | Ad caption in a fixed white font, no links, @ or hashtags; account name 20 characters (10 in Chinese, Japanese or Korean). The preview shows a 100-character ad-text counter (the help text does not state it) | [In-Feed ads specs](https://ads.tiktok.com/resources/help/article/tiktok-auction-in-feed-ads); [creative best practices](https://ads.tiktok.com/resources/help/article/creative-best-practices?lang=en) |
| TikTok Spark Ads | The organic post | No restriction | Up to 4 lines of the organic caption, emojis included | [In-Feed ads specs](https://ads.tiktok.com/resources/help/article/tiktok-auction-in-feed-ads) |
| TikTok organic | MP4, WebM or MOV, H.264 recommended, 23 to 60 fps, 360 to 4096 px per side, 4 GB | 3 min for all creators, 5 or 10 min for some | Caption length: Unknown (secondary sources disagree) | [Content Posting API guide](https://developers.tiktok.com/doc/content-posting-api-media-transfer-guide) |
| YouTube Shorts | Square or vertical; no recommended resolution published | Up to 3 min | | [Shorts](https://support.google.com/youtube/answer/12779649?hl=en) |

Organic Reels length limits were not read (only the ad specs): Unknown.

TikTok's creative guidance suggests 5 to 10 on-screen words per second; Studio's readable hold rule is slower and wins for text the viewer must actually read.

## Platform captions next to burned-in captions

| Platform | Automatic captions | Own caption file | Source |
| --- | --- | --- | --- |
| Instagram | Speech recognition creates captions for reels and videos; a Captions sticker and a closed-caption setting exist | Not stated: Unknown | [Instagram Help](https://help.instagram.com/225479678901832/) |
| Facebook Reels | On by default; can be turned off for all reels or one reel, with a review-before-publishing option | Not stated: Unknown | [Meta Business Help](https://www.facebook.com/business/help/385195769594602) |
| TikTok organic | Generated for uploads; the creator sets the language and can edit or remove them; creator captions are styled in the editor | Not mentioned: Unknown | [TikTok accessibility](https://support.tiktok.com/en/using-tiktok/creating-videos/accessibility) |
| TikTok Spark Ads | Auto-captions with translation for viewers (US and EU feeds); burned-in text is not translated; an auto-caption identical to burned-in text is filtered out; opting out needs a request | | [Spark Ads captions](https://ads.tiktok.com/resources/help/article/about-captions-and-translations-for-spark-ads?lang=en) |
| YouTube (long-form and Shorts) | Speech recognition creates captions | SRT, SBV/SUB, VTT and other formats are supported; the page does not mention Shorts specifically | [automatic captions](https://support.google.com/youtube/answer/6373554?hl=en); [file formats](https://support.google.com/youtube/answer/2734698?hl=en) |

When captions are burned in, tell the user to turn off the platform's automatic captions for that post (where the platform allows it), or the viewer may see the same words twice. For translation to other languages on TikTok, a sidecar or the platform's own captions reach viewers that burned-in text cannot.

## Handoff

Record in the caption plan which placement row it follows, its check date, the safe box in pixels for the delivered frame size and any Unknown that the user must check in the platform's preview.
