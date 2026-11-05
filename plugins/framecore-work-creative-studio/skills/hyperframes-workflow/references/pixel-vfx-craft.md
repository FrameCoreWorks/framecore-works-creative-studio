# Pixel art effects (VFX) craft

How Studio makes pixel art effects that look hand-animated: fire, explosions, hits, magic, pickups, UI pops and
transitions, inside a pixel-art film, a game trailer, a reel with a game look, or as sprite sheets for a game.
Use it with the [Animate engine's pixel style](animate-engine.md#pixel-look-studios-additions) or any canvas
composition drawn at a low internal resolution.

Written in Studio's own words from a review of [pixelfx](https://github.com/patch-gg/pixelfx) by Patch at
`a84159688af3ca37a4be05a0d422b94451b2e24e` (0.3.0, MIT), whose method comes from Hugo Duprez's
[How to make (good) pixel art effects with Claude](https://www.spritefusion.com/blog/how-to-make-good-pixel-art-effects-with-claude)
and his MIT [Sprite Fusion effects](https://www.spritefusion.com/pixel-art-vfx). No code or skill text was copied.
Credit both when a piece follows this method closely.

## Route

- **pixelfx installed** (its skill `pixelfx:pixelfx` or `pixelfx` is in this host's list, from the
  [Toolbox catalog](../../workflow-orchestrator/references/extensions.md#toolbox-catalog)): say in one line that
  Studio uses it for the effect, read its skill and follow it for that step only ([installed catalog
  entries](../../pipeline-core/references/companion-routing.md#installed-catalog-entries)). Start from its 244 ready
  effects (recolor with a palette, change the seed, mirror) before drafting a new one. Studio keeps the brief, the
  plan and the review.
- **Not installed:** when a pixel effect is central to the piece, offer the entry once in the user's terms (ready
  effects and sprite sheets); otherwise build the effect yourself with the rules below.
- **Sprite sheets for a game** (Godot, Unity, Phaser, GameMaker): that is pixelfx's own deliverable (transparent
  PNG grid plus frame JSON with FPS, loop and pivot). Studio does not write an engine exporter of its own.

## Build an effect from two layers

Draw every frame into two buffers and composite them at the end:

1. **Colour:** the pixels themselves, opaque or dithered, on whole pixels at the internal resolution.
2. **Light:** additive glow summed on top of the colour (soft pools, hot cores, a glint per spark). Hot things
   read as hot because of this layer, not because of large saturated fills.

Keep the effect in local space around one anchor (feet, point of impact, muzzle, base of a torch): x right, y down,
1 unit = 1 pixel, the floor at y = 0. Directional effects face right; the composition mirrors or rotates them.

## The quality bar

1. **Lines and light, not fills.** Build from 1 px rims, rings, trails and sparks. White only in the hottest core
   and edges, tinted middles, deep colour only in shadow. A large flat area of saturated colour is nearly always
   wrong.
2. **Light on everything that burns or shines:** a wide faint pool, a tight bright core, a small light per spark,
   lights that flare on the impact frame and fall away, a warm or cold pool on the floor while something burns or
   freezes.
3. **Translucent volumes.** Smoke, steam, dust and mist are soft, truly translucent discs that swell, thin and are
   lit on top. A dither checkerboard is not smoke.
4. **Real motion.** Sparks stretch with their speed, fall and bounce; debris tumbles, settles and fades; fire rises
   and cools into smoke; landings kick up dust. Use drag: a fast burst, then a slow drift.
5. **Choreography in phases:** gather (energy pulling in), release (a 1 to 2 frame white flash plus light and a
   burst), spread, hold (glints, embers, twinkles), break-up, long decay. Many small events, each varied in size,
   speed, delay and life.
6. **Depth.** A ring on the floor is a flat ellipse: its far half behind the character, its near half in front.
   Back rows are dimmer.
7. **Timing.** Fast attack, slow release. Hits are snappy (0.3 to 0.8 s) but keep a follow-through; big effects
   linger 2 to 4 s while smoke clears.
8. **Reads at 1x** on a phone, with one focal point and no lone noise pixels inside shapes.
9. **Original.** Generic motifs are fine; never a specific game's sprite, character or logo.
10. **Clean.** Stays inside its canvas, a one-shot ends on an empty frame, a loop wraps with no seam, the same seed
    gives the same frame every time.

## Acting: an effect needs a body

An effect alone looks like a sticker. What sells a hit is the body around it:

- **Wind-up** before the effect starts, in the opposite direction to the blow, so the viewer knows something is
  coming.
- **A big silhouette change** on the release frame.
- **Hit-stop:** freeze everything (effect, attacker, target) for 0.03 to 0.2 s on contact, longer for heavier
  blows, with a short screen shake of 1 to 3 px.
- **The target reacts:** rocks back, flashes, takes a tint (ice, shock, poison), then settles.
- **Follow-through and recovery** that overshoot a little, then return to guard.
- **Poses step at 12 fps** like hand-drawn sprites, while particles run at full frame rate. Line the hand up with
  where the effect fires from on the release frame, and put the hit on the effect's own impact time, not one
  guessed by eye.

This is also game "juice" for motion graphics outside pixel art: a click, a coin, a counter or a logo hit lands
harder with anticipation, a two-frame hold and a reaction ([motion craft](motion-craft.md) keeps the general
timing rules).

## Determinism

- Every random number comes from a seeded generator; never `Math.random()` or the clock. Frame 40 is the same
  frame on every render, so a revision changes only what was asked.
- **Loops** are a pure function of time `t` (cycling particles, noise sampled on a loop, sines with whole cycles
  per loop), so they tile with no seam.
- **One-shots with physics** step their particles at a fixed rate (120 Hz or finer) and draw from that state, so the
  motion is identical at 24, 30 or 60 fps.

## Make it look hand-animated

1. **Say it in one line** with the art direction: what it is, how it moves, its palette and timing ("a frost nova:
   crystals erupt in a ring from the feet outward, a white flash at the centre, shards spin off, the floor stays
   frosted and fades").
2. **Find references first:** the closest ready effect, or a reference the user supplied. When the direction is
   open, draft 3 to 5 genuinely different takes and compare them before choosing; show the user the best two or
   three.
3. **Render and look** at a contact sheet of sampled frames, then **fix the worst thing** and render again. Three
   rounds minimum; a showpiece takes more.
4. **Judge motion from consecutive frames** or the video, never from samples alone: motion bugs hide between
   samples.
5. **Benchmark** against the reference at the same size on screen: if it has more detail, light or life, yours is
   not done.

| You see | Usual fix |
| --- | --- |
| Mush at 1x | Fewer colours, a clear silhouette, one focal point, bigger shapes |
| Speckle inside shapes | Less noise threshold, snap noise to ramp steps, no noise on small shapes |
| Floaty, no punch | Fast in and slow out, a 1 to 2 frame white flash, shorter total time, hit-stop |
| Stiff or mechanical | Vary every particle; add secondary motion (sparks, smoke, debris) |
| Washed out | Less glow, darker edge steps, white only in the core |
| Flat | One light side: brighter top-left, a darker step bottom-right and at the base |
| Smooth vector look | Hard ramp steps in colour; softness only in light and smoke |
| Checkerboard smoke | Translucent soft discs lit on top |
| Seam when a loop wraps | Whole cycles per loop, loop-sampled noise, cycling particles |
| A one-shot that pops off | Shrink, dither out or fall away before the last frame |
| A great effect on a dead character | Add the act: wind-up, release pose, hit-stop, reacting target, recovery |
| The act feels weightless | Wind-up the other way, longer freeze (up to 0.2 s), bigger silhouette change, shake |

## Placing it in a film

- Draw at an internal resolution that divides the output exactly (see the pixel style's era table) and scale up by
  whole numbers with nearest-neighbour sampling; a supplied sprite sheet follows the rules in
  [Pixel look: Studio's additions](animate-engine.md#pixel-look-studios-additions).
- Glow baked into a sprite sheet reads as additive only over dark scenes; on a bright background render a recoloured
  version or keep the effect on a dark layer.
- A palette is a dark-to-bright ramp: recolour an effect by swapping its ramp (blue fire, pink heal) instead of
  redrawing it, and keep a brand's colours as one ramp.
- Text, captions and the call to action stay outside the effect's burst and inside the 9:16 safe area; the frame QA
  checks the flash frames too.

## Rights

pixelfx code and effects are MIT: renders may be used commercially, and code copied into a game keeps its `LICENSE`
and `NOTICE.md`. Its Patch Pixel font (`gallery/fonts`) is all rights reserved and never goes into a deliverable.
