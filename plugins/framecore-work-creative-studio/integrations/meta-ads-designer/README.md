# Meta Ads Designer: selective method adaptation

Source: [AI Evolution Labs / meta-ads-designer](https://github.com/aievolutionpl/meta-ads-designer/tree/656ce907380448389559958f055c8b43d71ab26e), observed version 6.5.0, pinned commit `656ce907380448389559958f055c8b43d71ab26e`. Reviewed on 2026-10-03.

This integration adapts selected MIT-licensed methods. [The original license](LICENSE) retains Copyright (c) 2026 AI Evolution Labs. The source repository is not installed or vendored as a second skill. Its code, artwork, rule registry and provider routes are not part of this package. Source paths and Git blob hashes are in [the manifest](source-manifest.json).

## Decision map

| Source method | Decision | Studio destination or reason |
| --- | --- | --- |
| Static format selected from available proof | Adapt | [Ad creative analysis](../../skills/ecommerce-campaign-strategy-director/references/ad-creative-analysis.md); eight practical structures tied to claims and source evidence |
| Competitor ad teardown | Adapt with correction | Same reference and [experiment card](../../skills/ecommerce-campaign-strategy-director/templates/creative-experiment-card.md); observation separated from hypothesis, no winner inference from longevity |
| Results become the next brief | Adapt with correction | [Performance feedback](../../skills/ecommerce-campaign-strategy-director/references/creative-performance-feedback.md); comparable cohorts, alternatives and scoped next action |
| Variation matrix | Already present; add a worksheet | Existing strategy owns exploration/test distinction; card binds actual baseline and variant revisions |
| Product truth, exact copy, typography, original mechanism and visual QA | Already present | Existing integrated static method, claim ledger, references and shared QA remain authoritative |
| Style atlas and niche catalogues | Defer | Large overlapping catalogue; year/trend claims need their own evidence and do not justify a global aesthetic |
| Fixed safe-zone/export constants and Andromeda duplicate-delivery claims | Do not adopt as platform facts | Current placement checks stay task-specific; no deterministic delivery guarantee |
| Mandatory 3–6-question intake, blanket regeneration and scored QA | Reject for this integration | Conflicts with proportional intake, preservation and one existing bounded review loop |
| Diagnostic script, pixel QA helper and provider wrapper | Do not import | Automatic metric labels and mixed-metric handling are unsuitable as authoritative diagnoses; pixel heuristics do not prove design quality; generation routing is already owned |

## Source review findings

The reviewed diagnostic helper maps link/all-click rates into one field, pools available rows without cohort/attribution controls, drops zero rates from medians and labels frequency of at least 3.5 as fatigue without a time-series decline. Its number parser reads a comma-only value such as `1,000` as `1.000`, with no locale declaration. These are source-level findings, not claims from live account testing. The adaptation therefore retains explicit metric definitions, locale, valid zeros, undefined denominators and alternative explanations; the upstream script was not executed or installed.

The competitor guide calls long-running ads proven winners. Studio treats observed presence and dates as observations only. Neither a public ad nor attractive design establishes profitable performance.

The upstream format guide makes proof a useful selection constraint. Studio also requires substantiation for objective claims inside customer quotations, keeps necessary qualifiers readable, and treats synthetic demonstration as illustration rather than evidence of a real result.

## Evidence scope

Inspection covered the entrypoint, README, license, relevant format/teardown/variation/performance/platform methods, and diagnostic/generation/QA code. Additional design, headline, artifact and style material was sampled for overlap and conflicts. Promotional image quality, provider behavior and live ad-account outcomes were not tested.

Primary-source checks:
- [Meta engineering: Andromeda](https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/) describes learned retrieval and hierarchical indexing. It does not establish the upstream's operational rule that visually similar ads receive only one delivery chance. This integration makes no such promise.
- [Meta Ads Guide](https://www.facebook.com/business/ads-guide/update) redirected to login during this review. Current placement dimensions and safe zones were not verified and are not hard-coded here.
- [Meta's Ad Library announcement](https://about.fb.com/news/2019/03/a-better-way-to-learn-about-ads/) is historical context, not verification of today's fields. Read the actual accessible source for a particular campaign; unavailable fields remain Unknown.

Saved instructions and source checks do not prove active-client behavior, image quality or campaign lift. No account connector, dependency, generation provider, ad publication or budget change is introduced.
