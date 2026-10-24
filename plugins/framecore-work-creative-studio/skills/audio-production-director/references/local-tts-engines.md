# Local voice engines: let the user choose

Use this when a voice-over, narration or dialogue is to be generated on the user's own computer instead of read by a person or made in a connected service. Studio offers four open engines from the [recommended extensions](../../workflow-orchestrator/references/extensions.md) (`extensions.py list --category tts`). The user chooses; Studio never picks one silently and never installs one without an explicit request.

## 1. Ask which engine

Once the script and the voice direction are settled, ask one question in the user's language: which engine they want, Voicebox, OmniVoice, VoxCPM2 or MOSS (MOSS-TTS for one narrator, MOSS-TTSD for dialogue), or that they do not know. A user who already uses one keeps it. Studio's own script, timing, pronunciation notes and review stay the same whichever engine runs.

## 2. When the user does not know: describe them

Give this comparison in the user's language, then recommend one for their need and their computer:

| | Voicebox | OmniVoice | VoxCPM2 | MOSS-TTS / MOSS-TTSD |
|---|---|---|---|---|
| What it is | A desktop app (macOS, Windows; Linux from source) with several engines inside, plus a REST API and MCP server | A Python library and command line | A Python library and command line | A model family; TTSD is its dialogue model |
| Best for | Working without code: clone, design and edit voices in one app | Many languages, quick drafts, a modest GPU | Client voice-overs and ads: the cleanest sound | Long narration with exact pauses (TTS); dialogues and podcasts with up to five voices (TTSD) |
| Polish | Yes, in some engines inside (Chatterbox Multilingual, TADA, OmniVoice) | Yes, among 646 languages | Yes, among 30 languages | Yes (31 and 20 languages) |
| Cloning | From a few seconds | From 3 to 10 seconds | From audio, or audio plus transcript for an exact match | From short audio; one reference per speaker in TTSD |
| Voice from a description | Yes (Qwen VoiceDesign inside) | Attributes (gender, age, pitch, accent); best in English and Chinese | Yes, from a written description, with style and emotion | Yes, through MOSS-VoiceGenerator |
| Sound | Depends on the engine | 24 kHz | 48 kHz | 24 kHz (48 kHz stereo in the 4B model) |
| Computer | A CPU is enough for the lightest engine | A small GPU (4 GB tested), Apple or Intel | About 8 GB of VRAM; slower on Apple or a CPU | A strong NVIDIA GPU (8B models) |
| Commercial use | The app is MIT; check the licence of the engine picked inside | Weights reported as non-commercial: check the model card first | Yes, Apache-2.0 | Yes, Apache-2.0 |

Recommendation by need: no code or a first try, Voicebox; a paid ad or client voice-over, VoxCPM2; a dialogue, podcast or scene with several voices, MOSS-TTSD; a long narration with exact pauses on a strong GPU, MOSS-TTS; a rare language or a weak GPU for a draft, OmniVoice (not for paid work until its licence allows). Say which computer requirements the user must meet; when they cannot, say so and offer the route that fits.

## 3. Install and generate

Install only on an explicit request, through the [extension route](../../workflow-orchestrator/references/extensions.md): `extensions.py show <id> --host <host>`, its plan, then install, verify and the restart. Voicebox is installed by the user from its release page; Studio then connects its MCP server or calls its REST API. Every engine downloads model weights of several gigabytes on first use.

Discover the current host's actual tools and authorized connections before choosing execution. An available Voicebox MCP connection in Claude Desktop or another host can provide a native route; a local executor may expose an existing engine. Use the registry's exact host/engine route and verify it, without assuming that a host name proves availability. If no supported runtime or authorized connection exists, deliver the script, voice direction (voice, pace, pauses, pronunciation, emotion per line) and engine settings for the user's local generation.

## 4. Consent and delivery

Clone a voice only with its owner's documented permission (the user's own voice, or a speaker who agreed in writing); never imitate a real person, a celebrity or a client's competitor. Mark a synthetic voice where the platform or the law asks. Record the engine, model, version, licence and the voice source in the delivery notes.

After generation, measure the read against the [voice-over budget](../../pipeline-core/references/short-form-timing.md), listen for wrong stress in names and numbers, regenerate only the faulty lines, and hand the files to the mix (in a motion film, Motion Graphics's sound step).
