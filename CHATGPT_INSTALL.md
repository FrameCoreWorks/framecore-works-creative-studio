# Install Creative Studio in ChatGPT Work

Open **Work**, select **Plugin Creator**, and paste:

```text
Use Plugin Creator to create my private FrameCore Works Creative Studio plugin from:
https://github.com/FrameCoreWorks/framecore-works-creative-studio

Read CHATGPT_INSTALL.md and config/install-sources.json. Resolve main once to a full commit and
use it for every source read. Verify the complete bundle and SHA-256 hashes. Install the full
Studio with all 37 modules, references, templates, shared resources, original source bundles and logo.

Check whether I already have this plugin. If it exists, follow CHATGPT_UPDATE.md and update the
same entry within this request; do not create a duplicate or overwrite conflicting personal edits.
For a fresh copy, use the actual Plugin Creator workflow with the canonical plugin directory.
Preserve identity, interface, starter prompts, files and relative references.

Continue in my language. This request authorizes the installation; do not repeat approval questions
for unchanged scope. After saving, read back the version and source and report the actual result.
If source access, Plugin Creator, saving or readback is unavailable, state the specific limitation.
Do not simulate installation, substitute a Codex installer, connect providers, upload client assets
or publish my copy publicly.
```

## Source and preparation

1. Pin the repository to one full immutable commit. Read this guide and the source inventory at that commit; do not mix moving-source reads.
2. Follow the active host's current Plugin Creator creation/update skill for saving, identity checks and permissions. Do not invent an install function or assume regular Chat exposes Work capabilities.
3. Discover an existing matching plugin before creation. Read its actual files, not only its name. Updates use the exact backend ID and current release guard.
4. Fetch every file in the inventory, including binary assets and source archives. Verify SHA-256 and the complete path set. Missing bytes or unavailable hashing must be reported; do not omit files or label an unverified copy verified.
5. Package exactly the canonical `plugins/framecore-work-creative-studio` directory in the format Plugin Creator accepts. Preserve both manifests, the complete starter prompt value/order, logo, all skill roots and nested resources. Do not flatten the bundle or recreate only the SKILL.md text.
6. Reuse current installation authorization. Ask only about material conflicts or scope choices. User onboarding is optional after saving; do not import the author's private preferences.

## Save and verify

Use the actual creation operation and retain its returned plugin and release IDs. Read back identity,
version, interface, asset references and accessible source. A successful save and complete byte readback
are separate evidence; report any readback limit. On an ambiguous response inspect actual saved state
before retrying, rather than making another copy.

This creates the user's own private plugin. Public repository access does not share the author's
hosted entry or synchronize later edits. Use [CHATGPT_UPDATE.md](CHATGPT_UPDATE.md) for updates.
No provider connection, media generation or external client-data transfer is part of installation.

Package format reference, checked 2026-09-29: [OpenAI, Package your plugin](https://developers.openai.com/plugins/build/plugins). Preserve the portable root manifest and complete skills directory. Use the current host's actual private creation capability, not an assumed public directory listing.
