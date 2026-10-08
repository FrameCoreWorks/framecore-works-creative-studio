# Motion sound design

Sound gives a motion video's actions weight: a line lands, a screen pushes in on air, a tap clicks, the end card settles with a low hit, and a music bed carries the energy. Studio builds the whole track from the motion contract's own timing with the [motion sound tools](../assets/motion-sound/README.md), so every sound fits the picture to the frame. Methods are adapted from [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) (Apache-2.0) and [kaventro/motion-designer](kaventro-motion-designer-adaptation.md) (MIT).

## Studio-grade synthesis, never toy tones

Studio designs its sounds and music with code, at the standard of a sound designer's layered work: band-limited noise shaped by moving filters for air, pitched sub layers for weight, modal resonances for clicks and knocks, tuned bells, saturation for density, a shared room and mastering. It never delivers bare oscillator beeps, a single untreated sine or untreated noise (a designed pop glides, breathes and is saturated): they sound like a toy and misrepresent the result. A one-note body without texture (a hollow drum) fails the same way; the generator's quality gate designs such a sound again. Every delivered track is planned with `sound.py plan`, rendered with `sound.py mix` (or a renderer with the same rules) and checked; the reply states the timing check and loudness.

## Order of work

1. **Picture first.** Plan sound only after the timing is approved; a change to timing moves the cues, so plan again after it: `revise.mjs extend` moves the existing cues and marks the sound design stale, `sound.py mix` refuses a stale design, and `sound.py plan` keeps the choices the user fixed.
1. **Design new sound for this video.** Studio never reuses a fixed set of sounds or loops. `sound.py analyze` reads the style, motion tempo and easing, colours, scene kinds, taps, pacing and the brief's words, scores its moods and pace with the [sound base](../assets/motion-sound/sound-base.json), and designs every effect and the whole music anew for this video: the kind of each sound, its material, pitch, layers and envelopes, a new chord progression, rhythms, motif, instruments and drum kit ([how a video's sound is made](../assets/motion-sound/README.md#how-a-videos-sound-is-made)). State the profile and what was designed, with the reasons, in two or three lines. When the user wants something else, design again (`--variation 1`) or fix a choice (`--set landing=blip`, `--set lead=piano`, `--set key="E minor"`); a recipe in the contract can also be edited directly.
1. **Music sets the energy.** The composed bed uses instrument families the video's style allows, designed anew each time. A track the user supplies goes in `music.src` (analyse and cut it with [`beats.py` and `music_edit.py`](../assets/motion-sync/README.md#analysing-a-supplied-track)); otherwise Studio composes a bed. Under words and effects the music is a bed: mixed below the effects, no lead melody over text.
1. **Then the effects,** one per action that matters, from one central cue list (`sfx`), each named after the event it marks.
1. **Mix, check, deliver,** with the cue table, and ask the user to listen once with the picture.

## Choosing and placing sounds

- **Vocabulary from the film type.** A product or brand video uses air (whooshes), weight (impacts, one boom for the final reveal), mechanical foley (clicks, taps, knocks) and one bright tuned accent; never cartoon or game feedback tones unless the story is "the system speaks". The kind of each sound follows the moods: a struck object (its material by mood) or a felt thump for calm and organic pieces, a tonal blip for playful or technical ones, a small swish for bold and fast ones, a plucked string tuned to the key, or silence for sparse editorial pieces; every one is a new design that passes the quality gate against near-pure tones.
- **One sound per action that matters,** starting on the frame the thing moves or lands; `density` sets how much.
- **Loudness says importance.** Clicks and final hits lead; whooshes sit 10 to 17 dB below a hit (the owner judged louder whooshes too strong); landings and ticks stay quiet and step down for later lines and slower counts.
- **Length follows motion.** A sweep's whoosh lasts as long as the line crosses and peaks in the middle; a wipe's whoosh peaks halfway through the wipe and travels in its direction; a riser ends on the reveal.
- **No machine-gun.** Variations by seed and pitch, no two cues of one design within two frames, counter ticks at least three frames apart and quieter as the count slows, staggered items panned apart and stepping up a scale.
- **Taps are two sounds:** the click on the press frame and a soft release four frames later.
- **Pitched sounds follow the key** of the music, so accents never clash with the bed.

## Mix

- −14 LUFS integrated for social delivery (−16 with `--lufs -16` for the web), true peak at most −1 dBTP in the delivered file: limit with true-peak detection and leave margin for AAC encoding; measure the delivered file.
- Music ducks about 8 dB under a voice-over, with short ramps; the voice stays on top. It also dips briefly (1.5 to 5 dB) under clicks, louder impacts and the final hit, so each hit reads without the music pumping.
- The final reveal falls on a downbeat: the composed bed's tempo is fitted inside the style's range (or within 8% of its usual tempo), the bar before closes the progression, and the reveal lands on the tonic and rings out to the end. A bed that is cut off at the last frame sounds unfinished.
- Low end belongs to one element at a time: the reveal's hit comes from the effects, so the music adds no kick under it; bass carries upper harmonics, because phone speakers do not play its root.
- The picture is never re-encoded; the MP4's video stream is copied.
- A hit more than a frame off is noticeable; `sound.py` holds transients within 2 ms.

## Rights

Synthesized sounds and composed beds are original and need no licence or credit. Any recording or track the user supplies needs a licence that allows the planned use, recorded in the asset ledger; a "free" label is not a licence, and libraries that forbid redistribution are never bundled into Studio. A connected voice or music provider is used only when the user confirms its cost and terms.
