# Creative Studio 1.129.0

Motion Graphics can now draw technique from all 703 films of the Opus 5.5 gallery.

## What changed

Every entry of [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) at commit `92aee2f` is a link-only record in the motion prompt library, with a Studio-written note on the technique, the brief types it fits, a link to the creator's post and a prompt link pinned to that commit. No creator prompt text or media is copied: the MIT licence covers the compilation and the credits leave each prompt with its creator. The gallery supplies technique after the idea is chosen from the brief, never the idea. A brief lookup lists up to three matching records; 16 records carry a caution (credential or settings instructions, real people, protected characters), and games and interactive pieces stay opt-in. A new guide covers writing a prompt for a coded film. Motion Graphics, Remotion and Storyboard Sequence Architect link the gallery, and the extension registry lists it as `awesome-opus-videos`.

## What did not change

Startup, routing, skill names and paths are unchanged; no path was removed.

## Verification limits

The canonical validator, library tests and the full check suite passed. In headless Claude Code evaluation, writing a prompt for another coding agent and showing a record with a caution passed; a storyboard-only brief still failed, because the model named the gallery but left the lookup for the build. Fresh ChatGPT, Work and Codex clients were not run, and the hosted ChatGPT plugin update is pending.
