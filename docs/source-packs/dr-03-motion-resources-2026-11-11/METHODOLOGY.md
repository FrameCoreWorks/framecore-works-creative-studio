# DR-03 — metoda i poziomy dowodów
Badanie z 2026-11-11, Europe/Warsaw. Zakres: rozszerzenia motion dla FrameCore, bez implementacji lub benchmarków. Oryginalny PROMPT.md zachowano. Trzy lane: wykonawcze moduły, wiedza agentowa, production assets. Baseline poprzedza selekcję; po częściowym przerwaniu trzy sesje odtworzyły brakujące wyniki z zapisanych źródeł i ponownych odczytów.

## Odczyt i selekcja
GitHub czytano przez connector: metadane commitów, drzewa, konkretne README/licence/manifest/code/reviews; źródła pozagithubowe przez web. Przykładowe rzeczywiste zapytania discovery leada: „animowane ikony SVG Lottie darmowe licencja komercyjna” oraz „motion graphics deterministic frame seek alpha rendering library”. Wyniki wyszukiwania służyły odkryciu, nie stanowią same dowodu; źródła z read_scope=NOT_READ/failed pozostają lukami. To celowy przegląd, nie wyczerpujący katalog rynku.

Nie pobrano repo checkoutów, paczek binarnych lub mediów. Registry zawiera URL, pin i zakres odczytu; nie jest mirror źródeł. Drzewo plików nie oznacza odczytania wszystkich treści. GitHub issue jest raportem autora zgłoszenia, a nie potwierdzoną reprodukcją. Pin current head nie zaleca automatycznie użycia prerelease.

## Etykiety
| Etykieta | Znaczenie |
|---|---|
| DOCUMENTED | Twierdzenie odczytane w primary docs/manifest/licence; może opisywać test fixture bez wyniku |
| CODE_INSPECTED | Przeczytany konkretny kod na podanym SHA; nie uruchomiono go |
| AUTHOR_TEST | Odczytany jawny wynik próby autora z określonym zakresem; sam skrypt/test suite/demo bez wyniku nie wystarcza |
| OWN_TEST | Próba rzeczywiście wykonana tutaj; **brak testów wykonawczych kandydatów**. Własna kontrola dokumentów jest odrębna |
| NOT_RUN | Nie wykonano instalacji, import/decode/render, odsłuchu, testów wizualnych ani integration/host activation |
| Unknown | Brak dostępnego dowodu właściwości lub niewyjaśniona sprzeczność |
| DERIVED | Nasza propozycja, szacunek integracji, ranking, reguła adaptacji, fixture lub wniosek z zakresu dowodów |

Źródła mogą mieć dodatkowy typ MANIFEST/LICENSE/ISSUE/METADATA, który opisuje dokument; nie zastępuje powyższego poziomu dowodu claim. Reported zewnętrzne testy useAnimations/Generative Icons zachowują osobny kwalifikator PASS_REPORTED/FAIL_REPORTED; nie stają się naszymi OWN_TEST. Repo source, saved package, installed version i active behavior są oddzielne.

## Rankingi
Kolejność wynika z marginalnej użyteczności wobec baseline, możliwości kontroli czasu i eksportu, zakresu praw, ograniczeń oraz szacowanej pracy. Żadnych punktów za stars/downloads. To kolejność przyszłych prób lub adaptacji wiedzy, nie lista produkcyjnie zaakceptowanych integracji. Mały moduł z jasnym frame function ma pierwszeństwo przed kolejnym pełnym silnikiem. Asset z niezależną licencją i edytowalnym źródłem ma przewagę nad galerią.

## Weryfikacja artefaktów
verify_artifacts.py jest własnym małym skryptem strukturalnym: sprawdza hash promptu, wymagane pliki/pola, source references, spójność CSV/JSON, trzy lane, deep-dive index, limity projektu Hipsona i deklarowane zamknięcie uwag. Nie testuje produktu ani prawdziwości każdego źródła. Świeży recenzent czyta dokumenty i sprawdza wybrane primary claims; lead rozstrzyga uwagi. Końcowy Hipson close uruchamia zadeklarowany check bez force.

