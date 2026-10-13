# FrameCore Works Creative Studio: ocena zmian do 1.75.0

Data: 2026-10-13. Zakres: przegląd repozytorium i aktualnej zapisanej wtyczki, bez ich modyfikacji.

## Werdykt

**Rozwój jest wartościowy, a ostatnie zmiany poprawiają codzienną pracę. Stabilizacja nadal jest niepełna: sześć problemów z poprzedniego audytu odtworzono również w 1.75.0.** Zapisany plugin jest zgodny z aktualnym źródłem. Główne ograniczenie nie dotyczy więc synchronizacji, lecz kompletności kontroli poprawności i przenośności wykonania.

Najwyżej oceniam zmiany związane z realnymi zadaniami: krótsze wejście do projektu, pilnowanie właściwego właściciela, wyraźne błędy narzędzi, ochrona istniejących plików, synchronizacja lyric video, kontrola nadmiernie statycznych filmów i eksport HTML bez npm. To lepsza podstawa produkcji niż sama rozbudowa instrukcji.

Nie utożsamiam większej biblioteki technik ani liczby testów z jakością reklamy. Nowe narzędzia mają sens, ale finalny tekst, obraz, tempo i dźwięk nadal wymagają rzeczywistej kontroli.

| Obszar | Ocena |
| --- | --- |
| Użyteczność produktu | Wyraźny postęp, szczególnie motion i obsługa gotowych plików |
| Orkiestracja | Lepsza i bardziej jednoznaczna; część przypadków nadal wymaga testu hosta |
| Zgodność repo/plugin | Potwierdzona: 1190/1190 identycznych plików |
| Stabilność wykonania | Niepełna: powtórzone usterki oraz dwa lokalne błędy testów |
| Dowód jakości kreatywnej | Lepszy proces i więcej evali; brak nowego porównania finalnych prac na identycznych briefach w tym audycie |

## Aktualne źródła i stan pluginu

- Repozytorium: [FrameCoreWorks/framecore-works-creative-studio](https://github.com/FrameCoreWorks/framecore-works-creative-studio).
- `main`: [`bc6756b2e689e0a0adfd19f61e69f53bcbec8d13`](https://github.com/FrameCoreWorks/framecore-works-creative-studio/commit/bc6756b2e689e0a0adfd19f61e69f53bcbec8d13).
- Wydanie paczki: **1.75.0**, tag wskazuje `1eb21947b58fef90d70d64b67c7f062b97207439`.
- Istniejący plugin: `plugins_6ab8e226cbd48191b661cb2ea24d0351`.
- Zapisane wydanie: **1.75.0**, `pluginrel_6ace3ff36838819181f372c738d0b337`.
- Pełny odczyt archiwum: **1190 plików zgodnych bajtowo z repo, 0 różnic, 0 braków, 0 dodatkowych plików**. Aktualny release ID i `main` odczytano ponownie przed zamknięciem analizy.
- Paczka na `main` jest taka sama jak na tagu 1.75.0; późniejsze commity dotyczą dokumentacji repozytorium.

Jest to potwierdzenie zapisanej paczki. **Aktywne przeładowanie klienta, działanie menu i kompletna ścieżka produkcyjna w bieżącym czacie pozostają Unknown / NOT_RUN.**

Baza porównania: poprzedni audyt **1.61.0 z 2026-10-11**. Łącznie zmieniono 266 plików repozytorium, dodano 35 693 i usunięto 712 linii; statystyka obejmuje także raporty i zapisy evali. W paczce: **63 nowe, 103 zmienione, 1024 identyczne pliki, 0 usuniętych ścieżek**. Powitanie PL/EN i przypięte źródła `upstream/` są identyczne z bazą. Menu kreatywne zmieniło się celowo, zgodnie z decyzją właściciela CR-20261013-01.

Odczytano aktualny `AGENTS.md`, załączoną księgę zasad, poprzedni raport, changelog, ledger, status wydania, wybrane aktywne instrukcje i narzędzia oraz powiązane testy. Ocena merytoryczna koncentruje się na zmienionych ścieżkach i wcześniejszych usterkach; zgodność wszystkich plików nie oznacza osobnego audytu semantycznego każdego z nich.

## Najważniejsze dobre zmiany

### 1.75.0: naprawy konkretnych problemów

Nowe instrukcje przekazują pracę do właściciela: Humanizer oddaje nowe copy do Copy Voice, Caption Studio nie wymyśla samodzielnie treści reklamy, a statyczny projektant przekazuje animację do właściwej domeny. To ogranicza mieszanie ról i omijanie ich kontroli jakości. Reguły umieszczono w aktywnych `SKILL.md`, które model faktycznie ładuje.

Poprawiono też kilka błędnych deklaracji: przestrzeń kosztów nie oznacza zgody na płatne wykonanie, Humanizer nie powinien dodawać nieudokumentowanych claimów, a Copy Voice nie może twierdzić, że wstawił U+00A0, jeżeli dostarczony tekst go nie zawiera. Dobre są jedno pytanie przy brakującym briefie oraz zakaz obietnicy renderu przed sprawdzeniem hosta.

Narzędzia lepiej zgłaszają brakujące wejścia i odmawiają nadpisywania plików w compositorze i lyric timing. Poprawiono odkrywanie Chromium z Playwright i ujednolicono pin HyperFrames.

Repozytorium dokumentuje **18 naprawionych ustaleń z własnego gap audytu Claude’a** oraz jedno nieodtworzone. To inny zestaw niż problemy F01–F07 z mojego poprzedniego raportu. Pięć przypadków hostowych G01–G05 ma zapisane sukcesy w celowanych przebiegach: pierwszy 3/5, następnie rerun dwóch nieudanych 2/2. Zapisy dotyczą kandydatów z markerem 1.74.0 i niezacommitowanymi zmianami, później wydanych jako 1.75.0. Nie są nowym pełnym testem całej opublikowanej paczki w ChatGPT.

### 1.74.0: krótsza ścieżka startowa

Po wyborze trybu kreatywnego użytkownik otrzymuje w jednym komunikacie obszary `1–8` i tempo `A/B`, np. `8, B`. Sam numer obszaru wybiera Quick. To usuwa zbędną turę i zachowuje czytelność wyborów. Nazwy i kolejność obszarów są teraz wpisane w entrypoint, a pending menu ze starej sesji zachowuje dawną numerację.

Zmiana jest zgodna z zapisaną decyzją właściciela. Dostępne są evale Claude Code przed/po; nowe zachowanie w zwykłym ChatGPT wymaga oddzielnego potwierdzenia. Powitanie nie zostało skrócone.

### 1.73.0: eksport HTML przy zablokowanym npm

`capture-html.mjs` uzupełnia rzeczywistą lukę: przy dostępnym Node, Chromium i FFmpeg można wyrenderować kompozycję z `window.renderFrame(t)` bez instalacji silnika przez npm. Obsługuje całkowite i wymierne FPS, jawne wymiary i opcjonalne audio. Skrypt odmawia nadpisania pliku, sprawdza parzyste wymiary i usuwa niekompletny wynik po błędzie.

Runtime probe przed obietnicą wykonania jest dobrym rozwiązaniem. Reguła czystej końcowej planszy i pozostawiania dodatków wyłączonych do akceptacji również odpowiada konkretnemu problemowi produkcyjnemu. Brak lokalnego browsera ogranicza nowe wykonanie capture w tym audycie; dostępny jest historyczny zapis testów kontenerowych.

### 1.70–1.72: motion, tekst piosenki i druk

- Podział odpowiedzialności Studio/HyperFrames dla rolek klientów jest czytelniejszy: Studio utrzymuje brief, kierunek, tekst i review, a silnik wykonuje kompozycję.
- `motion_activity.py` wykrywa film, który po krótkim wejściu staje się prawie nieruchomy. Jawne holds pozwalają zachować celowy spokój. Mierzy jednak piksele, więc sam ruch kamery może przejść test bez rozwoju pomysłu.
- `lyric_timing.py` zachowuje tekst użytkownika, dopasowuje słowa do dostarczonych/rozpoznanych czasów, oznacza luki i proponuje cięcia na siatce rytmu. Naprawiono ujemne cięcie na starcie i odwrócone przedziały interpolacji; dziewięć lokalnych testów przeszło. To nie jest dowód dokładnego alignmentu na każdej piosence; realna długa piosenka nadal jest wskazana w handoverze jako następny test.
- Atlas 637 technik jest sensownym słownikiem do realizacji konkretnego briefu, z przypiętym pochodzeniem. Instrukcje nakazują tworzyć ruch z briefu, zamiast kopiować kod kart. Nie traktuję liczby rekordów jako miary craftu.
- `print_pdf.py` daje użyteczne kontrole TrimBox/BleedBox, rozdzielczości, kolorów, farby, fontów, przezroczystości oraz porównanie regionów i edycję bloków wektorowych. Poprawnie odróżnia output intent od konwersji kolorów i preflight od certyfikacji PDF/X. Tego modułu nie wykonano lokalnie z powodu braku pikepdf; siedem testów zostało pominiętych. Nie potwierdzam jego poprawności wyłącznie z zielonego CI.

### Ideacja i handoffy od 1.66

Przejście od gotowych schematów do mechanizmu wymyślonego z briefu jest właściwe. `creative_direction` w Project State pozwala nie rozpoczynać koncepcji od nowa po przekazaniu zadania. Korygowanie routingu ruchomego materiału i rozdzielenie oglądu klatek od odsłuchu dźwięku wzmacnia uczciwość QA.

Evale kreatywności wykazują zarówno poprawę, jak i zmienność wyników oraz ograniczenia dopasowania słów. Dobrze, że raporty nie ukrywają tych ograniczeń. To dowody określonych przypadków, nie ogólnego wyniku jakości wszystkich prac.

## Ponowna kontrola wcześniejszych usterek

**P1**: priorytet przed finalnym dostarczeniem lub automatycznym wydaniem. **P2**: istotny błąd warunkowy albo przenośności. Wszystkie poniższe reprodukcje wykonano ponownie na aktualnym źródle; izolowany commit powstał wyłącznie w tymczasowym repo, bez pushu.

| ID / priorytet | Wynik w 1.75.0 | Dowód i skutek |
| --- | --- | --- |
| F01 / P1 | Nadal występuje | Cena `129,00 zł` w polu `[1000,40,700,120]` na płótnie 800 × 400: compositor `--strict` zwraca kod 0 i `ok`, a PNG nie zawiera żadnego widocznego tekstu. Nadal brakuje kontroli położenia całego tekstu wobec eksportu |
| F02 / P1 | Nadal występuje | Persistent z hasłem o bezpłatnej dostawie: 1959 px na płótnie 1080 px, x = −965. Active-word z długim nazwiskiem: 1808,75 px, x = −364,375. Oba rendery kończą się kodem 0 z pustą listą overflow |
| F03 / P1 | Nadal występuje | `release.commit()` przez `git add -A` włącza `unfinished-user-draft.txt` obok zamierzonego `release.txt`. Nie ma dowodu, że dotychczasowe wydania faktycznie opublikowały taki szkic; jest potwierdzona możliwość naruszenia zakresu |
| F04 / P2 | Nadal występuje | Wejście brutto 123 przy podanej stawce 23: sumy 100/23/123 są prawidłowe, ale 123 trafia pod nagłówek „Cena jedn. netto” |
| F05 / P2 | Nadal występuje | Stawka godzinowa −150 i 17 godzin przechodzą walidację, dając −2550,00 |
| F06 / P2 | Nadal występuje | Po zmianie kolorów i fontu Inter na Anton oraz po wariancie tokens zachowuje się `approved` i dowód poprzedniej rewizji. Reset dotyczy tylko copy, nie zatwierdzenia zmienionego wyglądu |
| F07 / P2 | Nadal występuje, dodatkowy podobny przypadek | Starszy przykład color-block i nowy snippet FC-SOCIAL-10 nie mają przypiętych fontów; fallback DejaVu daje przepełnienie. Lokalny zestaw ma dwa FAIL |

Źródła: [compositor](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/1eb21947b58fef90d70d64b67c7f062b97207439/plugins/framecore-work-creative-studio/skills/static-graphic-design-creator/assets/static-render/compose.py), [renderer](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/1eb21947b58fef90d70d64b67c7f062b97207439/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-render/render.py), [kalkulator](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/1eb21947b58fef90d70d64b67c7f062b97207439/plugins/framecore-work-creative-studio/skills/brief-architect/scripts/quote_calc.py), [warianty](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/1eb21947b58fef90d70d64b67c7f062b97207439/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-variants/variants.py), [release helper](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/bc6756b2e689e0a0adfd19f61e69f53bcbec8d13/scripts/release.py).

Repozytorium dodało zabezpieczenie compositorowego nadpisywania. To dobra naprawa, ale nie dotyczy F01. Kopie plików w zapisanym pluginie są identyczne, więc również zawierają powyższe problemy.

## Dwa lokalne błędy testów

1. `motion-quality.test.mjs:82`: snippet **FC-SOCIAL-10**, styl meadow, domyślny Arial/Helvetica bez plików fontu. Tutaj wybrano DejaVu Sans. `Dziękujemy!` ma **977 px przy kolumnie 908 px**; renderer słusznie odmawia renderu, choć przykład ma działać bez zmian.
2. `motion-toolkit.test.mjs:796`: przykład **color-block** używa tego samego fallbacku. `colour` ma **984 px przy kolumnie 928 px**. Critique zwraca błąd, a test oczekuje sukcesu.

To potwierdzona zależność wzorców od dostępnych fontów. Nie oznacza awarii wszystkich nowych renderów. Dokładny font wybrany w CI pozostaje Unknown w tym audycie. Potrzebne są przypięte fonty w przykładach i snippetach, a test fallbacku powinien mieć osobne kryteria.

## Utrzymanie i granice QA

- Orkiestrator zmniejszył się z 31 995 do **30 331 bajtów**, czyli ma **1669 bajtów** zapasu do repozytoryjnego limitu 32 000. Problem jest częściowo rozwiązany; dawny docelowy poziom 29 000 nadal nie został osiągnięty.
- Opisy skilli nadal zajmują **7773 z 7800 znaków** dopuszczanych przez walidator. To 27 znaków zapasu i ostrzeżenie. Nie jest to dowód aktualnego ucinania przez host.
- `release.parse_checks()` nadal nie rozpoznaje lokalnego reportera Node 24 (`ℹ tests/pass`), zwracając pusty słownik statystyk. Kod wyjścia testów nadal blokuje release; problem dotyczy raportowania.
- `motion_activity.py` jest nakazany w aktywnej instrukcji, lecz automatyczne włączenie go do `acceptance.py` nadal figuruje jako przyszły krok. Poprawa procedury nie oznacza twardego wymuszenia każdego sprawdzenia.
- 204 canonical cases, 19 presentation cases i 6 motion/sound cases pozostają planowane. Osobne wykonane evale Claude Code nie zmieniają automatycznie ich statusu.
- Repo jest w maintenance mode. Wykazane teraz błędy są konkretnymi triggerami napraw; samo zwiększanie liczby skilli, katalogów i metod nie jest uzasadnionym następnym krokiem.

## Faktycznie wykonana weryfikacja

| Kontrola | Wynik | Co potwierdza |
| --- | --- | --- |
| Pełne archiwum zapisanej paczki wobec repo | **1190/1190 identycznych plików** | Zapisane źródło i inventory |
| Canonical validator | **PASS**, ostrzeżenie budżetu opisów | Struktura i kontrakty źródłowe |
| CI aktualnego main | **success**, [run 38406483882](https://github.com/FrameCoreWorks/framecore-works-creative-studio/actions/runs/38406483882) | Kontrole w środowisku CI |
| Lokalny Node | **218: 208 PASS, 2 FAIL, 8 SKIP** | Testy źródeł i wykonania; opcjonalny browser niewykonany |
| Lokalny Python | **267: 256 PASS, 0 FAIL, 11 SKIP** | Wszystkie zestawy wykonane, także osobno po zatrzymaniu check_all na Node |
| Pominięte Python | 7 print PDF, 3 GEPA, 1 Claude CLI | Brak odpowiednich lokalnych zależności; nie zaliczono jako PASS |
| Reprodukcje F01–F06 i parsera release | Wykonane, usterki potwierdzone | Podane przypadki brzegowe |
| Nowe testy na aktualnym ChatGPT/Work | **NOT_RUN** | Brak nowego dowodu UI i zachowania klienta |
| Nowy odsłuch / pełny ogląd pracy klienta | **NOT_RUN** | Brak nowej oceny finalnego medium |

Środowisko: Python 3.12.14, Node 24.19.0, Pillow i numpy dostępne; brak pikepdf oraz lokalnego Claude CLI/browsera. Nowych zależności nie instalowano. Nie wykonywano nowych wywołań generacyjnych ani płatnych evali. Odczytane historyczne evale Claude Code opisano jako REPORTED_HISTORY, a lokalne wyniki jako EXECUTED_CHECK.

## Zalecenie

**Zachować ostatnie zmiany i domknąć zgłoszone usterki w niewielkim wydaniu utrzymaniowym.** Najpierw kompletność wszystkich warstw tekstu i kontrola zakresu stagingu. Następnie etykiety kwot, walidacja stawek i stan akceptacji wariantów. Potem przypięcie fontów wzorców oraz stabilny parser wyników.

Po naprawach wystarczy mały test przekrojowy aktualnej wersji w ChatGPT Work i zwykłym ChatGPT: wejście `1 → 8, B`, dokładna grafika z ceną, wariant zatwierdzonego motion, długi napis w 9:16 i oferta z danymi brutto. To da więcej pewności niż kolejna rozbudowa katalogu.

Repo i zapisany plugin nie zostały zmienione. Raport przedstawia ocenę i zalecenia, nie wykonane naprawy.

---

## Maintainer decisions (2026-10-13, change CC-20261013-06, release 1.76.0)

The evaluation above is the owner's (Polish, kept as received). Each finding was checked against the 1.75.0 source before a change.

| Finding | Decision | Evidence after |
| --- | --- | --- |
| F01 compositor text outside the canvas | Fixed: a text box outside the canvas is `text_overflow` (exit 4) | `static_render_test` case with the report's 800 x 400 price box |
| F02 persistent line and active word wider than the frame | Fixed in `render.py`: both are overflows | two `motion_kinds_test` cases; both error on 1.75.0 |
| F03 release commit stages unrelated files | Fixed: `release.py prepare` refuses a dirty working tree before writing anything | `tests/test_release.py` |
| F04 gross entry under a net header | Fixed: "Cena jedn. brutto" / "Unit price (gross)" when `prices` is gross | `quote_calc_test` |
| F05 negative rate accepted | Fixed: negative `rates.hour`, `rates.day` and extra prices are refused | `quote_calc_test` |
| F06 approval kept after a look change | Fixed: a brand kit or variant that changes tokens or fonts resets approval to proposed | `motion_variants_test` |
| F07 examples overflow without Arial | Environment dependency, not a layout defect: the examples are laid out for Arial and the renderer correctly refuses to crop with the wider DejaVu Sans. The renderer now reports a `font_warning`, its README names `fonts-liberation`, and the two tests skip with that reason when no Arial-compatible face exists | tests pass here with Liberation Sans |
| Release parser on Node 24 | Fixed: counts are read from TAP (`#`) and spec (`ℹ`) reporters | `tests/test_release.py` |
| Maintenance notes (orchestrator size, description budget, motion activity not wired into acceptance, planned evals) | No change: no defect seen in use | |
