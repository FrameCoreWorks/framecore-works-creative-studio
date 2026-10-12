# Handover: motion graphics after 1.70.0

Written 2026-10-12 by Cloud Code (change CC-20261012-04) for the next surface, normally Codex. Read `AGENTS.md` first: Studio is in maintenance mode, and the motion round that produced 1.70.0 was an owner-requested exception. Continue these items only when the owner asks for them, one release per coherent step.

## Owner's goal

Motion graphics is the owner's main paid use: short client reels and Meta ads, built in Claude Code with HyperFrames. He wants Studio to plan, build and review them well in that setting, with a usable set of ad structures, lyric videos, hybrid films (AI-generated images and clips combined with motion graphics), still frames and strong transitions.

## Done in 1.70.0

- `skills/hyperframes-workflow/references/claude-code-reels.md`: HyperFrames as the default engine in Claude Code, setup, the Studio-HyperFrames division of labour, a map of the 21 HyperFrames skills (commit `86521b9`, 0.8.149), the eight-step production loop, render evidence.
- `skills/hyperframes-workflow/references/reel-board-system.md`: boards, persistent frame, type, motion targets, twelve ad structures with registry blocks, formats and safe boxes, lyric video, hybrid footage, transitions, still frames.
- `skills/hyperframes-workflow/assets/motion-quality/motion_activity.py` with `tests/motion_activity_test.py`: REVISE above 40 % undeclared still time or a still over 2.5 s; `--hold` declares intended stills.
- Wiring in the skill's runtime and review steps, the runtime map and `hyperframes-engine.md`; AGENTS.md records the owner decision.

## Reference material

The owner supplied five reference reels (vertical, 30 to 47 s, with sound): a lyric video with one line per board and a constant HUD frame; a local-service ad mixing work photos with heavy condensed type and a booking end card; an app ad with recreated UI screens and a cashback number; a B2B service ad with UI panels; a voice-over demo with word-by-word captions over a dark chat UI. They stood still 14 to 38 % of the time. They are third-party work: do not copy them into the repository or name their brands; use only the patterns described in `reel-board-system.md`.

## Next steps, in order of value

0. **Lyric timing on a real song (added in 1.71.0).** On the owner's Mac or a container with enough disk: `pip install stable-ts` (and `demucs` for dense mixes), run `skills/hyperframes-workflow/assets/motion-sync/lyric_timing.py` on a 2 to 3 minute licence-free song with its lyrics, check the matched share and the lines it lists by ear, build the lyric reel from the timing JSON with skill `music-to-video`, run motion activity, and record the result in the motion-sync README. The compendium (`references/motion-compendium.md`, 1.71.0) holds the research of 2026-10-12.
1. **A recorded client-style reel through the route.** In a container with Node.js 22, FFmpeg and Chromium: `npm install hyperframes@0.8.149`, `HYPERFRAMES_BROWSER_PATH=<chromium>`, build one 20 to 30 s local-service reel from `reel-board-system.md` section 3 with neutral placeholder copy, render 9:16 and 4:5, run `motion_activity.py`, snapshot every board, and record the result in `claude-code-reels.md#evidence`. Fix the route text wherever the run shows it is wrong.
2. **Starter compositions, not catalogues.** For the three most common jobs (local service, app or product, offer), add one HyperFrames starter each under `skills/hyperframes-workflow/assets/reel-starters/<job>/` (index.html, sub-compositions per board, a persistent frame track, slots for copy and photos, a README with the board table). Each must pass `npx hyperframes check`, render at 9:16 and 4:5, and pass motion activity. Keep them structures: copy, palette and idea come from the brief. Never delete a path once released.
3. **Lyric video check.** Run skill `music-to-video` on a short licence-free track with supplied lyrics; write down where Studio's board rules (`reel-board-system.md` section 5) and the skill disagree, and settle it in the reference.
4. **Hybrid footage in the contract route.** The bundled contract engine has no video layer (plan item 3.1, "footage underlay", deferred). If hosts without a shell need hybrid films, add a `footage` scene kind to `motion-scenes.mjs`, its three byte-identical copies and the Python renderer (ffmpeg frame decode), with parity tests. Otherwise leave hybrid films to HyperFrames.
5. **Transitions in the contract route.** Today: scene exit fade, `sweep`, background wipes. Add only what briefs ask for (push, iris, split), in every engine copy and the renderer, with pixel parity tests.
6. **Motion activity in automation.** Call `motion_activity.py` from `acceptance.py` as part of the temporal verdict when an MP4 is supplied, and from the automated frame review summary.
7. **Meta placement facts.** If a client needs exact Reels or Stories interface margins, research Meta's current placement guide, record the date and the source in `reel-board-system.md` section 4, and keep the HyperFrames safe boxes as the default.

## Constraints that bite

- Never delete, rename or move a package path; retire with a stub (`AGENTS.md`).
- Skill descriptions are at 7,773 of 7,800 characters; the orchestrator `SKILL.md` must stay at or under 32,000 bytes (29,225 now). Do not edit descriptions without measuring.
- A change to startup metadata (orchestrator description, manifests) needs the owner's ChatGPT startup check.
- Releases: `python3 scripts/release.py prepare X.Y.Z --change-id ... --push`, then `publish`; hosted ChatGPT Work is `not_tracked` (give the owner the Plugin Creator prompt only).
- Host evaluations cost the owner's plan usage: run them only when a change needs them, at most 25 cases per pass and 5 per gate, and record cases, tokens and time.

## Open findings from the full check of 2026-10-12

RT18 (named Studio, teacher worksheet, no skill loaded), RT01 and RT08 (no Studio name), F02 (catalog wording), and the name rule missing from the motion skill: see `docs/full-check-2026-10-12.md`.
