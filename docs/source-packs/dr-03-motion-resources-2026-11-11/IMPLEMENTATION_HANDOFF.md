# IMPLEMENTATION_HANDOFF — DR-03 motion resources
Data: 2026-11-11. Odbiorca: **Claude, główny architekt FrameCore**. To materiał do analizy i planowania, **nie architektoniczna akceptacja**, nie gotowa integracja. Próby wykonawcze wszystkich kandydatów: **NOT_RUN**.

## Co przekazujemy
Pełny raport REPORT.md, BASELINE.md, katalog CATALOG.json/CSV, pełne CARDS.md, 12 DEEP_DIVES, SOURCES.json, trzy RANKINGS, TIME_ADAPTER i TEST_PLAN. Source pin ≠ installed runtime; source registry i agent artifacts zachowują brakujące dane. Root: ten katalog DR-03. Nie ma zmian repozytoriów/pluginów/Shared/INDEX.json.

## Decyzja produktowa do rozważenia — DERIVED
Najpierw małe zasady i adaptery dla bieżących rendererów. Studio już ma master frame clock, Lottie/Pixi/D3/Three i cztery werdykty QA. FrameMotion repo/API nie zostało podane; nie projektujemy jego istniejącej architektury z domysłów. Toolbox discovery/instalacja pozostaje osobne od motion execution, a Open Assets od assetu/rights/provenance.

Przed implementacją Claude powinien:
1. Wskazać rzeczywisty repo/pin/API FrameMotion i wybrać jeden istniejący owner dla danego dodatku.
2. Zweryfikować delta względem najnowszego HEAD, ponieważ nasze commity to snapshot 2026-11-11.
3. Wybrać jeden bounded pilot, fixture i kryteria z TEST_PLAN, w ramach kolejnej autoryzacji wykonawczej.
4. Dopiero po wynikach rozstrzygnąć dependency/admission/skill-adaptation. Obecne Toolbox rules wymagają konkretnej wykazanej poprawy; review kodu nie zastępuje tego gate.

## Backlog — propozycja, nie wykonane zadania
| Priorytet / ID | Zadanie i właściciel proponowany | Artefakt implementacyjny | Acceptance po osobnej próbie |
|---|---|---|---|
| P0-01 | Studio motion QA: K01/K02, exact-copy grapheme+font contract | Mały dodatek do istniejących instructions + własne NFC/NFD/ZWJ/PL fixtures | T05/T06, brak samodzielnych combining marks/tofu, zgodna copy i layout; fonts.check negative test |
| P0-02 | Studio motion QA: K03/R10, zachowanie badanego ruchu | Capture policy + explicit settled/time + negative live-clock fixture | T02/T07; baseline A repeatable, celowo live B FAIL lub INCONCLUSIVE |
| P0-03 | Claude/FrameMotion po repo intake: model czasu | Minimalna deklaracja pureSeek/replaySeek/bakedOnly/unsupported; TIME_ADAPTER jako wejście | Każda operacja ma jednoznaczne błędy i brak cichego clock fallback |
| P0-04 | Studio/Open Assets: rights+asset identity split | Oddzielne code/font/model/media licences, file hash i source/release pins | Brak użycia/redystrybucji Unknown; nie mylić black background z alpha |
| P0-05 | Motion owner: R06 narrow helper spec | noiseAt(frame,coords,seed), modulo przed phase dla loop; bez nowego engine | T02/T03; powtarzalny pełny loop w zadanej konfiguracji |
| P1-01 | Motion owner: R03 text SDF spike | Local font manifest, readiness cache, timeout i jawne failure | T05/T12 + headless/Three test; zero niejawnego CDN |
| P1-02 | Motion owner: R01/R12 przy potrzebie geometrii | Small shape/glyph adapter, nie engine swap | T01/T02/T05; odrzucenie holes/multi-contour jeśli unsupported; prawa fontów |
| P1-03 | Motion owner: R04/R05 whitelist static bloom/outline/CRT | Per-effect clock+RNG+padding contract | T02/T04/T07; glitch/history nie korzystają z samego seed uniform |
| P1-04 | Open Assets consumer: A01/A02/A06 bounded acquisition | Pojedyncze wybrane pliki + provenances, nie nowy generic provider | T01/T03/T04/T06/T11; asset saving effort zmierzony przy równym briefie |
| P1-05 | Studio/FrameCut: K04/K05/K07/K08 | Istniejące refs: onset/frame, renderer matrix, alpha evidence, side effects | T08/T09/T10 zgodnie z wybraną metodą, pełny playback/listening jeśli audio |
| P1-06 | Export utility: R09 qualification; R02 rights resolution | Stable package wybór, platform pin, font/image limits; wyjaśnienie license label | T01/T04/T10/T12; pamięć/crash i native matrix; production HOLD do wyniku |
| P2-01 | FrameMotion po API: K06/A05 Rive | Zgodny WASM/runtime, linear first, fixed-step replay i event log | T08+feature matrix; odmowa unsupported Layer Masks i determinism gaps |
| P2-02 | Motion 3D: A03/A04/R08 | Retarget/root motion/VDB clip lub seeded sim bake | Clip boundaries i loop, FPS, pamięć; temporal review w docelowym rendererze |
| P2-03 | Resource gaps | Tylko rzeczywista potrzeba alpha overlays / ASCII / halftone / cloth/fluid | Per-item prawa i mały porównawczy test; bez sztucznego rozszerzania katalogu |

Priorytety leada powyżej porządkują pojedyncze sugestie autorów kart. P0 R03/R09 w kartach oznacza **kwalifikację ryzyka**, nie instalację produkcyjną; w tym wspólnym backlogu ich próby są P1. Żaden nowy entry Toolbox nie jest gotowy do admission na samym researchu.

## Zależności i zachowanie błędów
Pin source SHA, dokładne package version/lock i osobno asset/font/WASM checksum. Nie instalować HEAD prerelease dlatego, że jest odczytanym commitem. Przed zmianą dependencies sprawdzić istniejący compatible project. Git branch w source Cargo manifest nie dowodzi runtime network w prebuilt paczce; należy sprawdzić wybraną dystrybucję.

Błędy licencji, unsupported features, niepowtarzalny seek, brak glyphów, zły alpha mode: zatrzymanie tej ścieżki. Jedno celowane ponowienie transient read; żadnych automatycznych provider swapów lub zbędnych reinstalacji. Bake lub prostsza geometria tylko jawnie, z nowym evidence scope. Szacunki pracy w RANKINGS są DERIVED, koszt runtime/GPU i wartościowa oszczędność tokenów Unknown.

## Otwarte sprawy
- FrameMotion repository/API/runtime/installed version: Unknown.
- Samodzielny test wybranych bibliotek, plików i integracji: NOT_RUN.
- Asset byte hashes poza odczytanym upstream release digest: Unknown; upstream digest nie jest naszym hashem.
- Prawdziwe alpha overlays: DAEDAL jest na czerni, ActionVFX blocked terms; brak pełnego pozytywnego kandydata z wykonanym alpha testem.
- Claudex review nie wykonano: wcześniejsze OAuth401, badanie dopuszczone bez Claude CLI; nie próbowano loginu ani fallbacku.
- Review artifacts i Hipson structural check nie są zgodą architektoniczną ani testem produktu.

## Prompt do następnego kroku Claude
„Przeanalizuj DR-03 z tego katalogu jako główny architekt. Przeczytaj REPORT.md, BASELINE.md, RANKINGS.md, DEEP_DIVES.md i ten IMPLEMENTATION_HANDOFF. Zweryfikuj rzeczywisty stan FrameMotion. Zaproponuj najmniejszy bounded pilot z konkretnym ownerem, fixtures i acceptance; zachowaj NOT_RUN, aż wykonasz osobno autoryzowane próby. Nie dodawaj automatycznie entries Toolbox, zależności, MCP ani providerów. Nie utożsamiaj źródłowego SHA z installed version albo asset hash.”

Nie wysłano tego promptu do innego czatu; jest materiałem dla głównego wątku i użytkownika.

