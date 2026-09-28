# Music provider routing and rights

**Evidence snapshot: 2026-09-28.** TikTok Help was updated July 2026; check a newer source on each use. Provider names, interfaces, models, available controls and plan terms change. Re-open current owner documentation for the exact account surface and operation whenever producing a live recommendation. These are adapters to research and prompt architecture; Creative Studio contains no connector or credentials for the services.

## Route the user means

| User label | Current route to recognize | What to verify now |
|---|---|---|
| Suno | Suno music generation | Current model/UI or API, section and lyric controls, audio input, output length, plan tied to generation date, and rights statement |
| ElevenLabs music / Eleven Music | Eleven Music website or Music API | Current model/version and surface, prompt vs composition plan, available section timing/editing, subscription conditions and exact Music Terms |
| Google Flow Music, formerly ProducerAI | Google Flow Music | Current product name, prompt workflow, model and feature controls; account-specific plan and current Terms of Service |

A name identifies the requested provider family, not the connector, user login or enabled model. If a service is unavailable, deliver a correctly bounded prompt/plan for it; do not switch providers. If an old label is ambiguous, map it once in plain language and continue under the current documented label.

## Build an original provider-native prompt

Keep the user's concept and cut map as authorities. Describe the emotional job and tempo/feel, then the arrangement over time, instrumentation/timbre, vocal status and delivery, intentional spaces, scene/cut accents, mix hierarchy and exclusions. For a short social film, supply time-aligned anchors only if you have an actual timebase or clearly label them as targets. Preserve exact approved lyrics; do not create lyrics merely because a provider can. Do not instruct a model to imitate a living artist or recreate a copyrighted track. Translate the desired musical attributes into an original brief.

The prompt should be provider-native only after fresh research. For example, current ElevenLabs docs describe text prompting for rapid prototyping and ordered composition-plan chunks for precise section structure; current best-practice docs discuss concise evocative prompts and arrangement language with explicit entrances/exits. Do not turn this API-specific structure into a generic JSON request or assume a UI exposes every API control. Current Suno documentation distinguishes text/lyrics workflows and its own music usage terms. Google Flow Music's current product and help pages are the authority for its own workflow.

## Commercial-use checks

Treat these as distinct questions:

1. Which exact track or output is being used? Record title/ID, creator/provider, source page, version and date retrieved.
2. What is the actual use? Organic post, paid ad, branded content, client/agency delivery, event playback, resale, derivative/remix, cross-platform distribution?
3. What does the specific license cover? Platform, region, account/plan at creation or download, duration/term, editing, attribution, client transfer, and required proof.
4. Which parts remain conditional or unknown? State the gap and avoid the word “cleared” until the exact use is supported.

Snapshot notes from official documentation opened 2026-09-28:

- Suno says its free-plan songs are for personal/non-commercial use and are not automatically granted retroactive commercial-use rights when upgrading. It says songs made/downloaded while subscribed to a paid plan receive commercial-use rights; that does not itself guarantee copyright protection. Confirm the exact track's creation/download date, relevant terms and jurisdiction. Sources: [free-plan rights](https://help.suno.com/en/articles/9601601), [retroactive rights](https://help.suno.com/en/articles/2425729), [paid-plan rights](https://help.suno.com/en/articles/9601665), [copyright explanation](https://help.suno.com/en/articles/9602305).
- ElevenLabs describes Eleven Music as cleared for broad/nearly all commercial uses subject to particular subscriptions and conditions; its Music Marketplace separately issues a license based on a selected usage type. The Marketplace distinguishes a social-media license from a paid-marketing license, so do not transfer either to a different product, plan or asset without checking the applicable terms. Sources: [Eleven Music](https://elevenlabs.io/docs/overview/capabilities/music), [Music Terms entry point](https://elevenlabs.io/docs/eleven-creative/products/music), [Marketplace license types](https://elevenlabs.io/docs/help-center/product/monetization-business/music-marketplace/what-usage-types-exist-in-music-marketplace).
- TikTok's Commercial Music Library is a platform-specific commercial music route. Its help page, last updated July 2026, states that selected CML tracks can be used for organic or paid TikTok content and instructs users to select campaign region and usable placement. Confirm the exact selected track, region, current CML status and intended TikTok placement; do not treat that catalogue entry as a cross-platform licence. Sources: [TikTok CML](https://ads.tiktok.com/help/article/commercial-music-library?lang=en), [commercial use guidance](https://ads.tiktok.com/business/en/blog/audio-library-royalty-free-music).
- Meta's music library availability and usage differ by account/post. In this research pass, its official Ads guide and Instagram Sound Collection help page redirected to a login wall, so specific product rights remain unverified here. Re-open current account/territory-specific guidance and check the exact track before making a rights recommendation. Sources: [Meta Reels ad guide](https://www.facebook.com/business/ads/facebook-instagram-reels-ads), [Instagram Sound Collection help](https://www.facebook.com/help/instagram/402084904469945).
- Google Help maps Google Flow Music plan features and directs users to its Terms; a plan-level feature such as “commercial use rights” is not an asset-level review. The current interface and product label may differ from older ProducerAI material. Verify the active plan, exact output, usage and current terms. Sources: [Flow Music help](https://support.google.com/flow/answer/17083868?hl=en), [Google Flow/AI product terms entry](https://support.google.com/flow/answer/16353333?hl=en).

When a specific license source is inaccessible, say unverified, search the official provider help/terms once, or ask for the relevant license screenshot/document. Never infer rights from “royalty-free,” a social app music sticker, a subscription alone, a search listing, an audio file, or an AI watermark. Do not make a legal conclusion.
