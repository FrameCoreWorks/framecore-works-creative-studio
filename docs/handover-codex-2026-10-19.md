# Handover for Codex, 2026-10-19 (package 1.94.0)

For a Codex session that continues or checks the work after the full audit. Read [AGENTS.md](../AGENTS.md), this note, the [audit](reviews/full-audit-2026-10-19.md), the latest entries of the [development ledger](development-ledger.md) and `git log -15` before writing.

## State

- `main` carries 1.94.0 (audit fixes) on top of 1.91.0 (huashu-art-motion and Iso Glow, welcome option 4), 1.92.0 (Open Design) and 1.93.0 (anti-slop). All were released with `scripts/release.py` by Cloud Code and published to GitHub; ChatGPT Work is `not_tracked`; Codex sync is `not_run`.
- No host test has run on 1.91.0 to 1.94.0 (owner decision 2026-10-19). Source checks pass; they are not host behavior.

## Where the added knowledge lives and who uses it

| Knowledge (source, licence) | Files | Loaded by |
| --- | --- | --- |
| Craft rules: type, colour, interface patterns, liveliness, honest content, responsive layout (Open Design Apache-2.0, anti-slop MIT) | `skills/pipeline-core/references/craft-rules.md` | Static Graphic Design Creator, Motion Graphics, Output Critic, Pipeline Core, routing boundaries |
| Craft lint and WCAG contrast | `skills/pipeline-core/assets/craft-lint/` (`craft_lint.py`, `contrast_check.py`) | the same owners; Output Critic for contrast |
| DESIGN.md export and import | `skills/pipeline-core/assets/design-md/` | static owner, Delivery Documentation, brand identity profile |
| Reviewed prompt examples (87 records) | `skills/pipeline-core/assets/prompt-examples/` | Image and Video Prompt Architects, static owner (after the idea, before a web search) |
| AI writing patterns, EN and PL | `skills/copy-voice/references/ai-writing-patterns.md`, `skills/copy-voice/scripts/ai_writing_check.py` | Copy Voice, Humanizer, output review (loop protocol) |
| Art-style and explainer motion direction (huashu-art-motion) | `skills/hyperframes-workflow/references/art-and-explainer-motion-direction.md`, `assets/reference-breakdown/` | Motion Graphics; routing boundaries for reference animations |
| Iso Glow (MIT) | `skills/hyperframes-workflow/assets/iso-glow/`, `assets/motion-sync/audio_envelope.py` | Motion Graphics |
| Lyric timing | `skills/hyperframes-workflow/assets/motion-sync/lyric_timing.py` | Motion Graphics, Caption Studio, Creative Music Video Director |
| Recommended repositories (welcome option 4) | `skills/workflow-orchestrator/assets/extensions/` and `references/extensions.md` | orchestrator |

`tests/knowledge_wiring_test.py` holds this map as data; a missing link fails the suite.

## How to extend without breaking it

1. **A new outside repository.** Review it at a pinned commit; restate its rules in Studio's own English text in the owning reference (no copied skill files); keep its licence in an `integrations/<name>/` folder with a decision map; add a registry entry in `extensions.json` with a category, pins and per-host status. Hosts that cannot install it get `manual` or `not_supported` with a reason.
2. **A new tool.** Put it under its owner's `assets/` or `scripts/`, standard library first; add a test under `plugins/framecore-work-creative-studio/tests/` and its line in `scripts/check_all.sh`; add a capability card entry (requirements only from `requirement_values`); for an owner of motion, captions or Remotion, add the runtime-map row (`motion_variants_test` checks it).
3. **Wire it.** Link it from the SKILL.md of every owner that must use it and from the routing row or routing-boundaries rule a request lands on; add a row to `tests/knowledge_wiring_test.py`; add a host-eval case to `tests/host-evals/additions.json` (status `not_run`).
4. **Budgets.** Orchestrator SKILL.md at most 32,000 bytes (31,7xx now); skill descriptions 7,800 characters in total (7,699 now). Put detail in references, not in the routing table.
5. **Never** delete, rename or move a path in the shared package (hosted updates cannot delete); retire a file with a stub. Keep the startup welcome byte-identical to its assets; option 4 is part of it since 1.91.0.

## Release procedure (what Cloud Code ran)

```sh
find . -name __pycache__ -prune -exec rm -rf {} +
python3 -B scripts/build_install_manifest.py
node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs
bash scripts/check_all.sh --fast           # the release runs the full list
python3 scripts/release.py prepare X.Y.Z --change-id CC-YYYYMMDD-NN --title ... --changelog FILE --notes FILE --summary ... --push
python3 scripts/release.py publish X.Y.Z --change-id CC-YYYYMMDD-NN --push
```

The notes file starts with `# Creative Studio X.Y.Z`. `release.py` writes the records, the ledger entry and the trailers, refuses a dirty tree and refuses to push when `origin/main` moved. A Codex release uses its own origin and the `Origin-Agent: codex` trailer.

## Open decisions and suggested next work

- Owner decision: an optional tier in the environment check for faster-whisper, yt-dlp and pikepdf (now not listed because every listed tool is required).
- Done 2026-10-19: the owner deleted the 80 merged or superseded remote branches by hand; the remote keeps `main`, `gh-pages` and the active session branch, and the repository deletes head branches after a merged pull request. `release.py --push` now pushes `main` and only the branches named in `STUDIO_RELEASE_BRANCHES`, never the local working branch, so releases no longer leave remote branches. Develop on a local working branch; push it only for a pull request.
- Run `python3 scripts/host_eval.py --suite additions` when the owner allows paid runs (budget under USD 1 for a gate subset), and record cost.
- Split the Motion Graphics "Deliver the video" section into host route, a look-by-brief table and review.
- Small items listed at the end of the audit.

## What a Codex check should verify

- `git log` shows each change with `Origin-Agent`, `Change-ID`, `Baseline-SHA`, `Shared-Package-Changed`, `ChatGPT-Work-Sync` and `Codex-Sync` trailers.
- Validator PASS, `bash scripts/check_all.sh` PASS on a clean checkout.
- In Codex, a bare Studio invocation shows the full welcome with option 4 in the user's language; "4" lists the recommended repositories with Codex install status from `extensions.py catalog --host codex`.
- A request for a landing mockup loads Static Graphic Design Creator and the craft rules; a lyric-video request loads Motion Graphics and lyric timing.
