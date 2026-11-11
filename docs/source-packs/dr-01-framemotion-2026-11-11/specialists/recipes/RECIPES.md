# DR-01 — 18 receptur produkcyjnych motion designu

Badanie: 2026-11-11. Autor syntezy: specjalista Codex / recipes. Status: badanie dokumentacji i publicznych tekstów; wszystkie sceny i testy wykonawcze **NOT_RUN**. Nie wygenerowano filmu ani projektu AE. Procedury, przykłady, kryteria QA i analogie kodowe są **DERIVED**. Krótkie zdania oznaczone **SOURCED** wskazują wyłącznie mechanizm potwierdzony źródłem, a nie przetestowanie całej receptury. Nie kopiowano plików tutoriali, fontów, assetów ani kodu autorów.

## Jak korzystać

Każda receptura ma znaczenie komunikacyjne i punkt zatrzymania. Nie trzeba wykorzystać wszystkich: pojedyncza scena zwykle potrzebuje jednego dominującego działania. „Budowa” opisuje świadomy wariant sceny, nie instrukcję odtworzenia cudzego projektu. Wszelkie liczby w polu **Parametry** są **proponowanymi punktami startowymi**, nie normami programu ani branży. Wspólny kontekst ćwiczeń: 1920 × 1080 px, 25/1 fps; wariant pionowy 1080 × 1920 px wymaga ponownego rozmieszczenia elementów. 1 klatka w tym ćwiczeniu = 40 ms. W produkcji obowiązuje FPS właściciela timeline, nie ten przykład.

Podane tolerancje QA są propozycją umowy dla syntetycznego benchmarku. Trzeba je zmienić przy innym rozmiarze, rodzaju ruchu, kanale i odbiorcy. Ocena techniczna to także pełne odtworzenie w czasie rzeczywistym; pojedyncze klatki nie potwierdzają płynności. Każdy zapis audio zachowuje czas źródła oraz czas nadrzędnej osi; klatki analizy audio nie są klatkami wideo.

| ID | Receptura | Dominująca decyzja | Program odniesienia |
|---|---|---|---|
| R01 | Logo z kontrolowanego rysunku | Kierunek odsłania znaczenie znaku | After Effects |
| R02 | Kinetic typography | Ruch podporządkowany składni | After Effects / Motion |
| R03 | Lower third o zmiennej długości | Chronione wejście i wyjście | After Effects |
| R04 | Product reveal | Najpierw sylwetka, potem detal | AE + Blender/C4D jako wariant hybrydowy |
| R05 | Explainer przyczynowo-skutkowy | Widz śledzi jedną przyczynę | After Effects |
| R06 | Animacja stanu UI | Zachowanie tożsamości elementu | AE dla filmu, web dla interakcji |
| R07 | Infografika | Geometria wynika z danych | After Effects / SVG |
| R08 | Przejście maskowe | Zmiana sceny przy pełnym przykryciu | After Effects |
| R09 | Parallax 2.5D | Rozdzielenie planów i marginesów | After Effects |
| R10 | Particles z rolą w scenie | Emisja akcentuje zdarzenie | Apple Motion |
| R11 | Synchronizacja muzyczna | Impact przypada na wybrany cue | AE / Motion + lista cue |
| R12 | VO i lyrics alignment | Czytelność przed podświetleniem | AE / Fusion |
| R13 | Screen replacement | Obiekt trzyma płaszczyznę | Fusion |
| R14 | Keying i integracja | Osobna kontrola krawędzi i koloru | Fusion |
| R15 | Overshoot i overlap | Masa bez ciągłego kołysania | C4D / AE |
| R16 | Pętla bez szwu | Zgodność stanu i prędkości | AE / kod |
| R17 | Cloner sterowany polem | Ruch wynika z położenia | Cinema 4D |
| R18 | Rack focus | Ostrość przekazuje uwagę | After Effects / Blender |

## R01 — Logo z kontrolowanego rysunku

**Problem i cel.** Znak ma zostać rozpoznany, zanim ozdobniki odciągną uwagę. Odsłonięcie podkreśla konstrukcję znaku: np. wspólną linię dwóch liter, a nie przypadkowe rozpadanie na fragmenty.

**Użyj / nie używaj.** Dla znaku liniowego i krótkiej identyfikacji; nie dla złożonego herbu, którego kolejność kreskowania ukrywa nazwę, ani gdy księga marki zabrania zmiany geometrii. Znak z wypełnieniem odsłaniaj maską, zamiast udawać, że każda jego granica jest kreską pisma.

**Assety.** Zatwierdzony wektor, osobne ścieżki znaczeniowe, końcowa plansza referencyjna, minimalny rozmiar logo i kolor tła.

**Budowa referencyjna.** W AE oddziel „rysunek” od nienaruszonego logo docelowego; przygotuj stroke jako matte dla finalnej grafiki. **SOURCED:** Trim Paths udostępnia Start, End, Offset oraz wspólną albo indywidualną obsługę wielu paths [R-S01].

**Parametry — proponowane punkty startowe.** Reveal 0,72 s; końcowa ekspozycja 1,2 s; 3 grupy ze stagger 0,08 s; stroke matte szerszy od odsłanianej kreski o 4 px w tej rozdzielczości. Brak overshootu w geometrii samego logo.

**Operacje.** Najpierw porównaj finalny znak z plikiem wzorcowym. Ustal początek i kierunek każdej kreski. W blocking odsłoń cały znak liniowo. Następnie dopracuj przyspieszenie dominującej kreski; inne podporządkuj jej zakończeniu. Zatrzymaj ruch przed planszą końcową, dopiero wtedy oceniaj dodatkowy akcent światła.

**Błąd → naprawa.** Znak „gryzie się” w przecięciu ścieżek: zbyt szeroka matte odsłania sąsiedni fragment. Podziel maskę na logiczne obszary lub zastosuj lokalne holdouty, zamiast zwiększać blur. Poprawny wariant odsłania fragmenty w zamierzonej kolejności i kończy dokładnie na oryginale.

**Kod.** SVG path + długość łuku + `strokeDashoffset`, osobny clip/mask dla finalnego wektora. Wierny dla prostego stroke; złożony kompozyt matte jest zależny od backendu. Nie rasteryzuj logo w niskiej rozdzielczości.

**QA.** Końcowe kontury i proporcje zgodne ze wzorcem; żadna przypadkowa wyspa przed reveal; brak szwu na join; czytelność miniatury; stabilna pełna ekspozycja.

**Źródło mechanizmu:** [R-S01 — Adobe, Shape operations](https://helpx.adobe.com/after-effects/desktop/drawing-painting-and-paths/shapes-and-shape-attributes/shape-attributes-paint-operations-path.html).

## R02 — Kinetic typography z polskim tekstem

**Problem i cel.** W zdaniu „Ruch pomaga zrozumieć zmianę” widz powinien odczytać myśl i zauważyć słowo „zmianę”. Jednoczesny skok wszystkich liter daje aktywność bez hierarchii.

**Użyj / nie używaj.** Dla krótkich tez i rytmicznego copy; nie dla gęstej instrukcji, tekstu prawnego ani długich napisów dostępności. Nie animuj grafemów niezależnie, gdy niszczy to ligaturę lub połączenie znaku ze znakiem diakrytycznym.

**Assety.** Dokładny tekst, font z polskimi znakami i licencją, akceptowany podział wierszy, słowa akcentowane, ewentualny cue VO.

**Budowa referencyjna.** AE: jeden stabilny layout i animator słów, osobna grupa akcentu. **SOURCED:** animatory i selectors działają na zakresach tekstu [R-S02]. Motion: Sequence Text pozwala wybrać znak, słowo lub wiersz, kierunek oraz seed [R-S03].

**Parametry — proponowane punkty startowe.** Wejście słowa 0,24 s; stagger 0,10 s; przesunięcie 0,35 wysokości wiersza; akcent skali 100→104→100% przez 0,32 s; pełne zdanie nieruchome przez 1,4 s.

**Operacje.** Najpierw zatwierdź statyczny skład i wyrenderuj próbkę „Zażółć gęślą jaźń”. Ustal chwile pełnej czytelności, potem wylicz starty. Zacznij od słów, a literowe szczegóły dodaj tylko do jednego fragmentu. Maskę odsłonięcia odsuń od ogonków i akcentów. Dopasuj wersję 9:16 przez nowy podział wierszy, nie przez zmniejszenie wszystkiego.

**Błąd → naprawa.** Litera „ą” miga lub odrywa ogonek: segmentacja po punktach kodowych / przeładowanie fontu. Segmentuj po grafemach, poczekaj na font i zamroź metryki; przy trudnym shaping animuj całe słowo. Poprawny wynik zachowuje kerning podczas ruchu.

**Kod.** Shaped text runs, identyfikatory słów i bounds; `localTime = t - cue.start - word.delay`. DOM/SVG daje dobry odpowiednik, jeśli metryki i font są identyczne; rozdzielenie każdego znaku na span może zmienić kerning.

**QA.** Zgodność tekstu znak w znak; brak reflow; widz odczytuje zdanie bez pauzowania; jednoznaczny akcent; brak obciętych diakrytyków.

**Źródła:** [R-S02 — Adobe, Animating text](https://helpx.adobe.com/after-effects/desktop/animating-text/text-animation/animating-text.html), [R-S03 — Apple, Sequence Text](https://support.apple.com/en-mide/guide/motion/motn1607df2b/mac).

## R03 — Lower third z chronionym wejściem i wyjściem

**Problem i cel.** Ten sam podpis musi działać przez 4 i 11 s bez spowolnienia wejścia. Długość nazwiska może zmienić szerokość tła, lecz nie tempo ruchu.

**Użyj / nie używaj.** Rozmowy, identyfikacja osoby, lokalizacja; nie jako osobna dominująca plansza ani na twarzy / napisach już obecnych w obrazie.

**Assety.** Imię, nazwisko, funkcja, font, tło testowe jasne i ciemne, zaakceptowana pozycja i zakres czasowy od FrameCut.

**Budowa referencyjna.** Oddziel tekst, tło i accent bar. **SOURCED:** Responsive Design–Time w AE chroni wskazane okresy podczas rozciągania pozostałej części; zmienione markery zagnieżdżenia trzeba aktualizować [R-S04]. Wariant Fusion: Text+ i osobna maska; Follower tylko, jeśli ruch liter ma sens [R-S11].

**Parametry — proponowane punkty startowe.** Intro 0,40 s; outro 0,28 s; padding poziomy 24 px i pionowy 14 px; test nazw 8, 22 i 40 znaków; ekspozycja liczona po zakończeniu ruchu tekstu.

**Operacje.** Wyznacz width z rzeczywistych bounds. Odsłoń podkład, po nim tekst. Oznacz intro/outro jako chronione, a hold jako elastyczny. Zdefiniuj minimalną długość jako sumę intro, zaakceptowanego hold i outro. Testuj skrajne długości copy. Eksportuj tylko jawne kontrolki: treść, wariant, kolor z zatwierdzonej palety.

**Błąd → naprawa.** Krótki klip nakłada outro na ostatnie litery intro. Odrzuć zbyt krótki slot albo wybierz zatwierdzony uproszczony wariant; nie kompresuj całej sceny bez decyzji timeline owner. Animowane audio w MOGRT wymaga osobnej kontroli — dokumentacja wskazuje ograniczenie adaptacyjnego rozciągania audio [R-S04].

**Kod.** Trzy odcinki `intro/hold/outro`, layout constraints i funkcja czasu kawałkami. Wierny dla transform/matte; eksport do MOGRT to osobny adapter, nie sam JSON.

**QA.** Długość intro identyczna we wszystkich testach; pełne nazwisko bez ellipsis, jeśli nie uzgodniono skrótu; kontrast na rzeczywistym ujęciu; logo i treść zachowują locks.

**Źródła:** [R-S04 — Adobe, Responsive Design–Time](https://helpx.adobe.com/after-effects/desktop/motion-graphics/add-responsive-design/responsive-design.html), [R-S11 — Blackmagic, rozdz. 6](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fusion-Visual-Effects.pdf).

## R04 — Product reveal: sylwetka, cecha, etykieta

**Problem i cel.** Widz ma rozpoznać produkt i jedną cechę. Przedłużona ciemność lub ciągły obrót może wyglądać efektownie, lecz nie wyjaśniać, co jest sprzedawane.

**Użyj / nie używaj.** Packshot, komponent przemysłowy, prezentacja materialności; nie przy braku poprawnego modelu, gdy obrót ujawni wymyślony tył produktu. Płaskiej fotografii nie obracaj poza zakres, który potrafi wiarygodnie pokazać.

**Assety.** Zatwierdzona fotografia z alfą lub model, tekstury/etykiety, wymiary, referencja materiału i końcowy packshot.

**Budowa referencyjna.** AE: cutout produktu, odrębny cień, matte dla kontrolowanego glintu, spokojne tło i etykieta. **SOURCED:** kamera AE steruje perspektywą 3D; zwykłe 2D nie staje się modelem bryłowym [R-S18]. Dla realnego obrotu wybierz hybrydę Blender/C4D: model w skali, kamera na rig, duże powierzchnie świetlne i osobny render do compositingu. Kontrole perspektywy i ostrości kamery Blendera potwierdza [R-S19]; cały wariant pozostaje **DERIVED / NOT_RUN**.

**Parametry — proponowane punkty startowe.** 3,6 s całości; sylwetka czytelna w 0,6 s; obrót 15° przez 1,2 s; końcowy hold 1 s. W scenie 3D obiektyw 70 mm i orientacyjna wysokość produktu 0,20 m wyłącznie dla syntetycznej butelki; nie dla każdego produktu.

**Operacje.** Zatwierdź nieruchomy końcowy packshot. Ustaw światło na kształt i etykietę. Zaprojektuj jedno odsłonięcie; ruch kamery dodaj później. Tekst cechy pojawia się, gdy powierzchnia produktu przestaje gwałtownie zmieniać orientację. Sprawdź kadr pionowy z większą przestrzenią nad produktem.

**Błąd → naprawa.** Odbicie przechodzi przez nazwę w chwili czytania. Zmień tor/rozmiar źródła i moment glintu; nie naprawiaj wyłącznie obniżeniem ekspozycji całego produktu. Poprawny reveal daje kulminację i spokojny czas identyfikacji.

**Kod.** Dla cutout: SVG/Canvas; dla bryły: Three.js lub render Blender Python. To workflow hybrydowy; światła i BRDF nie mają wiernego odpowiednika w zwykłym CSS box-shadow.

**QA.** Poprawna etykieta, brak deformacji produktu, wiarygodny cień, brak przepaleń zasłaniających istotną treść, identyczny hero pose ze styleframe.

**Źródła:** [R-S18 — Adobe, Cameras](https://helpx.adobe.com/after-effects/desktop/work-with-layers/camera-layer/cameras-lights-points-interest.html), [R-S19 — Blender, Cameras](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cameras.rst). Wariant Blender nie został uruchomiony.

## R05 — Explainer: przepływ przyczyny przez system

**Problem i cel.** Wyjaśnić, jak wejście zmienia wynik, np. „sygnał → filtr → czytelny wykres”. Przedmioty mają reagować na zdarzenie, a nie pojawiać się jak slajdy.

**Użyj / nie używaj.** Procesy, zależności, onboarding; nie gdy model przyczynowy jest niepotwierdzony lub animacja sugerowałaby rzeczywistą skalę czasu, której dane nie uzasadniają.

**Assety.** Zatwierdzony diagram, nazwy etapów, treść VO, ikony, wybrany kierunek czytania i legenda koloru.

**Budowa referencyjna.** AE: osobny precomp na etap i jeden kontroler czasu zdarzenia; connectors jako shapes. **SOURCED:** operacje ścieżek mogą sterować odsłanianiem connectora [R-S01]. Część narracyjna pozostaje własną syntezą, a nie automatycznym wynikiem efektu.

**Parametry — proponowane punkty startowe.** 3 etapy; podróż tokenu 0,60 s; reakcja etapu 0,24 s; pauza rozumienia 0,65 s; token 18 px, connector 4 px w ćwiczeniu.

**Operacje.** Zrób storyboard stanu przed/po. W animatic pokaż tylko token i zmianę wyniku. Ustaw opóźnienia od przybycia tokenu, nie od arbitralnego początku sceny. Dopiero potem dodaj etykiety pomocnicze i secondary motion. Jeśli VO wydłuży zdanie, wydłuż hold uzgodniony z właścicielem timeline, nie zmieniaj prędkości „fizycznej” bez intencji.

**Błąd → naprawa.** Wynik świeci, zanim token dotrze do filtra; oko nie widzi przyczyny. Zapisz dependency `result.start >= filter.impact`; przejrzyj animatic bez dźwięku. Poprawny wariant komunikuje tę samą relację także w ciszy.

**Kod.** Graf zdarzeń, `onArrival` jako deklaratywny cue i krzywa długości łuku. Nie używaj callbacków zależnych od poprzednio odtworzonej klatki; każda klatka ma wynikać z czasu i stanu projektu.

**QA.** Kolejność przyczynowa poprawna, etykiety nie konkurują z ruchem, connector dochodzi do właściwego portu, wszystkie trzy etapy widoczne w obu formatach. Odbiorca potrafi powiedzieć, co się zmieniło.

**Źródło mechanizmu:** [R-S01 — Adobe, Shape operations](https://helpx.adobe.com/after-effects/desktop/drawing-painting-and-paths/shapes-and-shape-attributes/shape-attributes-paint-operations-path.html).

## R06 — Przejście stanu UI z zachowaniem tożsamości

**Problem i cel.** Karta rozwija się w widok szczegółowy. Użytkownik ma rozumieć, że to ten sam obiekt, a nie nowy ekran oderwany od działania.

**Użyj / nie używaj.** Demo produktu, prototyp interakcji; nie przenoś długiego filmowego reveal do często używanej kontrolki. Animacja filmu i działające UI mają inne wymagania dotyczące przerwania.

**Assety.** Dwa stany layoutu, stały ID obiektu, fonty, treść, stany loading/error, scenariusz kliknięcia oraz reduced-motion.

**Budowa referencyjna.** AE do filmu: card container, content i clip region osobno. **SOURCED:** Apple HIG zaleca celowy, krótki feedback, możliwość anulowania ruchu i alternatywny sposób komunikowania informacji [R-S05]. Ta zasada projektowania nie określa uniwersalnego czasu tweena.

**Parametry — proponowane punkty startowe.** Przejście 0,28 s; opacity nowej treści 0→100% przez końcowe 0,12 s; brak bounce na obszarze tekstowym; reduced-motion: krótka zmiana opacity 0,08 s, jeśli zaakceptowana dla docelowego produktu.

**Operacje.** Wybierz element zachowujący ciągłość: obraz lub nagłówek. Animuj jego bounds, a tekst nowego widoku ujawnij po ustabilizowaniu layoutu. Zaprojektuj powrót i przerwanie w połowie ruchu. W demonstracji filmowej pokaż kursor i rzeczywisty moment inputu, nie „telepatyczną” reakcję.

**Błąd → naprawa.** Skalowanie całego screenshotu rozciąga tekst i radius narożników. Rozdziel bounds kontenera, obraz i layout typografii; tekst zmień przez kontrolowaną wymianę, jeśli identyczny shaping nie jest możliwy. W prawdziwym UI nowy input przejmuje sterowanie bez resetu do starego początku.

**Kod.** Wierny geometryczny odpowiednik: FLIP / shared-element layout; state machine dla interakcji. AE jest wizualnym prototypem, nie testem zachowania aplikacji. Fallback: crossfade zachowujący treść i focus.

**QA.** Tożsamość obiektu czytelna, brak reflow błysku, keyboard focus poprawny w wersji interaktywnej, możliwość przerwania, wynik działania zrozumiały także bez ruchu.

**Źródło:** [R-S05 — Apple HIG, Motion](https://developer.apple.com/design/human-interface-guidelines/motion.md).

## R07 — Infografika, w której ruch nie fałszuje danych

**Problem i cel.** Pokazać syntetyczne wartości 20, 35 i 50 jednostek. Kolejność animacji ma objaśniać porównanie, a geometria zachować relacje.

**Użyj / nie używaj.** Porównania, zmiany, skład udziałów; nie stosuj do niezweryfikowanych danych lub gdy atrakcyjne overshooty sugerują chwilowe wyniki, których nie było.

**Assety.** Tabela źródłowa, jednostki, okres, denominator, etykiety, zaakceptowana skala. Dane tego ćwiczenia są jawnie syntetyczne.

**Budowa referencyjna.** AE shapes mają anchor na baseline; etykiety pozostają osobnymi elementami. Kod renderuje ten sam model danych. **SOURCED:** oddzielenie parametrów shape od ścieżek umożliwia parametryczny rysunek [R-S01]; reguły prawdziwości wykresu są tutaj **DERIVED**, nie przypisane Adobe.

**Parametry — proponowane punkty startowe.** Wysokość wykresu 500 px; domena 0–50 jednostek; wzrost 0,8 s; stagger 0,12 s; końcowy hold 1,8 s; brak overshootu wartości.

**Operacje.** Sprawdź dane i jednostki przed designem. Wyrysuj stan końcowy oraz baseline. Przy animowaniu słupków utrzymaj wspólną skalę. Możesz animować licznik, ale odróżnij interpolację ilustracyjną od zmiany w czasie rzeczywistych danych. Końcowe etykiety pojawiają się najpóźniej wraz z zatrzymaniem słupka. W 9:16 rozważ poziome słupki, zachowując wartości i kolejność.

**Błąd → naprawa.** Anchor na środku powoduje rośnięcie w obu kierunkach; odbiorca traci wspólny punkt odniesienia. Przenieś anchor na baseline albo bezpośrednio wylicz top/bottom. Inny błąd: licznik osiąga 50, gdy słupek ma jeszcze 90% wysokości — użyj jednej funkcji postępu.

**Kod.** `height = scale(value) * progress(t)`; jawny domain/range, formatowanie locale PL i decimal policy. SVG jest wierny dla płaskiego wykresu. 3D słupki jako dekoracja mogą utrudniać porównanie.

**QA.** Finalne wartości i proporcje zgodne z tabelą; zero obciętych etykiet; brak zmiany denominatora; sprawdzony odczyt bez dźwięku; oznaczenie danych przykładowych.

**Źródło mechanizmu:** [R-S01 — Adobe, Shape operations](https://helpx.adobe.com/after-effects/desktop/drawing-painting-and-paths/shapes-and-shape-attributes/shape-attributes-paint-operations-path.html).

## R08 — Przejście maskowe z kontrolowanym punktem cięcia

**Problem i cel.** Zmienić scenę bez utraty kierunku uwagi. Kształt ze sceny A rozszerza się, przykrywa kadr i staje się elementem sceny B.

**Użyj / nie używaj.** Gdy wspólna forma niesie związek znaczeniowy; nie przy każdej zmianie sceny ani gdy zwykłe cięcie jest czytelniejsze. Handles muszą wystarczyć na przejście.

**Assety.** Sceny A/B, wspólny kształt, wskazany moment cięcia, ustalona alfa i kolor pracy.

**Budowa referencyjna.** AE: osobna matte i dwa precompy; wybór alpha/luma jest jawny. **SOURCED:** tabela trybów Adobe definiuje Alpha/Luma 100% jako opaque i wersje inverted odwrotnie [R-S06]. W tekście tej samej strony istnieje sprzeczne zdanie ogólne; nie wykorzystuj go jako specyfikacji.

**Parametry — proponowane punkty startowe.** Przejście 0,48 s; pełne przykrycie przez 2 klatki; overscan maski 32 px; feather 0 px dla ostrego brandowego wipe, ewentualnie 2 px po kontroli krawędzi.

**Operacje.** Wyznacz klatkę pełnego przykrycia. Zaprojektuj środek przejścia przed początkiem i końcem. Przełącz źródło w zakrytym okresie; dopasuj pozycję elementu wyjściowego. Dodaj blur dopiero po pewności, że coverage jest pełny. Sprawdź alpha oraz matte w osobnym podglądzie.

**Błąd → naprawa.** Jednoklatkowy błysk A albo czerni przy zmianie B: maska nie pokrywa rogu po transformacji. Powiększ jej geometryczny zakres, sprawdź motion blur i indeksy [in,out), zamiast przykrywać usterkę glow. Poprawny wynik zachowuje ciągłą dominantę ruchu.

**Kod.** SVG clipPath dla ostrej granicy, alpha mask / render target dla feather i luma; `mix(A,B,m)` tylko przy zgodnym color/alpha pipeline. To przybliżenie dla efektów zależnych od render order AE.

**QA.** Test matte 0%, 50%, 100% oraz inverted; brak dziur na całym kadrze, również 9:16; identyczna długość filmu; brak nieuzgodnionego freeze ostatniej klatki.

**Źródło:** [R-S06 — Adobe, Track Mattes](https://helpx.adobe.com/after-effects/desktop/work-with-transparency-and-compositing/work-with-track-mattes-and-traveling-mattes/track-mattes-and-traveling-mattes.html).

## R09 — Parallax 2.5D z jednego obrazu

**Problem i cel.** Nadać nieruchomej ilustracji oddech i głębię bez udawania dowolnego ruchu kamery w pełnej scenie 3D.

**Użyj / nie używaj.** Dla ilustracji z separowalnymi planami; nie dla dużego obrotu odsłaniającego tył obiektów, wielu przejrzystości i braku materiału pod wycięciami.

**Assety.** Foreground, middle, background z alfą; uzupełnione obszary wcześniej zasłonięte; referencyjna klatka bez ruchu.

**Budowa referencyjna.** AE: karty 3D na różnych Z i kamera poruszana jednym rigiem. **SOURCED:** wielkość projekcji zależy od odległości warstwy względem Zoom kamery [R-S18]. Przy rozstawianiu planów skompensuj scale, aby klatka referencyjna zachowała kompozycję.

**Parametry — proponowane punkty startowe.** 3 plany; ruch ekranu dla planu bliskiego 45 px i dalekiego 10 px przez 4 s; poziomy overscan co najmniej wynikający z maksymalnego odsłonięcia plus 20 px testowego marginesu. Wartości Z dobierz do kamery, nie kopiuj między scenami.

**Operacje.** Wytnij plany i obejrzyj ich krawędzie na kontrastowym tle. Napraw brakujące obszary. Ustaw pozycje w referencyjnym kadrze. Zbadaj skrajne położenia kamery przed easingiem. Potem dodaj jeden wolny ruch; osobne ruchy obiektów tylko z uzasadnieniem.

**Błąd → naprawa.** Za głową pojawia się halo albo dziura: wycięcie zostało przesunięte bez uzupełnienia tła. Napraw clean plate, zmniejsz ruch albo zmień ujęcie; blur nie odtwarza informacji. Jeśli scena wygląda jak karton, ogranicz różnicę prędkości i wybierz dłuższy dystans kamery.

**Kod.** Three.js textured planes — wierny model kart perspektywicznych; CSS translate dla planów — przybliżenie bez prawdziwej projekcji. Blender: proponowana hybryda z płaszczyznami, kamerą i uzupełnionymi teksturami, **NOT_RUN**.

**QA.** Brak odkrytych pustych obszarów w skrajnych klatkach; stabilna alfa; plan bliski reaguje zgodnie z ruchem; tekst 2D nie otrzymuje przypadkowej perspektywy.

**Źródło:** [R-S18 — Adobe, Cameras](https://helpx.adobe.com/after-effects/desktop/work-with-layers/camera-layer/cameras-lights-points-interest.html).

## R10 — Particles jako skutek zdarzenia

**Problem i cel.** Krótkie rozproszenie oznacza energię po kontakcie, nie stały „brokat” odciągający uwagę od produktu.

**Użyj / nie używaj.** Dla iskier, rozproszenia, atmosfery lub przepływu; nie do przykrycia słabej kompozycji ani na obszarze tekstu wymagającego spokojnego odczytu.

**Assety.** Własny prosty sprite z alfą, miejsce emisji, cue zdarzenia, paleta, strefa wolna od cząstek.

**Budowa referencyjna.** Motion: emitter i osobna particle cell. **SOURCED:** Birth Rate jest liczbą narodzin na sekundę, Life czasem życia w sekundach; opacity over life pozwala uniknąć nagłego znikania [R-S07]. Ustal seed, jeśli dana konfiguracja go eksponuje; sam seed nie gwarantuje zgodnego seek przy symulacji stanowej.

**Parametry — proponowane punkty startowe.** Burst 45 cząstek; emisja ciągła 0 cząstek/s po burst; life 0,6–0,9 s; rozmiar sprite 3–9 px; prędkość w modelu kodowym 80–220 px/s; fade przez ostatnie 30% życia. Jednostkę prędkości kontrolki konkretnego programu sprawdź osobno.

**Operacje.** Zatwierdź pojedynczą cząstkę na tle. Ustaw moment i kierunek emisji od zdarzenia. Sprawdź gęstość, tor, zanikanie; dopiero potem włącz additive/glow. Zrób cache lub analityczny model po czasie. Przy pętli przelicz też cząstki narodzone przed początkiem widocznego odcinka.

**Błąd → naprawa.** „Popcorn” na końcu życia: opacity pozostaje stała do śmierci. Wprowadź krzywą zaniku i zróżnicowane life. Drugie ryzyko: zbyt wiele nakładających się additive sprites przepala logo — ogranicz emisję i wyklucz jego obszar.

**Kod.** Lista stabilnych ID, birth/death, seed per ID, analityczne `p=p0+v*a+0.5*g*a²`. Wierny dla prostego balistycznego ruchu; fluid/collision wymaga symulacji i cache, nie kilku tweenów.

**QA.** Identyczny układ dla renderu kolejnego i seek tej samej klatki; brak nagłych zniknięć; limit widocznych cząstek; czysty obszar copy; kontrola nad czasem emisji.

**Źródło:** [R-S07 — Apple, Particle cell controls](https://support.apple.com/en-mide/guide/motion/motn7ccaeefa/mac).

## R11 — Synchronizacja muzyczna z momentem wizualnego akcentu

**Problem i cel.** Najmocniejszy ruch ma trafiać w wybrany akcent muzyki; nie każdy element ma pulsować do amplitudy.

**Użyj / nie używaj.** Spot, ident, sekwencja tytułowa; nie opieraj narracji wyłącznie na detekcji beatów w ambientach, rubato lub utworze z niejednoznacznym pulsem.

**Assety.** Legalny plik audio w ustalonej wersji, sample rate, offset montażowy, lista ręcznie skorygowanych cue i właściciel timeline.

**Budowa referencyjna.** AE markers jako zdarzenia, krzywe ruchu jako odpowiedź. Motion Audio behavior może sterować parametrem od właściwości audio, np. pasma basowego [R-S10], lecz nie stanowi automatycznej analizy metrum. **SOURCED:** librosa oddziela detekcję onsetów od beat tracking opartego także na tempie [R-S08, R-S09].

**Parametry — proponowane punkty startowe.** Anticipation 0,16 s; impact w `cue.time`; settle 0,24 s. Dla syntetycznego 120 BPM beat co 0,5 s, ale nie przypisuj takiej siatki nagraniu o zmiennym tempie. QA twardego akcentu: odchyłka do 1 klatki tego benchmarku, ostatecznie odsłuch.

**Operacje.** Odsłuchaj frazy. Rozdziel onset, beat, downbeat i zmianę sekcji. Oznacz pewność oraz ręczne korekty. Wybierz kilka akcentów o różnych rangach. Wylicz `start = impact - lead_in`, a nie `start = beat`. Dodaj SFX dopiero po akceptacji ruchu. Sprawdź offset na początku i drift pod koniec całego fragmentu.

**Błąd → naprawa.** Start tweena trafia w werbel, lecz element uderza 0,3 s później. Przypnij kontakt / maksimum skali / pełne reveal do cue, a przygotowanie przesuń wcześniej. Przy dryfie nie przesuwaj wszystkich cue o ten sam offset — sprawdź sample rate, retiming i mapę tempa.

**Kod.** Jawne eventy `{kind,time_s,confidence,source,manual_override}`, interpolacja po absolutnym czasie. Downbeat wymaga metrum lub oddzielnej analizy; nie jest „co czwartym znalezionym onsetem”.

**QA.** Rozpoznane frazy i pauzy; jeden główny impact na cue; brak fałszywego tempa w ciszy; odsłuch z obrazem, a potem obraz bez dźwięku.

**Źródła:** [R-S08 — librosa beat_track](https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html), [R-S09 — librosa onset_detect](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html), [R-S10 — Motion Audio](https://support.apple.com/en-mide/guide/motion/motn13746bcf/mac).

## R12 — VO i lyrics: przygotowanie tekstu przed akcentem

**Problem i cel.** Słowa mają wspierać wypowiedź lub śpiew. Pojawienie się całego wiersza, rozpoczęcie słowa i zmiana koloru to różne zdarzenia.

**Użyj / nie używaj.** Kinetic VO, karaoke, lyric video; nie traktuj jako zamiennika standardowych napisów dostępności bez osobnej specyfikacji. Nie wyciągaj granic słów śpiewanych z samej amplitudy.

**Assety.** Zatwierdzony tekst, faktyczne audio tej samej wersji, word/syllable cues, poprawki interpunkcji, font i layout.

**Budowa referencyjna.** AE: baza tekstu i kopia highlight odsłaniana matte. **PRACTITIONER / SOURCED:** pisemne kroki Evana Abramsa opisują warstwy tekstu, maski wierszy oraz następujące po sobie reveal i highlight [R-S17]; film nie był oglądany. Fusion Follower nadaje się do sekwencji znaków, ale nie zastępuje alignmentu audio [R-S11].

**Parametry — proponowane punkty startowe.** Wiersz czytelny 0,20 s przed początkiem śpiewu; highlight przy ręcznie potwierdzonym onset słowa; koniec widoczności 0,30 s po końcu frazy, o ile następna fraza nie koliduje. Są to propozycje dla krótkiego benchmarku, nie norma napisów.

**Operacje.** Uzgodnij tekst z nagraniem. Rozdziel frazy według sensu i oddechu. Zweryfikuj czas słów, a dla wydłużonej sylaby również jej koniec. Najpierw pokaż pełny wiersz, następnie prowadź highlight po słowach. VO informacyjny może wymagać akcentu dopiero na słowie kluczowym, bez karaoke.

**Błąd → naprawa.** Stały liniowy wipe przechodzi przez trzy krótkie słowa i spóźnia się na długą sylabę. Zastąp go odcinkami po granicach słów; szerokość fragmentu ma wynikać ze składu, czas z audio. Nie rozciągaj tekstu, by wymusić rytm.

**Kod.** Shaped word boxes + cue list w sekundach, `highlight(word,t)` niezależne od `visibility(line,t)`. Typografię zachowaj z R02. Forced alignment, jeśli później dodany, to propozycja cue do odsłuchu, nie dowód poprawności śpiewu.

**QA.** Każde słowo zgodne z audio i pisownią; diakrytyki nie giną; tekst czytelny przed podświetleniem; brak zasłaniania twarzy; zmiana wersji VO unieważnia zależne cue.

**Źródła:** [R-S17 — Evan Abrams, Karaoke Text, kroki pisemne](https://www.premiumbeat.com/blog/after-effects-video-tutorial-karaoke-text/), [R-S11 — Blackmagic, Follower](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fusion-Visual-Effects.pdf).

## R13 — Screen replacement z planar tracking

**Problem i cel.** Wstawić UI do nagranego ekranu, utrzymując perspektywę, odbicia i zasłonięcia przez palce.

**Użyj / nie używaj.** Płaska, sztywna powierzchnia; nie zakładaj, że planar tracker wyjaśni deformującą się tkaninę lub mocno zakrzywiony ekran.

**Assety.** Plate, nowe UI w poprawnym aspekcie, reference frame, occlusion matte, informacje o dystorsji, kolorze i alfa.

**Budowa referencyjna.** Fusion: analiza Planar Tracker, dane do Planar Transform, potem Merge. **SOURCED:** Planar Transform stosuje dane śledzenia; sam nie śledzi i nie kompozytuje [R-S11]. Analizuj czytelną powierzchnię, unikając ruchu niezależnego od płaszczyzny.

**Parametry — proponowane punkty startowe.** Wybrany 4-sekundowy plate; referencja w najczytelniejszym momencie, nie obowiązkowo pierwsza klatka; testowy checker 10 × 6 pól; tolerancja ślizgania narożników 2 px przy 1080p do dalszej oceny w ruchu.

**Operacje.** Ustal, czy dystorsja wymaga korekty. Track od klatki referencyjnej w obie strony. Zweryfikuj nieruchomość powierzchni w trybie stabilizacji. Nałóż checker, potem UI. Przywróć odbicia i occlusion; dopasuj ostrość, poziom czerni i motion blur do plate.

**Błąd → naprawa.** Treść „pływa” mimo poprawnych narożników w jednej klatce: tracking objął palec albo odbicie. Zmień region analizy, wyklucz niezależny ruch, podziel track na zakresy lub ręcznie popraw błędne klatki. Nie ukrywaj dryfu agresywnym blur.

**Kod.** Homografia `H(t)` + raster UI + warstwa occlusion; wierny compositor 2D, ale dane trackingu wymagają osobnego narzędzia. Hybryda: analizuj w Fusion, eksportuj zweryfikowane transformacje lub render.

**QA.** Checker przyklejony przez cały zakres, poprawne zasłonięcia, brak dubla odbić, ekran nie jest ostrzejszy od nagrania, wszystkie krawędzie sprawdzone przy szybkim ruchu.

**Źródło:** [R-S11 — Blackmagic, rozdz. 4, drukowane s. 87–109](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fusion-Visual-Effects.pdf).

## R14 — Keying: czysta sylwetka, osobna integracja

**Problem i cel.** Osoba na nowym tle ma zachować włosy, półprzezroczystość i relację świetlną. Usunięcie zieleni nie kończy compositingu.

**Użyj / nie używaj.** Dobrze naświetlony green screen; nie zakładaj odzyskania nieistniejących szczegółów z przepalonej lub silnie skompresowanej krawędzi.

**Assety.** Plate, clean plate gdy dostępny, tło, maski pomocnicze, referencja oświetlenia, informacja straight/premultiplied.

**Budowa referencyjna.** Fusion: kluczowanie i matte przed końcowym Merge, osobne gałęzie do korekcji koloru oraz zasłonięć. **SOURCED:** oficjalny rozdział prowadzi przez clean plate, Delta Keyer, pomocnicze roto i dopasowanie koloru [R-S11]. Szczegółowe wartości zależą od plate.

**Parametry — proponowane punkty startowe.** Syntetyczny test 3 s z włosami, dłonią i szybkim ruchem; podgląd 100% oraz 200%; edge erosion początkowo 0 px, nie „profilaktyczne” wycinanie; feather dopiero po sprawdzeniu źródłowej ostrości.

**Operacje.** Oceń RGB i alfę oddzielnie. Usuń tło bez niszczenia drobnych detali. Garbage matte ogranicza zbędny obszar; holdout chroni wnętrze sylwetki. Dopiero potem usuń spill, dopasuj ekspozycję i temperaturę, dodaj pasujące grain. Sprawdź kompozyt na czarnym, białym i finalnym tle.

**Błąd → naprawa.** Ciemny obrys na białym tle: możliwa błędna interpretacja premultiplication lub skażony kolor krawędzi. Zweryfikuj alpha mode i kolejność unpremultiply/color/premultiply; nie poszerzaj key bez diagnozy. Migające włosy wymagają temporal review, nie tylko ładnej stopklatki.

**Kod.** Hybryda: wyeksportowany matte i foreground do compositor; prosty chroma-distance shader jest przybliżeniem, nie równoważnikiem Delta Keyer. Zachowaj oba strumienie i identyczny retiming.

**QA.** Brak zielonego spill w krytycznych miejscach, stabilne drobne włosy, brak dziur w ubraniu, poziom czerni i grain zgodne z plate; jawne nieweryfikowane fragmenty.

**Źródło:** [R-S11 — Blackmagic, rozdz. 5, drukowane s. 111–137](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fusion-Visual-Effects.pdf).

## R15 — Kontrolowany overshoot i overlap

**Problem i cel.** Element ma sprawiać wrażenie sprężystego albo ciężkiego, a po akcji osiągnąć stabilny stan. Sprężyna nie powinna stale odciągać wzroku.

**Użyj / nie używaj.** Brand o energicznym charakterze, miękki obiekt, secondary motion; nie dla danych liczbowych, geometrii logo chronionej lockiem lub UI wymagającego precyzyjnego końcowego położenia.

**Assety.** Hierarchia obiektu, punkt kontaktu, zatwierdzona poza końcowa, opis materiału / charakteru ruchu.

**Budowa referencyjna.** C4D: główny Effector wykonuje gest, Delay znajduje się po efektorach, których ruch przetwarza [R-S13]. AE: własne klucze są często lepsze do precyzyjnego staging niż expression dodany do każdej właściwości. **SOURCED:** historyczna dokumentacja R21 opisuje Spring oraz ryzyko Sub-Frame Motion Blur; nie jest to potwierdzenie aktualnego błędu 2026.

**Parametry — proponowane punkty startowe.** Główny ruch 0,36 s; overshoot 6% drogi; settling 0,48 s; secondary element opóźniony o 0,08 s; końcowe odchylenie pozycji poniżej 0,5 px w benchmarku.

**Operacje.** Najpierw ustaw docelową pozę i moment kontaktu. Zbuduj drogę bez sprężyny. Dodaj jedno przekroczenie celu oraz mniejsze cofnięcie. Opóźnij element wtórny, ale zachowaj jego przyczepienie. Jeżeli używasz symulacji, sprawdź start, preroll, cache i render z losowego frame.

**Błąd → naprawa.** Wszystko drga tym samym tempem: brak hierarchii masy. Ogranicz secondary do końcówki anteny / badge; rdzeń niech zatrzyma się wcześniej. Inny błąd: skok przy doklejeniu sinusoidy do tweena — dopasuj wartość i prędkość na łączeniu lub użyj jednej spójnej funkcji.

**Kod.** Analityczna tłumiona oscylacja albo solver z bake. Własny model nie jest identyczny z Delay C4D. Przykładowo `error(t)=A·exp(-λt)·sin(ωt+φ)` wymaga doboru fazy i warunków startu, nie tylko dodatniego A.

**QA.** Brak przenikania, stabilny koniec, czytelny jeden kontakt, ciągłość prędkości tam, gdzie nie zamierzono impactu; brak różnicy między preview i renderem.

**Źródła:** [R-S13 — Maxon, Delay 2026](https://help.maxon.net/c4d/2026/en-us/Content/html/OEDELAY.html), [uzupełnienie historyczne R21](https://help.maxon.net/c4d/r21/us/html/OEDELAY-MGDELAYEFFECTOR_GROUPEFFECTOR.html).

## R16 — Pętla bez szwu i bez przestoju

**Problem i cel.** Animacja tła lub mechanizmu ma powtarzać się bez zauważalnego restartu. Identyczne pierwsza i ostatnia wyświetlana klatka nie wystarczają.

**Użyj / nie używaj.** Ambient loop, loader, cykl mechaniczny; nie wymuszaj pętli na narracji, w której pojawia się nowa informacja.

**Assety.** Elementy cyklu, stan początkowy, długość w klatkach, kierunek, seed oraz obszar tekstu wolny od dominanty ruchu.

**Budowa referencyjna.** AE: powtarzany zakres parametrów albo jawny cykl; Motion może sekwencjonować tekst w Wrap/Ping-Pong [R-S03]. **PRACTITIONER / SOURCED:** Motion State rozróżnia przejście A/B od ruchu Continuous o stawkach na sekundę [R-S16]. To przydatny model myślenia, nie instrukcja instalowania pluginu.

**Parametry — proponowane punkty startowe.** T = 3,2 s, czyli 80 klatek przy 25 fps; obrót 360°/T; amplituda delikatnego oscylowania 6 px; eksport klatek 0–79, stan t=T służy do sprawdzenia zamknięcia, nie do podwójnego pokazania startu.

**Operacje.** Najpierw porównaj stany w t=0 i T. Sprawdź pochodne oraz kolejność warstw. Potem renderuj połączenie końców dwóch cykli. Dla noise użyj okresowej funkcji lub próbkowania po zamkniętej trajektorii; losowanie nowej wartości co klatkę nie tworzy spójnego ruchu. Dla particles przygotuj rozkład urodzeń z poprzedniego cyklu.

**Błąd → naprawa.** Pętla „zawiesza się” na szwie: wyeksportowano zdublowaną klatkę startową lub easing zeruje prędkość na każdym obrocie. Usuń duplikat, a ciągłą rotację prowadź liniowo. Poprawna pętla ma zamierzoną prędkość przez szew.

**Kod.** `phase = (frame % N)/N`; pozycja okresowa przez sin/cos, stabilne ID i deterministyczny seed. Wierny dla analitycznego cyklu; stanowa symulacja wymaga zamkniętego cache albo innego projektu.

**QA.** Widoczność szwu oceniona na co najmniej 3 cyklach; brak podwójnej klatki; zgodna prędkość; brak skoku blur lub noise; poprawny seek.

**Źródła:** [R-S03 — Sequence Text](https://support.apple.com/en-mide/guide/motion/motn1607df2b/mac), [R-S16 — Jake In Motion, Timing and Easing](https://docs.jakeinmotion.com/motion-state/concepts/timing-and-easing/).

## R17 — Budowanie formy przez Cloner i Field

**Problem i cel.** Wieloelementowa struktura ma powstawać według przestrzennej reguły. Kolejność wynikająca z indeksów pliku często nie odpowiada kompozycji.

**Użyj / nie używaj.** Moduły, dane, opakowania, abstrakcyjna architektura; nie dla małej liczby unikalnych obiektów wymagających indywidualnej gry aktorskiej.

**Assety.** Moduł źródłowy, docelowe transformacje, rozkład instancji, oś przejścia, materiał i seed.

**Budowa referencyjna.** Cinema 4D: Cloner i Plain Effector kontrolowany Field, osobne ograniczenie randomness. **SOURCED:** dokumentacja Maxon pokazuje oddzielne funkcje Plain/Box Field, Spline i Target oraz liczenie wpływu na klony [R-S12]. Nie są to nazwy równoważne Repeater AE.

**Parametry — proponowane punkty startowe.** Siatka 8 × 6 instancji; odstęp 0,12 m dla modułu 0,08 m; przesunięcie początkowe 0,25 m; przejście pola przez układ w 1,6 s; strefa falloff szerokości 0,24 m; random rotacji do ±6°.

**Operacje.** Ustaw finalny układ. Wyświetl pole wpływu jako grayscale/debug. Przesuń je przez strukturę i sprawdź kolejność. Dodaj minimalne zróżnicowanie, utrzymując powtarzalność. Dopiero potem światło, DOF i ewentualny Delay. Nie ukrywaj błędnego porządku pola przez zwiększanie liczby obiektów.

**Błąd → naprawa.** Konstrukcja składa się w pasy niezgodne z kierunkiem pola: pomylono przestrzeń lokalną i światową albo użyto indeksu zamiast położenia. Ujednolić układy współrzędnych i wizualizować `weight(position,t)`. Poprawny wynik tworzy czytelną falę, lecz nie wymusza ruchu każdego elementu identycznie.

**Kod.** Instancing + funkcja scalar field `w(p,t)` + mapowanie transformacji; Three.js/WebGL lub Blender Geometry Nodes/Python jako proponowany backend. Wierny dla zadeklarowanego pola matematycznego, przybliżony względem całej implementacji MoGraph.

**QA.** Stała liczba i tożsamość instancji; brak kolizji, chyba że zamierzone; kolejność zgodna z polem; powtarzalny seed; finalny układ zgodny ze styleframe; render seek nie zmienia układu.

**Źródło:** [R-S12 — Maxon, Effectors 2026](https://help.maxon.net/c4d/2026/en-us/Content/html/7443.html).

## R18 — Rack focus: prowadzenie uwagi ostrością

**Problem i cel.** Przekazać uwagę z bliskiego detalu na odległy obiekt, bez równoczesnego przesuwania wszystkich elementów i tekstu.

**Użyj / nie używaj.** Produkt, miniaturowa scena, narracyjny foreground/background; nie do ukrywania ważnej treści ani gdy płaska ilustracja ma pozostać graficznie ostra.

**Assety.** Rozdzielone plany lub rzeczywista scena 3D, pozycje celów ostrości, czytelny detal, informacja o rozmiarze / jednostkach sceny.

**Budowa referencyjna.** AE: karta bliska i daleka oraz kamera z animowanym Focus Distance; osobny null celu ostrości. **SOURCED:** AE udostępnia focus distance, aperture/f-stop i link ostrości do warstwy [R-S18]. Proponowany wariant Blender: zdefiniować skalę modelu, kamerę perspektywiczną, cel focus na Empty poruszający się między obiektami; finalną ocenę robić w wybranym rendererze. **SOURCED:** dokumentacja Blendera potwierdza Focus Object i informuje, że jego ustawienie wyłącza ręczny Focus Distance [R-S19]. Cała scena **DERIVED, NOT_RUN**; konkretna wersja runtime i API wymagają sprawdzenia.

**Parametry — proponowane punkty startowe.** Ujęcie 3 s; hold bliskiego planu 0,7 s; zmiana ostrości 0,8 s; hold celu 1,5 s; obiektyw przykładowej sceny 50 mm. F-stop dobierz do odległości i skali, zamiast kopiować jedną wartość „cinematic”.

**Operacje.** Ustal końcowe kompozycje i wymaganą ostrość obu celów. Włącz DOF bez ruchu. Zdefiniuj tor focus target w głębi. Ruch kamery dodaj tylko, jeśli wzmacnia zmianę znaczenia. Sprawdź bokeh i przezroczyste krawędzie; przy planach 2D nie obiecuj optyki identycznej z ray tracingiem.

**Błąd → naprawa.** Focus „pompkuje” lub przechodzi za obiektem: animowano arbitralną liczbę zamiast odległości do celu, bądź zmieniła się kamera. Podepnij cel w spójnej przestrzeni, sprawdź kilka klatek pośrednich. Halo na krawędzi przy blur głębokości może wymagać osobnych warstw albo pełnego renderu 3D.

**Kod.** Kamera i target distance w Three.js/Blender; post-process DOF to przybliżenie zależne od depth buffer. CSS blur dwóch kart daje tylko umowny efekt i nie odtwarza bokeh ani odsłonięć. Przy późniejszym motion blur nie myl DOF z Vector Blur: ten drugi używa passów Combined/Vector/Depth i ma ograniczenia odsłonięć; osobne render layers mogą pomóc [R-S20].

**QA.** Dokładnie jeden istotny cel czytelny w każdej fazie; stabilna ekspozycja; brak halo; tytuł nie ginie w blur; ostrość końcowa potwierdzona w pełnej rozdzielczości.

**Źródła:** [R-S18 — Adobe, Camera settings](https://helpx.adobe.com/after-effects/desktop/work-with-layers/camera-layer/cameras-lights-points-interest.html), [R-S19 — Blender, Cameras](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cameras.rst), [R-S20 — Blender, Vector Blur](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/filter/blur/vector_blur.rst).

## Wspólna kontrola i ograniczenia

Wykonawca powinien najpierw sprawdzić końcowy stan, potem moment głównego akcentu, a następnie drogę między nimi. Zmiany po feedbacku mają wskazywać recepturę, zakres klatek, obserwowalny błąd i lock, który pozostaje ważny. Proponowana granica iteracji: do dwóch poprawek jednej klasy błędu; przy trwałym problemie technicznym zmiana metody i raport luki, nie losowe dokładanie efektów. To limit organizacyjny przykładu, nie norma jakości.

Szczegółowe metadane źródeł są w `sources.json`. Docelowy kontrakt FrameMotion i dostępność backendów nie były w tym podzadaniu weryfikowane. Żaden program nie został uruchomiony. Źródła opisują funkcje; nie stanowią dowodu, że aktualna wtyczka je implementuje. Warianty Blender pozostają propozycjami wykonawczymi, lecz odczytano ich pierwotną dokumentację kamery i Vector Blur przez publiczne pliki RST; stron HTML nie udało się pobrać. Nie przypięto rewizji main do commit hash. Nie ustalono uniwersalnego FPS, safe zone, easingu, głośności ani długości sceny.
