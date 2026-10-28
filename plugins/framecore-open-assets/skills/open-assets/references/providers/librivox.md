# LibriVox

Sources: [official API guide](https://librivox.org/api/info), [public-domain statement](https://librivox.org/pages/public-domain/). Read 2026-10-27.

Public audiobook feed and section URLs need no account/key. The guide specifies JSON/XML, `extended=1` for sections, pagination, default 50 and maximum 500 results; use courteous delays. No numeric request quota, required UA, cache interval or hotlink obligation was established. Use only chapter URLs returned by the LibriVox feed. Its verified `archive.org` storage hosts remain a delivery dependency, subject to their client rules; this module does not search that host's general catalogue. The tested Raven recording (book 397; reader Chris Goringe) downloaded as a real 64 kbps MP3. The provider permits reuse, including commercial use, without required credit under its **US public-domain** claim; outside the US, check both text and recording rights. Do not copy the page's historical year cutoff as current copyright law. This source is narrated literature, not a music, SFX or custom narration service. Preserve author, reader and source-page provenance even where attribution is optional.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
