# anti-slop: decision map

Reviewed 2026-10-19 at [`439a2ef`](https://github.com/miqdadbadjuber/anti-slop/tree/439a2ef5b9dd0ebe74e8113ff43f5928d0fe2a6a) (plugin version 3.2.21, MIT, Copyright (c) 2026 Miqdad Badjuber, [licence](LICENSE)) after the owner sent the repository and chose a full adaptation. Studio restates its rules in its own English text and adapts its contrast checker; no skill file is copied.

| Part | Decision | Where in Studio |
| --- | --- | --- |
| Copywriting skill (AI writing patterns, what not to flag, signs of a human writer, draft-audit-final) | adapted, with Polish forms added | [AI writing patterns](../../skills/copy-voice/references/ai-writing-patterns.md) and [`ai_writing_check.py`](../../skills/copy-voice/scripts/ai_writing_check.py) in Copy Voice, used by Humanizer and output review |
| Core: purpose test, craftsmanship questions, liveliness dials and levers, Design Read, honest placeholders, verify before delivery | adapted | [craft rules](../../skills/pipeline-core/references/craft-rules.md) sections Purpose before technique, Liveliness, Honest content and verification |
| UI skill (dose caps, decoration, layout templates, app and dashboard patterns) | adapted; the checkable ones became lint rules | [craft rules](../../skills/pipeline-core/references/craft-rules.md#more-interface-patterns) and [`craft_lint.py`](../../skills/pipeline-core/assets/craft-lint/README.md) |
| Human skill (contrast, keyboard, focus, states) and its `contrast-check.py` | adapted; the checker rewritten with a self-test | [`contrast_check.py`](../../skills/pipeline-core/assets/craft-lint/contrast_check.py) and the `low-contrast` and `focus-outline-removed` lint rules |
| Layout-mobile skill | adapted for page and app mockups | [craft rules](../../skills/pipeline-core/references/craft-rules.md#responsive-layout) |
| Code-comment skill | not adapted | Studio does not ship software products; the original stays available through the extension |
| The em dash ban (R-02) | not adopted as a ban | Polish typography uses the dash correctly and a brand may choose it; Studio treats English em dashes as cluster evidence and follows the brand or user preference |
| Installer `npx antislop-ai` | not used in the registry | It writes a pointer into CLAUDE.md or AGENTS.md; the registry installs with the pinned skills CLI, which copies the skill folders only |
| Contrast MCP server | not used | The Python checker covers the same calculation without a server |

Registry entry: `anti-slop` in [extensions.json](../../skills/workflow-orchestrator/assets/extensions/extensions.json). The pinned skills CLI listed its six skills on 2026-10-19; no host installation was run.
