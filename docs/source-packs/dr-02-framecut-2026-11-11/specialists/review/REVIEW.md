# DR-02 — niezależna recenzja końcowa

REVIEW_STATUS: PASS_WITH_LIMITATIONS

Data: 2026-11-11. Recenzent: świeży agent Codex, model odziedziczony z hosta; dokładna nazwa modelu nie została ujawniona recenzentowi. To **nie jest recenzja Claude**, zatwierdzenie architektury przez Claude ani wykonanie claudex-loop. Zastosowano Superpowers `verification-before-completion`.

Werdykt dotyczy treści badania i kontraktów przedstawionych jako propozycje. Nie certyfikuje runtime FrameCut, aplikacji NLE, renderów, pełnej implementacji JSON Schema ani jakości obejrzanego/odsłuchanego filmu. Otwarte major: **0**. Otwarte minor wymagające poprawki przed przekazaniem badania: **0**. Jeden major i trzy minor zgłoszono wcześniej; ich poprawki sprawdzono ponownie w ograniczonym rereview.

## Zakres i metoda

Baza wszystkich ścieżek względnych w tym dokumencie:

`[DR-02 research package root]`

Przeczytano pełny `PROMPT.md`, `SCOPE-CLARIFICATION.md`, `COMPREHENSIVE-REPORT.md`, `CODE-AND-CONTRACTS.md`, `IMPLEMENTATION_HANDOFF.md`, `COVERAGE-MATRIX.md`, `editorial-intent.schema.json`, wszystkie cztery pliki `examples/*.json`, trzy raporty `specialists/repo`, trzy raporty `specialists/craft`, oba raporty `specialists/nle` oraz ich rejestry źródeł. Po finalizacji odczytano również scalony rejestr i `VERIFICATION.md`. Rejestr NLE nie został pominięty mimo późniejszego zapisu.

Recenzja obejmowała ręczną analizę semantyki, świeży odczyt przypiętego kodu przez GitHub, odczyt pierwotnych dokumentów web oraz własne krótkie kontrole parserem JSON i arytmetyką wymierną. Nie importowano ani nie uruchamiano pobranego kodu. Nie instalowano zależności, nie wykonywano renderów, NLE, uploadów ani zmian w repozytoriach produktu. Recenzent zapisuje wyłącznie `specialists/review/`.

## Findings i ponowna kontrola

### R1 — major, zamknięty: native ripple zmienia sequence.duration

Pierwotnie `CODE-AND-CONTRACTS.md:50` i `:57` oraz oczekiwany wynik przypadku ripple w `examples/native-operations.json` sugerowały osobną decyzję o długości sekwencji. Było to sprzeczne z `fc_edit.shift`, które wykonuje `seq['duration'] += delta`; wywołują je native trim/remove z ripple. Dowód: [fc_edit.py, pin 4611c9c, L38–48 i L119–150](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_edit.py#L38-L48).

Wymagana naprawa: podać rzeczywisty skutek native op, zmienić expected JSON i generator, zachowując NOT_RUN. Po poprawce tabela podaje trim 300→280 i extract 300→200; niezależny fixture A/B podaje 200→180. Ponowny odczyt potwierdził te wartości. To zamknięcie błędu dokumentacji, nie wykonany test silnika.

### R2 — minor, zamknięty: niespójny długi benchmark w handoff

`IMPLEMENTATION_HANDOFF.md:127` wcześniej wskazywał +5 klatek/90 minut, podczas gdy B5 w `specialists/nle/QA-BENCHMARKS.md:169–173` definiuje +90 klatek w frame90000 przy długości 100min6s. Wymagana naprawa: ujednolicić dane albo nazwać odrębny test. Handoff obecnie wskazuje dokładnie B5; sprawdzono ponownie.

### R3 — minor, zamknięty: delta slip w klatkach źródła wymaga CFR

Gałąź slip w `editorial-intent.schema.json` i `examples/editorial-intents.json` używa `delta_source_frames` z FPS źródła. Bez ograniczenia mogłaby sugerować konwersję VFR przez nominalny rate. `CODE-AND-CONTRACTS.md:61` obecnie dopuszcza tę formę wyłącznie dla potwierdzonego CFR; VFR wymaga rzeczywistej mapy PTS albo odmowy. Ograniczenie przeczytano i uznano za wystarczające dla opisanego RFC, nie za formalną walidację tego warunku przez JSON Schema.

### R4 — minor, zamknięty: zakres zależności nie był jednoznaczny dla każdej intencji

Gałęzie roll/slip/slide/freeze oraz trim z ripple nie posiadają własnego `affected_lanes`. Wymagana naprawa: jawne domyślne scope, pre/postconditions i odmowy zamiast domysłu kompilatora. Dodany podrozdział `CODE-AND-CONTRACTS.md:65–77` określa wpływ na linked/absolute/anchored events, captions, source bounds, locks i konflikty. Odróżnia native scope od propozycji i od walidacji strukturalnej. Ponowna kontrola potwierdziła usunięcie niejednoznaczności w zakresie badania.

## Pokrycie pełnego promptu

„Pokryte” poniżej oznacza dostarczoną, ocenioną treść, nie runtime PASS.

| Punkt | Ocena i dowód | Zachowana granica |
|---|---|---|
| 1. Cel i obecny produkt | Pokryte w COMPREHENSIVE-REPORT oraz CURRENT-STUDIO: standalone/specjalista, publiczny pin, wersje pakiet/runtime/schema, README/AGENTS/manifesty. | Nowe osobne repo FrameCut/FrameMotion Unknown; cache nie udaje aktywnej sesji. |
| 2. Metoda i źródła | 88 rekordów, 86 różnych URL, komplet wymaganych pól, 88 identyfikatorów użytych w głównych raportach. Są źródła EN i polski wywiad SFP, dokumentacja, kod i praktycy. | Liczba rekordów nie oznacza niezależności źródeł; te same podręczniki bywają użyte w różnych zakresach. |
| 3A. Dramaturgia | CRAFT, GLOSSARY i RECIPES rozdzielają intencję, wykonanie, reakcję, rytm, pauzę, ciągłość i decyzję „zostaw”. | Heurystyki mają wyjątki; brak automatycznego rankingu najlepszego dubla. |
| 3B. Rodzaje produkcji | CRAFT §5 oraz receptury obejmują fabułę, dokument/wywiad, reklamę/produkt, tutorial, multicam/podcast, muzykę, showreel i social. | Brak jednego narzuconego hook/body/CTA lub beat-cut template. |
| 3C. Ingest | Inwentarz/hash/backup, logging, selects, proxy, relink, sync, metadane i rozróżnienie source media/source clip/instance. | Oryginały zachowane; odtworzenie realnego archiwum NOT_RUN. |
| 3D. Edycja | 100-hasłowy słownik, tabela przed/po, native envelope, intencje NLE i jawny wpływ na sąsiadów/lanes. | Pełne track targeting, multicam, nesting i nowe first-class ops nie są przypisane obecnemu FrameCut. |
| 3E. Czas | Rational FPS, PTS, source/timeline, DF/NDF, VFR, mixed rates, samples, handles, retime/reverse/freeze/ramp i interpolacja. | Sampling/optical flow nie mają dowodu jakości z samego contact sheet. |
| 3F. Audio | Dialogue, room tone, ambience, SFX/music, fades, gain, EQ/dynamics/de-essing/NR, ducking, routing/stems i metryki. | Pomiar oddzielony od odsłuchu; profil benchmarku nie jest uniwersalną normą LUFS. |
| 3G. Kolor/finishing | NLE §7, receptury i słownik obejmują transforms, matching/scopes/LUT/log/RAW, SDR/HDR, range, scaling/reframe/stabilizację i tekst. | Technical correction oddzielona od looku; pełny HDR nie jest obiecaną funkcją FrameCut. |
| 3H. Pipeline | Brief→archive, strony Resolve i rewizje po picture lock mają właścicieli oraz artefakty. | Uwzględniono nowe Photo w21, stare podręczniki20 i lokalny snapshot SDK2025. |
| Doprecyzowanie NLE | Merytoryczne różnice modeli Resolve/Premiere/FCP/Avid oraz Pro Tools/Nuke/Baselight, nie ranking nazw. | Zakres SDK za licencją/formularzem pozostaje Unknown. |
| 4. Receptury | 18 receptur; każda ma wszystkie 11 pól. Selekcja poprzedza timeline; są błędy, naprawy, warianty i QA. | Receptury są własną syntezą, próby medialne NOT_RUN. |
| 5. Kod i operacje | Pipeline analysis→decision→plan→JSON→validate→compile→preview→QA→export; FFmpeg/OTIO/API, tabela odpowiedników, 14 rodzin intencji i 11 native-shaped cases. | Sidecar RFC nie jest przyjmowany przez native CLI; pełny validator i engine execution NOT_RUN. |
| 5. Odwracalność | Immutability, revisions, undo, stale conflicts, idempotency receipt proposal, checkpoints/cache/dependency invalidation opisane. | CAS nie jest utożsamiony z idempotencją; minimalny DAG nie udaje gotowej funkcji. |
| 6. Granice i wymiana | CRAFT/QA rozdzielają detekcję, rozpoznanie i narrację; EDL/XML/FCPXML/AAF/OTIO mają loss/bake i round-trip plan. | Brak bezstratności obiecanej dla dowolnych efektów; nie oglądano ruchu ani nie słuchano mediów. |
| 7. Współpraca | Jeden master FrameCut, istniejący brief Studio, obecni owners audio/captions/assets, scoped Motion i revision propagation. RFC zawiera wymagane pola wymiany. | Handles/color/font/seed extensions i osobna wtyczka FrameMotion są propozycjami; hash/font UNBOUND oznaczono. |
| 8. Repo/licencje | Konkretne piny/pliki/API/I-O/dependencies/licencje/utrzymanie/odrzucenia oraz rozróżnienie metody, instrukcji, dependency i kopii kodu. | Licencja kodu nie jest licencją każdego modelu, wag lub assetu; niczego nie zainstalowano. |
| 8. Benchmarki | Pięć wymaganych scenariuszy, operacje, expected outputs, techniczne i redakcyjne kryteria, źródłowe/projektowe tolerancje. | Wszystkie pięć NOT_RUN; wymagany real-time ogląd/odsłuch pozostaje do przyszłego wykonania. |
| 9. Wynik i handoff | Wieloczęściowe kompendium, mapa nauki, repo/odrzucenia, schemat/przykłady, QA, macierz produktu i 10 zadań P0/P1/P2. | Handoff opisuje owner/I-O/files/deps/constraints/fallback/acceptance; nie autoryzuje wdrożenia. |

## Niezależny sample fact-check

Poniższe sprawdzenia wykonano w tej recenzji, nie przejęto jako PASS od autorów. Pin kodu Studio: `4611c9c4ed44579b8a2c0224c9276d955fccd8d6`. Kod tylko czytano.

| Twierdzenie | Świeże źródło pierwotne i locator | Wynik |
|---|---|---|
| source_in to PTS ticks z time_base/start_pts, nie indeks klatki | [fc_core.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_core.py), L154–162 | Potwierdzone w formule span_seconds. |
| Native apply jest ograniczoną tablicą z zamkniętym envelope i końcową walidacją kopii | Ten sam fc_core.py, L429–469 | Potwierdzone: ≤500, op/sequence/id/value, deepcopy, locks, validate. |
| Ripple aktualizuje także długość sekwencji | [fc_edit.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_edit.py), L38–48,119–120,149–150 | Wykryty R1; raport poprawiony. |
| Rampa ma dodatnie rational speeds i integralną mapę źródłową; trim zachowuje remainder | [fc_time.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_time.py), L55–71,79–93,110–129 | Potwierdzone; nie oznacza wykonania interpolacji jakościowej. |
| Native variable-speed audio zmienia pitch | [fc_audio.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_audio.py), L32,48–53 | Potwierdzona jawna continuous-varispeed policy i source map. |
| Motion request ma local0/global placement, a binding sprawdza context/hash/frames/geometry | [fc_render.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py), L87–137 | Potwierdzone; handles envelope poprawnie opisano jako rozszerzenie. |
| Technical QA nie sprawdza narracji; target loudness jest warunkowy | Ten sam fc_render.py, L404–426 | Potwierdzone. Raport nie utożsamia tego z local sync lub odsłuchem. |
| EDL/OTIO export jest ograniczony, a trailing gap ma kandydat do osobnego testu | [framecut.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/framecut.py), L88–138 | Potwierdzone w kodzie: końcowy check do previous, nie seq.duration. Nadal nie jest to reprodukcja. |
| OTIO available/source/trimmed/visible/parent ranges mają odmienne role | [OTIO Time Ranges](https://opentimelineio.readthedocs.io/en/latest/tutorials/time-ranges.html), Clips: source_range i visible_range | Potwierdzone; widoczny zakres może uwzględniać przejścia. |
| Obecna strona produktu to Resolve21 z Photo, a 21.1 AI jest komunikatem producenta | [Produkt](https://www.blackmagicdesign.com/products/davinciresolve), What’s New; [komunikat 2026-09-08](https://www.blackmagicdesign.com/media/partial/release/20260908-03), akapity otwierające | Potwierdzone; raport nie zamienia zapowiedzi w działający adapter FrameCut. |
| Premiere SequenceEditor insert/overwrite/remove/clone mają minimum25.6 | [Adobe SequenceEditor](https://developer.adobe.com/premiere-pro/uxp/ppro-reference/classes/sequenceeditor), wskazane metody | Potwierdzone w oficjalnym API. |
| EBU−23, różne tolerancje QC/live i true peak nie tworzą jednego celu dla wszystkich filmów | [EBU R128-2023](https://tech.ebu.ch/docs/r/r128.pdf), punkty h–i,m | Potwierdzone: ±0.2LU pomiar/QC, ±1LU warunkowo, −1dBTP linear production. |
| EBU Short-term to3s, Momentary0.4s | [EBU Tech3341-2023](https://tech.ebu.ch/docs/tech/tech3341.pdf), §2.2 | Potwierdzone; nie przejmowano rozbieżnego Short30s z Fairlight. |
| Amend nie wymaga konfliktu w każdym dokumencie i ostrożnie stosuje muzykę pod wywiadem | [Wywiad IDA, Christine Fugate, 2002-09-01](https://documentary.org/feature/cut-above-kate-amend-creative-contributions-documentary-editors), pytania conflict/music | Potwierdzony kontekst i wyjątek; nie uniwersalny zakaz muzyki. |
| Murch w rozmowie z Duerr preferuje sprawdzenie sceny przed temp music | [CineMontage, 2004-05-01](https://cinemontage.org/visual-music-walter-murch/), pytania intuitive rhythm/temp track | Potwierdzona praktyka konkretnego montażysty, a nie norma wszystkich gatunków. |

Niezależna próba ponownego dostępu do FFmpeg przez web zakończyła się timeoutem, a bezpośredni HTTPS resetem połączenia. Nie przypisuję jej udanego ponownego fact-checku. Rejestr autora wskazuje wcześniejszy odczyt oficjalnego HTML i hashe; ograniczenie ponownego dostępu nie zostało ukryte. Wymagane minimum pięciu kluczowych twierdzeń sprawdzono ponad ten zakres w innych źródłach pierwotnych.

## Świeże kontrole liczb i rejestru

- W agregacie: 88 unikalnych ID i 86 URL; brak wymaganych pól: 0; niezdefiniowane cytowania: 0; niewykorzystane ID w głównych raportach: 0. Dane agregatu odpowiadają czterem rejestrom po pominięciu dodanego pola `used_in`.
- Słownik: 100 odrębnych ID G001–G100. Receptury: 18, każda 11 ponumerowanych pól. Benchmarki: dokładnie B1–B5.
- Parser JSON odczytał schema i przykłady; ręczna inspekcja rozdzieliła 14 intencji RFC od 11 native-shaped cases. Wszystkie native cases mają NOT_RUN; nie oceniano ich przez fc_core.validate.
- Własny rachunek: B5 180000×1001/30000=6006s; po dodaniu90 klatek wynik ma288432144 próbek48kHz. Body Motion[12,132) ma120 klatek, render z handles144. Subtitle source126000..162000 przy TB1/90000 mapuje się z10..20 na0..10 po opisanym trimie.
- Świeży odczyt 14 wskazanych installed files: 14/14 hashy zgodnych z zapisanymi hashami przypiętego GitHub. To ograniczone porównanie, nie kwalifikacja całego pluginu lub uruchomionej sesji.
- Handoff: 10 zadań z polami celu, właściciela, wejść/wyjść, zależności, zakresu plików, ograniczeń/fallbacku i acceptance.

## Ograniczenia werdyktu i zamknięcie pakietu

Pełny zewnętrzny JSON Schema validator, runtime/native transaction tests, rendery, pomiary mediów, round-trip w konkretnych NLE, odsłuch i ogląd: **NOT_RUN**. Idempotency wrapper, dependency DAG, handles-aware Motion, nowe intencje i backendy wymagają przyszłego wdrożenia i testów; raport konsekwentnie traktuje je jako propozycje. Nie badano każdej pozycji rejestru ponownie niezależnie — wykonano próbkę powyżej oraz sprawdzenie spójności całego rejestru.

W chwili zapisu tej recenzji lead kończy techniczne opakowanie: README, wynik bounded link check i pełne `verify_research.py`. Recenzent nie uruchomił pełnego weryfikatora przed kompletnością tych plików i nie ogłasza jego wyniku. Lead ma po skopiowaniu recenzji wykonać końcową kontrolę i zapisać rzeczywisty rezultat. Jeżeli kontrola wykryje merytoryczną rozbieżność lub zmieni się treść ocenionych kontraktów, ten werdykt nie obejmuje automatycznie nowej treści.

Brak dalszej naprawy merytorycznej wymaganej przez tę recenzję. Materiał nadaje się do przekazania jako badanie z jawnymi ograniczeniami, po zakończeniu opisanej kontroli technicznej pakietu.
