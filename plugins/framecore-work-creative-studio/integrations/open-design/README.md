# Open Design: decision map

Reviewed 2026-10-19 at release 0.25.0 ([`de6d2c0`](https://github.com/nexu-io/open-design/tree/de6d2c072a18dfef80ecad4a455b31f0d5aca090)) and updated on 2026-10-22 to release 0.26.0 ([`bfee093`](https://github.com/nexu-io/open-design/tree/bfee093942f8578c8b6ec7f26862e96f81026a89), "Share, Review, Refine"). Apache-2.0 ([licence](LICENSE)); its motion skills carry their own MIT licences. The code was read, never run. No code or text is copied into Studio; methods are written again in Studio's own words.

| Part | Decision | Reason |
| --- | --- | --- |
| Desktop app, `od mcp install <agent>` (with `--print` and `--uninstall`) | extension | A local design workspace driven by the user's own agent. Registering its MCP server gives that agent write and delete tools over Open Design projects (`write_file`, `delete_file`, `delete_project`), so the user decides where to register it |
| `curl \| sh` installer in its README | reject | Studio installs only from a pinned, checked release and shows the change first |
| Share (0.26.0) | extension with a warning | Uploads project files to OpenDesign's cloud and needs sign-in; never with client material unless the client agreed |
| Telemetry | disclosed | On by default, including scrubbed and truncated conversation and tool content for quality review, until the user chooses Don't share; safety and reliability telemetry stays on in official builds |
| Craft rules, artifact linter, DESIGN.md, prompt templates | adapted earlier | `pipeline-core/references/craft-rules.md`, `craft_lint.py`, `design_md.py` and the licence-filtered prompt examples (from `78d5637`); unchanged in 0.26.0 |
| Photosensitivity screening | adapted | `hyperframes-workflow/assets/motion-quality/flash_check.py`, labelled screening, not conformance |
| Transcript sanity checks | adapted | FrameCut `transcribe` and `import-transcript` warnings; an English-only model refuses another language before decoding |
| Encode checks for audio and cover | adapted | `inspect-encode.py --audio required\|silent` and `--cover-time` |
| Flash and strobe limit, "the transition is the exit", right-to-left and complex scripts, beat-envelope restraint | adapted | `references/motion-craft.md`, `motion-sync/README.md`, Caption Studio readability defaults |
| Transparent overlay export from Remotion | adapted | Remotion implementation notes, checked with FrameCut's `has_alpha` probe |
| Pilot before a batch, 360 spin in quarter turns, conversation pacing and plain failures | adapted | Video Producer, Video Prompt, FrameCut, the extensions route and Tools And Costs |
| Five official motion templates | reject | Explicit remakes of third-party viral posts; Studio builds ideas from the brief |
| `frame-*` looks, the jury's numeric composite, the live-artifact runtime, the scroll runtime, interface animation corpora | reject | Ready-made looks or scoring outside Studio's review; not a delivery need |
| Page capture of other companies' sites | reject | Rights and identity risk |
| Brand capture of the user's own site, an optional motion block in the brand kit, fitting a reference clip's motion to the easing presets | noted for later | Ideas without a trigger yet; they go to the owner as notes |

The original app is not recommended by FrameCore Works: the Toolbox catalog listed it from 2026-10-29 and removed it in Toolbox 1.4.0 (owner decision 2026-10-31: Toolbox 1.4.0 lists only tools with no account, API key or separate desktop app). Studio's adaptation above needs nothing from it.
