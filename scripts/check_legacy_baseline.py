#!/usr/bin/env python3
"""Retired on 2026-10-10 by the owner's decision.

The historical legacy suite (validate-package.mjs and package.test.mjs) predated the conditional research policy and
failed by design (134 validator errors, 20 of 67 tests). It no longer gates releases; both files are inert stubs in the
package, because a hosted plugin update cannot delete paths. tests/legacy-baseline.json is kept as the historical record
of what the suite reported last. Current behaviour is checked by scripts/check_all.sh.
"""
import sys

if __name__ == '__main__':
    print('Legacy suite retired on 2026-10-10 (owner decision); tests/legacy-baseline.json is kept as history.')
    sys.exit(0)
