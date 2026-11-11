# QA i benchmarki FrameMotion

Data: 2026-11-11. Wszystkie sceny poniżej są **DERIVED**, oryginalne i syntetyczne. Parametry to **proponowane punkty startowe**, nie normy branżowe. Własne wykonanie renderów, odtwarzanie, odsłuch, natywne AE/Fusion/Motion/Blender/C4D: **NOT_RUN**. Ten plik jest specyfikacją akceptacji, a nie raportem udanych filmów.

## Oddzielne poziomy dowodu

| Poziom | Co potwierdza | Czego nie potwierdza |
|---|---|---|
| Dokumentacja | Zamierzona semantyka parametru w podanej wersji | Że ten renderer, projekt i komputer dały poprawny obraz |
| Inspekcja kodu | Gałąź obliczeń, walidację, publiczne I/O | Że gałąź uruchomiono lub pokrywa cały program |
| Test autora | Wynik opublikowany przez autora, tylko jeśli odczytany | Niezależny test w naszym środowisku |
| Własny test analityczny | Arytmetykę, referencje JSON i zakresy sprawdzone własnym skryptem | Natywny rendering, płynność, jakość estetyczną |
| Własny test medialny | Rzeczywisty export, ciągłe odtwarzanie i odsłuch | Zgodność innych platform, których nie sprawdzono |

Źródła podstaw semantycznych: [H01 Font Loading §3.3–3.4](https://www.w3.org/TR/css-font-loading/), [H02 OTIO Time Ranges](https://opentimelineio.readthedocs.io/en/latest/tutorials/time-ranges.html), [H03 RationalTime](https://opentimelineio.readthedocs.io/en/latest/api/python/opentimelineio.opentime.html), [H04 beat tracker](https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html), [H05 onset detector](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html). Progi i poniższa procedura są własną syntezą.

## B01 — logo reveal: integralność znaku

**Brief:** fikcyjna marka „ŁUK”; znak stanowi własny trójkąt z trzema wierzchołkami i krótkie słowo. Celem jest ujawnienie konstrukcji, a potem stabilne rozpoznanie, bez deformacji finalnego logo. **Dane:** dwie krzywe SVG, bbox 200×160 px, neutralne tło, brak muzyki. 120 klatek przy 30/1 fps = 4 s.

**Plan:** 0–11 anticipation samego nośnika; 12–35 reveal po ścieżce; 36–47 osadzenie; 48–107 hold; 108–119 kontrolowane wygaszenie. Logo podczas hold ma tę samą geometrię co asset. Stroke-reveal nie musi odtwarzać kolejności rysowania litery — gdy geometria jest wielopolowa, wybrać maskę powierzchniową.

**16:9:** 1920×1080, znak i nazwa w układzie poziomym; duża wolna przestrzeń. **9:16:** 1080×1920, znak nad nazwą; ponownie ułożyć optyczny środek, nie cropować gotowego 16:9. Margines roboczy 8% krótszego wymiaru, do zastąpienia przez faktyczną specyfikację placementu.

**Oczekiwane:** jeden wyraźny moment identyfikacji, potem spokój. **Wstrzyknięte błędy:** błędny anchor point, niewłaściwy fill-rule, pikselowe obrzeże alfa, reset losowości przy seek. **Akceptacja:** dokładne ścieżki i słowo „ŁUK”; brak niezamierzonego przeskoku w 47→48; żaden piksel znaku poza bezpiecznym polem; hold co najmniej 60 klatek w tym briefie; overlay na białym/czarnym/kolorowym tle bez obwódki. Przesunięcie bbox względem zatwierdzonego layoutu <=1 px w tym fixture. Oglądanie całych 4 s obowiązkowe.

## B02 — kinetic type: polski tekst i stabilny skład

**Brief:** dokładna kopia: „Zażółć gęślą jaźń.” oraz „Łączymy ruch z treścią”. Bez dopisywania słów. **Dane:** 210 klatek przy 30/1 fps = 7 s, lokalny font z licencją, hash pliku i zdefiniowana waga; sekwencje znaków NFC, osobny przypadek testowy z decomposed diacritics. **Plan:** 0–17 reveal grupy; 18–89 czytelny pierwszy wers; 90–107 zmiana hierarchii; 108–191 czytelny drugi komunikat; 192–209 exit.

**16:9:** dwa szerokie wersy z asymetrycznym wyrównaniem; **9:16:** ustalone łamanie na krótsze wersy, animacja frazami; znaczenie i kolejność kopii niezmienne. Ręczna interlinia i kerning tylko tam, gdzie metryki fontu wymagają korekty. Dzielić po grapheme clusters, nie po jednostkach UTF-16, by znak łączący nie animował się sam.

**Oczekiwane:** akcent semantyczny na „ruch” i „treścią”, ograniczony do dwóch zdarzeń. **Błędy:** fallback bez polskich glifów, font swap po pierwszej klatce, rozcięte akcenty, zmiana szerokości po wejściu, wszystkie słowa poruszają się jednocześnie. **Akceptacja:** dokładny tekst i kolejność w danych oraz obrazie; bbox każdego glifu mieści się w masce; layout po załadowaniu fontów nie zmienia się między renderami; hold 72/84 klatek to propozycja do testu czytania, nie uniwersalna prędkość czytania. OCR pomocniczy — prawdziwą akceptację ortografii wykonuje człowiek. Własny test w przeglądarce: NOT_RUN.

## B03 — product explainer: obraz i argument

**Brief:** fikcyjny filtr wody „Przepływ”; opowiedzieć trzy etapy: wejście → filtracja → wyjście. Nie zamieszczać niezweryfikowanych twierdzeń zdrowotnych ani liczbowych. **Dane:** syntetyczny schemat przekroju, trzy etykiety, 360 klatek przy 30/1 fps = 12 s. Brak fotorealistycznego produktu; to celowo benchmark schematyczny.

**Plan:** 0–59 kontekst; 60–149 wejście i prowadząca linia; 150–239 wnętrze i przepływ; 240–329 rezultat; 330–359 zakończenie. Zamiast jednego ciągłego ruchu kamery stosować zmianę skali wyłącznie w przejściach. Dane wejściowe 100 jednostek i wyjściowe 100 jednostek służą wyłącznie sprawdzeniu zachowania przepływu symbolicznego, nie obietnicy skuteczności urządzenia.

**16:9:** schemat po lewej, etykiety po prawej; **9:16:** droga pionowa, etykiety pod aktywną częścią, żaden przewód nie przecina tekstu. **Błędy:** etykieta wskazuje inny port, animacja kierunku przeczy strzałce, cienie zakrywają przekrój, dwie konkurujące dominanty. **Akceptacja:** kolejność przyczynowa prawidłowa, wszystkie połączenia ciągłe, jeden nowy argument w każdym bloku; brak przeniesienia cue poza przydzielone 360 klatek; realne odtworzenie 12 s z testem zrozumienia trzech etapów. Test autora/własny medialny: NOT_RUN.

## B04 — scena 2.5D: parallax i integracja

**Brief:** własna abstrakcyjna scena z kartami na trzech głębokościach; kamera wykonuje niewielki boczny truck bez obrotu, a tekst pozostaje czytelny. **Dane:** 180 klatek przy 30000/1001 fps = 6.006 s; trzy prostokąty 500×400 jednostek sceny z checkerem, środki {(-300,0,0),(0,0,200),(300,0,400)}. Świat: x w prawo, y w górę, kamera patrzy +z. Kamera zaczyna w (0,0,-1000), target=(0,0,0), poziomy FOV=50°; dystanse planów wynoszą 1000/1200/1400 jednostek, wszystkie dodatnie. Kamera i target przesuwają się razem po x od0 do80, zatem kierunek pozostaje stały.

**Plan:** blocking statyczny → kamera → zasłanianie → antyaliasing i blur → finalny kolor. Boczny ruch kamery zajmuje 120 klatek; reszta stanowi hold. Przy stałej głębi i bez obrotu prędkość ekranowa każdego planu wynosi |v_x|·focal_px/depth; dlatego bliższy plan jest szybszy. Dla dolly po osi optycznej ta reguła wymagałaby dodatkowego uwzględnienia pozycji ekranowej i nie jest tu testowana. **16:9:** więcej przestrzeni bocznej; **9:16:** zmienić kadr i rozmieszczenie kart, zachować relacje głębokości; w fixture zachować poziomy FOV=50° i jawnie dostosować położenia kart do kompozycji; inny FOV wymaga nowego oczekiwanego wyniku.

**Błędy:** odsłonięte puste obszary tekstury, przecinające się planes, niezgodny z maską blur, niewłaściwa kolejność alpha blend, DOF rozmywa jedyny komunikat. **Akceptacja:** bliższa karta ma większą prędkość ekranową przy tej geometrii; brak dziur we wszystkich klatkach; poprawne zasłanianie; ten sam index klatki z seek daje ten sam stan transformacji; przejście sequential vs random-access bez zmiany układu. Pixel-identical cross-GPU nie jest kryterium bez osobnego dowodu. Własny render: NOT_RUN.

## B05 — fragment muzyczny: impact, offset i drift

**Brief:** 10 s abstrakcyjnego motion, cztery główne akcenty; animacja reaguje na frazę, nie na każdy pik amplitudy. **Dane:** jawna lista cue w próbkach audio przy 48000 Hz, FPS 30000/1001, syntetyczne kliknięcia zamiast cudzej muzyki. Cue samples={48048,144144,288288,432432}; odpowiadają klatkom {30,90,180,270}. Każdy impact następuje 12 klatek po starcie wejścia: start={18,78,168,258}. Całość 300 klatek = 10.010 s, zatem brief „10 s” musi zostać sprecyzowany do czasu ramkowego.

**Plan:** wyznaczyć cue w audio → podać ich rodzaj/pewność → ręcznie wybrać cztery akcenty → cofnąć start o czas narastania → sprawdzić na początku/środku/końcu. Drugi fixture ma dryf 1000 ppm: po 10 s błąd 10 ms; trzeci zmienia tempo, więc stała siatka BPM jest celowo niewłaściwa. Zmiana tempa wymaga jawnej listy zdarzeń lub segmentów, nie dopasowania jednego offsetu.

**16:9:** rytm przekazywany poziomą drogą; **9:16:** pionową, z mniejszą drogą i odpowiednio zmienioną krzywą, by zachować odczuwany akcent. **Błędy:** onset uznany za downbeat, próbki audio uznane za klatki wideo, animacja startuje na beat zamiast akcentować beat, zmiana speed bez retime dźwięku. **Akceptacja:** impact na cue ±0.5 klatki po najbliższej kwantyzacji; odtwarzanie normalne z odsłuchem potwierdza wyczuwalny akcent; pomiar raportuje offset i nachylenie dryfu osobno. Tolerancja ±0.5 klatki jest arytmetyczna, nie normą percepcji. NOT_RUN dla renderu/audio; mapowanie liczb testowane w własnym weryfikatorze.

## Ograniczona pętla QA agenta — DERIVED

1. **Preflight:** wersja kontraktu, zgoda dla revision, komplet assetów/hashów i fontów, zakres przydziału, capabilities backendu, prawa. Niedostępny font lub nieobsługiwane compositing: jawna blokada; nie cichy zamiennik.
2. **Blocking review:** sprawdzić styleframe, początek, impact i hold; oceniane kompozycja/tekst/przyczynowość. To jeszcze nie dowód płynności.
3. **Ciągły preview:** obejrzeć całość w docelowym FPS i rozmiarze; odsłuch przy intencjonalnym audio. Zanotować faktyczne miejsce i objaw, np. „klatka 42: dolna część ogonka ą obcięta”.
4. **Diagnoza pojedynczego mechanizmu:** font bbox/maska/anchor zamiast przypadkowego zwiększania bluru. Hipoteza i oczekiwany skutek przed poprawką. Maksymalnie 2 poprawki na dany defekt, 3 rundy całego benchmarku — proponowany budżet.
5. **Regresja:** odtworzyć zmieniony fragment z handles oraz cały film po każdej zmianie timingu; zachować accepted locks. Przekroczenie budżetu lub nieznana przyczyna → blocker i przekazanie do właściciela, nie automatyczne „upiększenie”.
6. **Delivery:** zależności, editable project, render jeśli wykonany, revision, manifest i QA z osobnymi wynikami technicznymi/percepcyjnymi. PASS tylko w rzeczywiście wykonanym zakresie.

## Checklista obrazu, czasu i eksportu

- Klatki: N sztuk dla [0,N); ostatnia klatka N−1; brak czarnej klatki po out. Timecode drop-frame nie oznacza usuwania obrazów.
- Krzywe: skoki wartości tylko intencjonalne, ciągłość prędkości tam gdzie intencjonalny gładki ruch; zbyt gładko wszędzie także może być błędem rytmu.
- Alfa: porównać na czerni/bieli/kolorze; inspect RGB i alpha osobno. [H07 Nuke Premult](https://learn.foundry.com/nuke/content/reference_guide/merge_nodes/premult.html) potwierdza zależność premultiplication od Merge. Uogólnienie na inne backendy wymaga ich własnego testu.
- Kolor: przypięte input/work/output oraz view transform. Histogram nie dowodzi braku bandingu — ocena przy normalnym odtwarzaniu oraz gradient test.
- Blur: sprawdzić krawędzie w szybkim ruchu, liczbę próbek i shutter; frame blending/optical flow osobne operacje. Nie maskować judderu przez losowe rozmywanie.
- Tekst: font hash, glify PL, line breaks, raster w docelowym rozmiarze, czas bez ruchu umożliwiający czytanie; safe zone zależy od kanału.
- Dźwięk: clipping, rozumienie VO, offset/drift, start/end fades, intencjonalny brak dźwięku; LUFS i true peak według konkretnego delivery briefu, bez globalnego progu.
- Performance: sekundy/klatkę (wall clock), peak RAM/VRAM, rozdzielczość, sample count, CPU/GPU i wersje; nie porównywać różnych quality settings jako wydajności silnika.
- Resume: render manifest i lista ukończonych klatek; ponowna generacja tylko brakujących/niezgodnych hashów. Sim cache może wymagać stanu wcześniejszego, nie tylko obrazów: [H08 Houdini cache](https://www.sidefx.com/docs/houdini/dyno/cache).
