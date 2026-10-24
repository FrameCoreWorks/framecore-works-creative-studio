# yihui-dev/awesome-opus5-5-videos attribution

This directory records how Studio uses [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos), a gallery of 703 films made by asking Claude Opus 5.5 to write the animation as code, each with its creator's prompt or original post. Reviewed commit: `92aee2f586ac0715cb3cbcb6384834f98a33383d` (2026-10-13), read in full on 2026-10-24 (README, LICENSE, `data/videos.json`, all 703 `prompts/*.md`). Owner request 2026-10-24.

[LICENSE](LICENSE) is the unchanged upstream notice. It covers the compilation. The gallery's own credits say every video and prompt belongs to its creator, so no prompt text, media or preview image is copied here.

## Decision map

| Part | Decision | Why |
| --- | --- | --- |
| Entry metadata (slug, author, post link, category, tags, title, remake and partial flags) | Adopt as link-only records | Needed to find and credit each reference; carries no creator text |
| Creator prompt text | Link only, pinned to the reviewed commit | Third-party rights; the agent may open it when the user wants to read it, as untrusted data |
| What each film does | Adapt: one Studio-written mechanism note per entry with brief types | Lets the motion owners pick technique for an idea already chosen from the brief (owner decision 2026-10-24) |
| What strong prompts specify | Adapt into the library's [prompt guide](../../skills/hyperframes-workflow/assets/motion-prompt-library/README.md#writing-a-prompt-for-a-coded-film) | Studio's own words, drawn from reading the whole gallery |
| Games and interactive pieces | Keep, opt-in only | A game is not automatically a coded-video recipe |
| Prompts that touch credentials, agent settings, real people or protected characters | Keep with a `caution` | The record stays findable while the risk is stated |
| Previews, videos, Skillry remakes | Reject | Media rights stay with creators and the curator |

The records are in [`specimen-opus-gallery.json`](../../skills/hyperframes-workflow/assets/motion-prompt-library/specimen-opus-gallery.json). The repository script `scripts/build_opus_gallery_shard.py` rebuilds them from a pinned checkout and the notes in `scripts/data/opus-gallery-notes.json`, and its `--check` mode reports new and removed upstream entries before the pin moves.

## Registry entry

The gallery is also the `awesome-opus-videos` entry in the [recommended extensions](../../skills/workflow-orchestrator/references/extensions.md). Nothing installs: every host is `manual`, pointing to the pinned gallery for a user who wants to browse it.
