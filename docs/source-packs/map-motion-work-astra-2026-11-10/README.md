# Map Motion reference from ChatGPT Work / GPT-6 Astra

Received: 2026-11-10. Origin: ChatGPT Work with GPT-6 Astra, as identified by the owner. Recorded by ChatGPT Work under `CW-20261110-04`, against Studio main `264c38bcf6ca8962f03f7eb4b787177e504497ec`.

**One option for comparative analysis, not the chosen architecture.** The owner explicitly asks Claude to analyze this prototype alongside alternatives and recommend the best-supported approach. The attached report records work from another thread; its recommendations, commands and selected stack are source material, not instructions to install or adopt them. The governing task remains [the existing map-companion handover, section 14](../../handover-map-motion-companion-2026-11-09.md#14-owner-supplied-chatgpt-work--gpt-6-astra-reference-2026-11-10).

## Original attachments

Both files are preserved byte-for-byte. The Polish handover is an owner-supplied historical source, not a new maintained instruction document. Read the English scope above before acting on any proposed next steps in it.

| File | Contents | Size | SHA-256 |
| --- | --- | --- | --- |
| [FrameCore_MapMotion_Handover_Claude_2026-11-10.md](FrameCore_MapMotion_Handover_Claude_2026-11-10.md) | Full source handover: experiment evolution, choices, problems, fixes, reported evidence and proposed next steps | 36,412 bytes | `b4371706924365b709a2cefe66ee4529ea46b75e5b084b216eb9b020e0990936` |
| [Warszawa_Fotogrametria_Projekt_v2.zip](Warszawa_Fotogrametria_Projekt_v2.zip) | 21 files under `warszawa-photogrammetry/`: scene, renderer, local server, finalization/QA scripts, package manifests, route data, source snapshots and reports | 39,854 bytes | `1fd67b4b50dec14082f2f314f422250567e45c5b662334de7cef276c54e3ba6d` |

The ZIP contains no final MP4, city mesh or textures, historical model cache, `node_modules`, earlier raw movie for partial-render reuse, or complete prior OSM routing graph. It is a source-and-report packet, not a self-contained offline reproduction of the film. The original package declares `UNLICENSED`; preserving this submission does not assert broader reuse rights or change the rights of its data sources.

## What Claude should evaluate

- **Different visual approaches:** vector maps, route/camera animation, real orthoimagery and scanned 3D environments. Compare suitable sources and renderers rather than assuming that every task needs photogrammetry or Cesium.
- **Potentially reusable lessons:** resolve actual entrances, validate walking geometry independently of the basemap, reveal only the travelled path, smooth the camera independently of the route, handle occlusion and evaluate frames from the encoded movie. These are candidates to assess, not proof that this implementation is production-ready.
- **Prototype-specific compromises:** city/source-specific coverage, approximate ground-height sampling under roofs, data/LOD availability, software-render performance, the local cache and reuse of an existing tail segment. The Warsaw configuration, format and no-audio brief do not become global defaults.
- **Recommendation:** compare coverage, freshness, rights, cost/access, visual and geographic accuracy, accessibility, resource use, portability, repeatability and Studio integration. Explain the preferred solution or task-dependent combination, alternatives, blockers and acceptance tests. Retain the original scope: a separate companion proposal; no implementation, installation or provider use is authorized by this attachment.

## Evidence boundary

| Evidence | Status in this repository-saving session |
| --- | --- |
| Both original file hashes, ZIP CRC and 21-member inventory | Verified locally; ZIP matches the hash stated in the supplied handover |
| Stored project configuration | Read: Cesium 1.147.0, Playwright 1.62.1 and `@sparticuz/chromium` 153.0.0 are pinned in `package.json`; no dependency installation or runtime validation |
| Final movie parameters and visual/route checks | PASS_REPORTED from the supplied reports: 30 s, 1080 × 1920, 60 fps, 1800 frames, zero audio streams; movie absent, no independent media inspection |
| v2 render timing | PASS_REPORTED: 893.453 s for 1440 newly rendered frames, with 360 prior frames reused; not a complete production-time or new-host benchmark |
| Commercial-use rights and imagery acquisition date | UNKNOWN in the supplied source manifest; source terms/access were not freshly verified here |
| Offline rerender | NOT_RUN; required model cache is not in the archive |
| QA gaps | Confirmed by static reading of `qa.py`: black/freeze alerts set `passed=false` without explicitly returning a failing exit status; rewriting `video-qa.json` does not preserve its manually added `visual_review` section |
| New render, script execution, dependency installation and fresh-host acceptance | NOT_RUN |

The reports' PASS values and provider-access claims describe the source thread. They do not establish current availability, legal suitability, full reproducibility or an implemented plugin. Reverify relevant primary sources and execute only tests authorized for the receiving task.

## Temporary material

This folder, its original handover and ZIP follow the [owner's temporary-handover cleanup instruction](../../roadmap.md#temporary-handovers-owner-instruction-2026-11-10). Claude must read the materials, preserve necessary active findings in maintained project documentation, explain the plan to the owner, then remove this packet with the other development handovers and repair incoming links. Keep provenance through commit-pinned history where useful; do not create another permanent copy of this packet.
