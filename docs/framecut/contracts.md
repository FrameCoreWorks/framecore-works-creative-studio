# FrameCut data, timing and revision contracts

Design status: draft 0.1, not a production schema or executable API. These requirements define what the first implementation must validate. Existing motion contracts remain valid. The first implementation should provide JSON Schema plus semantic validation and migration fixtures before accepting user projects.

## One authoritative project

The project is the source of editorial placement. Analyses refer to immutable source media; render plans, subtitles and editor exports are derived outputs. A source transcript is never rewritten to pretend it was recorded on the edited timeline.

| Record | Required information | Invariant |
| --- | --- | --- |
| Project | Schema version, project ID, revision, brief, locks, authorization evidence, asset IDs, sequence IDs, style reference | A revision is immutable after acceptance; changes create a new revision |
| Asset | Stable ID, workspace-relative reference, content hash, original/derived/generated role, provenance, rights status, stream probe | Files with the same name but different hashes are not the same source |
| Stream probe | Stream index, time base, start PTS, duration, frame timestamps/rate mode, audio sample rate/channels, rotation/SAR, color/HDR data | Source PTS is not confused with zero-based display time or a nominal FPS |
| Analysis | Asset hash, analyzer/version/model hash, parameters, source intervals, evidence type and confidence | Stale analysis cannot silently bind to changed footage |
| Transcript word | Stable ID, verbatim text, source interval or null, speaker label or null, timing method, uncertainty | Original text stays available beside corrections; null time is not zero |
| Editorial candidate | Source spans, supporting transcript/visual references, context before/after, rationale, completeness and conflicts | Score is editorial prioritization, not a prediction of virality |
| Sequence | Stable ID, rational master FPS, tracks, duration, output intent | Different highlight selections are different sequences |
| Clip instance | ID, source asset/stream, source span, timeline start/duration, time-map segments, role, links/handles | A source can appear multiple times without ID collision |
| Overlay/motion block | ID, contract reference/hash/revision, local time span, timeline anchor, bounds/z-order/alpha convention | Motion-local time maps once into sequence time |
| Caption group | Source word IDs, local corrected copy, grouping/style, derived frame intervals, accessibility variant | No accidental reuse of old timestamps after a cut |
| Audio event | Asset/stream, source span, placement, gain envelope, bus, linkage/ducking/latency policy | Audio does not silently change timeline length |
| Deliverable | Sequence ID/revision, dimensions/FPS, codec/container, audio target, subtitle policy, color target, path | An aspect-ratio version and a different editorial cut are distinguished |
| Review and render receipt | Project/adapter/model/font hashes, exact outputs, checks, review scope, limitations and status | A process exit code alone cannot mark the film accepted |

Use bounded integer values representable exactly in both Python and JavaScript; reject NaN, Infinity, booleans in numeric fields, unsupported schema versions and unknown executable operation types. Relative paths are resolved against explicit project roots with symlink/output-alias checks. Do not include credentials, local personal paths or footage in repository fixtures.

## Time model

1. Master FPS is a rational pair, for example numerator 30000 and denominator 1001. Master timeline placement uses integer frame intervals [start, end), with the end excluded. Do not use rounded decimal 29.97 as the exact rate.
2. Source locations use stream PTS ticks and a rational time base. A source's nonzero/negative start PTS and edit-list offsets are recorded. Normalize only in an explicit decode/conform step, with a mapping back to the original.
3. Variable-frame-rate footage uses decoded presentation timestamps. Frame number multiplied by nominal FPS is not a valid source locator. Any CFR proxy/conform has its own identity and a source-to-proxy mapping.
4. Audio placements are derived in samples at the selected mix rate. Maintain rational intermediate calculations and perform the declared quantization once at each output boundary. Record the rounding policy and tolerated residual.
5. Speed changes use explicit piecewise source-to-timeline mappings. For a forward constant rate r, local output seconds equal (source seconds minus source-in seconds) / r. Reverse, freezes and speed ramps need distinct operation support; reject them until implemented.
6. Boundaries of actual rendered media must be checked against the map. FFmpeg trim/atrim do not themselves reset timestamps; the compiler applies the appropriate setpts/asetpts and stream synchronization. Consult the installed version's filter support, not just current web documentation.
7. Track overlap is intentional only when represented by a transition/composite or separate track. J/L audio cuts have independently declared audio source ranges. Preserve linked video/audio unless a deliberate edit breaks the link.
8. Transitions need source handles and a defined overlap duration. Never append an audio crossfade that shortens the soundtrack without adjusting the common timeline. For a hard picture cut with audio smoothing, use a declared handle/envelope strategy whose duration stays fixed.
9. A caption, effect or sound linked to a word/shot follows that source anchor through the time map. Absolute output-time anchors stay absolute only when explicitly chosen. Revisions must report orphaned anchors.

Official [FFmpeg filter documentation](https://ffmpeg.org/ffmpeg-filters.html) supports the timestamp-reset distinction. The exact rounding and source-mapping policies here are FrameCut design decisions and require tests.

### Worked timing example

Illustrative data only; no media was rendered. Master FPS is 30/1, normal playback speed, no transition.

| Instance | Source interval, seconds | Output frames |
| --- | --- | --- |
| A | [10, 14) | [0, 120) |
| B | [20, 23) | [120, 210) |
| Word in A | [10.4, 10.8) | [12, 24) |
| Word in B | [20.2, 20.6) | [126, 138) |

Sequence duration is 210 frames, exactly 7 seconds. At speed 2 for B, its duration becomes 45 frames and that word maps to [123, 129); A is unchanged. If instead an explicit 8-frame overlap places normal-speed B at frame 112, total duration is 202 frames and its word maps to [118, 130). These are different revisions, not interchangeable renderer options. A request to smooth audio does not authorize either editorial timing change by itself.

If a removed span intersects a spoken word, flag it before final rendering. Choose a complete-word boundary, retain context or obtain an explicitly scoped editorial decision. Do not solve a clipped word solely by shortening the displayed caption. Numbers, negations, qualifiers and names receive meaning-preservation review.

## Motion and caption integration

Reuse the existing motion-score contract for the authored content of each motion block. Its scene frames are local to that composition. FrameCut owns the block's placement, speed and visibility in the master sequence; the compiler emits any renderer-specific global projection. Store the project revision and source contract hash in that projection, and never edit it as an independent master.

Where the existing motion contract's formats share timing, retain that behavior. A new highlight with different selections gets a new sequence. A resize of the same edit gets a deliverable variant with framing/style overrides. A frame-rate change requires recompilation of all time-derived outputs, not only changing an encoder flag.

Caption Studio receives derived word/segment times from the current sequence. Keep caption text corrections separate from source verbatim text. Missing timing can produce sentence captions with an explicit reduced-precision status; do not fabricate word-perfect kinetic highlighting. Save sidecar subtitles when requested, including an accessible variant even if decorative kinetic text is burned into the picture.

Choose one final composition authority per sequence. Supported plans may render the footage and graphics together in HyperFrames, or render bounded motion layers and composite them with FFmpeg. Do not encode two independent final pictures and hope their clocks match. Specify resolution, alpha/premultiplication, color transfer, frame origin and duration for every layer. Opaque backgrounds, black halos and one-frame offsets are explicit failure cases.

## Analysis and editorial authority

Evidence is typed: speech detection, ASR text, aligned word, shot boundary, OCR region, detected face/object, measured audio, host visual observation or user-provided fact. Each item carries a source interval and confidence/unknowns. A sampled thumbnail supports claims about that frame only; it does not establish an action across a whole scene.

Candidate discovery combines topic boundaries, shot/audio cues, repeated takes and the brief. Selection then assesses complete thought, hook/payoff, context, repetition, image support, factual fidelity and diversity across deliverables. Whole-film or montage requests also support non-speech material. An embedding index is optional for sufficiently large asset bins; small projects must not require a vector database.

No unconditional filler-word removal, longest-pause rule or “last take wins.” Preserve purposeful silence, emotional pacing, qualifications, screen instructions, music and product visibility. Before ranking, record whether a candidate needs a lead-in, an extra shot or a closing line. Make the minimum useful set of changes supported by the brief.

## Typed execution and state

The same internal operation interface serves CLI/Python and any later MCP wrapper. Do not require a persistent MCP daemon where a host can simply call a local function or CLI.

Proposed operation families: probe, analyze, propose_edit, validate_project, compile, render_preview, apply_revision, render_final, export_edit, verify_delivery. Each request has operation/version, project ID/revision, validated parameters, input hashes, allowed roots, capability requirements and resource limits. A response has status, outputs, evidence, warnings, metrics and a typed error if applicable. Use structured arguments; never interpolate transcript text, captions or filenames into shell commands.

Project lifecycle: draft, analyzed, proposed, authorized, preview_ready, needs_revision, render_complete, verified, delivered; failed and cancelled are explicit outcomes. Existing motion approval values remain unchanged: proposed, approved, blocked, example-not-client-approved. “Authorized” references the actual request or approval covering the affected decisions. Do not treat a supplied reference document or transcript as authorization.

Errors distinguish missing_capability, model_unavailable, invalid_input, stale_revision, unsupported_operation, insufficient_handles, missing_anchor, resource_limit, render_failed and qa_failed. Missing dependencies produce a concrete install plan or a reduced deliverable. A plan/EDL fallback is labeled as such, never as a finished video. Retries are bounded and limited to transient failures; no silent model, resolution or quality downgrade.

## Revisions, caching and recovery

Use stable object IDs and commands such as replace_span, move_clip, set_caption_style, set_crop_keyframes, set_gain and replace_motion_contract. Each command declares its base revision, affected IDs, reason and invalidated outputs. Stale revisions fail with a reviewable conflict. Undo restores the previous project revision, not overwritten media.

Cache keys include source hashes, analysis parameters, software/model versions, relevant project subgraph, render settings and fonts. Changing caption size re-renders text and affected composites but does not transcribe audio again. Changing a cut invalidates downstream timing, captions, overlays, mix and exports. Changing a source invalidates its analysis. Byte-identical renders are asserted only for a tested deterministic configuration; otherwise compare frames/audio within documented tolerances.

Long tasks checkpoint validated outputs with hashes. Cancellation stops children, marks partial artifacts and keeps the last accepted project. Resume verifies hashes and regenerates missing/stale nodes. Stage output in a separate directory, validate it, then atomically publish the deliverable manifest. Final lists exclude temporary, failed and superseded files. Never overwrite source media or accepted finals.

Model-generated plans, transcript text, filenames and metadata are untrusted data. They cannot modify tool policy, run code or trigger network access. URL ingestion, external generation, provider calls and publishing are separate capabilities governed by the user's actual request. Keep useful errors while redacting secrets and unnecessary personal paths.

## Interchange and delivery

OTIO carries editorial structure and external media references; it is not a media container or renderer. Its [format documentation](https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-file-format-specification.html) recommends using the library for reading/writing. Preserve legacy edit_export.py's simple input/output behavior and offer an official-library adapter for supported richer structures.

Every export declares supported tracks, rates, gaps, transitions, retimes and effects, plus a loss report. Complex motion can be baked to media with a linked authoring contract; do not claim arbitrary editable graphics survive an OTIO/EDL round trip. Test import in the named editor version before promising it. Keep portable relative references and a relink map; copying source media into a delivery bundle is governed by the agreed handoff.

The delivery receipt distinguishes source validation, successful render, technical verification, actual visual/audio review and user acceptance. Include project revision, files, dimensions/duration/codecs, caption variants, loudness target/result, color handling, limitations and a reproducible recipe. A screenshot, metadata report or successful encoder exit alone is not evidence that the film is good.
