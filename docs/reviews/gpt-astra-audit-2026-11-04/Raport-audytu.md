# Audyt FrameCore Works Creative Studio

Data: 4 listopada 2026. Audyt zakończony z ograniczeniami wskazanymi przy każdej metodzie. Zakres obejmuje źródła, istniejące zapisy pluginów, lokalne testy i 110 syntetycznych profili. Poprawek produktu nie wdrażano.

## Wniosek

Studio ma rozbudowany warsztat kreatywny i sensowny podział odpowiedzialności. Największą wartość przyniesie teraz usunięcie sprzecznych instrukcji, wzmocnienie kontraktów integracji oraz sprawdzenie zachowania i efektów nauki. Dokładanie kolejnych skilli przed tym etapem zwiększyłoby koszt utrzymania bez potwierdzonej korzyści.

Potwierdzono konkretne błędy w istniejących ścieżkach. Najpilniejszy dotyczy nadpisania poprzedniego nagrania przez nieudaną poprawkę Voicebox. Bezpieczna lokalna reprodukcja obejmowała jeden testowy WAV. Osobny test wykazał warunkowe pominięcie granicy publicznego HTTP w Brand Kit przy konfiguracji proxy. Kontrakt companion nie sprawdza jeszcze dostatecznie związku żądania, rzeczywistej operacji i przyjmowanego wyniku. Są też dwa błędy przenośnej paczki REA oraz niezgodności instrukcji nauki, kosztów, dowodów marketingowych i motion QA.

To audyt źródeł, wybranych wykonań kodu i zachowania modelu. Nie poświadcza jakości wszystkich wygenerowanych mediów, skuteczności dydaktycznej u ludzi ani poprawnego działania wszystkich hostów. Pełny rejestr podaje zakres dowodu dla każdego ustalenia.


Rejestr zawiera **42 wpisy: 1 P0, 6 P1, 25 P2, 9 P3 i 1 INFO**. Są to błędy, luki dowodowe i rekomendacje. Backlog zawiera ponadto trzy odrębne propozycje rozbudowy.

## 1. Co dokładnie audytowano

| Element | Wersja / commit | Zakres |
|---|---|---|
| Creative Studio | 1.167.1 / `d2dbc1855e0552fbe753b69eeeb222faa282f016` | 2784 śledzone pliki; wspólny pakiet 1609 plików, 37 skilli |
| Toolbox | 1.6.1 / `8652ba3494a3a2a58ef77bdfb619fd956a42d55e` | 117 śledzonych plików, integracja i własne pakiety |
| Open Assets | 0.4.1 / `b15c35aa54d4efdf809cd3f21416da044ada2281` | 85 śledzonych plików, 14 aktualnych źródeł oraz research kandydatów |
| Zapisana instalacja Studio | 1.167.0 / `pluginrel_6ae8e608e2a48191908446eb2bf3ee58` | Porównanie wszystkich 1609 publicznych plików ze źródłem 1.167.1 |

Repozytoria: [Studio](https://github.com/FrameCoreWorks/framecore-works-creative-studio), [Toolbox](https://github.com/FrameCoreWorks/framecore-works-toolbox), [Open Assets](https://github.com/FrameCoreWorks/framecore-open-assets).

Instalacja i źródło różnią się w dziewięciu publicznych plikach. 1600 plików jest identycznych, żadnego nie brakuje. W zapisanej instalacji znaleziono także 55 plików prywatnych, których treści nie są częścią raportu ani paczki dowodowej. Poprawka 1.167.1 dotyczy między innymi routingu do zainstalowanych pozycji Toolboxa. Nie wykonano aktualizacji instalacji w ramach audytu.

Z 37 kanonicznych skilli 34 są widoczne w katalogu bieżącego hosta. Trzy pozostałe mają świadomie ograniczoną aktywację: `producer-ai-task-builder`, `hipson-adapter` i `workflow-self-improvement`. Sama różnica liczników nie jest błędem.

## 2. Metoda i granice kompletności

Plan obejmuje strukturę repozytorium, README, dystrybucję, orkiestrację, każdy skill, jego zasoby, przekazywanie wiedzy, naukę, kreatywność, integracje, bezpieczeństwo, zależności, CI i utrzymanie. Wszystkie 2986 śledzonych plików trafiły do inwentarza z rozmiarem, hashem, integralnością względem przypiętego Git blobu i jawnym poziomem przeglądu. Wszystkie 37 głównych SKILL.md Studio przeczytano w całości.

Pełny odczyt semantyczny, odczyt fragmentów i kontrola strukturalna są osobnymi statusami. Samo sparsowanie JSON, wyszukanie słów, sprawdzenie ścieżki lub wykonanie testu nie jest recenzją całej treści pliku. Pełne odczyty semantyczne: 306/2986; częściowe: 156/2986; wyłącznie strukturalne: 2524/2986. Szczegółowy licznik znajduje się w dołączonym rejestrze pokrycia. Nie deklaruję pełnego merytorycznego przeczytania każdego pliku historycznego, upstream i każdego programu.

Wykorzystano Hipsona do przydziałów i rejestru dowodów oraz metody przeglądu i weryfikacji Superpowers. Włączono wymagania Plugin Creator i Skill Creator dotyczące dystrybucji, odkrywania, struktury, stopniowego ładowania zasobów i oceny zachowania. Weryfikowano faktycznie dostępne źródła: Hipson Work 1.1.0 z core 1.6.0 i późniejszymi zmianami upstream oraz prywatny Superpowers 7.0.2. Dostępne wersje narzędzi PC/SC to 0.1.28 i 0.1.2; ich globalny status „najnowsze” pozostaje Unknown.

Przeglądy domenowe powstawały osobno. Najważniejsze reprodukcje bezpieczeństwa, integralności i oceny nauki powtórzono niezależnie w izolowanych lokalnych próbach. Nie wykonano płatnych generacji, instalacji narzędzi, pushu, publikacji ani zmian w audytowanych źródłach.

## 3. Najważniejsze mocne strony

- Podział Studio jako koordynatora, Toolbox jako wykonawcy i Open Assets jako źródła materiałów pozwala ograniczyć rozmiar oraz odpowiedzialność głównego pluginu.
- W instrukcjach widać świadome rozróżnienie planu, wyniku narzędzia, obejrzanego materiału i potwierdzonego faktu. Wymaga ono kilku lokalnych korekt, ale nie budowy od nowa.
- Kompetencje kreatywne mają treść warsztatową: mechanika kontaktu, ciągłość ujęć, hierarchia informacji, właściwości referencji, celowe relacje muzyki i obrazu, krytyka oraz poprawki.
- Nauka zawiera już 14 domen, planowanie, ćwiczenia, feedback, wsparcie stopniowane, postęp i Teacher Studio. Głównym brakiem jest kalibracja dowodu samodzielności i badanie efektu, nie brak ogólnego „mentora”.
- Repo ma znaczący zestaw testów i mechanizmy kontroli źródeł. Trzeba zachować ich mocne strony, uzupełniając parsery i próby zachowania tam, gdzie obecne testy dopuszczają błędny wynik.

## 4. Architektura i przepływ pracy

| Warstwa | Właściciel | Powinna otrzymywać | Powinna oddawać |
|---|---|---|---|
| Cel i etap pracy | Studio Guide / workflow-orchestrator | Bieżące zadanie, język, ograniczenia, ważne decyzje | Minimalną trasę specjalistów i następny krok |
| Warsztat kreatywny | Specjaliści Studio | Brief, właściwe referencje i blokady | Konkretną koncepcję, specyfikację, krytykę lub ćwiczenie |
| Stan i integracja | pipeline-core / delivery-documentation | Task ID, rewizję, zgodę, lokalizatory i hashe | Wynik powiązany z tym samym zamówieniem, status i ślady |
| Wykonanie techniczne | Toolbox / konkretny runtime | Dokładną operację, wejścia, root, zakres kosztu | Wynik faktycznego wykonania, ograniczenia, artefakty |
| Materiały zewnętrzne | Open Assets | Rodzaj materiału, licencję, wymagany sposób dostępu | Sprawdzoną próbkę, źródło, prawa, manifest |

Najważniejsza korekta to walidacja połączeń między tymi warstwami. Poprawny hash pliku potwierdza jego bajty, ale nie dowodzi, że pochodzi z właściwego zadania lub rewizji. `placeable=true` powinno wymagać zgodności z oczekiwanym requestem. Trzeba też zachować odmowę instalacji każdego companion, prawidłowo przenosić ważną zgodę w rozmowie oraz odróżnić prywatny handoff od eksportu publicznego.

Wszystkie 37 kart opisują cel, wejścia, wyjścia lub odpowiedzialność, mocne strony, braki, propozycje rozwoju i odbiór. Każda zawiera trzy scenariusze graniczne: właściwą aktywację, podobne zadanie spoza zakresu i przypadek niepełny lub sprzeczny. Te 111 wcześniejszych scenariuszy są projektem testów albo przejściem po źródle; nie są automatycznie zaliczane jako wykonane próby nowego swarmu.

## 5. README, repozytorium i utrzymanie

README działa wizualnie w sprawdzonym widoku desktopowym GitHuba. Obrazy wczytały się, struktura nagłówków i alt text są użyteczne. Droga do instalacji pojawia się jednak dopiero około 2866 pikseli od początku artykułu, po obszernej galerii. Sześć GIFów w źródle waży łącznie 27 680 150 bajtów. Jest to pomiar plików, a nie transferu sieciowego lub Core Web Vitals. Widok mobilny pozostaje NOT_RUN.

Proponowany początek README: krótkie wyjaśnienie celu, link do instalacji z wyborem hosta, jeden reprezentatywny przykład, trzy konkretne zadania startowe oraz rozróżnienie Studio/Toolbox/Open Assets. Pozostała galeria może zostać niżej. Nie ma potrzeby usuwać wartościowych demonstracji.

Na zdalnym repo stwierdzono tylko `main` i `gh-pages`. W sprawdzonych dziesięciu ostatnich wykonaniach CI były sukcesy, w tym kontrola źródła aktualnego commitu. Publiczny odczyt konfiguracji nie wykazał ochrony `main` ani wymaganych kontroli. Proponowana ochrona powinna zachować ustalony przez właściciela model pracy bezpośrednio na `main`: blokada force push i usunięcia, bez narzucania zdalnych gałęzi i obowiązkowych PR.

## 6. Nauka: rozwój o największej wartości

Najpierw naprawić aktywną rubrykę LM01 i scorer W06. LM01 opisuje nieaktualne warianty menu. W06 potrafi zaliczyć odpowiedź z dwoma pytaniami oraz bezpodstawną deklaracją ukończenia kursu. To potwierdzony problem pomiaru, a nie dowód, że każda lekcja pluginu zachowuje się źle.

Następnie spiąć istniejące elementy w jedną przenośną strukturę `learning_context`: cel, poziom początkowy i jego podstawa, ograniczenia narzędziowe, język, dostępność, próba ucznia, rodzaj udzielonej pomocy, kryterium oceny, kolejny krok i późniejszy powrót. Nie tworzyć równoległego systemu pamięci ani nowej warstwy agentów do każdej lekcji.

Proponowana jednostka nauki: krótki cel i kryterium, pierwsza próba, feedback o jednej najważniejszej przyczynie, poprawka, a potem samodzielne zadanie transferowe z innym briefem. Zaliczenie poprawki z pomocą należy odróżnić od samodzielnego zastosowania zasady. Jeśli materiał istnieje tylko w opisie, ocena dotyczy opisu, a nie faktycznej czytelności plakatu, jakości ruchu lub brzmienia audio.

Pełny plan mapuje 14 istniejących domen na obserwowalne kompetencje i zawiera sześciomodułową przykładową ścieżkę od briefu do mikrorealizacji. Teacher Studio powinno dodatkowo przejść próby przygotowania i prowadzenia lekcji, dostępności materiałów, czasu zajęć i oceny rzeczywistej pracy uczniów.

Wykonana podczas audytu grupa 25 profili nauki otrzymała niezależnie 24 PASS i 1 PARTIAL. W U024 odpowiedź unikała nieuzasadnionego obwiniania użytkownika oraz gwarancji naprawy, ale nie podała dość konkretnego minimum dowodów rozróżniających instrukcję, referencje, narzędzie i wykonanie. Dwa profile Teacher Studio zaliczyły kryteria. Te próby uzupełniają wcześniejszy brak dowodów zachowania w repo; nie mierzą uczenia się ludzi ani rzeczywistego przebiegu zajęć.

Podstawa projektowa: [IES/WWC](https://ies.ed.gov/ncee/wwc/PracticeGuide/1) wspiera m.in. rozłożenie nauki w czasie, przeplatanie przykładów z samodzielnymi zadaniami i aktywne przypominanie. [CAST UDL 3.0](https://udlguidelines.cast.org/) podpowiada alternatywne formy prezentacji i odpowiedzi oraz stopniowanie wsparcia. Są to przesłanki do projektu, nie walidacja tego pluginu. Skuteczność dla dorosłych twórców pozostaje Unknown do badania z ludźmi.

Plan przewiduje pilotaż 12–18 dorosłych, zadanie wejściowe, praktykę i niezależną próbę po 7–14 dniach. To propozycja wykonalnego pilotażu, bez twierdzenia, że taka liczebność wystarcza do statystycznego potwierdzenia skuteczności. Należy mierzyć wykonanie i samodzielność, a nie tylko satysfakcję lub liczbę ukończonych lekcji.

## 7. Kreatywność i nieszablonowe rozwiązania

Ocena twórcza powinna badać mechanizm pomysłu, jego związek z briefem, wykonalność, spójność i reakcję na krytykę. Zmiana koloru lub fontu nie jest automatycznie inną koncepcją. Jednocześnie świadoma oszczędność, nieruchomy kadr, cisza lub kontrapunkt nie powinny przegrywać przez uniwersalne reguły „dodaj ruch”, „przyspiesz” albo „wyrównaj do beatu”.

Wykryto sześć konkretnych niezgodności: źródło marketingowe zbyt łatwo staje się dowodem, linter nie uwzględnia cytowanej terminologii, oferta kosztowa jest mylona z wydatkiem, motion QA nakazuje usunąć świadomy offset, skrót UGC gubi własne wyjątki, a przykład FrameCut używa starej rewizji po alignment. Ostatni przypadek potwierdza prawidłowe działanie blokady runtime; naprawić należy przykład, nie osłabiać ochrony rewizji.

Do porównań przygotowano pięć stałych briefów: plakat oparty wyłącznie na typografii, reklamę usługi z ograniczonym dowodem, nieruchomy film obserwacyjny, motion z zadanym kontrapunktem i realizację z dwoma istniejącymi assetami. Kompletne prompty i kryteria są w planie rozwoju kreatywnego. Nie obiecują oryginalności rynkowej bez osobnego researchu.

## 8. Open Assets: co można dołączyć

Sprawdzono 37 pozycji: 14 aktualnych źródeł, 18 nowych kandydatów, cztery wcześniej usunięte źródła i Openverse wyłączony decyzją właściciela. Wszystkie 14 aktualnych prób wyszukania otrzymało HTTP 200. Dziewięć parserów przeszło próbę na zapisanych rzeczywistych odpowiedziach. Sam status HTTP nie potwierdza całego adaptera ani poprawnych praw każdego obiektu.

Nowy research obejmuje sześć kandydatów dźwiękowych, pięć muzycznych, trzy graficzne i cztery wideo. Cztery konkretne ścieżki przeszły pełne E0–E4: prawa, wyszukanie, obiekt, pobranie/dekodowanie i manifest.

| Kandydat | Sprawdzona próbka | Prawa próbki | Wynik techniczny | Następny krok |
|---|---|---|---|---|
| BigSoundBank | Pages that turn, 0493, Joseph SARDIN | CC0 | OGG 12,792 s, mono 48 kHz | Zweryfikować stabilny anonimowy sposób wyszukiwania i parser praw |
| OpenGameArt | Ghosts & Heroes, loop 2025, Bobjt | CC0; sprawdzono też źródło remiksu | MP3 115,252 s, stereo 44,1 kHz | Obsłużyć różne licencje i relacje remiksu; ocenić słuchowo pętlę |
| National Gallery of Art | Monet, Palazzo da Mula, obiekt 46657 | CC0 dla sprawdzonego materiału | IIIF JPEG 950 × 721 | Ustalić deterministyczny search i zachować prawa konkretnego obiektu |
| National Park Service | Grand Canyon, Yaki Point timelapse | Public domain z zastrzeżeniem braku endorsement | MP4 H.264/AAC 640 × 360, 44,9115 s | Wybrać metodę wyszukiwania i jawnie wskazywać dostępną rozdzielczość |

Źródła: [BigSoundBank](https://bigsoundbank.com/pages-that-turn-s0493.html), [OpenGameArt](https://opengameart.org/content/ghosts-heroes), [NGA Open Access](https://www.nga.gov/artworks/free-images-and-open-access), [NPS B-roll](https://www.nps.gov/grca/learn/photosmultimedia/b-roll_hd01.htm).

VERIFIED dotyczy wyłącznie wskazanej próbki i metody. Nie oznacza gotowego adaptera ani potwierdzenia całego katalogu. Liczba nowych zaimplementowanych adapterów: 0. Liczba nowych w pełni sprawdzonych anonimowych search API: 0. NGA ma sprawdzoną metodę pobrania obrazu przez IIIF, co jest inną funkcją niż search API.

Pozostali kandydaci mają jawne statusy PARTIAL, BLOCKED lub NOT_RUN. Przeszkody obejmują konto, klucz API, licencję spoza przyjętego zestawu, 403 lub zbyt duży plik próbny. Nie rekomenduję wpisania ich jako działających źródeł produkcyjnych. Pinterest może służyć jako kontekst referencyjny po osobnej ocenie metody dostępu i praw; nie jest tu zatwierdzonym źródłem otwartych assetów.

## 9. Bezpieczeństwo i powtarzalność

Priorytet P0 w tym planie wynika z potwierdzonej utraty istniejącego pliku Voicebox. Zakres ogranicza się do pojedynczego wyjściowego WAV przy konkretnej ścieżce błędu. Rozwiązanie: tymczasowy plik, pełna walidacja, atomowa podmiana dopiero po sukcesie, spójna aktualizacja metadanych.

Brand Kit wymaga sprawdzania rzeczywistej drogi połączenia, w tym `NO_PROXY`, i adresu końcowego po przekierowaniach. Lokalna próba używała fikcyjnego serwera i kontrolowanych odpowiedzi DNS. Nie odczytywano wewnętrznych sekretów ani nie testowano rzeczywistych usług organizacji.

W CI przypięto Pillow 12.3.0. Oficjalne [GHSA-w889-685w-c8fh](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh) obejmuje tę wersję; poprawka jest w 13.0.0. Dotyczy szczególnej ścieżki EPS/Ghostscript i nazwy wejściowej. Potwierdzono zgodność pinu z zakresem advisory, nie wykonano exploita na podatnej wersji. Host audytu używał Pillow 13.0.0, więc lokalny sukces testów nie potwierdza bezpieczeństwa zadeklarowanego pinu.

VoxCPM2 wymaga pełnego locka zależności i model revision; przypięcie tylko głównego pakietu nie zapewnia odtwarzalności. Akcje CI Open Assets warto przypiąć do pełnych commitów. Przegląd wzorców sekretów nie wykazał trafień w skanowanym materiale, lecz płytki checkout i brak pełnego skanu historii nie pozwalają stwierdzić, że sekretów nigdy nie było. Pełny transitive SBOM/CVE review pozostaje poza uzyskanym dowodem.

## 10. Kolejność rozwoju

| Etap | Zakres | Warunek odbioru |
|---|---|---|
| A. Integralność i bezpieczeństwo | SEC-002, SEC-001, ORCH-01; aktualizacja pinu Pillow po zgodności | Negatywne próby chronią poprzedni plik, publiczną granicę HTTP i właściwe task/revision/input |
| B. Paczki i dowód instalacji | DIST-001/002/003; wspólna walidacja YAML/JSON; późniejsza aktualizacja zapisanej instalacji | Parsery wykrywają wadliwe fixture, tożsamość i dodatki zachowane, odczyt po zapisie oraz nowy kontekst potwierdzają właściwą wersję |
| C. Spójne instrukcje | CR-001–006, ORCH-02–09, ASSET-001/002 | Każdy konflikt ma jeden właścicielski zapis i konkretną próbę akceptacyjną |
| D. Nauka | LM01, W06, karta postępu, transfer, Teacher Studio | Próbka z pomocą nie jest mastery; checkpoint zachowuje ograniczenia; pilotaż bada samodzielność |
| E. Lepsze przykłady i materiały | Pięć briefów kontrastowych, cztery kandydatury assetów | Warianty zmieniają mechanizm; adaptery przechodzą własne E0–E4, błędy, retry i limity |
| F. Utrzymanie i wejście do produktu | README, serwerowe ograniczenia main, locki i odświeżanie źródeł | Krótsza droga do instalacji, zgodny model main-only, jawne wersje i wyniki wykonanych kontroli |

Wdrożenie powinno następować małymi zmianami z odbiorem, nie jednym szerokim refaktorem. Nie zmieniać chronionych ścieżek pakietu, nie usuwać aliasów wymaganych przez kompatybilność, nie zastępować działających ownerów nowym „super-agentem”. Szczegółowy rejestr zawiera kryterium akceptacji każdej poprawki. Szacunki nakładu powinny powstać po wyborze zakresu wdrożenia, bez wymyślonych godzin na podstawie samego audytu.

## 11. Instalacja w ChatGPT Work i wyszukiwanie Vercel

Instalacja obejmuje kilka odrębnych czynności: znalezienie źródła, wybranie modułu, odczyt wersji i wymaganych zasobów, przygotowanie zgodnej paczki, zapis na platformie, odkrycie przez nową rozmowę, przygotowanie runtime i wykonanie zadania. Żaden wcześniejszy etap nie poświadcza automatycznie następnego.

Macierz instalacyjna zawiera 17 pozycji marketplace Toolbox, łącznie 21 kandydatów paczek, 42 własne pliki skillowe w sześciu własnych paczkach oraz 59 składników środowiska. Własne 37 skilli Studio jest częścią wspólnej paczki. Nie trzeba instalować każdego osobno. Silnik Earshot, modele głosu, biblioteki, przeglądarka i inne zależności wykonawcze stanowią osobną warstwę.

Faktycznie sprawdzono także zapisane metadane powiązanych pluginów. Toolbox ma 1.6.1, Open Assets 0.4.1, Studio 1.167.0. Dla jedenastu zewnętrznych pozycji znaleziono własne zapisane pluginy i odczytano ich inventory. Brak wpisu w wykazie własnych pluginów nie dowodzi, że nie ma zarządzanej lub osobistej instalacji skilla inną drogą. Szczegółowe porównanie wybranych źródeł, zmian frontmatter i brakujących zasobów jest w dodatku instalacyjnym.

Dodatkowy przegląd obejmuje wszystkie 15 pozycji zewnętrznych Toolboxa oraz 93 wybrane pliki SKILL.md na przypiętych commitach. Wszystkie 93 mają zgodne Git blob SHA; 92 parsują się jako poprawny YAML. Pełny odczyt semantyczny objął 13 z nich, pozostałe mają jawnie oznaczony przegląd ukierunkowany i kontrolę mechaniczną. Z 37 odczytanych aktywnych plików w jedenastu zapisanych pluginach 36 jest identycznych bajtowo z upstream; wszystkie 37 zachowują identyczną treść po frontmatter. Motion Designer dodaje dwa cudzysłowy naprawiające YAML i zachowuje oryginał jako provenance. Nie jest to obecna awaria zapisanej instalacji.

Potwierdzono dwa braki zasobów. Huashu ma 474 z 491 oczekiwanych ścieżek: brakuje sześciu fontów i jedenastu materiałów pokazowych. Oba standardowe bootstrapy renderera czekają na załadowanie wszystkich 45 zadeklarowanych fontów przed zgłoszeniem gotowości. Brakujące fonty prowadzą do ścieżki błędu, którą render.py odrzuca. To dowód statyczny na podstawie faktycznej zapisanej listy i identycznych callerów; renderu w przeglądarce nie wykonano. Animate ma 106 ze 107 oczekiwanych ścieżek. Brak `styles/riso/sample.png` usuwa Riso z galerii wyboru, lecz nie usuwa kodu tego stylu ani nie dowodzi awarii wszystkich renderów.

Minimalny odbiór późniejszej naprawy obejmuje kompletne zasoby i hashe, odczyt po zapisie, odkrycie skilla w nowej rozmowie, kontrolę faktycznie dostępnego runtime oraz jeden adekwatny wynik końcowy. Dla Huashu najpierw przywrócić dokładne pliki fontów i zachować ich licencje; dla Animate potwierdzić siedem kafelków galerii. Samo poprawne SKILL.md nie wystarcza do potwierdzenia instalacji modułu wykonawczego.

Stwierdzono konflikt instrukcji Toolboxa: główny `CHATGPT_INSTALL.md` każe traktować zewnętrzne pozycje jako Claude-only, podczas gdy aktywna referencja opisuje zapis ich niezmienionych skilli jako osobnych prywatnych pluginów w Work. Użytkownik może więc otrzymać różną odpowiedź zależnie od odczytanego pliku. Trzeba ujednolicić obie drogi i nadal odrzucać nieobsługiwane hooks, aplikacje desktopowe i niezweryfikowane integracje.

Mechanizm wyszukiwania Studio jest własną adaptacją metody Vercel, odnotowaną przy źródle 1.7.2. Oficjalny upstream odczytano na commicie `9197d919034d19010ae303cf96bf19ad087dd4be`, którego `package.json` ma wersję 1.7.6. Sama różnica wersji nie dowodzi błędu adaptacji. Sprawdzono aktualną dokumentację komend, agentów i telemetrii.

Wykonany żywy test `typography` zwrócił trzy wyniki. Opis i odczyt `jakubkrehel/skills/better-typography` zakończyły się sukcesem, z tekstem przypiętym do `60bf140e43c98b248e6594487384ec967e89d98a`. Nie wykonano `npx skills add`, instalacji pakietów ani zapisu na koncie. Oceny katalogu były odczytane jako dane; popularność i zielona ocena nie gwarantują jakości lub bezpieczeństwa.

Najważniejsza luka to brak przejścia z zaakceptowanego wyniku wyszukiwania do natywnej instalacji Work. Finder podaje ogólną niemożność trwałego zapisu w Work, choć bieżąca platforma udostępnia zarządzanie własnymi skillami i prywatnymi pluginami. Prawidłowe ograniczenie brzmi: lokalny Vercel CLI nie zapisuje skilla do konta ChatGPT. Należy dobrać natywną drogę do dostępnych funkcji i rodzaju paczki, zachowując kompletność, licencję i tożsamość.

Dwie dalsze korekty: obsłużyć poprawny JSON o niewłaściwej strukturze bez nieprzechwyconego wyjątku oraz powiązać zatwierdzony commit, licencję, inventory i później instalowane bajty. Obecnie tekst one-time use jest przypięty, ale licencja pochodzi z bieżącej gałęzi, ocena audytu nie jest powiązana z tą rewizją, a komenda instalacji pozostaje nieprzypięta.

Dziesięć dodatkowych profili U101–U110 sprawdza sposób prowadzenia użytkownika przez te granice. Niezależne oceny tej dziesiątki: 9 PASS, 1 PARTIAL, 0 FAIL i 0 BLOCKED. Poprawna odpowiedź modelu może rozwiązać konflikt między źródłami, ale nie usuwa błędnej instrukcji z repozytorium. Są to testy odpowiedzi i decyzji procesowych. Faktyczny nowy zapis pluginu, instalacja silnika oraz świeże użycie po zapisie pozostają NOT_RUN w tym audycie.

## 12. Wyniki testów i symulacji

| Zakres techniczny | Zaobserwowany wynik | Granice |
|---|---|---|
| Studio, 72 kanoniczne polecenia Python | Dla każdego istnieje udany przebieg; 861 zgłoszonych testów, 17 pominiętych | Wyniki z pełnego przebiegu i uzupełniających poleceń, nie jeden nieprzerwany sukces |
| Studio, Node | 244 testy: 233 pass, 11 skip, 0 fail | Skipy pozostają pominięciami |
| Nieprzerwany `check_all.sh` | **FAIL, exit 1** | Jeden błąd sondy kodeka FrameCut; późniejsza próba tego testu przeszła, dokładna przyczyna Unknown |
| Toolbox | 70 testów, PASS | Nie jest to instalacja wszystkich pozycji katalogu |
| Earshot w Toolbox | 71 testów: 69 zaliczonych, 2 skip | Full tier niewykonany |
| Open Assets | 63 testy, PASS; reprodukowalne pakowanie | Nie potwierdza całego katalogu w sieci |
| Opcjonalny browser | ENVIRONMENT_BLOCKED | Lokalny Chromium odrzucał operację gniazda; nie zaliczać jako regresję produktu ani sukces |
| Strukturalny walidator Studio | PASS, 37 ownerów, 1609 plików | Repo deklaruje 206 zaplanowanych eval fixtures; licznik ich wykonania pozostaje 0 |

Pierwsze próby pełnego zestawu były zatrzymywane przy nadmiernym równoległym obciążeniu BLAS. Ograniczenie liczby wątków pozwoliło przejść ten fragment. Nieprzerwany późniejszy przebieg nadal zakończył się błędem FrameCut i zachowano ten wynik. Powtórzenie wyłącznie nieudanej próby przeszło bez zmian źródła; wcześniej pełny FrameCut również miał 45/45 PASS. Te obserwacje wskazują niestabilność warunków, ale nie ustalają przyczyny. Nie ogłasza się całego canonical run jako zielonego.

Środowisko audytu różniło się od przypięć CI: między innymi numpy 2.3.5, Pillow 13.0.0 i fonttools 4.61.1 wobec deklarowanych 2.5.3, 12.3.0 i 4.66.1. Zależności pikepdf i GEPA nie były dostępne; odpowiednie pominięcia są zapisane. Zestawów nie należy sumować z historycznymi logami ani liczyć ponownych prób jako dodatkowego pokrycia.

Wykonano **110/110 profili i 172/172 tur użytkownika** w świeżych kontekstach agentów. Niezależne oceny: 105 PASS, 5 PARTIAL, 0 FAIL i 0 BLOCKED. Oceniono 405 kryteriów i 237 warunków krytycznych; stwierdzone triggery krytyczne: 0. Sprawdzono dosłowność 642 cytatów. Są to wyniki wybranego zbioru dialogów, bez wnioskowania o odsetku niezawodności w populacji.

Grupy obejmują 25 profili nauki, 35 kreatywnych, 40 orkiestracji i integracji oraz 10 instalacji Work/findera. Przygotowane przypadki odnoszą się łącznie do wszystkich 37 właścicieli skilli. Związek profilu z właścicielem jest planem pokrycia, a odczyt ścieżki podany przez klienta jest self-reportem; nie są niezależną telemetrią aktywacji.

Badany agent otrzymywał pełny profil przed pierwszą turą: doświadczenie, cel, host, narzędzia, czas, budżet i język. Nie otrzymywał przyszłych surowych wiadomości, rubryk ani diagnoz audytu. Niektóre fakty pojawiające się później w dialogu znał już z profilu. To ogranicza wnioski o spontanicznym rozpoznawaniu nieznanego klienta. Pełny protokół i transkrypty są dołączone.

Badano źródło 1.167.1, nie starszą zapisaną instalację 1.167.0. Rzeczywisty host to natywne agenty ChatGPT Work; inne hosty w profilach są warunkami scenariusza. Model backend, tokeny, koszt i porównywalna latencja: Unknown. Generacje, instalacje, wywołania usług i publikacje pozostawały wyłączone. Poprawna deklaracja planu nie jest wykonaniem operacji.

Pełne oceny, również kryteria częściowo zaliczone, są w [Raport-symulacji.md](Raport-symulacji.md), [Wyniki-110-profili.csv](Wyniki-110-profili.csv) i [Oceny-symulacji.json](Oceny-symulacji.json). Nie doliczano zaplanowanych fixture, historycznych logów, dwóch pilotów ani metadanych po dialogu jako nowych klientów.

Oceny sporządzali agenci inni niż badani klienci. Nie był to w pełni zaślepiony eksperyment: sędziowie U081–U100 oraz U101–U110 zostali uruchomieni z dziedziczonym kontekstem koordynatora, mimo ograniczenia dalszych odczytów do przypadków, odpowiedzi i rubryk. Pełnego zaślepienia wcześniejszych grup nie zweryfikowano. Wszystkie oceny mają dosłowne dowody, ale wpływ wcześniejszego kontekstu pozostaje ograniczeniem. Sześć dodatkowych powtórzeń otrzymuje osobnych sędziów bez dziedziczenia historii.



Dla trzech wybranych scenariuszy wykonano jeszcze sześć prób w nowych kontekstach, po dwie dodatkowe na U024, U099 i U101. Razem z bazowymi daje to po trzy wykonania: U024: PARTIAL, PARTIAL, PARTIAL; U099: PASS, PASS, PASS; U101: PASS, PASS, PASS. Powtórzenia obejmują osiem dodatkowych tur i nie zwiększają mianownika 110 unikalnych profili. Wybrano je celowo; U024 po pierwszej ocenie, dwa pozostałe przed odpowiedziami bazowymi. Każde powtórzenie oceniał osobny świeży sędzia. Szczegóły i granice: [Powtorzenia-symulacji.md](Powtorzenia-symulacji.md).

## 13. Co pozostaje Unknown

- Skuteczność nauki u ludzi oraz trwałość i przenoszenie nabytej umiejętności.
- Rzeczywista jakość wszystkich obrazów, audio i wideo; badane próbki techniczne nie zastępują pełnej oceny percepcyjnej.
- Świeża instalacja i pełne przepływy każdego hosta, w tym mobilnego.
- Zachowanie wszystkich zewnętrznych connectorów, płatnych modeli i zmian ich API.
- Pełna historia sekretów, kompletny łańcuch zależności przechodnich i wszystkie możliwe ataki.
- Dostępność każdego obiektu w zewnętrznym katalogu w późniejszym terminie.

Audyt obejmuje wszystkie zaplanowane obszary, ale jego kompletność nie oznacza braku tych ograniczeń. Szczegółowy status jest przypisany do konkretnego pliku, próby i wniosku.


## 14. Odbiór i materiały

Niezależny review wykrył pięć korekt raportowych: starszy status instalacji, niepełne wymiary kart, brak propozycji w eksporcie backlogu, niejednolite pola pewności/rewizji i niepoprawne odwołania po przeniesieniu dokumentów. Poprawki zostały ponownie sprawdzone. Dwóch najważniejszych reprodukcji kodowych nie uznano za potwierdzone wyłącznie na podstawie opinii pierwszego wykonawcy. Końcowa recenzja zamrożonych materiałów jest w `evidence/final-review/final-review.json` i `.md`.

Otwarte ustalenia produktu pozostają otwarte. Hipson przyjął dowody wykonanych przeglądów; akceptacja wyniku analizy nie oznacza naprawy usterek ani automatycznego zamknięcia ledgerów wymagających ich rozwiązania. Nie zmieniano źródeł trzech repozytoriów; ich drzewa robocze sprawdzono jako czyste. Ponowny odczyt `main` 4 listopada o 15:41 UTC zwrócił te same trzy commity.

Spis wszystkich materiałów znajduje się w [CZYTAJ-NAJPIERW.md](CZYTAJ-NAJPIERW.md). Najważniejsze dodatki to [37 kart skilli](Karty-37-skilli.md), [plan nauki](Plan-rozwoju-nauki.md), [instalacja Work](Instalacja-modulow-Work.md), [backlog](Backlog-rozwoju.md) i [rejestr źródeł Open Assets](Open-Assets-37-zrodel.csv).
