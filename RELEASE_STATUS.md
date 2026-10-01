# Release status

Source version: **1.3.2**. Date: 2026-10-01.

| Field | Value |
|---|---|
| Changes | Required short descriptions added to fourteen skill interface files; canonical metadata guard and negative tests |
| Metadata coverage | All 37 included skill interfaces have valid descriptions; existing names, prompts and policies preserved |
| Confirmed source defect | Current OpenAI package checks require a nonempty interface.short_description when agents/openai.yaml is included |
| Canonical welcome | Unchanged; SHA-256 ec8422f9611c58f10706b9b71d5f0990d586f644e5d15f59121560cb6a71c943 |
| Source verification | 99 Node, 8 GEPA adapter, 10 installer and 23 asset tests PASS; 140 full checks in serial suites; canonical validation and packaging PASS |
| GitHub publication | PENDING |
| Existing hosted plugin | Update PENDING; saved baseline 1.3.1 |
| Post-update active client | NOT_RUN; this release does not establish ordinary-ChatGPT registration or startup compliance |
| Baseline host feedback | Ordinary ChatGPT startup FAIL in owner trials; Work capability introduction PASS_REPORTED, exact match Unknown. [1.3.1 feedback](verification/startup-host-feedback-1.3.1.json) |
| Full readback | PENDING |
| Scope and evidence | [Bounded metadata repair](verification/scope-1.3.2.json), [release checks](verification/release-1.3.2.json) |

The metadata defect is confirmed, while its causal role in the reported ordinary-ChatGPT missing-skill response remains unproven. Every skill instruction, canonical welcome, menu, checkpoint, learning method, ID, existing display name, prompt, policy, asset and pinned source is preserved. Source checks and publication remain separate from active-client behavior.
