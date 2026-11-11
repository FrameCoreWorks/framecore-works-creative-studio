# FrameCut: od decyzji montażowej do operacji i dowodu

Data badania: 2026-11-11. **DERIVED** oznacza propozycję tego badania. Fakty o obecnym kodzie są z inspekcji przypiętego publicznego main, nie z wykonania. Zob. `specialists/repo/CURRENT-STUDIO.md` i jego rejestr Rxx. **Żaden przykład z tego rozdziału nie został uruchomiony przez FrameCut ani NLE.** Własny test rachunkowy jest opisany oddzielnie.

## 1. Zachować istniejący kontrakt

Przypięcie: `4611c9c4ed44579b8a2c0224c9276d955fccd8d6`, commit 2026-11-11T07:20:22Z. `plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/README.md`, `schema.json`, `fc_core.py`, `fc_time.py` i `fc_edit.py` opisują/dostarczają istniejący projekt v1. Package 1.174.1, runtime VERSION 1.1.0 i schema_version 1 to różne osie wersji. Pole projektu to `id`, FPS to `{num,den}`, a `source_in` to **PTS ticks aktywa**, nie indeks klatki. Nie przemianowujemy tych pól w v1. [R03][R04][R06]

Proponowany `editorial-intent.schema.json` jest **zewnętrznym sidecarem RFC 0.1**, nie nowym formatem projektu ani plikiem przyjmowanym przez CLI. Zawiera intencję, zakres wpływu i dowody. Adapter ma z niego zbudować dozwoloną tablicę `apply`; nie wolno wysłać sidecara do istniejącego `apply`. Projekt pozostaje źródłem czasu i rewizji. Pole sidecara `project_id` mapuje się na `project.id`, `fps_num/fps_den` na `sequence.fps.num/den`.

W projekcie asset oznacza niezmienne medium z hashem i probe. Klip źródłowy jest wybranym zakresem tego medium; instancja na timeline ma własne ID i pozycję. Dwie instancje nie są dwiema kopiami pliku. Relink zmienia lokalizator po sprawdzeniu tożsamości; inne bajty wymagają nowego asset_id. **DERIVED:** wykorzystać źródłowy hash, metadane i referencję do oryginału także w proxy; prosty zgodny czas trwania nie dowodzi zgodności kadru.

## 2. Łańcuch decyzji i audytu

1. **Analiza**: probe, hash, PTS, transkrypcja z niepewnością, marker akcji, kadry kontaktowe. ASR/scene detect/beat detect to obserwacje. Nie są rankingiem dubli.
2. **Decyzja redakcyjna**: co widz ma zrozumieć/poczuć, który fragment to uzasadnia, jaka alternatywa została odrzucona, dlaczego pauza została zachowana. Wybór przed budową timeline.
3. **Plan**: selects/stringout → assembly → rough/fine cut. ID decyzji łączy zakres źródła z konkretną instancją.
4. **Operacje**: typowana transakcja, bazowa rewizja, jawne zależności, plan skutków na inne ścieżki.
5. **Walidacja**: schema/semantyka → dry-run → porównanie zmiany z zaakceptowanymi fragmentami.
6. **Kompilacja**: backend capability report; jeśli nie umie zachować sensu operacji, odmowa albo jawny render pośredni.
7. **Storyboard całego filmu**: realne kadry, znaczące momenty, ending i mapowanie pokrycia; obowiązują istniejące zasady akceptacji aktualnej planszy.
8. **Podgląd i QA**: preview filmu jest opcjonalne według istniejącego workflow, ale ruch/odsłuch krytycznych miejsc trzeba sprawdzić przed oceną jakości. Finalny render wymaga pełnego oglądu i odsłuchu.
9. **Eksport**: manifest, techniczny QA, osobna ocena percepcyjna, loss report, relink i archiwum.

Nie dodawać drugiego intake, kopii briefu ani approval każdego cięcia. Creative Studio zachowuje intencję i stan. FrameCut ma master timeline; Caption Studio ma craft/QA napisów; Motion Graphics implementację animacji i dźwięku; Audio Production kierunek audio; Asset Manifest inwentarz. [R09][R10][R11][R12][R33] Nowa samodzielna wtyczka FrameMotion pozostaje projektem integracji o niepodanym repo, a nie potwierdzoną instalacją.

## 3. Czas: rachunek, który musi być jawny

**DERIVED**, zgodnie z istniejącym wyborem racjonalnych zegarów i zakresem półotwartym:

- Dla master FPS `N/D` czas klatki `f` to dokładnie `f*D/N` sekund. Nigdy nie akumulować float `1/29.97`.
- Zakres `[in,out)` ma `out-in` klatek. Klatka `out` należy do następnego zakresu. Zero duration jest punktem/markerem, nie klipem.
- Dla źródła o `time_base=a/b`, `source_in` oznacza tick. Czas względem początku streamu: `(source_in-start_pts)*a/b + source_remainder`. Nominalny FPS źródła nie daje mapy VFR.
- Łączny czas źródła przy zmiennej prędkości to całka prędkości po czasie timeline. Przy liniowych odcinkach wystarczy suma trapezów. Odwrotność mapy służy napisom; nie używać jednego globalnego mnożnika przy rampie.
- Granice audio obliczyć od absolutnego czasu i zaokrąglić raz do próbek. Dla 48 kHz i 30000/1001 FPS jedna klatka to 1601.6 próbki. Powtarzanie `round(1601.6)=1602` przez 100000 klatek daje **40000 próbek = 5/6 s** błędu. Zaokrąglenie absolutnej końcowej granicy daje 160160000 próbek.
- 1800 klatek przy 30000/1001 to 60.06 s, nie 60 s. Timecode to etykieta, frame index to pozycja. Drop-frame zmienia numerację, nie usuwa klatek obrazu. Adapter timecode musi znać framerate i DF/NDF, a nie zgadywać z separatora.
- 24000/1001→25: zachowanie realnego czasu wymaga resamplingu kadencji; interpretacja klatek 1:1 skraca czas o ok. 4.096% (prędkość rośnie o ok. 4.271%). To różne świadome decyzje, zwłaszcza dla dialogu i muzyki.
- Optical flow tworzy szacowane klatki: artefakt na skrzyżowanych rękach nie jest błędem długości. Frame blending może dać podwójne kontury. Ocena obu wymaga ruchu, nie tylko contact sheet.

Źródło OTIO rozróżnia `available_range`, `source_range`, `trimmed_range`, `visible_range` i pozycję w parent; transition może poszerzyć widoczny zakres względem trymu. To pomaga projektować adapter, ale **OTIO nie jest rendererem**. [F06]

## 4. Semantyka operacji: przed/po, sąsiedzi i błędy

Wszystkie poniższe liczby są **oryginalnym fixture DERIVED** przy 25 FPS, bez przejść i locków. A=[0,100), B=[100,200), C=[200,300); każdy ma zapas źródła. `δ=10` klatek = 0.4 s. Audio zakotwiczone w klipie śledzi klip, audio absolutne wymaga jawnej polityki. Nie nazywać tabeli obecną pełną funkcjonalnością CLI.

| Operacja | Przed → po | Warunki, ścieżki, postcondition | Status / typowy błąd |
|---|---|---|---|
| Split A w 50 | A→A-left[0,50), A-right[50,100) | brak zmiany duration, źródło/animacja ciągłe, nowy stabilny ID; aktualizacja caption sources/anchors | natywny `split_clip`; granica 0/100 to błąd |
| Trim A in=10,out=90 | A→[10,90), B nadal 100 | źródło +10 klatek; luki [0,10) i [90,100) jawne | natywny `trim_clip,ripple:false`; nie nazywać luki błędem, jeśli zamierzona |
| Ripple trim A 10..90 | A→[0,80), B→[80,180), C→[180,280) | usunięte 20, źródło A +10; zdarzenia przecinające granicę mogą blokować | natywny `shift` zmienia sequence.duration o −20: 300→280; conflict oznacza brak zapisu [R05] |
| Insert X=25 w 50 | A-left0..50, X50..75, A-right75..125, B125..225 | split na przecięciu, wszystkie wybrane zależności +25; locked track kolidujący → odmowa | adapter RFC, brak natywnego `insert` |
| Overwrite X=25 w 50 | A-left0..50, X50..75, A-right75..100, B100..200 | długość stała; A-right source+75; modyfikacja tylko jawnie wybranych lanes | adapter RFC; przypadkowe nadpisanie dialogu |
| Roll A/B +10 | A0..110, B110..200 | duration sum stała, A +handle, B in+10 i duration−10; niezależny dialog zachować jeśli wybrano picture only | adapter RFC; brak handle→reject |
| Slip A +10 | A0..100 bez zmiany pozycji | źródło A in+10 i out+10; przypięte zdarzenia pozostają czasowo, ich treść wymaga recheck | adapter RFC; przesuwanie klipu zamiast źródła |
| Slide B +10 | A0..110, B110..210, C210..300 | B zachowuje źródło/duration; A out+10, C in+10 i duration−10 | adapter RFC; musi mieć sąsiadów i handles |
| Lift B | gap100..200, C200..300 | pozostałe pozycje stałe; zależności reject/detach/remove | native remove ripple=false, polityka jawna |
| Extract B | C100..200 | późniejsze objęte lanes −100; crossing event → konflikt | native remove ripple=true zmienia także sequence.duration: 300→200 [R05] |
| Freeze A w50 na25 | A-left0..50, hold50..75, A-right75..125 | source nie konsumowane w hold, dźwięk hold cichy; downstream +25 | native; captions wypowiedzi nie mogą rozciągnąć się automatycznie na hold |
| Transition A→B overlap10 | A0..100, B90..190 | overlap10 wymaga prawidłowych źródeł; suma ekspozycji != końcowa długość | natywny `replace_clip`+transition; nie dodawać przejścia bez przesunięcia B |

W RFC `slip.delta_source_frames` dopuszczamy wyłącznie potwierdzone źródło CFR o podanym rate; dla VFR trzeba wybrać rzeczywistą granicę PTS z decoded map albo odmówić tej postaci intencji. Nie wolno użyć nominalnego FPS jako zastępstwa mapy. Przykład projekcji słowa przed/po trimie: `examples/subtitle-time-map.json`; to syntetyczny rachunek bez sfabrykowanego hasha i bez importu do runtime.

Nesting/compound clip: **DERIVED** wrapper ma własny zakres lokalny, ale mapę do master. Nie zagnieżdżać ukrytych zegarów bez mapy. Obecny prosty FrameCut nie jest pełnym track-targeting/multicam systemem NLE. Linked selection, snapping, źródłowy/rekordowy monitor i three/four-point editing są intencjami interfejsu; agent powinien zamienić je na precyzyjne zakresy i target lanes. Przy four-point mismatch nie wolno samemu wybrać retime, trim lub ripple; decyzja wynika z briefu albo wymaga jednego wyjaśnienia konsekwencji.

### Wspólne preconditions i polityka zależności RFC 0.1

**DERIVED normatywna semantyka propozycji**, nie dodana funkcja runtime. Każda intencja wymaga tej samej bazowej rewizji i sequence FPS, istniejących ID/hash/probe, dozwolonego źródłowego zakresu, nieujemnych długości oraz zachowania runtime i creative locks. Przed kompilacją odczytać wszystkie lanes/anchors/caption sources, utworzyć impact report i sprawdzić go po zbudowaniu kandydata. Zero częściowego zapisu. Nieznane zależności, crossing event lub brak uchwytów → `DEPENDENCY_CONFLICT` / `HANDLE_UNAVAILABLE` w proponowanym adapterze; stare native typed errors pozostają bez zmiany.

| Gałąź bez affected_lanes w RFC | Jednoznaczny zakres domyślny | Postcondition / odmowa |
|---|---|---|
| trim z ripple=true / osobny ripple intent | Jak native: wszystkie **absolutne** lanes clips/audio/overlays/texts po starym końcu; anchors podążają za właścicielem raz; wycięty fragment klipu i jego captions remapowane | sequence.duration += delta; crossing absolute event i anchor poza nowym clip range → reject. Jeśli RFC affected_lanes nie odpowiada takiemu native scope, v0.1 nie kompiluje i raportuje unsupported scope. |
| freeze | Jak native: silent hold + wszystkie absolute downstream lanes przesunięte; anchors zgodnie z native split; brak dialogu/napisów w hold | duration += hold; brak źródłowej klatki, kolizja ID, chroniona zależność lub crossing event → reject |
| roll | Dwa sąsiednie base clips wraz z ich linked source audio; niezależne audio/overlays/texts zachowują absolutny czas. Captions tych clipów są przeliczane z source map; inne pozostają | suma długości i końcowy czas sekwencji stałe. Anchored dependent, który wymagałby przestawienia poza pierwotną absolutną pozycję lub wyjścia poza źródło, → reject w v0.1; operator może wcześniej jawnie go odpiąć/przebudować |
| slip | Wybrane źródłowe okno picture i linked source audio; placement/duration wszystkich eventów bez zmian; source captions przeliczone | source span mieści się w aktywie; source-semantic dependents wymagają ponownej oceny. Nieobsługiwany VFR frame delta → reject, nie konwersja przez nominalny FPS |
| slide | Środkowy clip+linked audio zmienia placement, źródło/duration zachowane; dwa sąsiednie clipy+linked audio trymowane. Niezależne absolute lanes bez zmian | całkowity zakres i duration stałe; w RFC0.1 anchored dependent na którymkolwiek z trzech zmienianych clipów → reject do czasu jawnej rewizji dependentu; brak sąsiada/handles/lock → reject |

Insert/overwrite mają affected_lanes, ale nie deklarują jeszcze działającego dowolnego track modelu: adapter v0.1 musi odmówić nieobsługiwanej kombinacji. Transform/gain/subtitles nie zmieniają placement; transition wymaga jawnego nowego placement dwóch clipów i kontroli ich independent sound. Ten dokument definiuje znaczenie, a zamknięty JSON Schema sprawdza jedynie kształt; kontrola pre/post i typed errors to przyszły validator domenowy.

## 5. Operacja → backend → ograniczenie → test

Podstawy SOURCED: ffprobe ujawnia streams, frames i liczniki; `read_intervals` nie gwarantuje dokładnego seek. [F03] Przy transkodowaniu `-ss` może dekodować od wcześniejszego seek point i odrzucać nadmiar; stream copy zachowuje inny zakres i nie pozwala stosować filtrów. [F01] `trim/atrim` nie zerują PTS, `setpts/asetpts` to osobny etap. `concat` filter wymaga segmentów od PTS 0; `xfade` zgodnych parametrów CFR; `atempo` ponad 2 może pomijać próbki. `loudnorm` ma warunki trybu liniowego, a `sidechaincompress` reaguje na drugi sygnał. [F02] Concat demuxer wymaga zgodności strumieni; błędne durations i interframe inpoints mogą psuć połączenie. [F04]

Poniższa mapa to **DERIVED projekt adaptera**, nie dowód jakości samego filtra:

| Decyzja | Dane/operacja | Kandydat | Wierność i ograniczenie | Test akceptacji |
|---|---|---|---|---|
| zachować całe słowo | source PTS + dokładna granica | decode→trim/atrim→PTS reset | wierna granica przy poprawnej mapie, nie stream-copy GOP | porównać numery klatek i próbki na markerach |
| złożyć selects | lista zakresów i pełny mapping | concat po normalizacji | wierny cut; brak gwarancji rytmu | zero obcych ramek, ręczny screening |
| J/L-cut | niezależne source intervals obrazu/audio | oddzielne trim/atrim i mix | wierna struktura, warunek sync | klaśnięcie i granice sylab + odsłuch |
| dissolve | overlap, uchwyty, parametr koloru | xfade/acrossfade | przybliżenie charakteru NLE/color pipeline | środek przejścia, halo i black flash |
| stałe 0.5× | mapa czasu, pitch policy | setpts + atempo lub osobny stem | przybliżenie brzmienia; native ramp ma pitch zmianę | frame map + słuch zrozumiałości |
| speed ramp | krzywa i jej całka | native map lub wyrenderowany retime NLE | hybryda, pitch-preserving/optical flow nieudowodnione | punkty kontrolne mapy, końce i ruch |
| hold | wybrana źródłowa klatka | native freeze/odcinek still | wierne dla obrazu; świadomie bez źródłowego dialogu | hash kadru hold i silent span |
| tracking reframing | trajektoria obiektu | native keyframes po ręcznych/analizowanych punktach | przybliżenie; brak automatic tracking | ogląd obiektu i UI na całej trajektorii |
| ducking muzyki | voice intervals lub sygnał sidechain | native schedule / inny adapter sidechaincompress | różne modele: schedule != detektor głośności | brak pompowania i zachowanie oddechu |
| napisy | source word times + inverse map | Caption Studio + libass/SRT/VTT | styl zależy od formatu/fontu; tłumaczenie osobne | timed words, pełny glyph coverage i safe zones |
| technical color conform | jawne input/output transform i range | color-managed NLE; testowany zscale adapter | hybryda; tag != przekształcenie pikseli | wzorzec, scopes, metadata, display |
| matching emocjonalny koloru | intencja i porównanie ujęć | colorist/Resolve/Baselight | brak automatycznej pełnej równoważności | continuity reel na skalibrowanym torze |
| dialogue restoration | oryginał + wariant po restauracji | Fairlight/Pro Tools lub specialist derived asset | hybryda; szum vs artefakty mowy | A/B odsłuch, latency compensation |
| multicam narracyjny | synchroniczne źródła, role, reaction markers | NLE multicam / przyszły adapter | brak native multicam w sprawdzonym FrameCut | drift start/mid/end, sens reakcji |

FFmpeg to backend wykonawczy. Nie jest dowodem reprodukcji gradingu, pluginów audio, śledzenia czy efektu NLE. W czasie wdrożenia spisać faktyczne `-version`, `-buildconf`, `-filters`, encodery; nie utożsamiać dokumentacji online z lokalnym buildem. Licencja zależy również od opcji builda, opcjonalnych komponentów i sposobu dystrybucji. Nie składać deklaracji „wszystko LGPL” dla paczki z x264. [F05]

## 6. Transakcje, rewizje, undo i cache

Obecne `apply` przyjmuje do 500 zamkniętych operacji `{op,sequence?,id?,value}`. Nie przyjmuje shell string/filtergraph/callback. `fc_core.apply_operations` kopiuje projekt, stosuje operacje, sprawdza stare locks i waliduje wynik. `commit_revision` sprawdza bazową rewizję i zapisuje historię. To **inspekcja kodu**, a nie wykonany test współbieżności.

**DERIVED propozycje**: `request_id` + digest intencji + base revision w sidecar receipt. Ponowienie identycznego request zwraca poprzedni wynik; to nie oznacza ponownego split po stale_revision. Nieznany wynik mutacji → najpierw odczyt historii i ID. Inny hash pod tym samym request_id → conflict. Undo zapisuje nową rewizję odtwarzającą stan, nie usuwa historii. Zmiana istniejącego zaakceptowanego locka wymaga wyraźnego upoważnienia; alias „fix” nie znosi locka.

Cache kluczować źródłami i ich hashami, semantycznymi parametrami, wersjami adaptera/renderera, fontami, color pipeline. Przestawienie napisu powinno unieważnić composite i delivery, nie źródłowy transcode. Obecny silnik ma cache i ogólną invalidację; **minimalne odcinki zależności** są dalszą propozycją, nie potwierdzoną funkcją. W proposal dependency DAG ripple przesuwa temporal dependents, ale nie przelicza niezmienionych źródłowych analiz. Zapis checkpoint po atomowym etapie, limit dysku/timeout i brak nadpisania finali.

Błędy: stale revision→reload/diff/replan; locked content→odmowa zależnej zmiany; source hash mismatch→nowe ingest ID; missing handle→alternatywny cut albo jawnie zaakceptowany synthetic frame; unknown operation→capability fallback do planu; render timeout→jeden wznowiony etap po sprawdzeniu receipt; QA fail→naprawa przyczyny, nie retry tej samej komendy w pętli.

## 7. Kontrakt z FrameMotion / Studio

**DERIVED RFC**: obowiązkowe envelope fields w sidecarze: `project_id`, `schema_version`, `revision`, `timeline_owner`, `asset_id/hash`, `fps_num/fps_den`, `time_units`, `[in,out)`, `source_time`, `timeline_time`, `handles`, `retiming`, `resolution`, `color_space`, `alpha_mode`, `audio_sample_rate`, `fonts`, `seed`, `provenance`, `accepted_locks`. Nie dodajemy ich hurtowo do zamkniętego natywnego schematu v1. `seed:null` oznacza brak stochastycznej generacji, nie powtarzalność gwarantowaną seedem.

Istniejące `motion-request`/`attach-motion` są punktem rozszerzenia, nie konkurencyjnym routerem. Wyjście Motion: render i/lub edytowalny projekt, manifest/hashes, wersje/fonty/zależności, QA i dokładny frame count. Lokalny zegar sceny zaczyna się od 0; jej placement zna wyłącznie master FrameCut. Własny format źródłowy projektu Motion nie jest zmianą master timeline.

Przykład: placement [1000,1120) przy 25 FPS ma 120 klatek=4.8 s. Handles po12 dają render 144 klatki, z body [12,132). Jest to **proponowana obsługa handles**, nie obietnica, że dzisiejsze attach-motion przyjmie taki plik bez nowego jawnego zakresu body. Gdy scena rośnie do150 klatek, Motion zwraca change request (+30), nie przestawia dalszych scen. FrameCut liczy wpływ na muzykę, captions, locks, delivery length i approved board, publikuje nową rewizję/placement i dopiero wtedy nowe request. Odrzucona zmiana zachowuje render źródłowy jako nieprzyjęty wariant, a nie nowy obowiązujący master.

Pełen storyboard pokaże wszystkie sceny i istotne momenty, ale ruch krytyczny wymaga odtworzenia: przejścia, zgranie ust, rampy, tracking, flicker, rolling shutter, napisy na cięciu. Odsłuch krytyczny: J/L join, room tone, plosives, redukcja szumu, ducking, cisza po puencie. Receipt może przechować obejrzane zakresy i osobę; nie może sam dowieść, że ktoś obejrzał lub usłyszał materiał.

## 8. Co rzeczywiście weryfikujemy w tym badaniu

`examples/native-operations.json` zawiera niezależne przykłady do istniejącego API; `examples/editorial-intents.json` — propozycje i ich mapowanie. Weryfikator raportu sprawdza strukturę, referencje, podstawowe rachunki i zadeklarowane statusy. **Nie wykonuje ani nie certyfikuje `fc_core.validate`, nie renderuje mediów, nie potwierdza zgodności NLE.** JSON Schema opisuje ograniczenia struktury; domenowa semantyka czasu pozostaje osobną walidacją. [F07] Formalna walidacja pełnego JSON Schema przez zewnętrzny validator: NOT_RUN (brak instalacji; własny ograniczony structural check nie jest jej zamiennikiem). Ten zakres jest świadomy i zgodny z zakazem uruchamiania pobranego kodu.
