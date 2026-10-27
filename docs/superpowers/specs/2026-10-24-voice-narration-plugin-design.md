# voice-narration: a public voice-over plugin beside Studio

Date: 2026-10-24. Status: approved in conversation section by section; this spec awaits the owner's review.

## Intent

The owner chose "Voice and narration" from the five companion proposals in `https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/8a8c78c8b15be8934b32c49c88c30413f185c387/docs/handover-development-proposals-2026-10-24.md`. Studio already describes five local text-to-speech engines and helps a user choose (`skills/audio-production-director/references/local-tts-engines.md`), but it neither generates nor measures a read. Motion graphics and FrameCut are Studio's main paid uses, and a voice-over is a direct input to both.

Success: a user installs `voice-narration` from this repository's marketplace next to Studio, hands it an approved script with per-line time limits, and receives one WAV per line, measured against those limits, with a lock file that FrameCut or Motion Graphics Workflow takes into the mix. Nothing is installed, downloaded, cloned or paid for without the user's yes.

Owner decisions in this conversation (2026-10-24):

- Engines in version 1: Voicebox and VoxCPM2 locally, plus ElevenLabs in the cloud. OmniVoice, MOSS-TTS and MOSS-TTSD stay described in Studio only.
- ElevenLabs only through the host app's connector; no API key in files or scripts.
- VoxCPM2 is installed by the plugin with consent, Earshot-style: a printed plan, then a pinned isolated environment; model weights are fetched separately with their own consent.
- Local engines run only on the user's own computer (owner, 2026-10-24): Claude Code or Codex on a desktop or laptop, or Claude Desktop with a local Voicebox. Their libraries and weights are large and belong on a persistent local disk. In a phone app or a cloud environment (Claude Code on the web or mobile, Codex cloud, ChatGPT or ChatGPT Work on a phone) installing them is advised against; ElevenLabs through the connector, or the script with voice direction, is the route there.
- Approach: a separate plugin modelled on `plugins/earshot-audio/` (one skill, one standard-library launcher). Rejected: adding this to Studio's shared package (maintenance mode, permanent paths) and a custom MCP server (avoided for Earshot too).

## Structure

New directory `plugins/voice-narration/`, listed in `.claude-plugin/marketplace.json` beside Studio and Earshot, with `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` and `plugin.json`. Plugin version starts at 1.0.0. Working display name `Voice And Narration`, following the plain role names in the pending naming list; it changes if the owner picks the FrameCore-qualified direction.

| Path | Content |
| --- | --- |
| `skills/narrate/SKILL.md` | The only skill, `voice-narration:narrate`, with `agents/openai.yaml` display metadata per `docs/skill-naming.md`. Readiness, consent and honest reporting first; then engine choice, lexicon, generation, measurement and handoff. |
| `skills/narrate/references/elevenlabs-connector.md` | How to run a read through the host's ElevenLabs connector. |
| `skills/narrate/references/formats.md` | The cue sheet, lexicon and lock file formats with examples. |
| `scripts/runtime.py` | The launcher (below). Standard library only, Python 3.10+. |
| `tests/runtime_test.py`, `tests/package_test.py` | Repository tests, wired into `scripts/check_all.sh`. |
| `LICENSE`, `NOTICE`, `README.md`, `CHANGELOG.md` | Licence, engine credits (Voicebox MIT, VoxCPM Apache-2.0, pinned commits from `integrations/tts-engines/README.md`), description, history. |

No engine code or model is vendored.

## Launcher (`scripts/runtime.py`)

- `status [--json]`: the environment (`local` or `cloud`: cloud when a known sandbox marker is set, such as `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` or Codex cloud's task variables, otherwise local; `unknown` is reported as such), Python, venv path, installed `voxcpm` version, whether weights are cached, whether the Voicebox API answers on `127.0.0.1:17493`, FFmpeg/FFprobe presence, GPU memory when detectable. Never installs or downloads; missing pieces report `unavailable`.
- `install voxcpm [--yes]`: without `--yes` prints what is written, where (`~/.framecore-studio/extensions/voxcpm`, or `--root`, `VOICE_NARRATION_ROOT`) and approximate size, and exits 0 without writing. In a `cloud` environment the plan leads with a warning that the files land on a temporary disk and are lost with the session, and `--yes` is refused unless `--allow-cloud` is also given. With `--yes`: creates the venv and installs `voxcpm==2.0.3`, the version reviewed on 2026-10-16.
- `fetch-models [--yes]`: downloads the VoxCPM2 weights (several GB), separately and only with consent.
- `generate --engine voxcpm|voicebox --cues cues.json [--lexicon lexicon.json] --out DIR [--only LINE_ID...]`: applies the lexicon, generates one WAV per cue line, writes or updates `narration.lock.json`. VoxCPM2 runs from the venv with model caches in offline mode; Voicebox through `POST /generate` on its local API. A failed line is recorded as failed while the others are kept; `--only` regenerates selected lines.
- `measure --cues cues.json --out DIR [--json]`: duration of each WAV with trailing silence excluded (standard-library `wave`, threshold-based), compared with each line's limit; reports `fits`, `over` with seconds over, or `missing`.
- `stretch LINE_ID --percent N --out DIR [--yes]`: FFmpeg `atempo` speed-up of at most 5%, only with `--yes`, recorded in the lock file.
- Any other command is refused with exit 2 before a process starts.

ElevenLabs is not called by the script. The skill drives the connector (voice list, speech generation) and records the result in the same lock file format.

## Formats

- **Cue sheet** `cues.json`: ordered lines `{id, text, max_seconds, voice_notes?}`, from the board plan or a FrameCut timeline. Text comes from Copy Voice with locked facts intact.
- **Lexicon** `lexicon.json`: per project, `{word: spoken_form}` (for example `"FrameCore": "frejm kor"`), applied as whole-word text substitution identically for every engine. A lexicon belongs to one project, so one client's terms never reach another's. Its SHA-256 is recorded per generation.
- **Lock** `narration.lock.json`: per line the engine, model and version, voice source and consent reference (for a cloned voice), the text actually sent, duration, limit, verdict, any stretch, WAV path and SHA-256, and the lexicon hash.

## Behaviour (skill text)

1. Check readiness with `status` before promising a result; plugin visible, engine installed, weights cached and a finished read are separate facts.
2. Local engines are for the user's own computer. In a phone app or a cloud environment, advise against installing them, say why (several GB on a temporary disk, no GPU, lost with the session) and offer ElevenLabs through the connector or the script with voice direction; install there only if the user insists after that warning. Voicebox is never reachable from a cloud environment, because its API listens on the user's own machine.
3. Ask which engine when the user has not said; describe the three with Studio's comparison when they do not know. Never switch engines silently: when Voicebox does not answer, the connector is missing or the GPU is too small, say so and offer another route or the script with voice direction for the user's own recording.
4. Clone a voice only with the owner's recorded consent; refuse otherwise. No imitation of real people.
5. ElevenLabs: ask before spending credits, name the chosen voice, never retry automatically (each attempt costs credits).
6. After generation run `measure`. For a line over its limit change nothing; propose, in order: shorten the text through Copy Voice keeping locks; regenerate that line at a faster pace; a speed-up of at most 5% with the user's consent.
7. Pronunciation check: a person listens, always. Automatic transcription through the ElevenLabs connector is optional and needs separate consent, because it uploads the audio and spends credits.
8. Handoff: the WAV files and `narration.lock.json` go to FrameCut (master timeline) or Motion Graphics Workflow (sound step). Studio keeps brief, copy locks and final review.

## Studio changes

Done only after the in-flight display-name release has landed on `main`, rebased onto it, and announced to the coordinator before pushing:

- Registry entry `voice-narration` in `skills/workflow-orchestrator/assets/extensions/extensions.json` (category `tts`), install from this marketplace, plan, verify and remove steps.
- One link from `skills/audio-production-director/references/local-tts-engines.md` section 3 to the plugin as the generation route. No path is deleted or moved.
- Released as a new Studio minor version; the hosted ChatGPT plugin is recorded `pending` with the ready prompt from `CHATGPT_UPDATE.md`.

## Verification

- Repository: `runtime_test.py` covers lexicon substitution (whole words, case, no cross-project leakage), measurement on synthetic WAVs written by `wave` (with and without trailing silence), limit verdicts, the install plan writing nothing without `--yes`, cloud detection and the `--allow-cloud` refusal, refusal of unknown commands, the Voicebox client against a fake local HTTP server, lock file contents and `--only` regeneration. `package_test.py` checks manifests, versions and skill metadata. Both run in `scripts/check_all.sh`; the Studio validator and the full check suite pass.
- The cloud warning is checked in a Claude Code cloud session (this environment) by running `status` and the install plan.
- Real generation with VoxCPM2 and Voicebox needs a GPU or the desktop app and is `NOT_RUN` until the owner tests it on their computer (`PASS_REPORTED` then).
- An ElevenLabs connector read is run in a cloud session only with the owner's consent to spend credits.
- Acceptance proof for release: a known Polish script to actual WAVs, measured durations against limits, a lexicon word read as written, the consent rule exercised for cloning, and unsupported-host behaviour (no engine, no connector) giving the script handoff.

## Out of scope for version 1

OmniVoice, MOSS-TTS, MOSS-TTSD; an ElevenLabs API-key route; automatic text shortening; music or sound effects (Earshot, Audio Production Director); lip sync.
