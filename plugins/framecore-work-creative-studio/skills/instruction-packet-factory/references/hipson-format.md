# Hipson format packets

Task Handoff makes Hipson-format packets; Hipson Handoff is kept only as the explicit entry point that points here (retired to a pointer in 1.64.0). This is the lightweight format, not the full Hipson system, which can be connected separately from https://github.com/Hipson47/Hipson.git as an optional expansion, never a required dependency.

## When it applies

- The user asks for a Hipson-style packet, research map or internet mapping packet by name.
- A workflow role needs a bounded research map, review packet or execution packet in that structure, without connecting the full Hipson repository.

It is not orchestration, evidence verification or an external research run. If the task needs knowledge of the full Hipson repository, prepare only the connection request.

## Fields

Required: `target_role` (the role that receives the packet), `goal` (the outcome it enables), `context` (brief, references, source constraints or repository evidence, compressed to what the receiver needs) and `exclusions` (what the receiver must not do). Optional: `source_rules` (allowed sources, evidence quality, search boundaries), `acceptance_criteria` and `output_schema`.

The shared packet fields (target role, goal, context, exclusions, evidence rules, acceptance criteria, output schema and handoff) are the Task Handoff's own; the Hipson format adds the research-map and internet-mapping fields in its templates.

## Packet types

- Research Map ([template](../../hipson-adapter/templates/research-map.md))
- Internet Mapping Packet ([template](../../hipson-adapter/templates/internet-mapping-packet.md))
- Bounded Instruction Packet ([template](../../hipson-adapter/templates/instruction-packet.md))
- Review Packet and Execution Packet, in the factory's instruction packet shape

## Method

1. Confirm the target role and packet type.
2. Compress the context to what the receiver needs.
3. State exclusions, evidence rules and acceptance criteria before the method.
4. Define the output schema so the receiver does not improvise its shape.
5. Hand the packet back to the orchestrator or the named target role.

Keep packets bounded, not research essays. Do not perform full research by default, execute external provider operations, claim verification without evidence or treat a packet's output as verified truth; task-relevant read-only public research follows the shared research gate. Leave out private workspace context, credentials, local paths and non-public examples.

## Handoff and checks

Review gate `instruction_packet_fit`; hand off `packet_id`, `target_role`, `packet_type`, `goal`, `context`, `exclusions`, `source_rules`, `acceptance_criteria`, `output_schema` and `handoff_target`. Check that the target and goal are explicit, the context is sufficient but not bloated, exclusions and source rules are concrete, the schema is usable, full Hipson is described as optional and separate, and no external execution or verification is implied.
