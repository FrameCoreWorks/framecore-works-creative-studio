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

Keep one project folder or conversation per client and keep the client's data there, not in plugin files. A user who works in ChatGPT can keep the brand kit and the offer terms in a Project; in Claude, in a Project or a project's CLAUDE.md; in Codex or Claude Code, as files in the project folder (AGENTS.md or CLAUDE.md can point to them).
