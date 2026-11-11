# DR-04 — trwałe rozszerzenie FrameCore Open Assets

Stan badania: **2026-11-11, Europe/Warsaw**. Hipson **T-0007**. Raport badawczy dla Claude, głównego architekta. Implementacja i testy dostawców: **NOT_RUN**.

Najlepszym następnym krokiem jest mały projekt rozszerzenia audio NASA oraz osobna decyzja o bezpiecznej obsłudze SVG i fontów. Internet Archive zasługuje na ograniczone badanie podkolekcji, lecz nie ma podstaw do przyjęcia całego katalogu. Badanie nie znalazło nowego, w pełni zakwalifikowanego źródła współczesnych nagrywanych SFX, komercyjnej muzyki wielu twórców i stockowego wideo z alfą, które jednocześnie spełniałoby wszystkie warunki bez opłat, konta i klucza. Ten brak jest wynikiem badania, nie powodem do obniżenia wymagań.

Pakiet obejmuje **26 pozycji**, **10 kart pogłębionych** i **22 odczytane rekordy lub wpisy metadanych**. Katalog zawiera 23 nowe źródła, 2 istotne rozszerzenia obecnych providerów i 1 rozpoznane pokrywanie się kolekcji. Nie są to 26 gotowych adapterów. Ranking: **3 CORE_CANDIDATE**, **13 OPTIONAL**, **6 MANUAL_REFERENCE_ONLY**, **4 REJECTED**. Wszystkie mają HOST_READINESS `NOT_RUN`. Pełne dane: [catalog.csv](catalog.csv), [catalog.json](catalog.json), [rankingi](RANKINGS.md), [rekordy](records.json).

## Baseline i rzeczywiste luki

Open Assets **0.5.0** przypięto do `889471fcdbc2216ddc465715eff0e82784d5b8ee` z 2026-11-06. Przeczytano README, skill, provider index, wszystkie dossier i adaptery, manifesty, rejestr, kontrakt, runtime, testy i ograniczenia. W pełnym drzewie brak AGENTS.md; jego odczyt dał 404. Kontekst: Studio **1.174.1**, `4611c9c4ed44579b8a2c0224c9276d955fccd8d6` z 2026-11-11; Toolbox **1.12.0**, `adc8094f8e087889e4337c99dd0d267ae1b11a51` z 2026-11-07. [Pełny audyt i przypięte źródła](baseline/BASELINE.md).

Rejestr obejmuje 15 dostawców i 24 pary provider–category. Wśród 23 historycznych prób Work pięć było technical-only: Commons photos/audio, NASA photos/video i LibriVox audio. Incompetech jest oddzielną historyczną próbą Claude Code. Nie wolno traktować wszystkich 24 ścieżek jako aktualnej zgody na produkcyjne użycie. Dwie lokalne kopie cache 0.5.0 odpowiadają 71/71 plikom przypiętego pakietu; aktywność klientów pozostaje Unknown. Repo, cache i działający host to różne obserwacje. [Walidacja autora](https://github.com/FrameCoreWorks/framecore-open-assets/blob/889471fcdbc2216ddc465715eff0e82784d5b8ee/docs/VALIDATION.md), [dane baseline](baseline/baseline.json).

| Potrzeba | Aktualny zakres | Wartość nowych kandydatów | Pozostała luka |
|---|---|---|---|
| Recorded SFX, ambience, foley | Commons audio/SFX; SFXMint syntetyczny | NPS ma konkretne nagrania manual, CLR ma paczki o mieszanych prawach, Archive może zawierać dozwolone podkolekcje | brak nowego zakwalifikowanego szerokiego no-key API recordedSFX |
| Muzyka | Incompetech jeden twórca; Commons szerokie audio; LibriVox audiobooki | Archive i CLR do wąskiego przeglądu; opcjonalne systemy kont/kluczy wyraźnie oddzielone | brak bezwarunkowej biblioteki muzyki reklamowej wielu twórców |
| Wideo, B-roll, alfa | NASA + Commons | NPS/Blender manual, Archive po prawach, Pixabay optional key | brak nowego core stock alpha; 32 MiB często ogranicza oryginały |
| Współczesna grafika | reprodukcje muzealne, bitmapy, sylwetki PhyloPic | Iconify skaluje ikony, PhyloPic SVG rozszerza wektory, Open Peeps ma ręczne materiały | ikony i muzealia nie zastępują pełnej biblioteki współczesnych ilustracji produktowych |
| Fotografie/wycięte obiekty | archiwa, muzea, Commons/NASA | Openverse tylko discovery, Unsplash optional key i własne warunki | brak nowego zakwalifikowanego stocku reklamowego/transparentnych wycięć |
| Tekstury/PBR/HDRI/3D | ambientCG ZIP z rastrami, Poly Haven diffuse/albedo | przyszłe rozszerzenie tych samych providerów; Quaternius manual | HDR/EXR/3D/rig/animacja wymagają nowych kontroli formatu, nie nowego banku URL |
| Fonty | brak kategorii | Fontsource API + źródłowe Google Fonts repo | nowa walidacja font software, OFL/notices i konsumentów |

Wnioski o lukach są DERIVED z kodu i kart. Dokładna lista bieżących providerów, ich filtry, formaty i dowody znajduje się w [baseline](baseline/BASELINE.md). AIC/Archive/ccMixter/Gallica historycznie usunięto; przy ponownej kwalifikacji pozostają NEW_PROVIDER względem obecnego pakietu. LibriVox używający hostów Archive nie oznacza integracji ogólnego katalogu Archive.

## Rekomendacje i zakres kwalifikacji

**NASA audio — CORE_CANDIDATE warunkowy, EXISTING_NEW_CATEGORY.** Dokumentacja API jawnie przewiduje audio i ten sam model manifestów co obecny adapter. To niewielkie rozszerzenie istniejącego modułu, ale wymaga oddzielnego proof dla audio i nadal `review_nasa`. W badaniu odczytano trzy wpisy Artemis na stronie NASA; nie potwierdzono ich przynależności do images-api ani NASA ID. Jeden podany wariant przekracza 32 MiB. Nie planować importu do obecnego Earshot przez obejście jego wymogu `eligible`. [NASA API](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf), [karty audio/wideo](audio_video/CARDS.md).

**Iconify — CORE_CANDIDATE warunkowy.** Dokumentowane publiczne API i użyteczne kolekcje ikon, lecz rozszerzenie wymaga SVG oraz praw per kolekcja/ikona. Pilot powinien dotyczyć jednej kolekcji, bez marek, z notice i obsługą wyjątków. Materiały źródłowe pokazują ISC, MIT oraz CC BY-SA; nie są zamienne. Zapasowych hostów API nie należy używać do obchodzenia blokady. [Iconify API](https://iconify.design/docs/api/), [karta i trzy rekordy](visual_data/CARDS.md).

**Fontsource — CORE_CANDIDATE warunkowy.** API udostępnia metadane i wersjonowane warianty bez konta/klucza; potrzebna jest nowa kategoria fontów i rozszerzenie jednej istniejącej polityki licencji o właściwy zakres OFL. Wybrane warianty WOFF/WOFF2/TTF nie są automatycznie wymienne między rendererami. Repo Google Fonts stanowi osobną drogę statyczną i dowód praw; rodziny z obu źródeł muszą być deduplikowane. [Fontsource API](https://fontsource.org/docs/api/introduction), [OFL](https://openfontlicense.org/open-font-license-official-text/), [karty](visual_data/CARDS.md).

**Internet Archive — OPTIONAL; P0 oznacza dalszą kwalifikację, nie implementację.** Publiczny katalog jest zbyt szeroki, aby jego prawa oceniać jednym znacznikiem. Pliki dodatkowe, soundtrack i warianty mogą mieć inne pochodzenie. Dwa odczytane przykłady pokazują historyczne oznaczenie PD USA i niejasne prawa; nie dają nowego wzorca bezwarunkowego PDM. Ogólne terms nie zostały w pełni odczytane, a rootowy ponowny odczyt strony bots był niedostępny. Zachować te luki przed dopuszczeniem. [Karta, źródła i historyczny kontekst](audio_video/CARDS.md).

**Wyzowl SFX Kit — OPTIONAL static manifest.** Wersjonowane metadane, CC0 i krótkie WAV są dobrym modelem małego manifestu, ale badane efekty są syntetyczne. Nie zastępują nagrywanego foley. Nie uruchamiać generatorów repo w downloaderze. **CLR — OPTIONAL static pack**, ponieważ prawa są mieszane, deklaracje SA niespójne, część nagrań to krótkie wycinki, a paczki mogą znacznie przekraczać limit. **NPS — MANUAL**, mimo konkretnych public-domain nagrań i B-roll: nie potwierdzono maszynowego katalogu kolekcji. [Pełne karty](audio_video/CARDS.md).

Pozostałe decyzje opisano w [RANKINGS.md](RANKINGS.md). OPTIONAL zachowuje powód OUT_OF_CORE, gdy potrzebny jest klucz, konto, opłata lub szczególna licencja. REJECTED oznacza odrzucenie proponowanej automatycznej integracji w tym zakresie, nie ogólną ocenę serwisu. Np. BBC ma ograniczenia NC nagrań, Free To Use ograniczenia bezpłatnej licencji komercyjnej, a unDraw/ShareTextures nie dają tu podstaw do automatycznej integracji. Nie zaliczono popularności jako dowodu przydatności.

## Głębokość i rzeczywiste rekordy

| Karta pogłębiona | Odczytane wpisy | Rodzaj dowodu / ograniczenie |
|---|---:|---|
| NASA audio | 3 | strony Artemis, bez NASA ID i bez dowodu membership w images-api |
| Internet Archive curated | 2 | rzeczywiste strony item; PD USA/niejasne prawa, bez potwierdzenia pobrania |
| Wyzowl SFX Kit | 2 | manifest przy commit SHA; parametry deklarowane, binaria NOT_RUN |
| CLR Music | 3 | wpisy źródłowe/paczki; nie każdy ma kompletny manifest pojedynczego pliku |
| NPS sound/video | 3 | strony rekordów; manual access, brak API tych kolekcji |
| Iconify | 3 | rekordy trzech zbiorów z różnymi licencjami |
| Fontsource | 2 | jeden JSON i jedna strona fontu; brak pełnych danych CDN w drugim |
| Google Fonts repo | 2 | METADATA.pb i OFL przy commit SHA; te same rodziny co Fontsource |
| Art Institute of Chicago | 2 | API: public-domain flag true/false; oba mogą mieć image_id; legal pages 403 |
| Openverse | 0 | spec w indeksowanym widoku; odczyt bezpośredni 403, brak prób obejścia |

Suma 22 obejmuje różne rodzaje rekordów, nie 22 odrębne pobrane pliki ani 22 kandydatów produkcyjnych. Brak dwóch przykładów dla Openverse jest jawny. Każdy odczyt ma URL, datę, source ID i status w [records.json](records.json). Ścieżki wariantów nie są generowane, gdy źródło ich nie podało. Nie przypisano zmyślonych SHA-256, czasu trwania, kanałów czy alfy.

## Kontrakt, bezpieczeństwo plików i granice konsumentów

Zachować istniejące `core.asset()`, `license_policy()`, `Client` i `framecore-task-result/1`. Sidecar używa `id/source_page/license`, envelope `asset_id/source_url/licence`. Nie tworzyć drugiego katalogu praw, generalnego downloadera arbitrary URL ani oddzielnego politycznego retry. Projekty dziewięciu dróg opisuje [ADAPTER_DESIGNS.md](ADAPTER_DESIGNS.md).

Dzisiejszy runtime rozpoznaje raster, wybrane texture ZIP oraz obsługiwane sygnatury A/V; SVG/fonty/3D/HDRI nie są natywnie weryfikowane. ZIP nie jest ekstrahowany. A/V verification nie zapisuje FPS, kanałów, sample rate ani alfy. Limity 32 MiB, 40 MP, 100 ZIP entries/128 MiB expanded i ograniczenia czasu pozostają. Nowe formaty i addytywne parametry są propozycją do decyzji Claude. Udany decode nie mówi o wyglądzie lub brzmieniu. [Kod core](https://github.com/FrameCoreWorks/framecore-open-assets/blob/889471fcdbc2216ddc465715eff0e82784d5b8ee/plugins/framecore-open-assets/scripts/core.py).

401/403/429/challenge i hostowy `network_blocked` kończą daną drogę. Runtime nie wykonuje automatic retry ani failover. Jedna dodatkowa ręczna próba może dotyczyć błędu przejściowego z nazwaną hipotezą i poszanowaniem Retry-After; nie służy ponawianiu blokady. JSON cache pozostaje exact URL+Accept, z TTL/ETag i respektowaniem no-store/no-cache/private. [Kontrakt](https://github.com/FrameCoreWorks/framecore-open-assets/blob/889471fcdbc2216ddc465715eff0e82784d5b8ee/plugins/framecore-open-assets/skills/open-assets/references/contract.md).

## Wdrożenie jako osobny etap

[BACKLOG.md](BACKLOG.md) i [backlog.json](backlog.json) zawierają 10 zadań z celem, wejściami, wyjściami, właścicielem, zależnościami, błędami, limitami, kosztem i akceptacją. Priorytety implementacyjne w głównym BACKLOG.md są nadrzędne względem ocen atrakcyjności w kartach specjalistycznych (np. Iconify P0 w karcie jest B05/P1 dla wykonania; Archive P0 to kwalifikacja, nie wdrożenie). P0 to ustalenie dokładnego zakresu, próba kwalifikacji Archive, NASA audio i zgodność konsumentów; P1 to SVG/fonty/static SFX oraz jawna decyzja o nierozwiązanych lukach; P2 to dalsze formaty i uzupełniające źródła. Nie ma podstaw do zbiorczej aktywacji wszystkich providerów.

[TEST_PLAN.md](TEST_PLAN.md) opisuje 20 małych prób, wszystkie NOT_RUN, ze stop po blokadzie i preferencją jednego pliku ≤5 MiB. [MANIFEST_EXAMPLE.json](MANIFEST_EXAMPLE.json) jest niewykonywalnym szablonem projektowym z realną tożsamością rekordu i pustymi wynikami wykonania. [IMPLEMENTATION_HANDOFF.md](IMPLEMENTATION_HANDOFF.md) wskazuje konkretne decyzje dla Claude.

## Dowody, braki i odbiór badania

[sources.json](sources.json) / [CSV](sources.csv) zawierają także nieudane odczyty, jawnie oznaczone. Liczby wpisów i unikatowych URL, ze statusem READ/BLOCKED/INDEXED_EXCERPT, znajdują się w [summary.json](summary.json); lista URL nie jest traktowana jako lista przeczytanych źródeł. Pin datuje stan repo, nie gwarantuje przyszłej stałości API/warunków. Rejestr niepewności: [GAPS.md](GAPS.md).

Rzeczywisty swarm obejmował trzy specjalizacje na rozłącznych plikach i osobną świeżą recenzję. Role, przebieg, przerwanie oraz obserwacje modeli: [RUN_LOG.md](RUN_LOG.md). Claude CLI pominięto zgodnie z udzielonym wyjątkiem po OAuth401; nie próbowano logowania ani fallbacku. Wynik nie jest zatwierdzeniem architektury przez Claude.

Końcowy status kontroli dokumentów i recenzji zapisuje [VERIFICATION.md](VERIFICATION.md). Skrypt `verify_artifacts.py` bada integralność, referencje, liczniki i zachowanie oryginalnego promptu. Nie wykonuje kandydatów, nie pobiera próbek ani nie potwierdza integracji. Brak instalacji, publikacji, pushu, prywatnych uploadów i zmian wtyczek. Shared i główny INDEX.json pozostają poza zakresem zapisu tego badania.
