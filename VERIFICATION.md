# Verification evidence

This document records bounded package verification. It is not a certification of every host or generated output.

## Current source: 1.2.0

The learning-mode source checks are recorded in [1.2.0 verification](verification/release-1.2.0.json). They cover the 37-skill package, mapped learning domains, menu/production-entry instructions, lesson/progress contracts, source-guarded greeting override, existing production checks, native wrapper and complete source inventory. These are deterministic source and filesystem checks, not executed conversations or educational outcome measurements.

The new `learning-mode-cases.json` contributes sixteen planned scenarios. The effective suite contains 183 planned cases; loading and validating them is not running a model. The [1.2.0 hosted readback](verification/hosted-release-1.2.0.json) confirms the existing private plugin was updated: all 22 changed/new files match local source (byte equality, except normalized JSON where recorded), and its complete 732-path inventory matches. This does not confirm a client cache refresh or a running lesson. GitHub publication is now authorized as part of the paired update; see [release status](RELEASE_STATUS.md). The subsequent [source parity check](verification/source-parity-1.2.0.json) confirms byte equality for 721 readable files and path/size equality for all 732 files after matching the host manifest serialization. Seven large text files and four binary files could not be hash-checked because source reads returned HTTP 413 and archive downloads returned HTTP 403; these files were not changed in this update.

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
