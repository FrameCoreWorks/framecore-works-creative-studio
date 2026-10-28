# Art Institute of Chicago (AIC)

Sources: [official API documentation](https://api.artic.edu/docs/); attempted [image licensing](https://www.artic.edu/image-licensing) returned 403 in documentation retrieval. Read/attempted 2026-10-27.

API documentation describes unauthenticated access, 60 requests/minute/IP, caching and field selection. It prefers hotlinking; for local image collection it asks for one download at a time and suggests a one-second delay and the 843-pixel JPEG rendition. JSON supplies `image_id` and an IIIF base. Metadata CC0 does not clear every artwork image: inspect `is_public_domain`, copyright and credit fields. Detailed licensing-page review remains incomplete. `AIC-User-Agent` with project/contact information is requested as a courtesy, not an authentication requirement; this probe used ordinary User-Agent only. The fresh search received **403 HTML, `cf-mitigated: challenge`**. Stop; no alternative egress, repeated request or image attempt was made. Image availability/formats are documented, not validated on this host.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.

## 2026-10-28 recheck

2026-10-28 fresh Work search again returned HTTP 403/Cloudflare; no media request followed.
