# ffmpeg-skill: reuse and integration review, 2026-10-28

**Later owner decision, 2026-10-28:** the owner requested adding this entry to Toolbox. Toolbox catalog 1.0.2 lists the pinned original at commit [`f68470c`](https://github.com/FrameCoreWorks/framecore-works-toolbox/commit/f68470c03f7268f0926cd5446fd100642aa6eb96). An isolated original skill-directory installation and Toolbox package/catalog-file checks passed; native client activation and Studio routing remain NOT_RUN. The original review below remains historical.

## Scope and decision status

Owner trigger: the owner supplied `https://github.com/kajisho5/ffmpeg-skill` in the ongoing repository-reuse review. The standing instruction is to preserve findings in Claude's handover. This task reviews source, compares existing capabilities and runs bounded synthetic checks; it does not install a user-facing extension or change Studio behavior.

Bounded scope packet: `FCW-REVIEW-FFMPEG-20261028`; receiving owner: Studio orchestration / FrameCut maintainer; goal: identify useful complementary media operations and their integration boundary; sources: pinned public upstream, current Studio and Toolbox; exclusions: new orchestrator, master timeline, skill duplication, provider activation, user-media processing and hosted publication; acceptance: source-backed comparison, reproducible narrow evidence, honest host/quality limits and a concrete recommendation. Only this review, the current handover and the development ledger may change.

**Recommendation: a strong candidate for an optional Toolbox execution tool, with a small Studio routing contract.** Prioritize audio-based recording alignment, multicam preparation and explicit HDR-to-SDR conversion. Preserve FrameCut as the editing owner and its accepted master timeline; preserve Earshot and Caption Studio ownership. This is a recommendation, not an accepted installation or implementation decision.

## Reviewed sources

| Surface | Reviewed state |
| --- | --- |
| [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill/tree/1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff) | `1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff`, version 2.17.3; MIT; 337 tracked files / 21,445,787 bytes in the complete Git tree, including documentation and demos, not an installed-runtime size |
| Creative Studio | `964c477f981ecf5bad26100ff6bd4ef91ca9fbfd`, version 1.150.0 |
| Toolbox | `23b84ac8ca1736c152457dc0262d43a1287aa27f`; its 32-entry marketplace does not contain ffmpeg-skill |

The upstream is an executable Python/FFmpeg tool layer, not just a prompt collection. Its generated contract contains **42 tools**. The standard-library MCP transport is local **stdio**; it advertises 12 core tools by default and can expose all 42. The source has a Claude plugin manifest and installer routes for Claude Code, Codex and Cursor. Those facts do not certify native installation or discovery in this session's clients.

## Useful additions versus existing Studio capabilities

| Capability | Upstream implementation | Existing FrameCore state and value |
| --- | --- | --- |
| Align camera and external recorder; correct clock drift | [sync.py](https://github.com/kajisho5/ffmpeg-skill/blob/1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff/scripts/sync.py): audio correlation, offsets, optional drift correction and replacement/trim output | Strong candidate for preparing source assets before FrameCut ingestion; return measured offsets and time mapping, not a new master timeline |
| Multicam assembly | [multicam.py](https://github.com/kajisho5/ffmpeg-skill/blob/1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff/scripts/multicam.py): source alignment, explicit switching, periodic/energy-based modes and edit/project exports | FrameCut's current [supported scope](../../plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/README.md#supported-scope-and-honest-delivery) explicitly excludes multicam. Useful optional specialist, with selected cuts mapped into the accepted FrameCut design |
| HDR/HLG/PQ to SDR, LUTs and typed color correction | [color.py](https://github.com/kajisho5/ffmpeg-skill/blob/1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff/scripts/color.py) | FrameCut explicitly requires a tested SDR conform before HDR editing and refuses silent tone mapping. A deliberate, reviewed derived SDR asset is a direct fit; this does not add HDR mastering to FrameCut |
| Footage preparation | `stabilize.py`, `denoise.py`, `deinterlace.py`, `sphere.py`, `proxy.py` | Useful optional stabilization, picture denoising, deinterlacing, 360 projection and proxy preparation; some depend on optional FFmpeg filters. Evaluate the specific operation when needed |
| Cuts, joins, speed changes, stills, overlays, captions, loudness, export | Existing 42-tool layer | Much overlaps current FrameCut, Caption Studio and audio tools. Do not migrate all implementations or create competing owners merely because another implementation exists |
| Machine-readable operation contract | [_contract.py](https://github.com/kajisho5/ffmpeg-skill/blob/1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff/scripts/_contract.py), `doctor`, structured errors/diagnostics and [MCP transport](https://github.com/kajisho5/ffmpeg-skill/blob/1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff/mcp/server.py) | Useful integration interface and design pattern: read actual arguments/capabilities, request a bounded operation and consume its evidence. CLI input schemas derive from argparse; roles, output semantics and some capability metadata remain authored tables |

The existing FrameCut source already supports rational timebases, one versioned project, cuts/gaps/crossfades, captions, reframing/keyframes, speed ramps/freeze, overlays, sound mixing, opt-in measured normalization, durable jobs and editor exports. Earshot supplies audio-specific analysis/processing. These are existing capabilities, not missing functionality to replace.

## Patterns worth retaining

1. **Contract and capability discovery.** Generate the CLI input schema from the actual parser and derive MCP descriptions from the same contract. `doctor` distinguishes available, missing and unknown capabilities and reports optional dependencies. This is stronger than interpreting a tool name as proof it can execute.
2. **Plan, execute, inspect.** A stored plan records source fingerprints, and execution refuses changed inputs. Output includes probe data, operation diagnostics and structured refusal reasons. Preserve the distinction between a plan, a successful command, decoded-media evidence and actual perceptual acceptance.
3. **Output protection.** Existing outputs require explicit overwrite; inputs are protected; timeout/interruption and staged outputs have explicit handling. A future adapter must preserve these semantics, with user scope deciding authorization.
4. **Small default tool exposure.** The 12-tool MCP subset is useful for context control. Keep optional runtime details outside Studio's already constrained startup entrypoint.

These patterns are candidate implementation references, not a reason to add a new knowledge layer or duplicate the complete 42-tool surface inside Studio.

## Limits that affect the recommendation

- Audio correlation aligns recording tracks; it **does not verify lip sync**. Low-confidence alignment and actual picture/sound agreement need review. Multicam energy-based switching is a signal heuristic, not identification of the best story moment or the current speaker.
- `fit`, `cropdetect` and contact sheets do not detect/track faces, products or subjects. The caller supplies the framing decision. `look.py` creates images; it does not inspect their creative quality.
- `--dry-run` is not a blanket promise of zero processing. The [deliberate-behavior record](https://github.com/kajisho5/ffmpeg-skill/blob/1ae1bdf1ca0adbb1606fbca493948b1bbb2f83ff/docs/design-decisions.md#dry-run) permits measurement passes, `--plan` intentionally writes a plan, and `verify` runs real checks despite accepting `--dry-run`. The generated contract correctly marks `verify` as not supporting dry-run. Use contract semantics rather than the README's abbreviated blanket description.
- Source fingerprints use file size plus SHA-256 of the first/last 8 MiB; for a large file this is not a full-content hash. Keep Studio's full asset hashes where identity/provenance requires them.
- Core execution uses local Python/FFmpeg; transcription requires separately available Whisper/Parakeet engines/models. Some engines download weights on first use. No model or transcription engine was installed for this review.
- Advertised GPU encoding is specifically Apple VideoToolbox in the documented routes. Detected NVENC/QSV/VAAPI/AMF does not mean the tool uses those encoders.
- Platform presets and upstream CI claims are not current platform-policy verification or tests in every FrameCore host. The full upstream test suite and native client installations were not run here. This is not a complete security audit.

## Narrow local verification

Environment: this Work execution workspace, Python 3.12.14, FFmpeg/FFprobe 6.1.1-3ubuntu5. No private media, API keys, external generation, model downloads or global/user-skill installation. Upstream code was checked out separately; tests used synthetic media.

- Static contract generation: PASS; 42 tool specifications.
- Local capability check: PASS (`ok: true`, no missing required or unknown capabilities); optional Parakeet/Whisper engines absent. The doctor also emitted an upstream-version-based FFmpeg security advisory; distribution backport/security status was not independently assessed, and the capability result is not a security certification.
- Selected upstream tests: **PASS, 7 tests, zero failures/skips, 81.109 seconds**. Exact cases: `ContractTests.test_contract_schema`, `ContractTests.test_mcp_tools_list_defaults_to_the_core_12`, `ContractTests.test_a_refused_plan_says_what_changed_and_leaves_an_audit_record`, `AnalysisTests.test_sync_detects_offset_and_replaces_audio`, `AnalysisTests.test_sync_fine_resolution_and_drift`, `OrchestrationTests.test_multicam_offsets_and_switch`, `PictureTests.test_hdr_to_sdr_tonemap`.

The selected suite covers the contract schema, MCP's default 12-tool exposure, refusal/audit after a planned input changes, measured recording offset plus replacement, measured drift correction, multicam alignment/rendering and HDR-to-SDR output metadata. A synthetic fixture passing its checks does not certify visual grading, long client recordings, every HDR/Dolby Vision profile, transcription, all 42 tools, or installed-client behavior.

| Host surface | Evidence in this review |
| --- | --- |
| Work local Python/FFmpeg execution | Contract/doctor and the selected synthetic checks above; this is local CLI evidence |
| Work/ordinary ChatGPT installed plugin or MCP connection | NOT_RUN; upstream's local stdio server is not automatically a ChatGPT remote connector or portable Work package |
| Claude Code native plugin/MCP | Declared upstream route; fresh install, discovery and execution NOT_RUN |
| Codex native skill/MCP | Declared upstream route; fresh install, discovery and execution NOT_RUN |

## Proposed integration boundary

Toolbox should list the pinned original as an optional execution dependency if an installation task is opened. Preserve the original MIT attribution. A FrameCore wrapper should exist only if real host/contract differences require it; no wholesale engine copy into Studio and no new repository are justified by this review alone.

Studio retains brief, exact-copy/asset locks, storyboard acceptance, project revision, master timeline and final review. A bounded request to ffmpeg-skill should carry operation, source IDs/paths and hashes, permitted parameters, source/master timebase mapping, output destination, overwrite scope and required verification. The response should return derived assets, measured timing/color/audio facts, commands/version, warnings, checks and explicit failures. Re-ingest the verified derived asset under the existing Studio owner. A separate `render.py` project must not silently replace the master FrameCut project or imply storyboard approval.

Suggested first acceptance case: an explicitly requested HDR-to-SDR conform followed by FrameCut ingestion, with source/derived hashes, duration/frame/audio checks and a visible color review. A second bounded case can align a camera and recorder; multicam needs a separate test of offset/drift/timebase conversion and the preservation of accepted edit choices. Failure, missing filters, changed inputs and output collisions must remain explicit. Test each requested host separately and record native discovery distinctly from a direct CLI run.

## Review closure

Only repository documentation changes in this task. The external tool is not installed, registered, adopted or published as a FrameCore plugin. Studio 1.150.0 and companion runtimes remain unchanged. Existing independent-companion decisions and the earlier Workflow Kit review remain in force. The next implementation step requires a bounded owner task; this review does not authorize a broad FrameCut rewrite or another orchestrator.
