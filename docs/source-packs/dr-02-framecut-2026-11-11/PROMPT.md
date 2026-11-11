Przeprowadź pogłębiony Deep Research i przygotuj praktyczne kompendium warsztatu profesjonalnego montażysty, ze szczególnym uwzględnieniem DaVinci Resolve oraz porównaniem Adobe Premiere Pro, Final Cut Pro i Avid Media Composer. Następnie przełóż tę wiedzę na agentowy montaż w kodzie dla wtyczki FrameCut i jej współpracy z FrameCore Works Creative Studio oraz FrameMotion.

To zadanie badawcze. Wykonaj badanie i syntezę, nie poprzestawaj na planie, liście linków ani rankingu programów. Raport po polsku, z zachowaniem angielskich terminów technicznych.

1. KONTEKST I CEL

Rozwijam FrameCore Works Creative Studio oraz dwie nowe wtyczki: FrameCut i FrameMotion. Ten research jest przeznaczony przede wszystkim dla FrameCut.

Roboczy podział odpowiedzialności:
- Creative Studio: brief, koncepcja, scenariusz, kierunek kreatywny i koordynacja.
- FrameCut: analiza źródeł, selekcja materiału, montaż, nadrzędna oś czasu, integracja obrazu/dźwięku, finishing i delivery.
- FrameMotion: zamówione sceny animowane, typografia, motion graphics i compositing.

To założenia do porównania z aktualnymi materiałami, a nie opis potwierdzonej implementacji. FrameCut ma pracować samodzielnie i jako specjalista Studio. Nie ograniczaj go do shortsów, automatycznego usuwania ciszy ani kinetic captions.

Repozytorium Creative Studio:
https://github.com/FrameCoreWorks/framecore-works-creative-studio

Jeśli dostęp jest możliwy, przeczytaj README, AGENTS.md, manifesty i pliki związane z FrameCut, montażem, timeline, napisami, audio, renderem i QA. Zapisz commit i datę. Adresów repozytoriów nowych wtyczek nie podano: nie wymyślaj ich. Oddziel kod na GitHub od wersji zainstalowanej. Brak dostępu nie blokuje kompendium; stan implementacji oznacz Unknown.

Najważniejsze pytanie: jak profesjonalny montażysta podejmuje decyzje i jak agent może przełożyć je na jawne, odwracalne operacje bez utraty sensu, ciągłości i kontroli nad materiałem?

2. METODA I WIARYGODNOŚĆ

Przeszukaj oficjalne podręczniki i szkolenia Blackmagic Design, Adobe, Apple i Avid, materiały zawodowych montażystów, breakdowny, wywiady o procesie, publiczne repozytoria i dokumentację narzędzi. Zbadaj różnice metod pracy, nie tylko nazwy przycisków.

Celuj w co najmniej 40 rzeczywiście wykorzystanych, wartościowych źródeł. Nie dopełniaj liczby słabymi linkami. Szukaj po angielsku i polsku. Zachowaj klasyczne zasady montażu, a wersje programów, API, licencje i aktualne wymagania delivery weryfikuj na dzień badania.

Przy ważnych ustaleniach podawaj URL, autora, datę, wersję i rozdział lub timestamp, jeśli został sprawdzony. Oddziel materiał obejrzany, transkrypcję i opis. Tytuł tutorialu nie dowodzi jego treści.

Oznaczaj SOURCED, DERIVED, PRACTITIONER i Unknown. Opinie praktyków zachowuj z kontekstem. Twierdzenia techniczne potwierdzaj w dokumentacji, kodzie autorów lub innych źródłach pierwotnych. Przedstaw rozbieżności i kontrprzykłady. Nie deklaruj przeszukania wszystkich poradników w internecie.

3. KOMPENDIUM MONTAŻYSTY

Zbuduj słownik około 100 pojęć PL/EN: definicja, przykład, zastosowanie i typowy błąd. Uwzględnij cały proces:

A. Dramaturgia i decyzje:
intencja sceny, selekcja dubli, emocja, przekaz, rytm, pauza, napięcie, kolejność informacji, elipsa, ciągłość czasu/przestrzeni, oś akcji, eyeline, kierunek ruchu, cut on action, match cut, jump cut, cutaway, B-roll, reakcje, J-cut, L-cut i kontrapunkt. Pokaż, kiedy ciąć oraz kiedy pozostawić ujęcie.

B. Różne rodzaje produkcji:
fabuła, dokument i wywiad, reklama, produkt, tutorial/screen recording, multicam/podcast, teledysk, showreel i social video. Dla każdego określ cel, sposób selekcji, konstrukcję, tempo, rolę audio oraz kryteria jakości. Nie narzucaj wszystkim hook/body/CTA ani cięcia na każdy beat.

C. Ingest i organizacja:
inwentaryzacja, sumy kontrolne i backup, metadane, biny, nazewnictwo, logging, transkrypcja, markery, selects/stringout, proxy/optimized media, relink, multicam i synchronizacja timecode/waveform. Oddziel nośnik źródłowy od klipu i instancji klipu na timeline. Zachowuj oryginały.

D. Operacje edycyjne:
source/record monitor, in/out, three-point i four-point editing, insert/overwrite, append, split, trim, ripple, roll, slip, slide, lift/extract, gaps, linked selection, track targeting/locking, snapping, nesting/compound clips, multicam switching i undo/redo. Pokaż przed/po na osi czasu oraz wpływ na inne ścieżki.

E. Czas:
rational FPS, timebase, timecode versus frame index, drop-frame/non-drop-frame, VFR/CFR, mixed frame rates, próbkowanie audio, source time versus timeline time, handles, retiming, reverse, freeze, speed ramps, frame blending i optical flow. Omów synchronizację, rounding, drift, duration i granice klipów.

F. Dźwięk:
dialogue editing, room tone, ambience, SFX, music editing, J/L-cuts, crossfades, gain/automation, EQ, compression, de-essing, redukcja szumu, ducking, loudness/true peak, routing, stemsy i synchronizacja. Rozróżnij pomiar od oceny odsłuchowej. Nie traktuj jednego LUFS jako uniwersalnego celu.

G. Kolor i finishing:
podstawy zarządzania kolorem, input/output transforms, balans, ekspozycja, kontrast, matching ujęć, scopes, LUT versus grading, log/RAW, SDR/HDR, full/legal range, scaling, stabilizacja, reframing, napisy i grafika. Wyjaśnij ograniczenia automatycznego gradingu i rozdziel korekcję techniczną od decyzji estetycznej.

H. Pipeline zawodowy:
brief → ingest → logging/selects → assembly → rough cut → fine cut → picture lock → turnovers → sound/color/VFX → conform → QC → delivery → archive.
Wyjaśnij rolę stron Media, Cut, Edit, Fusion, Color, Fairlight i Deliver w Resolve oraz istotne różnice w pozostałych programach. Uwzględnij poprawki po picture lock.

4. RECEPTURY I REGUŁY DECYZYJNE

Opracuj 15–20 praktycznych receptur, m.in. wywiad z B-rollem, rozmowę wielokamerową, reklamę produktu, scenę ciągłej akcji, tutorial ekranowy, montaż do muzyki, pracę z materiałem o różnych FPS i końcowy conform.

Każda receptura:
cel → potrzebne źródła → decyzje montażowe → kolejność operacji → parametry/jednostki → warianty → błędy → naprawa → reprezentacja agentowa → QA → źródła.

Pokaż, jak ocenić materiał i wybrać ujęcie, zanim zostanie zbudowany timeline. Dla reguł twórczych podaj warunki, wyjątki i kontrprzykłady. Nie przedstawiaj usuwania wszystkich pauz, skracania każdego ujęcia ani dużej liczby przejść jako automatycznej poprawy filmu.

5. PRZEŁOŻENIE NA KOD

Zaprojektuj model: analiza materiału → decyzja redakcyjna → plan montażu → operacje JSON → walidacja → kompilacja do backendu → preview → QA → finalny eksport.

Zbadaj FFmpeg/ffprobe, narzędzia analizy audio/obrazu, OpenTimelineIO i odpowiednie biblioteki lub silniki timeline. Sprawdź oficjalne możliwości skryptowania Resolve i pozostałych NLE, ale oddziel je od pracy lokalnej bez zainstalowanego programu.

FFmpeg jest ważnym kandydatem wykonawczym, nie obowiązkowym odpowiednikiem każdej funkcji NLE. Dla techniki podaj:
decyzja montażowa → operacja timeline → dane → filtr/biblioteka/adapter → ograniczenia → test.

Przypisz: odpowiednik wierny, przybliżenie, workflow hybrydowy albo brak praktycznego odpowiednika. Zwróć uwagę na frame-accurate seeking, GOP, stream copy versus re-encode, trim/atrim, PTS, concat, transitions, retiming obrazu i audio, napisy i color metadata. Nie zakładaj, że samo istnienie filtra daje jakość zawodową.

Zaproponuj wersjonowany schemat JSON i spójne przykłady dla: trim/split, insert/overwrite, ripple/roll/slip/slide, speed curve/freeze, transform keyframes, transition, gain/ducking i subtitles. Określ semantykę, preconditions, postconditions, wpływ na ścieżki i obsługę błędów. Kod nieuruchomiony oznacz jako przykład wymagający walidacji.

Uwzględnij immutability źródeł, identyfikatory rewizji, undo, idempotencję, conflict detection, checkpoints, cache i aktualizowanie tylko zależnych fragmentów. Agent ma odczytywać właściwości plików, zamiast pytać o dane dostępne w metadanych.

6. GRANICE AUTOMATYZACJI I WYMIANA

Rozróżnij wykrycie cięcia, rozpoznanie treści, wybór najlepszego dubla i decyzję narracyjną. ASR, diarization, beat detection i analiza obrazu dostarczają dowodów z niepewnością, nie nieomylnych decyzji.

Kontakt sheet nie zastępuje oglądania ruchu; transkrypcja nie zastępuje oceny tonu wypowiedzi. Zaproponuj lokalizowanie momentów wymagających dokładnego oglądu i odsłuchu. Nie zmieniaj sensu wypowiedzi przez skróty.

Zbadaj EDL, XML/FCPXML, AAF i OTIO: co przenoszą, jakie informacje tracą, które efekty trzeba wyrenderować i jak sprawdzić round-trip. Nie zakładaj bezstratnej wymiany między wszystkimi programami.

7. WSPÓŁPRACA WTYCZEK

Zaproponuj wspólny, wersjonowany kontrakt:
project_id, schema_version, revision, timeline_owner, asset_id/hash, fps_num/fps_den, jednostki czasu, zakresy [in, out), source time i timeline time, handles, retiming, rozdzielczość, color space, alpha mode, audio sample rate, fonty, seed, provenance i accepted locks.

FrameCut jest właścicielem nadrzędnego montażu w projekcie montażowym. Do FrameMotion wysyła brief, dokładny zakres, długość, format, handles i wymagania alfa/audio. Odbiera render i/lub projekt edytowalny, manifest oraz QA. Opisz zmianę długości sceny i propagowanie rewizji bez dwóch konkurencyjnych zegarów.

Creative Studio zachowuje kontekst kreatywny i koordynację. Nie twórz drugiego intake, osobnych kopii briefu ani dublujących się routerów. Sprawdź istniejących właścicieli napisów, audio i assetów przed proponowaniem nowych skilli.

Zaplanuj storyboard/contact sheet całego montażu oraz podgląd ruchu w miejscach krytycznych. Uwzględnij akceptację planu, jeśli wymaga jej istniejący workflow; nie wymagaj zatwierdzania każdego cięcia. Zachowaj zaakceptowane fragmenty przy poprawkach.

8. REPOZYTORIA I WALIDACJA

Znajdź konkretne moduły, SKILL.md, cookbooki, parsery timeline, edytory, analizatory i narzędzia QC. Dla najlepszych podaj URL, commit/tag, istotne pliki, wejścia/wyjścia, CLI/API, zależności, licencje, utrzymanie i ograniczenia.

Preferuj rozwiązania lokalne i bezpłatne. Oddziel przejęcie metody, adaptację instrukcji, zależność i kopiowanie kodu. Sprawdzaj osobno licencje modeli, wag i assetów. Nie dodawaj projektu tylko dlatego, że jest popularny.

Zaproponuj benchmarki:
- wywiad z B-rollem i J/L-cutami;
- produkt/reklama z muzyką i grafiką FrameMotion;
- multicam z osobnym dźwiękiem;
- screen recording z VFR i adaptacją formatu;
- dłuższy montaż ujawniający drift oraz poprawkę ripple w środku timeline.

Dla każdego określ dane, oczekiwane operacje, wynik i testy. Kontroluj frame count, długość, A/V sync, niezamierzone gaps/black frames, przejścia, retiming, napisy, loudness, clipping, color metadata i odtwarzalność pliku. Osobno oceniaj narrację, emocję, rytm i ciągłość.

Tolerancje opisz jako źródłowe lub projektowe. Testy autora oddziel od własnych. Niewykonane testy oznacz NOT_RUN, a nie PASS. Końcowa ocena wymaga także oglądu i odsłuchu w czasie rzeczywistym.

9. WYNIK I GRANICE

Dostarcz:
- pełne kompendium i słownik;
- mapę poradników z konkretnymi umiejętnościami;
- receptury, reguły decyzyjne i tabelę operacja → kod;
- katalog repozytoriów i odrzuceń;
- propozycję schematu JSON i kontraktów wymiany;
- checklisty QA, benchmarki i plan round-trip;
- macierz „potwierdzone w obecnej wtyczce / luka / Unknown”;
- backlog P0/P1/P2 i IMPLEMENTATION_HANDOFF dla Codex.

Każde zadanie wdrożeniowe ma mieć cel, właściciela, wejścia, wyjścia, zależności, zakres plików potwierdzony lub proponowany, ograniczenia, fallback i test akceptacyjny. Dla integracji opisz błędy, retry, limity, koszt i weryfikację. Rozdziel wiedzę, instrukcje agentowe, kod adapterów i testy.

To research, bez zmian w repozytoriach, instalacji, uruchamiania pobranego kodu, płatnych usług, uploadu prywatnych danych, pushu, deployu i publikacji. Możesz czytać publiczne źródła. Nie obchodź logowania i paywalli. Twórz własną syntezę, nie kopię kursów.

Jeśli środowisko umożliwia tworzenie plików, przygotuj kompendium Markdown, rejestr źródeł CSV/JSON i handoff. W przeciwnym razie podaj pełną treść w odpowiedzi. Zapisz datę badania, ograniczenia i macierz pokrycia. Przy limicie długości podziel wynik na ponumerowane części bez ukrywania braków.

Zacznij właściwe badanie teraz, bez pytań o konkretny film. Priorytetem jest warsztat montażysty i jego wiarygodne przełożenie na FrameCut.