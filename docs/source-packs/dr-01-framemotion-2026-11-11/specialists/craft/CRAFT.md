# DR-01 — Warsztat motion designu i compositingu

Data badania: 2026-11-11. Zakres specjalisty: A–D oraz typografia z E. Stan dowodu: przeczytane fragmenty dokumentacji i tekstowe podsumowanie samouczka; nie oglądano filmów, nie uruchamiano aplikacji ani projektów. Wszystkie proponowane testy: **NOT_RUN**. Funkcje obecnego FrameMotion: **Unknown**. To specyfikacja wiedzy do adaptacji, nie opis istniejącego silnika.

**SOURCED** oznacza zwięzłe ustalenie źródłowe. **DERIVED** oznacza autorską regułę, przykład, obliczenie lub test. W poniższych tabelach wszystkie decyzje, kontrprzykłady i testy są DERIVED, chyba że wprost zaznaczono SOURCED. Nie ma dowodów PRACTITIONER opartych na obejrzanym materiale. Rejestr 32 rzeczywiście odczytanych źródeł zawiera `sources.json`; próby nieudane są osobno, nie zwiększają licznika.

## A. Reżyseria ruchu

### Ruch ma znaczenie zanim ma krzywą

**SOURCED:** IBM definiuje własne stosowanie klasycznych zasad: ogranicza deformację i bounce, dopuszcza opóźniony ruch elementów podrzędnych i zaleca uporządkowane przejścia osiowe. To instrukcja konkretnej marki, nie uniwersalne prawo animacji. [C27]

**SOURCED:** Toon Boom omawia staging, przygotowanie akcji, deformację z zachowaniem objętości i opóźnione reakcje części obiektu. [C28]

**SOURCED:** IBM stosuje siatkę także w wideo, z konkretnymi proporcjami dla własnego systemu. [C29] Jego wskazówki animacji łączą prowadzenie uwagi, złożoność i rytm. [C30] Nie przenosimy wskazanego tam minimum 24 fps na uniwersalny test płynności: płynność zależy również od prędkości, kontrastu, shutter i sposobu próbkowania.

**DERIVED:** Animowane zdanie powinno mieć podmiot, czynność i skutek. „Panel rozwija się, aby ujawnić cenę” jest instrukcją wykonawczą; „dodaj dynamiczny vibe” nie pozwala rozpoznać błędu. W briefie zapisz:

- Co odbiorca ma zauważyć jako pierwsze, a co zapamiętać?
- Co zmienia stan: otwarcie, porównanie, wynik, połączenie, nagroda?
- Co jest obiektem fizycznym, co symbolem, a co elementem interfejsu?
- Które właściwości są zablokowane: kształt logo, treść, kolor, proporcje, czas czytania?

| Decyzja DERIVED | Kiedy działa | Kontrprzykład | Test NOT_RUN |
|---|---|---|---|
| Jeden dominujący akcent w danym momencie | Wyjaśnienie nowej informacji | Orkiestracja wielu punktów może świadomie oznaczać tłum lub złożoność | Obejrzeć bez dźwięku; wskazać pierwszy i drugi punkt uwagi |
| Ruch wynika z relacji przestrzennych | Karta wraca do stosu, linia łączy przyczynę ze skutkiem | Dekoracyjny wipe nie musi symulować obiektu | Przejścia zachowują rozpoznawalność obiektu przed i po ruchu |
| Staging przewiduje trajektorię | Bohater przechodzi przez pustą część kadru | Pusta przestrzeń bez funkcji rozprasza kompozycję | Obrys ruchu nie zasłania ceny, twarzy ani znaku |
| Pauza następuje po znaczeniu | Po odsłonięciu kluczowej liczby | Pauza przed odsłonięciem buduje napięcie | Po pierwszym odtworzeniu widz umie powtórzyć liczbę |
| Kontrast tempa tworzy hierarchię | Szybkie wejście, spokojne czytanie | Jednolite tempo może być potrzebne do porównania danych | Najwolniejszy fragment pokrywa się z najbardziej wymagającą treścią |
| Siatka stabilizuje punkty docelowe | Seria plansz lub UI | Ruch organiczny nie wymaga osiowego toru | Końcowe stany sprawdzić z jedną nakładką siatki |
| Kolor koduje funkcję | Akcent identyfikuje aktywną część | Zmiana koloru może fałszywie sugerować zmianę danych | W skali szarości nadal widać hierarchię wielkością i położeniem |

### Timing versus spacing

**DERIVED:** Timing to rozkład zdarzeń w czasie; spacing to odległości między kolejnymi stanami. Dwa ruchy mogą trwać tyle samo i przebywać tę samą drogę, a sugerować inną masę. Dla hipotetycznego przesunięcia o 600 px w 1 s przy 25 fps, ruch liniowy pokonuje 24 px między klatkami. Ruch z rozpędzaniem ma małe odstępy początkowe i większe w środku. Te liczby są przykładem matematycznym, nie receptą marki.

Anticipation nie musi być cofnięciem obiektu: może nim być zwężenie światła, zatrzymanie konkurujących elementów albo krótka zmiana skali otoczenia. Overshoot jest przekroczeniem celu; follow-through jest kontynuacją reakcji po głównej akcji; overlap oznacza przesunięcie faz między częściami. Nie stosuj jednego odbicia do wszystkich trzech.

Przykład autorski: pudełko z miękką zawartością może wyhamować, a jego etykieta dojść później. W wykresie kwartalnym taki sam poślizg wartości sugerowałby niepewność pomiaru. Sprężystość powinna opisywać materiał lub charakter komunikatu, a nie zasłaniać brak pomysłu.

| Charakter hipotetycznej marki | Propozycja ruchu DERIVED | Co odrzucić | Próba porównawcza |
|---|---|---|---|
| Precyzja techniczna | Ruch osiowy, czytelna przyczyna, kontrolowany settle | Losowy wobble liczb | Wersja ze stałym końcem versus pływającym końcem |
| Miękkość i zabawa | Umiarkowana deformacja, overlap, wyraźna reakcja | Deformowanie chronionego logotypu | Deformować nośnik, pozostawić znak w proporcji |
| Spokój i rzemiosło | Dłuższe przejścia materiałowe, mała liczba akcentów | Automatyczne „premium = wolno” | Zwięzła wersja z dłuższym czytaniem niż wejściem |
| Energia i sport | Kontrast przyspieszeń, kierunkowe przejścia | Nieprzerwane drżenie całej sceny | Czy akcja jest czytelna również bez SFX? |

## B. Model pracy After Effects

### Kompozycja, precomp i zależności

**SOURCED:** Kompozycje zagnieżdża się jako warstwy; standardowe zagnieżdżenie tworzy wynik obrazu przed jego użyciem w kompozycji nadrzędnej. Collapse transformations zmienia tę granicę. [C01]

**DERIVED:** Precomp wybieraj według odpowiedzialności: „logo wraz z własnymi odsłonięciami”, „produkt z cieniem”, „panel danych”. Nie zakładaj precompa wyłącznie po to, by ukryć bałagan. Każdy ma określony czas lokalny, obszar obrazu i wejścia. Dobrze zaprojektowany precomp można wymienić bez przesunięcia pozostałych scen.

**SOURCED:** Parenting propaguje transformacje przestrzenne, ale nie opacity. Dziecko ma jednego rodzica, a null może sterować innymi warstwami. [C06] Adjustment layer obrabia złożony obraz warstw pod nią, a nie niezależnie każdy ich obraz. [C02]

**DERIVED:** W danych FrameMotion rozdziel `parentTransform`, grupę compositingową i jawne powiązanie opacity. Jeden ogólny „group” ukrywa trzy odmienne działania. Anchor point umieszczaj przy zawiasie, kontakcie lub osi ruchu, zanim dopracujesz keyframes. Przy zmianie pivota oblicz kompensację położenia, żeby zaakceptowany kadr nie skoczył.

**SOURCED:** AE udostępnia konwersje współrzędnych warstw, m.in. użycie `toComp` na punkcie ścieżki. [C10]

**DERIVED:** Każda pozycja musi mieć przestrzeń: layer, composition, world lub screen. Wektor kierunku wymaga innej transformacji niż punkt, ponieważ przesunięcie nie powinno zmieniać kierunku. Test diagnostyczny: oznacz punkt kontrolny krzyżykiem, obróć i przeskaluj rodzica, sprawdź pokrycie. Jeśli etykieta odpływa, nie naprawiaj jej kolejnym offsetem bez ustalenia przestrzeni.

### Kolejność renderowania jest częścią obrazu

**SOURCED:** Dla warstwy rastrowej Adobe podaje masks → effects → transforms → layer styles. Dla ciągle rasteryzowanego wektora: masks → transforms → effects. Efekty wewnątrz stosu biegną od góry. Tekst i shape layers są ciągle rasteryzowane. Collapse może zachować współdziałanie 3D; adjustment layer wewnątrz collapsed precompa może ponownie wymusić spłaszczenie i crop. [C01]

**DERIVED:** To skrócony model wybranych operacji, nie kompletna specyfikacja każdego renderera, stylu, matte i efektu. Przed adaptacją zapisuj semantyczną kolejność operacji, zamiast samej listy nazw.

Test C-RO-01: koło z maską, blur o promieniu 12 px, skalowanie 200%, wariant wektorowy i raster. Zmieniaj tylko jeden przełącznik naraz. Rozmiar koła, szerokość brzegu i obcięcie poza granicą precompa porównuj oddzielnie. Wartości to proponowany punkt startowy. Kontrprzykład: „wygląda ostrzej” po włączeniu gwiazdki nie dowodzi poprawności — glow może przestać skalować się zgodnie z projektem.

### Shape layers i przezroczystość

**SOURCED:** Trim Paths operuje Start, End i Offset; może traktować wiele ścieżek jednocześnie lub kolejno. Repeater tworzy przekształcone kopie. Operacje path i paint mają określony zasięg w grupie. [C05]

**DERIVED:** Przy animowaniu znaku najpierw rozstrzygnij, czy chcesz odsłonić istniejący kontur, czy faktycznie zmienić geometrię. Trim nie jest morphem. Morph wymaga kontroli liczby, kolejności i korespondencji wierzchołków. Merge Paths może łączyć ścieżki w compound path lub wykonywać operacje boolowskie; sprawdzaj wybrany tryb, kolejność i regułę wypełnienia. Repeater nadaje się do struktury zależnej od jednego wzorca; osobne instancje lepiej obsłużą wyjątki z różnymi assetami.

**SOURCED:** Maska jest ścieżką modyfikującą właściwość warstwy, często alfa. [C07] Track matte może wskazywać dowolną warstwę, także wspólną dla kilku odbiorców; kontrolki rozróżniają alpha/luma i inversion. [C16] Większość blend modes zmienia RGB, lecz są wyjątki wpływające na alfa. [C08]

**Uwaga dowodowa:** Strona C16 ma zdanie sprzeczne z własną tabelą: opis ogólny mówi o wzroście przezroczystości wraz z wartością, a tabela Alpha/Luma mówi „100% = opaque”. Przyjmujemy jawne definicje kontrolek; test w aplikacji **NOT_RUN**. Nie powielać sprzecznego zdania do skilla.

**DERIVED:** Test C-MAT-01: trzy prostokąty matte — czarny, 50% szary, biały — z alfa równą 1. Alpha matte odsłania wszystkie; luma matte rozróżnia jasność; invert odwraca wynik. Druga wersja używa czerwieni i zieleni o tej samej alfa: wynik luma nie musi być identyczny. Nie traktuj luma jako „czerwonego kanału” ani dowolnej średniej RGB bez określenia przestrzeni.

## C. Animacja na poziomie ustawień

### Value graph i speed graph odpowiadają na różne pytania

**SOURCED:** Value graph pokazuje wartości właściwości; interpolacja czasowa opisuje ich zmianę w czasie, przestrzenna — kształt toru. Auto Bezier może spowodować niechciany „boomerang” między równymi pozycjami. [C04] Speed graph służy do tempa zmian; wpływ uchwytów jest osobnym parametrem. Easy Ease ustawia prędkość 0 i influence 33,33% po odpowiednich stronach klucza. To zachowanie narzędzia, nie wzorzec każdego ruchu. [C03]

**DERIVED — model matematyczny:** Dla położenia `p(t)=[x(t),y(t)]`, prędkość wektorowa to pochodna `v(t)=dp/dt`, a szybkość to jej długość `s(t)=||v(t)||`. Wykres skalarnej szybkości nie mówi, w którą stronę obiekt jedzie. Wykres x może być poziomy, gdy obiekt szybko porusza się po y. Wartość dodatnia nie oznacza dodatniej prędkości.

Dla skalaru `x(t)` nachylenie value graph wyraża `dx/dt`; w miejscu maksimum x pochodna wynosi zero, ale maksimum speed nie jest maksimum położenia. Należy odróżnić szybkość wzdłuż trajektorii od podpisanej pochodnej konkretnego kanału. Rozdzielenie X/Y ułatwia projektowanie łuku, ale dwa osobno wygładzone kanały mogą zmienić tor.

Proponowane zadanie: obiekt przechodzi przez punkt pośredni bez zatrzymania. Jeśli każdy keyframe dostanie Easy Ease, pojawi się zbędny stop. Poprawa: zachować niezerową prędkość przejścia i zgodny kierunek stycznych. Przy faktycznym zderzeniu ciągłość prędkości nie jest celem — skok prędkości może być intencją.

### Krzywe, fizyka i proceduralność

| Problem | Decyzja DERIVED | Kontrprzykład | Test NOT_RUN |
|---|---|---|---|
| Ruch kończy się zbyt miękko | Skrócić fazę hamowania, zachować poprawną pozycję końcową | Ciężki obiekt może wymagać dłuższego hamowania | Zestawić timing tej samej odległości, bez zmiany skali |
| Obiekt „zawraca” podczas pauzy | Sprawdzić tangenty przestrzenne; użyć Hold lub jawnego odcinka stałego | Umyślny orbit nie powinien być spłaszczony | Ślad pozycji podczas pauzy nie opuszcza punktu |
| Sprężyna nigdy nie siada | Zdefiniować próg oraz końcowy stan, nie tylko wzór | Wieczny oscylator jest poprawny dla metronomu | Ostatni zaakceptowany odcinek pozostaje stabilny |
| Pętla szarpie na szwie | Sprawdzić wartość i prędkość na granicy okresu | Stop-motion może celowo skakać | Powtórzyć pętlę trzy razy w ciągłym odtwarzaniu |
| Stagger trwa zbyt długo | Osobno sterować czasem jednostki i rozpiętością całej grupy | Długa lista wymaga alternatywnego reveal, nie mikroskopijnych opóźnień | Ostatni element ma pełny czas odczytu |
| Noise rozbija hierarchię | Modulować małą właściwość pomocniczą, zachować stały seed | Drganie może być znaczeniem awarii | Porównać klatkę w losowej kolejności renderu i liniowo |

**DERIVED:** W modelu fizycznym definiuj jednostki, siły, tłumienie, warunki początkowe i metodę integracji. W stylizowanym ruchu kontroluj czytelność gestu. Nie nazywaj arbitralnego overshoot „fizyką”. Prostą oscylację tłumioną można opisać `x=x_c+A·exp(-λt)·sin(ωt+φ)`; λ ma jednostkę 1/s, ω rad/s. To model przebiegu, nie dowód poprawnej symulacji kontaktów czy sprężyny z dowolnymi warunkami początkowymi.

**SOURCED:** `seedRandom(offset,true)` usuwa czas z ziarna funkcji random; parametr timeless nie steruje w ten sam sposób wiggle. [C10]

**DERIVED:** Stały seed nie wystarcza, jeśli liczba wywołań generatora zależy od liczby wcześniej wyrenderowanych klatek. Projektuj losowanie z tożsamości obiektu i czasu próbki albo zapisuj stan symulacji. Seek do klatki 70 po klatce 150 powinien odtworzyć zamierzony stan, nie historię odtwarzacza.

**SOURCED:** Time remapping zmienia przypisanie czasu kompozycji do czasu źródła. AE ma Frame Mix i Pixel Motion; motion blur materiału może utrudnić estymację ruchu. [C11]

**DERIVED:** Jeśli `t_source=f(t_timeline)`, pochodna f oznacza lokalne tempo. Wartość 0 oznacza zamrożenie, ujemna — cofanie. Nie retimuj całej sceny, gdy trzeba wydłużyć tylko pauzę na odczyt. Zachowaj intro/outro, zmień hold i zgłoś zmianę właścicielowi nadrzędnej osi.

## D. Obraz i compositing

### Przestrzeń, tracking i wiarygodność

**SOURCED:** Kamera AE rozróżnia położenie, zoom, focus distance i aperture; zmiana aperture wpływa na DOF, lecz AE nie symuluje przez nią automatycznie wzrostu ekspozycji. [C15] Tracking punktowy używa regionu cechy, regionu szukania i punktu przyczepienia; dwa punkty pozwalają śledzić skalę i obrót. [C17]

**DERIVED:** 2.5D jest sensownym modelem dla plansz w przestrzeni. Gdy trzeba zobaczyć bok produktu, wzajemne zasłanianie brył lub materialny refleks zmieniający się z kątem, wybierz geometrię 3D albo render hybrydowy. Sam ruch kamery nie tworzy brakującego boku zdjęcia. Parallax wymaga poprawnego kierunku i relacji prędkości planów; zbyt duża separacja ujawnia puste miejsca po wycięciu.

Dopasowuj kolejno: perspektywę i punkt kontaktu → zakres tonalny i kierunek światła → cień i odbicia → ostrość/DOF → rozmycie ruchu → grain. Ta kolejność jest propozycją diagnostyczną. Świetnie dopasowany grain nie naprawi cienia biegnącego w przeciwną stronę.

Test trackingu: porównaj marker z cechą obrazu na początku, końcu, zasłonięciach i zmianach kierunku oraz obejrzyj pełny przebieg. Mały średni błąd nie wyklucza widocznego jednorazowego skoku. Wstawka może wymagać planar trackingu, a nie kolejnych punktowych „łat”.

### Matte: wnętrze, brzeg i czas

**SOURCED:** Keying definiuje transparentność z koloru, luminancji lub różnicy względem tła. Adobe opisuje garbage/holdout mattes oraz sekwencję Keylight → Key Cleaner → Advanced Spill Suppressor. [C18] Roto Brush propaguje segmentację, umożliwia poprawkę na pierwszej błędnej klatce i zamrożenie zaakceptowanego zakresu. [C25]

**DERIVED:** Oceniaj osobno pokrycie wnętrza, drobne włosy, półprzezroczyste materiały, motion blur i stabilność w czasie. Jedna binarna maska nie opisze tych wszystkich zjawisk. Despill to korekta koloru zanieczyszczonego ekranem; nie zastępuje poprawy alfa. Nadmierne choke usuwa halo kosztem prawdziwego brzegu.

Test C-KEY-01: podłożyć czarne, białe, nasycone oraz docelowe tło. Obejrzeć krawędzie w ruchu, nie tylko zatrzymany portret. Freeze oznacza utrwalenie wyniku, nie jego akceptację jakościową.

### Alfa, liniowe światło i głębia

**SOURCED:** Straight i premultiplied mogą mieć tę samą alfa, ale inne RGB. Błędna interpretacja tworzy obwódki. [C14] AE rozdziela linearize working space od blend using 1.0 gamma; druga opcja ma węższy zakres. Adobe zaleca ustalenie tego przy tworzeniu projektu. [C12]

**DERIVED — przykład liczbowy:** Czerwony piksel `C=(1,0,0), a=0.25` zapisany jako associated/premultiplied RGB ma `Cp=(0.25,0,0)`. Ponowne mnożenie przez alfa przyciemnia go do `0.0625`. Dla compositingu over w reprezentacji premultiplied: `Cp_out=Cp_fg+(1-a_fg)Cp_bg`, `a_out=a_fg+(1-a_fg)a_bg`. To przykład modelu czarnego tła premultiplikacji; „matted with color” wymaga także znajomości koloru matowania.

Operacje na kolorze wymagają jawnej polityki unpremultiply/premultiply. Dzielenie przez bliskie zero wzmacnia szum; alfa zero wymaga obsługi, a nie „dzielenia z nadzieją”. Testuj miękką krawędź po resize, blur i grade na kilku tłach.

Linear light nie jest synonimem szerszego gamutu ani 32-bit. Rozdziel: primaries/gamut, transfer function, zakres scene/display, view transform, bit depth, alpha association. Dane sterujące, takie jak mapa głębi lub displacement, nie powinny przypadkowo dostać transformacji wyglądu.

**SOURCED:** AE obsługuje 8/16/32 bpc; 32 bpc jest float i pozwala na wartości poza zakresem 0–1. Wyższa precyzja ogranicza błędy pośrednich obliczeń, lecz niski bit depth eksportu nadal może ujawnić banding. [C13]

**DERIVED:** Nie zmieniaj przestrzeni i głębi dopiero po akceptacji glow. Test rampy gradientowej przeprowadź w pliku końcowym, ponieważ podgląd nie jest kodekiem dostawy. Dither może rozbić kontury kwantyzacji; grain jest również decyzją estetyczną i nie powinien być uniwersalnym maskowaniem złego pipeline.

### Motion blur, frame blending i optical flow

**SOURCED:** W AE shutter angle określa czas ekspozycji, phase przesuwa okno próbkowania. Phase równe minus połowie angle centruje blur wokół klatki. Przełącznik motion blur warstwy nie odtwarza automatycznie ruchu wewnątrz nagrania. [C19]

**DERIVED:** Przy FPS=f, angle=θ i phase=φ, okno próbkowania klatki w chwili t można zapisać jako `[t+φ/(360f), t+(φ+θ)/(360f)]`. Hipotetyczne 25 fps, 180°, -90° daje 20 ms ekspozycji, od -10 do +10 ms. Są to obliczone wartości przykładu, a nie norma dla reklamy lub UI.

- Motion blur integruje wygląd ruchu w czasie ekspozycji. Dla scen proceduralnych próbkuj również chwile między klatkami.
- Frame mixing miesza sąsiednie obrazy; może tworzyć podwójne krawędzie.
- Optical flow estymuje przemieszczenia obrazu i używa ich do syntezy lub dalszego przetwarzania. Zasłonięcia, odbicia i cienkie struktury mogą nie mieć jednoznacznej korespondencji.

Test C-BLUR-01: jasny cienki pręt przesuwa się przed ciemnym tłem i zasłania drugi obiekt. Sprawdzić schodkowanie, ciągłość smugi, pozycję centroidu, brzegi maski i pierwszą/ostatnią klatkę. Zwiększenie liczby próbek naprawia niedopróbkowanie; nie naprawia błędnego okna shutter ani niewłaściwego czasu źródła. Podwójny blur — zapisany w assetcie i dodany ponownie — może zniszczyć ostrość.

### Efekt wynika z materiału

**DERIVED:** Displacement wymaga ustalenia kanału, neutralnej wartości, skali w px/jednostkach świata i zachowania poza granicą. Glow powinien wynikać z emisji lub zamierzonej stylizacji; dodanie go do całego obrazu zaciera hierarchię. Particles projektuj jako populację z celem: kierunek, rozkład wieku, gęstość i relacja do bohatera. Przypadkowe konfetti nie jest uniwersalnym product reveal.

Test efektu: porównać wersję bez efektu oraz finalną. Jeśli efekt pogarsza odczyt produktu lub danych, jego koszt nie ma uzasadnienia. Cień, blur i grain należy oceniać w docelowym rozmiarze, także podczas odtwarzania.

## E. Typografia kinetyczna

**SOURCED:** Animatory AE i selektory mogą działać na znaki, znaki bez spacji, słowa albo wiersze. Grouping zmienia punkt odniesienia transformacji. [C09] Kerning reguluje parę znaków, tracking szerszy zakres, leading odległość wierszy. [C26] Tekstowe podsumowanie lekcji Iana Robinsona pokazuje relację Text Animator ↔ Range Selector oraz edycję keyframes presetów. Nie obejrzano osadzonych filmów. [C23]

**SOURCED:** Wskazówki typografii IBM wiążą hierarchię, wyrównanie i długość wiersza z czytelnością. Są zasadami konkretnej identyfikacji; reguły angielskiej interpunkcji nie są automatycznie normą polskiego tekstu. [C31]

**DERIVED:** Zacznij od gotowego statycznego składu. Ustal font, odmianę, interlinię, łamanie, kontrast i długość tekstu. Dopiero potem animuj maskę, transformację lub selektor. Odsłonięcie słowa powinno odpowiadać frazie, nie przypadkowemu indeksowi.

Dla „Zażółć gęślą jaźń — 1 234,50 zł” sprawdź wszystkie glify, znak minus/myślnik, odstępy nierozdzielające oraz kerning. W kodzie nie dziel tekstu naiwnie na jednostki UTF-16; potrzebne są granice grafemów i zachowanie kształtowania tekstu. Font i layout muszą być gotowe przed pomiarem bounding box. Brak fontu ma zatrzymać eksport lub wymagać jawnie zaakceptowanego zamiennika — cichy fallback zmienia szerokość, timing i charakter.

Maskę reveal policz na pełne znaki diakrytyczne, descenders i ewentualny blur. Testuj krótką i najdłuższą dopuszczalną wersję treści. Dla 9:16 projektuj łamanie osobno od 16:9; mechaniczny crop nie jest adaptacją.

Czas czytania licz od momentu stabilnej czytelności, nie od początku wejścia pierwszej litery. Nie ma jednej wartości sekund na każde hasło: uwzględnij długość, nowość pojęć, wielkość, ruch tła i konkurujące VO. Przygotuj próbę jednokrotnego odtworzenia na docelowej wielkości. Duplikowany tekst powinien mieć identyczną treść po eksporcie, a animacja nie może przemienić „nie” w niewidoczny detal.

## Porównanie metod profesjonalnych

To porównanie sposobów reprezentacji pracy; nie ranking szybkości ani kosztu.

| Narzędzie i dowód | Wartość warsztatowa | Adaptacja DERIVED do FrameMotion | Granica / test |
|---|---|---|---|
| After Effects, dokumentacja C01–C19, C25–C26 | Oś czasu warstw, precompy, selektory, krzywe | Osobne relacje: transform, matte, effect chain, compositing group | Nazwa efektu nie dowodzi zgodności pikseli; zestaw fixture'ów |
| Fusion, strona producenta [C24]; poradnik sprawdzony przez specjalistę receptur [R-S11] | Graf połączeń operacji obrazu, compositing i 3D; parametry makr | Jawne porty wejść i zależności, współdzielona maska, kontrola kolejności | Szczegółowy Reference Manual przekroczył limit tego narzędzia; Visual Effects Guide odczytany w pakiecie receptur. Test natywny NOT_RUN |
| Apple Motion, podręcznik [C22]; źródło hosta [H10] | Keyframes służą do precyzyjnych wydarzeń; zachowania do generowania ruchu | Oddziel kanał proceduralny od autorskiej korekty i końcowej wartości | Strona zachowań była lokalnie niedostępna; host odczytał Combining behaviors. Test sumowania NOT_RUN |
| Cinema 4D, dokumentacja C20–C21 | Effectors modyfikują populacje; Fields opisują przestrzenny wpływ | `influence(position,time,id)` steruje instancjami bez kopiowania setek kluczy | Pole może mieć wartości poza 0–1; adapter nie może zawsze clampować |
| Blender, oficjalny raw manual [C32]; cache w źródle specjalisty backendów [B43] | Shutter w jednostkach klatek, pozycja ekspozycji i bake symulacji | Przeliczaj jednostki ekspozycji; osobno przechowuj stan symulacji | Odczytany branch main, commit Unknown. Ograniczenia kamery ortograficznej i ruchu świateł wymagają kontroli wersji oraz testu |

**SOURCED:** W C4D Fields mogą reprezentować przestrzenny rozkład siły, koloru lub kierunku; nie są ograniczone do zakresu 0–1. [C21] Effectors modyfikują pozycję, wielkość i inne cechy instancji oraz mają ograniczenia zależne od rodzaju obiektu. [C20] Fusion opisuje makra z wystawianymi parametrami i węzły łączące operacje. Odczytano deklaracje producenta, bez testu niezależnego. [C24]

**SOURCED:** Odczytany źródłowy podręcznik Cycles podaje shutter w klatkach, sterowanie pozycją ekspozycji oraz zalecenie bake dla fizyki. Wymienia brak camera motion blur dla kamery ortograficznej i nieuwzględnianie ruchu świateł w świecie. To ograniczenia opisanego stanu manuala, nie obietnica wszystkich rendererów Blendera. [C32]

**DERIVED:** Wspólny kontrakt może przechowywać ekspozycję w sekundach albo ułamku okresu klatki, a adapter przeliczać ją na stopnie AE lub klatki Blendera. Przykład: 180° odpowiada 0,5 klatki przy tym samym FPS; nie oznacza to identycznych wag próbkowania, shutter curve ani pikseli.

**DERIVED:** Najważniejsze zapożyczenie z C4D to rozdzielenie „co zmieniam” od „gdzie i jak silnie”. Z Fusion: zależność obrazu jako graf. Z Motion: rozdzielenie proceduralnego zachowania i momentów znaczących. Z AE: czytelna autorska oś czasu. Nie należy budować jednego uniwersalnego tweena i nazywać go wszystkimi czterema systemami.

## Mapa lektury, pokrycie i odbiór

| Pytanie | Przeczytane źródła | Wynik badania | Luka |
|---|---|---|---|
| Jak dobrać charakter ruchu? | C27–C30 | Kontrast charakteru marki i zasad postaci | Brak obejrzanych breakdownów praktyków |
| Dlaczego precomp zmienia obraz? | C01–C02, C05–C08, C16 | Kolejność, granice grupy, przestrzenie i matte | Test na aktualnym AE NOT_RUN |
| Jak naprawić easing? | C03–C04, C10–C11 | Osobno tor, czas, szybkość i pochodne | Nie zmierzono natywnej implementacji krzywych |
| Jak uniknąć halo/bandingu? | C12–C14 | Jawna alfa, przestrzeń i głębia | Plik wyjściowy i monitor niebadane |
| Jak zintegrować element z filmem? | C15, C17–C19, C25 | Kontakt, track, matte, shutter, czas | Brak obejrzanych ujęć testowych |
| Jak zrobić poprawny kinetic type? | C09, C23, C26, C31 | Selekcja, skład, znaczenie, diakrytyka | Font loading w backendach — praca specjalisty kodu |
| Co przenieść z innych narzędzi? | C20–C22, C24, C32; krzyżowo R-S11, B43, H10 | Pola, graf, zachowania, parametry, shutter/cache | Natężenie błędów, wydajność oraz zgodność pikselowa niebadane |

**Proponowany odbiór wiedzy DERIVED:** pięć krótkich scen testowych — krzywe z przejściem przez punkt; precomp z blur i maską; miękkie alfa po resize; tekst polski w dwóch proporcjach; retime z zasłonięciem. Przy każdej wykonawca zapisuje wersję narzędzia, parametry, wejścia i faktycznie obejrzany zakres. Sukces dokumentacji nie jest sukcesem renderu.

**Ograniczenia badania:** badanie obejmuje dokumentację, tekstową lekcję oraz jawnie oznaczoną własną syntezę. Strony marketingowe nie potwierdzają dokładności ani wydajności. Nie sprawdzono licencji assetów kursowych i nie pobierano ich. Nie przyjęto domyślnej zgodności AE z CSS, FFmpeg lub dowolnym GPU. Po osiągnięciu kryteriów sceny kończy się poprawki; nie dodaje się kolejnego efektu dla samego urozmaicenia.

## Dowody uzupełniające innych części DR-01

Nie wlicza się ich ponownie do 32 rekordów C. Ich pełne rejestry należą do autorów odpowiednich części:
- [R-S11] — Damian Allen, Tony Gallardo, Dion Scoppettuolo, *The Visual Effects Guide to DaVinci Resolve 20*, 2025. Specjalista receptur odczytał m.in. drukowane s.87–109 (planar tracking), s.112–123 (keying), s.153–155 (Follower). Szczegóły i receptury znajdują się w jego pakiecie; ten specjalista nie deklaruje osobistego odczytu całego PDF.
- [B43] — oficjalny Blender manual, `physics/simulation_nodes.rst`, odczytany w całości przez specjalistę backendów; sekcje Baking, Calculate to Frame, Cache. Commit Unknown.
- [H10] — Apple, *Combining behaviors in Motion*, odczytane przez hosta; test natywny pozostaje NOT_RUN.

[C01]: https://helpx.adobe.com/after-effects/using/precomposing-nesting-pre-rendering.html
[C02]: https://helpx.adobe.com/after-effects/using/creating-layers.html
[C03]: https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/speed-between-keyframes/speed.html
[C04]: https://helpx.adobe.com/after-effects/using/keyframe-interpolation.html
[C05]: https://helpx.adobe.com/after-effects/using/shape-attributes-paint-operations-path.html
[C06]: https://helpx.adobe.com/after-effects/using/layer-properties.html
[C07]: https://helpx.adobe.com/after-effects/using/alpha-channels-masks-mattes.html
[C08]: https://helpx.adobe.com/after-effects/using/blending-modes-layer-styles.html
[C09]: https://helpx.adobe.com/after-effects/using/animating-text.html
[C10]: https://helpx.adobe.com/after-effects/using/expression-language-reference.html
[C11]: https://helpx.adobe.com/after-effects/using/time-stretching-time-remapping.html
[C12]: https://helpx.adobe.com/after-effects/using/color-management.html
[C13]: https://helpx.adobe.com/after-effects/using/color-basics.html
[C14]: https://helpx.adobe.com/after-effects/using/importing-interpreting-footage-items.html
[C15]: https://helpx.adobe.com/after-effects/using/cameras-lights-points-interest.html
[C16]: https://helpx.adobe.com/after-effects/desktop/work-with-transparency-and-compositing/work-with-track-mattes-and-traveling-mattes/track-mattes-and-traveling-mattes.html
[C17]: https://helpx.adobe.com/after-effects/using/tracking-stabilizing-motion-cs5.html
[C18]: https://helpx.adobe.com/after-effects/using/keying.html
[C19]: https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/assorted-animation-tools/assorted-animation-tools.html
[C20]: https://help.maxon.net/c4d/en-us/Content/html/7443.html
[C21]: https://help.maxon.net/c4d/en-us/Content/html/58091.html
[C22]: https://support.apple.com/en-lamr/guide/motion/motn1474ab82/mac
[C23]: https://www.adobe.com/pl/learn/after-effects/web/creating-animating-text
[C24]: https://www.blackmagicdesign.com/products/fusion
[C25]: https://helpx.adobe.com/after-effects/using/roto-brush-refine-matte.html
[C26]: https://helpx.adobe.com/after-effects/using/formatting-characters-character-panel.html
[C27]: https://www.ibm.com/design/language/animation/classic-principles/
[C28]: https://helpcentre.toonboom.com/hc/en-ca/articles/57087608774931-About-the-12-Principles-of-Animation
[C29]: https://www.ibm.com/design/language/2x-grid/
[C30]: https://www.ibm.com/design/language/animation/tips-and-techniques/
[C31]: https://www.ibm.com/design/language/typography/type-basics/
[C32]: https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/motion_blur.rst

[R-S11]: https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fusion-Visual-Effects.pdf
[B43]: https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/physics/simulation_nodes.rst
[H10]: https://support.apple.com/en-gb/guide/motion/motn13743116/mac

