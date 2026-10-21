# Update the existing ChatGPT Work plugin

In **Work**, type `@`, search for **Plugin Creator**, and select it from the menu. Paste the complete prompt below with that selection attached. If the pasted invocation is only plain text, select Plugin Creator through the menu before sending.

```text
@plugin-creator

Use Plugin Creator to update my existing FrameCore Works Creative Studio from:
https://github.com/FrameCoreWorks/framecore-works-creative-studio

Read CHATGPT_UPDATE.md and config/install-sources.json. Identify my exact plugin and read its
current source and release ID. Resolve main once to a full commit, verify all declared source
files and compare the complete proposed update with my actual installation.
Preserve identity, starter prompts, logo, integrations and personal additions. Apply the requested
upstream changes to the same plugin using the current release guard. This request authorizes
the update; ask only about a material conflict or changed scope. Do not create duplicates.
If already current, report that without saving.
Use the actual host update workflow, read back the result and report version, release and
verification limits. On a lost response, inspect saved state before retrying.
Do not change sharing, provider connections, project data or unrelated behavior.
Write the declared files exactly as published: never merge private provider preferences, connection
details or personal notes into the plugin's skill or reference files. Do not repeat optional setup unless requested or needed
for a changed selected route. Studio updating does not authorize new provider connections.
After saving, run the update check of the required tools from the saved plugin in code execution:
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --update --host chatgpt_work
and show me its verdict and the tools this chat cannot run.
```

Follow the active Plugin Creator update skill. Compare previous verified source, actual saved
content and pinned new source. If the old baseline is unknown, say `baseline_unknown`; names
alone do not establish provenance. Preserve personal additions and resolve overlapping edits.

Overlay updates may preserve omitted files and may not support deletion. Absence upstream is
not proof of hosted deletion. Report that limitation rather than creating a replacement plugin.

For an explicit owner-requested connection removal, inspect the current installed declarations,
remove their owning references, and use exact `delete_paths` when the active update tool supports
them. Verify deletion against the complete saved inventory. Such a removal supersedes the old
connection-preservation instructions for that connection only; retain unrelated App bindings,
runtimes and credentials. Do not restore a retired connection from an older overlay or archive.

Owner decision 2026-10-21: remove the private Sunra MCP configuration. The public source at
`96f8e97a160c22dcd1d359cf708aedaa7c58013b` contains no Sunra MCP configuration. Preserve that
absence during future source merges. The separate API route and other private integrations
are outside this removal. See the dated record in `docs/development-ledger.md`.

Preserve canonical identity, interface, prompt values/order and existing components. Use a permitted
greater version for a real update and recheck release drift before submission. Refresh the comparison
if source or access changed.

After success read back affected files and metadata. Report save success separately from incomplete
verification. Repository publication and hosted updating remain separate operations.

Finish every update with the [complete runtime check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#update-check-after-a-plugin-update), using `--update` and the actual host. It repeats all 59 components offline, including models and isolated Python/Node environments. Show missing/broken/Unknown findings and the concrete installation plan before executing it under existing scope authorization. Preserve working versions and private runtimes; a different reference version is not an automatic upgrade. Recheck afterward. `pass` confirms installation evidence; all other verdicts remain explicitly incomplete. Without execution, report Unknown. Saving the plugin alone is not proof its tools are installed.

## Readback record (optional)

Owner decision 2026-10-20 supersedes the historical procedure below: use the current hosted release as the guarded baseline, preserve the private integrations maintained by the separate integrations thread, apply the verified public-source changes, and read back the affected files. Record the public source version and hosted version separately when the private overlay has a newer version. Never replace newer integrations with an older public snapshot or publish private configuration to GitHub.

Historical owner decision 2026-10-10: hosted readbacks were no longer requested and ChatGPT Work was recorded as `not_tracked`; the
owner tests the plugin himself. The procedure below stays available when someone wants a byte-level comparison.

After the update, ask Plugin Creator in the same chat to read the saved plugin back and write one JSON file with:
`version` (from the saved `plugin.json`), `date`, `plugin_id`, `release_id`, `scope`, `audience`, `source_commit` (the
pinned commit), `inventory` (every saved path with `size_bytes`), `files` (`path` and `sha256` for every file it could
read) and `unreadable` (the paths it could not read). Do not fill a hash it did not compute.

In the repository, `python3 scripts/check_hosted_readback.py <file> --record verification/hosted-release-<version>.json`
compares that file with `config/install-sources.json` of the release and writes the record. `full_byte_parity` means every
path, size and hash matches; `path_size_parity` means paths and sizes match and every given hash matches, with some
files not hashed; `mismatch` lists what differs. Extra saved paths are listed, not failed: an overlay update keeps
files it cannot delete, and the user may add their own. Only a parity verdict lets the records call ChatGPT Work
`synchronized`; a save without this readback stays `pending`.
