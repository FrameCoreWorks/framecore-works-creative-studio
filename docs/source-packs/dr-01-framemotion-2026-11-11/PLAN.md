# DR-01 — plan badania i syntezy

Data: 2026-11-11. Specyfikacja: PROMPT.md + SCOPE-CLARIFICATION.md. Hipson: T-0005.

Cel: praktyczne, źródłowe kompendium motion/compositingu i wiarygodny most do FrameMotion. Wykonanie badania autoryzowane bez kolejnej bramki planu. Nie jest to plan wdrożenia kodu.

## Role i pliki

- Host Codex: koordynacja, PLAN.md, synteza, QA-BENCHMARKS.md, CODE-AND-CONTRACTS.md, COVERAGE-MATRIX.md, IMPLEMENTATION_HANDOFF.md, integracja źródeł, weryfikacja.
- Agent craft: specialists/craft — warsztat A–D, typografia, 100 terminów; źródła Cxx.
- Agent recipes: specialists/recipes — 18 receptur, proces i mapa poradników; źródła R-Sxx.
- Agent backends: specialists/backends — backendy, repozytoria, publiczny main Studio, istniejące kontrakty; źródła Bxx.
- Świeży recenzent po integracji: review/ — kontrola wymagań i dowodów; nie implementuje ani nie zatwierdza architektury za Claude.

Agenci używają odziedziczonego modelu, bez override. Faktyczny identyfikator dostawcy/modelu nie jest ujawniony w artefaktach narzędzia: Unknown. Brak wywołań CLI Claude i fallbacków.

## Sekwencja

1. Odczyt pełnego promptu, zasad, Superpowers writing-plans/dispatching-parallel-agents/verification-before-completion, Studio workflow-orchestrator/research-evidence/deep-research-method.
2. Równoległe badanie pierwotnych źródeł; oddziel dokumentację, kod, test autora i własny test. Nie liczyć samych wyników wyszukiwania jako przeczytanych źródeł.
3. Synteza claim → source → decyzja → kontrprzykład → test; poprawne liczby i jednostki, porównania narzędzi, jedno nadrzędne timeline.
4. Własne małe testy analityczne JSON, rational FPS, granic przedziałów i zależności. Render/native/audio pozostają NOT_RUN.
5. Niezależna recenzja końcowej syntezy. Host rozstrzyga uwagi i wykonuje świeży weryfikator.
6. Rejestruje wyniki i akceptację Hipson; zamyka tylko po przejściu zadeklarowanych kontroli. Zwraca indeks, liczby i luki głównemu czatowi.

## Granice i kryteria

Zapis tylko w tym katalogu badania i własnym dozwolonym temp. Istniejące pliki przed edycją otrzymują datowaną kopię. Zero zmian pluginu/repo, instalacji, usług płatnych, uploadów, push/deploy. Publiczny kod jest czytany, nigdy uruchamiany. Brak wideo/audio nie staje się pozytywnym QA. Cel >=40 źródeł nie upoważnia do dopełniania listy.

Krytyczne ryzyka recenzji: niepoprawny render order, speed/value confusion, straight/premultiplied i color-space mismatch, float FPS drift, pomieszanie istniejącego kontraktu z propozycją, utożsamienie main z instalacją, prawa kodu vs fontów/assetów, deklaracje percepcyjne bez oglądania.
