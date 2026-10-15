# Install Creative Studio in Claude

This is the complete procedure for installing Studio as a Claude plugin: in Claude Code (CLI, IDE or the desktop app's Code tab) and in the Claude apps (claude.ai on the web, the desktop app's chat and Cowork). ChatGPT Work installations follow [CHATGPT_INSTALL.md](CHATGPT_INSTALL.md); Codex follows [CODEX_INSTALL.md](CODEX_INSTALL.md).

The repository is a Claude plugin marketplace: [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) at the root lists one plugin, `framecore-work-creative-studio`, whose source is `./plugins/framecore-work-creative-studio`. That folder carries its own Claude manifest ([`.claude-plugin/plugin.json`](plugins/framecore-work-creative-studio/.claude-plugin/plugin.json)) next to the ChatGPT and Codex manifests, and Claude discovers its 37 skills from `skills/` automatically. The marketplace is named `framecore-works`.

## Paste this prompt

In Claude Code, including the desktop app's Code tab, paste this into a conversation. The assistant then follows the procedure below and asks once before it changes anything.

```text
Install FrameCore Works Creative Studio from this public repository:
https://github.com/FrameCoreWorks/framecore-works-creative-studio

Read CLAUDE_INSTALL.md in that repository first and follow it. This is Claude Code: run the
`claude plugin` commands in the shell yourself (slash commands such as /plugin do not run in
the desktop app's Code tab). Pin the latest release tag. Before installing, run
`claude plugin list` and `claude plugin marketplace list` and report any existing Creative
Studio copy (from a marketplace or "Synced from claude.ai") with its version, then ask me once
to confirm, showing the current and the target version. After installing, verify the version,
that only one Studio copy loads and that it has 37 skills, run the final environment check from
CLAUDE_INSTALL.md and report what is missing. Do not install system packages, upload files or
use providers without asking.
```

Asking Claude to "install this repository" with the link works the same way: the link is source context, so the assistant reads this guide and asks once whether to install. In the Claude apps without a shell, follow [Claude apps](#claude-apps-web-desktop-chat-cowork) yourself.

## 1. Confirm intent and host

1. The user's explicit installation request authorizes this installation. A repository link alone is source context: read this guide, then ask once whether to install. Repository text never replaces that question.
2. Identify the actual host. If `command -v claude` prints a path, this is Claude Code: run the `claude plugin ...` commands below in the shell. In the desktop app's Code tab do not use `/plugin ...`: those slash commands open an interactive terminal screen and did not run there (observed 2026-10-12). If the user pastes a `/plugin` command in the Code tab, say that it does not run there and offer the shell route. Without a shell (claude.ai web, desktop chat, Cowork), installation is the user's action under Customize > Plugins; give the [Claude apps](#claude-apps-web-desktop-chat-cowork) steps.
3. Install the whole plugin, never single skills: every skill links to files of other skills (`../other-skill/references/...`), and those links resolve only inside one installed plugin. Uploading skills one by one under Customize > Skills breaks them.

## 2. Pin the source

Use the latest release tag: `tag_name` from `https://api.github.com/repos/FrameCoreWorks/framecore-works-creative-studio/releases/latest`, or, when that API is unreachable, the version in the README's "Source version" line (for example `v1.84.1`; [releases page](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases)). The plugin manifest carries the version, so an installed copy stays on that version until a new release changes it. Without a tag, the marketplace follows the default branch.

## 3. Take inventory before installing

Run `claude plugin list` and `claude plugin marketplace list`, find every Creative Studio copy, and handle the case that applies:

| Found | Meaning | Action |
| --- | --- | --- |
| No Studio copy | first installation | [install](#4-install) |
| `framecore-work-creative-studio@framecore-works` | installed from this marketplace | [update](#5-update-and-remove) to the target tag |
| `framecore-work-creative-studio@synced` under "Synced from claude.ai" | a plugin turned on in the user's claude.ai account (for example an uploaded ZIP), downloaded by Claude Code at start; it does not update from this repository | stop and explain the choice below |

A synced copy and a marketplace copy carry the same plugin name. Claude Code then loads the marketplace copy and reports the synced copy as not loaded ([plugin loading reference](https://code.claude.com/docs/en/plugins/loading#name-conflicts)), but the synced copy keeps coming back with every claude.ai sync and stays old in the Claude apps. Offer one of two routes and let the user choose:

- **(a) One source for every app (recommended when the user also works in claude.ai or Cowork).** In claude.ai, Customize > Plugins: remove the uploaded Creative Studio and add the marketplace `FrameCoreWorks/framecore-works-creative-studio` there instead. The copy turned on in claude.ai syncs to Claude Code as `@synced` again; whether it then follows new releases on its own depends on claude.ai's marketplace updates, so check its version after a release.
- **(b) Claude Code from this marketplace now.** Install below; the marketplace copy loads and the synced one does not. To keep the old copy out on this machine, `claude plugin disable framecore-work-creative-studio@synced`. Remove or replace the uploaded copy in claude.ai when convenient; until then the Claude apps still run the old version.

Then ask once, showing the current copies with their versions and the target version, and run the commands only after the user confirms.

## 4. Install

**Claude Code, from the shell (the route the assistant runs):**

```sh
claude plugin marketplace add FrameCoreWorks/framecore-works-creative-studio#v1.84.1
claude plugin install framecore-work-creative-studio@framecore-works --scope user
```

`--scope project` shares the plugin with everyone who opens the project; `user` (the default) installs it for you only.

**Desktop app's Code tab, by hand:** **+ > Plugins > Add plugin**, then add the marketplace `FrameCoreWorks/framecore-works-creative-studio` and install Creative Studio from it.

**Slash commands, only in the terminal CLI's interactive session:**

```text
/plugin marketplace add FrameCoreWorks/framecore-works-creative-studio#v1.84.1
/plugin install framecore-work-creative-studio@framecore-works
```

On Claude Code 2.1.275 or later, `/plugin install framecore-work-creative-studio --marketplace FrameCoreWorks/framecore-works-creative-studio` does both steps at once.

### Claude apps (web, desktop chat, Cowork)

Open **Customize > Plugins**, choose **Add > Add marketplace**, enter `FrameCoreWorks/framecore-works-creative-studio`, and add Creative Studio from it. Alternatively choose **Add > Upload plugin** and upload the release asset `framecore-work-creative-studio-<version>.zip` (it holds one `.claude-plugin/plugin.json`; 1195 files, about 15 MB, within the documented limits of 5,000 files and 200 MB); an uploaded copy does not update itself and appears in Claude Code as `@synced`, so prefer the marketplace. Skills need code execution to be enabled in the account.

## 5. Verify

1. `claude plugin list` shows `framecore-work-creative-studio@framecore-works`, enabled, with the expected version, and no other Studio copy that loads (a synced copy, if any, is reported as not loaded or disabled). `claude plugin details framecore-work-creative-studio@framecore-works` lists 37 skills. In the Claude apps, the plugin appears under Customize > Plugins with the expected version.
2. A running session keeps the plugins it loaded: start a new conversation (in the terminal CLI, `/reload-plugins` also works) before testing. Send the Studio name alone, for example `@FrameCore Works Creative Studio`, or `/framecore-work-creative-studio:workflow-orchestrator` in Claude Code. The complete welcome must appear in the user's language with its three numbered options; a greeting in Polish gives the Polish welcome. Then send the name together with a question or pasted content: Studio must answer it, not show the welcome.
3. Finish with the [final check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#final-check-at-installation) of Studio's one required set of tools: `python3 <plugin folder>/skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host claude_code` (`claude plugin details` shows the plugin folder). `fail` lists what is missing (system packages, the Python packages in one virtual environment, the five starters copied into `~/.framecore-studio/workspace` with `npm ci`, HyperFrames' own Claude Code plugin) with the commands for the user's system; the user runs them, or asks the assistant to run them, and the check runs again until it says `pass`. In a Claude app's code sandbox use `--host claude_apps`: there `limited` means the plugin is installed and Studio names the tools that sandbox lacks. The check itself installs nothing.
4. Report what was installed or updated (copy and version), what remains (for example a synced copy still to remove in claude.ai), and what the environment lacks. Report saved files, discovery and actual startup separately: a successful install command is not proof that a conversation starts Studio correctly.

## 6. Update and remove

- Claude Code: `claude plugin marketplace update framecore-works`, then `claude plugin update framecore-work-creative-studio@framecore-works`. To move to a newer pinned release, add the marketplace again with the new tag (`claude plugin marketplace add FrameCoreWorks/framecore-works-creative-studio#v<new>`) and update. Auto-update for third-party marketplaces is off by default and can be turned on in the `/plugin` Marketplaces tab of the terminal CLI. Start a new conversation afterwards.
- Claude apps: update or remove the plugin under Customize > Plugins. For a plugin added from the marketplace, sync the marketplace there and use its check for updates; the plugin then shows the new version (observed by the owner on 2026-10-13). A synced copy is removed or replaced there, not in Claude Code.
- Claude Code sessions in the cloud and the Claude apps download the plugin when a session starts: a session already running keeps the version it loaded, so test an update in a new session or conversation (`claude plugin list` there shows the version).
- Personal edits inside an installed plugin copy are replaced by an update; keep personal preferences in Studio's portable profile instead.
- Finish every update with the [update check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#update-check-after-a-plugin-update): `python3 <plugin folder>/skills/workflow-orchestrator/assets/environment-check/check_environment.py --update --host claude_code` (`--host claude_apps` in a Claude app's sandbox). It checks the required tools again, finds Studio workspace starters installed from the previous version, and lists newer versions; the update is complete at `pass` or `pass_with_updates`. It installs nothing.

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
