# DR-06 — pełne animacje i serie YouTube tworzone z pomocą kodu

**Najbliższy znaleziony przykład bajki fabularnej to Milo. Najmocniejsze publiczne dowody techniczne pochodzą z kodowanych explainerów 3Blue1Brown, Reducible i Primer.** Badanie uzasadnia rozpoczęcie FrameCore od kontrolowanej sceny, wersjonowanych assetów i lokalnego renderu ujęć. Nie dowodzi jeszcze niezawodnej produkcji całego dialogowego serialu ani jej kosztu.

Stan: **11 listopada 2026**. Użytkownik doprecyzował nacisk na narzędzia code-based i potwierdził przydatność wcześniejszych klasycznych referencji. Zachowano je jako warsztat pomocniczy. Oryginalny PROMPT pozostaje niezmieniony.

## Co warto obejrzeć i sprawdzić w pierwszej kolejności

| Przykład | Co faktycznie potwierdzono | Zastosowanie dla FrameCore |
|---|---|---|
| [Milo in Space](https://www.youtube.com/watch?v=OBIBsnzPKZI) i [Milo and the Umbrella Storm](https://www.youtube.com/watch?v=t2Xq2fpFmwE) | Dwie publikacje ok. 4,5 min i wybrane kadry. [Autor](https://ubedev.com/milo/) deklaruje budowę obrazu, postaci i muzyki w kodzie; człowiek odpowiada za historię, ujęcia i cięcia. **CREATOR_CLAIM / CODE_RENDERED**; brak publicznego repo. | Najbliższe pytaniu o bajkę. Wspólna postać, świat i parametry ruchu jako dane. Nie przyjmować deklaracji za test odtwarzalności. |
| [3Blue1Brown — neural network](https://www.youtube.com/watch?v=aircAruvnKk) | 18:40 w playerze, próbka 09:19, adaptacja lekcji i [kod Manim](https://github.com/3b1b/videos/blob/master/_2017/nn/part1.py). **CONFIRMED_WORKFLOW / CODE_RENDERED** dla animacji. | Dane, geometria, etykiety i kolejne objaśnienia pochodzą ze wspólnych obiektów. Dźwięk/mastering to osobny zakres. |
| [Reducible — GJK](https://www.youtube.com/watch?v=ajv46BSqcK4) | [Repo](https://github.com/nipunramk/Reducible) wiąże film z kodem scen. Potwierdza warstwę animowaną, bez wykonania historycznego projektu. | Algorytm i sposób objaśnienia mają osobne testy; aktualizacja danych nie powinna wymagać ręcznej podmiany każdej grafiki. |
| [Primer — Natural Selection](https://www.youtube.com/watch?v=0ZGbIKd0XrM) | 10:00, kadr 05:00. Opis odcinka wskazuje Blender/Python; [repo archiwalne](https://github.com/Helpsypoo/primerpython) dokumentuje kod wizualizacji. Nie ustalono commitu finalnego renderu. | Symulacja i rendering oddzielone; seed, stan świata i zdarzenia zapisane, kamera nie zmienia wyniku eksperymentu. |
| [Đi Làm IT — benchmark AI](https://www.youtube.com/watch?v=OWCMEja1pzo) | Pełna publikacja 5:02; [silnik Remotion](https://github.com/LocNguyenSGU/whiteboard-explainer-engine) linkuje film. Kod silnika jest publiczny; pełne wejścia finalnego projektu Unknown. Próbki obrazu i tekst bez audytu tez filmu. | Łączenie animowanej tablicy z materiałem źródłowym, oddzielne spoken_text, visual_action i zakres nagrania. |
| [HyperFrames — 19 Claude Code Tips](https://www.youtube.com/watch?v=fnKGWHSd0NE) | [README autora](https://raw.githubusercontent.com/chenyuxiaojin/cyxj-hyperframes/main/README.md) wiąże ok. 7,5 min z 28 kompozycjami. To instruktaż, nie fabularna bajka; brak oglądu. | Pomocniczy przypadek lokalnego składania kompozycji i wersjonowania źródeł. |
| [ESCAPEMENT](https://github.com/Leonxlnx/escapement) | Publiczny krótki projekt Blender Python i FFmpeg, ok. 36,5 s. **Poza próbą pełnych odcinków YouTube.** | Shotlist, kolejka renderu, zależności i cue. Nie jest dowodem skali serialu. |

Kod tworzący symulację wewnątrz devloga nie oznacza, że cały devlog został wyrenderowany kodem. Pomoc AI w pisaniu kodu nie oznacza, że model generował każdą klatkę. Raport rozdziela rodzaj procesu — CODE_RENDERED / CODE_ASSISTED / GENERATIVE / Unknown — od rangi dowodu — CONFIRMED_WORKFLOW / CREATOR_CLAIM / INFERRED_FROM_VIDEO / Unknown. [Pełna mapa produkcji](production/PRODUCTION_CASES.md).

## Zakres i ograniczenia badania

Próba główna obejmuje **44 publikacje z 23 kanałów**, w tym **11 code-based z 5 kanałów**. Aneks rozszerza katalog do 60 publikacji i 34 kanałów. Dla głównej próby nie ustalono 32 długości oraz 11 dat i liczników wyświetleń; braków nie zastąpiono estymacjami. Dokładne liczby, braki długości/dat/wyświetleń, udział code-based, okno ostatnich 12 miesięcy i kryteria wyłączeń zawiera [COVERAGE](catalog/COVERAGE.md). [JSON](catalog/episodes.json) i [CSV](catalog/episodes.csv) zachowują źródło każdego typu metadanych, jawne Unknown i flagę main_sample. Search result metadata nie jest potwierdzeniem oglądu.

**Oględziny objęły statyczne kadry z 11 filmów, 0 filmów obejrzanych w całości i 0 odsłuchów.** Wyeksportowano 7 transkrypcji. [12 pogłębionych kart](catalog/DEEP_DIVES.md) łączy źródła autorów, kod, opisy, transkrypcje i dostępne kadry, z jawnym zakresem. Są to karty o ograniczonej podstawie, a nie pełne analizy audiowizualne. Rytm cięć, miks, lipsync i ciągłość całego odcinka pozostają NOT_OBSERVED. [Dziennik oględzin](evidence/VIEWING_LOG.md).

Scalony rejestr zawiera 178 unikalnych publicznych adresów; 118 ma odczyt strony lub dokumentacji w co najmniej jednym rekordzie. To liczba adresów dowodowych, nie niezależnych produkcji ani obejrzanych filmów.

Próbka jest celowa, nie reprezentatywna statystycznie. Obejmuje polskie i międzynarodowe publikacje, małych autorów i studia, starsze referencje oraz nowe uploady. Mały kanał Milo (11 subskrybentów w chwili oglądu) i nowy Đi Làm IT (13) pomagają uniknąć próby samych wielkich sukcesów, lecz ich niewielkie wyświetlenia nie dowodzą słabej jakości. Starszy odcinek 3Blue1Brown i nowa publikacja małego kanału nie mają porównywalnego czasu ekspozycji ani dystrybucji.

Nie obliczano retencji, CTR, watch time, przychodów, RPM ani „wpływu na algorytm”. Publiczne liczniki są stanem z daty odczytu, a metadane z indeksu mogą być starsze. Data nowego uploadu nie potwierdza daty produkcji lub aktualnego workflow studia. Pełnych cudzych transkrypcji i filmów nie dołączono do pakietu.

## Wniosek produkcyjny

Najbardziej uzasadniony pierwszy krok to krótki fixture z kontrolowanymi 2D postaciami albo narracyjny explainer. Wspólny zestaw danych powinien wiązać skrypt, dokładną kwestię, rig, kamerę, zdarzenia, zakres czasu i prawa. Renderować po ujęciu, składać na jednym master timeline. Baza ma zachować możliwość podmiany zdania bez przebudowy całej historii.

Dramaturgia pozostaje pracą redakcyjną. Każde ujęcie potrzebuje celu, nowej informacji lub reakcji. Klasyczne referencje pokazują użyteczne relacje sylwetek, obiektów i planów, lecz nie stanowią dowodu automatyzacji ich procesu. Dobrze zaplanowana animacja ograniczona jest sensownym wariantem dla małej produkcji; musi przejść ocenę całego animatiku z dźwiękiem.

Dla explainera kluczowa jest zgodność danych, tekstu i kolejności ujawniania. Dla powracających postaci — stały rig, garderoba, głos i ciągłość rekwizytów. Dla tajemnicy starszej widowni — czytelność wskazówek, kontrola narracji i dźwięku. Żaden renderer nie zastępuje tych decyzji.

## Mapa pakietu

| Materiał | Co zawiera |
|---|---|
| [Katalog i luki](catalog/COVERAGE.md), [kanały CSV](catalog/channels.csv) | Próba główna/aneks, pochodzenie metadanych, daty, języki i ograniczenia. |
| [Karty odcinków](catalog/DEEP_DIVES.md), [log oglądu](evidence/VIEWING_LOG.md) | Obserwowalne przykłady i zakres NOT_OBSERVED. |
| [Metody](production/METHODS.md), [przypadki](production/PRODUCTION_CASES.md) | Vector, puppet, klatkowanie, Blender/Grease Pencil, kod, generacja, hybrydy i granice narzędzi. |
| [Biblia i warsztat](SERIES_BIBLE_AND_WORKSHOP.md) | Proces serii, polski język, timing/voice/music-first i zmiana dialogu. |
| [Ekonomika](ECONOMICS.md) | Trzy scenariusze z jawnymi roboczogodzinami i stawką wyłącznie ilustracyjną. |
| [Trzy oryginalne formaty](ORIGINAL_FORMATS.md) | Fabuła dziecięca, explainer i historia dla starszej widowni — DERIVED. |
| [Baseline](baseline/BASELINE.md), [kontrakty](baseline/CONTRACTS.md), [operacje](baseline/OPERATION_MAP.md) | 3 przypięte repo; istniejące mechanizmy i oddzielne propozycje. |
| [Benchmarki i QA](BENCHMARKS_AND_QA.md) | Pięć fixture’ów, wszystkie NOT_RUN. |
| [Polityki i delivery](POLICY_AND_DELIVERY.md) | Oficjalne zasady z datą i warunki gotowego wydania. |
| [IMPLEMENTATION_HANDOFF](IMPLEMENTATION_HANDOFF.md) | P0/P1/P2, decyzje architekta, bez twierdzeń o akceptacji lub wdrożeniu. |
| [Rejestr źródeł](SOURCES.json), [statystyki](EVIDENCE_STATS.json) | Scalone indeksy z zachowaniem rodzaju dowodu; deduplikacja URL. |
| [Niezależna recenzja](review/REVIEW.md), [przebieg](SWARM.md) | Wynik kontroli, rozstrzygnięte uwagi i ograniczenia niezależnego audytu. |

Przed implementacją architekt powinien wybrać format i jeden adapter, a następnie zmierzyć B01–B04. Pełny pilot B05 sprawdzi dopiero zachowanie historii, polskiego dźwięku, ciągłości i kosztu w całym odcinku. To proponowany następny zakres, nie wykonana produkcja.
