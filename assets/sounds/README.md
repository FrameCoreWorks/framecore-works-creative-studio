# Example sounds

**[Listen to all of them in the browser](https://framecoreworks.github.io/framecore-works-creative-studio/sounds/)**: one click plays, a second click stops.

Ten short sounds that show what Studio can make and check without samples, accounts or paid services: eight effects for motion graphics and two music beds. Claude synthesized each one in code ([`source/make_sounds.py`](source/make_sounds.py), NumPy oscillators and seeded noise) in a Claude Code cloud session on 2026-10-31, and Earshot, built into [FrameCore Works Toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox), measured and described every published MP3. They are repository presentation files, outside the plugin package, and are not installed with Studio.

**Licence:** [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Use them anywhere, commercially too, without credit.

| # | Sound | Use it for | Length | Loudness | Earshot check |
|---|---|---|---|---|---|
| 1 | [Whoosh](01-whoosh.mp3) | a transition between shots | 1.3 s | −11.6 LUFS, −1.7 dBTP | strong match for "a fast whoosh swoosh transition", z +4.4 |
| 2 | [UI click](02-ui-click.mp3) | a button, cursor or tap | 0.12 s | too short for LUFS, −3.1 dBTP | strong match for "a short user interface click", z +3.2 |
| 3 | [Pop](03-pop.mp3) | an element or chat bubble appearing | 0.45 s | −16.0 LUFS, −1.7 dBTP | plausible for "a short bubbly pop", z +2.8; top tag "a bubble pop" |
| 4 | [Riser](04-riser.mp3) | a build-up before a reveal | 3.6 s | −14.9 LUFS, −2.2 dBTP | plausible for "a rising tension riser", z +2.8; top tag "an uplifter sweep" |
| 5 | [Bass impact](05-bass-impact.mp3) | a logo hit or end card | 3.4 s | −18.1 LUFS, −1.8 dBTP | strong match for "a deep cinematic bass impact boom", z +4.0 |
| 6 | [Ding](06-ding.mp3) | a notification or success | 2.2 s | −11.1 LUFS, −1.8 dBTP | plausible for "a bell ding notification chime", z +2.9; top tag "a triangle hit" |
| 7 | [Typing](07-typing.mp3) | a keyboard under a chat or text scene | 3.4 s | −19.1 LUFS, −2.4 dBTP | plausible for "typing on a computer keyboard", z +2.9; top tag "an old typewriter" |
| 8 | [Glitch](08-glitch.mp3) | a digital stutter or cut | 0.7 s | −13.8 LUFS, −1.2 dBTP | strong match for "a digital glitch stutter", z +4.3 |
| 9 | [Calm bed](09-music-calm.mp3) | a quiet background; loops seamlessly | 32 s | −16.5 LUFS, −3.8 dBTP | plausible for "calm ambient music, soft relaxing pad", z +2.9; key C major |
| 10 | [Energetic bed](10-music-energetic.mp3) | an upbeat reel or ad; loops seamlessly | 32 s, 120 BPM | −16.4 LUFS, −3.7 dBTP | strong match for "an energetic techno track, a four on the floor beat with bass", z +3.7 |

No file has clipped samples. Every "Forced choice" against unrelated alternatives (for example a car engine for the whoosh, calm ambient music for the energetic bed) chose the intended description at more than 99%. The full readings, with each sound's top five tags, are in [`earshot-readings.json`](earshot-readings.json).

How to read the check: Earshot compares the sound with a text description. "strong" and "plausible" are its own verdicts; z is how far the match stands above its vocabulary of 322 descriptions. Earshot marks music descriptions as unvalidated, so the music readings are a guide rather than proof. The UI click is too short for an integrated LUFS reading. Earshot cannot judge taste: these are starting points to listen to, adjust and mix, not finished sound design for a client.

## Rebuild them

From the repository root, with Python 3, NumPy and ffmpeg (with libmp3lame):

```sh
python3 assets/sounds/source/make_sounds.py /tmp/fc-sounds-wav
bash assets/sounds/source/encode.sh /tmp/fc-sounds-wav assets/sounds
```

The noise is seeded, so the same NumPy version gives the same WAVs. The music beds are normalized to −16 LUFS integrated with a −1.5 dBTP ceiling; the effects keep their synthesized peak level. To repeat the check with Earshot installed through Toolbox (full tier):

```sh
python3.12 <toolbox>/capabilities/earshot/scripts/runtime.py exec -I assets/sounds/source/earshot_check.py assets/sounds readings.json
```

The listening page is [`index.html`](index.html); the Pages workflow publishes it with the MP3s to `gh-pages` under `sounds/`.
