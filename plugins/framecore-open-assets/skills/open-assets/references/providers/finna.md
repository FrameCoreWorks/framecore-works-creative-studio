# Finna

Sources: [API guide](https://www.kiwi.fi/spaces/Finna/pages/53839221/Finna+API+in+English), [API Terms of Use](https://www.kiwi.fi/spaces/Finna/pages/53839699/Finna+API+Terms+of+Use), [API](https://api.finna.fi/v1/). Directly read 2026-10-28.

Public reads require no key, account or registration. Metadata CC0 does not cover the images. The module uses online-image/free-use filters and reads `imagesExtended[].rights.link`; default download accepts explicit PDM/CC0/CC BY, blocks NC/ND/unknown, and requires separate SA acceptance. Creator and institution credits are retained; credit Finna.fi and the institution even when optional. Restrictions and third-party rights still require item review.

No numeric quota or special header requirement was established in the read terms. Use an honest identifying User-Agent, serial requests at least 1.1 seconds apart, bounded results, response-directed cache and no bulk harvesting. Relative image links resolve against api.finna.fi; record links against www.finna.fi. JPEG originals and proxy/resized variants are returned. Institutional originals are usable only on reviewed allowlisted hosts; other originals are skipped in favor of official proxy variants, never followed through an unrestricted redirect.

Work 2026-10-28: official search and a 3008×2000 JPEG from the source institution passed decoding. This confirms one actual image path, not every Finna institution or file.
