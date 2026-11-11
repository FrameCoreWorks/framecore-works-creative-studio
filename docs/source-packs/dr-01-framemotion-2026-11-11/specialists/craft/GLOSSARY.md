# DR-01 — Słownik PL/EN: dokładnie 100 terminów

Data: 2026-11-11. Źródła oznaczono klikalnymi ID zgodnymi z `sources.json`. Krótkie definicje są autorskimi objaśnieniami mechanizmów opisanych w źródłach; przykłady i konsekwencje są **DERIVED**. Dla ogólnych pojęć warsztatowych ID wskazuje kontekst metody, nie normę terminologiczną. Wartości w przykładach są hipotetyczne, nie zalecane dla każdego filmu. Testy produkcyjne nie zostały wykonane (**NOT_RUN**).

| # | Termin PL / EN | Znaczenie robocze | Przykład DERIVED | Konsekwencja produkcyjna DERIVED | Źródła |
|---|---|---|---|---|---|
| 1 | Projektowanie ruchu / Motion design | Organizowanie znaczenia przez zmianę obrazu w czasie. | Linia łączy problem z rozwiązaniem. | Każdy ruch potrzebuje funkcji w przekazie. | [C30] |
| 2 | Inscenizacja / Staging | Ułożenie akcji tak, by była czytelna. | Przed ujawnieniem wyniku wygasają ozdobniki. | Kontrola uwagi poprzedza dodawanie efektów. | [C28] |
| 3 | Hierarchia wizualna / Visual hierarchy | Porządek ważności elementów obrazu. | Cena dominuje, przypis pozostaje wtórny. | Wielkość i timing nie mogą walczyć o pierwszeństwo. | [C31] |
| 4 | Rozkład czasowy / Timing | Momenty i długości znaczących działań. | Wynik pojawia się po zakończeniu porównania. | Przesunięcie klucza może zmienić sens przyczyny. | [C28] |
| 5 | Odstępy ruchu / Spacing | Rozkład pozycji między kolejnymi chwilami. | Bliskie pozycje na starcie, dalsze w środku. | Równa długość scen nie oznacza równego odczucia. | [C03] |
| 6 | Przygotowanie akcji / Anticipation | Zapowiedź działania. | Ikona cofa się przed wybiciem. | Zapowiedź musi zmieścić się przed akcentem. | [C28] |
| 7 | Przekroczenie celu / Overshoot | Ruch poza wartość docelową. | Karta mija końcowe położenie i wraca. | Ustal zakres; liczba na wykresie nie powinna sugerować fałszywego wyniku. | [C30] |
| 8 | Ruch po akcji / Follow-through | Dalsza reakcja części po zatrzymaniu całości. | Etykieta dogina się po zatrzymaniu opakowania. | Koniec głównego ruchu nie kończy całej reakcji. | [C28] |
| 9 | Nakładanie faz / Overlapping action | Części wykonują ruch w różnym rytmie. | Podtytuł podąża za nagłówkiem z opóźnieniem. | Opóźnienie musi zachować czytelność ostatniego elementu. | [C27] |
| 10 | Ściskanie i rozciąganie / Squash and stretch | Deformacja sugerująca elastyczność. | Miękka piłka spłaszcza się przy kontakcie. | Rigid produkt i znak mogą wymagać zakazu deformacji. | [C28] |
| 11 | Łuk / Arc | Zakrzywiony przebieg ruchu. | Uchwyt obraca się wokół zawiasu. | Łuk przestrzenny nie definiuje tempa. | [C28], [C04] |
| 12 | Akcja wspierająca / Secondary action | Dodatkowe działanie wspierające główne. | Drobna ikona potwierdza końcowy stan. | Nie może wyprzedzać uwagą głównego komunikatu. | [C28] |
| 13 | Rytm / Rhythm | Układ akcentów, odstępów i odpoczynku. | Dwa krótkie ruchy i dłuższy hold. | Stałe pulsowanie wszystkich warstw usuwa kontrast. | [C30] |
| 14 | Pauza czytelnicza / Reading hold | Czas stabilnego, możliwego odczytu. | Hasło pozostaje po końcu odsłaniania. | Licz czas po osiągnięciu czytelności. | [C30] |
| 15 | Sylweta / Silhouette | Rozpoznawalny zewnętrzny kształt. | Produkt da się rozpoznać jako czarną bryłę. | Przejścia nie powinny przypadkowo łamać kształtu. | [C30] |
| 16 | Negatywna przestrzeń / Negative space | Celowo wolny obszar kompozycji. | Miejsce na tor wejścia etykiety. | Puste miejsce może zabezpieczać ruch i odczyt. | [C28], [C29] |
| 17 | Siatka / Grid | Relacje wyrównań i odstępów. | Trzy karty kończą na wspólnej osi. | Siatka projektu nie jest globalną safe zone. | [C29] |
| 18 | Pole wpływu / Field | Rozkład wartości sterujących efektem. | Sfera unosi pobliskie instancje. | Przechowuj przestrzeń, kanał i zakres wartości. | [C21] |
| 19 | Efektor / Effector | Operacja zmieniająca cechy populacji. | Każda kopia otrzymuje obrót z pola. | Oddziel zmianę parametru od siły wpływu. | [C20] |
| 20 | Zachowanie / Behavior | Generator przebiegu zamiast samych kluczy. | Obiekt wykonuje ruch proceduralny między akcentami. | Dokładny moment końca może wymagać kluczy lub bake. | [C22] |
| 21 | Kompozycja / Composition | Scena z własnymi warstwami i czasem. | Plansza z produktem i podpisem. | Zapisz rozdzielczość, FPS i czas lokalny. | [C01] |
| 22 | Prekompozycja / Precomposition | Kompozycja użyta jako warstwa w innej. | Logo z maskami tworzy jeden moduł. | Jej granice mogą przyciąć obraz lub zmienić render. | [C01] |
| 23 | Warstwa / Layer | Element sceny z właściwościami. | Zdjęcie, tekst, null lub kamera. | Nie każda warstwa ma widoczne piksele. | [C02] |
| 24 | Stos warstw / Layer stack | Kolejność kompozytowania elementów. | Tekst ponad tłem, korekcja ponad obu. | Kolejność zmienia obraz i zasięg adjustment. | [C02], [C08] |
| 25 | Rodzicielstwo / Parenting | Dziedziczenie transformacji przestrzennych. | Dwie etykiety obracają się wraz z produktem. | W AE nie zakładaj dziedziczenia opacity. | [C06] |
| 26 | Obiekt zerowy / Null object | Niewidoczny kontroler transformacji. | Null steruje kamerą i celownikiem. | Kontroler powinien mieć nazwę funkcji i jednostki. | [C06] |
| 27 | Punkt kotwiczenia / Anchor point | Punkt odniesienia obrotu i skali. | Drzwi obracają się na krawędzi. | Zmiana pivota po animacji może przesunąć obiekt. | [C06] |
| 28 | Przestrzeń współrzędnych / Coordinate space | Układ odniesienia pozycji. | Punkt logo przeliczony do kompozycji. | Nie sumuj pozycji z różnych przestrzeni. | [C10] |
| 29 | Transformacja / Transform | Przesunięcie, obrót, skala i powiązane parametry. | Karta rośnie względem dolnego narożnika. | Kolejność mnożenia transformacji ma znaczenie. | [C06] |
| 30 | Scalanie transformacji / Collapse transformations | Zmiana granicy przetwarzania zagnieżdżenia. | Precomp zachowuje relacje 3D z otoczeniem. | Wymaga testu masek, efektów i przycięcia. | [C01] |
| 31 | Ciągła rasteryzacja / Continuous rasterization | Rasteryzowanie wektora według aktualnego przekształcenia. | Logo pozostaje ostre po powiększeniu. | Może zmienić kolejność względem efektów. | [C01] |
| 32 | Grafika wektorowa / Vector graphics | Obraz oparty na kształtach i ścieżkach. | Kontur znaku skalowany do dużej planszy. | Przed eksportem nadal powstaje raster. | [C05] |
| 33 | Raster / Raster image | Obraz z próbkowanych pikseli. | Fotografia produktu w PNG. | Powiększenie nie tworzy brakujących szczegółów. | [C14] |
| 34 | Warstwa kształtu / Shape layer | Warstwa z geometrią i operatorami. | Okrąg z obrysem i Repeaterem. | Grupowanie decyduje o zasięgu operatorów. | [C05] |
| 35 | Ścieżka / Path | Przebieg geometrii lub ruchu. | Kontur służy jako maska. | Te same punkty mogą mieć inne jednostki i zastosowanie. | [C05], [C07] |
| 36 | Krzywa Béziera / Bézier curve | Krzywa kontrolowana punktami i uchwytami. | Łagodny zakręt ruchu kamery. | Kształt toru nie gwarantuje płynnej prędkości. | [C04] |
| 37 | Przycinanie ścieżki / Trim Paths | Ograniczenie widocznego odcinka ścieżki. | Linia wykresu rysuje się od lewej. | Kierunek ścieżki wpływa na kolejność odsłonięcia. | [C05] |
| 38 | Powielacz / Repeater | Kopie z kolejnymi transformacjami. | Kreski tarczy rozmieszczone po okręgu. | Zmiana wzorca wpływa na całą serię. | [C05] |
| 39 | Łączenie ścieżek / Merge Paths | Operacja na zestawie kształtów. | Otwór wycięty z prostokąta. | Sprawdź kolejność, kierunki i fill rule. | [C05] |
| 40 | Wypełnienie / Fill | Kolor wnętrza kształtu. | Pełny czerwony prostokąt. | Rozróżnij krycie fill od krycia całej warstwy. | [C05] |
| 41 | Obrys / Stroke | Pas wzdłuż ścieżki. | Kontur przycisku rośnie z zera. | Skala i rasteryzacja wpływają na postrzeganą grubość. | [C05] |
| 42 | Maska / Mask | Ścieżka ograniczająca działanie lub widoczność. | Prostokąt odsłania nagłówek. | Jej przestrzeń może podążać za warstwą. | [C07] |
| 43 | Mapa krycia / Matte | Obraz opisujący pokrycie. | Osobny render sylwety produktu. | Oceniaj matte także bez RGB. | [C07] |
| 44 | Maska alfa / Alpha matte | Pokrycie pobierane z kanału alfa. | Tekst wycina wideo swoim kształtem. | Kolor tekstu nie powinien sam zmieniać pokrycia. | [C16] |
| 45 | Maska luminancji / Luma matte | Pokrycie pobierane z jasności. | Szary gradient odsłania zdjęcie. | Jawnie zapisz inversion i domenę koloru. | [C16] |
| 46 | Zmiękczenie maski / Mask feather | Stopniowe przejście na brzegu. | Miękkie odsłonięcie fragmentu tła. | Miękki brzeg potrzebuje miejsca poza granicą kadru. | [C07] |
| 47 | Warstwa korekcyjna / Adjustment layer | Efekt na złożeniu warstw pod nią. | Jeden grade na planszy. | Efekt na sumie nie równa się sumie efektów. | [C02] |
| 48 | Tryb mieszania / Blend mode | Reguła łączenia kanałów obrazu. | Świetlny element używa trybu addytywnego. | Wynik zależy także od alfa i przestrzeni. | [C08] |
| 49 | Klatka kluczowa / Keyframe | Zadana wartość w określonym czasie. | Pozycja końcowa na wskazanej klatce. | Klucz jest warunkiem; ruch pomiędzy trzeba zaprojektować. | [C04] |
| 50 | Interpolacja czasowa / Temporal interpolation | Wyznaczanie wartości pomiędzy chwilami. | Krycie rośnie łagodnie. | Osobno kontroluj wejście i wyjście klucza. | [C04] |
| 51 | Interpolacja przestrzenna / Spatial interpolation | Wyznaczanie toru pomiędzy pozycjami. | Karta omija przeszkodę łukiem. | Linear timing może biec po krzywym torze. | [C04] |
| 52 | Wykres wartości / Value graph | Wartość parametru jako funkcja czasu. | Wysokość piłki maleje do podłoża. | Nachylenie ma inne znaczenie niż wysokość wykresu. | [C04] |
| 53 | Wykres szybkości / Speed graph | Tempo zmiany parametru w czasie. | Pojedynczy szczyt tempa przy wejściu. | Nie odczytuj go jako współrzędnej obiektu. | [C03] |
| 54 | Styczna / Tangent | Kierunek lokalnego przebiegu krzywej. | Uchwyty wyrównują wejście i wyjście. | Dopasuj też długość i znaczenie jednostek. | [C04] |
| 55 | Wpływ uchwytu / Influence | Zakres oddziaływania uchwytu na przebieg. | Długie wygaszenie przed zatrzymaniem. | Influence nie jest samą wartością speed. | [C03] |
| 56 | Łagodzenie / Easing | Kształtowanie przyspieszania i hamowania. | Panel szybko rusza i spokojnie siada. | Ease na każdym kluczu może dodać zbędne postoje. | [C03] |
| 57 | Interpolacja skokowa / Hold interpolation | Wartość trwa aż do następnego klucza. | Stan etykiety przełącza się bez przejścia. | Użyj do dyskretnego stanu, nie niechcący do ruchu. | [C04] |
| 58 | Klucz wędrujący / Roving keyframe | Czas pośredniego klucza dopasowuje przebieg ruchu. | Tor ma ustalone punkty i płynne tempo. | Nie przypinaj nim krytycznego akcentu audio. | [C03] |
| 59 | Prędkość wektorowa / Velocity | Zmiana pozycji z kierunkiem. | Ten sam moduł, inny kierunek przed odbiciem. | Szybkość skalarna nie opisuje całej ciągłości. | [C03], [C04] |
| 60 | Przyspieszenie / Acceleration | Zmiana prędkości w czasie. | Wózek nabiera tempa po starcie. | Badaj zmiany tempa, nie tylko końcowe pozycje. | [C03] |
| 61 | Wyrażenie / Expression | Reguła wyliczająca parametr. | Etykieta śledzi punkt produktu. | Zależności i błędy muszą być widoczne. | [C10] |
| 62 | Ograniczenie / Constraint | Relacja utrzymywana między elementami. | Kamera stale celuje w produkt. | Zdefiniuj zachowanie w położeniach osobliwych. | [C10], [C15] |
| 63 | Pętla / Loop | Powtarzalny przebieg w czasie. | Znacznik krąży po zamkniętej trasie. | Na szwie sprawdź wartość i prędkość. | [C30] |
| 64 | Przesunięcie grupowe / Stagger | Systematyczne opóźnienie części grupy. | Słowa wchodzą kolejno. | Długi tekst nie może wydłużyć sceny bez zgody. | [C09], [C30] |
| 65 | Szum proceduralny / Procedural noise | Generowana nieregularna zmiana. | Drobne odchylenie papierowej tekstury. | Ogranicz pasmo i amplitudę, by uniknąć migotania. | [C10] |
| 66 | Ziarno losowości / Random seed | Parametr ustalający losową sekwencję. | Ten sam układ drobin w preview i eksporcie. | Zapis seed nie naprawi zależności od kolejności klatek. | [C10] |
| 67 | Zmiana czasu / Retiming | Przypisanie innego tempa źródłu. | Fragment stopniowo zwalnia przed wynikiem. | Akcenty wymagają ponownego sprawdzenia. | [C11] |
| 68 | Czas źródłowy / Source time | Chwila odczytywana z materiału. | Klatka źródła pojawia się później na osi filmu. | Nie utożsamiaj z czasem nadrzędnej osi. | [C11] |
| 69 | Liczba klatek na sekundę / Frame rate | Częstotliwość próbkowania obrazu. | Sekunda materiału ma 25 klatek. | Conform może zmienić długość i synchronizację. | [C14] |
| 70 | Kamera / Camera | Model projekcji widoku sceny. | Wirtualny ruch odsłania boczny plan. | Zapisz projekcję i parametry, nie sam transform. | [C15] |
| 71 | Perspektywa / Perspective | Relacja projekcji zależna od odległości. | Dalsza karta wydaje się mniejsza. | Zdjęcie produktu musi pasować do punktu widzenia. | [C15] |
| 72 | Paralaksa / Parallax | Różny ruch planów przy zmianie widoku. | Bliskie liście przesuwają się szybciej. | Duży ruch ujawnia luki po wycięciu tła. | [C15] |
| 73 | Głębia ostrości / Depth of field | Zakres odległości odbieranych jako ostre. | Produkt ostry, dalszy podpis rozmyty. | Zbyt mała głębia może uniemożliwić odczyt. | [C15] |
| 74 | Śledzenie ruchu / Motion tracking | Estymowanie ruchu cechy obrazu. | Etykieta trzyma się obiektu w kadrze. | Oceniaj cały przebieg, nie tylko średni błąd. | [C17] |
| 75 | Śledzenie płaszczyzny / Planar tracking | Estymowanie ruchu obszaru płaskiej powierzchni. | Grafika przyklejona do ekranu telefonu. | Zasłonięcie i deformacja nadal wymagają kontroli. | [C17] |
| 76 | Kluczowanie / Keying | Wyznaczanie pokrycia z cech obrazu. | Zielone tło staje się transparentne. | Kompresja i podobny kolor obiektu ograniczają wynik. | [C18] |
| 77 | Zafarbowanie tłem / Spill | Kolor tła odbity na obiekcie. | Zielona krawędź na jasnych włosach. | Despill nie zastępuje poprawnej alfa. | [C18] |
| 78 | Rotoskopia / Rotoscoping | Izolowanie obiektu w kolejnych chwilach. | Korekty maski dłoni przy zasłonięciu. | Zamrożenie wyniku wymaga wcześniejszej kontroli czasu. | [C25] |
| 79 | Kanał alfa / Alpha channel | Dane pokrycia lub przezroczystości. | Półprzezroczysty brzeg produktu. | Sam czarny RGB nie oznacza przezroczystości. | [C07] |
| 80 | Alfa prosta / Straight alpha | RGB niepomnożone przez pokrycie. | Czerwony brzeg zachowuje pełną czerwień w RGB. | Import musi znać reprezentację. | [C14] |
| 81 | Alfa skojarzona / Premultiplied alpha | RGB powiązane mnożeniem z alfa. | Brzeg o alfa 0,25 ma osłabione RGB. | Podwójna premultiplikacja daje ciemne obrzeże. | [C14] |
| 82 | Liniowe światło / Linear light | Liczby proporcjonalne do ilości światła. | Mieszanie jasnego brzegu przed transferem ekranu. | Nie utożsamiaj linear z 32 bpc. | [C12] |
| 83 | Przestrzeń barwna / Color space | Określenie znaczenia wartości koloru. | Asset sRGB trafia do jawnej przestrzeni pracy. | Bez profilu identyczne RGB może wyglądać inaczej. | [C12] |
| 84 | Głębia kanału / Bit depth | Precyzja reprezentacji kanału. | Obliczenia w 32-bpc float. | Sprawdź zgodność efektów i głębię eksportu. | [C13] |
| 85 | Pasmowanie / Banding | Widoczne stopnie zamiast gładkiej gradacji. | Ciemny gradient tworzy pierścienie. | Kontrola musi obejmować kodek dostawy. | [C13] |
| 86 | Aliasing / Aliasing | Fałszywy wzór powstały z niedopróbkowania. | Cienka ukośna kreska migocze. | Większy blur nie zawsze jest właściwym lekarstwem. | [C12], [C19] |
| 87 | Rozmycie ruchu / Motion blur | Uśrednienie wyglądu w czasie ekspozycji. | Smuga szybko przemieszczanego pręta. | Próbkuj też czasy między klatkami. | [C19], [C32] |
| 88 | Kąt migawki / Shutter angle | Ekspozycja jako część okresu klatki. | 180° oznacza pół okresu klatki. | Przy innym FPS zmieni się czas w sekundach. | [C19] |
| 89 | Faza migawki / Shutter phase | Przesunięcie okna ekspozycji. | -90° przy 180° centruje smugę. | Zły offset może wyglądać jak opóźniony tracking. | [C19] |
| 90 | Mieszanie klatek / Frame blending | Tworzenie przejściowych obrazów przy retime. | Frame Mix miesza sąsiednie ujęcia. | Kontroluj podwójne krawędzie. | [C11] |
| 91 | Przepływ optyczny / Optical flow | Estymacja ruchu między obrazami. | Wektory pomagają utworzyć brakującą chwilę. | Zasłonięcia mogą dawać artefakty syntezy. | [C24], [C11] |
| 92 | Przemieszczenie mapą / Displacement | Zmiana położenia sterowana danymi obrazu. | Mapa porusza teksturę wody. | Dane sterujące wymagają jawnej polityki koloru. | [C12] |
| 93 | Poświata / Glow | Rozprzestrzenienie jasnego efektu wokół źródła. | Emitująca kreska oświetla sąsiedztwo. | Głębia i zakres jasności zmieniają rezultat. | [C13] |
| 94 | Ziarno obrazu / Grain | Drobna struktura obrazu przypominająca ziarno. | Render otrzymuje teksturę dopasowaną do ujęcia. | Nie myl z ditheringiem i błędami kompresji. | [C18] |
| 95 | Układ cząstek / Particle system | Populacja elementów zmieniająca się w czasie. | Drobiny lecą w jednym strumieniu. | Symulacja może wymagać bake przed blur/renderem. | [C24], [C32] |
| 96 | Typografia kinetyczna / Kinetic typography | Tekst, którego ruch współtworzy przekaz. | Słowo „razem” scala oddzielne grupy. | Animacja ma wspierać znaczenie i odczyt. | [C09], [C30] |
| 97 | Selektor tekstu / Text selector | Zakres elementów objętych animatorem. | Zaznaczenie biegnie słowo po słowie. | Wybór znaków ze spacjami zmienia rytm. | [C09], [C23] |
| 98 | Korekta pary liter / Kerning | Odstęp konkretnej pary znaków. | Para „AV” otrzymuje korektę. | Nie zastępuj korekt par globalnym trackingiem. | [C26] |
| 99 | Rozstrzelenie tekstu / Tracking | Odstępy w całym wybranym zakresie. | Nagłówek delikatnie rozszerza się. | Zmiana szerokości może złamać wiersz. | [C26], [C31] |
| 100 | Interlinia / Leading | Odstęp pomiędzy wierszami. | Dwa wiersze hasła mają czytelny oddech. | Maska musi uwzględnić cały blok i diakrytykę. | [C26], [C31] |

Nie utożsamiaj: tracking ruchu (#74) i tracking tekstu (#99); hold czytelniczego (#14) z interpolacją Hold (#57); motion blur (#87) z frame blending (#90); alpha matte (#44) z luma matte (#45); value graph (#52) ze speed graph (#53).

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

