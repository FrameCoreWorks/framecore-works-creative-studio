# FrameCut: component research and selection

Observed 2026-10-20. Read with [architecture](README.md), [contracts](contracts.md) and the [machine-readable source snapshot](research-sources-2026-10-20.json).

## Method and evidence limits

Two web-search passes identified both established media libraries and newer agent-oriented editing projects. GitHub API reads captured metadata and default-branch commits for 31 repositories. The most relevant README files, official documentation and selected implementation files were read. This is a comparative source review, not a security audit, an exhaustive dependency-license audit or a runtime benchmark of 31 projects. The snapshot identifies which repositories received selected code inspection. No candidate was installed or executed for this research.

GitHub license labels describe the repository's detected license; binary distributions, codecs, dependencies, assets and model weights can have additional terms. NOASSERTION means GitHub did not classify a single SPDX license, not “no restrictions.” A recent push can affect a non-default branch; commit dates and archived flags are recorded separately. Stars are not used as a quality score.

## Recommended stack

Reuse existing FFmpeg/FFprobe, the local Whisper binding, PySceneDetect/OpenCV, Caption Studio, Motion Graphics Workflow with HyperFrames, and Studio audio/QA tools. Add an exact-time project compiler and source-grounded editorial layer. Pilot Kinocut as an execution adapter and faster-whisper/WhisperX as optional analysis upgrades before deciding whether they justify new dependencies. Use OpenTimelineIO for validated interchange. This recommendation is an architectural inference from source review and the existing Studio implementation; it is not a claim that the integrated stack has passed tests.

## Candidate matrix

License entries are repository labels except where a primary license/terms page was read. Decision meanings: reuse = already relevant to Studio; pilot = bounded compatibility test before adoption; optional = selected by a concrete job; defer/reference = do not add to the default dependency graph.

| Component and primary repository | Role | License observation | FrameCut decision |
| --- | --- | --- | --- |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Decode, cuts, filters, audio, encoding | LGPL/GPL depends on build | Reuse; inspect actual build and filters |
| [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Editorial interchange | Apache-2.0 | Pilot official adapter; not a renderer |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Local ASR engine | MIT | Reuse existing route |
| [PyWhisperCpp](https://github.com/absadiki/pywhispercpp) | Python binding | MIT | Reuse; normalize word/segment output |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | CTranslate2 ASR, word times, VAD | MIT | Pilot CPU INT8 and optional GPU |
| [WhisperX](https://github.com/m-bain/whisperX) | Forced alignment and speaker workflow | BSD-2-Clause code | Pilot for accurate captions; models separately checked |
| [stable-ts](https://github.com/jianfch/stable-ts) | Timestamp refinement | MIT; archived at observation | Defer new dependency |
| [Silero VAD](https://github.com/snakers4/silero-vad) | Speech activity | MIT | Pilot only if not already provided by ASR |
| [pyannote.audio](https://github.com/pyannote/pyannote-audio) | Speaker diarization | MIT code; model differs | Optional multi-speaker jobs |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Shot boundaries | BSD-3-Clause | Reuse as evidence |
| [Auto-Editor](https://github.com/WyattBlue/auto-editor) | Silence/motion editing proposals | Unlicense source; binaries may differ | Reuse installed CLI through versioned adapter |
| [ClipsAI](https://github.com/ClipsAI/clipsai) | Transcript segmentation and speaker reframing | MIT | Reference/pilot only; stale observed source |
| [MediaPipe](https://github.com/google-ai-edge/mediapipe) | Face/subject evidence for reframing | Apache-2.0 code | Pilot current detector, not automatic legacy AutoFlip adoption |
| [OpenCut](https://github.com/OpenCut-app/OpenCut) | Interactive NLE | MIT | Optional handoff; new automation interfaces are announced |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | HTML/CSS/media motion renderer | Apache-2.0 | Reuse through existing owner |
| [Remotion](https://github.com/remotion-dev/remotion) | React video renderer | Custom Remotion license | Existing optional route; check deployment eligibility |
| [Mediabunny](https://github.com/Vanilagy/mediabunny) | Browser media IO/preview | MPL-2.0 | Optional browser layer; already in inventory |
| [Motion Canvas](https://github.com/motion-canvas/motion-canvas) | Coded animation | MIT | Defer duplicate motion stack |
| [Revideo](https://github.com/midrender/revideo) | TypeScript headless video and player | MIT | Defer; canonical repository is now midrender |
| [libass](https://github.com/libass/libass) | ASS/SSA rendering | ISC | Reuse via FFmpeg when compiled in |
| [pysubs2](https://github.com/tkarabela/pysubs2) | Subtitle file editing/interchange | MIT | Optional only for a missing format |
| [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) | Speech denoising | MIT OR Apache-2.0 code | Optional existing route; measure delay and speech damage |
| [MLT](https://github.com/mltframework/mlt) | Alternate editing framework | LGPL-2.1 label; modules need review | Defer second backend |
| [MoviePy](https://github.com/Zulko/moviepy) | Python video composition | MIT | Defer extra orchestration without demonstrated benefit |
| [LosslessCut](https://github.com/mifi/lossless-cut) | Interactive lossless editing | GPL-2.0 label | Optional external editor, not core |
| [wavesurfer.js](https://github.com/katspaugh/wavesurfer.js) | Browser waveform UI | BSD-3-Clause | Optional review UI later |
| [Kinocut](https://github.com/KyaniteLabs/kinocut) | Typed media tools, workflow, receipts | Apache-2.0 | Highest-priority new adapter pilot |
| [Vex](https://github.com/AKMessi/vex) | Conversational editing suite | PolyForm Noncommercial 1.0.0 | Exclude as commercial default dependency |
| [VEA](https://github.com/Memories-ai-labs/vea-open-source) | Conversational footage/story agent | MIT code | Architectural reference; external service path not local default |
| [OpenTake](https://github.com/appergb/OpenTake) | Desktop timeline and MCP | GPL-3.0 | Optional independent editor adapter |
| [StoryToolkitAI](https://github.com/octimot/StoryToolkitAI) | Transcript search and story selection | GPL-3.0 | Optional external editorial workspace |

## Findings that change implementation decisions

### 1. Kinocut is worth a pilot, not an immediate wholesale import

The [README](https://github.com/KyaniteLabs/kinocut/blob/b01b82eaf60c675451c74945f78239ccf01adfcd/README.md) describes CLI/Python/MCP access and integration with FFmpeg/HyperFrames. Selected [timeline schema](https://github.com/KyaniteLabs/kinocut/blob/b01b82eaf60c675451c74945f78239ccf01adfcd/kinocut/timeline_ir/schema.py) and [workflow spec](https://github.com/KyaniteLabs/kinocut/blob/b01b82eaf60c675451c74945f78239ccf01adfcd/kinocut/workflow/spec.py) contain typed contracts, rational times, operation restrictions and path checks. Those are useful adapter foundations. Their presence does not prove complete execution safety, timing fidelity or compatibility with Studio.

Its [highlight discovery](https://github.com/KyaniteLabs/kinocut/blob/b01b82eaf60c675451c74945f78239ccf01adfcd/kinocut/product/highlight_discovery.py) constructs bounded transcript windows and uses punctuation/heuristics, including English abbreviation patterns. Treat output as candidates. Polish linguistic quality and multimodal editorial quality remain untested. The adapter pilot must check cancellation, dependency isolation, revision mapping, partial failures and work without MCP registration. Keep Studio's brief, timeline and approval authority.

### 2. A currently popular editor can still be the wrong mandatory backend

OpenCut's [current README](https://github.com/OpenCut-app/OpenCut/blob/e668010778568641babef2cc40be4703ae6916d6/README.md) explicitly describes a rewrite and lists Editor API, MCP and headless mode as forthcoming. It points users to [OpenCut Classic](https://github.com/opencut-app/opencut-classic). This supports keeping OpenCut as an optional handoff, not claiming its new automation interfaces already work. Recheck a released API and a real headless render before promotion.

OpenTake describes a Rust timeline, command-based undo and authenticated MCP; its own platform evidence distinguishes macOS verification from Linux targets. StoryToolkitAI offers transcript/story search and editor export. Both are useful optional external workflows, but making either mandatory would add a desktop and packaging surface to a cross-host plugin. Their code licenses also require a separate integration decision.

### 3. Highlight extraction is not just removing silence

ClipsAI's [README](https://github.com/ClipsAI/clipsai/blob/8e73c8adc112c745b84ec240f11a91457bfd3141/README.md) targets audio-centric narrative video, uses WhisperX and requires a Hugging Face token for its documented speaker-reframing path. Its [ClipFinder implementation](https://github.com/ClipsAI/clipsai/blob/8e73c8adc112c745b84ec240f11a91457bfd3141/clipsai/clip/clipfinder.py) uses TextTiling over embeddings. The last observed default-branch commit and repository push are January 2024. It is a useful reference for topic candidates, not evidence of a maintained universal montage engine.

Auto-Editor proposes edits using audio/motion criteria and supports editor exports. Its current source describes a Nim application; the installed Studio version must be probed before using current documentation's options. PySceneDetect identifies scene transitions. FrameCut must combine those signals with source meaning, image evidence, brief, context and protected moments. Do not implement “keep the last take” as an unconditional rule: a later take can be less accurate or contradict the accepted wording.

### 4. Word timing and ASR quality need separate evaluation

[faster-whisper](https://github.com/SYSTRAN/faster-whisper/blob/9e472ae9de8bb374552f531f752654554b76b2d6/README.md) documents CPU INT8, word timestamps and integrated Silero VAD; CUDA requirements depend on CTranslate2. Upstream speed comparisons do not predict Work or a user's laptop.

[WhisperX](https://github.com/m-bain/whisperX/blob/db8fde4d31a3e7f49fe5835938685a76f5ba5477/README.md) adds alignment but documents overlapping-speech and unalignable-token limitations. Its [alignment map](https://github.com/m-bain/whisperX/blob/db8fde4d31a3e7f49fe5835938685a76f5ba5477/whisperx/alignment.py) includes Polish. That verifies a configured route, not Polish accuracy, model clearance or reliable timing for numbers. Missing word times remain explicitly estimated/unknown; do not silently label interpolated values as aligned.

Pyannote's [community-1 model card](https://huggingface.co/pyannote/speaker-diarization-community-1) states CC BY 4.0, gated access and offline use after obtaining the files. The library code is MIT. Keep download/token requirements separate from inference and never substitute its hosted precision pipeline without authorization. Speaker labels are anonymous tracks, not identification of a person.

### 5. Reframing needs intent and stability

The official [MediaPipe face detector guide](https://developers.google.com/edge/mediapipe/solutions/vision/face_detector) provides face locations and landmarks. FrameCut still needs to choose the subject, smooth crop motion, handle occlusion/cuts and preserve products, captions and screen content. A face detector alone cannot determine the relevant speaker or best framing.

The legacy [AutoFlip guide](https://chuoling.github.io/mediapipe/solutions/autoflip.html) includes an OpenCV 3 constraint and Bazel build. Studio's catalogued OpenCV 4 runtime is not evidence of that example's compatibility. Prefer a bounded current detector/tracker pilot over silently adding the whole legacy pipeline.

### 6. Licenses affect product architecture

[FFmpeg's official legal page](https://ffmpeg.org/legal.html) distinguishes LGPL from builds incorporating GPL components. Record configuration flags and distribution method; an external process does not erase redistribution duties. Check the actual codecs and binary sources before bundling.

[Remotion licensing](https://www.remotion.dev/docs/license/pricing) and its [FAQ](https://www.remotion.dev/docs/license/faq) distinguish free eligibility from company licensing. Keep it available, but do not promise that every Studio customer may use it without a paid license. HyperFrames' repository declares Apache-2.0, which makes the existing route a simpler default at the framework level; dependencies and media rights remain separate.

[GSAP's standard terms](https://gsap.com/community/standard-license/) include restrictions concerning competing visual animation builders. Existing coded animation use and a future visual editor are different deployment questions. Do not assume “no charge” means unrestricted open source. Mediabunny declares MPL-2.0; modified distributed library files require the appropriate source/license treatment.

[Vex's LICENSE](https://github.com/AKMessi/vex/blob/87d027cead8f7019f347ac004fe23e072cb520c6/LICENSE) is PolyForm Noncommercial 1.0.0. Do not copy its implementation into a commercial Studio module or assume GitHub visibility grants that right. No Vex code is included here.

### 7. A service dependency is a separate product choice

VEA's [README](https://github.com/Memories-ai-labs/vea-open-source/blob/4078381031d028ab3c86cdcb8d1c872a155ed9fc/README.md) describes a conversational timeline workflow and a datalake path that uploads footage. Configuration wording also mentions alternative backend selection; full offline parity was not established. It can inform a future optional connector but cannot justify a default “local processing” promise.

## Evidence ledger and remaining uncertainty

| Claim | Status / confidence | What the evidence proves; next resolving test |
| --- | --- | --- |
| OpenCut lists new automation as forthcoming | Verified / high | README at pinned commit; revisit a released interface and run a render |
| Kinocut has typed IR and workflow contracts | Verified / high | Selected source exists; adapter compatibility/security/performance NOT_RUN |
| Existing Studio exports a limited edit plan | Verified / high | Local edit_export.py inspection; no claim of layered rendering |
| WhisperX has a Polish alignment model mapping | Verified / high | Selected source map; word timing on Polish speech NOT_RUN |
| Stable-ts is archived; ClipsAI has old observed commits | Verified / high | GitHub metadata at snapshot; not a claim about every fork |
| FFmpeg + existing motion owners are the best minimal foundation | Supported inference / medium | Fits current ownership and capabilities; integration gates remain |
| Kinocut will save implementation effort | Unknown | Measure adapter effort and failures on the same three vertical workflows |
| Tiny ASR is adequate for finished Polish kinetic captions | Unknown | Transcription and word-boundary benchmark required |
| A detected face is the right crop subject | Unverified | Validate against brief and actual temporal footage |
| All 59 tools are installable on every host | Unverified | Existing Work inventory result does not generalize to OS/CPU/client |

Before promoting a candidate, record exact package/model/browser versions, transitive requirements, license files, available wheel/binary platforms, minimal probes, installation size and the chosen fallback. Default-branch pins in this document are research references only. No benchmarks, cost estimates or quality scores have been invented.
