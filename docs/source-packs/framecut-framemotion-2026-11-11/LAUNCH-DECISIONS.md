> Portable copy of the earlier planning edition. Read [the packet index](README.md) and the current repository handover for the owner's intake, applicability, implementation and cleanup workflow. Proposals are not automatically approved architecture.

# Proposed launch promise and review termination

Status: concrete recommendations answering the independent builder check. These are not approved architecture or new standing user rules. Claude and the user may revise them before implementation; do not infer consent from silence.

## Minimum launch support

The recommendation is a complete domain extraction with an explicit capability matrix, not a release that silently treats every unavailable feature as optional.

| Surface / operation | Initial release requirement | What may remain explicitly unavailable |
|---|---|---|
| Codex, standalone and Studio companion | Install/discover the correct instance, load relevant knowledge, execute the default local route, inspect output bytes and retain review evidence | Paid/external providers absent from the brief |
| Claude Code, standalone and Studio companion | Same local execution proof in a fresh authenticated session | Current OAuth failure is an unresolved release blocker, not a passing result |
| GPT Work, standalone and Studio companion | Demonstrated package materialization, knowledge access and actual default-route execution with accessible artifact evidence | If the host cannot execute, label that capability unavailable; this does not satisfy the proposed full Work launch promise |
| Ordinary ChatGPT without execution tools | Knowledge/intake, explanation, an honest capability limit and a concrete handoff | Local rendering, filesystem inspection and native application operation; do not advertise them as tested here |
| FrameCut default route | Existing Python/FFmpeg edit, independent sound, captions, storyboard, export and retained meaningful tests/regressions | Multicam, optical flow, managed HDR and native NLE control not implemented by the extracted engine |
| FrameMotion default routes | Both the Canvas/motion-reel route and HyperFrames route, with declared supported output formats and the same request/revision evidence | Optional engines that are declared unavailable before work begins |
| Retained Remotion route | Preserve its knowledge/code/notices, verify packaged integrity and applicable existing tests; advertise executable support only after real render proof in that host | No promise of every current upstream feature or automatic licence entitlement |
| Named NLE interchange | No specific Resolve/Premiere/FCP/Avid native roundtrip is required for this initial standalone launch recommendation | Native interoperability remains NOT_RUN until a named-version import/output comparison passes; retain existing EDL/optional OTIO as bounded interchange exports |

Both default motion routes must pass wherever default local execution is promised. A route that cannot be supported must be removed from the launch promise explicitly during architecture review, not silently reclassified while closing a failed test. Preserving code does not obligate advertising untested capabilities. A limited preview release would be a separate, explicitly narrowed release decision.

This does not add model probes beyond the proposed 24-case host budget. Plan one relevant default-route exercise per applicable probe and cover the other default through local engine fixtures with host-observed execution evidence where available. If that cannot establish the declared matrix, do not call the full launch verified; scope another bounded pass explicitly.

## Review termination

Recommendation for the future product's default creative review policy:

- One initial review of the actual candidate. If its required checks pass, stop; no cosmetic rewrite merely to satisfy a minimum-round count.
- If correctable defects remain, allow one correction and one further review of the affected output, for at most two creative review rounds by default. An explicit brief may set another finite bound.
- A technical acceptance failure can never be waived by exhausting the round budget. At the bound, preserve the latest candidate, evidence and unresolved defects, return the existing blocked/review-required status appropriate to the schema, and request the next scope decision. Do not deliver it as accepted.
- A revision that changes approved copy, duration, assets or intent invalidates the affected evidence. Review only the necessary scope plus dependent checks; do not reuse stale acceptance.
- A one-shot instruction may waive the intermediate board approval for its explicit scope. It does not waive final self-QA, the honesty of review flags or actual user acceptance.

The bound applies to repeated creative generation/review cycles, not to a universal limit of two unit-test runs or to every debugging operation. Expensive calls retain their own explicit task authorization. This is a proposed resolution of conflicting historical three-minimum/two-maximum/stop-on-pass rules; preserve those historical sources unchanged and label their scope until the proposal is accepted.

Implementation tests should cover first-pass success, successful correction, remaining defect at the bound, unsupported required review, explicit custom bound, stale-revision rejection and a valid scoped one-shot waiver. The exact stored fields and status values must reuse existing contracts rather than introduce a second state machine.
