# Udokumentowane przypadki produkcji animacji

Odczyt źródeł 11 listopada 2026. Główna część omawia odcinki z animacją sterowaną kodem, a dalsza część dokumentuje warsztat porównawczy. Daty przy tytułach dotyczą materiałów o produkcji. Identyfikatory źródeł prowadzą do [rejestru](sources.json). Przypadki dobrano pod kątem dostępności materiałów roboczych i różnic techniki. Próba nie pozwala oszacować udziału metod wśród kanałów.

- **CONFIRMED_WORKFLOW** — projekt, kod, dokumentacja produkcyjna lub credits potwierdzają konkretną operację, zakres bądź rolę. Na przykład credits potwierdzają funkcję osoby, a opis struktury opublikowanych ujęć potwierdza sposób przekazywania danych w tych ujęciach.
- **CREATOR_CLAIM** — relacja twórcy lub producenta dotycząca własnego procesu. Wywiad wykorzystano w zakresie wypowiedzi rozmówcy.
- **INFERRED_FROM_VIDEO** — wniosek na podstawie rzeczywistego oglądu ze wskazaniem materiału i zakresu. W tej części badania nie użyto tej kategorii.
- **Unknown** — materiał nie ustala danej informacji. Tekst strony, tytuł filmu i zdjęcie robocze nie ustanawiają pomiaru montażu, odsłuchu, sposobu przygotowania całej serii ani użycia AI.

## Publikacje i przykłady z produkcją sterowaną kodem

Oznaczenie metody dotyczy tego, co powstaje z kodu, a oznaczenie dowodu określa, skąd to wiadomo.

- **CODE_RENDERED** — kod bezpośrednio buduje lub animuje deklarowaną warstwę pikseli, np. sceny matematyczne, postacie wektorowe albo ujęcia 3D. Zakres może obejmować część obrazu albo całość odcinka.
- **CODE_ASSISTED** — kod zasila część procesu, np. symulację, efekt, dane lub montaż. Dostępny materiał nie ustala renderowania całego odcinka przez kod.
- **GENERATIVE** — model generuje elementy obrazu lub dźwięku użyte w finalnym materiale, jeżeli jest na to dowód. Pomoc AI w pisaniu skryptu z deterministycznym wykonaniem należy do procesu kodowego.
- **Unknown** — zakres i metoda nieustalone.

| Publikacja | Dowód produkcji i zakres | Mechanizm do zastosowania |
|---|---|---|
| **Milo**, familijny format fabularny bez dialogu. [Milo in Space](https://www.youtube.com/watch?v=OBIBsnzPKZI), 4:35 i [Milo and the Umbrella Storm](https://www.youtube.com/watch?v=t2Xq2fpFmwE), 4:30 według autora. | **CREATOR_CLAIM / CODE_RENDERED, deklarowany pełny obraz.** UBE Dev opisuje postać zbudowaną programowo, opis scen, wspólny renderer, ruch jako timing i easing oraz master 1440p, 24 fps. Studio deklaruje też kod muzyki, miniaturek i Shorts. AI pomaga pisać kod, a sceny i cięcia określają twórcy. Strona oznacza dwa pełne filmy jako opublikowane, pozostałe jako zaplanowane. Odczyt web stron odcinków się nie powiódł. Publiczny oEmbed potwierdził tytuły i autora obu odcinków. W tym badaniu produkcji nie ustalono metryk ani niezależnego oglądu. Publicznego kodu nie znaleziono. [C01, strona i indeks twórcy](https://ubedev.com/milo/), [V01, metadane pierwszego filmu](https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DOBIBsnzPKZI&format=json), [V02, metadane drugiego filmu](https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dt2Xq2fpFmwE&format=json) | Jedno źródło proporcji bohatera i lokacji. Parametry ruchu plus ręczne decyzje dramaturgiczne. Dźwięk i reakcje muszą nieść przebieg historii przy braku dialogu. |
| **3Blue1Brown**, pełny explainer [The essence of calculus](https://www.youtube.com/watch?v=WUvTyaaNkzM). | **CONFIRMED_WORKFLOW / CODE_RENDERED, warstwa animacji.** Strona lekcji i repozytorium wiążą cykl z kodem Manim; plik `_2017/eoc/chapter1.py` istnieje w repo. W starszych projektach autor wskazuje zależność od historycznych wersji. Nie ustalono całej ścieżki dźwięku i masteringu. [C08, lekcja](https://www.3blue1brown.com/lessons/essence-of-calculus/), [P07, repo scen](https://github.com/3b1b/videos) | Rozkładać objaśnienie na kolejne sprawdzalne stany tego samego obiektu. Przypiąć renderer i wersję kontraktu sceny. |
| **Reducible**, pełny explainer [A Strange But Elegant Approach to a Surprisingly Hard Problem (GJK Algorithm)](https://www.youtube.com/watch?v=ajv46BSqcK4). | **CONFIRMED_WORKFLOW / CODE_RENDERED, warstwa animacji.** README wskazuje `2021/GJK/gjk.py` jako kod animacji do filmu GJK, zależność Shapely i wykorzystanie oryginalnego Manim, a w nowszych materiałach Manim Community. Publiczny oEmbed potwierdził tytuł i autora. [C02, repo kanału](https://github.com/nipunramk/Reducible), [V03, metadane filmu](https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dajv46BSqcK4&format=json) | Odseparować bibliotekę geometrii od narracji. Testować algorytm i wizualną kolejność objaśnień osobno. |
| **Primer**, pełne explainery z symulacją, np. [Simulating Natural Selection](https://www.youtube.com/watch?v=0ZGbIKd0XrM). | **CONFIRMED_WORKFLOW / CODE_RENDERED dla wizualizacji w archiwalnym procesie, zakres konkretnego mastera Unknown.** Archiwalne repo Primer opisuje Blender Python, `draw_scenes.py`, obiekty `Bobject` i keyframes. Publiczny fork PrimerUnity opisuje C# i sceny Unity do wizualizacji i symulacji Primer. Brak zweryfikowanego przejścia między wersjami i przypisania commitu do wskazanego odcinka. [C03, archiwum Blender Python](https://github.com/Helpsypoo/primerpython), [C04, fork PrimerUnity](https://github.com/gg-big-org/PrimerTools) | Oddzielić stan symulacji od reprezentacji. Utrwalić seed, parametry i snapshot wejścia. Wybrać instancję wyjaśniającą regułę i wyjaśnić jej zakres w narracji. |
| **Sebastian Lague**, [Coding Adventure: Clouds](https://www.youtube.com/watch?v=4QOcCGI6xOU), odcinek o budowie systemu chmur. | **CONFIRMED_WORKFLOW / CODE_ASSISTED, kod fragmentu obrazowego.** Repo autora linkuje ten film i zawiera projekt chmur raymarching w Unity. Nie ustala, jak powstał pozostały materiał filmu. [C07, Clouds](https://github.com/SebLague/Clouds) | Traktować generowanie świata lub efektu jako powtarzalny komponent przypięty do wejść, z osobnym scenariuszem, kamerą i montażem. |
| **ESCAPEMENT**, opublikowana próbka 36,5 s na GitHubie. | **CONFIRMED_WORKFLOW / CODE_RENDERED, krótki film techniczny poza próbą odcinków YouTube.** Repo pokazuje brief, shotlist, biblioteki, skrypty ujęć i montażu. Opis autora przypisuje obiekty, światła, kamerę i animację Blender Python, conform i mix skryptom oraz FFmpeg. Wydanie wskazuje master i zewnętrzne źródła muzyki/Foley. Autor opisuje wycięcie ujęć i ograniczenie równoległych renderów po problemach GPU. [C05, projekt](https://github.com/Leonxlnx/escapement), [C11, wydanie](https://github.com/Leonxlnx/escapement/releases/tag/v1.0) | Oddzielić kolejkę CPU i GPU, testować klatki ryzyka przed całym ujęciem, zapisać decyzje o zmianie planu renderu i cue na wspólnej siatce. Obecność kodu nie daje pomiaru odporności ani dowodu na serię z dialogiem. |
| **NODO 404**, [34-sekundowa pionowa pętla](https://youtube.com/shorts/0enpupe-v6Y). | **CONFIRMED_WORKFLOW / CODE_RENDERED, próbka techniczna wyłączona z próby pełnych odcinków.** Publiczne repo opisuje sześć JSON-ów ujęć, Blender Python, lokalny compositing i syntetyzowany dźwięk. Odtwarzalność deklaruje autor. [C06, kod](https://github.com/kvothesson/procedural-anime) | Warianty postprocessu zależne od numeru klatki, plik ujęcia jako wejście, przejście między trybem szkicu i finalnym bez przepisywania sceny. |
| **Freya Holmér**, [The Continuity of Splines](https://www.youtube.com/watch?v=jvPPXbo87ds), oraz **CodeParade**, 4D Golf Devlog. | **Unknown** w zakresie finalnego renderowania odcinków. W tej próbie nie znaleziono otwartego projektu łączącego dane ujęcia, kod i obraz danego filmu. Narzędzie powiązane tematycznie lub repo gry może tłumaczyć działanie obiektu, ale samo nie potwierdza pipeline’u publikacji. | Mogą inspirować komunikację geometrii i narrację o tworzeniu systemu. Bez podnoszenia do dowodu produkcyjnego. |

Dwa pełne filmy Milo są najbliższym znalezionym przykładem fabularnym. Źródło potwierdza, co deklaruje twórca, a publiczny kod pozostał nieustalony. Przykłady edukacyjne dają silniejszy materiał roboczy. W tej próbie brak publicznego repo i pełnego odcinka seryjnej bajki z dwoma mówiącymi postaciami, które łącznie dowodzą renderowania postaci, lip-sync, zmiany kwestii po animacji i stabilnej powtarzalności odcinków. Próbki ESCAPEMENT i NODO 404 wypełniają lukę techniczną częściowo, na krótkiej skali.

## Warsztat porównawczy

Poniższe karty dotyczą podejść tradycyjnych i hybryd. W większości zakres roli kodu w opublikowanym obrazie pozostaje **Unknown**. Sprite Fright potwierdza **CODE_ASSISTED** w pracy z ujęciami, plikami i zależnościami. Karta 3Blue1Brown rozwija skrócony przykład kodowy z tabeli.

## 1. Kurzgesagt – In a Nutshell

**CREATOR_CLAIM.** Na stronie pracownia opisuje kolejność od lektury źródeł pierwotnych i konsultacji, przez arkusz źródeł, wiele redakcji scenariusza i szkice metafor, po ilustrację. Narracja Steve’a ustala czas dla animatorów. Studio deklaruje połączenie płaskiej animacji 2D z elementami 3D i osobno komponowaną muzykę Epic Mountain. To deklarowany proces zespołu łączącego research, ilustrację, animację, głos i dźwięk. [P01, Our video process](https://kurzgesagt.org/what-we-do?visit=videos)

**Przeniesienie.** Powiązać twierdzenie, dokładny tekst narracji i metaforę wizualną jednym identyfikatorem segmentu. Dla zmiany merytorycznej zidentyfikować dotknięty fragment VO, ilustrację i napisy. **Unknown:** aplikacje i wersje na konkretnym odcinku, udział re-use, liczba roboczogodzin, przebieg rund montażu.

## 2. The Amazing Digital Circus — GLITCH Productions

**CREATOR_CLAIM.** Kevin Temmer, lead animator, opisuje w wywiadzie z 24.10.2024 animowanie w Maya, przenoszenie ujęć przez samych animatorów do Unreal Engine 5 i powrót do Maya po ocenie w oświetleniu. Storyboard jest odniesieniem dla pozy i ekspresji. Rozwinięcie postaci Gangle przewidziano już na etapie riga. Temmer podaje przykłady przeskalowania dłoni pod kamerę, zapożyczonych elementów twarzy w zwiastunie i rozciągnięcia kończyn na potrzeby smear frames. Wskazuje wpływ podobnych zmian na światło i symulację. [P02, rozmowa z Kevinem Temmerem](https://80.lv/articles/we-spoke-to-the-amazing-digital-circus-lead-animator-about-cheating-in-3d-animation)

**Przeniesienie.** Zdefiniować zakres riga na podstawie trudnej akcji ze storyboardu. Korekty bryły pod konkretną kamerę trzymać w pliku ujęcia. Oceniać je w roboczym świetle i po compositingu. Zespół ma odrębne kompetencje riggingu, storyboardu i animacji. **Unknown:** pełny zestaw narzędzi, koszt odcinka, nagrania i lipsync, polityka render farmy, workflow najnowszych odcinków.

## 3. Simon’s Cat — Cat Man Do i wczesna seria

**CREATOR_CLAIM.** W wywiadzie z 15.11.2011 Simon Tofield opisuje pierwszy film jako projekt poboczny do nauki Flash. We wczesnym procesie sam nagrywał odgłosy zwierząt, a Russell Pay przygotowywał Foley i efekty. Tofield opisuje serię bez dialogów, opartą na zachowaniu i mowie ciała. Podaje 6–7 tygodni animacji i kolejny tydzień dźwięku jako ówczesną przybliżoną średnią z rozrzutem zależnym od długości. Ta relacja dotyczy etapu, na którym niezależny twórca współpracował z dźwiękowcem. [P03, wywiad z Simonem Tofieldem](https://www.skwigly.co.uk/simon-tofield/)

**Przeniesienie.** Przetestować beat w szkicu bez dialogu, potem doprecyzować spojrzenie, reakcję i pojedynczy efekt synchroniczny. Oddzielić odgłos bohatera od dźwięku przedmiotów. **Unknown:** wersja oprogramowania, liczba rysunków, obecne narzędzia i skala zespołu, sposób montażu i korekt w nowszej produkcji.

## 4. Alan Becker — Animator vs. Animation IV

**CREATOR_CLAIM.** W rozmowie z 18.12.2014 Becker rozróżnia część rozgrywającą się w płaskim interfejsie, dla której przygotował przebieg historii, od części live action, dla której robił storyboard. Opisuje usunięcie dwóch scen z gagami, które nie popychały fabuły, oraz pomoc drugiej osoby przy wybranych ujęciach live action. Wczesny przypadek autorski z konkretnym wsparciem na planie. [P04, rozmowa z Alanem Beckerem](https://shots.net/news/view/alan-becker-gives-us-the-chosen-one)

**Przeniesienie.** Dla scen ograniczonych interfejsem zapisać stan ekranu, strefy działania i zdarzenia z timingiem. W kadrach wymagających pracy kamery i połączenia z animacją przygotować storyboard i plan nakładek. **Unknown:** technika konkretnych klatek IV, komplet zasobów i dźwięku, pipeline współczesnych odcinków Animation vs. Minecraft. Link do twórcy sprzedającego plik AVM i wynik wyszukiwania making-of pozostały na poziomie search-only w tej próbie.

## 5. Rodzina Treflików — KAZstudio, Polska

**CREATOR_CLAIM.** Strona marki identyfikuje technikę jako fizyczne stop-motion i opisuje fotografowanie zmian mimiki, pozy oraz scenografii. Podaje zastosowanie druku 3D do sylwetek i scenografii, obsadę głosową oraz format odcinka z dwiema piosenkami. Strona opisuje ok. ośmiominutową formę i pełne odcinki dostępne na YouTube. Zasoby produkcji obejmują fizyczne lalki, rekwizyty i gotowe plany. Podane liczby pochodzą z opisu historycznego producenta i mają różne zakresy niż bieżące podsumowanie studia. [P05, technika, obsada i muzyka](https://thetreflikfamily.com/o-serialach/rodzina-treflikow/)

**Przeniesienie.** W wersji cyfrowej prowadzić odpowiednik katalogu lalek i planów, z indeksowanymi twarzami, rękami, rekwizytami i dopuszczalnymi ustawieniami. Dla piosenki zablokować tempo i akcenty przed animacją. **Unknown:** harmonogram przed/po nagraniu aktorów, sprzęt zdjęciowy, liczba klatek z unikalną pozą, koszt pracy i obecna skala dla pojedynczego odcinka.

## 6. Bobaski i Miś — KAZstudio, Polska

**CREATOR_CLAIM.** Strona serii kieruje do odcinków na YouTube, deklaruje odbiorców 2+, około trzyminutowe odcinki i decyzję o zastąpieniu dialogów odgłosami przedmiotów i delikatną muzyką. To drugi format tego samego studia, porównywalny z Treflikami pod kątem projektu komunikacji, z odrębnymi bohaterami i regułami dźwięku. [P06, MiniSERIAL dla maluchów](https://thetreflikfamily.com/o-serialach/bobaski-i-mis/)

**Przeniesienie.** Ułożyć akcję wokół jednego rekwizytu i dać osobne znaczniki dla zauważenia, próby i rezultatu. Przy odbiorze animaticu sprawdzić, czy odgłos wskazuje właściwy przedmiot i jest zrozumiały z gestem. **Unknown:** harmonogram Foley i muzyki, biblioteka cykli i plany zdjęciowe. Trzyminutowa forma i wiek są opisem wydawcy, więc nie stanowią danych o skutkach zdrowotnych ani ogólnej granicy długości.

## 7. 3Blue1Brown — kod scen matematycznych

**CONFIRMED_WORKFLOW.** Repozytorium autora gromadzi kod scen, które generują animacje do filmów 3Blue1Brown. README identyfikuje Manim, a katalogi roczników i ścieżka `_2017/eoc/chapter1.py` wiążą przykład z cyklem o rachunku różniczkowym. Kod jest materiałem roboczym dla warstwy wyjaśniającej. Autor repozytorium wskazuje możliwą niezgodność starszych scen z nowszymi wersjami Manim. [P07, README i drzewo projektu](https://github.com/3b1b/videos)

**Przeniesienie.** Budować wykres, podpis i przejście z tego samego rekordu danych. Oddzielić równanie, kolejność ujawniania, narrację i czas. Zapisać wersję renderera, fonty i wejścia, by móc przeliczyć jedną scenę po korekcie danych. **Unknown:** kompletny projekt montażowy, rejestracja głosu i muzyka, udział innych narzędzi dla określonych nowszych filmów, konfiguracja pierwotnego renderu.

## 8. Lackadaisy — pilot Iron Circus Animation

**CREATOR_CLAIM.** Fable Siegel w wywiadzie z 12.04.2023 opisuje ręcznie rysowaną animację pilota i świadome zachowanie śladów procesu. Ujawnia, że część widocznych linii konstrukcyjnych została dodana przez cleanup. Uproszczono język rysunku względem komiksu, a mowa ciała i zwierzęce cechy niosą część emocji w dialogowych scenach. Dwa różne podejścia do palety i ciągłości przypisano światu realnemu i wspomnieniom. To niezależna produkcja zespołowa z finansowaniem społecznościowym. [P08, rozmowa z reżyserem](https://www.cartoonbrew.com/interviews/lackadaisy-director-fable-siegel-interview-art-227758.html)

**Przeniesienie.** Każdej warstwie stylistycznej przypisać kryterium odbioru i właściciela. Uzgodnić, gdzie dodatkowe rysunki służą aktorstwu, a gdzie proste ekspozycje utrzymują czytelność. **Unknown:** liczba etapów na każde ujęcie, wersje narzędzi i pełna ścieżka dźwiękowa, finansowy rozkład pracy. Pilot pozostaje osobnym przypadkiem wobec późniejszych produkcji marki.

## 9. Sprite Fright — Blender Studio, pełny film porównawczy

**CONFIRMED_WORKFLOW.** Andy Goralczyk dokumentuje 24.11.2021 struktury realnych plików ujęć. Paczki wyodrębniano z repozytorium SVN narzędziem BAT. Zawierały zależności postaci, rekwizytów i planów oraz oddzielne cache. Plik animacji wystawiał kolekcję `<shot name>.anim.output`. Zbierały ją pliki efektów i światła. Lighting łączył zasoby oraz mógł używać osobnych View Layers, np. do separacji postaci od rozmytego tła. Smear frames i wybrane efekty Grease Pencil docierały przez tę kolekcję, a przed renderem konwertowano je w tej produkcji do siatki. [P09, File structure i Lighting files](https://studio.blender.org/blog/exploring-production-files/)

**Przeniesienie.** Ujęcie wystawia jawnie nazwane wyjścia, a praca pomocnicza animatora zostaje w jego pliku. Cache symulacji wiązać z wejściami. W razie zmiany riga odtworzyć przegląd animacji, efektów i światła tylko w ujęciach korzystających ze zmienionego zasobu. **Unknown:** infrastruktura renderująca, kompletny przebieg voice/lipsync, polityka opóźnionych zmian tekstu. Przeczytano dokumentację plików, bez uruchamiania opublikowanych paczek. Ten przypadek nie opisuje kosztu cotygodniowej serii.

## 10. Hero — Blender Studio, pełny film porównawczy

**CONFIRMED_WORKFLOW.** Strona projektu i indeks udostępnionych materiałów pokazują film Grease Pencil z okresu Blender 2.8, w reżyserii Daniela Martineza Lary, finansowany przez Blender Cloud. Materiały projektu odnoszą się do rysunku 2D w środowisku 3D i integracji tych elementów w tłach. Premiera projektu w kwietniu 2018 jest punktem odniesienia dla sprawdzalnego zastosowania techniki. [P10, projekt i lista materiałów](https://studio.blender.org/projects/hero/)

**Przeniesienie.** Użyć stabilnego layoutu 3D do perspektywy i przejść kamery, a rysunków i efektów 2D tam, gdzie niosą ekspresję. W przyszłym teście ocenić przy zmianie ogniskowej sortowanie warstw, przecięcia i czytelność konturów. **Unknown:** pełny graf plików, czasy poprawek, wydajność na bieżącym Blenderze. Finansowanie przez Blender Cloud nie ustala miejsca renderowania.

## Luki i rozbieżności

- Nie ustalono aktualnych metod produkcji całych sezonów tych serii. Wywiady z 2011–2024 zachowują wartość dla opisanej produkcji i okresu.
- Produkcja cyfrowych lalek cut-out i użycie lipsync przez odcinkowy kanał pozostają słabiej udokumentowane w tej próbie. Dokumentacja Harmony w [porównaniu](METHODS.md) opisuje mechanizmy narzędzia. Fizyczne lalki Treflików służą jako analogia zarządzania zasobami.
- Brakuje odcinka z publicznie udokumentowaną pełną ścieżką generatywną i audytem spójności oraz liczby prób. Oficjalne dokumentacje generatorów dają granice wejścia i wyjścia, nie wyniki jakości.
- Liczby odcinków i zasobów u producenta Treflików odnoszą się do opisów z różnych momentów. Nie obliczano z nich średniej pracy ani kosztu. [P05, opis serii](https://thetreflikfamily.com/o-serialach/rodzina-treflikow/), [P11, portfolio producenta](https://kazstudio.pl/)
- Przeczytano treść stron lub bezpośrednie materiały publiczne. Wpisy search-only o pliku Flash Alan Beckera i o making-of YouTube nie wnoszą twierdzeń do kart.
