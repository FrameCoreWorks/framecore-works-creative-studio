# Formats

## Cue sheet (`cues.json`)

An ordered list of lines (or `{"lines": [...]}`). `id` must be unique, `text` non-empty and `max_seconds` positive;
the launcher stops before any generation and names the line otherwise.

```json
[
  {"id": "s01", "text": "(calm, warm female voice)FrameCore Works ships today.", "max_seconds": 2.8},
  {"id": "s02", "text": "Edit, caption and deliver in one place.", "max_seconds": 3.2, "voice_notes": "smile"}
]
```

A leading `(...)` is a VoxCPM2 voice description and is not touched by the lexicon. `voice_notes` is for the
person directing the read.

## Lexicon (`lexicon.json`)

One per project. Each word maps to how it should be read; matching is whole-word and case-insensitive, longest
entry first, so `Hardcore` is not changed by an entry for `Core`.

```json
{"FrameCore": "frejm kor", "FrameCut": "frejm kat", "2026": "dwa tysiące dwadzieścia sześć"}
```

## Lock file (`narration.lock.json`)

Written in the output folder and updated line by line, so `--only` keeps the other lines.

```json
{
  "version": 1,
  "lexicon_sha256": "…",
  "lines": {
    "s01": {"engine": "voxcpm", "model": "openbmb/VoxCPM2", "engine_version": "2.0.3",
            "voice_source": "voxcpm default voice", "consent": null,
            "text_sent": "(calm, warm female voice)frejm kor Works ships today.",
            "wav": "takes/s01.wav", "sha256": "…", "duration": 2.61, "max_seconds": 2.8,
            "verdict": "fits", "stretch_percent": null, "status": "ok", "error": null}
  }
}
```
