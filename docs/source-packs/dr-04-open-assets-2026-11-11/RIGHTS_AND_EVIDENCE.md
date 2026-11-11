# Prawa i znaczenie dowodów

Data odczytu: 2026-11-11. To objaśnienie istniejącej polityki Open Assets i warunków kandydatów, nie druga polityka praw ani akceptacja architektury.

## Osiem rozróżnień

| Znacznik | Co stwierdzamy |
|---|---|
| DOCUMENTED | Odczytano oficjalną dokumentację, warunki lub metadane. Nie oznacza testu adaptera. |
| CODE_INSPECTED | Przeczytano kod przy wskazanym commit; nie wykonano go. |
| AUTHOR_TEST | Autor repo opublikował wynik próby/CI; zakres i host pozostają takie jak w dowodzie. |
| OWN_TEST | Własny wykonany test; w DR-04 wyłącznie integralność dokumentów, nie kandydat/provider. |
| NOT_RUN | Nie wykonano; dotyczy wszystkich nowych download/decode i readiness. |
| Unknown | Źródło nie ustala faktu lub nie udało się go odczytać. |
| DERIVED | Wniosek badawczy oparty na jawnych przesłankach, a nie deklaracja dostawcy. |
| RECORD_READ | Pomocnicza etykieta odczytu rzeczywistych metadanych, traktowana jako DOCUMENTED; nie jest OWN_TEST. |

PROVIDER_ELIGIBILITY opisuje usługę, ASSET_ELIGIBILITY konkretny plik i zamierzone użycie, HOST_READINESS lokalną zdolność wykonania. CORE_CANDIDATE znaczy kandydat do małego spike po zamknięciu wymienionych zależności. Nie znaczy że działa, że każdy asset wolno użyć ani że został zatwierdzony przez Claude.

## Istniejące bramki

`license_policy()` rozpoznaje CC0/PDM i CC BY jako `eligible`; CC BY-SA jako `review_sa`; inne URL/licencje jako `blocked`. Brak autora przy CC BY blokuje. NASA i LibriVox mają właściwe `review_nasa` / `review_jurisdiction`, nie globalne public domain. Rozszerzenie fontów/ikon może wymagać typu assetu i przeglądu parsera OFL/ISC/MIT w tym samym miejscu; nie wolno podawać MIT kodu jako licencji zdjęć. [core.py, pin 889471f](https://github.com/FrameCoreWorks/framecore-open-assets/blob/889471fcdbc2216ddc465715eff0e82784d5b8ee/plugins/framecore-open-assets/scripts/core.py) — CODE_INSPECTED.

## Znaczenie tekstów licencji

CC BY 4.0 dopuszcza udostępnianie i adaptację z zachowaniem wymaganej informacji o autorze, licencji i zmianach. Nie licencjonuje znaków towarowych ani wszystkich praw osobistych. Synchronizacja muzyki lub nagrania z ruchomym obrazem jest adaptacją według definicji licencji. Produkcja musi więc zachować atrybucję w sposobie odpowiednim do finalnego medium. [CC BY legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en), DOCUMENTED.

CC BY-SA nie jest CC0. Adaptacja podlega warunkom ShareAlike; przy muzyce synchronizowanej z filmem nie wolno zakładać, że sam wpis w credits wystarczy. Zachować istniejącą świadomą akceptację SA, a gdy zakres utworu zależnego jest niejasny — Unknown do decyzji przed produkcją. [CC BY-SA legal code](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en), DOCUMENTED.

CC0 to zrzeczenie się praw przez uprawnionego w zakresie dozwolonym prawem, z konstrukcją licencji zastępczej. Nie dostarcza gwarancji dotyczących cudzych praw, patentów ani znaków. PDM oznacza identyfikację braku znanych ograniczeń; status może zależeć od jurysdykcji. Żaden z tych sygnałów nie jest model/property release. [CC0 legal code](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en), [PDM](https://creativecommons.org/publicdomain/mark/1.0/), DOCUMENTED.

OFL 1.1 dotyczy font software. Użycie w dokumencie różni się od redystrybucji samego fontu; ta druga wymaga zachowania licencji i informacji, a modyfikacje muszą uwzględniać Reserved Font Names. Nie klasyfikować OFL jako CC BY-SA ani CC0. [SIL OFL official text](https://openfontlicense.org/open-font-license-official-text/), DOCUMENTED.

## Prawa per plik i dwa rodzaje wykorzystania

W każdej karcie osobno oceniamy regulamin usługi, metadane/API, plik źródłowy, udział osób trzecich, wizerunek/marki, gotowy film oraz redystrybucję assetu. Licencja API ani informacja o public domain w jednej próbce nie obejmuje całego katalogu. NC/ND/Unknown pozostają blokowane przez obecną politykę; licencje własne są jawnie poza jej automatycznym rozstrzyganiem. Do produkcji wymagany jest odczyt strony konkretnego obiektu i warunków wariantu, z datą i zachowaniem pochodzenia.

Nie oceniano jakości artystycznej, obrazu, odsłuchu ani release'ów. Odczyt JSON, zgodność schematu, rozdzielczość deklarowana przez API i nawet przyszły poprawny decode nie dowodzą przydatności artystycznej ani pełnej czystości prawnej.
