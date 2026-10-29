# Kinetic launch films: teasers, trailers and launch films on the beat

Read for a short, high-energy film carried by huge type on a music beat: a game or film teaser, a trailer, a product or app launch film, a brand film. Landscape 16:9 by default, with a 9:16 version. It adds three things to the [reel board system](reel-board-system.md) and [motion craft](motion-craft.md): a beat sheet with a structure per genre, the energy targets this style needs, and a 4K master that plays everywhere. A vertical brand showreel with a carrier follows [dense kinetic reels](dense-kinetic-reels.md); a film of a product's interface follows [product films](product-films.md).

## Beat sheet first

Everything is placed in beats, not seconds: scenes, word hits, cuts, captions and sound cues. One beat is `60 / BPM` seconds, so a tempo change retimes the whole film and every cut stays on the music. Write the sheet before any style frame and get it approved with the copy.

- **One idea per beat or half beat**, one or two words filling the frame width. Phrases run 4 or 8 beats; change something on each phrase: the ground colour, the type style, the camera direction.
- **Tempo by genre**, as a starting point the brief can override: teasers and game trailers 140 to 175 BPM (drum and bass, half-time, trap), launch films 118 to 128, calm brand films 95 to 115. At 172 BPM a beat is 0.35 s; at 120 it is 0.5 s.
- **Words come from the brief.** On-screen numbers and claims come from the user or from facts the film can prove; never invent a statistic for energy.

| Genre | Length | Sheet (beats at the film's tempo) |
| --- | --- | --- |
| Teaser | 15 to 25 s | charge 4 to 8 beats (small type, rising sound, filtered drums) → drop on beat 8 or 16 (the biggest move: the hero word or key art) → two or three 4- to 8-beat phrases → the title on the last hit → hard stop and end card |
| Trailer | 30 to 60 s | setup phrases (the world or the problem) → proof (claims, then the thing that proves them, see F8 in the [reel board system](reel-board-system.md)) → escalation in half-beat cuts → title → date or call to action → a short button after the title (a gag, a sound, one last word) |
| Launch film | 20 to 45 s | the problem in two or three words → the product's name as the drop → three features, one phrase each → one proof (a number the user supplies, a screenshot) → name, line and call to action |

## Moves, not fades

- **Word styles** change per phrase: a slam (scale from 140 % with a hard settle), a stack (two lines locking together), a split (words from opposite sides), a punch-in through extruded 3D letters, a typed line with a caret. Measure every word and scale it to the frame; fit is checked on the rendered frame, never assumed.
- **Transitions are moves**: whip pans in and out, a zoom through the counter of a letter into the next scene, a collapse to a point, a ground flip between dark, paper and accent on the phrase change. A cross-fade is the tell of template motion; keep it for nothing.
- **Nothing parks.** Between hits the camera drifts, type slides, ghost rows or particles move. The end card is the only long hold.
- **Key art or footage** (optional) cuts in on the drop or between phrases. Push, pan and punch in on each word over it, and darken it in the film for legible type rather than asking a generator for empty space.

## Energy targets and how to measure them

Studied references of this style keep under a quarter of their frames still and rarely hold a shot longer than 0.4 to 0.7 s; a teaser runs about 8 to 14 cuts per 10 s. Measure the render, not the plan:

```sh
python3 assets/motion-quality/motion_activity.py film.mp4 --max-share 0.25 --max-still 0.6 --hold 20.5-24
```

Declare only the end card with `--hold`. A failing film gets more motion inside the long boards (camera drift, a punch-in per word, a cut-in to a detail), not shorter boards everywhere. Calmer reels keep the [dense kinetic reels](dense-kinetic-reels.md) figures.

## Build and render

- Every visual state is a pure function of the frame time: no unseeded randomness, wall clock or state carried between frames. That lets the renderer seek anywhere and average sub-frames for motion blur ([Python renderer](../assets/motion-render/README.md) `--blur`; in HyperFrames or Remotion, their own sub-frame options). Keep the shutter open across the fastest frame of a whip: a whip rendered sharp looks like a jump.
- Check at 1080p first; render the master at 3840×2160 from the same composition once every check passes. Never upscale a 1080p file to call it 4K. 4K renders use a lot of memory: run few workers in parallel.
- Stills at the beats that matter (the drop, each phrase change, the title) go to the review before the full render, at full size and at phone size.

## Music and sound

- **A supplied track**: [`beats.py`](../assets/motion-sync/README.md#analysing-a-supplied-track) gives the tempo, bar 1 and the drops; `music_edit.py` cuts whole bars so the drop lands on the sheet's drop beat; `sync.mjs` puts the grid in the contract. Fit the tempo on the stretch the film uses: a 0.15 % error puts the last hits of a 50 s film about 70 ms late.
- **A generated track (optional)**: [Audio Production](../../audio-production-director/SKILL.md) writes the prompt for the generator the user has (any music model with a connector or app, Scenario MCP among them): instrumental, the exact tempo, the intro length in bars, where the drop falls, the length plus a few seconds. Prefer a model with a tempo input. Show the price before a paid run and wait for the user's go. Measure every take with `beats.py` and keep the clearest grid with the strongest drop; a prompt's tempo is a hope, the measured tempo is the fact. Record the generator, terms and asset ids in the asset ledger.
- **A sound kit**: about 12 to 15 one-shots, each on a cue in beats: whooshes for whips, impacts for slams, a riser into the drop, a sub drop on it, key clicks for typed lines, a stop or tape-stop on the title, plus one custom sound for the film's own joke. Mix under [motion sound design](motion-sound-design.md): each hit audible over the bed, −14 LUFS for social.

## Master and formats

| File | Size | Encode |
| --- | --- | --- |
| Master | 3840×2160 | H.264 High, `-level:v 5.2` at most, `yuv420p`, BT.709 tags, `-movflags +faststart`, under about 1 GB |
| Web and social | 1920×1080 | H.264 High, level 4.2, scaled from the master with Lanczos |
| Vertical | 1080×1920 | a recomposed 9:16 cut when the type was laid out for it; otherwise the film centred on black, said so in the delivery note |

- A slower preset without an explicit level can produce level 6.0, which plays in ffmpeg and nowhere on a Mac or phone. Read it back: `ffprobe -v error -select_streams v:0 -show_entries stream=profile,level,width,height,pix_fmt -of csv=p=0 master.mp4` (52 means 5.2).
- Mux the mix without `-shortest`: it drops the last frames when the audio is a few milliseconds shorter. Pad or trim the audio to the film's exact duration instead.
- Playback on a hardware decoder (QuickTime, a phone, `ffmpeg -hwaccel videotoolbox` on a Mac) is a separate check; a sandbox decode is not that test and stays `NOT_RUN` until someone runs it.

## Before delivery

- [ ] Beat sheet approved; every hit and cue placed in beats.
- [ ] Copy exact; every number traced to the user or the film.
- [ ] `motion_activity.py` passes with only the end card declared.
- [ ] Stills of the drop, phrase changes and title reviewed at full and phone size.
- [ ] Mix measured on the delivered file; generated music and sounds recorded with their terms.
- [ ] Master level read back at 5.2 or lower; 1080p and 9:16 files made from the master.

Source: the mechanism (beat-sheet films assembled from scene blocks, measured energy gates, a scored 4K master) was studied from Scenario's public Kinetic Film exploration (reviewed 2026-10-29). This reference is written from scratch and copies no code or text; the original skill is listed as an app note in FrameCore Works Toolbox.
