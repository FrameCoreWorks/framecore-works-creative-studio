# Creativity audit of 1.81.0: decisions

Date: 2026-10-15. Input: the owner's creativity audit of 1.81.0 at `e9343c2` (text trials M01 to M06 and C1 to C6, an independent rubric judgement, a small paired comparison and counterexamples against the evaluator). Trigger under maintenance mode: reproduced defects in the creative evaluation and weaknesses the audit documents in the ideation output. Change CC-20261015-01, release 1.82.0.

## Fixed

| Audit point | Change | Evidence |
|---|---|---|
| P1 "creative PASS" passes a template answer: three coloured squares passed all 11 briefs | new `directions` check in `scripts/host_eval.py`: the exact number of directions where the brief names it, each direction mentions this brief (client, category or offer), no two directions are near copies (word overlap above 0.6); added to every case of `tests/host-evals/creative.json` | `tests/test_host_eval.py`: the squares answer now fails all 11 cases |
| P1 a changed offer passes ("+20% on a second check-up in Warsaw") | C02 locks "-20%", "first check-up" and Poznań and refuses "+20%", "second" and Warsaw; H03 locks the two-hour promise | `tests/test_host_eval.py` |
| P1 words stand in for meaning: "Nie tylko kłosy" read as excluding wheat; "Wariant A/B/C" read as no directions; four directions accepted for three | "nie tylko" is no longer a negation; "wariant", "opcja", "propozycja" label directions; a "Trasa pracy" footer is not a direction; the count is exact | `tests/test_host_eval.py` |
| P1 three directions are not always three arguments (C1) | `ideation-method.md` step 5: write what the viewer concludes for each direction; if two of these sentences could swap places, rebuild one; a new metaphor, name or reveal order on the same argument is not a new direction | live creative run below |
| P1 product-specific is not brand-specific (C1, C2, C5) | step 6 brand test: tell apart category fit, a true product trait and what only this brand could own; ask for a missing brand fact or leave it openly unresolved; never invent history, patents or advantages to pass the swap test | live creative run below |
| P2 an effect added under pressure does not strengthen the idea (C4) | step 6 removal test: what does the viewer stop understanding without the effect; if nothing, find a better event instead of adding particles, moves or transitions | live creative run below |

The rubric judge stays advisory: a second model call is not deterministic enough to block a release, and the audit's own paired comparison shows how narrow such judgements are. The new checks make the deterministic part harder to pass with a template; they still do not certify originality.

## Live run after the change

Claude Code, 2026-10-15, the whole creative suite with the new checks (`verification/host-evals/2026-10-15-1.81.0-creative.json`, 11 cases, about 0.45 million tokens, about 5 minutes): 7 PASS, 4 FAIL. The new `directions` check passed in every case but one, where its brief pattern missed "oprawki" and "salon" (fixed). The four failures are the older stock-motif check: two of three directions still lean on the category's motifs (Motława and a beach for a Gdańsk bike service, scales and figures for an accounting firm, frames for an optician named "Soczewka", and in C02 only a passing mention of teeth). The same check failed in six of eleven cases in the 1.66.0 runs, so this is a lasting limit of the ideation output, not a regression; one run per case cannot show whether the new step 5 and step 6 text changes it. The instructions were not tuned further on this suite, as the audit advises.

## Kept as it is

- The plan validator's `structurally_valid_plan`, `unverified`, `uninspected` result: the audit confirms it reports structure only and must not be widened into a creative verdict.

## Owner decisions (not done here)

- P1 media evidence and P2 repertoire and fair comparison: animatics and renders with real audio, briefs that need ambitious FX or a music-led edit, repeated trials per condition with blind ordering, a practitioner's motion and mix review, then an audience test. These are a study with renders, costs and outside reviewers; the audit's own proposal for the next stage (section 7) is the plan when the owner wants it.
- The audit's three rewrites (M05, C2, C4) are the judge's ideas, not Studio output; they are not added to the package (owner decision 2026-10-11: no ready-made ideas).
