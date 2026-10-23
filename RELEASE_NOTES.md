# Creative Studio 1.124.3

When Earshot Audio is added but its sound engine is not installed yet, Studio now asks one question with both choices: install Earshot's light engine (about 200 MB, on your machine) or make the sound right away with Studio's own sound engine. It runs neither before you answer and always says which engine made the sound. Before this, ChatGPT Work could switch to Studio's engine without asking.

Verification: source tests and Claude Code runs before and after (new case C16), recorded in verification/host-evals. ChatGPT Work behavior after the update remains NOT_RUN; the hosted plugins are updated separately.
