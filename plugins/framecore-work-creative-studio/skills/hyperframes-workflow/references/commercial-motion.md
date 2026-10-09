# Commercial motion: argument, picture and acceptance

Use this for an advert, promo or launch film made from code, especially one built from a website or product page. It turns a brief into one argument the viewer can follow, proves the picture on a few real frames before the film grows, and accepts the result in four separate verdicts. It came from a 2026-10-09 review of a 20-second 9:16 shop reel: a generic hook, catalogue cards, four identical wipes, photos showing white rectangles, a few pixels of drift standing in for pacing, and a decorative word cut off for whole scenes. That reel was accepted on a contract-only score of 100 while its frames were never inspected.

## 1. Decide the argument before the look

Derive these from the brief, the site and the assets actually available, and write them into the contract's `strategy` ([fields](motion-contract-json.md)):

| Field | Question |
| --- | --- |
| `audience` | Who stops scrolling for this, in what situation |
| `action` | The one thing the viewer should do next |
| `benefit` | What they get that a generic store would not give them |
| `friction` | What stops them today (not knowing where to start, buying blind, price doubt) |
| `evidence` | What can be shown, not just said: a search field, a product, a result, a comparison, a review |
| `mechanism` | How the film proves the benefit, in one sentence |
| `claims` | Every price, size, saving, availability or equivalence used, with `status` and, when verified, `source` and `checked` date |
| `alternatives` | At least two genuinely different concepts with a reason each; exactly one `chosen` |
| `hook` / `cta` | The hook's copy ID and the scene that pays it off; the CTA's copy ID and the action it `closes` |

- **Open brief:** weigh a few different concepts yourself and pick the strongest; do not hand the user a compulsory menu. Record the losers and why. A category list ("for her, for him, unisex") is a catalogue, not a concept.
- **Hook with a payoff:** the first line raises a specific question or situation the film answers later. "One scent?" fits any store; "Love a scent? Find its equivalent" sets up the search the film then shows.
- **Every scene argues:** each scene's `argues` names the step it adds (situation, action, result, proof, action again). A scene that only re-arranges the same products adds nothing.
- **The CTA closes what was shown:** ask for the action the film demonstrated ("find your equivalent"), not a new generic one ("buy now").
- **Claims:** check prices, capacities, availability, promotions and comparisons on the source page through [Research Evidence](../../research-evidence/SKILL.md) on the day, and record the source. Anything not verified stays Unknown and never appears in the copy (`check-score.mjs` fails it). If the strongest idea depends on an unverifiable claim, choose another idea the evidence supports; do not soften the claim into vagueness.

## 2. Prove the picture on real frames first

Before building the whole film, render the opening frame, the densest readable moment and the ending with the exact copy and the real assets, and look at them at full size and at phone scale (`critique.py` saves them in `keyframes/`, both sizes). Fix the composition there, where it is cheap.

- **A carrier connects states.** Where scenes belong together, let one element carry the change: the product grows out of a search result, the search field becomes the end card, a selection mark moves from option to option. Choose each transition for what it connects; a repeated full-screen wipe is a slide deck (the critique flags three or more). A real break may still be a cut or a wipe.
- **Do not force effects.** Morphs, 3D, particles, continuous motion or a single shot are tools, not quality; use one only when the brief and the assets support it.
- **Photographs belong to the frame.** Put a photo with a white background on the same white, or use an isolated (transparent) version prepared through an authorised route. Record each asset's `background` so the critique can flag a mismatch, then inspect the encoded pixels: a `mix-blend-mode` line in the code does not prove the rectangle is gone.
- **Design for the format.** In 9:16, give the product real scale, keep type large enough at phone scale, and use the full height on purpose; empty space should direct attention, not be left over. A 16:9 film is not a vertical adaptation; recompose, never crop.
- **Pacing comes from information.** Hold as long as reading or looking needs, then reveal something new. A few pixels of drift keep pixels moving but give the viewer nothing; the critique measures still stretches four times a second and counts drift as still.
- **Runtime and specifications.** Keep the user's runtime and delivery choices; otherwise use the simplest available runtime that serves the brief: the bundled renderer, the GSAP or Remotion starters, or [HyperFrames](hyperframes-engine.md) where it is installed. Higher FPS, resolution or more effects are not quality.

## 3. Accept in four separate verdicts

`acceptance.py` ([motion review tools](../assets/motion-review/README.md)) writes them from the evidence that exists; each is pass, fail or not_verified:

| Verdict | Passes only when |
| --- | --- |
| A. Technical | The encoded file has the contract's size, frame rate, frame count and expected audio |
| B. Fidelity | All copy reaches the picture verbatim, no unverified claim is used, every asset has an authority, and a person compared product and source with the frames |
| C. Composition | The text audit or frame review covered the readable holds with no error, and a person judged the opening, densest and ending frames at full size and phone scale; a contract-only critique leaves it not_verified whatever the score |
| D. Temporal | Pacing was sampled from frames and a person watched the encoded file at normal speed and judged continuity, hook-to-payoff and CTA |

A technical pass never passes B, C or D. A high critique score never overrides a material defect: a cut word in a hold blocks delivery.

**Every visible text, not only the copy.** The [text audit](../assets/motion-review/README.md#visible-text-audit) measures each word's glyphs after fonts load, through transforms, against the frame and every clipping ancestor, including decorative words, Polish diacritics and long phrases. A container that fits proves nothing about its text. During a transition a word may be cut on purpose; in a readable hold an incomplete word fails unless the element carries `data-text-clip-ok` with a reason (at least 12 characters), which records a narrow exception for pixel review. Flags such as `data-layout-ignore` never exempt visible text.

**Coverage.** Inspect the encoded first and last frames, every readable hold, the densest scene and both sides of every transition, at full size and phone scale; watch at normal speed when the host can play video, otherwise mark the viewing not_verified. Record the artifact revision, what was inspected, the findings and the stop decision in the [QA record](../templates/motion-qa-record.md). An unobserved modality never receives PASS.

## The reviewed reel, failure by failure

| Failure | Correction | Caught by |
| --- | --- | --- |
| Generic hook "JEDEN ZAPACH?" | Hook with a named payoff scene; alternatives recorded | `check-score.mjs` (`strategy.hook`, `alternatives`) |
| Catalogue cards instead of an argument | Every scene `argues`; CTA closes the demonstrated action | `check-score.mjs` |
| Four identical wipes | Carrier transitions; wipe only for a real break | critique `transitions` |
| White photo rectangles on cream | Matched background or isolated asset; pixel check | critique `integration`; key frames |
| Weak use of the vertical frame | Key-frame proof at full size and phone scale | critique key frames, `composition` |
| Drift presented as pacing | Hold for reading, then new information | critique `pace` (drift counted as still) |
| "TWÓJ WYBÓR" cut for whole scenes, marked `data-layout-ignore` | All visible text audited; flag not honoured | text audit `text-cut`, `ignore-flag` |
| Contract-only score 100 taken as a pass | Four verdicts; contract-only leaves C not_verified | `acceptance.py` |

Fixing one text defect does not make the reel a good advert; the argument and the picture still have to be rebuilt.
