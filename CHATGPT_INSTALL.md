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

The installation ends with the [complete runtime check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#final-check-at-installation). It checks all 59 components in `runtime-tools.json`, including isolated interpreters, models, CLI tools and motion libraries. Work's reported versions are references, not proof of another host or mandatory downgrades.

1. Run `python3 <plugin>/skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host chatgpt_work --json` from the saved bundle in the actual target environment. Supply additional `--python-env` or `--node-root` paths for installations outside discovery.
2. Show confirmed tools and the concrete missing/broken/Unknown list in the user's language. Before installation, state which tools will be installed, their purpose, target environments and download/admin requirements. Reuse authorization that already covers that plan; otherwise ask once for that concrete scope. A check alone authorizes no installation.
3. Preserve working versions and locks. Install only the disclosed missing components with compatible OS/architecture/Python environments where authorized and supported, then rerun the full check. `pass` confirms installation evidence. `fail`, `limited` or `unknown_host` leaves an explicit incomplete setup; `limited` does not mean Work/Claude is incapable of installation. Without execution, report Unknown rather than simulated success.

Plugin saving, tool installation and end-to-end creative behavior are separate results. No providers, generation, client-asset upload or publication is included in tool setup.

## First recommended companion: Superpowers

Right after the final check, in the same conversation and before providers or other add-ons, follow [first companion setup](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#first-companion-setup). Check whether Superpowers is already readable. Otherwise recommend it once: it supports requirements, technical plans, debugging, code review and verification while Studio keeps creative direction, boards and production ownership. The user installs it separately through the actual host Plugins/Marketplace interface; use the registry's host-specific manual steps. The upstream identity is obra/superpowers, Jesse Vincent / Prime Radiant. An official catalog listing does not mean the platform authored it.

Skipping, declining, unavailable catalog access or unverified activation leaves Studio usable. Do not install automatically, clone as a fallback, connect an account, or repeat a known decline/defer. Recheck actual readable skills after installation; saved files or the user's click do not prove activation. Preserve choices on ordinary updates. Catalog/ZIP installations can run the host's setup action where available, or explicitly ask Studio to configure its companion support. This setup path is separate from the complete bare-name welcome.

## Second recommended companion: Earshot Audio

Right after Superpowers, [first companion setup](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#first-companion-setup) explains Earshot in plain words and asks once: full (recommended, about 2.6 GB with its models), light (about 200 MB) or not now. It is the separate plugin `earshot-audio` (folder `plugins/earshot-audio`; Earshot 0.4.0 by Leon Lin, MIT): it chooses, makes and places sound effects on the film's moments and checks them against the picture, on the user's machine, uploading nothing. The user's answer is the consent; then the assistant installs the plugin and the chosen tier in the same conversation:

- ChatGPT Work with code execution: Plugin Creator creates (or updates) the `earshot-audio` plugin from the whole folder at the same pinned commit as Studio, then reads its files back. A Work sandbox may not keep the engine between conversations; Studio runs `status` again and offers the same choice.
- An ordinary ChatGPT chat without code execution cannot run it; Studio says so and names ChatGPT Work, Claude Code or Codex.

Then, from the plugin folder: `python3 scripts/runtime.py install --tier <full|light>` (the plan), the same with `--yes`, for full also `fetch-models --yes`, then `runtime.py status --json` (`ready_full` or `ready_light`). The engine is pinned and checked file by file; `llm` and `mcp` are refused. A blocked download names its host (PyPI; for full also `download.pytorch.org`, `*.pytorch.org`, `huggingface.co`, `*.huggingface.co`, `*.hf.co`) and stops. If `earshot-audio:earshot` is already readable, `status` decides what is still needed. Studio works without it.

Remove it with the host's plugin controls.

## More companions: Voice And Narration and Brand Kit

The repository carries two more separate plugins, created with Plugin Creator from the whole folder like Earshot. Studio proposes each one only when it clearly helps the user's task, and installs it only after the user agrees; the [registry](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.json) entries `voice-narration` and `brand-kit` hold the steps for this host.

- **Voice And Narration** (folder `plugins/voice-narration`, skill `voice-narration:narrate`): measured voice-overs from an approved script with VoxCPM2 or Voicebox on the user's own computer or ElevenLabs through a connector. Local engines are installed only on consent and are advised against in a cloud sandbox.
- **Brand Kit** (folder `plugins/brand-kit`, skill `brand-kit:brand`): a brand kit from a company website (colours, fonts, logo, voice and messaging) with revisions per brand and a direction plan. It needs Python 3 and reads only public pages.

Use the same pinned commit as Studio and copy the whole folder.

## 6. Offer optional providers after installation

Then read the bundled [provider setup guide](plugins/framecore-work-creative-studio/docs/provider-setup-guide.md) and [setup method](plugins/framecore-work-creative-studio/skills/tool-routing-cost/references/provider-setup.md). Offer one optional question about existing accounts, additional tools, a setup guide or skipping setup. Match the actual host and distinguish native apps from API/MCP/CLI access and billing.

After installation in ChatGPT Work, the owner's own tests used Studio both in ChatGPT Work and in ordinary ChatGPT chats, including on a phone (reports of 2026-10-07 and 2026-10-08 in `verification/`); whether every plan and account behaves the same is not verified. Which interactive elements appear in a reply depends on the client. Installation creates the user's own private Studio copy. It does not connect providers, spend credits, upload client assets, generate media, publish the copy publicly, synchronize account history or automatically apply future repository changes. Skipping provider setup leaves the Studio installation complete. On updates, preserve private preferences and do not repeat onboarding unless requested or materially needed.

## Recommended extensions

Studio's [recommended extensions](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md) are outside repositories the owner reviewed as engines or knowledge. Each states whether it runs in ChatGPT and ChatGPT Work; one that needs a local MCP server (such as REA) is not installed there, and Studio names Codex or Claude Code instead. Do not install an extension during the ChatGPT installation.

## References

- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins).
- [OpenAI: Build plugins](https://learn.chatgpt.com/docs/build-plugins).
- [Studio update instructions](CHATGPT_UPDATE.md).

The documented invocation distinction was checked on 2026-09-29. Use the current host's actual capabilities and permissions when performing installation.
