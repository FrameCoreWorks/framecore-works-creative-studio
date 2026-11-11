# STUDIO-AUDIT — publiczne kontrakty i rzeczywisty zakres implementacji

Badanie: 2026-11-11. Publiczne main sprawdzono na **4611c9c4ed44579b8a2c0224c9276d955fccd8d6**, commit autora/committera **2026-11-11T07:20:22Z**. To punktowe przypięcie, nie obietnica, że gałąź nie zmieniła się później. README i trzy manifesty deklarują **1.174.1**. [Commit](https://github.com/FrameCoreWorks/framecore-works-creative-studio/commit/4611c9c4ed44579b8a2c0224c9276d955fccd8d6), [README B01](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/README.md).

Odczytano README, AGENTS, portable/Codex/Claude manifesty, dokumentację motion/render/audio/QA/FrameCut oraz wybrane pliki implementacji. **Nie wykonano kodu repozytorium. Nie zmieniono repo, instalacji ani konfiguracji.** Lokalne skille z cache 1.174.1 były źródłem instrukcji badania; nie wykonano porównania całego zainstalowanego bundle z publicznym commitem. Aktywna wersja runtime i zachowanie świeżej sesji: **Unknown**. Adresów oddzielnych repozytoriów FrameMotion i FrameCut nie podano; ich istnienia ani stanu nie wywnioskowano z nazw.

## 1. Potwierdzone ownership

**SOURCED:** istniejący opencut-video-studio to owner FrameCut dla montażu: mapowanie source→sequence, transitions, caption timing, audio placement i final composition. Pure coded-motion może pozostawać w Motion Graphics. [B11](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/SKILL.md).

**SOURCED:** toolkit routing dodaje możliwości wewnątrz obecnych ownerów Motion Graphics / Remotion Video; nie ustanawia nowego ownera workflow, stanu ani timeline. [B17](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-routing.md).

**DERIVED:** roboczy podział Studio → FrameMotion → FrameCut jest sensowny jako interfejs specjalisty. Jego wdrożenie powinno zachować aktualne ID ownerów przez adapter lub plan migracji. Nowa nazwa produktu nie upoważnia do przejęcia globalnej osi z FrameCut ani do usunięcia obecnej ścieżki HyperFrames.

## 2. Mapa plików i poziom dowodu

W poniższej tabeli P oznacza publiczny prefiks: plugins/framecore-work-creative-studio/. Wszystkie ścieżki są w przypiętym repo; nie są proponowanymi nowymi plikami.

| Źródło | Potwierdzony artefakt | Co z niego wynika | Czego nie dowodzi |
|---|---|---|---|
| B02 root AGENTS.md | Reguły maintenance i evidence | Saved/source/live test są rozdzielone | Autoryzacji wdrożenia w tym research |
| B03 P/plugin.json | Portable manifest 1.174.1 | Deklaracje dystrybucji i onboarding | Runtime obecny u użytkownika |
| B04 P/.codex-plugin/plugin.json | Codex manifest 1.174.1 | Katalog skills i onboarding reference | Discovery w nowym czacie |
| B53 P/.claude-plugin/plugin.json | Claude manifest 1.174.1 | Ta sama deklaracja wersji | Sesji CLI Claude |
| B05 P/skills/hyperframes-workflow/references/motion-contract-json.md | Dokumentowany motion-score | Plan, approval i timeline w jednym pliku | Formalnej walidacji każdego rozszerzenia |
| B06 …/assets/motion-quality/score.mjs | Kod helperów | Kontrola frame ranges i coverage | Jakości renderu |
| B07 …/assets/motion-scenes/motion-scenes.mjs | Kod scen i frame functions | Istnieje wykonywalny scene layer | Dowolnych efektów AE |
| B08 …/assets/motion-render/README.md | Python render workflow | Udokumentowany renderer i wymagania | Własnego testu na hoście |
| B09 …/assets/motion-review/README.md | QA/acceptance contract | Rozdzielone werdykty i hash binding | Faktycznego oglądania tego badania |
| B10 …/assets/motion-sync/README.md | Music/VO/lyrics/envelope workflow | Różne źródła cue i ograniczenia | Uniwersalnej skuteczności beat detectora |
| B12 P/skills/opencut-video-studio/assets/framecut/schema.json | JSON Schema v1 | Interchange shape | Całej semantyki runtime |
| B13 …/framecut/fc_core.py | Strict validator i commit_revision | Nieznane pola i stale revisions mają kontrolę kodową | Testu uruchomieniowego |
| B14 …/framecut/fc_render.py | motion_request, bind_motion, Cache | Handshake i ponowne użycie cache są implementowane | Testu wykonania konkretnego filmu |
| B15 …/framecut/fc_time.py | Rational time map | Trim/retime zachowuje source time | Zgodności arbitrary NLE |
| B16 …/framecut/README.md | Kontrakt runtime | Granice SDR/alpha/jobów | Dostępności aktualnych narzędzi |

Wszystkie URL i dokładne lokatory są w [sources.json](sources.json). Katalog nie traktuje samego README jako wystarczającego dowodu implementacji.

### Ważna niespójność dokumentacyjna

Package README opisuje Python renderer i FrameCut, lecz w starszej sekcji Scope and limitations pozostawia stwierdzenie o braku audio/video engine. **DERIVED:** traktować ten zwrot jako nieprecyzyjny/stary opis zakresu pluginu, a nie dowód braku wykonywalnych narzędzi. Odczytane fc_render.py, fc_time.py i motion-scenes.mjs potwierdzają konkretny kod. Nie wnioskować z tego, że wszyscy użytkownicy mają działające FFmpeg, Chrome, Python lub GPU. Naprawa README nie jest częścią niniejszego zadania.

## 3. Kontrakt istniejący ma pierwszeństwo

**SOURCED:** motion-score posiada m.in. schema_version, id, revision, approval, fps.num/den, totalFrames, width/height, scenes.start/end, copy, assets, fonts, formats i cues. Pola audio obejmują music, voiceover, sfx, soundDesign, captions. [B05](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-contract-json.md). To nie jest proponowany nowy format.

**SOURCED:** FrameCut schema_version=1 ma zamknięty zestaw top-level keys egzekwowany przez fc_core.validate. Schemat JSON sam opisuje ten walidator jako autorytet semantyczny. [B12](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/schema.json), [B13](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_core.py).

| Wymaganie researchu | Obecny nośnik i status | Wniosek do propozycji integracji |
|---|---|---|
| project_id | FrameCut root id; request project_id | Nie zmieniać nazwy root id bez migracji |
| schema_version / revision | Oba systemy; request project_revision | Rozdzielić wersję schema od rewizji projektu |
| timeline_owner | Brak takiego top-level pola v1; owner request wskazuje specialist | Semantyczny owner wynika z trasy; metadata nowego API w sidecarze |
| asset_id/hash | assets map + sha256 w FrameCut; motion asset id/revision | Hash manifestu uzupełniającego nie zastępuje native asset identity |
| fps_num/fps_den | Natywnie zagnieżdżone fps.num/den | Zachować aktualną postać |
| jednostki i [in,out) | FrameCut start/duration w frames; source_in w PTS; motion start/end | Adapter wylicza out, nie gubi jednostki |
| source/timeline time, retiming | speed, speed_curve, source_remainder, freeze | Globalny retime pozostaje w fc_time |
| handles | Source-span/transition validation; brak ogólnego handles object | W sidecarze deklarować żądane uchwyty, sprawdzać istniejący media span |
| rozdzielczość | deliverables oraz motion width/height/formats | Nie robić samego crop 16:9 → 9:16 jako „adaptacji” |
| color space | Request color=SDR bt709; source probe metadata | HDR/multi-space wymagają osobnego zakresu; nie przyjmować milcząco |
| alpha mode | Native deklaracja opaque lub straight; bind kontroluje obecność alpha | Association straight/premultiplied wymaga osobnego testu/conform |
| audio sample rate | Dokumentowany master 48 kHz, nie globalne arbitrary pole | Zarejestrować faktyczny rate w delivery receipt |
| fonty | Motion fonts z plikami; FrameCut captions font family | Wspólny hash manifest jako uzupełnienie; font family to za mało |
| seed | SoundDesign seed; brak uniwersalnego top-level seed v1 | Seed proceduralnego renderer adaptera w sidecarze |
| provenance | FrameCut assets provenance/rights; motion asset authority | Zachować źródło i licencję per asset |
| accepted locks | Clip locks; motion approval/copy/asset authority | Akceptacja stylistyczna nie jest tym samym co execution authorization |

Tabela to **DERIVED comparison** na podstawie B05, B12–B16, nie deklaracja nowego schema.

## 4. Dokładny handshake Motion Graphics

**SOURCED / CODE_INSPECTION:** fc_render.motion_request generuje lokalne pochodzenie 0, długość/FPS/wymiary/alpha, global_start_frame, stable project/sequence/event IDs, projektową revision oraz hashe project/sequence/deliverable/brief. Owner obecnie ma wartość hyperframes-workflow. bind_motion odczytuje historyczny projekt, kontroluje kontekst, hash media, frame count, FPS, wymiary i obecność kanału alpha; wiąże authoring JSON przez SHA-256. Linia 131 nie rozróżnia straight/premultiplied. Funkcja nie waliduje koloru zadeklarowanego w request. [B14](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py).

Pełna obserwowana lista pól: [request.fields.json](request.fields.json). Jest to **opis kształtu, nie prawidłowy execution request**. Poprawne hashe musi wygenerować istniejące CLI z rzeczywistego projektu. Nie podstawiać wymyślonych hashy.

**DERIVED:** FrameMotion powinien:

1. Przyjąć native request bez modyfikowania globalnego przedziału.
2. W swoim sidecarze dopiąć wersję adaptera, dependency manifest, seed, unsupported features i granice fidelity.
3. Zwrócić editable source + native motion-score albo inny authoring JSON, media oraz QA receipt związany z byte hash.
4. W razie żądania dłuższej sceny zwrócić change_request do ownera filmu. Nie przesuwać scen nadrzędnych.
5. Po zmianie brief/sequence/format żądać nowego native request. Sam ingest zwrotnego pliku może zwiększyć revision bez zmiany kontekstu; nie odrzucać go tylko z powodu wyższej liczby.
6. Brak assetu → lista konkretnych ID i zależnych scen; brak funkcji → unsupported z proponowanym bake/hybrid, bez cichego usunięcia.

Sidecar jest propozycją **DERIVED / NOT_IMPLEMENTED**. Nie wolno twierdzić, że obecny CLI go czyta. Przyszła integracja potrzebuje walidatora, migration tests i fail-closed dla nieznanych *wymaganych* funkcji. Ignorowanie dodatkowych pól w części motion runtimes nie jest dowodem ich zachowania ani round-trip.

## 5. Stan audio, QA i delivery

**SOURCED:** motion-sync rozróżnia zadany beat grid, źródła VO/lyrics timing oraz band envelope; przykłady raportują opóźnienie AAC i ograniczenia testów. [B10](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-sync/README.md). **DERIVED:** zachować te komponenty; nowy motion specialist nie powinien tworzyć konkurencyjnego beat detectora tylko dlatego, że analizuje klip.

**SOURCED:** motion review dokumentuje cztery werdykty oraz contract/video hash binding. FrameCut technical verify i delivery_readiness są oddzielne; recorded full picture/audio review jest warunkiem READY. [B09](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-review/README.md), [B16](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/README.md).

**DERIVED:** review flag jest zarejestrowanym oświadczeniem o oglądaniu/odsłuchu, nie automatycznym dowodem, że czynność wykonano. Badanie nie ustawia tych flag. Progi critique (np. liczba słów, safe regions, tempo) traktować jako aktualne heurystyki produktu do oceny w kontekście, nie uniwersalne normy motion designu, WCAG czy broadcast.

## 6. Backlog do hosta — bez autoryzacji implementacji

| Priorytet / zadanie | Cel i owner | Wejścia → wyjścia | Zakres plików / zależności | Ograniczenie, fallback i test akceptacji |
|---|---|---|---|---|
| P0 Native-contract compatibility | Host integracji + owner FrameCut | Pinned v1, request → compatibility map | Potwierdzone fc_core.py, schema.json, fc_render.py; nowy adapter path **proponowany, Unknown** | Nie dopisywać pól do v1; fallback native request + ręczny sidecar; test stare fixtures nadal walidują, nowe unsupported nie gubią danych |
| P0 Provenance-bound return | FrameMotion adapter + FrameCut | Native request, media, source → bound return | bind_motion i istniejący motion acceptance; source/asset hashes | stale brief/format/trim odrzucane; ingest-only revision dozwolona; test także wrong alpha/FPS/frame count |
| P0 Declared capability loss | Renderer adapter | Required techniques → fidelity/unsupported report | Nowy sidecar i validator **proponowane**; matrix BACKENDS | Brak cichej degradacji; fallback bake/zmiana briefu przez ownera; test nieznany required effect blokuje |
| P1 Frame/seed parity | Wybrany renderer owner | Pinned fonts/assets/spec → frame evidence | Istniejące starters; nowy test adaptera **proponowany** | Jeden backend na przypadek; test forward/reverse/shuffle/fresh-process |
| P1 Resume and memory | Render owner, global job pozostaje FrameCut | Interruption + unchanged inputs → resumed receipt | Potwierdzone Cache.stage/fc_jobs opis; runner adaptera proponowany | Nie usuwać source/history/finals; test przerwany chunk nie przechodzi jako gotowy |
| P1 Color/alpha/font contract | Delivery owner + specialist | Declared handling → measured receipt | Request deklaruje SDR/straight; bind nie dowodzi association/koloru; motion fonts, sidecar fields proposed | Test straight/premultiplied na dwóch tłach, color patches, polskie glyphs i missing font; HDR poza zakresem |
| P2 README precision | Właściciel dokumentacji Studio | Niespójny opis → precyzyjny opis runtime scopes | Potwierdzony package README | Osobne zadanie ownera; nie rozszerzać feature scope; test links i brak twierdzenia o aktywnym hoście |
| P2 Backend qualification | Obecny Motion Graphics / Remotion owner | Wspólny brief + kryteria → decyzja dependency | Repo map REPOSITORIES; zero install w research | Bez płatnych fallbacków; test benefit przy tej samej jakości i jawnej rewizji |

Retry/limity/koszt: projektowanie w tym raporcie kosztuje wyłącznie bieżący research; nie wywołano płatnego renderer API. Rekomendowany przyszły test lokalny ma jawny limit klatek, dysku, RAM, czasu i dwóch korekt. Timeout/transient failure nie upoważnia do zmiany providera. Nie wymyślono cen ani przewidywanego speed-up.

## 7. Ostateczny stan macierzy

**Potwierdzone w publicznym źródle:** native motion contract; global FrameCut; actual strict validator, rational time maps, motion binding, scene code; udokumentowany render/audio/review workflow.

**Luki implementacyjne względem propozycji:** publicznie sprawdzony standalone FrameMotion adapter, negocjacja fidelity i capability schema, uniwersalny dependency manifest/seed/color envelope przy zachowaniu v1, benchmark różnych backendów.

**Unknown:** repozytoria nowych wtyczek, ich stan wdrożenia, rzeczywista wersja zainstalowana/załadowana, testy klienta, cross-platform determinism, wydajność i prawa konkretnych przyszłych assetów. Wszystkie własne media/runtime tests: **NOT_RUN**.

