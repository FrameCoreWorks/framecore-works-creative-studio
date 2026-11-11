# DR-06 | Kontrakty produkcyjne dla odcinków

**Status DERIVED.** Projekt dla Claude jako architekta. Przykład jest fikcyjny i ma status `NOT_RUN`. Opiera się na istniejących powierzchniach opisanych w [BASELINE.md](BASELINE.md). Nazwy nowych obiektów i profili wymagają przeglądu architektury oraz wyboru miejsca przechowywania. Kontrakt odcinka nie zakłada istnienia zewnętrznej wtyczki wykonawczej.

## Granice własności i formaty

Creative Studio prowadzi Project State i rewizje twórcze. Scenarzysta prowadzi wersję skryptu i dokładny tekst. Reżyser zatwierdza beaty i warunki ujęć. Asset owner zarządza wybranymi rewizjami postaci, rigów, miejsc i praw w Asset Manifest. Animator otrzymuje zamrożone zależności i zwraca rendery w zegarze lokalnym. Sound przygotowuje take'i, pomiary, stemy i proponowane cue. QA dopisuje dowody do rewizji, a o akceptacji decyduje właściciel danej bramki.

Właściciel montażu utrzymuje **jeden master timeline**. Punktem odniesienia P0 jest projekt istniejącego FrameCut v1. Tylko montaż może zaakceptować i atomowo wykonać operacje na jego rewizji. Studio zapisuje decyzje i odsyłacz do wybranego projektu, animator i sound oddają propozycje lokalne. Kopia źródłowej mapy, animatic, SRT/VTT, render plan i zakresy w paczce ujęcia są odczytem/projekcją przypiętą do `project_id, sequence_id, revision, sha256`. Kandydat otrzymuje `base_revision` i hash bazowy, a przy rozbieżności wraca do właściciela montażu. Ponowny odczyt przed typed apply i walidacja oczekiwanego base hash/revision chronią przed nadpisaniem. Wygenerowany i zweryfikowany podgląd zmiany pokazuje ripple, locki i skutki dla dźwięku, napisów oraz przejść.

Jeśli odrębny FrameCut przejmie projekt po zweryfikowanej migracji, właściciel przenosi autorytet jednym przełączeniem przypiętego projektu. Przed przełączeniem nowy adapter pracuje na kopii kontrolnej, a poprzedni zapis pozostaje edytowalnym źródłem. Po przełączeniu poprzednia rewizja pozostaje snapshotem historii. Dwa klienty mogą czytać ten sam snapshot i proponować operacje. Konkretna rewizja ma jednego piszącego.

Połączenia z obecnym Studio [STUDIO-ARTIFACTS, STUDIO-MOTION, FC-SCHEMA, FC-RUNTIME, STUDIO-ASSET-LIFE, STUDIO-ENVELOPE]:

| Dane dodatkowe | Miejsce i granica |
|---|---|
| Biblia, skrypt, decyzje, mapa scen/ujęć | Uzupełnienia Project State, Storyboard Contract i Asset Manifest. Referencje rewizyjne z manifestu, praca na dokładnie wskazanych danych. |
| Parametry ujęcia i lokalny render | Lokalny Motion Contract lub źródło adaptera. Oddawane jako media plus receipt, lub kompozycja wtedy, gdy zweryfikowany adapter umie ją otworzyć. |
| Master, instancje, trymy, ścieżki, miks, finalny timecode | Projekt FrameCut v1. Projekcja do kontraktu ujęcia jest odczytem z zapisanego projektu, opcjonalnym przed animatikiem. |
| Wywołanie companion | Zachować `framecore-task-request/1` i `framecore-task-result/1`. Dołączyć plik kontraktu jako `inputs[]` z SHA-256 i rolą. Parametry wykonawcze zgodne z faktycznie zarejestrowaną operacją. Workflow ustala zgody, warunki, oczekiwania i reguły wznowienia. Result wraca przez intake z oryginalnym requestem. |
| Zgodność wykonania i gotowość | Oddzielić `planned`, faktyczną próbę i output, gotowość adaptera, status koperty, QA techniczne, kreatywne i prawa. Ostateczny Delivery Manifest wskazuje zaakceptowany snapshot i pliki. |

## Wersjonowanie i kontrakty danych

Każdy obiekt trwały ma stabilny identyfikator w swoim zakresie, monotoniczną rewizję i hash całego pliku wejściowego lub dokładnie zdefiniowanego pola. Hierarchia ID `series_id/episode_id/scene_id/shot_id`; ID sceny nie jest pozycją i pozostaje przy przestawieniu sceny. `shot_id` oznacza ujęcie twórcze, `event_id` jego instancję w sekwencji. Dwa użycia jednego take'a mają osobne `event_id`. `ref` zawiera ID, rewizję, SHA-256 i w razie potrzeby lokalizator. Hash na rekordzie oznacza UTF-8 zapisanej treści lub bajty pliku. Dla kluczy cache implementacja musi wskazać wersjonowaną, deterministyczną serializację (np. RFC 8785 dla obsługiwanych wartości) i kolejność semantycznie uporządkowanych tablic. Akceptacje i output przypięte do starej rewizji pozostają audytowalne. Nowa rewizja dostaje własne decyzje.

| Rekord | Minimalne pola i reguła |
|---|---|
| Series | `series_id`, `revision`, `bible_ref`, locale, format, audience i reguły treści, zatwierdzeni właściciele, zasady świata, ID postaci i lokacji, paleta, słownik nazw/wymowy, profil delivery, reguły i wyjątki continuity. |
| Episode | `episode_id`, `series_id`, `revision`, `script_ref`, bazowe rewizje biblii/assetów, tryb timing-first, voice-first lub music-first, decyzje redakcyjne, referencje scen, QA oraz identyfikator i rewizja mastera. Dobór trybu jawnie określa, co jest źródłem pierwszego timingu. |
| Script i dialogue | Wersja scenariusza z dowodami dla twierdzeń. `line_id`, `revision`, `speaker_character_id`, `exact_text`, `language`, wskazówki wykonania, `pronunciation_overrides`, powiązana akceptacja i `voice_identity_ref`. Zmiana choćby jednego znaku lub intencji przechodzi przez rewizję. Do TTS/nagrania osobno przekazać zatwierdzony wariant fonetyczny lub SSML; exact text pozostaje źródłem skryptu i kontroli treści. Napisy mogą mieć zatwierdzoną redakcję powiązaną z `line_id`. |
| Scene i shot | `scene_id`, `shot_id`, rewizja, `beat_id`, funkcja, start/end state, blokowanie postaci i kamery, cel ruchu, timeline binding read-only, lokalne wymagania czasowe, wejściowe refy postaci, rigów, miejsc i kwestii, wymagane uchwyty przejścia, `continuity_locks`, reguła QA. Dla osobnych wygenerowanych ujęć przekazać zatwierdzone referencje właściwych cech i jasno oznaczyć weryfikowalną kontrolę. |
| Character/asset | Stabilne ID, revision/hash, typ, rola i autorytet cechy, pochodzenie, rights ref, skala/jednostka i układ współrzędnych dla rigów, model/turnaround/expression/pose sheets, warianty stroju i przydział rekwizytów. Rzeczywiste typy i klucze istniejącego Asset Manifest zachować, szczegóły umieścić w przypiętym pliku lub udokumentowanych polach pomocniczych. |
| Voice identity i take | Wewnętrzne `voice_id`, rev, character/locale, provider i jego dokładna voice/model/version lub wewnętrzne ID aktora, zakres zgody i provenance ref, zatwierdzony wzorzec wykonania. Take zawiera własne ID/revision/hash pliku, `line_id@rev`, `voice_id@rev`, `duration_samples`, sample rate/kanały, `phoneme_timing` lub `word_timing` wraz z metodą i niepewnością, proof słuchu i rights. Czas nieznany to `null` z powodem. Brak zgody blokuje nową syntezę i dopuszczenie take'a. |
| Audio cue i stem | `cue_id`, rodzaj (dialogue, music, ambience, SFX, silence), source ref/stream, source range, ankra ujęcia lub zdarzenia, związek z kwestią, `anchor_basis` (onset/peak/end/offset), `gain_db`, fade, bus, wymagana synchronizacja, latencja, speed/offset jeśli stosowane, prawa i QA. Stem ma role/mix profile oraz zakres, wejściowe cue refs i pomiar. Kontekstowe overlaps zależą od montażu. |
| Render spec i receipt | `render_id/revision`, input refs, silnik/adapter/wersja i operacja, hash toolchainu/sceny/fontów, rozmiar/FPS, klatki wejścia i handles, alpha/color, format, determinism/seed jeśli obsługiwany, limit wall time/dysku, warunki praw, wymagane QA. Receipt niesie rzeczywisty backend/wersję, job ID, faktyczne parametry, SHA-256 i bajty plików, dekodowane właściwości, kontrole z zakresem, warnings i unexecuted checks. `requested/verified/unknown` pozostają rozdzielone. |
| Rights i QA | `rights_ref` łączy source URL/locator, autor/dostawca, licencja/zgoda i data, zakres (kanał, komercja, terytorium, czas, transformacja, użycie głosu), credit, dowód zgody i ograniczenia. Prawa do assetu, nagrania i wzorca głosu mogą być osobnymi rekordami. `qa` określa gate, artefakt/rev/hash, status (`NOT_RUN/PASS/FAIL/BLOCKED/WAIVED`), metodę, dokładny zakres, evidence ref, kto i kiedy, uzasadnienie i ewentualny wyjątek. Wyjątek nie może nadać nieistniejących praw. |

## Implementacja ujęć w kodzie

Rekomendowana pierwsza ścieżka pilota to wersjonowane, programowo renderowane ujęcia ze wspólnym scene graph, biblioteką pozycji i wymiennymi adapterami. Zatwierdzona akcja opisuje stan wejściowy i wyjściowy, cel ruchu i beat w klatkach. Kod przekłada to na węzły postaci, planu, rekwizytów, kamery, masek i warstw. Węzły mają stabilne ID, parent, z-order, przestrzeń współrzędnych, transformaty, zasady zasłaniania i jawnie dozwolone interpolacje. Pozy, ekspresje, usta/visemy, cykle i rekwizyty wskazują konkretne rewizje w bibliotece. Oś czasu kompozycji pozostaje lokalna. Konstrukcję pełnego odcinka utrzymują zatwierdzone beaty, animatic, montaż i odbiór całej historii.

W rendererze P0 zegar klatki zastępuje zegar ścienny. Przypiąć commit albo hash źródła sceny, zależności, wersję runtime/adaptera, graf i pliki wejściowe. Seed jest jawny na operację i węzeł używający losowości. Przypiąć fonty, kolor, wartości easing i deterministyczny klucz wyboru wariantu. Walidować ograniczone typy operacji i własność źródła kodu; dane od agenta lub źródła publicznego nie stają się wykonywalnym skryptem. Różnice w przeglądarce, sterowniku lub backendzie mogą zmieniać piksele mimo zbieżności timingu. Test referencyjny definiuje środowisko, dozwolone odchylenie i zakres. Akceptacja jakości i ciągłości wymaga odczytu rzeczywistych klatek.

Adapter jest mały i zależny od metody. Remotion lub autorski SVG/Canvas w przeglądarce mogą obsłużyć oszczędne 2D i bibliotekę póz; Manim pasuje do animowanych relacji i diagramów; WebGL lub Blender Python do przypadków potrzebujących sceny przestrzennej lub oświetlenia. HyperFrames można rozważyć dla nakładek/motion zgodnie z istniejącym Motion Contract. To kandydaci, których zdolność do wykonania danej operacji i zachowania layoutu wymaga fixture. Kontrakt adaptera przyjmuje zakres lokalny, wersję sceny, assety i wymagania eksportu. Zwraca kandydacki klip lub klatki, mapę lokalnego czasu, zweryfikowane właściwości i receipt. FrameCut konsumuje wynik w formie udokumentowanego źródła/overlayu. Scena może pochodzić też z ręcznego riggingu albo generowanego klipu z jawnym zakresem kontroli. [STUDIO-MOTION, STUDIO-ADAPTER, FC-RUNTIME]

## Czas i ciągłość

- Reprezentacja pochodna deklaruje dodatnie, skrócone `fps: {numerator, denominator}`, a konwerter jawnie mapuje na istniejące `{num, den}`. Pozycje montażowe i comp są zerowane w ich własnych domenach. `[start,end)` używa integerów z jawnie określonym `unit`, `clock_id` i początkiem. Wspólna granica należy do następnego przedziału. Duration w danej domenie to `end-start`, a duration w sekundach to ułamek. Wygenerowane proxy i final podają własną bazę czasu. Zaokrąglone 29,97 nie zastępuje 30000/1001.
- `source_pts` używa oryginalnych timestampów i time base ze stream probe. Dla VFR mapa dekodowanych PTS wyznacza pozycje, a przy montażu wartość nominalnego FPS opisuje profil, nie indeks źródłowy. `source_frame` dopuszcza się przy dowiedzionym CFR albo konkretnym pliku wygenerowanym z numeracją klatek. Zachować start PTS, ewentualny offset, źródłowy extent i `time_map` ze speed/hold zgodne z rzeczywistym zakresem adaptera. Wartości żądane, dostępne i sprawdzone są osobne.
- `audio_sample` indeksuje próbkę w danym pliku/strumieniu. W masterze wbudowany FrameCut przelicza granicę klatki na sample 48 kHz raz, przez nearest z ties away from zero [FC-RUNTIME]. Dla `f` na głównym zegarze `S(f)=round_nearest(f * denominator * sample_rate / numerator)`; długość odcinka audio to `S(end)-S(start)`. Unikać sumowania już zaokrąglonych długości kolejnych klipów. Offset/ankra w cue pozostają jawne. Earshot otrzymuje zgodny z adapterem format sekund, wynik porównuje się z kanoniczną liczbą próbek [TOOLBOX-HANDOFF].
- Blokada ciągłości ma `lock_id`, pole/cechę, autorytet (asset ref), wartość lub mierzalną granicę, zakres (seria, scena, sąsiednie ujęcia), entry/exit, wyjątek zatwierdzony przez właściciela i dowód porównania. Przykłady: skala twarzy, strona wejścia, kolejność trzymanych przedmiotów, kostium, stan drzwi, pora dnia, barwa i locale głosu. Postać może celowo zmienić stronę, strój lub stan rekwizytu po zaznaczonym zdarzeniu. Lock ma wtedy wersję i przejście między stanami. Przy montażu wymagać testu na sąsiednich ujęciach, nawet gdy hashe tych ujęć są z cache.
- Timing-first blokuje długość i okna akcji, a głos sprawdza dopasowanie do okna. Voice-first blokuje take i czas przed animacją twarzy. Music-first blokuje wersję ścieżki i grid, a narracja dostaje jawne okna. Zmiana podstawy timingu wymaga decyzji reżysera i montażu. Offscreen bez ruchu ust jest prawidłową metodą, gdy wynika z zaakceptowanej inscenizacji.

## Przykładowa paczka ujęcia

Poniższy JSON jest propozycją formy danych `framecore-episode-shot/0.1-draft`. SHA w przykładowych refach są sztucznymi identyfikatorami danych testowych. W projekcie muszą odpowiadać bajtom. Próbka pokazuje lokalny klip 72 klatek, wzięty z `[12,84)` renderu i umieszczony w `[240,312)` mastera; po `[0,96)` renderu pozostaje po 12 klatek uchwytu. Cue 48 048 próbek trwa 24 klatki przy 24000/1001 i 48 kHz. Brak realnych plików i zgody w przykładowej paczce blokuje produkcyjne użycie.

```json
{
  "contract": "framecore-episode-shot/0.1-draft",
  "fixture": true,
  "series_id": "latarnia-na-wzgorzu",
  "episode_id": "e001",
  "scene_id": "s003",
  "shot_id": "sh012",
  "revision": 2,
  "bible_ref": {"id": "bible", "revision": 3, "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
  "script_ref": {"id": "script-e001", "revision": 4, "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
  "beat_id": "s003-door-open",
  "function": "Pokazać otwarcie zatrzaśniętych drzwi",
  "action": "Nela naciska klamkę i przesuwa dłoń w lewo",
  "camera": "Plan bliski, statyczny, od strony zawiasów",
  "characters": [{"id": "nela-rig", "revision": 2, "sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc", "rights_ref": "rig-use"}],
  "location": {"id": "latarnia-drzwi", "revision": 1, "sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd", "rights_ref": "set-use"},
  "master_projection": {
    "source": "FrameCut project v1",
    "project_id": "latarnia-e001",
    "sequence_id": "main",
    "event_id": "video-sh012",
    "base_revision": 8,
    "base_project_sha256": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "fps": {"numerator": 24000, "denominator": 1001},
    "timeline_range": {"clock_id": "main", "unit": "timeline_frame", "start": 240, "end": 312}
  },
  "continuity_locks": [
    {"lock_id": "coat-s003", "scope": "s003", "subject": "nela", "property": "coat", "authority": "bible@3", "entry": "green-A", "exit": "green-A"},
    {"lock_id": "door-sh012", "scope": "sh012", "subject": "latarnia-drzwi", "property": "door_state", "authority": "s003-door-open", "entry": "closed", "exit": "open"}
  ],
  "dialogue": [{
    "line_id": "s003-l005", "revision": 2, "speaker_character_id": "nela",
    "exact_text": "Już się otwiera.", "locale": "pl-PL", "performance": "cicha ulga", "pronunciation_overrides": [],
    "voice_identity_ref": {"id": "nela-pl-human", "revision": 1, "sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"},
    "take_ref": {"id": "take-l005-b", "revision": 1, "sha256": "1111111111111111111111111111111111111111111111111111111111111111"},
    "voice_rights_ref": "nela-voice-use",
    "take_rights_ref": "l005-recording-use"
  }],
  "audio_cues": [{
    "cue_id": "dialogue-s003-l005", "role": "dialogue", "bus": "dialogue", "line_id": "s003-l005", "line_revision": 2,
    "source_range": {"clock_id": "take-l005-b@1", "unit": "audio_sample", "sample_rate_hz": 48000, "start": 0, "end": 48048},
    "anchor": {"clock_id": "main", "event_id": "video-sh012", "unit": "timeline_frame", "offset": 12, "basis": "source_range_start"},
    "duration_samples": 48048, "gain_db": 0, "lip_sync": "offscreen"
  }],
  "render_settings": {
    "profile_id": "pilot-edit-intermediate",
    "adapter_state": "proposed",
    "adapter_id": null, "observed_backend": null,
    "fps": {"numerator": 24000, "denominator": 1001},
    "render_range": {"clock_id": "shot-sh012", "unit": "source_frame", "start": 0, "end": 96},
    "visible_source_range": {"clock_id": "shot-sh012", "unit": "source_frame", "start": 12, "end": 84},
    "left_handle_frames": 12, "right_handle_frames": 12,
    "width_px": 1920, "height_px": 1080, "alpha": "opaque", "color_profile": "Rec.709", "audio_embedded": false,
    "limits": {"wall_timeout_s": 180, "max_disk_bytes": 536870912, "max_transient_retries": 1}
  },
  "rights": {
    "rig-use": {"status": "unknown", "scope": "pilot YouTube", "evidence_ref": null},
    "set-use": {"status": "unknown", "scope": "pilot YouTube", "evidence_ref": null},
    "nela-voice-use": {"status": "unknown", "scope": "nagranie głosu dla pilota YouTube", "evidence_ref": null},
    "l005-recording-use": {"status": "unknown", "scope": "użycie konkretnego nagrania w pilocie", "evidence_ref": null}
  },
  "qa": [
    {"gate": "continuity", "status": "NOT_RUN", "criterion": "Zielony strój Neli i ta sama geometria drzwi na obu granicach", "evidence_ref": null},
    {"gate": "audio", "status": "NOT_RUN", "criterion": "Dokładna polska kwestia, jedna wypowiedź, głos poza kadrem", "evidence_ref": null},
    {"gate": "rights", "status": "BLOCKED", "criterion": "Dowody dla konkretnego użycia rig, lokacji, głosu i nagrania", "evidence_ref": null}
  ]
}
```

## Zależności i wznowienie

1. Rejestruj faktycznie użyte wejścia przy wyniku jako `ID@rev + SHA`. W P0 użyj istniejącego Asset Manifest do analizy po ID i rewizjach oraz dodatkowego indeksu semantycznych zależności potrzebnych do kompilacji ujęcia. Graf jest acykliczny. `video-shot`, `dialogue-take`, `viseme-track`, `scene-mix`, `caption-group`, `export` i `qa-check` to typy węzłów. Każdy etap ma deklarację używanych pól; klucz obrazu pozbawionego lipsyncu nie obejmuje treści offscreen. Pełny hash wejściowego pliku pozostaje w dowodzie pochodzenia. Klucz operacji z węższą projekcją potrzebuje testu, że pominięte pola rzeczywiście nie są konsumowane.
2. Po rewizji oznacz zmienione zależności i wyznacz ich przechodni wpływ. Odnowa akceptacji i odnowa bajtów mają osobne podstawy. Zmiana praw wymaga powtórnej bramki prawa i może zablokować publikację bez renderu. Zmiana dialogu o tym samym czasie w offscreen przebudowuje take, właściwy fragment miksu, napisy i zakodowany master, a zachowane ujęcia są kandydatami do cache po sprawdzeniu hashy. Mowa widoczna dopisuje visemes/facial pass, zależne shot render/composite oraz QA w sąsiedztwie. Inny timing otwiera reżyserię i montaż, jeśli łamie okno lub lock. Przy ripple zmieniają się placement, napisy, chapter marks i użycia po granicy; render ujęcia w lokalnym zegarze może być ponownie użyty, jeśli jego parametry i uchwyty nadal pasują.
3. Cache kluczuje semantyczne wejścia etapu, wersję adaptera i profilu, hash kodu/rigów/fontów, model/voice/seed według powierzchni, parametry czasu/koloru/alfa i wersję kanonizacji. Locale, sample rate i konfiguracja foley muszą być w kluczu odpowiedniego etapu. Niezmieniony plik można przenieść po ponownym hash checku. Na cache hit sprawdź faktyczne pliki, checksum, metadata/decoder i zakres ważności QA; zachowaj provenance i ograniczenia wykorzystania. Dla niepowtarzalnych generatorów klucz identyfikuje próbę i cache'owany zaakceptowany output, a identyczne wejścia nie obiecują tych samych bajtów nowej generacji.
4. Plan rozpisuje granice czasu, dysku, prób, kosztu i zgód. Zapisuj `job_id`, `attempt_id`, `base_revision`, fingerprint, identyfikator operacji zdalnej, ślady stanów, receipt i limity. Po timeout odczytaj status po istniejącym ID. Ponowna wysyłka dopiero przy rozstrzygniętym stanie, udokumentowanej idempotencji jeśli dostępna i w obrębie budżetu. P0 proponuje maks. jedną dodatkową próbę przejściowego błędu, ograniczoną polityką wykonawcy i zgodą. Błąd praw, gotowości, uwierzytelnienia, typu danych lub brak capability wymaga jawnej decyzji; automatyczny retry go nie rozwiązuje. Uczciwe fallbacki obejmują animatic lub podgląd lokalny jako szkic, ręczny montaż albo zatwierdzony cutaway. Przełączenie dostawcy, głosu lub wysyłka do nowego celu wymagają zgody właściwej dla operacji.
5. Wznów po weryfikacji rewizji projektu, wejść i istniejących wyników. Użyj istniejącego mechanizmu `job-status/job-resume`, gdy to ten sam render FrameCut; nowe dane lub inny render plan tworzą nową próbę. Zapis pliku roboczego idzie do obszaru próby, odbiór używa zweryfikowanego hasha i atomowej publikacji w bieżącej rewizji. Przy zmianie mastera podczas zdalnego renderu przyjmij zwrócony materiał jako kandydata do ponownego przypięcia i sprawdzenia, a starego placementu nie stosuj automatycznie. [FC-RUNTIME, STUDIO-ADAPTER, ASSETS-CONTRACT]

## Migracja i kompatybilność

- Wprowadzić opt-in sidecar poza zamkniętym top-level `FrameCut project v1`. Stary projekt otwiera się bez niego. Pierwszy import tworzy rekordy z zachowanych FrameCut ID i projektowego hasha, a brakujące biblię, rewizje linii, voice, provenance i dane praw oznacza jako `Unknown`. Brakujące dane nie blokują historycznego odczytu, lecz wstrzymują bramkę, gdy są warunkiem nowego wykonania lub finalnego użycia. Zachować oryginalne źródłowe mapy, czasy, historie, artefakty i zgody w ich realnym zakresie. Przenieść tylko rzeczy jawnie udowodnione. [FC-SCHEMA, FC-RUNTIME]
- Wymiana nadal używa koperty v1. Oryginalny request podać do intake, w wyniku odczytać `partial`, `unexecuted_checks` i ostrzeżenia. Klient widzący tylko kopertę v1 może nadal użyć istniejących rezultatów. Nowy klient czyta rozpoznane sidecary, a nierozpoznany major zgłasza właścicielowi i zachowuje plik. Konwersja `numerator/denominator ↔ num/den` musi być odwracalna. Przy luce semantycznej w source map lub operacji adapter odmawia importu tej zmiany. [STUDIO-ENVELOPE, STUDIO-INTAKE]
- Fixture migracyjny P0 to zapis istniejącego projektu v1 bez danych serialowych. Odczyt i powrót zachowują master ID, dokładny FPS, rewizję, momenty cięć, anchory, source map, locki i oczekiwane assety. Sprawdzić hash projektu przy odczycie, nieporuszony starszy bundle, odrzucony konflikt dwóch propozycji z tą samą rewizją bazową, niezależną ścieżkę w cache i unieważnienie dowodu QA po zmianie. Wdrożenie, test round-trip i test renderu są **NOT_RUN**. [FC-RUNTIME, STUDIO-ASSET-LIFE]
