# IMPLEMENTATION_HANDOFF — FrameCut profesjonalny montaż

2026-11-11. **Badanie / propozycje do decyzji architekta. Bez wykonanej implementacji.** Claude pozostaje głównym architektem; nie uruchomiono CLI Claude i nie uzyskano jego review. Żaden plan tutaj nie jest zgodą na instalację, migrację, publikację ani upload. Zakres bieżącego zadania kończy się na artefaktach badawczych.

## Punkt startowy

Źródło: publiczny main Studio `4611c9c4ed44579b8a2c0224c9276d955fccd8d6` (2026-11-11T07:20:22Z). Bazowy prefiks **B**: `plugins/framecore-work-creative-studio/skills/opencut-video-studio/`. Ścieżki zaczynające się od B niżej są ścieżkami względem potwierdzonego repo Studio, nie lokalizacją nowej wtyczki. Nowe repo FrameCut/FrameMotion: **Unknown, adresów nie podano**. Przed pracą odświeżyć commit i porównać zmiany; nie zakładać, że pin pozostał main.

Czytać w kolejności: `COMPREHENSIVE-REPORT.md`, `specialists/craft/CRAFT.md`, `specialists/craft/RECIPES.md`, `CODE-AND-CONTRACTS.md`, `specialists/repo/CONTRACT-FINDINGS.md`, `specialists/nle/QA-BENCHMARKS.md`, `REVIEW.md`. Rejestr źródeł zawiera zakres faktycznego odczytu. Testy autora odczytane w kodzie nie są naszym PASS.

Nie budować nowego master clock, intake, caption engine ani ogólnego routera. Wbudowany FrameCut już ma ingest, analizę, native edits, frames/storyboard, retime, binding motion, render jobs, QA oraz ograniczony export. Rozwój powinien rozróżniać: **wiedzę warsztatową**, **instrukcje agenta**, **adapter/semantykę operacji**, **testy**.

## Backlog P0 — poprawność i granice kontraktu

### P0-1 — semantyka edycji i differential fixtures

- Cel: zachować źródłowe zakresy, sync i locks podczas złożonych zmian, zanim pojawią się nowe skróty edycyjne.
- Właściciel: FrameCut; architekturę zatwierdza Claude, wykonawca przyszłego kodu zgodnie z zasadami projektu.
- Wejścia: natywny project v1, `fc_core.py`, `fc_edit.py`, `fc_time.py`; synthetic cases z tego raportu.
- Wyjścia: zestaw testów before/after i spisana semantyka sequence.duration, absolute/anchored events, transition crossing, audio/caption dependencies.
- Zależności: aktualny pin i probe fixtures; bez mediów klienta.
- Pliki potwierdzone: B`assets/framecut/fc_core.py`, `fc_edit.py`, `fc_time.py`; `plugins/framecore-work-creative-studio/tests/framecut_development_test.py`. Proponowany nowy plik testowy: `tests/framecut_editorial_semantics_test.py` w pluginie, o ile repo nie ma nowszego odpowiednika.
- Ograniczenia/fallback: bez zmiany schema_version1; konflikt → plan + czytelny diff, nie heurystyczna naprawa.
- Akceptacja: split+undo zachowuje źródło, ripple+crossing event odmawia atomowo, locked clip niezmieniony, stale revision nie zapisuje, długości i sub-PTS remainder dokładne; zero runtime crash na błędzie wejścia.

### P0-2 — wykonać pięć benchmarków i screening

- Cel: oddzielić poprawną strukturę od gotowego filmu.
- Właściciel: FrameCut QA + Caption Studio + Audio Production; człowiek lub uprawniony reviewer ogląda/słucha.
- Wejścia: specyfikacje benchmarków wywiad, produkt/motion, multicam, VFR/screen, długi drift/ripple; licencjonowane lub własne testowe media z hashem.
- Wyjścia: receipts, decoded measurements, loss reports i review z pokryciem zakresów. Obecnie wszystkie te próby **NOT_RUN**.
- Zależności: jawna zgoda na wykonanie przyszłego kodu, dostępny FFmpeg/NLE, zgodność fontów i źródeł.
- Pliki: potwierdzone B`assets/framecut/fc_render.py`, `fc_audio.py`, `fc_captions.py`, testy autora; proponowane `tests/fixtures/editorial/` i manifest fixture, bez dużych plików w rejestrze Hipson.
- Ograniczenia/fallback: bez automatycznego PASS z frame count. Brak NLE/odsłuchu → wynik techniczny plus REVIEW_REQUIRED.
- Akceptacja: zgodne frame counts/PTS/sync, brak niezamierzonych black/gaps i clipped speech, napisy zgodne ze źródłem, kolor i audio według konkretnego delivery; pełen real-time screening; tolerancje z QA-BENCHMARKS.

### P0-3 — round-trip i jawna utrata informacji

- Cel: import/eksport nie obiecuje stratności zerowej; sprawdzić także końcową lukę sekwencji.
- Właściciel: FrameCut interchange adapter.
- Wejścia: obecny export EDL/OTIO i trzy klipy, trailing gap, transition, independent audio, marker, caption, retime.
- Wyjścia: machine-readable loss matrix per format i porównanie zrekonstruowanych zakresów.
- Zależności: oficjalny OTIO i wersja adaptera; native NLE round-trip osobno.
- Pliki potwierdzone: B`assets/framecut/framecut.py` funkcja export; proponowane `tests/framecut_interchange_semantics_test.py`.
- Ograniczenia/fallback: EDL tylko do reprezentowalnych picture cuts; reszta JSON+CSV+reference movie+loss report. Trzeba konwertować transition semantics FrameCut↔OTIO.
- Akceptacja: pełny sequence end wraz z gap albo jawny loss; każde źródło/trim/marker porównane; unsupported effect wyraźnie odrzucony, nie cicho spłaszczony. Własny test API i NLE import nie mogą mieć jednej etykiety PASS.

### P0-4 — kontrakt właścicieli i zgodność instalacji

- Cel: utrzymać jeden brief i master timeline podczas przyszłego wydzielenia FrameCut/FrameMotion.
- Właściciel: Claude architekt; Studio coordination; FrameCut i obecny Motion Graphics.
- Wejścia: owner map, motion-request/attach-motion, manifest wersji, raport read-only porównania instalacji.
- Wyjścia: decyzja RFC zaakceptowana przez użytkownika/architekta w właściwym workflow; mapowanie migracyjne nazw, nie cichy nowy router.
- Zależności: adresy nowych repo i decyzja o podziale; dziś Unknown.
- Pliki potwierdzone: `skills/pipeline-core/references/studio-integration-policy.md`, `skills/workflow-orchestrator/SKILL.md`, B`SKILL.md`, B`assets/framecut/fc_render.py`. Nowe manifesty repo dopiero po ustaleniu adresu i zakresu.
- Ograniczenia/fallback: w badaniu nie zmieniono instalacji. Wyświetlana nazwa FrameCut nie dowodzi osobnej paczki. Bez migracji pozostać przy obecnym ownerze.
- Akceptacja: jedno project.id, jedna revision/master FPS, brak podwójnego intake, request/return wraca do FrameCut, brak samowolnych zmian accepted locks.

## Backlog P1 — operacje i warsztat

### P1-1 — intencje insert/overwrite/roll/slip/slide

- Cel: zapewnić jawne operacje zawodowe, bez swobodnego przepisywania całej sekwencji przez model.
- Właściciel: FrameCut editing.
- Wejścia: sidecar RFC `editorial-intent.schema.json`, capability report, project v1 i jawny target lanes.
- Wyjścia: walidowany intent → minimalna native transaction + impact/diff; request receipt dla idempotencji.
- Zależności: P0-1; rozstrzygnięcie source units, handle policies i track-lock semantics. RFC nie jest dziś przyjmowany przez CLI.
- Pliki: istniejące B`assets/framecut/fc_edit.py`, `fc_core.py`; proponowany `fc_intent.py` i testy dopiero po review architektury.
- Ograniczenia/fallback: bez raw JSON Patch, shell/filtergraph z modelu. Przy braku op bezpieczny jawny set_sequence candidate po diff/dry-run, albo plan-only.
- Akceptacja: wszystkie before/after z CODE-AND-CONTRACTS; brak możliwości cichego przesunięcia niezależnej muzyki/napisu; stale retry nie dubluje insert.

### P1-2 — selekcja źródeł przed timeline

- Cel: utrzymać sens wypowiedzi i wybierać materiał według celu, nie score ciszy/beatów.
- Właściciel: FrameCut wsparty Story/Screenplay i Shot Sequence.
- Wejścia: brief ze Studio, log źródeł, evidence z niepewnością, sąsiedni kontekst transkrypcji i actual viewing/listening intervals.
- Wyjścia: selects/stringout, decision ledger, odrzucone alternatywy i confidence/review_needed.
- Zależności: obecne `propose`, `analyze`, `plan-cuts`; brak nowej ASR instalacji.
- Pliki potwierdzone: B`references/editor-craft.md`, B`assets/framecut/fc_editor.py`; proponowany reference `editorial-decision-cards.md` pod B`references/`.
- Ograniczenia/fallback: wrażliwa mowa bez pewnej transkrypcji → zachować kontekst i zlecić sprawdzenie; brak „best take” z samego contact sheet.
- Akceptacja: zestaw par dobry/zły cut, zachowana negacja/warunek, pauza narracyjna chroniona, reakcja nie podszywa się pod inny moment; reviewer może prześledzić source→claim→decyzję.

### P1-3 — dźwięk i kolor jako jawne conform steps

- Cel: oddzielić technical correction od estetyki oraz current native DSP od przyszłego profesjonalnego finishingu.
- Właściciel: Audio Production (kierunek), Motion Graphics/Toolbox (wykonanie dostępnego audio), FrameCut (integracja); colorist/NLE przy gradingu.
- Wejścia: source color tags/scopes, waveform, target delivery spec, approved intent.
- Wyjścia: derived audio/color assets, latency/source map, measurement+perceptual review.
- Zależności: P0 QA; do pipeline niedopuszczone automatyczne denoise/grade bez uzasadnienia.
- Pliki potwierdzone: B`assets/framecut/fc_audio.py`, `fc_render.py`, `skills/audio-production-director/SKILL.md`; nowy color adapter to propozycja osobnego modułu, nie obecna funkcja.
- Ograniczenia/fallback: HDR w obecnym FrameCut odrzucone; przygotować sprawdzony SDR asset albo plan NLE. Denoise zniszczy consonants → wrócić do oryginału/łagodniejszego wariantu.
- Akceptacja: input/output transforms jawne, metadata zgodna z pikselami, stała synchronizacja po restauracji, stems mają te same granice, target LUFS zależy od delivery; odsłuch obowiązkowy.

### P1-4 — motion handles i revision propagation

- Cel: dodawać sceny Motion bez konkurencyjnego zegara i bez odcinania handles.
- Właściciel: FrameCut contract; obecny Motion Graphics jako dostawca; przyszły FrameMotion dopiero po mapowaniu.
- Wejścia: istniejący motion request, source hashes, master placement, body/handles, color/alpha/font contract.
- Wyjścia: wersjonowany envelope/binding i change request na zmianę długości.
- Zależności: P0-4; `motion-handoff-rfc.json` jest przykładem, nie dzisiejszą zgodną komendą.
- Pliki potwierdzone: B`assets/framecut/fc_render.py`; propozycje rozszerzeń wersjonować w istniejącym kontrakcie, bez zmiany znaczenia v1.
- Ograniczenia/fallback: current attach bez handles-aware update wymaga dokładnego body render; nie wgrywać 144 klatek jako oczekiwanego body120.
- Akceptacja: przypadek 120+12+12, alpha straight/premultiplied, font mismatch, stale brief, +30 scene frames, locked downstream; przy błędzie zero silent conform.

## Backlog P2 — poszerzenie warsztatu i backendów

### P2-1 — adaptery NLE i multicam

- Cel: wykorzystać Resolve/Premiere/FCP/Avid tam, gdzie profesjonalny backend daje potrzebną funkcję.
- Właściciel: FrameCut adapter; użytkownik wybiera zainstalowany/posiadany program.
- Wejścia: capability probe, wersja NLE/SDK, media+timeline contracts, jasno ograniczony operation set.
- Wyjścia: native project/turnover, import receipt, error/loss report, reference export.
- Zależności: P0-3 i P0-4; API availability/edition/release aktualizowane przy wdrożeniu.
- Pliki: **proponowane** B`assets/framecut/adapters/resolve.py`, `premiere.py`, `fcpxml.py`, `aaf.py`; obecne repo tych modułów nie potwierdza. Nie tworzyć wszystkich bez konkretnego use case.
- Ograniczenia/fallback: Resolve 21.1 announcement nie jest dowodem dostępnego SDK w tym hoście. FCPXML nie równa się pełne sterowanie UI FCP. Avid panel/AAF nie równa się dowolny headless edit. Brak aplikacji → plan/OTIO+loss report.
- Akceptacja: cztery osobne fixtures per NLE; imports/exports sprawdzone w faktycznej wersji; manual conform tam, gdzie plugin effects/retime nie przechodzą. Multicam synchronizuje źródła, a wybór kamery ocenia reviewer.

### P2-2 — cache odcinków i długi projekt

- Cel: po zmianie środka filmu renderować tylko realnie zależne części, zachowując końcową zgodność.
- Właściciel: FrameCut render/cache.
- Wejścia: dependency DAG, semantic hashes, długi benchmark, approved locks.
- Wyjścia: precyzyjne invalidation spans i measured reuse receipts.
- Zależności: P0-1/P0-2; istniejący cache pozostaje bazą.
- Pliki potwierdzone: B`assets/framecut/fc_render.py`; proponowany graf zależności w oddzielnym module wyłącznie po pomiarze potrzeb.
- Ograniczenia/fallback: crossfade/temporal effects poszerzają zależność; cały mix może wymagać ponownego pomiaru integrated loudness. Fallback pełny render przy niepewnej granicy.
- Akceptacja: +90 frames insert/ripple w frame90000 w 100min6s fixture B5, zgodność pełnego i częściowego renderu w decoded semantics, brak drift, niezmienione źródła/cache receipts; benchmark czasu nie zmyślony.

## Integracje: błędy, retry, limity, koszt i weryfikacja

| Integracja | Błędy / retry | Limity i koszt | Weryfikacja / fallback |
|---|---|---|---|
| native CLI | typowany błąd, stale hash/revision → replan; timeout po sprawdzeniu stanu; nie retry validation failure | obecnie <=500 ops, <=6h sekwencja, <=2000 eventów/lane; czas CPU/dysk; brak płatnego wywołania w tym badaniu | dry-run + actual QA; plan-only |
| FFmpeg | brak filtra/codec, decode failure, nonmonotonic PTS; max jeden uzasadniony retry transient stage | build-dependent; licencja/codec zależne od kompilacji; CPU/dysk mierzyć | version/buildconf/filter capability + pełny decode; neutral intermediate albo odmowa |
| Resolve scripting | brak app/edition/API/method, niedziałające job ID | licence app, render hardware/time; bez gwarancji bezpłatnego headless | GetVersion+metody i mini fixture; interchange/human conform |
| Premiere UXP | wersja API, transaction failure, denied permissions | lokalna licencja i host; API limit sprawdzić aktualnie | feature-detect + fixture, brak raw UI macro jako równoważności |
| FCPXML/AAF/OTIO | schema/version, missing media, effect unsupported | biblioteka/licencja osobno od NLE; adapters nie wszystkie w core OTIO | loss report+native import; reference movie i edytowalny native JSON |
| Motion/Toolbox | stale request, frames/dim/alpha/font mismatch | obecny lokalny runtime; rendering budget ustalony z tasku | request-bound hash+QA; nie przyjmować częściowego wyniku jako final |

Wszystkie przyszłe operacje zewnętrzne obowiązuje bieżąca zgoda użytkownika; ten handoff jej nie rozszerza. Zmiany współpracy z Claude nie zostały wykonane, dlatego nie edytowano Shared ani globalnych lekcji. Materiał przekazania pozostaje tutaj zgodnie z zakresem DR-02.
