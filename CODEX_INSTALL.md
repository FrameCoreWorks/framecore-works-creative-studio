# Install Creative Studio in Codex

This is the complete native direct-source procedure for the assistant performing a user-requested installation in Codex with filesystem access. ChatGPT Work installations follow [CHATGPT_INSTALL.md](CHATGPT_INSTALL.md).

## Paste this prompt

The simplest route, for anyone who has never used a terminal (owner request 2026-10-30): paste the repository link into the agent with one sentence, in any language. The same sentence works in ChatGPT Work, Codex and Claude Code (desktop, web, cloud or phone):

```text
Install FrameCore Works Creative Studio for me from
https://github.com/FrameCoreWorks/framecore-works-creative-studio
Read its installation guide for this app first, then explain each step in plain words.
```

In Polish: „Zainstaluj mi FrameCore Works Creative Studio z https://github.com/FrameCoreWorks/framecore-works-creative-studio. Najpierw przeczytaj jego instrukcję instalacji dla tej aplikacji, potem wytłumacz krok po kroku, co robisz.” The request is the installation consent. The assistant then follows this guide by itself: it says in one plain sentence what each step does before doing it, shows no command unless asked, asks only where this guide asks, and after installing runs the first
companion setup in the same conversation (Open Assets first, then Toolbox with a numbered list to pick from). Users who prefer the terminal follow the numbered sections below.

## 1. Confirm intent and host capabilities

1. Use the user's explicit installation request as authorization for the described local Studio installation. Do not ask again for unchanged scope. A bare repository link without installation intent is source context; clarify the intended action before writing an installation.
2. Resolve the actual Codex host, filesystem access and supported skill locations. Use Plugin Creator for package checks when available; its documented Codex invocation is `$plugin-creator`, selected from completion. Pasted text alone does not establish availability.
3. The native helper below does not depend on Plugin Creator. If that capability is absent, report it and continue with the supported local route. Do not create a hosted plugin copy, register a plugin catalog or claim a connector was enabled.
4. Continue in the user's language, including the complete startup welcome and later menus. Apply the automatic language policy in Workflow Orchestrator; English repository documentation and localized examples do not set a fixed response language.

## 2. Pin and verify the complete source

Source repository: <https://github.com/FrameCoreWorks/framecore-works-creative-studio>.

1. Resolve the requested release or, by default, `main` once to a full immutable Git commit. Obtain an exact temporary checkout/archive. Use the same commit for this guide, source reads and [config/install-sources.json](config/install-sources.json).
2. Fetch every declared file, including binary assets and pinned source archives. Verify the complete path set and SHA-256 hashes. Inspect [scripts/install_codex.py](scripts/install_codex.py) before execution. Python 3 is required; the helper uses only the standard library and makes no network requests.
3. Keep all 37 modules, references, templates, shared resources, source bundles and the logo together. A generic installer copying one specialist folder breaks cross-folder dependencies.

## 3. Resolve destinations and existing content

1. Follow the observed host's actual skill-installation rules. OpenAI documents repository `.agents/skills` and user `~/.agents/skills`; managed installers may use other destinations. Do not assume a path merely from the client name.
2. Inspect every active scope for an existing Studio plugin, native entry or overlapping Workflow Kit skills. The helper checks only its selected destination. For existing, changed, partial or ambiguous content, follow [CODEX_UPDATE.md](CODEX_UPDATE.md); preserve personal edits and avoid duplicates.
3. Select a persistent bundle directory outside **every** active skill-discovery root. Do not place the bundle in a user's project unless that scope was requested. A transient checkout is preparation, not a persistent installation destination.
4. Show the resolved native-entry and bundle destinations, then proceed under the existing installation authorization. Ask only about material unresolved scope or conflicts.

## 4. Install one entry and verify

The helper creates one native skill named `framecore-work-creative-studio` backed by the complete bundle outside skill discovery. Codex reads the original orchestrator and specialists from their canonical locations; the nested modules remain supporting instructions, not separately installed personal skills. This preserves relative references and avoids a second orchestrator.

The assistant fills these placeholders with verified absolute paths and the same full source commit. The user does not need to run the commands:

```sh
python3 scripts/install_codex.py plan --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
python3 scripts/install_codex.py install --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
python3 scripts/install_codex.py verify --skills-dir "<observed-skills-dir>" --bundle-dir "<persistent-bundle-dir>" --source-commit "<full-commit>"
```

1. Run `plan`, inspect the destinations and source checks, then run `install` and `verify` sequentially.
2. The helper repeats inventory checks, rejects symlinks, unsafe overlaps, partial installations and conflicts, saves a receipt next to the entry and verifies every bundle file. A byte-identical repeat reports read-only `already_up_to_date`. Changed source or personal edits require the update guide.
3. On a copy failure, inspect the actual entry, bundle and receipt before recovery. Report partial state; never blindly delete or overwrite an existing installation.
4. Report saved-file verification separately from actual host discovery/invocation. If activation is unobserved, say so; a new turn or refreshing the skills view may be needed. Check an ordinary Studio invocation when the host permits it, preserving the full canonical welcome contract.

This installs the same Studio knowledge through a local native entry. It does not install the hosted ChatGPT UI, a provider, a persistent agent roster or unrelated project configuration, and it does not synchronize history, preferences or connections.

## 5. Final check of the required tools

The installation ends with the [complete runtime check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#final-check-at-installation). It checks all 59 components in `runtime-tools.json`, including isolated interpreters, models, CLI tools and motion libraries. Work's reported versions are references, not proof of another host or mandatory downgrades.

1. Run `python3 <plugin>/skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host codex --json` from the saved bundle in the actual target environment. Supply additional `--python-env` or `--node-root` paths for installations outside discovery.
2. Show confirmed tools and the concrete missing/broken/Unknown list in the user's language. Before installation, state which tools will be installed, their purpose, target environments and download/admin requirements. Reuse authorization that already covers that plan; otherwise ask once for that concrete scope. A check alone authorizes no installation.
3. Preserve working versions and locks. Install only the disclosed missing components with compatible OS/architecture/Python environments where authorized and supported, then rerun the full check. `pass` confirms installation evidence. `fail`, `limited` or `unknown_host` leaves an explicit incomplete setup; `limited` does not mean Work/Claude is incapable of installation. Without execution, report Unknown rather than simulated success.

Plugin saving, tool installation and end-to-end creative behavior are separate results. No providers, generation, client-asset upload or publication is included in tool setup.

## After installation: Open Assets, then Toolbox

Right after the final check, in the same conversation and before providers or other add-ons, follow [first companion setup](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#first-companion-setup). It is the same on every host (owner request 2026-10-30), in plain words for a user who knows nothing about plugins:

1. **FrameCore Open Assets** (repository [FrameCoreWorks/framecore-open-assets](https://github.com/FrameCoreWorks/framecore-open-assets)): the assistant explains that it finds free photos, videos, music and sound effects from legal sources and downloads them with their licence and author note, so Studio builds from real material a client may use, and asks once: add it (recommended) or not now. On yes it installs it through this host's route (section FrameCore Open Assets below).
2. **FrameCore Works Toolbox** (repository [FrameCoreWorks/framecore-works-toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox), folder `plugins/toolbox`): the assistant says it is adding Toolbox, the catalog of tools FrameCore Works recommends plus Earshot for sound, installs it, and shows one numbered list: Studio's own add-ons first (Superpowers, Voice And Narration, Brand Kit), then the Toolbox catalog in two groups, **works right away in a session** (chat, cloud, phone) and **needs your computer** (programs, libraries or a separate app). Each item says what it is and how it improves Studio. The user answers with numbers; only those are installed, one by one, each reported as installed, waiting for the user's step, or not available on this host.
3. **Earshot**, only when picked from the list (section below), then the startup-style question, then a one-line "done" with how to start.

Superpowers (obra/superpowers, Jesse Vincent / Prime Radiant) is one item of that list: the user installs it through the host's own plugin catalog with the registry's steps; an official catalog listing does not mean the platform authored it. Skipping or declining anything leaves Studio usable; a decline is not repeated. Recheck actual readable skills after installation; saved files or the user's click do not prove activation. Catalog/ZIP installations can run the host's setup action where available, or ask Studio to configure its companion support. This setup path is separate from the complete bare-name welcome.

## Earshot in FrameCore Works Toolbox (when picked from the list)

When the user picks Earshot from the setup list, [first companion setup](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#first-companion-setup) explains it in plain words and asks once: full (recommended, about 2.6 GB with its models), light (about 470 MB) or not now. Earshot (0.4.0 by Leon Lin, MIT) is built into the standalone plugin FrameCore Works Toolbox (`toolbox`, repository [FrameCoreWorks/framecore-works-toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox), folder `plugins/toolbox`); there is no separate Earshot plugin. It chooses, makes and places sound effects on the film's moments and checks them against the picture, on the user's machine, uploading nothing. Studio asks it through the [companion contract](plugins/framecore-work-creative-studio/skills/pipeline-core/references/companion-routing.md) and never runs the engine itself. The user's answer is the consent; then the assistant installs the chosen tier in the same conversation (Toolbox itself was added in the step above):

- Codex: follow Toolbox's `CODEX_INSTALL.md` at a resolved commit (`scripts/install_codex.py plan`, `install`, `verify`); it creates one native `toolbox` entry with Earshot inside (not yet tested in a live Codex client).

Then, from the Toolbox plugin folder: `python3 capabilities/earshot/scripts/runtime.py status --json` first (it lists any existing runtime under `candidates`; nothing is selected for the user), `python3.12 capabilities/earshot/scripts/runtime.py install --tier <full|light>` (the plan), the same with `--yes`, for full also `fetch-models --yes` (or `fetch-models --from <root> --yes` to reuse models from a runtime the user picked), then `status --json` again (`ready_full` or `ready_light`). The engine is pinned and checked file by file; `llm` and `mcp` are refused. A blocked download names its host (PyPI; for full also `download.pytorch.org`, `*.pytorch.org`, `huggingface.co`, `*.huggingface.co`, `*.hf.co`) and stops. If `toolbox:toolbox` is already readable, `status` decides what is still needed. Studio works without it.

### Moving from Earshot Audio

The separate `earshot-audio` plugin (in Studio's marketplace up to 1.151.0 and in Toolbox 1.0.x) is retired; no Studio route uses it. Install Toolbox first, then remove the old plugin only when the user agrees (its native entry, after checking its receipt). Its engine folder `~/.framecore-studio/extensions/earshot` is not deleted: Toolbox lists it under `candidates`, and a new locked root can reuse its models with `fetch-models --from`.

Remove (only on request): the helper has no removal step (it offers `plan`, `install` and `verify`); check the entry's `installation.json` receipt and any local edits, then delete the verified `toolbox` entry and its bundle as Toolbox's `CODEX_INSTALL.md` describes, and the engine root (default `~/.framecore-works/earshot`) only if the user asks for it too.

## More companions: Voice And Narration and Brand Kit

The repository carries two more separate plugins, each with `.codex-plugin/plugin.json`. Studio proposes each one only when it clearly helps the user's task, and installs it only after the user agrees; the [registry](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.json) entries `voice-narration` and `brand-kit` hold the steps for this host.

- **Voice And Narration** (folder `plugins/voice-narration`, skill `voice-narration:narrate`): measured voice-overs from an approved script with VoxCPM2 or Voicebox on the user's own computer or ElevenLabs through a connector. Local engines are installed only on consent and are advised against in a cloud sandbox.
- **Brand Kit** (folder `plugins/brand-kit`, skill `brand-kit:brand`): a brand kit from a company website (colours, fonts, logo, voice and messaging) with revisions per brand and a direction plan. It needs Python 3 and reads only public pages.

Use the same pinned commit as Studio and copy the whole folder.

## 6. Offer optional providers after installation

Then read the bundled [provider setup guide](plugins/framecore-work-creative-studio/docs/provider-setup-guide.md) and [setup method](plugins/framecore-work-creative-studio/skills/tool-routing-cost/references/provider-setup.md). Offer one optional question about existing accounts, additional tools, a setup guide or skipping setup. Match the actual host and distinguish native apps from API/MCP/CLI access and billing.

Installation does not connect providers, modify unrelated settings, generate media, spend credits, upload client assets or publish anything. Skipping provider setup leaves the Studio installation complete. On updates, preserve private preferences and do not repeat onboarding unless requested or materially needed.

## 7. Offer recommended extensions (optional)

After the providers question, Studio may offer its [recommended extensions](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md): Studio's own companions and knowledge sources; third-party tools FrameCore Works recommends are in the [Toolbox catalog](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#toolbox-catalog). Run `python3 <persistent-bundle-dir>/skills/workflow-orchestrator/assets/extensions/extensions.py list --host codex` and ask one optional question. Install one only when the user explicitly asks, with its pinned dry-run plan first, then its install and verify commands, and a restart. Skipping leaves the installation complete.

## References

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills).
- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins).
- [OpenAI: Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins).
- [Pinned Workflow Kit installation pattern](https://github.com/FrameCoreWorks/framecore-works-codex-chatgpt-workflow-kit/tree/55c8bf19962c7bf7fb43648637ee433d990eb2a9).

The mechanism and invocation references were checked on 2026-09-29. Use the observed host's actual installation rules and preserve the complete Studio bundle.

## FrameCore Open Assets

FrameCore Open Assets is a standalone companion in its own repository,
[FrameCoreWorks/framecore-open-assets](https://github.com/FrameCoreWorks/framecore-open-assets). Install its
`plugins/framecore-open-assets` folder from a resolved commit of that repository (this repository no longer
carries a copy), preserving its portable manifest, `.codex-plugin/plugin.json`, Claude compatibility manifest, skill,
references and runtime. Follow this guide's native plugin installation/discovery procedure; do not
copy it into the personal-skills repository or replace Studio. The technical name is
`framecore-open-assets`; the exposed skill is `open-assets`.

After installation, resolve the actual skill directory and run the companion's runtime `status`.
Use `--host codex` only in the actual Codex environment. Python 3.10+, Pillow for images and
FFmpeg/FFprobe for audio/video are checked separately from network/provider readiness. The first
requested file follows search, rights review and `verify`, which saves the asset and sidecar and
records this host/category only. No Work or Claude result substitutes for that test. Policy holds
remain blocked, and missing dependencies require authorized installation. No account, API key,
model download or MCP server is needed.
