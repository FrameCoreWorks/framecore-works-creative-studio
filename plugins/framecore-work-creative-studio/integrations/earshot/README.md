# earshot: attribution

Studio's own sound tools (`listen.py`, `place_sfx.py` in `skills/hyperframes-workflow/assets/sound-listen/`) adapt definitions and measurements from [earshot](https://github.com/Leonxlnx/earshot) by Leon Lin (MIT, [licence](LICENSE)), rewritten in Studio's own code; no earshot source file is copied. The licence stays here as long as those tools ship.

Earshot itself is not part of Studio (owner decision 2026-10-29). It is a capability built into FrameCore Works Toolbox (`toolbox:toolbox`, repository FrameCoreWorks/framecore-works-toolbox), which pins, installs and runs it. Studio only sends Toolbox a task and checks the result: see [sound through Toolbox](../../skills/pipeline-core/references/companion-routing.md#sound-through-toolbox).
