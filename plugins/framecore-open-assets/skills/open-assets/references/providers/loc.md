# Library of Congress (LoC)

Sources: [JSON/YAML API](https://www.loc.gov/apis/json-and-yaml/), [requests](https://www.loc.gov/apis/json-and-yaml/requests/), [working within limits](https://www.loc.gov/apis/json-and-yaml/working-within-limits/). Read 2026-10-27. [Legal page](https://www.loc.gov/legal/) timed out; a collection rights-page retrieval was also inaccessible.

Public API reads need no account/key. Official limits distinguish JSON/YAML **20 requests/minute**, images 150/minute, streaming media 60/minute and media downloads 150/minute; excessive traffic can trigger a one-hour block and lower protective thresholds may apply. Budget below the ceiling (e.g. one JSON request every four seconds), stop on 429/challenges and obey Retry-After. No compulsory special header was established. Search responses exposed a 24-hour cache header; this is an observation, not a universal policy. Media variants vary: JPEG/TIFF/JP2, audio and moving-image resources. The selected Detroit Publishing photograph says **“No known restrictions on publication”**, which is not a CC0 licence or a guarantee. Preserve the advisory, collection context and item link. Only a JPEG was validated.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
