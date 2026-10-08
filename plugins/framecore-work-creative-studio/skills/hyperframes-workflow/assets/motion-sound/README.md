# Motion sound design

[`sound.py`](sound.py) gives a motion video a finished sound track, designed for that video, from the same timing as the picture. It reads the [motion contract](../../references/motion-contract-json.md), finds every visible event with the [Python renderer](../motion-render/README.md)'s port of the scene engine (lines, items, captions and cards landing, taps, screen pushes, sweeps, canvas wipes, counter steps, camera moves, the final reveal), analyses what the video is, and designs new sounds and new music for it. Nothing is picked from a set of finished sounds or stored loops: every effect and every part of the music is designed anew for each video and synthesized with code. The method is in [motion sound design](../../references/motion-sound-design.md).

```sh
python sound.py analyze video.motion.json
python sound.py plan video.motion.json --out video-r2.motion.json --table cues.md
python sound.py mix video-r2.motion.json --video video.mp4 --out video-sound.mp4 --wav mix.wav --stems stems
python sound.py check stems/effects.wav video-r2.motion.json
```

- **`analyze`** prints the video's profile, the direction (palette, key, the effects' character) and what was designed, with reasons; nothing is written.
- **`plan`** writes a new revision of the contract with `sfx` (the cue list) and `soundDesign`: `engine` (`studio-generative-1`), `density`, `seed`, `variation`, `direction` (profile, choices, character and the design log), `recipes` (one designed sound per role) and `music` (tempo, key, palette, energy per bar, level, `revealBar` and the composed `recipe`). When the video ends on an end card or logo, the tempo is fitted inside the style's range (or within 8% of its usual tempo) so the reveal falls exactly on a downbeat. `--variation N` designs the same video anew; choices the contract records as set by the user are kept when planning again (after a revision, for example), and `--set ROLE=OPTION` (repeatable, and winning over a recorded choice) fixes a choice: `palette`, `key` (`key="E minor"`), the kind of `landing` (struck, blip, swish, pluck, felt, none), `transition` (air, tonal, whip, flutter, crossing), `impact` (sub-drop, thud, metal-hit, soft), `accent` (bell, fm-bell, glass, chime) or the `lead` instrument family (string, fm, piano, mallet, saw). `--density` is `minimal` (scene changes, sweeps, wipes, taps, final hits), `standard` (also landings, captions, counter ticks, screen pushes, tap releases, accents) or `rich` (also exits, camera moves, a riser and a boom into the final reveal). `--no-music` plans effects only; a supplied `music.src` is always used instead of composing.
- **`mix`** renders every cue from its recipe and the composed music from its recipe (or the supplied track and voice-over; music ducks 8 dB under the caption intervals of a voice-over and dips 1.5 to 5 dB for a moment under clicks, impacts and the final hit), adds a shared room reverb, high-passes, glues the loudest moments with a gentle bus compressor, sets the loudness to −14 LUFS with a true-peak limiter (ceiling −1.5 dBTP, so AAC encoding stays under −1 dBTP), then copies the picture unchanged into the output MP4 with AAC audio, decodes the delivered AAC and measures it: when encoding raised its true peak above −1 dBTP, the master is trimmed by the excess and muxed again (`delivered` in the summary reports the file's own loudness and true peak; no further loudness pass is needed). It checks the timing itself and exits 1 when a hit is off.
- **`check`** measures an effects-only track (`--stems` writes the dry `effects.wav` and `music.wav`): the first sample above half the local peak for transients (within 2 ms), the loudest 10 ms for swells (within 15 ms); risers end on their frame by construction; cues masked by a neighbour are reported, not judged; a cue with no sound above about -80 dBFS in its window is reported as `missing` and fails the check, never counted as on time.

Needs Python 3.8 or newer, numpy and ffmpeg (with `loudnorm` for loudness; otherwise only the peak is set and the summary says so). Every random choice is seeded from the video's content (and the variation), so the same contract always gives the same audio and another video gets another design. Keep `sound.py` with `synth.py`, `music.py`, `recipe.py`, `generate.py`, `compose.py`, `direction.py`, `sound-base.json`, `../motion-render/render.py` and `../motion-styles/styles.json`.

## How a video's sound is made

1. **Analyse.** [`direction.py`](direction.py) reads the style, the motion tempo and easing (an overshoot reads playful), the canvas colour (a dark canvas leans technical), the scene kinds and taps, the pacing and the brief's own words in English or Polish (goal, audience, message, concept, copy), and scores six moods (calm, bold, playful, technical, organic, editorial) and the pace. What it knows is in [`sound-base.json`](sound-base.json): the words, styles, tempos and scene kinds that point to each mood, and which palette fits which moods. It then fixes the direction: the palette (the style's own when the style sets one), a major or minor key with a root drawn from the seed, and the effects' character.
2. **Design the effects.** [`generate.py`](generate.py) designs one new sound per role: transition, landing, press, release, tick, impact, boom, riser and accent. For each it chooses a kind of sound by the moods (better fits are likelier, never certain), then designs it: the material and its resonances (wood, glass, metal, plastic, ceramic, skin, each perturbed), pitches tuned to the key, band paths, envelopes, layers and their balance, inside ranges that keep it at studio standard.
3. **Compose the music.** [`compose.py`](compose.py) writes a new chord progression with a grammar of harmonic functions ending on a chord that leads home, with a colour (triads, sevenths, add9 or sus2); new rhythms for bass, lead, hats, kick and backbeat from Euclidean patterns shaped by energy and pace, with swing; a short motif in the key; new instruments for pad, bass and lead, each designed within the families the style allows (an additive pad, FM keys, a plucked string, a felt piano, mallets, a filtered saw, a rounded bass); and a drum kit designed as recipes (the backbeat on a continuum from a rim or snap to a snare or clap). It decides how the music ends (a struck chord, a rising arpeggio or the motif's cadence).
4. **Check.** Every designed sound passes a quality gate before it is kept: no third of an octave above 150 Hz may hold more than 70 to 85% of its energy (by role), so a near-pure tone, a toy beep or a hollow one-note drum is designed again (up to six times). The design log records each sound's score. The mix then checks timing and loudness.
5. **Record and refine.** The recipes go into the contract with the design log, so the host model or the user can read why each sound is what it is, ask for a variation or fix a choice, or edit a recipe directly; `mix` renders whatever the contract holds.

| Style | Families the composer may use |
| --- | --- |
| Brand-native, none | additive pad; rounded or saw bass; mallet, FM or plucked lead; band kit |
| Meadow | soft additive pad; rounded bass; string, FM or felt piano lead; soft kit with shaker |
| Warm ink | no pad or a soft one; rounded bass; FM or piano lead; tight kit |
| Midnight | bright additive pad; saw bass; saw or FM lead; electronic kit |
| Field guide | soft additive pad; rounded bass; string or mallet lead; organic kit with shaker |
| Paper and ink | soft additive pad; no bass or a rounded one; piano, mallet or FM lead; sparse kit |
| Color block | no pad or an additive one; saw bass; saw, FM or mallet lead; house kit, four on the floor |

Energy per bar works the same in every design: 0 a quiet pad, 1 the core (bass and the main instrument), 2 the moving parts and light percussion, 3 full drums. The bar before the reveal leads in (a backbeat roll and a reversed cymbal, softer for acoustic kits); the reveal lands on the tonic in the video's own instruments and rings out to the end, so the music resolves instead of being cut off. Every design is set to the same level, so a new design never changes the balance against the effects.

## Sound designs

Each cue's `sound` names the role it plays; with a designed video it renders from that role's recipe, fitted to the cue.

| `sound` | Role recipe | Fitted by the cue | Aligned on |
| --- | --- | --- | --- |
| `whoosh` | transition | `duration` (the move's length), `direction`, `intensity` | its measured loudest 10 ms |
| `landing` | landing (or none) | `pitch` steps up for later lines and items | onset, or the measured peak of a swish |
| `click`, `release` | press, release | `pitch` | onset |
| `tick` | tick | `pitch` rises with the count | onset |
| `impact`, `boom` | impact, boom | gain per cue | onset |
| `riser` | riser | `duration` | its end |
| `shimmer` | accent, tuned to the key | `degree` in the scale | onset |

`knock`, `tap`, `pop` and `swish` are the built-in landing designs of earlier versions, kept so older contracts still render.

## Recipes

A recipe is JSON, described in [`recipe.py`](recipe.py): a sound is a list of layers (`tone`, `fm`, `noise`, `modal`, `string`), each with its gain, envelope, optional tremolo, delay, moving pan and filters, plus how the sound aligns (onset, measured peak or end) and the level its role needs. The music recipe in `soundDesign.music.recipe` holds the progression, colour, the three part timbres, the rhythms, the motif, the drum kit recipes and the ending. A contract planned before the generative engine (without `recipes`) still renders with the built-in designs of [`synth.py`](synth.py) and the palettes of [`music.py`](music.py).

## Verification boundary

During package preparation, in a Linux development container with numpy 2.5 and ffmpeg 6.1, the `app-film`, `color-block` and all-kinds examples were planned and mixed with designed sounds and music: every judged hit landed within 2 ms of its frame, the reveal on the music's downbeat within 0.01 ms, loudness was −14.0 to −14.4 LUFS with true peak at most −1.5 dBTP before encoding, a video's effects were designed in about 0.25 seconds and mixes took 9 to 23 seconds for 9 to 23 seconds of video. Over 200 designs for one profile the composer wrote 71 distinct major and 38 distinct minor progressions. Earlier, on 2026-10-07, the owner listened to renders of the built-in designs: music and clicks approved, whooshes lowered by 6 to 7 dB, the knock and the snare rejected as flat and empty; the owner then asked that every video get newly designed sound instead of a fixed set. The 1.33.0 audit had measured and corrected the 1.32.0 mixes (the reveal off the bar grid by up to 0.7 s, an abrupt end, a heavy low end, one example 1.7 dB under the loudness target). How the sound plays in ChatGPT or ChatGPT Work is not verified.
