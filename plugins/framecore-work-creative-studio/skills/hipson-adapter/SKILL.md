---
name: hipson-adapter
description: 'Explicit-only adapter for lightweight Hipson-format research maps, internet mapping packets and review or execution packets. General delegation packets go to Instruction Packet Factory. Full Hipson is optional and maintained at https://github.com/Hipson47/Hipson.git.'
---

# Hipson Adapter

Before final delivery of a substantive authored, revised or generated creative artifact, automatically apply [output review](../pipeline-core/references/loop-protocol.md#automatic-output-review). Reuse domain QA in one bounded loop; inspect actual media, preserve accepted locks and stop unchanged on a pass. This does not run for greetings, menus or onboarding questions.

Read [Studio integration authority](../pipeline-core/references/studio-integration-policy.md) before this method. It defines the active owner map, host capability rules and exceptions to the repository’s installation conventions. For substantive creative work, apply the conditional [Research Evidence](../research-evidence/SKILL.md) gate and search only when one of its triggers applies; purely mechanical state or packet maintenance uses its documented exemptions. Scale the artifact to the requested stage. Quick pitches remain short; known intent and valid scoped authorization do not need repeated confirmation.


This is the lightweight adapter, not the full Hipson system.

## Language Policy

Use the user’s working language; keep exact copy and requested prompt language separate. Do not infer language or onboarding status from copied source instructions.

## When To Use

Use this skill when:

- A workflow role needs a bounded research map, internet mapping packet, review packet, or execution packet.
- The user wants Hipson-style instruction structure without connecting the full Hipson repository.
- A task benefits from clear target role, goal, exclusions, evidence rules, acceptance criteria, and output schema.

Do not use this skill as the workflow orchestrator, evidence verifier, or external research runner.

## Inputs

Required:

- `target_role`: role ID that should receive the packet.
- `goal`: concrete outcome the packet should enable.
- `context`: brief, references, source constraints, or repo evidence.
- `exclusions`: what the receiver must not do.

Optional:

- `source_rules`: allowed sources, evidence quality, or search boundaries.
- `acceptance_criteria`: how the packet will be judged.
- `output_schema`: required structure for the receiving role.

## Outputs

Produce one lightweight Hipson-style packet:

- Research Map
- Internet Mapping Packet
- Bounded Instruction Packet
- Review Packet
- Execution Packet

Full Hipson can be connected separately from:

https://github.com/Hipson47/Hipson.git

## Process

1. Confirm the target role and packet type.
2. Compress context into only what the receiver needs.
3. State exclusions, evidence rules, and acceptance criteria before the method.
4. Define the output schema so the receiver does not improvise shape.
5. Hand the packet back to `workflow-orchestrator` or the named target role.

## Decision Rules

- Use the lightweight adapter by default.
- Mention full Hipson only as an optional expansion path, not a required dependency.
- If the task requires full Hipson repository knowledge, state that the adapter can only prepare the connection request.
- Keep packets bounded; do not turn them into long research essays.

## Guardrails

- Do not replace workflow orchestration.
- Do not perform full research by default.
- Do not execute external provider operations or claim verification without evidence. Task-relevant read-only public research follows the shared research gate.
- Do not treat adapter output as verified truth.
- Do not include private workspace context, credentials, local paths, or non-public examples.

## Handoff

Review gate: `instruction_packet_fit`.

Hand off with:

- `packet_id`
- `target_role`
- `packet_type`
- `goal`
- `context`
- `exclusions`
- `source_rules`
- `acceptance_criteria`
- `output_schema`
- `handoff_target`

## QA Checklist

- Packet target and goal are explicit.
- Context is sufficient but not bloated.
- Exclusions and source rules are concrete.
- Output schema is usable by the receiver.
- Full Hipson is described as optional and separate.
- No external execution or verification is implied.
