# HyperFrames skill map

Checked 2026-11-04 against [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) tag `v0.9.13`, commit `06722eb9b90834beee636d1a9d41cd22452bd7fd` (npm `hyperframes` 0.9.13, Apache-2.0). Studio bundles none of these skills; they come with HyperFrames' own plugin or `npx hyperframes@0.9.13 skills update` ([engine](hyperframes-engine.md)). Studio keeps the brief, idea, copy, boards and review; this map says which HyperFrames skill builds each job and what it needs beyond a shell with Node.js 22, FFmpeg and Chrome.

## The nine published skills

| Studio job | HyperFrames skill | Install | Requires beyond the shell |
| --- | --- | --- | --- |
| Any composition: render contract, work loop, format, motion, look, captions, sound, storyboard, per-type notes (launch, explainer, music, vertical, data, 3D, character) | `hyperframes` | core | none |
| Init, check, snapshot, timeline edits, beats, audio measures, local render | `hyperframes-cli` | core | none for local work; **cloud render and `publish` need a HeyGen account** |
| A named look, effect, transition, caption style, chart or card (about 450 blocks); search before hand-building | `hyperframes-registry` | core | none |
| Music, effects, voice, avatars, generated video, transcripts, cutouts, grades | `media-use` | core | free local tools for transcripts, cutouts, grades and mixing; **HeyGen catalog, voice, avatars and generation need a HeyGen account and credits**. Studio defaults to the user's files, [Open Assets](../../pipeline-core/references/open-assets-native-routing.md) and its own sound design; HeyGen only on request |
| Port Remotion, Motion Canvas, Lottie, Three.js, p5.js or canvas work, or reuse Manim, After Effects or Blender renders | `remotion-to-hyperframes` | on demand | none; only on an explicit port request ([Remotion](../../remotion-video-production/SKILL.md)) |
| Rebuild a video file as an editable project and diff it frame by frame | `reverse-any-video` | on demand | `hyperframes reverse` opens a run noted with HeyGen; parts are **HyperFrames Pro**. Studio's rules: [reference style rebuild](reference-style-rebuild.md) |
| A new episode in a catalogue style (collage, finance, science, 3D brand, true crime) | `style-sampling` | on demand | **HyperFrames Pro** subscription and `hyperframes auth login` |
| Figma frames, tokens, logos, storyboard sections | `figma` | on demand | **Figma access** (the user's link and token or connector) |
| A live deck with presenter mode | `slideshow` | on demand | none (`hyperframes present`); not a rendered video |

Core skills install with `npx hyperframes@0.9.13 skills update`; on-demand ones with `npx hyperframes@0.9.13 skills update <name>`. Inside HyperFrames' plugin, its skills say not to update themselves during a task. The desktop **HyperFrames app** (`hyperframes open`, `catch-up`) is the user's own tool and needs a HeyGen sign-in; Studio prepares the brief and reviews the result.

## Names removed in v0.9.0

HyperFrames 0.9.0 (2026-11-02) folded 22 skills into the nine above. An older install or note may still name these; route them as follows.

| Removed skill | Now |
| --- | --- |
| `hyperframes-core`, `hyperframes-studio`, `hyperframes-creative`, `hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-audio` | `hyperframes` (its `format`, `motion`, `look`, `sound` and `storyboard` references) plus `hyperframes-cli` for keyframes and audio measures |
| `motion-graphics`, `general-video`, `faceless-explainer` | `hyperframes` (types `explainer`, `vertical`, `data`) |
| `product-launch-video`, `pr-to-video` | `hyperframes` (type `launch`); Studio's [product films](product-films.md) |
| `music-to-video` | `hyperframes` (type `music`) with `hyperframes beats`; Studio's [motion sync](../assets/motion-sync/README.md) |
| `embedded-captions` | `hyperframes` (`captions` reference) and caption blocks in the registry; Studio's [caption formats](../../caption-studio/references/talking-head-caption-formats.md) |
| `talking-head-recut` | `hyperframes` (`overlays` reference); FrameCut's [moment roles and clips](../../opencut-video-studio/references/moment-roles-and-clips.md) |

## Telemetry

The CLI sends anonymous usage data by default. Set `HYPERFRAMES_NO_TELEMETRY=1` (or `DO_NOT_TRACK=1`), or run `npx hyperframes telemetry disable`, before the first command when the user has not agreed to it.

## Evidence

2026-11-04, Linux container, Node.js 22.23.4: `npx hyperframes@0.9.13 init demo --example swiss-grid --non-interactive --skip-skills --resolution portrait`, then `render`: 1080 x 1920, 30 fps, 300 frames, 10.0 s, rendered in 18.1 s with software GPU, no warnings. Skill routing through Studio with 0.9.13: NOT_RUN.
