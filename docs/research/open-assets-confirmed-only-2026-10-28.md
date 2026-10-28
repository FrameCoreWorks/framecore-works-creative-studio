# Open Assets: confirmed providers only

## Bounded instruction packet

- Change: CW-20261028-08; origin: chatgpt-work.
- Baseline: `6dd0886abd98321d79341ab6d9404ba1accb5518` on main; Open Assets 0.2.0.
- Target role: Open Assets package maintenance; Hipson bounded scope/review method.
- Trigger and authorization: the owner explicitly requires complete removal of unqualified sources, without disabled entries, pointers or dormant modules, from the existing asset plugin. Resume authorized after reading the updated project knowledge.
- Goal: ship only the fourteen qualified providers and their twenty-three demonstrated Work media paths, retaining per-item rights checks and actual-host verification.
- Allowed edits: Open Assets provider registry; the four excluded provider dossiers; README, changelog, provider index and relevant skill/contract paragraphs; NASA's unused audio branch; qualification regression tests; synchronized package version markers and marketplace entry. Repository-only scope, ledger, current handover/roadmap/status and verification receipts may record the result. Correct the obsolete Plugin Creator deletion-capability statement in AGENTS.md while preserving Studio path protection.
- Exclusions: no Studio or Earshot runtime edits, startup/menu/identity changes, new provider, copied private overlay, account/key setup, retry of blocked endpoints, new remote branch, force push or history rewrite. Historical research outside the distributed plugin remains evidence, not an operational provider catalogue.
- Source rules: actual current package and hosted inventory; existing dated Work HTTP/decode evidence is historical evidence, not a fresh request. Re-decode retained samples with the candidate runtime; exercise removal and remaining integration contracts without inventing host coverage.
- Acceptance: registry/modules/dossiers are one-to-one for fourteen qualified providers; all twenty-three supported categories have observed Work search/download/decode evidence; no excluded provider entries, dossiers or links in the distributed package; NASA implements photos/video only; removed providers fail before network; rights gates and Studio/Earshot handoff remain intact; all required repository checks pass; GitHub source and existing hosted plugin are read back, including physical file absence.
- Compatibility dependency: LibriVox's reviewed, working section downloads use provider-returned `archive.org` storage URLs. Retain that delivery dependency, with no general archive search API or provider entry.
- Publication: Open Assets 0.2.1 only; Studio 1.150.0 and Earshot 1.1.0 remain unchanged. Current Plugin Creator supports explicit `delete_paths`; use exact observed file paths and the current release guard. This is an owner-authorized companion deletion, not permission to delete Studio paths.
- Output schema: delta, checks, GitHub commit, saved release/readback, limitations and next step.
- Rollback: selective revert of this change against the then-current main and guarded update of the same existing plugin; no force/reset of other work.

## Checkpoint

Implementation complete. Hosted baseline: Open Assets 0.2.0, release `pluginrel_6ae1c36dedd88191ab85a7005103cde5`; all 65 files read. Candidate 0.2.1 has 61 files, fourteen providers and twenty-three categories. Focused package/runtime/provider tests pass (4/19/7 cases). All twenty-three retained Work samples match their original hashes and decode with the candidate. Complete package text scanning finds no excluded provider names or dossier pointers; removed IDs fail before network. Extracted archive status, CLI choices and runtime fingerprint match the source. Studio/Earshot source trees are unchanged. Canonical validation and the full repository suite pass (1072 passed, 29 skipped), including the Earshot import regression. GitHub publication and full saved-plugin readback are complete, as recorded below. Implementation, publication and saved-plugin verification are complete. GitHub source CI was still running at receipt time; its run is linked in the receipt. Fresh-client startup and other-host execution remain NOT_RUN.

## Review

The diff follows the bounded packet. The four excluded sources had no executable adapters: their remaining registry entries and dossiers are removed, rather than replaced with stubs. NASA's dormant audio code is removed; confirmed photo/video mappings are unchanged. The generic fail-closed policy guard remains, with an explicit injected-invalid-policy regression instead of a vacuous loop over nonexistent held entries. The archive contains no downloaded media or operational state.

Evidence: [candidate checks and dated Work sample lineage](../../verification/open-assets-0.2.1-cleanup.json). Earlier HTTP results retain their original timestamps and technical-only rights restrictions; no fresh provider request is claimed for this cleanup. A working sample establishes the observed path, not permanent uptime or rights to every catalogue item.

## Publication and saved-plugin readback

Source commit `0ec35cfac545a5d79812f69442848534974287c0` was fast-forwarded to main after fetch/rebase; the fetched tree matches the tested local tree. The existing Open Assets plugin was updated to 0.2.1 with four explicit `delete_paths`, using its current release guard. Saved release: `pluginrel_6ae1e793e458819183183bc46e9d9859`.

Complete inventory and all 61 surviving files were read back: 60 byte-identical; the Codex manifest differs only in JSON formatting/key order, with equal parsed content. Each deleted path is absent from the complete inventory and explicitly returned as missing. Scope, audience, identity and prompts are preserved. The current catalog skill was read and contains the cleaned instructions. [Readback receipt](../../verification/open-assets-0.2.1-hosted.json). GitHub CI is tracked separately in that receipt; fresh-client startup and other-host execution remain NOT_RUN.
