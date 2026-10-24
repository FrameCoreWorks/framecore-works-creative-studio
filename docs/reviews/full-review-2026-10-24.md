# Full repository and plugin review, 2026-10-24

Requested by the owner after the Brand Kit release: an A-to-Z review of the repository and all four plugins (Studio, Earshot Audio, Voice And Narration, Brand Kit). **Review only; nothing was fixed in this step.** Each finding says, in plain words, why it matters.

- Baseline: `main` at `f3f612a` (Studio 1.131.0; the only change since the release commit `2f50e07` is the publication record).
- Method: Superpowers review with five independent reviewers (orchestration and core skills; video and motion skills; visual, copy, strategy and audio skills; companion plugins with the plugin-dev validator; infrastructure, CI, docs and AGENTS.md with claude-md-improver criteria), then the lead reviewer re-checked every important finding in the source.
- Checks run: `bash scripts/check_all.sh` passed (exit 0, no failures); companion plugin tests earshot-audio 28/28, voice-narration 60/60, brand-kit 52/52 pass.
- Not run: real host conversations (ChatGPT, Work, Codex, Claude), real media generation, a built repository ZIP measurement.

## Summary

No critical defect was found: nothing breaks installation, startup or a release today. About 400 relative links in the 37 Studio skills resolve, every routing target exists, all `agents/openai.yaml` files are present and all manifests agree on versions. The weak spots are around the edges: the three newer companion plugins are not covered by the release and documentation machinery that Studio has, a few texts and one script assume Polish, and the skill budgets are almost full.

| Priority | Count |
|---|---|
| Critical | 0 |
| Important | 11 |
| Minor | 19 |

## Important

1. **Companion plugins have no version guard or release flow.** `scripts/check_version_bump.py` hard-codes the Studio package; `release.yml`, `release.py` and `package_release.py` only know Studio. Brand Kit, Voice And Narration and Earshot Audio can change on `main` without a new version, tag or ZIP. *Why it matters:* a user's Claude cannot tell an old copy from a new one, so a fix may never reach them.
2. **Install guides and README do not mention Brand Kit or Voice And Narration.** `README.md`, `CLAUDE_INSTALL.md`, `CODEX_INSTALL.md`, `CHATGPT_INSTALL.md` and `INSTALL.md` cover only Superpowers and Earshot, while the marketplace lists four plugins. *Why it matters:* users and agents cannot find two of the four shipped plugins by the documented path.
3. **Voice And Narration registry pin is stale.** `workflow-orchestrator/assets/extensions/extensions.json` pins `397c9eba` (voice-narration 1.0.0, "48 launcher tests"); the shipped plugin is 1.0.1 with fixes in `runtime.py`, `formats.py`, `audio.py` and `voicebox.py` and 60 tests. *Why it matters:* Studio's "install from the pinned commit" steps give users the older, buggier version.
4. **Brand Kit's private-address guard can be bypassed by DNS rebinding.** `plugins/brand-kit/scripts/site_fetch.py:22-62, 140-153` checks the resolved address, then `urlopen` resolves the name again. *Why it matters:* a hostile site could make the tool read a page from the user's own network or a cloud metadata address and save it into `evidence.json`, which the plugin promises not to do. Low likelihood, but it is a stated safety promise.
5. **Storyboard sheets rewrite the user's on-screen text in Polish style.** `storyboard-board-architect/scripts/board_compose.py:111` wraps every super in „…” and `keep_together` (`:26`, `:33`) applies Polish non-breaking-space rules; the "Audio"/"Super" labels are fixed English. *Why it matters:* an English or German board shows quotes and spacing the user never wrote, which breaks Studio's exact-copy rule.
6. **The ad-script owner's description does not mention ad scripts.** `screenplay-story-architect/SKILL.md:3` lists stories and screenplays only, though its body (`:19`) and the orchestrator route "ad script" there. *Why it matters:* when a host picks a skill by description alone, a 30-second ad script request can land in Copy Voice and return a copy pack instead of a two-column AV script.
7. **Large test archives ship in every repository ZIP.** `verification/` is about 499 MB tracked, mostly `verification/host-evals/candidates/` ZIPs of about 18 MB each; `EXCLUDED_DIRS` in `scripts/build_install_manifest.py:16` does not exclude them. *Why it matters:* slow clones and huge release downloads with no value for users.
8. **`check_all.sh` hides the validator's error text.** `scripts/check_all.sh:12` sends `validate-studio.mjs` output to `/dev/null`. *Why it matters:* when a release or CI run goes red, nobody sees why without rerunning by hand.
9. **AGENTS.md contradicts the owner's current branch rule.** Rule 2 still invites pushing a host session branch and naming it in `STUDIO_RELEASE_BRANCHES`, and `scripts/release.py:39, 302-306` still pushes `SESSION_BRANCHES`; the owner now allows pushing only `main`. *Why it matters:* an agent following AGENTS.md can create the remote branch sprawl the owner banned.
10. **AGENTS.md rule 1 and "Maintenance mode" describe a pause that is no longer true.** They say development paused after 1.115.0 and that nothing further is authorized, yet 1.119.0 to 1.131.0 shipped owner-opened work. *Why it matters:* a new agent may refuse reasonable owner requests or misjudge what is allowed.
11. **`docs/roadmap.md` is four releases out of date.** It says "1.122.0, 37 skills, 1,552 files" and does not mention the skill finder, Opus gallery, Voice or Brand Kit; AGENTS.md tells every agent to read it first. *Why it matters:* every new session starts from a wrong picture of the project.

## Minor

1. Stray scratch scripts `edit2.py`, `edit3.py`, `edit4.py` are tracked at the repository root (commit `4f5caa4`) and ship in the ZIP; run from the plugin folder they would rewrite skill text. *Why:* an agent may mistake them for tools.
2. The Studio skill list in Claude Code can lose descriptions. In this review session, with many plugins installed, Claude Code listed `tool-routing-cost`, `ugc`, `video-prompt-architect` and `workflow-orchestrator` with empty descriptions (the host's listing budget ran out alphabetically). *Why:* without a description the model may not pick the entry skill. Host-dependent; worth a host check before adding more description text.
3. `voice-narration/scripts/runtime.py:421` defaults `--language` to `pl` and the skill example hard-codes `--language pl`. *Why:* a non-Polish user on the Voicebox route can silently get Polish speech.
4. `earshot-audio/scripts/runtime.py:121` downloads the fallback archive with no timeout. *Why:* a stalled connection hangs the install forever (the source is still hash-checked).
5. Earshot and Voice install dependencies with `>=` ranges and Voice upgrades pip. *Why:* a future dependency release can break an install that worked yesterday (recorded as a deliberate decision in voice-narration 1.0.1).
6. `earshot-audio` `exec` only filters `-m earshot`; `exec -c` runs any Python. *Why:* the "allowlist of local commands" wording is wider than the code.
7. Marketplace descriptions of the three companions differ from their own manifest descriptions. *Why:* two texts to keep in step.
8. `opencut-video-studio/SKILL.md:50` gives a Polish acceptance question without "in the user's language". *Why:* a model may copy Polish to an English user.
9. `delivery-documentation` client handoff and acceptance templates and `copy-voice/assets/client-emails.pl.md` exist only in Polish, with Polish legal terms, and nothing says to adapt them. *Why:* a non-Polish client can get a Polish legal template.
10. `copy-voice/SKILL.md:23-24` and its `openai.yaml` default prompt still offer "polish", which Humanizer owns. *Why:* a bare "polish this" has two owners.
11. `marketing/SKILL.md:34, 45, 57` lists ecommerce, marketplace and offer framing although the description excludes commerce goals. *Why:* a store campaign can get a second, competing plan.
12. `delivery-documentation` ships the project manifest tools while its description says the file inventory belongs to Asset Manifest. *Why:* an inventory request has two plausible owners.
13. `commercial-video-campaign-director/SKILL.md:26` also claims the shared visual system that Visual Campaign owns. *Why:* format-adaptation requests can go either way.
14. Both `storyboard-sequence-architect` and `hyperframes-workflow` define the motion storyboard for coded video, with no stated winner. *Why:* two different storyboards for one film.
15. `remotion-video-production/SKILL.md:120-122` places the FrameCut handoff inside the QA checklist heading. *Why:* the return contract is easy to miss.
16. `video-prompt-architect/SKILL.md:131` says to research "for every substantive video task", against the conditional gate at `:12`. *Why:* unnecessary searches and cost.
17. `screenplay-story-architect/SKILL.md:19` names `vo_budget.py` without a path (it lives in `copy-voice/scripts/`). *Why:* the model cannot find the script from this skill.
18. `brief-architect/SKILL.md:88` hands off to `reference-curator` (a role ID) instead of the skill `reference-pack-curator`; `pipeline-core/SKILL.md:17, 36-41` and `startup-and-creative-menus.md:3` name ChatGPT and Codex but not Claude Code. *Why:* Claude Code may look for a skill that does not exist or treat the contract as not applying.
19. Release tooling gaps: `release.yml` fires on any `plugin.json` edit and then fails noisily; `check_version_bump.py` and `publish_github_release.py` guard branches have no tests; `.gitignore` lacks `*.zip.tmp`, `.venv/`. `research-evidence/SKILL.md:35` keeps eval-fixture notes in the runtime text. *Why:* noise and context cost rather than wrong results.

## Room for new skills and richer references

The owner asked whether there is room for more skills or for deeper reference material. Measured on `f3f612a`:

| Budget | Used | Limit | Left |
|---|---|---|---|
| Studio skill descriptions, total | 7,495 chars | 7,800 (warning from 7,500) | about 300 chars |
| `workflow-orchestrator/SKILL.md` | 31,726 bytes | 32,000 | 274 bytes |
| Orchestrator description | 446 chars | 450 | 4 chars |
| `hyperframes-workflow/SKILL.md` | 31,965 bytes | no enforced limit | (largest skill) |

**New Studio skills: not recommended now.** One new skill needs about 180 to 220 description characters plus a routing row in the orchestrator; that uses the whole remaining budget for one skill, and minor finding 2 shows the host listing is already tight. Two better routes:

1. *Companion plugins* (like Voice and Brand Kit) carry their own budgets and do not touch Studio's. Ideas already on the owner's list: localization, publishing and scheduling, stock and licence checks.
2. *References inside existing skills* cost nothing in the description budget, because a model reads them only when the skill links them. This is the cheapest way to deepen Studio.

**Where new references would help most** (each needs the owner's go-ahead as a bounded task, since maintenance mode asks for a trigger; no ready-made idea lists, only method):

| Priority | Skill | Today | Suggested reference | Why |
|---|---|---|---|---|
| 1 | `cinematography` | no references | lens, shot-size, movement and lighting decision cards | Called by most video owners; today everything sits in a 6 KB SKILL.md |
| 2 | `caption-studio` | 1 reference | dated platform specs card (safe zones, sizes, caption limits per platform) | Platform facts go stale; a dated card is easy to refresh |
| 3 | `ugc` | 1 reference | dated disclosure and branded-content rules per platform | Paid-social risk; rules change |
| 4 | `delivery-documentation`, `copy-voice` | Polish-only templates | English source versions with "adapt to local law" notes | Fixes minor finding 9 and serves non-Polish users |
| 5 | `marketing` | no references | positioning and audience research method (questions, evidence ledger) | Strategy is the input for every campaign |
| 6 | `creative-video-producer` | no references | production schedule, budget and approval-gate templates | The coordinator of multi-stage video has no worksheet |
| 7 | `storytelling`, `character-design` | 1 to 2 references | structure diagnostics and continuity checklists | Supports longer narrative work |

## Suggested order of fixes

1. Release safety for companions (important 1, 3) and the docs that tell users they exist (2).
2. Correctness for non-Polish users (important 5, minor 3, 8, 9).
3. Rules agents read first (important 9, 10, 11) and `check_all.sh` output (8).
4. Brand Kit DNS pinning (4) and repository size (7).
5. Routing wording (important 6, minor 10 to 18), batched into one Studio release.

## Evidence

- `bash scripts/check_all.sh` on `f3f612a`: exit 0; Node 242 tests (231 pass, 11 opt-in browser tests skipped), every Python suite OK, no failures.
- Reviewer coverage: about 210 links in the orchestration group, about 270 in the video group and every link in the visual, copy and audio group were resolved; route targets, role IDs and gate names were matched to `role-skill-map.md` and `gate-registry.md`.
- Re-checked by the lead reviewer: important 1, 3, 5, 6, 7, 8, 11 and minor 1, 3 in the source.

## Fix status (1.132.0, 2026-10-24)

The owner asked to fix every finding. Released in Studio 1.132.0 with Voice And Narration 1.0.2, Brand Kit 1.0.1 and Earshot Audio 1.0.8.

- **Fixed, important:** 1 (companion version guard in `check_version_bump.py`, with tests; companions ship in Studio's tagged releases and the marketplace), 2, 3, 4, 5, 6, 7 (repository ZIP only; the snapshots stay in Git as evidence), 8, 9, 10, 11.
- **Fixed, minor:** 1, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, and from 19 the release workflow gate, `.gitignore` and the fixture paragraph (moved to `docs/host-evals.md`).
- **Kept by decision, no change:** minor 2 (a host listing budget, nothing in the repository to fix; descriptions stay within Studio's own budget), minor 5 (recorded in voice-narration 1.0.1: only the engine is pinned), minor 6 (`exec` running the user's own scripts in the venv is the documented use; the allowlist covers `run` and `-m earshot`).
- **Done in 1.134.0:** from minor 19, tests for the guard branches of `publish_github_release.py` (`tests/test_publish_release.py`), and reference recommendation 1 (Cinematography decision cards).
