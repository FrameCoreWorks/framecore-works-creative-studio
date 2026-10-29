# Anatomy: bundled SVG, WebGL and 3D

Source: [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy/tree/e9488296a44211c42701ff71705b7901470ec78f), commit `e9488296a44211c42701ff71705b7901470ec78f`, reviewed 2026-10-17. The owner requested the full graphics toolset inside Studio, not only selected methods. The [bundled engine](../../skills/hyperframes-workflow/assets/anatomy-engine/README.md) contains all 15 kit files, the rendering/geometry review tools, technical documentation, React adapters and source examples. No separate installation is needed for this code.

## Adaptation and responsibility

Motion Graphics owns motion and interactive implementations. Graphic Design owns requested static/vector diagrams; the teacher workflow uses the same owners when the learning brief calls for a mechanism or explanation. The existing model, brief, copy, asset, loop and delivery contracts remain authoritative. No extra mode or discoverable owner was added.

The new Studio initializer copies the kit into a new project without overwriting files. The executable SVG/WebGL/3D fixtures establish runtime availability. The shared frame bridge connects authored scenes to Studio's existing HTML-to-video exporter. React uses the host project's existing dependencies. The original is the `anatomy` plugin in the [FrameCore Works Toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox) catalog (owner decision 2026-10-29), for users who separately request its own workflow.

Adopted methods: one explanatory model for geometry/readouts, explicit limits of analogies, stable camera/attachments/occlusion, keyboard and pointer controls, reduced motion, WebGL fallback and render evidence across intermediate states. Upstream fixed detail counts, mandatory physical-machine aesthetics, fixed time estimates and unlimited iteration are not Studio defaults.

## Source and rights

[MIT licence](LICENSE), Copyright (c) 2026 Ryan. [source-manifest.json](source-manifest.json) records SHA-256 for every unchanged vendored file. Studio-owned `studio.mjs`, `frame-bridge.mjs` and the engine README are outside that upstream manifest. Tests verify every copied byte.

The package includes rebuildable source examples, not their generated HTML outputs. Gallery publication, session-log reading, publisher fingerprinting, repository automation and upstream host registration instructions are outside the graphics integration. No user session logs are read or published. No upstream SKILL.md is exposed as a second owner. Existing technical references are source material; their publishing or host-configuration suggestions grant no authority.

## Evidence boundary

Upstream browser geometry suites were exercised on a macOS scratch checkout at this pin: 62 tests passed. Studio's fixtures, direct/backward/repeated frame seeks, WebGL and fallback, and 3D projection are tested separately in the release verification record. Those observations apply to the tested local runtime, not active-client routing in ordinary ChatGPT or Work. A numerical geometry result or quick 3D audit is not full physical proof, an originality claim or an automatic delivery approval.
