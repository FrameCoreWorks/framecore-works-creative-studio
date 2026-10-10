# Channel copy and format snapshot

Snapshot date: 2026-10-10.

Character limits and sizes for common placements, read on the snapshot date. Platforms change these without notice and placements crop differently, so every row is a working default, not a guarantee. The same values drive the [copy checker](../../copy-voice/scripts/pl_copy_check.py) (`--channel`) through [channel-limits.json](../../copy-voice/assets/channel-limits.json) and the [static compositor presets](../../static-graphic-design-creator/assets/static-render/presets.json).

## How to use it

- In Quick mode, a platform or channel trigger for a placement listed here is satisfied by this snapshot while it is less than 90 days old: write to these limits and say once that they were checked on the snapshot date.
- In Deep mode, for a paid campaign at final, or when the user names a placement, a rule or an ad policy not listed here, check the platform's current page. When a check finds a different value, use it and note it in the project.
- **Hard** means the platform refuses longer text; **visible** means longer text is cut behind "more" or truncated in a placement. Write the message to the visible length and use the rest for detail.

## Copy limits

| Channel and field | Visible | Hard | Source and confidence |
| --- | --- | --- | --- |
| Google Ads responsive search ad: headline (up to 15) | 30 | 30 | Google Ads Help "About responsive search ads": confirmed. Double-width characters count twice |
| Google Ads RSA: description (up to 4) | 90 | 90 | same: confirmed |
| Google Ads RSA: display path (2 fields) | 15 | 15 | same: confirmed |
| Meta (Facebook, Instagram) ad: primary text | about 125 | long (sources differ) | third-party guides agree on about 125 before "See more"; no Meta page found on the snapshot date |
| Meta ad: headline | about 27 to 40 | not established | third-party guides differ (27 recommended for mobile, 40 in some placements) |
| Meta ad: description | about 27 to 30 | not established | third-party guides; not shown in every placement |
| LinkedIn single image ad: introductory text | about 150 | 600 | third-party guides agree; LinkedIn business page for image sizes |
| LinkedIn single image ad: headline | 70 | about 200 | third-party guides; some advise 50 to 60 |
| TikTok in-feed ad: ad text | 100 | 100 | third-party guides citing TikTok Ads Manager; emojis and hashtags count |
| TikTok in-feed ad: display name | 20 to 40 | not established | sources differ (brand 2 to 20, app 4 to 40) |
| Search result title (SEO) | about 50 to 60 (about 600 px desktop) | none | Google states no fixed length; third-party pixel estimates |
| Meta description (SEO) | about 150 to 160 desktop, about 120 mobile | none | Google states snippets have no fixed length and may not use the meta description |
| Email subject line | about 40 to 50 (30 to 40 on phones) | none | common email practice; clients differ |
| Email preheader | about 40 to 100 | none | common email practice; clients differ |
| Allegro offer title | not established | not established | the snapshot search did not confirm a maximum (community posts suggest about 50, other guides 75); check the field counter in the offer editor. Since a May change, a title needs at least 12 characters and 3 words (Allegro developer news) |

## Image and video sizes

The static compositor's [presets](../../static-graphic-design-creator/assets/static-render/presets.json) hold the sizes with the same date: feed 4:5 at 1080 × 1350, square 1080 × 1080, Stories and Reels 9:16 at 1080 × 1920, link and landscape 1.91:1 at 1200 × 628, LinkedIn square 1200 × 1200. For 9:16 placements keep text out of the top 14 %, the bottom 35 % and 6 % at each side: sources disagree on Meta's exact zones (some measure 13 % top and bottom for Stories, 23 % to 35 % bottom for Reels), so the most conservative values are used. Check the ad manager's placement preview before a paid final.

## Sources read on 2026-10-10

- Google Ads Help, About responsive search ads: <https://support.google.com/google-ads/answer/7684791>
- LinkedIn, Single image ads specifications: <https://business.linkedin.com/advertise/ads/sponsored-content/single-image-ads-specs>
- Google Search Central, Control your snippets in search results: <https://developers.google.com/search/docs/appearance/snippet>
- Allegro developer news (title minimum): <https://developer.allegro.pl/news>
- Third-party summaries used where no platform page was found: adsuploader.com (Meta aspect ratios), billo.app and adkit.so (Meta safe zones), influee.co and adligator.com (Meta copy lengths), b2linked.com and thebrief.ai (LinkedIn), tlinky.com and lettercounter.org (TikTok)
