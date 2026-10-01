# Release status

Source version: **1.3.2**. Date: 2026-10-01.

| Field | Value |
|---|---|
| Changes | Required short descriptions added to fourteen skill interface files; canonical metadata guard and negative tests |
| Metadata coverage | All 37 included skill interfaces have valid descriptions; existing names, prompts and policies preserved |
| Confirmed source defect | Current OpenAI package checks require a nonempty interface.short_description when agents/openai.yaml is included |
| Canonical welcome | Unchanged; SHA-256 ec8422f9611c58f10706b9b71d5f0990d586f644e5d15f59121560cb6a71c943 |
| Source verification | 99 Node, 8 GEPA adapter, 10 installer and 23 asset tests PASS; 140 full checks in serial suites; canonical validation and packaging PASS |
| GitHub publication | [v1.3.2](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases/tag/v1.3.2); source 7234f02bdca05c29c57ade13796e40a224eb30ea; release CI 36869967557 PASS |
| Existing hosted plugin | 1.3.2; pluginrel_6abe61f7ab2c8191a5548f4fae4eb010; identity and private personal audience preserved |
| Post-update active client | NOT_RUN; this release does not establish ordinary-ChatGPT registration or startup compliance |
| Baseline host feedback | Ordinary ChatGPT startup FAIL in owner trials; Work capability introduction PASS_REPORTED, exact match Unknown. [1.3.1 feedback](verification/startup-host-feedback-1.3.1.json) |
| Full readback | All 743 GitHub blob hashes and saved-TAR/uploaded-ZIP file contents match; all 37 interface descriptions valid; zero unreadable files |
| Scope and evidence | [Bounded metadata repair](verification/scope-1.3.2.json), [release checks](verification/release-1.3.2.json) |

The metadata defect is confirmed, while its causal role in the reported ordinary-ChatGPT missing-skill response remains unproven. Every skill instruction, canonical welcome, menu, checkpoint, learning method, ID, existing display name, prompt, policy, asset and pinned source is preserved. Source checks and publication remain separate from active-client behavior.
