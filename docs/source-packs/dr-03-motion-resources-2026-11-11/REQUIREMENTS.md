# DR-03 — mapa wymagań do artefaktów
Mapa do recenzji, nie samodzielna deklaracja weryfikacji.

| Wymóg PROMPT | Artefakt i dowód |
|---|---|
| Baseline trzech repo, SHA/date, README/AGENTS/manifest/reviews | BASELINE.md; sources/baseline-inventory.json i baseline-sources.json; toolbox-catalog.json |
| FrameMotion bez wymyślonego repo/API, role Studio/Toolbox/FrameCut/Open Assets | BASELINE.md i IMPLEMENTATION_HANDOFF.md |
| useAnimations/Generative Icons dedup i niezakładanie wdrożenia | BASELINE.md sekcja dedup; B27/B28; REJECTIONS.md |
| Trzy klasy A/B/C | CATALOG.json/CSV; agents/runtime, knowledge, assets |
| 25–40 jakościowych kandydatów orientacyjnie, 8–12 deep dives | CATALOG, CARDS, DEEP_DIVES; counts końcowego verifiera |
| Wszystkie kategorie albo jawna luka | REPORT.md mapa pokrycia |
| Primary sources, pinning, source status | SOURCES.json; źródła blisko kart; METHODOLOGY.md |
| Implementacja/manifest/install scripts najlepszych bez wykonania | agents/runtime/DEEP_DIVES.md; review/LEAD_SPOTCHECK.md |
| Pełne karty, wejścia/wyjścia/runtime/export/cost/rights/maint/owner/test | CATALOG.json + CARDS.md; Unknown pozostawiony jawnie |
| Asset metadata, rendered-film vs source redistribution | agents/assets/CARDS.md i CATALOG asset_metadata; REJECTIONS |
| Absolute time/seek/RNG/bake/interaction adapter | TIME_ADAPTER.md; runtime/knowledge deep dives |
| Lottie/Rive/SMIL renderer compatibility, nie sama poprawność JSON | knowledge/assets karty; TEST_PLAN T01/T02/T08 |
| Polski tekst/font/layout | TEST_PLAN T05/T06; K01/K02/R03/R12 |
| Source→rule→condition→data→operation→example→limits→QA | DEEP_DIVES i lane deep dives |
| Forma integracji i właściciel, bez automatycznego skill sprawl | CATALOG integration/target_owner; IMPLEMENTATION_HANDOFF |
| Import, random-order frames, loop, alpha, text, formats | TEST_PLAN T01–T12, wszystkie NOT_RUN |
| Pinning/errors/retry/fallback/cost estimates | TIME_ADAPTER, karty, handoff |
| Trzy osobne rankingi | RANKINGS.md |
| Odrzucenia i REFERENCE_ONLY | REJECTIONS.md + asset cards |
| P0/P1/P2 i handoff do Claude | IMPLEMENTATION_HANDOFF.md |
| Rzeczywisty swarm i świeża recenzja | PROGRESS.md, Hipson assignments i review/REVIEW.md |
| Bez obcych zapisów/install/run/paid/upload/push | Granice PLAN i METHODOLOGY; wszystkie wykonawcze NOT_RUN |
| Weryfikacja, nie test produktu | verify_artifacts.py, Hipson check i final status |

