# Motion quality helpers

These original, dependency-free adapter functions extend the existing frame contract. They neither install packages nor implement a second renderer. Copy into the authorized project before using them. Run score logic with Node; browser/render integrations need the actual installed runtime.

`python3 inspect-encode.py existing-local-video.mp4 new-review-directory` uses existing FFmpeg/ffprobe to read decoded metadata, sample up to 30 frames including endpoints, and write a contact sheet plus hash-linked evidence. It refuses an existing destination and accepts no remote input. This is an inspection helper, not a downloader or renderer. Supplement uniform samples with the score's boundary/hold frames and full playback. Its report deliberately leaves visual, temporal and listening results `not_run` for the reviewer. Two optional checks are recorded in `evidence.json` and exit 1 when they fail: `--audio required` (an audio stream whose peak is above -80 dB, measured with ffmpeg `volumedetect`) or `--audio silent` (nothing audible), and `--cover-time SECONDS` (that exact frame saved as `cover.png`; a time outside the film is refused before anything is written). They prove presence and position, not that the sound or cover is right.

- `validateScore(score)`: rational FPS, scene coverage, readable holds and finite sound-cue intervals.
- `secondsAtFrame(frame,score)`: master time conversion.
- `reviewFrames(score)`: first/last, uniform samples, neighboring boundary frames, readable holds, cue contacts and the start, middle and end of each caption. Sampling does not certify the entire film.
- `cueTimes(score)`: sound-event seconds from the same master frames.
- `renderPaperFrame(mount,frame,score)`: stop Paper playback, set its time in milliseconds. Await actual renderer completion separately.
- `renderToneCues(Tone,score)`: synthesize sine accents into an offline stereo buffer using injected Tone. Cue duration includes the release tail. No Transport, network, provider or autoplay.

Example score is synthetic and not approved client content. Overlap layer/blend ownership remains in the storyboard. A structurally valid score does not prove design quality or audible sync.

## Motion activity

[`motion_activity.py`](motion_activity.py) samples a rendered video at 6 frames per second and reports the share of still time and the longest still stretch outside declared holds. It fails (REVISE, exit code 1) above 40 % undeclared still time or with an undeclared still longer than 2.5 s; `--hold START-END` declares an intended still such as the end card, `--json` prints the report, with the video's `video_sha256` so `acceptance.py --motion-activity` can bind it to the delivered file. It measures pixels, not meaning: a slow drift counts as motion. Needs Python 3.8+, numpy and ffmpeg.

```sh
python3 motion_activity.py film.mp4 --hold 27-30
```

On 2026-10-12 it returned REVISE for the 6-second film reviewed on 2026-10-11 (83 % still, a 4.7 s still), PASS for a reference client reel (20 % still) and PASS for a HyperFrames example render (35 % still); `tests/motion_activity_test.py` covers moving, still and mixed videos and declared holds.

[`flash_check.py`](flash_check.py) screens a rendered video for photosensitivity risk. It samples at 30 frames per second (`--fps` 24 to 30; the 6 fps of the activity check is too slow for flicker), converts each frame to relative luminance and counts flashes: pairs of opposing changes of at least 0.10 whose darker side is below 0.80, over at least a quarter of the frame. More than 3 flashes in any one-second window fails (REVISE, exit code 1) and the report names that second; `--json` adds `video_sha256`. It is screening, not WCAG, Harding or broadcast conformance: it does not judge saturated red flashes or patterns. Run it on any render with beat-driven brightness, strobes or flash cuts. `tests/flash_check_test.py` covers fast and slow flicker, a fade, a small area and bright-only flicker.

```sh
python3 flash_check.py film.mp4 --json
```

## Optional libraries

Paper Shaders 0.0.81: use the installed package's real ShaderMount setup and verified API. Versions from 0.0.77 use Apache-2.0; preserve LICENSE/NOTICE if shipping library code. The adapter vendors no library code. Set dimensions, seed and all uniforms explicitly. A feedback simulation may require fixed prerendering, not arbitrary seeking.

Tone.js 15.1.22: MIT. Inject an already authorized installation. Offline returns a ToneAudioBuffer; use its actual channel data with the project's existing WAV/container writer and muxer. This helper supplies sound accents for sync tests, not a composed score, and its tones are never delivered as a project's sound. Check clipping from overlapping voices and listen to the actual mix.

No Paper/Tone installation or live runtime test is implied by helper unit tests. Mocks verify unit conversion/scheduling, not GPU drawing or audio quality. Record current API/version, initialization, direct/backward seeks and encoded sync in the existing QA record.
