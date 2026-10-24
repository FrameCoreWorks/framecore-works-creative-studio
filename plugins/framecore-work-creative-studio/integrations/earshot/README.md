# earshot: decision map

## Current route (2026-10-23): one Earshot

There is one Earshot route on every host: the public `earshot-audio` plugin in this repository ([plugins/earshot-audio](https://github.com/FrameCoreWorks/framecore-works-creative-studio/tree/main/plugins/earshot-audio), skill `earshot-audio:earshot`), Earshot v0.4.0 by Leon Lin (MIT) pinned to `591fa3e`. Its `runtime.py` (`status | install --tier light|full | fetch-models | run | exec`) installs the pinned engine into `~/.framecore-studio/extensions/earshot` after the user agrees, checking all 282 upstream files, and runs it offline with its own model cache; `llm` (Gemini) and `mcp` are refused and stubbed out. Light is about 200 MB (measure, `critique --fast`, `sfx`, `kit`); full adds CPU PyTorch and about 1.1 GB of CLAP and AST models (`timeline`, `sheet`, `describe`, `match`, `rank`, `find`, `compare`, `ab`, `realness`, full `critique`, and the choice of effects by listening).

- **Setup.** First configuration offers it second, after Superpowers, in plain words with a choice of full, light or not now, and installs the plugin and the chosen tier where code runs (ChatGPT Work, Claude Code, Codex): [first companion setup](../../skills/workflow-orchestrator/references/extensions.md#first-companion-setup).
- **Routing.** [Native Earshot routing](../../skills/pipeline-core/references/earshot-native-routing.md): Motion Graphics, FrameCut, Audio Production and Remotion name the skill; listed without its engine, Studio asks before using its own tools; every effect is chosen by listening; Superpowers supplies the method for the code around it.
- **Studio's own tools** (`listen.py`, `place_sfx.py`, `sound.py`, `synth.py`) are the fallback the user may choose, named when they run; `listen.py`'s model commands pass through to the same plugin-installed engine.
- **Superseded:** the owner's private adapter (Earshot 0.3.0, `925ebe5`) and the registry's own pip installation (2026-10-20 to 2026-10-23). The decisions below are the 2026-10-20 review of 0.3.0, kept as history; where they name "the registry entry" or "the extension", read the earshot-audio plugin.
- **Evidence:** light and full tiers through the plugin in Claude Code with an end-to-end film and the owner's listening choice (`verification/earshot-audio-1.0.3-full-tier.json`, `verification/earshot-audio-1.0.4-listening.json`).

## Decisions (2026-10-20 review of 0.3.0, history)

Reviewed 2026-10-20 at [`925ebe5`](https://github.com/Leonxlnx/earshot/tree/925ebe56a1b755e5d354ab642bb8f344440cfa9c) (version 0.3.0, MIT, Copyright (c) 2026 Leon Lin, [licence](LICENSE)) after the owner sent the repository and asked for every capability to be implemented next to Studio's existing skills. Studio rewrites the model-free half in its own code and keeps the model half as a pinned extension; no earshot source file is copied.

| earshot capability | Decision | Where in Studio |
| --- | --- | --- |
| `measure` (LUFS, LRA, true peak, spectrum, stereo, onsets, tempo, key) | adapted, own code (NumPy, FFmpeg) | [`listen.py measure`](../../skills/hyperframes-workflow/assets/sound-listen/README.md) |
| `timeline`, `sheet` (listening transcript and annotated picture) | adapted | `listen.py timeline`, `listen.py sheet` |
| sync of sound to cuts and cue frames, salient hits, stop-downs, picture-event detector | adapted | `listen.py sync`, `timeline` |
| `critique` (launch-film scorecard with timed fixes) | adapted without the model rows; the verdict says it is partial | `listen.py critique`; ranges from earshot's seven films, marked as SaaS launch style |
| `profile` (your own reference ranges) | adapted | `listen.py profile`, `critique --profile` |
| `ab` (two sounds in words) | adapted for the measured differences | `listen.py ab` |
| sound audit (clicks, cut tail, clipping, DC, glide) | adapted | `listen.py check` |
| sfx and kit placement on frames (sound aimed at the picture, measured onset and peak) | adapted as a placement tool for any sample the user may use | [`place_sfx.py`](../../skills/hyperframes-workflow/assets/sound-listen/README.md#place-samples-on-the-frames); Studio's own designed sound stays `sound.py` |
| `describe`, `match`, `rank`, `find`, `compare`, `realness` (CLAP and AST models) | not rewritten: needs PyTorch and about 1.1 GB of models | registry entry `earshot`, full tier; `listen.py describe ...` passes through when the extension is installed |
| bank of 201 code-made sound effects (`sfx`, `kit`), `forge`, `fit`, `gallery`, `mcp`, `doctor` | not rewritten: a large library with its own benchmark | registry entry `earshot`, light tier for `sfx` and `kit`; Studio's `synth.py` and `sound.py` stay the default for designed sound |
| `llm` (audio-LLM critique through Gemini) and `mcp` (its MCP server) | outside the integration (owner decision 2026-10-22) | Earshot runs locally only; no audio upload and no MCP server |
| Motion-design SFX study (what professional effects are made of) | restated in Studio's own words with the owner-relevant targets | [sound listening and motion SFX](../../skills/hyperframes-workflow/references/sound-listening-and-motion-sfx.md) |
| Third-party reference films and trims | not used, not copied | earshot kept them local; Studio ships none |

Evidence (2026-10-20, Linux container, CPU): earshot installed from the pinned commit in two tiers; on a 16.7 s film Studio rendered, its LUFS, LRA and true peak agreed with `listen.py` to a few tenths; cuts-with-sound (54 % against 38 %), sub-band level (2 to 3 dB), onsets per second (3.65 against 3.05) and tempo detection differed, so those are approximations in `listen.py` and earshot is the reference. earshot's realness model flagged Studio's code-made sound as likely synthesized, which is information and not a defect.

Registry entry: `earshot` in [extensions.json](../../skills/workflow-orchestrator/assets/extensions/extensions.json). No host installation through the registry was run.
