# Niezależna recenzja końcowa DR-01 — wznowienie

Data: 2026-11-11. Recenzent: Codex, osobna sesja pomocnicza `/root/review_finish`. **Werdykt: PASS_WITH_LIMITATIONS.** Nie pozostała stwierdzona uwaga blocking lub major. Pakiet spełnia zakres badania z PROMPT.md i rozszerzenia ponad After Effects. Nie oznacza to kwalifikacji produkcyjnej renderera ani zatwierdzenia architektury przez Claude.

## Ciągłość i rzeczywisty zakres recenzji

Pierwsza niezależna recenzja została przerwana przed zapisem werdyktu. Odzyskano jej checker, wyniki i snapshot. Relację o wcześniejszej lekturze całości oraz siedmiu ponownych otwarciach źródeł traktowano jako **częściowy materiał odzyskany**, nie dowód własnej czynności obecnego recenzenta. Nie przepisano wcześniejszego wyniku jako świeżego testu.

W tej sesji przeczytano PROMPT.md, SCOPE-CLARIFICATION.md, README, zasady modeli oraz skill verification-before-completion. Oceniono główną syntezę, warsztat CRAFT, słownik, receptury, proces i mapę poradników, profesjonalne modele pracy, kontrakty, audyt Studio, macierz pokrycia, benchmarki i handoff. W BACKENDS/REPOSITORIES odczytano mapowania, konkretne interfejsy, licencje i odrzucenia; nie wykonywano ponownego audytu wszystkich zewnętrznych repo. Odczytano przykładowe dane i oba lokalne checkery przed ich uruchomieniem. To samodzielna ocena treści i ukierunkowana weryfikacja, a nie powtórzenie całego researchu.

Wynik kontroli zamrożonej treści: **30/30 hashy zgodnych** z odzyskanym REVIEW-SNAPSHOT.json. Dowód: [RESUMED-SNAPSHOT-CHECK.json](RESUMED-SNAPSHOT-CHECK.json). REVIEW.md i VERIFICATION.json nie należą do tego snapshotu, ponieważ pozostają plikami zamknięcia hosta.

## Świeże sprawdzenia

| Kontrola | Rzeczywisty wynik | Granica |
|---|---|---|
| Odczytany checker poprzedniej niezależnej recenzji, uruchomiony ponownie | 56/56, 0 błędów | Struktura, referencje, hashe, arytmetyka i kompletność pól |
| Odczytany verifier hosta z `--draft`, uruchomiony ponownie | 41/41, exit 0 | Pomija końcową bramkę plików recenzji i rozstrzygnięć |
| Porównanie snapshotu | 30/30 zgodnych | Zamrożone pliki; nie historia wcześniejszych lektur |
| Ponowne sprawdzenie czterech przekazanych uwag | 4 resolved | Dane/opis/analityka, bez natywnego renderu |

Dowody: [INDEPENDENT-CHECKS.json](INDEPENDENT-CHECKS.json), [RESUMED-HOST-CHECK.json](RESUMED-HOST-CHECK.json). Przed nadpisaniem istniejącego wyniku wykonano kopię [INDEPENDENT-CHECKS.json.bak-20261111T093300Z](../EXPORT-MANIFEST.json) (backup pominięty w eksporcie; odsyłacz prowadzi do manifestu). Kod checkera nie został zmieniony. Zbiory kontroli częściowo się pokrywają; nie należy dodawać ich jako niezależnych dowodów jakości.

## Samodzielnie ponownie otwarte źródła

- [W3C CSS Font Loading, §3.3–3.4](https://www.w3.org/TR/css-font-loading/): `check` może zwrócić true przy nieistniejącej rodzinie lub fallbacku, a `ready` samo nie odrzuca obietnicy. Raport poprawnie wymaga kontroli konkretnego fontu i glifów.
- [Adobe Track Mattes](https://helpx.adobe.com/after-effects/desktop/work-with-transparency-and-compositing/work-with-track-mattes-and-traveling-mattes/track-mattes-and-traveling-mattes.html): ogólny opis przezroczystości pozostaje sprzeczny z tabelą trybów. CRAFT i R08 ujawniają tę sprzeczność i nie przedstawiają testu AE jako wykonanego.
- [GSAP Standard License](https://gsap.com/community/standard-license/): aktualnie odczytany tekst zawiera szczególne ograniczenia zastosowania w konkurencyjnych narzędziach wizualnego authoringu. Katalog poprawnie odróżnia tę licencję od MIT i od praw do assetów.
- [Studio fc_render.py w przypiętym commicie](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py): ponownie odczytano `motion_request` i `bind_motion` przez connector GitHub. Sprawdzenie `has_alpha` nie rozstrzyga association ani color. Próba tego samego pliku przez raw/web zakończyła się cache miss; nie była udanym odczytem.

Były to odczyty tekstu/kodu źródłowego. Nie uruchamiano kodu repozytoriów. W tej wznowionej recenzji nie otwierano ponownie Remotion terms/license ani score.mjs; wcześniejsze odczyty tych plików należą do odzyskanego materiału pierwszego recenzenta i specjalistów.

## Cztery wcześniejsze uwagi

| ID | Samodzielne potwierdzenie bieżącego rozwiązania | Stan |
|---|---|---|
| DR01-R1 — maska i stan kanału | Maska jest niewidocznym wejściem alfa w `composition-px`; cel deklaruje tę samą przestrzeń. Graf stosuje maskę po world transform. `hold-first/hold-last` i widoczność tekstu [45,240) definiują stan klatek granicznych. | resolved |
| DR01-R2 — alpha/color w bind | Audyt, kontrakt, macierz i backlog mówią o obecności kanału alfa oraz jawnej luce association/koloru. Ponowny odczyt źródła potwierdza ten zakres. | resolved |
| DR01-R3 — geometria parallax | B04 definiuje truck bez obrotu, ruch kamery i celu razem oraz głębokości 1000/1200/1400. Odwrotna proporcjonalność prędkości do głębokości jest poprawna dla tych założeń; dolly wyłączono z wniosku. | resolved |
| DR01-R4 — nazwa długiej osi | `long_sequence_fraction_is_exact` nie sugeruje dokładnej godziny. 108000 klatek przy 30000/1001 to 3603.6 s; przyszły godzinny test wdrożeniowy jest osobną rzeczą. | resolved |

Historyczne problemy przekazał host; obecne rozwiązania sprawdzono niezależnie. W [findings.json](findings.json) mają severity `info` i status `resolved`, aby nie udawać bieżących błędów ani gubić śladu recenzji.

## Ocena względem zamówienia

Pakiet zawiera 100 terminów z przykładem i konsekwencją, 18 receptur z parametrami, błędem/naprawą i QA, 5 benchmarków z adaptacjami 16:9/9:16, 10 rodzin backendów, 22 mapowania oraz 12 zadań P0/P1/P2. Źródła są powiązane z zastosowaniem i ograniczeniem; rejestr rozróżnia 124 rekordy, 121 URL i 117 jednostek po rozpoznanym scaleniu. Liczby nie są utożsamione z niezależnymi autorami lub wieloma potwierdzeniami tej samej tezy.

Poszerzenie poza AE jest merytoryczne: Fusion wnosi DAG i tracking/keying, Motion zachowania/tekst/cząstki, C4D instancje/pola, Blender kamerę/geometrię/cache, a Nuke/Houdini uzupełniają compositing i stan symulacji. Te metody są przełożone na dane, ograniczenia adapterów i testy. Nie znaleziono obietnicy identyczności każdego efektu AE z CSS albo FFmpeg.

Propozycja zachowuje istniejący score i handshake FrameCut oraz jednego właściciela nadrzędnego czasu. Rozdziela kod publicznego Studio od instalacji i aktywnego runtime. Handoff ma właścicieli, wejścia/wyjścia, zależności, proponowane/potwierdzone pliki, fallback, błędy/retry/limity/koszt i kryteria odbioru. Jest propozycją wdrożenia, nie zgodą na nie.

## Ograniczenia i warunek zamknięcia hosta

Natywne rendery, ciągłe oglądanie, odsłuch, font rendering, wydajność i cross-platform parity pozostają **NOT_RUN**. Wideo źródłowe pozostaje **NOT_VIEWED**. Sprawdzenia danych nie zastępują tych dowodów. Nie przeprowadzono pełnego ponownego odczytu wszystkich zewnętrznych źródeł ani audytu prawnego przyszłego produktu.

Sidecar i adapter są projektowane; schema obejmuje rdzeń, nie pełną produkcyjną semantykę. Brak rzeczywistego fontu i requestu jest jawnie blokującym preflightem przykładu, a nie nieujawnioną usterką. Publiczny commit `4611c9c4ed44579b8a2c0224c9276d955fccd8d6` nie potwierdza zainstalowanego runtime. Claude CLI nie uruchamiano i nie przypisuje się mu akceptacji.

Zapis tej recenzji jest ograniczony do `review/`. Nie zmieniono źródłowej treści raportów, kodu wtyczek, konfiguracji ani rejestru Hipson. Host powinien zapisać rozstrzygnięcia i REVIEW.md, a następnie uruchomić pełny verifier bez `--draft`; ten krok nie został tu zastąpiony deklaracją PASS. Werdykt dotyczy kompletności i wiarygodności badania w opisanych granicach.
