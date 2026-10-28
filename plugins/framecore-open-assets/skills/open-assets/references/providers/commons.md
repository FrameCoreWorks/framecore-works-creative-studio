# Wikimedia Commons

Sources: [Commons API](https://commons.wikimedia.org/wiki/Commons:API), [API etiquette](https://www.mediawiki.org/wiki/API:Etiquette), [User-Agent policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy), [reuse policy](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia). All read 2026-10-27.

Public Action API reads require no account/key; observed search and image download confirm this path. Send an informative application/version/contact User-Agent. Use serial requests, efficient/batched fields, caching and `maxlag` for noninteractive work; respect errors and backoff. A universal safe anonymous read rate was not established. Downloading and hotlinking are described as possible; credit belongs to the creator, not necessarily the uploader. Media licences vary: PD, CC0, BY, BY-SA and other accepted free licences; never substitute the wiki-text licence. The selected ocean image is **CC BY-SA 3.0**, not CC0. Formats include JPEG/PNG/SVG, audio and video originals/transcodes; returned MIME and rendition links must be inspected. Only JPEG was tested.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
