# Cleveland Museum of Art

Sources: [Open Access API](https://openaccess-api.clevelandart.org/), [Open Access policy](https://www.clevelandart.org/open-access). Read 2026-10-27.

Public search/download needs no account or key. Use the documented `cc0` and `has_image` parameters and inspect `share_license_status`. Open metadata can describe copyrighted works, so metadata openness alone is insufficient. CC0 images allow commercial modification without required attribution; provenance is recommended and trademarks/other rights are separate. The selected `1972.47` record explicitly reports CC0. JSON exposes web/print JPEG and full TIFF variants; the web JPEG decoded. No mandatory special header, numeric quota, fixed cache duration or hotlink requirement was found in the reviewed official pages. Keep the returned source-page and rendition links and respect HTTP caching. Cloudflare ray headers occurred with successful responses; a ray header alone is not a challenge.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
