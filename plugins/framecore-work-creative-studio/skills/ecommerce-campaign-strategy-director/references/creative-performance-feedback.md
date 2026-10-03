# Creative results to the next brief

Use when the user supplies campaign results or asks to interpret an existing ad comparison. This is a practical extension of [measurement and iteration](website-to-campaign.md#measurement-and-iteration). Reuse that contract and one Project State; do not add a campaign-management service or an automatic optimization loop.

## Establish what can be compared

Bind each row to campaign/asset ID and creative revision. Names alone may collide. Record source, reporting period/timezone, currency, business objective, conversion event, attribution basis, audience, placement, delivery changes and known data gaps. Compare like cohorts and time windows; an account-wide median mixing prospecting, remarketing, objectives or currencies is not a defensible creative baseline.

For CSVs, tables or screenshots:
- Preserve the original headers and values, then map each metric explicitly. Record any transcription uncertainty.
- Resolve locale, delimiter, decimal/thousands separators and percentage units before arithmetic. A value such as `1,234` is ambiguous without its export convention.
- Keep link clicks distinct from all clicks, each conversion event distinct, and zero distinct from missing. Reject non-finite or impossible values for dependent calculations.
- Retain valid zero rates in summaries. Derive a rate only from compatible numerator and denominator. Never average row percentages or CPAs as an aggregate; use sums of compatible counts and amounts where appropriate. Do not sum overlapping reach as unique people.
- With zero conversions, show spend and zero conversions and mark CPA undefined; never report zero acquisition cost. Missing or zero denominators remain undefined/Unknown. Zero revenue with positive known spend gives a zero attributed ROAS, not missing data.
- Video measures need the platform's actual definitions and comparable clip durations. Do not apply a video retention ratio to static ads or infer that it measures continuous viewing.

Use the account's relevant historical cohort when available, with the comparison period and its limits. Otherwise report observations and a proposed measurement plan. No universal frequency cutoff, impression floor, CTR target or winning-ad threshold is introduced. A large impression count alone does not establish sufficient outcome evidence.

## Symptoms produce hypotheses, not diagnoses by decree

Select only rows supported by the supplied data. Inspect the actual creative and relevant destination before making a design-specific claim.

| Observed pattern within a comparable cohort | Creative hypothesis to inspect | Other explanations to check | Bounded next action |
| --- | --- | --- | --- |
| Link CTR falls over time while frequency rises | Message may have become familiar | Audience/placement mix, seasonality, offer changes, delivery changes | Compare periods and inspect the opening message; propose one new hook only if evidence supports that test |
| Few early video views | First frame or opening may not communicate the promise | Autoplay/view definitions, placement, audience delivery | Review actual opening and measurement basis; test one opening change |
| Early views remain stable but later-view ratio falls | Product/proof may arrive late or opening and body may mismatch | Clip duration, denominator definition, distribution differences | Inspect timing; propose one sequence change rather than declaring the story failed |
| Link CTR looks adequate but attributed conversion cost rises | Ad-to-page promise may be unclear | Tracking, conversion lag, destination errors, price, stock, checkout, audience quality | Verify continuity and data first; creative-only repair may be the wrong intervention |
| CPM rises with similar creative | No design conclusion follows from CPM alone | Auction conditions, audience/placement mix, objectives, bids or budgets | Inspect delivery context before proposing a design change |
| A variant has a lower reported CPA | Its mechanism is a candidate for further study | Few conversions, allocation bias, different audiences, lag or attribution | Retain as a candidate within the measured scope; do not label an untested universal winner |

Changing one creative variable does not by itself establish causality. Also check how exposure was assigned, whether the groups and periods are comparable, whether delivery or tracking changed, and whether the planned evidence threshold was met. Adaptive delivery and sequential before/after comparisons can confound results. Report a causal conclusion only when the actual experimental design and evidence support it; otherwise name a hypothesis.

## Write the smallest next brief

Return:
1. Observed result with source, counts/denominators, comparison and limitations.
2. Candidate explanation plus alternatives, and what would distinguish them.
3. A proposed decision: retain, revise, test further, stop or inconclusive, using the existing strategy meanings.
4. A next-brief delta: asset/revision, one tested change when isolation is intended, locks to preserve, needed evidence, primary metric and checkpoint.

Use the [creative experiment card](../templates/creative-experiment-card.md) only as a view of the current campaign state. Keep lessons scoped to the brand, audience, offer, period and evidence; do not promote them into permanent global rules or user memory. Reuse successful locks without assuming old results transfer to a new offer.

Proposed pause, scale, publication and budget changes remain recommendations requiring separate authorization. A request to analyze results does not authorize account access, uploading client exports, executing providers or producing a new asset. Keep private results out of public source packages.

## Worked interpretation, synthetic data

Two ads each have 10,000 impressions and PLN 400 spend in an otherwise comparable supplied table. A has 200 link clicks and 4 attributed purchases; B has 100 link clicks and 8 attributed purchases. Link CTR is 2% versus 1%; reported cost per attributed purchase is PLN 100 versus PLN 50.

B has the lower reported acquisition cost in this table, while A has the higher link CTR. With only these rows, neither the design cause, statistical reliability nor incremental effect is known. Inspect assignment, event/attribution definitions, creative revisions and destination continuity before a next test. If assignment or creative versions are unavailable, report the comparison as inconclusive for causal learning. Do not call A a winner from CTR alone.

Source adaptation and limitations: [Meta Ads Designer integration](../../../integrations/meta-ads-designer/README.md).
