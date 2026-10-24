# Changelog

## 1.0.1 - 2026-10-24

- Review fix (2026-10-24 full review): every connection checks its actual peer address, so a name that resolves to a public address at the check and to a private one at connect time (DNS rebinding) is refused; behind a configured proxy the proxy resolves names, as before.

## 1.0.0 - 2026-10-24

- First release: `brand-kit:brand` skill with the brand audit outline and the direction menu; `scripts/brandkit.py`
  with bounded website evidence (`extract`), a draft in Studio's brand kit format with a source ledger (`draft`) and a
  per-brand revision catalog (`save`, `list`, `show`, `diff`).
