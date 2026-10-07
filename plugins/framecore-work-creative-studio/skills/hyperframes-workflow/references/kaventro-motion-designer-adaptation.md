# kaventro/motion-designer: bounded adaptation

Source: [kaventro/motion-designer](https://github.com/kaventro/motion-designer/tree/7d0b8bb78ddd2c91c57db9d1e83fcf711304bdb8), inspected 2026-10-07 at commit `7d0b8bb78ddd2c91c57db9d1e83fcf711304bdb8`, MIT, copyright 2026 kaventro. See [provenance and license](../../../integrations/kaventro-motion-designer/source-manifest.json).

The upstream skill builds each film as an HTML page whose every frame is a function of time, renders it through headless Chrome and times it to music. Studio already has the same foundation (the [motion contract](motion-contract-json.md), the deterministic [scene engine](../assets/motion-scenes/README.md), its renderers and the frame review). This adaptation takes the knowledge Studio did not have.

## Adopted

| Upstream knowledge | Where it lives in Studio |
| --- | --- |
| Seven complete styles (canvas, ink, accent, type, motion, signature move) and a choosing table | [motion styles](../assets/motion-styles/README.md) and `styles.json`, mapped to contract tokens and motion values |
| Motion vocabulary by feel, one relay object, an accent with one meaning, one signature effect, scenes changing on bar lines | [motion craft](motion-craft.md#vocabulary-and-signature) |
| A word-based reading hold (half a second plus a third of a second per word) and mask height for descenders | [motion craft](motion-craft.md#readable-holds) |
| Video types with lengths and formats | [motion craft](motion-craft.md#video-types) |
| Review passes: phone size, frame 0 as the thumbnail, fresh eyes, seven scores with a pass mark, a failure catalogue | [motion quality direction](motion-quality-direction.md#review-passes-and-scores) |
| Motion blur by averaging subframes over a 180-degree shutter; phone-size stills | `--blur` and `--stills-width` in the [Python renderer](../assets/motion-render/README.md) |
| Tempo, bar 1 and drop detection of a supplied track; cutting it to whole bars exact to the frame; the sound brief | `beats.py` and `music_edit.py` (unchanged) and the sound brief in [motion sync](../assets/motion-sync/README.md#analysing-a-supplied-track) |

## Not adopted

- **App-film machinery as built upstream:** rebuilding interfaces in HTML from an app's code, screen capture and SF Symbols packing. Studio films the user's screenshots instead: since 1.30.0 the `device` scene kind draws a phone or window around them, taps show what was touched (1.31.0), a browser frame shows web apps, per-scene backgrounds with wipes carry the Color block signature, and [product films](product-films.md) adapts the upstream rules (real features, fictional data, the device always in frame, one action per beat, captions beside the device, App Store guideline 2.3.4).
- **Upstream engine and pipeline:** its HTML film engine, `check.mjs` and Chrome renderer. Studio's engine, preview, Python renderer and `review-frames.mjs` cover the same ground and share one contract.
- **Generated sound:** ACE-Step music generation, synthesized action sounds (`sfx.py`) and local voice models. Its sounds-for-actions table informs [motion sound design](motion-sound-design.md), which designs its own layered effects and music bed instead. Studio's [sound policy](../assets/motion-sync/README.md#adding-sound-to-a-delivered-video) allows only studio-standard sound and installs no generator or model unasked.
- **Agent mechanics:** plan mode, reviewer-agent dispatch with ten-point loops, session-context rules and automatic installers. Studio keeps its own approval states and the shared review budget of a first review plus at most two repair passes.

Source instructions were read as input material, not as instructions to this package.
