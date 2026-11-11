# Dostawcy obrazów, wektorów, fontów i 3D

Stan badania 2026-11-11. Punktem odniesienia jest FrameCore Open Assets 0.5.0, commit `889471fcdbc2216ddc465715eff0e82784d5b8ee` z 2026-11-06. Aktualna lista ma 15 identyfikatorów dostawców i 24 ścieżki. Obsługa `graphics` obejmuje raster lub wybrany ZIP tekstur, z zachowaniem ZIP bez ekstrakcji. SVG, typografia i samodzielne pliki 3D wymagają rozszerzenia kontraktu lub wspólnej kontroli formatu. [Audyt baseline](../baseline/BASELINE.md)

Dwa kandydaty publicznego API z największą wartością dla obecnych luk to Iconify (skalowalne ikony) i Fontsource (fonty z podzbiorami i stabilnymi wariantami). Oba wymagają nowych reguł dla odpowiedniego formatu i licencji w istniejącej polityce Open Assets. Rozszerzenie PhyloPic o `vectorFile` może korzystać z tej samej walidacji SVG. Art Institute of Chicago daje IIIF i jednoznaczny negatywny przykład praw w metadanych, z mniejszą wartością dla współczesnego stocku. Brak pełnego kandydata automatycznego na współczesne fotografie produktowe lub szeroką bibliotekę gotowych ilustracji postaci.

| Kwalifikacja dostawcy | Pozycje |
| --- | --- |
| CORE_CANDIDATE | Iconify, Fontsource. Gotowość formatu i praw warunkowa, host NOT_RUN. |
| OPTIONAL | Google Fonts Files, Openverse discovery, Art Institute of Chicago, PhyloPic SVG, Smithsonian Open Access, OpenMoji — wydania autora. |
| MANUAL | Open Peeps, Quaternius. |
| OUT_OF_CORE | Unsplash z kluczem i odrębnymi regułami API. |
| REJECTED | unDraw, ShareTextures jako integracje wtyczki. |

`DOCUMENTED` obejmuje oficjalne deklaracje, specyfikacje i odczytane rekordy metadanych. Pole `record_read: true` potwierdza odczyt rekordu. `CODE_INSPECTED` oznacza odczyt przypiętego kodu lub repozytoryjnych metadanych. `AUTHOR_TEST` oznacza wynik deklarowany przez autora w podanym zakresie. `OWN_TEST` odnosi się wyłącznie do kontroli dokumentów w walidatorze, jeśli zostanie wykonana. `NOT_RUN` oznacza niewykonaną próbę pobrania, decode, integracji lub hosta. `Unknown` oznacza nieustaloną informację. `DERIVED` oznacza proponowaną kwalifikację, architekturę lub test. Brak pobrania binariów i oceny artystycznej. Zestawienie [JSON katalogu](catalog.json), [rekordów](records.json) i [dowodów](sources.json).


## Iconify

Zakres `DEEP`. NEW_PROVIDER. Provider `CORE_CANDIDATE`. Asset `CONDITIONAL: wybrane ikony po weryfikacji upstream, obsłudze notice i rozbudowie tej samej polityki praw; SA i Unknown poza automatycznym zakresem.` Host `NOT_RUN`. Priorytet `P0`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i zastosowanie** — Iconify OÜ; autorzy zbiorów. Kategorie `graphics`, `icons`, `svg`. [Projekt](https://iconify.design/)
- **Nowość** — Brak Iconify w baseline. PhyloPic ma inny profil i istniejącą ścieżkę PNG.
- **Dostęp i automatyzacja** — `PUBLIC_API`. Brak klucza i konta; bezpłatny serwer publiczny. Oficjalne użycie maszynowe do selektorów ikon i generowania SVG. Unikać zbędnych zapytań i pobierania hurtowego.
- **Wyszukiwanie** — GET /search?query=…; opcjonalnie prefix, prefixes, category, limit, start. Limit 32–999, domyślnie 64; słowa kluczowe i nazwy; gwarancja obsługi języka polskiego Unknown.
- **Szczegóły** — prefix:name; GET /collection?prefix=…, /{prefix}.json?icons=…, /collections; autor i licencja na poziomie kolekcji, sprawdzić wyjątki upstream. Data per ikona Unknown.
- **Plik i warianty** — GET /{prefix}/{icon}.svg; SVG dynamiczne. SVG i JSON metadanych; PNG tylko jeśli jawnie wyprowadzony i zweryfikowany jako lokalna pochodna. Bazowy viewBox. Udokumentowane warianty width/height/color/rotate/flip; zapisać parametry w sidecar. Alfa po rasteryzacji do weryfikacji. FPS/audio nie dotyczy.
- **Prawa** — Licencje dzieł per ikona, punktem startu są collections.info. Tabler MIT, Lucide ISC z wyjątkami Feather MIT. Kod i dokumentacja Iconify nie określają praw ikony. Zachować notice; wykluczyć marki i inne prawa niepotwierdzone.
- **Transport i cache** — api.iconify.design. Oficjalne hosty zapasowe api.simplesvg.com i api.unisvg.com, bez rotacji po blokadzie. /last-modified?prefixes=… do unieważniania cache. 400/404 udokumentowane; limit żądań, ETag, Retry-After, podpisane URL i warunki redirectu Unknown.
- **Ryzyko i adapter** — Treść SVG aktywna, źródłowe wyjątki licencyjne, logotypy, aliasy, wynik może zmienić się bez zmiany nazwy. Średni. Nowy typ SVG z weryfikacją statycznego podzbioru i dotychczasowy sidecar. Najpierw pojedyncza kolekcja Tabler bez marek, potem Lucide z wyjątkiem Feather.
- **Źródła pierwotne** — [v-icon-api](https://iconify.design/docs/api/), [v-icon-query](https://iconify.design/docs/api/queries.html), [v-icon-search](https://iconify.design/docs/api/search.html), [v-icon-lucide](https://icon-sets.iconify.design/lucide/camera/), [v-icon-tabler](https://icon-sets.iconify.design/tabler/camera/), [v-icon-openmoji](https://icon-sets.iconify.design/openmoji/avocado/), [v-lucide-lic](https://lucide.dev/license), [v-tabler-lic](https://github.com/tabler/tabler-icons/blob/845a74971e5f39fe1360a9987e4ae327ef1c90b9/LICENSE), [v-cc-sa](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en), [v-icon-svg](https://iconify.design/docs/api/svg.html).

Pilotaż ograniczony do Tabler i bez logotypów. Potem sprawdzić Lucide na parze ikona rodzima/ikona pochodna Feather i zapisać właściwy notice. Label serwisu o braku atrybucji w reklamie nie znosi obowiązku licencji dołączanej do kopii assetu.

Rekordy z `record_read: true` (3)

- `lucide:camera` — camera, Lucide Contributors, ISC. Odczyt rekordu i licencji autora. camera nie występuje w jawnej liście ikon pochodnych Feather na stronie licencji. [Rekord](https://icon-sets.iconify.design/lucide/camera/)
- `tabler:camera` — camera, Paweł Kuna, MIT. Odczyt rekordu i licencji autora przypiętej do commita 2026-11-10. [Rekord](https://icon-sets.iconify.design/tabler/camera/)
- `openmoji:avocado` — avocado, OpenMoji, CC-BY-SA-4.0. Odczyt rekordu potwierdza SA i pokrycie się części katalogów. [Rekord](https://icon-sets.iconify.design/openmoji/avocado/)


## Fontsource

Zakres `DEEP`. NEW_PROVIDER. Provider `CORE_CANDIDATE`. Asset `CONDITIONAL: pilotaż OFL-1.1 po ustaleniu wersjonowanego LICENSE/copyright tego pliku i rozszerzeniu polityki oraz formatu fontów.` Host `NOT_RUN`. Priorytet `P1`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i zastosowanie** — Projekt Fontsource; rodziny od autorów, dystrybucja CDN jsDelivr. Kategorie `fonts`, `typography`. [Projekt](https://fontsource.org/)
- **Nowość** — Fontów i Fontsource brak w baseline. Konkretne warianty webowe i podzbiory uzupełniają statyczny upstream Google Fonts.
- **Dostęp i automatyzacja** — `PUBLIC_API_CDN`. Publiczny odczyt bez konta/klucza. Sponsoring proszony, bez opłaty wskazanej w docs. Read-only API dokumentowane dla dowolnego klienta HTTP oraz wersjonowany CDN; użycie i cache z fair use.
- **Wyszukiwanie** — GET /v1/fonts i filtry id, family, subsets, weights, styles, variable, category, version, type. Paginacja i pełnotekstowy silnik API Unknown; docs zwracają tablicę, można filtrować lokalnie.
- **Szczegóły** — GET /v1/fonts/{id}; stabilny slug z wersją, licencja, źródło, lastModified, npmVersion zaobserwowane. Twórcę brać z uprawnionych metadanych upstream.
- **Plik i warianty** — Bezpośrednie URL z variants.*.*.*.url, oficjalny cdn.jsdelivr.net; zachować dokładną wersję npm. WOFF2/WOFF/TTF. TTF dla docelowego narzędzia motion/desktop po sprawdzeniu, WOFF2 na potrzeby web. Waga, styl, podzbiór, statyczny/zmienny. Latin-ext nie zastępuje sprawdzenia pełnego zestawu znaków do projektu. Rozmiar/FPS/alfa/audio nie dotyczy.
- **Prawa** — Id w JSON i rekord źródłowy, exact package license i notices. OFL wymaga zachowania tekstu i notices w dystrybucji, reguluje RFN i sprzedaż samego fontu. Upstream licencja TTF jako dowód pochodzenia, wersjonowany pakiet jako dowód konkretnej dystrybucji. Osobne licencje kodu, metadanych i fontu.
- **Transport i cache** — api.fontsource.org, cdn.jsdelivr.net. Exact SemVer cache długotrwały. 400/404/422/429/500 i fair use, twardy limit 2500/10 s nie jest zalecaną przepustowością. ETag, Last-Modified HTTP, Retry-After, zachowanie redirectu i pełna lista dalszych hostów Unknown.
- **Ryzyko i adapter** — FontSource i Google Fonts mogą prowadzić do tej samej rodziny; podzbiór vs pełny TTF; RFN i transformacje; część binariów może być nieobsługiwana przez renderery. Średni/wysoki. Wpiąć do licencji istniejącej kategorii rozszerzonej o fonts, walidacja struktury/fontu i glyph coverage, brak instalacji systemowej; rejestrować pakiet, wersję i podzbiór.
- **Źródła pierwotne** — [v-font-api](https://fontsource.org/docs/api/introduction), [v-font-search](https://fontsource.org/docs/api/fonts), [v-font-detail](https://fontsource.org/docs/api/font-id), [v-font-cdn](https://fontsource.org/docs/getting-started/cdn), [v-font-inter](https://fontsource.org/fonts/inter), [v-font-instrument](https://api.fontsource.org/v1/fonts/instrument-serif), [v-google-inter-meta](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/inter/METADATA.pb), [v-google-inter-lic](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/inter/OFL.txt), [v-google-ins-meta](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/instrumentserif/METADATA.pb), [v-google-ins-lic](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/instrumentserif/OFL.txt), [v-ofl](https://openfontlicense.org/open-font-license-official-text/).

Rekordy z `record_read: true` (2)

- `instrument-serif` — Instrument Serif, Rodrigo Fuenzalida, Jordan Egstad (upstream), OFL-1.1. Odczyt rzeczywistego JSON, npmVersion 5.3.0, version v5, lastModified 2025-09-05, type google; wybrane warianty, bez weryfikacji dokładnego notice pakietu ani transferu. [Rekord](https://api.fontsource.org/v1/fonts/instrument-serif)
- `inter` — Inter, Rasmus Andersson (upstream), OFL-1.1. Odczyt strony rekordu. Dokładne CDN/format/wersja pakietu Unknown w tym rekordzie. [Rekord](https://fontsource.org/fonts/inter)


## Google Fonts Files

Zakres `DEEP`. NEW_PROVIDER. Provider `OPTIONAL`. Asset `CONDITIONAL: pliki pojedynczych rodzin ze zweryfikowaną OFL-1.1 i provenance. Apache-2.0/UFL poza pilotem.` Host `NOT_RUN`. Priorytet `P1`. Dowody `DOCUMENTED`, `CODE_INSPECTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i zastosowanie** — Google Fonts; właściciele poszczególnych fontów. Kategorie `fonts`, `typography`. [Projekt](https://github.com/google/fonts)
- **Nowość** — Brak katalogu fontów w baseline; źródłowy TTF i licencja różnią się od pochodnych dystrybucji Fontsource. Dedup per rodzina i wersja.
- **Dostęp i automatyzacja** — `STATIC_REPOSITORY`. Publiczne repo Git bez klucza w udokumentowanej drodze sync. Oddzielny Developer API wymaga klucza. README wspiera maszynową synchronizację Git i self-host. Pełne ZIP według README >1 GB, poza ścieżką małych próbek.
- **Wyszukiwanie** — Lokalnie po METADATA.pb, nazwie, kategorii, podzbiorach, osiach, opcjonalnie opisie en-US. Paginacja lokalna; Developer API wyłączone w tej ścieżce.
- **Szczegóły** — Folder rodziny i wariant `fonts.filename` przy pinie repo, `designer`, `date_added`, `license`, źródłowy commit gdy obecny.
- **Plik i warianty** — Oficjalne pliki repo przy przypiętym SHA, bez pobierania całego archiwum; transport pojedynczego pliku do ustalenia na hoście. TTF; METADATA.pb jest tekstowym formatem metadanych. OFL.txt lub właściwy plik licencji. Static regular/italic, font zmienny i zakresy osi tam, gdzie wskazane; deklarowane podzbiory to wskazówka przed sprawdzeniem cmap.
- **Prawa** — Top-level license tree jako wskazówka; konkretne LICENSE/OFL.txt i METADATA.pb. Większość OFL-1.1, są także Apache-2.0/UFL; prawa do grafik/biogramów poza zakresem.
- **Transport i cache** — github.com, dalsze hosty rzeczywistego transportu, zakres GET, redirecty, limity, ETag, Retry-After i podpisane URL Unknown w tej pracy. Pin SHA i lokalny indeks.
- **Ryzyko i adapter** — Duże repozytorium; family path nie jest samą licencją; treść METADATA i nagłówki fontu mogą się różnić; licencja per plik i notices/RFN. Średni/wysoki. Statyczne repo jako źródło proweniencji i pełnych TTF dla tego samego modelu fonts. Unikać dublowania rodzin i pobrania całego repo.
- **Źródła pierwotne** — [v-google-repo](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/README.md), [v-google-api](https://developers.google.com/fonts/docs/developer_api), [v-google-meta](https://googlefonts.github.io/gf-guide/metadata.html), [v-google-inter-meta](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/inter/METADATA.pb), [v-google-inter-lic](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/inter/OFL.txt), [v-google-ins-meta](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/instrumentserif/METADATA.pb), [v-google-ins-lic](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/instrumentserif/OFL.txt), [v-ofl](https://openfontlicense.org/open-font-license-official-text/).

Statyczny snapshot w dokumentach i metadanych odczytano z commita `5bb28733cec313b63fbd415b574b5ae35c8aa8b8` z 2026-11-08. Ewentualny importer może wykorzystywać ten sam model praw i deduplikacji co Fontsource.

Rekordy z `record_read: true` (2)

- `ofl/inter` — Inter, Rasmus Andersson, OFL-1.1. Konektor GitHub, odczyt METADATA.pb i OFL.txt; commit repo 5bb28733cec313b63fbd415b574b5ae35c8aa8b8. Latin-ext deklarowany. [Rekord](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/inter/METADATA.pb)
- `ofl/instrumentserif` — Instrument Serif, Rodrigo Fuenzalida, Jordan Egstad, OFL-1.1. Konektor GitHub, odczyt METADATA.pb i OFL.txt; commit repo 5bb28733cec313b63fbd415b574b5ae35c8aa8b8. Latin-ext deklarowany. [Rekord](https://github.com/google/fonts/blob/5bb28733cec313b63fbd415b574b5ae35c8aa8b8/ofl/instrumentserif/METADATA.pb)


## Openverse

Zakres `DEEP`. NEW_PROVIDER. Provider `OPTIONAL`. Asset `ORIGIN_REQUIRED: licencja, twórca, wariant i automatyzacja do ponownego ustalenia u dostawcy oryginału.` Host `NOT_RUN`. Priorytet `P1`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i zastosowanie** — Projekt Openverse / WordPress Foundation (wg ToS); media u wydawców. Kategorie `photos`, `graphics`, `audio`, `discovery`. [Projekt](https://openverse.org/)
- **Nowość** — Nie ma tego agregatora w baseline. Wiele rekordów to te same pliki co w Commons, muzeach i innych aktualnych providerach.
- **Dostęp i automatyzacja** — `PUBLIC_DISCOVERY_API`. Anonimowe bezpłatne API z limitami, opcjonalna rejestracja dla podwyższonych limitów. ToS zastrzega przyszłe opłaty commercial/heavy. API służy wyszukiwaniu maszynowemu, zakaz scrapingu indeksu i obchodzenia limitów. Warunki hosta źródłowego rozstrzygają pobranie.
- **Wyszukiwanie** — GET /v1/images/ i /v1/audio/, query, filtry licencyjne i źródłowe, paginacja. Nazwy i wartości filtrów oraz limity planu potwierdzić z aktualnego OpenAPI przed wdrożeniem; języki Unknown.
- **Szczegóły** — Endpointy szczegółów image/audio per ID; zachować identyfikator indeksu, rekord dostawcy, twórcę i URL do rekordu źródłowego. Data/parametry mogą być niepełne.
- **Plik i warianty** — Pobranie przez istniejący/zweryfikowany adapter origin. W URL z indeksu może być miniatura, wygasły wariant albo niezweryfikowany host; użyć jako wskazówki do lookup. Zależne od oryginału; kategorie obrazy/audio z obecnego API. Preview i źródłowy URL mają oddzielne role; finalny format, rozmiar i alfa do weryfikacji u źródła.
- **Prawa** — Mieszana deklaracja źródła. ToS nie przypisuje praw do plików i wymaga niezależnego sprawdzenia hosta oraz licencji; MIT w nagłówku specyfikacji to nie licencja mediów. Status licencji zbioru metadanych do osobnego ustalenia przed jego dystrybucją.
- **Transport i cache** — api.openverse.org plus niejednorodne hosty upstream. Nagłówki rate-limit według specyfikacji; aktualne liczby, ETag, Last-Modified i Retry-After Unknown. Dalszy odczyt web zwrócił 403; zachować stop po blokadzie.
- **Ryzyko i adapter** — Duplikaty, błędne lub stare deklaracje, martwe linki, prawa wizerunku/marek, komercyjny koszt w przyszłości, obowiązek wskazania Openverse bez sugerowania endorsementu. Średni discovery-only. Po wyniku mapowanie do źródłowego ID i dedup. Bez automatycznego pobierania dowolnego wskazanego URL.
- **Źródła pierwotne** — [v-openverse-api](https://api.openverse.org/v1/), [v-openverse-tos](https://docs.openverse.org/terms_of_service.html), [v-openverse-git](https://github.com/WordPress/openverse/blob/50135c93a3630f908b7bbd8bfe5da8acd96f3ce3/documentation/terms_of_service.md).

Rekordy 0/2. Specyfikację odczytano z widoku indeksowanego (`INDEXED_EXCERPT`). Późniejszy odczyt bezpośredni jest oznaczony `BLOCKED` (HTTP 403). Zakończono próby w tym kanale. Aktualny limit liczbowy, domeny oryginałów i ich warunki pozostają Unknown.



## Art Institute of Chicago

Zakres `DEEP`. NEW_PROVIDER. Provider `OPTIONAL`. Asset `CONDITIONAL: is_public_domain=true i jawne prawa konkretnego obrazu; formalne Image Licensing i ToS nieodczytane (403). is_public_domain=false odrzucić niezależnie od image_id.` Host `NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`, `Unknown`.

- **Właściciel i zastosowanie** — Art Institute of Chicago. Kategorie `graphics`, `photos`, `cultural-heritage`, `iiif`. [Projekt](https://api.artic.edu/docs/)
- **Nowość** — Brak w aktywnych 15; wcześniejsze wykluczenie i search 403 w próbie Work 2026-10-28 (historyczny baseline). Nowa bezpośrednia kolekcja i IIIF, kategoria reprodukcji już pokryta.
- **Dostęp i automatyzacja** — `PUBLIC_API_IIIF`. Bez konta i klucza; 60/min anonimowo; HTTPS i nagłówek AIC-User-Agent z projektem i adresem kontaktowym zalecane. API do integracji w aplikacjach. Instytucja dopuszcza lokalne kopie IIIF w małej skali, zaleca 1 wątek, odstęp 1 s i 843 px. Duży zbiór metadanych osobnym oficjalnym dumpem.
- **Wyszukiwanie** — GET /api/v1/artworks/search?q=… z `query[term][is_public_domain]=true`; możliwe GET/POST i Query DSL. `page`, `limit`, `fields`; docs paginacji 1000/search. Tagi term_titles/subject_titles; wsparcie języków Unknown.
- **Szczegóły** — GET /api/v1/artworks/{id}; `artist_title`, `date_display`, `image_id`, `alt_image_ids`, `is_public_domain`, `copyright_notice`, `config.iiif_url`. Per-PD IIIF manifest pod /manifest.json.
- **Plik i warianty** — IIIF 2.0 na www.artic.edu: /iiif/2/{image_id}/full/{size}/0/default.jpg, z config.iiif_url zatwierdzonym przez allowlist. JPEG IIIF i metadane JSON/IIIF; żądania obrazu bez alfa/audio. 112/200/400/600/800/843 px szer.; dla PD 1200/1686 px, preferowane 843. Oddzielny alt_image_id wymaga odrębnej kontroli. Wartość thumbnail.width/height nie jest zmierzonym plikiem.
- **Prawa** — Metadane w JSON CC0 poza description CC BY 4.0, podlegają ToS. is_public_domain dotyczy dzieła; prawa konkretnego obrazu i ograniczenia strony trzeba zweryfikować. Oficjalne strony licencyjne i ToS zwróciły 403.
- **Transport i cache** — api.artic.edu, www.artic.edu; HTTP przekierowuje na HTTPS. Cache zalecany przez autora. ETag/Last-Modified/Retry-After, signed URLs i dalsze redirecty Unknown; historyczny 403 Work.
- **Ryzyko i adapter** — Publiczny rekord, miniatura lub image_id mogą istnieć także dla chronionego dzieła. Historyczny 403 i nierozpoznane aktualne warunki; limity rozdzielczości. Niski/średni po potwierdzeniu praw i hosta. Ograniczyć do JPEG, osobnych wariantów i wyszukiwania małego; osobna ścieżka do dumpa tylko gdy potrzeba.
- **Źródła pierwotne** — [v-aic-api](https://api.artic.edu/docs/), [v-aic-rights](https://www.artic.edu/image-licensing), [v-aic-tos](https://www.artic.edu/terms), [v-aic-seurat](https://api.artic.edu/api/v1/artworks/27992), [v-aic-thomas](https://api.artic.edu/api/v1/artworks/129884), [v-aic-dump](https://github.com/art-institute-of-chicago/api-data/blob/8c7e65089ac8145a241f237e065c81861a35f359/README.md), [v-cc0](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en).

Strony Image Licensing i Terms mają status `BLOCKED` (HTTP 403). Dwa rekordy JSON odczytano. Wcześniejszy 403 na wyszukiwaniu pochodził z próby Work 2026-10-28. Harmonogram zrzutu jest opisany jako tygodniowy w API docs i miesięczny w README repo. Bieżąca częstotliwość Unknown. [Historyczna weryfikacja Work](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/verification/open-assets-0.2.0-work.json)

Rekordy z `record_read: true` (2)

- `27992` — A Sunday on La Grande Jatte — 1884, Georges Seurat, Public domain wg flagi dzieła; licencja reprodukcji Unknown w tej weryfikacji. JSON: is_public_domain=true, copyright_notice=null, thumbnail.width=9310 i height=6237 jako wartości metadanych; JPEG nieodczytany, przykładowy IIIF 843 px w docs. [Rekord](https://api.artic.edu/api/v1/artworks/27992)
- `129884` — Starry Night and the Astronauts, Alma Thomas, RESTRICTED. JSON: is_public_domain=false, obecne image_id e966799b-97ee-1cc6-bd2f-a94b4b8bb8f9, copyright Estate of Alma Thomas / Artists Rights Society. Żaden wariant niekwalifikowany. [Rekord](https://api.artic.edu/api/v1/artworks/129884)


## PhyloPic — wariant SVG

Zakres `SURVEY`. EXISTING_NEW_CATEGORY. Provider `OPTIONAL`. Asset `CONDITIONAL: CC0/PDM i obsługiwane CC BY z wymaganym twórcą, licencją i atrybucją; SA/NC wg istniejącego filtra.` Host `NOT_RUN`. Priorytet `P1`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`, `Unknown`.

- **Właściciel i zastosowanie** — PhyloPic / T. Michael Keesey i autorzy sylwetek. Kategorie `graphics`, `silhouettes`, `svg`. [Projekt](https://www.phylopic.org/)
- **Nowość** — `phylopic` dostarcza istniejące rasterFiles PNG. Dodać vectorFile w tym samym providerze; baseline nie ma ścieżki SVG.
- **Dostęp i automatyzacja** — `PUBLIC_API_EXISTING_ADAPTER_EXTENSION`. Istniejąca droga publiczna, oficjalne receptury bez klucza i konta. Oficjalne receptury API. Nie rozbudowywać skali pobierania.
- **Wyszukiwanie** — Istniejący lookup taksonu/filtry i build/page; ponowne ustalenie polityki języków poza zmianą.
- **Szczegóły** — GET /images/{uuid}; contributor i per-image license w źródle.
- **Plik i warianty** — `_links.vectorFile` wskazany w metadanych; `sourceFile` jest odrębnym wariantem. PNG istniejące, nowy SVG wektorowy. Wg docs czarna sylwetka na przezroczystym tle, pochodna sourceFile. Zweryfikować technicznie w pilotażu.
- **Prawa** — Każda sylwetka ma własne warunki. Generowanie SVG przez PhyloPic nie zmienia licencji oryginału.
- **Transport i cache** — api.phylopic.org i oficjalny host zasobu z runtime. V2 API docs i przykładowy JSON web 403/niedostępny. ETag/limity/Retry-After/redirect Unknown.
- **Ryzyko i adapter** — SVG aktywny; automatyczna wektoryzacja może zmienić wygląd; ta sama sylwetka w dwóch wariantach. Rozszerzyć obecny adapter po wspólnej kontroli SVG z Iconify i testach praw.
- **Źródła pierwotne** — [v-phylopic-api](https://www.phylopic.org/articles/api-recipes), [v-phylopic-lic](https://www.phylopic.org/articles/image-usage).



## Smithsonian Open Access

Zakres `SURVEY`. NEW_PROVIDER. Provider `OPTIONAL`. Asset `CONDITIONAL: oznaczenie CC0 dla danego zasobu 2D/3D; CC0 metadanych nie świadczy o dostępności ani prawach do medium.` Host `NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`, `Unknown`.

- **Właściciel i zastosowanie** — Smithsonian Institution. Kategorie `photos`, `graphics`, `cultural-heritage`, `3d`. [Projekt](https://www.si.edu/openaccess)
- **Nowość** — Brak w baseline. 3D obiektów muzealnych wnosi wartość inną niż istniejące fotoreprodukcje i tekstury.
- **Dostęp i automatyzacja** — `STATIC_DATASET_S3; KEYED_API_SEPARATE`. AWS S3 publiczne bez konta; oddzielny API publiczny wymaga klucza api.data.gov. Oficjalny otwarty dataset S3 i machine-readable JSONL; stary GitHub kieruje do AWS.
- **Wyszukiwanie** — S3 katalog per jednostka i shard. Własny indeks lokalny wymaga osobnej warstwy; API z kluczem poza zakresem.
- **Szczegóły** — JSONL i IIIF manifest dostępne wg FAQ; dokładne mapowanie rekordów/CC0 i spójność 3D Unknown.
- **Plik i warianty** — S3 per rekord po ustaleniu źródła, nie pełny mirror. Dokładne URL poszczególnych modeli Unknown. JPG/TIFF; glTF/GLB/OBJ; dane JSON/IIIF. OBJ 150k/full res według FAQ; warianty dla każdego modelu Unknown.
- **Prawa** — CC0 dla oznaczonych pozycji, instytucja zaleca minimalny credit. Prawa do innych elementów i warunki zewnętrznych mediów sprawdzić indywidualnie.
- **Transport i cache** — Bucket smithsonian-open-access, us-west-2. Aktualizacje tygodniowe wg AWS. Cache, limity, Retry-After, podpisane URL i dalsze hosty Unknown.
- **Ryzyko i adapter** — Wysoki koszt indeksowania, odrębna walidacja 3D/archiwów, nakładanie rekordów w Commons, niepełne prawa lub brak medium. Wysoki. Jeśli powstanie statyczny importer, wybrać jednostkę/podzbiór 3D i sprawdzić per-media CC0.
- **Źródła pierwotne** — [v-si-faq](https://www.si.edu/openaccess/faq), [v-si-aws](https://registry.opendata.aws/smithsonian-open-access/), [v-si-repo](https://github.com/Smithsonian/OpenAccess/blob/c2ac3e2a671755e03e1ec439ad7b9b0020636281/README.md), [v-cc0](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en).



## Open Peeps

Zakres `SURVEY`. NEW_PROVIDER. Provider `MANUAL`. Asset `CONDITIONAL: autorska biblioteka CC0 ze strony projektu, z zachowaniem pochodzenia poszczególnych komponentów.` Host `NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`, `Unknown`.

- **Właściciel i zastosowanie** — Pablo Stanley. Kategorie `graphics`, `illustrations`, `characters`. [Projekt](https://openpeeps.com/)
- **Nowość** — Brak w baseline; współczesna biblioteka modułowych ilustracji ludzi, odrębna od sylwetek taksonomicznych.
- **Dostęp i automatyzacja** — `MANUAL_LIBRARY`. Autor deklaruje bezpłatność. Warunki i obowiązkowe konto podczas pobierania u dystrybutora Unknown. Oficjalne API, statyczny manifest i zgoda na zautomatyzowane pobieranie Unknown.
- **Wyszukiwanie** — Ręczny wybór i kompozycja z elementów, brak udokumentowanej paginacji, API/języki Unknown.
- **Szczegóły** — Autor biblioteki i deklaracja praw znane. Maszynowe ID, data i licencja poszczególnych plików Unknown.
- **Plik i warianty** — Ręczna strona projektu z odnośnikiem do Gumroad; alternatywnie edycja w Blush; direct URLs Unknown. Autor opisuje wektorowe komponenty; komplet dokładnych formatów i wersji paczki Unknown. Włosy, twarze, ubrania, pozy; rozdzielczości i faktyczna alfa Unknown. FPS/audio nie dotyczy.
- **Prawa** — Autor deklaruje CC0 dla biblioteki. Prawo do konkretnego pliku potwierdzić w paczce; nie rozszerzać deklaracji na inne materiały Blush/Gumroad.
- **Transport i cache** — openpeeps.com, gum.co, blush.design jako odnośniki; cache/ETag/Last-Modified/Retry-After, dalszy download host i podpisy Unknown.
- **Ryzyko i adapter** — Dystrybutor i strona autorska to odrębne powierzchnie, plik ma zawierać dowód pochodzenia; aktywny SVG/archiwum przy ewentualnym imporcie. Brak adaptera API. Użycie manual lub import pliku już pobranego przez użytkownika.
- **Źródła pierwotne** — [v-peeps](https://openpeeps.com/), [v-cc0](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en).



## Quaternius

Zakres `SURVEY`. NEW_PROVIDER. Provider `MANUAL`. Asset `CONDITIONAL: część dawnych paczek deklaruje CC0; QAL ma ograniczenie redystrybucji. Ustalić dokładną paczkę i licencję; QAL poza automatyczną polityką.` Host `NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `AUTHOR_TEST`, `DERIVED`, `NOT_RUN`, `Unknown`.

- **Właściciel i zastosowanie** — Quaternius. Kategorie `3d`, `rigs`, `animation`, `textures`. [Projekt](https://quaternius.com/)
- **Nowość** — Brak w baseline; stylizowane zestawy i animacje humanoidalne są odrębne od obsługiwanych obrazów i tekstur ZIP.
- **Dostęp i automatyzacja** — `MANUAL_PACKS`. Wybrane standardowe paczki deklarują bezpłatność; Source/pełne warianty mogą być dla wspierających. Konto, koszt per wariant Unknown. Oficjalna zgoda na automatyzację i udokumentowane API Unknown.
- **Wyszukiwanie** — Ręczne strony paczek. API, filtry, języki i paginacja Unknown.
- **Szczegóły** — Slug i opis paczki, data i deklarowana licencja w przykładach. ID/licencja modeli wewnątrz paczki wymagają odczytania faktycznego archiwum w osobnym teście.
- **Plik i warianty** — Ręczne odnośniki w rekordach; brak potwierdzonego hosta finalnego, wersji i URL pliku. FBX/OBJ/glTF/GLB/Blend zależnie od paczki i poziomu. Atlas/indywidualne materiały według FAQ. Standard/Source i ewentualne dodatkowe warianty; rig oraz deklarowane animacje. FPS, nazwy klipów i ścieżki zależności Unknown.
- **Prawa** — Starsze rekordy i FAQ CC0; nowsza QAL v1.0 dla wydań pod QAL dopuszcza użycie w gotowym produkcie i zakazuje dystrybucji samego assetu, także zmodyfikowanego. Nie uogólniać jednej licencji.
- **Transport i cache** — quaternius.com; finalny transport, limity, ETag, Last-Modified, cache, Retry-After i podpisy Unknown.
- **Ryzyko i adapter** — FAQ i QAL mają różny zakres. Pakiet i wersja decydują; ryzyko płatnego rozszerzenia i niezabezpieczonych plików 3D/archiwów. Brak obecnie. Import lokalny wyłącznie po rozbudowie walidacji i potwierdzeniu licencji dokładnej wersji.
- **Źródła pierwotne** — [v-quat-license](https://quaternius.com/license.html), [v-quat-faq](https://quaternius.com/faq.html), [v-quat-anim](https://quaternius.com/packs/universalanimationlibrary.html), [v-quat-old](https://quaternius.com/packs/ultimatespacekit.html), [v-cc0](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en).

AUTHOR_TEST ograniczony do deklaracji autora Universal Animation Library dotyczącej silników Godot, Unity i Unreal. Nie przeprowadzono własnego testu modelu, animacji ani czasu importu.



## OpenMoji — wydania autora

Zakres `SURVEY`. DUPLICATE_MIRROR. Provider `OPTIONAL`. Asset `REVIEW_REQUIRED: CC BY-SA 4.0 dla grafiki, warunki adaptacji i atrybucji wymagają ręcznej decyzji.` Host `NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i zastosowanie** — HfG Schwäbisch Gmünd, Benedikt Groß, Daniel Utz i współtwórcy OpenMoji. Kategorie `graphics`, `icons`, `emoji`, `svg`, `png`. [Projekt](https://openmoji.org/)
- **Nowość** — Projekt nie ma wpisu w baseline, lecz ilustracje pokrywają się z kolekcją OpenMoji w nowym kandydacie Iconify; wydania autora dodają warianty PNG i są kanonicznym źródłem praw.
- **Dostęp i automatyzacja** — `STATIC_RELEASE_REPOSITORY`. Publiczne repozytorium i udokumentowana dystrybucja CDN; bez klucza w opisanej drodze. Koszt użycia 0 pod warunkami licencji. README opisuje maszynowe użycie paczek i CDN. Dokumentowane API pakietu npm działa jako interfejs lokalny, nie jako publiczne API wyszukiwania.
- **Wyszukiwanie** — Lokalny indeks data/openmoji.json z metadanymi emoji. Serwerowy search, jego filtry, paginacja i języki Unknown.
- **Szczegóły** — Kod Unicode dla emoji i pochodzenie projektu; różnicować wersję, kolor i kompozycję. Autor indywidualny i data konkretnego emoji Unknown.
- **Plik i warianty** — Wersjonowane GitHub Releases lub oficjalnie opisany UNPKG/jsDelivr; wybrać wersję, nie latest. SVG, PNG 72/618 px, eksperymentalne fonty. Dekodowanie i alfa NOT_RUN. Czarne/kolorowe, rozmiary 72 i 618 px wg README, podtypy Unicode zależnie od rekordu.
- **Prawa** — Grafika CC BY-SA 4.0, kod LGPL-3.0. Zachować atrybucję, licencję i oznaczenie zmian; SA stosować zgodnie z licencją dzieła.
- **Transport i cache** — github.com, unpkg.com, cdn.jsdelivr.net; redirecty, ETag, limity i podpisane URL Unknown.
- **Ryzyko i adapter** — Duplikaty Iconify; dziedziczenie SA; zewnętrzne prawa do treści lub znaków. Wybór finalnego wariantu wymaga kontroli. Statyczny importer opcjonalny wyłącznie jeśli potrzebny PNG i po uzgodnieniu procesu SA.
- **Źródła pierwotne** — [v-om-repo](https://github.com/hfg-gmuend/openmoji/blob/3e01de523ddefe9c5e46a7765b15efef04bf9002/README.md), [v-icon-openmoji](https://icon-sets.iconify.design/openmoji/avocado/), [v-cc-sa](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en).



## unDraw

Zakres `SURVEY`. NEW_PROVIDER. Provider `REJECTED`. Asset `MANUAL_ONLY: użycie ilustracji w konkretnym projekcie według własnych warunków autora; integracja i budowa zbioru wymagają odrębnej zgody.` Host `NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`, `Unknown`.

- **Właściciel i zastosowanie** — Katerina Limpitsouni. Kategorie `graphics`, `illustrations`, `svg`. [Projekt](https://undraw.co/illustrations)
- **Nowość** — Brak w baseline; współczesna biblioteka ilustracji wektorowych rozwiązuje istotną lukę wizualną, lecz warunki ograniczają integrację.
- **Dostęp i automatyzacja** — `MANUAL_WEBSITE`. Licencja opisuje nieodpłatne użycie materiałów w projektach; autoryzacja integracji odrębna. Oficjalny tekst ogranicza nawet maszynowe linkowanie, osadzanie, wyszukiwanie i pobieranie bez zgody.
- **Wyszukiwanie** — Ręczne wyszukiwanie w serwisie. Udokumentowane publiczne API, parametry, języki i paginacja Unknown.
- **Szczegóły** — Właściciel praw znany. Stabilne ID/licencja konkretnej wersji pliku i data Unknown.
- **Plik i warianty** — Ręczne użycie w zgodzie z licencją projektu; automatyczny direct download poza zakresem. Wektory/obrazy wg licencji; dokładne warianty formatów i alfa Unknown. Rozdzielczości, alfa i metadane pliku Unknown. FPS/audio nie dotyczy.
- **Prawa** — Własna licencja; obejmuje zastosowania komercyjne, zakazuje kompilacji, integracji bez zgody oraz określonych zastosowań ML.
- **Transport i cache** — undraw.co; mechanika transferu, cache, redirecty, limity, Retry-After, podpisy i CDN Unknown.
- **Ryzyko i adapter** — Zakaz integracji niezależnie od prawa w gotowym projekcie. Osobne ograniczenia ML. Brak; nie projektować integracji pod obecne warunki.
- **Źródła pierwotne** — [v-undraw](https://undraw.co/license).



## ShareTextures

Zakres `SURVEY`. NEW_PROVIDER. Provider `REJECTED`. Asset `MANUAL_ONLY: sprawdzić warunki strony i rekord, kwalifikacja automatyczna wyłączona.` Host `NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`, `Unknown`.

- **Właściciel i zastosowanie** — ShareTextures. Kategorie `pbr`, `textures`, `3d`. [Projekt](https://www.sharetextures.com/)
- **Nowość** — Brak w baseline; pokrycie typu PBR dubluje część użyteczności istniejących dostawców.
- **Dostęp i automatyzacja** — `MANUAL_WEBSITE`. Strona licencji opisuje bez konta i bez opłaty, warunki konkretnego pliku/pakietu Unknown. Wyraźny zakaz automatycznego pobierania/scrapingu, hotlinkowania i pobierania w aplikacjach.
- **Wyszukiwanie** — Ręczne przeglądanie. Publiczne API, języki, filtrowanie maszynowe i paginacja Unknown.
- **Szczegóły** — Per plik: ID/autor/data/licencja/wersja Unknown.
- **Plik i warianty** — Własna strona z przyciskiem wg licencji. Zakaz direct links z wtyczki. Tekstury i modele do 4K według strony. Dokładne formaty/rodzaje map/alfa Unknown. Do 4K deklarowane, parametry konkretnego pliku i mapy Unknown.
- **Prawa** — Warunki rozbieżnie opisują licencję jako CC0 1.0 oraz własną CC0-based. Zapis warunków platformy osobno; nie oznaczać jednoznacznie jako unrestricted CC0.
- **Transport i cache** — www.sharetextures.com. Host finalny, CDN, ETag, limity, Retry-After, redirecty i podpisy Unknown.
- **Ryzyko i adapter** — Zakaz automatyzacji przesądza o kwalifikacji, nawet gdy zastosowanie gotowego pliku jest dozwolone. Rozbieżność sformułowań licencyjnych. Brak. Nie budować integracji na tych warunkach.
- **Źródła pierwotne** — [v-share-lic](https://www.sharetextures.com/p/license), [v-share-tos](https://www.sharetextures.com/p/terms).



## Unsplash

Zakres `SURVEY`. NEW_PROVIDER. Provider `OUT_OF_CORE`. Asset `CONDITIONAL: własna licencja Unsplash dla darmowych zdjęć i odrębne prawa wizerunku/marek; Unsplash+ wyłączony.` Host `NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`, `Unknown`.

- **Właściciel i zastosowanie** — Unsplash i indywidualni fotografowie. Kategorie `photos`, `contemporary-stock`. [Projekt](https://unsplash.com/)
- **Nowość** — Brak w aktywnych ID baseline; współczesny stock fotograficzny ma inną użyteczność niż archiwa.
- **Dostęp i automatyzacja** — `KEYED_API; MANUAL_WEBSITE`. Konto, aplikacja i access key. Demo 50/h; produkcja po akceptacji. Dokumentacja API i wytyczne ograniczają je do doświadczeń nieautomatycznych; obowiązują hotlink, tracking download i atrybucja.
- **Wyszukiwanie** — GET /search/photos, stronicowanie i filtry dokumentowane; języki Unknown.
- **Szczegóły** — GET /photos/{id}, dane fotografa i identyfikator zdjęcia; zakres licencji ustalić per plik.
- **Plik i warianty** — URL variants w photo.urls; osobny obowiązkowy download event przez photo.links.download_location. Warianty obrazów z API; format/rozdzielczość/alfa potwierdzić dla pliku. raw/full/regular/small/thumb w docs. Rozdzielczości zależne od rekordu; alfa Unknown.
- **Prawa** — Własna licencja zdjęć i odrębne API Terms. Wykorzystanie w filmie rozpatrywać osobno od sprzedaży samego zdjęcia, tworzenia konkurencyjnego zbioru i praw innych osób.
- **Transport i cache** — api.unsplash.com, URL zdjęć hotlinkowanych z API. Klucz chroniony, limity z nagłówków; ETag, podpisy, Retry-After i redirecty Unknown.
- **Ryzyko i adapter** — Klucz, nieautomatyczne doświadczenia, własna licencja i prawa osób trzecich. Demo nie kwalifikuje. Brak w głównej ścieżce. Ewentualne ręczne użycie konkretnego pliku na jego warunkach.
- **Źródła pierwotne** — [v-unsplash-api](https://unsplash.com/documentation), [v-unsplash-guide](https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines), [v-unsplash-lic](https://unsplash.com/license).



## Przypięte wersje źródeł repozytoryjnych

| Repozytorium | Commit | Data UTC |
| --- | --- | --- |
| FrameCoreWorks/framecore-open-assets | `889471fcdbc2216ddc465715eff0e82784d5b8ee` | 2026-11-06 |
| tabler/tabler-icons | `845a74971e5f39fe1360a9987e4ae327ef1c90b9` | 2026-11-10 |
| google/fonts | `5bb28733cec313b63fbd415b574b5ae35c8aa8b8` | 2026-11-08 |
| WordPress/openverse | `50135c93a3630f908b7bbd8bfe5da8acd96f3ce3` | 2026-11-07 |
| art-institute-of-chicago/api-data | `8c7e65089ac8145a241f237e065c81861a35f359` | 2026-10-18 |
| hfg-gmuend/openmoji | `3e01de523ddefe9c5e46a7765b15efef04bf9002` | 2026-11-04 |
| Smithsonian/OpenAccess | `c2ac3e2a671755e03e1ec439ad7b9b0020636281` | 2021-12-21 |

## IMPLEMENTATION_HANDOFF — propozycje dla Open Assets

Każdy krok ma status `NOT_RUN`. Właścicielem kontraktu i prawa pliku jest FrameCore Open Assets. Studio sprawdza import po dostarczeniu zweryfikowanego oryginału i sidecara. Koszt dotyczy opłaty providera na opisanej ścieżce, nakład wdrożeniowy i hostowany pozostaje Unknown.

| Priorytet i właściciel | Wejście, zależności i wyjście | Limit i koszt | Test akceptacyjny |
| --- | --- | --- | --- |
| P0, Open Assets — Iconify i walidacja SVG | Uprawniona kolekcja Tabler, przypięty MIT i API. Rozbudowa istniejącego `license_policy`, kontrola SVG i aktualnego sidecara. | 1 zapytanie wyszukiwania, 2 odczyty metadanych, 1 SVG ≤256 KiB, 10 s na żądanie, bez opłaty wg docs. | Wyszukać `camera`, zachować `tabler:camera` i notice. MIME i XML zgodne, statyczny podzbiór, odczyt viewBox, SHA-256 i sidecar. Oddzielnie lokalna próba aktywnej treści i niedozwolonego hosta ma zakończyć się odrzuceniem przed handoffem. `openmoji:avocado` klasyfikować wg istniejącego review SA. |
| P1, Open Assets — PhyloPic SVG | Obecny adapter i kontrola SVG P0. Wybór oryginalnego `rasterFiles` albo `vectorFile` przy tym samym UUID i tej samej licencji. | 1 rekord i 1 SVG ≤256 KiB, 10 s na żądanie. Koszt Unknown; ścieżka publiczna. | Dla obrazu z udokumentowaną licencją porównać warianty metadanych, wybrać SVG i utrwalić źródło. Brak `vectorFile` daje jawny błąd wariantu, zachować działanie istniejącego trybu PNG. |
| P1, Open Assets i Studio — Fontsource / Google Fonts | Potwierdzony plik licencji w dokładnej dystrybucji Fontsource, metadane upstream, kontrola binariów fontów i rozszerzenie istniejącego modelu praw o OFL. Wyjście TTF lub WOFF2 ze specyfiką wariantu i sidecarem, bez instalacji. | 2 rekordy, jeden wersjonowany plik fontu ≤2 MiB i licencja, 10 s na żądanie. Brak opłaty wskazanej w docs. | Sprawdzić rodzinę i wariant `instrument-serif`, weryfikację nagłówka/tablic, zakres znaków `ĄĆĘŁŃÓŚŹŻ ąćęłńóśźż` i rozróżnienie `latin`/`latin-ext`. Odrzucić źródło bez przypisanego OFL i notice. Inter służy oddzielnej próbie osi zmiennych. To samo ID rodziny z obu ścieżek widoczne raz, zachować różne warianty. |
| P1, Open Assets — Openverse discovery | Sprawdzić aktualny OpenAPI, warunki i oryginalny provider. Powiązanie identyfikatorów, zachowanie śladu indeksu i deduplikacja. | 1 search i 1 detail per kategoria, 0 bajtów mediów z indeksu. Aktualny koszt komercyjny Unknown. | Dwa wyniki reprezentujące ten sam oryginał zachowują jedno źródłowe ID. Rozbieżna licencja lub nieznany origin nie dają wariantu do pobrania. 403 i 429 w teście lokalnym prowadzą do stop. |
| P2, Open Assets — AIC | Odczyt obowiązujących Image Licensing/ToS i niezależne sprawdzenie hosta. Wejście: rekord 27992 i negatywny 129884. Wyjście: zweryfikowany JPEG tylko dla potwierdzonego prawa obrazu. | 2 detale i maks. 1 JPEG 843 px ≤4 MiB, 10 s na żądanie, jedno żądanie naraz, odstęp co najmniej 1 s. Opłata Unknown. | Potwierdzić source page, ID i prawidłowy wariant przy 27992. 129884 ma `image_id`, a jednak musi zostać zatrzymany na prawach przed pobraniem. 403 hosta kończy próbę i zapisuje dowód. |
| P2, Open Assets — Smithsonian | Próbka publicznego indeksu jednej jednostki i jawny CC0 konkretnego pliku, jeśli istnieje potrzeba archiwalnego 3D. Wyjście: kwalifikacja statycznego importera. | 1 shard metadanych do 4 MiB, 10 s, 0 bajtów plików 3D w preflight. Koszt dostępu na ścieżce S3: konto niewymagane; dalsze koszty Unknown. | Rekord CC0 metadanych bez CC0 medium nie daje wariantu. Przy późniejszym odrębnym teście 3D sprawdzić kontrolę względnych zależności i ograniczenie rozpakowania. |

Wspólna ścieżka po wdrożeniu: wyszukaj → uzyskaj szczegóły i dowód praw → wybierz wariant → ponownie zweryfikuj prawa → pobierz z dozwolonego hosta → skontroluj bajty i decode → zapisz oryginał i sidecar → przekaż asset do Studio. `source_page` identyfikuje pochodzenie. `selected_variant`, `downloaded_utc`, `sha256` i `verification` zachowują stan pobrania. W kopercie wynikowej zachować `asset.asset_id`, `asset.source_url`, `asset.licence`, `asset.credits.creator`, `asset.retrieval`. Wersję kolekcji, pakietu, parametr wariantu i dowód licencji przechowywać jako pola addytywne po uzgodnieniu kontraktu. [Kontrakt i pola](../baseline/BASELINE.md)

Kontrola obejmuje allowlist na każdym przekierowaniu, ograniczenia bajtów i czasu, weryfikację sygnatury przy neutralnym MIME, odrzucanie HTML/challenge i aktywnych SVG oraz zachowanie oryginału z hashem i identyfikacją wariantu. Dane SVG analizować bez sieci i ładowania zewnętrznych zasobów. Dla glTF rozwiązywać wyłącznie zatwierdzone względne zależności. Archiwa sprawdzać przed ekstrakcją pod kątem ścieżek, rozmiarów i liczby plików. Brak autora wymaganej atrybucji, brak praw, wygasły lub zmieniony wariant zatrzymują produkcyjny handoff. Na 401/403/429 lub challenge zakończyć próbę zgodnie z runtime, zachować `Retry-After` jeśli wystąpił i wznowienie rozpatrywać jako odrębną próbę. Preferować cache z `last-modified` dla kolekcji Iconify i exact SemVer dla Fontsource. Potwierdzać prawa od nowa po zmianie wersji.

