# Companion routing

Studio is the orchestrator. FrameCore Works Toolbox (skill `toolbox:toolbox`) and FrameCore Open Assets (skill `framecore-open-assets:open-assets`) are standalone companions: each installs and works without Studio, and Studio declares no dependency on either (owner decisions 2026-10-29). Studio chooses when to ask a companion, sends one task, and checks what comes back. A companion never invokes Studio or another companion; it returns its result to the caller.

## Skill names by host

Hosts list the same companion skill under different names (2026-10-31 Codex retest). Claude, and Codex plugins installed with `codex plugin add` (checked 2026-10-31): `toolbox:toolbox` and `framecore-open-assets:open-assets`. Codex native entries from the companions' older installers: `toolbox` and `open-assets`. Another host: the name its catalog shows for that plugin's skill. Any of these names in the host's skill list means the companion is installed; never report it missing because the Claude name is absent. The registry's `skill_names` keeps this mapping. In this file and the skills, `toolbox:toolbox` and `framecore-open-assets:open-assets` stand for the companion under whatever name the host lists.

The [companion registry](../assets/companion-registry.json) lists each companion, its skill, its capabilities and operations, the minimum contract version and the release Studio reviewed. The [shared contract schema](../assets/companion-contract.schema.json) is byte-identical in all three repositories (SHA-256 `e7cc0f4e612395768e8c8c6cf2a033a555bc69b4c8ea5ca45c4db019a342897a`); no code is shared.

## Choosing a companion

| Need | Companion and capability | Without it |
|---|---|---|
| Sound analysis, procedural SFX, sound kits, audio-to-picture sync checks | Toolbox, capability `earshot` ([sound through Toolbox](#sound-through-toolbox)) | Studio's `listen.py`, `sound.py`, `synth.py`, named as the engine that ran |
| Openly licensed photos, graphics, audio, music, SFX or video from public sources | Open Assets, capability `open-assets` ([Open Assets routing](open-assets-native-routing.md)) | Explain the gap; ask before installing or changing route |
| A reviewed third-party plugin, skill or app for a task (the tools FrameCore Works recommends) | Toolbox catalog: read its index and offer the entry once | Studio's own owner |

Resolve the companion's skill from the host's catalog and read it before asking. A skill name in this file does not prove the companion is installed, ready or allowed to run anything.

## Request

Studio describes the task as a `framecore-task-request/1`:

- `task_id`: `<project>:<item>` from Project State, reused on a resume (`resume_of`).
- `origin: "studio"`, `requester: {"plugin": "framecore-work-creative-studio"}`, `owner`: the Studio owner skill that asked.
- `provider`: `plugin`, `capability`, `operation` and, for Earshot `run`, `command` (for example `sfx`, `measure`, `kit`).
- `inputs`: local paths with SHA-256; `parameters`: the operation's own options; `acceptance`: what Studio will check.
- `constraints`: limits such as `runtime_root` (only a root the user picked from Toolbox's `candidates`), tier or offline.
- `consent`: what the user already agreed to, in their words; empty means nothing was agreed.

Hosts with a shell run the companion's own launcher (Toolbox `capabilities/earshot/scripts/envelope.py`, Open Assets `scripts/runtime.py --envelope-out`); the companion's skill gives the exact command. A shell-less host gets the request as a plan and no run is claimed.

### Toolbox Earshot operations

| Studio intent | Operation | Changes anything? |
|---|---|---|
| Is Earshot ready, which runtime roots exist | `status` | No |
| Set up the light or full tier | `plan_install`, then `install` after consent | Writes the runtime root |
| Download the models | `plan_fetch_models`, then `fetch_models` after consent | Writes the model cache |
| Reuse models from another root | `plan_reuse_models`, then `reuse_models` after consent | Links or copies into the chosen root |
| Add the real-sound source to a root | `plan_attach_source`, then `attach_source` after consent | Writes the source snapshot |
| Measure, rank, match, render SFX or a kit, review sync | `run` with `command` | Writes declared outputs only |
| Real-sound script from a verified recording | `real_sound_script` | Writes declared outputs only |
| Bring an Open Assets file into Earshot | `import_source_record` (a separate Toolbox tool, not an envelope operation) | Writes a source record |

`exec` is user-only and is never requested by Studio. A plan operation returns `needs_consent` with Toolbox's plan; Studio relays it as one question and runs the follow-up only after the user agrees.

## Result

The companion returns a `framecore-task-result/1`: `status` (`succeeded`, `partial`, `needs_input`, `needs_consent`, `blocked`, `refused`, `failed`, `cancelled`), `readiness` (`ready`, `ready_full`, `ready_light`, `unlocked_legacy`, `unavailable`, `blocked_host`), the commands that actually ran, inputs and outputs with SHA-256, verification evidence, warnings, errors and `unexecuted_checks`.

Before anything goes on a timeline, board or delivery, check the result with the [companion intake check](../../delivery-documentation/scripts/companion_intake.py):

```sh
python3 <studio>/skills/delivery-documentation/scripts/companion_intake.py check result.json --base <folder the companion ran in> --json
```

Relative output paths resolve against `--base` (default: the folder holding the result file). It validates the result against the shared schema, confirms the provider and operation are registered, re-hashes every declared output and compares its size, and returns a ledger entry with every output marked `not_reviewed`. `placeable` is true only for a `succeeded` or `partial` result whose outputs all verified. A failure (exit 1) means Studio uses nothing from that result and says why; exit 2 means the file could not be read. The check never opens media: listening, looking and acceptance stay with the Studio owner.

Record in Project State what the result says, not more: an `unlocked_legacy` run keeps its warning, a light-tier run says recognition did not run, and `unexecuted_checks` stay open. For Open Assets, the `.asset.json` sidecar, licence and attribution travel with the file into the [asset manifest](../../asset-manifest/SKILL.md); a verified download is not rights clearance for every use.

## Versions

Studio accepts contract major version 1 and the companions' `min_contract` from the registry. A result with another contract version or an unregistered capability or operation fails the intake check. A companion release older or newer than the reviewed one is used as reported, with an `intake_warnings` line naming both releases, and Studio says which release ran; it never guesses a mapping. Update the registry only after reviewing a companion release.

## Sound through Toolbox

Earshot (v0.4.0 by Leon Lin, MIT, pinned to `591fa3e`) comes to Studio only as the capability built into FrameCore Works Toolbox (owner decisions 2026-10-29): skill `toolbox:toolbox`, launcher `capabilities/earshot/scripts/runtime.py` in the Toolbox plugin, with `capabilities/earshot/scripts/envelope.py` as the entry point for a caller's task. Use it for sound analysis, procedural SFX, sound kits and audio-to-picture verification. Resolve and actually read the skill through the current host catalog. Studio owns the brief, creative choices, acceptance and final edit. Toolbox runs Earshot and returns evidence; Superpowers supplies the selected planning/debugging/verification method. None of these names proves execution or adds permissions.

There is no other Earshot route: no `earshot-audio` plugin, no `earshot-local` binary, no engine bridge in Studio's `listen.py` and no bare venv interpreter. Studio never resolves an Earshot root or binary; Toolbox owns the runtime root, its `candidates` and its consent questions. The request and result shapes are above.

Without the Toolbox skill in the skill list under any of its [host names](#skill-names-by-host), offer FrameCore Works Toolbox once (it is the one Earshot route; [first companion setup](../../workflow-orchestrator/references/extensions.md#first-companion-setup) has the steps) or use Studio's own `listen.py`, `sound.py` and `synth.py`, and name the engine that actually ran. Never claim an Earshot run that did not happen.

When the skill is listed but Toolbox's `status` reports `unavailable` (owner decision 2026-10-23), ask one question with both routes: install Earshot through Toolbox, full (about 2.6 GB, chooses sounds by listening) or light (about 470 MB, makes and measures sounds but does not choose them by listening), saying what is written, local, from the pinned commit, or make the sound now with Studio's own `sound.py`/`synth.py` and check it with `listen.py`. Run neither before the answer, never fall back silently, and say which engine made the delivered sound. Toolbox returns that setup as `needs_consent` with its own plan; Studio relays the one question and does not restate Earshot's requirements. A runtime Toolbox lists under `candidates` (for example an earlier Studio-built `~/.framecore-studio/extensions/earshot`) is the user's choice: pass it as `constraints.runtime_root` only after the user picks it; an `unlocked_legacy` root is labelled in every result.

Pass each cue's character (from the picture and the request, e.g. a heavy landing: a deep dull thud, no metallic tail) to Earshot and accept a take only with its selection readings: ranked candidates, a match against likely confusions, onsets per second and speaker-audible bands (owner report 2026-10-23: a preset's hit with a debris tail). On the light tier only the measurement gates run (onsets per second, bands, duration); say that recognition (`rank`, `match`) needs the full tier and offer it. With Studio's own engine, apply the same measurement checks with `listen.py`.

`llm` and `mcp` are out of scope (owner decision 2026-10-22): no audio goes to Gemini or any other model service, no MCP server is installed or started, and Studio does not configure keys for them. Earshot runs locally through Toolbox; a request to send audio to an external model is declined with the local route offered instead.

### Route by the task

| Trigger | Owner and native operation |
|---|---|
| Authorized sound for motion graphics, kinetic type, transitions, UI, reveals or logo cues | Motion Graphics asks Toolbox for SFX/kit generation when ready, then implements the mix against existing motion-score cues. Preserve a selected Remotion or other visual engine. |
| FrameCut needs generated effects or checks of speech/music/SFX timing | FrameCut delegates through the existing motion/audio owners with its current revision, rational FPS, cue mapping and master timeline. Toolbox returns assets and evidence to that owner. |
| Supplied audio needs description, candidate ranking, trimming or semantic comparison | Audio Production asks Toolbox for the corresponding Earshot analysis command and reports model availability and uncertainty. |
| Finished soundtrack/delivered MP4 needs objective QA | Ask Toolbox for the applicable Earshot measurement/timeline/sheet checks within the existing bounded QA. Select a genre-appropriate critique profile. |
| Runtime or technical failure | `superpowers:systematic-debugging` when available: read the result's `errors[]`, `readiness` and `commands_run[]`, identify the real failing tier or blocked host before repairing or offering the fallback. |
| Code around Earshot (scripts on `earshot.api`, cue files, placement, mix, mux) | Superpowers' method ([sound with Earshot](superpowers-native-routing.md#sound-with-earshot)): a plan for a multi-step soundtrack, a failing onset check per cue before the mix, verification on the encoded MP4 before reporting done. |

Earshot through Toolbox is the preferred procedural SFX/kit engine when available and appropriate. Existing `sound.py`, `synth.py`, `listen.py`, mixing/mastering and placement tools remain available for their supported roles and fallback. Do not make every audio task run all tools or repeat QA. Earshot does not supply general music generation, voice synthesis or speech transcription. Recorded-only briefs use licensed recordings rather than mislabelling procedural takes as recorded.

### Capability and initialization

Read the Toolbox skill and its Earshot instructions (readiness and consent first). Toolbox runs `status` at the actual materialized plugin path and distinguishes native plugin availability, `light_ready`, cached neural files, successful model inference and task-specific verified results; Studio reads them from the returned `readiness`. Ordinary runs default to offline. Installation, model downloads, model reuse and source attachment are Toolbox operations that print a plan and run only after the user agrees. No automatic external audio upload follows from installing Toolbox.

Judge ChatGPT, ChatGPT Work, Codex and other hosts by available execution, files and dependencies, not a blanket brand-level support flag. A shell-less host gets a precise plan/handoff with execution unavailable. A saved plugin persists; a sandbox runtime may need restoration. No global remote server, runtime synchronization or MCP endpoint is implied. Do not initialize, modify or push a project repository for this native integration.

Studio's `listen.py` keeps its own model-free measurements; its Earshot command names (`describe`, `match`, `kit` and the rest) exit 4 with a pointer to Toolbox and start nothing. Keep the native catalog path dynamic.

### Handoff and timing

Send a `framecore-task-request/1` ([request](#request)) with `provider.capability: "earshot"` and include project/revision, asset paths/hashes, owner, operation, exact `fps_num/fps_den`, frame-index convention, local/global origin, source trim/speed mapping, sample rate, cue ID/frame, requested onset/peak/end anchor, palette/rights and acceptance criteria. Use the same Project State, accepted board and FrameCut master clock.

Convert zero-based frame `f` as `f * fps_den / fps_num`; place the take at `round(t * sample_rate) - round(measured_anchor_s * sample_rate)`. Use measured anchors from `kit.lock.json` or SFX output. Export numeric fps and explicit seconds for Earshot 0.4.0's cue reader; retain rational metadata in Studio. `30000/1001` is not an accepted string fps in Earshot's parser. Account for offsets/retiming once; resolve negative placement rather than silently clipping the onset.

Toolbox returns a `framecore-task-result/1`: runtime/model readiness, actual commands, audio paths/hashes, kit lock, measured onset/peak/end, warnings, errors and what did not run. Check it with [companion intake](../../delivery-documentation/scripts/companion_intake.py) (re-hashes every output, records `not_reviewed`) before placing anything on the master timeline. Reuse accepted generated assets for later renders. Models and scores do not prove taste, licences or recorded provenance; `timeline --detail low` still requires CLAP. A failed or unavailable neural route may use clearly labelled Studio measurement fallback.

Inspect the final encoded MP4 for the checked synchronization and audio scope, not just a source WAV. Retain valid storyboard acceptance; technical repairs do not restart intake. New films follow the existing full-board gate. Intentionally silent deliveries stay silent without sound authorization.

### Maintenance

Keep this section, the shared policy link, the companion registry and the `framecore-works-toolbox` extension record together. Toolbox owns the Earshot pin, launcher and instructions; Studio records which Toolbox release it reviewed. Preserve the separate Superpowers route. This integration creates no automatic synchronization.

### External asset sourcing

Use [Open Assets native routing](open-assets-native-routing.md) for external audio. Studio forwards the Open Assets file and its `.asset.json` to Toolbox's separate `import_source_record` tool; Toolbox checks bytes and its narrower rights policy, then audits and measures it; Studio retains the brief and timeline. Do not re-download a received file.
