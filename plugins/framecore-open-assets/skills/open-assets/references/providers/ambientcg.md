# ambientCG

Sources: [API overview](https://docs.ambientcg.com/api/), [v3 assets](https://docs.ambientcg.com/api/v3/assets/), [licence](https://docs.ambientcg.com/license/). Read 2026-10-27.

The documented public assets endpoint and one download worked without registration/key. Assets and preview images use CC0, including commercial use without required attribution. A canonical asset link is available as `https://ambientcg.com/a/{id}`. Numeric quota, mandatory UA and fixed cache/linking rules were not found; respect actual HTTP cache headers. The provider explicitly cautions that this is a one-person service intended for hobbyists/educators and may not provide enterprise reliability. The v3 endpoint exposes download packages; Ground054's 1K-JPG ZIP was retrieved, CRC-checked and its seven images decoded. Other advertised variants include higher-resolution JPEG/PNG material maps and HDR-related assets; they were not downloaded. This is a graphics/material source, not general stock photos or SFX.

Implementation note: the provider register records the current policy gate. Historical HTTP tests do not prove runtime or host readiness.
