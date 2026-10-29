# Native Earshot routing

Earshot (v0.4.0 by Leon Lin, MIT, pinned to `591fa3e`) comes to Studio only as the capability built into FrameCore Works Toolbox (owner decisions 2026-10-29): skill `toolbox:toolbox`, launcher `capabilities/earshot/scripts/runtime.py` in the Toolbox plugin, with `capabilities/earshot/scripts/envelope.py` as the entry point for a caller's task. Use it for sound analysis, procedural SFX, sound kits and audio-to-picture verification. Resolve and actually read the skill through the current host catalog. Studio owns the brief, creative choices, acceptance and final edit. Toolbox runs Earshot and returns evidence; Superpowers supplies the selected planning/debugging/verification method. None of these names proves execution or adds permissions.

There is no other Earshot route: no `earshot-audio` plugin, no `earshot-local` binary, no engine bridge in Studio's `listen.py` and no bare venv interpreter. Studio never resolves an Earshot root or binary; Toolbox owns the runtime root, its `candidates` and its consent questions. The request and result shapes are in [companion routing](companion-routing.md).

Without `toolbox:toolbox` in the skill list, offer FrameCore Works Toolbox once (it is the one Earshot route; [first companion setup](../../workflow-orchestrator/references/extensions.md#first-companion-setup) has the steps) or use Studio's own `listen.py`, `sound.py` and `synth.py`, and name the engine that actually ran. Never claim an Earshot run that did not happen.

When the skill is listed but Toolbox's `status` reports `unavailable` (owner decision 2026-10-23), ask one question with both routes: install Earshot through Toolbox, full (about 2.6 GB, chooses sounds by listening) or light (about 200 MB, measures only), saying what is written, local, from the pinned commit, or make the sound now with Studio's own `sound.py`/`synth.py` and check it with `listen.py`. Run neither before the answer, never fall back silently, and say which engine made the delivered sound. Toolbox returns that setup as `needs_consent` with its own plan; Studio relays the one question and does not restate Earshot's requirements. A runtime Toolbox lists under `candidates` (for example an earlier Studio-built `~/.framecore-studio/extensions/earshot`) is the user's choice: pass it as `constraints.runtime_root` only after the user picks it; an `unlocked_legacy` root is labelled in every result.

Pass each cue's character (from the picture and the request, e.g. a heavy landing: a deep dull thud, no metallic tail) to Earshot and accept a take only with its selection readings: ranked candidates, a match against likely confusions, onsets per second and speaker-audible bands (owner report 2026-10-23: a preset's hit with a debris tail). On the light tier only the measurement gates run (onsets per second, bands, duration); say that recognition (`rank`, `match`) needs the full tier and offer it. With Studio's own engine, apply the same measurement checks with `listen.py`.

`llm` and `mcp` are out of scope (owner decision 2026-10-22): no audio goes to Gemini or any other model service, no MCP server is installed or started, and Studio does not configure keys for them. Earshot runs locally through Toolbox; a request to send audio to an external model is declined with the local route offered instead.

## Route by the task

| Trigger | Owner and native operation |
|---|---|
| Authorized sound for motion graphics, kinetic type, transitions, UI, reveals or logo cues | Motion Graphics asks Toolbox for SFX/kit generation when ready, then implements the mix against existing motion-score cues. Preserve a selected Remotion or other visual engine. |
| FrameCut needs generated effects or checks of speech/music/SFX timing | FrameCut delegates through the existing motion/audio owners with its current revision, rational FPS, cue mapping and master timeline. Toolbox returns assets and evidence to that owner. |
| Supplied audio needs description, candidate ranking, trimming or semantic comparison | Audio Production asks Toolbox for the corresponding Earshot analysis command and reports model availability and uncertainty. |
| Finished soundtrack/delivered MP4 needs objective QA | Ask Toolbox for the applicable Earshot measurement/timeline/sheet checks within the existing bounded QA. Select a genre-appropriate critique profile. |
| Runtime or technical failure | `superpowers:systematic-debugging` when available: read the result's `errors[]`, `readiness` and `commands_run[]`, identify the real failing tier or blocked host before repairing or offering the fallback. |
| Code around Earshot (scripts on `earshot.api`, cue files, placement, mix, mux) | Superpowers' method ([sound with Earshot](superpowers-native-routing.md#sound-with-earshot)): a plan for a multi-step soundtrack, a failing onset check per cue before the mix, verification on the encoded MP4 before reporting done. |

Earshot through Toolbox is the preferred procedural SFX/kit engine when available and appropriate. Existing `sound.py`, `synth.py`, `listen.py`, mixing/mastering and placement tools remain available for their supported roles and fallback. Do not make every audio task run all tools or repeat QA. Earshot does not supply general music generation, voice synthesis or speech transcription. Recorded-only briefs use licensed recordings rather than mislabelling procedural takes as recorded.

## Capability and initialization

Read the Toolbox skill and its Earshot instructions (readiness and consent first). Toolbox runs `status` at the actual materialized plugin path and distinguishes native plugin availability, `light_ready`, cached neural files, successful model inference and task-specific verified results; Studio reads them from the returned `readiness`. Ordinary runs default to offline. Installation, model downloads, model reuse and source attachment are Toolbox operations that print a plan and run only after the user agrees. No automatic external audio upload follows from installing Toolbox.

Judge ChatGPT, ChatGPT Work, Codex and other hosts by available execution, files and dependencies, not a blanket brand-level support flag. A shell-less host gets a precise plan/handoff with execution unavailable. A saved plugin persists; a sandbox runtime may need restoration. No global remote server, runtime synchronization or MCP endpoint is implied. Do not initialize, modify or push a project repository for this native integration.

Studio's `listen.py` keeps its own model-free measurements; its Earshot command names (`describe`, `match`, `kit` and the rest) exit 4 with a pointer to Toolbox and start nothing. Keep the native catalog path dynamic.

## Handoff and timing

Send a `framecore-task-request/1` ([companion routing](companion-routing.md)) with `provider.capability: "earshot"` and include project/revision, asset paths/hashes, owner, operation, exact `fps_num/fps_den`, frame-index convention, local/global origin, source trim/speed mapping, sample rate, cue ID/frame, requested onset/peak/end anchor, palette/rights and acceptance criteria. Use the same Project State, accepted board and FrameCut master clock.

Convert zero-based frame `f` as `f * fps_den / fps_num`; place the take at `round(t * sample_rate) - round(measured_anchor_s * sample_rate)`. Use measured anchors from `kit.lock.json` or SFX output. Export numeric fps and explicit seconds for Earshot 0.4.0's cue reader; retain rational metadata in Studio. `30000/1001` is not an accepted string fps in Earshot's parser. Account for offsets/retiming once; resolve negative placement rather than silently clipping the onset.

Toolbox returns a `framecore-task-result/1`: runtime/model readiness, actual commands, audio paths/hashes, kit lock, measured onset/peak/end, warnings, errors and what did not run. Check it with [companion intake](../../delivery-documentation/scripts/companion_intake.py) (re-hashes every output, records `not_reviewed`) before placing anything on the master timeline. Reuse accepted generated assets for later renders. Models and scores do not prove taste, licences or recorded provenance; `timeline --detail low` still requires CLAP. A failed or unavailable neural route may use clearly labelled Studio measurement fallback.

Inspect the final encoded MP4 for the checked synchronization and audio scope, not just a source WAV. Retain valid storyboard acceptance; technical repairs do not restart intake. New films follow the existing full-board gate. Intentionally silent deliveries stay silent without sound authorization.

## Maintenance

Keep this reference, the shared policy link, the companion registry and the `framecore-works-toolbox` extension record together. Toolbox owns the Earshot pin, launcher and instructions; Studio records which Toolbox release it reviewed. Preserve the separate Superpowers route. This integration creates no automatic synchronization.

## External asset sourcing

Use [Open Assets native routing](open-assets-native-routing.md) for external audio. Studio forwards the Open Assets file and its `.asset.json` to Toolbox's separate `import_source_record` tool; Toolbox checks bytes and its narrower rights policy, then audits and measures it; Studio retains the brief and timeline. Do not call Openverse or re-download a received file.
