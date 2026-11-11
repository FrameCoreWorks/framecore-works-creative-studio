# IMPLEMENTATION_HANDOFF — propozycja dla Codex i architekta Claude

Data: 2026-11-11. Status: **research complete candidate; backlog DERIVED, nie wdrożony**. Żaden punkt tego handoffu nie rozszerza zgody na modyfikację repozytoriów. Claude pozostaje głównym architektem; jego akceptacji ani uruchomienia CLI nie było. Wdrożenie wymaga osobnego zlecenia użytkownika i ustalenia właściwego repozytorium FrameMotion. Nie znamy jego adresu ani katalogu.

## Zasada architektury

Rozszerzyć istniejące role i adaptery, bez drugiego źródła prawdy dla timeline. Publiczny snapshot Studio: `4611c9c4ed44579b8a2c0224c9276d955fccd8d6`, pakiet 1.174.1. Zobacz `specialists/backends/STUDIO-AUDIT.md` oraz `CODE-AND-CONTRACTS.md`. Przed wdrożeniem odświeżyć main i porównać kontrakty; nie zakładać, że snapshot jest aktywną instalacją.

**Potwierdzone ścieżki w publicznym repo** (prefiks `plugins/framecore-work-creative-studio/skills/`):

- `hyperframes-workflow/references/motion-contract-json.md` — istniejący score/storyboard/approval.
- `hyperframes-workflow/assets/motion-quality/score.mjs` — zakresy klatek, score i sampling QA.
- `opencut-video-studio/assets/framecut/fc_render.py` — motion_request/bind_motion/cache.
- `opencut-video-studio/assets/framecut/fc_core.py` — strict schema i rewizje.
- `opencut-video-studio/SKILL.md` — właściciel montażu i handoff.

Wskazane poniżej nowe pliki `contracts/…`, `adapters/…`, `tests/…` to **nazwy proponowane we właściwym przyszłym repozytorium**, nie istniejące pliki ani adresy. Nie dopisywać ich automatycznie do Studio.

## P0 — fundamenty przed obietnicą profesjonalnego renderera

### P0-1. Zgodność request/score i manifest rozszerzenia

**Cel:** przyjąć zlecenie z istniejącego FrameCut bez zmiany globalnej osi. **Właściciel:** Claude zatwierdza architekturę; Codex implementuje; FrameCut zachowuje timeline, motion owner zachowuje score. **Wejścia:** prawdziwy `motion_request`, score, przypięte rewizje, capability table. **Wyjścia:** sidecar, compile report i editable result manifest. **Zależności:** znajomość faktycznego repo FrameMotion i jego wersji; brak duplikacji obecnych engine.

**Pliki:** potwierdzone `fc_render.py`/`fc_core.py` czytać jako kontrakt; proponowane `contracts/frame-motion-sidecar.schema.json`, `adapters/framecut-binding.*`, `tests/contract-roundtrip.*`. **Ograniczenia:** closed keys w FrameCut v1; bez cichego extra-field passthrough do kanonicznego projektu. **Fallback:** sam score i natywny projekt jako explicit manual handoff. **Błędy/retry/limity/koszt:** stale kontekst requestu → nowy request, zero retry attach; wzrost revision po ingest przy niezmienionym kontekście dopuszczalny według bind_motion; schema major unknown → STOP; idempotency hash; lokalna walidacja bez usług płatnych. **Akceptacja:** round-trip zachowuje wszystkie znane pola i unknown sidecar payload, celowo nieobsługiwana required capability odrzucana; przydzielone [900,1140) daje lokalne [0,240), out wyłączony, żadnej modyfikacji sąsiednich eventów.

### P0-2. Czas i deterministyczne renderowanie klatki

**Cel:** ten sam frame number daje ten sam stan sceny bez historii odtwarzania dla kanałów bez symulacji. **Właściciel:** Codex, motion runtime owner. **Wejścia:** rational FPS, score, keyframes, adapter version. **Wyjścia:** `evaluateFrame` i manifest środowiska. **Zależności:** P0-1. **Pliki proponowane:** `core/time.*`, `core/evaluate-frame.*`, `tests/time-and-seek.*`; nie zastępować istniejących helperów jeśli da się je wykorzystać.

**Ograniczenia:** rational contract nie oznacza bitowej zgodności GPU; solver wymaga bake. **Fallback:** jawny CFR obsługiwany przez backend po zgodzie ownera, albo inny backend; brak cichej zamiany 30000/1001 na30. **Błędy/retry/limity/koszt:** invalid fps/out-of-range → błąd danych bez retry; render timeout najwyżej jedno powtórzenie po diagnostyce; 1 worker na początek, limit RAM konfigurowalny; lokalny koszt mierzony s/frame. **Akceptacja:** sekwencja 0,100,20,100 daje identyczne macierze klatki100; 240 klatek=8.008 s; sample48048@48k→frame30; brak błędu kumulacyjnego w 1h testowej osi.

### P0-3. Assety, fonty, kopia i zależności

**Cel:** nie dopuścić zamiany logo/fontu/tekstu ani braków glyphów. **Właściciel:** asset-manifest + motion adapter; caption-studio dla napisów. **Wejścia:** pliki lokalne, SHA256, rights, copy IDs, required glyph set. **Wyjścia:** dependency manifest, font preflight, blokady. **Zależności:** P0-1. **Pliki:** proponowane `preflight/assets.*`, `preflight/fonts.*`, `tests/polish-type.*`.

**Ograniczenia:** `document.fonts.ready/check` nie dowodzi właściwego kroju; shaping i grapheme clusters ważniejsze niż count UTF-16. **Fallback:** jawny approved font substitute albo tekst jako zaakceptowany outline przy zachowanym źródle edytowalnym; brak samowolnego fallback. **Błędy/retry/limity/koszt:** missing file/hash mismatch → STOP, nie pobierać z internetu; load failure one local retry only after cause resolved; limit pliku zgodny z projektem, nie magiczny globalny; koszt lokalny. **Akceptacja:** brak fontu z fixture jest BLOCKED; „Zażółć gęślą jaźń.” identyczne w danych i obrazie; NFD/NFC fixture bez zgubionych znaków; zmiana assetu unieważnia tylko zależne wyniki.

### P0-4. QA z konkretnym defektem i kryterium stopu

**Cel:** połączyć kontrolę techniczną z realnym oglądaniem i odsłuchem. **Właściciel:** motion QA + istniejący output-critic-iteration, bez nowej równoległej bramki. **Wejścia:** 5 benchmarków, export/probe, brief acceptance, locks. **Wyjścia:** QA report z dokumentacją/kodem/testem autora/własnym testem osobno. **Zależności:** P0-2/3. **Pliki:** rozszerzenie istniejącego motion-quality po zgodzie; proponowane `qa/review-manifest.*`, `tests/fixtures/benchmark-*`.

**Ograniczenia:** OCR, klatki i metryki nie dowodzą płynności; cisza może być intencjonalna. **Fallback:** NOT_RUN/needs-human-review, żadnego PASS z próbek statycznych. **Błędy/retry/limity/koszt:** ograniczyć 3 rundy QA i 2 poprawki jednego defektu jako konfigurację startową; po budżecie blocker; lokalny render review mierzony. **Akceptacja:** brak native video/listening zachowuje NOT_RUN; defekt np. obcięte „ą” ma zakres, hipotezę, zmianę i regresję; zaakceptowane elementy bez przyczyny pozostają niezmienione.

### P0-5. Rewizje i accepted locks

**Cel:** zmiana kopii, czasu lub assetu unieważnia właściwy approval i render. **Właściciel:** Studio project state + FrameCut global revision; Codex implementuje adapter, nie nowy approval service. **Wejścia:** stara/nowa revision, dependency DAG i approval evidence. **Wyjścia:** impact diff, nowy sidecar, preserved history. **Zależności:** P0-1/3. **Pliki:** istniejące score/revision helpers do odczytu, proponowane `contracts/change-impact.*`, `tests/locked-revisions.*`.

**Ograniczenia:** hash zmiany pliku nie wyjaśnia znaczenia, a niezmienny filename nie dowodzi niezmiennych bytes. **Fallback:** manual approval dla niejednoznacznej zmiany. **Błędy/retry/limity/koszt:** konflikt revision → odświeżenie ownera, nie last-write-wins; atomic save, zero płatnych usług. **Akceptacja:** duration-change request nie zmienia filmu; aktualizacja fontu oznacza re-review tekstu, a przeniesienie pliku przy tym samym hash nie unieważnia automatycznie koncepcji.

## P1 — warsztat i jakość w obrębie potwierdzonych backendów

### P1-1. Jawny compositor: masks, blend i alpha/color

**Cel:** przewidywalne krawędzie i render order; zamknąć lukę obecnego bind_motion, który przy straight sprawdza obecność alpha, bez potwierdzenia association i transformu koloru. **Właściciel:** motion renderer adapter. **Wejścia:** DAG, alpha mode, input/work/output color, effect order. **Wyjścia:** capability report i render graph. **Zależności:** P0-2/4. **Pliki:** proponowane `adapters/compositing.*`, `tests/alpha-color-order.*`. **Ograniczenia:** collapse transformations/3D adjustment/roto nie są prostym CSS blend. **Fallback:** native prerender RGBA z manifestem. **Błędy/retry/limity/koszt:** cycle/unknown color→fail; memory→mniejsza concurrency, bez zmniejszenia jakości; lokalny GPU/CPU. **Akceptacja:** alpha0/1/invert, over fixture i permutacja operacji dają oczekiwany wynik; visual edge test na 3 tłach, linear-vs-gamma fixture; AE parity tylko dla sprawdzonych podzbiorów.

### P1-2. Proceduralny ruch i bake

**Cel:** stagger, pola wpływu, seeded noise i particles z kontrolowaną historią. **Właściciel:** motion owner; Blender/native owner dla solvera. **Wejścia:** seed, stabilne IDs, trajectory/velocity, constraints i cache settings. **Wyjścia:** sampled/baked channels oraz cache manifest. **Zależności:** P0-2, P1-1. **Pliki:** proponowane `core/procedural.*`, `cache/bake-manifest.*`, `tests/seek-simulation.*`. **Ograniczenia:** solver kolizji wymaga stanu; analytic particle nie jest zamiennikiem fluid sim. **Fallback:** bake z native projektu; brak implikowanej instalacji. **Błędy/retry/limity/koszt:** version/seed mismatch unieważnia cache; jedno wznowienie z checksum checkpoint; limit cząstek/memory ustalany benchmarkiem. **Akceptacja:** seek i render chunk boundary nie zmieniają stanów; usunięcie jednego instance nie przelosowuje innych; capture subframes poprawny dla shutter.

### P1-3. Audio cues i synchronizacja znaczenia

**Cel:** przypinać impact do muzyki/VO, nie do przypadkowych amplitud. **Właściciel:** audio-production-director + motion-sync; FrameCut trzyma globalny mix. **Wejścia:** waveform/annotations, sample rate, tempo map, source offsets, word timing, confidence. **Wyjścia:** cue map i manual corrections provenance. **Zależności:** P0-1/2; istniejące audio owner/engine do ponownego użycia. **Pliki:** istniejący motion-sync do inspekcji, proponowane `adapters/audio-cue-map.*`, `tests/offset-drift.*`. **Ograniczenia:** beat tracker nie wykrywa sam semantycznego downbeat/lyrics; variable tempo wymaga mapy. **Fallback:** ręczne markery, jawny confidence Unknown. **Błędy/retry/limity/koszt:** brak audio nie wywołuje automatycznej generacji; empty detections ≠ silence approval; one analysis rerun po poprawie parametrów; lokalne obliczenia. **Akceptacja:** B05: sample→impact i start lead poprawne; różne offset/drift oddzielnie; odsłuch obowiązkowy, LUFS tylko według briefu.

### P1-4. Adaptacja formatów zamiast cropu

**Cel:** zachować hierarchię i znaczenie w 16:9/9:16. **Właściciel:** Creative Studio direction + motion scene owner. **Wejścia:** score.formats, locked copy/assets, placement requirements. **Wyjścia:** layout overrides i osobne render/QA manifests. **Zależności:** P0-3/4. **Pliki:** wykorzystać istniejące formats; proponowane `adapters/layout-constraints.*`, `tests/portrait-adaptation.*`. **Ograniczenia:** tekst i tempo czytania mogą wymagać nowego approval; safe zones z konkretnej platformy. **Fallback:** ponowny styleframe/animatic review. **Błędy/retry/limity/koszt:** overflow→raport, nie shrink-to-illegibility; dwie propozycje layoutu maksymalnie przed decyzją; koszt lokalny. **Akceptacja:** każdy benchmark ma świadomy układ obu formatów, żadnego obciętego glifu/logo, ten sam argument i impacty.

### P1-5. Render/cache/resume i preview parity

**Cel:** wznowić pracę bez utraty walidacji albo powtarzania całego renderu. **Właściciel:** istniejący renderer/cache owner, bez nowej farmy. **Wejścia:** hash spec/deps/backend/quality/environment/range. **Wyjścia:** frames, checksums, completed ranges i resource measurements. **Zależności:** P0-2/4, P1-2 dla symulacji. **Pliki:** potwierdzony FrameCut Cache w fc_render.py do inspekcji; proponowane `adapters/render-manifest.*`, `tests/resume-parity.*`. **Ograniczenia:** cloud fractional FPS bywa inną capability niż local FPS; pixel-identical CPU/GPU Unknown. **Fallback:** single-worker local image sequence po uprawnionej decyzji. **Błędy/retry/limity/koszt:** partial file nie jest done; restart 1× po potwierdzeniu przyczyny; chunk/pool limity jawne; raport CPU/GPU/RAM/dysk. **Akceptacja:** uszkodzone 3 klatki regenerowane, reszta zachowana; zmiana quality unieważnia odpowiedni cache; out=exclusive w każdym chunku.

## P2 — zaawansowane rozszerzenia po dowodzie P0/P1

### P2-1. Tracking, roto, keying i natywny handoff

**Cel:** przyjmować motion jako część rzeczywistego plate, z poprawną perspektywą/mattem. **Właściciel:** motion compositing specialist + native program owner; FrameCut utrzymuje film. **Wejścia:** legalny plate, camera/tracking data, roto matte, scene contract. **Wyjścia:** editable native project lub render RGBA, transform/camera metadata, QA. **Zależności:** P1-1 i P0-4. **Pliki:** proponowane `adapters/native-composite-manifest.*`, `tests/tracking-occlusion-fixtures.*`; brak założenia AE API automatyzacji w instalacji. **Ograniczenia:** hair/motion blur/key spill/occlusion to osobne problemy; zero obietnicy prostego FFmpeg zamiennika. **Fallback:** wykonanie native przez uprawnionego operatora, reszta pakietu pozostaje edytowalna. **Błędy/retry/limity/koszt:** lost track→manual anchors; 2 korekty segmentu startowo, potem eskalacja; native licencja i dostęp osobno weryfikowane. **Akceptacja:** overlay nie ślizga się po planie, occlusion mask zgodna w całym ruchu, brzegi bez spill; real-time review całego clipu.

### P2-2. Parametryzowane sceny i biblioteka wiedzy

**Cel:** udostępnić receptury z ograniczonymi parametrami i kontrprzykładami zamiast biblioteki losowych efektów. **Właściciel:** istniejący hyperframes-workflow/remotion owner; Studio research-evidence przechowuje źródła. **Wejścia:** 18 receptur, mapowanie backendów, prawa i wynik 5 benchmarków. **Wyjścia:** progressive-disclosure skill cards i typed presets. **Zależności:** zaliczone P0/P1 benchmarki. **Pliki:** propozycje `knowledge/recipes/*.md`, `presets/*.json`; entry SKILL tylko linkuje, nie kopiuje całego raportu. **Ograniczenia:** licencja tutoriala nie daje praw kopiowania projektu/assetów, nazwy narzędzi nie są dostępnością. **Fallback:** wiedza proceduralna i oryginalne przykłady, bez zależności. **Błędy/retry/limity/koszt:** nieaktualne API→recheck źródła; zakaz silent fallback; brak paid calls. **Akceptacja:** preset ma trigger, wyjątek, units, test i ślad źródła; zmiana source invaliduje zależne instrukcje, a approved locks przechodzą nienaruszone.

## Bramka przed wdrożeniem

Odczytać aktualne repo/AGENTS, ustalić owner i zakres plików, sprawdzić model współpracy z Claude i dostęp bez ponawiania znanego błędu OAuth. Zatwierdzić architekturę przez właściwego właściciela, a potem wykonać wdrożenie w uprawnionym katalogu z kopiami przed edycją. Ten raport nie jest zgodą na zmiany infrastruktury, repozytorium, publikację ani usługi.

Materiały startowe: `README.md`, `COMPREHENSIVE-REPORT.md`, `CODE-AND-CONTRACTS.md`, `QA-BENCHMARKS.md`, `SOURCE-LEDGER.json`, `specialists/backends/REPOSITORIES.md`. Własny weryfikator potwierdza strukturę i analitykę; natywne API, render/parity, oglądanie i odsłuch trzeba wykonać dopiero w projekcie wdrożeniowym.
