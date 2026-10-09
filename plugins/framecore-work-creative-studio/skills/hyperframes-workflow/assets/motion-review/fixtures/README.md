# Text-audit and acceptance fixtures

Small, original pages and one contract that reproduce the defects of a reviewed 20-second 9:16 shop reel (2026-10-09) and the cases that must keep passing. No brand assets or real prices are used. Each HTML page is a 1080 x 1920 composition with a HyperFrames-style `window.__timelines.main` that seeks without GSAP, so it runs offline.

| Fixture | Expected result |
| --- | --- |
| `floor-word-clipped.html` | FAIL: the decorative "TWÓJ WYBÓR" (182 px, `left: 70px`, `letter-spacing: -9px`, `nowrap`, inside `overflow: hidden`) shows "WYBÓR" about 62% visible in a hold |
| `floor-word-ignored.html` | FAIL: the same word marked `data-layout-ignore`, plus an `ignore-flag` warning |
| `container-fits-lines-clipped.html` | FAIL: a box that fits the frame hides the last two words of its text, and a word is cut by its own box |
| `fitted-text-pass.html` | PASS: Polish diacritics and long phrases, all complete |
| `transition-mask-pass.html` | PASS: a reveal with `clip-path` and a slide-in cut words at 0.4 s (transitional); the hold at 2 s is complete |
| `declared-exception.html` | PASS with one exception: `data-text-clip-ok` gives the reason, and the exception asks for a pixel review |
| `search-to-cta.motion.json` | A 20 s, 1080 x 1920, 30 FPS silent proof contract with a recorded `strategy` (hook and payoff, CTA closing the shown action, an unknown claim kept out of the copy, three concepts weighed). It checks the tools, not taste: its picture is text only, because no product photographs were authorised |

```sh
node ../text-audit.mjs floor-word-clipped.html --out audit --times 1 --holds 0.5-7.5
node ../text-audit.mjs transition-mask-pass.html --out audit-mask --times 0.4,2
node ../../gsap-motion-starter/check-score.mjs search-to-cta.motion.json --storyboard
```

The tests in `tests/motion-toolkit.test.mjs` (browser, opt-in) and `tests/motion_acceptance_test.py` run these expectations.
