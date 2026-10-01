# Creative mode and learning mode

Since version 1.2.0, Studio recognizes two equally supported work intents:

- **Learning mode:** short onboarding, a personal curriculum, a lesson, independent practice and feedback on the attempt.
- **Creative mode:** the existing workflow toward the requested deliverable; the existing localized creation alias remains supported.

Every sent Studio-only invocation, greeting or startup-menu request copies the entire [single canonical welcome](../skills/workflow-orchestrator/assets/startup-welcome.pl.md). It introduces Studio, explains capabilities, invites optional materials and ends with the creative/learning choice. It adds no extra greeting and does not paraphrase the text. Repeated invocations repeat the same welcome while preserving earlier project and learning state; a concrete resume request continues the saved work. A creative-only choice leads to quick/expanded pace, the seven work areas and the needed task question. These steps apply regardless of the host's model or reasoning setting. Numeric replies belong only to a pending choice group; resolved menus expire. Two simultaneous groups use distinct digit/letter tokens, such as `7, A`. The first substantive offline lesson briefly discloses its research limitation. The [entry contract](../skills/workflow-orchestrator/references/startup-and-creative-menus.md) also covers older-conversation resumes and skipping already supplied decisions.

A direct project description or learning request enters the relevant workflow without redundant choices. Buttons depend on actual host capabilities; text selection remains supported. Quick/Deep controls pace and depth independently of intent.

## Starting to learn

Studio reuses information already supplied. Onboarding is sequential: **one question per message, the learner's answer, then the next needed question**. Choices accept a number or free text. Studio does not show the whole form, combine several decisions into one question or repeat resolved issues. It asks at most six short questions in total, selecting only those that affect the plan. Once enough is known, it prepares the plan and starts a lesson. Short answers, skipped irrelevant details and an unknown answer are accepted. Lacking software, equipment or a paid account does not block paper/text exercises.

Example: “I want to design posters independently. Beginner, 30 minutes three times a week, no budget. I prefer examples and exercises.” This complete input allows the plan and first lesson to start immediately.

## Curriculum and lessons

The plan describes the goal, module sequence, skills, exercises, progress criteria, tools and verified costs or unknowns, no-render alternatives and estimated effort. Broad goals combine shared foundations, selected specializations and an integrative project. Studio begins the first short lesson after the plan unless only a plan was requested.

Each lesson contains a goal, simple explanation, necessary term definitions, example, exercise and criteria. After an attempt, the learner receives one or two priority corrections and a check of understanding. The learner can request a simpler explanation, harder version, another example, quiz or skipped topic. Showing a lesson does not mark it completed.

## Coverage

The [domain map](../skills/workflow-orchestrator/assets/learning-domains.json) links existing skills for 14 areas: graphics/illustration, typography, story/screenplay, character intent/performance, reference/identity, storyboard/sequence, camera/light, commercial video, music video, copy/brand voice, prompting, audio/music, editing/motion and campaign/workflow.

Webinar support covers structure and materials; acting support covers intent/blocking; voice support covers pace/pauses/emphasis; VFX support covers effect planning. Studio does not offer a complete live-broadcast engineering course, advanced simulation training, clinical voice coaching or professional certification. Each domain records its boundaries.

## Switching modes and progress

A request for a finished result switches to creation without more lessons. A request to learn through the current project starts learning while retaining project context. Switching modes does not change accepted revisions, exact text or the selected concept.

Progress covers the selected path, per-domain level, current module, completed/skipped lessons, documented strengths, practice needs and next action. Without persistent saving, a compact [progress card](../skills/workflow-orchestrator/assets/learning-progress.template.md) can be copied for a break or another conversation. Memory and attachment transfer between hosts are not guaranteed.

## Tools and evidence

An explanation or exercise does not invoke generation, a paid provider, API/MCP or an upload. An exercise involving rendering first offers a no-render alternative. Actual execution requires a separate request and compliance with active host rules. A ChatGPT subscription does not guarantee free external services. Verify current capabilities and prices for the specific tool; keep unknowns explicit.

The method uses existing skills and [sourced teaching references](../skills/workflow-orchestrator/references/learning-mode.md#method-evidence). `evals/learning-mode-cases.json` contains 16 planned scenarios. Repository tests check structure and protected contracts; they do not establish that a host delivered these lessons or that learning was effective.
