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

Rows for the remaining findings are added as they are handled.
