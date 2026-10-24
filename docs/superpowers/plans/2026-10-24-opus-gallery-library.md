# Opus 5.5 gallery in the motion prompt library: implementation plan

Owner task 2026-10-24 (Kamil): Studio should draw on [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) in its video workflow so the skills actually know to use it. Owner decisions the same day: the gallery supplies technique after the idea is chosen from the brief, never the idea (the 2026-10-11 rule stands); all 703 entries go in, not a curated subset; no manual ChatGPT startup test is required for this change. The owner-facing plan is the Claude Doc "Plan: galeria Opus 5.5 w FrameCore Works Creative Studio".

**Goal:** every coded-motion owner reaches the 703 gallery records through the existing motion prompt library, with a Studio-written mechanism note per record, a link to the creator and a pinned prompt URL, and without redistributing creator prompt text.

**Source:** commit `92aee2f586ac0715cb3cbcb6384834f98a33383d` (2026-10-13). The repository's MIT licence covers the compilation; its Credits section says every video and prompt belongs to its creator. Records are therefore `creator_prompt_link_only` with `prompt_text: null`.

**Exclusions:** no new skill, menu, runtime, provider, download of media, or change to `workflow-orchestrator/SKILL.md` (byte budget). No path is deleted, renamed or moved.

## Tasks

1. **Failing tests** in `tests/motion-quality.test.mjs`: the gallery shard loads 703 link-only records; each has a mechanism note, a prompt URL pinned to the commit, valid brief types; a brief view lists at most three gallery records; interactive records stay out of default search; tampered records fail validation.
2. **Library code** in `motion-prompt-library/library.mjs`: validate gallery fields, check `brief_types` against the brief index, add `gallery` to `presentBrief`, search the mechanism note, show the mechanism and the prompt URL.
3. **Build script** `scripts/build_opus_gallery_shard.py` (repository only): reads a pinned checkout plus the Studio notes file `scripts/data/opus-gallery-notes.json`, writes `specimen-opus-gallery.json`, and with `--check` reports new, changed and missing upstream slugs. Removed upstream entries are kept and marked `retired`.
4. **Notes:** one original sentence per entry (what happens on screen and the technique), written from the prompt text; `brief_types` from the existing 19 brief ids. Three entries whose prompts carry shell or credential instructions get a `caution`.
5. **Knowledge and routing:** `SOURCE-NOTICE.md` and the library README describe the gallery; a prompt-structure section in `references/claude-code-reels.md`; short hooks in `hyperframes-workflow/SKILL.md` and `remotion-video-production/SKILL.md`; `knowledge_wiring_test.py` rows; `motion-quality-research.md` points to the shard; registry entry `awesome-opus-videos`.
6. **Checks and release:** canonical validator, `bash scripts/check_all.sh`, at most five headless cases, ledger entry, release steps; push `main` only after the coordinator's signal (voice plugin first). Hosted ChatGPT update: `pending`, update prompt from `CHATGPT_UPDATE.md`.
