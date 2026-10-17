# Web reach

`web_reach.py` reads public sources for research with the Python standard library: no install, no login, no key.

```sh
python3 web_reach.py read https://example.com/page             # page as text (Jina Reader, then a direct fetch)
python3 web_reach.py feed https://example.com/feed.xml          # RSS or Atom entries
python3 web_reach.py github owner/repo                          # public repository facts and README
python3 web_reach.py youtube https://www.youtube.com/watch?v=…  # title and subtitles; needs yt-dlp (pip install yt-dlp)
```

Use it when a research decision depends on a public page, a feed, a public repository or a video's wording and the host's own web tools cannot read it. Every result names the source URL, the retrieval date and, for pages, the route that answered (`jina-reader` or `direct`); cite them. A bot challenge is reported as a failure, never returned as the page. Private, local and cloud-metadata addresses are refused and responses are capped at 5 MB.

Not included, by design: X/Twitter, Reddit, Facebook, Instagram and other channels that need cookies, tokens or a logged-in session. Studio never exports cookies, uses spare accounts or automates a platform against its terms. Jina Reader is a separate service with its own terms; the `--route direct` option avoids it.

Hosts: anywhere Studio runs Python with internet access (Codex, Claude Code, a desktop shell). A code sandbox without internet access (often the case in chat apps) cannot use it: say so once and continue with the host's own search.

Adapted from [Agent Reach](../../../../integrations/agent-reach/README.md) (MIT): the Jina Reader route, the challenge markers and the public-URL guard. The full Agent Reach CLI remains an optional extension.

Checked 2026-10-17: offline tests in `tests/web_reach_test.py`; in a Linux container `read https://example.com` answered through Jina Reader. Not run in a chat app's sandbox.
