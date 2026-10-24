# Reel board system

How Studio plans a commercial reel, a lyric video or a hybrid film as a sequence of boards, and which structures fit which ad job. The structures carry an idea; they never replace it: the idea comes first from the [ideation method](../../pipeline-core/references/ideation-method.md), then the structure that fits it. Block and example names refer to the HyperFrames registry at commit `86521b9` (0.8.149); search with `npx hyperframes catalog <words>`, because the registry changes.

## 1. Boards

A board (plansza) is one screen with one statement: a line of copy, a number, a product, a proof, a question. A reel is a sequence of boards on one beat grid.

- **One statement per board**, readable in the time it is on screen: about 0.3 s per word plus 0.5 s, never under 0.8 s for a single word.
- **Every board changes something** the viewer notices: the background field, the scale, the object, the camera, the type treatment. Two consecutive boards of the same kind need a different scale or position. Inside a board something keeps changing too (a reveal, a camera move, an object entering); a board that settles in its first second and then waits reads as a slide.
- **A persistent frame** ties the boards together: a HUD or viewfinder frame (corner marks, a timecode, a format label: `camcorder-hud`, `telemetry-hud`), a logo corner, one caption style, one accent colour. Boards vary; the frame does not.
- **Type**: one display family, condensed or heavy for statements, a quiet text face for small labels; one accent colour for the word that carries the meaning (`inline-highlight`, `marker-highlight`, `caption-editorial-emphasis`).
- **Pictures carry a service ad.** A local service, a product or a before-and-after needs real pictures: the client's photos or footage, or generated stills and clips ([generated assets](generated-motion-assets.md)). Type, paper and drawn icons alone make a quiet reel; never draw a realistic object in code. Without pictures, say so before building and offer the type-only reel as a weaker fallback.
- **Objects instead of decoration**: each board may hold one object drawn for the idea (a record, a phone, a curve, a ticket). UI is recreated as clean HTML (`chat-message`, `chat-thread`, `native-notification-pop`, `notification-stack`, `device-frame-stage`) when the client has no screenshots; the client's real screens win when they exist.
- **Real photos** carry type over a calm area; the photo moves (`push-in`, `parallax-zoom`, Ken Burns through `hyperframes-keyframes`), the type lands on the beat.
- **The end card** says the action in words and shows how: phone, address, button, store badge (`cta-close`, `cta-lockup`, `store-badge-lockup`, `logo-brand-close`), held long enough to read twice. After the reveal the card is clean: whatever covered or framed the reveal clears together within one beat, and no decoration stays on the card unless the user asks for it. An addition Studio proposes (a tagline, a badge) stays off until the user clearly accepts it; on an unclear answer, ask once.

## 2. Motion that keeps going

Measured on five commercial reels the owner supplied as references (30 to 47 s), the picture stood still for 14 to 38 % of the time and the longest still stretch was 0.7 to 3.8 s. The 6-second film reviewed on 2026-10-11 stood still for 83 % of its time, with one still of 4.7 s, although its frame check scored 90/100. [Motion activity](../assets/motion-quality/README.md#motion-activity) fails a render above 40 % undeclared still time or with an undeclared still longer than 2.5 s; declare real holds (the end card, a pause the idea needs) with `--hold`. Fix a failure by adding a change that belongs to the idea (a new board, a camera move, a reveal), not ambient particles.

## 3. Ad structures

Lengths are starting points; the brief and the placement decide. Each row names the boards in order and the blocks that usually build them. The local-service row has a tested [starter composition](../assets/reel-starters/README.md) with slots for copy and photos.

| Job | Boards | Length | Blocks to search first |
| --- | --- | --- | --- |
| Local service (studio, salon, workshop, clinic) | hook claim, three work photos with one-word labels, proof (award, number, review), the person behind it, booking end card with phone and address | 20 to 35 s | `headline-slam`, `push-in`, `testimonial-card`, `star-rating-fill`, `cta-lockup` |
| App or digital product | everyday moment (a notification), the problem in one line, the flow on three recreated screens, the number it pays back, button end card | 20 to 35 s | `native-notification-pop`, `chat-message`, `device-frame-stage`, `count-up`, `cta-close`, example `app-showcase` |
| Offer or sale | the price or discount slammed in, three reasons, the deadline, end card | 10 to 20 s | `number-pop-in`, `stagger-cascade`, `split-flap-board`, `cta-close` |
| Before and after | the before, the switch, the after, how to get it | 10 to 20 s | `before-after-wipe`, `comparison-split` |
| How it works | promise, three steps, result, action | 15 to 30 s | `onboarding-stepper-flow`, `marker-checklist-card`, `cta-lockup` |
| Social proof | the quote, who said it, the number behind it, action | 10 to 25 s | `testimonial-proof-card`, `social-proof-card`, `trust-strip` |
| Event or opening | date, place, what happens there, how to come | 10 to 20 s | `kinetic-center-build`, `split-flap-board`, `cta-lockup` |
| Recruitment | the role, three reasons to join, how to apply | 15 to 25 s | `headline-slam`, `stagger-cascade`, `cta-close` |
| Service launch (B2B) | input goes in, result comes out, how it works, where it runs, demo end card | 25 to 40 s | `typed-prompt`, `screen-flow-carousel`, `mk-progress-stat`, `cta-lockup` |
| Voice-over explainer | screen recording or recreated UI under word-by-word captions, real footage at the payoff | 30 to 60 s | `caption-pill-karaoke`, `caption-highlight`, skill `embedded-captions` |
| Brand showreel, dense kinetic (agency, classes, services) | chat or notification hook, the brand's carrier launched by an action, three to five verb or offer boards in kinetic type with the object doing the job, a summary in the brand's lettering, payoff in the same chat, logo assembled from its parts | 15 to 18 s | `chat-message`, `ai-chat-reveal`, `halftone-field`, `cta-lockup`; method in [dense kinetic reels](dense-kinetic-reels.md) |
| Lyric video | one line per board, cut on the beat, see section 5 | the song or a cut of it | skill `music-to-video`, `caption-kinetic-slam`, `beat-accent` |
| Hybrid AI footage | generated plates under exact type, see section 6 | 15 to 30 s | `push-in`, `grain-overlay`, `lt-*` lower thirds |

## 4. Formats and safe boxes

- Vertical 9:16 at 1080 x 1920 for Reels, Stories and TikTok; 4:5 at 1080 x 1350 for the feed; 1:1 at 1080 x 1080 when asked. Build vertical first and adapt; do not crop a wide film.
- Keep everything visible inside the action-safe box (90 % of the frame, 5 % inset) and captions and key content inside the title-safe box (80 %, 10 % inset), as `hyperframes-studio` defines them. Platform interface overlays move with app versions: take Meta's or TikTok's current placement guide when the client needs exact margins, and record its date.
- Design for sound off: every claim is on screen; sound adds, never carries alone.
- The first board reads in under a second and the cover frame is a board whose text reads at thumbnail size.

## 5. Lyric video

- **Rights.** The user supplies a track and lyrics they may use; Studio does not fetch lyrics.
- **Timing.** Use the user's LRC or SRT, or run [lyric timing](../assets/motion-sync/README.md#lyric-timing) on the track and the supplied lyrics: word and line times, the beat grid and board cuts snapped to half-beats when close. Text arrives with the voice; beats drive the accents.
- **Boards.** One line per board, two short lines at most. Vary the board kind on every line (colour field, pattern, object, photo, negative space) while the frame, type family and accent stay constant. The emphasis word of each line takes the accent colour or scale.
- **Cuts.** Board changes land on beats or on the first syllable; holds follow sustained notes. Fast sections cut by word (`per-word-rise`, `caption-kinetic-slam`), slow ones by line.
- **Build.** Skill `music-to-video` analyses the track once, lays out the frames and builds each one; Studio supplies the boards, the locked words and the review.

## 6. Hybrid: generated images and clips with motion graphics

- **Exact layers.** Logos, names, prices and claims are typed in the composition, never generated inside an image or clip ([exact layers in video](../../video-prompt-architect/references/exact-layers-in-video.md)).
- **Generated stills** become plates: a camera move (`push-in`, `parallax-zoom`, a Ken Burns through `hyperframes-keyframes`), a mask reveal, type on the calm area.
- **Generated clips** play as video layers in the composition; plan each clip's length on the beat grid and its handover to the next board ([joining generated clips](../../video-prompt-architect/references/blocking-continuity-and-extension-workbook.md#7-joining-generated-clips)). Prompts come from Video Prompt.
- **One look.** A shared grade or grain (`grain-overlay`, `npx hyperframes grade-compare`) makes plates from different generators sit together.
- **Provenance.** Record which generator made each plate and the rights the user holds.

## 7. Transitions

Pick one or two families per reel and use them for a reason: a match or shape cut (`match-cut`, `text-match-cut`, `type-match-cut`) joins two boards that share a form; a whip or push (`whip-pan-cut`, `transitions-push`) adds energy between beats; a wipe or iris (`directional-wipe`, `iris-reveal`, `curtain-reveal`) reveals something new; a zoom-through (`zoom-through-transition`) moves deeper into the same idea. `hyperframes-animation` holds the transition blueprints. A cut on the beat is often the strongest transition. The best transition comes out of the action that just happened: the bored hole the camera flies through, the hammer hit that floods the frame, the cut-through whose off-cut falls into the wipe ([scene logic check](dense-kinetic-reels.md#scene-logic-check-run-it-on-the-storyboard-and-again-on-the-frames)).

## 8. Still frames

- **Style frames** before animating: snapshot two or three key boards and get the look approved on stills.
- **Cover frame** for the post: a board snapshot that reads at thumbnail size.
- **Static ads** from the same reel: snapshot the strongest boards at 4:5 and 1:1 for a static set; check exact copy on each PNG.
