# Poprawiony plan storyboardu — oba formaty

Projekt: `SYNTHETIC-REPORT`, projekt źródłowy r3. Proponowana rewizja planu storyboardu: **B3**, do przeglądu. Zakres: 20 s, 25 kl./s, 9:16 i 16:9.

Zachowuję aktualną kolejność i długości scen: **intro 0–7 s → orders 7–11 s → conversion 11–16 s → cta 16–20 s**. Najważniejsza poprawka merytoryczna: konwersja liczona jako zamówienia / sesje **spadła z 4,0% do 3,6%, czyli o 0,4 punktu procentowego**. W pionowej scenie `orders` przewiduję większe `+12,5%`, zgodnie z F01, bez zmiany koloru.

To kompletny **tekstowy plan całej sekwencji na podstawie dostarczonych danych**, nie wykonane plansze wizualne ani zaakceptowany storyboard. Dostarczono wyłącznie `project.json` i `metrics.csv`; `rendered_media` ma wartość `null`. Nie ma obrazów plansz, filmu, dźwięku ani szczegółowego zapisu animacji. Znane parametry zachowuję; brakujących właściwości dotychczasowego wyglądu nie przedstawiam jako sprawdzonych.

## 1. Co pozostaje, co się zmienia

| Element | Decyzja B3 |
|---|---|
| Montaż | Obecny `current_sequence` r3 ma pierwszeństwo przed starszymi czasami B2. Bez nowych scen, cięć, przesunięć i zmiany 20 s. |
| Marka | Zachować `navy`, `cream` i Inter. Dokładne odcienie, grubości i dotychczasowy podział kolorów nie są zapisane; przejąć je z oryginalnej kompozycji, bez zgadywania wartości HEX. |
| Intro | Zachować dokładnie „Wyniki sklepu”. |
| Zamówienia | Zachować dokładnie „Zamówienia +12,5%”; wynik jest zgodny z CSV. Powiększenie dotyczy tylko `+12,5%` w 9:16. |
| Konwersja | W obu formatach zastąpić nieprawdziwe „Konwersja wzrosła o 0,4%” tekstem „Konwersja spadła o 0,4 p.p.”. |
| CTA | Zachować dokładnie „Zobacz wyniki”, w obu formatach i do końca sekwencji. |
| Ruch, przejścia, audio | Zachować istniejące rozwiązania, gdy zostaną udostępnione. Ten plan nie dodaje animacji, nowych przejść, lektora, muzyki ani SFX. Nie ustala ich nieznanych parametrów. |
| Kontekst liczb | Proponuję krótkie linie z miesiącami i wartościami źródłowymi w scenach danych. To jawne dodatki do przeglądu, nie wcześniej zaakceptowane copy. |

## 2. Dane i poprawne znaczenie komunikatu

Źródło: dostarczony statyczny `metrics.csv`, nagłówek w wierszu 1, September w wierszu 2, October w wierszu 3. Polskie etykiety miesięcy odpowiadają tym dwóm wartościom źródłowym. CSV nie podaje roku, daty aktualizacji, źródła analitycznego, filtrów ani kompletności miesięcy. Nie zakładam, że chodzi o rok bieżący lub pełne miesiące.

| Okres w CSV | Etykieta w planie | Sesje | Zamówienia | Zamówienia / sesje |
|---|---|---:|---:|---:|
| September | Wrzesień | 1000 | 40 | 40 / 1000 × 100% = 4,0% |
| October | Październik | 1250 | 45 | 45 / 1250 × 100% = 3,6% |

| ID twierdzenia | Wynik i wyprowadzenie | Weryfikacja i zależności |
|---|---|---|
| C-ORD | Wzrost liczby zamówień: `(45 − 40) / 40 × 100% = +12,5%`. Jednostka wejściowa: liczba zamówień; mianownik zmiany: 40 zamówień we wrześniu. | Zgodne z wierszami 2–3, kolumną `orders`. Copy O1–O3; scena `orders`; panele V-ORD-01 i H-ORD-01. |
| C-CONV | Wskaźniki: wrzesień 4,0%, październik 3,6%; różnica `3,6% − 4,0% = −0,4 p.p.`. Względnie: `(3,6 / 4,0 − 1) × 100% = −10%`. | Obliczenia zgodne z wierszami 2–3, kolumnami `orders` i `sessions`. Copy K1–K4; scena `conversion`; panele V-CON-01 i H-CON-01. Tekst B2 o wzroście jest sprzeczny z CSV. |

Wyświetlamy zmianę w **punktach procentowych**; względnego `−10%` nie dokładamy do kadru, żeby nie mieszać dwóch miar. „Konwersja” w tym planie oznacza wyłącznie iloraz zamówień i sesji z tego pliku. Definicji oficjalnego wskaźnika analitycznego nie dostarczono. Przyjmuję porównywalność sposobu liczenia obu wierszy jako założenie planu, nie wynik audytu analityki. Nie wyciągam wniosku o przyczynie zmiany, przychodzie ani skuteczności kampanii.

Obliczenia wykonano na dokładnych ułamkach. Prezentacja: jedna cyfra po przecinku, polski przecinek dziesiętny. Na tych danych zaokrąglenie nie zmienia wyniku. Sprawdzono dwa unikalne okresy, kompletność wymaganych komórek, liczby całkowite i dodatnie mianowniki. Nie stwierdzono duplikatów okresów. Nie imputowano danych i nie sumowano miesięcznych wskaźników.

## 3. Rozwiązanie zapisanej uwagi F01

> „Powiększ liczbę w tej scenie, bez zmiany koloru.”

| Pole | Rozpoznanie / korekta |
|---|---|
| Obejrzany materiał | Storyboard B2, `event_id: orders`, 9:16, 5 s, czyli klatka 125 przy 25 kl./s. W B2 scena zajmowała 4–10 s. |
| Obecny cel | Ten sam stabilny event `orders`, teraz 7–11 s, klatki `[175,275)`, panel V-ORD-01. Stare 5 s wypada teraz w `intro` — nie jest celem poprawki. |
| Zakres właściwości | Rozmiar liczby `+12,5%` w 9:16. Bez zmiany znaku, wartości, koloru, fontu, sceny ani czasu jej trwania. |
| Propozycja do obejrzenia | Rozmiar fontu liczby **120% jej dotychczasowej wartości**; etykieta „Zamówienia” pozostaje w dotychczasowym rozmiarze. To propozycja, bo zapis nie zawiera oryginalnych wielkości. Zachować bazowy punkt wyrównania; dopasować odstępy lokalnie, żeby uniknąć kolizji. |
| Granica przeniesienia czasu | Uwaga dotyczy całej sceny, a nie pojedynczej klatki ruchu. Nie wyliczam nowego dokładnego momentu przez dodanie 3 s ani przez proporcjonalne przeskalowanie skróconej sceny. Potwierdzono tożsamość eventu, nie mapowanie wewnętrznej animacji. |
| Drugi format | F01 nie zmienia wielkości liczby w 16:9. |
| Stan | Uwzględniona w planie B3; identyfikacja celu sprawdzona. Zmiana nie jest wdrożona w mediach ani wizualnie zweryfikowana. F01 pozostaje otwarta do sprawdzenia poprawionej planszy. |

Test późniejszej planszy: porównanie pionowego `orders` przed/po pokazuje większe `+12,5%`, ten sam kolor i Inter, kompletny znak `%`, brak kolizji z etykietami oraz niezmienione granice 7–11 s. Wariant poziomy nie dziedziczy powiększenia.

## 4. Dokładne teksty B3

Zapis poniżej określa treść, a łamanie wierszy opisują karty formatów. Identyfikatory są metadanymi planu, nie napisami w filmie.

| ID | Dokładny tekst | Status |
|---|---|---|
| I1 | Wyniki sklepu | Zachowany z B2 |
| O1 | Zamówienia +12,5% | Zachowany z B2; można rozdzielić wiersz po „Zamówienia” |
| O2 | Wrzesień: 40 | Proponowany kontekst z CSV |
| O3 | Październik: 45 | Proponowany kontekst z CSV |
| K1 | Konwersja spadła o 0,4 p.p. | Poprawka merytoryczna B3; do przeglądu |
| K2 | Wrzesień: 4,0% | Proponowany kontekst z CSV |
| K3 | Październik: 3,6% | Proponowany kontekst z CSV |
| K4 | Zamówienia / sesje | Proponowana definicja mianownika wskaźnika |
| A1 | Zobacz wyniki | Nienaruszalny lock CTA |

## 5. Pełna oś i mapa paneli

Czas pochodzi z `current_sequence` projektu r3. Przedziały są lewostronnie domknięte i prawostronnie otwarte: `[start,end)`. Łącznie **500 klatek**, od 0 do 499. Nie są to pomiary pliku wideo.

| Event | Czas | Klatki | Czas sceny | Panel 9:16 | Panel 16:9 |
|---|---|---|---:|---|---|
| intro | `[0,7)` s | `[0,175)` | 7 s | V-INT-01 | H-INT-01 |
| orders | `[7,11)` s | `[175,275)` | 4 s | V-ORD-01 | H-ORD-01 |
| conversion | `[11,16)` s | `[275,400)` | 5 s | V-CON-01 | H-CON-01 |
| cta | `[16,20)` s | `[400,500)` | 4 s | V-CTA-01 | H-CTA-01 |

Panel oznacza docelowy czytelny stan danej sceny, a przypisany przedział wskazuje pełny zakres jej odpowiedzialności. Liczba kart wynika z czterech znanych stanów treści w dwóch formatach. Nie jest zestawem równomiernie próbkowanych klatek. Do każdej karty należą wejście, odczyt i wyjście opisane poniżej. Jeśli źródłowy projekt zawiera dodatkowy reveal, istotną zmianę kompozycji lub przejście wewnątrz sceny, pełna plansza wizualna musi dostać odpowiednie dodatkowe panele w obrębie tego samego eventu; obecne pliki ich nie dokumentują.

W obu formatach kolejność czytania ma być taka sama: temat → wynik zamówień → kierunek zmiany konwersji → CTA. Nie wprowadzam wykresów o nieznanej skali, liczników pokazujących pośrednie nieprawdziwe wartości ani kodowania wyniku nowym kolorem. Dane przedstawiają konkretne pary etykiet i wartości.

## 6. Karty 9:16

Układ pionowy ma własne łamanie tekstu i kolejność elementów. Nie jest wycinkiem poziomej kompozycji. Opis rozmieszczenia stanowi propozycję tam, gdzie źródło nie zawiera geometrii. Przy odtworzeniu należy zachować istniejące kotwice, marginesy, tło i dekoracje; zmienić tylko obszar zależny od poprawki. Nie narzucam niepodanej rozdzielczości ani stref konkretnej platformy.

| Panel / pełny zakres | Kompozycja i exact copy | Wejście → odczyt → wyjście; ruch i dźwięk |
|---|---|---|
| **V-INT-01** · 0–7 s | Zachowany tytuł I1 „Wyniki sklepu”, pełny w obrębie pionowego kadru. Bez dodawania nowych danych i hasła wstępnego. Zachować dotychczasowe wyrównanie i wielkość. | Początek sceny w 0 s; zachować jej istniejące wejście. Czytelny tytuł ma pozostać głównym elementem. Wyjście do `orders` na granicy 7 s, bez zmiany rodzaju przejścia. Nie dopisywać ruchu ani cue audio; ich przebieg jest nieznany. |
| **V-ORD-01** · 7–11 s | O1 w układzie „Zamówienia” / „+12,5%”. Liczba większa o proponowane 20% względem poprzedniej pionowej wersji; ten sam kolor i Inter. O2 oraz O3 poniżej, w kolejności wrzesień → październik, każdy okres ze swoją wartością. To dodatkowe linie do akceptacji. | Wejście na granicy 7 s zachowuje istniejący charakter. Zmiana rozmiaru jest cechą całego stanu tekstu, nie nowym efektem pulsowania. Pełna liczba i obie etykiety muszą być czytelne w części przeznaczonej na odczyt. Wyjście na 11 s. Bez nowych akcentów dźwiękowych. |
| **V-CON-01** · 11–16 s | K1 można złamać jako „Konwersja spadła” / „o 0,4 p.p.”, bez skracania jednostki. Pod nim pionowo K2 i K3, dalej K4 „Zamówienia / sesje”. Pierwszeństwo ma kierunek zmiany i jednostka p.p.; definicja pozostaje czytelna. Użyć obecnych kolorów, bez nowej czerwieni. | Wejście na 11 s już z poprawnym komunikatem; błędne „wzrosła” nie może wystąpić w żadnym stanie, także animowanym. Jeśli istnieje animowana zmiana wartości, wymaga odtworzenia i osobnej kontroli zgodności z 4,0% → 3,6%; nie projektuję jej na podstawie samego JSON. Utrzymać czytelny stan, wyjście na 16 s. Sprawdzić ewentualną zależną narrację po jej udostępnieniu. |
| **V-CTA-01** · 16–20 s | Dokładne A1 „Zobacz wyniki”, z zachowaniem dotychczasowej hierarchii i miejsca. Bez dopisywania przycisku, adresu, logo lub obietnicy. | Wejście na 16 s, końcowa część na odczyt do ostatniej klatki 499. Nie skracać sceny ani dodawać końcowej planszy. Zachować istniejące zakończenie ruchu i audio; dokładny czas pełnej czytelności pozostaje do sprawdzenia na planszach/źródle. |

## 7. Karty 16:9

Wariant poziomy zachowuje wszystkie liczby i słowa. Wykorzystuje szerokość do porównania miesięcy obok siebie, bez rozciągania pionowej karty. To proponowane przełożenie dodatkowych etykiet; istniejącą kompozycję źródłową należy zachować poza niezbędnymi zmianami copy.

| Panel / pełny zakres | Kompozycja i exact copy | Wejście → odczyt → wyjście; ruch i dźwięk |
|---|---|---|
| **H-INT-01** · 0–7 s | I1 „Wyniki sklepu” w istniejącej poziomej kompozycji. Bez zmiany rozmiaru tytułu, wyrównania lub dodatkowych napisów. | Jak w obecnej scenie; początek 0 s, przejście do `orders` na 7 s. Nie wymyślać nowego ruchu ani audio. |
| **H-ORD-01** · 7–11 s | O1 „Zamówienia +12,5%” zachowuje dotychczasową wielkość. O2 i O3 można ułożyć poniżej obok siebie: wrzesień po lewej, październik po prawej, z równorzędnym formatowaniem. F01 nie skaluje tej wersji. | Zachować wejście na 7 s i wyjście na 11 s. Liczba oraz etykiety mają tworzyć jeden czytelny stan, bez dokładania osobnej sekwencji odkrywania danych. Audio bez zmian. |
| **H-CON-01** · 11–16 s | K1 „Konwersja spadła o 0,4 p.p.” w poziomym bloku tytułowym; K2 i K3 obok siebie, w tym samym porządku miesięcy co w `orders`. K4 „Zamówienia / sesje” w osobnym wierszu przy danych. Zachować Inter i dotychczasowe role kolorystyczne. | Wejście na 11 s z poprawionym kierunkiem zmiany, odczyt porównania, wyjście na 16 s. Skorygować każdą zależną warstwę tekstu, gdy będzie dostępna. Nie zachowywać błędnego komunikatu w przejściu lub narracji. Nie dodawać nowego cue. |
| **H-CTA-01** · 16–20 s | Dokładne A1 „Zobacz wyniki” w istniejącym poziomym układzie. Bez nowych treści. | Zachować czterosekundową scenę końcową i obecny sposób zakończenia. Ostatnia klatka to 499; plansza z CTA ma być sprawdzona także na końcu. Dokładny czytelny hold i końcówka audio nie zostały zmierzone. |

## 8. Ruch, czas odczytu i zależności

Granice scen i całkowity czas są ustalone. Wewnętrzne wejścia, wyjścia, nakładanie warstw i długości faktycznie czytelnych zatrzymań nie są zapisane. Nie utożsamiam więc 4 s sceny `orders` z 4 s pełnej czytelności tekstu. Pełne teksty należy przedstawić jednocześnie w istniejącym stanie odczytu; nowe etykiety nie otrzymują własnego czasu kosztem wyniku. Jeśli istniejący ruch pozostawia zbyt mało czasu na dodatkowe linie, należy wrócić z konkretną planszą do przeglądu, a nie samodzielnie wydłużać scenę lub zmieniać montaż.

F01 wymaga później sprawdzenia lokalnej geometrii V-ORD-01 i jego wejścia/wyjścia, bez zmiany sąsiedniego intro. Korekta C-CONV obejmuje oba warianty `conversion`, wszystkie ich warstwy tekstowe, ewentualny wykres, animowaną wartość, napisy i lektora — jeśli takie elementy istnieją. Nie potwierdzono ich obecności. Nie ma podstaw do zmiany audio w pozostałych scenach.

## 9. Checkpoint do wznowienia

Ten dokument jest jedynym zapisanym wynikiem pracy. `project.json` i CSV pozostają niezmienione; poniższy checkpoint nie jest zastosowaną operacją runtime.

| Pole | Stan roboczy |
|---|---|
| Projekt bazowy | `SYNTHETIC-REPORT`, r3 |
| Poprzedni storyboard | B2 ma w pliku `accepted: true`; nie ma osobnego zapisu wiadomości potwierdzającej. B2 zawiera starsze czasy i błędną konwersję. |
| Bieżąca propozycja | B3 — plan tekstowy, `awaiting_feedback`, oba formaty, cała oś `[0,500)`. |
| Mapa paneli | 9:16: V-INT-01 → V-ORD-01 → V-CON-01 → V-CTA-01; 16:9: H-INT-01 → H-ORD-01 → H-CON-01 → H-CTA-01. |
| Plansze / ścieżki obrazów | Nie utworzono. Brak podglądów źródłowych i szczegółów kompozycji; ten zakres obejmował plan. |
| Feedback | F01 uwzględniona w planie, poprawne powiązanie eventu sprawdzone; wdrożenie i ocena wizualna oczekują. |
| Akceptacja B3 | Brak. Akceptacja B2 nie przenosi się na zmienione czasy, copy ani poprawiony pionowy rozmiar. |
| Następny krok | Przegląd tego planu: powiększenia w V-ORD-01, poprawnego copy konwersji oraz dodatkowych etykiet źródłowych. Następnie komplet rzeczywistych plansz obu formatów z zachowaniem oryginalnego wyglądu i ich akceptacja przed produkcją filmu. |

## 10. Faktycznie wykonana kontrola

Kryteria przyjęte przed opracowaniem: zgodność liczb z CSV; prawidłowe rozróżnienie procentów i punktów procentowych; F01 przypięta do aktualnego `orders` wyłącznie w 9:16; pełne pokrycie 20 s obu formatów; zachowanie marki i CTA; oddzielenie planu od wykonanego i zaakceptowanego materiału.

| Kontrola | Wynik i zakres dowodu |
|---|---|
| Pliki wejściowe | Odczytano JSON i CSV. Lista dostarczonych plików zawiera tylko te dwa pliki. |
| Dane | Kontrola programowa: 2 unikalne i kompletne wiersze, prawidłowe mianowniki, dokładne obliczenia `+12,5%`, `4,0%`, `3,6%`, `−0,4 p.p.` i względnie `−10%`. PASS dla zgodności z plikiem, nie audyt źródła biznesowego. |
| Montaż | Kontrola programowa: 4 sąsiadujące przedziały, bez luk i nakładania, koniec w 20 s, 500 klatek. Plan używa obecnych czasów, nie czasów B2. PASS. |
| F01 | Kontrola programowa powiązania `event_id`: stare 5 s należało do `orders`; aktualne 5 s należy do `intro`. Korekta wskazuje `orders` 7–11 s i format 9:16. PASS dla planu. |
| Copy i oba formaty | Przegląd tekstowego planu: zachowano „Wyniki sklepu”, „Zamówienia +12,5%” i „Zobacz wyniki”; korekta konwersji występuje w obu kartach, wzrost rozmiaru tylko w pionie. PASS dla specyfikacji. |
| Pokrycie | Osiem kart obejmuje wszystkie cztery znane sceny obu formatów, wraz z zakończeniem. Dodatkowe stany nieudokumentowanej animacji wymagają źródła. PASS dla kompletności planu względem dostarczonego opisu. |
| Obraz, ruch, audio | **Nie sprawdzono**: nie dostarczono mediów. Czytelność w pikselach, rzeczywiste kolory, kolizje, animacje, hold, odsłuch i zgodność wykonania pozostają niezweryfikowane. |

Jedna ograniczona pętla kontroli planu; wynik `stop_sufficient` dla zamówionego dokumentu. Nie oznacza to zgody na render ani wizualnego PASS. Nie wykonywano renderu, nie uruchamiano providerów, niczego nie wysłano ani nie opublikowano.

Identyfikacja źródeł, SHA-256:

- `project.json`: `d05f320d18139e2dfda85c22679e617a47abc99501f8816418c8a657a4d8a088`
- `metrics.csv`: `b68d4608390790674b29794b21f42394824f017d7576a673d46dd8ae18046ba8`
