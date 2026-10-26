# Openverse: decision map

Reviewed 2026-10-26 at [`49f5b60`](https://github.com/WordPress/openverse/tree/49f5b6067a6eb40ef7eaa251ced43eaccfc35226) (WordPress Foundation, MIT, Copyright (c) 2021 Openverse, [licence](LICENSE)) after the owner sent https://openverse.org. Owner decision 2026-10-26: Openverse is Studio's reference base for images and sound, announced once at first configuration.

| Part | Decision | Where in Studio |
| --- | --- | --- |
| Public API (`api.openverse.org/v1/images/`, `/v1/audio/`), anonymous: about 20 requests a minute and 200 a day (headers checked 2026-10-26); no video endpoint (404) | used directly, no installation or key | [`openverse.py`](../../skills/reference-pack-curator/scripts/openverse.py) and the [Openverse reference base](../../skills/reference-pack-curator/SKILL.md#openverse-reference-base) in Reference Pack. Pointers in every owner that sources pictures or sound: Graphic Design, Image Prompt, Storyboard Board, Cinematography, Character Design (never a real person's identity), Motion Graphics (pictures for service reels, recorded sound), FrameCut (stills, b-roll, ambience, effects), Audio, Research and the orchestrator's picture rule; the Earshot companion (1.0.9) finds Freesound candidates through Openverse with `license=cc0,by` |
| Per-work licence, source page and ready attribution line | carried into the asset manifest | Reference Pack section above |
| Search site (`openverse.org/search/...`) | the hand-search link where neither code nor a web tool reaches the API | Reference Pack section above |
| API source code, frontend, catalogue ingestion | not adopted | not needed to call the public API |
| Third-party Openverse MCP servers (Pipeworx and others) | not adopted, not reviewed | the plain API needs no intermediary |

Terms (API terms of service, read 2026-10-26): keep to the rate limits, never scrape the catalogue or spread requests over machines to evade limits, attribute CC-licensed works and respect the hosting platforms' terms. Openverse does not verify licences and gives no warranty; the source page decides before client use.

Registry entry: `openverse` in [extensions.json](../../skills/workflow-orchestrator/assets/extensions/extensions.json). Live searches for images and audio were run from a Claude Code cloud container on 2026-10-26; Claude apps, ChatGPT and ChatGPT Work reach to the API: NOT_RUN.
