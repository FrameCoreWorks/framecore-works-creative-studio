# Plan małych prób — wszystkie NOT_RUN

To przyszły, odrębnie zatwierdzony etap. W DR-04 nie wykonano download, decode, instalacji, importu fontów/3D ani odsłuchu. Własny `verify_artifacts.py` sprawdza tylko dokumenty.

Wspólny warunek wejścia: Claude oceni projekt, użytkownik zatwierdzi konkretny scope wykonania, provider ma odczytane warunki, domeny i dopuszczony asset. Realny host/model, nie fałszywe `claude_code` w Codex. Małe testy mają osobny katalog poza pluginem, żadne stare pliki nie są nadpisywane. Nie przenosić proof między hostami.

Budżet jednostkowy: 1 provider/category, 1 query ≤240 znaków, maks. 3 wyniki, do 6 metadata GET i 1 download; serial ≥1 s lub większy interwał providera; metadata ≤8 MiB, plik ≤32 MiB, preferowany ≤5 MiB. Runtime limit 30 get/Client pozostaje dodatkową granicą, nie celem. Max 5 redirectów, 25 s socket / 60 s odczyt / 30 s ffprobe / 90 s full decode, do 40 MP. Audio próbka najlepiej ≤15 s, wideo ≤10 s, jeśli oficjalny wariant istnieje; to warunki planu, nie wbudowany limit długości. Żadnego automatycznego transkodowania całego dużego pliku tylko dla spełnienia limitu. Brak małego wariantu = odroczenie.

Koszt: 0 opłaty pobrania tylko tam, gdzie potwierdzają to warunki; koszt transferu i pracy lokalnej Unknown. Nie korzystać z próbnych kredytów/płatnej licencji. Każde 401/403/429/challenge/network_blocked → stop, zachować trace, bez dalszej federacji, bez workaroundu. Jedna ręcznie rozważona próba przejściowej awarii tylko według istniejącego kontraktu. Testy fault injection używają lokalnych tekstowych fixtures/test server, nie prowokują dostawcy.

| ID | Wejścia i cel | Oczekiwane wyjście / błąd | Limity i właściciel | Status |
|---|---|---|---|---|
| T01 | Adapter + odczytany query endpoint; 1 zapytanie, 3 results | stable IDs, source_page, creator, rights, variants; bez pliku i bez proof ready | wspólny metadata budget; wykonawca adaptera | NOT_RUN |
| T02 | 1 asset CC0/CC BY i 1 NC/ND/Unknown; licence page + metadata | CC0/BY kwalifikuje tylko ten asset, NC/ND/Unknown `rights_blocked` przed download | ≤4 metadata reads, 0 binariów; prawa + wykonawca | NOT_RUN |
| T03 | CC BY bez autora, SA bez i ze świadomą akceptacją | brak autora blocked; SA nie staje się eligible automatycznie; credits zachowane | lokalne fixtures; 0 sieci; wykonawca | NOT_RUN |
| T04 | NASA audio z realnym manifestem, item-specific use review | `review_nasa`; bez notatki odmowa, techniczna próba nie otwiera production proof | 1 small original/official rendition ≤5 MiB; wykonawca NASA | NOT_RUN |
| T05 | Archive item z 2 plikami o różnych lub niejasnych prawach | nie dziedziczyć blanket licencji na każdy plik; brak dowodu = blocked | ≤6 metadata reads, max 1 ≤5 MiB plik; wykonawca Archive | NOT_RUN |
| T06 | Realny variant URL; signed results; exact byte/hash jeśli advertised | podpis zachowany, właściwy variant, bytes/hash pass; podmieniony URL → `untrusted_result` | 1 plik, bez mutacji produkcyjnych danych; wykonawca core | NOT_RUN |
| T07 | Usunięty/wygasły URL lub zmieniony wariant (lokalna fixture) | czytelny http_error/transport trace; nowy search do nowej tożsamości, brak cichego wyboru innego pliku | 0 real network, 1 fixture request; wykonawca network | NOT_RUN |
| T08 | MIME JPEG + HTML payload, wrong extension, octet-stream + poprawne bytes | HTML refused; real decode rozstrzyga medium, mismatch jawny, brak aktywnego wykonania | text fixtures + autorska minimalna test fixture przy implementacji; ≤1 MiB; QA | NOT_RUN |
| T09 | Redirect do niezatwierdzonej domeny, credentials URL, >5 redirects | `unapproved_host`/`unsafe_url`/`redirect_limit`; żądanie do obcej domeny nie wykonywane | loopback fixtures, 0 zewnętrznego ruchu; QA | NOT_RUN |
| T10 | 401,403,429,challenge,egress refusal, Retry-After fixture | stop i trace; zero kolejnych providerów/ponowień, właściwe next_action | 5 niezależnych fixtures, zero provider calls; QA | NOT_RUN |
| T11 | ETag/304, max-age,no-store,no-cache,private, --fresh | zgodność obecnego cache; trace rozróżnia cache_hit/revalidated/network; bez obietnicy If-Modified-Since | local fixture, ≤6 GET; wykonawca cache | NOT_RUN |
| T12 | Realny obraz/audio/wideo w obsługiwanym formacie | pełny decode, kind zgodny z kategorią, oryginał zachowany; brak kodeka → decoder_missing | limity wspólne; runtime QA | NOT_RUN |
| T13 | Future SVG: script/event/external image/DTD; poprawna prosta ikona | aktywne refs odmowa, brak sieci, sanitizer/preview w odrębnym output; nie przyznawać safety na samym XML parse | ≤256 KiB, timeout ≤5 s, 1 proces; wykonawca formatów + świeży reviewer | NOT_RUN |
| T14 | ZIP: ..,absolute,symlink,nested bomb, >100 members, >128 MiB deklarowane | obecny tryb bez ekstrakcji; future extractor odrzuca niebezpieczne entries przed zapisem; CRC/image checks | handcrafted metadata fixtures, bez realnej bomby; QA | NOT_RUN |
| T15 | Font: OFL i RFN z jednej rodziny, jeden wariant | notices + version/subset/weight/style; brak instalacji fontu; tekst renderowany ≠ redystrybucja font software | 1 font ≤1 MiB, izolowana walidacja; wykonawca fontów | NOT_RUN |
| T16 | Ikona per-file z wyjątkiem licencyjnym i kolekcja o innej licencji | powiązać exact element z właściwymi notices; kolekcja MIT/ISC nie nadpisuje wyjątku | 2–3 metadata records, 0 pobrań przed kwalifikacją; wykonawca Iconify | NOT_RUN |
| T17 | Sidecar/envelope po jednym zatwierdzonym pobraniu | source/id/creator/license/variant/date/hash/trace i runtime provenance; schema valid; unexecuted listening/visual review jawne | plik + sidecar + envelope ≤40 MiB łącznie; integrator | NOT_RUN |
| T18 | Host proof z innej kategorii/hosta, stale >24h i technical-only | odmowa, brak transferable ready; nowe rzeczywiste verify wymagane | local fixtures, 0 provider calls; runtime QA | NOT_RUN |
| T19 | Dwa mirror IDs do tych samych bytes + ponowne pobranie do zajętej ścieżki | hash-based duplicate wskazany bez usuwania źródła; output_exists chroni oba pliki | 2 approved ≤1 MiB files lub own fixtures; integrator | NOT_RUN |
| T20 | Odsłuch/wizualna ocena wybranego małego assetu po legalnym decode | człowiek ocenia szum/artifacts/treść/przydatność; metadata test nie zalicza tej próby | ≤1 asset/kategoria, lokalnie, bez uploadu; użytkownik/Studio | NOT_RUN |

Akceptacja przyszłego providera wymaga co najmniej T01–T03, T06–T12, T17–T18 oraz właściwych testów domenowych. Dla Archive obowiązuje T05, SVG T13/T16, fontów T15. T20 jest odrębną akceptacją produkcyjną. Nie planować od razu pełnego katalogu ani kilkuset pobrań.
