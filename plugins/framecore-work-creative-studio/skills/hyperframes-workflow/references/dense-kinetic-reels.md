# Dense kinetic reels: brand showreels with a carrier and scene logic

Read for a short vertical brand reel built from type, the brand's own marks and illustrated objects, with a cut about every second: an agency or studio showreel, an offer reel for classes, services or products, a "what we do" reel. It adds three things to the [reel board system](reel-board-system.md): a structure for this genre, a carrier that ties the boards together, and the scene logic check that keeps every action believable and every transition motivated. The lessons come from two studied reference reels and a reel Studio built and the owner approved on 2026-10-19 (see the end).

## Brand first, always

- **Colours, type, characters and objects come from the brand**, never from the reference. Take the palette from the logo and brand kit (the wood orange, the metal grey, the outline navy of an illustrated logo, for example), the display type from the brand or a bundled font that fits it, and the objects from the brand's own drawings. A reference teaches a mechanism (a chat hook, a carrier, kinetic letters, a logo assembly), not a look: copying its colours copies someone else's identity.
- **Tempo follows the audience and the brand.** A reel for parents, a clinic or a bakery can run a little calmer than an agency reel; measure the result instead of guessing (below). Calmer is not slower to read: every board still moves.
- **Cut-outs from the brand's artwork.** When the logo carries illustrated objects, cut them out as separate PNGs with transparency (remove the white background, keep each object as one connected region, check the edges at 100 % on a contrasting colour) and animate them. Never redraw a client's object in a different style next to the original.

## Structure (about 15 to 18 s, 9:16)

| Board | Time | Job | Typical motion |
| --- | --- | --- | --- |
| Hook | 0 to 3.5 s | a recognisable everyday moment: a group chat or a notification asking the question the brand answers | messages pop in with reading time, keyboard rises, a reply is typed, the brand card is sent |
| Carrier launch | 0.5 s | the brand's mark leaves the card and becomes the carrier | it grows and spins to the centre; an action lands on it (a hammer hit, a tap) and opens the next board |
| Offer boards | 1 to 1.5 s each, three to five | one verb or offer per board in large kinetic type, with the object that does it | letters enter with a different family per board (drop, pop, slam, slide); the object performs the action |
| Summary | about 2 s | what the brand is, in its own lettering | halftone or pattern field from the brand colour, objects orbit, the carrier lands in the middle |
| Payoff | 1.5 to 2 s | back to the hook: the answer worked | replies in the same chat, then a wave or wipe out |
| End card | 2 to 2.5 s | logo assembled from its parts, the line, one call to action | parts fly in, wordmark halves drop, the carrier lands last with a squash and a shake |

The studied references ran 0.7 and 1.0 cuts per second with 11 to 16 % still frames; the approved reel ran about 0.8 cuts per second, 15 % still and no still longer than 0.67 s (the reading pauses).

## The carrier

One element of the brand's mark (a nail from the logo, a "3" from the wordmark) travels through every board and is the reason the boards belong together.

- It enters each board from where it left the last one (falls from above after being yanked out at the top, flies out of the card), lands with a squash and settles with a small elastic overshoot. It leaves the same way before the next transition.
- **When it replaces a letter** (the nail as the I in PIŁUJEMY, WIERCIMY, WBIJAMY, MIERZYMY), draw it as a vector glyph at the weight of the display type: the shank as thick as a stem, the head wider, clearly larger than the letters (the head above the cap height, the tip below the baseline) and centred in a slot with the same spacing on both sides as between the other letters. A raster cut-out scaled into a word looks pasted on: thin, grainy and off-centre. Check the word zoomed in.
- Do not put it everywhere: one role per board (a letter, a landing point, the thing hit by the tool).

## Scene logic check (run it on the storyboard and again on the frames)

Every object must do its real job in a way a viewer believes at a glance, and every transition should come out of what just happened. For each board answer:

1. **What does the object do, to what, and from which side?** Choose the camera side that shows the result. A drill bores into the face of a board, so the board is seen turned towards the drill (or face-on) and the bit disappears into it; a drill running beside a block "from the side" reads as a tool switched on next to the wood. A saw cuts in its own kerf: the blade sits behind the board's face, strokes run along the blade, and the kerf deepens with each stroke. A hammer hits the head of a nail and the nail goes in.
2. **What is the visible result?** Chips come out of the cut or the hole, the off-cut drops away when the cut is through, the hole grows with the depth, the nail sinks with each hit. A tool that moves without changing its material is decoration.
3. **Does the next board grow out of that result?** The bored hole widens and the camera flies through it into the next board; the hammer hit floods the frame from the nail head; the cut-through drops the off-cut and a wipe follows its fall. A transition chosen only because it looks energetic hides an unrelated scene.
4. **Is anything faked in a way that shows?** Use perspective (a CSS 3D turn of the board, not of a side-view drawing of the tool), masks or clips that hide the part inside the material, and layer order (the blade behind the board's face). A side-view drawing rotated in 3D still reads as a side view; turn the object it acts on instead.
5. **Does the whole reel close?** The payoff returns to the hook's situation with its answer, and the carrier ends inside the logo.

## Chats and reading time

- About 0.75 s between short messages (up to about 40 characters), more for longer ones; let the last message of a group stand at least 0.8 s before the keyboard rises or the scene changes.
- Typing: about 0.065 s per character with the key pop-up; keep typed text short (a name, two words).
- Payoff replies: the first stands alone about 0.6 s, the second joins, both hold about 0.9 s before the transition.
- Camera in a chat film (owner real-use finding 2026-10-30): few shots, one per beat (a group of lines, the typing, the sent bubble), each holding about 1 to 1.5 s so every line can be read. Moves take about 0.4 to 0.55 s and only push in or travel at the same zoom; never pull the zoom out in the middle of a move. While someone types, push in close on the input bar and hold until it is sent, then travel up with the bubble.
- Length follows the holds: when a requested length cannot keep these holds, propose a longer one to the user before building ("let's make it 20 s, because the reel needs its holds"); never speed up moves or cut holds silently to hit the number.
- Recreate the chat as clean HTML (status bar, header with a cover so scrolled messages never show behind it, bubbles, input bar, keyboard). Do not reproduce a named messenger's exact interface or logo, and present the people as a staged scene the client approves, never as real testimonials.

## Persistent labels

A thin top rule with the brand name on the left and "01 · VERB" on the right is part of this genre's system and passes the [development review](motion-development-review.md) when it belongs to the brand's identity; it fails when it is only a template habit. One style, same position, every offer board.

## Build notes (HyperFrames)

- Pin positions and draw order: tools that work on a material sit behind its face where they enter it; a clip-path that grows with the advance hides the part already inside.
- Start states belong in CSS or in the first tween's from-values; a `fromTo` renders its start immediately, so a later scale or position change on a visible board needs `immediateRender: false`.
- Vibration and the move it rides on go on different elements (an inner image shakes, its wrapper travels), so tweens never overlap.
- To give a scene more time after a review, remap the timeline positions with one function (everything after time A moves by d) instead of editing every number, and shift the sound cues by the same function.
- Render with `npx hyperframes render --quality high`; in a Linux container a 16.7 s 1080×1920 reel of flat illustration and type rendered in about 45 s.

## Measure and sound

- Before building, break the references down with [reference breakdown](../assets/reference-breakdown/README.md) (cuts, transitions, still share) and [`beats.py`](../assets/motion-sync/README.md#analysing-a-supplied-track); after rendering, run [motion activity](../assets/motion-quality/README.md#motion-activity) and the breakdown on your own reel and compare the cut rate and still share.
- Sound: [sound for supplied footage](../assets/motion-sound/README.md#sound-for-supplied-footage) with the board cuts and one `--hit` per action (message pops, typing ticks, the send, each hit, saw strokes, the drill, each whoosh, the logo landing) and `--reveal` on the end card. Choose the key from the brand's mood (`--set key="F major"` for a light, family brand) rather than accepting a minor key the analysis picked from dark boards.

## Evidence

On 2026-10-19 two reference reels supplied by the owner (40 s and 18 s, 1080×1920) were broken down: 29 and 18 cuts, 172 and 108 BPM, still share 16 % and 11 %. A Knock Knock reel (children's woodworking classes) was then built in a Linux container with HyperFrames 0.8.149 from the client's logo: chat hook, the logo's nail as the carrier and as the I of four verbs, saw, drill, hammer and set-square boards, a halftone summary, chat payoff and logo assembly, 16.7 s, motion activity PASS (15 % still, longest 0.67 s), 51 sound cues on their frames at −14 LUFS. Four review rounds with the owner produced the rules above: the vector, bold, centred letter carrier; the saw in its kerf; drilling into the board's face followed by the fly-through; longer chat reading time. The owner approved the brand-matched palette and tempo. The client's files are not stored in the package; host behaviour outside Claude Code in a container is not verified.
