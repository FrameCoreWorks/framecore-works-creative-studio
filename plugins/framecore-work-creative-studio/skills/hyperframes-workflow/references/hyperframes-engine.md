# HyperFrames as an optional engine

Checked 2026-10-09 against [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) at commit `3aa68869f7d4cec8b37cdfcb9cd539389b63abed` (CLI `@hyperframes/cli` 0.8.143, Apache-2.0). HyperFrames is HeyGen's open framework that writes video as HTML compositions and renders them in headless Chrome with FFmpeg. It ships agent skills (a `/hyperframes` router plus workflows such as `product-launch-video`, `motion-graphics`, `general-video`, `embedded-captions`, `music-to-video` and `media-use`) and a desktop Studio app for Mac and Linux. Studio does not bundle any of it; this reference says when to use it and how Studio stays in charge.

## When to offer it

Offer HyperFrames once, as an engine, when all of these hold:

- the user chose a finished video from code, or asked for HyperFrames or HyperFrames Studio by name;
- the host has a shell with Node.js 22 or newer, FFmpeg and a local Chrome or Chromium (Codex or a local project); ChatGPT's code execution is not such a host unless a check shows otherwise;
- the brief benefits from what it adds: a promo or launch film built from a website or product URL with its own assets, a longer narrated or multi-scene video, word-level captions on footage, or a music-driven edit.

Otherwise keep the bundled route: the Python renderer, the motion player, [sound design](motion-sound-design.md) and the [captions tool](../../caption-studio/assets/captions/README.md). Choosing area `8` never selects HyperFrames by itself; a recommendation names the reason.

## Installing it

Installing downloads code from npm and GitHub, so it needs the user's request for this project. Prefer the version-pinned route:

1. **HyperFrames' own plugin** for Codex or Claude Code, installed through that client's plugin manager. Its launcher runs the CLI version the plugin release names, and its skills say not to self-update during a task.
2. **Standalone skills**, when the user prefers them: `npx skills add heygen-com/hyperframes --full-depth` (the interactive picker's Core Skills group), or for agents `npx hyperframes@0.8.143 skills update`, which installs the core set from HyperFrames' current main. Whether `skills add` accepts a commit pin is Unknown; record the commit actually installed (`git ls-remote https://github.com/heygen-com/hyperframes HEAD`).
3. **The desktop Studio app** (hyperframes.dev/studio, HeyGen account sign-in) is the user's own tool; Studio can prepare the brief and review the result, not drive the app.

Never install into the plugin directory, and never overwrite an existing project's lockfiles to match a HyperFrames version; report the conflict.

The [environment check](../../workflow-orchestrator/assets/environment-check/README.md) shows whether HyperFrames' CLI or skills are already present and whether Node.js, FFmpeg and Chrome meet its needs, before anything is installed.

## Who decides what

HyperFrames' router describes itself as the mandatory entry point for every video request. Inside Studio it is an execution engine, not a second orchestrator:

| Decision | Owner |
| --- | --- |
| Intake, route choice, language, approvals and the welcome | Workflow Orchestrator |
| Brief, copy locks, claims, story and storyboard | Studio's owners (Copy Voice, Storyboard Sequence Architect, the campaign directors) |
| Composition, layout, animation and render | HyperFrames workflow chosen for the brief, with the approved brief as its input |
| Review before delivery | This skill: watch the render, run the [craft critique](../assets/motion-review/README.md) on its frames where a contract exists, check captions with the captions tool |
| Sound | HyperFrames' audio or this skill's [sound for supplied footage](../assets/motion-sound/README.md#sound-for-supplied-footage) on the rendered MP4, as the user chooses |

Pass HyperFrames the approved brief, exact copy, asset list with sources and rights, format and duration. Do not let its intent interview repeat questions the user already answered. Report its output with the commit or plugin version that made it.

## Assets and the HeyGen catalog

- **Website assets.** A launch film may take images, logos and copy from a website. Use them only when the user owns the site or says they may; record each asset's source page.
- **HeyGen media (`media-use`).** Use the HeyGen catalog (music, effects, images, voice, avatars) only when the user asks for it and has a HeyGen account; signing in to the `heygen` CLI is the user's action. Record each item's source and licence terms as the catalog gives them. Without that request, use the user's files, Studio's own sound design, or other sources the user approves.
- No paid generation, upload or publication follows from installing HyperFrames; each needs its own request.

## Evidence

On 2026-10-09 the owner reported a test in HyperFrames Studio: from a link to a perfume shop, an agent connected to the Studio app collected the site's assets and edited a high-quality reel. That is an owner report about HyperFrames, not a test of this route. No HyperFrames render has been run through Studio; the route is planned, not verified.
