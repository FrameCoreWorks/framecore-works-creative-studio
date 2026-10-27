# Keyless free-media providers: October 2026 research

Research date: **2026-10-27 (UTC)**. Change: **CW-20261027-01**. Owner trigger: Task 1 in the [current handover](../handover-claude-code-2026-10-27.md), restricted in this session to research and ChatGPT Work tests. Baseline: `84c4b2a7d92c895f4e793985fb171580ded66fc7`, Studio **1.149.0**.

## Owner selection decision, 2026-10-27

Follow-up decision **CW-20261027-02**: the companion must include **all sources that fully satisfy the provider requirements**, without an arbitrary provider-count cap or a restricted launch shortlist. Naming decision **CW-20261027-03**: the owner approved **FrameCore Open Assets**, with technical identifier `framecore-open-assets`. These decisions approve the selection rule and name; implementation, installation and release have not been authorized in this research task.

Qualify each supported provider/media path against official documentation: free public search and download without registration or keys; permitted automated access; enforceable asset-rights and commercial-use filtering; all applicable attribution, User-Agent, rate, cache, linking and file-variant rules; and fresh search/download/decoder evidence on the required target hosts. Unknown material conditions, incomplete rights evidence, failed host paths and unrun required tests block enabling that path. Do not bypass protections or turn a technical PASS into complete qualification.

A mixed-rights catalogue may qualify through a documented, enforceable eligible subset. Provider inclusion never grants permission to use every asset: retain per-file rights, source and attribution; exclude NC, ND and unknown rights from automatic commercial selection, and flag SA for a deliberate choice. Stated limits and attribution requirements are conditions to satisfy, not automatic exclusions. This is evidence-based conformance for the intended use, not a guarantee of permanent availability or universal rights clearance.

A provider that does not publish a fixed numeric quota is not excluded for that absence alone: follow its published client/fair-use guidance, response headers and conservative request budgets. An unreadable or unresolved applicable policy is a different situation and remains a qualification gap.

The earlier priority tiers below describe research readiness and possible implementation order only. They do not limit the approved provider scope. The existing HTTP evidence remains unchanged; no candidate is newly certified by this decision. Openverse remains set aside.

## Research summary

Eighteen plausible keyless providers received fresh search requests from this ChatGPT Work execution environment. Fifteen completed a search-to-file path with a locally decoded medium. AIC and Gallica blocked search; ccMixter returned search JSON but denied the selected download. These are point-in-time transport results, not uptime promises, licensing clearances, installed-plugin tests, or Claude Code results.

The initial research prioritized **Wikimedia Commons, The Met, Cleveland Museum of Art, NASA Image and Video Library, Poly Haven, and LibriVox**; the owner's all-qualified-sources decision above supersedes a six-provider launch limit. LibriVox is a conditional spoken-word source, with jurisdiction checks; it does not fill the music/SFX gap. Rijksmuseum, Wellcome, ambientCG and PhyloPic are equally in scope when fully qualified. Finna and SMK need outstanding client/terms documentation resolved. Library of Congress and Internet Archive need collection-specific rights policies before automatic commercial selection. AIC, ccMixter and Gallica are not enabled candidates for this host.

Openverse is set aside by the owner and was not queried. No provider modules, companion package, Studio rewiring, plugin update or release were built. The selection rule and name **FrameCore Open Assets** (`framecore-open-assets`) are approved; qualification must still be completed. Earlier name suggestions are superseded by the approved name. Name availability and trademark checks are NOT_RUN.

The follow-up [GitHub solution mapping](free-media-github-solutions-2026-10.md) reviews **31 existing repositories** at pinned commits. It discovered **SFXMint**, now also tested: add it conditionally for library SFX if synthetic/AI provenance and a 20-download daily network allowance fit the product. Its generator and paid/account routes stay outside scope.

## Scope and interpretation

- “Keyless” concerns public search and public downloadable files. It does not mean every record is downloadable or that accounts for uploads/borrowing are unnecessary.
- Provider documentation, observed HTTP behavior and recommendations are identified separately below. **Unknown** means this session could not establish a fact; it never means unrestricted.
- A provider appearing in several category tables was tested once in the representative category stated in the results table. Other categories are documented coverage, **not separately tested**. Audio means speech/recordings; music means musical recordings, not just sheet-music images; SFX means reusable effects/ambiences.
- All linked documentation below was read or attempted on **2026-10-27**. Failed reads are explicitly named. A search-engine extraction of an official page is weaker than a successful direct read and is identified where used.
- No HTML search scraping, credentials, login, CAPTCHA solving, copied cookies, browser impersonation, proxy/IP rotation or protection bypass was used. Public API JSON/XML and provider documentation were the only discovery interfaces used for the tested candidates.

### Rights policy for the proposed companion

The [Creative Commons licence overview](https://creativecommons.org/cc-licenses/) distinguishes commercial permission from attribution and adaptation conditions. CC0 has no copyright attribution condition; PDM is a status label, not a new grant of rights. CC BY requires credit and licence information. BY-SA also requires compatible licensing of adaptations. NC is unsuitable for the proposed commercial default. ND is unsuitable for a default that expects edits/adaptations; it is not a blanket ban on all commercial distribution. Unknown rights and “no known restrictions” must not silently become CC0. Non-copyright rights, third-party material and jurisdiction still need consideration.

Recommended default: accept verified CC0/PDM and CC BY records with retained provenance; flag SA explicitly and require a deliberate choice; exclude NC, ND and unknown rights from automatic commercial selection. For audio, check the composition, performance and sound recording, not just the item's upload label. This is a proposed product policy, not a claim that every source below already meets it.

## Category coverage and named gaps

### Audio: speech, interviews and other recordings

| Provider | Useful coverage and rights gate | Recommendation / gap |
|---|---|---|
| LibriVox | Human-read public-domain books; provider's public-domain statement is US-specific | Conditional first version; no commissioned voice-over or contemporary interviews |
| Wikimedia Commons | Speech, field recordings; per-file PD/CC terms | First version; audio path itself NOT_RUN here |
| Internet Archive | Public audio collections, oral histories and radio; uploader/collection rights vary | Curated collections only; technical PASS is not clearance |
| NASA | Mission and science recordings; NASA media conditions and third-party exceptions | First version provider; audio path NOT_RUN, video tested |
| Library of Congress | Oral history and recorded sound; item/collection restrictions | Reserve; photo path tested, audio NOT_RUN |
| Finna / Gallica | National-library and partner catalogues can describe recordings | Finna terms incomplete; Gallica blocked and commercial media reuse generally licensed for payment |

**Gap A1:** no verified broad, modern, commercially cleared speech/audio stock library with keyless search and downloads. LibriVox's public-domain catalogue is useful but narrow.

### Music

| Provider | Useful coverage and rights gate | Recommendation / gap |
|---|---|---|
| ccMixter | Music, stems and remixes; individual CC licences, including NC | Search PASS, download FAIL; advertising clause needs clarification before client ads |
| Internet Archive | Netlabels, live music, community music and historical recordings | Audio download PASS; blanket CC0 query was not sufficient for clearance |
| Wikimedia Commons | Open musical recordings and scores | Candidate with per-recording rights checks; tested only with a photograph |
| Library of Congress | Historical music recordings and scores | Reserve; digitized score does not provide a cleared recording |
| Gallica | Scores and historical recorded music | Exclude from free commercial-media default; search blocked |
| Jamendo / Freesound | Potential alternatives if account/key rule changes | Excluded at documentation gate; NOT_RUN |

**Gap M1:** no first-version recommendation for a dependable, general-purpose music catalogue for advertising that meets every requirement. **Gap M2:** composition, master, performer and sample/remix rights cannot be inferred from a single licence field. Internet Archive's sampled community album illustrates why an upload label alone is insufficient.

### Sound effects (SFX)

| Provider | Useful coverage and rights gate | Recommendation / gap |
|---|---|---|
| SFXMint | Dedicated synthetic/AI library under CC0; WAV/MP3 and some OGG, duration/loop metadata | Conditional first version; search plus WAV PASS; 20 distinct anonymous downloads/day/network |
| Wikimedia Commons | Environmental and discrete sounds; individual licences | Best general keyless candidate; SFX download NOT_RUN |
| Internet Archive | Field recordings and sound collections | Curated subset only; sampled music does not validate SFX coverage |
| NASA | Mission sounds and specialist science audio | Specialist source; no claim of a complete SFX library |
| Freesound | Dedicated effects/ambiences | API credential required; excluded, NOT_RUN |
| BBC Sound Effects / OpenGameArt | Discovery leads only | No suitable documented public keyless search API established in this review; not admitted to the test set |

**Gap S1:** SFXMint closes part of the dedicated keyless SFX gap, but only for synthetic/AI audio and within its daily network allowance. No broad recorded-foley library passed this review; suitability, seamless loops and production quality need listening tests. Do not present imagery/texture providers as filling that gap.

### Graphics and illustrations

| Provider | Coverage | Recommendation / rights gate |
|---|---|---|
| The Met / Cleveland | Art, prints, drawings and decorative works | First version; select public-domain/CC0 images explicitly |
| Wikimedia Commons | SVG, diagrams, illustrations and scanned art | First version; retain licence and attribution, flag SA |
| Poly Haven | Texture maps, HDRIs, 3D assets | First version; CC0 assets, separate live-API credit requirement |
| ambientCG | Materials/textures, HDRIs and related assets | Next candidate; CC0, one-person service with explicit reliability caveat |
| PhyloPic | Biological silhouettes, SVG and PNG | Next candidate; CC0/BY subset, NC/SA filtering |
| Rijksmuseum / Wellcome | Historical art; scientific/medical illustrations | Next candidates; inspect image-level rights |
| SMK / Finna | Museum art and aggregated cultural collections | Technical PASS; outstanding policy reads |
| Art Institute of Chicago | Artworks and IIIF | Search blocked from this host |
| LoC / Gallica | Posters, prints and historical documents | LoC rights vary; Gallica outside free commercial default |

**Gap G1:** broad contemporary vector/icon packs and modern commercial illustrations are not covered by the validated art/texture/silhouette set. A texture is not a finished illustration.

### Photos

| Provider | Coverage | Recommendation / rights gate |
|---|---|---|
| Wikimedia Commons | Broad subjects and locations | First version; per-file licence, likeness/property review when relevant |
| NASA | Space, technology and mission photography | First version; NASA/third-party distinction, no endorsement |
| LoC / Finna / Wellcome | Historical, cultural, scientific photographs | Strong discovery sources; item-level rights and documented gaps below |
| The Met / Cleveland / Rijksmuseum / SMK / AIC | Photographic collections and reproductions of objects | Useful institutional imagery; an artwork reproduction is not general lifestyle stock |
| Internet Archive | Heterogeneous public image collections | Curated provenance required; audio tested here |
| Pixabay / Pexels / Unsplash | Contemporary stock | Key/account required; excluded, NOT_RUN |
| Gallica | Historical photos | Search blocked; commercial reuse generally paid |

**Gap P1:** no equivalent to a modern lifestyle/product stock library with model/property releases established by this research.

### Video

| Provider | Coverage | Recommendation / rights gate |
|---|---|---|
| NASA | Mission footage and science features; multiple MP4 renditions | First version; one preview MP4 fully decoded |
| Wikimedia Commons | Open clips, principally WebM/Ogg and derivatives | First version provider; video path NOT_RUN |
| Internet Archive | Public moving-image archives, including collection-specific sources | Curated subset only; Prelinger presence is not universal permission |
| Library of Congress / Finna | Archival moving images or catalogue links | Reserve; actual video files NOT_RUN |
| Gallica | Some video records | Blocked; rights restrictions |
| Pexels / Pixabay | Contemporary stock footage | API key required; excluded |

**Gap V1:** validated video is strongest for NASA subject matter; no broad, commercially cleared contemporary B-roll source passed the complete no-account/no-key gate.

## Provider dossiers: official sources and client rules

For each dossier, “no published limit found” is **Unknown**, not permission for unlimited requests. Unless a provider explicitly states otherwise, hotlink obligations are Unknown; preserve the canonical item page and returned file URL, and do not invent CDN URLs. The recommended common client behavior is one outstanding request per provider, at least one second between requests, smaller responses, HTTP cache/ETag handling, bounded time/size limits and a stop on challenges. LoC needs a slower budget. These are proposed safeguards, not provider-issued quotas.

### 1. Wikimedia Commons

Sources: [Commons API](https://commons.wikimedia.org/wiki/Commons:API), [API etiquette](https://www.mediawiki.org/wiki/API:Etiquette), [User-Agent policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy), [reuse policy](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia). All read 2026-10-27.

Public Action API reads require no account/key; observed search and image download confirm this path. Send an informative application/version/contact User-Agent. Use serial requests, efficient/batched fields, caching and `maxlag` for noninteractive work; respect errors and backoff. A universal safe anonymous read rate was not established. Downloading and hotlinking are described as possible; credit belongs to the creator, not necessarily the uploader. Media licences vary: PD, CC0, BY, BY-SA and other accepted free licences; never substitute the wiki-text licence. The selected ocean image is **CC BY-SA 3.0**, not CC0. Formats include JPEG/PNG/SVG, audio and video originals/transcodes; returned MIME and rendition links must be inspected. Only JPEG was tested.

### 2. The Metropolitan Museum of Art

Sources: [official API documentation](https://metmuseum.github.io/), [Open Access policy](https://www.metmuseum.org/hubs/open-access). Read 2026-10-27.

No key or registration. Current documentation migrates **search to v1.1**, while object details remain under v1; the former `/v1/search` returned HTTP 410 with a migration message. The documented successor succeeded. The stated ceiling is 80 requests/second; this is not a recommended operating rate. v1.1 introduces pagination; do not assume one search returns the entire catalogue. Public-domain artwork images and basic Open Access data use CC0; `hasImages` alone is not a licence filter, so check `isPublicDomain` and a nonempty image URL. Attribution is useful provenance, not a CC0 condition. No extra mandatory header, cache duration or hotlink rule was found in the reviewed pages. JSON provides primary/small/additional image links, generally JPEG. The tested Sunflowers object is `436524`, with `isPublicDomain=true`.

### 3. Art Institute of Chicago (AIC)

Sources: [official API documentation](https://api.artic.edu/docs/); attempted [image licensing](https://www.artic.edu/image-licensing) returned 403 in documentation retrieval. Read/attempted 2026-10-27.

API documentation describes unauthenticated access, 60 requests/minute/IP, caching and field selection. It prefers hotlinking; for local image collection it asks for one download at a time and suggests a one-second delay and the 843-pixel JPEG rendition. JSON supplies `image_id` and an IIIF base. Metadata CC0 does not clear every artwork image: inspect `is_public_domain`, copyright and credit fields. Detailed licensing-page review remains incomplete. `AIC-User-Agent` with project/contact information is requested as a courtesy, not an authentication requirement; this probe used ordinary User-Agent only. The fresh search received **403 HTML, `cf-mitigated: challenge`**. Stop; no alternative egress, repeated request or image attempt was made. Image availability/formats are documented, not validated on this host.

### 4. Cleveland Museum of Art

Sources: [Open Access API](https://openaccess-api.clevelandart.org/), [Open Access policy](https://www.clevelandart.org/open-access). Read 2026-10-27.

Public search/download needs no account or key. Use the documented `cc0` and `has_image` parameters and inspect `share_license_status`. Open metadata can describe copyrighted works, so metadata openness alone is insufficient. CC0 images allow commercial modification without required attribution; provenance is recommended and trademarks/other rights are separate. The selected `1972.47` record explicitly reports CC0. JSON exposes web/print JPEG and full TIFF variants; the web JPEG decoded. No mandatory special header, numeric quota, fixed cache duration or hotlink requirement was found in the reviewed official pages. Keep the returned source-page and rendition links and respect HTTP caching. Cloudflare ray headers occurred with successful responses; a ray header alone is not a challenge.

### 5. Rijksmuseum

Sources: [data services](https://data.rijksmuseum.nl/docs/), [Search API](https://data.rijksmuseum.nl/docs/search), [IIIF images](https://data.rijksmuseum.nl/docs/iiif/image), [Information and Data Policy](https://data.rijksmuseum.nl/policy/information-and-data-policy), [terms index](https://www.rijksmuseum.nl/en/footer/terms-and-conditions). Read 2026-10-27; the linked website-terms PDF could not be retrieved because its redirected download was inaccessible.

The current Search API explicitly needs no key; do not reuse assumptions about the old Rijksstudio API. Search returns Linked Art identifiers; obtain the record and follow image access points. JSON-LD and IIIF support resized JPEG/PNG renditions. The tested SK-C-5 record and 800-pixel JPEG succeeded. Policy makes no distinction between commercial and other users, but rights are still attached to data/media: PDM/CC0 predominate, BY is possible, and restricted third-party content is not open data. Attribution is recommended good practice. Do not apply the policy document's own BY licence to collection images. Numeric quota, compulsory UA and fixed cache period were not established; use returned cache headers and persistent identifiers. Full website-terms review remains an explicit gap.

### 6. Library of Congress (LoC)

Sources: [JSON/YAML API](https://www.loc.gov/apis/json-and-yaml/), [requests](https://www.loc.gov/apis/json-and-yaml/requests/), [working within limits](https://www.loc.gov/apis/json-and-yaml/working-within-limits/). Read 2026-10-27. [Legal page](https://www.loc.gov/legal/) timed out; a collection rights-page retrieval was also inaccessible.

Public API reads need no account/key. Official limits distinguish JSON/YAML **20 requests/minute**, images 150/minute, streaming media 60/minute and media downloads 150/minute; excessive traffic can trigger a one-hour block and lower protective thresholds may apply. Budget below the ceiling (e.g. one JSON request every four seconds), stop on 429/challenges and obey Retry-After. No compulsory special header was established. Search responses exposed a 24-hour cache header; this is an observation, not a universal policy. Media variants vary: JPEG/TIFF/JP2, audio and moving-image resources. The selected Detroit Publishing photograph says **“No known restrictions on publication”**, which is not a CC0 licence or a guarantee. Preserve the advisory, collection context and item link. Only a JPEG was validated.

### 7. NASA Image and Video Library

Sources: [official API PDF, v1.22](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf), [NASA images and media guidance](https://www.nasa.gov/nasa-brand-center/images-and-media/). Read 2026-10-27.

`images-api.nasa.gov/search` and returned asset manifests are public without a key/account; do not confuse this API with api.nasa.gov key-based services or copy their quotas. No numeric rate, required special header, fixed cache duration or mandatory hotlink rule was established for this library. Search JSON supports image/audio/video types; asset manifests enumerate originals and size/quality variants. Tested video offered original/large/medium/mobile/preview/small MP4s and thumbnails; one preview decoded as H.264/AAC. The manifest supplied HTTP media links; the same returned host/path was requested with HTTPS, not a bypass host. NASA material is not universally CC0: identify third-party copyright, credit NASA, avoid implied endorsement, and follow logo/insignia and identifiable-person rules. Current employees' likenesses have additional advertising restrictions. Government origin alone is not a blanket commercial clearance.

### 8. Internet Archive

Sources: [developer portal](https://archive.org/developers/), [advanced search and query help](https://archive.org/advancedsearch.php), [metadata read API](https://archive.org/developers/md-read.html), [automated-access policy](https://archive.org/developers/bots.html). Read 2026-10-27. The [general terms](https://archive.org/about/terms) did not expose readable terms in the retrieval; review remains incomplete.

Public search, metadata and unrestricted files worked without an account; restricted/borrowed items are excluded. Current bot policy asks for tool/version identification and AI-model information in User-Agent, caching, polite pacing and handling 429/Retry-After. No single guaranteed numeric quota was established. The first search and metadata request used an identifying UA but **omitted model identification**; this was corrected before subsequent Archive requests and the LibriVox download. Preserve this limitation in the evidence instead of claiming complete policy conformance from the outset.

The first CC0-tagged result contained metadata but no audio file. A second, explicitly hypothesized search constrained collection and MP3 format; its selected public MP3 decoded. Its uploader's CC0 claim does not establish rights to compositions, performances or samples. This community album is **not approved for reuse**. Files can include MP3/OGG/FLAC/WAV, video and images; read `files`, `format`, size and access restrictions, following ordinary download redirects. No harvesting or raw uploader-account metadata is published here.

### 9. LibriVox

Sources: [official API guide](https://librivox.org/api/info), [public-domain statement](https://librivox.org/pages/public-domain/). Read 2026-10-27.

Public audiobook feed and section URLs need no account/key. The guide specifies JSON/XML, `extended=1` for sections, pagination, default 50 and maximum 500 results; use courteous delays. No numeric request quota, required UA, cache interval or hotlink obligation was established. Download URLs may point to Internet Archive, whose client rules also apply. The tested Raven recording (book 397; reader Chris Goringe) downloaded as a real 64 kbps MP3. The provider permits reuse, including commercial use, without required credit under its **US public-domain** claim; outside the US, check both text and recording rights. Do not copy the page's historical year cutoff as current copyright law. This source is narrated literature, not a music, SFX or custom narration service. Preserve author, reader and source-page provenance even where attribution is optional.

### 10. ccMixter

Sources: [Query API](https://ccmixter.org/query-api), [terms of use](https://ccmixter.org/terms). Read 2026-10-27.

Anonymous query API works without a key/account. `f=json`, tags, licence and limit parameters support bounded discovery. Response MIME was **text/plain**, but its body parsed as JSON; MIME alone would wrongly reject this search. Individual tracks can use BY, BY-NC and other CC variants; inspect the exact licence and all credited sample sources. The selected “Lost Roamin'” record (`71077`, Speck and credited collaborators) declared CC BY 3.0, but its MP3 URL returned 403. No retry followed.

Terms section 4 also limits using material to advertise/promote products or services other than the resulting work or oneself. The interaction with client advertising and the track's CC licence needs clarification; this report does not adjudicate enforceability. Hold it out of client-ad defaults. Numeric quota, required headers, cache policy and mandatory hotlink behavior were not established. JSON can expose MP3 and other submitted-file links; only the denied MP3 download was attempted.

### 11. Finna (National Library of Finland)

Sources: [official English API guide](https://www.kiwi.fi/spaces/Finna/pages/53839221/Finna+API+in+English), linked [API terms](https://www.kiwi.fi/display/Finna/Finna+API+Terms+of+Use). Guide read 2026-10-27; terms retrieval returned 403.

Anonymous `/v1/search` worked without a key/account; an original image link from `imagesExtended` also worked. Finna aggregates institutions: the tested `tmk.161011074953400` photograph (Sea Enterpriser, Forum Marinum) declared PDM, but this must not be generalized to other records. Inspect each image's rights, credit, source institution and usage links. JSON can expose thumbnail, large/original and IIIF variants; the selected original was JPEG 3008×2000. Search and image responses included no-cache/no-store controls; do not overwrite those with a blanket persistent cache. Required UA, numeric quotas, definitive API attribution/linking obligations and broader automated-use terms remain **Unknown because the terms page was blocked**. Technical PASS, policy qualification pending.

### 12. Wellcome Collection

Sources: [Catalogue API guide](https://developers.wellcomecollection.org/docs/catalogue), [API reference](https://developers.wellcomecollection.org/api/catalogue), [first-party repository](https://github.com/wellcomecollection/catalogue-api). Read 2026-10-27.

The guide explicitly permits starting without signup or authentication. Own catalogue data are CC0; third-party data are not automatically CC0. Digitized media need their own rights field/IIIF context. The botanical illustration tested here declared PDM and its IIIF JPEG decoded. Search provides works/images and links to digitized resources; JPEG renditions and IIIF manifests are the useful image path. Full catalogue harvesting should use the daily snapshot, not repeated API queries. No fixed numerical quota, compulsory UA or hotlink requirement was established. The sampled IIIF file had a 28-day cache lifetime; do not assume every API response has that policy. General website content licensing is not the same as collection-image licensing. Good candidate for a later curated scientific-illustration module.

### 13. ambientCG

Sources: [API overview](https://docs.ambientcg.com/api/), [v3 assets](https://docs.ambientcg.com/api/v3/assets/), [licence](https://docs.ambientcg.com/license/). Read 2026-10-27.

The documented public assets endpoint and one download worked without registration/key. Assets and preview images use CC0, including commercial use without required attribution. A canonical asset link is available as `https://ambientcg.com/a/{id}`. Numeric quota, mandatory UA and fixed cache/linking rules were not found; respect actual HTTP cache headers. The provider explicitly cautions that this is a one-person service intended for hobbyists/educators and may not provide enterprise reliability. The v3 endpoint exposes download packages; Ground054's 1K-JPG ZIP was retrieved, CRC-checked and its seven images decoded. Other advertised variants include higher-resolution JPEG/PNG material maps and HDR-related assets; they were not downloaded. This is a graphics/material source, not general stock photos or SFX.

### 14. PhyloPic

Sources: [API v2 documentation](https://api-docs.phylopic.org/v2/index.html), [official API recipes](https://www.phylopic.org/articles/api-recipes), [image usage](https://www.phylopic.org/articles/image-usage). Read 2026-10-27; the reference landing page was script-heavy, so operational details came from the readable first-party recipes.

Anonymous taxon search and image metadata/download work without a key/account. Recommended `Accept: application/vnd.phylopic.v2+json`; omitted build causes a documented 307 redirect to the current build. Old builds return 410; do not pin build 560 permanently. List search, page and image relations are separate calls, not duplicate search retries. Build-pinned responses carried one-year immutable caching. No numeric quota or compulsory User-Agent was established. Images have individual CC0/PDM/BY/BY-SA/NC terms; PhyloPic itself never requires site credit, but creators/licences can require attribution. The tested silhouette by Steven Traver was CC0, available as SVG source/vector and multiple PNG sizes; PNG 1536×1020 decoded. This covers silhouettes, not a general icon library.

### 15. Poly Haven

Sources: [first-party Public API README](https://github.com/Poly-Haven/Public-API), [current API terms](https://raw.githubusercontent.com/Poly-Haven/Public-API/master/ToS.md), [OpenAPI schema](https://raw.githubusercontent.com/Poly-Haven/Public-API/master/swagger.yml). Read 2026-10-27.

Current terms explicitly allow free commercial API use without a key or commercial licence. Earlier assumptions of noncommercial-only API access must not be carried forward. Requests must identify the software through a unique User-Agent **or** Referer. A product surfacing content through the live API must visibly credit Poly Haven without implying endorsement. That service-credit condition does **not** become a copyright attribution condition on downloaded/self-hosted CC0 assets. Abuse is prohibited; no fixed numerical quota was established. The tested search/files responses exposed HTTP cache lifetimes; honor those rather than hard-coding a global TTL. Search and `/files/{id}` yielded a CC0 sand texture, and its 1K diffuse JPEG decoded. Other file variants include PNG/EXR maps, HDRIs and model formats. API code licensing is separate from asset licensing.

### 16. SMK (National Gallery of Denmark)

Sources: [official Swagger UI](https://api.smk.dk/api/v1/docs/), its public [swagger-ui-init.js schema](https://api.smk.dk/api/v1/docs/swagger-ui-init.js), [SMK API page](https://www.smk.dk/article/smk-api/), [SMK Open](https://www.smk.dk/en/article/smk-open/). Read/attempted 2026-10-27. The institutional prose pages required JavaScript and their full policy text was not available in the retrieval; this is not evidence of forbidden automation.

The official OpenAPI schema documents public art search, filters and image fields; search and the advertised thumbnail worked without account/key. The sampled KKS2004-95 record explicitly had `public_domain=true` and a PDM rights URL. Preserve that record-level statement rather than assuming every SMK image is open. JSON supplies IIIF, thumbnail and native image links; stored TIFF/JP2 identifiers can produce JPEG renditions. Tested JPEG 1024×683. No required UA, numerical rate, definitive attribution/hotlink rule or general cache policy was verified from the inaccessible prose pages; the thumbnail response allowed a one-day cache. Technical PASS; full policy qualification remains pending.

### 17. Gallica / Bibliothèque nationale de France

Sources: [official search API](https://api.bnf.fr/fr/api-gallica-de-recherche), [BnF API/data portal and rights explanation](https://www.bnf.fr/fr/portail-bnf-api-et-jeux-de-donnees), [provider's API listing](https://www.data.gouv.fr/dataservices/api-gallica-recherche). Read 2026-10-27. The linked detailed Gallica terms page was blocked, but the BnF institutional rights summary was directly readable.

The public SRU search is documented without account/key, using CQL/XML and up to 50 records; a one-record query here received **403 HTML**. No file request followed. Numeric request quota, special UA and cache/hotlink obligations were not established; abuse is excluded by the provider listing. Metadata are under the French open-data licence with source attribution, including commercial reuse. **Digitized documents have different terms:** BnF says noncommercial reuse is free with source credit, while commercial reuse is paid/licensed; partners can differ. This excludes Gallica from the free commercial-media default even if its transport later works. Image/document derivatives and sound/video catalogue records are documented coverage, not locally validated downloads.

### 18. SFXMint (discovered through GitHub mapping)

Sources: [official API documentation](https://sfxmint.com/api/docs), [library licence](https://sfxmint.com/license), [terms](https://sfxmint.com/terms), [first-party MCP README](https://github.com/flreey/sfxmint-mcp). Read 2026-10-27; terms dated 2026-10-22.

Library search/metadata and files need no key/account. Library sounds are CC0, allowing commercial edits and redistribution without required attribution; retain page and hash provenance. The provider describes them as AI-generated or procedurally synthesized, not recordings. This does not validate exclusivity or scene suitability. Free private generations can instead be NC; generation is outside this research and must not inherit the library's CC0 label. Terms prohibit reselling API/generation access; that service restriction is separate from commercial reuse of downloaded CC0 library audio. Review any future paid access model against it.

Script/API downloads allow **20 different sounds/day/network**, resetting at UTC midnight; additional formats/repeats of the same sound do not count again. A limit response is 429 with Retry-After; stop rather than change addresses. Search has no verified numeric rate ceiling. No mandatory special header was found; use an honest identifying UA. Hotlinking is permitted. Search returned `no-store`; the downloaded WAV returned one-year immutable caching. Preserve returned URLs and canonical pages. Formats: WAV/MP3; OGG is available for some older sounds. Structured metadata includes per-format duration, bytes and SHA-256; loop claims still need independent playback checks.

One bounded search and one WAV download succeeded, with matching hash and full local decode (1.0 s, stereo PCM, 44.1 kHz). No generation, login, installation or MCP connection was attempted. Conditional first-version SFX candidate; not a music or speech catalogue.

## Documentation-gate exclusions and unresolved leads

These were screened before attempting a media search. They are not counted among the 18 tested keyless candidates. **NOT_RUN** is intentional where an account/key or undocumented interface would violate scope. Documentation was checked on 2026-10-27; no API search/download time exists for these rows.

| Source | Official evidence / gate | Search / download |
|---|---|---|
| Freesound | [API overview](https://freesound.org/docs/api/overview.html): API credential required for basic calls; some resources additionally require OAuth | NOT_RUN / NOT_RUN |
| Jamendo | [Authentication](https://developer.jamendo.com/v3.0/authentication): every call needs client_id obtained via developer signup; published demonstration credentials are not a keyless production API | NOT_RUN / NOT_RUN |
| Harvard Art Museums | [First-party API README](https://github.com/harvardartmuseums/api-docs): registration/key required; representative university museum exclusion | NOT_RUN / NOT_RUN |
| Europeana | [Get an API key](https://pro.europeana.eu/page/get-api): account and key required | NOT_RUN / NOT_RUN |
| Smithsonian | Official [developer-tools page](https://www.si.edu/openaccess/devtools) search extraction says api.data.gov key; direct page returned 404, so current detailed client rules remain Unknown. [First-party repository](https://github.com/Smithsonian/OpenAccess) points to open bulk data, not a keyless hosted search substitute | NOT_RUN / NOT_RUN |
| Pixabay | [API docs](https://pixabay.com/api/docs/): key-based image/video API; website music/SFX categories do not establish music/SFX API endpoints | NOT_RUN / NOT_RUN |
| Pexels | [API docs](https://www.pexels.com/api/documentation/): Authorization key; no inference here about whether new keys are currently issued | NOT_RUN / NOT_RUN |
| Unsplash | [API docs](https://unsplash.com/documentation): developer/application registration and access key | NOT_RUN / NOT_RUN |
| BBC Sound Effects | [Provider site](https://sound-effects.bbcrewind.co.uk/): no suitable official public keyless search API verified; terms retrieval incomplete | NOT_RUN / NOT_RUN; eligibility Unknown |
| OpenGameArt | [Provider site](https://opengameart.org/): a searchable website was not accepted as an API; no suitable official API contract established | NOT_RUN / NOT_RUN; eligibility Unknown |
| Iconify | [API documentation lead](https://iconify.design/docs/api/): documentation access blocked by retrieval robots policy; no attempt to circumvent it | NOT_RUN / NOT_RUN; eligibility Unknown |
| Lots of Sounds | [Official API examples](https://github.com/lotsofsounds/lots-of-sounds-api-examples): search requires a Pro/Enterprise key; anonymous samples do not provide keyless search | NOT_RUN / NOT_RUN |
| Openverse | Owner decision: set aside; no renewed availability investigation | NOT_RUN / NOT_RUN |

This is a broad discovery pass, not a claim to enumerate every archive. Additional university repositories or national libraries should enter only with an official supported search contract and their own rights/client dossier; public IIIF images alone do not prove a searchable provider API.

## ChatGPT Work test results

Tests ran on **2026-10-27**, from this session's command execution environment. They used ordinary Python HTTPS GETs with a descriptive User-Agent, no authentication/cookies, a 25-second socket timeout and a 32 MiB response cap. Calls were sequential within each provider chain; independent providers sometimes ran concurrently. Requests were small (normally one result); necessary record/manifest calls are separately recorded. Automatic HTTP redirects are listed in the evidence. No retry was made after a protection block.

The [sanitized machine-readable evidence](../../verification/free-media-providers-2026-10-chatgpt-work.json) records **every probe**: hypothesis stated before request, exact URL, start/end UTC, request headers, HTTP status, selected response headers, redirects, bytes, SHA-256, parsing and decoder results. Original response bodies and downloaded media are not committed; body hashes identify the actual observations without republishing media or uploader account fields. This is an HTTP/decoder test, not a visual-quality or listening review.

Status meanings: **PASS** = successful public search plus one downloaded and decoded medium for the representative path; **FAIL** = attempted request failed that path; **NOT_RUN** = not attempted; **Unknown** = evidence insufficient. Missing `cf-mitigated`/`cf-ray` means not observed in that response, not proof that no protection exists. A Cloudflare ray with HTTP 200 is not treated as failure. Claude Code, standalone Codex and installed companion behavior are all **NOT_RUN**.

| Provider | Overall | Search status / HTTP / UTC | Download status / HTTP / UTC | Decoded representative medium |
|---|---|---|---|---|
| Wikimedia Commons | **PASS** | PASS / 200 at 15:28:27 | PASS / 200 at 15:30:28 | JPEG photograph 960×698 |
| The Met | **PASS** | PASS / 200 at 15:30:22 | PASS / 200 at 15:33:45 | JPEG artwork 599×423 |
| Art Institute of Chicago | **FAIL** | FAIL / 403 at 15:29:08 | NOT_RUN | search blocked |
| Cleveland Museum of Art | **PASS** | PASS / 200 at 15:29:15 | PASS / 200 at 15:30:35 | JPEG artwork 778×893 |
| Rijksmuseum | **PASS** | PASS / 200 at 15:29:23 | PASS / 200 at 15:33:52 | IIIF JPEG artwork 800×664 |
| Library of Congress | **PASS** | PASS / 200 at 15:29:31 | PASS / 200 at 15:32:15 | JPEG photograph 640×502 |
| NASA Image and Video Library | **PASS** | PASS / 200 at 15:29:40 | PASS / 200 at 15:33:59 | MP4 preview video 281.77 s |
| Internet Archive | **PASS** | PASS / 200 at 15:34:06 | PASS / 200 at 15:40:08 | MP3 music recording 128.23 s |
| LibriVox | **PASS** | PASS / 200 at 15:31:22 | PASS / 200 at 15:34:34 | MP3 spoken word 570.96 s |
| ccMixter | **FAIL** | PASS / 200 at 15:31:29 | FAIL / 403 at 15:34:57 | MP3 download denied |
| Finna | **PASS** | PASS / 200 at 15:31:37 | PASS / 200 at 15:35:05 | JPEG photograph 3008×2000 |
| Wellcome Collection | **PASS** | PASS / 200 at 15:31:45 | PASS / 200 at 15:35:13 | IIIF JPEG illustration 800×1326 |
| ambientCG | **PASS** | PASS / 200 at 15:32:51 | PASS / 200 at 15:39:45 | ZIP with texture images; CRC and all 7 images PASS |
| PhyloPic | **PASS** | PASS / 200 at 15:32:55 | PASS / 200 at 15:40:52 | PNG silhouette 1536×1020 |
| Poly Haven | **PASS** | PASS / 200 at 15:34:23 | PASS / 200 at 15:40:03 | JPEG texture 1024×1024 |
| SMK | **PASS** | PASS / 200 at 15:35:00 | PASS / 200 at 15:39:57 | IIIF JPEG artwork 1024×683 |
| Gallica / BnF | **FAIL** | FAIL / 403 at 15:35:05 | NOT_RUN | search blocked |
| SFXMint | **PASS** | PASS / 200 at 16:02:31 | PASS / 200 at 16:03:11 | WAV SFX, 1.0 s stereo PCM; advertised hash matches |

### Additional attempts and hypothesis changes

- **Met H02b:** the old documented route returned 410 with a v1.1 migration instruction. The next search tested that published successor; it was not an anti-bot retry. Both responses remain in evidence.
- **Archive H08b:** initial search succeeded, but metadata contained no audio file. The next search tested whether an explicit downloadable MP3 format/collection constraint supplied a usable file. Exactly one media file was then downloaded. Its licence claim remains unapproved.
- **PhyloPic:** the initial result describes a paginated list; the next page and primary-image calls follow documented relations. The build redirect and all steps remain visible.
- **AIC, Gallica, ccMixter download:** stop after the failed request. No alternate host or altered browser-like headers were tried.

### Response trace

The table includes metadata/manifest calls because a successful search often does not itself contain a file URL. Times are request start times; all dates are 2026-10-27 UTC. Full URLs, headers and end times are in the JSON evidence. `—` means header absent.

| Request / hypothesis | UTC | HTTP | Content-Type | cf-mitigated | cf-ray | Bytes |
|---|---|---|---|---|---|---|
| `commons-search` / H01 | 15:28:27 | 200 | application/json; charset=utf-8 | — | — | 3693 |
| `met-search` / H02 | 15:29:01 | 410 | application/json | — | — | 438 |
| `aic-search` / H03 | 15:29:08 | 403 | text/html; charset=UTF-8 | challenge | a512bc39ebb9eb62-ORD | 6793 |
| `cleveland-search` / H04 | 15:29:15 | 200 | application/json | — | a512bc678cd113cd-ORD | 10196 |
| `rijks-search` / H05 | 15:29:23 | 200 | application/ld+json | — | — | 675 |
| `loc-search` / H06 | 15:29:31 | 200 | application/json | — | a512bccb0cf013cd-ORD | 54996 |
| `nasa-search` / H07 | 15:29:40 | 200 | application/json | — | — | 2056 |
| `archive-search` / H08 | 15:29:47 | 200 | application/json | — | — | 557 |
| `met-search-v1-1` / H02b | 15:30:22 | 200 | application/json | — | — | 35 |
| `commons-download` / H01d | 15:30:28 | 200 | image/jpeg | — | — | 165931 |
| `cleveland-download` / H04d | 15:30:35 | 200 | image/jpeg | — | a512be59eccdeb62-ORD | 567422 |
| `rijks-metadata` / H05m | 15:30:43 | 200 | application/ld+json | — | — | 173384 |
| `librivox-search` / H09 | 15:31:22 | 200 | application/json | — | a512bf7cb96d13cd-ORD | 1236 |
| `ccmixter-search` / H10 | 15:31:29 | 200 | text/plain | — | — | 1990 |
| `finna-search` / H11 | 15:31:37 | 200 | application/json | — | a512bfdac9e913cd-ORD | 999 |
| `wellcome-search` / H12 | 15:31:45 | 200 | application/json | — | — | 1431 |
| `met-metadata` / H02m | 15:32:08 | 200 | application/json | — | — | 2257 |
| `loc-download` / H06d | 15:32:15 | 200 | image/jpeg | — | a512c0c8ea27eb62-ORD | 104656 |
| `nasa-manifest` / H07m | 15:32:22 | 200 | application/json | — | — | 5017 |
| `archive-metadata` / H08m | 15:32:30 | 200 | application/json | — | — | 2611 |
| `ambientcg-search` / H13 | 15:32:51 | 200 | application/json | — | — | 3320 |
| `phylopic-search` / H14 | 15:32:55 | 200 | application/vnd.phylopic.v2+json; charset=utf-8 | — | — | 278 |
| `met-download` / H02d | 15:33:45 | 200 | image/jpeg | — | — | 208766 |
| `rijks-download` / H05d | 15:33:52 | 200 | image/jpeg | — | a512c325394c13cd-ORD | 71556 |
| `nasa-download` / H07d | 15:33:59 | 200 | video/mp4 | — | — | 22511852 |
| `archive-search-downloadable` / H08b | 15:34:06 | 200 | application/json | — | — | 653 |
| `polyhaven-search` / H15 | 15:34:23 | 200 | application/json; charset=utf-8 | — | a512c3e8a83513cd-ORD | 183 |
| `librivox-download` / H09d | 15:34:34 | 200 | audio/mpeg | — | — | 4568002 |
| `ccmixter-download` / H10d | 15:34:57 | 403 | text/html | — | — | 10 |
| `smk-search` / H16 | 15:35:00 | 200 | application/json; charset=utf-8 | — | — | 3679 |
| `finna-download` / H11d | 15:35:05 | 200 | image/jpeg | — | — | 2495448 |
| `gallica-search` / H17 | 15:35:05 | 403 | text/html; charset=UTF-8 | — | a512c4d5eaa1eb62-ORD | 4560 |
| `archive-metadata-downloadable` / H08m2 | 15:35:08 | 200 | application/json | — | — | 24682 |
| `polyhaven-files` / H15m | 15:35:12 | 200 | application/json; charset=utf-8 | — | a512c51b4e9c13cd-ORD | 24188 |
| `wellcome-download` / H12d | 15:35:13 | 200 | image/jpeg | — | — | 197314 |
| `phylopic-page` / H14p | 15:35:19 | 200 | application/vnd.phylopic.v2+json; charset=utf-8 | — | — | 3860 |
| `ambientcg-download` / H13d | 15:39:45 | 200 | application/zip | — | a512cbdc6c91eb62-ORD | 8674949 |
| `smk-download` / H16d | 15:39:57 | 200 | image/jpeg | — | — | 95106 |
| `polyhaven-download` / H15d | 15:40:03 | 200 | image/jpeg | — | a512cc26993ceb62-ORD | 703132 |
| `archive-download` / H08d | 15:40:08 | 200 | audio/mpeg | — | — | 2997094 |
| `phylopic-image` / H14m | 15:40:19 | 200 | application/vnd.phylopic.v2+json; charset=utf-8 | — | — | 2102 |
| `phylopic-download` / H14d | 15:40:52 | 200 | image/png | — | — | 32118 |
| `sfxmint-search` / H43 | 16:02:31 | 200 | application/json | — | a512ed1bcbeb13cd-ORD | 15517 |
| `sfxmint-download` / H44 | 16:03:11 | 200 | audio/wav | — | a512ee0c7936eb62-ORD | 176478 |

## Proposed next step (not implementation authorization)

1. Apply the owner's all-qualified-sources rule to every candidate, without a fixed provider-count limit. Keep the no-key/no-account constraint unless explicitly changed. Use the approved name **FrameCore Open Assets** and identifier `framecore-open-assets`; implementation still requires owner authorization.
2. Resolve policy, rights and target-host evidence gaps before enabling each provider/media path. Keep unresolved candidates pending rather than silently excluding them because of the old priority tiers or treating a download as licence clearance.
3. After build authorization, implement separate documented provider modules and provenance/licence filtering. Validate each actual media path and the active host; this session's JPEG successes cannot stand in for audio/video tests.
4. Run fresh Claude Code tests separately before enabling providers there. Preserve host-specific failures and the Studio rule about explaining a failure before choosing another route.

Coverage gaps remain explicit: limited spoken-word audio, **no broadly recommended music catalogue**, and **synthetic/AI SFX with a daily download allowance**. The all-qualified-sources rule does not relax the keyless requirement or erase these limits. The name is approved; build authorization remains pending.
