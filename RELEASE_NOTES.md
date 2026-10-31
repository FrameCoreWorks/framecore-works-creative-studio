# Creative Studio 1.163.0

Studio now has a delivery gate that really blocks. `studio_gate.py` measures every final file in `export/` against the brief's `gate.json` and writes a PASS, FAIL or BLOCKED report tied to the file's hash. A Stop hook (`hooks/hooks.json`) keeps Claude Code, and Codex after the user trusts the hook in `/hooks`, from ending a turn while a final file has no PASS or user waiver. ChatGPT Work has no plugin hooks: there the model runs the script and shows the verdict.

Update: follow `CHATGPT_INSTALL.md`, `CODEX_INSTALL.md` or `CLAUDE_INSTALL.md`. In Codex, trust the new Studio Stop hook in `/hooks` after updating.
