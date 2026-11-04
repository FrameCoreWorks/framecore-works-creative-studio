# Audyt i projekt rozwoju nauki w FrameCore Works Creative Studio

Stan źródła: `d2dbc1855e0552fbe753b69eeeb222faa282f016`. Data audytu: 4 listopada 2026. Charakter dokumentu: analiza i propozycja, bez wdrożenia. Nie przeprowadzono nowego testu zainstalowanego hosta ani badania z uczniami. Skuteczność dydaktyczna: **Unknown**.

Najważniejszy wynik: istniejący moduł ma większość potrzebnych mechanizmów mentoringu. Priorytetem jest sprawdzenie ich działania w pełnym cyklu, poprawa niespójnych scenariuszy testowych oraz kalibracja zadań i ocen. Tworzenie drugiego nauczyciela, osobnej pamięci lub nowego skilla do każdej kompetencji zwiększyłoby złożoność bez rozwiązywania wykazanych problemów.

## 1. Werdykt i granice dowodów

**Zgodność ze specyfikacją źródłową:** dobra w głównej metodzie i kontrakcie stanu; niepełna w aktualnej dokumentacji i rubrykach ewaluacji. Potwierdzono sprzeczne oczekiwania LM01, przestarzały opis menu i zbyt słaby scorer W06. Nie wykazano awarii bieżącej rozmowy modelu.

**Jakość zadania dydaktycznego:** sensowna podstawa, ale bez udokumentowanej walidacji całej pętli nauki oraz wyników samodzielnej pracy ludzi. Kontrole źródłowe chronią obecność reguł, właścicieli i granic uprawnień. Nie rozstrzygają, czy feedback jest trafny albo czy uczeń przeniósł umiejętność na nowy brief.

Przeczytano w całości 30 plików, częściowo 25 plików; kolejne 510 plików objęto wyłącznie leksykalnym skanem source guard. Ten ostatni licznik nie oznacza merytorycznej oceny 510 plików. Szczegóły i mianowniki są w [Pokrycie-2986-plikow.csv](Pokrycie-2986-plikow.csv). Rozwiązano zadania trzech lekcji Teacher Studio i sprawdzono 12 aktywności, klucze oraz sumy proponowanych czasów. Nie znaleziono błędu tych przykładów; nie badano ich rzeczywistej długości, czytelności wydruku lub skuteczności w klasie.

## 2. Co już jest i powinno pozostać

| Element | Rzeczywista implementacja | Ocena |
|---|---|---|
| Rozdzielenie intencji | `interaction_mode` learning/creation odrębne od Quick/Deep | Zachować. Stworzenie karty pracy jest creation; uczenie się jej projektowania jest learning. |
| Diagnoza wejścia | Maksymalnie sześć potrzebnych pytań, jedno na odpowiedź; znane dane pomijane | Zachować. Nie zamieniać sześciu w obowiązkową ankietę. |
| Diagnostyka praktyczna | Pierwsza mała próba w lekcji, bez dodatkowego egzaminu, z możliwością pominięcia | Zachować; dodać wykonane ślady zachowania. |
| Plan | Cel samodzielny, moduły, podstawy, powód kolejności, ćwiczenia, kryteria, koszty i droga bez renderu | Zachować i kalibrować przykłady, nie budować nowego planera. |
| Cykl lekcji | Cel, wyjaśnienie, przykład, próba, feedback, korekta i sprawdzenie rozumienia | Zachować; najważniejsza brakująca warstwa to dowód wieloturowego wykonania. |
| Pomoc | `none`, `hint`, `guided`, `partial_example`, `worked_example`; najsilniejsza pomoc per kryterium | Zachować. Prośba o pełne wyjaśnienie nie może skutkować wymuszoną zgadywanką. |
| Kompetencja | `Unknown`, `supported`, `independent_familiar`, `independent_transfer`; oddzielna jakość pracy i ukończenie lekcji | Mocny element. Są to obserwacje konkretnego zadania, nie trwała etykieta osoby. |
| Utrwalenie | `review_queue`, jedna `pending_practice`, retrieval i transfer przy odpowiednim kontekście | Zachować. Nie dodawać automatycznych przypomnień ani wyniku za upływ czasu. |
| Feedback | Kryterium, ślad w pracy, mocna strona, 1–2 poprawki; rozdzielenie craft/instruction/reference/generator/tool/Unknown | Zachować. Awaria generacji nie dowodzi błędu ucznia. |
| Projekt przewodni | `learning_project` z rewizją, zależnościami, chronionymi decyzjami i kolejną czynnością | Zachować jako opcję; pojedyncza umiejętność nie musi stawać się kampanią. |
| Postęp | Jedno `learning_context` we wspólnym Project State i przenośna karta | Zachować. Pasted card jest deklaracją źródła, a nie nowym dowodem kompetencji. |
| Dostęp bez opłat | Każda domena ma ćwiczenie bez renderu; wykonanie wymaga osobnego zakresu | Zachować. Wspomnienie narzędzia nie uruchamia generacji. |
| Dostępność | Tekstowy odpowiednik interakcji, znaczenie niezależne od koloru, opis ilustracji; Teacher pozwala zmienić formę odpowiedzi | Zachować, doprecyzować przenoszenie deklarowanych ograniczeń przez kartę. |
| Teacher Studio | Osobny profil autorskich materiałów, trzy pełne lekcje, 12 mikroaktywności, szablon pakietu i dokumentacji | Zachować w creation, bez nowego agenta i bez automatycznego oceniania identyfikowalnych uczniów. |

`taste-learning` dotyczy preferencji twórczych, a `workflow-self-improvement` retrospektyw procesu. Nie należy ich zaliczać do historii opanowania kompetencji ucznia. Mają odrębne źródła dowodów i warunki zapisu.

## 3. Ustalenia wymagające działania

Pełne dowody, lokalizacje, reprodukcje i odbiór zawiera [Rejestr-ustalen.md](Rejestr-ustalen.md).

| ID | Typ | Priorytet | Działanie |
|---|---|---|---|
| LEARN-01 | Potwierdzona wada specyfikacji testu | P2 | Poprawić rubrykę LM01: pięć opcji, łączny obszar i tempo, poprawna semantyka tokenu 3. |
| LEARN-02 | Potwierdzona luka testu | P2 | W06 musi odrzucać dwa pytania oraz zakończenie kursu bez próby. Oba kontrprzykłady obecnie przechodzą. |
| LEARN-03 | Drift dokumentacji | P3 | Usunąć nieaktualny skrót motion, ujednolicić liczbę scenariuszy i warunek research disclosure. |
| LEARN-04 | Luka dowodowa | P2 | Wykonać pełne rozmowy nauki, a dopiero później pilotaż skuteczności. |
| LEARN-05 | Niepełna projekcja kontraktu | P2 | Utrzymać dostępność, język i formę dowodu w istniejących constraints karty. |
| LEARN-06 | Luka dowodowa Teacher Studio | P2 | Weryfikować odpowiedzi, kompletność i adaptacje, obok samego routingu. |
| LEARN-07 | Propozycja rozwoju | P3 | Dodać kilka skalibrowanych sekwencji zadań, a nie drugi system mentoringu. |

Lokalny probe `validateLearningMode` na izolowanej kopii zwrócił `errors: []`. Trzy celowe mutacje, sprzeczna rubryka LM19, nieprawidłowy enum w karcie oraz zastąpienie dokumentacji błędną deklaracją mastery, również nie zostały wykryte przez ten guard. To nie zarzut, że regex powinien oceniać pedagogikę. To dowód, że potrzebna jest osobna warstwa sprawdzająca relacje między kontraktami i obserwowane zachowanie. Nie uruchamiano pełnego `learning-mode.test.mjs`; jego treść została przeczytana. Pełne kontrole pakietu należą do nadrzędnego audytu.

## 4. Podstawa dydaktyczna i jej ograniczenia

Źródła odczytano 4 listopada 2026. Szczegóły zakresu odczytu znajdują się w [evidence/learning/sources.json](evidence/learning/sources.json).

1. [IES/WWC, 2007](https://ies.ed.gov/ncee/wwc/PracticeGuide/1): powroty do materiału, przeplatanie przykładów i samodzielnych prób, aktywne przypominanie oraz pytania wymagające wyjaśnienia mają uzasadnienie badawcze, z różną siłą dowodów. To uzasadnia zachowanie obecnego cyklu; nie wyznacza optymalnej długości lekcji Studio ani efektu w twórczości.
2. [CAST UDL 3.0](https://udlguidelines.cast.org/): projektować wokół celu i bariery dostępu, dopuszczać odpowiednie formy prezentacji i odpowiedzi, stosować stopniowane wsparcie. Nie przypisywać uczniowi sztywnego stylu uczenia się. Deklaracja zgodności instrukcji nie dowodzi dostępności rzeczywistego UI.
3. [Bastani i współautorzy](https://hamsabastani.github.io/education_llm.pdf): wynik zadania z pomocą AI i późniejsza praca bez pomocy są różnymi obserwacjami. Badanie matematyki motywuje test niezależnej decyzji; nie dowodzi skuteczności określonego kursu kreatywnego ani długotrwałego transferu. Odczytano abstrakt i początkowe sekcje, nie pełne 68 stron.
4. [Harvard Project Zero](https://pz.harvard.edu/resources/eight-habits-of-mind) i [autorzy Studio Thinking](https://www.studiothinking.org/the-framework.html): edukacja artystyczna obejmuje również obserwację, refleksję, ekspresję i eksperymentowanie. Projektowy wniosek dla Studio: poza poprawnym promptem oceniać wybór, uzasadnienie, krytykę i rewizję. Nie importować ich ośmiu kategorii jako nowej konkurencyjnej taksonomii.
5. [UNESCO](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research): podtrzymać sprawczość człowieka, minimalizację danych oraz walidację w realnym kontekście. To wskazówki projektowe, nie potwierdzenie zgodności z prawem lub podstawą programową.

Zaproponowane niżej progi, próbki i kolejność prac są decyzjami projektowymi audytu. Źródła nie stanowią walidacji tych konkretnych parametrów.

## 5. Minimalna architektura rozwoju

Właściciel pozostaje `workflow-orchestrator`, warsztat pozostaje u istniejących specjalistów, a stan w `learning_context`. Utrzymać progressive disclosure: główny entrypoint prowadzi do metody i wybranej domeny, bez ładowania wszystkich 14 naraz. Materiały klasyfikować jako wzorce do adaptacji, nie obowiązkową instrukcję produkcji.

Kolejność rozbudowy istniejących komponentów:

| Komponent | Co doprecyzować | Czego nie potrzeba |
|---|---|---|
| `learning-domains.json` | Powiązanie ćwiczenia z jego własnymi kryteriami, przykładowy warunek wstępny i zmiana kontekstu | Nowych owner IDs i encyklopedii każdego programu |
| `learning-plan.template.md` | Widoczny rezultat każdej próby, miejsce sprawdzenia bez pomocy, zakres niezbadany | Sztywnego kursu dla wszystkich i obietnic terminu mastery |
| `learning-progress.template.md` | Przenoszenie constraints, pochodzenie i rewizja próby, aktualna luka obok wcześniejszego sukcesu | Drugiego rejestru postępu, zbierania danych zdrowotnych |
| Metoda mentoringu | Krótka reguła rozróżnienia błędu technicznego, niedopasowania do celu i uzasadnionego wyboru artystycznego | Rozbudowanej punktacji osobowości lub talentu |
| Istniejące examples/fixtures | 2–3 kompletne kreatywne sekwencje do prób zachowania | Masowego kopiowania upstream i jego dawnych tras |
| Evals | Pełne tury, artefakty, negatywne przypadki i ocena dowodów | Następnych testów, które sprawdzają tylko występowanie słów |

Nie trzeba od razu wymagać JSON Schema dla każdej rozmowy. Najpierw ustalić semantykę na konkretnych kartach. Lekki lokalny checker prywatnych zapisów jest uzasadniony, jeśli rzeczywiste roundtrip tests ujawnią błędy. Musi tolerować starsze karty i nie nadawać statusu kompetencji bez oceny materiału.

## 6. Mapa kompetencji: wykorzystanie 14 istniejących domen

Poniższe zależności są propozycją projektową, nie deklaracją istniejącego grafu w repo. Każda ścieżka może zacząć od dostarczonej pracy i ominąć opanowane podstawy.

| Domena | Obserwowalna czynność | Przydatna podstawa | Dowód i przykład transferu |
|---|---|---|---|
| `static_graphics` | Tworzy dwa różne układy przekazujące cel | Intencja i odbiorca | Szkice z uzasadnieniem; inny temat przy tym samym formacie |
| `typography_layout` | Ustala kolejność czytania bez utraty exact copy | Hierarchia informacji | Układ trzech tekstów; węższy format lub dłuższy tytuł |
| `story_screenplay` | Buduje scenę z konfliktem i zmianą | Cel postaci, przyczyna i skutek | Krótka scena; inna relacja przy tym samym konflikcie |
| `performance` | Zapisuje obserwowalne działanie realizujące intencję | Cel sceny | Dwie interpretacje tej samej kwestii; ograniczenie gestu |
| `character_reference` | Rozdziela widoczne fakty, niewiadome i potrzebne referencje | Źródło prawdy i role odniesień | Opis pakietu; brakujący profil innej postaci |
| `storyboard_sequence` | Łączy stany wejścia i wyjścia ujęć | Zależność działania i rekwizytu | Trzy shot cards; zmiana rekwizytu i osi |
| `cinematography` | Dobiera kadr i kierunek światła do informacji | Cel obrazu i relacje przestrzenne | Szkic lub opis; nowy obiekt i ograniczona przestrzeń |
| `commercial_video` | Buduje demonstrację bez zmyślonych właściwości | Brief, prawda produktu, kolejność | Plan 15 sekund; mniej ujęć przy tym samym dowodzie |
| `music_video` | Łączy motyw z emocjonalnym przebiegiem | Funkcja sceny, rytm narracji | Opis motywu; zmiana znaczenia bez nowych dekoracji |
| `copy_voice` | Zmienia ton przy zachowaniu faktów | Odbiorca, cel, copy locks | Dwa teksty; inna publiczność bez dopisania obietnic |
| `prompting` | Mapuje decyzje na instrukcję i test wyniku | Cel, referencje, ograniczenia | Prompt oraz uzasadnienie; inna forma briefu bez zmiany faktów |
| `audio_music` | Przypisuje dźwiękom funkcję i moment | Akcja, priorytet informacji | Cue map; mniej warstw. Odsłuch oceniać tylko z audio. |
| `editing_motion` | Uzasadnia cięcie, hold, przejście i czytelność | Czas, hierarchia, rytm | Timeline; inny czas trwania. Płynność tylko z ruchem. |
| `campaign_workflow` | Spina cele, materiały, prawa, wersje i QA | Brief, odbiorca, artefakty | Macierz kampanii; nowy kanał z innymi ograniczeniami |

Research, prawa, QA i budżet pozostają przekrojowe. Dobra odpowiedź tekstowa nie wystarcza do uznania praktycznej pracy z kamerą, odsłuchu, płynności animacji ani przygotowania do druku. W planie oznaczyć oddzielnie umiejętność planowania i faktycznie obejrzany lub wykonany rezultat.

## 7. Format jednej lekcji i operacyjne kryteria przejścia

Lekcja powinna ujawniać uczniowi tylko potrzebną część; szczegółowy zapis jest wewnętrznym widokiem istniejącego stanu.

| Część | Zawartość |
|---|---|
| Cel | Jedna czynność, którą można zobaczyć w odpowiedzi lub artefakcie |
| Zadanie | Kompletny krótki brief, dane, ograniczenia i forma oddania |
| Kryteria | 2–4 widoczne własności pracy; każde sprawdzalne w tym zadaniu |
| Wyjaśnienie/przykład | Jeden mechanizm; przy diagnostyce przykład nie zdradza rozwiązania |
| Próba | Jedna oczekująca decyzja lub praca; brak zmyślonej odpowiedzi |
| Ocena | Kryterium, konkretna obserwacja, co działa, priorytet poprawki |
| Wsparcie | Najmniejsza użyteczna pomoc, z zapisem najsilniejszej udzielonej |
| Rewizja | Ten sam istotny problem przy zachowaniu poprawnych decyzji |
| Transfer | Nowy kontekst bez rozwiązania; nie równolegle do oczekującej poprawki |
| Zapis | Rewizja pracy, pochodzenie, wynik kryteriów i kolejny krok |

Przejście dalej nie wymaga ogólnego progu procentowego. Jeśli uczeń wykonał kryterium z pomocą, może poznawać następny moduł, lecz obecny dowód pozostaje `supported`. Dla niezależnego wyniku potrzebna jest nowa próba bez rozwiązania ani kierującej podpowiedzi. `independent_transfer` wymaga znaczącej zmiany warunku, nie samej nazwy produktu. Jedna próba nie jest trwałą certyfikacją.

Nie kasować wcześniejszej udanej obserwacji po niepowodzeniu. Obok niej przechować datę/revizję i bieżącą lukę. Przy planowaniu następnego zadania pierwszeństwo ma aktualny obserwowalny problem, aby stary sukces nie ukrywał potrzeby powtórki. Nie dodawać automatycznego starzenia punktów ani rankingu uczniów.

## 8. Przykład ścieżki: od briefu do spójnej mikrorealizacji

Założenia projektowe: osoba początkująca, 20–30 minut na spotkanie, telefon lub papier, bez dodatkowych kosztów; tematem jest fikcyjne lokalne spotkanie czytelnicze. Ścieżka ma sześć modułów, ale nie obiecuje ukończenia w sześciu sesjach. Realizacja obrazu/wideo pozostaje opcjonalnym osobnym działaniem.

| Moduł | Ćwiczenie i rezultat | Dowód przejścia | Dalsze wykorzystanie |
|---|---|---|---|
| 1. Intencja | Jedno zdanie: komu, co i dlaczego komunikujemy | Oddziela fakt briefu od założenia, nazywa odbiorcę i cel | To samo zdanie steruje plakatem i sekwencją |
| 2. Hierarchia | Dwa szkice tekstów „Wspólne czytanie”, „Sobota 12:00”, „Wstęp wolny” | Copy bez zmian, zamierzona pierwsza informacja, widoczne różnice ważności | Wybrany szkic staje się wersją r1 |
| 3. Mechanizm wizualny | Dwa różne pomysły pokazania wymiany książki | Różni je relacja/akcja, nie tylko kolor | Jeden wybrany mechanizm, uzasadnienie i odrzucony wariant |
| 4. Sekwencja | Trzy opisane ujęcia przekazania zamkniętej książki | Spójny rekwizyt i stan rąk, każde ujęcie wnosi informację | Shot cards, bez twierdzenia o sprawdzonej płynności |
| 5. Instrukcja i QA | Prompt lub opis realizacji oraz lista sprawdzeń | Każde ograniczenie ma źródło i sprawdzalne kryterium | Brief, copy i referencje powiązane z rewizją |
| 6. Transfer | Inny odbiorca i krótszy format z nowymi danymi | Uzasadniona adaptacja bez kopiowania poprzedniego rozwiązania | Niezależne obserwacje per kryterium i potrzeby praktyki |

Trzy warianty trudności dotyczą tego samego celu, nie etykiety osoby:

- Początkujący wybiera jedną z trzech informacji jako pierwszą i uzasadnia. Pozostałe zmienne są ograniczone.
- Osoba średniozaawansowana projektuje dwie hierarchie dla różnych odbiorców, zachowując wszystkie teksty.
- Zaawansowany broni świadomej nieoczywistej hierarchii wobec briefu, pokazuje kompromis i proponuje test czytelności. Nie musi wybrać estetyki mentora.

### Przykład feedbacku bez wykonywania zadania za ucznia

Próba ucznia: „Wszystkie trzy napisy będą tak samo duże i czerwone”. Kryterium: wskazana informacja ma być pierwszą odczytaną. Obserwacja: opis nie różnicuje żadnego napisu. Mentor zachowuje poprawne exact copy, wskazuje jedną trudność i pyta wyłącznie o priorytet informacji. Nie podaje od razu kompletnego layoutu.

Jeśli uczeń wybierze tytuł, następna próba polega na zmianie jednego parametru względem daty i CTA. To próba wspierana. Dopiero nowy brief, na przykład czytelny plakat akcji porządkowej o trzech innych tekstach, pozwala sprawdzić decyzję bez podpowiedzi. Ocena nie wymaga identycznego układu jak przykład mentora. Taka sekwencja jest propozycją testową, nie wykonanym dialogiem uczącego się.

## 9. Dostępność, język i powrót do pracy

Nie pytać o diagnozę. Zapisywać tylko deklarowaną barierę i użyteczną adaptację: krótsze bloki, wersja do odsłuchania, tekst zamiast obrazu, większy kontrast, brak dźwięku lub możliwość odpowiedzi głosowej, jeśli faktycznie dostępna. Preferencja formy nie jest dowodem, że dana osoba uczy się wyłącznie wizualnie lub słuchowo.

Telefon: jedna mała praca na turę, listy zamiast szerokiej tabeli tam, gdzie poprawia to użycie, krótki checkpoint dopiero przy pauzie. Ćwiczenie musi być wykonalne bez wygodnego przełączania kilkunastu plików. Nie uznawać miniatury w rozmowie za wystarczającą do oceny detalu.

Polski opis z angielskim terminem: objaśnić raz znaczenie w kontekście, np. `hold` jako czas utrzymania informacji, potem stosować konsekwentnie. Odpowiedź ucznia może używać własnych słów. Nie punktować anglicyzmu, jeśli celem jest właściwa decyzja montażowa.

Resume test powinien zachować: bieżącą pracę i rewizję, następną akcję, najsilniejszą pomoc, dowody z ich pochodzeniem, jedno oczekujące zadanie oraz constraints. Nieobecny obraz nadal jest nieobecny. Deklaracja „zrobiłem sam” w karcie nie staje się obserwacją mentora. Wcześniejsza zgoda na lekcję nie staje się zgodą na render, upload lub płatny provider.

## 10. Teacher Studio: osobny plan jakości

Trzy oryginalne lekcje są kompletne tekstowo: instrukcje 7–9 lat, wnioskowanie z tabeli 9–12 i decyzje 14–17. Zawierają źródła zadań, klucze, alternatywy, wsparcie, rozszerzenie i jawny brak testu klasowego. To rzeczywisty zasób do zachowania. Wiek jest orientacyjny, a dopasowanie zależy od rzeczywistych podstaw.

Następna ewaluacja powinna adaptować treść zamiast wyłącznie sprawdzać odczyt profilu. Przykład: zmienić budżet i czas w lekcji decyzji, wymagać przeliczenia dopuszczalnych opcji oraz klucza; usunąć jedną informację z tabeli i sprawdzić, czy system ujawni brak. Dla zadania otwartego wymagać co najmniej dwóch różnych obronionych rozwiązań. W PDF/DOCX/PPTX sprawdzić rzeczywiste oddzielenie klucza, polskie znaki, łamanie strony i przestrzeń na odpowiedzi.

Nie dodawać obowiązkowo alignment do krajowego programu. Jeśli użytkownik go prosi, wymagane są jurysdykcja, etap, wersja dokumentu, odczytany oficjalny zapis oraz mapowanie wymaganie→zadanie→sprawdzenie. Treść polska i zgodny temat nie dowodzą takiego alignment. Niewykonane sprawdzenie eksportu i niewykonane zajęcia pozostają `NOT_RUN`.

## 11. Protokół testów przed pilotażem

Zachować niezależność testera: otrzymuje surowe zadanie i potrzebne artefakty, bez listy spodziewanych błędów i bez proponowanej poprawki. Rubrykę odbioru ma osobny recenzent. Trzy powtórzenia kluczowej niedeterministycznej próby są rozsądną próbką roboczą, nie statystycznym dowodem niezawodności. Liczba realnie wykonanych powtórzeń musi trafić do raportu.

| Próba | Aktywacja / kontrprzypadek / brak danych | Warunek odbioru |
|---|---|---|
| Wejście | Uczyć się plakatów / zrobić plakat / „nie wiem” | Właściwa intencja, jedno pytanie, brak wymuszonych danych |
| Pełny brief | Początkujący, papier, 15 min / plan-only / brak narzędzi | Plan i jedna próba albo sam plan zgodnie z prośbą |
| Feedback | Faktycznie błędna hierarchia / celowa eksperymentalna hierarchia / brak obrazu | Ocenia dostępny dowód, nie narzuca gustu, przyczyna Unknown gdzie trzeba |
| Pomoc | Prośba o hint / pełne wyjaśnienie / prośba o gotowy rezultat | Jedna pomoc, odpowiednie pozostanie lub zmiana trybu, brak fikcyjnej samodzielności |
| Transfer | Udana próba / kopiowanie rozwiązania / nieweryfikowalna deklaracja | Przejście stanu tylko dla konkretnego kryterium z dowodem |
| Resume | Pełna karta / stara karta / niedostępny plik | Zachowuje constraints, pomoc, rewizję i pending task bez odtwarzania wygasłych menu |
| Zaawansowany | Nowe ograniczenie / dodatkowy początkujący wykład / sprzeczne kryteria | Wyzwanie problemowe, nie więcej prozy; konflikt jawny |
| Teacher | Karta z kluczem / prośba o naukę tworzenia karty / brak danych do zadania | Właściwy tryb, kompletny materiał, poprawny klucz |
| Uprawnienia | Lekcja audio bez kont / osobny render request / skopiowana stara zgoda | Brak wykonania z samej nauki, zachowanie obecnej granicy |

Dla każdej próby zapisać: commit, wersję, host, dostępny model/ustawienie lub Unknown, wejścia, faktycznie udostępnione pliki, narzędzia, pełne odpowiedzi, przejścia stanu, kryteria i wynik. Działający source guard, rzeczywiste wykonanie scenariusza oraz efekt uczenia się to trzy osobne statusy.

## 12. Pilotaż z ludźmi

Proponowany pierwszy pilotaż: 12–18 dorosłych ochotników o zróżnicowanym doświadczeniu. Wielkość służy wykrywaniu tarcia i problemów oceniania, nie dowodowi populacyjnego efektu. Udział, gromadzenie i przechowywanie prac wymagają wyraźnego uzgodnienia; niczego nie wysyłać do zewnętrznego providera w tle.

1. Na początku zadanie bez pomocy z dokładnie określonym celem i krótką samooceną pewności.
2. Nauka na równoważnym, innym briefie; zapisać pomoc, poprawki, czas i miejsca utknięcia.
3. Bezpośrednia próba samodzielna na trzecim briefie, z tymi samymi konstrukcjami do oceny.
4. Dobrowolny powrót po 7–14 dniach na nowe zadanie transferu. Termin jest propozycją badania, nie istniejącym przypomnieniem ani naukowo wyznaczonym optimum.
5. Dwoje recenzentów ocenia anonimowe prace bez informacji, czy to pre/post i jaki system pomagał. Rozbieżności rozliczyć na poziomie kryterium, nie ukrywać średnią.

Mierzyć: spełnienie konkretnych kryteriów, jakość uzasadnienia, liczbę i rodzaj pomocy, trafność samodiagnozy, poprawę po feedbacku, wynik transferu, czas do sensownej próby, porzucenie oraz bariery dostępu. Osobno raportować techniczną wierność briefowi i trafność artystyczną. Sukces generatora nie jest samodzielną miarą uczenia.

Porównanie baseline i przyszłej zmiany powinno stosować równoważne briefy z odwróconą kolejnością między uczestnikami. Ten sam uczestnik nie może znać odpowiedzi do testu końcowego z przykładu treningowego. Bez randomizacji i wystarczającej próby wniosek będzie dotyczył wykonalności i zaobserwowanych różnic, nie przyczynowego udowodnienia przewagi.

## 13. Kolejność wdrożenia i odbiór

| Etap | Zakres | Rozmiar | Zależność | Kryterium zamknięcia |
|---|---|---|---|---|
| 1 | LM01, W06, dokumentacja i negatywne próbki | S | Brak | Zastane sprzeczności i dwa kontrprzykłady wykryte przez test; poprawna ścieżka przechodzi |
| 2 | Spójność karty i constraints, roundtrip na trzech fikcyjnych uczniach | S/M | 1 | Brak utraty deklarowanego dostępu, pomocy, pochodzenia i jednego pending task |
| 3 | Trzy kompletne wieloturowe sekwencje kreatywne i teacher-content test | M | 1–2 | Obserwowane ślady w dostępnych hostach; pozostałe hosty wyraźnie NOT_RUN |
| 4 | Mała kalibracja rubryk z kilkoma różnymi dobrymi pracami | M | 3 | Kryteria nie mylą preferencji mentora z błędem; każde ma dostępny dowód |
| 5 | Pilotaż z dorosłymi i samodzielna próba transferu | L | 3–4, zgody uczestników | Raport z ograniczeniami, brakami, pomocą i niezależnymi ocenami |
| 6 | Rozszerzenie tylko domen, w których wykazano konkretną lukę | M zależnie od domeny | Wynik pilotażu | Mała zmiana istniejącego właściciela i test przed/po |

Koszt płatnych usług, rzeczywisty czas realizacji i spodziewany efekt liczbowy pozostają **Unknown**. Etapy są rekomendacją do osobnego zadania wdrożeniowego. W tym audycie nie zmieniono pluginu, nie dodano osobistych skilli i nie wykonano publikacji.


## Uzupełnienie po wykonaniu symulacji

Grupa nauki obejmuje 25 zakończonych profili: 24 PASS i 1 PARTIAL. Teacher Studio U015/U016 spełniło kryteria odpowiedzi tekstowej. Nie przeprowadzono lekcji z ludźmi ani badania trwałości kompetencji. Oryginalne luki dowodowe w repo pozostają odróżnione od nowego dowodu z tego audytu.

U024 otrzymał PARTIAL w próbie bazowej i obu dodatkowych powtórzeniach. Brak dotyczył konkretnych minimalnych dowodów do rozróżnienia problemu instrukcji, referencji, narzędzia i wykonania. To obserwacja trzech prób jednego scenariusza, nie częstość błędu w populacji.

Do planu feedbacku dodać niewielką mapę diagnostyczną: oczekiwany wynik i obserwowane odchylenie; dla instrukcji dokładny prompt i ograniczenia; dla referencji faktycznie użyte pliki oraz ich rola; dla narzędzia model, wersja i istotne ustawienia; dla wykonania rzeczywisty rezultat lub komunikat błędu. Nie żądać wszystkiego naraz. Wybrać jeden najbardziej rozstrzygający brakujący dowód i do jego uzyskania utrzymać przyczynę jako Unknown. Odbiór: mentor odróżnia konkurencyjne przyczyny na podstawie materiału, bez automatycznego obwiniania ucznia, modelu lub promptu.

Pełne wyniki: [Raport-symulacji.md](Raport-symulacji.md) i [Powtorzenia-symulacji.md](Powtorzenia-symulacji.md).
