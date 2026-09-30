# Verification evidence

This document records bounded package verification. It is not a certification of every host or generated output.

## Current source: 1.2.2

The [1.2.2 source checks](verification/release-1.2.2.json) passed canonical validation, 48 local Node runner checks, 23 asset checks, 10 installer tests and nine additional installer probes. Two fresh low-reasoning sandbox conversations covered seven responses, including expired-menu clarification and offline-learning disclosure. These are source-use probes, not installed-client observations. GitHub CI passed 62 Node checks, 10 installer tests and 23 asset checks, then published v1.2.2 with five verified assets. The plugin ZIP digest matches the complete local archive. [GitHub publication](verification/github-publication-1.2.2.json) verifies all 733 package file hashes; [hosted readback](verification/hosted-release-1.2.2.json) verifies the 14 changed files byte-for-byte and the complete 733-path/size inventory, with 719 omitted files preserved by the guarded overlay. The package retains 733 files and 37 skill roots; no stress reports or transcripts were added. Active-client behavior remains unverified.

## Previous source: 1.2.1

This update restores the complete welcome and the creative entry sequence. Current deterministic source checks, package inventory, bounded text-only entry probe and paired release readback are recorded in [1.2.1 source checks](verification/release-1.2.1.json). GitHub CI passed all 62 Node tests and published v1.2.1 with five verified assets. All 17 changed/new hosted files are byte-equal to source, and the complete 733-path/size inventory matches; see [publication](verification/github-publication-1.2.1.json) and [hosted readback](verification/hosted-release-1.2.1.json). The probe is an attributed source-use exercise, not observed behavior of a newly installed ChatGPT/Codex client. The 183 planned cases remain unexecuted host specifications.

## Previous source: 1.2.0

The learning-mode source checks are recorded in [1.2.0 verification](verification/release-1.2.0.json). They cover the 37-skill package, mapped learning domains, menu/production-entry instructions, lesson/progress contracts, source-guarded greeting override, existing production checks, native wrapper and complete source inventory. These are deterministic source and filesystem checks, not executed conversations or educational outcome measurements.

The new `learning-mode-cases.json` contributes sixteen planned scenarios. The effective suite contains 183 planned cases; loading and validating them is not running a model. The [1.2.0 hosted readback](verification/hosted-release-1.2.0.json) confirms the existing private plugin was updated: all 22 changed/new files match local source (byte equality, except normalized JSON where recorded), and its complete 732-path inventory matches. This does not confirm a client cache refresh or a running lesson. GitHub commit `65ab9bb8e54a88155acf3316241b79591ecc7983` and release `v1.2.0` are published, with a successful release workflow and five verified assets; see [publication evidence](verification/github-publication-1.2.0.json) and [release status](RELEASE_STATUS.md). The subsequent [source parity check](verification/source-parity-1.2.0.json) confirms byte equality for 721 readable files and path/size equality for all 732 files after matching the host manifest serialization. Seven large text files and four binary files could not be hash-checked because source reads returned HTTP 413 and archive downloads returned HTTP 403; these files were not changed in this update.

The historical [1.1.1 source checks](verification/release-1.1.1.json) and [hosted readback](verification/hosted-release-1.1.1.json) retain their original scope and release attribution.

## Historical evidence

The [1.1.0 source checks](verification/release-1.1.0.json) cover the provider catalog and installation guidance. They do not establish live provider authentication, entitlement, generation or all-host support.

The [dev.31 report](plugins/framecore-work-creative-studio/docs/creative-upgrade-verification.json) records 43 passing Node checks, 23 passing Python checks and two bounded text-use exercises. These are historical observations, not fresh results for 1.0.0.

The dev.33 saved package was checked against the submitted source and its original logo. Its structural validation passed before this release preparation.

## Not executed

- The 183 planned behavioral evaluation specifications, including sixteen learning-mode scenarios.
- Real-client pilots and generated-media quality evaluation.
- External paid-provider integrations.
- New installations across every ChatGPT/Codex surface.
- Automatic cross-host memory synchronization.
- Fresh-session learning/creation behavior, native choice controls and educational effectiveness on the 1.2.0 release.

The presence of fixtures, examples or expected outputs is not recorded as passing execution.
