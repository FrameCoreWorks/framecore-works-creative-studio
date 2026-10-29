# Local voice engines: what Studio keeps

Owner request 2026-10-16 added four open text-to-speech engines to Studio's recommendations. Owner decision 2026-10-29 removed them all from Studio: Voicebox moved to the [FrameCore Works Toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox) catalog as an app note, and OmniVoice, VoxCPM2, MOSS-TTS and MOSS-TTSD were erased from Studio together with their copied licences. No code or model is vendored.

| Engine | Source, reviewed at | Licence |
|---|---|---|
| Voicebox | [jamiepine/voicebox](https://github.com/jamiepine/voicebox/tree/2bcb98d1a8b6fe05e15fbc1559e3085669e4035d), release v0.5.0 | MIT ([licence](LICENSE-voicebox)); each model inside has its own |

## Decision map

| Part | Decision | Studio destination or reason |
|---|---|---|
| The Voicebox app | Toolbox app note | Pinned, installed by the user by hand from its release page, only on request |
| How to choose between `voice-narration` and Voicebox | Adopt as a choice guide | [Local voice engines](../../skills/audio-production-director/references/local-tts-engines.md) in Audio Production |
| Voicebox's REST API and MCP server | Adopt as the agent route | Studio generates through `POST /generate` on 127.0.0.1:17493 or the MCP server once the user installed the app |
| Responsible-use terms | Adopt | Consent before cloning, no impersonation, disclosure, and the engine, model and licence recorded in delivery |

## Evidence

2026-10-16, Linux container: Voicebox's README, documentation and licence read at the commit above. The app was not installed or run, so audio quality and speed are the project's own claims, not measured by Studio.
