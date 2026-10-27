# GitHub solution mapping for a keyless media companion

Research date: **2026-10-27 (UTC)**. Change: **CW-20261027-01**. Owner trigger: expand Task 1 research with a deep GitHub mapping of existing solutions. Studio baseline: `84c4b2a7d92c895f4e793985fb171580ded66fc7`, **1.149.0**. Companion construction and installation remain unapproved and were not started.

Read together with the [official-provider research and live tests](free-media-providers-2026-10.md). The [machine-readable source inventory](../../verification/free-media-github-solutions-2026-10.json) records all 31 repositories, complete commit pins, licence evidence, retrieved files, review depth and runtime status.

## Finding and recommended reuse plan

**No reviewed repository is a complete, already-verified fit for all six categories and all owner constraints.** There are useful existing components, and one important new provider discovery: SFXMint has a documented keyless SFX library that passed this session's direct search and WAV download/decoding test. This narrows the SFX gap to recorded/production-quality coverage and service limits; it does not solve music sourcing.

The strongest proposed combination is:

| Need | Existing solution | What can be reused after approval | What remains |
|---|---|---|---|
| Multi-provider museum discovery | **open-museum-mcp** | Adapter/federation model, provenance, conservative rights handling | Audit open fixes, provider pacing, explicit commercial/SA policy; disable keyed/unqualified providers |
| Current Met adapter | **cyanheads/met-museum-mcp-server** | Correct endpoint split, cache/error handling, image-origin checks | Choose selected code or a separate server; avoid importing a whole framework unnecessarily |
| Commons public API | **mwclient** | Established anonymous reads, pagination and streamed image access | Per-file rights, meaningful HTTP errors, bounded download and local decoder |
| Spoken-word audio | **pipeworx-io/mcp-librivox** local server | Four small direct-provider tools | Jurisdiction handling, result caps, verified files; no broad Pipeworx gateway |
| Dedicated SFX | **sfxmint-npm** and **sfxmint-mcp** | Existing API/CLI/MCP shape, hash manifest, safe overwrite behavior | Library-only mode, honest UA, bounded streaming, independent decode, quota and synthetic-origin disclosure |
| Poly Haven / ambientCG | Two **3d-asset-server** API adapters | Variant/format normalization and current ambientCG v3 handling | Isolate from scrapers/proxy features; provider terms, truthful UA and package licence notices |
| Thin alternative to a larger MCP base | **web-media-getter-skill** | Small Python aggregation/manifest skeleton | Significant rights/download hardening; remove Openverse from the enabled set |
| Media browser workflow | **Open-Media-Explorer / FootageFlow** | Adapter organization, source visibility, result/queue/attribution UX ideas | These are applications, not drop-in companion plugins; source eligibility differs |

This is a reuse recommendation, not a decision to vendor, fork, install or expose any upstream tool. For a small first version, prefer a thin companion with individually approved adapters, using these implementations as reviewed references. Choose a single runtime after the host interface is decided; do not combine Python, Node, PHP, R and desktop toolchains just because they exist.

## Method and evidence boundaries

Search covered aggregators, MCP servers, agent skills, provider SDKs, museum clients, audio/SFX clients, downloaders and material libraries. Query families included keyless/free media, museum MCP, LibriVox API, Poly Haven/ambientCG, ccMixter API, sound-effects CC0 API, Freesound Python and free-media MCP without keys. GitHub search was supplemented by links in project READMEs. This is a targeted map, not an exhaustive count of GitHub.

For every listed repository, GitHub metadata, the default-branch head, recursive tree and README were retrieved. Available licence files were read; selected source files were inspected where the table says **Selected code**. **Docs/tree** means a documentary screen, not an implementation audit. All repositories reported unarchived at retrieval. Head dates are commit timestamps, not a promise of active support. Old clients remain old even if a separate branch or PR was pushed recently.

- **Source retrieval/review: PASS**, with the stated depth and pinned sources.
- **Repository builds, test suites, dependency installation and MCP/client startup: NOT_RUN** for all 31.
- **Upstream CI health and release reproducibility: Unknown**; repository test files/README claims are not our test results.
- **Provider HTTP tests:** separate direct requests described in the provider report. A successful NASA or SFXMint download does not prove an upstream MCP server works.
- No third-party software was executed, no new source was enabled in Studio, and no extension-registry entry or hosted plugin was created. The owner asked for research, not installation.

## Repository inventory

Every pin below is immutable. Licence refers to **code/configuration**, not media, API access, model releases or provider terms. “Unknown” means no applicable code grant was identified in the inspected scope; public GitHub visibility is not permission to copy code.

| Repository | Reviewed commit · head date (UTC) | Code licence | Form | Decision | Review depth |
|---|---|---|---|---|---|
| [connerkward/web-media-getter-skill](https://github.com/connerkward/web-media-getter-skill) | [c30653ac](https://github.com/connerkward/web-media-getter-skill/commit/c30653ac216602257b2ced8d75125cd9ff13bdd3) · 2026-06-17 | MIT | Python skill / CLI | Adapt selected skeleton | Selected code |
| [cfpramod/open-museum-mcp](https://github.com/cfpramod/open-museum-mcp) | [dc5d2e11](https://github.com/cfpramod/open-museum-mcp/commit/dc5d2e119b1a1c30d5acd549d5f7d10b2e8f2f1c) · 2026-10-24 | MIT | TypeScript MCP | Primary architecture candidate | Selected code |
| [puf3zin/art-mcp](https://github.com/puf3zin/art-mcp) | [64c8b321](https://github.com/puf3zin/art-mcp/commit/64c8b32147f71d8223ca2a1f2fcece60357da62a) · 2026-07-27 | MIT | TypeScript MCP | Reference only | Selected code |
| [chuoke/media-bridge](https://github.com/chuoke/media-bridge) | [e800e32d](https://github.com/chuoke/media-bridge/commit/e800e32dfdddc462cfca23bf28aa0c3f8bda35a6) · 2026-04-28 | MIT | PHP / Laravel library | Reference only | Selected code |
| [aivrar/Open-Media-Explorer](https://github.com/aivrar/Open-Media-Explorer) | [1d3f00ca](https://github.com/aivrar/Open-Media-Explorer/commit/1d3f00cabbfe1495a78dd276bc42a57148b87e8c) · 2026-10-07 | MIT | JavaScript UI + local Python | Adapter / UX reference | Selected code |
| [bring42/hand-me-downs-workers](https://github.com/bring42/hand-me-downs-workers) | [eb24a911](https://github.com/bring42/hand-me-downs-workers/commit/eb24a9112005140b11fa4073e79724de61949b73) · 2026-04-14 | Unknown | Cloudflare Workers / Hono | Hold: code licence | Docs/tree |
| [jacobramirezsf/open-collections](https://github.com/jacobramirezsf/open-collections) | [3928c706](https://github.com/jacobramirezsf/open-collections/commit/3928c706390ad462e059c7a3036ef5d8768633ea) · 2026-10-18 | Unknown | React / Vercel / bulk index | Hold: code licence | Docs/tree |
| [xcslys99/FootageFlow](https://github.com/xcslys99/FootageFlow) | [6b111063](https://github.com/xcslys99/FootageFlow/commit/6b1110639854b4e4e59fa6dde701ea85350f63dc) · 2026-09-17 | MIT | Swift + C# desktop apps | UX reference | Docs/tree |
| [jjjake/internetarchive](https://github.com/jjjake/internetarchive) | [3e2a57de](https://github.com/jjjake/internetarchive/commit/3e2a57de598482db35dc99b072a22cffbb8d6798) · 2026-10-22 | AGPL-3.0 | Python library / CLI | Conditional dependency | Selected code |
| [mwclient/mwclient](https://github.com/mwclient/mwclient) | [87113730](https://github.com/mwclient/mwclient/commit/87113730b1f41d8160057621bfd90ad88428f602) · 2026-05-15 | MIT | Python API client | Useful dependency candidate | Selected code |
| [edrlab/librivox2lpf](https://github.com/edrlab/librivox2lpf) | [4b7f23ca](https://github.com/edrlab/librivox2lpf/commit/4b7f23ca42a40f369a5b6c079de07f42d374aa1a) · 2023-03-14 | BSD-3-Clause | Python packager | Packaging reference | Selected code |
| [pipeworx-io/mcp-librivox](https://github.com/pipeworx-io/mcp-librivox) | [c9e73852](https://github.com/pipeworx-io/mcp-librivox/commit/c9e7385212533736e1ce2e267650583d5ce5a3ba) · 2026-10-27 | MIT | TypeScript MCP | Local adapter candidate | Selected code |
| [matthill/librivox-java](https://github.com/matthill/librivox-java) | [39f91c72](https://github.com/matthill/librivox-java/commit/39f91c7237a3d400a62b81cb927f8cc739139ad7) · 2014-04-06 | Apache-2.0 | Java / Android client | Historical reference | Docs/tree |
| [CharlesPikachu/musicdl](https://github.com/CharlesPikachu/musicdl) | [dca2f096](https://github.com/CharlesPikachu/musicdl/commit/dca2f0967e46a8faf8d279737535471102d74ca3) · 2026-10-16 | PolyForm-Noncommercial-1.0.0 | Python downloader | Reject for this scope | Docs/tree |
| [LeMetadatarr/metadatarr](https://github.com/LeMetadatarr/metadatarr) | [61e7baf8](https://github.com/LeMetadatarr/metadatarr/commit/61e7baf8f26c86864d88e800d26796e82194ef04) · 2026-10-25 | Apache-2.0 | Python metadata resolver | Reject as acquisition base | Docs/tree |
| [gronnmann/cs2asset](https://github.com/gronnmann/cs2asset) | [b8e1b1dd](https://github.com/gronnmann/cs2asset/commit/b8e1b1dd86023ca8604db874052f63ce7659ba85) · 2026-10-05 | Unknown | Python / CS2 importer | Hold: code licence | Docs/tree |
| [arielshad/3d-asset-server](https://github.com/arielshad/3d-asset-server) | [12312694](https://github.com/arielshad/3d-asset-server/commit/1231269407dda5af7c585e7ddeb96821ada9fcdd) · 2026-10-27 | Apache-2.0 | TypeScript REST / MCP | Select two API adapters | Selected code |
| [strike-digital/asset_bridge](https://github.com/strike-digital/asset_bridge) | [41abe1c5](https://github.com/strike-digital/asset_bridge/commit/41abe1c574474e0a1803c0ebecf17250c40e98bf) · 2025-05-21 | GPL-3.0-or-later | Blender add-on | Specialist reference | Selected code |
| [Poly-Haven/polyhavenassets](https://github.com/Poly-Haven/polyhavenassets) | [1e1e1633](https://github.com/Poly-Haven/polyhavenassets/commit/1e1e1633ea23103b00d081c0a6ab67b841acb235) · 2026-10-01 | GPL-3.0 | Official Blender add-on | Official reference | Docs/tree |
| [kwokcb/materialxMaterials](https://github.com/kwokcb/materialxMaterials) | [752bb463](https://github.com/kwokcb/materialxMaterials/commit/752bb46304e59b54c90ecb63a262a10bf22cd917) · 2026-08-27 | Apache-2.0 | Python / JavaScript / MaterialX | Specialist reference | Docs/tree |
| [mikechao/metmuseum-mcp](https://github.com/mikechao/metmuseum-mcp) | [576b5441](https://github.com/mikechao/metmuseum-mcp/commit/576b5441daa04cae33d4583c23c35074390c9e2f) · 2026-04-27 | MIT | TypeScript MCP Apps | Hold: stale endpoint | Selected code |
| [cyanheads/met-museum-mcp-server](https://github.com/cyanheads/met-museum-mcp-server) | [73cf09b8](https://github.com/cyanheads/met-museum-mcp-server/commit/73cf09b8a5a11dcb7b597f6d1a5bf5316e175521) · 2026-10-17 | Apache-2.0 | TypeScript MCP | Current Met reference | Selected code |
| [nesaro/librivox-api](https://github.com/nesaro/librivox-api) | [11ed0342](https://github.com/nesaro/librivox-api/commit/11ed0342f4312a2c3df0176705d54cc95d11d686) · 2014-03-22 | GPL-3.0 | Python client | Historical reference | Docs/tree |
| [palaeoverse/rphylopic](https://github.com/palaeoverse/rphylopic) | [d2e7bc29](https://github.com/palaeoverse/rphylopic/commit/d2e7bc2954bf13125899b3f1563985d77663000c) · 2026-10-02 | GPL-3.0-or-later | R library | Specialist reference | Selected code |
| [fedebertolini/ccmixter-js](https://github.com/fedebertolini/ccmixter-js) | [8cc88cd5](https://github.com/fedebertolini/ccmixter-js/commit/8cc88cd55ea76575c5eac3a5e42d9ee4750ba42a) · 2021-05-09 | MIT | Node.js client | Hold: old transport / provider | Selected code |
| [MTG/freesound-python](https://github.com/MTG/freesound-python) | [7f53a3e9](https://github.com/MTG/freesound-python/commit/7f53a3e92f2282b26cff3152d4dcc5e4f013d6b9) · 2026-10-22 | MIT | Official Python client | Exclude: credentials | Docs/tree |
| [sandraschi/sfx-mcp](https://github.com/sandraschi/sfx-mcp) | [61cecd39](https://github.com/sandraschi/sfx-mcp/commit/61cecd392dd64cc301b0d47abdf819e974a11c30) · 2026-10-24 | MIT | Python FastMCP | Exclude: credentials | Docs/tree |
| [Cy4nWare/sfx-api](https://github.com/Cy4nWare/sfx-api) | [ab0ae1c1](https://github.com/Cy4nWare/sfx-api/commit/ab0ae1c1de5a872e9989a87323a42e2100533032) · 2026-07-27 | Unknown | Static catalogue + JS player | Offline-library concept | Selected code |
| [lotsofsounds/lots-of-sounds-api-examples](https://github.com/lotsofsounds/lots-of-sounds-api-examples) | [7a0bb1c3](https://github.com/lotsofsounds/lots-of-sounds-api-examples/commit/7a0bb1c3f0d055c02ee68de78beb621301923a9c) · 2026-10-02 | MIT | Official API examples | Exclude: keyed search | Docs/tree |
| [flreey/sfxmint-mcp](https://github.com/flreey/sfxmint-mcp) | [84bf8ab1](https://github.com/flreey/sfxmint-mcp/commit/84bf8ab1a603db12309020cffbc335bcd911fa21) · 2026-10-27 | CC0-1.0 | MCP config + agent skill | Conditional ready interface | Docs/tree |
| [flreey/sfxmint-npm](https://github.com/flreey/sfxmint-npm) | [a41f6647](https://github.com/flreey/sfxmint-npm/commit/a41f6647e1ff224ced4dcd05c8a8368d60a1e2ea) · 2026-10-27 | MIT | Node CLI / stdio / Web Audio | Best SFX implementation reference | Selected code |

## Closest implementations: source findings

### Museum federation: cfpramod/open-museum-mcp

The pinned project provides a substantial TypeScript museum MCP architecture: separate provider fetchers, federated search, source failures, caching, deduplication, field provenance and citations. Its [licence gate](https://github.com/cfpramod/open-museum-mcp/blob/dc5d2e119b1a1c30d5acd549d5f7d10b2e8f2f1c/src/licenseGate.ts) rejects missing or inadequate rights evidence for covered sources and distinguishes image rights from open metadata. The [Met fetcher](https://github.com/cfpramod/open-museum-mcp/blob/dc5d2e119b1a1c30d5acd549d5f7d10b2e8f2f1c/src/fetchers/met.ts) already uses `/v1.1/search` while object details stay under `/v1/objects`.

Two different policies need deliberate reconciliation: [commercialRights](https://github.com/cfpramod/open-museum-mcp/blob/dc5d2e119b1a1c30d5acd549d5f7d10b2e8f2f1c/src/rights/commercialRights.ts) permits CC0/PDM/BY/BY-SA, whereas [clearance licence mapping](https://github.com/cfpramod/open-museum-mcp/blob/dc5d2e119b1a1c30d5acd549d5f7d10b2e8f2f1c/src/core/clearance/licenseMap.ts) is narrower. “Commercially permitted” must not silently mean attribution-free or suitable for every adaptation. Our proposed default flags SA and rejects NC/ND/unknown rights.

The [federation code](https://github.com/cfpramod/open-museum-mcp/blob/dc5d2e119b1a1c30d5acd549d5f7d10b2e8f2f1c/src/core/federation.ts) has a default per-museum concurrency of eight. That is unsuitable as a universal provider budget: LoC's JSON limit and AIC's image-download guidance require their own queues. A User-Agent helper does not guarantee access through an institutional protection service; AIC remained blocked in our direct test.

A limited latest-issues/PR read found **open**, not merged, corrections: [#211](https://github.com/cfpramod/open-museum-mcp/pull/211) concerns dropped maker-attribution qualifiers in citations, [#210](https://github.com/cfpramod/open-museum-mcp/pull/210) Rijksmuseum attributed-maker/date handling, and [#208](https://github.com/cfpramod/open-museum-mcp/pull/208) escaped-markup sanitization. These are upstream reports, not locally reproduced bugs. Check their disposition and the relevant code before adoption; do not assume proposed fixes exist at the reviewed pin. This makes the project the strongest architecture reference, not an unconditional production recommendation.

### Two current Met implementations versus two stale clients

[cyanheads' Met service](https://github.com/cyanheads/met-museum-mcp-server/blob/73cf09b8a5a11dcb7b597f6d1a5bf5316e175521/src/services/met/met-service.ts) preserves the required endpoint split, handles upstream HTML/errors and rate-limit responses, caches responses and constrains image origins. The [endpoint tests](https://github.com/cyanheads/met-museum-mcp-server/blob/73cf09b8a5a11dcb7b597f6d1a5bf5316e175521/tests/services/met/met-service-base-url.test.ts) are a useful design reference, but were not run. Its broader MCP framework and recent Bun/Node requirements add integration weight.

In contrast, [mikechao's API client](https://github.com/mikechao/metmuseum-mcp/blob/576b5441daa04cae33d4583c23c35074390c9e2f/src/api/MetMuseumApiClient.ts) and [art-mcp's Met provider](https://github.com/puf3zin/art-mcp/blob/64c8b32147f71d8223ca2a1f2fcece60357da62a/src/providers/met.ts) construct the retired `/v1/search`. Our independent HTTP probe received **410** from that endpoint. This is concrete compatibility evidence, although neither repository was executed here. The latter also removes the public-domain field when projecting search results; a search-result adapter must retain rights evidence. New UI or MCP features do not make an obsolete provider endpoint usable.

### Lightweight general aggregator: web-media-getter-skill

[webmedia.py](https://github.com/connerkward/web-media-getter-skill/blob/c30653ac216602257b2ced8d75125cd9ff13bdd3/webmedia.py) is a compact Python standard-library implementation with normalized records, concurrent search, source attribution and delayed Internet Archive file resolution. It is the closest small skill/CLI skeleton, covering imagery, video and GIF rather than all six media categories.

Required changes are substantial: the no-key list includes Openverse; NASA rights are represented too broadly; Archive/LoC unknown rights are not a strict commercial gate; the download path reads the response without a streaming byte cap or independent media decode. Its UA also needs current product/contact identification and Archive's model information. Preserve the useful manifest idea, but do not treat a manifest as proof that its licence values are correct. This is an optional alternative to a larger MCP foundation.

### General media applications: Open-Media-Explorer and FootageFlow

[Open-Media-Explorer's HTTP layer](https://github.com/aivrar/Open-Media-Explorer/blob/1d3f00cabbfe1495a78dd276bc42a57148b87e8c/src/lib/http.js) distinguishes malformed/HTML responses, supports timeouts and bounded responses, and offers a useful injectable transport pattern. Its [LibriVox adapter](https://github.com/aivrar/Open-Media-Explorer/blob/1d3f00cabbfe1495a78dd276bc42a57148b87e8c/src/adapters/librivox.js) searches books and resolves chapter URLs through the feed. The broad public-domain label still needs a US-jurisdiction qualification. A public stream, podcast or television channel is not automatically reusable stock.

The project is valuable for adapters and browsing UX, but its wider provider list and local transport choices need independent eligibility checks. A local CORS bridge is not permission to evade a provider's access block.

FootageFlow's pinned README describes rights filters, provider health, download queues, source records and attribution sidecars. It also mixes official APIs, keyed services and site/downloader modes. This mapping inspected its documentation/tree/licence, **not the desktop implementation**, so these features are author-described, not verified behavior. Its Swift/C# applications are not a lightweight plugin base.

[media-bridge's NASA driver](https://github.com/chuoke/media-bridge/blob/e800e32dfdddc462cfca23bf28aa0c3f8bda35a6/src/Drivers/NasaDriver.php) is another useful rendition-selection example, but assigns `cc0` to NASA results indiscriminately. The official NASA policy has third-party and use restrictions. Reuse data-shaping ideas only after correcting this semantic error.

### Commons and Internet Archive clients

[mwclient's image helper](https://github.com/mwclient/mwclient/blob/87113730b1f41d8160057621bfd90ad88428f602/mwclient/image.py) supports streamed file reads and anonymous MediaWiki access. The inspected download method does not itself enforce a successful HTTP status, a valid media MIME or decoding. Callers must add these checks and use API extended metadata for licence, creator and source attribution. Its [retry helper](https://github.com/mwclient/mwclient/blob/87113730b1f41d8160057621bfd90ad88428f602/mwclient/sleep.py) also needs integration with provider-specific budgets; generic retry behavior should stop at a challenge.

[internetarchive's file implementation](https://github.com/jjjake/internetarchive/blob/3e2a57de598482db35dc99b072a22cffbb8d6798/internetarchive/files.py) provides format/size metadata, resume/checksum behavior and useful public-download plumbing. AGPL-3.0 obligations need a distribution/integration decision before embedding it. The inspected retry expression substitutes a nonzero default for a false/zero value, so “zero retries” cannot be assumed from merely passing zero to that path. Metadata and checksums establish neither copyright ownership nor a cleared music master. Our sampled Archive MP3 remains **not approved for reuse**.

### Spoken-word audio: LibriVox

[mcp-librivox's tool handlers](https://github.com/pipeworx-io/mcp-librivox/blob/c9e7385212533736e1ce2e267650583d5ce5a3ba/src/index.ts) expose audiobook search/detail, authors and tracks using the public LibriVox API. The [local stdio server](https://github.com/pipeworx-io/mcp-librivox/blob/c9e7385212533736e1ce2e267650583d5ce5a3ba/src/server.ts) is the relevant bounded interface. The README also promotes a shared Pipeworx gateway that introduces a much wider tool catalogue; do not confuse that gateway with a four-tool local provider module.

Search limits are passed through and need validation against current provider caps. Downloads, rights outside the US and Archive's transport policy still require our own handling. The hosted gateway's initial anonymous allowance is not a durable no-account contract. No gateway or local server was connected in this task.

The older Java/Python clients are historical references. The BSD-licensed **librivox2lpf** is more useful for packaging already acquired audiobook chapters than for search. None of these is a general music catalogue.

### Dedicated SFX discovery: SFXMint

GitHub discovery led to the provider's [API documentation](https://sfxmint.com/api/docs), [licence](https://sfxmint.com/license) and [terms](https://sfxmint.com/terms), all read 2026-10-27. Library search and downloads require no account/key. Library audio is offered as CC0; the service currently limits script/API downloads to **20 different sounds per day per network**. Audio is AI-generated or procedurally synthesized, not a recorded-foley collection. Generation is a separate keyed/account feature and is excluded. The terms prohibit reselling API/generation access, which is distinct from using the CC0 audio commercially.

The **sfxmint-mcp** repository is chiefly configuration, documentation and a skill for the hosted service, not the full server backend. **sfxmint-npm** provides actual Node 20+ client/CLI code and a local stdio bridge. [Its downloader](https://github.com/flreey/sfxmint-npm/blob/a41f6647e1ff224ced4dcd05c8a8368d60a1e2ea/src/download.mjs) checks the returned byte count and SHA-256, rejects unexpected initial file origins, retains source/page links and refuses to overwrite different existing bytes without an explicit option. This is the best SFX implementation reference found.

Important limits in the inspected code: `arrayBuffer()` buffers the whole file without a streaming cap; the code trusts provider decodability metadata instead of independently decoding; a missing licence falls back to CC0. The [API client](https://github.com/flreey/sfxmint-npm/blob/a41f6647e1ff224ced4dcd05c8a8368d60a1e2ea/src/api.mjs) includes an optional maintainer-internal mode with a browser-style UA. **Do not use or copy that mode**; the research probe used an honest identifying UA. Missing-match/generation suggestions are provider data, not authority to enable paid generation.

Direct Work evidence: search **200 JSON at 16:02:31 UTC**, one WAV **200 audio/wav at 16:03:11 UTC**; full decode produced 1.0-second stereo PCM at 44.1 kHz, and SHA-256 matched the API. This supports **conditional first-version inclusion for library SFX**. MCP/CLI runtime and listening suitability remain NOT_RUN.

### Texture and material clients

[Poly Haven](https://github.com/arielshad/3d-asset-server/blob/1231269407dda5af7c585e7ddeb96821ada9fcdd/src/providers/polyhaven.ts) and [ambientCG](https://github.com/arielshad/3d-asset-server/blob/1231269407dda5af7c585e7ddeb96821ada9fcdd/src/providers/ambientcg.ts) adapters use their documented JSON APIs; the latter explicitly targets v3. The [download infrastructure](https://github.com/arielshad/3d-asset-server/blob/1231269407dda5af7c585e7ddeb96821ada9fcdd/src/core/download.ts) contains useful URL/path/redirect defenses. However, the full project also includes HTML-based source adapters and proxy-oriented advice. Use only independently approved API modules; replace its browser-style default UA with a clear application identity.

The official **polyhavenassets** Blender add-on is a good source for provider-specific variants, but its GPL code and packaged distribution are distinct from CC0 assets. **asset_bridge** has a GPL-3-or-later notice in its source even though repository metadata did not identify it. **materialxMaterials** is an Apache-licensed specialist material-conversion reference; a large data repository is unnecessary for a small companion. **cs2asset** has relevant import/cache concepts but no code licence was identified in its reviewed manifest/root.

For silhouettes, [rphylopic's attribution implementation](https://github.com/palaeoverse/rphylopic/blob/d2e7bc2954bf13125899b3f1563985d77663000c/R/get_attribution.R) preserves attribution, contributor and licence links. Its map includes NC/NC-SA as well as CC0/BY/SA: availability in the API is not a commercial filter. Its optional permalink feature creates a collection via POST; a future read-only provider adapter should not inherit that side effect by default. The R runtime is not justified merely to obtain silhouettes.

## Exclusions and why they do not close the gaps

| Solution / pattern | Evidence | Consequence |
|---|---|---|
| **musicdl** | Actual LICENSE is PolyForm Noncommercial 1.0.0; broad unofficial download integrations | Reject as the commercial companion's acquisition base |
| **metadatarr** | Metadata/scraper focus; manifest includes `unblock_requests` and HTML tooling | Not a cleared-media API aggregator; do not inherit its access assumptions |
| **freesound-python / sfx-mcp** | Official client and wrapper both require Freesound credentials; full-quality download additionally uses OAuth2 | A free SDK does not satisfy a no-key provider requirement |
| **Lots of Sounds examples** | Official README requires a Pro/Enterprise API key for catalogue search; only a sample route is anonymous | Exclude from keyless search; NOT_RUN intentionally |
| **ccmixter-js** | [HTTP-only transport](https://github.com/fedebertolini/ccmixter-js/blob/8cc88cd55ea76575c5eac3a5e42d9ee4750ba42a/src/services/httpClient.js), [all-licences default](https://github.com/fedebertolini/ccmixter-js/blob/8cc88cd55ea76575c5eac3a5e42d9ee4750ba42a/src/services/songs.js), 2021 head | Historical schema reference; no fix for our provider download 403 or advertising-terms gap |
| **Cy4nWare/sfx-api** | Client downloads a static catalogue and searches locally; CREDITS distinguishes Kenney media from the author's tooling | Possible offline-library pattern, not a provider API; code licence Unknown, original pack rights need validation |
| **hand-me-downs-workers / open-collections / cs2asset** | No applicable code grant identified in inspected root/README/manifest | Do not copy or vendor until licensing is established |
| Arbitrary public radio/TV/podcast/video downloaders | Playback access is separate from commercial reuse permission | Exclude without official API access and item-level rights |
| An Openverse-backed “free media” wrapper | Same underlying provider, regardless of wrapper | Does not reverse the owner's decision to set Openverse aside |

Permissive MIT/BSD/Apache code can reduce implementation work if its notices and conditions are preserved. GPL/AGPL code is not “noncommercial”; it has a different set of obligations that must be evaluated for the chosen integration. Media CC0 does not relicense application code, and an open-source application cannot waive a provider's API terms.

## Six-category reuse coverage

| Category | Existing building blocks worth retaining | Remaining gap |
|---|---|---|
| Audio / speech | LibriVox local MCP, Commons client, Archive file metadata | Modern speech stock; US versus other jurisdictions; actual audio path checks per provider |
| Music | Archive client and historical ccMixter schema | No validated broad commercial music catalogue without accounts/keys; composition/master/sample rights |
| SFX | SFXMint client/MCP and API; Commons for selected recordings | Synthetic versus recorded provenance, 20/day network allowance, no scene listening acceptance |
| Graphics / illustrations | Museum federation, current Met adapter, PhyloPic attribution, texture adapters | Contemporary vector/icon breadth and explicit per-item SA/NC handling |
| Photos | Commons, museums, NASA adapter patterns | Lifestyle stock/model releases; NASA cannot be mapped globally to CC0 |
| Video | NASA/Archive/Commons schemas and browser UX references | General contemporary B-roll; rights, variants and full-file validation |

## New discovery leads, not approved providers

Repository provider lists also point to V&A, Japan Search, the National Gallery of Art, Getty, Yale and the Walters Art Museum. These are **leads only**: no official-policy qualification or fresh search/download test was completed for them here. They do not inherit the repository author's “keyless” or “commercially safe” labels. Before enabling any, apply the same official-documentation and one-search/one-download process.

The Kenney static-catalogue pattern could support a separately curated offline CC0 pack, but that is a different product decision from aggregating live official APIs. Lots of Sounds was screened out by its own API README. SFXMint alone was promoted from this follow-up discovery to the tested-provider set, because it met the documentary gate and received fresh controlled HTTP tests.

## Concrete decision for the owner

Approve provider scope and name before implementation. The proposed first scope is **Commons, The Met, Cleveland, NASA, Poly Haven, conditional LibriVox**, plus **SFXMint if synthetic/AI SFX and its anonymous download allowance are acceptable**. Music remains an explicitly named gap. A smaller launch could postpone LibriVox instead of pretending that it supplies music.

For implementation planning after approval, use **open-museum-mcp** for federation/rights structure, **cyanheads** for current Met behavior, **mwclient** or direct MediaWiki requests for Commons, and **sfxmint-npm** for a carefully bounded SFX module. Use the small Python aggregator only if a Python-first skill interface is preferred. Existing source pins and documented defects make this selection reviewable; none is a claim of installed-client readiness.

Name candidates remain **FrameCore Media Shelf**, **Open Media Desk**, and **FrameCore Media Atlas**. No name availability or trademark check was performed. No plugin was built or released.
