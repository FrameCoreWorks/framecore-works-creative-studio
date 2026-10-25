# Production worksheets: schedule, budget, approval gates

Read when a multi-stage video project needs a plan that people can run: a schedule from the delivery date backwards, a budget by line, the approval gates and the risks. Rates, fees, taxes and supplier prices are always the user's input at run time; Studio never assumes them. Mark every planned figure as planned until a quote, an invoice or a measured render confirms it.

## 1. Schedule from the delivery date backwards

Start from the fixed date (publication, event, client deadline) and place each stage's end before the next stage's start, with the owner's review time inside the stage.

| Stage | Owner (Studio owner or person) | Input needed | Output | Review by | Duration | Start | End | Depends on |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Brief and acceptance criteria | Brief Architect | the user's notes | Brief Contract | client | | | | |
| Idea and direction | Video Campaign or Music Video | Brief Contract | chosen direction | client | | | | brief |
| Script or copy | Story And Screenplay / Copy Voice | direction | locked script and supers | client, legal if claims | | | | direction |
| Storyboard and shot list | Shot Sequence | locked script | timed storyboard | client | | | | script |
| Assets and rights | Asset Manifest | storyboard | asset list with sources and licences | producer | | | | storyboard |
| Production | FrameCut, Motion Graphics, Remotion, Video Prompt | storyboard and assets | first cut or renders | producer | | | | assets |
| Sound and voice | Audio Production, voice companion | cut | mix and voice | client | | | | first cut |
| Captions and versions | Caption Studio | final cut | captioned versions per format | producer | | | | mix |
| Review and fixes | Output Review, motion acceptance | versions | accepted versions | client | | | | versions |
| Delivery | Delivery Pack | accepted versions | package, handoff letter, acceptance record | client | | | | review |

Rules: name the critical path (the stages with no slack); give every client review a date and say what happens if it is late (the delivery moves by the same number of days, or a stage is shortened, never silently); keep a buffer before the fixed date, sized by the project's risk (state the size as an assumption the user can change); one owner per stage.

## 2. Budget by line

| Line | Unit | Quantity | Rate (user's) | Planned cost | Status | Source of the rate |
| --- | --- | --- | --- | --- | --- | --- |
| Creative and production time | hour or day | | | | planned / quoted / invoiced | the user's rate card |
| Generation credits or subscriptions | credits or month | | | | | the provider's current price page, dated |
| Stock, music, fonts, licences | item | | | | | the licence page, dated |
| Talent, voice, crew, location | day or item | | | | | the supplier's quote |
| Revisions beyond the included rounds | round | | | | | the offer |
| Contingency | percent of the subtotal | | | | | the user's choice |

Totals are calculated, never estimated in words; taxes follow the user's status and country (the [quote calculator](../../brief-architect/references/client-offer-and-quote.md) where it runs). A line without a rate stays blank and listed as Unknown. Paid provider runs are planned in Tools And Costs and start only with the user's approval.

## 3. Approval gates

Each gate has an owner, a decision and what it locks. Work after a gate does not reopen what the gate locked without a recorded change.

| Gate | Decision | Locks | Evidence shown to the approver |
| --- | --- | --- | --- |
| G1 Brief | the goal, audience, deliverables and acceptance criteria are right | scope and budget frame | Brief Contract |
| G2 Direction | one direction is chosen | idea, tone, look basis | direction boards or frames |
| G3 Script and copy | the words are final | spoken words, supers, claims | locked script with claim IDs |
| G4 Storyboard | the order and timing are right | shot order, durations, formats | timed storyboard |
| G5 First cut | the edit works | structure and pacing | the first cut at full size and phone scale |
| G6 Final | ready to deliver | everything | accepted versions with QA results |

A request that changes something a gate locked goes through change control: describe the change, its effect on schedule and budget, and get a yes before doing it; record it with the date and the approver.

## 4. Risk register

| Risk | Likelihood | Impact | Early sign | Response | Owner |
| --- | --- | --- | --- | --- | --- |
| A client review is late | | | no reply by the review date | move the delivery date, or reduce scope by agreement | producer |
| Missing rights to an asset | | | no licence recorded in Asset Manifest | replace the asset or get the licence before G5 | Asset Manifest |
| A generator or tool fails | | | failed test render | switch to the planned fallback route | Tools And Costs |
| Unproven claims | | | claim without an evidence ID | rewrite or remove before G3 | Copy Voice |

Likelihood and impact are the producer's judgement, written as low, medium or high with one line of reason; they are not measured values.

## 5. Status report

At each gate or once a week: stage and percent of planned work done (stated as an estimate), the next gate and its date, open decisions with owners, budget spent against planned (only invoiced or quoted lines count as spent), new risks. Keep it to what changed.
