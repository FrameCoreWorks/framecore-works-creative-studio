# Native Earshot routing

Use the public plugin `earshot-audio` from this repository's marketplace (Earshot v0.4.0 by Leon Lin, pinned to `591fa3e`), skill `earshot-audio:earshot`, for sound analysis, procedural SFX, sound kits and audio-to-picture verification. Resolve and actually read the skill through the current host catalog. Studio owns the brief, creative choices, acceptance and final edit. Earshot supplies the audio engine; Superpowers supplies the selected planning/debugging/verification method. None of these names proves execution or adds permissions.

Without the `earshot-audio` plugin in the skill list, offer it once (it is the one Earshot route; first companion setup has the steps) or use Studio's own `listen.py`, `sound.py` and `synth.py`, and name the engine that actually ran. Never claim an Earshot run that did not happen.

When the skill is listed but `runtime.py status` reports `unavailable` (owner decision 2026-10-23), ask one question with both routes: install Earshot's light tier (what is written, about 200 MB, local, from the pinned commit) or make the sound now with Studio's own `sound.py`/`synth.py` and check it with `listen.py`. Run neither before the answer, never fall back silently, and say which engine made the delivered sound.

Pass each cue's character (from the picture and the request, e.g. a heavy landing: a deep dull thud, no metallic tail) to Earshot and accept a take only with its selection readings: ranked candidates, a match against likely confusions, onsets per second and speaker-audible bands (owner report 2026-10-23: a preset's hit with a debris tail). With Studio's own engine, apply the same measurement checks with `listen.py`.

`llm` and `mcp` are out of scope (owner decision 2026-10-22): no audio goes to Gemini or any other model service, no MCP server is installed or started, and Studio does not configure keys for them. Earshot runs locally through its skill, CLI or Python; a request to send audio to an external model is declined with the local route offered instead.

## Route by the task

| Trigger | Owner and native operation |
|---|---|
| Authorized sound for motion graphics, kinetic type, transitions, UI, reveals or logo cues | Motion Graphics Workflow delegates SFX/kit generation to Earshot when ready, then implements the mix against existing motion-score cues. Preserve a selected Remotion or other visual engine. |
| FrameCut needs generated effects or checks of speech/music/SFX timing | FrameCut delegates through the existing motion/audio owners with its current revision, rational FPS, cue mapping and master timeline. Earshot returns assets and evidence to that owner. |
| Supplied audio needs description, candidate ranking, trimming or semantic comparison | Audio Production Director uses the corresponding Earshot analysis command and reports model availability and uncertainty. |
| Finished soundtrack/delivered MP4 needs objective QA | Run the applicable Earshot measurement/timeline/sheet checks within the existing bounded QA. Select a genre-appropriate critique profile. |
| Runtime or technical failure | `superpowers:systematic-debugging` when available: read the actual error and `runtime.py status --json`, identify the real failing tier or blocked host before repairing or offering the fallback. |
| Code around Earshot (scripts on `earshot.api`, cue files, placement, mix, mux) | Superpowers' method ([sound with Earshot](superpowers-native-routing.md#sound-with-earshot)): a plan for a multi-step soundtrack, a failing onset check per cue before the mix, verification on the encoded MP4 before reporting done. |

Earshot is the preferred procedural SFX/kit engine for the requested native integration when available and appropriate. Existing `sound.py`, `synth.py`, `listen.py`, mixing/mastering and placement tools remain available for their supported roles and fallback. Do not make every audio task run all tools or repeat QA. Earshot does not supply general music generation, voice synthesis or speech transcription. Recorded-only briefs use licensed recordings rather than mislabelling procedural takes as recorded.

## Capability and initialization

Read the Earshot skill's runtime reference and run its bundled `runtime.py status` at the actual materialized skill path. Check the returned interpreter and binary; PATH absence alone is insufficient. Distinguish native plugin availability, `light_ready`, cached neural files, successful model inference and task-specific verified results. Ordinary runs default to offline. With an authorized installation/restore scope, use the bundled installer and explicit model-fetch action. No automatic external audio upload follows from installing either plugin.

Judge ChatGPT, ChatGPT Work, Codex and other hosts by available execution, files and dependencies, not a blanket brand-level support flag. A shell-less host gets a precise plan/handoff with execution unavailable. A saved plugin persists; a sandbox runtime may need restoration. No global remote server, runtime synchronization or MCP endpoint is implied. Do not initialize, modify or push a project repository for this native integration.

The established Studio bridge can use the verified `EARSHOT_BIN` or `listen.py ... --earshot <binary>`; the bundled default runtime also uses its existing discoverable installation folder. Keep the native catalog path dynamic. Preserve any user-selected interpreter or known authorized installation instead of inventing a cache path.

## Handoff and timing

Include project/revision, asset paths/hashes, owner, operation, exact `fps_num/fps_den`, frame-index convention, local/global origin, source trim/speed mapping, sample rate, cue ID/frame, requested onset/peak/end anchor, palette/rights and acceptance criteria. Use the same Project State, accepted board and FrameCut master clock.

Convert zero-based frame `f` as `f * fps_den / fps_num`; place the take at `round(t * sample_rate) - round(measured_anchor_s * sample_rate)`. Use measured anchors from `kit.lock.json` or SFX output. Export numeric fps and explicit seconds for Earshot 0.4.0's cue reader; retain rational metadata in Studio. `30000/1001` is not an accepted string fps in Earshot's parser. Account for offsets/retiming once; resolve negative placement rather than silently clipping the onset.

Return runtime/model status, actual commands, audio paths/hashes, kit lock, measured onset/peak/end, cue mapping, QA evidence, limitations and next owner. Reuse accepted generated assets for later renders. Models and scores do not prove taste, licences or recorded provenance; `timeline --detail low` still requires CLAP. A failed or unavailable neural route may use clearly labelled Studio measurement fallback.

Inspect the final encoded MP4 for the checked synchronization and audio scope, not just a source WAV. Retain valid storyboard acceptance; technical repairs do not restart intake. New films follow the existing full-board gate. Intentionally silent deliveries stay silent without sound authorization.

## Maintenance

Keep this reference, the shared policy link and the Earshot extension record together during native package updates. Preserve the separate Superpowers route. Future repository-to-plugin replacement must reconcile these native changes against the then-current release; this integration creates no automatic synchronization.
