# Talking-head caption formats

Studio's own notes on caption and overlay formats for a single speaker filmed to camera (9:16, locked or near-locked shot). Written 2026-11-04 after reviewing the format guides shipped in the HyperFrames desktop app (0.9.12); those guides carry no licence, so nothing here is copied from them: no wording, presets, scripts, palettes or fonts. Each format below is a pattern; the build uses the user's brand, Studio's [readability defaults](readability-defaults.md) and [platform specs](platform-caption-specs.md).

## Shared rules

- **The words are the speaker's.** Captions come verbatim from a word-level transcript (Whisper or the user's own); never rewrite, shorten or add words on screen. A written hook title is a separate layer and needs Copy Voice's exact copy.
- **Read the take into beats first:** hook line, each thing the speaker names (a product, a person, a page, a step), the turn, the close. Every visual change lands on the word that names it, not on a sentence boundary.
- **Check framing before choosing a format.** Note where the head sits (top of the head, chin line, shoulder width) on the first, middle and last frame. A format that puts text behind or beside the head needs room there; if the head is too high or too wide, pick another format or crop, and say so.
- **Platform chrome wins.** Keep every caption inside the 9:16 title-safe box of the target platform; nothing under the right-hand action rail or the bottom caption/description band.
- **Hold long enough to read.** At least the readability default per line; if a named-word cut is shorter, the caption may stay while the picture changes.
- **Visual QA:** extract frames at every caption change and check that no word is cut off, covered by the head or hands, or touching the safe-box edge.

## Formats

| Format | What happens | Needs | Watch for |
| --- | --- | --- | --- |
| **Word pills** | One or two words at a time in a rounded, slightly translucent pill near the chin line; the active word changes weight or colour | word timings | pills jumping position; keep one anchor line |
| **Accent behind the head** | One emphasis word per caption block set very large behind the speaker, so the head covers part of it; the other words small in front, under the chin | word timings and a **person matte** (segmentation of the speaker per frame) | the covered word must stay recognisable: the head may hide its middle, never its first or last letter |
| **Captions in depth** | Caption groups placed at different depths; a virtual camera pushes, trucks or whips between them, and hero words can pass behind the speaker | word timings, a person matte, a 3D or layered-depth composition | motion sickness: one camera move per beat, ease out before the next word group |
| **Cards behind the speaker** | The real thing the speaker names (a page capture, a screenshot, a recreated chat or terminal, a grid of posts) appears as a card behind head and shoulders on the word | the user's own captures and a person matte | only real, owned or permitted captures; recreate an interface only with real content the user supplies |
| **Takeover on the named word** | The graphic for the named thing takes the full frame for a beat, then hands back to the speaker; the hook can run as word-by-word uppercase pills | word timings and the visuals for each named thing | no more than one takeover per sentence; return to the face for the turn and the close |
| **Split with a breaking head** | Graphic in the top area, the speaker in a rounded panel below, with the head rising over the panel edge into the graphic | a person matte and room above the head | the head break must not hide the graphic's key text |

## Routes

- **With a shell (Claude Code, Codex):** build as a HyperFrames composition ([skill map](../../hyperframes-workflow/references/hyperframes-skill-map.md)); search the registry for caption blocks first. A person matte comes from a local cutout tool (HyperFrames' `media-use` lists free local routes) or from a matte the user supplies; without one, use word pills or takeovers only.
- **Without a shell:** deliver the caption file (SRT/VTT plus word JSON), the beat map and a style card for the user's editor; formats that need a matte are marked as needing one.
- FrameCut owns the edit when captions are one layer of a larger cut ([moment roles and clips](../../opencut-video-studio/references/moment-roles-and-clips.md)).

## Evidence

Source review only (2026-11-04). No format here has been built or rendered through Studio yet: NOT_RUN.
