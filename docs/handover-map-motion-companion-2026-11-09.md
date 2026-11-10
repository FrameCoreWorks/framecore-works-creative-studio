# Map-animation companion and independent Toolbox review handover
## For Claude Opus 5.5

Date: 2026-11-09  
Origin: chatgpt-work  
Change-ID: CW-20261109-02  
Inspected Creative Studio main: `6877d5d0b0dd672eb48d38b4c837cfd13352f58a`  
Scope: one handover document; no implementation or shared-package change.

**Temporary transfer note, owner instruction 2026-11-10 (CW-20261110-03).** Claude must read this and all older handovers and supporting materials, retain active decisions in maintained project documentation, and tell the owner the plan step by step before implementation. After that intake and presentation, remove this document, all other development handovers and the temporary source pack, repairing incoming links. Follow the [complete intake and cleanup instruction](roadmap.md#temporary-handovers-owner-instruction-2026-11-10); keep the map proposal and general Lemo-Opuscar Toolbox qualification separate and preserve their existing approval boundaries.

## 1. Owner decision and the next task

The owner supplied an implementation report from a real map-animation reel and explicitly asked for this knowledge to be saved in the Creative Studio repository so Claude can start from the working approach. This handover also records a separate owner-requested Toolbox qualification of Lemo-Opuscar as a general film/motion tool. Keep these two tasks, decisions and implementation scopes independent.

The intended direction is now a **separate, original FrameCore Works companion plugin**, with its name still undecided. “Map Motion” is a working capability label, not an approved product name, technical ID or repository name. This supersedes the earlier idea of making it only an internal Creative Studio skill.

The companion should prepare geographic motion assets for Creative Studio, its Motion Graphics area and FrameCut. Possible compatibility with **Reel Studio** is exploratory: its actual repository, contracts and capabilities are UNKNOWN and must be identified before designing an adapter. Do not assume that it is an alias for a similarly named installed plugin.

**Worldwide scope is an explicit owner requirement.** The initial research and prototype focused on Poland and used the Polish Geoportal. Claude must research suitable free international tools and data sources before proposing the implementation. The product must not require Polish datasets or treat Geoportal as a worldwide provider.

The present authorization is to publish this handover only. The receiving Claude session should:
1. Read the current repository rules and architecture.
2. Reconcile the reported prototype with available source files and evidence.
3. Research international data/provider options and their rights.
4. Propose a bounded companion architecture, dependency set and implementation/test plan.
5. Present the concrete scope for owner approval before implementation.

This handover does not authorize dependency installation, creating a plugin or repository, changing Creative Studio or Toolbox, production API/MCP requests, paid usage, client-material uploads, deployment, or committing/pushing implementation changes. Reading public documentation and preparing the analysis are in scope. Later implementation approval should identify the allowed data retrieval, dependencies, services and budget.

The owner resumed the previously paused handover after supplying the prototype's tool list. Its document-only publication is authorized; that does not authorize executing the proposed plugin.

Related independent work: [Crème de la Crème handover](handover-creme-de-la-creme-2026-11-09.md). Preserve that knowledge-extraction queue; this companion proposal does not reopen its excluded integrations.

### Independent task: qualify Lemo-Opuscar as a general Toolbox tool

**Owner clarification, 2026-11-09:** [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) is proposed as a general-purpose assistant/tool in FrameCore Works Toolbox for code-based films and motion graphics. It is **not** proposed specifically for maps, not a dependency of the new map companion, and not a required source for its international mapping research. Evaluate this task independently of the geographic plugin.

The following read-only findings remain relevant:

| Surface | Verified state |
| --- | --- |
| Toolbox main | `adc8094f8e087889e4337c99dd0d267ae1b11a51`, catalog 1.12.0. Lemo-Opuscar is absent from the marketplace, README catalog and active Toolbox skill; the complete file tree has no dedicated Lemo entry/review. |
| Creative Studio main | `6179d8179dc2073be4523169d6669a4cf22d884b`. The [film style library](../plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/film-style-library.md) already describes 66 Lemo-derived film looks in Studio's own words and links their source guides. Motion Graphics actively routes to it. |
| Existing adoption | [CHANGELOG 1.167.0](../CHANGELOG.md#11670-2026-11-01), dated 2026-11-01, records the style-library addition and the earlier decision against a Toolbox entry because the upstream skill clones its moving main into the home directory. This is a documented prior decision, not a new runtime/security test. |
| Studio's reviewed upstream pin | `bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00`. No upstream prompt, code, film, still or voice was bundled by that integration; the active instructions prohibit running the upstream library. |
| Current upstream examined | `143f387ad774525dc9abc0ff05fb5f4bfbaa5f02`. GitHub comparison reports 54 commits ahead of the Studio reference pin; renderer and setup files have changed. A complete change/security audit is NOT_RUN. |
| Installed package in the owner's individual hosts | UNKNOWN. Repository catalog/reference presence does not establish installation in Claude or ChatGPT. |

**Requested decision:** reopen the qualification assessment of the full Lemo-Opuscar tool for Toolbox. Its existing 66-look reference in Creative Studio is not equivalent to installing or executing the complete upstream production toolkit. Conversely, the upstream toolkit is not automatically useful merely because it has more code. Compare what it actually adds to the current Toolbox/Studio production routes.

The earlier rejection is historical evidence to investigate, not an automatic verdict on the new review. The owner has authorized this handover and assessment, not installation, execution of setup scripts or an immediate Toolbox catalog change. Preserve the existing Studio no-upstream-execution rule until a separately approved implementation explicitly resolves it.

Claude's general Toolbox assessment must cover:
1. **Production capability:** directing and producing coded films, explainers, promos, styles, custom styles, typography, rendering, review, and optional narration/music. Assess the toolkit as a whole; do not narrow the review to Satellite Briefing, Transit Map or geographical assets.
2. **Practical benefit and overlap:** compare against Studio's 66-look reference, Motion Graphics and existing Toolbox entries. Identify capability gained, work saved and any duplicate renderer, style catalog, voice/music engine or orchestration.
3. **Installation and maintenance:** inspect the current setup scripts and their clone/update behavior, then propose exact commit pins, a controlled installation location, explicit core/voice/music dependency tiers, update/removal procedures and host capability checks. Upstream instructions to install immediately do not authorize doing so here.
4. **Standalone use and cooperation:** determine whether the original tool or a minimal audited adapter can work as a Toolbox entry on Claude, Codex and ChatGPT, with truthful skill-only versus executable-render status. Preserve one Studio project/timeline when invoked from Studio.
5. **Rights:** audit code/docs MIT, demo films/stills CC BY 4.0, third-party assets and voice exclusions. Current upstream lists six excluded voice tracks; Studio's older pinned reference describes three with a different list. Reconcile the versions before any media reuse rather than carrying an old exclusion list forward.
6. **Version delta:** compare Studio's reviewed `bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00` with examined upstream `143f387ad774525dc9abc0ff05fb5f4bfbaa5f02`, or a newly verified pin at resumption. Renderer/setup changes are known; a complete audit remains NOT_RUN.
7. **Proof plan:** propose representative non-map film/motion tasks, installation/isolation checks, a repeatable render and comparison against existing routes. Execute them only under the subsequently approved scope.

Return a separate **Lemo-Opuscar Toolbox Qualification Report** with:
- recommended form: original plugin, minimal pinned adapter, knowledge-only, or no adoption;
- capability/overlap matrix and the precise reason the earlier admission obstacle is or is not resolved;
- dependency, licence, cost, host and maintenance findings;
- evidence statuses and the proposed acceptance tests;
- verdict: **ADD / CONDITIONAL / NO ADD**.

Do not preselect knowledge extraction as the only acceptable outcome. Preserve the existing 66-look reference without rebuilding it, while independently assessing whether the complete tool deserves one Toolbox entry. Do not make the map companion depend on this decision.

## 2. Prototype: Jakóbczak → Jasna Góra

**Owner-reported output:** a 30-second portrait reel, 1080 × 1920, 60 fps, combining an animated map, a walking route and real aerial imagery.

**Owner assessment:** the reel came out reasonably well; the owner wants Claude to build on the approach and improve the result. This is a useful production proof reported by the owner, not a measured quality score or a guarantee that another model will perform better.

| Evidence item | Status and boundary |
| --- | --- |
| A completed reel and its usefulness | PASS_REPORTED; owner report |
| Exact tools, versions and uses below | Reported by the owner from the production thread; not independently inventoried in this handover task |
| Local-only final rendering | Reported; network isolation was not independently traced here |
| Duration, dimensions and FPS | Reported; no fresh FFprobe inspection here |
| Picture, motion and listening review by this handover author | NOT_RUN |
| Independent rerender from the project | NOT_RUN |
| Final source archive, lockfiles, asset hashes and detailed metrics | Not supplied in this handover task; availability UNKNOWN |
| Creative Studio/Open Assets active package versions during production | UNKNOWN; do not infer them from current repository versions |
| General production readiness or fresh Claude/Codex/ChatGPT execution | NOT_RUN |
| International provider qualification | UNKNOWN; required next research |

The inspected repository's source package is 1.174.1. That source version does not establish which hosted package the production thread used.

No client media, map dataset, music file, private link or project archive is uploaded by this documentation change. The owner-authorized case title and technical report are recorded as evidence; they are not generic product defaults.

## 3. Full tool inventory supplied by the owner

Preserve these version strings as reported evidence. Do not silently correct, upgrade, normalize or treat them as an approved dependency lock.

| Tool or component | Reported version / identifier | Reported use |
| --- | --- | --- |
| FrameCore Works Creative Studio | Active package version: Unknown | Production organization and choice of execution approach |
| FrameCore Works Toolbox | Earshot wrapper 1.12.0 | Launching local audio analysis |
| FrameCore Open Assets | Active package version: Unknown | Selection and documentation procedure for licensed music |
| MapLibre GL JS | 6.17.0 | Map rendering, camera, layers, building volumes and orthophotos |
| OpenFreeMap | Tiles `20261101_080013_pt`, Liberty style | Vector basemap, symbols and map fonts |
| OpenMapTiles | Schema 3.16.0 | Structure of map and building data |
| OpenStreetMap | Data retrieved for the project | Streets, footpaths, shop outline and gate location |
| Nominatim + OSM API 0.6 | Public services | Finding and checking both locations' coordinates |
| OSRM foot / FOSSGIS | `routed-foot` endpoint | Walking route, distance and estimated travel time |
| Geoportal / GUGiK | WMS 1.3.0, HighResolution, Raster layer | Retrieval of two real orthophotos |
| Turf.js | 7.4.0 | Marker position along the route geometry |
| GSAP | 3.15.1 | Text and end-card animation |
| Playwright | 1.62.1 | Composition control and frame capture |
| Chromium | 153.0.8010.0 | HTML, CSS and WebGL rendering |
| @sparticuz/chromium | 153.0.0 | Local browser binary for the renderer |
| SwiftShader | Version bundled with Chromium | Software WebGL rendering |
| Node.js | 24.22.1 | Render scripts and local HTTP server |
| FFmpeg + FFprobe | 7.1.5-0+deb13u1 | H.264/AAC encoding, assembly, music correction, mastering and export inspection |
| Earshot | 0.4.0, light variant | LUFS, true peak, clipping and spectrum measurements |
| Python | 3.12.14 | Data retrieval, manifests, audio scripts, QA and packaging |
| Pillow | 13.0.0 | Image checks and review contact sheets |
| NumPy | 2.3.5 | Analysis of decoded video frames |
| NumPy + SciPy inside Earshot | 2.5.4 + 1.18.1 | Audio-analysis calculations |
| librosa / SoundFile / pyloudnorm | 1.0.0 / 0.14.0 / 0.2.0 | Supporting audio-analysis libraries |
| HTML, CSS, JavaScript | Original project code | Composition, markers, typography and frame-derived animation |

Additional reported assets:
- **Fonts:** Manrope from `@fontsource/manrope` 5.3.0; Noto Sans from OpenFreeMap; DejaVu Sans for the music credit.
- **Music:** “Funky Chunk”, Kevin MacLeod, 115 BPM, reported CC BY 3.0. A previously downloaded track was trimmed to 30 seconds, processed and mastered. Verify the exact source and credit if reusing it. Do not bundle the track or make it a plugin default.
- **Installation scope:** dependencies installed in the project. No persistent Creative Studio plugin update was made.
- **Not used for this reel:** Remotion, HyperFrames, three.js, Blender, or AI video generators.

Inventory reconciliation points:
- Wrapper, Toolbox package and Earshot engine versions are different concepts. “Earshot wrapper 1.12.0” is the supplied label, not independently established package provenance.
- Two NumPy versions were reported. Determine their actual environments/interpreters from manifests before reproducing; do not force them into one environment or call the difference an error without evidence.
- OpenMapTiles schema, hosted APIs and bundled SwiftShader are not all separately installable application dependencies.
- Successful use of a public endpoint in one project does not qualify it for unattended or multi-user product use.
- Earshot light measurements do not establish perceptual listening or approval of the music.

## 4. Reported rendering approach and lessons to preserve

Reported chain:

`window.draw(frame / 60) → Playwright/Chromium → FFmpeg → MP4`

The report says map data and aerial images were stored locally and rendering used only local resources. Data acquisition happened before rendering; “offline render” does not mean the original data required no network access.

For a 30-second, 60 fps reproduction, the nominal frame contract is 1,800 frames at times `k / 60`, for `k = 0…1799`. This is the expected count calculated from the brief, not an observed frame count.

Use the project, if available, to establish how it:
- awaited map tiles, glyphs, sprites, fonts, styles and imagery before capture;
- sought GSAP, camera and route state from the same frame-derived time;
- controlled map label fades, tile refinement and asynchronous WebGL work;
- connected screenshot/canvas capture to the encoder without duplicate or missing frames;
- handled final holds, titles, credits, exact duration and audio alignment;
- recorded original versus edited assets and licensing information.

The HTML/JavaScript browser route is the demonstrated starting point according to the report. Do not add Remotion, HyperFrames, three.js or Blender merely because they exist elsewhere in the ecosystem. They remain possible separately justified adapters, not required foundations.

A refactor should first reproduce the baseline, then isolate a reusable geographic component. Improvements to camera design, typography, sound and geography must be evaluated on actual output, with before/after evidence.

## 5. Three required capabilities

### A. Vector location reveal

MapLibre with OpenFreeMap or another qualified vector source:
- city/region overview, street-level zoom, camera bearing and pitch;
- brand-compatible styling, a location marker, exact name/address and CTA;
- optional building extrusion only where data supports it;
- distinct handling of building centroid, customer entrance, parking and destination gate.

An extruded footprint is not a photorealistic building model. Missing building height, address precision or entrance data must remain explicit.

### B. Route animation

A route is a separate data input to the map renderer:
- accept verified GeoJSON route geometry without requiring an online routing service;
- optionally acquire a route from a qualified provider with an explicit walking/driving/cycling profile;
- reveal the line, move a dot/arrow along distance, orient it to the route and optionally follow it with the camera;
- distinguish estimated distance/travel time from live traffic information.

No straight-line shortcut may be labelled a real walking/driving route. Check endpoints, foot access and the appropriate entrance/gate. Do not assume that every OSRM deployment exposes every travel profile.

### C. Aerial location reveal

Use real, rights-cleared aerial imagery with geographic registration:
- support the Polish Geoportal as one regional adapter;
- support independently qualified international or country-specific sources;
- keep acquisition date, resolution, bounds, CRS, source and rights with the asset;
- align route and markers after explicit reprojection and axis-order checks;
- limit zoom to the source's actual useful detail.

A tilted orthophoto is not a reconstruction of street-level facades. A transition to the real shop entrance requires separate authorized footage or photography. Photorealistic 3D reconstruction is outside the initial proposal unless separately justified.

## 6. Mandatory worldwide research

**Do not stop after validating Poland.** Find free tools and data sources that can support users internationally, with the widest practical geographic reach and honest fallbacks.

Separate these research categories:
1. Vector basemaps, streets, paths, place names and building footprints.
2. Geocoding and address/entrance verification.
3. Walking, cycling and driving route geometry.
4. Satellite imagery versus high-resolution aerial orthophotography.
5. Optional terrain/elevation; exclude it from the minimum dependency set unless useful.
6. Code libraries and acquisition/rendering infrastructure.

Distinguish a globally available dataset from a globally detailed and current dataset. A coarse global satellite layer may be useful for an establishing shot but unsuitable for identifying a storefront or gate. Coverage, language, accuracy and imagery dates differ by area.

Prefer:
- genuinely free, legally usable sources with clear commercial-video/export rights;
- no mandatory paid plan, account, API key or desktop application;
- documented APIs, downloadable datasets, permitted local caching and reproducible preparation;
- swappable providers and regional adapters under one input/output contract.

Record exceptions explicitly. “Free trial”, “free for noncommercial use”, “open-source client with a paid backend” and “self-hosting that costs money” must not be presented as equivalent to a free public production service.

Required **Global Coverage & Provider Matrix**:

| Required field | What Claude must establish |
| --- | --- |
| Provider and official source | Exact product/dataset/API and authoritative documentation |
| Geographic coverage | Countries/regions actually covered; global claims checked against documentation |
| Layer and use | Vector, routing, geocoding, satellite, orthophoto, terrain |
| Precision and age | Useful zoom/resolution, dates, address/entrance precision or UNKNOWN |
| Access | Download/API format, CRS, credentials, account and hosting needs |
| Cost | Free allowance, paid boundary, local compute/storage and maintenance costs |
| Rights | Code/data/style/font licences, commercial MP4 use and required credit |
| Operational policy | Limits, caching, offline use, bulk access, automation and redistribution |
| Portability | Claude, Codex, ChatGPT and browser/rendering prerequisites |
| Evidence | Documentation, authorized test evidence or NOT_RUN |
| Decision | QUALIFIED / CONDITIONAL / REJECT / UNKNOWN, with a reason |
| Fallback | What the user gets when the desired precision or imagery is unavailable |

Research coverage across Europe, North America, South America, Africa, Asia and Oceania. Propose representative urban and rural tests across these regions for a later authorized phase; one provider's claimed worldwide reach is not proof that every address works. Include non-Latin scripts and differing address conventions.

Recommend:
- a broadly available **vector-and-route baseline**;
- an **optional aerial tier** selected by location and rights;
- a documented **degraded mode**, such as vector-only output or user-supplied licensed imagery, when detailed imagery is unavailable.

Never invent coverage or silently substitute lower-resolution imagery. The goal is usefulness for users worldwide, not an unsupported promise of identical capabilities at every location.

International-source qualification is not yet complete in this document. Claude owns that research and must return evidence, rather than installing an unreviewed provider list.

## 7. Existing research and provider constraints to re-check

Earlier documentation research in this conversation identified these starting points. Recheck current policies before implementation or data acquisition:

- **OpenFreeMap:** the official site describes commercial and video use with attribution, public access without an API key/account, and no SLA. Its offline-download policy currently lists up to 3,000 tiles or 50 MB per download, at most four concurrent requests and an identifying User-Agent. Apply a conservative stop at either threshold, and do not split work to evade a limit. This does not authorize scraping arbitrary areas.
- **OpenStreetMap:** open data and the public tile service are different resources. Do not build a bulk/offline pipeline on `tile.openstreetmap.org`. Audit ODbL and appropriate attribution, distinguishing the data/derived database from a produced video.
- **Nominatim:** the public service is not the default generic geocoder for this plugin. Its policy includes an application-wide maximum of one request/second, identification, caching, no autocomplete, bulk restrictions and specific restrictions on generic no-code/low-code/vibe-coding integrations. Deliberate developer responsibility and policy compliance must precede any approved use. Coordinates/manual point selection are a valid baseline.
- **OSM API 0.6:** reported prototype lookup is not a reason to use the editing API as a generic map/routing or bulk-download backend. Establish the appropriate permitted access route.
- **OSRM/FOSSGIS:** inspect the actual routed-foot service operator, profile, data, usage policy and available guarantees. The open routing engine's licence does not qualify a third party's hosted service.
- **Geoportal:** the ORTO dataset page describes free retrieval and reuse. Check the precise layer and retrieval route. The reported WMS 1.3.0 HighResolution/Raster path is a prototype fact, not a mandate to use WMS for every dataset. Compare supported downloads/WCS where appropriate. Do not generalize the ORTO terms to every portal layer.
- **Google:** the earlier Geo Guidelines check found Earth/Earth Studio and Maps satellite imagery unsuitable for promotional shop videos under those guidelines; standard Google Maps in video advertising requires submission for approval. Keep these out of the default free advertising workflow.
- **GSAP, browsers, encoders, fonts and music:** verify the exact distribution/reuse terms and dependency pins. A freely downloadable library or file does not automatically allow redistributing it in a companion package.

Make required credits visible in the actual rendered output. HTML attribution outside the captured canvas can disappear during encoding; inspect the final MP4. Preserve source URLs and full credit information in the asset manifest as well.

## 8. Companion responsibilities and integration boundaries

The proposed companion should own:
- geographic input validation and provider/data selection;
- permitted acquisition and preparation of map/imagery/route assets;
- map-specific camera and route composition;
- deterministic rendering and geographic QA;
- provenance, rights and technical handoff for the generated assets.

Creative Studio retains the creative brief, campaign direction, copy locks and orchestration. FrameCut retains the editing project and master timeline. Motion Graphics retains broader authored motion where required. Open Assets retains general licensed media sourcing. Toolbox retains the existing Earshot capability and tool catalog.

Do not copy Earshot or install a second audio stack as a mandatory map dependency. Separate:
- **core map render**;
- **optional routing/geocoding/imagery acquisition adapters**;
- **optional music/audio analysis and editorial assembly**;
- **review/packaging utilities**.

The original prototype's full environment is a reproduction record, not the minimum installation footprint. Evaluate whether Turf and GSAP are useful retained dependencies, and whether the browser can be reused before downloading another binary. Python image/audio libraries need not all ship in the core map renderer.

Propose standalone use without requiring Creative Studio, while preserving compatible handoffs when it is present. A Reel Studio adapter depends on discovering its real contract. An interactive browser preview may be useful, but interactive product navigation is not proven by a pre-rendered MP4 and is not a separate application mandate.

Inspect the current owners and contracts:
- `plugins/framecore-work-creative-studio/skills/hyperframes-workflow/` — Motion Graphics; technical ID does not require HyperFrames.
- `plugins/framecore-work-creative-studio/skills/opencut-video-studio/` — FrameCut.
- `plugins/framecore-work-creative-studio/skills/remotion-video-production/` — existing optional renderer path.
- `plugins/framecore-work-creative-studio/skills/asset-manifest/` and `reference-pack-curator/`.
- `plugins/framecore-work-creative-studio/skills/pipeline-core/references/studio-integration-policy.md`.
- `plugins/framecore-work-creative-studio/skills/pipeline-core/references/companion-routing.md`.

No second Project State, intake sequence, QA budget or master clock. Document the smallest request/result contract that fits the existing companion mechanism.

## 9. Proposed portable contract and render requirements

Inputs should cover:
- location IDs, verified coordinates, CRS/axis order and address/entrance precision;
- route geometry/profile/source/date, or an explicitly approved acquisition request;
- map or aerial source, bounds, source date, resolution and rights;
- camera keyframes, route progress, easing and timing;
- exact copy, brand assets, fonts and locked content;
- requested duration, FPS, resolution and separately composed aspect ratios;
- permitted network services, acquisition limits, cache rules and cost budget.

Outputs should cover:
- final local MP4(s), source code/configuration and reproducible dependency/data references;
- actual composition stills/contact sheets and a QA receipt;
- asset manifest with source dates, licences, credits, hashes and environment versions;
- FrameCut handoff: path, hash, duration, FPS, dimensions, revision and placement/credit constraints.

Avoid bundling client footage, a large map cache, paid credentials or the prototype music into the plugin. Record what can be redistributed separately from what can only be used in a project.

Rendering requirements:
- one time model, derived from frame/FPS; seek all dependent animations explicitly;
- authorized data preparation followed by local rendering with all required assets resolved;
- frame-ready checks, stable style/font loading, controlled label/LOD changes and meaningful failure messages;
- safe interruption/resume with a recorded project/data revision;
- explicit limits and bounded retries for transient acquisition failures; respect Retry-After and never bypass 403/429 or rights restrictions;
- clear fallback or NOT_RUN when the host cannot execute WebGL or the renderer.

Reproducibility should be measured in a pinned environment. Cross-GPU/browser pixel identity is not assumed; define justified tolerances. Repeat/backward seeking must preserve geography, composition and timing.

Design separate 9:16 and 16:9 compositions when both are requested, not automatic crops. Keep 60 fps as the reported prototype benchmark, not an unconditional default for every user or host.

## 10. Verification plan after implementation approval

1. **Recover and audit the baseline.** Inspect project code, lockfiles, actual tool paths/versions, source maps, acquisition receipts, font/music licences and output metadata if supplied. Missing evidence stays UNKNOWN.
2. **Reproduce the reported case.** Confirm 30 s, 1080 × 1920, 60 fps and the expected frame count; compare actual map/route, camera, label/credit stability and audio measurements. Do not infer successful listening from LUFS alone.
3. **Prove all three modes.** Location reveal, route follow and aerial locator, with separately composed portrait/landscape outputs when in scope.
4. **Verify location semantics.** Check the actual entrance/gate, route mode and endpoints. Measure control-point alignment after reprojection and record a justified tolerance.
5. **Verify offline rendering.** Trace/block external network during rerender after authorized acquisition. Check for missing fonts, sprites, glyphs and image dependencies.
6. **Verify reproducibility.** Repeated renders and out-of-order/backward frame seeks; record actual environment and comparison method.
7. **Inspect real motion and sound.** Full playback plus critical frames, phone-size typography, no overlays crossing copy, no abrupt tiles/labels, smooth transitions and an intentional ending.
8. **Test worldwide samples.** Urban/rural cases across the researched regions, non-Latin labels, absent detailed imagery and vector fallback. Record failures and actual provider coverage.
9. **Test error handling.** Ambiguous address, no walking route, unavailable imagery, wrong CRS, missing font, provider rate limit, interrupted acquisition/render and unavailable WebGL.
10. **Test integration and cost.** Real FrameCut import, no duplicate intake/clock, measured render time/memory/storage/network usage, optional audio path and per-host results.

Use PASS / FAIL / NOT_RUN / UNKNOWN; use PASS_REPORTED only for identified owner reports. A one-project prototype does not establish a validated cross-platform plugin.

## 11. Deliverables expected from Claude before implementation

- **Prototype Reconstruction Report:** reported versus inspected versions, artifacts, licence evidence, environment split, missing data and reproducibility gaps.
- **Global Coverage & Provider Matrix:** worldwide and regional free candidates, precise coverage/rights/limits, decisions and fallbacks.
- **Companion Architecture Proposal:** core responsibilities, standalone use, Studio/FrameCut cooperation and conditional Reel Studio compatibility.
- **Dependency & Packaging Plan:** core versus optional packages/services; browser reuse; exact audited pins, rights, install sizes and cost.
- **Implementation Roadmap:** small P0/P1/P2 increments with concrete paths, inputs/outputs, tests, benefits and stop conditions.
- **Acceptance Plan:** executable checks and real renders with format, resolution, FPS, verification method and observed differences.
- **Approval Request:** one concrete implementation scope and the services/dependencies/data retrieval it needs; the product name remains an owner decision.

Suggested priorities:
- **P0:** reconcile evidence, inspect existing contracts, complete international research and choose the minimum architecture.
- **P1:** reproduce the local browser-render approach, build a reusable map/route core and qualify at least one non-Polish imagery path if available; keep regional gaps explicit.
- **P2:** additional regional imagery, optional geocoding/routing, multiple locations and additional host/adaptor coverage only where demonstrated useful.

Do not promise detailed aerial coverage everywhere. Do not omit the aerial capability simply because the first implementation is easier with vectors. Bring any scope tradeoff back with evidence.

## 12. Official starting references

These are documentation starting points from the earlier research, not proof that every proposed service has passed production qualification. Verify versions and policies again at use time.

- MapLibre GL JS: https://maplibre.org/maplibre-gl-js/docs/
- Route animation example: https://maplibre.org/maplibre-gl-js/docs/examples/animate-a-point-along-a-route/
- Camera animation example: https://maplibre.org/maplibre-gl-js/docs/examples/customize-camera-animations/
- OpenFreeMap: https://openfreemap.org/
- OpenFreeMap terms: https://openfreemap.org/tos/
- OpenStreetMap copyright/licence: https://www.openstreetmap.org/copyright
- OSM public tile policy: https://operations.osmfoundation.org/policies/tiles/
- OSM API policy: https://operations.osmfoundation.org/policies/api/
- Nominatim public service policy: https://operations.osmfoundation.org/policies/nominatim/
- OSRM API documentation reference: https://project-osrm.org/docs/v5.24.0/api/ — not a required implementation pin.
- Polish Geoportal ORTO: https://www.geoportal.gov.pl/pl/dane/ortofotomapa-orto/
- Geoportal WCS: https://www.geoportal.gov.pl/pl/usluga/uslugi-pobierania-wcs/
- Google Geo Guidelines: https://about.google/brand-resource-center/products-and-services/geo-guidelines/

## 13. Documentation-change provenance

- Trigger: owner-provided real-use tool inventory and instruction to save it in the repository, plus the explicit worldwide research requirement.
- Baseline: `6877d5d0b0dd672eb48d38b4c837cfd13352f58a`, branch `main`.
- Change: add this single document; existing files and shared plugin package remain untouched.
- Previous unpublished internal-skill RFP: concept scope superseded by the separate-companion direction here; do not treat it as implementation authority.
- No library/package installation, map download, production-provider invocation, prototype rerender, paid usage or client-media upload was performed for this handover. Repository checks are separate from prototype/media acceptance.
- Development provenance is recorded here instead of editing the existing ledger, following the owner's handover-only/no-other-changes scope.
- Shared package/version and hosted plugin updates: not applicable to this document-only change.
- Source checks and publication/readback are reported separately by the saving task. They do not validate the prototype or the future companion.
- Follow-up CW-20261109-03 (2026-11-09), baseline `6179d8179dc2073be4523169d6669a4cf22d884b`: resolve the owner-supplied Lemo-Opuscar URL, verify its absence from Toolbox and existing adoption in Studio, and replace the unresolved-source note with a targeted delta-review brief. Only this document changes; no Toolbox entry, existing style reference or dependency is modified.
- Follow-up CW-20261109-04 (2026-11-09), baseline `ff0b7bedb8da462f20c50a73b2a69e4adc9fd855`: owner correction supersedes the map-focused Lemo assessment in CW-20261109-03. Lemo-Opuscar is now a separate general Toolbox qualification task; map-specific Lemo research instructions are removed. Only this handover changes.

**Resume instruction:** Read the current AGENTS.md and CLAUDE.md, then this handover. Prepare two separate results: (A) the map-companion proposal in section 11, starting from the reported prototype and worldwide provider research; (B) the general Lemo-Opuscar Toolbox Qualification Report specified in section 1. Do not narrow Lemo to maps or make either task depend on the other's adoption. Present concrete scopes for owner approval before implementation, installation or catalog changes; the new companion's name remains undecided.

