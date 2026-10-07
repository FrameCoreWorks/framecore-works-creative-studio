# Motion sound design

Sound design gives a motion video's actions weight: a line lands with a knock, a screen pushes in on air, a tap clicks, the end card settles with a low thud. In Studio it is built from the motion contract's own timing, so it fits the picture frame for frame, with the [motion sound tools](../assets/motion-sound/README.md) and their bundled CC0 recordings. Methods are adapted from [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) (Apache-2.0) and [kaventro/motion-designer](kaventro-motion-designer-adaptation.md) (MIT); see [the sources](../../../integrations/motion-sound-sources/README.md).

## Order of work

1. **Picture first.** Plan sound only after the timing is approved; a change to timing moves the cues, so plan again after it (`sound.py plan` on the new revision).
2. **Music, if any, sets the energy.** A track the user supplied or a connected provider made (never music synthesized with code) goes in `music`; analyse and cut it with [`beats.py` and `music_edit.py`](../assets/motion-sync/README.md#analysing-a-supplied-track). Under words and sound effects it is a bed: mixed low, few instruments, no lead over text.
3. **Then the effects,** one per action that matters, from one central cue list (`sfx` in the contract), each cue named after the event it marks.
4. **Mix, check, deliver.** `sound.py mix`, then `sound.py check`, then listen once with the picture before delivery.

## Choosing sounds

- **Vocabulary from the film type, not from the event name.** A product or brand video uses air, impacts and real mechanical foley: whooshes for movement, knocks and thuds for landings, clicks for taps, a bright ting for a final value. Synthetic interface tones (bleeps, confirmation chimes, plucks, cartoon pops) make it sound like a game; use them only when the story is deliberately "the system speaks".
- **One sound per action that matters,** starting on the frame the thing moves or lands. A sound for everything is noise; `density` sets how much (`minimal`, `standard`, `rich`).
- **Loudness says importance.** Default gains: tap click −4 dB, end-card thud −2 dB, scene whoosh −6 dB, sweep and wipe whooshes −2 dB, landings −10 dB and quieter for later lines, counter ticks −14 to −20 dB as the count slows, a camera move −18 dB.
- **No machine-gun.** Repeated events use the family's variants in turn, no two cues of one family within two frames, counter ticks at most every four frames and quieter as they go, staggered items panned slightly apart.
- **Place on the hit, not on the file start.** A sound's transient (or a whoosh's loudest moment) lands on the cue frame; the file starts earlier by its measured offset. Whooshes for a sweep peak at the middle of the line's crossing; a wipe's whoosh peaks halfway through the wipe and is panned toward the side it comes from.
- **Taps are two sounds:** the click on the press frame and a quiet release four frames later.

## Mix

- Integrated loudness −16 LUFS for the full mix with music, true peak at most −1.5 dBTP; a mix of only effects stays quieter, limited by its loudest hit. Platforms normalize loudness; measure the delivered file.
- Music ducks about 8 dB under a voice-over, with short ramps; the voice stays clearly on top and the music still present between lines.
- The picture is never re-encoded for sound; the MP4's video stream is copied.
- Sync tolerance: a cut or hit more than a frame late is noticeable; `sound.py check` holds transients within 2 ms.

## Rights

Bundled sounds are CC0 recordings and need no credit (credit is appreciated). Any other sound needs a licence that allows the planned use, recorded in the asset ledger; a "free" label is not a licence. Libraries that forbid redistribution (for example Mixkit) can be used by the user in their own project but are never bundled into Studio. Studio never synthesizes music, voices or effects with code for a delivery.
