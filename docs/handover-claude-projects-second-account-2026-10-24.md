# Handover: Claude Projects coordinator on the owner's second account, 2026-10-24

For the owner's second Claude account, which runs this same project as a Claude Projects coordinator. Read [AGENTS.md](../AGENTS.md) first; where this note and the owner's project instructions differ from AGENTS.md, the owner's newer instructions win (they are listed below). Earlier context: [handover-claude-code-2026-10-23.md](handover-claude-code-2026-10-23.md) and [handover-development-proposals-2026-10-24.md](handover-development-proposals-2026-10-24.md).

## Working rules (owner, 2026-10-24)

1. At most 2–3 working threads at once. The coordinator makes sure their changes fit together.
2. Push **only `main`** to GitHub (trunk-based). No thread or session branches on the remote; a local branch inside a session is fine. This overrides the AGENTS.md rule 2 exception for host branches.
3. One change at a time reaches `main`. Fetch the latest `main` before starting; rebase and run the full checks before pushing.
4. Threads that touch the same files or release a plugin version never run in parallel; the second waits until the first has pushed and reported its SHA to the coordinator.
5. Do not wait for the owner's manual tests in ChatGPT, Work or Claude. Repo checks are enough; record untested client or engine behaviour as `NOT_RUN`. Leave the ChatGPT update prompt in a file (`CHATGPT_UPDATE.md` or the release notes) and keep going.
6. Make small design decisions with a sensible default and record it; ask the owner only about risky or irreversible steps.
7. Use the **Superpowers** plugin for all repo work (brainstorming, plans, TDD, code review, verification before claiming success).
8. Use the other installed plugins when they fit: **context7** (current library docs), **playwright** (browser tests, for example the motion player on `gh-pages`), **plugin-dev** (building and validating Studio plugins and skills), **claude-md-management** (keeping AGENTS.md and CLAUDE.md concise). In Claude Code cloud containers context7 currently fails to connect (the agent proxy refuses `mcp.context7.com`); fall back to the library's own docs through web search or fetch.
9. Reply to the owner in Polish. Repository files stay in English (AGENTS.md).

## State on 2026-10-24

- **Studio 1.127.0:** skill display-name rename (owner-approved list).
- **Studio 1.128.0** (tag `v1.128.0` = `35af152`, publication record `2acb34d`): new public companion plugin **voice-narration** (`plugins/voice-narration`, skill `voice-narration:narrate`): VoxCPM2 or Voicebox on the user's own computer, ElevenLabs through the host connector. **voice-narration 1.0.1** (review minors) is on `main` at `4bf66c3`. Real engine generation and the ElevenLabs read: `NOT_RUN`.
- **Studio 1.129.0:** Opus gallery, all 703 entries brought in as technique only, used by motion graphics only. Known gap: the storyboard step checks the gallery too late.
- **Studio 1.130.0** (`main` at `ccf925d` before this note): Studio searches skills.sh during a task when no Studio skill or recommended extension covers a need, offers up to three audited candidates once per need, and uses a listed skill once (method only) or installs it on consent. A live skills.sh search: `NOT_RUN`.
- **Studio 1.131.0** (release `2f50e07`, tag `v1.131.0`, publication record `f3f612a`): new public companion plugin **brand-kit** (`plugins/brand-kit`, skill `brand-kit:brand`): a company website becomes evidence, a draft kit in Studio's brand kit schema, a brand audit with voice and messaging, revisions per brand and a direction menu. Audit and direction steps in a real host conversation: `NOT_RUN`.
- **Studio 1.132.0** (release `e595120`, tag `v1.132.0`, publication record `7ff580f`): fixes from the owner's [full review](reviews/full-review-2026-10-24.md) (0 critical, 11 important, 19 minor; fix status at its end), with **voice-narration 1.0.2**, **brand-kit 1.0.1** and **earshot-audio 1.0.8**. `check_version_bump.py` now also guards companion plugins; `release.py` pushes only `main`; AGENTS.md current rules are consolidated 2026-10-24.
- **Studio 1.133.0** (CC-20261024-15): opt-in startup style. First configuration asks once: `guided` (default, complete welcome and menus) or `workflow` (one ready line on a bare invocation, "menu" gives the full welcome). Saved as `work_preferences.startup_style` only with consent through a real per-user mechanism; see the `## Startup style` section of `workflow-orchestrator/references/startup-and-creative-menus.md`. Host cases ST01 and ST02 in `tests/host-evals/additions.json`.
  - Kept by decision (minor 2, 5, 6): Claude Code's skill-listing truncation is a host budget, not a repository defect; dependency ranges stay unpinned apart from the engines; Earshot's `exec` runs the user's own scripts by design.
  - Deferred (minor 19): tests for the guard branches of `scripts/publish_github_release.py` (ambiguous release, tag on another commit, partial upload).
- **Hosted ChatGPT plugin:** `pending` for 1.127.0 to 1.133.0; one update to 1.133.0 covers them all (Plugin Creator writes the whole declared inventory). Prompt: `CHATGPT_UPDATE.md` and the project file `startup-style/chatgpt-update-1.133.0.txt`. The owner runs it with Plugin Creator when convenient.
- Plugins the owner installed on claude.ai: Superpowers, context7, playwright, plugin-dev, claude-md-management. The skills.sh `handoff` skill is not installed.

## In flight

1. **Brand kit from a website:** done in 1.131.0 (see above); out of its MVP: pixel sampling, competitor analysis, a hosted ChatGPT package.
2. **Known follow-up:** make the storyboard step consult the Opus gallery earlier (gap noted in 1.129.0).

## Suggested project instructions (paste into the second account's project)

```text
Zasady pracy (od Kamila):
- Maksymalnie 2-3 wątki robocze naraz. Koordynator pilnuje, żeby ich zmiany się spinały.
- Na GitHub wypychamy wyłącznie main (trunk-based). Nie wypychaj własnych gałęzi na zdalne repo; lokalna gałąź w sesji jest w porządku. Jedna zmiana naraz trafia do main; przed startem pobierz najnowszy main, a przed wypchnięciem zrób rebase i pełne testy.
- Wątki dotykające tych samych plików lub wydające wersję pluginu nie działają równolegle; drugi czeka, aż pierwszy wypchnie i zgłosi SHA koordynatorowi.
- Nie czekaj na ręczne testy Kamila w ChatGPT, Work ani Claude. Wystarczą testy repo. Prompt aktualizacji dla ChatGPT zostaw w pliku i jedź dalej; nie blokuj pracy na zwrotkę od Kamila.
- Drobne decyzje projektowe podejmuj sam rozsądnym domyślnym wyborem i zapisz go; pytaj tylko o rzeczy ryzykowne lub nieodwracalne.
- Używaj pluginu Superpowers do całej pracy nad repo (brainstorming, plany, TDD, code review, weryfikacja przed ogłoszeniem sukcesu).
- Używaj też pluginów, gdy pasują do zadania: context7 (aktualna dokumentacja bibliotek), playwright (testy w przeglądarce, np. odtwarzacz na gh-pages), plugin-dev (budowa i walidacja pluginów i skilli Studia), claude-md-management (utrzymanie AGENTS.md i CLAUDE.md zwięzłymi).
- Na start przeczytaj docs/handover-claude-projects-second-account-2026-10-24.md i najnowszy docs/handover-*.md.
- Odpowiadaj po polsku.
```

## Handing work between accounts

Both accounts work on the same `main`. Before starting, fetch `main` and read the newest `docs/handover-*.md` and the top of `docs/development-ledger.md`. When a thread stops before finishing, leave a short `docs/handover-*.md` (state, evidence, what is left, the next step) and push it on `main`, so the other account can continue without asking the owner again. Never run a release on both accounts at the same time.
