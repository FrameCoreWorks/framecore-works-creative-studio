# MoneyPrinterTurbo: decision map

Reviewed 2026-10-22 at [`6992380`](https://github.com/harry0703/MoneyPrinterTurbo/tree/6992380c5e82f07f3e1fc46b90927b6f1c655407) (package `mpt` 1.3.9 on PyPI, MIT, [licence](LICENSE)) after the owner sent the repository. No code or text is copied into Studio.

| Part | Decision | Reason |
| --- | --- | --- |
| Topic or script to a finished short video (LLM script, stock footage, voice-over, subtitles, music, composition) | extension | A different job from Studio's: automatic, stock-footage-led shorts. Studio keeps the brief, script, claims and review, and sends edits of the user's own footage to FrameCut and designed motion to Motion Graphics Workflow |
| CLI with a JSON result and exit codes, WebUI | extension | `mpt cli` is the agent-friendly route; the WebUI listens on 127.0.0.1 |
| REST API server (`main.py`) | extension with a warning | Listens on 0.0.0.0 by default and has no sign-in: start it only with a loopback `listen_host` |
| Local footage plus the user's own narration (offline route) | extension | Runs without keys and is the safe first check |
| Paid AI clip providers (Seedance, WaveSpeed, OFox, MiniMax H3 and others) | extension, ask first | Each generated clip is a paid task. The project's own skill asks for an explicit charge flag; Studio asks before any paid generation as well |
| Bundled background songs | reject | The README says they come from YouTube videos and asks users to delete them if there are copyright issues. Use no music or licensed music |
| The project's agent skill (`docs/skill`) | reject for Studio | It installs without asking, pipes a downloader into the shell for `uv`, fetches its helper from the `main` branch unpinned and reads the whole `config.toml`. Studio installs only on the user's explicit request, from a pinned version, after a dry run |
| Sponsor and referral links in the README | reject | Not endorsements |

## Methods adapted into FrameCut (2026-10-22 code review)

A read-only review of its code (nothing was run) found little editing intelligence to adopt: footage is cut into fixed slices, shuffled and given random transitions. What Studio took are methods, written originally; no code or text is copied.

| Idea | Decision |
| --- | --- |
| Correct subtitles against the known script | adapted as `align-script`: word-level alignment with a coverage report instead of its greedy line merge, which writes the script line whatever the similarity and pads missing lines with zero timings |
| Break cues at punctuation and never end a line on a one-letter word | already in Caption Studio; FrameCut's cue grouping now uses it |
| Check that the subtitle font can draw the text | adapted as the blocking `font_missing_glyphs` warning (Polish letters are the common case) |
| BT.709 tagging of piped frames | already correct: a render of a known colour measured within two levels of its source |
| Stage-level fingerprints and a rebuild plan | FrameCut already caches stages by fingerprint; a `plan` that explains rebuilds is a possible later item |
| Needs-input exit code, spend-approval gate, hash-verified revisions | noted; FrameCut has no paid provider yet, so no gate |
| Pause tags with sample-accurate voice-over offsets, source-fitness checks, coverage ledger | noted for later, with the owner |

Not adopted: random shuffle and transitions, silent looping of short footage, black-bar fitting, three generations of re-encoding, hiding script mismatches, and its agent skill's silent install and credential reuse.

Registry entry: `moneyprinterturbo` in [extensions.json](../../skills/workflow-orchestrator/assets/extensions/extensions.json). Evidence: static review, published-file and source comparison, the dry-run plan (`Would install mpt-1.3.9`) and a successful install into a fresh virtual environment. The program was not run (the container blocked executing the downloaded package), so its CLI and offline generation are NOT_RUN.
