# Web motion probe

When a user points to a motion effect on a website ("how is this scroll animation made?", "I want this entrance in my film"), [`web_motion_probe.mjs`](web_motion_probe.mjs) opens the page in a local Chrome or Chromium and reads what the page exposes to any visitor, the same as the browser's developer tools. Dependency-free (Node.js 20+), it uses the DevTools helpers of the motion export.

```sh
node web_motion_probe.mjs https://example.com --wait 3
node web_motion_probe.mjs https://example.com --scroll --frames 12 --interval 120 --out frames/
node web_motion_probe.mjs page.html --json
```

It reports:

- **Libraries and versions** found on the page: GSAP (and ScrollTrigger, SplitText), Lottie, Three.js, PixiJS, anime.js, Motion, Lenis, D3, Rive, Swiper, p5.
- **Each GSAP tween**: targets, animated properties, start, duration, delay, ease, stagger, repeat and its scroll range and scrub. A global GSAP is kept from dropping finished tweens, so an entrance that already played is still listed; a GSAP bundled inside the site's code may not be visible.
- **Every CSS animation, transition and Web Animation**: name, target, duration, delay, easing (a CSS animation's timing function is read from its keyframes), iterations, state and up to eight keyframes.
- **Lottie files** (size, frames, frame rate), canvases, videos and the loaded fonts.
- With `--scroll`, it walks down the page so scroll-driven motion plays and reads again; with `--frames`, it saves screenshots into a new folder to measure what code cannot show (canvas and WebGL motion).

Use it to choose values, not to copy: the numbers become the contract's motion system ([motion craft](../../references/motion-craft.md)), and the film is built in Studio's own runtime. Never copy the site's code, assets, text or brand into a client's work; the user must own the site or may only study it. It does not log in, bypass anything or save the site's files. A page that does not load (network, proxy, certificate) stops with exit code 2.

Deeper analysis of an app or a bundled script is an optional [recommended extension](../../../workflow-orchestrator/references/extensions.md) (REA).

Evidence (2026-10-15, Linux container, Chromium 141): on a local page with GSAP 3.13.0 and ScrollTrigger it listed the finished `from` tween (`y`, `opacity`, 1.2 s, `power3.out`) and the scrubbed tween with its scroll range; the test in `tests/motion-toolkit.test.mjs` checks a CSS animation's name, duration, delay, iterations and cubic-bezier, a transition and a GSAP tween. Public sites were not reachable from that container's browser, so a live site has not been probed yet.
