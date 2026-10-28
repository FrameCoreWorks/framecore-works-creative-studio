# Finna (National Library of Finland)

Sources: [official English API guide](https://www.kiwi.fi/spaces/Finna/pages/53839221/Finna+API+in+English), linked [API terms](https://www.kiwi.fi/display/Finna/Finna+API+Terms+of+Use). Guide read 2026-10-27; terms retrieval returned 403.

Anonymous `/v1/search` worked without a key/account; an original image link from `imagesExtended` also worked. Finna aggregates institutions: the tested `tmk.161011074953400` photograph (Sea Enterpriser, Forum Marinum) declared PDM, but this must not be generalized to other records. Inspect each image's rights, credit, source institution and usage links. JSON can expose thumbnail, large/original and IIIF variants; the selected original was JPEG 3008×2000. Search and image responses included no-cache/no-store controls; do not overwrite those with a blanket persistent cache. Required UA, numeric quotas, definitive API attribution/linking obligations and broader automated-use terms remain **Unknown because the terms page was blocked**. Technical PASS, policy qualification pending.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
