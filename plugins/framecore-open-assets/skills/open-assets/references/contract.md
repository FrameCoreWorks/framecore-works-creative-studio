# Runtime contract

## Inputs

Supply the actual host and model, a provider or explicitly federated selection, one of six categories,
a query up to 240 characters and 1-5 results/provider. Downloads consume an unchanged signed search
result from the same state directory, runtime revision and host, less than one day old. Select result
and variant by zero-based index. Output paths must be new and outside the plugin package.

## Results

The signed search payload carries `utc`, `host`, `fingerprint`, `query`, `category`, `items` and `trace`.
Each asset has `provider`, `id`, `title`, `creator`, `source_page`, `license`, `license_url`,
`rights_status`, `category`, `variants`, `warnings`, `attribution` and `retrieved_utc`. Each variant
has an exact provider URL and label, with byte count or SHA-256 when advertised. No fictitious
`download_url`, transformed CDN hostname or blanket site licence is accepted.

Downloads add selected variant, local path, SHA-256, byte count, response headers, decoded dimensions
or audio/video properties, rights-review note, SA choice and `technical_test_only`. Save the sidecar
with the file. The sidecar is provenance, not a model/property release or a guarantee of copyright.

## Rights

| Status | Normal download |
| --- | --- |
| eligible | Explicit CC0/PDM or supported CC BY with attribution |
| review_sa | User must deliberately accept SA and its obligations |
| review_nasa | User-supplied item/use-specific review of NASA restrictions |
| review_jurisdiction | User-supplied text and recording rights evidence for the intended jurisdiction |
| blocked | Refused; never reinterpret Unknown, NC or ND as permission |

Provider policy holds are independent and cannot be overridden by a CLI flag. Missing applicable
terms are a hold. A missing published numeric quota alone is not: documented fair-use rules and
conservative pacing still apply. One category's test never certifies another media category.

## Errors, pacing and cache

Exit 0 means the command completed, not that every result is commercially cleared. Exit 2 produces
JSON with `status`, `error`, `message`, request `trace` and `next_action`. Typical errors are
`policy_hold`, `rights_blocked`, `host_not_verified`, `cloudflare_challenge`, `access_denied`,
`rate_limited`, `transport_error`, `html_response`, `unapproved_host`, `size_limit`, `hash_mismatch`,
`decoder_missing`, `decode_failed`, `output_exists` and `untrusted_result`.

No automatic retry. A manually considered retry is limited to one additional attempt for a transient
failure, with a named hypothesis and provider Retry-After respected. No challenge/auth/rate bypass.
There is no source failover. Failed federated searches return their executed trace; other providers
are not queried after the failure. Preserve that failure when discussing alternatives.

JSON caching is keyed by exact URL and Accept header, uses cache-control max-age (capped at one day),
honors no-store/no-cache/private and may revalidate stale entries with ETag. `--fresh` bypasses it for
verification. Media is an explicitly requested local output, not a shared HTTP cache. Keep all
provider calls serial, at least one second apart. The state lock prevents concurrent local processes;
a lock left by a killed process requires inspection before removal, not repeated polling or bypass.

## Cross-host behavior

Three manifests identify one package/version. Claude uses the repository marketplace; ChatGPT uses
the complete private plugin package; Codex uses its compatibility manifest. The shared Python CLI
uses no remote MCP server, account, paid backend or generated browser session. Public GET requests
leave the host; downloaded media stays local until an independently authorized delivery.

Readiness evidence is local and short-lived. A host label is explicitly declared by the executing
agent. Never forge a Claude label in Work, move host proofs to another machine, or claim a package
test proves active-client registration. Missing shell/network yields a plan and a named limitation.
