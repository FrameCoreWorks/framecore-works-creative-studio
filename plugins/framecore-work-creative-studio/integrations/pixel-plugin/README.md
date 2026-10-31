# Pixel Plugin and pixel-mcp: decision map

Reviewed 2026-10-22 at [`dee3506`](https://github.com/willibrandon/pixel-plugin/tree/dee350645b705916655c013f208bf5580ecb9317) (plugin 0.5.0, MIT, [licence](LICENSE)) together with its engine [pixel-mcp v0.5.0](https://github.com/willibrandon/pixel-mcp) (MIT), after the owner sent the repository. The knowledge was mined first and the repository listed second; nothing was run. No code or text is copied: methods are written again in Studio's own words.

## What Studio took

| Idea | Where it went |
| --- | --- |
| Pixelate (box-average down, nearest-neighbour up), posterize to N levels, ordered Bayer dither | three versioned FrameCut picture effects: `pixelate`, `posterize`, `ordered_dither` (defaults change nothing; ordered dither is pinned to screen coordinates, so it does not crawl on video) |
| Hue-shifted colour ramps, one light direction, no "pillow shading", palette tiers, palette swaps by role | the Animate engine's Animate reference, Pixel look (`references/animate-engine.md`; the engine's own `STYLE.md` stays byte-identical to its source) |
| Choosing a Bayer size (2x2, 4x4, 8x8) and when error diffusion is wrong | Animate reference, Pixel look |
| Frame-based action timing (strike, anticipation, idle, walk key poses, blink) | Animate reference, Pixel look, expressed in render frames instead of milliseconds |
| Scaling a user's own sprites by whole numbers, nearest-neighbour, integer positions, sheet padding and frame data | Animate reference, Pixel look |

## What Studio did not take

| Part | Reason |
| --- | --- |
| The Aseprite MCP server, its 40 tools, the binaries, `.mcp.json`, setup commands | Needs a commercial program and five unverified prebuilt executables; listed as an optional extension for Claude Code users who own Aseprite |
| Error-diffusion dithering, an octree quantizer, palette harmony scores, auto-shading | Slow or unstable on video, or poorly done in the engine (its shading ignores the light direction, its smooth-shading dither is a no-op, texture dither patterns do not work, its antialias suggestions darken colours) |
| Texture pattern lists, console palette catalogues, sprite-size tables, Unity, Godot, Phaser, GameMaker and LibGDX integration | Ready-made lists and game-development content outside Studio's scope |
| GIF delivery notes, selective antialiasing, harmony analysis | Noted for later; Studio delivers MP4 and its pixel look forbids antialiasing |
| Many numbers and examples | The plugin contradicts itself in places (two walk-cycle definitions, a white highlight against its no-white rule, hue shifts in the wrong direction for warm colours) and several examples have empty bodies |

The original is no longer recommended: the [FrameCore Works Toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox) catalog listed it from 2026-10-29 and removed it in Toolbox 1.4.0 (owner decision 2026-10-31: Toolbox 1.4.0 lists only tools with no account, API key or separate desktop app). Studio installs nothing from it. Studio's review evidence: Evidence: static review of the plugin and engine, `claude plugin validate` (passed with one warning), tests for the three effects (`tests/framecut_pixel_test.py`). The server, Aseprite and every tool are NOT_RUN.
