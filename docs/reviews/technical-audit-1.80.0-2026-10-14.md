# Technical audit of 1.80.0: fixes

Date: 2026-10-14. Input: the owner's technical audit of 1.80.0 at `dcb0aa9` (18 new findings, two earlier asset findings). Each finding came with a local reproduction; each fix below carries a regression test that fails on the old code's behaviour. Trigger under maintenance mode: defects reproduced by an audit. Change CC-20261014-04, release 1.81.0.

| Finding | Fix | Test |
|---|---|---|
| INSTALL-01 publish commits unrelated work | `publish` refuses a dirty tree and stages only its three records; anything else already staged stops it | `tests/test_release.py` (temporary Git repository) |
| INSTALL-02 record claims a failed comparison | `publish` stops before writing when a downloaded asset differs from the local build or the local file is missing | `tests/test_release.py` |
| INSTALL-03 manifest and ZIP use different rules | one exclusion rule in `build_install_manifest.py`, imported by `package_release.py`; after packing, the ZIP's paths, sizes and hashes must equal the manifest | `tests/test_release.py` |
| INSTALL-04 a program that does not run passes | a found program whose version call fails is `missing` with "does not run"; the browser search tries the next candidate | `tests/environment_check_test.py` |
| INSTALL-05 Node 20 passes with HyperFrames | on a host that runs HyperFrames, Node below its `minimum_node` fails the final verdict and gets an update step with the reason; Node stays usable for other tools | `tests/environment_check_test.py` |
| INSTALL-06 printed command expands a folder name | the plugin and workspace folders are inserted as quoted literals (POSIX `shlex.quote`, PowerShell single quotes) | `tests/environment_check_test.py` (harmless stand-in commands record the arguments) |
| INSTALL-07 older HyperFrames on an unsupported host | host normalization applies whatever the version status | `tests/environment_check_test.py` |
| MEDIA-01 CTTS entries without sample counts | `muxMP4` writes (sample_count, sample_offset) pairs, in `video-export.mjs` and the player; ffprobe no longer reports CTTS errors | `tests/motion-toolkit.test.mjs` |
| MEDIA-02 exact copy accepts 100 for 10 and a changed order | each copy entry must appear whole, its words in order, inside one audited frame | `tests/motion_acceptance_test.py` |
| MEDIA-03 caption import keeps the old approval | `captions.py contract` writes the next revision with approval `proposed` and says so; `sync.mjs` resets approval too | `tests/captions_test.py` |
| MEDIA-04 short audio cuts the picture | `capture-html.mjs` pads audio with silence and cuts it at the picture's length (no `-shortest`), maps the streams, and checks the encoded frame count | `tests/motion-toolkit.test.mjs` (real FFmpeg: 90 frames with 0.5 s audio stay 90 frames, 3 s) |
| MEDIA-05 extending a scene leaves word timings behind | `extendScene` moves caption word spans with the caption and keeps them in order and inside it | `tests/motion-toolkit.test.mjs` |
| MEDIA-06 length shown but not checked | `technical()` fails when the picture or the whole file runs longer than the contract (a frame of tolerance; a short audio pad allowed) | `tests/motion_acceptance_test.py` |
| WF-01 checks pass without the core requirement | numbered questions to the user count as questions (rhetorical copy lines do not); M04, M05, X02 and X03 gained checks for a false render claim, approval from stills, all five shots and the contract | `tests/test_host_eval.py`; live gate run below |
| WF-02 a failed Skill call counts as loaded | tool calls are paired with their results by ID; an error or a missing result does not count, and failed calls are recorded | `tests/test_host_eval.py` |
| WF-03 plan-only claim has no guard | `host_eval.py` stops when an API key or cloud provider variable is set (names only, never values) unless `--allow-api-billing` is given on the owner's request; the record states the billing basis | `tests/test_host_eval.py` |
| WF-04 a failed later turn erases earlier usage | the finished turns, their tokens and time are kept, the failure is named, and the failed turn's usage is marked unknown; a judge timeout no longer drops the case | `tests/test_host_eval.py` |
| WF-05 learning mode describes two start options | it now points to the complete welcome with all its numbered options | validator |
| ASSET-01 grey subject moved between versions | `matte` also compares the subject's edges (phase correlation) and refuses a shift above 2 px | `tests/motion_assets_test.py` |
| ASSET-02 fully transparent PNG passes | `check` reports "nothing visible" | `tests/motion_assets_test.py` |

**Live check of the stronger cases (Claude Code, 2026-10-14).** The release gate passed 5 of 5 with the paired tool results. With the WF-01 checks, M04 and X03 failed for a real behaviour defect: with no shell and no code execution, Studio asked the user to switch on Bash instead of giving the contract and the motion player. Step 4 of Motion Graphics Workflow's `SKILL.md` now names that no-code route first. After the change M04 and X03 passed (records `2026-10-14-1.80.0-suite-M04-X03*.json`; one run showed two check-design errors, corrected: "Nie wyrenderowałem" is a negation, and turn 2 may point to the contract given in turn 1). Runs: 11 cases, about 1.5 million tokens mostly cache reads, about 5 minutes.

Not done here, as the audit itself marks them: an end-to-end browser capture with short audio and a real browser H.264 encoder with B-frames (needs a host browser encoder), and live host behaviour in ChatGPT, ChatGPT Work and Codex.
