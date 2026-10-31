"""Earshot readings for the example sounds. Run with the Toolbox launcher:
    python3.12 <toolbox>/capabilities/earshot/scripts/runtime.py exec -I earshot_check.py SOUND_DIR OUT_JSON
Writes measure (LUFS, true peak, length), describe (top AudioSet tags) and match (the intended
description against alternatives) for every MP3."""
import json, sys
from pathlib import Path
from earshot import api

CLAIMS = {
    "01-whoosh": ("a fast whoosh swoosh transition", ["a car engine", "a drum hit", "speech"]),
    "02-ui-click": ("a short user interface click", ["a long explosion", "music", "a bird"]),
    "03-pop": ("a short bubbly pop", ["a long whoosh", "a dog bark", "rain"]),
    "04-riser": ("a rising tension riser building up", ["a falling whoosh", "a single click", "speech"]),
    "05-bass-impact": ("a deep cinematic bass impact boom", ["a high bell", "a keyboard click", "birds singing"]),
    "06-ding": ("a bell ding notification chime", ["a bass drum", "noise", "a car horn"]),
    "07-typing": ("typing on a computer keyboard", ["footsteps", "rain on a window", "a clock ticking"]),
    "08-glitch": ("a digital glitch stutter", ["a bell", "a smooth pad", "birdsong"]),
    "09-music-calm": ("calm ambient music, soft relaxing pad", ["energetic dance music", "heavy metal", "speech"]),
    "10-music-energetic": ("an energetic techno track, a four on the floor beat with bass", ["calm ambient music", "speech", "classical piano"]),
}

def short(x):
    if isinstance(x, dict):
        return {k: short(v) for k, v in x.items() if not isinstance(v, (list, dict)) or k in ("tags", "top", "alts", "ranking", "labels")}
    return x

src, out = Path(sys.argv[1]), Path(sys.argv[2])
res = {}
for mp3 in sorted(src.glob("*.mp3")):
    name = mp3.stem
    claim, alts = CLAIMS[name]
    m = api.measure(str(mp3), music="music" in name)
    d = api.describe(str(mp3), top=5)
    ma = api.match(str(mp3), claim, alts=alts)
    res[name] = {"measure": m, "describe": d, "match": ma}
    print(name, "done", flush=True)
out.write_text(json.dumps(res, indent=1, default=str))
