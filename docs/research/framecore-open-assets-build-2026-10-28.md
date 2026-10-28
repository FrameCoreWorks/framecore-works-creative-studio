# FrameCore Open Assets: build and verification, 2026-10-28

Change: **CW-20261028-01**. Owner trigger: create the approved FrameCore Open Assets companion with
Earshot-compatible Claude, ChatGPT and Codex construction. Baseline main:
`1ef04c02d409a2c37d5900e1e09cdfe668d25c0c`. Studio remains **1.149.0**; Earshot remains **1.0.9**.

## Delivered source

The new `plugins/framecore-open-assets` package has one portable skill, three consistent 0.1.0
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
suites with 848 cases (832 passed, 16 skipped). Total: 1,062 passed, 29 explicit skips, no failures.
The companion contributes 17 runtime and 4 package tests. The final live and archive results appear below.

The initial live pass exposed two implementation defects: ambientCG ZIPs also contain project files,
and PhyloPic paginated requests require an API-returned build. Fixed with regression tests: decode
raster members, validate bounded ZIP CRCs, keep project files unexecuted and explicitly unverified;
discover the current PhyloPic build before requesting a page. No protection was bypassed.

An independent offline skill exercise used the Commons fixture, a tampered Unknown-to-CC0 result,
and host-readiness scenarios. SA was refused without deliberate acceptance; altered/unsigned results
were refused before network; missing shell and unrun Claude checks were reported honestly. This is
source-guided skill validation, not an installed-client test.

## Publication and host state

Repository publication and private Plugin Creator save/readback are pending until performed. The task
reply records exact commit/plugin/release identifiers. A new private plugin is authorized; no public
plugin-directory submission or sharing change is requested.

Claude CLI is absent in this execution environment. Claude Code and Claude apps provider/runtime
checks are NOT_RUN. Native Codex and ordinary ChatGPT behavior are NOT_RUN. Shared source, manifests
and local tests establish package compatibility structure, not every client's live capabilities.

### ChatGPT Work live CLI results

| Provider | Status | Search UTC | Download UTC | Rights / scope |
| --- | --- | --- | --- | --- |
| commons | PASS | 2026-10-28T06:56:29.978263+00:00 | 2026-10-28T06:56:34.503053+00:00 | review_sa |
| met | PASS | 2026-10-28T06:56:41.163084+00:00 | 2026-10-28T06:56:50.119043+00:00 | eligible |
| aic | NOT_RUN | NOT_RUN | NOT_RUN | Image licensing policy unreadable; last Work search was a Cloudflare challenge. |
| cleveland | PASS | 2026-10-28T06:56:55.150154+00:00 | 2026-10-28T06:57:00.008398+00:00 | eligible |
| rijks | NOT_RUN | NOT_RUN | NOT_RUN | Linked website terms remain unreadable; complete applicable terms review. |
| loc | NOT_RUN | NOT_RUN | NOT_RUN | General and collection rights terms remain unresolved; no-known-restrictions is not clearance. |
| nasa | PASS | 2026-10-28T06:57:04.634272+00:00 | 2026-10-28T06:57:13.915928+00:00 | review_nasa |
| archive | NOT_RUN | NOT_RUN | NOT_RUN | General terms unreadable; uploader licence claims alone do not clear recordings. |
| librivox | PASS | 2026-10-28T06:57:22.840586+00:00 | 2026-10-28T06:57:26.873234+00:00 | review_jurisdiction |
| ccmixter | NOT_RUN | NOT_RUN | NOT_RUN | Client-advertising terms unresolved and last media download denied. |
| finna | NOT_RUN | NOT_RUN | NOT_RUN | API Terms of Use unreadable; automated-use and attribution obligations Unknown. |
| wellcome | PASS | 2026-10-28T06:57:42.229930+00:00 | 2026-10-28T06:57:46.422818+00:00 | eligible |
| ambientcg | PASS | 2026-10-28T06:57:51.248355+00:00 | 2026-10-28T06:57:56.077926+00:00 | eligible |
| phylopic | PASS | 2026-10-28T06:58:05.385362+00:00 | 2026-10-28T06:58:23.843122+00:00 | eligible |
| polyhaven | PASS | 2026-10-28T06:58:29.582141+00:00 | 2026-10-28T06:58:38.279119+00:00 | eligible |
| smk | NOT_RUN | NOT_RUN | NOT_RUN | Institutional policy prose unreadable; full client rules unresolved. |
| gallica | NOT_RUN | NOT_RUN | NOT_RUN | Commercial digitized-media reuse generally requires a paid licence; outside free commercial scope. |
| sfxmint | PASS | 2026-10-28T06:58:43.560528+00:00 | 2026-10-28T06:58:50.727929+00:00 | eligible |

All times are UTC on 2026-10-28. PASS means one actual search-to-decoded-file path. Live files were marked technical-test-only, including review-gated NASA/LibriVox/SA examples, and are not commercially cleared production assets. Eight policy holds were not queried. Each request records its hypothesis, status, MIME, headers and redirects in [the HTTP/decoder evidence](../../verification/framecore-open-assets-0.1.0-work.json).

The release pass matches runtime fingerprint `d1c382dcae0cdf5f06ccf23337e19ed9da5b8c4045d20ab54fb1d9ccff68796b`. Ten paths PASS; eight policy holds NOT_RUN. Initial and corrected passes are retained; a final structured-error-boundary correction was verified by an offline regression and a release-runtime pass. No downloaded media or local signing key is committed. The 60-file archive also passed exact-byte inspection and a runtime status check from another absolute extraction path.
