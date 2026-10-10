# Copy pack: {project}, {channel or campaign}

Revision {r1} · {date} · language {pl} · form of address {Ty / Państwo / impersonal} · approved by {name or pending}

## Brief in one paragraph

{Product or offer, audience, the one thing the copy must make them feel or do, the call to action and where it leads.}

## Locked inputs

| Item | Exact wording | Source |
| --- | --- | --- |
| Brand and product names | {as the client writes them} | {client site, brief} |
| Price and offer | {39,90 zł; lowest 30-day price 44,90 zł if a reduction is shown} | {client} |
| Legal lines | {consent text, Omnibus line, #reklama, warnings} | {marketing rules snapshot, counsel} |

## Copy by placement

Each field lists its characters against the channel's visible and hard limits (checked with `pl_copy_check.py --channel …`; limits checked on {snapshot date}).

| Placement and field | Variant | Text | Characters / visible / hard |
| --- | --- | --- | --- |
| {Meta feed: primary text} | A | {…} | {118 / 125 / –} |
| {Meta feed: headline} | A | {…} | {24 / 27 / –} |
| {Google RSA: headline 1–15} | – | {…} | {28 / 30 / 30} |
| {Google RSA: description 1–4} | – | {…} | {86 / 90 / 90} |
| {Graphic: headline, price, legal line} | – | {…} | {lines as approved} |

## Claims and rules

| Claim or wording | Evidence status | Rules (PL/EU) | Note |
| --- | --- | --- | --- |
| {"najpopularniejszy w regionie"} | {needs_evidence} | {superlative: flag} | {client to supply the source or we drop it} |

## Checks

- `pl_copy_check.py` on every field: {no findings / findings resolved: …}
- Read aloud once; checked on a phone-sized preview: {yes / not done}
- Open questions for the client: {…}
