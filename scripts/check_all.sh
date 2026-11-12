#!/usr/bin/env bash
# Every current check, in one place: the release workflow, the checks workflow and a local run use this same list.
# `--fast` runs the quick subset for the edit loop: it skips the media determinism suite
# (motion-toolkit.test.mjs), and the GEPA pilot. Releases and CI always run the full list.
# The historical validate-package.mjs / package.test.mjs suite was retired on 2026-10-10.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")/.."
FAST=0
[ "${1:-}" = "--fast" ] && FAST=1
P=plugins/framecore-work-creative-studio
node "$P/scripts/validate-studio.mjs" > /dev/null || { node "$P/scripts/validate-studio.mjs"; exit 1; }
python3 -m unittest discover -s tests -p 'test_codex_install.py' -v
python3 -m unittest discover -s tests -p 'test_package_identity.py' -v
python3 -m unittest discover -s tests -p 'test_host_smoke.py' -v
python3 -m unittest discover -s tests -p 'test_hosted_readback.py' -v
python3 -m unittest discover -s tests -p 'test_hosted_update.py' -v
python3 -m unittest discover -s tests -p 'test_claude_plugin.py' -v
python3 -m unittest discover -s tests -p 'test_hookify_rules.py' -v
python3 -m unittest discover -s tests -p 'test_release.py' -v
python3 -m unittest discover -s tests -p 'test_version_bump.py' -v
python3 -m unittest discover -s tests -p 'test_publish_release.py' -v
NODE_TESTS=("$P/tests/studio.test.mjs" "$P/tests/workflow-kit.test.mjs" "$P/tests/creative-upgrade.test.mjs" \
  "$P/tests/learning-mode.test.mjs" "$P/tests/quality-methods.test.mjs" "$P/tests/presentation.test.mjs" "$P/tests/logo-design-engine.test.mjs")
node --test --test-concurrency=1 "${NODE_TESTS[@]}"
[ "$FAST" = 1 ] || python3 -m unittest discover -s tests -p 'test_gepa_studio_pilot.py' -v
python3 "$P/tests/asset_manifest_test.py"
python3 "$P/tests/environment_check_test.py"
python3 "$P/tests/runtime_inventory_test.py"
python3 "$P/tests/skill_finder_test.py"
python3 "$P/tests/extensions_test.py"
python3 "$P/tests/static_render_test.py"
python3 "$P/tests/print_pdf_test.py"
python3 "$P/tests/web_reach_test.py"
python3 "$P/tests/pl_copy_check_test.py"
python3 "$P/tests/studio_gate_test.py"
python3 "$P/tests/image_probe_test.py"
python3 "$P/tests/quote_calc_test.py"
python3 "$P/tests/vo_budget_test.py"
python3 "$P/tests/board_compose_test.py"
python3 "$P/tests/sheet_export_test.py"
python3 "$P/tests/shot_plan_check_test.py"
python3 "$P/tests/prompt_pack_test.py"
python3 "$P/tests/clip_review_test.py"
python3 "$P/tests/svg_wordmark_test.py"
python3 "$P/tests/brand_guide_test.py"
python3 "$P/tests/prompt_record_test.py"
python3 "$P/tests/craft_lint_test.py"
python3 "$P/tests/design_md_test.py"
python3 "$P/tests/ai_writing_check_test.py"
python3 "$P/tests/knowledge_wiring_test.py"
python3 "$P/tests/companion_intake_test.py"
python3 plugins/voice-narration/tests/runtime_test.py
python3 plugins/voice-narration/tests/package_test.py
for t in site style draft catalog package; do python3 plugins/brand-kit/tests/${t}_test.py; done
python3 -m unittest discover -s tests -p 'test_host_eval.py' -v
