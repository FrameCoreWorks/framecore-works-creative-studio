# FrameCut runtime

One project, source clocks, edit decisions, captions, motion placements, mix and delivery. Python 3.10+ standard library plus FFmpeg/FFprobe (libx264, AAC, libass, overlay, xfade, loudnorm). No network, MCP daemon, GPU or private package required. PyWhisperCpp/model and official OpenTimelineIO are optional explicit runtimes. Run `python3 framecut.py --help` for the complete command surface. All commands return JSON; failures exit 2 with a typed error.

## Workflow

The project file's parent is the allowed root. Place/copy authorized source media there without changing originals. Filenames may contain spaces/Unicode. Paths stored in the project are relative; traversal, symlinks, source replacement and output overwrite are rejected. Give each source, clip, sequence and deliverable a stable ID. Scripts never download models or install tools.

```bash
python3 framecut.py capabilities
python3 framecut.py init job/project.json --id job
python3 framecut.py ingest job/project.json --asset camera --media media/camera.mp4 --base-revision 1
python3 framecut.py analyze job/project.json --asset camera --out analysis/camera
python3 framecut.py import-transcript job/project.json --asset camera --transcript checked-transcript.json --base-revision 2
python3 framecut.py apply job/project.json --ops edit-operations.json --base-revision 3 --reason "Apply the requested edit"
python3 framecut.py compile job/project.json --deliverable vertical --out plans/r4.json
python3 framecut.py render job/project.json --deliverable vertical --out renders/r4-preview
python3 framecut.py render job/project.json --deliverable vertical --out renders/r4-final --mode final
python3 framecut.py verify job/project.json --bundle renders/r4-final
python3 framecut.py export job/project.json --sequence main --out handoff/r4
```

Numbers above illustrate revision increments; always read the actual revision. Omit transcript import for non-speech work and adjust the next base revision accordingly. `analyze`/`compile`/`render` do not change editorial revision. `ingest`, transcript import, `apply`, `attach-motion` and `undo` do. No finalized output is overwritten. Review precedes delivery: `review --bundle ... --evidence review.json` records who inspected which intervals, observations, outcome (`pass`, `needs_revision`, `blocked`), `picture_watched` and `audio_heard`. Do not fabricate either flag. Technical verification and human/agent review remain distinct.

`transcribe --asset camera --python /absolute/isolated/bin/python --model /absolute/ggml-tiny.bin --language pl --base-revision N` uses an existing PyWhisperCpp environment and explicit local model. Discover them through the existing inventory, not hardcoded home directories. It returns draft segment times. Add `--word-times` for real ASR token timestamps (approximate, not forced alignment); inspect/correct boundaries before kinetic delivery or import checked word times. Text is never split into fabricated equally spaced times. Transcript format: `{ "timing": "manual|aligned|asr_word|segment|unknown", "language": "pl", "engine": "...", "source_hash": "...", "words": [{"id":"w1","start":0.2,"end":0.6,"text":"Hello"}], "segments": [...] }`. Times are seconds relative to the selected source stream start, not the edited sequence. Unknown times are null. Preserve verbatim speech; display corrections live in sequence caption settings under `asset:word_id`.

`propose --asset camera` returns source transcript intervals and neighboring context for editorial assessment. It does not select highlights or rate virality. The host evaluates whole thoughts, relevance, context, visual support, diversity and pacing. Scene changes, pauses and repeated takes do not decide edits automatically. `analyze` writes bounded scene/silence evidence, source decoded PTS and timestamped thumbnails; inspect the actual media beyond samples where the decision needs it.

## Authoritative contract, version 1

`schema.json` documents shape; `fc_core.validate` is the authoritative strict semantic validator. Unknown operation/schema types fail. Source `probe` comes from `ingest`, not model guesses. Project fields: schema_version, id, revision, brief, authorization, assets, analyses, sequences, deliverables, locks, status, history. `authorization` records the user's real request already covering the edit/final; it is not a new mandatory confirmation. `locks` is a list of protected clip IDs. History snapshots are immutable. Undo keeps current locks unless explicitly unlocked in a separate authorized edit.

Master FPS is `{ "num": 30000, "den": 1001 }`, never rounded 29.97. All `start`, `duration`, `transition` and anchor offsets are integer sequence frames, half-open intervals. Audio boundaries are rounded once at 48 kHz, nearest/ties away from zero. Each clip references an asset and `source_in` in that asset's PTS ticks. For source-relative seconds `s`, use `start_pts + round_boundary(Fraction(str(s)) / Fraction(time_base))`. Do not multiply by nominal source FPS, especially for VFR. Clip source duration is `duration / fps * speed`; speed is a positive rational from 1/4 to 4. Original PTS, rotation, SAR and stream/color metadata remain in the asset. FFmpeg conforms picture to master CFR; the source map retains source intervals. HDR is explicitly rejected pending a tested SDR conform.

A sequence contains `id`, `fps`, `duration`, ordered `clips`, optional `audio`, `overlays`, `texts`, `captions`, `background` and editorial notes. Clips contain id, asset, start, duration, source_in, optional speed, mute, gain_db, fit (`contain|cover`), crop (`[x,y,width,height]` normalized), transition (overlap frames with previous picture), fade (seconds), note. Start must be explicit on base clips. Gaps are rendered background. A transition overlaps actual source media and reduces sequence length according to placement; it cannot exceed available handles. One sequence may contain no base clips for motion-only work.

Audio/overlay/text events have `start` OR `anchor: {"clip":"id","offset":frames}`. Orphaned anchors fail. Audio carries asset/source_in/duration, gain_db, fade, bus (`dialogue|music|sfx`) and duck_db (negative music gain while dialogue events are active). Linked source audio follows picture unless muted; independent events provide J/L cuts and replacement sound. Ducking is an event schedule, not speech recognition. Audio never independently shortens the sequence. Deliverable `lufs` opts into measured two-pass normalization, otherwise gain/mix is retained; silence is not a measured target match. Denoising through the existing specialist must produce an explicit derived asset with compensated delay; no unrequested denoising is applied.

Overlays additionally require normalized `rect: [x,y,width,height]` and alpha (`opaque|straight`). Premultiplied alpha must be conformed explicitly. Use a normal media clip for rendered HyperFrames/Remotion/Manim/Blender content. `motion-request --event event.json --deliverable ID --out request.json` gives Motion Graphics Workflow local origin 0, duration, FPS and parent revision/global placement. `attach-motion --asset ID --contract relative.motion.json --fps 30/1 --base-revision N` hashes the authoring contract. Changes to that contract require a new binding; the composition's global placement remains here. No generated request or media metadata is executable code.

Text events contain text, size (fraction of height), color (#RRGGBB), position (`top|center|bottom`) and animation (`none|fade|pop`). These are finishing primitives; richer motion belongs to the motion owner. Captions may select `sources: ["clip-or-audio-event-id"]` for independent narration; omitted sources means base clips. Set this explicitly when replacing source dialogue or combining tracks. Source-boundary comparisons allow only half a source PTS tick for quantization, never an output-frame-sized speech trim. Captions contain enabled, mode (`sentence|kinetic`), size, bottom, color, highlight, max_words, font, corrections. Kinetic color follows checked word intervals while the complete group stays visible. Partial words, partial sentence ASR, layout overflow and text/caption collisions block final rendering. Preview reports warnings for diagnosis. Framing of faces/products/UI requires actual image review; no automatic tracking is implied.

Deliverables contain id, sequence, width, height, fit, captions, optional lufs/safe_top/safe_bottom. Same sequence with two deliverables means the same edit in two aspect ratios. Different highlights are different sequences. Explicit clip crops currently apply to all variants; use distinct derived framing assets or a reviewed sequence copy when framing must differ per shot across variants. A per-deliverable crop animation is not implemented.

## Revision operations

`apply --ops operations.json --base-revision N --reason ...` accepts an array of closed typed operations: `add_sequence`, `set_sequence`, `replace_clip`, `set_captions`, `set_audio`, `set_overlays`, `set_texts`, `set_brief`, `set_authorization`, `set_locks`, `set_deliverables`. Every operation has `op` and `value`; sequence-scoped edits include `sequence`, and replace_clip includes `id`. `set_sequence` preserves its ID. Changes create a new revision; stale base revision fails. No arbitrary JSON Patch, filtergraph, shell string or callback is accepted.

```json
[
  {"op":"add_sequence","value":{"id":"main","fps":{"num":30,"den":1},"duration":90,"clips":[{"id":"take","asset":"camera","start":0,"duration":90,"source_in":0}],"captions":{"enabled":true,"mode":"sentence"}}},
  {"op":"set_deliverables","value":[{"id":"vertical","sequence":"main","width":1080,"height":1920,"fit":"contain"}]},
  {"op":"set_authorization","value":"The user's actual instruction to edit and deliver this material"}
]
```

This is data-shape guidance, not a creative template; replace duration/source_in with the probed source clock and chosen edit. `undo --revision K --base-revision N` restores K as N+1, never overwrites accepted outputs. A caption-size revision invalidates the final composite but reuses hash-verified source normalization/audio. Source changes fail; ingest a new asset identity. Cache receipts bind source, relevant settings, engine and FFmpeg environment. Delete only explicitly identified unused cache data when needed, never the source/project/history/finals.

## Supported scope and honest delivery

Cuts/gaps, explicit crossfades, constant speed, independent audio, crop/fit, still/video overlays, local animated text, timed captions and requested loudness targets are executable. Advanced tracking, multicam, speed ramps, HDR mastering, NLE-native project editing and diarization are unsupported here. Optional specialists may prepare tested derived assets without changing the master timeline.

Render stages have child timeouts, bounded inputs, a disk budget check and atomic final directory publication. Interrupting the CLI kills its active child; completed stages resume after hash checks. A machine/process kill may leave `render.lock`; inspect the owning process before removing an abandoned lock. No final is published until full decode, frame count, dimensions/rate/audio length and requested loudness checks pass. Receipt/project hashes prevent stale delivery. The default 2 GiB budget is a cache ceiling, not an OS memory quota; each stage can temporarily consume disk before the next checkpoint. Use host quotas for hard disk/RAM ceilings.

Bundles include video, SRT/VTT, Caption Studio QA, exact source map, project snapshot, projection, technical receipt and review frames. The snapshot retains original relative source paths; relink to the original project root when moved. `export` gives native JSON, relink map and CSV; picture EDL only for supported cuts. `--otio` uses the official library and verifies a read/write round trip. A loss report identifies omitted layered audio/motion/style, unsupported overlaps/retimes and untested editor imports. Do not claim a complete native NLE round trip.
