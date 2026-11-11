# Benchmarki produkcyjne i QA

**Wszystkie pięć prób: NOT_RUN.** Fixture, oczekiwane wyjścia i progi poniżej są propozycją DERIVED do uzgodnienia przed implementacją. Nie zmierzono wydajności, jakości animacji, mowy, miksu ani skuteczności cache. Dane maszynowe: [benchmarks.json](benchmarks.json). Weryfikacja dokumentów tego badania nie uruchamia tych prób.

| ID / cel | Fixture i operacja | Oczekiwany artefakt | Kryterium akceptacji |
|---|---|---|---|
| B01 — dialog dwóch postaci | 25 s, 2 oryginalne rigi 2D, 3 ujęcia, 4 krótkie kwestie PL, założony 24/1 FPS i 48 kHz, raz widoczne usta, raz reakcja słuchacza. Exact text obejmuje „Łódź” i nazwę własną z leksykonu. | Render z uchwytami, osobne stemy, mapa line→take→viseme, napisy, receipt i pełny odsłuch. | Brak zmiany postaci/stroju/głosu; zero brakujących słów i clippingu; ręcznie zaznaczone zamknięcia ust zgodne z zatwierdzonymi anchorami do 2 klatek jako próg roboczy; naturalność ocenia człowiek. |
| B02 — ciągłość wielu ujęć | 45 s, 6 ujęć, 2 lokacje, przekazanie rekwizytu z lewej ręki A do prawej B, jedno jawne przejście pory dnia. Ten sam seed i wersja riga. | Ciąg kadrów wejścia/wyjścia, continuity ledger, finalny fragment i raport ponownego renderu. | Zero niewyjaśnionych zmian właściciela, stroju, proporcji lub miejsca; oś/kierunek zgodne z kartą; drugi render ma zgodny timing i ustaloną tolerancję obrazu na tym samym środowisku. |
| B03 — trudne wyjaśnienie | 60–90 s PL: kolejka z różnymi czasami obsługi, jawne dane i jednostki, jeden kontrprzykład, dwie skale wykresu oznaczone. | Źródło danych, claim IDs, exact VO, kompozycja, napisy, odpowiedzi 3 dorosłych reviewerów bez scenariusza. | Wszystkie liczby/etykiety zgodne z wejściem; brak zasłonięć/nieznanych fontów; każdy reviewer potrafi wskazać mechanizm i ograniczenie modelu, albo zarejestrowana poprawka i ponowna ocena. To mała próba użyteczności, nie dowód edukacyjnej skuteczności populacyjnej. |
| B04 — późna zmiana kwestii | Fragment z B01 lub B03, jedna kwestia r1→r2: (a) poza kadrem, długość zachowana, (b) w kadrze +12 klatek. Powtórzyć część matematyki przy 24000/1001 i 48 kHz. | Dirty DAG, stare/nowe hashe, cue/sample ranges, cache receipts, typed ops z base_revision i dwa mastery porównawcze. | W (a) nie renderować ponownie niezależnego obrazu; w (b) poprawić tylko zależne etapy i zatwierdzony ripple. Odrzucić stale revision. Brak narastającego dryfu audio; próbki wyliczać z globalnych granic. Nie wymagać identycznych bajtów całego enkodowanego mastera. |
| B05 — pełny pilot i seria | Jeden kompletny oryginalny pilot w wybranym zakresie 4–8 min, biblia, trzy streszczenia kolejnych odcinków. Render po zatwierdzonym animatiku. | Cały master, napisy, prawa, metadata pack, raport kosztów i pełny seans+odsłuch; porównanie trzech historii. | Otwarcie, rozwój i rozwiązanie zrozumiałe; brak otwartych blocking defects; QC pliku i praw zaliczone; właściwy audience/disclosure; trzy epizody mają materialnie różne problemy i konsekwencje. Akceptacja człowieka; brak gwarancji YPP. |

## Zasady pomiaru

Czasy zapisywać osobno: praca aktywna człowieka, czas agenta, kolejka, render, transfer i odbiór. Zapisać sprzęt/OS, renderer i wersję, rozdzielczość, FPS, seed, fonty, liczbę prób, szczyt pamięci oraz koszt rzeczywiście naliczony. Powtórzenie po korekcie ma nowy run_id i wskazuje, co się zmieniło. Porównanie jakości dotyczy tej samej funkcji sceny i podobnego zakresu, nie różnych gatunków.

Błąd danych lub praw wraca do właściciela danych. Błąd przejściowy operacji może dostać maksymalnie jedną ponowną próbę w zatwierdzonym budżecie. Błąd twórczy wymaga diagnozy i jawnej rewizji; nie używa nieograniczonego losowania. Alternatywę renderera, uproszczenie sceny lub usługę chmurową traktować jako odrębną decyzję, a nie cichy fallback.

## Checklisty odbioru

- **Scenariusz:** cel widza i gatunek; pełna przyczyna–decyzja–konsekwencja; fact/fiction rozdzielone; exact text po read-through; brak zbędnego gagu.
- **Animatic:** czytelność działania bez dekoracji; zaplanowane reakcje/pauzy; sens kolejnych kadrów i ruchu; finał rozwiązuje obietnicę.
- **Assety:** przypięte id/revision/hash; sylweta, skala i strój; testy rigów i skrajnych póz; fonts/rights/głos bez Unknown.
- **Animacja i conform:** każdy render ma lokalne granice i FPS, master ma jednego właściciela; continuity_in/out pasują; brak nieplanowanego morfowania lub ruchu; alpha/kolor zgodne z warstwami.
- **Audio i PL:** dokładny tekst i wymowa; ten sam głos; ambience/Foley mają sens; cisza zaplanowana; zrozumiałość w docelowym miksie; brak clippingu; napisy zgodne z finalnym take’em.
- **Wydanie:** pełny seans i odsłuch; media probe i decode; prawa i credits; miniatura/tytuł zgodne; audience i AI zapisane; hash projektu i mastera. Publikacja osobnym działaniem właściciela.

W tym badaniu oceniono dokumenty i statyczne kadry referencyjne. Żadnej powyższej checklisty nie oznaczono jako zaliczonej dla wygenerowanego pilota.
