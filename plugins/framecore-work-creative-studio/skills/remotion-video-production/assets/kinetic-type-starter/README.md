# Kinetic type starter (Remotion 2D)

An original, synthetic starting project for the most common code-motion route: kinetic typography, title sequences and short 2D brand or product statements in Remotion. It is a teaching fixture, not a client concept or a mandated style. Use it through [Remotion Video Production](../../SKILL.md) and the shared [motion workflow](../../../hyperframes-workflow/references/code-based-motion-graphics.md).

## One contract for code and review

[`motion-score.json`](motion-score.json) is the single source for size, FPS, frame count, scenes, readable holds, exact copy, brand tokens and motion values. It extends the Motion Graphics Workflow score format, so the same file passes `validateScore` in `hyperframes-workflow/assets/motion-quality/score.mjs`. The composition reads it directly; change the contract, not hard-coded numbers in components.

- 1920 × 1080, 30 FPS, N = 300 frames, 10 seconds, frames 0..299, intentional silence.
- Two more [formats](../../../hyperframes-workflow/assets/motion-scenes/README.md#formats) from the same contract: `9x16` (1080 × 1920) and `1x1` (1080 × 1080), with smaller title and end-card type; the steps stack vertically there.
- `title` [0,127): line mask reveal, readable hold [24,117).
- `steps` [117,215): three items with an 8-frame stagger and a connector growing at constant speed; hold [149,205).
- `end` [205,300): slow-settling resolve and the longest hold [230,300); the final frame is stable.
- Motion values follow [motion craft](../../../hyperframes-workflow/references/motion-craft.md): 15-frame entries with ease-out cubic, 10-frame exits with ease-in cubic, ease-out expo for the final resolve.
- Copy is illustrative English; Arial is a system font, not a locked brand asset.

## Files

- `src/Root.tsx`: registers `KineticType` for the base size and `KineticType-<id>` for each format.
- `src/motion.ts`: types for the shared motion contract.
- `src/motion-scenes.mjs`: the shared [scene engine](../../../hyperframes-workflow/assets/motion-scenes/README.md), identical to the plugin copy.
- `src/KineticType.tsx`: a generic renderer that draws any declared scene kind from the master frame.
- `check-score.mjs`: dependency-free contract check, including the reading-hold heuristic.

## Authorized local use

Copy this folder to a new authorized project outside the installed plugin before installing dependencies or writing outputs. Requires Node.js 20 or newer.

```sh
npm ci
npm run check
npm run storyboard
npm run typecheck
npm run still
npm run render
npm run render:9x16
npm run render:1x1
```

`npm run studio` starts a local preview server; stop it after review. Remotion may download a headless browser when none is configured; pass an available browser with `--browser-executable=<path>` to avoid that. Rendering writes into `out/`.

## Adapting it

1. Replace the storyboard fields, copy, tokens and scenes in `motion-score.json` with the project contract (see [motion contract JSON](../../../hyperframes-workflow/references/motion-contract-json.md)). Run `npm run storyboard` to show it for approval and `node check-score.mjs motion-score.json --storyboard` before building; fix every FAIL and review every WARN.
2. Declare scenes with the six [scene kinds](../../../hyperframes-workflow/assets/motion-scenes/README.md) where they fit; they render identically in the single-file preview. For a scene no kind covers, add a small component that derives every state from the frame. Do not add CSS transitions, timers or unseeded randomness.
3. Load real brand fonts before rendering and check the longest strings and diacritics at target size.
4. Inspect stills at the first frame, each scene boundary, each hold and the last frame, then watch the full render.

## Verification boundary

During package preparation this example was typechecked, passed `npm run check`, rendered stills and a full H.264 file (1920 × 1080, 30 FPS, 300 frames, yuv420p) in a Linux development container with a local headless Chromium. That is evidence for this synthetic example in that environment only. It does not establish rendering in ChatGPT, Work or a particular Codex session, and it is not design approval for client work.
