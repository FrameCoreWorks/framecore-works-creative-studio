# Delivery gate

The output review judges the idea and the craft. The delivery gate is the part
that can say no on its own: a script measures each final file and returns
PASS, FAIL or BLOCKED, and a file reaches the user only with a current PASS
report or a waiver the user asked for.

## The rule

1. Final files for the user go in a folder named `export/` in the project.
   Drafts, previews and review sheets stay outside it.
2. Write the brief's measurable requirements in `gate.json` next to `export/`
   (or inside it) before the first check. Leave out what the brief does not fix.
3. Run the gate on every final file:

   ```bash
   python3 <plugin>/skills/delivery-documentation/scripts/studio_gate.py check export/<file>
   ```

4. FAIL: fix the file and run the check again. Tell the user what failed in
   plain words; do not call the file ready. BLOCKED: a measuring tool (ffmpeg,
   numpy, Pillow) is missing; install it or say the file is unchecked.
5. Only when the user explicitly accepts a failing file, record it in their
   words: `studio_gate.py waive export/<file> --reason "..."`.
6. Any change to a file voids its report (the report holds the SHA-256), so the
   last check is on the exact file delivered. `studio_gate.py status export/`
   lists what is still open.

Report: `export/.studio-gate/<file name>.json` (verdict, each check with its
result and detail, the spec used, the file hash). Exit codes: 0 PASS or WAIVED,
1 FAIL, 2 BLOCKED or an input problem.

## What it measures

| Kind | Checks |
|---|---|
| Video (mp4, mov, webm, mkv, m4v) | size, ratio, frame rate and duration against the spec; required or forbidden sound; a black stretch of 1 s or more inside the film (fades at the edges pass) or a film half black; undeclared still time (`motion_activity.py`, declare holds); photosensitive flashes (`flash_check.py`); near-silent sound, loudness against the spec and true peak (default at most -1 dBTP) |
| Audio (wav, mp3, m4a, aac, flac, ogg, opus) | duration, near-silence, loudness and true peak |
| Image (png, jpg, webp) | blank, flat-colour or fully transparent image; size, ratio and print checks (`image_probe.py`); transparency when required |
| Text (txt, md, srt, vtt) | empty text; machine-made writing clusters (`ai_writing_check.py`); for Polish, unapplied safe typography fixes and channel hard limits (`pl_copy_check.py`); `max_chars` |
| Other (pdf, gif, svg, zip, html and more) | the file exists and is not empty; review it yourself |

It measures files. It does not judge whether the idea works or the motion
feels right; that stays with the output review and the user.

## gate.json

```json
{
  "schema": "studio-gate-spec/1",
  "defaults": {"audio": "required", "lufs": -14, "true_peak_max": -1.0},
  "files": {
    "reel-*.mp4": {"width": 1080, "height": 1920, "fps": 30, "duration_min": 14, "duration_max": 16,
                   "holds": ["13.5-15"]},
    "post.png": {"width": 1080, "height": 1350},
    "caption.txt": {"language": "pl", "channel": "meta-primary-text"},
    "teaser.mp4": {"skip": {"still": "the brief asks for a static end card of 4 s"}}
  }
}
```

Keys: `width`, `height`, `aspect` ("9:16"), `fps`, `duration_min`,
`duration_max`, `audio` (`required`, `silent`, `any`), `lufs`,
`lufs_tolerance` (default 2), `true_peak_max`, `holds` ("start-end" seconds),
`max_still_share`, `max_still_seconds`, `preset` (an `image_probe` preset),
`alpha`, `language`, `channel` (a `pl_copy_check` channel), `max_chars`, and
`skip` (`{check id: reason}`; a skipped check is recorded, never silent).
Patterns under `files` match the file name and override `defaults`.

## Enforcement by host

| Host | How the gate is enforced |
|---|---|
| Claude Code | The plugin's `hooks/hooks.json` registers a Stop hook. While a recent file in an `export/` folder up to four levels below the session folder has no current PASS or WAIVED report, the turn cannot end: the hook sends the model back with the file list and the fix. After two blocks in a row it lets the turn end with a visible "NOT PASSED" warning instead of looping. Verified in a headless Claude Code session on 2026-10-31. |
| Codex | Codex loads the same `hooks/hooks.json` from an enabled plugin and uses the same Stop block shape. Codex skips plugin hooks until the user reviews and trusts them once in `/hooks`; until then this row works like ChatGPT Work. Live Codex run: NOT_RUN. |
| ChatGPT Work and other hosts without plugin hooks | No hook can stop the reply. Run the gate in the code tool, show its verdict line for each file in the delivery message, and never offer a FAIL or BLOCKED file as ready. The rule is the model's, and the report makes a skipped or failed check visible. |
| claude.ai and Cowork | Whether plugin hooks run there: NOT_RUN. Treat as ChatGPT Work until verified. |

An export folder counts once it holds gate reports or a deliverable changed in
the last 12 hours, so older projects stay quiet. A hook error never traps the
session; it ends the turn with a warning.
