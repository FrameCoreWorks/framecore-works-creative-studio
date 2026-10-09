# Capabilities and handoffs

Use for multi-owner work, linked revisions, resuming a project or an operation whose actual tool support is uncertain. Keep only the fields that prevent loss of a decision. This is an instruction contract, not an executable router, persistent database or reason to make the user fill in a form.

## Route by artifact and operation

Keep the requested stage separate from the medium. A direction, prompt, generated artifact, inspection and delivery specification are different outputs. Use the route table in the orchestrator for ownership; do not infer tool availability from an owner's name.

| Supplied artifact or task | Lead responsibility | Evidence boundary |
|---|---|---|
| Image supplied as a reference for a new asset | Reference Pack Curator plus the requested direction or prompt owner | The image controls only its assigned reference properties; it is not automatically under review |
| Approved base image supplied for an edit | Static Graphic Design Creator, or Image Prompt Architect for a prompt-only edit instruction | Preserve the approved base and named locks; review only when separately requested |
| Existing image explicitly supplied for review | Output Critic | Only visible/accessible pixels and actually measured file properties |
| Actual video clip | Video Prompt Architect | Temporal review requires accessible frames/time ranges; sound requires a real audio route |
| Motion video Studio rendered from a contract | Motion Graphics Workflow | The craft critique on its frames, the timing summary of its sound and the contract revision it came from |
| Actual audio, song or visible-singing diagnostic | Audio Production Director | Separate metadata, user report, transcript, and actual audio/video inspection; record range and method |
| Narrative scene or dialogue | Screenplay Story Architect | Story intent, continuity, action and exact selected dialogue |
| Commercial/editorial copy or narration wording | Copy Voice, supported by Humanizer | Audience, channel, supported claims and exact selected wording |
| Lyrics, music prompt, VO, sound design, music-first/picture-first plan or track-rights research | Audio Production Director | Provider-aware output, evidence-bound inspection and track-specific rights scope |
| Final delivery requirements | Delivery Documentation | Medium-specific requirements versus measured export properties; no invented certification |

Classify each supplied still image by its requested operation: reference for a new asset, approved edit base, or output explicitly submitted for review. References and edit bases are not automatically outputs under review. A supplied video with no accessible decoder may still support a review of its provided shot list or one actual frame. Name that narrower review. Never report that the full film or soundtrack passed. When a media operation is blocked, provide the useful plan or exact missing input without inventing an inspection.

## Check the actual capability when needed

For the operation being considered, distinguish:

- `planning_only`: instructions/specification can be prepared, but no execution is being performed;
- `callable_now`: an appropriate tool is actually exposed and supports this operation;
- `authorization_required`: the tool is available but this operation is outside the existing user authorization;
- `unavailable`: the required capability is absent or blocked;
- `unverified`: support, compatibility or resulting properties have not been established.

Tool availability and permission are separate facts. The user's request may already authorize reading their supplied files or performing an explicitly requested generation. Carry that authorization forward without asking again. Approval of a concept alone does not authorize a paid provider, external upload, publication or unrelated operation. A tool listing proves availability, not successful execution; a returned job ID proves submission, not a finished asset.

Do not probe accounts, providers or private services merely to build a capability map. Inspect only tools and assets relevant to the requested operation. Keep known costs distinct from estimates and unknowns. An unavailable preferred route is a reason to offer a bounded next step, not to silently use a different paid provider.

## What Studio executes itself

The [capability card](../assets/capability-card.json) lists every operation Studio runs with its own bundled tools, what each needs from the host (Python, Pillow, numpy, ffmpeg, Node.js, a browser or network), what it delivers and what to deliver instead when a requirement is missing, with the evidence observed so far. It also marks the boundary: image generation belongs to the host's own tool, and video, song and voice generators run outside Studio.

- Check a requirement in the current host before promising a file; a past observation is not a guarantee.
- When a requirement is missing, deliver the card's alternative and say why in one sentence.
- Keep the card and the owners' texts consistent: a change to what a tool needs or delivers updates the card in the same release.

## Minimal handoff

Pass the accepted facts and actual artifacts, not a summary that loses their exactness. For complex work retain:

1. Requested artifact/stage and next owner; source revision or short change description.
2. Selected concept and permitted adaptations; exact copy with language and line-break locks where applicable.
3. Actual accessible assets and property-level source authority; explicitly missing inputs.
4. Research question, decision-relevant sources, access date and unresolved current claims.
5. User requirement, execution readiness and observed result as separate facts.
6. Existing operation authorization and any real remaining boundary.
7. One acceptance test for the next artifact and the affected dependencies.

Do not copy private paths, credentials, confidential briefs or unnecessary personal data into shareable handoffs. No handoff implies that another agent ran. Use authorized delegation only when it adds value.

For poster + film + jingle, the orchestrator maintains the shared campaign premise and truth/copy locks. Static Graphic Design Creator owns the poster execution; Commercial Video Campaign Director owns the motion thesis. Audio Production Director receives the sonic job: role of voice/music/sound, intended emotion and pace, approved lyrics or narrative/copy source, durations as targets and relevant exclusions. Sequence and prompt compilers consume those decisions without reopening the concept.

## Revisions and resume

When a date, price, colour or approved line changes, trace it to the artifacts that use it. Edit the affected items within the authorized scope, preserve unrelated accepted versions, and list any downstream item requiring re-inspection. If the user requested only one separated asset, follow the working contract before altering a separately approved dependent asset. Do not manufacture a saved version or claim a missing asset remains accessible in a later chat.

On resume, read the supplied state and actual files. Resolve only a missing fact that blocks the next requested step. A prior quality verdict applies to the reviewed version and conditions; it is not a verdict on a revised export.

When a user supplies a conversation URL and asks to continue it, attempt the exact URL with the current host's available web/open capability. Treat only retrieved text as recovered context. Identify attachments that did not transfer and ask for the minimum missing source. For an explicit Codex↔ChatGPT Work transfer, use [the handoff template](../assets/cross-host-handoff.template.md); it carries decisions and evidence, not credentials or an implied sync service. The step-by-step procedure, including what to report when a link cannot be opened, is in [thread-link and cross-host resume](thread-link-and-cross-host-resume.md).

## Optional tool adapter boundary

Use an existing, exposed tool rather than pretending this package installs an integration. Before a requested operation, establish the actual input attachment, model/surface/operation, supported settings, permission and output destination. Afterward record the returned asset/job status and inspect the result where possible. Do not invent upload bindings, native parameters, measured loudness, continuity, cancellation, retry or cost controls that the tool lacks.

For an execution error, preserve the original inputs and error state, diagnose the relevant cause and retry only within the user's scope and the tool's documented limits. Avoid automatic repeated rendering or spending. A new output still needs its own applicable quality checks and acceptance.
