# External review of 1.76.0 (Argon 4): decisions

Date: 2026-10-13 to 2026-10-14. Input: a review of package 1.76.0 written by another model and passed on by the owner (26 numbered findings plus expansion proposals). Each finding was checked against the source at `e7ef587` before anything changed; a finding is fixed only when its failure reproduces. Fixes ship in 1.77.0 (change CC-20261013-07). Trigger under maintenance mode: defects reported by an external review and reproduced here.

## Fixed (reproduced, fixed, with a test or a direct check)

| Finding | What failed | Fix |
|---|---|---|
| BUG-01 | `render.py` read any file a contract named: an absolute or `../` asset path, and an absolute font file path | Assets must resolve inside the contract's folder; font files inside the contract's folder, `font_dirs`, `STUDIO_FONT_DIR` or the bundled fonts. `sound.py` applies the same rule to the three WAV inputs. SVG logos: cairosvg 2.9 already refuses external files by default (`unsafe=False`, checked with a `file://` image), so no change there. |
| BUG-02 (part) | The release job, which holds a write token, installed the GEPA pilot from a Git URL | Removed from `release.yml`; `checks.yml` (read-only) still runs the pilot. `pages.yml` keeps its credentials: it pushes `gh-pages`. |
| BUG-03 | `release.py` pushed one session's branch and wrote one session's trailer on every release | Both now come from `STUDIO_RELEASE_BRANCHES` and `STUDIO_COMMIT_TRAILERS`; empty by default. |
| BUG-04 | `quote_calc.py`: an hours line showed `4 h × 800 = 800`, days lines showed quantity 1, the discount was invisible, and an empty "Payment:" line appeared | Lines show hours or days with the hourly or daily rate; a discount line; payment only when terms exist. Test added. |
| BUG-05 (part) | `clip_review.py` matched shot `S1` to `S10.mp4` | Token-boundary match, longest ID first. Test added. The four decodes per clip are a speed matter, left as is. |
| BUG-11 (part) | `pl_copy_check.py` flagged "Ci klienci" as mixed address; the safe fix and `brand_guide.py` bound a no-break space after any one-letter word ("Wariant B", English "A") | `ci` removed from the informal-address pattern; binding only after the Polish one-letter words a, i, o, u, w, z. |
| BUG-12 | `vo_budget.py` dropped the pause of a standalone dash and of a full stop inside closing quotes | Pauses read from every token with closing quotes and brackets set aside. Test added. |
| BUG-13 (part) | `image_probe.py` OCR check: "Promocja 50 99 zł" passed for "Promocja -50% — 99,99 zł", and a word repeated in the copy counted once | Numbers keep sign, decimals and per cent; each occurrence counts. Test added. The presets file is part of the package, so its import is not a defect. |
| BUG-15 | Five scripts cut output names at the first dot (`spot.v2.json` → `spot`), so versions overwrote each other's outputs | Only the known contract suffixes are removed. Existing tests pass. |
| BUG-18 (part) | CI never ran the headless frame-review tests (no browser named) | `checks.yml` names the runner's Google Chrome. The M04 critique score is the owner's evaluation record, not reproduced here. |
| BUG-20 | UGC creator brief said disclosure goes "inside the video or caption" | Both: in the video (on screen and spoken) and at the start of the caption, in the audience's language. |
| BUG-26 | `NOTICE` and `LICENSE_STATUS.md` did not list the MIT integrations added after 1.0.0, the awesome-ai-motion card text, the HyperFrames registry names or the OFL fonts | Listed with pinned commits; each folder already keeps its upstream licence text (the atlas README carries the MIT text). |

## Not defects (checked, no change)

- **BUG-06**: persistent elements are rendered in Remotion: `buildCaptions` returns them in the overlay and `captionsFrame` times them. Sound cues are mixed to a file by `sound.py`, which Remotion plays as audio.
- **BUG-09**: `build_from_segments` has no `profile` or `audience` parameter; timing from supplied segments keeps the transcript's times by design.
- **BUG-10**: `edit_export.py` treats 29.97 timecode as non-drop-frame consistently and says so (`FCM: NON-DROP FRAME`).
- **BUG-16**: `motion-quality/score.mjs` is the small frame and tone helper its tests and the paper renderer use, not a second contract validator; the full check is `motion-scenes.mjs`.
- **BUG-25**: the validators refuse "executed" evaluation records on purpose: an execution claim must come from a host run recorded in `verification/`, never from editing a case file.

## Owner decisions (not done: maintenance mode needs a trigger from real use)

- BUG-07 (the GSAP starter has three fixed scenes: it is a starter, and HyperFrames is the production route), BUG-08 (browser export loses web fonts and sound: the shell route is `capture-html.mjs` or the renderer), BUG-14 (contrast of text over photos), BUG-17 (the bundled Animate `handwrite` demo has seven glyphs; vendored code stays byte-identical), BUG-21 (text-in-image policy wording across skills), BUG-22 (role roster count), BUG-23 (`openai.yaml` depth), BUG-24 (top-level display fields for Google Antigravity: a new host).
- BUG-19 (generator snapshot facts such as Sora 2 status and image model IDs): dated facts need a research pass with sources before any edit; the review gives none.
- Expansion proposals: new skills, merged or removed skills, Antigravity support, and package slimming. Slimming by deleting paths is not possible for existing ChatGPT installations (paths are permanent).
