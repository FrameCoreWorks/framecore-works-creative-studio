# Install Creative Studio in ChatGPT Work

This is the complete direct-source procedure for the assistant performing a user-requested installation in ChatGPT Work. Read it before fetching or saving the Studio package. Codex local installations follow [CODEX_INSTALL.md](CODEX_INSTALL.md).

## 1. Confirm intent and host capabilities

1. Use the user's explicit installation request as authorization for the described private Studio installation. Do not ask again for unchanged scope. A bare repository link without installation intent is source context; clarify the intended action before saving a plugin.
2. In ChatGPT Work, select **Plugin Creator** from the `@` menu. The documented invocation is `@plugin-creator`; pasted text alone does not prove that its tools are available. If the assistant can use an already available Plugin Creator capability, use it directly. Otherwise explain the required selection.
3. Follow the active host's current Plugin Creator creation/update workflow and actual permissions. Do not invent an installation operation, substitute the Codex local installer, or assume an ordinary Chat session exposes creation/save capabilities.
4. Continue in the user's language, including the complete startup welcome and later menus. Apply the automatic language policy in Workflow Orchestrator; English repository documentation and localized examples do not set a fixed response language.

## 2. Pin and verify the complete source

Source repository: <https://github.com/FrameCoreWorks/framecore-works-creative-studio>.

1. Resolve the requested release or, by default, `main` once to a full immutable Git commit. Use that same commit for this guide, all source files and the inventory; do not mix reads from moving refs.
2. Read [config/install-sources.json](config/install-sources.json) at that commit. Fetch every declared file, including binary assets and pinned source archives. Verify SHA-256 hashes and the complete path set.
3. Retain the canonical `plugins/framecore-work-creative-studio` structure. The full bundle contains all 37 skill roots, references, templates, shared resources, original source bundles, both manifests and the logo. Preserve relative references, identity, interface metadata and starter prompt values/order.
4. If source access, hashing or required bytes are unavailable, report the specific limitation. Do not omit resources, reconstruct only skill text or describe an incomplete copy as verified.

## 3. Handle an existing installation

1. Check for an existing matching Studio plugin before creation. Identify it from actual metadata and files, not its name alone.
2. If it exists, follow [CHATGPT_UPDATE.md](CHATGPT_UPDATE.md) and update the same entry within the authorized request. Preserve personal changes and inspect material conflicts before replacing them. Do not create a duplicate.
3. Use the exact backend plugin ID and current release guard returned by the host. Preserve the existing identity, scope and audience. The author's private hosted plugin is not the user's installation target.

## 4. Save and read back

1. Package exactly the canonical plugin directory in the format accepted by the active Plugin Creator workflow. Use the actual private creation operation for a fresh copy or the guarded update operation for an existing one.
2. Retain the returned plugin and release IDs. After saving, read back identity, version, interface, asset references and accessible source. Compare the complete saved package with the verified source when archive access permits.
3. Treat a successful save, file-byte verification and active-client discovery/startup as separate evidence. Report any unreadable files or unavailable host test; never claim observed activation from a source read alone.
4. On an ambiguous response, inspect the saved state before retrying so a second copy is not created. Report a concrete blocker if saving or readback cannot complete.

## 5. Final check of the required tools

The installation ends with the [final check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#final-check-at-installation). Studio uses one required set of tools (Python with Pillow, NumPy, CairoSVG, imageio-ffmpeg, matplotlib and Manim; FFmpeg with FFprobe; Node.js with npx; Chrome or Chromium; the five starters installed with `npm ci` in the Studio workspace; HyperFrames); the check decides which of them this host can run.

1. Run `python3 skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host chatgpt_work` from the saved plugin in the conversation's code execution (`--host chatgpt` in ordinary ChatGPT) and show the user the result in their language.
2. `pass`: the installation is complete. `limited`: the plugin is installed, but this chat sandbox lacks tools the user cannot add there; name them and say that Studio uses the capability card's alternatives (for example the bundled renderer instead of Remotion or HyperFrames). Tools a chat sandbox cannot run at all are listed as not on this host and do not count.
3. For the full required set, install Studio also where code runs on the user's machine (Codex or Claude Code) and run the final check there.

Installing these tools does not connect providers, generate media, spend credits or publish anything.

## 6. Offer optional providers after installation

Then read the bundled [provider setup guide](plugins/framecore-work-creative-studio/docs/provider-setup-guide.md) and [setup method](plugins/framecore-work-creative-studio/skills/tool-routing-cost/references/provider-setup.md). Offer one optional question about existing accounts, additional tools, a setup guide or skipping setup. Match the actual host and distinguish native apps from API/MCP/CLI access and billing.

After installation in ChatGPT Work, the owner's own tests used Studio both in ChatGPT Work and in ordinary ChatGPT chats, including on a phone (reports of 2026-10-07 and 2026-10-08 in `verification/`); whether every plan and account behaves the same is not verified. Which interactive elements appear in a reply depends on the client. Installation creates the user's own private Studio copy. It does not connect providers, spend credits, upload client assets, generate media, publish the copy publicly, synchronize account history or automatically apply future repository changes. Skipping provider setup leaves the Studio installation complete. On updates, preserve private preferences and do not repeat onboarding unless requested or materially needed.

## References

- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins).
- [OpenAI: Build plugins](https://learn.chatgpt.com/docs/build-plugins).
- [Studio update instructions](CHATGPT_UPDATE.md).

The documented invocation distinction was checked on 2026-09-29. Use the current host's actual capabilities and permissions when performing installation.
