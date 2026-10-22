# Creative Studio 1.123.2

Studio works with the Earshot audio plugin when it is installed: motion sound effects, sound kits and audio analysis go to Earshot, while Studio keeps the brief, the mix, the storyboard acceptance and the final review. Without the plugin, Studio uses the pinned Earshot command line where it can be installed, or its own sound tools, and always says which engine produced the result.

Everything stays on your machine: no audio is sent to Gemini or any other model service, and no MCP server is started.

Verification: source tests and canonical validation are recorded in verification/release-1.123.2.json; Claude Code host evaluations without Earshot pass. The joint Studio and Earshot run was not repeated here. Fresh ChatGPT behavior remains NOT_RUN; the hosted plugin is updated separately, preserving its private overlay.
