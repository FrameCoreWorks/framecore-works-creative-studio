# DR-02 — Kontrakty istniejące i wymagania migracji

Data: 2026-11-11. Baseline: Studio 4611c9c4ed44579b8a2c0224c9276d955fccd8d6; package1.174.1; runtime1.1.0; project schema1. Inspekcja źródeł, wszystkie runtime/round-trip tests **NOT_RUN**. Dokument nie wprowadza konkurencyjnego schematu JSON.

## Kontrakty do zachowania

| Obecne — SOURCED | Pułapka | Wymaganie migracji — DERIVED |
|---|---|---|
| fps:{num,den}, integer timeline frames, [in,out). [R04][R31] | 29.97 jako exact FPS lub nowy master w milliseconds. | Rational clock i jawne rounding dopiero na granicy backendu. |
| source_in to PTS ticks assetu; start_pts/time_base z probe. [R04] | Użycie nominalnego source frame index dla VFR/nonzero PTS. | Oddzielić source/timeline units; odczytywać metadane. |
| source_remainder to ułamek sekundy poniżej ticka. [R06] | Rounding po każdym split. | Zachować exact remainder i porównać source maps przed/po operacji. |
| Asset+hash oraz osobne event IDs. [R03][R04] | Mylenie pliku z instancją na timeline. | Media identity, source selection i placement mają oddzielne role. |
| apply to ARRAY {op,sequence?,id?,value}, ≤500. [R04] | Nowe op_id/preconditions zostaną odrzucone przez v1. | Envelope RFC otacza native ops; wymaga osobnej walidacji/capability version. |
| CAS base-revision, file lock i immutable history. [R04] | Samoczynne ponowienie na innej rewizji zmienia znaczenie intencji. | Stale→reload/diff/replan. |
| locks to lista base clip IDs. [R04] | Runtime lock nie obejmuje wszystkich approved copy/look/sound. | Zachować odrębne creative locks w Project State. |
| start XOR anchor:{clip,offset}. [R04] | Podwójne przesunięcie anchored event. | Jedna authority placement; jawny konflikt dla straddling absolute event. |
| Motion local start0; global placement w FrameCut. [R07] | Specialist render zawiera drugi global offset. | Oddawać local render, composite raz. |
| Caption source words i corrections osobno. [R10] | Double retime lub tłumaczenie przypięte do obcych word times. | Jedna projekcja; translation wymaga approved copy i phrase/alignment timing. |
| Technical PASS ≠ review ≠ user acceptance. [R07][R32] | Frame count uznany za dowód jakości. | Trzy jawne stany, zakresy i dowody. |

## Dokładny native operation shape

To opis bieżącego kodu, nie nowe nazwy. Każda structural op ma sequence; wszystkie poza set_framing mają id. Atomowa tablica pracuje na kopii; błąd któregokolwiek członu nie zapisuje części projektu. [R04][R05][R31]

| op | value | Semantyka |
|---|---|---|
| split_clip | {frame,right_id} | Absolute sequence frame wewnątrz clipu; right zachowuje source i animation window. |
| trim_clip | {in,out,ripple} | Offsety wewnątrz starego clipu, [in,out). Bez ripple przesuwa start o in; z ripple zachowuje start i przesuwa downstream o skrócenie. |
| move_clip | {start} | Absolute sequence placement; anchors podążają. |
| remove_clip | {ripple,dependents} | dependents=reject/detach/remove; default reject. |
| freeze_frame | {frame,duration,hold_id,right_id} | Wstawia silent held frame, rozcina clip i ripple tail. |
| set_keyframes | mapa parameter→points | Zastępuje animation eventu, resetuje local animation offset. |
| set_speed_curve | [{frame,speed:{num,den}},…] | 2–64 ordered points od0 do duration; rational speed1/4..4; source consumption=całka. |
| set_effects | array {id,version,params,enabled} | Closed versioned effects; brak arbitrary filtergraph/callback. |
| set_framing | {deliverable,framing} | Overrides wariantu, bez drugiego master edit. |

Pozostałe istniejące op: add_sequence, set_sequence, replace_clip, set_captions, set_audio, set_overlays, set_texts, set_brief, set_authorization, set_locks, set_deliverables. Nie istnieją first-class insert/overwrite/roll/slip/slide ani NLE track targeting. Generic replace/set_sequence może opisać wynik, ale nie dowodzi właściwej semantyki operacji. [R04][R05]

**DERIVED wymagania:** roll zachowuje total duration i zmienia wspólny cut point dwóch sąsiadów przy odpowiednich handles. Slip zachowuje placement/duration, zmienia source window. Slide zachowuje source window wybranego clipu, przesuwa placement i zmienia sąsiadów. move_clip nie jest zamiennikiem wszystkich trzech. Każda nowa operacja potrzebuje scope tracks, preconditions, dependent impact, conflict/locks i undo fixture.

## Motion exchange i propagacja zmian

Obecne motion_request zawiera schema_version1, owner=hyperframes-workflow, project_id/revision, sequence/event ID, global_start_frame, local_start_frame0, duration_frames, fps, width/height, alpha, color=SDR bt709, brief i project/sequence/deliverable/brief hashes. bind_motion porównuje history baseline i bieżący context, hash media, decoded frame count, FPS, dimensions i alpha. Niezależny ingest może zwiększyć revision, ale zmiana sequence/brief/deliverable wymaga świeżego requestu. [R07]

**Proponowane rozszerzenia, nie pola obecnego v1:** explicit color primaries/transfer/range; alpha association i test krawędzi; handles body/pre/post z niezależną media duration; font manifest/licences; engine/version i dependency hashes; seed tylko dla rzeczywiście losowej procedury; audio sample rate/channel layout/measured delay; references do accepted locks i provenance zamiast kopii briefu. Obecna stała color nie jest pełną walidacją color management, a obecność alpha channel nie dowodzi prawidłowego matte.

Gdy specialist potrzebuje innej długości, zgłasza propozycję. FrameCut analizuje audio bridges, captions, anchors, transitions, format variants i approval impact; zapisuje nową revision i wydaje nowy request. Stary render pozostaje historycznym assetem. Nie retimować go w ukryciu. Zmieniony element invaliduje zależne cache/QA, nie każdą niezależną scenę. [DERIVED z R04][R07][R09]

## Interchange: semantics przed formatem

OTIO source_range, available_range, visible_range i parent ranges nie są synonimami. OTIO dopuszcza reference poza dostępnym media, więc nie zastępuje native handle validation. OTIO Transition nie skraca ani nie wydłuża Track; FrameCut overlap klipów wpływa na ich wspólny zakres. Mechaniczna podmiana transition→in_offset/out_offset bez przeliczenia cut point i source windows daje inny montaż. [R14][R28]

FrameCut ogranicza EDL/OTIO do picture cuts, zapisuje pominięcia i wstrzymuje złożone retime/transitions. Jego OTIO boundary używa float(fps/start), zachowując source PTS w metadata. Należy sprawdzić długie rational/mixed-rate source maps. Round-trip test sprawdza obecnie tylko duration do końca ostatniego base clip; trailing sequence gap może zostać pominięty. To wniosek z kodu, **nie reprodukcja błędu**. [R08][DERIVED]

Minimalny future test: IDs/hash/relink, track order, source/record in-out, head/interior/tail gaps, rates, handles, audio topology, supported metadata i loss report. Potem import do konkretnej wersji NLE i porównanie renderu/audio. Zapis→odczyt .otio nie dowodzi NLE compatibility. Adapter read support nie implikuje write support. [R08][R14][R16][R17][R18]

## Błędy, retry i limity

- stale_revision: reload/diff/replan, nie retry na nowej bazie bez sprawdzenia intencji.
- stale_source: nowy asset identity i nowa analiza; zachować stare źródło.
- edit_conflict przy ripple: jawny trim/split/move/reanchor dependentu; nie silent skip.
- unknown operation/effect/version: capability gap; bez cichego zamiennika.
- Brak ASR/OTIO: missing capability; istniejący plan/native/CSV/EDL fallback albo osobno zatwierdzona instalacja.
- Lost reply po apply: CAS nie jest idempotency receipt. Proposed wrapper request_id+payload/base hash+saved result ma deduplikować identyczne żądanie i odrzucać changed payload.
- Interrupted render: istnieją cache/jobs; resume tylko unchanged context/source. Changed project→new job/output.
- QA failure: naprawa przyczyny, nie losowy retry.
- Native granice: assets1000, sequences100, lane events2000, fps1..120, sequence6h, ops500. Nie podnosić bez resource/latency benchmark. [R04][R05][R07][R08][R31]

## Backlog dla implementatora

Wszystko poniżej jest **DERIVED proposal, NOT_RUN**. Potwierdzone pliki mają prefix plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/. Testy istnieją w plugins/framecore-work-creative-studio/tests/. Nowy wrapper/schema jest proponowanym plikiem, nie potwierdzoną implementacją.

| Priorytet/cel | Owner; wejścia→wyjścia | Pliki/zależności | Ograniczenie/fallback/test acceptance |
|---|---|---|---|
| P0: RFC→native v1 | FrameCut; intent+baseline→ops+impact | fc_core.py, fc_edit.py; proposed adapter | Unsupported→edit plan/NLE. Unknown field/stale/lock/failed member nie zapisuje partial state. |
| P0: semantic export | FrameCut; native+adapter→export+loss | framecut.py, framecut_test.py; optional OTIO | Fixture trailing gap, nonzero PTS, rational FPS, celowo zamieniony source range. Same duration nie wystarcza. |
| P0: QA beyond duration | FrameCut+Audio+Caption; file→technical/review evidence | fc_render.py, existing tests; proposed QC helper | Expected gap/black intent map i lokalne sync transients; brak odsłuchu→REVIEW_REQUIRED. |
| P1: pełne edit semantics | FrameCut; source+target tracks+delta→transaction | fc_edit.py, fc_time.py, fc_core.py, framecut_development_test.py | Najpierw scope tracks/locks. Undo daje identyczną treść przy nowej revision. |
| P1: Motion contract | FrameCut+FrameMotion; scoped request→render/manifest/QA | fc_render.py, integration policy; proposed schema revision | Backward compatibility i jeden clock; wrong duration/hash/alpha/color/fonts reject albo explicit conform. |
| P1: idempotent receipt | FrameCut; request_id/basehash→saved result | Proposed wrapper przy framecut.py; fc_jobs.py jako istniejący punkt odniesienia | Identical repeat→same receipt; changed payload→conflict. |
| P2: opcjonalny backend/QC | FrameCut; compiled plan→output/check | MLT/PyAV/MediaInfo/libebur128 po kwalifikacji | Bez instalacji na podstawie katalogu; korzyść mierzona na tych samych assetach/acceptance. |

## Benchmarki kontraktowe

1. Długi 30000/1001 master, VFR/nonzero source PTS, audio48kHz, ripple w środku. Porównać exact source maps i lokalne transients początek/środek/koniec.
2. Motion request rN; independent ingest rN+1 kompatybilny, zmieniony sequence/brief/format odrzuca stary return; decoded body i alpha checks.
3. Caption-only correction zachowuje picture cut map/audio, przebudowuje zależny composite/QA; translation ma osobną authority.
4. Roll/slip/slide/overwrite z J-L na innych tracks i locked graphic; failed member nie zmienia całego projektu.
5. Interchange levels: cuts+gaps+tail+markers, następnie audio/overlays, następnie dissolve/ramp; każdy ma osobny capability/loss result.

Wszystkie benchmarki **NOT_RUN**. Contact sheets nie zastępują obejrzenia ruchu i odsłuchu. Implementacja/release/instalacje pozostają poza zakresem tego researchu. [R02]

