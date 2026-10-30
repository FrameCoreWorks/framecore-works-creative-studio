# Install paths for the three FrameCore Works plugins (2026-10-30)

Owner request 2026-10-30: one map of every way Creative Studio, FrameCore Works Toolbox and FrameCore Open Assets
get installed, what is proven and what is not, and a step-by-step test list to run together on the desktop.
Versions: Studio 1.158.0, Toolbox 1.3.0, Open Assets 0.3.0.

## The intended experience (all hosts)

1. The user pastes `https://github.com/FrameCoreWorks/framecore-works-creative-studio` with "install it and
   explain each step" ([prompt](../CLAUDE_INSTALL.md#paste-this-prompt)).
2. Studio is installed; the assistant explains each step in plain words.
3. Open Assets is offered, explained, optional.
4. Toolbox is added and one numbered list is shown: Studio's own add-ons, then the Toolbox catalog split into
   "works right away in a session" and "needs your computer", each with how it helps Studio. The user picks numbers.
5. Earshot's tier question only if Earshot was picked; startup style last; "done" with how to start.

## Map of routes

| Host | Route | Studio | Toolbox | Open Assets | Persists? |
| --- | --- | --- | --- | --- | --- |
| claude.ai account (web, desktop app, phone, Cowork, cloud Claude Code) | Customize > Plugins > Add marketplace `FrameCoreWorks/framecore-works-creative-studio`, turn on the plugins (recommended in Claude) | marketplace entry | marketplace entry `toolbox` (git-subdir pin) | marketplace entry `framecore-open-assets` (git-subdir pin) | yes, on the account; synced into every Claude Code cloud session as `@synced` |
| Claude Code on a computer (CLI, desktop Code tab) | pasted link: the assistant runs `claude plugin marketplace add` + `claude plugin install framecore-work-creative-studio@framecore-works` | installed | comes as a dependency | installed on yes | yes, on that computer |
| Claude Code cloud session (claude.ai/code, phone) | pasted link leads to the account route; a container install is for this session only | account route | account route | account route | container: no; account: yes |
| ChatGPT Work (web, desktop, phone) | pasted link: Plugin Creator saves each plugin, built from files read as text (no ZIP from the user) | Plugin Creator | Plugin Creator (`toolbox`) | Plugin Creator | yes, on the account |
| Codex | pasted link: `scripts/install_codex.py` plan, install, verify | native entry | Toolbox `install_codex.py` | Open Assets `tools/install_codex.py` (since 0.3.1) | yes, on that computer |

Catalog entries picked from the list: Claude installs them from the Toolbox marketplace
(`FrameCoreWorks/framecore-works-toolbox`); app notes are installed by hand from their docs; in ChatGPT Work and
Codex third-party entries without a reviewed route are listed "(Claude only)".

## Known host limits (check before building)

- Claude Code cloud containers are deleted; only plugins turned on in the claude.ai account load in a new session.
- A same-name local install takes precedence over its `@synced` copy; a different name or a loose skill in
  `~/.claude/skills` duplicates it. Never copy loose skills.
- `claude plugin install <entry>@framecore-works-toolbox` fails until that marketplace is added.
- ChatGPT Work code execution has no network: Earshot's engine and Open Assets downloads cannot run there.
- Plugin Creator takes only a ZIP path inside code execution; the GitHub connector writes no files.
- Claude apps are not documented to install plugin dependencies; turn each plugin on.

## What is proven

| Claim | Evidence | State |
| --- | --- | --- |
| Studio + Toolbox install from Studio's marketplace in Claude Code | empty config, Claude Code 2.1.314, 2026-10-30 (`CC-20261030-04`) | verified (source/CLI) |
| Toolbox 1.3.0 installs from its own marketplace | isolated config, 2026-10-30 | verified (CLI) |
| Account plugins sync into cloud sessions as `@synced`; same name overrides | owner's cloud session, 2026-10-30 | PASS_REPORTED |
| All 16 Toolbox marketplace entries install after adding its marketplace | owner's cloud session, 2026-10-30 | PASS_REPORTED |
| Toolbox 1.2.4 saved in ChatGPT Work without a ZIP | owner, 2026-10-30 | PASS_REPORTED |
| Studio installed in ChatGPT Work | 1.156.0 by a one-off ZIP upload | PASS_REPORTED (not the no-ZIP route) |
| The new setup order and numbered list in a live client | none | NOT_RUN |
| Account plugins visible in the desktop app, phone and Cowork | none | NOT_RUN |
| Fresh Studio install by pasted link in Work, Codex, Claude Code | none | NOT_RUN |
| Cloud environment setup script keeps plugins | none | NOT_RUN |
| Codex desktop (checklist item 7): Studio, Toolbox and Open Assets files and runtime | Codex through codex-bridge in an isolated `HOME`, 2026-10-30: Studio `install_codex.py` plan/install/verify PASS (37 modules, 1602 files), Toolbox PASS (31 files), Open Assets entry and bundle PASS by hand (0.3.0 had no helper; 0.3.1 adds `tools/install_codex.py`), real Open Assets downloads PASS | verified (files and runtime) |
| Codex: skills activate in a new Codex session | none | NOT_RUN |
| Earshot light (checklist item 8) | Codex isolated `HOME`, 2026-10-30: `ready_light`, 358 MB on disk (guides now say about 360 MB); a measurement through `envelope.py` gave −14.0 LUFS, −1.5 dBTP | verified in Codex; on the Mac in Claude NOT_RUN |
| Toolbox 1.3.0 from its own marketplace in an isolated Claude Code config | 2026-10-30: plugin PASS; 18 of 21 catalog entries installed, the three `git-subdir` entries (animate, open-design, nateherk-design) blocked by the test sandbox's proxy, not the repository (all passed in the owner's cloud session) | verified (CLI), 18/21 |

## Test checklist (desktop, together with the owner)

Record each result as PASS_REPORTED or the exact failure, with the client and version.

1. **claude.ai account.** Customize > Plugins: Studio's marketplace present and synced; Studio 1.158.0,
   Toolbox 1.3.0 and Open Assets 0.3.0 turned on. New Claude Code cloud session: `claude plugin list` shows all
   three as `@synced` with those versions, no duplicates.
2. **Same plugins elsewhere.** Desktop app chat, Cowork and the phone app: Studio's name starts the welcome;
   "toolbox" shows the numbered list.
3. **Claude Code on the Mac, fresh.** Empty project, paste the prompt. Expect: inventory first, one question,
   Studio + Toolbox installed, Open Assets asked, numbered list, a picked session entry installs, a picked
   computer entry gets its steps. New conversation: `claude plugin list` shows them.
4. **Claude Code cloud, pasted link.** Expect the account route explained step by step and the warning that a
   container install lasts only this session.
5. **ChatGPT Work desktop.** Paste the prompt. Expect Plugin Creator saves Studio (update guard if it exists),
   Open Assets asked, Toolbox saved, numbered list with "(Claude only)" marks and Earshot under "needs your
   computer". New conversation: Studio's welcome.
6. **ChatGPT Work phone.** Same prompt; at least the list and one Plugin Creator save.
7. **Codex desktop.** Paste the prompt. Expect `install_codex.py` plan, install, verify for Studio, then the
   same setup questions.
8. **Earshot.** Where code runs with network (Claude Code on the Mac), pick Earshot: light tier plan, consent,
   `status --json` shows `ready_light`.

Findings from the 2026-10-30 fresh-install test (report in the owner's working folder,
`raporty/2026-10-30-test-instalacji-trzech-pluginow.md`) were fixed the same day in Open Assets 0.3.1
(`status --host`, Codex helper), Toolbox 1.3.1 (Earshot request envelopes, staging inside `--root`, light size,
Codex routes for ffmpeg-skill and rea) and Studio (pins, light size and scope, photo-hero contrast, asset folder
rule); see `CHANGELOG.md`.

A failure goes to one place: this file's tables and the repository whose route failed, fixed in all three
repositories together when the fix touches the shared flow.
