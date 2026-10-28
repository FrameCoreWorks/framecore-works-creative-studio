# NASA Image and Video Library

Sources: [official API PDF, v1.22](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf), [NASA images and media guidance](https://www.nasa.gov/nasa-brand-center/images-and-media/). Read 2026-10-27.

`images-api.nasa.gov/search` and returned asset manifests are public without a key/account; do not confuse this API with api.nasa.gov key-based services or copy their quotas. No numeric rate, required special header, fixed cache duration or mandatory hotlink rule was established for this library. Search JSON supports image/audio/video types; asset manifests enumerate originals and size/quality variants. Tested video offered original/large/medium/mobile/preview/small MP4s and thumbnails; one preview decoded as H.264/AAC. The manifest supplied HTTP media links; the same returned host/path was requested with HTTPS, not a bypass host. NASA material is not universally CC0: identify third-party copyright, credit NASA, avoid implied endorsement, and follow logo/insignia and identifiable-person rules. Current employees' likenesses have additional advertising restrictions. Government origin alone is not a blanket commercial clearance.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.

2026-10-28 update: photos and video passed fresh Work download/decode. Audio is disabled in the registry: selected podcast renditions exceeded the 32 MiB cap, and a narrower historical query returned no match. Do not claim an audio delivery PASS.
