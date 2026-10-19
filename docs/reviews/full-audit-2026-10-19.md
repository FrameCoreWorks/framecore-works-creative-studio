# Full audit, 2026-10-19 (after 1.93.0)

Requested by the owner after the 1.91.0 to 1.93.0 integrations (huashu-art-motion, Iso Glow, Open Design, anti-slop): check the repository and plugin end to end, above all whether the knowledge added from outside repositories is connected so the plugin knows when and how to use it; check orchestration, handoffs between skills, the GitHub tree and branches; fix gaps at once. Baseline `beaba73` (main, package 1.93.0). Fixes ship in 1.94.0.

Method: three parallel read-only reviews (reachability of new knowledge from the skills that load it; orchestration and rule conflicts; records, checks and repository structure) plus direct checks: the canonical validator, a scan of every executable tool against the capability card, the test list against `scripts/check_all.sh`, remote branches and tags, and the Pages workflow. No host test, provider call or paid run (owner decision: no host tests for now).

## Verdict

- **Facts.** The new knowledge was stored and tested, but several pieces were reachable only from one skill or from none: page and app mockups, slide or pitch decks and contrast checks had no owner in the routing table; DESIGN.md export, prompt examples and the contrast checker were linked only from their own READMEs or one reference; reference breakdown, lyric timing and the audio envelope were not linked from the owners a request lands on first (orchestrator, Caption Studio, Creative Music Video Director). Two rules contradicted each other (one-pass text versus exact-copy compositing; "enter slowly, leave fast" versus "enter fast, settle slowly"). The Iso Glow example capped every film at 8 s. These are fixed.
- **Inference.** After the fixes, a model that loads the owner a request reaches reaches the adapted rule or tool in one link. `tests/knowledge_wiring_test.py` now fails if one of those links disappears.
- **Unknown.** Whether hosts actually follow the new routes: the new host-eval suite `additions` (11 cases) is `not_run`.

## Findings and what changed

| # | Severity | Finding | Fix in 1.94.0 |
| --- | --- | --- | --- |
| 1 | High | No owner for landing pages, app screen mockups, HTML pages, slide or pitch deck design | Routing row to Static Graphic Design Creator; collision rule in routing boundaries; the static SKILL.md names the craft-rules sections, Copy Voice for the words, Delivery for the export |
| 2 | High | No route for a contrast or accessibility check | Output Critic measures with `contrast_check.py`; HTML, CSS and SVG with `craft_lint.py`; cue added; collision rule |
| 3 | High | Orchestrator and Pipeline Core said text in rasters is always one-pass, contradicting the exact-copy compositing route | Both name the exception for the static owner's client-final route |
| 4 | High | DESIGN.md export hidden | Linked from the brand row cue, brand identity profile, Delivery Documentation, static SKILL.md and Pipeline Core's tool list |
| 5 | High | Iso Glow example: `D = Math.min(8, …)`, fixed `data-duration="8"`, no audio clip, no render step | `D = ENVELOPE.duration`; `audio_envelope.py --inject` sets the composition and music clip duration; commented clip line (the track is never committed); render step with HyperFrames or `capture-html.mjs`; test extended |
| 6 | High | Song-led requests did not reach lyric timing or the envelope tool | Links from Caption Studio, Creative Music Video Director (hand-off for coded lyric videos), Motion Graphics owners table and routing boundaries; cue "animacja do muzyki, lyric video" |
| 7 | Medium | `lyric_timing.py` preferred stable-ts (archived 2026-05-30, never verified here) over faster-whisper (verified on two songs) | faster-whisper first, then stable-ts, then whisperx; README and error text updated |
| 8 | Medium | Pipeline Core never named its shared tools | "Shared design tools" list: craft lint, contrast, DESIGN.md, prompt examples, AI writing check |
| 9 | Medium | Prompt examples could lose to a web search | Rule in Pipeline Core and the static SKILL.md: after the idea is chosen, before a web search, structure only |
| 10 | Medium | Overlapping look routes in Motion Graphics (Anatomy, Animate, Iso Glow, art-style) | One precedence line by deliverable |
| 11 | Medium | Motion timing conflict and "3:1" ambiguity in art-style direction | Entries longer than exits with ease-out, linked to motion craft; "about three times the size or a clear weight step" |
| 12 | Medium | `accent-overuse` fired on video compositions where the accent rule is per shot | Skipped in video compositions; README updated |
| 13 | Medium | Polish dash rule allowed only the spaced en dash while the protected welcome uses the em dash; the AI writing check scores the welcome as a cluster | Polish standard accepts the spaced em dash, one style per text; AI writing patterns: protected or locked text is reported, never silently rewritten |
| 14 | Medium | Capability card missed user-facing tools | Added `lyric_timing`, `motion_activity`, `html_capture`, `motion_prompt_library`, `asset_manifest`, `environment_check`, `web_reach`; HyperFrames engine names the reel starter and Iso Glow example; web research falls back to web reach; runtime-map rows added; card checked 2026-10-19 |
| 15 | Medium | Reel starter not offered at build time | Linked from Motion Graphics build step and Claude Code reels step 3 |
| 16 | Medium | Review loop: Output Critic did not mention craft rules; motion review row lacked motion activity; "finds anything" vague | Fixed in Output Critic, loop protocol and Motion Graphics |
| 17 | Medium | Storyboard owner ambiguous for motion | Motion keeps its own storyboard in the contract; Sequence Architect only for unresolved narrative order |
| 18 | Low | Extensions without category; catalog output ungrouped; `<plugin>` undefined | Categories for rea, animate, motion-designer, meta-ads-designer, agent-reach; catalog grouped by category; placeholder defined; test added |
| 19 | Low | Web reach sends client URLs to Jina Reader by default | Research Evidence: use `--route direct` for client or unpublished URLs |
| 20 | Low | Validator anchor slug collapsed hyphen runs, unlike GitHub, so one link that worked in the validator was broken on GitHub | Validator slug now matches GitHub; the heading renamed ("Google Flow Music and Lyria") so the link works everywhere |
| 21 | Low | RELEASE_STATUS said "origin: codex" since 1.87.1 | `release.py` now writes the origin; corrected |
| 22 | Low | Reference breakdown README said the environment check installs tools; motion-sync README pointed at a repository-only path as if in the package | Wording fixed |

## Regression guards added

- `tests/knowledge_wiring_test.py`: each integrated reference or tool is linked from the entry files of its owners, and the capability card names each wired tool. Add a row when a new reference is integrated.
- `tests/extensions_test.py`: every registry entry has a category; the catalog is grouped by it.
- `tests/iso_glow_test.py`: injection sets the root and music clip durations and leaves scene durations alone.
- Validator: GitHub-exact anchors.
- `tests/host-evals/additions.json`: 11 host cases (AD01 to AD11) for option 4, AI writing, page mockups, contrast, decks, DESIGN.md, lyric video, Iso Glow, art-style, reference breakdown and prompt examples. `not_run`.

## Repository structure

- `main` is linear with tags up to `v1.93.0` (125 tags). GitHub Pages (`gh-pages`) was last built from `0341238` (2026-10-14); the player and fonts have not changed since, so it is current.
- 83 remote branches. All are merged into `main` except two from 2026-10-07: `claude/plugin-cloud-update-vzrtk5` (a `package_claude_plugin.py` script and a ledger line; Claude packaging is now done by `release.py` and `claude plugin validate --strict`) and `cloud-code/CC-20261007-03-second-test-report` (a host-report file identical to the one on `main`). Inference: both are superseded. Nothing was deleted; branch cleanup is an owner decision.
- Every plugin test file and every root `tests/test_*.py` is run by `scripts/check_all.sh`.

## Open items (not changed, with reasons)

- **Environment check optionality (owner decision).** `tools.json` treats every tool as required by rule. faster-whisper, yt-dlp and pikepdf (used by `print_pdf.py`) are not in it; adding them would make them required. Options: keep as is; add an optional tier to the validator rule; or list them as required.
- **Skill descriptions** are at 7699 of 7800 characters. The Motion Graphics description does not name lyric video, beat-synced or isometric; the routing table and cues cover them. A wider description needs another description shortened.
- **Motion Graphics SKILL.md** is dense (its Deliver section mixes host routes, looks and review). A split into host route, a "look by brief" table and review is proposed, not done, to keep this release a set of links and fixes.
- Small items: `critique.py` large-text 3:1 branch versus the motion-review README wording; `ai_writing_check.py` inline CTA detection and its language label for mixed text; `prompt_examples.py` ranking; a GSAP CDN note for the offline capture route; the qa-iteration row in the role map (it maps through the text below the table).
