# GPT Astra audit, 2026-11-04

External audit of Creative Studio 1.167.1 (`d2dbc18`), Toolbox 1.6.1 (`8652ba3`) and Open Assets 0.4.1 (`b15c35a`), run by the owner in ChatGPT (GPT Astra, ultra reasoning) and sent on 2026-11-04. The original material is kept in Polish as received:

- [Raport-audytu.md](Raport-audytu.md): main report (scope, results, limits, recommended order).
- [Rejestr-ustalen.md](Rejestr-ustalen.md): the 42 findings with evidence and reproductions.
- [Backlog-rozwoju.md](Backlog-rozwoju.md): 42 findings plus three proposals, sized, with acceptance.
- [Plan-rozwoju-nauki.md](Plan-rozwoju-nauki.md): learning-mode development plan.
- [Instalacja-modulow-Work.md](Instalacja-modulow-Work.md): module installation in ChatGPT Work.

The full evidence ZIP (transcripts, simulations, raw reproductions) stays with the owner; it is not copied here.

The audit's simulations were text-response simulations, not studies of learning outcomes with people, and most installs were not run. Every finding was re-checked in the source before any change; the table below records the verdict and where it was fixed.

## Status per finding

| ID | Priority | Verdict | Fix |
|---|---|---|---|
| SEC-002 | P0 | Confirmed (reproduced: old WAV overwritten by `RIFFFAKE_BROKEN`) | Voice And Narration 1.0.3 (Studio 1.168.0): temporary file, validate, atomic replace; VoxCPM2 worker too |
| SEC-001 | P1 | Confirmed (reproduced: HTTP 200 from a private address with `HTTP_PROXY` + `NO_PROXY=*`); the existing test encoded the bug | Brand Kit 1.0.2 (Studio 1.168.0): the peer check follows urllib's actual per-request routing |
| ORCH-01 | P1 | Confirmed (both halves) | Toolbox 1.6.2 (`b4307db`): the envelope binds operation, command, root and input hashes to `--request`; Studio 1.168.0: `companion_intake.py --request` |
| Pillow pin | P1 (report section) | Confirmed: GHSA-w889-685w-c8fh covers 2.6.0 to 12.3.0, fixed in 13.0.0 | Studio `requirements-ci.txt` and Open Assets `requirements-dev.txt` pin 13.0.0 |
| DIST-001 | P1 | Confirmed (`yaml.safe_load` rejects the REA description; Claude's loader tolerated it) | Toolbox 1.6.2 |
| DIST-002 | P1 | Confirmed (no portable `mcp.json`) | Toolbox 1.6.2; host activation NOT_RUN |
| DIST-003 | P3 | Confirmed (42 and 41 characters against a 30-character limit) | Brand Kit 1.0.2, Voice And Narration 1.0.3, with a test |
| INSTALL-01 | P1 | Confirmed (finder said Work cannot keep a skill) | Studio 1.168.0 `skill-finder.md`: the Plugin Creator private-plugin route |
| INSTALL-02 | P2 | Confirmed (valid JSON of the wrong shape raised `AttributeError`) | Studio 1.168.0 `find_skills.py`: a controlled `offline` status |
| DIST-004 (Toolbox Work route conflict) | P2 | Confirmed | Toolbox 1.6.2 `CHATGPT_INSTALL.md` |
| UPSTREAM-01, UPSTREAM-02 | P1, P2 | Plausible from the saved inventory (not re-read here: the saved Work plugins are on the owner's account) | Toolbox 1.6.2 route carries binaries and names missing files; repairing the two saved Work plugins is a host step, pending |

| ORCH-07 | P2 | Confirmed | Toolbox 1.6.3 (`e9fe001`): an interrupted Earshot run returns status `cancelled` with code `interrupted` |
| ORCH-08, ASSET-001, ASSET-002 | P3, P2, P2 | Confirmed; ASSET-002 partly a false alarm (the provider dossier was stale, the index was right) | Open Assets 0.4.2 (`f71bd42`): envelope flags only on status/search/verify/download, `reach` explained as a connection check, Commons dossier corrected |
| CR-001 | P2 | Confirmed | `positioning-and-audience-research.md`: a page that repeats a claim is a source read, not proof |
| CR-002 | P2 | Confirmed | `ai_writing_check.py` skips quoted spans; copy-voice reviews flagged spans and keeps locked text, with a test |
| CR-003 | P2 | Confirmed | `production-worksheets.md`: planned, quoted, committed, invoiced and paid kept apart |
| CR-004 | P3 | Confirmed | `motion-quality-direction.md`: recorded offsets stay; N/A for a criterion the brief rules out |
| CR-005 | P2 | Confirmed | UGC disclosure default rule keeps the rows' exemptions and Unknowns |
| CR-006 | P3 | Confirmed | FrameCut example applies at revision 4 after `align-script`; SKILL.md lists `align-script` |
| ORCH-02 | P2 | Confirmed | `companion_setup` is one record per companion in Project State and the cross-host handoff |
| ORCH-03 | P2 | Confirmed | Instruction packets: private handoff to an approved target vs public export |
| ORCH-04 | P2 | Confirmed | `loop-protocol.md` authorization scope matches the integration policy |
| ORCH-05 | P3 | Confirmed | `producer-ai-task-builder` names the real reason its path is kept |
| ORCH-06 | P3 | Not changed: `workflow-orchestrator/SKILL.md` is under its 32,000-byte budget; reclaiming space is not needed for any fix here | — |
| ORCH-09 | P3 | Confirmed | `client-handoff.md`: the manifest script checks records, it does not write the list |
| LEARN-01 | P2 | Confirmed (LM01 described four options and a separate pace menu; "3" was treated as invalid) | LM01: five options, combined area and pace menu, `3` is skill search, `6` is the invalid token |
| LEARN-02 | P2 | Confirmed | W06: exactly one question, no unearned completion claim, with negative scorer samples |
| LEARN-03 | P3 | Confirmed | `docs/learning-mode.md`: five options, motion is area 8, disclosure only on a real research need, 29 scenarios |
| LEARN-05 | P2 | Confirmed | Learning progress card carries accessibility, language, evidence forms, no-render preference and research status |
| LEARN-04, LEARN-06 | — | Backlog: needs a pilot with people, not a source change | — |
| INSTALL-03 | P2 | Confirmed | `find_skills.py --read` reads the licence at the same commit and says the audits and install command are not tied to it |
| ROOT-01 | P2 | Confirmed (saved Work plugin was one release behind) | Host step: update the saved Work plugin to the current release; pending |
| ROOT-02 | P3 | Confirmed | README: one install line right under the introduction, linking to Install |
| ROOT-03 | P2 | Confirmed (no branch protection or ruleset on `main`) | Pending: a ruleset blocking force push and deletion of `main` and `gh-pages` needs repository admin access, which this session's tools do not have |
| SEC-003 | P2 | Confirmed (VoxCPM2's dependencies are not hash-locked) | Backlog: needs a reviewed lock file for a large ML stack |
