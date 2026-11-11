Przeprowadź pogłębiony Deep Research i przygotuj praktyczne kompendium profesjonalnego motion designu, animacji i compositingu, ze szczególnym uwzględnieniem Adobe After Effects. Następnie przełóż tę wiedzę na pracę agentów AI tworzących animację w kodzie dla wtyczki FrameMotion i jej współpracy z FrameCore Works Creative Studio.

To zadanie badawcze. Wykonaj badanie i syntezę, nie poprzestawaj na planie, liście linków ani rankingu programów. Raport po polsku, z zachowaniem angielskich terminów technicznych.

1. KONTEKST I CEL

Rozwijam FrameCore Works Creative Studio oraz dwie nowe wtyczki: FrameMotion i FrameCut. Ten research jest przeznaczony przede wszystkim dla FrameMotion.

Roboczy podział odpowiedzialności:
- Creative Studio: brief, koncepcja, scenariusz, kierunek wizualny i koordynacja produkcji.
- FrameMotion: projektowanie ruchu, animacja, typografia, efekty, compositing i renderowanie scen lub nakładek.
- FrameCut: montaż materiałów i nadrzędna oś czasu filmu.

To założenia do porównania z aktualnymi materiałami, a nie opis potwierdzonej implementacji. FrameMotion ma działać samodzielnie oraz jako specjalista wywoływany przez Studio lub FrameCut. W danym projekcie istnieje jeden właściciel nadrzędnej osi czasu.

Repozytorium Creative Studio:
https://github.com/FrameCoreWorks/framecore-works-creative-studio

Jeżeli dostęp jest możliwy, przeczytaj aktualne README, AGENTS.md, manifesty oraz pliki związane z motion, timeline, renderingiem, audio i QA. Zapisz sprawdzony commit i datę. Adresów repozytoriów FrameMotion i FrameCut nie podano: nie wymyślaj ich. Nie utożsamiaj zawartości GitHub z wersją zainstalowanej wtyczki. Brak dostępu nie blokuje kompendium; stan implementacji oznacz Unknown.

Celem jest przejęcie warsztatu zawodowca: jak podejmuje decyzje, buduje scenę, dopracowuje ruch, diagnozuje błędy i ocenia rezultat. Znajomość nazw efektów nie wystarcza.

2. METODA I WIARYGODNOŚĆ

Przeszukaj dokumentację producentów, podręczniki, oficjalne szkolenia, materiały autorów narzędzi, wartościowe tutoriale, breakdowny produkcyjne i publiczne repozytoria. After Effects jest głównym punktem odniesienia; porównaj użyteczne metody z Fusion, Apple Motion, Blender, Cinema 4D lub innymi programami, gdy wnoszą konkretną wiedzę.

Szukaj po angielsku i polsku. Materiały School of Motion, Video Copilot, Ben Marriott, Jake Bartlett, ECAbrams i studiów motion traktuj jako kierunki poszukiwań, nie automatycznie zweryfikowane źródła.

Celuj w co najmniej 40 rzeczywiście wykorzystanych, wartościowych źródeł. Nie dopełniaj liczby słabymi linkami. Podaj macierz pokrycia tematów i luki. Nie deklaruj przeszukania wszystkich poradników w internecie.

Przy ważnych ustaleniach podawaj URL, autora, datę, wersję programu i rozdział lub timestamp, jeśli rzeczywiście sprawdzono materiał. Sam tytuł filmu nie dowodzi jego zawartości. Oddziel obejrzany materiał, przeczytaną transkrypcję i opis.

Oznaczaj:
- SOURCED: twierdzenie poparte wskazanym źródłem.
- DERIVED: własna synteza lub proponowana adaptacja.
- PRACTITIONER: doświadczenie konkretnego praktyka, z kontekstem.
- Unknown: brak wystarczających danych.

Fora i społeczności wykorzystuj do odkrywania problemów i heurystyk. Działanie API i parametrów potwierdzaj w dokumentacji, kodzie autorów lub publikacjach pierwotnych. Dla metod podawaj także ograniczenia i kontrprzykłady.

3. KOMPENDIUM WARSZTATU

Zbuduj słownik około 100 istotnych terminów PL/EN, z krótkim przykładem i konsekwencją produkcyjną. Następnie opracuj:

A. Projektowanie i reżyseria ruchu:
kompozycja w czasie, hierarchia, typografia, siatki, negatywna przestrzeń, kolor, prowadzenie uwagi, staging, timing versus spacing, anticipation, overshoot, follow-through, overlap, squash/stretch, rytm, pauza i kontrast tempa. Pokaż, jak dobierać język ruchu do marki, przekazu i emocji.

B. Model pracy After Effects:
kompozycje, precompy, warstwy, parenting, nulls, anchor point, układy współrzędnych, shape layers, paths, Trim Paths, Repeater, Merge Paths, maski, track mattes alpha/luma, blend modes, adjustment layers, kolejność renderowania, continuous rasterization i collapse transformations. Wyjaśnij zależności i typowe pułapki.

C. Animacja na poziomie ustawień:
keyframes, interpolacja czasowa i przestrzenna, Graph Editor value/speed, tangenty, easing, ciągłość prędkości, trajektorie, expressions, constraints, pętle, stagger, procedural noise, deterministyczna losowość i retiming. Rozróżnij krzywą położenia od krzywej prędkości. Omów fizyczne i stylizowane modele ruchu.

D. Obraz i compositing:
2D/2.5D/3D, kamera, perspektywa, parallax, światło, cienie, depth of field, tracking, podstawy keyingu i rotoscopingu, displacement, particles, glow, grain, blur, tekstury i integracja elementów. Rozróżnij motion blur, frame blending i optical flow. Uwzględnij shutter angle/phase, próbkowanie, alfa straight/premultiplied, linear light, przestrzenie barwne, 8/16/32-bit, banding i aliasing.

E. Tekst i dźwięk:
kinetic typography, animatory tekstu, odsłanianie maskami, podział na znaki/słowa/wiersze, kerning, font loading, polskie znaki, stabilny layout i czas czytania. Muzyka, beat/downbeat/onset, frazowanie, markery, VO, SFX i lyrics alignment. Nie utożsamiaj amplitudy z beatem ani startu animacji z momentem wizualnego akcentu. Omów offset, drift, tempo zmienne i ręczne korekty.

F. Profesjonalny proces:
brief → research wizualny → concept → styleframes → storyboard → animatic → blocking → dopracowanie krzywych → compositing → dźwięk → QA → delivery. Uwzględnij szablony/MOGRT jako inspirację dla parametryzowanych scen, kontrolę wersji, poprawki klienta i zachowanie zaakceptowanych elementów.

Dla wartości liczbowych podaj jednostki, kontekst, źródło albo oznaczenie „proponowany punkt startowy”. Nie przedstawiaj jednego easingu, FPS, czasu sceny, safe zone ani LUFS jako uniwersalnej normy.

4. RECEPTURY PRODUKCYJNE

Opracuj 15–20 szczegółowych receptur, obejmujących animację logo, kinetic type, lower thirds, product reveal, explainer, animację UI, infografikę, przejścia maskowe, parallax, particles i synchronizację muzyczną.

Każda receptura:
problem i cel → kiedy użyć/nie używać → wymagane assety → budowa w programie referencyjnym → parametry z jednostkami → kolejność operacji → typowe błędy → naprawa → odpowiednik w kodzie → kryteria jakości → źródła.

Wyjaśniaj decyzje, nie tylko kliknięcia. Porównuj poprawny rezultat z charakterystycznym błędem. Nie redukuj motion designu do slideshow, przypadkowych efektów i pulsowania każdego elementu.

5. PRZEŁOŻENIE NA AGENTÓW I KOD

Porównaj zadaniowo HTML/CSS/SVG, GSAP, HyperFrames, Remotion/React/TypeScript, Canvas, PixiJS, Three.js/WebGL/shadery, Motion Canvas, Blender Python oraz FFmpeg do składania i eksportu. To kandydaci do zbadania, nie deklaracja dostępności.

Zbuduj tabelę:
technika zawodowca → zasada niezależna od programu → reprezentacja danych → operacja agenta → backend → ograniczenia → test.

Każdemu mapowaniu przypisz: odpowiednik wierny, przybliżenie, workflow hybrydowy albo brak praktycznego odpowiednika. Nie zakładaj, że efekt AE ma identyczny filtr FFmpeg lub prosty tween CSS.

Zaproponuj scene graph, dependency graph, timeline, keyframes, krzywe, maski, warstwy, kamerę, tekst i cue audio. Podaj spójny przykładowy JSON oraz kilka krótkich przykładów kodu lub pseudokodu. Opisz granicę między specyfikacją kreatywną a adapterem renderera.

Zbadaj render po numerze klatki, rational FPS, seeded randomness, seek/scrubbing, stan symulacji, bake/cache, fonty, lokalne assety, preview/export parity, CPU/GPU, pamięć i wznowienie renderu. Nie obiecuj identyczności bitowej między różnymi platformami bez podstaw.

Agent powinien umieć wybrać technikę, zbudować scenę, obejrzeć wynik i naprawić konkretną wadę. Zaprojektuj ograniczoną pętlę QA z kryteriami stopu, zamiast nieskończonego „upiększania”.

6. ŹRÓDŁA DO ADAPTACJI

Znajdź repozytoria, SKILL.md, cookbooki, przykłady, biblioteki efektów i narzędzia testujące, które rozwiązują wskazane luki. Dla najlepszych sprawdź konkretne pliki.

Podaj URL, commit/tag, moduł, wejścia/wyjścia, zależności, środowisko, utrzymanie, licencję kodu i osobno assetów/fontów/modeli. Preferuj lokalne, bezpłatne rozwiązania bez konta i z licencjami pozwalającymi na zamierzone użycie. Nie zakładaj, że każde open source jest darmowe w każdym zastosowaniu.

Oddziel: przejęcie metody, zapis wiedzy, adaptację instrukcji skilla, użycie zależności i kopiowanie kodu. Wybierz najbardziej użyteczną wiedzę, bez importowania całych repozytoriów bez potrzeby.

7. WSPÓŁPRACA WTYCZEK

Zaproponuj wspólny, wersjonowany kontrakt:
project_id, schema_version, revision, timeline_owner, asset_id/hash, fps_num/fps_den, jednostki czasu, zakresy [in, out), source time i timeline time, handles, retiming, rozdzielczość, color space, alpha mode, audio sample rate, fonty, seed, provenance i accepted locks.

FrameMotion przyjmuje brief sceny, długość i zakres na nadrzędnej osi czasu. Oddaje projekt edytowalny i/lub wyrenderowany materiał, manifest zależności oraz wynik QA. Nie zmienia samowolnie czasu całego filmu. Opisz obsługę zmiany długości, brakujących assetów i funkcji nieobsługiwanych przez backend.

Uwzględnij wersjonowanie schematu, migracje, zgodność wsteczną, walidację i brak cichej utraty danych. Aktualny kontrakt, jeśli istnieje i został odczytany, ma pierwszeństwo przed projektowaniem duplikatu.

8. WALIDACJA I PRZYKŁADY

Zaproponuj benchmarki: logo reveal, kinetic type z polskim tekstem, product explainer, scena 2.5D i fragment muzyczny. Dla każdego: brief, syntetyczne dane, plan sceny, oczekiwany wynik, błędy do wykrycia i warunki akceptacji.

Uwzględnij osobno 16:9 i 9:16 jako adaptacje kompozycji. Oceń technikę, dokładność tekstu/logo, płynność, czytelność, rytm, synchronizację i intencję. Automatyczne metryki nie zastępują oglądania filmu w czasie rzeczywistym i odsłuchu. Kilka klatek nie dowodzi płynności.

Stan dowodu opisuj osobno: dokumentacja, inspekcja kodu, test autora, własny test. Testy niewykonane oznacz NOT_RUN.

9. WYNIK I GRANICE

Dostarcz:
- pełne kompendium i słownik;
- mapę poradników z opisem, czego konkretnie uczą;
- receptury i tabelę technika → kod;
- katalog przydatnych repozytoriów oraz odrzuceń;
- projekt kontraktu i przykłady danych;
- checklisty QA i benchmarki;
- macierz „potwierdzone w obecnej wtyczce / luka / Unknown”;
- backlog P0/P1/P2 i IMPLEMENTATION_HANDOFF dla Codex.

Każde zadanie wdrożeniowe ma mieć cel, właściciela, wejścia, wyjścia, zależności, zakres plików potwierdzony lub proponowany, ograniczenia, fallback i test akceptacyjny. Dla integracji opisz także błędy, retry, limity, koszt i weryfikację. Nie dubluj istniejących ról ani silników.

To research, bez zmian w repozytoriach, instalacji, uruchamiania pobranego kodu, płatnych usług, uploadu prywatnych danych, pushu, deployu i publikacji. Możesz czytać publiczne źródła. Nie obchodź logowania i paywalli. Nie kopiuj całych kursów; opracuj własną syntezę.

Jeśli środowisko umożliwia tworzenie plików, przygotuj kompendium Markdown, rejestr źródeł CSV/JSON i handoff. W przeciwnym razie podaj pełną treść w odpowiedzi. Zapisz datę badania, ograniczenia i stan pokrycia. Przy limicie długości podziel wynik na ponumerowane części bez ukrywania braków.

Zacznij właściwe badanie teraz, bez pytań o konkretny projekt. Priorytetem jest praktyczny warsztat zawodowca i jego wiarygodne przełożenie na FrameMotion.