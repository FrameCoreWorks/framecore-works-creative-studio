# Quality development 1.3.0

The owner authorized implementation of five improvements in sequence. The
bounded Hipson packet is in `verification/scope-1.3.0.json`; it defines scope,
protected surfaces, serial checks, zero external-model budget and paired source
publication. Hipson Adapter supplies the method; no full Hipson service or
independent supervising agent is claimed.

## Implemented sequence

1. Align F01–F03 with active policy: apply explained corrections directly,
   route selected static execution to Static Graphic Design Creator, align
   H01/H02/KP02 expected owners without changing their unexecuted status.
2. Add bounded relevant-example retrieval and calibrated judging: eight original
   synthetic cases (four static), each with good/bad/borderline anchors, decisions,
   consequences and exclusions. Deterministic selection filters domain, stage and
   supported locks before matching problem tags; at most three examples. Reversed
   A/B verdicts identify order disagreement. Hard gates precede taste; a synthetic
   anchor is not a confirmed user preference or demonstrated calibration.
3. Add CRITIC-inspired tool-backed verification to the existing critic. The
   read-only evidence checker compares exact strings, dimensions, units, counts
   and durations against revision-bound declared observations. Missing or stale
   evidence remains Unknown. It neither probes files nor certifies media; actual
   inspection and tools remain with the existing modality owner.
4. Add explicit Reflexion to Workflow Self-Improvement: scoped error, cause
   hypothesis, successfully tested correction, exclusions and separate adoption.
   The blank template remains NOT_RUN/proposed. No hidden learning, client data
   in the shared package, automatic persistence or instruction rewrite.
5. Add a genuine official-GEPA adapter and a bounded development pilot, outside
   the runtime package. It exposes only `Relevant examples` in the shared quality
   reference, retains protected sentences, and never writes source. A candidate
   is a proposal requiring holdout, regressions and actual owner review.

## Local helper

Inside the plugin, the following reads a synthetic plan record only:

```bash
node scripts/quality-harness.mjs check skills/output-critic-iteration/assets/quality-review.example.json
```

`retrieve` accepts `{bank, query, limit}` with domain/stage/problem_tags/required_locks.
`pair` accepts two candidate IDs/revisions, required hard gates, criterion/anchor
IDs and verdicts with explicit A/B order. `lesson` validates tested, scoped records;
it performs no storage or adoption. Chat-only hosts use the same policy without
pretending the script ran. PASS is scoped declared-record agreement.

## GEPA pilot

The optional dependency is pinned to official GEPA commit
`3f160c295000dd31db3d438c3d17553c23cc5f81` (source version 0.1.4, checked 2026-10-01).
No provider SDK/key or mandatory runtime dependency is introduced.

```bash
python3 -m venv /tmp/studio-gepa
/tmp/studio-gepa/bin/pip install --no-deps -r requirements-gepa-pilot.txt
/tmp/studio-gepa/bin/python scripts/gepa_studio_pilot.py --output /tmp/studio-gepa-offline-report.json
```

The default run uses the actual GEPA engine with deliberately artificial local
callbacks. Its metric checks an offline marker; any increase proves adapter
plumbing only. It does not demonstrate better prompts, actual model behavior or
creative quality. Candidate text is saved only in a separate report, never
adopted into the plugin. Offline limits: 24 optimizer metric calls, 40 total task
calls including holdout, three proposal calls, 30 seconds and USD 0. Calls are
serial. Source equality is rechecked after selection. Holdout never enters
reflective feedback; duplicate case IDs/input leakage are rejected.

Real optimization is exposed through `run_pilot` with explicitly injected task
and proposer callbacks. The CLI supports offline mode only. An external run
needs actual owner authorization for provider/model/data, positive total and
worst-case per-call cost caps, call/time limits and an approval evidence ID.
The adapter reserves budget before each call and rejects invalid spend reports.
Callbacks must enforce transport timeouts and their declared per-call cost caps;
the wall-clock gate stops between calls and cannot interrupt a hung callback.
No callback is preconfigured and no external model invocation was authorized by
the five-direction implementation request. Do not manufacture approval in config.

The task callback executes the candidate on only the scenario's `input`, then
independently returns `score`, all named `hard_gates`, a concise sanitized
`feedback` and actual `cost_usd`. Do not pass expected verdicts or holdout to
the model/proposer, and never return private context or raw reasoning as feedback.
The proposer returns section `text` and `cost_usd`. Raw task outputs are discarded;
reflection uses bounded case IDs, hard-gate results and sanitized error summaries.
Unknown/missing hard evidence cannot count as success.

After a real run, review the candidate against untouched holdout, source regression
checks and bounded blind pairwise comparisons with the baseline. Record actual
owner preference and any judge disagreement. No gain or protected regression
means keep the baseline. Meaningful instruction changes require the owner's
explicit approval before a separate precise patch. Rollback is a selective revert
of the adopted section and its necessary dependencies, never a broad reset.

## Verification boundaries

Use serial Node checks, installer tests and optional GEPA tests. Source/record
checks, official-engine offline integration, fresh text exercises, GitHub source,
saved plugin readback, active-client behavior and media quality are distinct.
The 183 historical planned cases remain planned; no executed score is inferred
from fixture existence. Record actual checks and publication IDs in the external
release reports, not within the runtime package. Preserve welcome/menu assets,
all 37 IDs/display names, exact starters/logo, onboarding, upstream snapshots
and the initial-review-plus-two-repairs budget.

Sources and application limits are in the shared quality reference. These are
conditional tools for relevant decisions and evidenced errors, not extra work
at every request. Stop when the stated acceptance criteria are met.
