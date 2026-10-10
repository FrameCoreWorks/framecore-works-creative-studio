# Client offer and quote

For a user who sells creative work: turn a client's request into an offer the client can accept, with a price built from the user's own rates. Studio holds no prices: rates, VAT status, typical packages and terms are the user's and are asked for, or reused from their own project notes or [brand kit](../../pipeline-core/references/brand-kit.md), never invented.

## Steps

1. **Intake.** Send or fill in the [client intake](../assets/client-intake.pl.md) ([English](../assets/client-intake.en.md)); only the questions the request leaves open. Record the answers in the Brief Contract with its commercial fields (below).
2. **Scope.** Name the deliverables (format, sizes, versions, languages), what is not included, the revision rounds included, the timeline from the client's materials and approvals, and who approves.
3. **Packages.** Offer two or three packages when the client's goal allows a real choice (for example the logo alone; the logo with a brand card; the logo, brand card and launch materials). Each package differs in outcome, not only in quantity. One package is right when the request is precise.
4. **Price.** Fill in a quote spec (`python3 ../scripts/quote_calc.py --example`) with the user's rates or fixed prices, their VAT rate or exemption basis, the discount if any, the advance and payment term, and the validity date. Run `quote_calc.py spec.json --markdown offer.md`. Without code execution, compute line by line and show the arithmetic.
5. **Rights.** State the licence or transfer of rights per package in plain words with the fields of use (below). Mark it for the user's or their counsel's approval.
6. **Deliver.** The offer document (Markdown, or the user's document tool), the spec, and a short email from the [client email kit](../../copy-voice/assets/client-emails.pl.md). Keep the user's own terms where they have them.

## Brief Contract: commercial fields

Add these to the Brief Contract when the work is for a client: client and decision maker; budget range or "not given"; deadline and fixed dates; deliverables with formats and versions; revision rounds included; use of the work (channels, territory, duration, paid media or not); rights wanted (licence or transfer, exclusivity); materials the client supplies and by when; acceptance criteria and how acceptance is confirmed.

## Changes of scope

Work outside the agreed deliverables, a new direction after a direction was approved, or a revision round beyond those included is a change of scope. Name it when it appears, estimate it with the same rates, and get the client's written yes before starting. Record it in the [revision tracker](../../pipeline-core/templates/revision-tracker.md). A correction of Studio's own mistake is never a change of scope.

## Rights in Polish practice

Polish copyright law distinguishes a transfer of economic rights (przeniesienie autorskich praw majątkowych) from a licence (wyłączna or niewyłączna). Either covers only the fields of use (pola eksploatacji) named in the contract, such as printing and digital copies, putting copies on the market, public display, broadcasting and making available on the internet; a transfer and an exclusive licence need written form; consent to modifications and derivative works (prawa zależne) is stated separately; the moment of transfer is often tied to payment. AI-generated elements may have limited copyright protection, which matters for an exclusive logo. These are points to raise, not legal advice: the user or their counsel writes the contract.

## Guardrails

- No invented rates, market prices or "typical" figures. If the user asks what to charge, explain what drives the price (time, use and rights, revisions, urgency, the client's budget) and offer to compute from their rate or target amount. A market rate is a public price claim: give one only from sources found now, with their date, or say that no reliable figure is available; never present an estimate from memory as the market.
- VAT status and the exemption basis are the user's statement; the tool only applies them.
- Keep client data in the user's project, not in plugin files.
