# DR-06 — karty odcinków

5 kart odcinków code-based, 1 karta porównawcza narzędziowa HyperFrames i 6 kart warsztatu klasycznego. Łączą osobno opis, kod, tekst i próbkowane kadry. Dla każdej karty **NOT_OBSERVED** obejmuje pełny ogląd, odsłuch, miks, działanie lipsyncu, rytm i częstotliwość cięć, szczegółową ciągłość oraz zgodność całej treści z miniaturą. Napisy i kod dostarczają informacji o strukturze, nie o wykonaniu w gotowym renderze. Kadry zarejestrowano na publicznym odtwarzaczu 11 listopada 2026. [Dziennik oględzin](../evidence/VIEWING_LOG.md).

## Kod jako metoda produkcji

### 1. Milo in Space — The Light on the Moon | Explore with Milo

**Dowód.** Player 4:34, 514 publicznych wyświetleń w dniu odczytu. Strona autora opisuje film w całości generowany kodem, 24 fps i 1440p, scene graph i szkielet postaci. Rozwój historii, dobór ujęć i montaż przypisuje człowiekowi. Status **CREATOR_CLAIM**. Kod odcinka pozostaje niedostępny. [Odcinek](https://www.youtube.com/watch?v=OBIBsnzPKZI) · [Opis autora](https://ubedev.com/milo/).

**Obietnica i obraz.** Tytuł zapowiada zagadkę światła na Księżycu. W 00:27 postać odwrócona plecami kieruje uwagę ku Księżycowi. W 04:07 obca złotawa postać w lewym dole i Ziemia w prawym górnym rogu tworzą dwa oddalone punkty uwagi. W 02:17 viewport pokazał niepełny kadr z rakietą i kraterami. Karta pozostawia otwarty przebieg przeszkody i puentę. Twórca deklaruje format bez słów. **NOT_OBSERVED** obejmuje także zakres re-use i sposób ruchu szkieletu.

**Przeniesienie.** Rozdziel stan postaci, pozycję kamery i stan świata. Test w FrameCore może sprawdzać, czy zmiana wysokości obiektu zainteresowania aktualizuje kierunek spojrzenia postaci i zostawia oba obiekty w kadrze.

### 2. Milo and the Umbrella Storm — The Bird Who Couldn't Fly | Explore with Milo

**Dowód.** Player 4:29, 650 publicznych wyświetleń w dniu odczytu. Ta sama autorska deklaracja pipeline'u. Dwie opublikowane historie potwierdzają powracającą postać i odrębne scenariusze. Skala współdzielenia assetów pozostaje **Unknown**. [Odcinek](https://www.youtube.com/watch?v=t2Xq2fpFmwE) · [Opis autora](https://ubedev.com/milo/).

**Obietnica i obraz.** Tytuł łączy konkretną przeszkodę ptaka i burzę. Według twórcy odcinek prowadzą obraz i partytura, bez dialogu. W 02:14 pełna klatka pokazuje czerwono-białą parasolkę, wieżę zegarową i deszcz. W 04:02 przy Milo i ptaku widać złożoną parasolkę, tęczę i miasto w tle. Dwie klatki ujawniają zmianę stanu rekwizytu i pogody. Nie przesądzają, co rozwiązało konflikt. **NOT_OBSERVED** obejmuje także przejścia między stanami, ciężar rekwizytu, ruch ptaka i emocję głosu.

**Przeniesienie.** Zapisuj stan rekwizytu i pogody w danych ujęcia, np. otwarty/złożony oraz deszcz/przejaśnienie. Sprawdzaj, czy zmiana ma opisaną przyczynę w scenariuszu i widoczny skutek w kolejnych klatkach.

### 3. But what is a neural network? | 3Blue1Brown

**Dowód.** Autor udostępnia adaptację lekcji i plik Manim pierwszego rozdziału. Kod animuje reprezentację ręcznie zapisanej cyfry oraz warstwy i aktywacje sieci. Opis publikacji wskazuje rolę samodzielnej lekcji w kursie. **CONFIRMED_WORKFLOW** w zakresie scen Manim, skład pozostałych części **Unknown**. [Odcinek](https://www.youtube.com/watch?v=aircAruvnKk) · [Lekcja](https://www.3blue1brown.com/lessons/neural-networks/) · [Kod scen](https://github.com/3b1b/videos/blob/master/_2017/nn/part1.py).

**Konstrukcja.** Jeden problem, rozpoznanie cyfry, prowadzi od znanego obrazu do abstrakcji. Adaptacja pokazuje, jak opis stopniuje trudność od pojedynczej aktywacji do warstw sieci i przykładu klasyfikacji. Precyzję wyjaśnienia daje ciągłość tych samych pojęć między widokami. Uczenie parametrów przechodzi do kolejnych rozdziałów. W kadrze 09:19 po lewej 784 węzły wejściowe prowadzą do neuronu, po prawej widać pole pikseli i jasny pasek. Odtwarzacz pokazał 18:40. To dowód wybranej kompozycji. Ocena rytmu przekazywania informacji pozostaje **NOT_OBSERVED**.

**Przeniesienie.** Nadaj tym samym obiektom stałe identyfikatory. Scena przejścia od obrazu do wektora powinna odtwarzać tę samą instancję danych przed i po przekształceniu. Test może porównać wartości wyświetlone, tekst mówiony i odpowiadające im akcenty wizualne.

### 4. Simulating Natural Selection | Primer

**Dowód.** W opisie autor wskazuje Blender i Python, a publiczny odtwarzacz pokazał 10:00. W kadrze 05:00 po lewej stoi niebieski stworek, obok znajduje się nagłówek o rozmiarze i wzór kosztu energii w modelu. Odczytane napisy PL pokazują zmianę dostępności pożywienia, zaskoczenie wynikiem i puentę o zależności od środowiska. Karta nie weryfikuje modelu biologicznego. Repozytorium kanału dokumentuje kod animacji i biblioteki sterujące scenami. Powiązanie odcinka z konkretnym plikiem i render pozostają **Unknown**. **CREATOR_CLAIM** na poziomie odcinka i publiczny kod na poziomie kanału. [Odcinek](https://www.youtube.com/watch?v=0ZGbIKd0XrM) · [Repozytorium Primer](https://github.com/Helpsypoo/primerpython).

**Konstrukcja.** Odcinek stawia pytanie, jak zmienia się populacja, kiedy wybór cech zaczyna wynikać z przetrwania. Symulowane stworki są reprezentacją modelu. Widz może rozpoznać stały świat i śledzić zmianę liczebności pod wpływem reguły. Jest to objaśnianie przez eksperyment i skutek, z rolą narratora różną od dialogowej bajki. Wersja interaktywna jest oddzielnym artefaktem. Próba nie ustala, jak różni się od filmu parametrami, seedem ani przebiegiem montażu.

**Przeniesienie.** Zamroź przebieg symulacji do listy zdarzeń z ustalonym seedem. Reżyser wybiera punkty zwrotne z logu i dopiero potem łączy je z narracją. Test może zmienić ustawienie kamery bez zmiany wyniku eksperymentu.

### 5. Benchmark AI chấm thế nào? | Đi Làm IT

**Dowód.** Publiczny upload z 7 listopada 2026, player 5:02, 16 wyświetleń i 13 subskrybentów 11 listopada. Repozytorium łączy dokładny adres pełnego filmu z silnikiem Remotion i osobno wskazuje 80-sekundowy demo render. Autor deklaruje generowanie głosu, synchronizację do słowa oraz własny przegląd przed publikacją. Wymienia użycie nagrań terminala w animowanej tablicy. Kod silnika jest publiczny. Zakres dostępności źródeł finalnego projektu **Unknown**. [Pełny odcinek](https://www.youtube.com/watch?v=OWCMEja1pzo) · [Silnik i odnośniki do odcinków](https://github.com/LocNguyenSGU/whiteboard-explainer-engine).

**Konstrukcja.** Tytuł zestawia dwa wyniki i pyta, jak działa pomiar. Architektura daje realnemu nagraniu rolę źródła, a animowanej tablicy rolę prowadzenia po wyjaśnieniu. Napisy VI prowadzą od pytania o pomiar przez próbę na rzeczywistym zadaniu do powrotu do tego samego przykładu. W 02:31 białe pole pokazuje pasek rozdziałów. W 03:01 robot w ławce, kartka w otwartej szufladzie i nauczyciel obrazują sprawdzian. Pomarańczowy segment paska wskazuje aktywny rozdział. Dwa kadry nie pozwalają ocenić animacji ani tempa przejścia. Nie weryfikowano merytorycznie liczb i porównań benchmarków. Repo pokazuje rodzaj danych wejściowych.

**Przeniesienie.** Rozdziel w schemacie wejścia `visual_action`, `spoken_text` i `source_clip_range`. Po zmianie jednego zdania porównaj przebieg synchronizacji oraz czy zakres nagrania ekranu zachował poprawną długość i przypisanie.

### 6. 19 Claude Code Tips | @cyxj_ai — porównanie techniczne poza próbą główną

**Dowód.** Publiczny README podaje pełną publikację, ok. 7,5 min, 28 kompozycji i lokalizację źródła. Stos HTML + GSAP + HyperFrames jest jawny. W dacie odczytu ten kanał deklaruje przejście na Remotion jako główną metodę i utrzymywanie wcześniejszego archiwum HyperFrames. Rzeczywisty przebieg renderu **NOT_RUN**. [Publikacja](https://www.youtube.com/watch?v=fnKGWHSd0NE) · [README autora](https://raw.githubusercontent.com/chenyuxiaojin/cyxj-hyperframes/main/README.md).

**Konstrukcja.** Tytuł z góry określa modułową formę poradnika. 28 kompozycji przy 19 wskazówkach pokazuje, że jednostka produkcyjna może mieć inną wielkość niż jednostka przekazu. Zakres narracji, tempo poszczególnych porad, kadry, finał i dźwięk **NOT_OBSERVED**. To dowód produkcji pełnego instruktażu i utrzymywania komponentów.

**Przeniesienie.** Przypnij kompozycje do numerów scen zamiast do numeru porady. W teście zamień jedną kompozycję, sprawdź start następnej i wykryj w headless render brak fontu oraz rozjechane napisy.

## Warsztat klasyczny jako odniesienie

### 7. The Amazing Digital Circus — Pilot | GLITCH

**Dowód.** Player 25:45. Trzy kadry i napisy PL do 25:18. W 00:13 Caine zajmuje środek na tle czerwonej kurtyny, rozkłada ręce. W 12:52 otoczenie skalą dominuje Pomni. W 23:10 grupa jest rozłożona między pierwszy plan i głębię. [Pilot](https://www.youtube.com/watch?v=HwAPLk_sQ3w) · [Karta producenta](https://www.glitchprod.com/digital-circus).

**Obietnica i rozwój z napisów.** Gospodarz obiecuje show. Nowa bohaterka wprowadza pilniejszą potrzebę wydostania się. Transkrypcja pokazuje, że lokalna przygoda się domyka, a pytanie o wyjście pozostaje żywe. Obie obietnice działają na innej długości. Napisy końcowe ujawniają odrębne role dialogów, montażu, adiustacji, miksu i głosów polskiej lokalizacji. Wskazówki muzyczne w napisach pozostają wskazówkami tekstowymi.

**Przeniesienie.** Rozpisz lokalny cel i cel całej serii w osobnych polach. Dla dubu trzymaj ID kwestii, tekst, wymowę, mówcę i czas odrębnie od timeline'u obrazu.

### 8. Zabawka | Rodzina Treflików

**Dowód.** Player 8:07, dwa kadry i automatyczne napisy PL. KAZstudio opisuje lalkową animację poklatkową i wiek 3–6 lat. W 04:03 regał sklepu oddziela stojącego Treflika od niżej ustawionej postaci. W 07:18 leśny kadr porządkuje dwie postaci na tle spokojniejszej przestrzeni. [Odcinek](https://www.youtube.com/watch?v=LfHeHMt1Ewg) · [KAZstudio](https://kazstudio.pl/).

**Konstrukcja z napisów.** Piosenka przedstawia stałą obsadę. Lokalna przeszkoda zaczyna się od zniszczonej zabawki i potrzeby zastąpienia jej. W końcowej wymianie pomysł wspólnej zabawy i zwykła kreda rozwiązują praktyczny problem. Piosenka ujmuje finał w prostych rzeczownikach i działaniach. Błędy automatycznych napisów ograniczają pewność szczegółów dialogu.

**Przeniesienie.** Załóż oddzielny slot na stałą identyfikację serii i oddzielny na odcinkowe działanie. Kryterium planszy: dziecko potrafi nazwać przedmiot lub czynność rozwiązującą problem z samej sceny kulminacyjnej.

### 9. Gone to the Dogs | Aardman

**Dowód.** Player 7:00. W 03:30 pokazano pusty nocny plan farmy z budą i stodołą. W 06:18 grupę organizuje centralna pozycja Bitzera z podniesioną dłonią. Aardman opisuje serial jako stop-motion. [Odcinek](https://www.youtube.com/watch?v=orLMm76lwjY) · [Karta serii](https://www.aardman.com/film-tv-games/shaun-the-sheep/).

**Obietnica i stawka.** Opis wiąże kłopot z przyjazdem ojca Bitzera i dezaprobatą wobec sposobu prowadzenia stada. Kadry pokazują kontrast miejsca i relacji grupy, sam rozwój i puenta są **NOT_OBSERVED**. Brak odsłuchu wyklucza ocenę pracy wokalizacji, pauzy, ciszy i ambience.

**Przeniesienie.** W scenorysie gagu wskaż w każdej klatce źródło uwagi i adresata gestu. Test czytelności wykonaj na wyciszonym animatiku i sprawdź u widza, kto działa i czego chce.

### 10. Reksio poliglota | Studio Filmów Rysunkowych

**Dowód.** Player 9:58, opis studia podaje archiwalne 10:22 i rok 1967. W 08:58 płaskie kontury i kolory zwierząt kontrastują z fakturą tła, a postaci zbierają się wokół naczynia. Kadr 04:59 pominięto z powodu obciętego viewportu. [Odcinek](https://www.youtube.com/watch?v=-nnjsnRO8Ww) · [Informacja o oficjalnych publikacjach](https://www.gov.pl/web/bialorus/polskie-bajki-w-sieci).

**Obietnica i narracja.** Opis studia łączy uczenie się języków zwierząt z łagodzeniem sporów. W kadrze wspólny rekwizyt prowadzi wzrok między zróżnicowanymi sylwetkami. Końcowego wyniku konfliktu, znaczenia konkretnych odgłosów, rytmu montażu i ewentualnych powtórzeń nie ustalono.

**Przeniesienie.** Dla sceny bez dialogu zdefiniuj rekwizyt wspólny i kolejność przekazania uwagi jako instrukcje storyboardu. Czytelność grupy da się sprawdzić na małym podglądzie przed animacją.

### 11. Skazani na przypał | SPInka Film Studio

**Dowód.** Player 31:10, automatyczne napisy PL. W 15:35 symetrycznie rozmieszczeni wartownicy obramowują postać w szarym stroju, w tle widać nocną zabudowę. Z jednego kadru można ustalić hierarchię uwagi i karykaturalne proporcje, technika riggingu **Unknown**. [Odcinek](https://www.youtube.com/watch?v=mNCH4J65Jes).

**Konstrukcja z napisów.** Otwiera go rozmowa o strażniczce i reakcje postaci, w finale wraca temat zauroczenia i pojawia się kolejna wariacja żartu. Ten powrót widać w mowie. Błędy ASR utrudniają rekonstrukcję zwrotów i przypisanie wszystkich kwestii. W kadrze 15:35 centralna postać i dwaj wartownicy przedstawiają relację przestrzenną, bez potwierdzenia czasu trwania planu i charakteru gry.

**Przeniesienie.** W wersjach scenariusza przypnij każdą ripostę do poprzedzającej ją kwestii i intencji. Przy wymianie dialogu waliduj powracający żart w ostatniej scenie.

### 12. This Is the Scariest Place in The Universe | Kurzgesagt

**Dowód.** Player 9:13, angielskie napisy i kadr 04:36. Widać sieć jasnych punktów i włókien rozdzielonych rozległą ciemną przestrzenią. Kadr bez legendy nie wyjaśnia, co przedstawia. [Odcinek](https://www.youtube.com/watch?v=yDAAlojz8NU) · [Opis warsztatu kanału](https://kurzgesagt.org/what-we-do?visit=videos).

**Konstrukcja z napisów.** Groza jest wprowadzeniem do pytania o kosmiczne pustki. Narrator wciąga odbiorcę w wyobrażoną podróż, stopniuje skale i kończy konsekwencją dla przyszłości kosmosu. Następnie wraca na Ziemię i przechodzi do promocji. Badanie opisuje strukturę tej wypowiedzi. Twierdzenia naukowe i odczuwany rytm pozostają osobnymi zagadnieniami.

**Przeniesienie.** Wyprowadź sceny skali ze wspólnej tabeli jednostek i progów. Łącz kolejne zmiany skali z pytaniami, które ma wyjaśnić narracja. Oddziel zamknięcie merytoryczne od sekcji promocyjnej.
