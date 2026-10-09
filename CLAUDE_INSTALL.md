# Install Creative Studio in Claude

This is the complete procedure for installing Studio as a Claude plugin: in Claude Code (CLI, IDE or the desktop app's Code tab) and in the Claude apps (claude.ai on the web, the desktop app's chat and Cowork). ChatGPT Work installations follow [CHATGPT_INSTALL.md](CHATGPT_INSTALL.md); Codex follows [CODEX_INSTALL.md](CODEX_INSTALL.md).

The repository is a Claude plugin marketplace: [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) at the root lists one plugin, `framecore-work-creative-studio`, whose source is `./plugins/framecore-work-creative-studio`. That folder carries its own Claude manifest ([`.claude-plugin/plugin.json`](plugins/framecore-work-creative-studio/.claude-plugin/plugin.json)) next to the ChatGPT and Codex manifests, and Claude discovers its 37 skills from `skills/` automatically. The marketplace is named `framecore-works`.

## 1. Confirm intent and host

1. The user's explicit installation request authorizes this installation. A repository link alone is source context; clarify the intended action before installing anything.
2. Identify the actual host: Claude Code (a terminal with the `claude` command, the IDE extension or the desktop app's Code tab) or a Claude app (claude.ai web, desktop chat, Cowork). Installation is the user's action in the Claude apps; in Claude Code the assistant may run the commands below when the user asks.
3. Install the whole plugin, never single skills: every skill links to files of other skills (`../other-skill/references/...`), and those links resolve only inside one installed plugin. Uploading skills one by one under Customize > Skills breaks them.

## 2. Pin the source

Use a release tag, for example `v1.49.0` from the [releases page](https://github.com/FrameCoreWorks/framecore-works-creative-studio/releases). The plugin manifest carries the version, so an installed copy stays on that version until a new release changes it. Without a tag, the marketplace follows the default branch.

## 3. Install

**Claude Code, in a session:**

```text
/plugin marketplace add FrameCoreWorks/framecore-works-creative-studio#v1.49.0
/plugin install framecore-work-creative-studio@framecore-works
```

**Claude Code, from a shell:**

```sh
claude plugin marketplace add FrameCoreWorks/framecore-works-creative-studio#v1.49.0
claude plugin install framecore-work-creative-studio@framecore-works --scope user
```

`--scope project` shares the plugin with everyone who opens the project; `user` (the default) installs it for you only. On Claude Code 2.1.275 or later, `/plugin install framecore-work-creative-studio --marketplace FrameCoreWorks/framecore-works-creative-studio` does both steps at once. In the desktop app's Code tab, the same marketplace appears under **+ > Plugins > Add plugin**.

**Claude apps (web, desktop chat, Cowork):** open **Customize > Plugins**, choose **Add > Add marketplace**, enter `FrameCoreWorks/framecore-works-creative-studio`, and add Creative Studio from it. Alternatively choose **Add > Upload plugin** and upload the release asset `framecore-work-creative-studio-<version>.zip` (it holds one `.claude-plugin/plugin.json`; 936 files, about 10 MB, within the documented limits of 5,000 files and 200 MB). Skills need code execution to be enabled in the account.

## 4. Verify

1. `claude plugin list` shows `framecore-work-creative-studio@framecore-works`, enabled, with the expected version; `claude plugin details framecore-work-creative-studio@framecore-works` lists 37 skills. In a session, `/reload-plugins` loads a fresh install and the `/plugin` Errors tab shows load problems. In the Claude apps, the plugin appears under Customize > Plugins.
2. Start a new conversation and send the Studio name alone, for example `@FrameCore Works Creative Studio`, or `/framecore-work-creative-studio:workflow-orchestrator` in Claude Code. The complete welcome must appear in the user's language with both numbered modes; a greeting in Polish gives the Polish welcome. Then send the name together with a question or pasted content: Studio must answer it, not show the welcome.
3. Finish with the [final check](plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/environment-check/README.md#final-check-at-installation) of Studio's one required set of tools: `python3 <plugin folder>/skills/workflow-orchestrator/assets/environment-check/check_environment.py --final --host claude_code` (`claude plugin details` shows the plugin folder). `fail` lists what is missing (system packages, the Python packages in one virtual environment, the four starters copied into `~/.framecore-studio/workspace` with `npm ci`, HyperFrames' own Claude Code plugin) with the commands for the user's system; the user runs them, or asks the assistant to run them, and the check runs again until it says `pass`. In a Claude app's code sandbox use `--host claude_apps`: there `limited` means the plugin is installed and Studio names the tools that sandbox lacks. The check itself installs nothing.
4. Report saved files, discovery and actual startup separately. A successful install command is not proof that a conversation starts Studio correctly.

## 5. Update and remove

- Claude Code: `claude plugin marketplace update framecore-works`, then `claude plugin update framecore-work-creative-studio@framecore-works`, or **Update now** on the plugin in `/plugin`. To move to a newer pinned release, add the marketplace again with the new tag. Auto-update for third-party marketplaces is off by default and can be turned on in the `/plugin` Marketplaces tab.
- Claude apps: update or remove the plugin under Customize > Plugins.
- Personal edits inside an installed plugin copy are replaced by an update; keep personal preferences in Studio's portable profile instead.

## Differences from ChatGPT and Codex

- **Explicit-only skills.** In ChatGPT and Codex, Producer AI Task Builder, Hipson Adapter and Workflow Self-Improvement run only when called by name (`agents/openai.yaml`). Claude reads a different flag, `disable-model-invocation`, which the shared skill files do not set yet; whether ChatGPT and Codex accept that flag is Unknown, so their descriptions, which say they are explicit-only, are what keeps Claude from using them unasked.
- **Invocation.** Claude namespaces plugin skills: `/framecore-work-creative-studio:<skill>`. Natural requests and the Studio name work as in other hosts.
- **Tools.** Claude Code runs on the user's machine: Python, FFmpeg, Node.js and Chrome are installed by the user when the environment check reports them missing. In the Claude apps, what the code sandbox contains is not documented and is checked by running the environment check; network access depends on the account and organization settings.
- **Hooks, agents, MCP servers.** The plugin has none; it adds only skills.

## References

- [Claude Code: plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference.md), [create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace.md), [install plugins](https://code.claude.com/docs/en/plugins/install.md), [CLI reference](https://code.claude.com/docs/en/plugins/cli-reference.md), [skills](https://code.claude.com/docs/en/skills.md).
- [Claude plugins overview](https://claude.com/docs/plugins/overview) and [platform support](https://claude.com/docs/plugins/platform-support); [using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

Checked on 2026-10-09. In a Linux container with Claude Code 2.1.295, `claude plugin validate` passed for the plugin and the marketplace, a local marketplace install listed 37 skills, and headless conversations started the complete English welcome for the bare name, the complete Polish welcome for a Polish greeting, and a direct answer for a pasted question. The Claude apps route was not tested.
