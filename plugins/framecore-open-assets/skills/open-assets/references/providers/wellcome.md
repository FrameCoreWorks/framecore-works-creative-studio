# Wellcome Collection

Sources: [Catalogue API guide](https://developers.wellcomecollection.org/docs/catalogue), [API reference](https://developers.wellcomecollection.org/api/catalogue), [first-party repository](https://github.com/wellcomecollection/catalogue-api). Read 2026-10-27.

The guide explicitly permits starting without signup or authentication. Own catalogue data are CC0; third-party data are not automatically CC0. Digitized media need their own rights field/IIIF context. The botanical illustration tested here declared PDM and its IIIF JPEG decoded. Search provides works/images and links to digitized resources; JPEG renditions and IIIF manifests are the useful image path. Full catalogue harvesting should use the daily snapshot, not repeated API queries. No fixed numerical quota, compulsory UA or hotlink requirement was established. The sampled IIIF file had a 28-day cache lifetime; do not assume every API response has that policy. General website content licensing is not the same as collection-image licensing. Good candidate for a later curated scientific-illustration module.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
