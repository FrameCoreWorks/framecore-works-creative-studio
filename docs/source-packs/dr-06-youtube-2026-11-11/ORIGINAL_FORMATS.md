# Trzy oryginalne formaty — propozycje DERIVED

Status wszystkich: **hipotetyczne, NOT_RUN, bez wygenerowanego filmu i bez akceptacji architekta**. Nazwy robocze; nie sprawdzano znaków towarowych. Nie kopiują postaci, świata, muzyki ani głosów referencji. Długości to zakresy pilota, które ograniczają liczbę nowych assetów i pracy nad aktorstwem, nie recepta algorytmiczna.

## 1. „Pracownia małych napraw” — powracający bohaterowie

**Widz i obietnica:** dzieci 5–8 i opiekunowie, jeden czytelny problem wymagający współpracy. Dwie oryginalne postaci: ostrożna kartografka Iga i impulsywny konstruktor Tym. Mała nadbrzeżna pracownia; przedmioty mają materialne ograniczenia. Projekt kierowany do dzieci wymaga odpowiedniej decyzji audience.

**Pilot 4–6 min:** zepsuty mechanizm dzwonu nie ostrzega przeprawiających się łódek. Tym chce po prostu mocniej ciągnąć; próba pogarsza stan. Iga zauważa skrzywiony uchwyt. Wspólnie zmieniają konstrukcję, sprawdzają działanie na małej skali, potem uruchamiają dzwon. Zakończenie pokazuje skutek dla innej osoby, bez wykładu moralnego. Celem nie jest demonstracja realnej instrukcji bezpieczeństwa.

**Forma i kod:** proste modułowe 2D SVG, trzy widoki postaci, 6–8 póz bazowych, osobne ręce i oczy. Ograniczone krótkie kwestie; voice-first w dialogach, timing-first przy próbach i reakcji. Większość znaczenia niesie działanie i spojrzenie. Proceduralne fale i ruch mechanizmu, lecz krytyczny kontakt dłoni ma zaprojektowaną pozę. Master montażu oddzielony od rendererów ujęć.

**Asset plan:** dwie postaci, pracownia i pomost, dzwon z kilkoma stanami, skrzynka narzędzi i drobne rekwizyty. 30–45 ujęć to plan kosztowy; liczba zmieni się po animatiku. Człowiek projektuje sylwetkę, koryguje acting, słucha każdej kwestii i ogląda całość. Najpierw test 2D kontaktu oraz dialogu B01/B02.

**Kolejne odcinki:** np. cień zasłaniający mapę, niedopasowana skrzynka, zagubiony sygnał świetlny. Inny błąd rozumowania i rozwiązanie przy znanych lokacjach. Nowe maksymalnie dwa istotne rekwizyty na odcinek, jako założenie budżetowe. Ryzyka: sztywne obroty, powtarzane miny, zmiana właściciela przedmiotu, moralizowanie.

**Dlaczego ta skala:** publikacje Milo mają około 4,5 min według playera/opisu autora, a cyfrowa biblioteka ogranicza nowe zasoby. Milo dowodzi istnienia publikacji i deklaracji kodowego procesu; nie dowodzi wydajności proponowanego riga. [Milo](https://ubedev.com/milo/), [dwie próbki](evidence/VIEWING_LOG.md).

## 2. „Mechanizm pod lupą” — explainer z narracją

**Widz i obietnica:** młodzież 13+ i dorośli zainteresowani zrozumieniem jednego mechanizmu. Bez maskotki rozmawiającej do kamery. Każda teza ma źródło i jawne uproszczenie.

**Pilot 5–7 min:** „Dlaczego krótka kolejka czasem czeka dłużej?”. Najpierw dwie kolejki o różnej liczbie osób. Widz formułuje przewidywanie, po czym poznaje różnice czasu obsługi i zmienności. Pokazać kontrprzykład oraz ograniczenia prostego modelu. Wniosek ma odpowiadać na pytanie otwarcia; pełny research dziedzinowy tej historii jest przyszłym zadaniem.

**Forma i kod:** narrator PL, diagramy Manim lub jeden sprawdzony renderer SVG/Remotion; dane i symulacja oddzielone od stylu oraz kolejności objaśniania. Voice-first, znaczniki ujawniania wartości, wyświetlanie jednostek i założeń. 18–28 kompozycji, 6–10 typów grafiki, brak lipsyncu. Seed i wersja danych zapisane.

**Asset plan i praca człowieka:** wspólny font/paleta, kolejki jako neutralne symbole, wykres czasu, legenda, karty założeń. Researcher sprawdza tezy i matematykę, reżyser upraszcza metaforę, lektor/redaktor poprawia polski język. B03 testuje trudny fragment; B04 odwracalną zmianę narracji. Ryzyko: obraz wygląda wiarygodnie, ale pokazuje inną relację niż narracja.

**Seria:** inne mechanizmy, np. bufory, losowość próby, rozkład obciążenia. Re-use komponentów graficznych, odrębne pytanie, model, kontrprzykład i wynik. Katalog potwierdza kod animacji 3Blue1Brown/Reducible i kod symulacji Primer; ich kilkunastominutowe lekcje nie są obowiązkowym metrażem pierwszego pilota. Krótsza forma ma ograniczyć złożoność i umożliwić pełne sprawdzenie. [Dowody produkcyjne](production/PRODUCTION_CASES.md).

## 3. „Archiwum ostatniego sygnału” — opowieść dla starszej widowni

**Widz i obietnica:** 16+ / dorośli, fikcyjna tajemnica technologiczna bez podszywania się pod dokument lub realne zdarzenia. Każdy odcinek rozwiązuje lokalną zagadkę, a sezon rozwija jeden szerszy problem.

**Pilot 6–8 min:** nocna archiwistka odkrywa wiadomość wysłaną z zamkniętej stacji. Wyjaśnienie początkowo wygląda na pomyłkę czasu, ale ślady wskazują na wcześniejszą decyzję bohaterki. Rozstrzygnięcie ujawnia źródło sygnału i koszt moralny; ostatni detal otwiera następny epizod. To plan struktury, nie gotowy scenariusz.

**Forma i kod:** stylizowane wnętrza Blender Python, ograniczona liczba kamer i kontrolowany rig; narracja spoza kadru plus krótkie rozmowy przez radio. Proceduralne mapy, ekrany, światło i cząstki. 25–40 ujęć, 2 lokacje, 1 postać w kadrze i 1 głos radiowy. Na start bez generowanych ujęć; możliwe przyszłe inserty atmosferyczne po osobnym teście.

**Asset plan i człowiek:** model postaci, dwa kostiumowe stany, archiwum, stacja, terminal, nośnik danych. Człowiek ustala światło i kompozycję, redaguje wiarygodność fabuły, kontroluje acting, Foley oraz ciszę. Słyszalność clue musi przetrwać odsłuch na małym głośniku. Ryzyko: monotonne nieruchome kadry, zbyt gęsty narrator, render kosztowniejszy od przewidzianego, mylne odczytanie fikcji jako faktu.

**Seria:** rdzeń lokacji wspólny; każdy odcinek dodaje jeden ważny obiekt i ujawnia inną część reguł świata. Biblie rekwizytów i wiedzy bohaterki mają pierwszeństwo przed efektownym kadrem. Obecny research nie znalazł mocnego odpowiednika pełnej code-based dialogowej serii z otwartym kodem. Ta propozycja ma największą niepewność i wymaga B02/B05; nie korzysta z wyników krótkiej próbki ESCAPEMENT jako dowodu ekonomiki serialu.
