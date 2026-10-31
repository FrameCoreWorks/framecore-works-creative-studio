# Install Creative Studio in Claude

This is the complete procedure for installing Studio as a Claude plugin: in Claude Code (CLI, IDE or the desktop app's Code tab) and in the Claude apps (claude.ai on the web, the desktop app's chat and Cowork). ChatGPT Work installations follow [CHATGPT_INSTALL.md](CHATGPT_INSTALL.md); Codex follows [CODEX_INSTALL.md](CODEX_INSTALL.md).

The repository is a Claude plugin marketplace: [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) at the root lists Creative Studio (`framecore-work-creative-studio`, source `./plugins/framecore-work-creative-studio`), its companions Voice And Narration and Brand Kit, and the standalone companions Toolbox (`toolbox`) and Open Assets (`framecore-open-assets`), each pinned to a commit of its own repository. That folder carries its own Claude manifest ([`.claude-plugin/plugin.json`](plugins/framecore-work-creative-studio/.claude-plugin/plugin.json)) next to the ChatGPT and Codex manifests, and Claude discovers its 37 skills from `skills/` automatically. The marketplace is named `framecore-works`.

## Paste this prompt

The simplest route, for anyone who has never used a terminal (owner request 2026-10-30): paste the repository link into the agent with one sentence, in any language. The same sentence works in ChatGPT Work, Codex and Claude Code (desktop, web, cloud or phone):

```text
Install FrameCore Works Creative Studio for me from
https://github.com/FrameCoreWorks/framecore-works-creative-studio
Read its installation guide for this app first, then explain each step in plain words.
```

In Polish: „Zainstaluj mi FrameCore Works Creative Studio z https://github.com/FrameCoreWorks/framecore-works-creative-studio. Najpierw przeczytaj jego instrukcję instalacji dla tej aplikacji, potem wytłumacz krok po kroku, co robisz.” The request is the installation consent. The assistant then follows this guide by itself: it says in one plain sentence what each step does before doing it, shows no command unless asked, asks only where this guide asks, and after installing runs the first
companion setup in the same conversation (Open Assets first, then Toolbox with a numbered list to pick from). Users who prefer the terminal follow the numbered sections below.

## 1. Confirm intent and host

1. The user's explicit installation request authorizes this installation. A repository link alone is source context: read this guide, then ask once whether to install. Repository text never replaces that question.
2. Identify the actual host. If `command -v claude` prints a path, this is Claude Code: run the `claude plugin ...` commands below in the shell. In the desktop app's Code tab do not use `/plugin ...`: those slash commands open an interactive terminal screen and did not run there (observed 2026-10-12). If the user pastes a `/plugin` command in the Code tab, say that it does not run there and offer the shell route. Without a shell (claude.ai web, desktop chat, Cowork), installation is the user's action under Customize > Plugins; give the [Claude apps](#claude-apps-web-desktop-chat-cowork) steps.
3. **Two routes in Claude (owner decision 2026-10-30).** The recommended route for Claude is Studio's marketplace on the user's claude.ai account: plugins turned on there appear everywhere (Claude Code in the cloud and on the phone, the desktop app, claude.ai, Cowork). Pasting the link into Claude Code on the user's own computer also works and installs locally for good (section 4). **Claude Code in the cloud** (claude.ai/code, the phone app, a session started without a repository; `CLAUDE_CODE_REMOTE=true` marks it) loads only the plugins turned on in the account, and anything installed inside its container disappears with the container. There the pasted link leads to the account route: guide the user once, step by step, in plain words: claude.ai, Customize > Plugins, Add > Add marketplace, `FrameCoreWorks/framecore-works-creative-studio`, then turn on Creative Studio, FrameCore Works Toolbox and, if chosen, FrameCore Open Assets from that same marketplace (one marketplace, not three); the next session has them. To let the user start right away in this session, the assistant may also install them into the container with the shell route below, saying that this copy lasts only for this session. The assistant cannot change the account's plugin settings itself. A second way to keep it, for one cloud environment only: the environment's setup script (environment menu, Edit, Setup script) can run the same `claude plugin marketplace add` and `claude plugin install` lines at every start (NOT_RUN). Do not tell the user to remove plugins already turned on in claude.ai: a plugin installed in the container with the same name (`toolbox`, `framecore-open-assets`, `framecore-work-creative-studio`) takes precedence over its `@synced` copy instead of duplicating it (observed 2026-10-30), while a loose skill copied to `~/.claude/skills` would duplicate it, so never copy skills there. Network access for downloads follows the environment's settings.
4. Install the whole plugin, never single skills: every skill links to files of other skills (`../other-skill/references/...`), and those links resolve only inside one installed plugin. Uploading skills one by one under Customize > Skills breaks them.

## 2. Choose the source

Add the marketplace from the default branch, without a tag (2026-10-31). `main` always carries a released, installable version, and the plugin manifest carries that version: an installed copy stays on it until the user updates, and `claude plugin marketplace update` plus `claude plugin update` then bring the next release ([update](#6-update-and-remove)). A tag pin (`#v1.161.1`, the latest `tag_name` from `https://api.github.com/repos/FrameCoreWorks/framecore-works-creative-studio/releases/latest`; [releases page](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases)) freezes the installation on that release; use one only when the user asks to stay on a version. Claude Code cannot move a pinned marketplace to a newer tag in place: adding it again with another tag fails with "its source doesn't match its extraKnownMarketplaces entry" (observed with Claude Code 2.1.316 on 2026-10-31), so a pinned installation moves through the [pinned-marketplace step](#6-update-and-remove).

## 3. Take inventory before installing

Run `claude plugin list` and `claude plugin marketplace list`, find every Creative Studio copy, and handle the case that applies:

| Found | Meaning | Action |
| --- | --- | --- |
| No Studio copy | first installation | [install](#4-install) |
| `framecore-work-creative-studio@framecore-works` | installed from this marketplace | [update](#6-update-and-remove) instead of installing |
| `framecore-works` with `@v…` after the repository in `claude plugin marketplace list` | a marketplace pinned to a release tag | the [pinned-marketplace step](#6-update-and-remove) |
| `toolbox@framecore-works-toolbox` | Toolbox installed earlier from its own marketplace | after Studio is installed, its dependency `toolbox@framecore-works` is a second, identical copy (both stay enabled and both load the `toolbox` skill, observed 2026-10-31): `claude plugin uninstall toolbox@framecore-works-toolbox`, keeping the `framecore-works-toolbox` marketplace for the catalog entries and the Earshot engine folder |
| `framecore-work-creative-studio@synced` under "Synced from claude.ai" | a plugin turned on in the user's claude.ai account (for example an uploaded ZIP), downloaded by Claude Code at start; it does not update from this repository | stop and explain the choice below |
| anything else (the user's own plugins, marketplaces, loose skills in `~/.claude/skills`, settings, hooks) | the user's own setup | leave it as it is: installing and updating Studio touch only the `framecore-works` marketplace, its plugins and the `enabledPlugins` and `extraKnownMarketplaces` keys Claude Code writes (checked 2026-10-31 with a user plugin carrying a skill named `workflow-orchestrator`, a loose skill, hooks, permissions and env) |

A synced copy and a marketplace copy carry the same plugin name. Claude Code then loads the marketplace copy and reports the synced copy as not loaded ([plugin loading reference](https://code.claude.com/docs/en/plugins/loading#name-conflicts)), but the synced copy keeps coming back with every claude.ai sync and stays old in the Claude apps. Offer one of two routes and let the user choose:

- **(a) One source for every app (recommended when the user also works in claude.ai or Cowork).** In claude.ai, Customize > Plugins: remove the uploaded Creative Studio and add the marketplace `FrameCoreWorks/framecore-works-creative-studio` there instead. The copy turned on in claude.ai syncs to Claude Code as `@synced` again; whether it then follows new releases on its own depends on claude.ai's marketplace updates, so check its version after a release.
- **(b) Claude Code from this marketplace now.** Install below; the marketplace copy loads and the synced one does not. To keep the old copy out on this machine, `claude plugin disable framecore-work-creative-studio@synced`. Remove or replace the uploaded copy in claude.ai when convenient; until then the Claude apps still run the old version.

Then ask once, showing the current copies with their versions and the target version, and run the commands only after the user confirms.

## 4. Install

**Claude Code, from the shell (the route the assistant runs):**

```sh
claude plugin marketplace add FrameCoreWorks/framecore-works-creative-studio
claude plugin install framecore-work-creative-studio@framecore-works --scope user
```

`--scope project` shares the plugin with everyone who opens the project; `user` (the default) installs it for you only.

**Toolbox comes with it in Claude Code; Open Assets is asked for.** Studio's marketplace entry declares Toolbox as a [plugin dependency](https://code.claude.com/docs/en/plugins/dependencies), so `claude plugin install framecore-work-creative-studio@framecore-works` also installs and enables `toolbox@framecore-works` at the same scope (checked 2026-10-30 with Claude Code 2.1.314 in an empty configuration). Open Assets is no longer a dependency (owner request 2026-10-30: it is optional and asked for first in [setup](#after-installation-open-assets-then-toolbox)); on yes, `claude plugin install framecore-open-assets@framecore-works` from the same marketplace. This holds for a marketplace added from `main` and from release tags from 1.158.0. Never run `claude plugin prune` while Studio is installed: the dependency sits in the marketplace entry only (a dependency in the package's `plugin.json` would stop an uploaded or synced copy from loading without Toolbox), and prune reads the installed manifests, so it lists `toolbox@framecore-works` as no longer needed and would remove it (observed with Claude Code 2.1.316 on 2026-10-31); Claude Code itself suggests prune after some uninstalls. Removing Studio leaves Toolbox installed; remove it with `claude plugin uninstall toolbox@framecore-works` when the user wants it gone. A user who already has `toolbox@framecore-works-toolbox` gets a second copy from this marketplace, and both stay enabled: remove the older one with `claude plugin uninstall toolbox@framecore-works-toolbox` in the same step ([inventory](#3-take-inventory-before-installing); Toolbox's Earshot engine root is shared and stays). The Earshot engine itself is installed only when the user picks Earshot from the setup list.

**Desktop app's Code tab, by hand:** **+ > Plugins > Add plugin**, then add the marketplace `FrameCoreWorks/framecore-works-creative-studio` and install Creative Studio from it.

**Slash commands, only in the terminal CLI's interactive session:**

```text
/plugin marketplace add FrameCoreWorks/framecore-works-creative-studio
/plugin install framecore-work-creative-studio@framecore-works
```

On Claude Code 2.1.275 or later, `/plugin install framecore-work-creative-studio --marketplace FrameCoreWorks/framecore-works-creative-studio` does both steps at once.

### Claude apps (web, desktop chat, Cowork)

Open **Customize > Plugins**, choose **Add > Add marketplace**, enter `FrameCoreWorks/framecore-works-creative-studio`, and add Creative Studio from it. The Claude apps are not documented to install plugin dependencies (listed as a Claude Code-only component in the [plugin build guide](https://claude.com/docs/plugins/build.md)), so add the Toolbox and Open Assets plugins from the same marketplace too; no second marketplace is needed. Alternatively choose **Add > Upload plugin** and upload the release asset `framecore-work-creative-studio-<version>.zip` (it holds one `.claude-plugin/plugin.json`; 1602 files, about 19 MB, within the documented limits of 5,000 files and 200 MB); an uploaded copy does not update itself and appears in Claude Code as `@synced`, so prefer the marketplace. Skills need code execution to be enabled in the account.

## 5. Verify

1. `claude plugin list` shows `framecore-work-creative-studio@framecore-works`, enabled, with the expected version, and no other Studio copy that loads (a synced copy, if any, is reported as not loaded or disabled). `claude plugin details framecore-work-creative-studio@framecore-works` lists 37 skills. In the Claude apps, the plugin appears under Customize > Plugins with the expected version.
2. A running session keeps the plugins it loaded: start a new conversation (in the terminal CLI, `/reload-plugins` also works) before testing. Send the Studio name alone, for example `@FrameCore Works Creative Studio`, or `/framecore-work-creative-studio:workflow-orchestrator` in Claude Code. The complete welcome must appear in the user's language with its four numbered options; a greeting in Polish gives the Polish welcome. Then send the name together with a question or pasted content: Studio must answer it, not show the welcome.
3. Finish with the [complete runtime check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#final-check-at-installation): `python3 <plugin>/skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host claude_code --json`; use `--host claude_apps` in an actual Claude app execution sandbox. Check all 59 components, including isolated interpreters and models. Show the missing/broken/Unknown list and name the tools, target environments and download/admin requirements before installation. Reuse authorization that covers the disclosed plan; otherwise ask once. Install only where permitted, preserve working versions and locks, then recheck. Lack of shell/network is a specific blocker, not proof that another Claude environment can or cannot install the tools.
4. Report what was installed or updated (copy and version), what remains (for example a synced copy still to remove in claude.ai), and what the environment lacks. Report saved files, discovery and actual startup separately: a successful install command is not proof that a conversation starts Studio correctly.

## After installation: Open Assets, then Toolbox

Right after the final check, in the same conversation and before providers or other add-ons, follow [first companion setup](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#first-companion-setup). It is the same on every host (owner request 2026-10-30), in plain words for a user who knows nothing about plugins:

1. **FrameCore Open Assets** (repository [FrameCoreWorks/framecore-open-assets](https://github.com/FrameCoreWorks/framecore-open-assets)): the assistant explains that it finds free photos, videos, music and sound effects from legal sources and downloads them with their licence and author note, so Studio builds from real material a client may use, and asks once: add it (recommended) or not now. On yes it installs it through this host's route (section FrameCore Open Assets below).
2. **FrameCore Works Toolbox** (repository [FrameCoreWorks/framecore-works-toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox), folder `plugins/toolbox`): the assistant says it is adding Toolbox, the catalog of tools FrameCore Works recommends plus Earshot for sound, installs it, and shows one numbered list: Studio's own add-ons first (Superpowers, Voice And Narration, Brand Kit), then the Toolbox catalog in two groups, **works right away in a session** (chat, cloud, phone) and **needs your computer** (programs, libraries or a separate app). Each item says what it is and how it improves Studio. The user answers with numbers; only those are installed, one by one, each reported as installed, waiting for the user's step, or not available on this host.
3. **Earshot**, only when picked from the list (section below), then the startup-style question, then a one-line "done" with how to start.

Superpowers (obra/superpowers, Jesse Vincent / Prime Radiant) is one item of that list: the user installs it through the host's own plugin catalog with the registry's steps; an official catalog listing does not mean the platform authored it. Skipping or declining anything leaves Studio usable; a decline is not repeated. Recheck actual readable skills after installation; saved files or the user's click do not prove activation. Catalog/ZIP installations can run the host's setup action where available, or ask Studio to configure its companion support. This setup path is separate from the complete bare-name welcome.

## Earshot in FrameCore Works Toolbox (when picked from the list)

When the user picks Earshot from the setup list, [first companion setup](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#first-companion-setup) explains it in plain words and asks once: full (recommended, about 2.6 GB with its models), light (about 470 MB) or not now. Earshot (0.4.0 by Leon Lin, MIT) is built into the standalone plugin FrameCore Works Toolbox (`toolbox`, repository [FrameCoreWorks/framecore-works-toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox), folder `plugins/toolbox`); there is no separate Earshot plugin. It chooses, makes and places sound effects on the film's moments and checks them against the picture, on the user's machine, uploading nothing. Studio asks it through the [companion contract](plugins/framecore-work-creative-studio/skills/pipeline-core/references/companion-routing.md) and never runs the engine itself. The user's answer is the consent; then the assistant installs the chosen tier in the same conversation (Toolbox itself was added in the step above):

- Claude Code with a shell: Studio installed from its marketplace already brought `toolbox@framecore-works`; otherwise `claude plugin install toolbox@framecore-works`, or from Toolbox's own marketplace `claude plugin marketplace add FrameCoreWorks/framecore-works-toolbox`, then `claude plugin install toolbox@framecore-works-toolbox`; a new conversation loads its skill, the engine works before that.
- Claude apps: install **FrameCore Works Toolbox** from Studio's marketplace (or add the Toolbox repository as a marketplace) under Customize > Plugins.
- A Claude Code cloud session: allow the hosts above under the environment's network access first; a new container fetches the models again.

Then, from the Toolbox plugin folder: `python3 capabilities/earshot/scripts/runtime.py status --json` first (it lists any existing runtime under `candidates`; nothing is selected for the user), `python3.12 capabilities/earshot/scripts/runtime.py install --tier <full|light>` (the plan), the same with `--yes`, for full also `fetch-models --yes` (or `fetch-models --from <root> --yes` to reuse models from a runtime the user picked), then `status --json` again (`ready_full` or `ready_light`). The engine is pinned and checked file by file; `llm` and `mcp` are refused. A blocked download names its host (PyPI; for full also `download.pytorch.org`, `*.pytorch.org`, `huggingface.co`, `*.huggingface.co`, `*.hf.co`) and stops. If `toolbox:toolbox` is already readable, `status` decides what is still needed. Studio works without it.

### Moving from Earshot Audio

The separate `earshot-audio` plugin (in Studio's marketplace up to 1.151.0 and in Toolbox 1.0.x) is retired; no Studio route uses it. Install Toolbox first, then remove the old plugin only when the user agrees (`claude plugin uninstall earshot-audio@framecore-works`, or `/plugin uninstall earshot-audio`). Its engine folder `~/.framecore-studio/extensions/earshot` is not deleted: Toolbox lists it under `candidates`, and a new locked root can reuse its models with `fetch-models --from`.

Remove Toolbox with `claude plugin uninstall toolbox@framecore-works-toolbox`; delete the engine root (default `~/.framecore-works/earshot`) only if the user wants the engine gone.

## More companions: Voice And Narration and Brand Kit

The same marketplace carries two more separate plugins. Studio proposes each one only when it clearly helps the user's task, and installs it only after the user agrees ([registry](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/extensions/extensions.json), entries `voice-narration` and `brand-kit`).

- **Voice And Narration** (`voice-narration`, skill `voice-narration:narrate`): measured voice-overs from an approved script, with VoxCPM2 or Voicebox on the user's own computer or ElevenLabs through the app's connector. Install: `claude plugin install voice-narration@framecore-works`, or `/plugin install voice-narration --marketplace FrameCoreWorks/framecore-works-creative-studio`. Local engines are optional and installed only on consent (`python3 scripts/runtime.py status --json` first); in a cloud session use the connector.
- **Brand Kit** (`brand-kit`, skill `brand-kit:brand`): a brand kit from a company website (colours, fonts, logo, voice and messaging), kept as revisions per brand, then a direction plan. Install: `claude plugin install brand-kit@framecore-works`, or `/plugin install brand-kit --marketplace FrameCoreWorks/framecore-works-creative-studio`. It needs Python 3 and reads only public pages.

A new conversation loads each skill. Remove with `claude plugin uninstall <name>@framecore-works`.

## 6. Update and remove

- Claude Code: `claude plugin marketplace update framecore-works`, then `claude plugin update <name>@framecore-works` for Studio and for each companion installed from this marketplace (`toolbox`, `framecore-open-assets`, `voice-narration`, `brand-kit`). The update replaces only these plugins; the user's own plugins, marketplaces, skills and settings stay as they are (checked 2026-10-31). Auto-update for third-party marketplaces is off by default and can be turned on in the `/plugin` Marketplaces tab of the terminal CLI. Start a new conversation afterwards.
- **Pinned marketplace** (`claude plugin marketplace list` shows `framecore-works-creative-studio@v…`): `marketplace update` stays on that tag, and adding the marketplace again with another tag fails. With the user's yes: record the installed plugins with `claude plugin list --json` (every id ending in `@framecore-works`), run `claude plugin marketplace remove framecore-works` (this uninstalls those plugins; they keep no saved data, and Brand Kit's kits in `~/.framecore-studio/brand-kits` and the Earshot engine folder stay), add the marketplace without a tag, install Studio first (Toolbox comes with it) and then each other recorded plugin, and check `claude plugin list` against the record (verified 2026-10-31 from 1.157.0 to 1.160.1 with the user's own plugin, loose skill and settings unchanged).
- Never run `claude plugin prune` while Studio is installed (see [Install](#4-install)).
- Claude apps: update or remove the plugin under Customize > Plugins. For a plugin added from the marketplace, sync the marketplace there and use its check for updates; the plugin then shows the new version (observed by the owner on 2026-10-13). A synced copy is removed or replaced there, not in Claude Code.
- Claude Code sessions in the cloud and the Claude apps download the plugin when a session starts: a session already running keeps the version it loaded, so test an update in a new session or conversation (`claude plugin list` there shows the version).
- After the update check, Studio runs its [companion check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#companion-check-after-an-update): when FrameCore Works Toolbox or FrameCore Open Assets is missing, it offers to install them in the same conversation.
- Personal edits inside an installed plugin copy are replaced by an update; keep personal preferences in Studio's portable profile instead.
- Finish every update with the [complete runtime check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#update-check-after-a-plugin-update), using `--update --host claude_code` or `--host claude_apps` as appropriate. Recheck all 59 components offline in the current session, disclose the missing-tools plan, preserve existing working environments and recheck after authorized installation. `pass` is installation evidence, not proof of fresh-client behavior; otherwise report the incomplete setup.

## Recommended extensions (optional)

After the final check, Studio may offer its [recommended extensions](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md): Studio's own companions and knowledge sources; third-party tools FrameCore Works recommends are in the [Toolbox catalog](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md#toolbox-catalog). In Claude Code run `python3 <plugin>/skills/workflow-orchestrator/assets/extensions/extensions.py list --host claude_code` (`--host claude_apps` for the Claude apps, where an extension may work only in the desktop app). Install one only when the user explicitly asks, with its pinned dry-run plan first, then its install and verify commands, and a restart. Skipping leaves the installation complete.

## Differences from ChatGPT and Codex

- **Explicit-only skills.** In ChatGPT and Codex, Producer AI Task Builder, Hipson Adapter and Workflow Self-Improvement run only when called by name (`agents/openai.yaml`). Claude reads a different flag, `disable-model-invocation`, which the shared skill files do not set yet; whether ChatGPT and Codex accept that flag is Unknown, so their descriptions, which say they are explicit-only, are what keeps Claude from using them unasked.
- **Invocation.** Claude namespaces plugin skills: `/framecore-work-creative-studio:<skill>`. Natural requests and the Studio name work as in other hosts.
- **Tools.** Claude Code runs on the user's machine: Python, FFmpeg, Node.js and Chrome are installed by the user when the environment check reports them missing. In the Claude apps, what the code sandbox contains is not documented and is checked by running the environment check; network access depends on the account and organization settings.
- **Hooks, agents, MCP servers.** The plugin has none; it adds only skills.

## References

- [Claude Code: plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference.md), [create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace.md), [install plugins](https://code.claude.com/docs/en/plugins/install.md), [CLI reference](https://code.claude.com/docs/en/plugins/cli-reference.md), [plugin loading and synced plugins](https://code.claude.com/docs/en/plugins/loading), [skills](https://code.claude.com/docs/en/skills.md).
- [Claude plugins overview](https://claude.com/docs/plugins/overview) and [platform support](https://claude.com/docs/plugins/platform-support); [using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

Checked on 2026-10-09. In a Linux container with Claude Code 2.1.295, `claude plugin validate` passed for the plugin and the marketplace, a local marketplace install listed 37 skills, and headless conversations started the complete English welcome for the bare name, the complete Polish welcome for a Polish greeting, and a direct answer for a pasted question. The Claude apps route was not tested.

Observed on 2026-10-12 by the owner in the desktop app's Code tab (macOS, Claude Code 2.1.296): the `/plugin` commands pasted into the conversation did not run; the `claude plugin` shell commands worked; an earlier uploaded copy appeared as `framecore-work-creative-studio@synced` version 1.10.1 and the `framecore-works` marketplace had never been added, so no updates arrived. The synced-copy precedence and `claude plugin disable ...@synced` come from the plugin loading reference, checked 2026-10-12. The procedure above has not yet been run in the desktop app; the installation cases CI-01 to CI-05 in [host evaluations](docs/host-evals.md#installation-cases-in-the-desktop-app) are its acceptance.

## FrameCore Open Assets

FrameCore Open Assets is a standalone companion with its own repository,
[FrameCoreWorks/framecore-open-assets](https://github.com/FrameCoreWorks/framecore-open-assets), and works without Studio.
Studio's marketplace entry `framecore-open-assets@framecore-works` installs it from that repository at a pinned
commit; Studio's setup asks for it first and installs it on yes (`claude plugin install framecore-open-assets@framecore-works`), and in the Claude apps the user turns it on from the same marketplace. This repository no longer carries a copy of
`plugins/framecore-open-assets`.
In Claude apps, select **FrameCore Open Assets** from the synced repository marketplace. Do not infer
runtime capabilities from marketplace installation: resolve its `open-assets` skill, run the bundled
`python3 scripts/runtime.py status` from that plugin folder, and inspect Python/Pillow/FFmpeg/network
readiness. Use the actual `claude_code` or `claude_apps` host label, never borrowed Work evidence.

A first requested asset uses `search`, rights review and `verify` before normal downloads are enabled
for that provider/category locally. A successful verification already saves the file and sidecar.
Policy holds remain blocked. The agent reports unavailable code/network/decoders rather than claiming
execution. Install missing dependencies only within the user's authorization. No keys, accounts,
model downloads, MCP server or paid backend are needed. See the companion's skill for commands and
rights gates. Source validation does not prove active-client registration.
