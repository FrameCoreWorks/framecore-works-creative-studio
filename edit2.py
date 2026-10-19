import pathlib,sys
def rep(path, old, new, count=1):
    p=pathlib.Path(path); t=p.read_text()
    n=t.count(old)
    if n!=count: sys.exit(f'{path}: expected {count} got {n}: {old[:70]!r}')
    p.write_text(t.replace(old,new))
S='skills/'
rep(S+'copy-voice/references/polish-copy-standard.md',"""| Ranges use the en dash without spaces |""","""| The em dash (pauza) with spaces is also correct; use one dash style per text, the brand's if it has one | Sobota — niedziela | mixing – and — in one text |
| Ranges use the en dash without spaces |""")
rep(S+'copy-voice/references/ai-writing-patterns.md',"""- Unsourced claims are common everywhere;""","""- Protected or approved fixed text (Studio's startup welcome, a client's locked slogan, legal lines): report findings to the owner, never rewrite it silently. A structured menu with bold labels and lists of three by design is not a cluster.
- Unsourced claims are common everywhere;""")
H=S+'hyperframes-workflow/references/art-and-explainer-motion-direction.md'
rep(H,"""main word to secondary text at least 3:1;""","""main word clearly dominant over secondary text (about three times the size, or a clear weight step);""")
rep(H,"""6. **Enter slowly, leave fast, then hold:** entries 0.3–0.4 s, exits about 0.18 s;""","""6. **Entries take longer than exits, then hold:** entries 0.3–0.4 s with an ease-out (fast start, slow settle, as in [motion craft](motion-craft.md)), exits about 0.18 s with an ease-in;""")
P=S+'pipeline-core/SKILL.md'
rep(P,"""- [references/hyperframes-workflow.md](references/hyperframes-workflow.md) for coded-video workflow.""","""- [references/hyperframes-workflow.md](references/hyperframes-workflow.md) for coded-video workflow.
- [references/craft-rules.md](references/craft-rules.md) for type, colour, layout, interface and liveliness rules shared by static, page and motion work.

Shared design tools (Python standard library, run where code runs; each README says what it proves and what it does not):

- [`craft_lint.py`](assets/craft-lint/README.md) flags machine-made design tells in HTML, CSS and SVG; [`contrast_check.py`](assets/craft-lint/contrast_check.py) computes WCAG contrast for any colour pair.
- [`design_md.py`](assets/design-md/README.md) exports a brand kit as DESIGN.md for coding agents and imports one into a kit.
- [`prompt_examples.py`](assets/prompt-examples/README.md) searches reviewed image and video prompt examples by medium and subject. Use it after the idea is chosen and before a web search for prompt technique; an example supplies structure, never the direction.
- [`ai_writing_check.py`](../copy-voice/scripts/ai_writing_check.py) finds clusters of machine-made writing patterns in English and Polish copy ([patterns](../copy-voice/references/ai-writing-patterns.md)).""")
ST=S+'static-graphic-design-creator/SKILL.md'
rep(ST,"""Coded output (HTML, CSS, SVG) also passes [`craft_lint.py`](../pipeline-core/assets/craft-lint/README.md) before delivery.""","""Coded output (HTML, CSS, SVG) also passes [`craft_lint.py`](../pipeline-core/assets/craft-lint/README.md) before delivery, and text over colour is checked with `contrast_check.py`.
- A landing page, website or app screen mockup, an HTML page or a slide or pitch deck design belongs here: apply the craft rules sections on interface patterns, liveliness, honest content and responsive layout, take the words from Copy Voice when they are a separate deliverable, and hand the export to Delivery Documentation. When the client's design system should travel to a coding agent, export it with [`design_md.py`](../pipeline-core/assets/design-md/README.md).
- For a generation prompt, [`prompt_examples.py`](../pipeline-core/assets/prompt-examples/README.md) can supply reviewed prompt structure for the chosen direction before any web search; it never chooses the direction.""")
