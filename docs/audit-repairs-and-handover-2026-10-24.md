# Audit repairs and handover implementation, 2026-10-24

Scope: 28 reviewed findings, four reference workflows, measured mixed routing, and the owner-requested Hallmark integration. No skill merges, renames or new Studio owners.

## Audit disposition

| Finding | Corrected area | Evidence |
| --- | --- | --- |
| ORCH-01 | Planning instructions discard authorization that the same skill requires preserving | Source correction reviewed; canonical contract validation |
| ORCH-02 | Snapshot date grants a research pass to rows explicitly not checked | Source correction reviewed; canonical contract validation |
| ORCH-03 | Offline disclaimer is unconditional despite the stable-craft exemption | Source correction reviewed; canonical contract validation |
| ORCH-04 | Malformed quote structures bypass validation and raise exceptions | quote_calc_test.py (12) |
| GFX-01 | Contrast check ignores text opacity | static_render_test.py (17) |
| GFX-02 | PNG wordmark antialiasing attenuates RGB twice | svg_wordmark_test.py (6) |
| GFX-03 | Containment ignores negative glyph ink bearings | static_render_test.py (17) |
| GFX-04 | Poster-code recipe uses the wrong path from its stated directory | Source correction reviewed; canonical contract validation |
| GFX-S01 | PDF Form scan loses inherited stroke width | print_pdf_test.py (12) |
| GFX-S02 | PDF bleed can pass outside the physical MediaBox | print_pdf_test.py (12) |
| GFX-S03 | Anisotropic transforms hide thin PDF strokes | print_pdf_test.py (12) |
| SC-01 | Missing copy filenames containing spaces are treated as inline text | pl_copy_check_test.py (8) |
| SC-02 | Google RSA counter ignores the bundled double-width rule | pl_copy_check_test.py (8) |
| VM-01 | Acceptance rejects a valid declared non-base output format | motion_acceptance_test.py (34) and producer binding Node checks |
| VM-02 | Storyboard wrapping emits an oversized intermediate token unchanged | board_compose_test.py |
| VM-03 | Acceptance recipe documents literal repeatable copy but CLI expects one file | Source correction reviewed; canonical contract validation |
| VM-04 | FrameCut decoder uses -vsync, rejected by installed FFmpeg 9 | FrameCut focused real FFmpeg 9 decoder regression |
| VM-05 | Sound recipe leaves a multiword --hit value unquoted | Source correction reviewed; canonical contract validation |
| AUDIO-01 | Documented caption CLI handoff loses active-word timings | captions_test.py (20) |
| AUDIO-02 | TTS guide rejects a Claude Desktop route supported by the registry | Source correction reviewed; canonical contract validation |
| AUDIO-03 | Python and JavaScript caption import disagree at half frames | captions_test.py (20) |
| DEL-01 | OCR status match is ambiguous when checking a complete copy inventory | image_probe_test.py (17, optional OCR dependency skip) |
| DEL-02 | Image placement checks ignore EXIF orientation | image_probe_test.py |
| DEL-03 | RGB/greyscale PNG transparency is reported absent | image_probe_test.py |
| DEL-04 | Brand guide clips an oversized token followed by another word | brand_guide_test.py |
| HOST-01 | C17/C20 checks allow artifact-free and test-free responses to pass | test_host_eval.py (34); actual ffprobe fixture; negative claims/commands/cue/input binding cases |
| HOST-02 | Installer test fixtures fail through macOS /var symlink | test_codex_install.py (13), resolved temporary fixture path |
| HOST-03 | Text-audit fixture requires fully hidden words although this browser correctly detects partial clipping | Actual Chrome targeted Node tests (2); partial and fully hidden-word fixtures |

## Remaining handover

- Language versions: reuse the current picture owner, locked names/claims, separate translated timing and per-language evidence.
- Website brand kit: bounded observed-versus-proposed draft, approval, then the existing project kit schema.
- Platform delivery: one dated placement card; Unknown stays Unknown, queued/submitted does not imply published/live.
- Accessibility: aggregate actual modality evidence; still-frame contrast cannot certify a complete audiovisual deliverable.
- Mixed routing: [12 fresh source-guided Codex cases](../verification/host-evals/2026-10-24-routing-codex.json), 11 strict checks pass and one comparison-read failure retained. All 12 primary routes appropriate on manual review; no evidence for merging owners. This is not native installed-client equivalence.
- [Four reference cases](../verification/host-evals/2026-10-24-handover-codex.json) pass their source-guided checks. They do not establish rendered translation, published ads or accessibility certification.
- [Five companion plans and all 37 display-name proposals](handover-development-proposals-2026-10-24.md) remain owner selections. They are not silently implemented.

## Hallmark

[Decision map](../plugins/framecore-work-creative-studio/integrations/hallmark/README.md), [native evidence](../verification/hallmark-native-2026-10-24.json). Complete source skill 2.0.0 installed separately in Codex; 177 source files unchanged plus one declared Codex metadata compatibility override, with generated test evidence separately inventoried. Fresh native discovery/read, static positive/negative fixtures and Chrome preservation checks run. Studio takes the narrow useful methods through existing static/review owners. Full themes and engine remain native and optional.

## Verification and deployment

The [machine-readable repair record](../verification/audit-repairs-2026-10-24.json) records the final regression state. Public GitHub publication, saved plugin parity with declared private overlay, Codex cached bytes and fresh active-client behavior must each be recorded separately. A local source or metadata check never establishes a ChatGPT/Work startup pass.

## Additional regression-discovered compatibility correction

The full check exposed a separate existing crossfade graph failure with the local ASS-capable FFmpeg 7.1: after timestamp normalization, xfade rejected an input rate of 1/0. An isolated graph reproduced the error in 7.1 and passed in system FFmpeg 9; the latter lacks ASS locally and cannot replace the full rendering test environment. FrameCut now normalizes both already-timed inputs to the exact sequence FPS immediately before xfade, including an earlier concat, and invalidates the assembly cache version. The existing crossfade and a new rational-rate cut-then-fade regression pass in the complete 44-test FrameCut suite. This is an additional compatibility repair discovered during the requested regression, not a reclassification of the 28 audit findings.

The local regression environment also required a temporary interpreter path without spaces for a generated test shebang and temporary storage on the Codex volume (the system volume had less free space than the 2 GiB render budget). The Earshot default-cache test now isolates its mocked environment from an existing configured native root; the separate configured-root test remains active. No user cache, model, system configuration or production Earshot behavior changed.
