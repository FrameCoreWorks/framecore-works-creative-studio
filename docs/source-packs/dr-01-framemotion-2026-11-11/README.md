# DR-01 — FrameMotion: profesjonalny motion design i compositing

**Data:** 2026-11-11. **Hipson:** T-0005. Pełny prompt zachowano w [PROMPT.md](PROMPT.md); doprecyzowanie zakresu ponad AE w [SCOPE-CLARIFICATION.md](SCOPE-CLARIFICATION.md).

Najważniejszy wynik: zachować istniejący motion-score i handshake FrameCut, a FrameMotion projektować jako kompatybilnego specjalistę/adapter. Raport obejmuje After Effects oraz merytoryczne porównania Fusion, Apple Motion, Cinema 4D, Blender, Nuke i Houdini. To badanie, bez zmian kodu wtyczek.

## Zawartość i liczby

- **100 terminów PL/EN**, **18 szczegółowych receptur**, **5 benchmarków** z adaptacjami 16:9 i 9:16.
- **10 rodzin backendów**, **22 mapowania technika → dane → kod → QA**, **12 zadań P0/P1/P2**.
- **124 rekordy źródłowe**, **121 odrębnych URL**, **117 jednostek po połączeniu rozpoznanych duplikatów/aliasów**. To dokumenty i pliki, nie tyleż niezależnych autorów ani potwierdzeń.
- Publiczny Studio main: **4611c9c4ed44579b8a2c0224c9276d955fccd8d6**, commit 2026-11-11T07:20:22Z, manifesty **1.174.1**. Odczyt lokalnego skilla także 1.174.1; nie porównano całego installed bundle i nie potwierdzono aktywnego runtime.

## Czytanie

1. [Główna synteza](COMPREHENSIVE-REPORT.md) — wyniki i mapa całego kompendium.
2. [Warsztat](specialists/craft/CRAFT.md), [słownik](specialists/craft/GLOSSARY.md), [receptury](specialists/recipes/RECIPES.md), [proces i mapa poradników](specialists/recipes/PROCESS-AND-TUTORIALS.md).
3. [Profesjonalne modele pracy](PROFESSIONAL-WORKFLOWS.md), [backendy i mapowania](specialists/backends/BACKENDS.md), [repozytoria i prawa](specialists/backends/REPOSITORIES.md).
4. [Audyt obecnego Studio](specialists/backends/STUDIO-AUDIT.md), [kontrakty i kod](CODE-AND-CONTRACTS.md), [przykłady danych](examples/README.md).
5. [QA i benchmarki](QA-BENCHMARKS.md), [macierz pokrycia/luk](COVERAGE-MATRIX.md), [IMPLEMENTATION_HANDOFF](IMPLEMENTATION_HANDOFF.md).
6. [Rejestr JSON](SOURCE-LEDGER.json), [CSV](SOURCE-LEDGER.csv), [kontrola linków](LINK-CHECK.json), [niezależna recenzja i rozstrzygnięcia](REVIEW.md), [wynik weryfikacji](VERIFICATION.json).

## Co faktycznie sprawdzono

Trzech specjalistów wykonało odrębne odczyty źródeł i inspekcję kodu; host przygotował syntezę/kontrakt/QA, a świeży czwarty agent recenzował pakiet i ponownie otworzył kluczowe źródła. Superpowers: writing-plans, dispatching-parallel-agents, verification-before-completion. Creative Studio: workflow-orchestrator, research-evidence i metoda Deep Research. Plan/przypisania/wyniki/akceptacja są rejestrowane w Hipson T-0005.

Własny `verify_research.py` sprawdza strukturę, cytowania, referencje plików, niezmienność oryginalnego promptu, hashe przykładu, graf zależności, rational FPS/próbki audio, zakresy, alfa i geometrię testową. Nie uruchamia pobranego kodu ani bibliotek renderujących. Weryfikację można powtórzyć poleceniem `python3 verify_research.py` uruchomionym w katalogu tego badania; wynik JSON trafia na stdout.

## Ograniczenia

**Natywne rendery, ciągłe oglądanie filmów, odsłuch i cross-platform parity: NOT_RUN.** Materiały wideo: NOT_VIEWED; wykorzystano jawnie opisane teksty i transkrypcje. Przykład sidecar jest propozycją, ma celowo **blocked preflight** przez brak konkretnego fontu i prawdziwego requestu FrameCut. Hipson może potwierdzić ukończenie badania i jego kontroli; nie stanowi certyfikatu renderera.

Brak adresów repo nowych wtyczek → Unknown. Nie utożsamiamy publicznego main z instalacją. Claude pozostaje głównym architektem; nie uruchamiano jego CLI i nie przypisujemy mu akceptacji propozycji. Backlog wymaga osobnego zlecenia wdrożenia. Link-check bada transport HEAD; strony Adobe mogą zwracać 403 mimo wcześniejszego odczytu przez narzędzie badawcze. Szczegóły i rzeczywiste liczby są w LINK-CHECK.json.

Nie zmieniono repozytoriów, Shared, konfiguracji ani zainstalowanych pluginów. Nie instalowano, nie publikowano, nie używano płatnych usług ani uploadów. Datowane kopie poprzedzają edycje własnych istniejących plików; pozostają jako ślad pracy. Materiały z innych zadań DR nie były łączone z tym badaniem.
