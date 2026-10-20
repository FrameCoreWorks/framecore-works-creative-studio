# Task for ChatGPT Work: a native Reel Editing Assistant (2026-10-20)

Owner request: Studio should natively offer what paid courses and "AI editing assistants" sell, built by us instead of bought. This is an analysis plus a work order. Reply to the owner in Polish; direct, no em dashes; facts, inferences and unknowns separated. Attribute your work as `Origin-Agent: chatgpt-work`, change IDs `CW-YYYYMMDD-NN`.

## What the two offers sell (facts from their sales pages, 2026-10-20; the course and the assistant themselves were not seen or bought)

- [Montażysta AI course](https://zadykowiczmedia.pl/kurs-montazu-wideo-ai) (127 zł, Claude Pro needed): install, cut pauses and slips from raw phone footage, add text and animated typography and effects, weave in the user's own photos, logo and clips with one command, teach the AI the user's style once (fonts, colours, cut tempo, caption behaviour) and fix by writing one sentence. Vertical formats: Reels, TikTok, Shorts.
- [Asystent AI do montażu rolek](https://agenciai.pl/funnel/asystenci-ai-lejek2-organic/asystent-ai-do-montazu-rolek) (97 zł, ChatGPT Plus or Claude Pro, runs on the user's computer): the assistant cuts out mistakes and adds effects; a video guide and email support are part of the product. Its technical method is not described on the page (Unknown).

Inference: both are a packaged prompt/skill set around a coding agent with FFmpeg-style tooling, plus a tutorial. Nothing on the pages suggests technology Studio cannot build.

## What Studio has today (facts, from the repository at 1.98.0)

| Need | Studio | Gap |
| --- | --- | --- |
| Edit plan, asset bin, protected moments | Opencut Video Studio (plan, `edit_export.py` to EDL/OTIO/CSV) | plans only; nothing cuts the footage |
| Cuts of supplied footage, designed sound, music bed | `hyperframes-workflow/assets/motion-sound/footage.py`, `sound.py` | measures scene cuts, does not remove pauses or retakes |
| Captions and subtitles, burn-in | Caption Studio + `assets/captions/captions.py` (needs a transcript or SRT) | no transcription step as a tool; no link to a rough cut |
| Kinetic type, motion graphics, logo and assets in a reel | Motion Graphics Workflow (HyperFrames), dense kinetic reels, scene kinds | built for generated films, not for overlays on a talking-head clip |
| Hearing the result | `sound-listen/listen.py`, `place_sfx.py` (1.98.0) | none |
| User style kept between reels | Studio Workstyle Profile (pace, vocabulary) | no editing style profile (fonts, colours, tempo, caption behaviour) |

Conclusion: Studio plans edits and makes generated motion films well, but it cannot yet take a raw talking-head recording and return a finished reel. The missing piece is the automatic rough cut and its glue.

## Step 0 (owner addition): inventory every tool already wired into the plugin, then unify

The owner works in another thread that has already attached further tools to the plugin. Cloud Code cannot see that thread, and at `4a11e2d` (2026-10-20) `origin/main` contains none of its commits (Unknown whether they are unpushed, on another branch, in the hosted ChatGPT plugin only, or on the owner's machine). Before building anything:

1. **Inventory the repository.** List every tool and reference that touches editing, using `skills/workflow-orchestrator/assets/capability-card.json`, `skills/hyperframes-workflow/references/runtime-map.md`, `extensions.json` and `git log`. At minimum: `edit_export.py` (EDL/OTIO/CSV), `captions.py`, `footage.py` and `sound.py`, `listen.py` and `place_sfx.py`, `audio_envelope.py` and `beats.py`, `lyric_timing.py`, `reference-breakdown`, `motion_activity`, `image_probe.py`, craft lint and contrast, the HyperFrames and Remotion routes, `animate-voice/retime.py`, the pinned extensions (REA, OpenCreator, Upscayl, earshot and others). Produce a table: tool, owner skill, input, output, host requirements, status.
2. **Find the other thread's tools.** Check every branch and open pull request of `FrameCoreWorks/framecore-works-creative-studio`, the saved ChatGPT Work plugin (read the saved package inventory against the repository), and the commit trailers of recent history. If you cannot find them, ask the owner once, in Polish, for the branch, files or commit they live in, and do not guess. Do not overwrite or duplicate them: read their intent, keep compatible work, merge by inspection (see Development provenance in AGENTS.md).
3. **Resolve overlaps.** Where a new tool does what an existing one already does (cutting, captions, transcription, overlays), keep one, retire the other with a stub if it is in the shared package (never delete or move a path), and say which in the ledger.
4. **Bind them into one pipeline.** The Reel Editing Assistant is the single entry that orders these tools for a request: ingest and probe, transcribe, rough cut with approval, captions retimed to the cut, overlays and assets, sound (designed or placed) and loudness, checks, export (MP4 and an EDL/OTIO for an editor), iteration by sentence. Write the pipeline as one table and one worked example per input type (talking head, product clips, screen recording), add the routing rows, the capability card entries and runtime-map rows, and a test that fails when a listed tool path is missing.
5. **Report to the owner** in Polish: the inventory, what the other thread contributed, the overlaps and how they were resolved, and the numbered decisions that need the owner.

## Work order

Build one native owner, working title **Reel Editing Assistant** (an `agents/openai.yaml` with `interface.display_name` and a 25 to 64 character `short_description`; follow `docs/skill-naming.md`; keep within the 7,800 character description budget by shortening other descriptions if needed; add it to the routing tables, the welcome menus only if the startup contract allows it, the capability card and the runtime map). Decide first whether it is a new skill or an extension of Opencut Video Studio; give the owner a numbered recommendation with the trade-offs and then proceed with the recommended one.

1. **Rough cut tool** (`reel_cut.py`, Python and FFmpeg, standard library first): input a video and optionally a transcript; detect silence (`silencedetect`), long pauses and, with a transcript (word timing from `faster-whisper` when installed, else a supplied SRT/JSON), filler words, false starts and repeated takes of the same sentence (keep the last complete take); output a cut list (JSON, frame-snapped, with the reason for every cut) and, on approval, the cut video with short audio crossfades at the joins. Always keep the original and show the owner what was removed (a table with times and text). Never cut silently: the owner approves the list.
2. **Transcribe route**: a documented route for transcription per host (local `faster-whisper`, the host's own, or a supplied transcript); no audio leaves the machine without the user's explicit yes.
3. **Captions**: connect the cut list to `captions.py` so captions follow the cut timeline (retime after cuts); styles come from the style profile.
4. **Overlays**: titles, kinetic text, logo and the user's photos or clips placed on the cut video, using HyperFrames or Remotion where code runs; reuse the dense kinetic reel and motion-quality rules. Overlays must not collide with the caption safe zone.
5. **Editing style profile**: a small JSON the user creates once (fonts from the bundled OFL fonts or their own, brand colours, cut tempo target, caption position and highlight, logo placement, sound level). It is user input at run time, never a default tied to one person (owner decision 2026-10-10). Provide a template and a validator.
6. **Iterate by sentence**: define how a one-line change request ("bigger captions", "tighter cuts at the start") maps to profile or cut-list edits and a re-render, without redoing approved parts.
7. **Check the result** with the existing tools: `motion_activity` for dead time, `listen.py critique` and `sync` for sound, caption QA, contrast and safe zones, and the copy voice checks for on-screen Polish text.
8. **Tests and wiring**: a test with a synthetic video (tone, silences, a repeated sentence as generated speech or a stand-in transcript), `scripts/check_all.sh` line, knowledge wiring row, a host-eval case with `not_run` status, honest `when_missing` text in the capability card (no FFmpeg: deliver the cut list and an EDL through `edit_export.py`).

## Constraints

- Studio is a general product: nothing personalised to the owner. Rates, brands and fonts are run-time input.
- No copied course material or paid assistant files; the pages were read only for their feature lists.
- Do not delete, rename or move shared-package paths. A shared-package change needs the release procedure (`scripts/release.py`), then give the owner only the short Plugin Creator prompt; ChatGPT Work state stays `not_tracked`.
- Third-party audio and copyrighted material are never committed. Speech data in tests must be synthetic.
- Testing happens in your own sandbox (no Claude Code needed); report what ran and what did not. Host behavior in ChatGPT Work is verified only by owner-reported `PASS_REPORTED`.
- Unknown at writing: whether `faster-whisper` is available in your sandbox; check before choosing the default transcription route.
