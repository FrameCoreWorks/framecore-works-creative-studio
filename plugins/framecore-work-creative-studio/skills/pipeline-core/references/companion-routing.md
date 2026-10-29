# Companion routing

Studio is the orchestrator. FrameCore Works Toolbox (skill `toolbox:toolbox`) and FrameCore Open Assets (skill `framecore-open-assets:open-assets`) are standalone companions: each installs and works without Studio, and Studio declares no dependency on either (owner decisions 2026-10-29). Studio chooses when to ask a companion, sends one task, and checks what comes back. A companion never invokes Studio or another companion; it returns its result to the caller.

The [companion registry](../assets/companion-registry.json) lists each companion, its skill, its capabilities and operations, the minimum contract version and the release Studio reviewed. The [shared contract schema](../assets/companion-contract.schema.json) is byte-identical in all three repositories (SHA-256 `e7cc0f4e612395768e8c8c6cf2a033a555bc69b4c8ea5ca45c4db019a342897a`); no code is shared.

## Choosing a companion

| Need | Companion and capability | Without it |
|---|---|---|
| Sound analysis, procedural SFX, sound kits, audio-to-picture sync checks | Toolbox, capability `earshot` ([Earshot routing](earshot-native-routing.md)) | Studio's `listen.py`, `sound.py`, `synth.py`, named as the engine that ran |
| Openly licensed photos, graphics, audio, music, SFX or video from public sources | Open Assets, capability `open-assets` ([Open Assets routing](open-assets-native-routing.md)) | Explain the gap; ask before installing or changing route |
| A reviewed third-party plugin for a task (catalog) | Toolbox catalog: read its index and offer the entry once | Studio's own owner |

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
