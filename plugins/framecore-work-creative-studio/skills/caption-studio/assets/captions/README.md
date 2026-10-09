# Captions tool

[`captions.py`](captions.py) checks, converts and builds caption files, imports them into a motion contract and burns them into a supplied video. It turns the [readability defaults](../../references/readability-defaults.md) into checks a host can run.

```sh
python captions.py check captions.srt --profile social --language pl
python captions.py convert captions.srt --to vtt --out captions.vtt
python captions.py build --words words.json --to srt --out captions.srt --profile social --language pl
python captions.py build --segments segments.json --to vtt --out captions.vtt
python captions.py contract captions.srt video.motion.json --out video-r2.motion.json
python captions.py burn video.mp4 captions.srt --out video-captioned.mp4
```

`check`, `convert`, `build` and `contract` need only Python 3.8 or newer. `burn` also needs Pillow and ffmpeg with ffprobe, and the [motion renderer](../../../hyperframes-workflow/assets/motion-render/README.md) (`render.py`), which it finds in the Motion Graphics Workflow or next to `captions.py`; copy both into a sandbox. Every command refuses to overwrite a file. Exit codes: 0 without errors, 1 with errors, 2 when an input cannot be read or a tool is missing.

## Profiles

| Profile | Use | Reading speed | Duration | Limits break as |
| --- | --- | --- | --- | --- |
| `subtitles` | Dialogue, translation and accessibility subtitles | English 20, Polish 17 characters per second (children 17 and 13) | 5/6 s to 7 s | errors |
| `social` (default) | Captions burned into a short-form video and timed to its speech | the same limits | the same limits | warnings: the speech sets the pace |
| `text` | On-screen text with no speech to follow: supers, motion captions | Studio's readable hold: the longer of 13 characters per second plus 0.5 s and 0.5 s plus a third of a second per word, at least 1 s | the hold | warnings |

Every profile allows at most two lines of 42 characters, rejects overlapping cues and flags a gap under two frames, which reads as a flicker. A line that ends on an article, a short preposition or conjunction, or a one-letter Polish word is flagged. Another language than English or Polish is checked without a reading speed, and the report says that limit is Unknown.

## Building from timing

`build --words` takes timed words, as speech-to-text tools write them: a list, or `{"words": [...]}`, of `{"word" or "text", "start", "end"}` in seconds. A cue closes at a sentence end, after a comma once it holds half its length, at a pause of 0.7 s or more, or before it would pass one line (`social` and `text`) or two lines (`subtitles`); a cue that grows too long ends at its last punctuation or before a word that may start a line. End times then extend toward the profile's duration without crossing the next cue, and gaps under two frames close. `build --segments` takes `{"start", "end", "text"}` segments and splits one that cannot fit two lines, sharing its time by length. The written file is checked with the same profile and the report is printed.

## Into a motion video or a supplied video

- **A motion video Studio renders:** `contract` imports the cues into the contract exactly as the [motion sync tool](../../../hyperframes-workflow/assets/motion-sync/README.md) does (the same frames, copy IDs and warnings; a test compares the two), and the renderer draws them.
- **A supplied video:** `burn` draws each caption on the frames it covers with the motion renderer's caption style (`--size` at 1080 px on the short side, `--bottom` as a share of the height, 0.14 by default to stay above a 9:16 feed's controls, `--background`, `--color`, `--font`) and re-encodes the picture as H.264; the source audio is copied unchanged. Watch the result before calling it final: the tool measures frames, not legibility on a phone.

## Verification boundary

During package preparation, in a Linux container with Python 3.13, Pillow 12 and ffmpeg 6.1, the tests in `tests/captions_test.py` checked the file formats, every limit, building from Polish word timings, the contract import against `sync.mjs` and a burn-in on a synthetic video (captions only inside their cues, audio kept). No host run is recorded.
