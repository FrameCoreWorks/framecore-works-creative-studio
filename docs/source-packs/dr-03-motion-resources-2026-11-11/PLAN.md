# DR-03 Motion resources — plan badania
Data: 2026-11-11. Hipson: T-0006. Lead: Codex (model hosta bez zmiany; identyfikator modelu nieudostępniony).
Spec: PROMPT.md; SHA256 11aa9f40f5f10857d3a0dd41643928743173d610e128addbbde255ed48e438d4.

Użyte skille: Superpowers 7.0.2 using-superpowers, writing-plans (adaptacja research), dispatching-parallel-agents, verification-before-completion; Creative Studio workflow-orchestrator i research-evidence. Autoryzowane wykonanie badania nie wymaga ponownego zatwierdzenia planu. Nie uruchamiamy Claude CLI: zaakceptowany wyjątek OAuth401. Claude pozostaje architektem; wyniki są materiałem do decyzji.

## Pliki i role
Lead: BASELINE.md, REPORT.md, CATALOG.json/CSV, CARDS.md, SOURCES.json, RANKINGS.md, TEST_PLAN.md, IMPLEMENTATION_HANDOFF.md, REJECTIONS.md, PROGRESS.md, verify_artifacts.py.
Trzy niezależne sesje collaboration: agents/runtime, agents/knowledge, agents/assets. Każda czyta pełny prompt i baseline trzech repo przed oceną nowości, zapisuje karty, deep dives i źródła. Pisze tylko swój podkatalog.
Świeży recenzent: review/REVIEW.md + review/REVIEW.json; kontrola dowodów, deduplikacji i specyfikacji. Wynik wraca do głównego czatu. Sesje po zakończeniu pozostają zapisem pracy i nie wymagają działania użytkownika.

## Kolejność i kryteria
- [x] Przeczytać prompt i zasady wszyscy/codex, rozpocząć Hipson.
- [x] Baseline trzech repo: README, AGENTS jeżeli istnieje, drzewa, manifesty i relewantne reviews; przypięte SHA i data; osobno wersje repo i instalacji.
- [x] Trzy klasy zasobów: ok. 25–40 trafnych pozycji łącznie, bez sztucznego dopełniania.
- [x] 8–12 deep dives: rzeczywisty kod, manifesty, install scripts, prawa i kontrolowany czas.
- [x] Scalić katalog, pełne karty, rejestr źródeł; rankingi nowości, assetów, wiedzy; braki kategorii.
- [x] Adapter interakcja → czas/seek → render, temporal QA, polski tekst, próby NOT_RUN, P0/P1/P2.
- [x] Świeża recenzja, poprawki z datowanymi backupami i strukturalna weryfikacja.

Hipson close jest ostatnią czynnością po zapisaniu artefaktów; aktualny status i świeżość checku przechowuje ledger T-0006. Wynik lokalnej kontroli: VERIFICATION.md.

## Stałe granice
Tylko własny katalog; inne badania, Shared i repo tylko odczyt. PROMPT.md niezmienny. Brak instalacji, uruchamiania kodu kandydatów, binarnych pobrań, płatnych usług, uploadów, push/deploy. Wszystkie próby wykonawcze NOT_RUN. Kontrola artefaktów nie jest testem produktu. Źródła: GitHub connector oraz dokumentacja/warunki przez web. Brak pełnych repo w projekcie Hipsona.

## Ryzyka recenzji
1. NEW wobec znanego Toolboxa; 2. dokumentacja ≠ test; 3. prawa filmu ≠ źródłowa redystrybucja; 4. seek w demie ≠ deterministyczny export; 5. metadane ≠ wygląd/alfa/loop quality.

