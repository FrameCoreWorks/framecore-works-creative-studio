# Sound listening and motion SFX craft

Read when a film's sound has to be judged, fixed or checked against its picture, or when effects for a motion film are designed or placed. Studio cannot play audio, so it measures. The tools are in [sound listening](../assets/sound-listen/README.md); this page says when to use them and what good looks like. The targets restate a measured study of eight professional launch films done for the [earshot](../../../integrations/earshot/README.md) extension (one film supplied most of the clean examples, so read them as ranges from real work, not statistics).

## The listening loop

1. **Render the sound, then listen to it with numbers.** After `sound.py mix` or `place_sfx.py`, run `listen.py critique film.mp4` and `listen.py sync film.mp4`. Read the fix list first, then the rows marked high, low or silent.
2. **Look at the sheet** (`listen.py sheet`) when a number is surprising: a missing hit shows as a gap under a cut, a harsh band as a bright stripe, a late hit as a marker beside the cut.
3. **Fix the cause, not the row.** A late hit is a cue time or an alignment point, a silent cut is a missing cue, a harsh mid band is the loudest layer, clipping is gain staging. Rerun after each fix.
4. **Check single sounds before placing them** with `listen.py check`: clicks at the start or end, a tail cut by a gate, DC offset, a pitch glide where a tone should hold.
5. **State what was and was not measured.** Timing, loudness, peaks and balance are measured; taste, genre fit and whether a sound "feels right" are not. Say so in the delivery note.

## Where sound sits against the picture

- **Hits start early, peak on the cut.** Impacts, taps and clicks that start 30 to 200 ms before the cut with the loudest point within about 80 ms of it read as synchronised; a sound that starts on the cut reads late. `place_sfx.py` aligns the attack (`onset`), the loudest point (`peak`) or the end (`end`) to the cue, so choose by what must meet the picture.
- **Risers, zips up and glitches end on the cut** (within 20 ms) and hand over to the next sound; the hit or whoosh that follows blooms just after it.
- **A whoosh straddles the cut**: its peak within about 150 ms either side.
- **Element pop-ins land 25 to 40 ms after the picture event** when they are fired in a run (about every 200 ms in the studied film).
- **Not every cut needs a sound.** Six of the eight studied films let music or voice carry the cut rhythm and put designed effects on a few chosen moments. About half the cuts with a sound onset nearby is normal; a sound on every cut is a rhythm of its own and is chosen, not defaulted. Silence between ideas is a tool (the effects-only film dropped to silence a dozen times).
- **Levels over music:** accents about 13 to 17 dB over the quiet bed between beats, tonal sweeps 7 to 9 dB, a whoosh up to about 20 dB. Over a voice-over, effects stay under the voice; carve with the duck cues.
- **Supplied library samples** are often mastered to peak near 0 dBFS, so never place one at full level: start about 6 to 10 dB down (a gain of 0.3 to 0.5), and 9 to 12 dB down under a voice-over, then set the level by the targets above. One sound per visual event; the same sample at most twice in a film; never an impact and a riser's end stacked on one frame unless the riser hands over to that impact; leave the key spoken word clear of effects. When an effect is the first thing heard in a passage, it is too loud. Adapted from social-motion-agent's library rules (MIT); no samples are bundled or copied.

## What designed effects are made of

One gesture per sound, usually a pitch move or a gate, band-limited on purpose, with a hard end for short interface sounds.

| Sound | Length | Recipe in words |
| --- | --- | --- |
| Whoosh into a cut | 0.5 to 1 s | a low swell with most energy under 150 Hz, the centre of the spectrum falling about two octaves across the pass, a faint air layer 20 to 30 dB down, mono |
| Riser | 0.8 to 1.5 s | a rising tonal layer (about two octaves), a gate pulsing 40 to 50 times a second and speeding up toward the cut, a low drone; the rise is slow at first and fast in the last third |
| Impact | 0.6 to 1.3 s | a broadband transient, a sub body under 150 Hz that peaks 50 to 290 ms later, a textured tail (grains every 25 to 35 ms) ended by a gate |
| Sub drop | 0.8 to 1.5 s | a tone falling roughly 64 to 44 Hz that blooms 0.3 to 0.4 s after the cut, narrow stereo |
| Logo sting | 0.8 to 1.5 s | a fast falling chirp (about 1.5 kHz to 150 Hz in under 100 ms) landing on a low hum that rings about a second |
| Glitch | 0.4 to 0.8 s | crackle, then bursts every 32 ms speeding to 22 ms, bright, fully wide, ending on the cut |
| Shimmer | 1.5 to 2.5 s | grains every 15 to 25 ms over one steady tone, wide and moving |
| Notification ding | 0.2 to 0.4 s | a struck tone near 2 kHz with one inharmonic partial around 3.4 times higher, nothing under 500 Hz, stops short; each ding in a run steps up a semitone |
| Pop | 0.05 to 0.15 s | a sine falling about five octaves in 110 ms, or a gated 1 to 1.5 kHz blip |
| Pop-in (an element appearing) | 0.14 to 0.25 s | a 80 to 150 Hz thump with a very quiet noise tick on top, sometimes a double hit 60 to 70 ms apart |
| UI click or hover tick | 20 to 60 ms | bright, 3 to 10 kHz, 0 to 5 ms attack, almost nothing under 500 Hz |
| Typing key | 50 to 80 ms | high-passed noise only, 3 to 12 kHz, nothing under 2 kHz; a run of keys jitters 60 to 150 ms apart in time and level |
| Zip | 0.15 to 0.3 s | an exponential pitch sweep (20 to 60 octaves a second), up into a cut or down across it, quieter than hits |

Stereo: objects (pops, keys, clicks, whooshes, stings) are mono or nearly; textures (shimmer, glitch, impact tails) are wide and may move. The band between 300 Hz and 1 kHz is mostly left to music and voice.

## Placing samples

`place_sfx.py` is for recordings and bank sounds the user may use; `sound.py` designs sound from code. Either way: every cue has a label, the file is listed in the delivery notes with its licence, and copyrighted songs or lyrics are never downloaded or committed. When a sample's first milliseconds are silent or soft, align by `onset` or `peak`, not `start`, so the audible attack meets the frame.

## Honest limits

- The launch-film ranges are SaaS and AI product launches. A children's brand reel, a documentary or a music video may sit outside them legitimately; build a profile (`listen.py profile`) from films like the target or accept the row.
- A passing scorecard is not a good film (Goodhart's law). Use it to find faults and to prove timing, not to certify taste.
- Native tool numbers for band level, onset density and tempo are approximations of earshot's. When a decision hangs on one, ask Toolbox for the Earshot reading.
- Recorded versus code-made cannot be proven by the realness model; do not claim either.
- Host playback in ChatGPT or ChatGPT Work is not verified.
