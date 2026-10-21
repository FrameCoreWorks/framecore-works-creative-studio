# AGENTS.md history

Sections moved out of [AGENTS.md](../AGENTS.md) on 2026-10-21 (change CC-20261021-01) when its rules were consolidated, kept word for word. They are superseded by, or folded into, the current rules there; read them for context, not as instructions. A completed task section authorized only that task.

## Owner-directed account-free Adobe knowledge (2026-10-21)

The owner explicitly authorizes integrating useful Adobe-derived methods as skills/knowledge without Adobe accounts or services. Follow [the bounded scope](adobe-account-free-2026-10-21.md), preserve existing owners and the full FrameCut storyboard gate, and release repository first, then the same hosted plugin with its private overlay. The full upstream suite is excluded from installation under this profile; this restriction supersedes the generic extension-install convention for this source. No unrelated development is reopened.

## Owner-directed supplemental knowledge (2026-10-21)

The owner explicitly requests integrating the conclusions of the supplied Motion/Dashboards and Taste articles as supplementary Studio knowledge. Follow [the bounded packet](creative-knowledge-2026-10-21.md), existing owners and conditional references. This authorizes the knowledge update and its repository-first paired release, not a dashboard backend, new review UI, native Claude connection or unrelated feature round. Preserve the complete FrameCut board gate and private hosted overlay.

## Owner-directed FrameCut development (2026-10-21)

The owner's explicit follow-up reopens development for the six recommended Concat-inspired FrameCut capabilities and their orchestration. Follow [the bounded scope](framecut/concat-development-scope.md): implement original native editing, composited storyboards, jobs, keyframes/framing, freeze/speed and versioned effects. Preserve onboarding, full-board feedback/acceptance before final and optional requested samples. Publish verified source first, then update the existing hosted plugin with its current private overlay preserved. This supersedes the pause only for this task; unrelated development remains paused.

## Owner testing pause (2026-10-21)

The owner paused development after 1.115.0 to test FrameCut, Motion Graphics and other Studio modules in actual use. The current task is the [handover to Claude Code](handover-chatgpt-work-2026-10-21.md), covering ChatGPT Work's 2026-10-20 to 2026-10-21 work. Do not resume older work orders, expand features or run a new development round merely because they appear below or in historical handovers. Wait for the owner's findings or a new explicit task, then address the concrete trigger. This documentation-only handover leaves the shared package and saved plugin unchanged.

## Current owner instruction (2026-10-20)

Work directly on `main`; do not create local or remote working branches. After the required checks pass, commit and fast-forward push the completed changes to `main`. This supersedes the older working-branch guidance below. Preserve concurrent work and never force-push.

This development thread owns repository fixes and sandbox testing. A separate owner-directed thread owns permanent supplemental tool integrations in the private hosted plugin. For each shared-package release, update the existing hosted plugin with Plugin Creator when available, using its current release guard and preserving those integrations. Read back the affected files. The hosted version can be newer than the public source version because of its private overlay; record both versions and the actual comparison scope. Do not publish private overlay files or settings to this repository. These instructions supersede the historical `not_tracked` and whole-package equality rules below. Source checks, saved files and fresh-client behavior remain separate evidence.

## Branch hygiene (owner decision 2026-10-19)

Applies to every surface that writes to this repository: Claude Code (local and cloud), Codex (local and cloud) and ChatGPT Work. The owner deleted 80 accumulated remote branches on 2026-10-19; keep the remote at `main`, `gh-pages` and active session branches only.

- Develop on a local working branch (for Cloud Code `cloud-code/<change-id>-<short-scope>`, for Codex `codex/<change-id>-<short-scope>`) and do not push it. Integrate by fast-forwarding `main` after the checks pass: `python3 scripts/release.py prepare|publish ... --push` for a release, `git push origin HEAD:main` for a change that does not touch the shared package.
- Push a working branch only to open a pull request; the repository deletes the head branch after the merge.
- A branch the host itself requires (a Claude Code cloud `ccr-*` branch, a Codex cloud task branch, a ChatGPT Work branch) is the one exception: push only that branch, keep it equal to `main`, and name it in `STUDIO_RELEASE_BRANCHES` so `release.py` updates it. `release.py` never pushes the local working branch.
- Never create a remote branch per release or per change. Never delete `main` or `gh-pages` (`gh-pages` serves the motion player). Never delete a branch another surface is using without the owner; deleting branches is the owner's step.
- Before ending a task, run `git ls-remote --heads origin`. Anything beyond `main`, `gh-pages` and your own session branch goes in your report to the owner, with whether it is merged into `main`.

## Paired GitHub and ChatGPT updates: superseded paragraphs

Owner decision 2026-10-09: the owner performs the hosted ChatGPT Work update himself in Plugin Creator; a session without Plugin Creator access cannot do it. After every release that changes the shared package, do not ask whether to update the hosted plugin. Report the hosted state as pending and give the ready, standalone update prompt based on `CHATGPT_UPDATE.md` (source commit, readback fields). Plugin Creator reads the declared files from the repository at that commit through `config/install-sources.json`, not the release ZIP; the ZIP SHA-256 is reference only (owner correction 2026-10-10). When the owner returns the readback JSON, compare it with `scripts/check_hosted_readback.py` and record the result.

Owner decision 2026-10-10: hosted readback verification is stopped. After a release, give only the short Plugin Creator update prompt (source commit, no readback file), do not ask for or compare a readback or diff, and record ChatGPT Work as `not_tracked`; the owner tests the plugin himself and reports problems. This supersedes the readback steps above and in the paired-update section; `scripts/check_hosted_readback.py` stays available if the owner sends a readback on his own.

## Development provenance: superseded branch sentence

Treat `main` as protected even without GitHub enforcement. Develop on a local working branch, for Cloud Code `cloud-code/<change-id>-<short-scope>` with change ID `CC-YYYYMMDD-NN`, and integrate through review unless the owner decides otherwise; the branch stays local (see Branch hygiene).
