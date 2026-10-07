# Motion sound design

[`sound.py`](sound.py) gives a motion video a finished sound track from the same timing as the picture. It reads the [motion contract](../../references/motion-contract-json.md), finds every visible event with the [Python renderer](../motion-render/README.md)'s port of the scene engine (lines, items, captions and cards landing, taps, screen pushes, sweeps, canvas wipes, counter steps, camera moves) and designs a sound for each with [`synth.py`](synth.py): its hit, a whoosh's peak or a riser's end lands exactly on the frame, and its length follows the move. A music bed is composed to the video's length with energy that follows the scenes. The method is in [motion sound design](../../references/motion-sound-design.md).

```sh
python sound.py plan video.motion.json --out video-r2.motion.json --table cues.md
python sound.py mix video-r2.motion.json --video video.mp4 --out video-sound.mp4 --wav mix.wav --stems stems
python sound.py check stems/effects.wav video-r2.motion.json
```

- **`plan`** writes a new revision of the contract with `sfx` (the cue list) and `soundDesign` (`engine`, `density`, `status` and the composed `music`: tempo, key, energy per bar, level). `--density` is `minimal` (scene changes, sweeps, wipes, taps, final hits), `standard` (also landings, captions, counter ticks, screen pushes, tap releases, accents) or `rich` (also exits, camera moves, a riser and a boom into the final reveal). `--no-music` plans effects only; a supplied `music.src` is always used instead of composing. The cues are a starting point and stay editable.
- **`mix`** renders the effects and the music (or the supplied track and voice-over; music ducks 8 dB under the caption intervals of a voice-over), adds a shared room reverb, high-passes, limits and sets the loudness to −14 LUFS with true peak at most −1 dBTP, then copies the picture unchanged into the output MP4 with AAC audio. It checks the timing itself (transients on a track without whooshes, whooshes on a track without transients) and exits 1 when a hit is off.
- **`check`** measures an effects-only track (`--stems` writes one): the first sample above half the local peak for transients (within 2 ms), the loudest 10 ms for whooshes (within 15 ms); risers end on their frame by construction; cues masked by a neighbour are reported, not judged.

Needs Python 3.8 or newer, numpy and ffmpeg (with `loudnorm` for loudness; otherwise only the peak is set and the summary says so). Every random source is seeded, so the same contract always gives the same audio. Keep `sound.py` with `synth.py` and `../motion-render/render.py`.

## Sound designs

| Design | Built from | Aligned on |
| --- | --- | --- |
| `whoosh` | pink and brown noise through a band that brightens to the peak and darkens, an air layer and a faint tone, panned with the move; `duration`, `peak`, `direction`, `brightness`, `intensity` | its loudest 10 ms, measured |
| `impact` | a sub tone falling from about 150 to 50 Hz, a filtered noise body and a short bright transient, saturated together; `weight`, `brightness` | onset |
| `boom` | a heavy impact with a long sub tail, once per video for the final reveal | onset |
| `riser` | noise through a climbing band and a tone gliding up an octave, swelling to its end; `duration` | its end |
| `click`, `release` | a 1 ms excitation ringing stiff high modes and a short low body (modal synthesis); `pitch`, `softness` | onset |
| `tick` | a smaller, drier click for counters; `pitch` rises with the count | onset |
| `knock` | low inharmonic wood modes; `pitch` steps up for later lines and items | onset |
| `shimmer` | bell partials tuned to the music's key, slightly detuned left and right; `degree` in the scale | onset |

The music bed plays a four-chord progression in the planned key: a warm pad and bass at energy 1, a plucked arpeggio and hats at 2, kick and clap at 3 with the pad ducking under the kick. Tempo and key follow the contract's music grid or [style](../motion-styles/README.md) (for example Midnight 122 BPM in A minor, Meadow 100 BPM in D major); energy rises through the middle scenes and peaks into the final card.

## Verification boundary

During package preparation, in a Linux development container with numpy 2.5 and ffmpeg 6.1, the `app-film`, `color-block` and all-kinds examples were planned and mixed: every judged hit landed within 2 ms of its frame, loudness was −14.1 to −15.7 LUFS and true peak at most −1.05 dBTP, and a 13-second mix took 6 to 13 seconds. The owner listened to the first renders on 2026-10-07: music and clicks approved, whooshes too strong; whooshes were then lowered by 6 to 7 dB and softened. How the sound plays in ChatGPT or ChatGPT Work is not verified.
