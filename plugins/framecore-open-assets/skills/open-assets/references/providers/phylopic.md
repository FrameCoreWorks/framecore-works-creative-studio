# PhyloPic

Sources: [API v2 documentation](https://api-docs.phylopic.org/v2/index.html), [official API recipes](https://www.phylopic.org/articles/api-recipes), [image usage](https://www.phylopic.org/articles/image-usage). Read 2026-10-27; the reference landing page was script-heavy, so operational details came from the readable first-party recipes.

Anonymous taxon search and image metadata/download work without a key/account. Recommended `Accept: application/vnd.phylopic.v2+json`; omitted build causes a documented 307 redirect to the current build. Old builds return 410; do not pin build 560 permanently. List search, page and image relations are separate calls, not duplicate search retries. Build-pinned responses carried one-year immutable caching. No numeric quota or compulsory User-Agent was established. Images have individual CC0/PDM/BY/BY-SA/NC terms; PhyloPic itself never requires site credit, but creators/licences can require attribution. The tested silhouette by Steven Traver was CC0, available as SVG source/vector and multiple PNG sizes; PNG 1536×1020 decoded. This covers silhouettes, not a general icon library.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
