# Motion quality helpers

These original, dependency-free adapter functions extend the existing frame contract. They neither install packages nor implement a second renderer. Copy into the authorized project before using them. Run score logic with Node; browser/render integrations need the actual installed runtime.

`python3 inspect-encode.py existing-local-video.mp4 new-review-directory` uses existing FFmpeg/ffprobe to read decoded metadata, sample up to 30 frames including endpoints, and write a contact sheet plus hash-linked evidence. It refuses an existing destination and accepts no remote input. This is an inspection helper, not a downloader or renderer. Supplement uniform samples with the score's boundary/hold frames and full playback. Its report deliberately leaves visual, temporal and listening results `not_run` for the reviewer.

- `validateScore(score)`: rational FPS, scene coverage, readable holds and finite sound-cue intervals.
- `secondsAtFrame(frame,score)`: master time conversion.
- `reviewFrames(score)`: first/last, uniform samples, neighboring boundary frames, readable holds and cue contacts. Sampling does not certify the entire film.
- `cueTimes(score)`: sound-event seconds from the same master frames.
- `renderPaperFrame(mount,frame,score)`: stop Paper playback, set its time in milliseconds. Await actual renderer completion separately.
- `renderToneCues(Tone,score)`: synthesize sine accents into an offline stereo buffer using injected Tone. Cue duration includes the release tail. No Transport, network, provider or autoplay.

Example score is synthetic and not approved client content. Overlap layer/blend ownership remains in the storyboard. A structurally valid score does not prove design quality or audible sync.

## Optional libraries

Paper Shaders 0.0.81: use the installed package's real ShaderMount setup and verified API. Versions from 0.0.77 use Apache-2.0; preserve LICENSE/NOTICE if shipping library code. The adapter vendors no library code. Set dimensions, seed and all uniforms explicitly. A feedback simulation may require fixed prerendering, not arbitrary seeking.

Tone.js 15.1.22: MIT. Inject an already authorized installation. Offline returns a ToneAudioBuffer; use its actual channel data with the project's existing WAV/container writer and muxer. This helper supplies sound accents, not a composed score. Check clipping from overlapping voices and listen to the actual mix.

No Paper/Tone installation or live runtime test is implied by helper unit tests. Mocks verify unit conversion/scheduling, not GPU drawing or audio quality. Record current API/version, initialization, direct/backward seeks and encoded sync in the existing QA record.
