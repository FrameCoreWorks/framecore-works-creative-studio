# Creative Studio 1.157.0

ChatGPT Work now installs and updates FrameCore Works Toolbox and FrameCore Open Assets on its own, without a ZIP from the user: Studio's companion setup and update check read each companion's files as text through the GitHub connector, give them to Plugin Creator and check the saved plugin with the companion's `hosted_update.py`. The Studio update itself follows the same route ([CHATGPT_UPDATE.md](CHATGPT_UPDATE.md#no-zip-update-route)).

Source tests and validation passed. Fresh-client behavior was not run in Claude, ChatGPT Work or Codex.
