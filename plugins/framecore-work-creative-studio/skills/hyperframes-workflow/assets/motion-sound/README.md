# Motion sound design

[`sound.py`](sound.py) gives a motion video a finished sound track from the same timing as the picture. It reads the [motion contract](../../references/motion-contract-json.md), finds every visible event with the [Python renderer](../motion-render/README.md)'s port of the scene engine (lines, items, captions and cards landing, taps, screen pushes, sweeps, canvas wipes, counter steps, camera moves) and designs a sound for each with [`synth.py`](synth.py): its hit, a whoosh's peak or a riser's end lands exactly on the frame, and its length follows the move. A music bed is composed by [`music.py`](music.py) to the video's length, in the instruments of the video's style, with energy that follows the scenes. The method is in [motion sound design](../../references/motion-sound-design.md).

```sh
python sound.py plan video.motion.json --out video-r2.motion.json --table cues.md
python sound.py mix video-r2.motion.json --video video.mp4 --out video-sound.mp4 --wav mix.wav --stems stems
python sound.py check stems/effects.wav video-r2.motion.json
```

- **`plan`** writes a new revision of the contract with `sfx` (the cue list) and `soundDesign` (`engine`, `density`, `status` and the composed `music`: tempo, key, `palette`, `progression`, `seed`, energy per bar, level). When the video ends on an end card or logo, the tempo is fitted within 8% of the style's so the reveal falls exactly on a downbeat (`revealBar`, `revealFrame`). `--density` is `minimal` (scene changes, sweeps, wipes, taps, final hits), `standard` (also landings, captions, counter ticks, screen pushes, tap releases, accents) or `rich` (also exits, camera moves, a riser and a boom into the final reveal). `--palette` picks a music palette other than the style's own (for example `studio`); `--no-music` plans effects only; a supplied `music.src` is always used instead of composing. The cues are a starting point and stay editable.
- **`mix`** renders the effects and the music (or the supplied track and voice-over; music ducks 8 dB under the caption intervals of a voice-over and dips 1.5 to 5 dB for a moment under clicks, impacts and the final hit), adds a shared room reverb, high-passes, glues the loudest moments with a gentle bus compressor, sets the loudness to −14 LUFS with a true-peak limiter (ceiling −1.5 dBTP, so AAC encoding stays under −1 dBTP), then copies the picture unchanged into the output MP4 with AAC audio. It checks the timing itself (transients on a track without whooshes, whooshes on a track without transients) and exits 1 when a hit is off.
- **`check`** measures an effects-only track (`--stems` writes the dry `effects.wav` and `music.wav`): the first sample above half the local peak for transients (within 2 ms), the loudest 10 ms for whooshes (within 15 ms); risers end on their frame by construction; cues masked by a neighbour are reported, not judged.

Needs Python 3.8 or newer, numpy and ffmpeg (with `loudnorm` for loudness; otherwise only the peak is set and the summary says so). Every random source is seeded, so the same contract always gives the same audio. Keep `sound.py` with `synth.py`, `music.py`, `../motion-render/render.py` and `../motion-styles/styles.json`.

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

## Music palettes

The bed is played in the palette of the contract's [style](../motion-styles/README.md), following the music texture that style describes; tempo stays inside the style's range when a tempo there puts the reveal on a downbeat (otherwise within 8% of the style's usual tempo), and the key follows its mood (A minor for Midnight, Warm ink and Brand-native, D major otherwise).

| Palette | Styles | Instruments |
| --- | --- | --- |
| `studio` | Brand-native and any other | warm pad of three detuned voices with slowly breathing brightness, rounded bass, plucked arpeggio, kick, snare and clap, swung sixteenth hats |
| `meadow` | Meadow | nylon guitar picking (plucked-string synthesis, tuned exactly), Rhodes chords with sevenths, soft pad, shaker, brushes and a felt kick |
| `warm-ink` | Warm ink | muted electric-piano comping, soft electric bass, tight dry kick, rim and closed hats |
| `midnight` | Midnight | wide synth pad, filtered saw bass in eighths, sixteenth synth arpeggio, deep kick, clap and hats |
| `field-guide` | Field guide | strummed acoustic guitar, soft pad, shaker sixteenths, rim and a light kick |
| `paper-and-ink` | Paper and ink | sparse felt piano (stretched partials, two detuned strings, hammer) with space for the words, a quiet pad, almost no drums |
| `color-block` | Color block | house chord stabs, off-beat saw bass, four-on-the-floor kick, clap and open hats |

Each palette plays energy 0 as a quiet pad, 1 as its core (bass and the main instrument), 2 with its moving parts and light percussion, 3 with full drums. The progression is one of four loops per mode (for example I–V–vi–IV or i–VI–III–VII), chosen from the video's own content, so different videos do not share one bed; chords are voiced so the upper voices move as little as possible. The bar before the reveal closes the loop and leads in (a snare fill and a reversed cymbal, or a shaker build and a swell for the acoustic palettes); the reveal lands on the tonic in the palette's instruments and rings out to the end, so the music resolves instead of being cut off. Every palette is set to the same level, so a change of style never changes the balance against the effects. A beat grid the picture was cut to (`music.bpm`) is kept as it is.

## Verification boundary

During package preparation, in a Linux development container with numpy 2.5 and ffmpeg 6.1, the `app-film`, `color-block` and all-kinds examples were planned and mixed: every judged hit landed within 2 ms of its frame, the reveal on the music's downbeat within 0.01 ms, loudness was −14.0 LUFS (−13.8 to −14.1 measured in the AAC files) with true peak at most −1.3 dBTP, and mixes took 8 to 18 seconds for 9 to 23 seconds of video. The owner listened to the first renders on 2026-10-07: music and clicks approved, whooshes too strong; whooshes were then lowered by 6 to 7 dB and softened. A later audit (1.33.0) measured the 1.32.0 mixes and corrected what it found: the reveal was up to 0.7 s off the music's bar grid, the music stopped abruptly at the end, the low end held about 44% of the energy, and the true-peak trim after a sample-peak limiter left one example 1.7 dB under the loudness target. How the sound plays in ChatGPT or ChatGPT Work is not verified.
