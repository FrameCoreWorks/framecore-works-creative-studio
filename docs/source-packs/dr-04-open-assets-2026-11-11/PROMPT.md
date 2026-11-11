Przeprowadź Deep Research dodatkowych źródeł mediów i dostawców nadających się do integracji z wtyczką FrameCore Open Assets. Celem jest rozszerzenie trwałej możliwości wyszukiwania i pozyskiwania legalnych assetów, nie jednorazowe znalezienie kilku atrakcyjnych plików.

Raport po polsku. Wykonaj właściwe badanie, nie zatrzymuj się na planie ani katalogu popularnych banków zdjęć.

1. AKTUALNY STAN I GRANICE

Przeczytaj aktualne repozytorium:
https://github.com/FrameCoreWorks/framecore-open-assets

Sprawdź README, AGENTS.md, SKILL.md, provider index, manifesty providerów, kontrakt danych, runtime, adaptery, testy i udokumentowane ograniczenia. Zapisz commit i datę. Odróżnij dokumentację, kod i potwierdzone wykonanie. Nie utożsamiaj repozytorium z aktualnie zainstalowaną wersją.

Kontekst współpracy:
https://github.com/FrameCoreWorks/framecore-works-creative-studio
https://github.com/FrameCoreWorks/framecore-works-toolbox

Open Assets ma pozyskiwać media i ich metadane. Studio/FrameMotion/FrameCut odpowiadają za użycie w produkcji. Nie rozszerzaj researchu na płatne generowanie obrazów ani na budowę nowego montażysty.

Ustal, które źródła i kategorie są już obsługiwane. Każdy kandydat otrzymuje status NEW_PROVIDER, EXISTING_NEW_CATEGORY, ALREADY_COVERED, DUPLICATE_MIRROR albo BASELINE_UNKNOWN.

2. PRIORYTETY POSZUKIWAŃ

Szukaj zasobów przydatnych w reklamie, filmie, motion graphics, materiałach produktowych i projektowaniu:
- fotografie i wycięte obiekty;
- ilustracje, wektory, ikony, sylwetki, transparentne PNG;
- tekstury, PBR, HDRI, tła i powierzchnie;
- wideo, B-roll, pętle, overlaye i materiały z alfą;
- muzyka, nagrania SFX, ambience, foley i efekty syntetyczne;
- modele 3D, materiały, rigi i animacje;
- fonty oraz inne zasoby, jeśli stanowią sensowne rozszerzenie.

Zbadaj archiwa publiczne, instytucje kultury/nauki, biblioteki autorów, publiczne repozytoria, katalogi danych i serwisy specjalistyczne. Nie ograniczaj geografii do Polski.

Priorytetem są faktyczne luki obecnej wtyczki. Jeśli aktualny audyt potwierdzi słabe pokrycie nagrywanych SFX, muzyki, wideo lub nowoczesnych ilustracji, poświęć im więcej uwagi. Reprodukcje muzealne nie zastępują współczesnego stocku, audiobook nie jest muzyką, a tekstura nie jest ilustracją.

Oddziel obecnie wspierane formaty/kategorie od nowych wymagających rozszerzenia downloadera, dekodera i polityki praw.

3. WARUNKI KWALIFIKACJI

Główna ścieżka:
- bez opłaty za pobranie i wykorzystanie w zamierzonym zakresie;
- bez konta i klucza API;
- dokumentowane publiczne API zgodne z architekturą wtyczki;
- jednoznaczna identyfikacja konkretnego assetu i jego praw;
- dozwolona automatyzacja wyszukiwania i pobierania;
- realnie dostępne pliki produkcyjne.

Oficjalne statyczne manifesty, katalogi plików i repozytoria mogą być osobnymi kandydatami rozszerzenia, jeśli dostęp maszynowy jest dozwolony. Nie przedstawiaj ich jako już kompatybilnych adapterów API.

Źródła wymagające konta/klucza, ręcznego pobrania, specjalnej zgody lub płatności oddziel do OPTIONAL/OUT_OF_CORE/REJECTED. Darmowy trial, kredyty promocyjne i subskrypcja nie spełniają głównego kryterium.

Nie opieraj adaptera na nieudokumentowanych endpointach aplikacji, skopiowanych cookies, obchodzeniu CAPTCHA, podszywaniu się pod przeglądarkę, rotacji proxy ani scrapingu sprzecznym z zasadami źródła. Publiczna strona i robots.txt nie stanowią same w sobie zgody na ponowne użycie plików.

4. PRAWA I POCHODZENIE

Sprawdź aktualną politykę praw wtyczki. Preferuj jednoznaczne CC0, public domain/PDM i obsługiwane CC BY z prawidłową atrybucją. Fonty z OFL i kod z MIT/Apache/BSD oceniaj według właściwej kategorii; nie zastępują licencji mediów.

Rozróżnij:
- regulamin serwisu;
- licencję metadanych/API;
- licencję konkretnego pliku;
- prawa do wizerunku, marek i materiałów osób trzecich;
- prawo do użycia w gotowym filmie;
- prawo do redystrybucji samego assetu.

NC, ND, SA, nieznane prawa i licencje własne wymagają jawnej klasyfikacji zgodnej z polityką wtyczki. SA nie traktuj jak CC0. Nie uznawaj całej kolekcji za public domain na podstawie pojedynczego przykładu. Uwzględnij jurysdykcję tam, gdzie wpływa na status praw.

Wiedzę prawną opieraj na oryginalnych warunkach i tekstach licencji. Przy niejednoznaczności podaj Unknown, nie gwarancję prawną. Pinterest, galerie portfolio i inne źródła inspiracji bez potwierdzonych praw oznacz REFERENCE_ONLY.

5. KARTA DOSTAWCY

Dla każdego kandydata podaj:
- nazwa, właściciel, URL, dokumentacja API, regulamin i polityka licencji;
- kategorie i charakter materiałów, jakość i użyteczność produkcyjna;
- dowód nowości względem aktualnego baseline;
- wyszukiwanie: pełnotekstowe, tagi, filtry, języki, paginacja;
- stabilne ID, autor, data, źródło i licencja per asset;
- warianty, rozdzielczości, formaty, długość, FPS, kanały audio/alfa;
- udokumentowane endpointy wyszukiwania, szczegółów i pobierania;
- konto, klucz, limity, polityka automatyzacji i koszty;
- direct URLs, redirecty, podpisane/wygasające URL, CDN i wymagane domeny;
- cache, ETag/Last-Modified, Retry-After i udokumentowane błędy;
- powód rekomendacji, trudność adaptera, ryzyka i brakujące informacje.

Dla najlepszych źródeł wskaż 2–3 rzeczywiste rekordy o różnych wariantach/licencjach, jeśli można je odczytać. Nie wymyślaj ID, URL, parametrów ani przykładowych odpowiedzi API.

Oddziel trzy osie:
PROVIDER_ELIGIBILITY, ASSET_ELIGIBILITY, HOST_READINESS.
Dobry dostawca nie oznacza, że każdy jego plik jest dopuszczony. Sukces na jednym hoście nie dowodzi działania na innym.

6. ARCHITEKTURA I KONTROLA PLIKÓW

Porównaj kandydatów z obecnym kontraktem wtyczki. Zaproponuj adapter tylko tam, gdzie potrzebny; nie buduj równoległego katalogu lub polityki praw.

Opisz przepływ:
query → search results → szczegóły i licencja → wybór wariantu → weryfikacja praw → pobranie → kontrola pliku → sidecar/provenance → handoff.

Sprawdź, jak obsłużyć:
- MIME versus rozszerzenie i rzeczywistą zawartość;
- limity rozmiaru/czasu, redirecty i niedozwolone hosty;
- hash, duplikaty i zachowanie oryginału;
- decode obrazu/audio/wideo;
- archiwa, path traversal, nadmierną dekompresję i aktywne SVG/HTML;
- brak autora/licencji, usunięty plik, wygasły URL i zmianę wariantu;
- 401/403/429, challenge i Retry-After;
- cache, pacing i rejestr wykonania bez obchodzenia ograniczeń.

Plan retry ma respektować aktualne reguły runtime, w tym zatrzymanie po blokadzie. Nie proponuj nieskończonych ponowień ani cichego przełączania dostawcy.

W przykładzie manifestu zachowaj: source/provider, asset ID, source URL, download provenance, creator, license ID/URL, attribution, rights status, czas dostępu, wariant, parametry, SHA-256 i verification status. Użyj aktualnych nazw pól, jeśli są już zdefiniowane; nowe pola oznacz jako propozycję.

7. BADANIE I TESTY

Celuj w 20–30 nowych źródeł lub istotnych rozszerzeń i pogłębioną analizę 8–10 najlepszych, jeśli tyle spełnia wymagania. Nie uzupełniaj rankingu słabymi pozycjami.

Czytaj źródła pierwotne. Przy twierdzeniach podawaj URL i datę. Rozdziel DOCUMENTED, CODE_INSPECTED, AUTHOR_TEST, OWN_TEST, NOT_RUN i Unknown.

W ramach researchu nie instaluj i nie uruchamiaj kodu ani nie pobieraj binarnych próbek. Zaproponuj osobny plan testów małych próbek: wyszukanie, licencja per asset, wariant, download, decode, sidecar, poprawny błąd. Każdy test ma warunki wejścia, oczekiwany wynik i limit zasobów. Niewykonany test to NOT_RUN.

Nie oceniaj odsłuchu ani jakości obrazu, jeśli faktycznie nie miałeś do nich dostępu. Metadane i poprawny decode nie dowodzą jakości artystycznej.

8. WYNIK

Dostarcz:
- analizę luk obecnego Open Assets;
- katalog źródeł z kwalifikacją i dowodem nowości;
- tabelę pokrycia kategorii, praw i sposobów dostępu;
- osobne listy CORE_CANDIDATE, OPTIONAL, MANUAL/REFERENCE_ONLY i REJECTED;
- karty najlepszych providerów i przykłady rekordów;
- projekty adapterów, wymagane rozszerzenia formatu i plan testów;
- backlog P0/P1/P2 oraz IMPLEMENTATION_HANDOFF;
- rejestr źródeł, niepewności i braków.

Dla każdego zadania: cel, wejścia, wyjścia, właściciel, zależności, błędy, limity, koszt zweryfikowany lub Unknown oraz test akceptacyjny. Priorytet określ według nowej użyteczności, jakości metadanych, praw, trwałości dostępu i kosztu utrzymania.

Zapisz raport Markdown i katalog CSV/JSON, jeśli tworzenie plików jest dostępne. Nie zmieniaj wtyczek, nie instaluj providerów, nie wysyłaj prywatnych danych, nie publikuj i nie wykonuj pushu. Zakończ kompletnym pakietem badawczym, nie deklaracją wdrożenia.

Zacznij badanie teraz. Brak dostępu do jednego źródła nie blokuje pozostałych.