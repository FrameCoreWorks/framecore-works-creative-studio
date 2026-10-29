# Agent Reach: decision map

Reviewed 2026-10-17 at [`94f06c1`](https://github.com/Panniantong/agent-reach/tree/94f06c1969dfc1834001269d79d3ad0972d9dee6) (version 1.5.0, MIT, [licence](LICENSE)) after the owner sent the repository. Studio's web reach adapts its Jina Reader route, challenge markers and public-URL guard under the MIT licence; no other code is copied.

| Part | Decision | Reason |
| --- | --- | --- |
| Reading public web pages (Jina Reader), YouTube subtitles, RSS, public GitHub | adapted into Studio as [web reach](../../skills/research-evidence/assets/web-reach/README.md) (1.90.0, standard library; YouTube needs yt-dlp), and the full CLI stays an extension | Fills a research gap in shell hosts when the host's own web tools cannot read a page or transcript; Studio's research rules (dated sources, no invented facts) stay in charge |
| Exa search through mcporter | extension, with a check | A separate service; whether it needs its own key or plan is Unknown at review |
| X/Twitter, Reddit, Facebook, Instagram, Xiaohongshu, Boss Zhipin (cookies, tokens or a logged-in browser) | reject | Needs exported cookies or a session; the upstream README warns of detection and account bans and suggests spare accounts. Studio never exports cookies, uses spare accounts or automates a platform against its terms |
| `install --system` (installs tools, writes `~/.agent-reach/`, skills and MCP configuration) | only on the user's explicit request | The default `install` is a read-only check; no longer offered by Studio or Toolbox (owner decision 2026-10-29) |

Removed from Studio's recommendations by owner decision 2026-10-29 and not moved to the FrameCore Works Toolbox catalog; nothing is offered for installation. Review evidence at the time: Not installed or run in any host or container at review (owner decision 2026-10-17: no tests this round).
