# FrameCut runtime

One project, source clocks, edit decisions, captions, motion placements, mix and delivery. Python 3.10+, Pillow, plus FFmpeg/FFprobe (libx264, AAC, libass, overlay, xfade, loudnorm). No network, MCP daemon, GPU or private package required. PyWhisperCpp/model and official OpenTimelineIO are optional explicit runtimes. Run `python3 framecut.py --help` for the complete command surface. All commands return JSON; failures exit 2 with a typed error.

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
# The host first presents the full storyboard, applies user feedback and records acceptance.
# Revision r4 here is illustrative: use the current project and accepted board.
python3 framecut.py render job/project.json --deliverable vertical --out renders/r4-final --mode final
python3 framecut.py verify job/project.json --bundle renders/r4-final
python3 framecut.py export job/project.json --sequence main --out handoff/r4
```

FrameCut's host workflow is onboarding → complete visual storyboard/contact sheets → user feedback and revisions → acceptance of the current board → final render and review. The host coordinates Sequence Architect and Board Architect to generate actual stills and readable sheets covering every scene and meaningful moment, including the ending. A table or sparse source thumbnails alone do not complete the board. The existing `board_compose.py` produces PNG pages/PDF without rendering a video first. Display the pages in chat and retain stable IDs, timing, exact copy, motion/transition/audio notes and a coverage map in the project checkpoint.

A preview video is optional on user request, for example `python3 framecut.py render job/project.json --deliverable vertical --out renders/rN-sample --mode preview`. This command renders the selected deliverable's whole sequence; for a short sample, create an explicitly scoped derived sequence/deliverable while retaining the full master sequence. It is not a mandatory stage or acceptance of the complete film. Record the actual request and sample scope. Technical QA after final rendering remains required even with no sample.

The host retains `framecut_context` in Project State and the free-form project `brief`: stage, board revision, covered sequences/formats, ordered panel map and sheets, pending feedback, approval evidence and optional sample status. Confirm that the current edit implements the accepted board before final rendering; changed creative decisions return to board review. Ordinary revision-number changes do not themselves revoke an unchanged design. These are workflow assertions checked by the host, not a new runtime schema or a CLI-enforced storyboard gate. The CLI's existing `authorization` records execution scope, not acceptance of an unseen board.

Numbers above illustrate revision increments; always read the actual revision. Omit transcript import for non-speech work and adjust the next base revision accordingly. `analyze`/`compile`/`render` do not change editorial revision. `ingest`, transcript import, `transcribe`, `apply`, `attach-motion` and `undo` do. No finalized output is overwritten. Review precedes delivery: `review --bundle ... --evidence review.json` records who inspected which intervals, observations, outcome (`pass`, `needs_revision`, `blocked`), `picture_watched` and `audio_heard`. Do not fabricate either flag. Declare `coverage: "sampled"|"full"`; omitted coverage is conservatively sampled. A deliberately silent film may explicitly set `audio_intentionally_silent: true`. `verify.status` remains the technical result; `delivery_readiness.status` is READY only for recorded full picture review plus heard audio (or intentional silence) with a passing outcome. Failed review is BLOCKED; absent or partial review is REVIEW_REQUIRED. These are recorded assertions, not proof of listening or user acceptance. Later review evidence archives the previous record under `review/history/` before updating the current record. Technical verification and human/agent review remain distinct.

`transcribe --asset camera --python /absolute/isolated/bin/python --model /absolute/ggml-tiny.bin --language pl --base-revision N` uses an existing PyWhisperCpp environment and explicit local model. Discover them through the existing inventory, not hardcoded home directories. It returns draft segment times. Add `--word-times` for real ASR token timestamps (approximate, not forced alignment); inspect/correct boundaries before kinetic delivery or import checked word times. Text is never split into fabricated equally spaced times. Transcript format: `{ "timing": "manual|aligned|asr_word|segment|unknown", "language": "pl", "engine": "...", "source_hash": "...", "words": [{"id":"w1","start":0.2,"end":0.6,"text":"Hello"}], "segments": [...] }`. Times are seconds relative to the selected source stream start, not the edited sequence. Unknown times are null. Preserve verbatim speech; display corrections live in sequence caption settings under `asset:word_id`.

`propose --asset camera` returns source transcript intervals and neighboring context for editorial assessment. It does not select highlights or rate virality. The host evaluates whole thoughts, relevance, context, visual support, diversity and pacing. Scene changes, pauses and repeated takes do not decide edits automatically. `analyze` writes bounded scene/silence evidence, source decoded PTS and timestamped thumbnails; inspect the actual media beyond samples where the decision needs it.

## Authoritative contract, version 1

`schema.json` documents shape; `fc_core.validate` is the authoritative strict semantic validator. Unknown operation/schema types fail. Source `probe` comes from `ingest`, not model guesses. Project fields: schema_version, id, revision, brief, authorization, assets, analyses, sequences, deliverables, locks, status, history. The free-form `brief` retains the working agreement: intended viewer/result, materials, outputs, separate speech/caption languages, protected content, visual direction and accepted/delegated/provisional decisions. It is not another user form. Translations are separate approved copy with phrase timing or a specialist composition; source-word corrections cannot express translated word alignment. `authorization` records the user's real request already covering the edit/final; it is not a new mandatory confirmation. `locks` is a list of protected clip IDs. History snapshots are immutable. Undo keeps current locks unless explicitly unlocked in a separate authorized edit.

Master FPS is `{ "num": 30000, "den": 1001 }`, never rounded 29.97. All `start`, `duration`, `transition` and anchor offsets are integer sequence frames, half-open intervals. Audio boundaries are rounded once at 48 kHz, nearest/ties away from zero. Each clip references an asset and `source_in` in that asset's PTS ticks. For source-relative seconds `s`, use `start_pts + round_boundary(Fraction(str(s)) / Fraction(time_base))`. Do not multiply by nominal source FPS, especially for VFR. Clip source duration is `duration / fps * speed`; speed is a positive rational from 1/4 to 4. Original PTS, rotation, SAR and stream/color metadata remain in the asset. FFmpeg conforms picture to master CFR; the source map retains source intervals. HDR is explicitly rejected pending a tested SDR conform.

A sequence contains `id`, `fps`, `duration`, ordered `clips`, optional `audio`, `overlays`, `texts`, `captions`, `background` and editorial notes. Clips contain id, asset, start, duration, source_in, optional speed, mute, gain_db, fit (`contain|cover`), crop (`[x,y,width,height]` normalized), transition (overlap frames with previous picture), fade (seconds), note. Start must be explicit on base clips. Gaps are rendered background. A transition overlaps actual source media and reduces sequence length according to placement; it cannot exceed available handles. One sequence may contain no base clips for motion-only work.

Audio/overlay/text events have `start` OR `anchor: {"clip":"id","offset":frames}`. Orphaned anchors fail. Audio carries asset/source_in/duration, gain_db, fade, bus (`dialogue|music|sfx`) and duck_db (negative music gain while dialogue events are active). Linked source audio follows picture unless muted; independent events provide J/L cuts and replacement sound. Ducking is an event schedule, not speech recognition. Audio never independently shortens the sequence. Deliverable `lufs` opts into measured two-pass normalization, otherwise gain/mix is retained; silence is not a measured target match. Denoising through the existing specialist must produce an explicit derived asset with compensated delay; no unrequested denoising is applied.

Overlays additionally require normalized `rect: [x,y,width,height]` and alpha (`opaque|straight`). Premultiplied alpha must be conformed explicitly. Use a normal media clip for rendered HyperFrames/Remotion/Manim/Blender content. `motion-request --event event.json --deliverable ID --out request.json` gives Motion Graphics Workflow local origin 0, duration, FPS and parent revision/global placement. `attach-motion --asset ID --contract relative.motion.json --request request.json --fps 30/1 --base-revision N` checks the originating project/history, unchanged sequence, brief and deliverable, then decoded frame count, FPS, dimensions and alpha before hashing the authoring contract. Ingest may advance the revision without changing the requested edit. An affected edit/brief change needs a fresh request. Compile rejects moved, trimmed, retimed or differently formatted bound motion; legacy bindings without a request are preview-only until rebound. Changes to that contract require a new binding; the composition's global placement remains here. No generated request or media metadata is executable code.

Text events contain text, size (fraction of height), color (#RRGGBB), position (`top|center|bottom`) and animation (`none|fade|pop`). These are finishing primitives; richer motion belongs to the motion owner. Captions may select `sources: ["clip-or-audio-event-id"]` for independent narration; omitted sources means base clips. Set this explicitly when replacing source dialogue or combining tracks. Source-boundary comparisons allow only half a source PTS tick for quantization, never an output-frame-sized speech trim. Captions contain enabled, mode (`sentence|kinetic`), size, bottom, color, highlight, max_words, font, corrections. Kinetic color follows checked word intervals while the complete group stays visible. Partial words, partial sentence ASR, layout overflow and text/caption collisions block final rendering. Preview reports warnings for diagnosis. Framing of faces/products/UI requires actual image review; no automatic tracking is implied.

Deliverables contain id, sequence, width, height, fit, captions, optional lufs/safe_top/safe_bottom. Same sequence with two deliverables means the same edit in two aspect ratios. Different highlights are different sequences. Clip crops are defaults shared by variants; `deliverable.framing[event_id]` overrides crop/fit and selected animation tracks for that variant. Use per-deliverable `framing` for distinct static crops and animated zoom/pan/position/scale; the common edit and source clocks remain unchanged.

## Revision operations

`apply --ops operations.json --base-revision N --reason ...` accepts an array of closed typed operations (plus the native edit operations listed below): `add_sequence`, `set_sequence`, `replace_clip`, `set_captions` (a partial value changes those settings and keeps the rest), `set_audio`, `set_overlays`, `set_texts`, `set_brief`, `set_authorization`, `set_locks`, `set_deliverables`. Every operation has `op` and `value`; sequence-scoped edits include `sequence`, and replace_clip includes `id`. `set_sequence` preserves its ID. Changes create a new revision; stale base revision fails. No arbitrary JSON Patch, filtergraph, shell string or callback is accepted.

```json
[
  {"op":"add_sequence","value":{"id":"main","fps":{"num":30,"den":1},"duration":90,"clips":[{"id":"take","asset":"camera","start":0,"duration":90,"source_in":0}],"captions":{"enabled":true,"mode":"sentence"}}},
  {"op":"set_deliverables","value":[{"id":"vertical","sequence":"main","width":1080,"height":1920,"fit":"contain"}]},
  {"op":"set_authorization","value":"The user's actual instruction to edit and deliver this material"}
]
```

This is data-shape guidance, not a creative template; replace duration/source_in with the probed source clock and chosen edit. `undo --revision K --base-revision N` restores K as N+1, never overwrites accepted outputs. A caption-size revision invalidates the final composite but reuses hash-verified source normalization/audio. Source changes fail; ingest a new asset identity. Cache receipts bind source, relevant settings, engine and FFmpeg environment. Delete only explicitly identified unused cache data when needed, never the source/project/history/finals.

## Supported scope and honest delivery

Cuts/gaps, explicit crossfades, constant and variable speed, freeze frames, independent audio, variant framing, keyed transforms, still/video overlays, animated text, versioned effects, timed captions and requested loudness targets are executable. Advanced tracking, multicam, HDR mastering, NLE-native project editing and diarization remain unsupported here. Optional specialists may prepare tested derived assets without changing the master timeline.

Render stages have child timeouts, bounded inputs, a disk budget check and atomic final directory publication. Interrupting the CLI kills its active child; completed stages resume after hash checks. A machine/process kill may leave `render.lock`; inspect the owning process before removing an abandoned lock. No final is published until full decode, frame count, dimensions/rate/audio length and requested loudness checks pass. Receipt/project hashes prevent stale delivery. The default 2 GiB budget is a cache ceiling, not an OS memory quota; each stage can temporarily consume disk before the next checkpoint. Use host quotas for hard disk/RAM ceilings.

Bundles include video, SRT/VTT, Caption Studio QA, exact source map, project snapshot, projection, technical receipt and review frames. The snapshot retains original relative source paths; relink to the original project root when moved. `export` gives native JSON, relink map and CSV; picture EDL only for supported cuts. `--otio` uses the official library and verifies a read/write round trip. A loss report identifies omitted layered audio/motion/style, unsupported overlaps/retimes and untested editor imports. Do not claim a complete native NLE round trip.

## Native development commands

These are original FrameCut implementations. Concat was a functional research reference; no Concat code, binary, AGPL dependency or model is included. The native renderer uses Pillow for bounded RGBA transforms and FFmpeg for source decoding, composition, captions, audio and encoding. `capabilities` reports the Pillow requirement; install nothing implicitly. No GPU/MCP daemon or external service is needed.

```bash
python3 framecut.py timeline-read job/project.json --sequence main
python3 framecut.py apply job/project.json --ops edits.json --base-revision 4 --reason "Requested correction" --dry-run
python3 framecut.py apply job/project.json --ops edits.json --base-revision 4 --reason "Requested correction"
python3 framecut.py preview-frame job/project.json --deliverable vertical --frame 45 --out boards/r5-detail.png
python3 framecut.py storyboard job/project.json --deliverable vertical --panels authored-panels.json --out boards/r5
python3 framecut.py effects
python3 framecut.py effects --check
```

All timeline positions below are integer master frames. Operations are an atomic array; a bad member rejects the whole transaction. `--dry-run` checks locks, IDs, source bounds and dependent geometry and reports impact without a revision. Re-read before saving if another edit changed the base revision.

| Operation | `value` | Semantics |
| --- | --- | --- |
| `split_clip` | `{"frame":45,"right_id":"shot-b"}` | Absolute split frame inside the named clip; source and animation windows survive; later anchors and explicit caption sources follow the new right ID. |
| `trim_clip` | `{"in":5,"out":50,"ripple":true}` | Half-open offsets within the old clip. Ripple preserves its start and moves downstream absolute lanes by the removed duration; without ripple the new start advances by `in`. |
| `move_clip` | `{"start":90}` | Move the named clip and its anchored dependents; overlap without a valid transition fails. |
| `remove_clip` | `{"ripple":true,"dependents":"remove"}` | Explicit dependent policy `reject` (default), `detach` or `remove`; caption references and variant framing are reconciled. |
| `freeze_frame` | `{"frame":45,"duration":15,"hold_id":"hold","right_id":"tail"}` | Split inside a clip, insert a silent held source frame, and ripple subsequent events. |
| `set_keyframes` | parameter-to-points object | Replace the named event's animation and reset its local animation offset. |
| `set_speed_curve` | ordered speed-point array | Replace constant speed with a continuous piecewise-linear speed curve. |
| `set_effects` | applied-effect array | Replace the event's versioned picture or audio effects. |
| `set_framing` | `{"deliverable":"vertical","framing":{"shot-a":{"crop":[0.2,0,0.5,1]}}}` | Replace that deliverable's visual-event overrides; do not duplicate the master edit. |

Every structural operation includes `sequence`, and all except `set_framing` include the stable event `id`. Transitions and absolute events spanning a ripple boundary can require an explicit preliminary edit; the runtime fails with `edit_conflict` instead of guessing. Locks remain enforced across the whole transaction and at save time.

### Animation and framing

An event's `keyframes` maps parameters to 1..128 ordered points, each `{ "frame": 0, "value": 1, "easing": "smooth" }`. Easing is `linear`, `smooth` (smoothstep) or `hold`; it belongs to the outgoing segment. Values hold outside the first/last point. The shared evaluator is used by stills and encoded frames. `keyframe_offset` preserves the original animation window after a trim/split; callers normally leave it to edit operations.

Picture parameters: `x`/`y` are offsets in output-width/height units from the centered fit; `scale` is a factor, `rotation` is degrees clockwise, `opacity` is 0..1. `zoom` is 1..8 inside the crop, with normalized `pan_x`/`pan_y` selecting its position. `gain_db` is an additional audio envelope. Text supports position/scale/rotation/opacity; audio events support gain only. Explicit keyed text replaces its simple fade/pop animation. No automatic subject tracking is implied.

`deliverable.framing[event_id]` can override `crop`, `fit` and picture keyframe tracks. Crop is a normalized source rectangle; the variant's tracks override only matching event tracks. Source clocks, edit order, sound and captions remain shared. Native source decode is bounded to a 4096-pixel long side before these transforms; this is not a 16K-detail mastering path. POSIX uses cancellable bounded pipes; other hosts use a bounded file-backed fallback. Cross-platform runtime parity still requires host tests.

### Variable speed and freeze

`speed_curve` contains 2..64 points such as `[{"frame":0,"speed":{"num":1,"den":2}},{"frame":60,"speed":{"num":2,"den":1}}]`, covering frame 0 through `duration`. Speeds are rational 1/4..4, interpolated linearly. Source consumption is the integral of this curve; captions use its inverse. Split/trim preserve the actual source interval and slice the curve. A sub-PTS `source_remainder` preserves exact mapping rather than rounding repeatedly. Constant `speed` and `speed_curve` are mutually exclusive.

Variable-speed source audio is resampled continuously at 48 kHz stereo PCM: tempo **and pitch** follow speed. Use an independent voice/music event to keep it unchanged; this path is not pitch-preserving time stretch or optical-flow interpolation. Freeze holds picture and emits no source dialogue/captions for its inserted interval. Retimed/frozen native edits are retained in JSON; basic EDL/OTIO is withheld with a loss report where it cannot represent them.

### Full storyboard and actual stills

`preview-frame` returns one composited PNG with its frame, project revision/hash, deliverable and digest. `storyboard` generates structural moments across the whole sequence, including all clips/layers, boundaries, transitions, keyframes, captions and ending. The optional `--panels` JSON array adds authored action/reveal/camera/audio moments, e.g. `[{"id":"reveal","frame":37,"action":"Product becomes fully visible","audio":"Music accent"}]`; it does not remove structural coverage. The host must add meaningful content beats and inspect them. Structural completeness does not establish semantic coverage, motion quality or heard audio.

Outputs: `frames/*.png`, `board.json`, numbered `sheets/board-p*.png`, `sheets/board.pdf`, and `receipt.json` with project hash, panel hashes, event coverage, warnings and `awaiting_user_review`. No full video is rendered first. Available assets are required; the host supplies clearly labelled planned stills for missing imagery through the existing storyboard owner. The 512-moment safety bound fails explicitly; split large work into reviewed sequences rather than silently dropping panels. Raster still/video comparisons account for H.264 4:2:0 compression, but must preserve the same source frame, transform and exact copy.

### Durable jobs and retry

```bash
python3 framecut.py job-start job/project.json --request render-job.json
python3 framecut.py job-status job/project.json --job job-ID
python3 framecut.py job-cancel job/project.json --job job-ID
python3 framecut.py job-resume job/project.json --job job-ID
```

The request is `{ "kind":"render", "deliverable":"vertical", "out":"renders/r5", "mode":"final", "timeout":600, "max_disk_mb":2048 }`; `kind:"storyboard"` accepts an optional inline `panels` array. Preserve the real storyboard acceptance before starting a final. Each job stores an immutable project snapshot, request, worker log and atomic state under `.framecut/<project>/jobs/<job-id>/`. State survives CLI/session restarts. `queued`, `running`, `completed`, `failed`, `cancelled` and `interrupted` are distinct; progress names its stage and, where measured, processed frames/samples/panels. Never interpret one stage's counter as overall percent.

Cancellation is cooperative and targets only this worker's work. Wait for a terminal state before resuming. Resume creates a linked attempt only when the project hash and source hashes still match; finished cache stages are verified and reused. A proven dead job may recover only its own render lock. A changed project needs a new job/output. Hosts may terminate background processes; the API does not promise a persistent server. There is no automatic retry of invalid input, a changed source, failed QA or an unknown effect, and no paid calls. A completed technical render still needs the existing picture/audio review and delivery gate.

### Effect packages and verification

Applied effects use `{ "id":"brightness", "version":1, "params":{"amount":1.1}, "enabled":true }`. Initial picture effects: brightness, contrast, saturation, blur, grayscale and vignette. Independent audio effects: highpass, lowpass and denoise. `effects` exposes exact ranges/defaults and the catalogue hash. Disabled effects still validate IDs/parameters. Unknown IDs/versions fail; catalogue content is part of the cache environment.

Add a new versioned manifest under `effects/` using bounded supported primitives, numeric parameters and executable fixtures. Manifests cannot inject Python, shell commands or raw FFmpeg expressions. Picture fixtures check actual pixels/alpha; audio manifest fixtures check the compiled filter contract, supplemented by decoded-audio regressions. `effects --check` runs the catalogue fixtures. Run `tests/framecut_test.py` and `tests/framecut_development_test.py` from the plugin root's parent path as appropriate, plus the repository release gates. This catalogue does not add preselected creative directions.
