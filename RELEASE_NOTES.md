# Creative Studio 1.119.2

FrameCut defect fixes from the owner-requested audit (see docs/framecut/audit-2026-10-22.md).

- Partial `set_captions` keeps the other caption settings; words without timing block a final; `analyze` handles very short clips; no tempo stage at 1x.
- Revisions over 16 MiB are refused on write; probe values are validated; preview bundles are never READY; EDL and CSV exports cannot be forged through names or notes; export is atomic.
- A source swapped during a render is not cached; stale render locks are reclaimed; SIGTERM and Ctrl-C clean up; reserved output paths are refused.
- FrameCut guidance, orchestrator routing for footage requests and stale design documents corrected.

Seven product decisions wait for the owner; the ChatGPT startup should be rechecked after the orchestrator edits.
