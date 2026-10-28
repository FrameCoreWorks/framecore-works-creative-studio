# FrameCore Open Assets: build and verification, 2026-10-28

## Coordinated 0.2.0 update

The later owner request expanded this initial build to Studio 1.150.0, Open Assets 0.2.0 and Earshot 1.1.0. All three existing hosted plugins were updated and read back, with their current catalog skills readable. [Work execution](../../verification/open-assets-0.2.0-work.json) records 14 enabled providers/23 media paths and the local provenance handoff. [Hosted evidence](../../verification/open-assets-0.2.0-hosted.json) records comparison scope and retained legacy/private files. Earlier 0.1.x counts and limits below are historical. Claude/Codex and fresh-client startup remain NOT_RUN.


Change: **CW-20261028-01**. Owner trigger: create the approved FrameCore Open Assets companion with
Earshot-compatible Claude, ChatGPT and Codex construction. Baseline main:
`1ef04c02d409a2c37d5900e1e09cdfe668d25c0c`. Studio remains **1.149.0**; Earshot remains **1.0.9**.

## Delivered source

The new `plugins/framecore-open-assets` package has one portable skill, three consistent 0.1.1
manifests, a marketplace entry, a shared Python CLI, ten independent official-API adapters, eighteen
provider dossiers and offline tests. This is original code; no reviewed GitHub client is bundled.
The preceding 31-repository mapping informed the architecture, not runtime dependency installation.

The package works independently and hands asset provenance to other production owners. It does not
rewrite Studio's Openverse routing, modify Earshot or issue a Studio release. This keeps the owner's
creation request separate from the larger Studio migration described in the handover.

## Qualification and execution

Executable modules: Commons, Met, Cleveland, NASA, LibriVox, Wellcome, ambientCG, PhyloPic, Poly Haven,
and SFXMint. The remaining eight researched candidates have named policy holds in `providers.json`:
AIC, Rijksmuseum, LoC, Internet Archive, ccMixter, Finna, SMK, Gallica. Missing applicable terms and
commercial restrictions block enabling those sources; they are not an arbitrary provider cap.

NASA and LibriVox are discovery-capable but normal downloads require user-supplied item/use rights
review. SA requires deliberate acceptance; NC/ND/Unknown remain blocked. Technical-only verification
never authorizes production reuse. Source provenance is not a model/property release.

Every host uses its own local signed search and readiness state. First-file `verify` saves the actual
file and sidecar, then enables that runtime/provider/category for one day. Runtime or policy changes
invalidate the evidence. Search results cannot be edited to promote unknown rights or change URLs.
A host label is declared, not magically detected: Work evidence must never be relabelled Claude.

No public MCP server, account, API key, scraping, CAPTCHA solving, proxy/IP rotation or browser
impersonation is added. Requests use identifying User-Agent and API-specific Accept values, serial
pacing, bounded response/download sizes and times, allowlisted redirect hosts and HTTP cache rules.
No automatic retries or silent source failover. SFXMint's 20-distinct-sounds/day network limit wins
over the conservative local quota. No client media is uploaded.

## Verification

Canonical validation passed (37 owners, 1,597 unchanged Studio files). The full
`bash scripts/check_all.sh` passed: 243 Node cases (230 passed, 13 skipped) and 73 Python
suites with 850 cases (834 passed, 16 skipped). Total: 1,064 passed, 29 explicit skips, no failures.
The companion contributes 19 runtime and 4 package tests. The final live and archive results appear below.

The initial live pass exposed two implementation defects: ambientCG ZIPs also contain project files,
and PhyloPic paginated requests require an API-returned build. Fixed with regression tests: decode
raster members, validate bounded ZIP CRCs, keep project files unexecuted and explicitly unverified;
discover the current PhyloPic build before requesting a page. No protection was bypassed.

An independent offline skill exercise used the Commons fixture, a tampered Unknown-to-CC0 result,
and host-readiness scenarios. SA was refused without deliberate acceptance; altered/unsigned results
were refused before network; missing shell and unrun Claude checks were reported honestly. This is
source-guided skill validation, not an installed-client test.

## Publication and host state

Initial code was published as `47e63d272440c943378fc8e17ce8e84a5637c976` and all 72 changed
GitHub blobs matched. Private plugin `plugins_6ae19f3d08348191abb5df78a03a7d2b` was created at
release `pluginrel_6ae19f3ee31c819181df70945be5fb1d` (0.1.0). Full readback found 58 byte-identical
files and two platform-normalized manifests; it also exposed a source licence mismatch in the
Claude/Codex manifests. Version 0.1.1 aligns all declarations with the bundled Apache-2.0 licence,
with a regression assertion. Reusing the same Work state also exposed stale sentinel lock files.
OS-owned locks now release on process exit; contention, exception cleanup and abrupt exit have
offline regression coverage. The Windows locking branch is NOT_RUN. The final source was published as
`7954eb5d42a4a36a1149a2ac345ae1fb80be15c1` and all 11 correction blobs matched on readback.
The existing private plugin was updated to release `pluginrel_6ae1a2f2e3f08191a52f05377c6dfc10`
(version 0.1.1). All 60 saved files were read: 59 are byte-identical; `.codex-plugin/plugin.json`
differs only in JSON formatting and has identical parsed content. See [the hosted receipt](../../verification/framecore-open-assets-0.1.1-hosted.json). No public plugin-directory submission or sharing change is requested.

Claude CLI is absent in this execution environment. Claude Code and Claude apps provider/runtime
checks are NOT_RUN. Native Codex and ordinary ChatGPT behavior are NOT_RUN. Shared source, manifests
and local tests establish package compatibility structure, not every client's live capabilities.

### ChatGPT Work live CLI results

| Provider | Status | Search UTC | Download UTC | Rights / scope |
| --- | --- | --- | --- | --- |
| commons | PASS | 2026-10-28T07:13:08.386956+00:00 | 2026-10-28T07:13:14.882245+00:00 | review_sa |
| met | PASS | 2026-10-28T07:13:21.249766+00:00 | 2026-10-28T07:13:34.407170+00:00 | eligible |
| aic | NOT_RUN | NOT_RUN | NOT_RUN | Image licensing policy unreadable; last Work search was a Cloudflare challenge. |
| cleveland | PASS | 2026-10-28T07:13:41.474634+00:00 | 2026-10-28T07:13:47.520101+00:00 | eligible |
| rijks | NOT_RUN | NOT_RUN | NOT_RUN | Linked website terms remain unreadable; complete applicable terms review. |
| loc | NOT_RUN | NOT_RUN | NOT_RUN | General and collection rights terms remain unresolved; no-known-restrictions is not clearance. |
| nasa | PASS | 2026-10-28T07:13:54.924919+00:00 | 2026-10-28T07:14:08.055805+00:00 | review_nasa |
| archive | NOT_RUN | NOT_RUN | NOT_RUN | General terms unreadable; uploader licence claims alone do not clear recordings. |
| librivox | PASS | 2026-10-28T07:14:21.070621+00:00 | 2026-10-28T07:14:27.500479+00:00 | review_jurisdiction |
| ccmixter | NOT_RUN | NOT_RUN | NOT_RUN | Client-advertising terms unresolved and last media download denied. |
| finna | NOT_RUN | NOT_RUN | NOT_RUN | API Terms of Use unreadable; automated-use and attribution obligations Unknown. |
| wellcome | PASS | 2026-10-28T07:14:48.726733+00:00 | 2026-10-28T07:14:54.995384+00:00 | eligible |
| ambientcg | PASS | 2026-10-28T07:15:02.172976+00:00 | 2026-10-28T07:15:08.888528+00:00 | eligible |
| phylopic | PASS | 2026-10-28T07:15:22.019208+00:00 | 2026-10-28T07:15:46.666712+00:00 | eligible |
| polyhaven | PASS | 2026-10-28T07:15:53.632637+00:00 | 2026-10-28T07:16:06.408955+00:00 | eligible |
| smk | NOT_RUN | NOT_RUN | NOT_RUN | Institutional policy prose unreadable; full client rules unresolved. |
| gallica | NOT_RUN | NOT_RUN | NOT_RUN | Commercial digitized-media reuse generally requires a paid licence; outside free commercial scope. |
| sfxmint | PASS | 2026-10-28T07:16:13.843422+00:00 | 2026-10-28T07:16:23.472699+00:00 | eligible |

All times are UTC on 2026-10-28. PASS means one actual search-to-decoded-file path. Live files were marked technical-test-only, including review-gated NASA/LibriVox/SA examples, and are not commercially cleared production assets. Eight policy holds were not queried. Each request records its hypothesis, status, MIME, headers and redirects in [the HTTP/decoder evidence](../../verification/framecore-open-assets-0.1.1-work.json).

The release pass matches runtime fingerprint `e13cc982134c6c900b61883a0eb1ce7e0e316961cbe7e0d93840082f5ba54ab3`. Ten paths PASS; eight policy holds NOT_RUN. Initial and corrected passes are retained; structured-error, manifest-licence and OS-lock corrections have regression coverage and this final 0.1.1 runtime pass. No downloaded media or local signing key is committed. The 60-file archive also passed exact-byte inspection and a runtime status check from another absolute extraction path.
