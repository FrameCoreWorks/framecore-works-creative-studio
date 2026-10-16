# Local voice engines: what Studio took

Owner request 2026-10-16: four open text-to-speech engines for the user to choose from, with Studio describing them when the user does not know. Reviewed on 2026-10-16; no code or model is vendored, and each licence is copied here.

| Engine | Source, reviewed at | Licence |
|---|---|---|
| Voicebox | [jamiepine/voicebox](https://github.com/jamiepine/voicebox/tree/2bcb98d1a8b6fe05e15fbc1559e3085669e4035d), release v0.5.0 | MIT ([licence](LICENSE-voicebox)); each model inside has its own |
| OmniVoice | [k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice/tree/08be0b4ccbac3e13e374e86fbfead4b4cac343e2), PyPI `omnivoice` 0.2.1 | Apache-2.0 code ([licence](LICENSE-OmniVoice)); weights reported non-commercial, not verified (Hugging Face was not reachable) |
| VoxCPM2 | [OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM/tree/cce58a5b59303c9bd63d12f23afe6a49a4a80c59), PyPI `voxcpm` 2.0.3 | Apache-2.0 code and weights ([licence](LICENSE-VoxCPM)) |
| MOSS-TTS | [OpenMOSS/MOSS-TTS](https://github.com/OpenMOSS/MOSS-TTS/tree/934d6826b084c46a0d033402174d5f8ac4ed2519) | Apache-2.0 code and models ([licence](LICENSE-MOSS-TTS)) |
| MOSS-TTSD | [OpenMOSS/MOSS-TTSD](https://github.com/OpenMOSS/MOSS-TTSD/tree/46973e425da227bfa3b315dcd7a4aba8b6be5574) | Apache-2.0 code and models ([licence](LICENSE-MOSS-TTSD)) |

## Decision map

| Part | Decision | Studio destination or reason |
|---|---|---|
| The engines themselves | Extension | Natively installable [recommended extensions](../../skills/workflow-orchestrator/references/extensions.md) (category `tts`), pinned, installed only on request; models of several gigabytes and a GPU do not belong in the plugin |
| What each can do (languages, cloning, voice design, dialogue, sound, hardware, licence) | Adopt as a choice guide | [Local voice engines](../../skills/audio-production-director/references/local-tts-engines.md) in Audio Production Director: the user chooses, or Studio describes them and recommends one for the need and the computer |
| Voicebox's REST API and MCP server | Adopt as the agent route | Studio generates through `POST /generate` on 127.0.0.1:17493 or the MCP server once the user installed the app |
| Each project's responsible-use terms | Adopt | Consent before cloning, no impersonation, disclosure, and the engine, model and licence recorded in delivery |

## Evidence

2026-10-16, Linux container: READMEs, documentation, package files and licences read at the commits above; `pip install --dry-run` resolved `omnivoice` 0.2.1 and `voxcpm` 2.0.3. No engine was installed and no model was downloaded or run, so audio quality and speed are the projects' own claims, not measured by Studio.
