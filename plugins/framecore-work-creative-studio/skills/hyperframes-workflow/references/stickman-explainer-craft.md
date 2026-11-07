# Stickman and faceless explainer craft

How Studio makes stick-figure explainers, short stories and faceless channel videos (YouTube, Shorts, Reels,
TikTok): a narrator's voice, a simple figure acting out the idea, props and diagrams, captions and sound. Use it
with the Toolbox entry `stickman-kino` when it is installed, or with any HyperFrames, Remotion or Animate engine
composition, and for prompts to a video generator.

Written in Studio's own words from reviews of [stickman-kino](https://github.com/dsauce/stickman-kino) by Prerit
Ahuja at `d3d665301c0b62f04c885785e6bd6044de0785c6` (1.0.0, MIT) and
[Stickman Video Director](https://github.com/kaomei/stickman-video-director) by kaomei at
`eb4bb378c4716a617f9ad7d98a60379b9d1fa54a` (MIT). No code or skill text was copied. Credit them when a piece
follows their method closely.

## Route

- **stickman-kino installed** (its skill `stickman-kino:stickman-kino` or `stickman-kino` is in this host's list,
  from the [Toolbox catalog](../../workflow-orchestrator/references/extensions.md#toolbox-catalog)): say in one line
  that Studio uses it to build the film, read its skill and follow it for the build step only ([installed catalog
  entries](../../pipeline-core/references/companion-routing.md#installed-catalog-entries)). It draws rigged figures
  with ready poses, props, charts, captions, voice, music and effects locally in HyperFrames, with no video model or
  API key. Studio keeps the brief, script, copy locks, board plan and review, and passes the rules below as the
  direction.
- **Not installed:** when the stick-figure look is the point of the piece, offer the entry once in the user's terms
  (a ready stickman rig and render, no paid video service); otherwise build the figure yourself in the chosen
  runtime with the rules below.
- **Video generator instead** (Veo, Kling, Gemini, Sora and similar): write the clips with
  [video-prompt-architect](../../video-prompt-architect/SKILL.md) and apply the character and voice locks below.

## Pick a look

Offer at most three looks that fit the subject, then write the chosen one into the brief:

| Look | What it is | Good for |
| --- | --- | --- |
| Classic line | One black or white figure with a hollow round head on a flat white or black field, plus up to three bright accent colours on props and graphics only | Ideas, psychology, business lessons |
| Clean studio pop | A figure with one signature clothing item (a coloured cap, a shirt) on a bright white set with a faint floor grid and glassy blue interface panels | Tech and product explainers |
| Cozy story | White-headed figures with dark stick limbs in warm, full-colour cartoon places that change with each scene (cafe, street, room) | Life stories, habits, gentle narratives |
| Period cartoon | The same figure grammar in costume and cel-shaded settings of an era, with one era pack for the whole film | History |
| Hand-drawn minimal | Crayon-like line figures and props on paper or a light grid, captions in a handwriting face | Faceless channel explainers |
| Retro TV | Grey and white figures on a dark field, soft bloom, faint scanlines and vignette added after the picture and before clean captions | Lore, mysteries, retro topics |

Never copy a particular creator's or channel's character, colours or set design; a look is a general grammar,
not someone's identity. Any channel the user points to is a reference to learn from, not a template to reproduce.

## Lock the character

- Write one complete description of each figure (head, limbs, line weight, colour, the one clothing item, what the
  face may show) and freeze it after approval.
- In a code build, keep it as one component or rig used everywhere. For a video generator that takes no reference
  image, repeat the full frozen description word for word in every clip. "The same character" or a shortened
  description lets the generator drift.
- Keep the figure's design apart from what changes per shot: where it stands, its pose, which prop it holds and the
  state of that prop. A prop handed over in one shot stays handed over in the next.
- Two arms and two legs, one pose per limb at a time: a moving arm replaces its old position rather than adding a
  third arm.
- With several characters, freeze a card for each and name in every clip which ones are on screen.

## Rhythm

- Lead with the voice: record or generate the narration first, then time the pictures to the real speech and its
  pauses. Never slow the voice or stretch pauses to fit a planned length.
- Budget about 20 to 25 spoken words per 10 seconds (2 to 2.5 words a second) and check it with the
  [VO budget](../../copy-voice/SKILL.md) before the voice is made.
- Something meaningful changes every 2 to 3 seconds: a new action, a prop entering, a cut or a diagram building.
  The main figure or object is never still for more than about 2.5 seconds unless the board marks a deliberate hold.
- Give each 10-second stretch three timed beats, and end each shot in a way that leads into the next one: the same
  action continuing, a prop carried across, the same screen direction or a planned cut.
- Open on the most surprising question or picture within the first 2 to 5 seconds. A useful order for an explainer:
  hook, the common belief, why it is wrong, what is really going on, the payoff and one question for the viewer. Use
  it as an option, not a rule: a short story ends on its punchline, not on a question.
- Do not invent statistics, quotes or results the source does not support.

## Sound

- Give every scene a quiet bed of its place (room tone, street, rain, wind) under the voice, unless the board
  marks a deliberate cut.
- A deliberate cut to silence is written into the plan with its reason and with what brings the sound back (a door
  slam, the narrator's next line). It mutes the bed, music and effects, never the narration.
- Effects follow the action on screen (a step, a door, a pen tap), matching the material, weight and distance; they
  never stand in for missing motion.
- Keep the voice on top. The [audio direction](../../audio-production-director/SKILL.md) and Toolbox's Earshot
  measure loudness and place effects on the right frame.

## Captions and checks

- Captions are one line: break at meaning and real speech pauses, never by word count and never by shrinking the
  text. Follow [caption-studio](../../caption-studio/SKILL.md) for safe areas and check the encoded frames.
- Before delivery look at frames from the whole timeline (contact sheet), check that figures stand on the ground,
  nothing leaves the frame, every shot has visible motion and every caption is readable, then watch the render.
  Report what was checked and what is NOT_RUN.
