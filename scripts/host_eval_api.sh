#!/usr/bin/env bash
# Studio behaviour tests on the Claude API, under one dollar ceiling for the whole run (owner request 2026-11-06).
#
#   ANTHROPIC_API_KEY=... bash scripts/host_eval_api.sh gate 2           # release gate, at most USD 2
#   ANTHROPIC_API_KEY=... bash scripts/host_eval_api.sh all 30 --judge   # every suite except companion
#   ANTHROPIC_API_KEY=... bash scripts/host_eval_api.sh routing 5
#
# Each suite runs as its own pass (at most 25 cases, scripts/host_eval.py) with the budget still left; once the ceiling
# is reached no new case starts. Records go to verification/host-evals/. The key comes from the environment only.
set -uo pipefail
cd "$(dirname "$0")/.."
target="${1:?suite name, gate or all}"
ceiling="${2:?dollar ceiling for the whole run}"
shift 2
[ -n "${ANTHROPIC_API_KEY:-}" ] || { echo "host_eval_api: set ANTHROPIC_API_KEY" >&2; exit 2; }

case "$target" in
  gate) passes=("--gate") ;;
  all) passes=(); for f in tests/host-evals/*.json; do
         name="$(basename "$f" .json)"
         python3 -c "import json,sys; sys.exit(0 if json.load(open('$f')).get('requires_plugin') else 1)" && continue
         passes+=("--suite $name"); done ;;
  *) passes=("--suite $target") ;;
esac

spent=0
status=0
for pass in "${passes[@]}"; do
  left="$(python3 -c "print(f'{max(0.0, $ceiling - $spent):.2f}')")"
  if python3 -c "import sys; sys.exit(0 if $left <= 0 else 1)"; then
    echo "host_eval_api: ceiling USD $ceiling reached; not run: $pass" >&2; status=1; continue
  fi
  echo "== $pass (USD $left left)"
  before="$(ls verification/host-evals/ 2>/dev/null | sort)"
  # shellcheck disable=SC2086
  python3 scripts/host_eval.py $pass --write --allow-api-billing --max-cost-usd "$left" "$@" || status=1
  record="$(comm -13 <(echo "$before") <(ls verification/host-evals/ | sort) | tail -1)"
  if [ -n "$record" ]; then
    cost="$(python3 -c "import json; print(json.load(open('verification/host-evals/$record'))['summary'].get('cost_usd', 0))")"
    spent="$(python3 -c "print($spent + $cost)")"
  fi
done
echo "host_eval_api: total USD $(python3 -c "print(f'{$spent:.2f}')") of $ceiling"
exit $status
