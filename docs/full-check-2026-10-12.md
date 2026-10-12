# Full check: skills, orchestration, connections and handoffs

Written 2026-10-12 on the owner's request, before the main development work is closed. Baseline: `main` at `3144dd5`, package 1.66.0, 37 skills. Studio is in maintenance mode ([AGENTS.md](../AGENTS.md#maintenance-mode-owner-decision-2026-10-12)): this is a check, not a development round.

## Goal

Establish whether every skill, the orchestration, the connections between skills and the passing of tasks and state between them work as documented, and report each defect with its evidence. The plan is written first and the results are added below it.

## Rules

- Every finding carries its evidence type: `EXECUTED_CHECK` (reproduced by running something), `OBSERVED_SOURCE` (read in a named file and line) or `INFERENCE` (reasoned, not observed). Unknown stays Unknown.
- Severity: `critical` (breaks startup, routing to any owner, installation or user trust), `high` (wrong owner, lost task or state at a handoff, false pass), `medium` (contradiction or gap between documents that can mislead a run), `low` (wording, drift with no effect on a run).
- Findings from read-only helper agents count only after the finding is reopened in the named file and confirmed.
- Fixes follow maintenance mode: only confirmed defects, the smallest fix in the text the model reads, the case shown before and after. Protected: the startup welcome and its localizations, menu order and tokens, skill IDs, package paths (never deleted, renamed or moved), vendored snapshots.
- Host evaluations run in headless Claude Code within the owner's limits (at most 25 cases per pass, 5 per gate) and record cases, tokens and time. ChatGPT Work behavior is the owner's own test and is recorded as `PASS_REPORTED` only when he reports it.

## What already runs automatically

The canonical validator and `scripts/check_all.sh` already enforce: skill metadata and description budget, YAML safety, links and fragments, every reference reachable from a skill, every routed specialist present in the orchestrator's route table, duplicate routes, overlapping owners naming their neighbors, research gates, startup welcome identity, package identity, and the unit tests of every executable tool. This check does not repeat them; it runs them once as the baseline and covers what they do not.

## Phases

### 0. Baseline

Fresh worktree of `main`; record SHA and version. Run the canonical validator and the full `scripts/check_all.sh` with the browser motion suite; record every number.

### 1. Inventory and connection graph (`EXECUTED_CHECK`)

A read-only script, kept outside the package, builds the graph from the sources:

1. the 37 skills, their `agents/openai.yaml` interface and their frontmatter;
2. the orchestrator's route table: every owner it names exists, and every skill is either routed, reachable from a routed owner, or documented as explicit-only or support;
3. skill-to-skill links: every link resolves, and no skill points work at a skill that does not accept it;
4. the handoff matrix and the role map in Pipeline Core: every role in the matrix maps to a real skill, every mapped skill exists, and every role pair has a route in at least one owner's text;
5. executable tools: every script under a skill has a test or a documented reason it has none.

### 2. Handoff contracts per skill (`OBSERVED_SOURCE`)

For each of the 37 skills, read the `SKILL.md` and the references it requires and record: when it starts (entry condition), what it needs (inputs), what it produces (outputs), whom it hands to and with which fields, how it returns to the orchestrator, and when it stops to ask. Then compare each pair: what the sender writes against what the receiver reads, the route table against the skill's own scope, and the Project State template against the fields the skills say they carry. Read-only agents split the 37 skills; every finding is reopened and confirmed before it counts.

### 3. Startup, menus and command passing (`EXECUTED_CHECK`)

The startup welcome in English and Polish, numeric menu tokens mapped to routes, a sent file or text treated as a task, a repeated invocation, and a language change: covered by the Studio tests and by the host cases W01 to W06.

### 4. Routing behavior (`EXECUTED_CHECK`, host evaluation)

The Polish routing set (25 cases, with and without the Studio name) on 1.66.0. Last full run: 1.63.0 (23 of 25).

### 5. Handoff behavior (`EXECUTED_CHECK`, host evaluation)

The main suite (21 cases, three of them multi-turn) on 1.66.0, plus three multi-turn handoff cases written for this check, each passing a decision from one turn and one owner to the next:

- F01: directions for a poster, then the user picks one: the production owner makes that direction, not a new one;
- F02: a storyboard for a short ad, then the user asks for generator prompts: the prompts keep the storyboard's shots and timing;
- F03: a motion storyboard, then the user approves it: the next turn writes the motion contract from that storyboard, without re-asking settled facts.

The creative set (11 cases) ran on the released wording of 1.66.0 on 2026-10-11 and is not repeated.

### 6. Executable tools (`EXECUTED_CHECK`)

Covered by phase 0 (full suite and browser suite) and phase 1.5 (tools without tests).

### 7. Host check by the owner

A short checklist of standalone prompts for ChatGPT Work: startup, a routed task, a two-turn handoff, a delivery. Recorded as `PASS_REPORTED` or a finding when the owner reports it.

### 8. Report and fixes

Findings in one table with severity, evidence and state; confirmed defects fixed under maintenance mode; a release only when the package changes; the ledger entry and the Polish report to the owner.

## Results

Host runs: 61 cases in six passes, 4,189,885 tokens, 1,273 s, all in headless Claude Code (claude-sonnet-5-5); every record is linked from [host evaluations](host-evals.md).

### 0. Baseline (`EXECUTED_CHECK`)

`main` at `3144dd5`, package 1.66.0. Canonical validator PASS. Full `scripts/check_all.sh` exit 0 with the browser motion suite: Node 216 of 216, every Python suite OK (one with 3 documented skips).

### 1. Inventory and connection graph (`EXECUTED_CHECK`)

- 37 skills; the route table has 39 rows naming 35 skills and two profiles, and every owner it names exists.
- Not routed: the orchestrator itself (linked from ten owners) and `producer-ai-task-builder`, an explicit-only compatibility alias that forwards to Audio Production Director. No skill is unreachable.
- 199 skill-to-skill links from `SKILL.md` files resolve. The handoff matrix (53 rows) and `workflow-kit-routes.json` match exactly; every role in the matrix maps to existing skills.
- 92 executable tools. 16 are not named by any test: four validators run by `validate-studio.mjs`, four motion-toolkit helpers covered by `validate-motion-toolkit.mjs`, six vendored Animate engine tools, `export-svg-frames.mjs` and `inspect-encode.py` (used by `clip_review.py`). Low; no change.

### 2. Handoff contracts (`OBSERVED_SOURCE`)

Four read-only agents read the 37 skills and reported about fifty candidate defects. Each one below was reopened in the named file before it counted.

### 3 to 5. Startup, routing and handoffs (`EXECUTED_CHECK`)

- Startup and menus: W01, W02 and W04 to W06 PASS (the complete Polish and English welcome, then options 1, 2 and 3).
- Routing set: 21 of 25. RT14 failed once and passed on the rerun. RT01 and RT08, without the Studio name, were answered without a skill, as on 1.63.0. RT18 named Studio for a teacher worksheet and loaded no skill in both runs, where 1.63.0 loaded the orchestrator.
- Suite: 23 of 24 after rescoring M04 (the reply gave the player link without the word the check looked for).
- Handoff cases, read by hand:
  - X01: the direction chosen in turn 1 and the exact copy reached the poster unchanged.
  - X02: the Veo prompts kept the five shots and their order, with 4-second clips trimmed to 3 seconds because Veo has no shorter clip.
  - X03: after approval in a session without code execution, turn 2 wrote its own Python render script instead of the contract and the player route.

### Findings

| ID | Severity | Evidence | Finding | State |
| --- | --- | --- | --- | --- |
| F1 | high | `OBSERVED_SOURCE` | A rendered motion video with its contract was sent for review to Video Prompt Architect in eight texts: the shared output-review table in `loop-protocol.md`, the execution adapter, Delivery Documentation (skill and reference), the campaign director (skill and gate reference, twice) and asset-change routing. The role map, routing boundaries and route JSON give it to the Motion Graphics Workflow. | fixed: each text now names the Motion Graphics Workflow for that case |
| F2 | high | `OBSERVED_SOURCE` | Pipeline Core (three lines) and the orchestrator's kit (two lines) kept route lines that contradict the single route table: explainers, product films and UGC to Creative Video Producer, audiences and channel plans without a priced offer to the ecommerce director, music-video packets to Audio. | fixed: the lines now match the table |
| F10 | high | `EXECUTED_CHECK` (X03) | After approval in a session without code execution, a hand-made render script replaced the contract and the player route. | fixed: X03 FAIL, then FAIL on a first wording, then PASS (the contract in the reply with the player link) |
| F3 | medium | `OBSERVED_SOURCE` | No rule said which text wins when an owner's `kit/method.md` and its `SKILL.md` disagree. Examples: Video Prompt Architect's kit requires a storyboard for a single prompt; board and sequence kits send reference boards back and forth; the visual campaign kit hands static execution to Image Prompt Architect; the audio kit claims music-video Veo prompts. | fixed: the integration policy now says the `SKILL.md` and the route table win |
| F4 | medium | `OBSERVED_SOURCE` | Owners hand off along paths the handoff matrix does not list, and many rows name fields the sender never produces. | fixed: the matrix states that it lists core contracts, that a handoff in an owner's `SKILL.md` is also valid, and that missing fields are marked unknown, never invented |
| F5 | medium | `OBSERVED_SOURCE` | The ideation method (1.66.0) records the chosen direction in Project State, which had no field for it outside the commerce context. | fixed: `creative_direction` in both Project State files |
| F6 | medium | `OBSERVED_SOURCE` | Creative Video Producer built direction, beat map and shot cards itself, without the campaign director's, sequence owner's or prompt owner's methods, and sent dialogue to Copy Voice although the integration policy keeps it with Screenplay. | fixed: step 5 names the specialist methods and keeps dialogue with Screenplay |
| F7 | medium | `OBSERVED_SOURCE` | The motion reference said a direction owner and the sequence owner author an open motion brief, while the motion skill's step 2 (1.66.0) finds the idea itself. | fixed: the reference follows step 2 and keeps a direction set by another owner |
| F8 | low | `OBSERVED_SOURCE` | The captions README named an `import` command; the tool's command is `contract`. | fixed |
| F9 | low | `OBSERVED_SOURCE` | Asset-change routing sent a changed product reference for a designed piece to Image Prompt Architect; routing boundaries send designed pieces to the static owner. | fixed |
| H1 | harness | `EXECUTED_CHECK` | The M04 route check did not accept the player link or "Open contract". | fixed in the case file; the run is rescored |
| O1 | medium | `EXECUTED_CHECK` | RT18: named Studio, a teacher worksheet, no skill loaded (2 of 2 runs on 1.66.0). | open: mentioning teaching materials in the orchestrator's description changes startup metadata, which needs the owner's ChatGPT startup check first |
| O2 | medium | `EXECUTED_CHECK` | RT01 and RT08: short tasks without the Studio name are answered without Studio in Claude Code (since 1.63.0). | open: host skill selection; the description budget is at 7,773 of 7,800 characters |
| O3 | low | `EXECUTED_CHECK` | F02: "otwarty katalog" was read as the working directory, not the skills catalog. | open: the Polish word is ambiguous |
| O4 | medium | `EXECUTED_CHECK` | M04 on 2026-10-12: in a direct motion task the name was pictured literally (a wheat ear for „Kłos”); the name rule is in the direction owners, not in the motion skill. | open by the owner's choice of 2026-10-12 |
| O5 | observation | `EXECUTED_CHECK` | Without code execution, the built-in scene kinds give a simpler version of a richer motion idea; X03 now says so plainly. | recorded |

Recorded without a change, because they do not change a run's owner or result: gate names declared by owners that the gate registry assigns elsewhere; the `audio-production` role missing from the roster and gate registry; three named deciders for self-improvement adoption; Copy Pack template fields named by the schema; the Hipson description pointing both ways; Marketing's "offer framing"; the visual campaign kit's event-poster code list beside the one catalog; asset-manifest's "final candidate" wording; no owner executing provider calls (Studio runs none by design); captions built through the motion sync tool beside Caption Studio; cutdowns named by both video owners; a beat budget beside the no-formula rule. Static Graphic Design Creator restarting directions after a choice was reported but not reproduced: X01 executed the chosen direction.

### 6. Executable tools

Covered by phase 0 and phase 1.

### 7. Host check by the owner

Pending: the checklist is in the report to the owner; results are recorded as `PASS_REPORTED` or findings when he sends them.
