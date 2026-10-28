# Changelog

## 0.2.1, 2026-10-28

Only confirmed providers and media categories are distributed. The registry, provider dossiers and
CLI choices match the fourteen implemented providers; unused media handling is removed.
Per-asset rights checks, current-host verification and Studio/Earshot handoffs remain unchanged.

## 0.2.0, 2026-10-28

Four newly qualified image providers, host/category proof binding, provider pacing and media-type checks. Real Work validation and provenance handoff to Earshot/Studio.

## 0.1.1, 2026-10-28

- Align all three manifest licence declarations with the bundled Apache-2.0 licence.
- Guard the manifest agreement in the package regression test.
- Use OS-owned provider locks so completed or interrupted processes do not leave a permanent busy state; retain serial request pacing and reject real concurrency.

## 0.1.0, 2026-10-28

Owner-authorized creation of FrameCore Open Assets, using Earshot's Claude/ChatGPT/Codex packaging pattern.

- One sourcing skill, three consistent manifests, a portable Python CLI and ten separate provider adapters.
- Provider dossiers record official source URLs and reading dates.
- Per-asset rights gates, local host/category verification, signed search results, serial identified requests,
  HTTP cache controls, bounded downloads, full media decoding and provenance sidecars.
- No automatic source switching, paid generation, credentials, scraping or protection bypass.
- Source/package tests and actual Work CLI tests are distinct from fresh installed-client and Claude evidence.
