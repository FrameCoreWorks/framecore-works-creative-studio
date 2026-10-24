# Motion graphics compendium

The map of what Studio knows about motion graphics and where each part lives, plus the knowledge the other references do not hold: ad creative, the tool landscape and its licences, lyric timing, hybrid films with generated media, techniques and transitions by name, the working sequence and the fixes for common failures. Researched 2026-10-12; sources at the end. Facts that change (platform rules, licences, versions) carry their date: check them again before a client depends on them.

## 1. Where the knowledge lives

| Need | Read |
| --- | --- |
| Principles, easing presets, durations in frames, holds, rhythm, transition grammar, type and layout rules, defects | [motion craft](motion-craft.md) |
| References, style frames, a focused motion proof | [motion quality direction](motion-quality-direction.md) |
| Does the idea develop (idea, composition, rhythm, cause, signature, ending) | [development review](motion-development-review.md) |
| Ads: argument, offer, hook, proof, CTA | [commercial motion](commercial-motion.md) |
| Boards, ad structures, formats, lyric video, hybrid films, still frames | [reel board system](reel-board-system.md) |
| Building in Claude Code with HyperFrames | [client reels in Claude Code](claude-code-reels.md) |
| Sound design and mixing | [motion sound design](motion-sound-design.md) |
| Product interface films | [product films](product-films.md) |
| The idea before the look | [ideation method](../../pipeline-core/references/ideation-method.md) |
| A technique by name (637 techniques: what it does, when, pairings, registry candidates) | [technique atlas](../assets/technique-atlas/README.md), `atlas.py "<name>"` |
| HyperFrames craft: 47 motion rules, 22 scene blueprints, 13 transition families, text effects, runtime adapters | HyperFrames skill `hyperframes-animation` (installed with HyperFrames) |
| Remotion craft (when the user chose React) | Remotion's own agent skills, `npx skills add remotion-dev/skills` (`remotion-best-practices`, `remotion-markup`, `remotion-captions`, `remotion-render` and others) |

## 2. Ad creative that works on Meta and short-form platforms

- **Open with the message.** Meta advises capturing attention and including key messaging or branding within the first 3 seconds. Put the strongest statement, the product or the brand on the first board; a slow build loses most viewers.
- **Work without sound.** Many viewers watch muted; every claim is on screen, and sound makes it better, not possible. Reels ads play with sound by default, so the mix still matters.
- **Vertical first.** 9:16 for Reels and Stories, 4:5 for the feed (Meta's tailored campaign guidance). Build 9:16, then adapt.
- **Keep the interface clear.** For Reels ads the widely cited margins are about 14 % top, 35 % bottom and 6 % each side (269, 672 and 65 px at 1080 x 1920). Several guides repeat them; Meta's own help pages, as checked, give no general figure, so treat them as a conservative default, use the Ads Manager safe-zone overlay when the client sets up the ad, and leave the call to action to Meta's CTA button rather than burning a button where the platform draws its own.
- **Length.** Industry guides (not Meta) put conversion-focused Reels ads at about 15 to 30 seconds and reach-focused cuts at 7 to 15. Use them as a starting range; the brief decides.
- **Show the real thing.** Products, faces, real work and real numbers beat abstract decoration; Meta's guidance also favours showing people using the product.
- **Hooks worth testing** (first board only, same body): a number, a direct question to the viewer, a before-and-after flash, the product doing the surprising thing, a contradiction ("Nie musisz..."), the outcome first. Deliver two or three hook variants of one reel when the client tests ads.
- **One offer, one action.** The end card says what to do and how (phone, address, link, button text that matches the ad's CTA).

## 3. Tools and licences (checked 2026-10-12)

| Tool | What it is good for | Licence and cost |
| --- | --- | --- |
| HyperFrames | HTML compositions rendered in headless Chrome; agent skills, about 400 registry blocks, video and audio layers; Studio's default in Claude Code | Apache-2.0, free |
| GSAP | The timeline engine most HTML motion uses, including SplitText and MorphSVG | Free for commercial use since Webflow's 2025 change, plugins included; the standard licence excludes building no-code visual animation tools that compete with Webflow. Check gsap.com before shipping a product built on it |
| Remotion | React compositions, data-driven variants, server rendering | Source-available, not open source: free for individuals and companies of up to 3 people; companies of 4 or more need a company licence (remotion.dev/license) |
| Motion Canvas | Procedural, code-first animation on one canvas, with an editor synced to audio; strong for explainers and diagrams | MIT |
| Revideo | A Motion Canvas fork with a rendering API and templates for automated pipelines | MIT |
| Lottie | Vector animation exported from After Effects (Bodymovin), small files, plays in apps and HTML | Open format; player licences vary by library |
| Rive | Interactive, state-machine animation for apps and the web | Editor is a paid product with a free tier; runtimes are open source |
| Manim | Mathematical and diagram animation in Python | MIT (community edition) |
| awesome-ai-motion | A named vocabulary of 637 motion techniques with cards and 128 rendered clips (HTML with GSAP); Studio projects its English card text into the technique atlas, pinned at `1e3c249` | MIT for the author's cards; bundled GSAP and fonts keep their own licences; cards cite third-party concept sources; two commits when pinned, so check activity before moving the pin |
| Theatre.js | A keyframe editor and sequencer for web animation | Open source; check the package licence per module |

Choose by the deliverable and the host, not by habit: a client reel in Claude Code goes to HyperFrames; a React codebase or batch personalisation goes to Remotion; a host without a shell gets the contract and the motion player.

## 4. Lyric timing that holds

- **Rights first.** The user supplies the track and the lyrics and confirms they may use them.
- **Align known words rather than transcribe them.** When the words are known, align them instead of recognising them (a recogniser can change or drop words; the supplied text stays the spelling): WhisperX aligns words with a phoneme model; `syncalong` maps Whisper word times onto the supplied lyrics and writes LRC; `lyric-align` anchors lyric lines onto recognised words and writes LRC, SRT, ASS or JSON, with an option to separate the vocals first. Music blurs word boundaries, so on a dense mix compare the full master and a vocal stem on a short excerpt (a stem can also smear consonants), keep the better one and correct by ear; check the separation model's licence first (Demucs pretrained weights are for research use only, and allin1's default pipeline runs Demucs).
- **Line, then word.** Board changes follow line starts; word emphasis follows the word times; accents land on the beat grid. Studio's [lyric timing](../assets/motion-sync/README.md#lyric-timing) does the alignment, the beat grid and half-beat snapping in one run. In a reference lyric reel the cuts followed the sung words (56 % within two frames of a half-beat, 22 % of a beat), not the bar.
- **Choruses.** A repeated chorus repeats its visual motif and escalates it (scale, colour, a new layer), so the viewer recognises it and still sees something new.
- **Reading time wins** over sync: a line that cannot be read before the next one arrives is split or held.

## 5. Hybrid films: generated images and clips with motion graphics

- **Choose the generator per shot.** Models differ in motion realism, prompt adherence, identity across shots and native audio, and they change quickly; Video Prompt's dated maps hold the current comparison.
- **Continuity.** Define start and end frames for each clip, reuse reference stills for characters and style, and generate a little longer than the board needs, so the cut can sit on the beat.
- **Repeatability over hero shots.** Generate a few takes per shot and keep the one that matches its neighbours, not the single most impressive one.
- **One look.** Match colour across generators before the final grade, then unify with one grain or texture; HyperFrames' `grade-compare` shows candidates side by side.
- **Exact layers on top.** Names, prices, logos and claims are typed in the composition. Generated hands, faces and text artefacts are covered by a board element, cut around or regenerated, never captioned over in hope.
- **Sound.** Replace or mix down generated audio deliberately; designed sound and the music bed carry the reel.
- **Provenance.** Record the generator, the prompt pack version and the user's rights for every plate.

## 6. Techniques and transitions by name

HyperFrames names its craft, which lets a board plan say exactly what to build.

- **Motion rules** in `hyperframes-animation` include kinetic beat slams, spring pop entrances, scale swaps, counting with dynamic scale, gradient text sweeps, chromatic glitches, motion-blur streaks, depth-of-field blur, SVG path draws, particle bursts, multi-phase camera moves, cursor choreography and 3D text depth. Pick two to four per film and compose them; a film that uses every effect has no signature.
- **Scene blueprints** cover recurring structures: kinetic type on beats, title card reveal, typewriter reveal, logo assemble and lockup, comparison split, data count-up, device showcase, cursor UI demo, CTA morph and press, ticker takeover, camera journey and others.
- **Transition families**: push, cover, grid, light, radial, scale, blur, dissolve, distortion, destruction, mechanical, 3D and others, each with variants in the registry. Use the [transition grammar](motion-craft.md#transition-grammar) to choose: a transition must say something (continuity, energy, reveal, depth) or be a plain cut on the beat.
- **Names outside HyperFrames.** For a technique a client names that the registry does not have, `python3 assets/technique-atlas/atlas.py "<name>"` gives what it does, when it fits, its pairings and a card with a preview clip; order: registry block, then the atlas as vocabulary and preview, then your own implementation.
- **Text effects** (`animate-text` adapter): per-word and per-character entrances, decoding, typing, weight and variable-axis shifts, highlights and strike-throughs.

## 7. The working sequence

1. Brief, offer, exact copy, format, length, the idea (Studio).
2. Style frames: two or three key boards as stills; approve the look.
3. Animatic: the board plan with timings on the music or voice, boards as stills cut on the beat; approve the rhythm.
4. Build the boards; search the registry before hand-building.
5. Snapshot every board; fix type, contrast, glyphs and safe areas on stills.
6. Draft render, motion activity, development review, listen.
7. Client round on the draft: collect changes as a list against board numbers and times; apply them in one revision.
8. Delivery renders per format, cover frame, hook variants if asked, project folder and review record.

## 8. Failures and their fixes

| Symptom | Fix |
| --- | --- |
| Nothing moves for seconds (motion activity REVISE) | Add a change that belongs to the idea: the next board, a camera move, a reveal; or declare the hold if the idea needs it |
| Everything moves at once | One hero move per board; stagger the rest by 2 to 4 frames; let the eye land |
| Motion feels floaty or cheap | Ease out on entrances, ease in on exits; keep linear moves for motion that is mechanical or constant by design (drifts, conveyors, clocks); add overshoot only to small elements |
| Text unreadable on a phone | Fewer words per board, bigger type, more contrast, longer hold; check the snapshot at thumbnail size |
| It looks like a template | Go back to the idea; change the structure, not the colours |
| Generated media looks mismatched | Grade-match, unify grain, give every plate the same camera language |
| Garbled text in generated frames | Type it in the composition; never ask a generator for exact text |
| Jitter or shimmer | Animate transforms and opacity only; precompute layout; snap static text to whole pixels |
| Sound out of step | Time by frames, not wall clock; cut and accent on the beat grid; check the render, not the preview |
| Polish letters missing or wrong | A font with full Latin Extended-A; check ą ć ę ł ń ó ś ź ż on a snapshot before rendering |

## Sources

Checked 2026-10-12. Platform pages change; recheck before relying on a number.

- Meta for Business, tailored campaigns (first 3 seconds; 4:5 feed, 9:16 Stories and Reels): https://www.facebook.com/business/ads/automation/tailored-campaigns
- Meta for Business, Reels ads: https://www.facebook.com/business/ads/facebook-instagram-reels-ads
- Reels safe-zone margins as repeated by industry guides (not confirmed on Meta's own pages): https://billo.app/blog/meta-ads-safe-zones, https://adkit.so/tools/safe-zones/meta
- Reels ad length ranges (industry guide): https://cropink.com/reels-ads
- Remotion licence and FAQ: https://www.remotion.dev/license, https://www.remotion.dev/docs/license/faq
- Remotion agent skills: https://github.com/remotion-dev/skills
- GSAP free with plugins: https://webflow.com/blog/gsap-becomes-free; standard licence: https://gsap.com/community/standard-license/
- Remotion and Motion Canvas compared (by Remotion): https://www.remotion.dev/docs/compare/motion-canvas
- Motion Canvas, Revideo and alternatives (vendor guides): https://www.pkgpulse.com/guides/remotion-vs-motion-canvas-vs-revideo-programmatic-video-2026, https://www.wireflow.ai/blog/best-remotion-alternatives-in-2026
- Lyric alignment: https://syncalong.readthedocs.io/, https://pypi.org/project/lyric-align/, WhisperX overview https://intelligent-earth.ox.ac.uk/node/3991471
- Generated video across models (vendor comparisons): https://magichour.ai/blog/ai-video-model-benchmark
- HyperFrames skills at commit `86521b9`: https://github.com/heygen-com/hyperframes
