# The Metropolitan Museum of Art

Sources: [official API documentation](https://metmuseum.github.io/), [Open Access policy](https://www.metmuseum.org/hubs/open-access). Read 2026-10-27.

No key or registration. Current documentation migrates **search to v1.1**, while object details remain under v1; the former `/v1/search` returned HTTP 410 with a migration message. The documented successor succeeded. The stated ceiling is 80 requests/second; this is not a recommended operating rate. v1.1 introduces pagination; do not assume one search returns the entire catalogue. Public-domain artwork images and basic Open Access data use CC0; `hasImages` alone is not a licence filter, so check `isPublicDomain` and a nonempty image URL. Attribution is useful provenance, not a CC0 condition. No extra mandatory header, cache duration or hotlink rule was found in the reviewed pages. JSON provides primary/small/additional image links, generally JPEG. The tested Sunflowers object is `436524`, with `isPublicDomain=true`.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
