# AI writing patterns: what makes copy read as machine-made

A catalogue of the patterns that mark prose as generated, with the fix for each, in English and Polish. Adapted from [anti-slop](https://github.com/miqdadbadjuber/anti-slop) by Miqdad Badjuber (MIT, reviewed at commit `439a2ef`), its copywriting skill; the Polish forms and the dash policy are Studio's. [`ai_writing_check.py`](../scripts/ai_writing_check.py) flags the checkable ones. Copy Voice applies this when writing, Humanizer when polishing, and output review when copy is delivered.

Two rules govern everything here:

- **Never invent facts.** A rewrite adds no fact, name, number, date, quote or source that is not in the brief or supplied by the user. Specificity comes from the source, not from the rewrite; if a sentence needs a real detail to work, ask for it or write the plain version.
- **Do not sterilise.** Copy with no voice is as obviously machine-made as copy full of tells. Keep a supplied voice; matching the author beats scrubbing the tell.

**Look for clusters, not single tells.** One "however", one em dash, one short sentence, one formal word mean nothing. Three or more patterns in one short text, or the same pattern repeated, is the signal.

## Contents

- [Tone and voice](#tone-and-voice)
- [Rhythm and structure](#rhythm-and-structure)
- [Honesty and evidence](#honesty-and-evidence)
- [Hygiene](#hygiene)
- [Polish forms](#polish-forms)
- [What not to flag](#what-not-to-flag)
- [Signs of a human writer](#signs-of-a-human-writer)
- [Draft, audit, final](#draft-audit-final)
- [Checklist](#checklist)

## Tone and voice

| Pattern | Looks like | Fix |
| --- | --- | --- |
| Empty vocabulary | unlock, elevate, empower, delve, showcase, testament, landscape, journey, robust, seamless, cutting-edge, revolutionary, game-changer, next-level | say what the product does: "Work with your team in one shared space" |
| Significance inflation | "the future of", "a pivotal moment", "a new era of", "revolutionising" | the concrete effect: "cuts the time your team spends on status meetings" |
| Unproven social proof | "trusted by thousands", "industry-leading", "world-class", "loved by customers everywhere" | a real named customer or number with its source, or cut the claim |
| Weasel attribution | "experts say", "industry observers", "people report" | name the source or cut the sentence |
| Authority tropes | "at its core", "the real question is", "what really matters", "fundamentally" | state the point directly |
| Chatbot closers | "I hope this helps", "let me know if you have questions", "would you like me to expand" | end on the last concrete fact |
| Fake-candid openers | "Honestly?", "Here's the thing", "Real talk" | say the thing |
| Signposting | "let's dive in", "here's what you need to know", "without further ado" | start with the content |
| Caps for emphasis | "WE MUST ACT NOW" inside a paragraph | write the urgency into the sentence; a real headline may keep caps |
| Actorless passive | "the decision was made", "the page was updated" | name who did it, when the actor is known; passive stays for unknown or irrelevant actors |
| Abstraction with a human verb | "the data tells us", "the dashboard understands what you need" | what the thing actually does: "the dashboard opens on the three metrics you check daily" |
| Generic CTA | Get started, Learn more, Discover, Explore, Try now | the specific action: "Book a tasting", "Download the price list" |

## Rhythm and structure

| Pattern | Looks like | Fix |
| --- | --- | --- |
| Forced rule of three | "innovation, inspiration and insights" in every section | as many items as the content has |
| Negative parallelism | "It's not just X, it's Y", "Not only X but also Y", tacked-on "no guessing" | state what it is |
| Aphorism formulas | "X is the language of Y", "X is the currency of Z" | the precise claim |
| Staccato drama | "No templates. No defaults. No safety." in a run | one sentence that says it; a single short sentence for emphasis is fine |
| Synonym cycling | "the checkout… the process… the flow…" for the same thing | repeat the clearest word |
| False ranges | "from first click to final invoice, and everything in between" | list what it actually covers |

## Honesty and evidence

- **Fabricated specifics:** invented numbers, testimonials, names, dates or features that look real. Worse than a vague claim because it reads as honest. Write no number and no quote without a source; a placeholder is labelled as one (`[REAL DATA]`, "testimonial from a real client").
- **Speculative gap-filling:** "the company was likely founded in the 1990s". State what the sources say, or omit.
- **Generic positive conclusion:** "the future looks bright", "exciting times ahead". End on the last concrete fact or a real plan.

Studio's [claims rules](../../humanizer/references/copy-and-voice.md#9-claims-and-fact-checking), the [truth step](copy-development-and-human-voice.md#anti-generic-standard) and brand-kit approved claims decide what may be said; this catalogue only finds the shapes that hide an unsupported claim.

## Hygiene

- **Dashes.** In English, the em dash used as a connector is a well-known generated-text tell when it clusters with others. It is not banned: Polish typography uses the dash correctly for asides and dialogue (półpauza or pauza), editors use it on purpose, and a brand or user may prefer it. Follow the brand kit and the user's stated preference; when neither says, in English copy prefer a comma, colon, full stop or parentheses, and never rewrite a supplied text's deliberate dashes without saying so.
- **Bold overuse:** every key term bolded. Bold one thing, or none.
- **Scare quotes:** quotation marks for emphasis or distance. Keep them for dialogue, real quotations and titles.
- **Inline-header lists:** "- **Performance:** load times are faster" where the header repeats the item. Write the sentence.
- **Emoji in headings and bullets:** 🚀 Launch, 💡 Insight, ✅ Next steps. Emoji carry no information there; a brand voice that truly uses emoji in social copy may keep a few in the body.
- **Filler phrases:** "in order to", "due to the fact that", "it is important to note that", "at this point in time".
- **Stacked hedging:** "could potentially possibly". One qualifier.

## Polish forms

The same patterns in Polish copy (the checker recognises these):

| Pattern | Polish forms |
| --- | --- |
| Empty vocabulary | innowacyjny, kompleksowy, rewolucyjny, przełomowy, wyjątkowy (as default), najwyższej jakości, bezproblemowy, odkryj moc, wznieś na wyższy poziom, podróż (abstract), synergia, holistyczny |
| Significance inflation | „w dzisiejszym dynamicznym świecie”, „w erze cyfrowej transformacji”, „nowa era”, „rewolucja w” |
| Unproven social proof | „zaufały nam tysiące klientów”, „lider rynku”, „klasa światowa”, „pokochali nas klienci” |
| Weasel attribution | „eksperci twierdzą”, „badania pokazują” (without a named study), „wielu uważa” |
| Authority tropes | „w gruncie rzeczy”, „prawdziwe pytanie brzmi”, „to, co naprawdę się liczy” |
| Chatbot closers | „mam nadzieję, że to pomoże”, „daj znać, jeśli masz pytania”, „chętnie rozwinę” |
| Signposting | „zanurzmy się w”, „oto wszystko, co musisz wiedzieć”, „bez zbędnych ceregieli” |
| Negative parallelism | „to nie tylko X, to Y”, „nie tylko X, ale również Y” |
| Generic CTA | Dowiedz się więcej, Odkryj, Sprawdź (alone), Zacznij teraz |
| Filler | „w celu”, „z uwagi na fakt, że”, „warto zauważyć, że”, „należy podkreślić, że”, „na chwilę obecną” |
| Generic conclusion | „przyszłość rysuje się w jasnych barwach”, „podsumowując”, „to dopiero początek” |

Polish-specific: the dash is correct punctuation in Polish (see Hygiene); Ty or Państwo is the brand's choice (Copy Voice), not a tell; long compound sentences are normal Polish style, not padding.

## What not to flag

- Correct grammar and consistent style: professional writers are polished.
- Mixed formal and casual registers, often a sign of a real person.
- Dry or plain prose without specific tells is just dry.
- A precise formal word; only the listed vocabulary counts.
- A single transition word, a single dash, a single short sentence, curly quotes.
- Quoted text, titles, proper names, or a phrase being discussed rather than used.
- Unsourced claims are common everywhere; flag only the shapes above, and route truth to the claims rules.

## Signs of a human writer

Leave prose alone when it shows these: specific, hard-to-invent detail (a real address, an odd quote); mixed feelings and unresolved tension; era-bound references; varied sentence length; genuine asides and self-corrections. With a writing sample from the user, match its sentence length, vocabulary, openings and punctuation before removing any pattern.

## Draft, audit, final

1. **Draft** applying the patterns above, read aloud for natural rhythm and specific detail.
2. **Audit** with two questions answered briefly: "What makes this obviously generated?" and "Does it state any fact, name, number, date or source not in the brief?" Where code runs, run `ai_writing_check.py` on the text.
3. **Final:** fix both answers. A fabricated detail is a defect even when it sounds more human than the vague original.

## Checklist

- [ ] No fabricated numbers, testimonials, names, dates or claims; placeholders labelled.
- [ ] Empty vocabulary and buzzwords replaced with specific language (English and Polish lists).
- [ ] No rhythm tells: forced threes, "not just X, it's Y", staccato runs, aphorisms, false ranges.
- [ ] Every sentence names its actor where one is known; no abstraction doing human things.
- [ ] CTAs name the action.
- [ ] Bold, quotes, emoji and dashes follow the brand and serve meaning.
- [ ] A real voice is present (the user's sample or a chosen tone), not a sterile default.
- [ ] Read aloud: it sounds like a person.
