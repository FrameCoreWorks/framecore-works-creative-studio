# Internet Archive

Sources: [developer portal](https://archive.org/developers/), [advanced search and query help](https://archive.org/advancedsearch.php), [metadata read API](https://archive.org/developers/md-read.html), [automated-access policy](https://archive.org/developers/bots.html). Read 2026-10-27. The [general terms](https://archive.org/about/terms) did not expose readable terms in the retrieval; review remains incomplete.

Public search, metadata and unrestricted files worked without an account; restricted/borrowed items are excluded. Current bot policy asks for tool/version identification and AI-model information in User-Agent, caching, polite pacing and handling 429/Retry-After. No single guaranteed numeric quota was established. The first search and metadata request used an identifying UA but **omitted model identification**; this was corrected before subsequent Archive requests and the LibriVox download. Preserve this limitation in the evidence instead of claiming complete policy conformance from the outset.

The first CC0-tagged result contained metadata but no audio file. A second, explicitly hypothesized search constrained collection and MP3 format; its selected public MP3 decoded. Its uploader's CC0 claim does not establish rights to compositions, performances or samples. This community album is **not approved for reuse**. Files can include MP3/OGG/FLAC/WAV, video and images; read `files`, `format`, size and access restrictions, following ordinary download redirects. No harvesting or raw uploader-account metadata is published here.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
