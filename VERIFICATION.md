# Verification evidence

This document records bounded package verification. It is not a certification of every host or generated output.

## Current release

The current records are [1.0.1 checks](verification/release-1.0.1.json) and [hosted update/readback](verification/hosted-release-1.0.1.json). Earlier 1.0.0 and preparation reports are historical snapshots; their fields describe that earlier setup.

Seven isolated filesystem installer tests passed: read-only planning, complete install/readback and no-op repeat, local-edit preservation, identity collision, partial-state protection, symlink/discovery-overlap rejection and extra-file detection. Canonical structural validation passed with 37 modules. All existing skill, asset and original-source bytes and interface fields were preserved. These checks do not establish native host activation or creative quality.

Archive verification compares packaged bytes against the source inventories. This proves packaging integrity, not automatic skill selection or media quality.

## Historical evidence

The [dev.31 report](plugins/framecore-work-creative-studio/docs/creative-upgrade-verification.json) records 43 passing Node checks, 23 passing Python checks and two bounded text-use exercises. These are historical observations, not fresh results for 1.0.0.

The dev.33 saved package was checked against the submitted source and its original logo. Its structural validation passed before this release preparation.

## Not executed

- The 167 planned behavioral evaluation specifications.
- Real-client pilots and generated-media quality evaluation.
- External paid-provider integrations.
- New installations across every ChatGPT/Codex surface.
- Automatic cross-host memory synchronization.
- Exhaustive behavioral testing on the installed hosted 1.0.0 release.

The presence of fixtures, examples or expected outputs is not recorded as passing execution.
