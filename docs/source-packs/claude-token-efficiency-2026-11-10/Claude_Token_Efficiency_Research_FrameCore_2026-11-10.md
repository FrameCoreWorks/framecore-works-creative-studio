# Claude: oszczędzanie tokenów bez obniżania jakości pracy
## Research i propozycja adaptacji dla FrameCore Works
Stan weryfikacji: 10 listopada 2026, Europe/Warsaw.

## 1. Rekomendacja

Najpierw uporządkuj kontekst, zakres sesji i pomiar. Następnie przetestuj Ponytail wyłącznie przy kodowaniu oraz jedną metodę ograniczania nadmiarowych odczytów. Graphiti pozostaw jako opcję pamięci długoterminowej.

Dla FrameCore Works proponuję trzy tryby: CODE, CREATIVE i MIXED. Oszczędzanie kosztu technicznej realizacji ma być podporządkowane kompletności rezultatu. Kod animacji również może być pracą kreatywną.

Nie znalazłem podstaw do obietnicy, że zestaw tych narzędzi zmniejszy zużycie Twojego abonamentu o konkretny procent. Są pozytywne doświadczenia użytkowników, ale także pomiary pokazujące zerową oszczędność albo wzrost kosztu. Najsilniejsze dowody dotyczą określonych zadań i wersji, nie wszystkich środowisk.

| Kolejność | Rozwiązanie | Decyzja dla Ciebie |
|---|---|---|
| 1 | Natywne zarządzanie kontekstem, Projects, wybór modelu i effort | Wprowadzić do sposobu pracy jako pierwsze |
| 2 | Natywne /usage i /context, opcjonalnie ccusage | Zmierzyć rzeczywisty problem |
| 3 | Ponytail | Pilotaż w zadaniach CODE; bez globalnego wymuszania |
| 4 | Natywne LSP lub Serena | Porównać przy nawigacji po dużym kodzie |
| 5 | Context Mode Engine | Pilotaż przy dużych logach i wynikach narzędzi |
| 6 | QMD | Rozważyć dla dokumentacji, handoverów i bazy wiedzy |
| 7 | RTK | Testować selektywnie, jeśli logi są realnym kosztem |
| 8 | Graphiti | Dopiero gdy prosta pamięć dokumentowa nie wystarcza |
| 9 | Claude-Mem, Caveman, dodatkowe kompresory | Nie włączać domyślnie jako sposobu na limity |

Zakres wykonany: research dokumentacji, repozytoriów, publicznych benchmarków, zgłoszeń i relacji użytkowników. Nie instalowałem narzędzi, nie zmieniałem Twoich pluginów ani konfiguracji Claude, nie uruchamiałem płatnych modeli. Test end-to-end na Twoim koncie: **Unknown**.

## 2. Co prawdopodobnie zużywa limity

Twoja obserwacja jest zasadna: długość rozmowy ma znaczenie. Nie wynika z tego jednak, że głównym problemem jest samo mówienie długo.

Anthropic wskazuje m.in. długość wiadomości i rozmowy, załączniki, narzędzia, model, effort oraz wieloetapowe zadania jako czynniki zużycia. Ponownie wykorzystywana wiedza projektu może być cache’owana i liczyć się mniej do limitu. Nie oznacza to zerowego kosztu. [S1]

W Claude Code kolejne wywołania modelu obejmują rosnący kontekst. Jedno polecenie użytkownika może spowodować wiele rund: odczyt plików, analiza, edycja, testy, naprawa, ponowne testy. Dodatkowe procesy agentowe mają własne zużycie. To mechanizm wyjaśniający problem, nie pomiar Twojego konta. [S2]

Rozdziel pięć wielkości:

| Wielkość | Co oznacza | Typowy błąd |
|---|---|---|
| Rozmiar kontekstu | Materiał dostępny w konkretnym wywołaniu | Uznanie go za całe zużycie sesji |
| Tokeny wejścia/wyjścia | Wielkość zapytań i generacji | Pominięcie cache i dodatkowych agentów |
| Koszt równoważny API | Wyliczenie według cen modelu | Uznanie go za rachunek abonamentowy |
| Zużycie abonamentu | Oficjalny wskaźnik okna/session/week | Wyliczanie go ze zwykłej sumy tokenów |
| Jakość ukończonego zadania | Wynik po wszystkich poprawkach | Liczenie oszczędności przed naprawą regresji |

Prompt caching ogranicza koszt ponownego przetwarzania stabilnego prefiksu, ale nie usuwa jego zawartości z okna kontekstowego. Przepisanie historii może zmniejszyć liczbę tokenów i jednocześnie pogorszyć trafienia cache. Nie wolno utożsamiać oszczędności z surowym rozmiarem tekstu. [S3]

Limit długości rozmowy i limit korzystania z usługi to osobne ograniczenia. Automatyczne podsumowanie długiego czatu nie resetuje abonamentu i samo może zwiększać zużycie. [S4]

### Hipotezy do sprawdzenia w Twoim workspace

1. Długie sesje mieszają rozwój pluginu, research, debugging i produkcję klienta.
2. Przy każdym zadaniu ładowane są zbyt obszerne instrukcje lub niepotrzebne moduły.
3. Agent wraca do tych samych dokumentów, całych plików i dużych logów.
4. Kilka skilli równocześnie narzuca podobną procedurę planowania, recenzji i QA.
5. Dodatkowi agenci wielokrotnie czytają te same materiały.
6. Wysoki effort jest używany także do prostych zmian.
7. W tle działa obserwator pamięci albo inne automatyczne wywołania.

To lista kontrolna do audytu, nie stwierdzenie, że Twoja wtyczka ma te błędy. Aktualna konfiguracja i logi Twojego Claude: **Unknown**.

### Jak zachować swobodę dyktowania

Możesz nadal opisywać pomysł naturalnie. Proponuję jednorazowe przełożenie wypowiedzi na krótki dokument roboczy:

- cel i oczekiwany plik końcowy;
- zatwierdzone wymagania;
- elementy nienegocjowalne;
- aktualny etap;
- najbliższa zmiana;
- odnośniki do materiałów źródłowych.

Późniejsze doprecyzowania aktualizują te pola. Nie trzeba ponownie przepisywać całej historii.

Samo dopisanie streszczenia w tym samym wątku nie usuwa wcześniejszych wiadomości. Gdy kończy się etap albo zmienia temat, warto rozpocząć nową sesję z aktualnym stanem i dostępem do źródeł. Nie rozbijaj natomiast jednego spójnego zadania co kilka minut, bo ponowne przygotowanie kontekstu też kosztuje.

## 3. Co działa w poszczególnych środowiskach

Przyjmuję, że przez „cloud” masz na myśli Claude. Dodatkowo rozróżniam faktyczne sesje Claude Code w chmurze.

| Środowisko | Realistyczna metoda oszczędzania | Ważne ograniczenie |
|---|---|---|
| Claude w przeglądarce i zwykły czat na telefonie | Projects, krótkie instrukcje, aktualny brief, dobór modelu/effort, narzędzia na żądanie | Lokalny wrapper terminala nie przechwytuje tego czatu |
| Claude Desktop, zwykły czat | Powyższe; lokalne lub zdalne konektory do wyszukiwania danych | MCP dodaje narzędzia, nie zastępuje modelu rozmowy |
| Claude Code CLI lokalnie | Ponytail, LSP/Serena, RTK, Context Mode, QMD, pomiar lokalnych sesji | Instalacja i konfiguracja dotyczą konkretnego runtime |
| Claude Code w aplikacji Desktop | Narzędzia zgodne z lokalnym trybem Code | Nie utożsamiać zakładki Code z Chat ani z sesją cloud |
| Claude Code cloud | Instrukcje, account skills i dostępne narzędzia w środowisku zdalnym | Lokalne pluginy, pliki użytkownika i procesy nie przenoszą się automatycznie |
| Telefon jako Remote Control Claude Code | Obsługa lokalnej sesji z jej plikami i MCP | Komputer/runtime musi działać; własna bramka API wyklucza oficjalny Remote Control |
| Cowork sterowany z telefonu | Możliwe zadania korzystające z desktopu | To osobny tryb; nie dowód, że zwykły czat uruchamia lokalny plugin |

Zdalne konektory mogą działać na wielu powierzchniach Claude. Rozszerzenia lokalne potrzebują środowiska desktopowego. W Cowork część dostępu z telefonu może odbywać się za pośrednictwem komputera. To nie synchronizuje dowolnego lokalnego serwera do samodzielnego czatu mobilnego. [S5][S6]

Remote Control łączy telefon z sesją działającą na Twojej maszynie. Zachowuje jej narzędzia i konfigurację. Dokumentacja wskazuje jednak, że nie jest dostępny przy ANTHROPIC_BASE_URL kierującym na inny host niż api.anthropic.com. [S7]

Współczesny Claude ma synchronizację skilli konta, ale nie oznacza ona synchronizacji całego workspace. Dokumentacja rozróżnia account skills, repo skills i pluginy. Cowork/cloud nie czytają lokalnego ~/.claude/skills; projektowe wątki cloud mają dodatkowe ograniczenia. Przed adaptacją trzeba sprawdzić konkretny tryb i wersję. [S8]

### Ustawienia, od których warto zacząć

W zwykłym Claude sprawdź Tool access: Auto albo On demand przy dużej liczbie konektorów. Always available ładuje więcej definicji od początku. To ustawienie rozmowy, a nie instalacja nowej wtyczki. [S36]

W Claude Code użyj /context do sprawdzenia zajętości, /usage do zużycia i /mcp do stanu serwerów. Nowe niezwiązane zadanie rozpoczynaj przez /clear po zapisaniu potrzebnego stanu; /compact stosuj wtedy, gdy zachowanie ciągłości jest potrzebne. Kompaktowanie też wymaga pracy modelu. [S2]

Model i effort dobieraj na początku etapu. Częste przełączanie modelu w środku długiej sesji może unieważniać cache. Przy gatewayu sprawdź, czy zachowuje znaczniki cache_control. [S3]

## 4. Ponytail: sensowny kandydat do kodowania

Repozytorium: https://github.com/DietrichGebert/ponytail

Ponytail przede wszystkim kieruje zachowaniem agenta. Zachęca do wykorzystania istniejącego kodu i małego, kompletnego rozwiązania. Nie jest silnikiem, który automatycznie usuwa historię rozmowy. Odczytany skill ma tryby lite/full/ultra, z domyślnym full; działa do wyłączenia. Zawiera ochronę wymaganej walidacji, bezpieczeństwa i innych wymagań użytkownika. [S9]

Benchmark autora dla Ponytail 5: 39 zadań, pięć powtórzeń na wariant, Opus 5.5. Raportuje około 45% mniej tokenów wyjściowych i 26% niższy koszt. To różne metryki. Istotne ograniczenie: Bash był wyłączony, więc test nie odtwarza pełnego cyklu wykonywania poleceń i debugowania. Twarde ukryte testy dotyczyły 18 zadań; pozostałe miały inne kryteria. Nie jest to niezależna replikacja. [S10]

Relacje użytkowników są mieszane. Marmelab opisuje mniej kodu i mniej iteracji dev/reviewer. Inni chwalą zwięzłość, ale pojawia się także zgłoszenie dłuższego thinking i większego zużycia. Są to doświadczenia konkretnych osób, nie gwarancja. [S11][S12]

### Moja propozycja dla FrameCore Works

- Aktywacja tylko dla implementacji, napraw błędów, refaktoryzacji i utrzymania repo.
- Początek od lite albo krótkiej, własnej polityki inspirowanej zasadami Ponytail.
- Nie dodawać równocześnie pełnego Ponytail, kopii jego AGENTS.md i własnej parafrazy do globalnych instrukcji.
- Nie uruchamiać automatycznie pełnego audytu repo przy małej poprawce.
- Nie używać ultra jako domyślnego trybu dla realizacji klienta.
- Przy istniejących dobrych instrukcjach oczekiwać mniejszego przyrostu korzyści niż w benchmarku bez skilla.

Najważniejsza pułapka: polecenie „dopieszcz animację” nie oznacza zgody na minimalną wersję animacji. Mechanizm ograniczania zakresu musi ustąpić zatwierdzonemu rezultatowi.

Samo ograniczenie automatycznego wywołania skilla nie wyłącza niezależnego hooka pluginu. Przy adaptacji trzeba sprawdzić oba mechanizmy.

## 5. Graphiti: pamięć, której utrzymanie kosztuje

Repozytorium: https://github.com/getzep/graphiti

Graphiti buduje graf encji, relacji i faktów zmieniających się w czasie. Zachowuje powiązania z materiałami źródłowymi. Może pomóc, gdy wiele sesji potrzebuje małego fragmentu długiej historii. Nie zastępuje automatycznie mechanizmu kontekstu Claude. [S13]

Koszt może pojawić się przy ekstrakcji faktów, deduplikacji, aktualizacji i embeddingach. Użytkownik w issue #1193 opisuje wielokrotne wywołania modeli przy add_episode. Opiekun wskazuje poprawki zmniejszające ten narzut, ale nie wynika z tego jego wyeliminowanie. [S14]

Referencyjny serwer MCP wymaga infrastruktury grafowej i konfiguracji dostawców. Jego aktualna dokumentacja wprost zaznacza brak uwierzytelniania i autoryzacji oraz eksperymentalny charakter. Nie należy wystawiać go bezpośrednio publicznie na potrzeby telefonu. group_id organizuje dane, ale nie jest granicą uprawnień. [S15]

### Kiedy może pomóc Tobie

- śledzenie, która wersja ustaleń klienta jest aktualna;
- historia decyzji architektonicznych pluginu;
- powiązania między modułami, repozytoriami i ograniczeniami;
- pamięć zatwierdzonych preferencji produkcyjnych.

### Jak ograniczyć koszt i ryzyko utraty szczegółów

To proponowany projekt integracji, nie obecna funkcja Twojej wtyczki:

1. Zapisywać zatwierdzone decyzje przy końcu etapu, nie każdy komunikat narzędzia.
2. Oddzielić klienta, projekt i rodzaj pracy.
3. Każdy fakt powiązać ze źródłem, datą, wersją i statusem.
4. Do rozmowy pobierać najpierw kilka trafień, potem konkretne źródła.
5. Pełne prompty, teksty reklamowe i specyfikacje przechowywać jako dokumenty źródłowe.
6. Unieważniać zastąpione ustalenia zamiast trzymać dwie sprzeczne wersje jako aktualne.
7. Limitować ingest i retry; stały błąd schematu nie powinien uruchamiać kolejnych płatnych prób.
8. Osobno mierzyć koszt ingestu, retrieval i głównej sesji.

Warunek opłacalności: koszt unikniętego odtwarzania historii musi przewyższać koszt budowania pamięci, wyszukiwania i błędów.

Najpierw przetestowałbym zwykłe dokumenty stanu, natywną pamięć i QMD. Graphiti ma sens, gdy potrzebne są relacje i czasowa historia faktów, nie tylko znalezienie odpowiedniego handoveru.

## 6. Dodatkowe repozytoria i jakość dowodów

Skala dowodów: A = niezależny test zadań; B = benchmark autora z metodą; C = doświadczenie użytkownika; D = dokumentacja mechanizmu. Skala dotyczy dowodu korzyści, nie oceny całego projektu.

| Projekt | Mechanizm | Dowody i ograniczenia | Rekomendacja |
|---|---|---|---|
| ccusage/ccusage | Pomiar sesji i cache | D, nie kompresuje | Dobry dodatek diagnostyczny |
| anthropics/claude-plugins-official | M.in. pluginy code intelligence/LSP | D, oficjalne mechanizmy | Najpierw rozważyć natywne możliwości |
| oraios/serena | Operacje na symbolach i odwołaniach | C/D, relacje mieszane | Pilotaż na dużym kodzie |
| mksglu/context-mode | Wyniki poza kontekstem, indeks i wyszukiwanie | B/C, silne redukcje danych, nie dowód całego kosztu | Przy logach i dużych wynikach |
| tobi/qmd | Lokalne wyszukiwanie dokumentów | C/D, brak potwierdzonego uniwersalnego procentu | Bardzo dobry kierunek dla handoverów |
| rtk-ai/rtk | Skracanie wyjść poleceń | A/B/C, niezależny test bez poprawy całkowitego kosztu | Selektywnie |
| thedotmack/claude-mem | Obserwator i pamięć między sesjami | C/D, konkretne raporty dużego dodatkowego zużycia | Nie domyślnie |
| JuliusBrussee/caveman | Skracanie narracji | A, umiarkowany efekt w zadaniach agentowych | Niski priorytet, poza kreatywnymi rezultatami |

### ccusage

Aktualne repo to https://github.com/ccusage/ccusage. Czyta lokalne dane sesji i rozdziela m.in. cache creation/read. Ma tryb offline. Jest przydatne do porównywania pracy, ale nie monitoruje automatycznie wszystkich zwykłych czatów mobilnych. Kwota równoważna API nie jest rachunkiem ani dokładnym procentem limitu Max/Pro. [S16]

Najpierw /usage w aktualnym Claude Code i oficjalny panel konta. ccusage traktuj jako dodatkową analizę, zależną od kompletności zapisanych logów.

### Natywne LSP i Serena

Serena pozwala czytać i edytować właściwe symbole zamiast całych plików. Dla rozbudowanego kodu pluginu to sensowny kierunek. W aktualnym repo jest także interfejs REPL. Darmowy backend language-server i płatny backend JetBrains to różne warianty. [S17]

Użytkownik tworzący aplikację iOS opisuje korzyści, a inni w tym samym wątku wskazują brak przewagi przy prostszej bazie kodu. Nie przenoszę historycznych porównań liczby języków ani błędów dawnego LSP na bieżącą wersję. [S18]

W issue Sereny #802 omówiono, że dynamiczne ładowanie narzędzi Claude Code zmieniło dawny problem dużego narzutu MCP. Porady z 2025 roku o stałym ładowaniu wszystkich opisów mogą być nieaktualne. Aktualna dokumentacja Claude Code opisuje Tool Search i wyjątki przy gatewayach. [S19][S20]

Własna rekomendacja: najpierw porównać natywne LSP i Serena na dwóch rzeczywistych refaktoryzacjach. Nie utrzymywać obu tylko dlatego, że każdy obiecuje oszczędność.

### Context Mode Engine

Repo: https://github.com/mksglu/context-mode

Lokalny plugin przechowuje duże wyniki poza rozmową i umożliwia odczyt potrzebnych fragmentów. Obecna dokumentacja odróżnia go od płatnej, hostowanej usługi Gateway. Licencja lokalnego projektu jest source-available ELv2, a nie zwykłym MIT. [S21]

Podawane redukcje około 99% dotyczą wybranych bajtów wyjścia. Nie są automatycznie redukcją 99% tokenów całej sesji. Benchmark Gateway jest dodatkowo innym produktem i nie dowodzi identycznego efektu lokalnego pluginu. [S22]

Użytkownicy zgłaszają korzyści, ale także konflikty z RTK i instrukcjami agentów. Issue #1151 dotyczyło zawyżania „saved tokens” przez liczenie odczytów binarnych; według świeżego API zamknięte 4 listopada 2026. Traktuję to jako historyczną lekcję metodologii, nie nieusunięty błąd bieżącej wersji. [S23][S24]

Dla Ciebie: logi FFmpeg, Blender, testy i duże odpowiedzi JSON mogą być filtrowane. Krytyczne ostrzeżenia renderu muszą pozostać widoczne. Referencji obrazowych i finalnych klatek nie zastępować tekstowym skrótem.

### QMD

Repo: https://github.com/tobi/qmd

Lokalna wyszukiwarka dokumentów z wyszukiwaniem tekstowym i semantycznym; bardziej zaawansowane tryby korzystają z lokalnych modeli. Udostępnia CLI i MCP. Może kierować Claude do odpowiedniego pliku wiedzy zamiast ładowania całej biblioteki. [S25]

Jest pozytywna relacja użytkownika pracującego z dokumentacją biznesową, ale nie zawiera kontrolowanego pomiaru oszczędności. [S26]

Otwarte issue #897 opisuje uszkodzone embeddingi przy konkretnej granicy długości w wersji 2.5.3. Nie oznacza to, że cały QMD nie działa. Oznacza, że w pilotażu trzeba testować wyszukiwanie znanych informacji, a przy wątpliwościach zacząć od zwykłego wyszukiwania tekstowego. Aktualny status zgłoszenia potwierdziłem w API. [S27]

Własna rekomendacja: osobne kolekcje plugin-development, motion-knowledge i klientów. Domyślnie zwracać krótką listę trafień, a następnie odczytywać wskazane dokumenty w oryginale.

### RTK

Repo: https://github.com/rtk-ai/rtk

Skraca wyjścia poleceń, np. testów i git. Sam upstream rozróżnia obecnie kompresję outputu od oszczędności całego rachunku. Wskaźniki tokenów mogą być szacowane z bajtów. [S28]

Niezależny benchmark JetBrains na zadaniach SkillsBench wykazał około 7,6% wyższy koszt przy low effort i brak różnicy przy high effort. Jakość nie zmieniła się w wykrywalny sposób. To test określonej wersji i środowiska, nie dowód, że RTK nigdy nie pomaga. Jest jednak mocnym powodem, by nie obiecywać uniwersalnych 60–90%. [S29]

Własna rekomendacja: testować na nadmiernie gadatliwych komendach. Zachować możliwość odczytu pełnego logu i poprawne exit codes. Nie nakładać równocześnie RTK, Context Mode i kompresora bramki bez osobnego pomiaru.

### Claude-Mem

Repo: https://github.com/thedotmack/claude-mem

Aktualna dokumentacja opisuje dodatkowego obserwatora, który tworzy pamięć. Może używać planu Anthropic lub innego dostawcy. Istnieją też opcje płatnej usługi; przechowywanie lokalne nie oznacza, że cała analiza odbywa się bez wywołań LLM. [S30]

Issue #4965 opisuje bardzo duże zużycie obserwatora. Inne zgłoszenie #4070 przedstawia 43,3% surowego ruchu tokenowego przypadającego na obserwatora w czterogodzinnym oknie. Autor wyraźnie odróżnia to od kosztu i procentu abonamentu. Nie generalizuję wartości na wszystkich użytkowników. [S31][S32]

Własna rekomendacja: przy Twoim głównym problemie odłożyć automatycznego obserwatora. Pamięć tworzona na koniec etapu może być prostsza do kontrolowania.

### Caveman i duże frameworki workflow

Repo Caveman: https://github.com/JuliusBrussee/caveman

JetBrains zmierzył około 8,5% mniej tokenów wyjściowych w realnych zadaniach agentowych, przy wymuszonym aktywowaniu skilla. Reklamowane 65% pochodzi z innego rodzaju odpowiedzi. To nie jest uniwersalny limit możliwości techniki, tylko wynik danego eksperymentu. [S33]

Dla Ciebie wystarczy naturalne polecenie ograniczające zbędne komentarze podczas kodowania. Nie stosować stylu Caveman do scenariuszy, tekstów reklamowych i promptów.

Superpowers i podobne rozbudowane metodyki mogą podnosić jakość procesu, ale nie klasyfikuję ich jako automatycznych oszczędzaczy tokenów. Wiele etapów, recenzji i agentów może być uzasadnione dla trudnej pracy. W prostym zadaniu trzeba mierzyć ich narzut zamiast automatycznie uruchamiać całą procedurę.

## 7. Adaptacja do całego workspace bez przenoszenia oszczędności na jakość

To proponowana architektura, nie wykonana modyfikacja.

### Warstwa wspólna

Krótki zestaw reguł wybiera rodzaj zadania. Reszta jest ładowana dopiero, gdy potrzebna. Nie kopiować pełnej dokumentacji wszystkich narzędzi do globalnego CLAUDE.md.

Dokumenty stanu powinny rozdzielać: cel, zatwierdzone decyzje, aktualne pliki, otwarte problemy, następny krok i źródła. Jeden aktualny stan zastępuje serię nieuporządkowanych handoverów, ale nie usuwa archiwalnych źródeł.

### Tryby

| Obszar | CODE | CREATIVE | MIXED |
|---|---|---|---|
| Ponytail | Opcjonalnie, pilotaż | Wyłączony | Tylko techniczna implementacja |
| Minimalizacja zakresu | Do pełnego rozwiązania zgłoszenia | Bez samowolnego upraszczania briefu | Wymagania kreatywne mają pierwszeństwo |
| Logi i dane techniczne | Filtrować | Filtrować bez utraty QA | Filtrować |
| Prompty końcowe, copy | Kompletne, jeśli wymagane | Chronione przed skracaniem | Chronione |
| Referencje i klatki | Zależnie od zadania | Odczyt i ocena wizualna | Odczyt i ocena wizualna |
| Pamięć | Decyzje i ustalenia techniczne | Zatwierdzony brief, ciągłość i feedback | Oba typy, z jawnym statusem |
| Zmiana modelu | Po ocenie zadania | Bez ukrytego fallbacku | Model jawny dla każdego etapu |
| QA | Odpowiednie testy | Kryteria estetyczne i produkcyjne | Testy i ocena wizualna |

### Krytyczne rozróżnienie

- Naprawa parsera manifestu: CODE.
- Zmiana opisu trybu instalacji: CODE lub dokumentacja.
- Zaprojektowanie kinetycznej typografii: CREATIVE.
- Dopisanie shadera, by uzyskać zaakceptowany wygląd: MIXED.
- Refaktoryzacja kodu renderowania z identycznym rezultatem: CODE z kontrolą wizualnej regresji.
- Doprecyzowanie skilla reżyserii w Creative Studio: CREATIVE/MIXED, choć plikiem jest Markdown.

### Co można oszczędzać w produkcji kreatywnej

Można ograniczyć powielanie briefu, odczyt nieistotnych modułów, wielkie logi, raportowanie każdego kroku i niepotrzebne ponawianie renderu. Nie należy skracać wymaganych informacji o kamerze, świetle, ruchu, typografii, ciągłości, dźwięku i referencjach.

Przy Twoich materiałach osobne 9:16 i 16:9 pozostają osobnymi kompozycjami/generacjami, jeśli tak stanowi brief. Oszczędzanie nie upoważnia do zastąpienia jednego formatu cropem ani do oddania wersji uproszczonej.

## 8. Jak potwierdzić oszczędność u Ciebie

Nie porównywać dwóch różnych dni z innymi zadaniami i przypisywać różnicy pluginowi.

Proponowany test:

1. Wybrać 6–10 reprezentatywnych zadań: poprawka błędu, refaktoryzacja, mała funkcja, przegląd dokumentacji, analiza dużego logu, odszukanie decyzji.
2. Dodać dwa przypadki MIXED, aby sprawdzić, czy optymalizacja nie upraszcza produkcji.
3. Porównywać bazę z pojedynczym dodatkiem. Taki sam commit, model, effort i kryteria.
4. Dla istotnych wniosków powtórzyć każdą parę przynajmniej trzy razy; zmieniać kolejność wariantów.
5. Osobno zanotować warunki cache. Nie porównywać ciepłego cache jednej wersji z zimnym drugiej.
6. Liczyć cały przebieg aż do akceptowalnego wyniku, również poprawki i pracę pomocniczych modeli.
7. Zachować log użytych narzędzi oraz informację, czy dodatek rzeczywiście został użyty.

Przykładowy arkusz pomiarowy:

| Pole | Co zapisać |
|---|---|
| Zadanie | Jednoznaczny opis i kryterium ukończenia |
| Wersje | Klient, model, effort, plugin, commit repo |
| Wejście | Nowe input, cache read, cache write |
| Wyjście | Output oraz dostępne dane thinking |
| Agentowość | Liczba wywołań i pomocniczych sesji |
| Czas | Czas do zaakceptowanego wyniku |
| Poprawki | Próby po błędzie i interwencje użytkownika |
| Wynik | Testy, kompletność, jakość wizualna |
| Koszt dodatkowy | Indeksowanie, observer, embeddingi, gateway |
| Abonament | Oficjalny odczyt przed/po, ze świadomością innych sesji |

Kryterium proponowane przeze mnie: wdrażać dodatek, jeśli daje powtarzalną poprawę całkowitego kosztu lub czasu przy zachowaniu jakości. Próg orientacyjny 10–15% jest warunkiem biznesowym do wyboru, nie wynikiem researchu. Utrata wymagań, dodatkowe regresje albo trudna diagnostyka mogą przeważyć nawet nad większą redukcją tokenów.

## 9. Gotowy prompt do Claude na audyt przed adaptacją

### Dodatkowy zakres handoveru: dwa skille do przeanalizowania

Na prośbę Kamila do analizy dochodzą **Marketing Psychology (`marketing-psychology`)** oraz **Chief of Staff (`chief-of-staff`)**. To osobny zakres dotyczący jakości marketingu i organizacji pracy FrameCore Works. Nie są tu rekomendowane jako narzędzia oszczędzania tokenów ani zatwierdzone do instalacji.

Źródłem zgłoszenia są dwa zrzuty ekranu rolki konta Microtech.usa, zatytułowanej „5 Hidden Claude Skills”, przekazane 10 listopada 2026. Screeny pokazują nazwy skilli, ale nie ich autorów, repozytoriów ani treści. Dokładna implementacja, autor, URL, wersja i licencja: **Unknown**. Nie należy uznawać dowolnego projektu o tej samej nazwie za skill z filmu ani traktować materiału promocyjnego jako potwierdzenia skuteczności.

| Kandydat | Co Claude ma ocenić dla FrameCore Works |
|---|---|
| `marketing-psychology` | Czy zawiera użyteczne, uzasadnione zasady analizy odbiorcy, pozycjonowania oferty, hooków, copy, CTA i testowania komunikatów. Porównać z istniejącymi modułami marketingu, strategii kampanii i copy. Wskazać konkretną wiedzę „crème de la crème” wartą adaptacji oraz elementy powielone lub pozbawione dowodów. |
| `chief-of-staff` | Czy może usprawnić porządkowanie briefów, priorytetów, zadań, zależności, decyzji i przekazań między sesjami lub projektami. Porównać z obecną orkiestracją i dokumentacją studia. Ocenić, czy upraszcza pracę, czy dodaje zbędne raporty, spotkania i automatyczne odczyty. |

W pierwszej kolejności Claude ma odnaleźć i zweryfikować źródła oraz przeczytać rzeczywiste instrukcje. Jeśli tożsamość pozostaje niejednoznaczna, ma opisać znalezionych kandydatów i pozostawić identyfikację jako Unknown. Dla obu skilli ma określić wymagane integracje, uprawnienia, koszty i narzut kontekstu, a następnie zaproponować: adaptację wybranej wiedzy, osobny opcjonalny skill albo odrzucenie. Wartość marketingowa i organizacyjna ma być oceniana niezależnie od oszczędności tokenów. Na tym etapie wyłącznie analiza i propozycja.

### Kompletny prompt przekazania

Poniższy prompt nie jest zgodą na instalację, płatne wywołania ani zmianę dostawców.

```text
Przeprowadź audyt oszczędzania tokenów w moim środowisku FrameCore Works. Celem jest zmniejszenie zbędnego kontekstu i niepotrzebnych iteracji bez obniżania jakości kodu ani pracy kreatywnej.

Dodatkowo przeanalizuj dwa skille, niezależnie od tematu oszczędzania tokenów: Marketing Psychology (marketing-psychology) oraz Chief of Staff (chief-of-staff). Ten dodatkowy zakres dotyczy marketingu i organizacji pracy, nie instalacji.

Zakres bieżącego zadania: odczyt dostępnej lokalnej konfiguracji, instrukcji, skilli, hooków i logów oraz przygotowanie konkretnej propozycji zmian. Nie instaluj dodatków, nie zmieniaj konfiguracji, nie wysyłaj danych do nowych usług, nie uruchamiaj płatnych modeli i nie rób pushu. Nie odczytuj ani nie wypisuj sekretów.

Najpierw ustal, w jakim trybie pracujesz: Claude Chat, Claude Desktop Chat, lokalny Claude Code, Claude Code cloud albo Cowork. Nie zakładaj wspólnego systemu plików ani jednakowej obsługi pluginów. Sprawdź wersję klienta i dostępne mechanizmy. Brak danych oznacz Unknown.

Przejrzyj obowiązujące AGENTS.md, CLAUDE.md, reguły, aktywne pluginy i hooki. Zidentyfikuj duplikaty instrukcji, duże materiały ładowane zawsze, automatyczne pełne audyty, powtarzane odczyty, niepotrzebne delegowanie i ewentualne procesy pamięci w tle. Wykorzystuj ograniczone odczyty i nie wklejaj całych logów do rozmowy.

Rozdziel rodzaje pracy:
CODE: implementacja, debugging, refaktoryzacja i utrzymanie.
CREATIVE: koncepcja, reżyseria, motion graphics, obraz, scenariusz, copy, prompty i zlecenia klientów.
MIXED: kod lub dokumentacja realizujące wymagania kreatywne. Sam fakt pracy w Pythonie, JavaScript, shaderze albo Markdown nie oznacza CODE.

Oceń kandydatów:
- https://github.com/DietrichGebert/ponytail
- https://github.com/getzep/graphiti
- https://github.com/ccusage/ccusage
- https://github.com/oraios/serena
- https://github.com/mksglu/context-mode
- https://github.com/tobi/qmd
- https://github.com/rtk-ai/rtk

Osobno oceń marketing-psychology oraz chief-of-staff. Nazwy pochodzą z dwóch screenów rolki konta Microtech.usa „5 Hidden Claude Skills”. Screeny nie podają repozytoriów ani autorów. Dokładny autor, URL, wersja i licencja są obecnie Unknown. Wyszukaj źródła publiczne, zweryfikuj pochodzenie, aktualność i licencję oraz przeczytaj rzeczywiste SKILL.md i powiązane instrukcje. Nie uznawaj zgodności nazwy za dowód, że znalazłeś implementację z filmu. Jeśli identyfikacja pozostaje niepewna, opisz kandydatów i oznacz to Unknown. Nie traktuj obietnic z rolki jako potwierdzenia skuteczności.

Dla marketing-psychology sprawdź przydatność do analizy odbiorcy, pozycjonowania oferty, hooków, copy, CTA i testowania komunikatów w kampaniach FrameCore Works. Oddziel zasady poparte dowodami od nieuzasadnionych obietnic. Porównaj z istniejącymi modułami marketingu, strategii kampanii i copy.

Dla chief-of-staff sprawdź przydatność do porządkowania briefów, priorytetów, zadań, zależności, decyzji i handoverów. Porównaj z obecną orkiestracją i dokumentacją studia. Sprawdź, czy proponowany workflow ogranicza powtarzanie pracy, czy tworzy dodatkowy narzut raportowania i kontekstu. Sam skill nie daje zgody na wiadomości do innych osób, zmianę kalendarza ani działania zewnętrzne.

Dla obu wskaż konkretną wiedzę „crème de la crème” wartą adaptacji, powielone funkcje, wymagane integracje, uprawnienia, koszty oraz narzut tokenów. Zaproponuj adaptację wybranej wiedzy do istniejących modułów, osobny opcjonalny skill albo odrzucenie, z uzasadnieniem. Oceniaj wartość marketingową i organizacyjną oddzielnie od token efficiency. Nie deklaruj oszczędności bez pomiaru. Nie instaluj ani nie wdrażaj tych skilli w ramach tego audytu.

Nie utożsamiaj procentu skrócenia logów z oszczędnością całej sesji. Oddziel input, output, cache read/write, koszt dodatkowych modeli, szacowany koszt API i oficjalne zużycie abonamentu.

Ponytail oceniaj tylko jako opcjonalną politykę CODE. W CREATIVE pozostaje wyłączony. W MIXED nie może usuwać wymagań, upraszczać zaakceptowanej estetyki ani obniżać QA. Sprawdź, czy hook pluginu nie wstrzykuje go niezależnie od ustawień skilla.

Graphiti oceniaj jako pamięć decyzji, z kosztami ingestu i retrieval. Najpierw porównaj z prostymi plikami stanu i wyszukiwaniem dokumentów. Nie planuj automatycznego zapisywania każdej wiadomości.

W pracy kreatywnej chronione są: pełny brief, dokładny tekst, prompty końcowe, referencje, kamera, światło, ruch, rytm, ciągłość, formaty, dźwięk i kryteria jakości. Oszczędzaj na duplikacji i szumie technicznym.

Zwróć:
1. diagnozę opartą na dostępnych danych;
2. listę proponowanych zmian z konkretnymi plikami i zakresem;
3. oddzielne profile CODE, CREATIVE i MIXED;
4. plan A/B z metrykami całego zadania i jakością;
5. koszty dodatkowe, ograniczenia hosta i sposób cofnięcia każdej zmiany;
6. krótki dokument aktualnego stanu do dalszej pracy;
7. osobną ocenę marketing-psychology i chief-of-staff: identyfikacja źródeł i jej pewność, przydatność dla FrameCore Works, pokrywanie się z obecnymi modułami, wiedza do adaptacji, wymagania, koszty oraz rekomendacja dalszych kroków.

Nie wprowadzaj jeszcze zmian. Najpierw przygotuj propozycję, którą da się przejrzeć.
```

## 10. Granice pewności

- Nie mam danych o Twoim aktualnym planie, modelach, effort, hookach ani udziale poszczególnych procesów w limicie.
- Nie uruchomiłem benchmarków na Twoich repozytoriach.
- Doświadczenia użytkowników bywają zależne od starych wersji; nie traktuję ich jako opisu każdego obecnego wydania.
- Liczba gwiazdek, pobrań i pozytywna opinia modelu nie są dowodem oszczędności.
- Nie znalazłem niezależnego potwierdzenia jednolitej oszczędności abonamentu na web, mobile, Desktop i Code przez jeden z badanych dodatków.
- Bieżący stan repozytoriów i usług może się zmienić; przed instalacją trzeba ponownie ustalić wydanie i przypiąć wersję.
- Licencje trzeba sprawdzać przy kopiowaniu kodu do pluginu. Użycie zewnętrznego narzędzia i redystrybucja jego kodu to różne decyzje. W czasie researchu: Ponytail MIT, Graphiti Apache-2.0, QMD MIT, Context Mode ELv2; Serena ma podział licencji komponentów, RTK również rozróżnia edycje.

## 11. Źródła

Dokumentacja i repozytoria stanowią źródła mechanizmów. Reddit oraz GitHub Issues są źródłami bezpośrednich doświadczeń użytkowników, nie konsensusu. Benchmarki autora oznaczono jako takie. Wszystkie poniższe materiały wykorzystano podczas researchu; statusy wybranych issues dodatkowo odczytano przez GitHub API.

- [S1: Anthropic, Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)
- [S2: Claude Code, Manage costs effectively](https://code.claude.com/docs/en/costs)
- [S3: Claude Code, Prompt caching](https://code.claude.com/docs/en/prompt-caching)
- [S4: Anthropic, Usage and length limits](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)
- [S5: Desktop and web connectors](https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors)
- [S6: Cowork on web, desktop and mobile](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- [S7: Remote Control](https://code.claude.com/docs/en/remote-control)
- [S8: Skills, synchronizacja i zakresy](https://code.claude.com/docs/en/skills)
- [S9: Ponytail, właściwy SKILL.md](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md)
- [S10: Ponytail, benchmark autora 2026-10-07](https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-10-07-agentic.md)
- [S11: Marmelab, doświadczenia z trzema dodatkami](https://www.reddit.com/r/ClaudeAI/comments/1w3hxt1/i_tested_3_claude_code_plugins_to_reduce_costs/)
- [S12: Ponytail, pozytywne i negatywne relacje](https://www.reddit.com/r/ClaudeCode/comments/1x2w4yo/does_actually_ponytail_plugin_spend_less_tokens/)
- [S13: Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md)
- [S14: Graphiti #1193, koszt ekstrakcji](https://github.com/getzep/graphiti/issues/1193)
- [S15: Graphiti MCP, ograniczenia serwera referencyjnego](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md)
- [S16: ccusage](https://github.com/ccusage/ccusage)
- [S17: Serena](https://github.com/oraios/serena)
- [S18: Serena, doświadczenia z aplikacją iOS](https://www.reddit.com/r/ClaudeCode/comments/1qlz0em/my_claude_code_setup_after_8_months_12_custom/)
- [S19: Serena #802, narzut MCP i dynamiczne ładowanie](https://github.com/oraios/serena/issues/802)
- [S20: Claude Code, MCP i Tool Search](https://code.claude.com/docs/en/mcp)
- [S21: Context Mode Engine README](https://github.com/mksglu/context-mode)
- [S22: Context Mode Gateway, benchmark autora](https://contextmode.ai/docs/benchmarks)
- [S23: Context Mode, doświadczenia i konflikty](https://www.reddit.com/r/ClaudeCode/comments/1ttu85z/is_context_mode_really_working/)
- [S24: Context Mode #1151, pomiar saved tokens](https://github.com/mksglu/context-mode/issues/1151)
- [S25: QMD README](https://github.com/tobi/qmd)
- [S26: QMD, relacja użytkownika pracującego z dokumentami](https://www.reddit.com/r/ClaudeAI/comments/1qubibp/how_to_set_up_claude_code_qmd_local_search_in_15/)
- [S27: QMD #897, embeddingi](https://github.com/tobi/qmd/issues/897)
- [S28: RTK README](https://github.com/rtk-ai/rtk)
- [S29: JetBrains, niezależny benchmark RTK](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/)
- [S30: Claude-Mem README](https://github.com/thedotmack/claude-mem)
- [S31: Claude-Mem #4965, zużycie obserwatora](https://github.com/thedotmack/claude-mem/issues/4965)
- [S32: Claude-Mem #4070, pomiar narzutu i batching](https://github.com/thedotmack/claude-mem/issues/4070)
- [S33: JetBrains, niezależny benchmark Caveman](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/)
- [S34: Oficjalny katalog pluginów Claude Code](https://github.com/anthropics/claude-plugins-official)
- [S35: Claude Code w chmurze](https://code.claude.com/docs/en/claude-code-on-the-web)
- [S36: Zarządzanie dostępem do narzędzi Claude](https://support.claude.com/en/articles/13730515-manage-claude-s-tool-access)

