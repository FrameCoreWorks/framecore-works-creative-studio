# DR-02 — Profesjonalny montaż i agentowy FrameCut

**Data: 2026-11-11, Europe/Warsaw.** Oryginalne wymagania: [PROMPT.md](PROMPT.md), doprecyzowanie szerszego zakresu: [SCOPE-CLARIFICATION.md](SCOPE-CLARIFICATION.md). To kompendium wieloczęściowe. Rozdziały specjalistów są częściami raportu, a nie materiałami obiecanymi na później.

## 1. Najważniejszy wynik

Profesjonalny montaż to porządkowanie znaczenia w czasie. Agent może wykonywać znaczną część pracy powtarzalnej i precyzyjnej, jeśli oddzieli obserwację materiału, decyzję redakcyjną i operację. Wykryte cięcie oznacza zmianę obrazu, ASR oznacza hipotezę wypowiedzi, beat oznacza oszacowanie pulsu. Żadne z nich samo nie rozstrzyga, czy należy przerwać reakcję człowieka, pokazać detal produktu albo usunąć wahanie. **DERIVED**: FrameCut powinien optymalizować śledzalność i odwracalność decyzji, a nie liczbę wykonanych cięć.

Publiczny main Studio już zawiera FrameCut w `opencut-video-studio`. Projekt ma schemat v1, źródłowe PTS, rewizje, locks, natywne edycje, storyboard, motion binding, renderer i techniczne QA. To wymaga ewolucji istniejącego kontraktu. Nie ma podstaw do traktowania nowej osobnej wtyczki jako już wdrożonej ani do wymyślania jej repo. [R03][R04][R05][R07][R08]

Przypięty commit Studio: `4611c9c4ed44579b8a2c0224c9276d955fccd8d6`, 2026-11-11T07:20:22Z. Pakiet 1.174.1; runtime FrameCut 1.1.0; project schema 1. Inspekcja 14 wybranych plików z installed cache wykazała zgodność bajtową z pinem. To **nie jest pełny audyt instalacji ani sprawdzenie działania aktywnego hosta**. [R01][R30]; szczegóły w [CURRENT-STUDIO](specialists/repo/CURRENT-STUDIO.md).

## 2. Jak czytać poziom dowodu

| Etykieta | Znaczenie | Czego nie dowodzi |
|---|---|---|
| SOURCED | Twierdzenie ograniczone do przeczytanego źródła, wskazanego fragmentu i wersji | Działania na tym komputerze ani jakości dowolnego filmu |
| PRACTITIONER | Udokumentowany opis procesu konkretnego praktyka | Uniwersalnej normy albo reprodukcji jego efektu |
| DERIVED | Nasza synteza, obliczenie, projekt kontraktu lub reguła wynikająca z analizy | Zatwierdzenia architekta ani gotowej implementacji |
| Unknown | Brak wystarczającego dowodu | Ani istnienia, ani nieistnienia funkcji |
| NOT_RUN | Zdefiniowano test, lecz go nie wykonano | Nie wolno zamienić na PASS na podstawie dokumentacji |

Osobno rejestrujemy dokumentację, inspekcję kodu, testy autora przeczytane w repo i własne testy. Materiały wideo opisane w źródłach nie zostały obejrzane w tym badaniu. Wywiad tekstowy jest dowodem relacji montażysty, nie oglądu opisywanej sceny. Nie kopiowano kursów ani prywatnych materiałów. Duże publiczne PDF czytano poza katalogiem Hipsona; rejestr ma tylko niewielkie raporty/snapshoty kodu i dowody.

## 3. Warsztat: najpierw obejrzeć i wybrać, potem budować

Pełna analiza dramaturgii, gatunków, reguł i kontrprzykładów jest w [CRAFT](specialists/craft/CRAFT.md); [100 pojęć PL/EN](specialists/craft/GLOSSARY.md) i [18 receptur](specialists/craft/RECIPES.md) stanowią praktyczną część kompendium.

**DERIVED proces selekcji.** Zacząć od intencji sceny: zmiany wiedzy, stawki lub emocji. Spisać ograniczenia: fakty, kolejność zdarzeń, chronione wypowiedzi, konieczne informacje, prawa do materiałów. Następnie ocenić kandydatów w odrębnych wymiarach: treść/rola, wykonanie i emocja, czytelność akcji, ciągłość, dźwięk, techniczna używalność. Nie sumować ich bezmyślnie w pojedynczy „quality score”. Dubel z drobnym błędem technicznym może być najlepszym wykonaniem; ostrzejszy może zniszczyć intencję.

Log powinien mieć asset hash, source range, opis obserwacji i kontekst przed/po, ale również status faktycznego oglądu/odsłuchu. Przy dialogu sprawdzić negację, warunek, zaimek i odpowiedź na pytanie. Usunięcie „nie” lub poprzedzającego zastrzeżenia jest zmianą wypowiedzi, nawet jeśli nowe zdanie brzmi płynnie. W dokumencie reakcja z innego czasu nie może bez uzasadnienia udawać reakcji na inne słowa.

Cięcie jest przydatne, gdy przenosi uwagę, ujawnia informację, pokazuje konsekwencję albo kompresuje niepotrzebny czas. Pozostawienie ujęcia bywa właściwe, gdy znaczenie powstaje w reakcji, ruch musi się zakończyć albo widz musi przeczytać ekran. Szybkość montażu nie zastępuje napięcia; transition count nie mierzy profesjonalizmu. **PRACTITIONER** źródła w CRAFT zestawiają pracę bez muzyki z pracą z temp od początku, zamiast wybierać jedną doktrynę.

Gatunek zmienia cel. Fabuła prowadzi uwagę i identyfikację; dokument wymaga uczciwości wobec źródła; reklama może podporządkować formę demonstracji konkretnej korzyści; tutorial potrzebuje czasu na rozpoznanie interfejsu; multicam wykorzystuje wspólny czas zdarzenia i wybór punktu widzenia; teledysk może świadomie podporządkować sekwencję muzyce; showreel musi wykazać umiejętność; social video potrzebuje czytelności w swoim kontekście oglądania. Hook/body/CTA jest opcją dla części komunikacji, nie domyślną strukturą wszystkich filmów.

## 4. Pipeline i profesjonalne programy

Szczegółowe porównanie Resolve, Premiere Pro, Final Cut Pro, Avid, narzędzi audio i finishingu oraz mapa nauki: [NLE-WORKFLOWS](specialists/nle/NLE-WORKFLOWS.md).

**DERIVED wspólny pipeline**: brief → ingest → logging/selects → assembly → rough cut → fine cut → picture lock → turnovers → sound/color/VFX → conform → QC → delivery → archive. Etapy mają różne pytania. Assembly sprawdza, czy materiał niesie strukturę; rough cut poszukuje rozwiązania; fine cut poprawia relacje i rytm; picture lock stabilizuje podstawę pracy specjalistów. Picture lock nie jest zakazem późniejszej zmiany: późniejsza zmiana wymaga changelist i aktualizacji zależnych dźwięków, VFX, napisów, gradingu i akceptacji.

Resolve jest ważnym punktem odniesienia dzięki bliskości montażu, Fusion, koloru, Fairlight i delivery. Premiere wnosi podejście ścieżkowe, pracę z transkrypcją i ekosystemem Adobe; FCP każe myśleć relacjami primary storyline i connected clips, a także roles; Avid wymaga uważnego rozróżniania source/record, segment/trim i współpracy binów/media. Zasady geometrii cięcia są wspólne, ale skutki domyślnych operacji na zależnościach nie są identyczne. Dlatego agent powinien jawnie ustalać zakres wpływu zamiast naśladować gest interfejsu.

NLE-WORKFLOWS rozdziela klasyczne siedem stron Resolve od stanu aktualnej strony produktu (Resolve 21 z Photo), szkoleń Resolve 20 i lokalnego snapshotu dokumentacji skryptowej. Ogłoszenie Resolve 21.1 o AI assistants/API jest **ogłoszeniem producenta**, nie wynikiem naszego uruchomienia. Nie należy z niego wywodzić, że FrameCut ma działający adapter ani że dowolny agent może sterować dowolną lokalną instalacją.

## 5. Czas, audio, kolor i finishing

[CODE-AND-CONTRACTS](CODE-AND-CONTRACTS.md) podaje rachunek czasu i jawne operacje. Najważniejszy detal implementacyjny: master frames i źródłowe PTS są różnymi zegarami. Zaokrąglanie każdej klatki do stałej liczby próbek audio może akumulować drift; zaokrągla się absolutne granice. Mixed FPS wymaga wyboru między zachowaniem rzeczywistej długości a reinterpretacją prędkości. Kontakt sheet nie sprawdza jakości optical flow ani rytmu speed ramp.

**DERIVED workflow audio**: najpierw zrozumiałość i ciągłość dialogu, potem spójne room tone/ambience, świadomie ułożone efekty i muzyka, dopiero dalej dynamika, barwa, routing, stemsy oraz pomiar delivery. Redukcja szumu może pogorszyć spółgłoski, agresywna kompresja może uwypuklić tło, a automatyczny ducking może pompować w oddechach. Każdy krok potrzebuje A/B odsłuchu i zachowanego oryginału. Pomiar loudness i true peak nie ocenia narracji ani naturalności.

Docelowe LUFS wynikają z konkretnej specyfikacji dostawy. Nie zmieniać domyślnych tolerancji obecnego FrameCut w ogólną normę broadcast. W [QA-BENCHMARKS](specialists/nle/QA-BENCHMARKS.md) opisano rozbieżność podręcznika Fairlight z definicją short-term w EBU i osobno projektowe oraz źródłowe tolerancje.

**DERIVED workflow koloru**: zidentyfikować źródło i jego interpretację, ustalić working/output space, zrobić technical balance/exposure/matching, a potem look i świadome odstępstwa. LUT jest funkcją transformacji, nie zamiennikiem decyzji o ujęciu. Błędne oznaczenie full/legal range nie jest drobną kosmetyką; podobnie wpisanie tagu Rec.709 nie dokonuje konwersji pikseli. Automatyczne dopasowanie twarzy do średniej nie wie, czy scena ma być celowo nienaturalna. Obecny FrameCut nie oferuje potwierdzonego pełnego HDR finishingu; funkcja wymagająca tego workflow trafia do sprawdzonego NLE/specjalisty.

## 6. Agentowy model pracy i wymiana

Propozycja nie zastępuje istniejącego project v1. [editorial-intent.schema.json](editorial-intent.schema.json) to **zewnętrzny RFC**, a [przykłady](examples/editorial-intents.json) rozdzielają intent od rzeczywistego native API. Są też [11 niezależnych przykładów native-shaped](examples/native-operations.json), każdy z warunkami i oczekiwanym rezultatem. Wszystkie pozostają NOT_RUN w silniku.

OTIO powinno służyć wymianie struktury, FFmpeg wykonaniu określonej kompozycji, a NLE operacjom specyficznym dla jego modelu pracy. FFmpeg nie staje się pełnym Resolve przez samą obecność filtrów. OTIO nie staje się rendererem przez obecność efektu w strukturze. AAF/FCPXML/EDL nie gwarantują pełnej migracji pluginów, keyframes, fontów, gradingu i routingu. Adapter musi deklarować poziom: wierny odpowiednik, przybliżenie, workflow hybrydowy lub brak praktycznego odpowiednika. [F01][F06][R14][R16][R17][R18]

Szczególny kontrprzykład: FrameCut realizuje transition jako nakładanie faktycznych zakresów, a OTIO transition wymaga innego odwzorowania zakresów/handles. Sama równość duration nie sprawdza źródeł i pozycji. Inspekcja eksportu pokazała także kandydat do testu trailing gap — wniosek z kodu, nie odtworzony błąd. [R08][R14][R28]

Współpraca zachowuje jednego właściciela master timeline. FrameCut wysyła do obecnego Motion Graphics/future FrameMotion dokładny placement, lokalną długość/FPS, format i locks; dostaje hash-bound render/projekt i QA. Zmiana długości sceny jest change request. Tylko FrameCut ocenia ripple oraz zależności i wydaje nową rewizję. Creative Studio zachowuje brief i kontekst. Szczegóły i zgodne mapowanie nazw: [CONTRACT-FINDINGS](specialists/repo/CONTRACT-FINDINGS.md) oraz [CODE-AND-CONTRACTS](CODE-AND-CONTRACTS.md).

## 7. Walidacja i wdrażanie

Pięć benchmarków obejmuje wywiad z J/L-cutami, reklamę z motion, multicam z osobnym audio, screen recording VFR oraz długi film z ripple w środku. Mają dane, oczekiwane operacje, wyniki i progi; pozostają **NOT_RUN**. Nie nadano im PASS na podstawie tego, że istnieją testy autora lub przykładowy JSON. Ocena techniczna obejmuje frame count, długość, local sync, gaps/black frames, retime, napisy, loudness, clipping, color metadata i decode. Osobna ocena redakcyjna obejmuje sens, emocję, rytm, uczciwość i ciągłość.

[Katalog repozytoriów](specialists/repo/REPOSITORIES.md) podaje konkretne pliki, API, pin/licencje, ograniczenia i odrzucenia. Rekomendacja zależności nie jest jej instalacją, a przejęcie metody nie oznacza kopiowania kodu. Licencje kodu, wag i assetów należy sprawdzać niezależnie. [IMPLEMENTATION_HANDOFF](IMPLEMENTATION_HANDOFF.md) dzieli zadania P0/P1/P2 z właścicielem, wejściami/wyjściami, zakresem plików, fallbackiem i acceptance test.

Najbliższa właściwa kolejność to: test semantyki istniejącego kodu → benchmark i screening → round-trip/loss reports → decyzja o podziale wtyczek → nowe typy operacji i adaptery. Priorytetu nie ma nowy efekt, który maskuje niepewne zegary lub źródła.

## 8. Zakres i brakujące dowody

Kompendium jest syntezą publicznych źródeł, nie przeglądem wszystkich kursów internetu. Ograniczenia nie zamykają warsztatu do Resolve: porównanie programów oraz audio/finishing jest merytoryczną częścią NLE-WORKFLOWS. Nie obejmuje pełnego szkolenia operatora każdego programu.

Nie wykonano renderów, NLE-native import/export, testów runtime Studio, pomiarów wydajności, screeningu ani odsłuchu. Własne sprawdzenia dotyczą raportu, przykładowych struktur i rachunku. Faktyczne liczniki, link check i końcową recenzję podaje [README](README.md), [COVERAGE-MATRIX](COVERAGE-MATRIX.md), [REVIEW](REVIEW.md) i [VERIFICATION](VERIFICATION.md). Żadna z tych granic nie jest ukryta w ogólnym „gotowe”.
