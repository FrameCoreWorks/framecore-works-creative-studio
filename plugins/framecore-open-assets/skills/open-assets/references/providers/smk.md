# SMK — National Gallery of Denmark

Sources: [API](https://www.smk.dk/en/article/smk-api/), [official rights policy](https://connect.smk.dk/om/rettigheder), [OpenAPI explorer](https://api.smk.dk/api/v1/docs/). Directly read 2026-10-28 (API article and rights text; explorer schema referenced in the original research).

No key/account is required for public API reads. Public-domain artworks may be reused commercially; protected works need permission. The website's other images can carry CC BY-SA and do not grant a blanket licence to the collection. Require `public_domain=true` and each returned artwork's rights URL. NC/ND/unknown are blocked; the module's successful PDM example needs no licence attribution but preserves artist and SMK credit.

Use an honest User-Agent and serial pacing of at least 1.1 seconds; no provider numeric quota or special mandatory header was established. Obey cache headers and stop on challenges/429. The module requests bounded image/public-domain search results. It exposes provider JPEG thumbnails/native files; IIIF offers additional sizes but unsupported formats are not silently converted. Links retain the artwork's `frontend_url`.

Work 2026-10-28: search and a real 1600×1042 JPEG decoded successfully. Institutional policy was directly readable, resolving the earlier hold. Copyright/privacy/publicity can still vary by item and use.
