# earshot: decision map

## Native plugin route (2026-10-22)

The owner built a separate native plugin, `earshot-audio` (skill `earshot-audio:earshot`), that bundles the pinned upstream source (`925ebe5`, 259 files checked against their SHA-256), its licence and a runtime launcher (`runtime.py status | install --tier light|full | fetch-models | run`). Studio routes to it through [native Earshot routing](../../skills/pipeline-core/references/earshot-native-routing.md): Motion Graphics, FrameCut, Audio Production Director and Remotion name the skill directly and use it when it is in the skill list. Without it (most Claude Code and Codex users), the pinned command line from the registry runs the same engine, or Studio's own tools run and are named as such. Local only: `llm` (Gemini) and `mcp` are outside the integration. Evidence of the native plugin comes from the owner's ChatGPT Work run reported in the handover; the pair was not run in Claude Code here.

## Decisions (2026-10-20 review)

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
