# FrameCore Works: handover Map Motion dla Claude’a

**Właściciel:** Kamil Sikora, FrameCore Works  
**Data przekazania:** 10 listopada 2026  
**Produkcje opisane:** testy mapowe z 9 listopada 2026  
**Główny przypadek:** Warszawa Centralna → Pałac Kultury i Nauki, fotogrametria, wersja 2  
**Status:** wykonany test techniczny i korekta animacji trasy; prototyp projektu, bez wdrożenia stałego pluginu.

## 1. Cel przekazania i najważniejszy rezultat

Dokument przekazuje założenia, udokumentowane decyzje projektowe i ich uzasadnienia, rzeczywisty przebieg implementacji, problemy, poprawki oraz sposób kontynuowania pracy. Jest oparty na aktualnych zapisanych raportach i kodzie projektu. Opis źródeł internetowych odzwierciedla ich weryfikację podczas produkcji. Przy nowej produkcji trzeba ponownie sprawdzić dostępność, warunki wykorzystania i aktualność danych.

Powstał 30-sekundowy pionowy film pokazujący trasę pieszą z północnego wyjścia Warszawy Centralnej do wejścia głównego PKiN od placu Defilad. Ostatni wariant korzysta z istniejącego skanu fotogrametrycznego Warszawy, z oryginalnymi teksturami budynków i otoczenia. Obraz renderuje CesiumJS. Trasa pochodzi z wcześniej sprawdzonego lokalnego grafu pieszego OSM.

Wersja 2 realizuje ostatnią uwagę Kamila: ścieżka pojawia się dopiero wraz z ruchem punktu. Widoczny jest przebyty odcinek, którego koniec pozostaje pod znacznikiem. Pełna trasa pozostaje po dotarciu do celu. Film nie zawiera żadnego strumienia audio.

To **przyspieszony lot kamery nad trasą pieszego**, a nie odtworzenie spaceru z perspektywy oczu. Dokładność i wygląd miasta wynikają z jakości dostępnego skanu. Nie potwierdzono prawa do komercyjnego wykorzystania tego konkretnego modelu w reklamie. Wykonanie testu nie oznacza akceptacji estetycznej finalnej produkcji przez klienta.

## 2. Wymagania Kamila, które trzeba zachować

| Obszar | Wymaganie i konsekwencja |
|---|---|
| Charakter | Dynamiczny i czytelny ruch kamery; unikać ospałego tempa, przypadkowych ozdobników i przejść z gliczami. |
| Realizm | Znaleźć gotowe dane rzeczywistego miasta. Kamil odrzucił nakładanie fasad na wcześniejsze uproszczone bryły. |
| Geografia | Pieszy ma poruszać się po realnych ciągach pieszych i przejściach. Nie prowadzić go środkiem jezdni ani przez obrys budynku. |
| Znacznik i linia | Punkt prowadzi animację. Linia pokazuje wyłącznie już przebyty dystans. |
| Kamera | Wygładzać ruch kamery bez ścinania zakrętów rzeczywistej trasy. Nie zasłaniać celu napisami. |
| Stabilność | Brak nakładających się modeli PKiN, migotania powierzchni i znikającej trasy w eksporcie. |
| Dźwięk | Ostatni wariant: sam obraz. Zero muzyki, SFX, lektora i pustej ścieżki audio. |
| Format testu | 9:16, 1080 × 1920, 30 s, 60 kl./s, MP4 H.264. |
| Dostawa | Pobieralny MP4, projekt i zestaw źródeł/narzędzi. Nie zastępować pliku filmem osadzonym w Spaces. |
| Uprawnienia | Nie uruchamiać płatnych usług, publikacji, deployu, pushu ani zewnętrznego uploadu bez wyraźnego polecenia. |

We wcześniejszych reklamach użytkownik krytykował cyfrowo brzmiącą muzykę i nadmiar wysokich tonów/dzwonków. Nie należy traktować tych uwag jako zlecenia doboru nowej muzyki do obecnego filmu. Aktualna decyzja brzmi: bez audio.

## 3. Ewolucja rozwiązania

| Etap | Cel i użyte podejście | Wniosek |
|---|---|---|
| Jakóbczak → Jasna Góra | MapLibre, OpenFreeMap, pieszy OSRM, ortofotomapa Geoportalu. Promocja bliskości sklepu i klasztoru. | Dobre rozwiązanie do stylizowanej mapy, adresu i rzeczywistego zdjęcia z góry. |
| Warszawa Centralna → PKiN | Bardziej dynamiczna mapa, bryły OSM i osobno złożony model PKiN. | Ujawniono konflikt nakładających się brył i problem z przebiegiem trasy. |
| Warszawa, korekta wersji mapowej | Usunięcie duplikatów zabudowy, lokalny graf pieszy, audyt przejść. | Osobno trzeba kontrolować geometrię sceny i poprawność routingu. |
| Warszawa, fotogrametria | Gotowy IntegratedMesh Warszawy i CesiumJS, przy zachowaniu sprawdzonej trasy. | Rzeczywiste elewacje i dachy pochodzą z danych źródłowych. |
| Fotogrametria v2 | Narastająca linia za punktem, poprawka renderowania dynamicznej polilinii. | Pojedyncza poprawna klatka nie wystarcza do weryfikacji animacji. |

### Pierwszy test: Jakóbczak → Jasna Góra

Oficjalny adres sklepu: **ul. Bialska 2/4, Częstochowa**, domena **jakobczak.pl**. Współrzędne środka obiektu OSM: `[19.0943415, 50.8169296]`. Punkt początkowy routingu został dopasowany do chodnika oddalonego o 9,23 m.

Cel wybrano jako **Bramę Jana Pawła II**, `[19.0958907, 50.8122078]`, zamiast środka bazyliki. Wynik OSRM: 647,2 m, 517,8 s, prezentowane w przybliżeniu jako 650 m i 9 minut. Wszystkie kroki miały tryb walking. Nie wykonywano wtedy tak rygorystycznego audytu sieci chodników jak później w Warszawie.

Podkład pochodził z OpenFreeMap, styl Liberty. Ortofotomapy z Geoportalu stanowiły rzeczywisty widok terenu z góry. Nie zastępowały modelu elewacji. Brak zweryfikowanego zdjęcia wejścia do sklepu oznaczał zakończenie na mapie/adresie, bez wymyślania wyglądu lokalu.

### Warszawa: dwie niezależne poprawki przed fotogrametrią

**Migotanie PKiN.** Bazowa zabudowa MapLibre pokrywała się z osobno dodanymi częściami pałacu. Powstały współpłaszczyznowe powierzchnie i z-fighting. W tym projekcie podejście z filtrem `within` nie rozwiązało problemu. Wykluczono 10 konkretnych identyfikatorów budynków z podkładu, zachowując osobny model pałacu. Dane zapisano w `data/palace-basemap-exclusions.json`. Test `test-palace.cjs` obejmował osiem ustawień kamery. Przy zmianie źródła lub zestawu kafli identyfikatory trzeba ustalić ponownie.

**Nieprawidłowy skrót pieszy.** Kandydat otrzymany z pieszej usługi OSRM zawierał około 50,4 m poza wybraną siecią pieszą. Profil foot sam w sobie nie gwarantował oczekiwanego przebiegu po chodnikach. Zbudowano lokalny graf OSM i wyznaczono trasę algorytmem Dijkstry w Pythonie. Wynik zweryfikowano geometrycznie.

Te poprawki należą do starszego projektu MapLibre. Ostatni projekt fotogrametryczny dziedziczy jego trasę, ale nie dziedziczy brył.

## 4. Logika wyboru technologii

| Potrzeba | Wybrana rodzina rozwiązania | Uzasadnienie i granica |
|---|---|---|
| Mapa ulic, pinezka, adres, kolory marki | MapLibre + OpenFreeMap | Kontrola stylu i kamery. Podkład nie wyznacza trasy. |
| Rzeczywisty widok z góry | Ortofotomapa Geoportalu | Prawdziwe zdjęcia terenu, ale bez kompletnej przestrzennej geometrii elewacji. |
| Pieszy odcinek A → B | Routing pieszy i audyt grafu | Oddziela poprawność drogi od atrakcyjności obrazu. |
| Gotowe realistyczne budynki Warszawy | Fotogrametryczny IntegratedMesh | Dostawca przygotował geometrię, tekstury i poziomy szczegółowości. |
| Odczyt znalezionego I3S | CesiumJS | Format źródła pasował do `I3SDataProvider`; nie trzeba było przerabiać modelu na bryły Three.js. |
| Powtarzalny ruch | Funkcja sceny zależna od czasu klatki | Ta sama klatka powinna odpowiadać temu samemu postępowi na trasie i ustawieniu kamery. |
| MP4 | Playwright/Chromium + FFmpeg | Przeglądarka renderuje scenę WebGL, FFmpeg koduje klatki i wykonuje techniczne kontrole. |

Najważniejsza kolejność decyzji: **najpierw dostępne dane miasta, ich zakres i prawa wykorzystania, potem renderer**. Samo dodanie repozytorium Cesium lub renderera 3D Tiles nie dostarcza darmowej fotogrametrii wszystkich miast.

Google Maps/Earth nie zostały użyte. Nie należy wywodzić możliwości użycia reklamowego z samego dostępu do mapy lub API. Warunki każdego nowego źródła trzeba zweryfikować osobno.

## 5. Dokładne źródło fotogrametrii

| Pole | Wartość z zachowanych metadanych |
|---|---|
| Tytuł | `DSM_Mesh_Warsaw_SURE5_0_1_33m` |
| ArcGIS item ID | `0d79fce75b8e44e1936bbbe2cc440333` |
| Warstwa | 0 |
| Typ | IntegratedMesh, OGC I3S 1.7 |
| Oznaczenie źródła | Warsaw University of Technology, Esri |
| Publikacja elementu | 23 lutego 2023 |
| Data wykonania zdjęć | **Unknown** |
| Zdjęcia wejściowe | DMC III, pokrycie 80/80%, GSD 8 cm według opisu |
| Dostęp w czasie testu | Publiczny odczyt, bez klucza API i bez płatnego konta |
| Pole `licenseInfo` | `null` |
| Licencja do filmu reklamowego | **Unknown** |
| Zasięg | Od `[20.9694258622, 52.2157658367]` do `[21.0311273873, 52.2536488253]` |

GSD 8 cm opisuje materiał zdjęciowy, nie gwarantuje takiej rozdzielczości każdej widocznej tekstury. W podglądach występowała gorsza szczegółowość i miejscowe deformacje odległej zabudowy. Model może przedstawiać starszy stan zagospodarowania niż trasa OSM.

- [Strona modelu](https://www.arcgis.com/home/item.html?id=0d79fce75b8e44e1936bbbe2cc440333)
- [Metadane elementu](https://www.arcgis.com/sharing/rest/content/items/0d79fce75b8e44e1936bbbe2cc440333?f=pjson)
- [SceneServer](https://tiles-eu1.arcgis.com/7cCya5lpv5CmFJHv/arcgis/rest/services/DSM_Mesh_Warsaw_SURE5_0_1_33m/SceneServer)

Sprawdzono również oficjalny skorowidz modeli siatkowych GUGiK. Zapytanie WFS o obszar tej trasy zwróciło `numberMatched="0"`. Był to wynik konkretnego zapytania, nie stwierdzenie braku fotogrametrii w całej Warszawie lub Polsce. Źródło: [WFS ModeleSiatkowe3D](https://mapy.geoportal.gov.pl/wss/service/PZGIK/NMT/WFS/ModeleSiatkowe3D), typ `gugik:SkorowidzModeleSiatkowe3D`, bbox `52.224,20.995,52.237,21.015` w kolejności osi EPSG:4326 użytej w zapytaniu.

Publiczny odczyt modelu nie został uznany za zgodę na reklamę ani redystrybucję skanu. Paczka przekazywana dalej nie zawiera kopii geometrii i tekstur miasta. Przed publikacją komercyjną potrzebne jest wyjaśnienie praw do tego źródła lub zastąpienie go materiałem z jednoznacznymi warunkami.

## 6. Trasa piesza: wejścia, przebieg i audyt

W plikach GeoJSON i kodzie sceny obowiązuje kolejność **długość, szerokość geograficzna**, czyli `[lon, lat]`.

| Parametr | Ustalony wynik |
|---|---|
| Start | Północne wyjście z hali Warszawy Centralnej |
| Start OSM | node `2350121417`, `[21.0031866, 52.2290728]` |
| Meta | Główne wejście PKiN od placu Defilad |
| Meta OSM | node `5148654078`, `[21.006901, 52.2319291]` |
| Długość audytowanej trasy | 635,7078415 m |
| Struktura | 79 węzłów, 32 różne OSM ways, 9 węzłów oznaczonych jako przejścia |
| Typy odcinków | `highway=footway` i `highway=steps` |
| Schody końcowe | `step_count=16`, `ramp=no` w zapisanych danych |
| Kontrola geometryczna | 0,0 m poza wybraną siecią pieszą przy tolerancji 0,6 m |
| Przybliżony czas | Około 9 min przy 4,5 km/h; bez oczekiwania na światłach i wyjścia z peronu |

Trasa wykorzystuje oznaczone przejścia, w tym sygnalizowane przekroczenie Emilii Plater. Audyt był testem zgodności z wybranymi danymi OSM. Nie obejmował aktualnej wizji lokalnej, remontów ani chwilowych zamknięć. Nie jest to wariant bez barier ze względu na schody.

Cesium oblicza długość tej samej polilinii przy użyciu `EllipsoidGeodesic` jako około **637,1555 m**. Różnica względem audytu wynika z metody liczenia. W filmie pokazano wspólne, zaokrąglone **640 m**.

Zachować rozdzielenie:

1. Geometria trasy: dokładne węzły i odcinki piesze.
2. Postęp pieszego: dystans wzdłuż tej geometrii.
3. Wygładzanie kamery: osobny zabieg wizualny.

Wygładzanie spline’em samej trasy może przesunąć punkt z chodnika na jezdnię. Format `routes[0].geometry.coordinates` w `route.json` jest opakowaniem danych, a nie dowodem, że końcową trasę wyznaczył zewnętrzny OSRM.

## 7. Scenariusz techniczny ostatniego filmu

| Czas | Obraz i komunikat | Parametry kamery |
|---|---|---|
| 0–5 s | Szeroki widok miasta, zbliżenie do wyjścia dworca. „WARSZAWA • FOTOGRAMETRIA”, „Centralny → PKiN”, „640 m pieszo”. Linia ukryta. | Heading 25° → 36°, pitch −53°, range 1050 → 330 m. |
| 5–24 s | Punkt pokonuje trasę. Żółty odcinek narasta za nim. Kamera podąża nad otoczeniem. | Heading 36° → −40°, pitch −53°, range 330 → 370 m. |
| 24–30 s | Punkt w celu, pełna przebyta trasa pozostaje. Odsunięcie kamery odsłania PKiN. „NA MIEJSCU”, „Pałac Kultury i Nauki”, „Spacer z Warszawy Centralnej”. | Heading −40° → 12°, pitch −53° → −40°, range 370 → 940 m. |

FOV wynosi 48°. Pierwszy napis jest pełny do 3 s i znika między 3 a 5 s. Końcowy tekst jest podmieniany po 25 s, pojawia się od 26 do 28 s. Kamera wykorzystuje cubic smoothstep. Przejazd pieszego ma łagodne rozpędzenie i hamowanie oraz prawie liniowy odcinek środkowy.

Stylistyka prototypu: biały punkt 16 px z ciemnym obrysem 4 px; linia `#f4e769`, szerokość 5 px; typografia HTML/CSS. Tytuł używa deklaracji Arial, 54 px, podtytuł 22 px. Rzeczywisty fallback fontu zależy od systemu, dlatego przy przenoszeniu projektu należy sprawdzić identyczność łamania tekstu.

## 8. Jak działa narastanie ścieżki

Jedna wartość `progress` steruje zarówno znacznikiem, jak i końcem linii. Postęp jest oparty na dystansie, a nie na liczbie węzłów. Dzięki temu zagęszczenie punktów OSM nie zmienia lokalnej prędkości animacji.

Dla czasu `t`:

- `u = clamp((t - 5) / 19, 0, 1)`;
- strefa rozpędzania/hamowania: `r = 0.08`;
- przed końcem rozpędzania: `progress = u² / (2r(1-r))`;
- po początku hamowania: `progress = 1 - (1-u)² / (2r(1-r))`;
- w środku: `progress = (u-r/2)/(1-r)`.

Z tabeli skumulowanych odległości wybierany jest segment bieżącego punktu i interpolowana pozycja na tym segmencie. Widoczna polilinia zawiera wszystkie wcześniej minięte węzły oraz tę interpolowaną pozycję. Przy `progress=0` ma być ukryta. Przy `progress=1` zawiera całą trasę.

Kamera korzysta z ważonej średniej trzech pozycji: przed punktem, w punkcie i za nim, z wagami 1:2:1. Zakres próbkowania wynosi `0.018 × sin(π × progress)`. Dotyczy to środka zainteresowania kamery, nie geometrii marszu.

### Poprawka krytyczna dla renderowania

Pierwsza implementacja zmieniała co klatkę tablicę pozycji polilinii typu Entity. Oczekiwanie na ustabilizowanie sceny dawało poprawny pojedynczy podgląd. Podczas ciągłego zapisu klatek uruchamiała się asynchroniczna przebudowa geometrii i w MP4 znikały linia oraz znacznik.

Ostatecznie zastosowano **`Cesium.PolylineCollection` jako synchroniczny primitive**. Co klatkę aktualizowane są `line.positions` i `line.show`. Znacznik pozostał punktem Entity. Przed pełnym renderem przeprowadzono próbę 18 kolejnych przechwyceń klatek, która potwierdziła widoczność obu elementów.

Nie wracać automatycznie do Entity polyline tylko dlatego, że statyczny screenshot wygląda poprawnie. Test musi obejmować dokładnie ten tryb przechwytywania, który tworzy wideo.

## 9. Wysokość trasy i kontakt z modelem

Proste dopasowanie linii do powierzchni skanu prowadziło ją po dachu dworca. Skan zawiera powierzchnie widoczne z powietrza, a chodnik może biec pod zadaszeniem.

Zastosowana heurystyka:

1. Dla każdego z 79 węzłów pobierz wysokość w środku i w sześciu sąsiednich pozycjach.
2. Offsety w metrach: `[-18,0]`, `[18,0]`, `[0,-18]`, `[0,18]`, `[-12,-12]`, `[12,12]`.
3. Odrzuć wyniki niefinitywne oraz poza zakresem 50–250 m.
4. Z sąsiednich próbek wyznacz regionalny 20. percentyl; lokalnie preferuj próbki w zakresie ±8 m od tej wartości.
5. Jeśli próbka centralna leży ponad 5 m nad oszacowanym gruntem, potraktuj ją jako prawdopodobne zadaszenie i użyj oszacowania gruntu.
6. Podnieś linię o 0,35 m. Punkt znajduje się 2 m ponad wysokością linii.

Wyniki zapisano w `data/route-height-audit.json`. Renderer wczytuje ten zapis, co stabilizuje kolejne wersje kamery i ułatwia łączenie fragmentów renderu.

To heurystyka tego obszaru, nie pomiar geodezyjny ani uniwersalny model chodników. Wymaga ponownego strojenia dla terenu górzystego, estakad, tuneli i wielopoziomowych przejść. Punkt ma włączony test głębokości. Zadaszenie może go fizycznie zasłaniać. Nie naprawiać tego przez podnoszenie całej trasy ponad budynki.

## 10. Pipeline faktycznie użyty do renderowania

### Scena

`index.html` ładuje Cesium i nakładkę tekstową. `film.js` tworzy Viewer, wczytuje I3S przez lokalne `/mesh/layers/0`, ustawia kamerę i udostępnia `window.draw(t)`.

Ustawienia zapisane w projekcie:

| Parametr | Wartość |
|---|---|
| Rozdzielczość przeglądarki | 1080 × 1920, deviceScaleFactor 1, resolutionScale 1 |
| maximumScreenSpaceError | 8 |
| skipLevelOfDetail | false |
| dynamicScreenSpaceError | false |
| cacheBytes | 768 MiB |
| maximumCacheOverflowBytes | 512 MiB |
| calculateNormals | false |
| Antyaliasing | WebGL antialias + FXAA |
| preserveDrawingBuffer | true |
| Cesium ion | Pusty token, bez użycia usługi ion |
| Tło i UI | Wyłączone podkład, glob, atmosfera, niebo, słońce, księżyc i standardowe kontrolki |

W adresie I3S istotny jest element `layers/0`. Podawanie nieodpowiedniego poziomu URL powodowało błędne rozwiązywanie ścieżek zasobów.

### Lokalny serwer i dane modelu

`server.py` udostępnia projekt pod `127.0.0.1:8767` oraz proxy do jednego wskazanego SceneServera. Limit pobrań wynosi 12, timeout odczytu źródła 45 s. Bufor dyskowy używa skrótów SHA-256 ścieżek i zapisuje MIME oraz czas ważności. Przy odczycie bufora online uwzględnia `Cache-Control: max-age` i `Age`. Odpowiedzi są też współdzielone w pamięci sesji.

To pomocniczy serwer prototypu, nie gotowa usługa produkcyjna ani uniwersalna implementacja cache HTTP. Należy rozwijać go zgodnie z warunkami konkretnego dostawcy.

W korekcie v2 utracono dostęp sieciowy. Wykorzystano wcześniej pobrane fragmenty z `MODEL_OFFLINE=1`. Tryb ten nie odświeża dat i nie pobiera brakujących zasobów. Brak fragmentu daje `OFFLINE_MISS`/HTTP 409 i zatrzymuje poprawny render.

Historyczny cache znajdował się w `/tmp/framecore-warsaw-photogrammetry-cache`. Nie jest częścią ZIP-a i nie należy zakładać, że nadal istnieje. Na świeżym stanowisku tryb offline bez kompletu danych nie odtworzy filmu.

### Przechwytywanie klatek

`render.cjs` uruchamia serwer jako proces potomny, a następnie Playwright i headless Chromium. To rozwiązanie omijało problem z dostępnością serwera uruchomionego w oddzielnej sesji środowiska.

Żądania `/mesh/**` są obsługiwane przez Playwright APIRequestContext z kolejką 12 slotów. Zastosowano timeout 90 s i `maxRetries:2`. Nie traktować tego jako pełnej polityki ponawiania dowolnych błędów HTTP. Odpowiedzi są zwalniane po przekazaniu do przeglądarki. Licznik aktywnych żądań zmniejsza się w `finally`, także po błędzie.

Przed zapisem scenę wczytuje się dla czasów 0, 5, 10, 15, 20, 24 i 29,99 s. Sprawdzane są brak aktywnych żądań, gotowość tilesetu i liczba wybranych trójkątów ponad 10 000. Maksymalne oczekiwanie na ustabilizowanie wynosi 10 minut. Ten warunek nie gwarantuje jakości wszystkich fasad.

Wyłączono domyślną pętlę renderującą. Każda klatka wywołuje `window.draw(frame/60)` oraz ręczne `viewer.render()`. Screenshot JPEG jakości 97 trafia do FFmpeg przez image2pipe. Przy nowych pobraniach renderer czeka na gotowość.

### Kodowanie

Pierwszy zapis: libx264, preset fast, CRF 18. Jawne przeliczenie zakresu JPEG PC i macierzy BT.601 na wyjściowe TV/BT.709. Format yuv420p, faststart, `-an`.

`finalize.py` dodaje widoczne oznaczenie „Trasa: © OpenStreetMap contributors”, następnie koduje finalny MP4 z CRF 16 i ponownie `-an`. Oznaczenie modelu WUT/Esri jest w scenie Cesium.

Wersja 2 odtworzyła klatki 0–1439 i zachowała stare klatki 1440–1799, ponieważ od 24 s pełna trasa była już poprawna. Łączenie odbyło się po numerach klatek i z resetowaniem PTS. Źródłem końcówki był wcześniejszy surowy render bez dodatkowego podpisu OSM. Nie należy używać już podpisanej wersji do ponownego wypalenia tego samego oznaczenia.

## 11. Narzędzia: użyte, historyczne i tylko rozważane

### Ostatni film fotogrametryczny

| Narzędzie | Wersja utrwalona w projekcie/raporcie | Rola |
|---|---|---|
| CesiumJS | 1.147.0 | Odczyt I3S, model miasta, kamera, trasa i punkt |
| ArcGIS Scene Service / I3S | I3S 1.7, layer 0 | Istniejąca geometria i tekstury Warszawy |
| OpenStreetMap | Snapshot projektu; globalny numer wersji nie dotyczy | Dane wejść, chodników, przejść i schodów |
| JavaScript / HTML / CSS | Kod projektu | Animacja i napisy |
| Playwright | 1.62.1 | Automatyzacja renderowania i przechwytywanie klatek |
| Chromium | 153.0.8010.0 | WebGL w przeglądarce |
| @sparticuz/chromium | 153.0.0 | Dostarczenie binarium przeglądarki |
| Node.js / npm | Node 24.22.1; npm Unknown | Orkiestracja i zależności z lockfile |
| Python | 3.12.14 w środowisku produkcji | Serwer, metadane, finalizacja, QA |
| FFmpeg / ffprobe | 7.1.5-0+deb13u1 | H.264, połączenie fragmentów, atrybucja, analiza MP4 |
| Shapely | 2.1.2 | Wcześniejszy audyt zachowanej trasy pieszej |
| Pillow / NumPy | 13.0.0 / 2.3.5 w środowisku QA | Wybrane analizy klatek i porównanie łączenia |
| Fonty | CSS Arial/fallback; DejaVu Sans dla drawtext | Napisy sceny i oznaczenie OSM |

Shapely, Pillow i NumPy nie są zależnościami podstawowej pętli renderującej w przekazanym ZIP-ie. Nie należy twierdzić, że każde z nich uruchamia się przez `npm run render`.

Repozytorium faktycznie wybrane: [CesiumGS/cesium](https://github.com/CesiumGS/cesium), silnik Apache-2.0. Licencja silnika nie rozstrzyga licencji skanu.

### Wcześniejsze mapowe testy

Używano MapLibre GL JS 6.17.0, Turf.js 7.4.0, GSAP 3.15.1, OpenFreeMap/OpenMapTiles, OSM, FOSSGIS OSRM routed-foot i Geoportalu WMS HighResolution. W audycie kafli Warszawy także `@mapbox/vector-tile` 3.0.0 i `pbf` 5.1.2.

Earshot 0.4.0 w wariancie light oraz wrapper Toolbox 1.12.0 służyły do wcześniejszych kontroli audio. Wykorzystywano muzykę „Funky Chunk” Kevina MacLeoda z oznaczeniem CC BY 3.0. Nie należy przenosić jej do obecnego niemego filmu. FrameCore Works Creative Studio i Open Assets stanowiły kontekst organizacyjny doboru narzędzi i materiałów; dokładna wersja ich aktywnego wydania w tej produkcji: **Unknown**.

### Sprawdzone alternatywy, bez udziału w ostatnim renderze

- [NASA-AMMOS/3DTilesRendererJS](https://github.com/NASA-AMMOS/3DTilesRendererJS): alternatywa renderera 3D Tiles dla Three.js; nie użyto.
- [CesiumGS/cesium-unreal](https://github.com/CesiumGS/cesium-unreal): kierunek dla Unreal Engine; nie instalowano i nie użyto.
- Remotion, HyperFrames, Three.js, Blender: nie renderowały ostatniego filmu.
- Generatory AI obrazu/wideo, synteza muzyki, lektor, SFX: nie użyto w ostatnim wariancie.
- Nie wykonano trwałej instalacji nowego modułu w Toolboxie, aktualizacji pluginu ani zmian na GitHubie.

## 12. Błędy i wiedza do zachowania

| Objaw | Przyczyna lub ustalenie | Zastosowane rozwiązanie / reguła |
|---|---|---|
| Migoczący pałac w starszej mapie | Dwie reprezentacje tych samych powierzchni | Usunięcie odpowiednich obiektów z podkładu; audyt z wielu kamer. |
| Pieszy skraca przez niewłaściwy fragment drogi | Wynik routingu nie odpowiadał wymaganej sieci chodników | Lokalny graf pieszy i geometryczne sprawdzenie trasy. |
| Linia wspina się na dach dworca | Próbkowanie wierzchniej powierzchni skanu | Estymacja gruntu pod zadaszeniem i zapis wysokości. |
| Błędne adresy zasobów I3S | Niewłaściwy poziom adresu usługi | Jawne `/layers/0`. |
| Pobieranie stoi lub zawodzi | Kolejka żądań, błędy sieci, dostęp źródła | Ograniczona równoległość, timeouty, jawne błędy; później istniejący cache offline. |
| Licznik aktywnych pobrań nie wraca do zera | Niewłaściwe śledzenie zakończeń | Liczenie we własnym handlerze z `try/finally`. |
| Render bardzo wolny / niestabilny | Nakładanie się ciągłej pętli przeglądarki i przechwytywania | Ręczny render dla ustalonego czasu każdej klatki. |
| Linia i punkt znikają w filmie | Asynchroniczna przebudowa Entity polyline | Synchroniczna PolylineCollection i test kolejnych przechwyceń. |
| Techniczny raport PASS mimo brakującej linii | Kontrola kodeka nie bada treści ujęcia | Osobna kontrola obrazu z zakodowanego MP4. |
| Ponowny render części filmu może dać skok | Inna kamera, wysokości, czas lub źródło końcówki | Te same dane wysokości, indeksy klatek i kontrola łączenia. |
| Odległe budynki są zdeformowane | Jakość skanu/LOD | Kontrola kadru; nie obiecywać naprawy samym zwiększeniem rozdzielczości filmu. |

## 13. QA i rzeczywiste czasy

Zachowany raport końcowy potwierdza:

- 30,000 s; 1080 × 1920; 60 kl./s; 1800 klatek.
- H.264, yuv420p; zero strumieni audio.
- Pełne dekodowanie FFmpeg bez błędu.
- Brak alarmów czarnego obrazu według użytego blackdetect i zatrzymań według freezedetect z progiem 0,5 s.
- Kontrola narastania trasy przy 0, 5, 10, 15, 20, 24 i 29,99 s.
- Osobna próba 18 kolejnych przechwyceń dla poprawionej polilinii.
- Oględziny wybranych klatek finalnego MP4: 0, 420, 600, 900, 1200, 1439, 1440.
- Dla łączenia klatek 1439→1440 średnia bezwzględna różnica RGB wyniosła około 1,415 w zastosowanym pomniejszonym wycinku kontrolnym.

Nie jest to deklaracja ręcznego obejrzenia każdej z 1800 klatek. Niski wynik różnicy RGB nie jest samodzielną miarą płynności. Automatyczny PASS nie oznacza aktualności skanu, poprawności wszystkich fasad ani satysfakcji klienta.

| Pomiar | Czas | Zakres |
|---|---|---|
| Pierwszy pełny zapis fotogrametrii | 2069,79 s, około 34 min 30 s | 1800 klatek; bez wstępnego wczytania i końcowego kodowania/QA |
| Ukończona poprawka v2 | 893,453 s, około 14 min 53 s | Nowe 1440 klatek; pozostałe 360 zachowano |
| Łączny czas całej produkcji i poprawek | **Unknown** | Obejmuje również przygotowanie i nieudane próby, więc nie wolno utożsamiać go z czasem zapisu |

Nie jest to miarodajny benchmark dedykowanej stacji GPU. Chromium uruchamiano z obsługą SwiftShader. Szybkości kolejnych maszyn nie zmierzono.

Zakupy płatnych generacji i płatnych usług danych w tym teście: brak. Koszt infrastruktury/subskrypcji środowiska: **Unknown**.

### Dwie luki w obecnym skrypcie QA, wykryte podczas odczytu kodu

1. `qa.py` zapisuje `passed=false`, gdy wykryje czarny lub zatrzymany odcinek, ale sam ten przypadek nie kończy skryptu błędnym kodem wyjścia. Automat powinien sprawdzić raport lub skrypt trzeba uzupełnić.
2. Ponowne wykonanie `qa.py` nadpisuje `delivery/video-qa.json` i nie odtwarza ręcznie dopisanej sekcji `visual_review`. Tę kontrolę trzeba prowadzić oddzielnie lub zachować w osobnym raporcie.

To zadania do dalszego utwardzenia projektu, nie poprawki wykonane w ramach tego handoveru.

## 14. Paczka projektu i znaczenie plików

Przekazywany projekt: **`Warszawa_Fotogrametria_Projekt_v2.zip`**, 39 854 bajty, 21 plików. Katalog po rozpakowaniu: `warszawa-photogrammetry/`.

| Pliki | Zastosowanie |
|---|---|
| `README.md` | Uruchomienie, ograniczenia, opis v2 |
| `package.json`, `package-lock.json` | Przypięte zależności i komendy |
| `index.html`, `film.js` | Scena, kamera, napisy, punkt, narastająca linia |
| `server.py` | Lokalny serwer i dostęp do źródła mesh |
| `render.cjs` | Browser, warmup, przechwytywanie, kodowanie surowego filmu |
| `finalize.py` | Atrybucja i opcjonalne zachowanie końcówki |
| `qa.py` | Parametry MP4, dekodowanie, detekcja czerni/zatrzymań |
| `package_project.py` | Złożenie ZIP-a |
| `data/route.json` | Geometria trasy |
| `data/foot-route-audit.json` | Węzły, odcinki, tagi i przejścia |
| `data/route-height-audit.json` | 79 wysokości używanych przez scenę |
| `data/route-reveal-check.json` | Kontrola postępu i długości widocznego odcinka |
| `data/source-manifest.json` | Pochodzenie danych i status źródła |
| `data/*-item.json`, `data/*-layers.json` | Snapshot metadanych modelu |
| `data/mesh-warsaw-hits.xml` | Wynik sprawdzenia skorowidza GUGiK |
| `data/render-report.json` | Pomiar renderowania v2 i sposób korekty |
| `data/route-credit.txt` | Treść oznaczenia OSM |
| `delivery/video-qa.json` | Zapisany wynik kontroli finalnego MP4 |

ZIP nie zawiera skanu, tekstur, node_modules, finalnego MP4 ani starego surowego filmu potrzebnego do częściowego renderu. Zawiera wynik routingu i jego audyt, ale nie pełny wcześniejszy graf OSM ani komplet skryptów wyznaczania tras z projektu MapLibre. Ponowne wyznaczenie innej drogi wymaga odzyskania starszego projektu lub przygotowania osobnego modułu routingu.

Suma SHA-256 ZIP-a:

```text
1fd67b4b50dec14082f2f314f422250567e45c5b662334de7cef276c54e3ba6d
```

Finalny film: **`Warszawa_Centralna_PKiN_Fotogrametria_v2_sciezka_za_punktem.mp4`**, 246 797 236 bajtów. SHA-256 według zachowanego raportu:

```text
5a8c0824b025449a8cf7ec7d74118c017eef176f533c0a054551a1b8efb3c656
```

## 15. Jak Claude ma odtworzyć test

Najpierw przeczytać README, manifest źródła i kod. Zweryfikować dostępność modelu oraz uprawnienia do planowanego użycia. Polecenia poniżej są instrukcją odtworzenia; nie były uruchamiane podczas przygotowania tego handoveru.

Wymagane: zgodny Node.js, Python 3, FFmpeg i ffprobe w PATH, biblioteki systemowe Chromium oraz font DejaVu Sans pod ścieżką używaną w `finalize.py`. Obecne binarium @sparticuz jest rozwiązaniem dla środowiska Linux. Na innym systemie trzeba dostosować uruchomienie przeglądarki.

Po rozpakowaniu, z dostępem do zależności i źródła:

```bash
cd warszawa-photogrammetry
npm ci
npm run review
```

Sprawdzić podglądy przed uruchomieniem całego filmu. Sam `npm run review` sprawdza scenę i stany trasy, ale nie odtwarza jeszcze całej sekwencji zapisu.

Pełny render, bez zależności od poprzedniego MP4:

```bash
cd warszawa-photogrammetry
npm run render
```

Wynik znajdzie się w `delivery/Warszawa_Centralna_PKiN_Fotogrametria_v2_sciezka_za_punktem.mp4`. Następnie sprawdzić raport i faktyczny obraz z MP4.

Tryb offline działa tylko przy istniejącym kompletnym cache:

```bash
cd warszawa-photogrammetry
MODEL_OFFLINE=1 npm run render
```

Częściowe odtworzenie 24 sekund jest możliwe wyłącznie wtedy, gdy dostępny jest właściwy wcześniejszy surowy film:

```bash
cd warszawa-photogrammetry
RENDER_FRAMES=1440 node render.cjs
python3 finalize.py --tail-from review/picture-before-route-credit.mp4
python3 qa.py
```

Zmienna `RENDER_OUTPUT` zmienia ścieżkę zapisu renderera, lecz `finalize.py` oczekuje domyślnego `review/route-reveal-raw.mp4`. Nie zmieniać jej bez dostosowania finalizacji.

Opcjonalny `REVEAL_PREFLIGHT=1` zapisuje 18 kolejnych przechwyceń i czeka do 10 minut na lokalny plik `review/reveal-preflight-approved`. Jest to techniczny mechanizm zatrzymania do oględzin przez operatora. Domyślna komenda render nie wymaga tego pliku. Mechanizm nie zastępuje kontroli końcowego MP4.

## 16. Co rozwijać dalej, a czego nie uznawać za wdrożone

Poniższe punkty są propozycją dalszych prac dla Claude’a i Kamila. Nie są opisem istniejącego globalnego pluginu.

### Priorytet 1: odtwarzalność i jakość

- Zachować działający wariant referencyjny i jego dane przed zmianą kamery lub źródła.
- Dodać test krótkiego zakodowanego odcinka z widoczną linią, znacznikiem i ruchem, przed wielominutowym renderem.
- Sprawdzać, że koniec linii pokrywa się ze znacznikiem, a żaden przyszły odcinek nie jest widoczny.
- Naprawić sposób sygnalizowania niepowodzenia przez QA i rozdzielić wyniki automatyczne od oględzin.
- Usunąć zależność awaryjnego szukania pakietów w sąsiednim katalogu `../jakobczak-map-motion`; lokalne `npm ci` powinno wystarczać.
- Zapisywać manifest zależności, wersję danych, ustawienia kamery, czas i raport błędów dla każdego renderu.
- Zaplanować kontrolę LOD i kompletności modelu w szerokim planie. Zwiększenie liczby pikseli nie naprawia brakujących tekstur.

### Priorytet 2: moduł Map Motion

Roboczy kontrakt wejściowy: lokalizacja A i B, konkretne wejścia, tryb pieszy, wymagania dostępności, długość filmu, format, fps, styl, tryb audio, źródło i status praw. Dodatkowo data pozyskania danych i wymagany rodzaj obrazu: mapa, ortofoto albo fotogrametria.

Wyjście: MP4, projekt, geometria i audyt trasy, manifest źródeł, atrybucje, storyboard/podglądy, raport QA i ograniczenia. Adres początku i końca trzeba rozwiązać na wejście lub dostępny punkt chodnika, a nie wyłącznie centroid budynku.

Warstwy funkcjonalne warto rozdzielić na: wybór źródła, routing, wysokości, scenę/kamerę, render, QA i dostawę. To umożliwia zmianę miasta lub dostawcy bez przebudowy całej animacji.

### Priorytet 3: źródła międzynarodowe i wydajność

Pierwotny research był mocno związany z Polską i Geoportalem. Rozszerzenie powinno zbadać rzeczywiste międzynarodowe źródła fotogrametrii i ortofoto: zasięg, daty, licencje, atrybucję, API, limity pobierania, możliwość cache, koszty i dostęp bez konta.

Przy braku prawidłowego skanu danego miasta należy jawnie zaproponować mapę lub ortofoto. Nie przedstawiać teksturowanych brył jako znalezionej fotogrametrii.

Można zbadać rendering fragmentami, checkpointy, ponowne użycie niezmienionych ujęć i maszynę z GPU. Trzeba uwzględnić deterministyczność kamery, identyczność LOD oraz zgodność danych między fragmentami. Nie obiecywać czasu renderu bez pomiaru. Zmiana 60 na 30 kl./s lub jakości eksportu jest decyzją produkcyjną, nie domyślną optymalizacją bez uzgodnienia.

Rozdzielenie czystego obrazu miasta od napisów może przyspieszyć poprawki tekstowe. Oddzielanie trasy od geometrii wymaga jednak zachowania właściwego zasłaniania przez budynki i perspektywy; zwykła nakładka 2D może zniszczyć tę relację.

## 17. Otwarte kwestie

| Pytanie | Status |
|---|---|
| Prawo do komercyjnego filmu z tego skanu | **Unknown** |
| Data zdjęć źródłowych | **Unknown** |
| Aktualne remonty i dostępność wszystkich przejść | **Unknown** |
| Wariant trasy bez schodów | Nieprzygotowany |
| Aktualna dostępność usługi po przeniesieniu projektu | Do ponownego sprawdzenia |
| Dostępność starego cache na nowej maszynie | Niepotwierdzona; nie ma go w ZIP-ie |
| Jedno darmowe źródło realistycznych modeli wszystkich miast | Nieustalone |
| Wydajność na dedykowanym GPU | **Unknown** |
| Łączny czas produkcji i koszt infrastruktury | **Unknown** |
| Akceptacja estetyczna ostatniego filmu przez Kamila | Niepotwierdzona w przekazanym kontekście |
| Stała integracja Map Motion z Creative Studio/Toolbox | Niewykonana w tym projekcie |

## 18. Materiały źródłowe handoveru

Przy opracowaniu dokumentu odczytano aktualne wersje:

1. `Warszawa_Fotogrametria_Projekt_v2.zip`: kod sceny, renderera, serwera, finalizacji i QA; dane, metadane i raporty.
2. `Warszawa_Fotogrametria_Narzedzia_i_Zrodla.md`.
3. `Warszawa_Centralna_PKiN_Narzedzia_i_Zrodla.md`.
4. `Jakobczak_MapMotion_Narzedzia_i_Zrodla.md`.
5. Uwagi i wymagania Kamila z rozmowy.

Pomocnicze źródła z dokumentacji wcześniejszych etapów:

- [Kontakt sklepu Jakóbczak](https://jakobczak.pl/pl/i/Kontakt/1)
- [OpenFreeMap: quick start](https://openfreemap.org/quick_start/)
- [OpenFreeMap: warunki](https://openfreemap.org/tos/)
- [OpenStreetMap: copyright i atrybucja](https://www.openstreetmap.org/copyright)
- [FOSSGIS routing: informacje o usłudze](https://routing.openstreetmap.de/about.html)
- [Geoportal: ortofotomapa](https://www.geoportal.gov.pl/pl/dane/ortofotomapa-orto/)
- [Geoportal WMS HighResolution](https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMS/HighResolution)
- [PKP: informacje o Warszawie Centralnej](https://www.pkp.pl/pl/dworce/warszawa-centralna-informacje-dla-podroznych)
- [PKiN: deklaracja dostępności](https://bip.pkin.waw.pl/p,79,deklaracja-dostepnosci)

Podczas przygotowania tego handoveru nie wykonano nowego renderu, nie zmieniono źródłowego projektu i nie wdrożono nowych funkcji. Weryfikacja dotyczyła zapisanej dokumentacji, kodu oraz raportów. Claude powinien zacząć od tej paczki i jasno rozróżniać odziedziczone wyniki, własne nowe testy i propozycje rozwoju.

