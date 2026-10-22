# Handing an edit to an editor

An Edit Pack becomes files and steps the editor can follow without guessing: the edit decision list exported with [`edit_export.py`](../scripts/edit_export.py), the captions as an SRT from [Caption Studio](../../caption-studio/SKILL.md), and the step list for the user's editor below.

## Export the edit decision list

```bash
python3 scripts/edit_export.py edit.json --out-dir handoff/    # edit.edl, edit.otio, edit-shots.csv
```

For a FrameCut project use `framecut.py export project.json --sequence ID --out handoff/rN` instead: it writes the native project, relink map, CSV, an EDL when the edit is plain picture cuts and optional OTIO (`--otio`), plus a loss report.

`edit.json` holds the title, the frame rate, an optional start timecode and the clips in order: `source` (file name), `in` and `out` (seconds or `HH:MM:SS:FF`), and optionally `record_in`, `name` and `note`. The tool writes:

- **`.edl`**: CMX 3600, one video track, reel names of up to 8 characters with the full file name in a `FROM CLIP NAME` comment. The format is standard CMX 3600; import into a named editor was not tested here, so check the first import.
- **`.otio`**: an OpenTimelineIO timeline with the same clips and any gaps, for editors that import OTIO.
- **`-shots.csv`**: the shot list with record and source timecodes, for an editor without EDL import and for the client's review.

Only picture cuts travel this way: transitions, speed changes, effects, titles, audio levels and colour stay as written instructions in the Edit Pack. Keep the source files' names unchanged so the editor can relink them. The export was checked by reading both files back with OpenTimelineIO 0.18.1 and its CMX 3600 adapter (2026-10-11); imports into each editor were not run.

## Step lists

Written on 2026-10-11 from the editors' documented features; menus change between versions, so check each step against the installed version and say where it differs.

### DaVinci Resolve

1. Set the timeline resolution (for example 1080 × 1920 for 9:16) and the frame rate in Project Settings before importing anything; the frame rate cannot change once media is in a timeline.
2. Add the source files to the Media Pool.
3. File > Import > Timeline and choose the `.otio` (or the `.edl`); let it link to the clips in the Media Pool.
4. Import the SRT into the Media Pool and drag it onto a subtitle track, or burn in the captions Studio already rendered.
5. Check every cut against `-shots.csv`, then export on the Deliver page: H.264 or the delivery spec's codec, the timeline's resolution and frame rate.

### Premiere Pro

1. Create a sequence with the delivery size and frame rate (custom frame size for 9:16).
2. File > Import and choose the `.edl`; Premiere builds a sequence from it. Relink the offline clips to the source files when asked.
3. Copy the cuts into the delivery sequence if the imported one has different settings.
4. Import the SRT and drag it onto the timeline as a caption track; style it in the captions panel, or use the burned-in captions.
5. Check against `-shots.csv`, then File > Export > Media: H.264, the sequence's size and frame rate.

### CapCut (desktop)

CapCut does not import EDL or OTIO.

1. Set the canvas ratio (9:16) and add the source files.
2. Place and trim the clips in the order and to the in and out points of `-shots.csv`.
3. Add the captions: import the SRT where the version offers it, or generate captions and correct them word for word against the approved SRT.
4. Export at the delivery resolution and frame rate.

### OpenCut and other editors

Use the OTIO or EDL where the editor imports them; otherwise follow the CSV as in CapCut. Report which file the editor accepted.

## After the edit

Ask for the exported file, not a screen recording, and check it with the delivery QA: duration, frame rate and size by a media inspector, the cuts against the shot list, the captions against the approved text, loudness against the delivery spec.
