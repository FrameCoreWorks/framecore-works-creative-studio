# Polish copy standard

How Studio sets Polish copy for ads, posts, graphics, video text, emails and pages. The [checker](../scripts/pl_copy_check.py) finds what can be found mechanically; the rest is the writer's judgement. Apply it to copy written in Polish whatever language the conversation is in; English copy keeps its own conventions.

## Typography (the checker fixes these with `--fix`)

| Rule | Right | Wrong |
| --- | --- | --- |
| Quotes open low, close high; nested quotes use « » | „Miód lipowy” | "Miód lipowy", “Miód lipowy” |
| A dash between words is the en dash with spaces | Sobota – niedziela | Sobota - niedziela |
| Ranges use the en dash without spaces | 10–18, s. 5–7 | 10-18 |
| One ellipsis character | Czekaj… | Czekaj... |
| No space before , . ; : ! ? and one after | Taniej, szybciej! | Taniej , szybciej ! |
| A number and its unit stay together (no-break space) | 5 kg, 10 zł, 30 min | 5kg |
| A one-letter word (a, i, o, u, w, z) never ends a line (no-break space after it) | w Beskidach | w / Beskidach split |
| Digit groups of numbers from 10 000 are separated by a (no-break) space | 12 000 zł, 1 299 zł or 1299 zł (one style) | 12000 zł |

## Numbers, money, dates and time (the checker asks a person)

- **Money:** decimal comma, currency after the amount: `39,90 zł`. Use `zł` in consumer copy and `PLN` in tables, invoices and international contexts, not both in one text. Prices to consumers are gross.
- **Percent:** `30%` and `30 %` are both used; keep one style per project. A discount is counted from the lowest price of the last 30 days (see the [marketing rules snapshot](../../research-evidence/references/marketing-rules-snapshot.md)).
- **Dates:** `10 października 2026 r.` in prose, `10.10.2026` in tables and forms; never `10/10/2026`. Months and weekdays are lowercase: `w poniedziałek`, `10 października`.
- **Time:** the 24-hour clock, `18:00` or `godz. 18.00`, one style per project.
- **Ordinals:** `2. miejsce`, `XXI wiek`; the dot after an Arabic ordinal is required.

## Headlines and capitals

Polish headlines use sentence case: `Najlepsze ceny w mieście`, not `Najlepsze Ceny W Mieście`. Capitals belong to the first word, proper names, brand spellings the client uses and, in direct letters and messages, the polite `Ty`, `Twój`, `Pan`, `Pani` and `Państwo` (in ads and on pages `ty`, `twój` stay lowercase unless the brand's style says otherwise). All caps is a design choice for a few short words, not for sentences. Avoid `!!` and `?!`.

## Forms of address

Pick one per project and keep it: `Ty` (most consumer brands, social media), `Państwo` (formal services, institutions, older audiences, B2B letters) or impersonal forms (`Zamów`, `Sprawdź` work with `Ty`; `Zapraszamy` works with both). Mixing `Kup teraz` with `Zapraszamy Państwa` in one piece is the most common error the checker reports. The client's brand voice decides; when unknown, ask once or use the form the client uses on their own site.

## Language

- Write Polish first, not a translation: `Sprawdź`, not `Zrób różnicę`; `za darmo` or `bezpłatnie`, not `free`; `dostawa` or `wysyłka`, not `shipping`, unless the brand uses the English word.
- English words the audience uses (`newsletter`, `influencer`, `e-book`) stay; inflect them the Polish way (`newslettera`, `e-booka`).
- Keep the client's exact names, slogans and product names unchanged, including their capitals.
- Consumer-facing descriptions, warnings and terms are in Polish; a slogan or brand name may stay in another language.

## Length

Channel limits are in the [channel specs snapshot](../../research-evidence/references/channel-specs-snapshot.md); `--channel` checks one field (`python3 pl_copy_check.py --channel meta-headline "…"`). Write to the visible length. Polish words are longer than English ones: a headline translated from English usually needs a new, shorter idea rather than a squeezed translation.

## What the checker does not do

It does not judge tone, persuasion, idiom, grammar beyond these patterns, or whether a claim is true and allowed. A clean report means no mechanical problems were found, not that the copy is good.
