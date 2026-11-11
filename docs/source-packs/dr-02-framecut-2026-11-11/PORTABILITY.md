# DR-02 portability and preservation record

The frozen original research was read only. Original Polish authored reports, source ledgers, examples, recipes, glossary, QA, benchmarks, backlog and handoff are preserved in full. Unmodified files retain byte identity. Every original file has an explicit disposition and original SHA-256 in EXPORT-MANIFEST.json; every exported source-derived file also has its exported hash and adaptation list. The original prompt and original verifier are unmodified.

## Exactly what changed

Private absolute research/cache/PDF paths become explicit labels. Installed-cache relative file identities and reported hashes remain. The local official Resolve SDK document N08 uses `urn:dr02:local-evidence:N08:resolve-sdk-readme-2025-08-18` instead of a machine file URL; its title, dated snapshot, section locator and original SHA remain. This URN is deliberately not a web URL or a claim that its underlying document is bundled. JSON and CSV receive the same substitutions. No substantive craft claim, test result, current/proposed distinction or source pin was rewritten.

CURRENT-STUDIO.md explicitly explains the omission of downloaded inspection copies. Public URLs for those six copies were derived only from their exact repository paths, pinned commit and github_sha256 in the original 14-file comparison, independently reconfirmed through the pinned GitHub source. The six saved inspection copies each add one trailing LF to that upstream content; both the saved-copy and public-content hashes are recorded. No private installation path was blindly translated into a public source URL.

## Exclusions

The full exclusion list is in EXPORT-MANIFEST.json: historical dated backups and six fetched Studio source/schema/README inspection snapshots. The latter have exact replacements in SOURCE-SNAPSHOT-REFERENCES.json. They are not authored research, installed runtime, or a runnable product package. The redacted historical 14-file comparison remains under specialists/repo/evidence/.

Raw third-party manuals, downloaded web/PDF bodies, training media, cache contents, credentials and other private host data are not shipped. The author kept large manuals in temporary storage outside the original research folder; their absence here is not a claim that they were fully read or that redistribution rights exist. No original source or backup was deleted.

## Review and verification history

REVIEW.md and specialists/review/REVIEW.md retain PASS_WITH_LIMITATIONS and the closed findings. VERIFICATION-RESULT.json retains the original 1597-check research result. HIPSON-HISTORICAL-RECEIPT.json is an explicitly sanitized transcription of the read-only observed completed T-0004 gate. Its fingerprint and timestamps refer to the frozen original. Historical reviewer hashes, source snapshots and Hipson evidence do not automatically certify the exported bytes or future product changes.

The original verifier is portable without a source change. The separate new verify_portable.py checks this edition and calls that unmodified script. It does not run imported product code, fetch URLs or require installed media tools. Newly generated PORTABLE-VERIFICATION.json records export-check output and is explicitly outside the manifest's hash set to avoid a self-referential receipt; the manifest itself likewise cannot hash itself. All other shipped files are hashed. A future independent run should compare the actual output, not reuse a recorded PASS.

All native/runtime/render/view/listen/round-trip and full external-schema limits remain NOT_RUN. The six HTTP403 availability results remain unchanged in meaning. Publication, applicability analysis, implementation, knowledge preservation and cleanup are distinct stages; this packet completes only the research transfer stage.
