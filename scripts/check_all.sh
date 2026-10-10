#!/usr/bin/env bash
# Every current check, in one place: the release workflow, the checks workflow and a local run use this same list.
# `--fast` runs the quick subset for the edit loop: it skips the media determinism suite
# (motion-toolkit.test.mjs), the benchmark script and the GEPA pilot. Releases and CI always run the full list.
# The historical validate-package.mjs / package.test.mjs suite was retired on 2026-10-10.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")/.."
FAST=0
[ "${1:-}" = "--fast" ] && FAST=1
P=plugins/framecore-work-creative-studio
node "$P/scripts/validate-studio.mjs" > /dev/null
python3 -m unittest discover -s tests -p 'test_codex_install.py' -v
python3 -m unittest discover -s tests -p 'test_package_identity.py' -v
[ "$FAST" = 1 ] || python3 -m unittest discover -s tests -p 'test_motion_benchmark.py' -v
python3 -m unittest discover -s tests -p 'test_host_smoke.py' -v
python3 -m unittest discover -s tests -p 'test_hosted_readback.py' -v
python3 -m unittest discover -s tests -p 'test_claude_plugin.py' -v
NODE_TESTS=("$P/tests/studio.test.mjs" "$P/tests/workflow-kit.test.mjs" "$P/tests/creative-upgrade.test.mjs" \
  "$P/tests/learning-mode.test.mjs" "$P/tests/quality-methods.test.mjs" "$P/tests/presentation.test.mjs")
# motion-toolkit.test.mjs also runs motion-quality.test.mjs, which it imports.
[ "$FAST" = 1 ] || NODE_TESTS+=("$P/tests/motion-toolkit.test.mjs")
node --test --test-concurrency=1 "${NODE_TESTS[@]}"
[ "$FAST" = 1 ] || python3 -m unittest discover -s tests -p 'test_gepa_studio_pilot.py' -v
python3 "$P/tests/asset_manifest_test.py"
python3 "$P/tests/captions_test.py"
python3 "$P/tests/environment_check_test.py"
python3 "$P/tests/motion_acceptance_test.py"
python3 "$P/tests/skill_finder_test.py"
python3 "$P/tests/animate_engine_test.py"
python3 "$P/tests/static_render_test.py"
python3 -m unittest discover -s tests -p 'test_host_eval.py' -v
