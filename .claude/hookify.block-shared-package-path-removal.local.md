---
name: block-shared-package-path-removal
enabled: true
event: bash
action: block
pattern: (^|[\s;&|(])(git\s+)?(rm|mv|unlink|rmdir)\b[^;&|\n]*plugins/framecore-work-creative-studio/
---

**Paths in the shared package are never deleted, renamed or moved** (AGENTS.md, current rule 5): the hosted ChatGPT update only adds and overwrites files, so a removed path breaks inventory parity.

To retire a file, keep its path and replace its content with an inert pointer or stub.
