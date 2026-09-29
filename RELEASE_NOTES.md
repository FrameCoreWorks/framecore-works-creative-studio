# Creative Studio 1.1.1

This release standardizes skill names displayed in ChatGPT and compatible Codex interfaces.

- All 37 skills have a display name with spaces and initial capitals; AI, UGC, HyperFrames and OpenCut keep their spelling.
- Adds 14 missing UI metadata files and corrects the metadata structure for Copy Voice and Tool Routing Cost.
- Changes Workflow Self-Improvement to Workflow Self Improvement.
- Documents the naming standard and checks it before packaging future releases.
- Preserves skill IDs, routing, instructions, existing prompts, policies, provider knowledge and assets.

Validation covers all 37 display-name fields, preserved source content, package structure, source inventory, the existing installer checks and archive integrity. The naming gate also detects missing, misplaced and incorrectly formatted names. Source verification does not establish UI cache refresh on every client. No media generation, provider setup or client pilot is part of this release.
