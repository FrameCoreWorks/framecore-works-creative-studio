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
Preserve private provider preferences. Do not repeat optional setup unless requested or needed
for a changed selected route. Studio updating does not authorize new provider connections.
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
