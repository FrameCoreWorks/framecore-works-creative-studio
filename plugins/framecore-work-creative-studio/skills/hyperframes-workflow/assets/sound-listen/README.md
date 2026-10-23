# Sound listening: hear what Studio made

Studio designs sound for films it cannot play. These two tools turn a soundtrack into numbers and a picture, so the film's sound can be judged, fixed and checked against its cuts. They need only Python with NumPy and FFmpeg (Pillow for the sheet) and run anywhere a shell does. They adapt the model-free half of the [earshot](../../../../integrations/earshot/README.md) extension (MIT); the half that needs neural models stays in that extension.

## `listen.py`: measure, time-align, score

```sh
python listen.py measure film.mp4                  # LUFS, LRA, true peak, spectrum, stereo, onsets, tempo, key
python listen.py timeline film.mp4                 # what sounds when, next to the cuts; --video, --cues for a separate track
python listen.py sync film.mp4                     # every cut or cue: has an onset within +-100 ms, offset, or silence
python listen.py critique film.mp4                 # scorecard against launch-film ranges, timed fixes first
python listen.py check hit.wav                     # one sound: clicks, cut tail, clipping, DC offset, pitch glide
python listen.py ab take1.wav take2.wav            # two sounds in numbers and words
python listen.py profile refs/*.mp4 -o refs.json   # your own reference ranges; then critique --profile refs.json
python listen.py sheet film.mp4 -o sheet.png       # an annotated picture: frames, events, spectrogram, loudness, sync
```

- Every command prints a plain summary first; `--json` prints the whole result and `--out f.json` saves it.
- Exit codes: 0 done, 1 a problem was found (`critique`, `check`), 3 bad input, 4 the earshot extension is needed.
- `--cues cues.json` takes times in seconds, `{t}`, `{time}` or `{frame, fps}` objects, or `{cues: [...]}`. For a motion video built from a contract, export the contract's event times and use them as the cues.
- A film with a picture is compared with its own hard cuts; a separate audio file needs `--video` or `--cues`.
- Reading a sheet: pass the PNG to a model that reads images, or open it yourself. It is how an agent "sees" the soundtrack.

### What the numbers mean and where they stop

- LUFS, LRA and true peak follow ITU-R BS.1770 (K-weighting through FFmpeg, true peak on a 4x oversampled signal). Against earshot on the same film they agreed to a few tenths of a unit. Band levels, onset counts and tempo differ by a few dB or a few percent because the detectors differ; earshot is the reference when the two disagree.
- The scorecard ranges come from seven professional launch films earshot measured (SaaS and AI product launch style). They are a useful default for a short product film, a poor one for a meditative film, a documentary or a music video: pass `--profile` with films like yours, or ignore a row that does not fit the genre.
- Nothing here uses a model, so it says what a sound measures like, never what it is ("a door slam"). `describe`, `match`, `rank`, `find`, `compare` and `realness` are the Earshot engine's.
- Optimising for the scorecard alone is Goodhart's law: a film can pass every row and still sound wrong. The numbers find faults (a hit 80 ms late, a silent cut, a harsh mid band); a listener decides taste.

## Place samples on the frames

```sh
python place_sfx.py --video silent.mp4 --cues cues.json --out film.mp4 [--keep-audio | --bed music.wav] [--target-lufs -14] [--ceiling -1] [--stem effects.wav]
```

A cue file lists `t` (seconds) or `frame` (with `fps`), `file`, optional `align` (`onset` the default, `peak`, `start`, `end`), `gain_db`, `pan`, `duck_db` and `label`. The tool measures each sample's attack, shifts it so the chosen point lands on the cue, mixes with the video's own sound or a bed, holds the true peak under the ceiling (a look-ahead limiter, then the encoded file is measured again) and renders every sound alone to confirm it sits within 5 ms of its cue (10 ms for peak alignment, whose measurement uses a 10 ms window). Exit 1 lists the cues that are off time. Use it for samples the user owns or the licence allows; Studio's own designed sound for a video is `sound.py` ([motion sound](../motion-sound/README.md)).

## The Earshot engine for the models and the sound bank

Earshot (v0.4.0) adds the neural commands and its bank of 252 code-made sound effects (`sfx`, `kit`, `forge`, `fit`, `gallery`). It has one route: the `earshot-audio` plugin from this repository, whose `runtime.py` installs the pinned engine after the user agrees, light (measurements, `critique --fast`, `sfx`, `kit`; no models) or full (adds `timeline`, `sheet` and the model commands; CPU PyTorch and about 1.1 GB of models), see the registry entry `earshot` in the [extension registry](../../../workflow-orchestrator/references/extensions.md). `listen.py describe ...` and the other model commands pass through to that engine, offline with its model cache and without API keys; `llm` and `mcp` are refused.

## Verification boundary

Tested with synthetic audio (planted onsets, clipping, cut video) and on a 16.7 s film Studio rendered. Not tested: music-led films, speech-led films, mono sources beyond the synthetic tests, files longer than a few minutes, hosts without FFmpeg.
