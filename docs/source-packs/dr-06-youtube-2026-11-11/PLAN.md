# DR-06 — plan badania

Goal: kompletny uczciwy pakiet badawczy pełnych animowanych odcinków i serii YouTube.
Spec: PROMPT.md, niezmieniony.
Architecture: trzy rozłączne specjalizacje badawcze, integracja leada, świeża niezależna recenzja.
Tech stack: publiczny web, read-only GitHub, Markdown/CSV/JSON, lokalny Python stdlib do kontroli artefaktów.

## Granice
Tylko katalog DR-06 i tymczasowe pliki. Bez instalacji, generacji, płatnych usług, zmian repo/runtime, uploadu, publikacji ani Claude CLI. Model hosta zachowany; modele pomocnicze jawne.
Adaptacja writing-plans do autoryzowanego researchu: wykonanie od razu zgodnie ze zleceniem; bez nowej bramki zgody i bez commitów.

## Role i pliki
- Lead Codex: dostęp multimedialny, polityki, synteza, ekonomika, oryginalne formaty, QA, HANDOFF.
- Catalog researcher: catalog/* — kanały, odcinki, jawny zakres dostępu, deepdives ograniczone dowodami.
- Production researcher: production/* — źródła twórców i narzędzi, potwierdzenie metod.
- Baseline/contracts researcher: baseline/* — 3 repo, SHA/data, istniejące kontrakty, propozycje bez deklaracji implementacji.
- Niezależny recenzent: review/* — świeży audit dowodów i zgodności.

## Kroki
- [x] Otwórz Hipson z acceptance i sprawdź dostęp legalny do publicznych filmów.
- [x] Uruchom 3 badaczy rzeczywistymi collaboration.spawn_agent; przypisania Hipson są tylko ewidencją.
- [x] Zbierz 15–25 kanałów, 30–50 odcinków, 8–12 pogłębionych kart, cel 40 użytecznych źródeł; każdą lukę policz.
- [x] Sprawdź aktualne oficjalne polityki YouTube.
- [x] Zintegruj series bible, pipeline, ekonomię, 3 DERIVED formaty, 5 NOT_RUN benchmarków i backlog.
- [x] Uruchom świeżą niezależną recenzję, napraw materialne uwagi, zapisz ack.
- [x] python3 verify_artifacts.py: hash promptu, schematy, URL, daty, zakres oglądu, komplet plików, NOT_RUN i brak obietnic wdrożenia.
- Końcowa bramka: Hipson fresh verify i close po rzeczywistym wyniku. Ostateczny status w ledgerze T-0008; nie jest deklaracją wdrożenia.

## Review focus
1. Metadane i transkrypcja nie dowodzą oglądu ani miksu.
2. Nowy upload nie dowodzi nowego workflow.
3. Cel liczbowy nie usprawiedliwia słabych lub zmyślonych URL.
4. Zdolność narzędzia z dokumentacji nie jest wdrożeniem FrameCore.
5. Własne propozycje i koszty pozostają DERIVED z założeniami.

## Wynik integracji
44 publikacje / 23 kanały w próbie głównej; 60 / 34 w całym katalogu. 12 kart, 11 filmów z próbką klatek, 7 odczytanych transkrypcji, 0 pełnych seansów i 0 odsłuchów. 32 długości oraz 11 dat/liczników w głównej próbie pozostają Unknown. Świeża niezależna recenzja pass_with_limitations, wszystkie materialne uwagi zamknięte. Pełna analiza audiowizualna i benchmarki pozostają niewykonane.
