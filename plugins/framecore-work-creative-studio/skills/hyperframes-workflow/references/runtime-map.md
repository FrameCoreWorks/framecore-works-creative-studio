# Motion runtime map

Choose the runtime from the host first, then from the brief. The host decides what can actually run in this conversation; the brief chooses among what can. This map is the first stop for every motion job; the [runtime selection](code-based-motion-graphics.md#runtime-selection) rules and the [toolkit routing table](motion-toolkit-routing.md#choose-by-the-required-result) apply after it, inside the column the host allows.

## 1. Find the host column

Use the profiles of the [capability card](../../workflow-orchestrator/assets/capability-card.json) and check by trying, never by assuming:

- **None:** no code execution (voice, or code execution switched off). Studio writes the contract, prompts and timing tables.
- **Code execution:** Python in a sandbox (ordinary ChatGPT, ChatGPT Work, Claude apps with code execution). Pillow, numpy, ffmpeg, Node and a browser are checked by running them. ChatGPT Work's sandbox had Node.js, FFmpeg, Chromium and the npm registry (owner test 2026-10-14), so the rows below marked yes for code execution that need Node and a browser run there too.
- **Shell:** a local shell (Codex, Claude Code, a local project) with Python, usually Node.js and sometimes a local Chrome or Chromium and FFmpeg.

The [environment check](../../workflow-orchestrator/assets/environment-check/README.md) reports each tool's status per host and installs what is missing when the user allows it.

## 2. Read down the column

| Job | Capability | None | Code execution | Shell | Needs |
| --- | --- | --- | --- | --- | --- |
| Render the MP4 from the contract | `motion_render` | no | yes | yes | Python, Pillow, ffmpeg |
| Craft critique of rendered frames | `motion_critique` | no | yes | yes | Python, Pillow |
| Four-verdict acceptance | `motion_acceptance` | no | yes | yes | Python |
| Sound effects and a music bed | `motion_sound` | no | yes | yes | Python, numpy, ffmpeg |
| Sound for supplied footage | `footage_sound` | no | yes | yes | Python, numpy, ffmpeg |
| Captions from timed words or an SRT | `captions` | no | yes | yes | Python |
| Burned-in captions on a video | `caption_burn_in` | no | yes | yes | Python, Pillow, ffmpeg |
| Brand kit, ad templates and variants | `motion_variants` | no | yes | yes | Python |
| Watch and export in the motion player | `motion_player` | yes | yes | yes | the user's browser |
| Contract check and storyboard view | `motion_contract_check` | no | no | yes | Node |
| Beat grid and caption sync | `motion_sync` | no | no | yes | Node |
| Contract revision with a change list | `motion_revise` | no | no | yes | Node |
| Automated frame review | `motion_frame_review` | no | no | yes | Node, browser |
| Visible-text audit of custom HTML | `motion_text_audit` | no | yes | yes | Node, browser |
| Remotion render | `remotion_render` | no | no | yes | Node, network, browser |
| HyperFrames engine | `hyperframes_engine` | no | yes | yes | Node, ffmpeg, browser, network |
| Animate engine (illustrated looks) | `animate_render` | no | no | yes | Node, browser, ffmpeg |
| Polish word times for an Animate voice-over | `animate_voice` | no | no | yes | Python |

A "yes" means the bundled tool can run in that profile once its needs are met; it is not a claim that it ran. When a need is missing, deliver what the capability card's `when_missing` says and mark the output NOT VERIFIED.

## 3. Default route per column

- **None.** Write the checked contract by hand from the [contract reference](motion-contract-json.md), using the declared scene kinds, and deliver it with the motion player link; the user's browser plays and exports it.
- **Code execution.** Render the MP4 with the [Python renderer](../assets/motion-render/README.md) copied as `<id>.render.py`, critique and accept it, add sound when asked. Start an ad from a [template](../assets/motion-variants/README.md) and make language or format versions with `variants.py`. Everything renders from declared scene kinds. Where the check finds Node.js 22 or newer, FFmpeg, a Chrome or Chromium and the npm registry (ChatGPT Work), HyperFrames is the route for client reels and looks that need custom code: with the user's consent install the pinned CLI for the session (`npm install -g hyperframes@0.8.149`), set `HYPERFRAMES_BROWSER_PATH` to the Chromium the check found, run `hyperframes doctor` and a short test render, then build as in [client reels in Claude Code](claude-code-reels.md). The install lasts only for that session. Without those tools a look that needs custom code is out of reach, so say so and offer the nearest scene kinds.
- **Shell.** Client reels and ads are HyperFrames compositions by default ([client reels in Claude Code](claude-code-reels.md)); for contract work, all of the above, plus the Node checker and the browser frame review. When the npm registry is unreachable, so neither HyperFrames nor Remotion installs, a hand-written HTML composition renders with the dependency-free [HTML capture](../assets/motion-export/README.md#hand-written-html-to-mp4-without-npm) (Node.js, FFmpeg, a local Chrome or Chromium). Offer an engine only when its needs are met and the brief calls for it: the GSAP or [Remotion starter](../../remotion-video-production/assets/kinetic-type-starter/README.md) for custom scenes, the [glTF product turntable](../../remotion-video-production/assets/gltf-turntable/README.md) for a 3D packshot, [HyperFrames](hyperframes-engine.md) for website films and longer narrated edits, the [Animate engine](animate-engine.md) for illustrated looks, and the toolkit layers (PixiJS, D3, Three.js, Lottie, Manim) for what the scene kinds cannot draw.

## 4. Pick by brief inside the column

The [brief index](../assets/motion-prompt-library/brief-index.json) tags each brief type with `scene_kinds` that every renderer runs and a `contract` (an example or ad template) that renders as it is. A brief with no scene kinds (looping idents, 3D, generative backgrounds, music-cut edits) needs custom code, so it needs a shell column; in the other columns, offer the nearest declared scenes or deliver the contract and prompts.
