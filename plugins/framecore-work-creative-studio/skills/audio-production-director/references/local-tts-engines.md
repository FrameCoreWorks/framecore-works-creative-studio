# Local voice engines: let the user choose

Use this when a voice-over, narration or dialogue is to be generated on the user's own computer instead of read by a person or made in a connected service. Studio itself recommends no voice engine (owner decision 2026-10-29); two routes remain, and the user chooses. Studio never picks one silently and never installs one without an explicit request.

## 1. Ask which route

Once the script and the voice direction are settled, ask one question in the user's language: the `voice-narration` plugin, the Voicebox desktop app, an engine they already use, or that they do not know. A user who already uses an engine keeps it. Studio's own script, timing, pronunciation notes and review stay the same whichever engine runs.

## 2. When the user does not know: describe them

| | `voice-narration` plugin | Voicebox |
|---|---|---|
| What it is | A separate plugin from this repository (skill `voice-narration:narrate`, registry entry `voice-narration` in the [recommended extensions](../../workflow-orchestrator/references/extensions.md)) | A desktop app (macOS, Windows; Linux from source) with several engines inside, plus a REST API and MCP server; an app note in the [Toolbox catalog](../../workflow-orchestrator/references/extensions.md#toolbox-catalog), pinned to release v0.5.0 (MIT, [licence](../../../integrations/tts-engines/LICENSE-voicebox)) |
| Best for | A finished read for the mix: lexicon, a length check per line, WAV files and `narration.lock.json` | Working without code: clone, design and edit voices in one app |
| Engines | Its own documented engines (local, with consent) or ElevenLabs through the connector | Several inside; check the licence of the engine picked inside |

Recommendation by need: a client voice-over that goes into a Studio film, `voice-narration`; no code or a first try on the user's own computer, Voicebox. Say which computer requirements the user must meet; when they cannot, say so and offer the route that fits.

## 3. Install and generate

Install only on an explicit request. `voice-narration` follows its registry entry (`extensions.py show voice-narration --host <host>`, its plan, then install, verify and the restart); it installs a local engine only with consent, and in a cloud session or a phone app it advises against installing one and offers ElevenLabs through the connector or the script handoff below. Voicebox is installed by the user from its pinned release page (Toolbox's app note has the steps); Studio then connects its MCP server or calls its REST API (`POST /generate` on 127.0.0.1:17493). Every local engine downloads model weights of several gigabytes on first use.

Discover the current host's actual tools and authorized connections before choosing execution. An available Voicebox MCP connection in Claude Desktop or another host can provide a native route; a local executor may expose an existing engine. Verify the route, without assuming that a host name proves availability. If no supported runtime or authorized connection exists, deliver the script, voice direction (voice, pace, pauses, pronunciation, emotion per line) and engine settings for the user's local generation.

## 4. Consent and delivery

Clone a voice only with its owner's documented permission (the user's own voice, or a speaker who agreed in writing); never imitate a real person, a celebrity or a client's competitor. Mark a synthetic voice where the platform or the law asks. Record the engine, model, version, licence and the voice source in the delivery notes.

After generation, measure the read against the [voice-over budget](../../pipeline-core/references/short-form-timing.md), listen for wrong stress in names and numbers, regenerate only the faulty lines, and hand the files to the mix (in a motion film, Motion Graphics's sound step).
