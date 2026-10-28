# SMK (National Gallery of Denmark)

Sources: [official Swagger UI](https://api.smk.dk/api/v1/docs/), its public [swagger-ui-init.js schema](https://api.smk.dk/api/v1/docs/swagger-ui-init.js), [SMK API page](https://www.smk.dk/article/smk-api/), [SMK Open](https://www.smk.dk/en/article/smk-open/). Read/attempted 2026-10-27. The institutional prose pages required JavaScript and their full policy text was not available in the retrieval; this is not evidence of forbidden automation.

The official OpenAPI schema documents public art search, filters and image fields; search and the advertised thumbnail worked without account/key. The sampled KKS2004-95 record explicitly had `public_domain=true` and a PDM rights URL. Preserve that record-level statement rather than assuming every SMK image is open. JSON supplies IIIF, thumbnail and native image links; stored TIFF/JP2 identifiers can produce JPEG renditions. Tested JPEG 1024×683. No required UA, numerical rate, definitive attribution/hotlink rule or general cache policy was verified from the inaccessible prose pages; the thumbnail response allowed a one-day cache. Technical PASS; full policy qualification remains pending.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
