# Client projects

The business side of creative work for a client, from enquiry to acceptance. Each step reuses Studio's normal owners; this page says which document each step produces. Rates, terms, VAT status and rights are always the user's inputs; Studio never fills them with its own numbers.

| Step | Document | Owner |
| --- | --- | --- |
| Enquiry | [Client intake](../../brief-architect/assets/client-intake.pl.md) ([English](../../brief-architect/assets/client-intake.en.md)), only the open questions | Brief Architect |
| Offer | Brief Contract with commercial fields, [offer and quote](../../brief-architect/references/client-offer-and-quote.md) priced by `quote_calc.py` from the user's rates | Brief Architect |
| Brand | [Brand kit](brand-kit.md): colours, fonts and their licences, logo files, tone, banned claims, legal lines | Pipeline Core, read by every owner |
| Concepts | [Concept presentation](../templates/concept-presentation.template.md): two or three directions in context, a recommendation and a numbered decision | the domain owner (static, video, motion, campaign) |
| Feedback | [Revision tracker](../templates/revision-tracker.md): consolidated feedback, revision, our error or change of scope | Workflow Orchestrator with the domain owner |
| Delivery | [Client handoff](../../delivery-documentation/references/client-handoff.md): files, naming, rights, AI-assistance line, acceptance protocol | Delivery Documentation |
| Messages | [Client email kit](../../copy-voice/assets/client-emails.pl.md) | Copy Voice |
| Afterwards | [Case study](../../delivery-documentation/assets/case-study.template.md) with the client's consent | Delivery Documentation |

## Client version of a document

A document the client reads (offer, concept, script, treatment, brief, report) states facts and decisions in its body and gathers everything assumed in one **Assumptions** box near the end: what was not confirmed, what the work depends on, and what changes if it turns out otherwise. No "(assumption)" notes scattered through the text, no internal reasoning, no Studio vocabulary. Every template above ends with that box.

| Template | Owner |
| --- | --- |
| [AV ad script](../../screenplay-story-architect/assets/av-ad-script.template.md) | Screenplay Story Architect |
| [Concept one-pager](../../commercial-video-campaign-director/assets/concept-one-pager.template.md) | Commercial Video Campaign Director |
| [Music-video treatment](../../creative-music-video-director/assets/music-video-treatment.template.md) | Creative Music Video Director |
| [Creator brief with usage rights](../../ugc/assets/creator-brief.template.md) | UGC |
| [Editor handoff: EDL, OTIO, shot list, step lists](../../opencut-video-studio/references/editor-handoff.md) | OpenCut Video Studio |
| Storyboard pages and PDF (`board_compose.py`) | Storyboard Board Architect |
| Shot list or AV script as XLSX, CSV, PDF (`sheet_export.py`) | Storyboard Sequence Architect |

Keep one project folder or conversation per client and keep the client's data there, not in plugin files. A user who works in ChatGPT can keep the brand kit and the offer terms in a Project; in Claude, in a Project or a project's CLAUDE.md; in Codex or Claude Code, as files in the project folder (AGENTS.md or CLAUDE.md can point to them).
