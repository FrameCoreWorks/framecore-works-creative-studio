# ccMixter

Sources: [Query API](https://ccmixter.org/query-api), [terms of use](https://ccmixter.org/terms). Read 2026-10-27.

Anonymous query API works without a key/account. `f=json`, tags, licence and limit parameters support bounded discovery. Response MIME was **text/plain**, but its body parsed as JSON; MIME alone would wrongly reject this search. Individual tracks can use BY, BY-NC and other CC variants; inspect the exact licence and all credited sample sources. The selected “Lost Roamin'” record (`71077`, Speck and credited collaborators) declared CC BY 3.0, but its MP3 URL returned 403. No retry followed.

Terms section 4 also limits using material to advertise/promote products or services other than the resulting work or oneself. The interaction with client advertising and the track's CC licence needs clarification; this report does not adjudicate enforceability. Hold it out of client-ad defaults. Numeric quota, required headers, cache policy and mandatory hotlink behavior were not established. JSON can expose MP3 and other submitted-file links; only the denied MP3 download was attempted.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
