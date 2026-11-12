# Changelog

## 1.0.3 - 2026-11-12

- The direction menu names the separate FrameMotion plugin for motion graphics, which Creative Studio 1.178.0 moved out of Studio (owner decision 2026-11-12).

## 1.0.2 - 2026-11-04

- Audit fix (GPT Astra audit 2026-11-04, SEC-001): with a proxy configured but `NO_PROXY` sending the host direct, the connect-time peer check was skipped, so DNS rebinding could reach a private address. The check now follows urllib's actual routing for each request and redirect: only a request that really goes through the proxy skips it (its peer is the proxy). Reproduced before the fix (HTTP 200 from a local server), refused after it, before any request is sent.
- Listing subtitle shortened to "Brand kit from a website" (Plugin Creator allows 30 characters; audit DIST-003).

## 1.0.1 - 2026-10-24

- Review fix (2026-10-24 full review): every connection checks its actual peer address, so a name that resolves to a public address at the check and to a private one at connect time (DNS rebinding) is refused; behind a configured proxy the proxy resolves names, as before.

## 1.0.0 - 2026-10-24

- First release: `brand-kit:brand` skill with the brand audit outline and the direction menu; `scripts/brandkit.py`
  with bounded website evidence (`extract`), a draft in Studio's brand kit format with a source ledger (`draft`) and a
  per-brand revision catalog (`save`, `list`, `show`, `diff`).
