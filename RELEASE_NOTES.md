# Creative Studio 1.125.0

Setting up Studio now works the same way in ChatGPT, ChatGPT Work and Claude, right after installation: first Studio offers Superpowers, then Earshot. Earshot is explained in plain words: a sound engine that picks and makes sound effects for the moments in your film, puts them exactly on the right frame and checks that they fit, on your own machine, sending nothing out. You choose the full version (about 2.6 GB, it also listens and picks the best-fitting sound), the light one (about 200 MB) or none, and Studio installs your choice in the same conversation where code can run (ChatGPT Work, Claude Code, Codex). In Claude you no longer need to type "Configure Studio" after installing.

There is now one Earshot: the Earshot Audio plugin (1.0.5) is the only way Studio installs and runs it, and older descriptions were brought up to date. Superpowers now helps with the code around Earshot: it plans multi-step soundtracks, checks sound placement with a test first, diagnoses installation or engine failures, and verifies the finished film before Studio calls it done.

Verification: source tests and Claude Code runs before and after (cases C14, C18, C19 and C20), recorded in verification/host-evals. ChatGPT, ChatGPT Work and Codex remain NOT_RUN; the hosted plugins are updated separately.
