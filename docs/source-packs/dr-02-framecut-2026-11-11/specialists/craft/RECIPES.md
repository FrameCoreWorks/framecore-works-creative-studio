# Osiemnaście receptur montażowych

Stan badania: 2026-11-11. Wszystkie receptury są **DERIVED**: autorskimi projektami pracy, a nie wykonanymi eksperymentami ani przepisanymi kursami. Źródła pod każdym przepisem wskazują tylko mechanizmy lub praktykę, które wspierają. Własne przykłady, struktury i liczby nie pochodzą z wywiadów. `QA: NOT_RUN` dotyczy prób na materiale, którego w zadaniu nie dostarczono. Czytano teksty dokumentacji i wywiadów, nie filmowe przykłady.

## Wspólna umowa wykonania

- Receptura zaczyna się od oceny źródeł, nie od automatycznego tworzenia timeline. Źródło pozostaje niezmienne; każdy wybór zachowuje identyfikator, zakres źródłowy i powód.
- Domyślne liczby w przykładach: `fps_num=25`, `fps_den=1`, audio 48000 próbek/s, zakresy `[in,out)`. To parametry hipotetycznego projektu, **nie wymogi platformy**. Każdą zmianę czasu liczymy w zegarze wskazanym przez pole.
- „Reprezentacja agentowa” jest opisem danych i oczekiwanych operacji, **nie istniejącym API FrameCut**. Kompilacja do jego aktualnego schematu wymaga mapowania i testu adaptera. Nie nazywamy konceptualnego polecenia funkcją wdrożoną.
- Każdy plan ma `project_id`, rewizję bazową, zbiór zmienianych instancji/ścieżek, źródła po hashach, preconditions i oczekiwany delta czasu. Niezgodna rewizja, brak handles lub niepewne źródło powodują zatrzymanie danej operacji, nie ciche zastąpienie materiału.
- Podgląd kontaktowy służy selekcji orientacyjnej. Ruch, dykcję, emocję, rytm i synchronizację sprawdza się w czasie rzeczywistym. Weryfikacja techniczna nie zastępuje odbioru redakcyjnego.

## R01 — Przyjęcie materiału i selekcja przed montażem

1. **Cel.** Ustalić, co faktycznie nagrano, co jest używalne i czego brakuje; zbudować odwracalną mapę kandydatów.
2. **Potrzebne źródła.** Struktury kart, osobny dźwięk, raport planu lub brief, scenariusz jeśli istnieje, wykaz zamierzonych scen i zgód na materiał. Nie zakładać, że nazwa pliku wyjaśnia treść.
3. **Decyzje montażowe.** Obejrzeć całe ujęcia, oznaczyć funkcję oraz najlepsze momenty; oddzielić wadę dyskwalifikującą od naprawialnej. Rejestrować zarówno mocne wykonanie, jak i ograniczenie. Dubel „A” może mieć lepszą emocję, „B” czytelniejszą demonstrację.
4. **Kolejność operacji.** Inwentaryzacja → kontrolowana kopia i weryfikacja hashy → odczyt metadanych → próbne dekodowanie → opis braków → synchronizacja robocza → pełny przegląd → markery i tematy → selects z linkami do pełnych źródeł. Dopiero potem wstępne grupy scen.
5. **Parametry/jednostki.** Hash odnosi się do bajtów; zakres selecta do klatek lub PTS źródła. Oceny `usable/conditional/reject` oraz pewność ASR są odrębnymi polami, nie jedną oceną „jakości”.
6. **Warianty.** Długi dokument potrzebuje tematów i osób; fabuła scen/dubli; reklama kategorii funkcji produktu. Selects jest opcjonalny: można preferować markery i regularny powrót do pełnych rushes.
7. **Błędy.** Usunięcie nieoznaczonych fragmentów, deduplikacja po nazwie, selekcja na podstawie miniatur, użycie proxy jako archiwum.
8. **Naprawa.** Powrót do oryginałów; odbudowa relacji po hashach i czasie. Niepewny rekord pozostaje `Unknown`; ponowny przegląd odrzuconego materiału po zmianie intencji sceny.
9. **Reprezentacja agentowa.** `asset → inspection_span → observation → candidate → reason`; obserwacja ruchu i odsłuch mają osobne statusy. Nie budować osi z kandydatów o nieznanym znaczeniu. Odrzucenie kandydata nie usuwa pliku.
10. **QA.** NOT_RUN: zgodność liczby i sum kopii; źródło dostępne dla każdego selecta; próbny odczyt początku/środka/końca oraz pełne obejrzenie wybranych zakresów. Redakcyjnie: alternatywa dla kluczowej sceny i jawna lista braków.
11. **Źródła.** [C02]: znaczenie przeglądania dubli. [C08]: Staenberg opisuje pracę z markerami bez selects reels. Strategia kopii, schemat danych i procedura kontroli: DERIVED.

## R02 — Wywiad z B-rollem oraz J/L-cutami

1. **Cel.** Zbudować spójną wypowiedź, zachować charakter rozmówcy i pokazać konkretne konteksty jego słów.
2. **Potrzebne źródła.** Pełny wywiad z pytaniami, dźwięk wysokiej jakości, room tone, opisane B-rolle, źródłowy transcript z czasem i zaznaczonymi niepewnościami.
3. **Decyzje montażowe.** Najpierw odsłuchać pełne odpowiedzi. Wybrać tezę, przykład i niezbędne zastrzeżenie; zachować negacje i modalność. B-roll ma coś objaśniać. Reakcja nie może sugerować innego wydarzenia niż udokumentowane.
4. **Kolejność operacji.** Paper edit → kontrola sensu w oryginale → assembly audio → dostrojenie oddechów → główne obrazy → B-roll → rozdzielenie granic A/V → room tone i crossfades → napisy → podgląd pełnej wypowiedzi. Zwykłe cięcie może pozostać widoczne, jeśli to uczciwsze i czytelniejsze.
5. **Parametry/jednostki.** Przykład J: audio B zaczyna się przy TL 200, obraz B przy 210; przy 25 fps wyprzedzenie wynosi 0,4 s. Źródłowy offset A/V pozostaje ten sam; zmieniamy wykorzystane granice, nie synchronizację ust. B-roll nad V1 nie wymaga wydłużenia osi.
6. **Warianty.** Wywiad obserwacyjny zachowuje dłuższe pauzy; film instruktażowy może skracać powtórzenia. Brak dobrego B-rollu: użyć prostego cięcia lub pozostać na twarzy.
7. **Błędy.** Frankenstein zdania, B-roll przedstawiony jako dowód zdarzenia, muzyka wymuszająca wzruszenie, identyczne crossfades wszędzie.
8. **Naprawa.** Przywrócić kontekst i zaimki; porównać skrót z pełną odpowiedzią; zamienić nieadekwatną przebitkę; przywrócić oddech lub obniżyć tło.
9. **Reprezentacja agentowa.** Każdy segment mowy ma `speaker_id`, source span, context span i zachowany sens. Oddzielne instancje obrazu/audio z sync group; B-roll jako warstwa nad obrazem. Raport wskazuje każde połączenie nieprzylegających fragmentów wypowiedzi.
10. **QA.** NOT_RUN: odsłuch bez obrazu; odsłuch oryginalnego kontekstu przy każdym skrócie znaczeniowym; ogląd J/L w czasie rzeczywistym; brak urwanych fonemów, klików i pozornej reakcji. Test techniczny: zero niezamierzonych zmian offsetu synchronizacji.
11. **Źródła.** [C02]: definicje split edits; [C06]: ostrożność wobec muzyki pod dokumentalnymi wypowiedziami. Cały porządek i przykład liczbowy: DERIVED.

## R03 — Scena fabularna: spojrzenia, reakcje i alternatywne duble

1. **Cel.** Pokazać zmianę relacji między postaciami, bez sprowadzenia sceny do naprzemiennych wypowiedzi.
2. **Potrzebne źródła.** Master, coverage każdej postaci, pickupy, raport ciągłości, pełny dźwięk i scenariusz. Oddzielne duble nie są multicamem tego samego wykonania.
3. **Decyzje montażowe.** Obejrzeć każdą wersję sceny. Dla każdego zwrotu wybrać, czy ważniejsze jest działanie mówiącego, czy odbiór słuchacza. Ocenić natężenie gry w kontekście sąsiednich scen, nie tylko atrakcyjność pojedynczego dubla.
4. **Kolejność operacji.** Mapa celu i zwrotów → orientacja przestrzenna → assembly dialogu → dobór reakcji → porównanie alternatyw → roll/slip granic → J/L → ciągłość tła → ogląd scen przed i po. Zachować wersję przed zmianą dubla.
5. **Parametry/jednostki.** Pierwsza korekta punktu cięcia może badać okno ±4 klatki; to zakres eksperymentu, nie norma. Zmiana długości dubla wymaga rozstrzygnięcia: wyrównanie w oknie albo jawne ripple zależnych ścieżek.
6. **Warianty.** Komedia może czekać na reakcję; thriller zatrzymać odpowiedź poza kadrem. Nie ciąć, gdy wewnętrzna przemiana aktora dzieje się w jednym ujęciu. Oś można zmienić po zrozumiałym przeorientowaniu przestrzeni.
7. **Błędy.** Cięcie przy każdej zmianie mówcy; zbyt szybkie ujawnienie reakcji; perfekcyjny rekwizyt kosztem właściwej emocji.
8. **Naprawa.** Odtworzyć szerszy plan, usunąć zbędną zmianę kąta, porównać dwie wersje bez muzyki i z pełnym dźwiękiem. Wybrać świadomy kompromis, zamiast mnożyć poprawki maskujące.
9. **Reprezentacja agentowa.** Graf zwrotów sceny z przypisanymi kandydatami; alternatywy mają wspólną funkcję i osobne source spans. Komentarz decyzji wskazuje utrzymany sens i zaakceptowane drobne odstępstwo ciągłości.
10. **QA.** NOT_RUN: widz potrafi określić, kto na kogo patrzy i co zmieniło relację. Kontrola rekwizytów oraz A/V; odtworzenie całej sceny z dwiema scenami sąsiednimi. Recenzja rytmu nie jest statystyką liczby cięć.
11. **Źródła.** [C02]: kompromis gra–ciągłość oraz odrębne duble. [C03]: rozpatrywanie materiału z perspektywy widza. Procedura i kryteria: DERIVED.

## R04 — Ciągła akcja i cut on action

1. **Cel.** Zapewnić zrozumienie celu ruchu, jego przebiegu i skutku przy zmianach punktu widzenia.
2. **Potrzebne źródła.** Master akcji, detale i kąty alternatywne, nagrania kontaktów i ruchu, mapa przestrzeni. Ujęcia oceniane w ruchu, nie po ostrych stopklatkach.
3. **Decyzje montażowe.** Wskazać inicjację, kierunek, kontakt i konsekwencję. Dobra reakcja lub skutek może być ważniejszy od najbardziej widowiskowej fazy. Wybrać kompatybilną pozycję ciała i prędkość ekranową.
4. **Kolejność operacji.** Zrozumiała szeroka baza → zaznaczenie faz akcji → podmiana wybranych momentów detalem → dopasowanie fazy przez slip → punktu cięcia przez roll → porównanie bez i z SFX → sprawdzenie całości.
5. **Parametry/jednostki.** Próbować kilku wariantów sąsiednich klatek. Zgodność przestrzeni nie wymaga idealnego zrównania źródłowych TC, gdy ujęcia są różnymi dublami. Zakres ruchu i wynikowy czas pozostają jawne.
6. **Warianty.** Powtórzona faza może celowo potęgować uderzenie w stylizowanej akcji; instrukcja obsługi zwykle wymaga jednoznacznej kolejności. Długi, czytelny master bywa lepszy od serii detali.
7. **Błędy.** Dwa kontakty dłoni z przedmiotem, zmiana strony ruchu, wycięty skutek, dźwięk kontaktu przesłaniający błędną fizykę.
8. **Naprawa.** Przywrócić fazę lub pominąć zbędną powtórkę; dołożyć plan orientacyjny, przesunąć detal lub całkiem z niego zrezygnować. Nie ratować nieczytelnej akcji samymi przejściami.
9. **Reprezentacja agentowa.** `action_id` i fazy z source spans; ograniczenia kierunku i stanu rekwizytu. Plan deklaruje zwykłą ciągłość albo celowe powtórzenie. SFX kotwiczony do punktu kontaktu w TL.
10. **QA.** NOT_RUN: real-time w normalnej prędkości, potem klatki wokół kontaktów; sprawdzenie kierunków i liczby zdarzeń. Osoba nieznająca planu potrafi odtworzyć przyczynę i skutek.
11. **Źródła.** [C08]: ciągłość energii ruchu między kadrami. [C02]: dopasowanie akcji z pickupem. Konkretne fazy i test: DERIVED.

## R05 — Dokument wielowątkowy i uczciwa kompresja

1. **Cel.** Zbudować zrozumiałą opowieść z rozproszonego materiału bez wynajdywania konfliktu ani fałszywej przyczynowości.
2. **Potrzebne źródła.** Pełne wywiady, sceny obserwacyjne, chronologia zdarzeń, dokumenty i archiwalia z pochodzeniem. Rozbieżne relacje zachowane osobno.
3. **Decyzje montażowe.** Ocenić, które zachowanie ujawnia postać, a które zdanie tylko informuje. Zaznaczyć różnicę między faktem, wspomnieniem a interpretacją. Wybrać punkt widzenia i konieczny kontekst kontrujący mocną tezę.
4. **Kolejność operacji.** Logowanie → mapa tematów i chronologii → karty wątków → osobne krótkie assembly → próby przeplotu → kontrola faktów i kontekstu → fine cut → osobny review etyczny scen wrażliwych.
5. **Parametry/jednostki.** Osobno czas wydarzenia, nagrania i montażu. Każdy archiwalny insert ma identyfikator i deklarację, co dokumentuje. Długości wynikają z rozumienia scen, nie ze stałego trzyaktowego procentu.
6. **Warianty.** Dokument śledczy potrzebuje silnej logiki dowodowej; portret może opierać się na obserwacji bez antagonisty. Nielinearność dopuszczalna, jeśli nie fałszuje relacji zdarzeń.
7. **Błędy.** Spojrzenie z innego dnia udaje odpowiedź; montaż sugeruje następstwo przyczynowe; music bed produkuje nieistniejące zagrożenie.
8. **Naprawa.** Przywrócić czas, identyfikację lub wypowiedź kontekstową; usunąć mylne zestawienie. Gdy chronologia pozostaje niepewna, oznaczyć ją i ograniczyć twierdzenie.
9. **Reprezentacja agentowa.** Graf twierdzeń, źródeł i relacji `observed/reported/inferred`; osobny plan redakcyjny. Każde przestawienie scen wymaga ponownego sprawdzenia zależnych tez, nie automatycznie całego filmu.
10. **QA.** NOT_RUN: audyt cytatów względem pełnych pytań; kontrola pochodzenia archiwaliów; odsłuch bez muzyki; zewnętrzny widz opisuje chronologię. Nie orzekać o „prawdzie filmu” jednym wynikiem automatu.
11. **Źródła.** [C06]: konflikt nie jest konieczny i nie należy go fabrykować; [C05]: gatunek i odbiorca warunkują montaż. Proponowany graf i audyt: DERIVED.

## R06 — Rozmowa wielokamerowa z osobnym rejestratorem

1. **Cel.** Pokazać rozmowę oraz reakcje, zachowując stabilny, czytelny dźwięk i synchronizację przez cały odcinek.
2. **Potrzebne źródła.** Kamery z zakresem pokrycia, rejestrator z kanałami rozmówców, scratch audio, dane TC i ewentualny klaps. Weryfikacja twarzy, ostrości i jakości każdego kąta przed przełączaniem.
3. **Decyzje montażowe.** Wybrać master audio niezależnie od kamery. Ciąć do osoby mówiącej, gdy obraz dodaje znaczenie; pozostać na słuchaczu przy ważnej reakcji. Krótkie przytaknięcie nie wymaga osobnego cięcia.
4. **Kolejność operacji.** Weryfikacja metadanych → sync TC/waveform/marker → odsłuch i kontrola klapsa → utworzenie mapy kątów → continuity pass bez skracania → selekcja treści → wspólne ripple obrazu i audio → fine pass kątów → miks.
5. **Parametry/jednostki.** Offset każdego źródła w sekundach wymiernych/próbkach; cięcia obrazu w klatkach. Przykładowy sync test na początku, w połowie i końcu 60 minut. Jednorazowy offset nie naprawia narastającego driftu.
6. **Warianty.** Podcast z jednym kadrem może potrzebować bardzo mało zmian. Przy braku kamery w danym przedziale wybór ogranicza się do rzeczywistego coverage; nie rozciągać klatki w ciszy bez jawnej decyzji.
7. **Błędy.** Audio follows video przełącza barwę głosu, wszystkie mikrofony otwarte dają przesłuch, automatyczny speaker switch reaguje na kaszlnięcie.
8. **Naprawa.** Zablokować wybór master audio, poprawić routing i mapę kanałów; skorygować lokalne granice, zbadać drift. Do niepewnego odcinka wrócić z szerszym planem, nie maskować go przypadkową reakcją.
9. **Reprezentacja agentowa.** Wspólny zegar rozmowy, `angle_available_ranges`, `audio_master`, sync constraints, propozycje cięć z reason i confidence. Diarization jest dowodem pomocniczym; brak zmiany kamery również jest decyzją.
10. **QA.** NOT_RUN: początek/środek/koniec A/V, brak kątów poza coverage, stała konfiguracja kanałów, odsłuch nakładania mówców. Pełne odtworzenie finalnego pliku, nie tylko multicam view.
11. **Źródła.** [C09]: tryby synchronizacji i wybór audio w Premiere; [C02]: multicam jako praca wymagająca późniejszego dopracowania. Plan kontroli: DERIVED.

## R07 — Film produktu z muzyką i sceną FrameMotion

1. **Cel.** Przedstawić istotną cechę produktu w sposób zrozumiały i wiarygodny, zakończyć rozpoznawalnym obrazem marki.
2. **Potrzebne źródła.** Master produktu, detale, demonstracja działania, potwierdzony opis cech, muzyka z prawami, identyfikacja i brief grafiki. Obejrzeć, czy demonstracja naprawdę dowodzi wskazanej cechy.
3. **Decyzje montażowe.** Wybrać ujęcie orientujące, dowód działania i rezultat. Atrakcyjny detal nie zastępuje rozpoznania produktu. Z góry rozstrzygnąć, czy grafika informuje, objaśnia niewidoczny mechanizm czy jest tylko ozdobą.
4. **Kolejność operacji.** Selekcja dowodów → krótki układ bez grafiki → test rytmu → wybór muzyki → plansza robocza o dokładnej długości → zlecenie FrameMotion → odbiór renderu i manifestu → compositing → kolor, miks, napisy → QC.
5. **Parametry/jednostki.** Przykład 30 s = 750 klatek przy 25 fps. Scena grafiki zajmuje `[300,425)` = 125 klatek; dodatkowe handles zamówione osobno, np. 12 klatek na stronę, jeśli planowane są przejścia. Alfa straight/premultiplied musi być określona.
6. **Warianty.** Film techniczny dłużej pokazuje działanie; film wizerunkowy może operować skojarzeniem. Nie każda reklama potrzebuje hook/body/CTA ani mówionego voiceoveru.
7. **Błędy.** Zbyt krótki czas odczytu cechy, logo zasłania mechanizm, kolor zmienia realną barwę produktu, muzyka wymaga nieosiągalnych praw.
8. **Naprawa.** Wydłużyć dowód kosztem dekoracji; przełożyć tekst; skorygować transformację barwną; wymienić muzykę i ponownie ocenić rytm zamiast podmienić plik bez review.
9. **Reprezentacja agentowa.** FrameCut posiada TL; FrameMotion otrzymuje `range`, duration, FPS, resolution, alpha, color, audio policy, accepted locks i rewizję. Zmiana długości grafiki jest change requestem do właściciela osi.
10. **QA.** NOT_RUN: widz rozpoznaje produkt i cechę; czyta tekst raz w normalnym tempie; brak niepotwierdzonych obietnic; kontrola alfa i koloru; render ma dokładnie zamówiony zakres treści i handles.
11. **Źródła.** [C13]: relacja muzyki, produktu i procesu reklamowego; [C04]: współpraca montażu, dźwięku i VFX w rozwijaniu rytmu. Kontrakt FrameMotion i scenariusz produktu: DERIVED.

## R08 — Skrócenie reklamy z 30 do 15 sekund

1. **Cel.** Zbudować samodzielną krótszą wersję zachowującą komunikat i wymagane elementy.
2. **Potrzebne źródła.** Zatwierdzona wersja 30 s, projekt źródłowy, lista locks, alternatywne ujęcia, editable grafika, muzyczne stemy i specyfikacja wersji.
3. **Decyzje montażowe.** Obejrzeć wariant bez znajomości dłuższej historii. Wybrać jedną główną obietnicę i dowód. Usuwać całe zbędne etapy, zamiast skracać każde ujęcie o połowę.
4. **Kolejność operacji.** Zidentyfikować wymagane elementy → policzyć ich realny czas czytania → nowy szkielet 15 s → selekcja pasujących dubli → remont muzyki → nowe długości grafik → finishing → porównanie komunikatu.
5. **Parametry/jednostki.** 15 s = 375 klatek przy 25 fps. Całość musi zawierać wymagany ogon dźwięku i planszę; zapas nie powstaje z retimingu czytanego tekstu. Długości napisów są decyzją po próbie odczytu.
6. **Warianty.** Można zrezygnować z wprowadzenia, gdy produkt jest od razu zrozumiały; przy nowej kategorii trzeba zachować orientację. Wersja 6 s bywa osobnym komunikatem.
7. **Błędy.** Przyspieszona mowa, niedokończona fraza muzyczna, pozostawiony zaimek bez poprzednika, logo miga za krótko.
8. **Naprawa.** Przepisać strukturę na podstawie istniejącego briefu; wybrać krótszą autentyczną wypowiedź; zamówić nowy przebieg grafiki w istniejącym workflow; stworzyć muzyczne zakończenie.
9. **Reprezentacja agentowa.** Nowa wariantowa rewizja z dziedziczonymi locks i relacjami do źródeł, bez nadpisania zaakceptowanego mastera. Manifest wymienia pominięte twierdzenia i zmienione zależności.
10. **QA.** NOT_RUN: frame count 375; brak niedokończonego sensu; odbiorca rozumie wersję bez znajomości 30 s. Sprawdzić finalne audio, czytelność i brak przypadkowych przejść po zmianie długości.
11. **Źródła.** [C05]: cel i odbiorca jako warunki pracy. [C13]: zależność montażu od struktury muzyki. Redukcja do jednego komunikatu jest propozycją DERIVED, nie nakazem źródeł.

## R09 — Tutorial ekranowy, także z VFR

1. **Cel.** Umożliwić odbiorcy wykonanie konkretnej czynności i rozpoznanie poprawnego wyniku.
2. **Potrzebne źródła.** Pełny screen recording, osobna narracja jeśli jest, metadane/PTS, wersja pokazywanego programu, lista kroków i oczekiwany efekt. Sprawdzić, czy kliknięcia i rezultaty są widoczne.
3. **Decyzje montażowe.** Oznaczyć kroki obowiązkowe, oczekiwanie systemu, błędy demonstracyjne i niepotrzebne powtórzenia. Czas potrzebny do odczytu UI ma pierwszeństwo przed energetycznym tempem.
4. **Kolejność operacji.** Odczyt rzeczywistego czasu → sync narracji → próba dekodowania VFR w docelowym torze → ewentualna kontrolowana pochodna CFR → selection → cięcia oczekiwania z jawną elipsą → crop/zoom → callouty → napisy → test wykonania instrukcji.
5. **Parametry/jednostki.** Source PTS nie zastępuje się indeksami `n/FPS` bez mapy. Dla pochodnej CFR zapisać zachowanie czasu rzeczywistego i mapowanie źródła. Zoom oceniać w rozmiarze docelowym, nie tylko przy powiększeniu edytora.
6. **Warianty.** Krótka instrukcja jednego polecenia może obyć się bez intro i muzyki. Tutorial debugowania zachowuje istotny błąd. Native VFR możliwy tylko po teście konkretnego backendu i wersji.
7. **Błędy.** Klik i stan końcowy są w innych wersjach aplikacji; zoom usuwa menu; wycięcie oczekiwania sugeruje natychmiastowy wynik; drift po transkodowaniu.
8. **Naprawa.** Przywrócić brakujący stan, dodać oznaczenie czasu oczekiwania, poprawić mapę synchronizacji; utrzymać oryginał. Nie naprawiać VFR samą zmianą interpretowanego FPS.
9. **Reprezentacja agentowa.** `step_id`, precondition UI, source span, expected state i annotacje w lokalnych współrzędnych obrazu. Transformacje obejmują callouty i obszary ochronne. Nie uznawać OCR za dowód udanego działania aplikacji.
10. **QA.** NOT_RUN: osoba testowa wykonuje zadanie; odczyt UI przy docelowym rozmiarze; sync na początku/środku/końcu; monotoniczne PTS, poprawna długość i brak znikających kroków.
11. **Źródła.** [C12]: VFR ma zmienne czasy klatek, a poprawki Adobe są ogłoszeniem beta. [C11]: rozróżnienie metod interpolacji. Receptura dydaktyczna i wymóg próby wykonania: DERIVED.

## R10 — Teledysk lub sekwencja do muzyki

1. **Cel.** Zbudować rozwój wizualny odnoszący się do utworu, bez mechanicznego przełączania obrazu na każdy beat.
2. **Potrzebne źródła.** Zatwierdzony master muzyczny, prawa, performance takes, obrazy narracyjne/abstrakcyjne, zapis playbacku do synchronizacji. Obejrzeć wykonania pod kątem fraz, nie samych póz.
3. **Decyzje montażowe.** Wyznaczyć formę utworu: wejście, frazy, zmiany harmonii, energii i zakończenie. Wybrać motywy, ich powroty i momenty odmowy cięcia. Czasem ruch wewnątrz ujęcia realizuje akcent lepiej niż cięcie.
4. **Kolejność operacji.** Odsłuch całości → mapa fraz → sync performance → selects → konstrukcja dłuższych sekcji → test akcentów → przeplot narracji → fine cut → kontrola praw i końcowego pliku.
5. **Parametry/jednostki.** Markery muzyczne w próbkach/sekundach, cięcia obrazu kwantowane do klatek. Przy hipotetycznych 120 BPM odstęp ćwierćnut to 0,5 s, czyli 12,5 klatki przy 25 fps; trzeba rozłożyć zaokrąglenia, nie kumulować ich.
6. **Warianty.** Performance wymaga zgodności ust/instrumentu; klip konceptualny może celowo odchodzić od beatów. Muzyka montowana do fabuły może powstać po obrazie — odwrócony proces jest równie uprawniony.
7. **Błędy.** Beat detector myli półtempo; każde cięcie ma tę samą długość; lip-sync poprawny na początku i błędny po retimingu; atrakcyjne ujęcia nie tworzą rozwoju.
8. **Naprawa.** Ręcznie zweryfikować frazę i metrum; przywrócić dłuższe ujęcie; resetować mapę sync dla dubla; zmienić kolejność motywów, zanim doda się przejścia.
9. **Reprezentacja agentowa.** Muzyczny master jako lock, kandydaci związani z sekcją i funkcją; `beat_candidates` odróżnione od zatwierdzonych punktów. Źródło performance ma mapę czasu do utworu.
10. **QA.** NOT_RUN: odsłuch i ogląd w normalnym tempie; lip-sync na spółgłoskach i kontaktach instrumentu; brak narastającego błędu gridu; łuk całej formy, a nie tylko atrakcyjny początek.
11. **Źródła.** [C07], [C08]: przykłady montażystów rozdzielających rytm obrazu od temp music; [C13]: kontrprzykład pracy z muzyką od początku. Mapa formy i przykład 120 BPM: DERIVED.

## R11 — Koncert multicam i prawdziwość wykonania

1. **Cel.** Oddać energię oraz relacje wykonawców, zachowując zgodność obrazu z nagranym wykonaniem.
2. **Potrzebne źródła.** Równoczesne kamery, master/stemy koncertu, scratch audio, mapa braków, ewentualne inne wykonania wyraźnie oznaczone.
3. **Decyzje montażowe.** Wykryć wejścia instrumentalne i ważne interakcje, potem ocenić, który kadr faktycznie je pokazuje. Ujęcie widowni ma rolę dramaturgiczną, nie obowiązkowy procent czasu.
4. **Kolejność operacji.** Sync → odsłuch pełnej formy → przegląd każdego kąta → assembly obrazu przy zablokowanym masterze audio → korekta punktów → matching kamer → ewentualne SFX/ambience → QC.
5. **Parametry/jednostki.** Zegar mastera muzyki jest punktem odniesienia. Dla każdego źródła zapisać offset i test driftu. Przełączanie obrazu nie zmienia mastera dźwięku.
6. **Warianty.** Muzyka kameralna może potrzebować dłuższego gestu; koncert rockowy nie wymaga wszystkich szybkich cięć. Zbliżenie z próby można wykorzystać tylko z kontrolą zgodności i jawną decyzją redakcyjną.
7. **Błędy.** Widzimy grę innej nuty, oklaski wyprzedzają finał, dźwięk skacze między kamerami, stroboskop i optical flow tworzą deformacje.
8. **Naprawa.** Wrócić do zgodnego kąta, poprawić offset, odrzucić niespójny insert; wybrać sampling zamiast syntezy ruchu, gdy zachowanie oryginalnych klatek jest ważniejsze.
9. **Reprezentacja agentowa.** Sync groups, zakresy obecności kamer, cues utworu, osobne audio lock i video choices. Nierównoczesny materiał ma flagę `non_contemporaneous`, nie jest ukrytym kątem multicam.
10. **QA.** NOT_RUN: przegląd wszystkich bliskich kontaktów instrumentalnych i ust, pełny odsłuch mastera, koniec utworu i ambience; płynność przejść barwy oraz brak pustych kamer.
11. **Źródła.** [C09]: niezależność ustawień audio w multicam; [C02]: kursowy przykład multicam i późniejsza korekta. Etykieta materiału nierównoczesnego i testy wykonania: DERIVED.

## R12 — Showreel z czytelnym autorstwem

1. **Cel.** Pokazać określoną kompetencję przez skończone przykłady, nie tylko gęstość efektów.
2. **Potrzebne źródła.** Projekty z prawami do prezentacji, opis własnej roli, rendery dobrej jakości, ewentualne before/after i muzyka.
3. **Decyzje montażowe.** Wybierać po tym, co ujęcie udowadnia o warsztacie. Silny materiał bez wyjaśnienia roli może wprowadzać w błąd. Ocenić, czy kilka sekund wystarcza do dostrzeżenia pracy.
4. **Kolejność operacji.** Mapa kompetencji → weryfikacja praw i credits → selekcja reprezentatywna → grupowanie kontrastów → assembly → rytm → podpisy ról → finał z danymi → kontrola końcowa.
5. **Parametry/jednostki.** Długość wynika z odbiorcy i zadania. W przykładzie trzy kompetencje mają po dwa dowody; nie jest to norma. Napisy muszą pozostawać czytelne przy docelowym skalowaniu.
6. **Warianty.** Reel montażysty może pokazać fragment sceny z dialogiem; reel motion krótkie pętle; colorist porównania. Jeden ciągły fragment może być mocniejszy niż dziesięć półsekundowych przebitek.
7. **Błędy.** Całość wygląda jak zestaw cudzych kadrów; brak roli; powtórzenia tej samej umiejętności; efekt muzyczny maskuje słaby montaż sceny.
8. **Naprawa.** Dodać konkretne credits, usunąć powtórzenia, oddać czas najważniejszemu fragmentowi; przygotować osobny case study zamiast przeciążać główny reel.
9. **Reprezentacja agentowa.** Każdy asset ma `role_credit`, rights status, skill evidence i source project revision. Select bez potwierdzonego uprawnienia do portfolio pozostaje wyłączony.
10. **QA.** NOT_RUN: odbiorca nazywa pokazaną kompetencję i autorstwo; brak nieczytelnych credits, niespójnego koloru i przypadkowych watermarków. Deklaracje umiejętności odpowiadają pokazanemu materiałowi.
11. **Źródła.** [C03]: perspektywa odbiorcy zamiast kosztu powstania ujęcia; [C05]: cel i gatunek. Zastosowanie do portfolio jest DERIVED, nie wypowiedzią tych twórców o showreelach.

## R13 — Adaptacja filmu do social bez utraty sceny

1. **Cel.** Przenieść sens zaakceptowanego materiału do innego kadru i warunków odbioru.
2. **Potrzebne źródła.** Master i źródłowy projekt, brief kanału, aktualna specyfikacja odbiorcy, wersje napisów, elementy graficzne i prawa do nowego użycia.
3. **Decyzje montażowe.** Ocenić, gdzie centrum akcji wypada poza nowym kadrem, kiedy gest wymaga planu ogólnego i co musi być zrozumiałe bez dźwięku. Nie zakładać obowiązkowego hook/CTA.
4. **Kolejność operacji.** Obejrzeć scenę docelowego formatu → wybrać crop/fit/recompose → ustalić nową hierarchię napisów → selektywne skróty → dostroić audio → preview na rozmiarze telefonu → finalny QC.
5. **Parametry/jednostki.** Przykładowy wariant 1080×1920 jest tylko formatem projektu. Reframe w pikselach/znormalizowanych współrzędnych z określonym anchor. Safe zones brać z aktualnej specyfikacji publikacji, nie z jednej uniwersalnej tabeli.
6. **Warianty.** Split-screen pomaga pokazać dwie osoby, ale może utrudnić czytanie. Fit z tłem zachowa dowód działania. Czasem potrzebny jest odrębny montaż zamiast cropu.
7. **Błędy.** Automatyka śledzi twarz, gubiąc produkt; napisy zasłaniają dłonie; cięcia niszczą żart; każdy wyraz skacze bez uzasadnienia.
8. **Naprawa.** Ręcznie skorygować obszar uwagi, odtworzyć przygotowanie pointy, uprościć tekst, dodać osobny wariant kompozycji.
9. **Reprezentacja agentowa.** Wariant dziedziczy narrative locks, lecz ma własne transform keyframes, obszary ochronne i status QA. Zmiany źródła unieważniają tylko zależne zakresy; nie tworzyć drugiej kopii briefu.
10. **QA.** NOT_RUN: odtworzenie bez dźwięku i z dźwiękiem na docelowym rozmiarze; kontrola całego ruchu cropu, napisów i relacji przestrzennej. Brak automatycznego PASS po wykryciu twarzy w kadrze.
11. **Źródła.** [C05]: odmienność gatunków i odbiorców; [C04]: znaczenie prowadzenia uwagi. Zastosowanie do pionu i danych kadrowania: DERIVED. Aktualne reguły konkretnej platformy: Unknown do czasu briefu.

## R14 — Materiał o różnych FPS bez przypadkowej zmiany czasu

1. **Cel.** Złączyć źródła zachowując zamierzoną prędkość, synchronizację i kontrolowaną kadencję.
2. **Potrzebne źródła.** Oryginały, metadane FPS i PTS, dane audio, specyfikacja osi i odbiorcy. Obejrzeć ruch reprezentatywny, panoramę, dłonie i materiał ze światłami impulsowymi.
3. **Decyzje montażowe.** Dla każdego klipu wybrać: real-time czy świadomy slow motion. Różnica FPS sama nie określa intencji. Zapisać, czy preferujemy zachowanie klatek, płynność czy ograniczenie artefaktów.
4. **Kolejność operacji.** Probe → klasyfikacja CFR/VFR → zamrożenie timebase projektu → mapa czasu klipów → krótki test kilku metod → wybór na podstawie ruchu → montaż → pełny eksport próbny i sync check.
5. **Parametry/jednostki.** 50 fps → oś 25 fps real-time zachowuje 1 s jako 1 s; użycie wszystkich klatek po jednej daje 2 s i świadome 50% speed. `30000/1001` nie jest 30. Dźwięk ma osobną mapę czasu i sample rate.
6. **Warianty.** Archiwalny ruch można zachować w charakterystycznej kadencji. Dla wypowiedzi preferować real-time; dla sportowego detalu slow motion może ujawnić fazę działania.
7. **Błędy.** Interpretacja wszystkich kamer jako 25 fps zmienia tempo; powtarzanie klatek powoduje nierówny ruch; optical flow deformuje krawędzie; zaokrąglony FPS kumuluje drift.
8. **Naprawa.** Przywrócić dokładne rationals i source timestamps, rozdzielić klipy wymagające różnych metod, renderować trudne przejścia osobno; nie zmieniać źródłowych plików.
9. **Reprezentacja agentowa.** Jawne `source_rate`, `timeline_rate`, `time_map`, interpolation policy i audio policy. Backend, który nie wspiera wybranej mapy, zwraca brak możliwości, a nie samodzielnie inną metodę.
10. **QA.** NOT_RUN: frame count i czas zgodne z planem, sync na początku/środku/końcu, real-time ogląd panoram, kontrola klatek syntetycznych. Estetyczne artefakty nie są wykrywane samą zgodnością metadanych.
11. **Źródła.** [C11]: trzy rodzaje interpolacji; [C12]: właściwość czasu VFR. Przykłady liczbowe i reguła zachowania długości: DERIVED.

## R15 — Rampa prędkości, reverse i freeze jako świadoma narracja

1. **Cel.** Wyeksponować wybraną fazę działania albo zatrzymać obraz do objaśnienia, bez przypadkowej zmiany znaczenia.
2. **Potrzebne źródła.** Długie ujęcie z handles, oryginalne FPS/PTS, materiał o wystarczającej ostrości ruchu, dźwięk oddzielony logicznie od obrazu.
3. **Decyzje montażowe.** Obejrzeć pełny ruch i wyznaczyć moment, który widz ma odczytać. Zadać pytanie, czy wystarcza zwykły trim. Reverse nie może udawać realnego dowodu działania urządzenia.
4. **Kolejność operacji.** Wybrać source span → wskazać chronione fazy → zbudować prostą mapę prędkości → policzyć długość → wybrać interpolację → zdecydować o audio → render krytycznego fragmentu → ogląd i ewentualna redukcja efektu.
5. **Parametry/jednostki.** Prędkość `ds/dt`; freeze ma zero przyrostu source time. Przykład: 1 s źródła przy 0,5× zajmuje 2 s wyjścia. Rampa wymaga jawnej interpolacji prędkości i jej domeny, a nie dowolnego uśrednienia skrajnych wartości. Dla liniowego `speed(timeline_time)` przyrost czasu źródła jest całką trapezu. Granice wyjścia kwantowane raz do klatek.
6. **Warianty.** Produkt może użyć wolniejszego detalu bez audio synchronicznego; tutorial zatrzymanego kadru z narracją. Dokument dowodowy powinien wyraźnie ujawniać zmianę prędkości.
7. **Błędy.** Wskazana długość nie zgadza się z mapą, optical flow deformuje palce, powtórzony dźwięk kontaktu, niemożliwe handles.
8. **Naprawa.** Zmniejszyć zwolnienie, użyć sampling, wybrać ujęcie o wyższym FPS, przebudować dźwięk świadomie albo zrezygnować z efektu. Brak materiału nie uprawnia do syntezy poza zakresem.
9. **Reprezentacja agentowa.** Węzły czasu wyjście–źródło, typ interpolacji mapy, funkcja audio i przewidywany końcowy zakres. Reverse jest konceptualnie jawnym malejącym segmentem; validator takiego backendu nie zakłada globalnej monotoniczności mapy źródła. W obecnym FrameCut reverse jest unsupported — wymaga qualified backend albo przygotowanego derived asset, z osobnym QA.
10. **QA.** NOT_RUN: długość, pierwszy/ostatni source frame, brak przeskoków na węzłach, ręce/twarze/kontakty w zwolnieniu oraz pełny ogląd z dźwiękiem.
11. **Źródła.** [C11]: mechanizmy interpolacji; [C08]: opis celowych freeze frames w procesie fabularnym. Mapa matematyczna i testy: DERIVED.

## R16 — Dialog, room tone i muzyka w miksie montażowym

1. **Cel.** Uzyskać zrozumiały, naturalny dialog oraz kontrolowane tło, które wspiera scenę.
2. **Potrzebne źródła.** Izolowane mikrofony, room tone z tej przestrzeni, ambience, muzyka/stemy, reference obrazu i specyfikacja dźwięku. Każdy mikrofon ocenić w odsłuchu przed wyborem.
3. **Decyzje montażowe.** Rozróżnić zakłócenie od oddechu lub zawahania istotnego dla postaci. Wybrać podstawowy mikrofon; drugiego nie dodawać tylko dlatego, że istnieje. Muzyka powinna mieć funkcję, początek i zakończenie.
4. **Kolejność operacji.** Weryfikacja sync/routingu → wybór nagrań → montaż dialogu → wyrównanie clip gain → uzupełnienie tła i fades → oszczędna korekcja → automatyka/ducking → miks kategorii → pomiar gotowego eksportu → odsłuch.
5. **Parametry/jednostki.** Edycja audio w próbkach; gain w dB; fades w ms lub próbkach. Przykładowe 5–20 ms do zbadania klików nie jest presetem dla wszystkich łączeń. LUFS/dBTP według konkretnego delivery; brak uniwersalnego celu.
6. **Warianty.** Scena bez muzyki może być silniejsza. Przy zaszumionym dialogu lepsza umiarkowana redukcja niż gładki, sztuczny głos. W dubbingu obowiązuje inny zestaw źródeł i uzgodnień.
7. **Błędy.** Gate ucina końcówki, crossfade usuwa spółgłoskę, NR tworzy metaliczność, sumowane mikrofony dają filtr grzebieniowy, ducking pompuje.
8. **Naprawa.** Przywrócić transjenty, zmniejszyć obróbkę, wybrać właściwy mikrofon, ręcznie narysować automatykę fraz, zrekonstruować tło. Odróżnić błąd edycji od braku dobrego nagrania.
9. **Reprezentacja agentowa.** Mapa kanałów, source sample ranges, fades, gain envelopes i routing. ASR/VAD oznacza kandydatów, nie usuwa ich sam. Stemy mają dokładnie wspólny start/długość i jawnie opisaną obróbkę magistrali.
10. **QA.** NOT_RUN: pomiar i pełny odsłuch to osobne wyniki; mono/stereo, słuchawki i głośnik roboczy; brak clippingu, utraty słów i zmiany barwy na cięciach. Sprawdzić także zakodowany finalny plik.
11. **Źródła.** [C01]: katalog oficjalnych szkoleń Fairlight jako dalsza ścieżka nauki, nie potwierdzenie parametrów. [C06], [C07]: funkcja i ryzyko muzyki. Techniczna sekwencja miksu jest DERIVED i wymaga walidacji w torze audio.

## R17 — Finishing koloru, napisów i grafiki

1. **Cel.** Doprowadzić zaakceptowany montaż do spójnej, czytelnej i technicznie opisanej wersji.
2. **Potrzebne źródła.** Oryginały, aktualny lock, deklaracje kamer/color metadata, referencje estetyczne, zatwierdzony tekst, fonty z prawami oraz rendery grafiki z manifestem.
3. **Decyzje montażowe.** Ocenić sąsiadujące ujęcia w sekwencji. Rozdzielić naprawę interpretacji sygnału od stylizacji. Napisy mają ułatwiać rozumienie, grafika nie może zmienić czasu odczytu w sposób pomijający sens.
4. **Kolejność operacji.** Conform roboczy → weryfikacja interpretacji barwy → korekcja techniczna → matching → look → grafika i napisy → kontrola rozmiaru/alfy → eksport testowy → ogląd i pomiar → finalne wersje.
5. **Parametry/jednostki.** Osobne wejście/working/output color spaces; frame size i pixel aspect; alfa straight/premultiplied; napisy w czasach TL. Zmiana rozdzielczości musi aktualizować położenia tekstów i regiony ochronne.
6. **Warianty.** SDR i HDR wymagają osobnych sprawdzeń. Burn-in napisów i osobny plik napisów to różne dostawy. Celowo odmienna barwa wspomnienia nie musi być wyrównana do sceny teraźniejszej.
7. **Błędy.** Podwójny LUT, błędne poziomy, automat wyrównuje całkiem różne kadry, nieobsługiwany font zmienia layout, czarne brzegi premultiplied alpha.
8. **Naprawa.** Najpierw poprawić interpretację wejścia i compositing, potem grading; podmienić font tylko zgodnie z akceptacją; ponownie obejrzeć wszystkie zależne kadry, zachowując niezależne locks.
9. **Reprezentacja agentowa.** Każda transformacja ma input/output contract i parametry, render grafiki pin do rewizji/hasza, napisy do zatwierdzonej treści. Agent proponuje kolor; scope nie stanowi dowodu właściwego nastroju ani koloru produktu.
10. **QA.** NOT_RUN: scopes plus ogląd, cięcia między kamerami, skóra/produkt, clipping barwy, czytelność napisów, brak brakujących glifów, analiza artefaktów alfa oraz końcowych metadata. Brak skalibrowanego odsłuchu/monitora ujawnić.
11. **Źródła.** [C01]: rozdzielenie szkoleń Color, Fusion, Fairlight i edycji. [C04]: współpraca działów jako proces rozwijania filmu. Szczegółowy plan finishingu: DERIVED; specyfikacje normatywne uzupełnia część NLE/QA raportu.

## R18 — Końcowy conform, zmiana po picture lock i archiwum

1. **Cel.** Odtworzyć zaakceptowany montaż z poprawnych źródeł i przekazać finalną wersję z dowodem zgodności.
2. **Potrzebne źródła.** Zapisany lock i reference z TC, source manifest/hash, oryginały, EDL/XML/AAF/OTIO zależnie od toru, rendery efektów, miks/stemy, napisy i change list.
3. **Decyzje montażowe.** Najpierw rozstrzygnąć, która rewizja jest obowiązująca. Elementy niewymienialne trzeba wyrenderować albo odtworzyć ręcznie. Nie poprawiać narracji „przy okazji” conformu.
4. **Kolejność operacji.** Zapis checkpoint → import do kopii projektu → relink → porównanie liczby i granic zdarzeń → kontrola retimingu/transforms/tekstów → porównanie referencji → podpięcie miksu → eksport → techniczne QC → pełny ogląd/odsłuch → manifest i archiwum.
5. **Parametry/jednostki.** FPS wymierny, start TC i DF/NDF, source spans, TL spans oraz handles. Przykład poprawki po lock: usunięcie 12 klatek w połowie wymaga change list `delta=-12` dla zależnych zdarzeń, nowego reference i uzgodnienia z działami; nie wolno po prostu przesunąć starego miksu globalnie.
6. **Warianty.** Przy braku bezpiecznego round-trip użyć spłaszczonych renderów z handles i zachować wersję edytowalną osobno. Stały slot reklamy może wymagać kompensacji w innym miejscu zamiast zmiany długości.
7. **Błędy.** Relink do złego dubla o tej samej nazwie, o jedną klatkę inny Out, zgubiona prędkość, tekst renderowany innym fontem, miks z poprzedniej rewizji.
8. **Naprawa.** Odrzucić błędne dopasowanie, prześledzić source TC/hash; odtworzyć pojedynczy efekt albo dostarczyć zatwierdzony render. Zmiana po lock wraca jako nowa rewizja z unieważnieniem zależnych akceptacji.
9. **Reprezentacja agentowa.** Manifest każdej instancji: źródło, mapa czasu, oczekiwany obraz, zależności i checks. Operacje na bazowej rewizji muszą być atomowe; ponowienie nie dubluje elementów. Referencja, export i QA związane z tym samym revision/hash.
10. **QA.** NOT_RUN: frame count i długość; każda granica cięcia; początek/koniec efektu; A/V na całej długości; brak niezamierzonych gaps; subtitles; loudness/true peak według odbiorcy; color metadata; odtwarzalność; pełne realtime. Archiwum sprawdzić przez próbę otwarcia kopii projektu z manifestem.
11. **Źródła.** [C02]: oficjalny kurs rozróżnia edycję i delivery; [C05]: odwracalność eksperymentowania jako praktyka montażowa. Pełny conform/change-control jest DERIVED i nie dowodzi bezstratnego wsparcia dowolnego formatu wymiany.

## Mapa dalszej nauki wykorzystana przy recepturach

| Materiał | Umiejętność | Co rzeczywiście sprawdzono | Ćwiczenie własne  Ograniczenie |
|---|---|---|---|---|
| [C02], rozdział 3, s.149–195 | Wybór wykonania, continuity, J/L | Tekst PDF wybranych sekcji, bez uruchamiania lesson files | Dwie wersje sceny: mocna reakcja kontra idealna ciągłość; uzasadnić kompromis  Nie wykonano lekcji ani nie oceniono gry na jej filmach. |
| [C02], rozdział 4, s.239–242 | Multicam jako rough cut i refinements | Tekst PDF | Ta sama minuta rozmowy z trzema różnymi strategiami kątów  Bez uruchomienia multicam i bez kontroli lokalnej wydajności. |
| [C09] | Sync i rozdzielenie wyboru audio/video | Dokumentacja tekstowa Premiere | Dwa kąty, jeden master audio, trzy punkty testowe sync  UI dokumentowane; API i lokalny sync nieprzetestowane. |
| [C10] | Slip bez zmiany długości i pozycji | Dokumentacja tekstowa Premiere | Trafić gestem w akcent, utrzymując granice instancji  Brak sprawdzenia zachowania linked audio w konkretnym adapterze. |
| [C11] | Sampling/blending/optical flow | Dokumentacja tekstowa; bez porównania renderów | Trzy rendery tej samej dłoni; ocenić deformacje i kadencję  Opis producenta nie dowodzi jakości renderu. |
| [C03], [C05], [C06] | Cel, punkt widzenia i uczciwa kompresja | Teksty wypowiedzi montażystów | Usunąć 20% czasu, zachowując zastrzeżenia i charakter wypowiedzi  Opinie z określonej praktyki, bez uniwersalnych wag decyzji. |
| [C07], [C08], [C13] | Kiedy muzyka prowadzi, kiedy maskuje | Wywiady tekstowe, nie odsłuch materiałów | Dwie strategie sceny: obraz przed muzyką oraz muzyka jako założenie briefu  Nie odsłuchano przywołanych ścieżek; strategie mogą współistnieć. |
| [C01] | Wybór dalszego kursu edycji, koloru i dźwięku | Opisy katalogowe kursów, nie ich zawartość wideo | Dobrać moduł do wykrytej luki; nie liczyć obejrzenia opisu jako ukończenia kursu  Katalog kursów nie potwierdza szczegółowej treści lekcji wideo. |

W żadnej recepturze liczba cięć, średnia długość ujęcia, wynik ASR ani zgodny JSON nie są samodzielnym kryterium profesjonalnej jakości.