# Creative Studio 1.124.2

A correction from a full test of Studio with Superpowers and Earshot Audio on a short logo animation (whoosh on the title, hit on the landing, finished MP4, sync check). The result was in sync within one frame, but the test showed that Earshot's light installation cannot run its `timeline` and `sheet` views: both need the full installation with models. Earshot Audio 1.0.2 and Studio's add-on list now say so, and on the light installation the sync is checked by measuring the sounds in the finished file against the frames.

Verification: source tests, and the end-to-end run before and after the fix in Claude Code, recorded in verification/earshot-audio-1.0.2-e2e.json. The full Earshot installation, ChatGPT Work and Codex remain NOT_RUN; the hosted plugins are updated separately.
