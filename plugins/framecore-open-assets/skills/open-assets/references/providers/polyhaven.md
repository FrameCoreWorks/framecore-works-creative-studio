# Poly Haven

Sources: [first-party Public API README](https://github.com/Poly-Haven/Public-API), [current API terms](https://raw.githubusercontent.com/Poly-Haven/Public-API/master/ToS.md), [OpenAPI schema](https://raw.githubusercontent.com/Poly-Haven/Public-API/master/swagger.yml). Read 2026-10-27.

Current terms explicitly allow free commercial API use without a key or commercial licence. Earlier assumptions of noncommercial-only API access must not be carried forward. Requests must identify the software through a unique User-Agent **or** Referer. A product surfacing content through the live API must visibly credit Poly Haven without implying endorsement. That service-credit condition does **not** become a copyright attribution condition on downloaded/self-hosted CC0 assets. Abuse is prohibited; no fixed numerical quota was established. The tested search/files responses exposed HTTP cache lifetimes; honor those rather than hard-coding a global TTL. Search and `/files/{id}` yielded a CC0 sand texture, and its 1K diffuse JPEG decoded. Other file variants include PNG/EXR maps, HDRIs and model formats. API code licensing is separate from asset licensing.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
