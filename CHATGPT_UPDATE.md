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
Build the update from files read as text, as in "No-ZIP update route" of CHATGPT_UPDATE.md: never
download the release ZIP, never ask me to attach or upload a file, and do not stop for one.
Use the actual host update workflow, read back the result and report version, release and
verification limits. On a lost response, inspect saved state before retrying.
Do not change sharing, provider connections, project data or unrelated behavior.
Write the declared files exactly as published: never merge private provider preferences, connection
details or personal notes into the plugin's skill or reference files. Do not repeat optional setup unless requested or needed
for a changed selected route. Studio updating does not authorize new provider connections.
After saving, run the update check of the required tools from the saved plugin in code execution:
python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --update --host chatgpt_work
and show me its verdict and the tools this chat cannot run.
Then follow Studio's companion check after an update (skills/workflow-orchestrator/references/extensions.md#companion-check-after-an-update):
if FrameCore Works Toolbox or FrameCore Open Assets is missing here, offer to install them in this chat and do it on my yes.
```

## No-ZIP update route

Owner decision 2026-10-29: the update runs on its own, without a release ZIP and without the owner attaching
anything. What ChatGPT Work's tools allow (attempts of 2026-10-30): Plugin Creator's `create_plugin` and
`update_plugin` take only `archive`, an absolute path to a ZIP in code execution (a data URL is refused with
`INVALID_ARGUMENT`); code execution has no network; the GitHub connector returns file text to the model but writes
no file into code execution. So the model writes each changed file's text into code execution, checks it against
the inventory and zips it there:

1. Resolve `main` (or the requested release) to one full commit and read `config/install-sources.json` at it
   (NEW). Read the same file at the tag of the saved version, for example `v1.150.0` (OLD); when the saved version
   has no tag, the baseline is unknown: delete nothing and review every difference.
2. Hash the saved plugin in code execution and compare it three ways with OLD and NEW: write every path whose NEW
   hash differs from the saved one and that the saved copy has not edited privately (saved equals OLD, or the path
   is new); delete exactly the paths that are in OLD, not in NEW and unchanged here; keep private overlays and
   private-only files untouched; merge by hand a path edited here that also changed upstream.
3. Read each path to write from `plugins/framecore-work-creative-studio/<path>` at the pinned commit through the
   connector and write its exact text under `/mnt/data/studio/<path>` (`pathlib.Path(...).write_text(text,
   encoding='utf-8')`; a long file in several appending cells), keeping every character and the final newline.
   Write `/mnt/data/expect.json` as {path: sha256} for those files, copied from NEW. Binary package files rarely
   change (none between 1.140.0 and 1.157.0); if one did, report it rather than guess its bytes.
4. Check and zip in one cell; it writes the ZIP only when every file matches:

   ```python
   import hashlib,json,pathlib,zipfile
   R=pathlib.Path('/mnt/data/studio');E=json.load(open('/mnt/data/expect.json'))
   bad=[p for p,h in E.items() if not (R/p).is_file() or hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
   print('BAD',bad) if bad else print('OK',len(E))
   if not bad:
       with zipfile.ZipFile('/mnt/data/studio.zip','w',zipfile.ZIP_DEFLATED) as z:[z.write(R/p,p) for p in sorted(E)]
   ```

   For each path in `BAD`, read the file again from the connector and rewrite it unchanged; never patch it by guess.
5. `update_plugin(archive="/mnt/data/studio.zip")` with the delete paths under the current release guard. The update
   overlays the saved release, so omitted files, including the private overlay, stay as they are. Read back the
   affected files, confirm the deleted paths are absent, then run the update check below.

For 1.150.0 to 1.156.0 this writes 82 files (68 changed, 14 new) and deletes 10, about 0.45 MB of text; a usual
release changes a handful of files. Hosted run: NOT_RUN until Work performs it. Where code execution can read the
whole repository (a host with network), `scripts/hosted_update.py plan` and `pack` build the same archive directly.

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
