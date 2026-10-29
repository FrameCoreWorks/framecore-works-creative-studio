# Kinetic launch films: teasers, trailers and launch films on the beat

Read for a short, high-energy film carried by huge type on a music beat: a game or film teaser, a trailer, a product or app launch film, a brand film. Landscape 16:9 by default, with a 9:16 version. It adds three things to the [reel board system](reel-board-system.md) and [motion craft](motion-craft.md): a beat sheet with a structure per genre, the energy targets this style needs, and a 4K master that plays everywhere. A vertical brand showreel with a carrier follows [dense kinetic reels](dense-kinetic-reels.md); a film of a product's interface follows [product films](product-films.md).

## Beat sheet first

Everything is placed in beats, not seconds: scenes, word hits, cuts, captions and sound cues. One beat is `60 / BPM` seconds, so a tempo change retimes the whole film and every cut stays on the music. Write the sheet before any style frame and get it approved with the copy. Start from a template in the [kinetic film kit](../assets/kinetic-film/README.md) (`beat-sheets.json`: teaser, trailer, launch film, brand film) and check it with `beat_sheet.py`, which also prints every block in seconds and the music offset for a measured drop.

- **One idea per beat or half beat**, one or two words filling the frame width. Phrases run 4 or 8 beats; change something on each phrase: the ground colour, the type style, the camera direction.
- **Tempo by genre**, as a starting point the brief can override: teasers and game trailers 140 to 175 BPM (drum and bass, half-time, trap), launch films 118 to 128, calm brand films 95 to 115. At 172 BPM a beat is 0.35 s; at 120 it is 0.5 s.
- **Words come from the brief.** Write the film as a short spoken script first, then cut it into one or two words per beat; a phrase of 4 to 8 words fills 4 to 9 beats. Concrete nouns and verbs beat adjectives. Every 3 or 4 phrases needs a turn: a denial, a number, a gag, a reveal. On-screen numbers and claims come from the user or from facts the film can prove; never invent a statistic for energy.
- **The drop is the turn.** Put the biggest visual change on it: a ground flip to the accent, the first picture, the push out of a typed line. Every block in the sheet names its start and end beat, its words, its ground and the hit on its first beat; the kit's phrase-to-scene table maps each phrase to a Studio scene kind or a custom move.

| Genre | Length | Sheet (beats at the film's tempo) |
| --- | --- | --- |
| Teaser | 15 to 25 s | charge 4 to 8 beats (small type, rising sound, filtered drums) → drop on beat 8 or 16 (the biggest move: the hero word or key art) → two or three 4- to 8-beat phrases → the title on the last hit → hard stop and end card |
| Trailer | 30 to 60 s | setup phrases (the world or the problem) → proof (claims, then the thing that proves them, see F8 in the [reel board system](reel-board-system.md)) → escalation in half-beat cuts → title → date or call to action → a short button after the title (a gag, a sound, one last word) |
| Launch film | 20 to 45 s | the problem in two or three words → the product's name as the drop → three features, one phrase each → one proof (a number the user supplies, a screenshot) → name, line and call to action |

## Moves, not fades

- **Word styles** change per phrase: a slam (scale from 140 % with a hard settle), a stack (two lines locking together), a split (words from opposite sides), a punch-in through extruded 3D letters, a typed line with a caret. Measure every word and scale it to the frame; fit is checked on the rendered frame, never assumed.
- **Transitions are moves**: whip pans in and out, a zoom through the counter of a letter into the next scene, a collapse to a point, a ground flip between dark, paper and accent on the phrase change. A cross-fade is the tell of template motion; keep it for nothing.
- **Nothing parks.** Every block drifts the camera a little (about a 6 % push with a slight roll); a landed word keeps living (2 to 5 % scale per second, rows sliding about 70 px/s, ghost rows, particles). The end card is the only rest, and it still pushes in slowly.
- **One new thing per beat**: a word, a colour, a cut or a hit, never two at once. Type fills the width (about 300 to 600 px on a 1920 frame); if a word must shrink under about 200 px, split the phrase. Runs of beat cuts accelerate: 1, 1, 1, ½, ½, ¼ beat, then a flash.
- **Grounds and type.** Three grounds (dark, the brand accent, paper) flip on phrase changes, or on every cut inside a run. Type follows the ground; the accent marks the word that matters. An outlined word for what is not true yet fills on its beat. A variable width axis can stretch a word to fill a line. Speed lines and rings only on the drop and the title; elsewhere a flash, a small shake or a scale bump is enough.
- **Whips alternate** horizontal and vertical, with a long smear (the shutter stretched to several times its normal angle inside the whip).
- **Key art or footage** (optional) cuts in on the drop or between phrases. A picture is the easiest place to park: push it, pan it, punch in on each word, cut in to a detail on a beat, add a weather or particle layer. Use pictures at least 2048 px wide for a 1080p film (about twice that for a 4K master).
- **Generated pictures** go through [Image Prompt](../../image-prompt-architect/SKILL.md): describe the composition in thirds and darken for type in the film; asking for "empty space" or "a calm band for the title" tends to come back as a literal grey band. Pass the first picture as a reference for the next ones so characters and places match. Inspect every picture at 100 % for real brand marks on vehicles, clothes and products and remove them before use. Say "no text, no logos"; wording about removing watermarks from a reference can be blocked by a generator's filter.

## Energy targets and how to measure them

Measured references of this style: the fastest kept 16 % of frames essentially still, its longest still 0.37 s and about 9 hard cuts per 10 s; calmer ones ran 23 to 53 % still, 0.7 s and 1.4 to 3.7 cuts per 10 s. A teaser built to this method passed at 24 % still, no still over 0.6 s before the end card and 12.5 cuts per 10 s. Measure the render, not the plan:

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
- **A generated track (optional)**: [Audio Production](../../audio-production-director/SKILL.md) writes the prompt for the generator the user has (any music model with a connector or app, Scenario MCP among them): instrumental, the exact tempo, the intro length in bars, where the drop falls, the length plus a few seconds. Prefer a model with a tempo input. Ask for two takes and about 15 s more than the film (spare intro and outro). Show the price before a paid run and wait for the user's go. Measure every take with `beats.py` and keep the clearest grid with the strongest drop; a prompt's tempo is a hope, the measured tempo is the fact. Record the generator, terms and asset ids in the asset ledger.
- **A sound kit**: the kit's [`sound-kit.json`](../assets/kinetic-film/sound-kit.json) lists twelve one-shots with lengths, uses and starting prompts (whooshes for whips, impacts for slams, a riser into the drop, key clicks for typed lines, a logo hit where the music stops dead), plus one custom sound for the film's own joke or world. Generate them short and isolated with a negative prompt that keeps music and voices out, or take them from a licensed library; name variants `key_1`, `key_2` and rotate them on repeated cues. Mix under [motion sound design](motion-sound-design.md): every hit sits above the bed, the music ducks under the big hits and stops dead on the title or logo hit, −14 LUFS for social. Listen before handing over: a meter cannot judge taste.

## Master and formats

| File | Size | Encode |
| --- | --- | --- |
| Master | 3840×2160 | H.264 High, `-level:v 5.2` at most, `yuv420p`, BT.709 tags, `-movflags +faststart`, under about 1 GB (CRF about 12 with a slower preset kept a 52 s grainy film under 1 GB) |
| Web and social | 1920×1080 | H.264 High, level 4.2, scaled from the master with Lanczos (CRF about 15) |
| Vertical | 1080×1920 | a recomposed 9:16 cut when the type was laid out for it; otherwise the film centred on black, said so in the delivery note |

- A slower preset without an explicit level can produce level 6.0, which plays in ffmpeg and nowhere on a Mac or phone. Read it back: `ffprobe -v error -select_streams v:0 -show_entries stream=profile,level,width,height,pix_fmt -of csv=p=0 master.mp4` (52 means 5.2).
- A browser capture for 4K must really be 4K: with a 1920×1080 page, capture at device scale 2 and check one frame's size. Headless browsers can also clip the bottom of the viewport or capture 3D layers before every tile is drawn; check the first and the densest frame at full size.
- Mux the mix without `-shortest`: it drops the last frames when the audio is a few milliseconds shorter. Pad or trim the audio to the film's exact duration instead.
- Playback on a hardware decoder (QuickTime, a phone, `ffmpeg -hwaccel videotoolbox` on a Mac) is a separate check; a sandbox decode is not that test and stays `NOT_RUN` until someone runs it.

## Before delivery

- [ ] Beat sheet approved and `beat_sheet.py` prints no errors; every hit and cue placed in beats.
- [ ] Copy exact; every number traced to the user or the film.
- [ ] `motion_activity.py` passes with only the end card declared.
- [ ] Stills of the drop, phrase changes and title reviewed at full and phone size.
- [ ] Mix measured on the delivered file; generated music and sounds recorded with their terms.
- [ ] Master level read back at 5.2 or lower; 1080p and 9:16 files made from the master.

Source: the mechanism (beat-sheet films assembled from scene blocks, measured energy gates, a scored 4K master) was studied from Scenario's public Kinetic Film exploration (reviewed 2026-10-29). This reference and the kit are written from scratch and copy no code or text. Scenario MCP is one optional generator among others; Studio needs no account with it.
