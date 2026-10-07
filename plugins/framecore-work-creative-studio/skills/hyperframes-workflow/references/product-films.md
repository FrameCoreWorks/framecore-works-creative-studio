# Product films

A product film shows a real product working: its screens inside a phone or a window, one step at a time, with every move timed. Studio builds it from the user's own screenshots with the [`device` scene kind](../assets/motion-scenes/README.md#device-scenes), so it runs in every renderer (preview, Python renderer, Remotion) and needs no access to the app's code. The rules are adapted from [kaventro/motion-designer](kaventro-motion-designer-adaptation.md), which rebuilds interfaces in HTML instead.

## Materials

- **Screenshots of the real product**, one per state the film shows (before and after an action, a detail, a result), at the device's native size or larger. PNG or JPEG; a data URI in the contract keeps the film self-contained and is required for the browser export. Record each in `assets` with `src`, `width`, `height`, `alt`, `source` and `status`.
- **Fictional data on screen.** Names, amounts, files and people in the screenshots are invented and plausible; no real customer data, even blurred. Card numbers show only fictional last digits. Label illustrative numbers ("Example data") when they could be read as claims.
- **Real features only.** Show what the product does, the way it does it: opt-in features as the user turning them on, never as defaults; nothing about speed, accuracy, privacy or on-device processing that the product does not support.
- Ask only for what is missing: the screenshots, the format and length, the features that must appear and claims to avoid. Studio does not invent a product's interface.

## Story

1. **Hook in the first two seconds:** the strongest action or result, or the problem it solves.
2. **One flow per scene,** in the product's own words: a screen, the action (a screen change), the result held long enough to read.
3. **The biggest result on the reveal** (on the drop when there is music), then a pull-back.
4. **End card:** name, one line in the product's voice, where to get it; the last frame can rhyme with the first.

## Rules for the frame

- **The device is always there.** A phone keeps both side edges and its island in frame; a window keeps its title bar and controls in frame. Never show the interface full-bleed. Keep camera focus at about 1.5× or less and aim it so the island or title bar stays visible.
- **One action per beat, then a hold.** A screen change takes the transition (12 frames by default); its result holds 1–2 s before the next action. Camera moves happen between actions, never during one.
- **Captions beside the device, never over it.** The `device` kind puts the caption on the free side in landscape and above the device in vertical formats.
- **Motion comes from the product.** Screen changes push like the product's own navigation; no crossfades between scenes, glow, 3D flips or particles on the interface.
- **Readable on a phone.** Text that matters is at least about 20 px on the 1080-short-side stage; move the camera in rather than shrinking the film, and review at phone size.

## App Store previews

App Review Guideline 2.3.4 allows only captures of the app itself (with narration and text overlays) in an App Store app preview, and 2.3.7 asks not to show prices. A Studio product film with drawn device frames is for websites, social posts, press and launch pages. For an App Store preview, record the app itself and say so.

## Contract example

[`examples/app-film.motion-score.json`](../assets/motion-scenes/examples/app-film.motion-score.json) shows a phone with two screens, a push between them, a camera focus on the new row and a caption, a desktop window with a caption on the other side, an end card, and a 9:16 variant. Its screenshots are original and show fictional example data.
