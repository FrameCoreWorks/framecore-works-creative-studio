# Motion sound design

[`sound.py`](sound.py) gives a motion video its sound design from the same timing as the picture. It reads the [motion contract](../../references/motion-contract-json.md), finds every visible event (a line or item landing, a card settling, a tap, a screen push, a sweep, a canvas wipe, a counter step) with the [Python renderer](../motion-render/README.md)'s port of the scene engine, and puts a recorded sound on it so that the sound's transient, or a whoosh's loudest moment, falls exactly on that frame. The method is in [motion sound design](../../references/motion-sound-design.md).

```sh
python sound.py plan video.motion.json --out video-r2.motion.json --table cues.md
python sound.py mix video-r2.motion.json --video video.mp4 --out video-sound.mp4 --wav mix.wav
python sound.py check mix.wav video-r2.motion.json
```

- **`plan`** writes a new revision of the contract with `sfx` (the cue list) and `soundDesign` (`library`, `density`, `status`), and optionally a Markdown cue table. `--density` is `minimal` (scene changes, sweeps, wipes, taps, final hits), `standard` (also lines, items, captions, counter ticks, screen pushes, tap releases) or `rich` (also exits, camera moves, accents on end cards and logos). The cues are a starting point: edit, remove or add entries by hand; `sound` can be a family or a sound ID from `library.json`.
- **`mix`** places every cue, adds `music.src` and `voiceover.src` from next to the contract (the music ducks 8 dB under the caption intervals when there is a voice-over), sets the loudness to −16 LUFS without passing −1.5 dBTP (a sound-effects-only mix stays quieter, limited by its loudest hit), writes a 48 kHz WAV and copies the picture unchanged into the output MP4 with AAC audio.
- **`check`** measures where each cue's hit landed in a mix (the first sample above half the local peak, or a whoosh's loudest 10 ms) and fails when one is more than 2 ms (10 ms for whooshes) from its frame. Cues within 50 ms of another are reported as masked rather than judged.

It needs Python 3.8 or newer and ffmpeg (with `loudnorm` for loudness; otherwise it normalizes the sample peak and says so). There are no Python packages and no randomness: variants of a family are used in turn, so the same contract always gives the same mix. Keep `sound.py` with `library.json`, `library/` and `../motion-render/render.py`.

## Library

`library.json` lists 79 recordings in nine families. [`build_library.py`](build_library.py) measures them (duration, transient, loudest moment, level around it, SHA-256); `--check` confirms the file is current.

| Family | Use | Sounds |
| --- | --- | --- |
| `whoosh` | scene changes, sweeps, wipes, screen pushes, camera moves | 13 swishes of swung wood and metal |
| `thud` | end cards, logos, a device or heavy result settling | 10 soft low impacts |
| `knock` | a line, card, caption or item landing | 10 light and medium wood knocks |
| `ting` | a final value, a highlight, an accent on a reveal | 15 light glass, metal and plate impacts |
| `click` | a tap, a button press | 11 mechanical clicks |
| `release` | the release of a press, a few frames after the click | 1 mouse release |
| `tick` | counter steps, fast repeated steps | 3 ticks |
| `switch` | a state change, a fade between screens | 11 switches and toggles |
| `scroll` | scrolling or a growing connector | 5 scroll-wheel ratchets |

Every file is an unchanged recording released under CC0 by Kenney or by artisticdude on OpenGameArt; see [the sources](../../../../integrations/motion-sound-sources/README.md). Synthetic interface tones (confirmations, errors, bleeps, plucks) were left out on purpose: they make a product video sound like a game. The library is small and dry; it is a base layer, not a replacement for music or a sound designer's own library.

## Verification boundary

During package preparation, in a Linux development container with ffmpeg 6.1: plans for the `app-film`, `color-block`, `two-statements` and all-kinds examples were mixed and checked. Every unmasked hit landed within 0.06 ms of its frame (whooshes within 5 ms, measured to their loudest 10 ms), also after AAC encoding into the MP4. How the mixes sound has not been judged by listening in this environment; the owner's listening decides.
