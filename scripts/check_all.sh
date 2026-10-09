#!/usr/bin/env bash
# Every current check, in one place: the release workflow, the checks workflow and a local run use this same list.
# The historical validate-package.mjs / package.test.mjs suite is not part of it; run it with
# `node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs --legacy` and report its status separately.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")/.."
P=plugins/framecore-work-creative-studio
node "$P/scripts/validate-studio.mjs" > /dev/null
python3 -m unittest discover -s tests -p 'test_codex_install.py' -v
python3 -m unittest discover -s tests -p 'test_package_identity.py' -v
python3 -m unittest discover -s tests -p 'test_motion_benchmark.py' -v
python3 -m unittest discover -s tests -p 'test_host_smoke.py' -v
python3 -m unittest discover -s tests -p 'test_hosted_readback.py' -v
# motion-toolkit.test.mjs also runs motion-quality.test.mjs, which it imports.
node --test --test-concurrency=1 "$P/tests/studio.test.mjs" "$P/tests/workflow-kit.test.mjs" "$P/tests/creative-upgrade.test.mjs" \
  "$P/tests/learning-mode.test.mjs" "$P/tests/quality-methods.test.mjs" "$P/tests/motion-toolkit.test.mjs" "$P/tests/presentation.test.mjs"
python3 -m unittest discover -s tests -p 'test_gepa_studio_pilot.py' -v
python3 "$P/tests/asset_manifest_test.py"
python3 "$P/tests/captions_test.py"
