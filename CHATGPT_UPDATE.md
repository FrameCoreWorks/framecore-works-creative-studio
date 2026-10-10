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

Preserve canonical identity, interface, prompt values/order and existing components. Use a permitted
greater version for a real update and recheck release drift before submission. Refresh the comparison
if source or access changed.

After success read back affected files and metadata. Report save success separately from incomplete
verification. Repository publication and hosted updating remain separate operations.

Finish with the [update check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#update-check-after-a-plugin-update) of the required tools (`--update --host chatgpt_work`, or `--host chatgpt` in ordinary ChatGPT). In the chat sandbox it reports `pass`, `pass_with_updates` or `limited` (tools that sandbox lacks, which the user cannot install there); for the full required set, run the same check where Studio is installed on the user's machine.

## Readback record (optional)

Owner decision 2026-10-10: hosted readbacks are no longer requested and ChatGPT Work is recorded as `not_tracked`; the
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
