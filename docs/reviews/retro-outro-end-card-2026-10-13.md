# Retrospective: a 6-second client end card (2026-10-13)

Source: the owner's Workflow Self-Improvement log from a Claude Code session (plugin 1.71.0, synced to 1.72.0 during the session): a 6-second animated end card (logo and contact) in 9:16 and 1:1, four MP4s delivered after three correction rounds. Client data was already replaced with neutral stand-ins.

## Decisions

| Proposal | Verified against the package | Decision |
| --- | --- | --- |
| CP-1 HTML capture without npm | Real gap: `export-video.mjs` drives the browser without dependencies but only for a contract; the code-motion starter writes SVG frames only; the Python renderer draws bundled scene kinds only | Fixed in 1.73.0: `motion-export/capture-html.mjs` (dependency-free, DevTools pipe, FFmpeg pipe, rational fps, `--query`, `--audio`), tests, routes in the skill, runtime map and Claude Code reel route |
| CP-2 probe before the runtime | Step 4 of the skill had no probe | Fixed: step 4 probes Node.js, FFmpeg, the browser and the npm registry, and names the chosen route in one line before the build |
| CP-3 end-card defaults | The end-card line in the reel board system said nothing about a clean card or optional additions | Fixed: covering elements clear together within one beat, no decoration stays unless asked, a Studio-proposed addition stays off until clearly accepted; an unclear answer gets one question |
| CP-4 one menu instead of two | Touches the protected startup and menu contract | Adopted by the owner as CR-20261013-01 and released in 1.74.0: areas `1–8` and pace `A–B` in one message. Host eval W05 in Claude Code: FAIL on 1.73.0 (two options after `1`), PASS after; the first after-run also showed the model renaming and reordering the areas because the list lived only in the reference, so the orchestrator `SKILL.md` now carries it and W05 checks the order. The owner's ChatGPT startup check is pending |
| CP-5 a "delicate" sound preset and `--lufs -16` | Hand-set cue gains worked; no defect in the delivered sound | Owner note, not changed |
| CP-6 acceptance tools for custom renders | Already in step 6 of the skill (visible-text audit, motion activity on every MP4, `acceptance.py`); the session did not run them | No text change; the HTML capture README now repeats the three checks where the custom route ends |

The log's own reading that a starter for custom animation was missing was partly wrong, as the log notes: GSAP and frame starters exist; the gap was capture and encoding without npm.
