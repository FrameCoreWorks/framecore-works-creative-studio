# Niepewności i granice DR-04

Data: 2026-11-11. Wszystkie przyszłe próby NOT_RUN. Unknown nie jest zgodą. Ten rejestr ma pierwszeństwo przed skrótowym marketingowym opisem dostawcy.

| ID | Luka / znany fakt | Konsekwencja i najmniejszy dalszy krok |
|---|---|---|
| G01 | Brak zakwalifikowanego nowego szerokiego no-key API recordedSFX, wielu kompozytorów i stock alpha | Nie deklarować zamknięcia tych luk; decyzja o pojedynczym dozwolonym subset lub manual/optional scope. |
| G02 | Internet Archive terms JS nieodczytane; strona bots dawniej zanotowana jako READ przez badacza, bieżący odczyt root niedostępny | Nie przypisywać nowej próbie dokumentowanego sukcesu; prior_read_status zachowany w source entry. Potwierdzenie warunków przed kwalifikacją, bez obejścia blokady. |
| G03 | NASA search audio niedostępny w narzędziu; 3 wpisy Artemis są stronami bez NASA ID | Udokumentowane media_type=audio nie poświadcza membership tych 3 rekordów. Pierwszy spike ma rozwiązać rzeczywisty ID/manifest na autoryzowanym hoście. |
| G04 | AIC image licensing i terms 403, mimo 2 odczytanych API records | OPTIONAL. image_id/thumbnail nie dowodzą praw; flag false bezwarunkowo nie kwalifikuje. Bez ponawiania 403 inną drogą. |
| G05 | Openverse 0 real records; API spec z indeksowanego widoku, bezpośredni 403 | Discovery proposal tylko; nie przedstawiać przeczytanej dokumentacji jako live API test. Origin nadal wymaga własnych praw/hostów. |
| G06 | CLR: sprzeczność SA, duże paczki, wycinki i źródła wtórne | Ustalenie praw per file + upstream; nie blanket CC0, nie import pełnych ZIP. Część index z indexed excerpt. |
| G07 | NPS/Blender/Mixkit/Sonniss/Quaternius/Open Peeps: brak zakwalifikowanej maszynowej drogi tej kolekcji | Manual/reference albo dalsza odrębna kwalifikacja. Strona download i robots nie są API/pozwoleniem na scraping. |
| G08 | Blender katalog CDN zwrócił w web 402 | To ograniczenie odczytu narzędzia, nie dowód płatnej licencji ani ceny CDN. |
| G09 | SVG, fonts, 3D/HDR/EXR poza native decode; A/V nie zapisuje alpha/FPS/channels | Wymagane format design i addytywne parametry, testy T13–T16. Preview/raster/CRC nie kwalifikują oryginalnego modelu/riggu. |
| G10 | Fontsource exact package notices/źródło konkretnego dystrybuowanego pliku niepełne | Pilot OFL dopiero po powiązaniu family/version/subset/file z notices. Google Fonts upstream nie automatycznie poświadcza każdej transformacji CDN. |
| G11 | ETag/Last-Modified/Retry-After/TTL i redirecty wielu kandydatów Unknown | Zachować obecny Client i brak retry; nie wpisać wymyślonych nagłówków ani hostów. 0 decode/download obecnie. |
| G12 | Release wizerunku, marek i osób trzecich; jurysdykcja PD i prawa nagrania często Unknown | Per asset/use review. CC0/PDM/CC BY nie zastępują release; bez gwarancji prawnej dla całej kolekcji. |
| G13 | Każdy nowy host readiness NOT_RUN, aktywna rejestracja cache Unknown | Source/cache match nie jest działającą instalacją. Osobny host/provider/category proof, żadnego transferu readiness. |
| G14 | Brak odsłuchu i oglądania plików | Nie oceniono wartości artystycznej, szumu, jakości footage ani treści wariantu. T20 odrębnie od decode. |
| G15 | OUT_OF_CORE wymaga konta/key/opłaty/custom licence | Nie aktywowano tych usług. „Free” na stronie nie usuwa ograniczeń API i wykorzystania reklamowego. |
| G16 | OpenMoji/Fontsource/Google Fonts/Archive/Openverse mogą powielać assety | Liczyć nową drogę oddzielnie od nowego pliku; dedup per asset/version/hash, nie po nazwie providera. |

Rejestr źródeł obejmuje także próby nieudane. READ oznacza odczyt treści w badaniu lub odziedziczony udokumentowany odczyt specjalisty, a nie ponowny odczyt każdej strony przez leada. INDEXED_EXCERPT oznacza ograniczony widok z narzędzia wyszukującego. BLOCKED oznacza, że odczyt wskazany w notatce nie dostarczył pełnej treści. Pełne `claim`, `prior_read_status` i notatki zachowano w sources.json. Zestawienie liczb jest w summary.json.
