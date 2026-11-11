# Dostawcy audio, SFX i wideo

Stan badania 2026-11-11. Porównanie z FrameCore Open Assets 0.5.0, commit `889471fcdbc2216ddc465715eff0e82784d5b8ee` z 2026-11-06. W bieżącym źródle LibriVox dostarcza audiobooki, Commons szeroki katalog audio i wideo, Incompetech muzykę jednego twórcy, SFXMint syntetyczne efekty, a NASA zdjęcia i wideo z bramką praw. Najsłabiej pokryte pozostają nagrania terenowe, foley, wieloautorska muzyka z prawami do synchronizacji oraz współczesny B-roll. Przebadane źródła nie ustanawiają gotowej ścieżki dla wideo z alfą. [Audyt baseline](../baseline/BASELINE.md)

| Kwalifikacja | Źródła | Znaczenie dla integracji |
| --- | --- | --- |
| CORE_CANDIDATE | NASA audio | Rozszerzenie obecnego providera po sprawdzeniu API audio i praw konkretnego pliku. |
| OPTIONAL | Internet Archive curated, Wyzowl SFX Kit, CLR Music | IA wymaga kuracji praw i tras pobrania. Wyzowl to wersjonowany manifest syntetycznych efektów. CLR wymaga sprawdzenia źródeł pierwotnych i pakietów. |
| OPTIONAL / OUT_OF_CORE | Freesound, Lots of Sounds, Pixabay Video | Udokumentowane API z kontem i kluczem. Freesound ma osobne warunki API dla zastosowań komercyjnych, Lots of Sounds płatne API, Pixabay licencję własną. |
| MANUAL | NPS, Blender Open Movies, Mixkit, Sonniss #GameAudioGDC | Ręczny wybór, weryfikacja prawa dla planowanego użycia i pochodzenia pliku. |
| REJECTED | BBC RemArc, Free To Use | Domyślne bezpłatne warunki nie obejmują oczekiwanego zakresu komercyjnego. |

`DOCUMENTED` obejmuje oryginalne dokumenty, deklaracje i odczytane metadane. `CODE_INSPECTED` obejmuje zawartość repozytorium i wersjonowane manifesty. `AUTHOR_TEST` jest wynikiem zgłoszonym przez autora w określonym zakresie. `OWN_TEST` dotyczy wyłącznie kontroli spójności dokumentów. `DERIVED` to ocena kwalifikacji i propozycja integracji. `NOT_RUN` dotyczy operacji runtime, pobrania, pełnego decode, pomiarów i handoffu. `Unknown` oznacza brak ustalenia. Żaden rekord nie ma potwierdzenia binariów ani oceny odsłuchu/obrazu. Status odczytu źródła i typ dowodu to osobne pola. Daty odczytów i luki są w rejestrze. [Katalog](catalog.json), [rekordy](records.json), [rejestr źródeł](sources.json).

W proponowanych ścieżkach sprawdzić prawa i konkretne ID przed wyborem wariantu. Pobrać tylko zatwierdzony wariant w limicie 32 MiB, zweryfikować sygnaturę, kategorię, hash i pełny decode w obecnym runtime, następnie zapisać sidecar z pochodzeniem. Parametry dodatkowe, np. kanały audio, częstotliwość próbkowania, FPS i alfa, wymagają osobnych dowodów. Przy 401, 403, 429, challenge lub `network_blocked` obowiązuje zatrzymanie, zapis dostępnego `Retry-After` i dotychczasowa polityka ponowień. [Audyt runtime i kontraktu](../baseline/BASELINE.md), [plan prób](../TEST_PLAN.md).

## Internet Archive — wybrane kolekcje

Zakres `DEEP`. Nowość `NEW_PROVIDER`. Kwalifikacja `OPTIONAL`. `PROVIDER_ELIGIBILITY=CONDITIONAL_API`, `ASSET_ELIGIBILITY=CONDITIONAL_PER_ASSET`, `HOST_READINESS=NOT_RUN`. Priorytet `P1`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i kategorie** — Internet Archive. `audio`, `music`, `sfx`, `video`. [Strona źródła](https://archive.org/)
- **Nowość i zastosowanie** — Brak w pakiecie 15 providerów. LibriVox używa hostów IA, ale wystawia audiobooki. Ogólny katalog IA wyłączono historycznie. Rozważyć tylko ograniczone kolekcje.
- **Dostęp, koszty i automatyzacja** — `DOCUMENTED_PUBLIC_API`. Publiczny odczyt i publiczne pliki bez klucza. Ograniczone rekordy poza zakresem. Opłata za publiczny odczyt: 0. IA dokumentuje automatyzację i identyfikację narzędzia, wersji i modelu w User-Agent. Ograniczyć do interaktywnych zapytań i wybranych plików. Zalecenia według zapisu poprzedniego odczytu dokumentacji botów. W ponownej próbie narzędzie nie mogło odczytać tej strony. Regulamin Terms nieodczytany.
- **Wyszukiwanie** — `GET /advancedsearch.php` z `q` i `output=json`. Składnia pól, kolekcji, zakresów, sortowania. Bez zakładania poprawności licenseurl. Parametry limitu/paginacji do potwierdzenia w próbie. Język jako metadana, jakość zapytań PL Unknown.
- **Szczegóły i tożsamość rekordu** — `GET /metadata/{identifier}` lub `/metadata/{identifier}/files`. Niezmienny item ID, wersja pliku po nazwie i checksums. Autor, data i licenseurl mogą być tylko na poziomie itemu. Details page jako source URL.
- **Pobieranie** — `GET /download/{identifier}/{filename}` wyłącznie dla jawnego publicznego pliku z manifestu. Dozwolone hosty i restrykcyjne przekierowania. Zachować oba URL w provenance.
- **Formaty i warianty** — W zależności od itemu m.in. H.264, MPEG4, MPEG2, Ogg, MP3, FLAC. Weryfikacja MIME/decode. FPS, alfa, liczba kanałów i długość per wariant często Unknown. Original/derivative z manifestu. Pominąć podgląd, metadane, torrent i niezweryfikowane ścieżki. Dźwięk/napisy/alternatywny soundtrack mogą mieć odrębne prawa.
- **Prawa do pliku i metadanych** — CC0/CC BY/PDM tylko ze zgodnym dowodem item/file, wiarygodnym źródłem i bez sprzeczności. CC BY-SA wymaga świadomej zgody i analizy synchronizacji. NC/ND/Unknown blokada. Licencja metadanych Unknown. Starszy Public Domain Certification USA ≠ PDM.
- **Transport, cache i błędy** — archive.org i ruchome maszyny storage IA. Utrzymać rozpoznanie wyłącznie zatwierdzonych hostów. Bez ogólnego wildcard. 429/Retry-After udokumentowane. Quota, CDN TTL, ETag/Last-Modified per route Unknown.
- **Ryzyko i trudność integracji** — Historyczne odrzucenie ogólnego katalogu mimo pojedynczego decode. Wtórne uploady i `licenseurl` bez wiarygodnego grantora. Jurysdykcja PD. Powielone LibriVox/NASA. Brak potwierdzonej alfy. Średnio-wysoki. Allowlista kolekcji, oddzielna kontrola item/file, wersje i origin uploadu, wąski transport. Ograniczony spike wyłącznie po potwierdzeniu autoryzowanego hosta i dowodu praw. Brak automatycznej aktywacji.
- **Źródła pierwotne** — [av-ia-search](https://archive.org/advancedsearch.php), [av-ia-meta](https://archive.org/developers/md-read.html), [av-ia-schema](https://archive.org/developers/metadata-schema/index.html), [av-ia-items](https://archive.org/developers/items.html), [av-ia-bots](https://archive.org/developers/bots.html) (`BLOCKED`), [av-ia-terms](https://archive.org/about/terms) (`BLOCKED`), [av-ia-rights](https://help.archive.org/help/rights/), [av-ia-trip](https://archive.org/details/TripDown1905), [av-ia-popeye](https://archive.org/details/popeye_taxi-turvey), [av-ia-legacy-pd](https://creativecommons.org/publicdomain/certification/1.0/us/), [av-ccby](https://creativecommons.org/licenses/by/4.0/legalcode.en), [av-ccbysa](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en).


### Ograniczenie kwalifikacji i próbka rekordów

Do ponownej kwalifikacji wybrać podkolekcję z wiarygodnym grantorem i rozróżnieniem praw oryginału oraz pochodnych. Dla publicznego pliku zachować identyfikator itemu, dokładną nazwę pliku, wskazanie original/derivative, dostępny checksum, URL strony i udokumentowany wariant. Dostępność wybranych plików, warunki przekierowań i małe rozmiary pozostają do sprawdzenia. Wyszukiwanie z filtrem licencji może służyć selekcji kandydatów. Kontrola praw wymaga osobnego sprawdzenia dokumentów, autora, osób, znaków i soundtracku. Ogólny katalog wcześniej wycofano mimo historycznego dekodowania jednego MP3. [Metadane pliku](https://archive.org/developers/md-read.html), [transport plików](https://archive.org/developers/items.html), [Rights Help](https://help.archive.org/help/rights/), [baseline](../baseline/BASELINE.md).

Poprzedni odczyt dokumentacji botów podaje identyfikowalny User-Agent z narzędziem, wersją i modelem, pacing, 429 i Retry-After. W ponownym odczycie strona była niedostępna dla web. Nie przełączano kanału. Terms wyświetliły wymóg JavaScript, więc ich treść pozostaje Unknown. Powyższe zalecenia transportowe nie ustanawiają zgody na planowaną integrację ani redystrybucję mediów. [Dokumentacja botów](https://archive.org/developers/bots.html), [Terms](https://archive.org/about/terms).

| Rekord | Autor, warianty, parametry | Prawa i decyzja |
| --- | --- | --- |
| `av-r-ia-trip` · `TripDown1905` | Miles Brothers. Warianty opisane jako 512KB MPEG4, H.264, MPEG2, Ogg Video, MP3. Bajty, rozdzielczość, czas, FPS, kanały i alfa Unknown. | `REVIEW_REQUIRED`. Starsza certyfikacja oparta na prawie USA. Sprawdzić jurysdykcję, grantora i pochodzenie każdego wybranego wariantu, zwłaszcza MP3. [Rekord](https://archive.org/details/TripDown1905), [certyfikacja](https://creativecommons.org/publicdomain/certification/1.0/us/). |
| `av-r-ia-popeye` · `popeye_taxi-turvey` | Tom Johnson i Frank Endres, muzyka Winston Sharples. Rok produkcji 1954. 512KB MPEG4, MPEG2, Ogg Video. Bajty, rozdzielczość, czas, FPS, kanały i alfa Unknown. | `BLOCKED_UNKNOWN`. Wersje pliku i rok nie ustalają praw filmu, muzyki ani postaci. Przydatny przypadek odmowy na etapie metadanych. [Rekord](https://archive.org/details/popeye_taxi-turvey). |

## NASA Image and Video Library — audio

Zakres `DEEP`. Nowość `EXISTING_NEW_CATEGORY`. Kwalifikacja `CORE_CANDIDATE`. `PROVIDER_ELIGIBILITY=CONDITIONAL_EXISTING_API`, `ASSET_ELIGIBILITY=REVIEW_REQUIRED_PER_ASSET`, `HOST_READINESS=NOT_RUN`. Priorytet `P0`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i kategorie** — NASA. `audio`, `sfx`. [Strona źródła](https://images.nasa.gov/)
- **Nowość i zastosowanie** — Provider nasa w baseline obejmuje photos i video. Oficjalne API dokumentuje audio. Realne nagrania misji to osobna kategoria.
- **Dostęp, koszty i automatyzacja** — `DOCUMENTED_PUBLIC_API`. Dokumentacja NASA Image and Video Library podaje publiczne żądania bez klucza. Zakres publicznego katalogu bez kosztu dostępu. Oficjalne REST API. Audio corpus nie zostało przetestowane w runtime. Odczyt publicznych artykułów Artemis niezależnie od API.
- **Wyszukiwanie** — `GET https://images-api.nasa.gov/search` z `media_type=audio`, `q`, `keywords`, `center`, zakres lat, `page` i `page_size`. Język/semantyka Unknown.
- **Szczegóły i tożsamość rekordu** — `GET /asset/{nasa_id}` manifest. `GET /metadata/{nasa_id}` zwraca location JSON. Pola data_created, description, center, keywords, ewentualny credit podlegają sprawdzeniu per rekord.
- **Pobieranie** — Z manifestu assetu, po wyborze wariantu i kontroli hosta. Artemis page ma odrębne rekordy informacyjne, bez przypisywania im `nasa_id`.
- **Formaty i warianty** — Artemis deklaruje WAV/MPEG. API audio formaty do potwierdzenia per asset. Długość, bit depth, kanały, dostarczony hash Unknown. Udokumentowane różne warianty w manifestach API ogólnie. Konkretna hierarchia WAV/MP3 i deklarowane bitrate dla audio Unknown.
- **Prawa do pliku i metadanych** — NASA usage guidelines i item-specific review. Kraj, osoba rozpoznawalna po głosie, cudzy materiał, identyfikatory, marki i endorsement. Prawa do metadanych API Unknown.
- **Transport, cache i błędy** — images-api.nasa.gov i hosty już zatwierdzone dla adaptera NASA, np. images-assets.nasa.gov. Kolejne domeny tylko po obserwacji w udokumentowanej trasie. JSON error reason. Limity/Retry-After/cache/URL TTL Unknown.
- **Ryzyko i trudność integracji** — Udokumentowana techniczna możliwość bez danych o faktycznej klasyfikacji konkretnych clipów w API. Identyfikowalny głos lub licencja osoby trzeciej → review/blokada. Nagrania często zawierają speech. Część WAV >32 MiB. Niska/średnia. Rozszerzenie obecnego adaptera, reguł category i testów audio, istniejący rights-review-note. Bez uprawnień dla nowych hostów na podstawie artykułu Artemis. review_nasa nie spełnia warunku eligible aktualnego importu Earshot.
- **Źródła pierwotne** — [av-nasa-api](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf), [av-nasa-rights](https://www.nasa.gov/nasa-brand-center/images-and-media/), [av-nasa-artemis](https://www.nasa.gov/artemisaudio/), [av-nasa-search-unread](https://images-api.nasa.gov/search?q=apollo%2011&media_type=audio&page_size=3) (`BLOCKED`).


### Ograniczenie kwalifikacji i próbka rekordów

Najmniejsze rozszerzenie to `media_type=audio` w istniejącym adapterze NASA, manifest kategorii i osobny test dekodowania audio. Ustalić realny `nasa_id`, zgodność wpisu w `search` i `asset` oraz format i rozmiar jednego wariantu. Odczyt przykładowego zapytania w narzędziu web był zablokowany. Trzy rekordy poniżej są wpisami redakcyjnymi Artemis Audio Library. Ich członkostwo w API, `nasa_id`, bezpośrednie URL z manifestu i czas nagrania są Unknown. Dla tych plików statusy API, pobrania i decode pozostają `NOT_RUN`. [Specyfikacja API](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf), [Artemis Audio Library](https://www.nasa.gov/artemisaudio/).

Ustalić, kto wypowiada się w nagraniu, kto wykonał utwór i czy dźwięk zawiera cudzy wkład. Warunki agencji dotyczą praw autorskich w USA i osobno ograniczeń identyfikowalnych osób, marek i sugerowania poparcia, istotnych w reklamie. Użycie w filmie i redystrybucję źródła rozpatrzyć oddzielnie dla pliku i jurysdykcji. W Open Assets zachować `review_nasa` i notatkę użytkownika o pliku, zastosowaniu i jurysdykcji. Aktualny Earshot przyjmuje wyłącznie `eligible`, więc `review_nasa` nie przejdzie importu nawet z pozytywnym decode i notatką. [Wytyczne NASA](https://www.nasa.gov/nasa-brand-center/images-and-media/), [baseline kontraktu](../baseline/BASELINE.md).

| Wpis Artemis | Data na stronie | Deklarowany format i rozmiar | Wniosek |
| --- | --- | --- | --- |
| `av-r-nasa-orion` · Artemis II Launch: Orion Communications Check | 2026-04-01 | MPEG, 1,66 MB | Kandydat do sprawdzenia kodeka po ustaleniu właściwego rekordu API. |
| `av-r-nasa-closest` · Artemis II Lunar Flyby: Closest to the Moon | 2026-04-07 | WAV, 8,23 MB | Mieści się deklaratywnie w limicie runtime 32 MiB. |
| `av-r-nasa-love` · Artemis II Lunar Flyby: We Love You, from the Moon | 2026-04-07 | WAV, 44,23 MB | Deklarowany plik przekracza limit 32 MiB. Osobny wariant Unknown. |

Wszystkie trzy mają `REVIEW_REQUIRED`. NASA jest źródłem publikacji, a kredyt twórcy i identyfikacja mówcy per plik są Unknown. Długość, kanały, bit depth i hash również Unknown. [Rekordy Artemis](https://www.nasa.gov/artemisaudio/).

## National Park Service — Yellowstone i Natural Sounds

Zakres `DEEP`. Nowość `NEW_PROVIDER`. Kwalifikacja `MANUAL`. `PROVIDER_ELIGIBILITY=MANUAL_CURATED_STATIC`, `ASSET_ELIGIBILITY=REVIEW_REQUIRED_PER_ASSET`, `HOST_READINESS=NOT_RUN`. Priorytet `P1`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i kategorie** — U.S. National Park Service. `sfx`, `audio`, `video`. [Strona źródła](https://www.nps.gov/yell/learn/photosmultimedia/soundlibrary.htm)
- **Nowość i zastosowanie** — Nieobecny w baseline. Nagrania rzeczywistych zwierząt, krajobrazów, dźwięków infrastruktury i parkowy B-roll z jawnie oznaczonych kolekcji.
- **Dostęp, koszty i automatyzacja** — `OFFICIAL_STATIC_HTML_INDEX`. Wskazane strony i publiczne kolekcje bez konta i opłaty. Ogólne NPS API wymaga klucza. Oficjalne indeksy i zgoda na pobieranie/użycie wybranych plików. Brak potwierdzonej umowy na crawler lub udokumentowanej ścieżki API dla tych rekordów.
- **Wyszukiwanie** — Alfabetyczne indeksy Yellowstone, Natural Sounds według kategorii. Metadane transkrypcji i opisy po angielsku. Bez publicznej paginacji i wyszukiwania asset API. Możliwy lokalny filtr po ręcznym imporcie.
- **Szczegóły i tożsamość rekordu** — Strona wpisu i opis wariantu. Daty oraz autor dla wybranych nagrań. Wideo bywa identyfikowane UUID embed, który nie jest dowodem osobnego endpointu download.
- **Pobieranie** — Pobieranie przez oficjalną stronę. Przed importem udokumentować jawne źródło URL. Bez odpytywania wewnętrznego player API.
- **Formaty i warianty** — Wybrane wideo H.264 w natywnej rozdzielczości. NPS opisuje rejestrację MP3. Dokładny format poszczególnych plików audio wymaga źródła i decode. Nagrania mono, stereo, osobne ujęcia/remiks według strony. H.264 sample 720p60 z audio 48 kHz. Alfa Unknown. Brak potwierdzonego transparentnego wariantu.
- **Prawa do pliku i metadanych** — Jawne public domain wybranych kolekcji. Zachować autorów/NPS. Uwzględnić prawo kraju użycia, wyjątki cudzych praw, osoby, logotypy, muzykę i znaki. Metadane osobna licencja Unknown.
- **Transport, cache i błędy** — www.nps.gov. Końcowe domeny assetów, redirecty, cache, ETag, Last-Modified, Retry-After, limity i błędy Unknown. Dodatkowy materiał kamerowy bywa wydawany po kontakcie i przesłaniu dysku.
- **Ryzyko i trudność integracji** — Nie wszystkie treści NPS są PD. Audio czasem mowa/muzyka, wizerunki i znaki w wideo. Rozmiary/zgodność produkcyjna Unknown. Ręczny manifest łatwo zdezaktualizować. Niski koszt małego ręcznego indeksu. Osobny import wersjonowanej kuracji dopiero z potwierdzonymi URL i podstawą praw per rekord. Bez dodawania publicznego providera API.
- **Źródła pierwotne** — [av-nps-sounds](https://www.nps.gov/yell/learn/photosmultimedia/soundlibrary.htm), [av-nps-gallery](https://www.nps.gov/subjects/sound/gallery.htm), [av-nps-video](https://www.nps.gov/yell/learn/photosmultimedia/videolibrary.htm), [av-nps-rights](https://www.nps.gov/aboutus/disclaimer.htm), [av-nps-key](https://www.nps.gov/subjects/developer/get-started.htm), [av-nps-old](https://www.nps.gov/yell/learn/photosmultimedia/sounds-oldfaithful.htm), [av-nps-dawn](https://www.nps.gov/yell/learn/photosmultimedia/sounds-dawnchorus.htm), [av-nps-spring](https://www.nps.gov/yell/learn/photosmultimedia/vl_grandprismatic.htm).


### Ograniczenie kwalifikacji i próbka rekordów

Ręczna kuracja daje ambience, nagrania fauny i parkowy B-roll z opisanym kontekstem. Zaczynać od jednej strony kolekcji z jawną deklaracją public domain i strony wskazanego pliku. Udokumentować warunki dla kraju publikacji, autora, dokładną datę i wariant, po czym potwierdzić link oraz bajty. Utwór pracowniczy rządu federalnego w USA i oznaczenie kolekcji mają określony zakres. Wizerunek, logo, muzyka, wykonanie, cudzy materiał oraz ponowne udostępnienie pliku wymagają osobnej oceny. Ogólne API wymaga klucza i nie potwierdza udostępnienia tych wpisów. [Deklaracja NPS](https://www.nps.gov/aboutus/disclaimer.htm), [klucz API](https://www.nps.gov/subjects/developer/get-started.htm), [indeks dźwięków](https://www.nps.gov/yell/learn/photosmultimedia/soundlibrary.htm), [indeks wideo](https://www.nps.gov/yell/learn/photosmultimedia/videolibrary.htm).

| Rekord | Autor i parametry deklarowane | Ograniczenie dowodu |
| --- | --- | --- |
| `av-r-nps-old` · Old Faithful | NPS / Jennifer Jerrett. Mono 2014-11-16, stereo 2015-03-22. Odrębne nagrania. | Brak ustalenia ID i formatów dystrybucji, rozmiaru, czasu i hashy. [Rekord](https://www.nps.gov/yell/learn/photosmultimedia/sounds-oldfaithful.htm). |
| `av-r-nps-dawn` · Dawn Chorus | NPS / Jennifer Jerrett, 2014-06-28, koło Mammoth Hot Springs. Śpiew ptaków i bębnienie dzięciołów według opisu. | ID, format, kanały i czas Unknown. [Rekord](https://www.nps.gov/yell/learn/photosmultimedia/sounds-dawnchorus.htm). |
| `av-r-nps-spring` · Grand Prismatic Spring | 26 s, 1280×720, 60 FPS, audio 48 kHz. Kolekcja wskazuje H.264. Strona podaje oryginał `00547.MTS`. | UUID `7E5FFF00-155D-451F-676262A83E6E19C7` dotyczy osadzenia. URL wariantu, bajty, kanały, alfa, data i autor Unknown. [Rekord](https://www.nps.gov/yell/learn/photosmultimedia/vl_grandprismatic.htm). |

Każdy przykład ma `REVIEW_REQUIRED`. Kredyt NPS i zidentyfikowanego twórcy zachować w pochodzeniu, a deklarację public domain przytoczyć w zakresie wskazanej kolekcji.

## Wyzowl SFX Kit

Zakres `DEEP`. Nowość `NEW_PROVIDER`. Kwalifikacja `OPTIONAL`. `PROVIDER_ELIGIBILITY=CONDITIONAL_STATIC`, `ASSET_ELIGIBILITY=CC0_DECLARED`, `HOST_READINESS=NOT_RUN`. Priorytet `P1`. Dowody `DOCUMENTED`, `CODE_INSPECTED`, `NOT_RUN`.

- **Właściciel i kategorie** — Wyzowl. `sfx`. [Strona źródła](https://github.com/wyzowl/sfx-kit)
- **Nowość i zastosowanie** — Nieobecny w baseline. SFXMint ma syntetyczne SFX, Wyzowl wnosi wersjonowane źródło z osobnymi plikami i metadanymi synchronizacji do motion.
- **Dostęp, koszty i automatyzacja** — `OFFICIAL_VERSIONED_REPOSITORY`. Publiczny Contents REST i manifest bez konta/klucza, bez opłaty za media. Repozytorium jawnie kieruje integratorów do sounds.json. Użyć oficjalnego transportu publicznych treści GitHuba, nie uruchamiać generatorów.
- **Wyszukiwanie** — Lokalne wyszukiwanie angielskiego `name`, `tags`, `use_for`, kategorii i filtrów duration/variant/sync. Brak API wyszukiwania usługodawcy i paginacji.
- **Szczegóły i tożsamość rekordu** — `sounds.json` w commit `92780e7ab0cdfb557497a988089c47f46e8c7412`. Stabilność ID wersjonowana przez pin, deklarowane ścieżki, duration, channels, sync i loudness. Osobnej daty i SHA per sound w odczytanych rekordach nie zaobserwowano.
- **Pobieranie** — GitHub Contents API `GET /repos/{owner}/{repo}/contents/{path}?ref={sha}` z udokumentowaną reprezentacją raw dla bezpośredniego pliku podanego w manifeście. Ewentualny redirect po walidacji allowlisty.
- **Formaty i warianty** — Jedna wersja WAV PCM signed 24-bit little-endian, 48 kHz, mono lub stereo wg manifestu. Czas per plik. Brak wideo/FPS/alfy. `variant` oznacza odrębne dźwięki o różnych właściwościach z własnymi ID. Bez utożsamiania ich z transkodowanymi wersjami tego samego dźwięku.
- **Prawa do pliku i metadanych** — CC0 1.0 dla audio i danych według Wyzowl. Atrybucja opcjonalna. Zachować źródło i wersję. Deklaracja dotyczy zestawu, w tym wskazanych rekordów. Brak wyczyszczenia znaków z innych źródeł. CC0 dotyczy praw przysługujących deklarującemu. Zakres ewentualnych praw osób trzecich Unknown.
- **Transport, cache i błędy** — api.github.com. Końcowe hosty CDN/raw w live próbie. Dokumentacja Contents uprzedza o wygasaniu download_url. REST 60/h bez logowania, 403/429 według limitów. Hostowe ETag/Last-Modified/TTL Unknown dla wybranego pliku.
- **Ryzyko i trudność integracji** — Synteza programowa z udziałem modelu według autora. Nie zaliczać do recorded/foley nawet gdy opis foley. Loudness autora nie zastępuje decode ani pomiaru hosta. Brak SLA repo. Niski/średni. Jeden importer wersjonowanego manifestu, jawne mapowanie danych do obecnego kontraktu, pojedynczy plik do weryfikacji i sidecar. Pola `sync` i dB przechować jako opcjonalną propozycję provenance/handoff.
- **Źródła pierwotne** — [av-wy-readme](https://github.com/wyzowl/sfx-kit/blob/92780e7ab0cdfb557497a988089c47f46e8c7412/README.md), [av-wy-catalog](https://github.com/wyzowl/sfx-kit/blob/92780e7ab0cdfb557497a988089c47f46e8c7412/sounds.json), [av-wy-license](https://github.com/wyzowl/sfx-kit/blob/92780e7ab0cdfb557497a988089c47f46e8c7412/LICENSE), [av-wy-head](https://github.com/wyzowl/sfx-kit/commit/92780e7ab0cdfb557497a988089c47f46e8c7412), [av-wy-transport](https://docs.github.com/en/rest/repos/contents), [av-wy-rate](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api), [av-cc0](https://creativecommons.org/publicdomain/zero/1.0/legalcode).


### Ograniczenie kwalifikacji i próbka rekordów

Zestaw użyteczny dla ruchu typografii, montażu i synchronizacji zdarzeń. Wydawca opisuje 320 syntetycznych efektów, WAV 24-bit/48 kHz i CC0 dla audio oraz danych. Metadane wersjonować po commicie. Zachować `id`, nazwę, ścieżkę, tagi, `variant`, zadeklarowaną długość i punkt synchronizacji. Odrzucać ścieżki spoza dopuszczonego drzewa i formatów. Weryfikować końcowy host i pobierać jeden wskazany WAV. CC0 daje zakres użycia i redystrybucji w granicach praw wydawcy, więc cudze wkłady i źródło pochodzenia nadal mają znaczenie. [README wydawcy](https://github.com/wyzowl/sfx-kit/blob/92780e7ab0cdfb557497a988089c47f46e8c7412/README.md), [licencja zestawu](https://github.com/wyzowl/sfx-kit/blob/92780e7ab0cdfb557497a988089c47f46e8c7412/LICENSE), [CC0](https://creativecommons.org/publicdomain/zero/1.0/legalcode).

| Rekord | Ścieżka w repozytorium | Metadane manifestu |
| --- | --- | --- |
| `av-r-wy-medium` · `whoosh-fast-medium` | `sounds/whooshes/whoosh-fast-medium.wav` | 0,252 s, stereo, PCM s24le 48 kHz, sync 0,096 s, wariant medium. |
| `av-r-wy-soft` · `whoosh-fast-soft` | `sounds/whooshes/whoosh-fast-soft.wav` | 0,250 s, stereo, PCM s24le 48 kHz, sync 0,099 s, wariant soft. |

Oba rekordy przypisuje Wyzowl, `CC0_DECLARED`, w rewizji `92780e7ab0cdfb557497a988089c47f46e8c7412` z 2026-10-20 UTC. Dane są `CODE_INSPECTED`, bez niezależnego pomiaru. Produkcyjny sidecar powinien wiązać lokalny SHA-256 z wybranym ID, ścieżką i rewizją. Gotowość Earshot wymaga przejścia standardowych bramek i pozostaje `NOT_RUN`. [Manifest](https://github.com/wyzowl/sfx-kit/blob/92780e7ab0cdfb557497a988089c47f46e8c7412/sounds.json), [kontrakt](../baseline/BASELINE.md).

## CLR Music

Zakres `DEEP`. Nowość `NEW_PROVIDER`. Kwalifikacja `OPTIONAL`. `PROVIDER_ELIGIBILITY=STATIC_PACK_ONLY_CONDITIONAL`, `ASSET_ELIGIBILITY=REVIEW_REQUIRED_PER_ASSET`, `HOST_READINESS=NOT_RUN`. Priorytet `P1`. Dowody `DOCUMENTED`, `DERIVED`, `NOT_RUN`.

- **Właściciel i kategorie** — CLR Music, podmiot prawny Unknown. `sfx`, `audio`, `music`. [Strona źródła](https://clr.fm/music/)
- **Nowość i zastosowanie** — Nieobecny w baseline. Materiały zbiorcze z Freesound/Kenney i wielu autorów. Pokrywające się utwory Incompetech nie są dodatkową treścią. Odfiltrować po origin.
- **Dostęp, koszty i automatyzacja** — `OFFICIAL_STATIC_RELEASE_PACKS`. Publiczne strony i opublikowane packi bez konta/klucza/ opłaty według wydawcy. Oficjalny download zbiorczy z deklarowanym LICENSES.txt i rozmiarami. Brak potwierdzonego API wyszukiwania/pojedynczego downloadu i automatycznej aktualizacji katalogu.
- **Wyszukiwanie** — Strona pozwala wyszukiwać dźwięki i przeglądać półki. Paginacja maszynowa, języki zapytań i kontrakt filtrów Unknown. Po imporcie selekcja lokalna.
- **Szczegóły i tożsamość rekordu** — Strony dźwięków i LICENSES.txt według wydawcy podają tytuł, twórcę, źródło, licencję. Trwałe ID/metadane API/bitrate Unknown. Oryginalne ID stosować wyłącznie kiedy odczytane ze źródła.
- **Pobieranie** — Dwa pełne ZIP GitHub Releases (1,75 i 1,60 GB) oraz 69 oficjalnych mniejszych packów. Użyć małego zatwierdzonego pakietu albo ręcznie wybranego pliku. Manifestu zamkniętego w ZIP nie traktować jako prawa przed pobraniem packa.
- **Formaty i warianty** — ZIP zawierający audio i LICENSES.txt. W części pozycji 10-sekundowe wycinki. Docelowe kontenery, WAV vs. stratne warianty, kanały, sample rate i source quality Unknown per record. Pełne utwory, foley, ambiences i pętle. Zachować oznaczenie clip/excerpt, nie oferować jako pełnej wersji. Czy istnieje wybór formatów na plik Unknown.
- **Prawa do pliku i metadanych** — CC0, PD, CC BY oraz CC BY-SA według aktualnych packów. Starsza strona twierdzi brak ShareAlike. Każdy plik wymaga oryginalnego źródła, warunków i zgodności ze zgodą autora. Metadane API/katalogu Unknown.
- **Transport, cache i błędy** — clr.fm, github.com, host końcowy GitHub Releases do potwierdzenia bez rozszerzania trust. Cache, ETag, Last-Modified, signed URLs, pacing i kody błędów dla CLR Unknown.
- **Ryzyko i trudność integracji** — Agregator wtórny, rozbieżność licencji SA, preview/excerpt, ryzyko błędnego provenance i duplikaty z Incompetech. Nie pobierać pełnych paczek. Obecna obsługa ZIP dotyczy tekstur. Średni/wysoki. Najpierw ręcznie zweryfikowana lista wybranych rekordów. Opcjonalny importer małych paczek z kontrolą plików i praw po udokumentowaniu publicznego mapowania licencji na pliki przed dostępem. Brak stałego crawla.
- **Źródła pierwotne** — [av-clr-index](https://clr.fm/music/) (`INDEXED_EXCERPT`), [av-clr-about](https://clr.fm/openaudio/), [av-clr-respect](https://clr.fm/music/respect), [av-clr-licenses](https://clr.fm/music/licenses), [av-clr-packs](https://clr.fm/music/packs/), [av-clr-bulk](https://clr.fm/music/download/), [av-ccby](https://creativecommons.org/licenses/by/4.0/legalcode.en), [av-ccbysa](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en).


### Ograniczenie kwalifikacji i próbka rekordów

Najpierw zestawić stronę konkretnego dźwięku, wersję licencji oryginału i uprawnienia dla wybranego pliku, w tym odróżnić pełne wykonanie od przyciętego fragmentu. Wydawca deklaruje licencje CC0, PD, BY i BY-SA, podczas gdy starsza strona wyklucza SA. Rozbieżność blokuje kwalifikowanie paczki na podstawie zbiorczej deklaracji. Synchronizacja fonogramu, muzyki lub wykonania z ruchomym obrazem pod CC BY-SA 4.0 jest adaptacją i wymaga oceny warunku SA przy dalszym udostępnianiu. Ten przypadek nie przejdzie importu Earshot w aktualnym baseline. Ustalić także uprawnienia osób trzecich i prawo do redystrybucji oryginalnego pliku. [Deklaracja CLR](https://clr.fm/openaudio/), [starsza polityka](https://clr.fm/music/licenses), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en), [baseline](../baseline/BASELINE.md).

Dwa wielkie ZIP-y przekraczają 32 MiB. Dla mniejszych pakietów samo `LICENSES.txt` dostępne dopiero po pobraniu nie daje pozytywnego dowodu przed wyborem. Wymagane publiczne mapowanie nazwa → źródło → prawa, a ewentualny importer audio ZIP musiałby rozszerzyć dzisiejszą ścieżkę tekstur o walidację zawartości, limity sumy bajtów po rozpakowaniu i bezpieczną kontrolę ścieżek. Ręcznie sprawdzony pojedynczy plik jest prostszą próbą. Deduplikację z Incompetech i innymi dostawcami oprzeć o źródłowe ID, twórcę, wersję oraz hash w razie dostępności. [Pakiety](https://clr.fm/music/packs/), [pełne archiwa](https://clr.fm/music/download/), [baseline](../baseline/BASELINE.md).

| Rekord | Widoczne informacje | Ograniczenie dowodu |
| --- | --- | --- |
| `av-r-clr-alfama` · Alfama street, Lisbon | Opisany jako 10-sekundowy wycinek, dio_333, CC BY 3.0. | CLR wskazuje Freesound `173901`. Źródłowego rekordu nie odczytano, licencja i wariant źródłowy do potwierdzenia. [Deklaracja CLR](https://clr.fm/openaudio/). |
| `av-r-clr-newer` · Newer Wave | 2:55, Songs & Full Tracks, oznaczenie CC BY 4.0. | `INDEXED_EXCERPT`. Autor i wersja pliku w badanym rekordzie Unknown. Możliwy duplikat Incompetech do sprawdzenia. [Indeks](https://clr.fm/music/). |
| `av-r-clr-foley` · Noise Two | 0:01, Foley Effects, oznaczenie CC0. | `INDEXED_EXCERPT`. Autor, sposób powstania, konkretny wariant, prawa do oryginału i URL pliku Unknown. [Indeks](https://clr.fm/music/). |

Każdy przykład ma `REVIEW_REQUIRED`. URL wskazują dowody odkrycia pozycji. Nie ustalono kanonicznego ID CLR, bezpośredniego URL, rozmiaru, kanałów ani formatu dla żadnego z trzech przykładów.
## Blender Open Movies

Zakres `SURVEY`. Nowość `NEW_PROVIDER`. Kwalifikacja `MANUAL`. `PROVIDER_ELIGIBILITY=MANUAL_CURATED_STATIC`, `ASSET_ELIGIBILITY=REVIEW_REQUIRED_PER_ASSET`, `HOST_READINESS=NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `NOT_RUN`, `Unknown`.

- **Właściciel i kategorie** — Blender Foundation / Blender Studio. `video`, `audio`. [Strona źródła](https://studio.blender.org/films/)
- **Nowość i zastosowanie** — Nieobecny w baseline. Otwarte filmy i zasoby projektu, użyteczne dla pojedynczych ujęć/animacji, ograniczone zastosowanie jako stock.
- **Dostęp, koszty i automatyzacja** — `OFFICIAL_STATIC_FILM_CATALOGUE`. Publiczne strony projektów i wskazane wydania Big Buck Bunny. Ceny i konto dla innych ścieżek Vault Unknown per projekt. Oficjalny indeks filmów i osobne strony wydań. Dozwolone pobieranie i redystrybucja materiału Big Buck Bunny na podstawie jego licencji, warunki ruchu maszynowego Unknown.
- **Wyszukiwanie** — Lista projektów wg tytułu/roku i opisów. Brak potwierdzonego API pełnotekstowego, tagów, języków i paginacji.
- **Szczegóły i tożsamość rekordu** — Strony filmu i wydania. Klucz projekt/konkretny plik. Credits filmu i ewentualne oddzielne prawa składników. Asset ID wewnętrznego API Unknown.
- **Pobieranie** — Projekt wskazuje download.blender.org. Odczyt katalogu 4K w web zakończony 402. Publiczne pliki produkcyjne innych projektów i Vault wymagają osobnej weryfikacji.
- **Formaty i warianty** — Udokumentowane wydania 4K/HFR/3D dla BBB. Konkretne kodeki, fps, audio channels i alfa poszczególnych plików Unknown. Oddzielne wydania filmu oraz zasoby produkcji. Pozycja w Vault ani plik .blend nie są dowodem dostępnego, zdekodowanego wideo z alfą.
- **Prawa do pliku i metadanych** — Big Buck Bunny CC BY 3.0. Inne projekty, soundtrack i pliki źródłowe wymagają osobnych dowodów. Licencja metadanych katalogu Unknown.
- **Transport, cache i błędy** — studio.blender.org, peach.blender.org, download.blender.org. Redirecty, limity, signed URLs, cache, ETag/Last-Modified i Retry-After Unknown.
- **Ryzyko i trudność integracji** — Duże pliki, rozbieżności praw per element, dostępność starszych linków, formaty obrazów klatkowych i aktywne pliki źródłowe poza downloaderem. Mały ręczny manifest filmu/fragmentu z licencją, wersją i autorami. Nie włączać całej biblioteki do automatu. Pliki scen i renderowanie zostawić Studio.
- **Luki do zamknięcia** — Błąd 402 dotyczy narzędzia odczytu. Cena rzeczywistego wydania, bajty, konkretne warianty i końcowe URL pozostają do sprawdzenia. Zweryfikować atrybucję konkretnego fragmentu i osobno materiały osób trzecich, szczególnie soundtrack. Rozdzielczość, czas, FPS, kanały i alfa dla wybranego pliku Unknown.
- **Źródła pierwotne** — [av-blender-films](https://studio.blender.org/films/), [av-blender-bbb](https://peach.blender.org/about/), [av-blender-dl](https://peach.blender.org/download/), [av-blender-dir-unread](https://download.blender.org/demo/movies/BBB/) (`BLOCKED`), [av-blender-vault](https://studio.blender.org/vault/).

## Freesound

Zakres `SURVEY`. Nowość `NEW_PROVIDER`. Kwalifikacja `OPTIONAL`. `PROVIDER_ELIGIBILITY=OUT_OF_CORE_ACCOUNT_KEY_API_TERMS`, `ASSET_ELIGIBILITY=CONDITIONAL_PER_ASSET`, `HOST_READINESS=NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `NOT_RUN`.

- **Właściciel i kategorie** — Universitat Pompeu Fabra / Music Technology Group. `sfx`, `audio`. [Strona źródła](https://freesound.org/)
- **Nowość i zastosowanie** — Brak bezpośredniego adaptera. Szeroki katalog recordedSFX, ambiences, foley i syntetycznych dźwięków.
- **Dostęp, koszty i automatyzacja** — `DOCUMENTED_AUTHENTICATED_API`. Konto i klucz dla API. Oryginały OAuth2. Bezpłatne tylko niekomercyjnie, komercyjnie indywidualna umowa/koszt Unknown. Udokumentowana automatyzacja po uzyskaniu klucza i uprawnień. Nie stosować preview w celu ominięcia OAuth2.
- **Wyszukiwanie** — `GET /apiv2/search/`. Tekst, tagi, czas, typ, licencja i cechy audio w filtrach, paginacja `page/page_size`. Pełny zakres obsługi języków Unknown.
- **Szczegóły i tożsamość rekordu** — `GET /apiv2/sounds/{sound_id}/`. Id, username, created, license, typ, czas, sample rate, kanały i udostępnione pola.
- **Pobieranie** — `GET /apiv2/sounds/{sound_id}/download/` z OAuth2 dla oryginału. Preview URLs w danych, ale uprawnienia API wymagają osobnego rozpatrzenia.
- **Formaty i warianty** — Oryginały np. WAV, AIF, FLAC, OGG, MP3. Preview MP3/OGG w różnych jakościach. Długość, sample rate i kanały według rekordów. Original i transkodowane preview. SoundID zachować razem z wybranym wariantem.
- **Prawa do pliku i metadanych** — Sprawdzić licencję per asset (CC0/CC BY/NC, starsze profile). Warunki API oddzielne od licencji pliku. Nie zakładać praw osoby trzeciej w zgłoszeniach użytkowników.
- **Transport, cache i błędy** — freesound.org. Właściwe hosty preview/redirecty/Cache-Control/ETag/Last-Modified i TTL finalnych URL Unknown. OAuth access token 24 h. 401 dla wygasłego tokenu. Limity API przydzielane.
- **Ryzyko i trudność integracji** — API-komercjalizacja osobna od CC. Ochrona sekretów, identyfikacja aplikacji, zmiana statusu licencji. Nie mylić odsłuchu preview z wersją produkcyjną. Poza bieżącym zakresem. Ewentualny osobny adapter opt-in po warunkach dostawcy. Metadata-only discovery nie przyznaje dostępu do oryginałów.
- **Luki do zamknięcia** — Zastosowania ambience i foley zależą od rzeczywistego źródła i praw każdego dźwięku. Licencja danych do redystrybucji, konkretne limity, kody błędów poza udokumentowanym przypadkiem OAuth i Retry-After dla tej trasy Unknown. Redystrybucję pliku oceniać na podstawie jego licencji i udokumentowanego grantora. Rozdzielczość, FPS i alfa nie dotyczą audio.
- **Źródła pierwotne** — [av-fs-res](https://freesound.org/docs/api/resources_apiv2.html), [av-fs-auth](https://freesound.org/docs/api/authentication.html), [av-fs-overview](https://freesound.org/docs/api/overview.html), [av-fs-terms](https://freesound.org/help/tos_api/), [av-fs-cost](https://freesound.org/docs/api/terms_of_use.html).

## BBC Sound Effects / RemArc

Zakres `SURVEY`. Nowość `NEW_PROVIDER`. Kwalifikacja `REJECTED`. `PROVIDER_ELIGIBILITY=OUT_OF_CORE_NONCOMMERCIAL`, `ASSET_ELIGIBILITY=BLOCKED_COMMERCIAL`, `HOST_READINESS=NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `NOT_RUN`.

- **Właściciel i kategorie** — BBC. `sfx`, `audio`. [Strona źródła](https://sound-effects.bbcrewind.co.uk/)
- **Nowość i zastosowanie** — Brak w baseline. Nagrania produkcyjne i terenowe z BBC obejmują luki ambience/foley.
- **Dostęp, koszty i automatyzacja** — `MANUAL_CATALOGUE`. Darmowe warunkowo do użytku osobistego/edukacyjnego/badawczego zgodnego z RemArc. Komercyjnie osobna licencja Pro Sound Effects, koszt Unknown. Publiczny katalog i własne warunki. Brak potwierdzonego produkcyjnego API wyszukiwania i pobierania.
- **Wyszukiwanie** — Strona wyszukuje i pozwala filtrować długość. Tagi, język, paginacja i kontrakt maszynowy Unknown.
- **Szczegóły i tożsamość rekordu** — Karta efektu z opisem i wariantami. ID stabilne dla integracji, autorska data nagrania i licencja per asset w API Unknown.
- **Pobieranie** — Ręczna strona efektu, komercyjnie odnośnik Buy sound. Brak zweryfikowanego publicznego endpointu download.
- **Formaty i warianty** — Warianty mono i stereo według FAQ. Kontener/sample rate per rekord Unknown. Wybór stereo, jeśli istnieje, i zakresy czasu. Redystrybucja tylko w granicach RemArc/odrębnej licencji.
- **Prawa do pliku i metadanych** — OGL v3 tylko metadane. Dźwięk własne warunki RemArc. Komercyjny i reklamowy użytek blokować w obecnej ścieżce.
- **Transport, cache i błędy** — sound-effects.bbcrewind.co.uk. Hosty plików, redirecty, limity, TTL/cache/ETag/Last-Modified/Retry-After Unknown.
- **Ryzyko i trudność integracji** — Licencja metadanych mylona z prawem nagrań. Ograniczenia promocji, monetyzacji i biznesu. Nie wdrażać dla reklamy/produkcji komercyjnej. Osobna decyzja o użyciu poza Open Assets.
- **Luki do zamknięcia** — Brak potwierdzenia danych technicznych, autora i direct URL dla wskazanego pliku. Opłata i zakres synchronizacji/redystrybucji w umowie komercyjnej Unknown. Rozdzielczość, FPS i alfa nie dotyczą audio.
- **Źródła pierwotne** — [av-bbc-terms](https://sound-effects.bbcrewind.co.uk/licensing), [av-bbc-faq](https://sound-effects.bbcrewind.co.uk/faqs).

## Lots of Sounds

Zakres `SURVEY`. Nowość `NEW_PROVIDER`. Kwalifikacja `OPTIONAL`. `PROVIDER_ELIGIBILITY=OUT_OF_CORE_PAID_KEY`, `ASSET_ELIGIBILITY=CC0_DECLARED`, `HOST_READINESS=NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `NOT_RUN`.

- **Właściciel i kategorie** — Lots of Sounds, podmiot prawny Unknown. `sfx`, `audio`, `music`. [Strona źródła](https://www.lotsofsounds.com/)
- **Nowość i zastosowanie** — Brak w baseline. Katalog efektów, ambience i muzyki, audio deklarowane CC0.
- **Dostęp, koszty i automatyzacja** — `DOCUMENTED_AUTHENTICATED_API`. Pro od 15 USD/mies., konto i `x-api-key`. Pro 2500 wywołań/dobę, Enterprise 50000. Wersja WWW ma bezpłatne ręczne pobrania w limicie według strony. REST i MCP dla integratorów. `GET /api/v1/sounds/sample` bez klucza zwraca wyłącznie kuratorowaną próbkę formatu, bez wyszukiwania i autoryzacji pełnego download.
- **Wyszukiwanie** — `GET /api/v1/sounds`. Q, kategorie, AND tagów, długość i sortowanie/paginacja. Języki poza domyślnym katalogiem Unknown.
- **Szczegóły i tożsamość rekordu** — `GET /api/v1/sounds/{id}`. Rekordy dokumentują id, typ/category, duration, tags, license. Źródło pierwotne/autorstwo i data per plik do potwierdzenia.
- **Pobieranie** — `GET /api/v1/sounds/{id}/download` generuje podpisany URL na godzinę. Download i full search z kluczem.
- **Formaty i warianty** — MP3. Bitrate, kanały i oryginał bezstratny Unknown. Oddzielne stream/download. Innych formatów nie potwierdzono.
- **Prawa do pliku i metadanych** — CC0 1.0 dla audio według publikującego. Terminy dostępu do API i prawa witryny/metadanych odrębne od CC0 pliku.
- **Transport, cache i błędy** — api.lotsofsounds.com, host finalnego CDN Unknown. 401, 429 i X-RateLimit-Reset udokumentowane. ETag/Last-Modified/cache Unknown.
- **Ryzyko i trudność integracji** — Koszt i klucz blokują core. CC0 dostępu do preview nie rozwiązuje prawa do automatyzacji pobierania poza uprawnioną trasą. Oddzielny opcjonalny adapter po zmianie zakresu. Nie wdrażać sample jako substytutu API.
- **Luki do zamknięcia** — Przydatność do nagrywanego foley zależy od udokumentowania techniki powstania efektów. Zakres praw osób trzecich, data i autor, parametry produkcyjne, przekierowania i Retry-After dla pliku Unknown. CC0 dotyczy praw, które dostawca może przekazać. Rozdzielczość, FPS i alfa nie dotyczą audio.
- **Źródła pierwotne** — [av-los-api](https://www.lotsofsounds.com/docs/api-reference), [av-los-license](https://www.lotsofsounds.com/license), [av-los-pricing](https://www.lotsofsounds.com/), [av-los-terms](https://www.lotsofsounds.com/terms).

## Free To Use

Zakres `SURVEY`. Nowość `NEW_PROVIDER`. Kwalifikacja `REJECTED`. `PROVIDER_ELIGIBILITY=OUT_OF_CORE_LICENSE`, `ASSET_ELIGIBILITY=BLOCKED_COMMERCIAL_FREE_TIER`, `HOST_READINESS=NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `NOT_RUN`.

- **Właściciel i kategorie** — Free To Use, podmiot prawny Unknown. `music`. [Strona źródła](https://freetouse.com/api)
- **Nowość i zastosowanie** — Brak w baseline. Muzyka wielu wykonawców z publicznym bezkluczowym API.
- **Dostęp, koszty i automatyzacja** — `DOCUMENTED_PUBLIC_API`. API bez konta, klucza i opłaty. Dla zakresu Commercial Content odrębna płatna licencja. Ceny Unknown. Udokumentowana automatyzacja, niezależna od praw filmu i dystrybucji samych plików.
- **Wyszukiwanie** — `GET https://api.freetouse.com/v3/music/tracks/search` z `query`, `limit`, `offset`, order/sort. Tytuły, tagi, kategorie, artyści. Osobne category/artist listings.
- **Szczegóły i tożsamość rekordu** — `GET /v3/music/tracks/{id}` UUID, `artists`, `release_date`, `duration`, `is_premium`, komplet tagów/kategorii. Pole języka lyrics nie jest gwarancją wielojęzycznego search.
- **Pobieranie** — `files.mp3` zwraca URL w rekordzie, host i zachowanie signed/redirect Unknown.
- **Formaty i warianty** — MP3. Sample rate, kanały, bitrate i alternatywne pliki Unknown. Free/premium jako uprawnienia, bez potwierdzonego zestawu formatów.
- **Prawa do pliku i metadanych** — Free To Use Free License zezwala na określone UGC z atrybucją, w tym jego monetizację, i wyklucza Commercial Content/Broadcast Content/Digital Products/Physical Products. Własna licencja.
- **Transport, cache i błędy** — api.freetouse.com. Dokumentacja 400/500. Rate limit, cache/ETag/Last-Modified, 429/Retry-After i host CDN Unknown.
- **Ryzyko i trudność integracji** — Darmowe API i UGC monetized nie spełniają żądanego komercyjnego zakresu. Ochrona praw wykonawców/poszczególnych plików zależy od licencji dostawcy. Brak integracji core. Jeśli zakres biznesowy się zmieni, osobne rozpoznanie licencji.
- **Luki do zamknięcia** — Data publikacji i artyści są w schemacie. Prawa metadanych do redystrybucji, licencja per plik, prawa do przekazywania pliku, parametry kodowania i domena downloadu Unknown. Rozdzielczość, FPS i alfa nie dotyczą audio.
- **Źródła pierwotne** — [av-ftu-api](https://freetouse.com/api), [av-ftu-openapi](https://api.freetouse.com/v3/openapi.json), [av-ftu-rights](https://freetouse.com/license).

## Pixabay Video

Zakres `SURVEY`. Nowość `NEW_PROVIDER`. Kwalifikacja `OPTIONAL`. `PROVIDER_ELIGIBILITY=OUT_OF_CORE_ACCOUNT_KEY`, `ASSET_ELIGIBILITY=PROPRIETARY_REVIEW_REQUIRED`, `HOST_READINESS=NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `NOT_RUN`.

- **Właściciel i kategorie** — Pixabay, marka Canva Germany GmbH. `video`. [Strona źródła](https://pixabay.com/api/docs/)
- **Nowość i zastosowanie** — Brak w baseline. Współczesny B-roll stockowy i animacje w API, zakres inny niż NASA/Commons.
- **Dostęp, koszty i automatyzacja** — `DOCUMENTED_AUTHENTICATED_API`. Login i klucz. Dokumentacja opisuje darmowe API przy wskazaniu źródła wyników. Zwiększone limity mogą wymagać uzgodnienia. Udokumentowana integracja wyszukiwania wideo per użytkownik. Zakaz masowego systematycznego downloadu i obowiązek 24h cache.
- **Wyszukiwanie** — `GET /api/videos/` z `key`, `q`, `lang`, `video_type`, `category`, min width/height, `page` i `per_page` (3–200). Max 500 wyników na zapytanie w standardzie.
- **Szczegóły i tożsamość rekordu** — Ten sam endpoint z `id`. Id, pageURL, user, duration i obiekty wariantów. Data, licencja wersjonowana per rekord i audio/alpha w odpowiedzi Unknown.
- **Pobieranie** — `videos.{large,medium,small,tiny}.url` i udokumentowany `download=1`. Domena `cdn.pixabay.com` w dokumentacji.
- **Formaty i warianty** — MP4 z wymiarami i przybliżonym size. 4K/1080p zależnie od rekordu. FPS, kodek, kanały audio i alfa Unknown. Cztery renditions, część dużych może nie istnieć. Brak kwalifikacji do stock alpha na podstawie video_type=animation.
- **Prawa do pliku i metadanych** — Pixabay Content License. Komercyjne adaptacje warunkowe, zakaz samodzielnego stocku i ograniczenia rozpoznawalnych znaków/osób. Atrybucja w użyciu assetu odrębna od kredytu w API. Licencja metadanych do re-use poza warunkami API Unknown.
- **Transport, cache i błędy** — pixabay.com i cdn.pixabay.com. 100 żądań/60s per key i nagłówki X-RateLimit, 429 plain text, cache 24 h. ETag/Last-Modified/TTL URL wideo/Retry-After Unknown.
- **Ryzyko i trudność integracji** — Własna licencja i znaki. Wymagane konto. API dokumentuje zdjęcia i wideo, a sekcje WWW muzyki/SFX nie stanowią API. Osobna ścieżka opcjonalna po jawnej zmianie zasad i review licencji. Brak potrzeby rozwoju dla core.
- **Luki do zamknięcia** — Przydatność konkretnego ujęcia do reklamy wymaga sprawdzenia release, znaków, praw autorskich do elementów kadru oraz wariantu bez niespodziewanego audio. Stabilność URL, reguły przekierowań i podpisy URL Unknown.
- **Źródła pierwotne** — [av-pix-api](https://pixabay.com/api/docs/), [av-pix-terms](https://pixabay.com/service/terms/), [av-pix-lic](https://pixabay.com/service/license-summary/).

## Mixkit

Zakres `SURVEY`. Nowość `NEW_PROVIDER`. Kwalifikacja `MANUAL`. `PROVIDER_ELIGIBILITY=MANUAL_ONLY_PROPRIETARY`, `ASSET_ELIGIBILITY=PROPRIETARY_REVIEW_REQUIRED`, `HOST_READINESS=NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `NOT_RUN`.

- **Właściciel i kategorie** — Envato. `sfx`, `music`, `video`. [Strona źródła](https://mixkit.co/)
- **Nowość i zastosowanie** — Brak w baseline. Katalog stock, efektów, ambience i muzyki.
- **Dostęp, koszty i automatyzacja** — `MANUAL_CATALOGUE`. Bezpłatna strona bez konta dla wybranych plików. Oficjalne publiczne API niepotwierdzone. User Terms zabraniają masowego pobierania botami/skryptami. Brak potwierdzonego kontraktu dla adaptera.
- **Wyszukiwanie** — Przeglądanie, tagi i kategorie interfejsu. Kontrakt maszynowy, paginacja, języki i filtry API Unknown.
- **Szczegóły i tożsamość rekordu** — Tytuł, długość i własny wariant licencji na stronie. Stabilne ID API, twórca i data per plik Unknown.
- **Pobieranie** — Ręczny przycisk na stronie. Nie używać endpointów aplikacji lub nieudokumentowanych linków CDN.
- **Formaty i warianty** — WAV/MP3 w SFX według strony. Wideo HD/4K na niektórych stronach. Kontener, fps, audio, alfa per asset Unknown. Rozdzielczości i odrębne licencje stocku, zasięg warunków dla wariantu sprawdzać przy pobraniu.
- **Prawa do pliku i metadanych** — Odrębne Mixkit Free/Restricted per rodzaj. SFX Free do włączenia w projekt. Brak redystrybucji jako stock lub z plikami źródłowymi. Video Restricted niekomercyjne. Odrębne warunki muzyki i prawa osoby/marki.
- **Transport, cache i błędy** — mixkit.co. Hosty finalne, redirecty, signed TTL, cache, ETag/Last-Modified, limity/Retry-After Unknown.
- **Ryzyko i trudność integracji** — Ryzyko licencji zależnej od typu/pozycji. Handoff surowych plików, template i użycie jako stock mogą naruszać licencję. Manual tylko dla własnego, zaakceptowanego projektu. Brak adaptera w obecnym kontrakcie.
- **Luki do zamknięcia** — Licencja danych katalogu, prawa osób trzecich i kredyt dla konkretnego ujęcia do sprawdzenia przed użyciem. Brak potwierdzonych parametrów API, wariantów pliku i limitów dla automatyzacji. Dla projektu ręcznego zachować kopię właściwej licencji i kredyt dla wybranego pliku.
- **Źródła pierwotne** — [av-mix-terms](https://mixkit.co/terms/), [av-mix-lic](https://mixkit.co/license/), [av-mix-sfx-lic](https://mixkit.co/license/modal/sfxFree/), [av-mix-sfx](https://mixkit.co/free-sound-effects/), [av-mix-video](https://mixkit.co/free-stock-video/?resolution=HD).

## Sonniss #GameAudioGDC

Zakres `SURVEY`. Nowość `NEW_PROVIDER`. Kwalifikacja `MANUAL`. `PROVIDER_ELIGIBILITY=MANUAL_ONLY_PROPRIETARY`, `ASSET_ELIGIBILITY=PROPRIETARY_REVIEW_REQUIRED`, `HOST_READINESS=NOT_RUN`. Priorytet `P2`. Dowody `DOCUMENTED`, `NOT_RUN`.

- **Właściciel i kategorie** — Sonniss Limited. `sfx`, `audio`. [Strona źródła](https://gdc.sonniss.com/)
- **Nowość i zastosowanie** — Brak w baseline. Dźwięki produkcyjne wielu autorów, z istotną rolą foley/ambience w obrębie paczek.
- **Dostęp, koszty i automatyzacja** — `OFFICIAL_STATIC_RELEASE_PACKS`. Publiczne darmowe ZIP wydania 2026. Osobna licencja do dalszego udostępniania wymaga zgody. Koszt rozszerzonych praw Unknown. Oficjalne ZIP i torrent. Wsparcie maszynowego wyszukiwania pojedynczych plików i zdalnego odczytu archive ranges Unknown.
- **Wyszukiwanie** — Oficjalna lista ścieżek edycji 2026 linkowana z witryny, zawartość listy 2026 nieodczytana. Pełnotekstowe API, języki, paginacja Unknown.
- **Szczegóły i tożsamość rekordu** — ID wydania, pack, nazwa pliku, twórca/label po sprawdzeniu listy. Stabilne ID per plik w API, date, parametry kanałów Unknown.
- **Pobieranie** — Oficjalne pięć ZIP na `downloads.sonniss.com` i wskazane alternatywy. Nie odczytywano binariów, oficjalnego torrenta ani indywidualnych download URL.
- **Formaty i warianty** — ZIP. Rzeczywiste audio formaty, sample rate, czas i warianty wewnątrz nieodczytane. Pięć części pakietu. Warianty/wybór pojedynczego pliku przed pobraniem Unknown.
- **Prawa do pliku i metadanych** — Własna GDC EULA v2 od 27.08.2026, właściwa wersja z dnia pobrania. Użycie w synchronizacji w gotowym projekcie, ograniczenia przekazywania SFX jako plików, wyjątek dla zespołu, zastrzeżenie zastosowań AI. Właściciele per plik według tracklisty.
- **Transport, cache i błędy** — gdc.sonniss.com i downloads.sonniss.com. Dodatkowe mirrory istnieją, pozostają poza propozycją. Limity/rozmiary plików, signed URLs, redirecty, cache i nagłówki Unknown.
- **Ryzyko i trudność integracji** — Licencja dotyczy synchronizacji, ogranicza dostarczanie surowych efektów, własne ograniczenia AI. Ustalić czy zamierzony sposób przetwarzania przez narzędzie jest objęty zgodą. Aktualna polityka Open Assets/Earshot nie dopuszcza tej licencji. Manual po review praw i rozmiarów. Integracja wymagałaby nowego modelu praw, pracy z wielkimi pakietami i odrębnego zakresu.
- **Luki do zamknięcia** — Przed użyciem odczytać tracklistę i sprawdzić twórcę, rozmiar, konfigurację kanałów, czas oraz warunki licencji na przetwarzanie i przekazanie w zespole. Licencja metadanych, kody błędów i Retry-After Unknown. Rozdzielczość, FPS i alfa nie dotyczą audio.
- **Źródła pierwotne** — [av-son-lic](https://sonniss.com/gdc-bundle-license/), [av-son-bundle](https://gdc.sonniss.com/).
