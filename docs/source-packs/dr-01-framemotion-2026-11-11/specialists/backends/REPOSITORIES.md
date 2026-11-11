# REPOSITORIES — konkretne pliki, kwalifikacja i prawa

Badanie 2026-11-11. **DOC_READ / CODE_INSPECTION**, bez instalacji i uruchamiania pobranego kodu. Oceny dopasowania, proponowane interfejsy adapterów i testy to **DERIVED**. Własne testy runtime: **NOT_RUN**. Repozytorium publiczne, manifest pakietu, release i aktywny runtime są odrębnymi stanami.

## 1. Co znaczy „przejąć”

| Kategoria | Znaczenie w tym raporcie | Wynik do rozważenia |
|---|---|---|
| Wiedza | Poznać semantykę, ograniczenie lub mechanizm | Notatka z dowodem i kontrprzykładem |
| Metoda | Własna implementacja zasady, np. stan z absolutnej klatki | Testowalny algorytm bez kopiowania source |
| Skill | Selektywna adaptacja instrukcji pracy agenta | Instrukcja zgodna z ownerem i kontraktem Studio |
| Dependency | Użycie biblioteki przez udokumentowany interfejs | Przypięta wersja, środowisko, licencja, fixture |
| Code-copy | Przeniesienie konkretnych linijek/modułu do własnego produktu | Osobna decyzja z notice, licencją i kosztem aktualizacji |

**DERIVED:** domyślnie przyjmować wiedzę/metodę. Dependency uzasadnia dopiero scena, której obecny stack nie obsługuje dostatecznie dobrze. Code-copy nie jest tutaj zatwierdzone. Instrukcje w obcym SKILL.md są materiałem badania, nie poleceniami dla tego procesu.

## 2. Przypięcie i sygnał utrzymania

Wersje poniżej odczytano z manifestów w badanym drzewie; nie deklarują opublikowania odpowiadającego npm release. Daty to daty commita, nie publikacji dokumentacji. SHA w linku jest pełny.

| Repozytorium / przypięcie | Zaobserwowany stan | Wniosek utrzymania |
|---|---|---|
| [FrameCore Works Studio](https://github.com/FrameCoreWorks/framecore-works-creative-studio/tree/4611c9c4ed44579b8a2c0224c9276d955fccd8d6) | 1.174.1; 2026-11-11T07:20:22Z | Obecny punkt integracji; bez porównania z zainstalowanym bundle |
| [HyperFrames](https://github.com/heygen-com/hyperframes/tree/3ad7611f9fd36c1cef589c59b116ad7043c3b041) | engine 0.9.33; 2026-11-11T06:35:29Z | Rozwijany kod; zmiany renderer/capture wymagają pinów i parity check |
| [GSAP](https://github.com/greensock/GSAP/tree/5e6c35ff8eedea12d4f229129def635277d8b0f2) | 3.15.1; 2026-11-04T00:56:17Z | Aktualny silnik; osobno sprawdzać warunki zastosowania |
| [GSAP skills](https://github.com/greensock/gsap-skills/tree/aed9cfd3277740755f6bfc1155c7aa645403b760) | commit 2026-04-21T23:47:02Z | Repo instrukcji, nie wersja silnika ani dowód renderera |
| [Remotion](https://github.com/remotion-dev/remotion/tree/889c61f2da985832fd35efc29eac29ffd72be12e) | core 4.0.542; 2026-11-11T07:05:31Z | Nie przenosić automatycznie przyszłych warunków v5 na v4 |
| [PixiJS](https://github.com/pixijs/pixijs/tree/eb96c76fa27c948c748ff0bb79fc7a29329cd5e9) | 8.22.0; 2026-11-10T14:38:53Z; dev snapshot | Kwalifikować wydanie, nie bezwarunkowo śledzić dev |
| [Three.js](https://github.com/mrdoob/three.js/tree/b5a9e5730f6122498e187da8f7cdedd4358f5aa0) | 0.187.0; 2026-11-10T22:24:55Z; dev snapshot | Testować renderer, color i importers po aktualizacji |
| [Motion Canvas](https://github.com/motion-canvas/motion-canvas/tree/7b91435c301d530351dcf5ebb91dd139c002e405) | core 3.17.2; 2026-07-02T20:01:32Z | Starszy commit sam nie dowodzi porzucenia; ryzyko zgodności sprawdzić fixture |
| [Blender](https://github.com/blender/blender/tree/ca56249b6affcc1b79dcde5a7a7feaf6dd630e32) | commit 2026-11-10T21:56:37Z; tutaj tylko COPYING | Nie przypisywać zainstalowanemu Blenderowi tego SHA |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg/tree/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba) | commit 2026-11-11T03:28:21Z | Faktyczne filtry i licencja zależą także od konfiguracji build |

Daty sprawdzono publicznym GitHub API dla wskazanych SHA. Nie przeprowadzono audytu otwartych issues, bus factor, bezpieczeństwa dependency ani stabilności całych repo; tabela nie jest oceną SLA.

## 3. Najbardziej użyteczne pliki i interfejsy

### Studio: najpierw istniejący kontrakt

Pliki B05–B17 i manifesty B03/B04/B53 opisano szczegółowo w [STUDIO-AUDIT](STUDIO-AUDIT.md). Najważniejszy code seam: [fc_render.py B14](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py), funkcje motion_request i bind_motion; wejście to projekt/sequence/event/delivery, wyjście to request lub binding zwrotnego assetu. [fc_core.py B13](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_core.py) pozostaje semantycznym walidatorem v1.

**DERIVED — decyzja:** adaptować przez te interfejsy; nie forkować równoległej osi czasu. Python/Pillow/FFmpeg i opcjonalne CairoSVG wynikają z opisu istniejącego motion-render [B08](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-render/README.md); nie świadczą o kompletności lokalnej instalacji. Test przyszłej integracji: poprawny bind, niezmienny globalny zakres, odrzucenie zmienionego briefu; ingest-only revision rozpatrywać zgodnie z rzeczywistym kontekstem.

### HyperFrames: gotowy eksport seekable composition

Najlepsze pliki to [fps.ts B19](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/core/src/fps.ts), [distributedFps.ts B20](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/core/src/distributedFps.ts), [config.ts B21](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/engine/src/config.ts) i [systemMemory.ts B22](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/engine/src/services/systemMemory.ts). Pierwszy przetwarza reprezentację FPS i argument FFmpeg, kolejne ograniczają routing i zasoby. [Manifest B60](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/engine/package.json): Node ≥22, Puppeteer/Puppeteer-core, wewnętrzne core/parsers, Hono, linkedom, undici; repo build obejmuje TypeScript.

**DERIVED — decyzja:** dependency przez istniejącego ownera HyperFrames, gdy potrzebny jest render HTML. Własny adapter ma wejście composition+asset manifest+native request, wyjście media+receipt. Nie kopiować engine wraz z pobocznym serwerem. Proponowany fixture: rational FPS lokalnie, unsupported fractional distributed, cold fonts, reverse seek, przerwanie capture. Szczególna pułapka: [zwalnianie WebGL B23](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/engine/src/services/webglRelease.ts) wymaga sprawdzenia odtworzenia wcześniejszej sceny.

### GSAP i oficjalne skille: timing, nie nowy renderer

[gsap-core.js B54](https://github.com/greensock/GSAP/blob/5e6c35ff8eedea12d4f229129def635277d8b0f2/src/gsap-core.js), metoda seek, przekazuje pozycję do totalTime. [Dokumentacja B24](https://gsap.com/docs/v3/GSAP/Timeline/seek()/) wyjaśnia pomijanie zdarzeń i niezależność paused. Runtime działa w JavaScript; dla DOM wymaga środowiska przeglądarki. Wejście API: czas/label; wyjście: zaktualizowany stan animowanych celów, nie plik filmu.

[gsap-timeline/SKILL.md B55](https://github.com/greensock/gsap-skills/blob/aed9cfd3277740755f6bfc1155c7aa645403b760/skills/gsap-timeline/SKILL.md) zawiera position parameter, defaults i nesting. [gsap-performance/SKILL.md B56](https://github.com/greensock/gsap-skills/blob/aed9cfd3277740755f6bfc1155c7aa645403b760/skills/gsap-performance/SKILL.md) obejmuje transform/opacity, read/write batching i cleanup.

**DERIVED — decyzja:** przejąć metodę i wybrane instrukcje o organizacji timeline; dependency tylko jeśli obecna scena go potrzebuje. Nie przejmować scroll/mouse jako zegara filmu ani zalecenia biblioteki dla każdej sceny. Test: render klatek w przypadkowej kolejności daje ten sam stan bez callback-side-effects. Nie kopiować całego zbioru skills do roli ownera.

### Remotion: komponent jako funkcja czasu i danych

[random.ts B31](https://github.com/remotion-dev/remotion/blob/889c61f2da985832fd35efc29eac29ffd72be12e/packages/core/src/random.ts) przyjmuje seed i zwraca liczbę; null jest niedeterministyczny. [validate-fps.ts B32](https://github.com/remotion-dev/remotion/blob/889c61f2da985832fd35efc29eac29ffd72be12e/packages/core/src/validation/validate-fps.ts) waliduje number. [useCurrentFrame B30](https://www.remotion.dev/docs/use-current-frame) może zwracać klatkę lokalną. [Manifest B61](https://github.com/remotion-dev/remotion/blob/889c61f2da985832fd35efc29eac29ffd72be12e/packages/core/package.json) wskazuje React/react-dom ≥16.8 i narzędzia TypeScript/Bun w repo.

**DERIVED — decyzja:** istniejący Remotion owner plus dependency do wariantów parametrycznych. Adapter: props+native request → kompozycja i renderowany clip. Nie wybierać tylko po popularności React. Test: Sequence offset, exact copy, local font, alpha i wynik encoded rational rate. Zachować num/den w kontrakcie, nawet jeśli API przyjmuje iloraz number.

### PixiJS: jawny stan GPU 2D

[Ticker.ts B35](https://github.com/pixijs/pixijs/blob/eb96c76fa27c948c748ff0bb79fc7a29329cd5e9/src/ticker/Ticker.ts), update(currentTime), wylicza delta przy postępie czasu; nie przewija symulacji wstecz. Środowisko: browser canvas + WebGL/WebGPU zależnie od konfiguracji; manifest zawiera m.in. typy WebGPU, earcut i eventemitter3. [Performance B36](https://pixijs.com/8.x/guides/concepts/performance-tips) uzasadnia testowanie batchingu, tekstu, masek i fill-rate.

**DERIVED — decyzja:** dependency specjalisty sprite/particles, nie zastępstwo exact-copy HTML bez powodu. Adapter przyjmuje absolutny frame state i atlas, zwraca canvas capture. Własny test: 10/100/1000 elementów jako kontrolowana próba skali, stały wygląd i pamięć po zmianach sceny. Bez obietnicy konkretnego FPS. Ticker usunąć z definicji czasu eksportowego.

### Three.js: kamera i scena, stan fizyki osobno

[AnimationMixer.js B37](https://github.com/mrdoob/three.js/blob/b5a9e5730f6122498e187da8f7cdedd4358f5aa0/src/animation/AnimationMixer.js), setTime(seconds), resetuje czas miksera/akcji i aktualizuje animację. [Color management B38](https://threejs.org/manual/pages/color-management.html) i [cleanup B39](https://threejs.org/manual/pages/cleanup.html) są ważniejsze dla eksportu niż sama liczba obiektów. Środowisko: browser, wybrany renderer i zgodne loaders; nie zakładać że przykładowy WebGPU shader zadziała w WebGL.

**DERIVED — decyzja:** dependency dla realnego 3D. Adapter: geometry/material/camera/time → render target, dalej istniejący exporter. Test: podświetlona powierzchnia, kolorowy tekst, przezroczysta krawędź, dispose/recreate. Method setTime nie wystarcza dla cloth/particles/feedback. Nie przejmować sample modeli bez osobnych praw.

### Motion Canvas: jawna sekwencja z kontrolą resetu

[PlaybackManager.ts B40](https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/core/src/app/PlaybackManager.ts), seek(frame), może resetować i wykonywać next aż do celu. [GeneratorScene.ts B41](https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/core/src/scenes/GeneratorScene.ts) resetuje generator i Random(meta.seed). [Manifest B62](https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/core/package.json): core 3.17.2, chroma-js 2.4.2, build TypeScript i testy Vitest.

**DERIVED — decyzja:** wiedza o generator flow; dependency dopiero dla lokalnego explainera. Wejście: generator sceny i time events; wyjście: stan sceny/klip przez osobny exporter, nie master timeline FrameCut. Test: długi seek do końca i powrót na początek z pomiarem czasu; oddzielić koszt replay od samego renderu. Zewnętrzny mutowalny stan musi być resetowalny.

### Blender: skrypt steruje aplikacją, cache steruje historią

Odczytane oficjalne źródła instrukcji: [simulation_nodes.rst B43](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/physics/simulation_nodes.rst) i [command_line/render.rst B44](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/advanced/command_line/render.rst). Publiczny main dokumentacji nie ma tutaj ustalonego SHA. HTML manual nie był dostępny przez użyte narzędzie; raw RST odczytano. Nie odczytano implementacji kamery ani rendererów Blendera.

**DERIVED — decyzja:** używać istniejącej aplikacji jako narzędzia, nie budować ani vendoryzować Blendera. Interfejs adaptera: .blend+skrypt+frame range+bake manifest → sekwencja obrazów/passes i metadata. Zależności: zgodna aplikacja, silnik renderu, device, fonty i assety. Test: bake sequential → render shuffled oraz interruption/resume z porównaniem klatek. Integracja Python nie oznacza dostępności bpy w zwykłym interpreterze.

### FFmpeg: wykonawca końcowego grafu mediów

[doc/filters.texi B45](https://github.com/FFmpeg/FFmpeg/blob/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba/doc/filters.texi), odczytane sekcje overlay, minterpolate, setpts/asetpts; [vf_overlay.c B46](https://github.com/FFmpeg/FFmpeg/blob/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba/libavfilter/vf_overlay.c) pokazuje obsługę alpha i EOF. Wejściami overlay są dwa strumienie; wynikiem klatki composite. Zależności i dostępne filtry wynikają z konkretnego binary build.

**DERIVED — decyzja:** istniejący lokalny komponent, wywoływany przez ownera eksportu. Przejąć metodę jawnych timebases, nie kopiować C. Test: różne długości wejść, repeatlast/EOF, overlay straight vs premultiplied, zero-frame tail, final decoded frame count. Interpolacja ruchu nie zastępuje ekspozycyjnego motion blur; porównywać wynik na cięciu i zasłonięciu.

## 4. Licencja kodu nie jest licencją wszystkich materiałów

Poniższe etykiety opisują odczytane dokumenty, nie pełny audyt prawny dystrybucji przyszłego produktu. Nie pobrano ani nie użyto żadnego modelu 3D, muzyki, fontu czy filmu z tych repo.

| Materiał | Odczytany dokument i wynik | Decyzja integracyjna DERIVED | Assety i pozostałe prawa |
|---|---|---|---|
| Studio | [B59 LICENSE](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/LICENSE): Apache-2.0 | Zachować notices przy dystrybucji; trzymać własne ownership | Root license nie nadaje praw do zewnętrznych assetów |
| HyperFrames | [B49 LICENSE](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/LICENSE): Apache-2.0 | Sprawdzić notices i dependency tree wybranej paczki | Template media/fonty osobno |
| GSAP engine | [B25](https://gsap.com/standard-license): Standard No Charge, warunki szczególne m.in. visual no-code builders konkurujące z Webflow | Nie oznaczać jako MIT; ocenić rzeczywisty zakres produktu FrameMotion przed przyjęciem dependency | Licencja silnika nie obejmuje cudzych demo assetów |
| GSAP skills | [B58 LICENSE](https://github.com/greensock/gsap-skills/blob/aed9cfd3277740755f6bfc1155c7aa645403b760/LICENSE): MIT | Selektywna adaptacja z notice; to osobna licencja od silnika | Brak przejętych mediów |
| Remotion v4 | [B33 LICENSE.md](https://github.com/remotion-dev/remotion/blob/889c61f2da985832fd35efc29eac29ffd72be12e/LICENSE.md): warunkowa free license, m.in. indywidualnie/nonprofit/firmy do 3 pracowników, inaczej company license | Zweryfikować podmiot i zastosowanie; nie nazywać uniwersalnie darmowym open source | Template fonts/music/media osobno |
| Remotion v5 terms | [B34 terms](https://www.remotion.dev/docs/terms): strona wyraźnie upcoming, wejście wraz z v5 | Nie stosować jako aktualnego uzasadnienia v4 | Brak rozszerzenia praw do assetów |
| PixiJS | [B50 LICENSE](https://github.com/pixijs/pixijs/blob/eb96c76fa27c948c748ff0bb79fc7a29329cd5e9/LICENSE): MIT | Notices dla użytych komponentów | Atlasy, sprite’y, fonty osobno |
| Three.js | [B51 LICENSE](https://github.com/mrdoob/three.js/blob/b5a9e5730f6122498e187da8f7cdedd4358f5aa0/LICENSE): MIT | Biblioteka jako dependency; examples wymagają sprawdzenia swoich materiałów | Modele, HDRI i tekstury mają własne pochodzenie |
| Motion Canvas | [B52 LICENSE](https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/LICENSE): MIT | Notices, zgodność selected exporter sprawdzana osobno | Muzyka/VO/obrazy osobno |
| Blender | [B57 COPYING](https://github.com/blender/blender/blob/ca56249b6affcc1b79dcde5a7a7feaf6dd630e32/COPYING): wskazuje GNU GPL i plik pełnej licencji | Nie wywodzić warunków addon distribution z samego wywołania CLI; pełny audyt poza zakresem | .blend, render, fonty, modele i tekstury nie są automatycznie GPL aplikacji |
| FFmpeg | [B47 LICENSE.md](https://github.com/FFmpeg/FFmpeg/blob/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba/LICENSE.md): LGPL2.1+ baza, opcjonalne GPL/nonfree i biblioteki zmieniają warunki | Zanotować configuration rzeczywistego build przed redystrybucją | Kodek/licencja programu nie daje praw do materiału filmowego |

W przyszłym asset manifest minimalny zapis DERIVED obejmuje źródło, autora, konkretną licencję/zgodę, datę pozyskania, wymagane attribution i identyfikację pliku. Nie zastępuje go etykieta „znalezione na GitHub”. W research nie wykonano code-copy.

## 5. Co odrzucić lub odłożyć

| Kandydat / wzorzec | Powód | Dopuszczalna alternatywa i test |
|---|---|---|
| Pełny import wszystkich repo do Studio | Dubluje toolchain, właścicieli i ciężar aktualizacji | Jeden adapter w istniejącej trasie; test native round-trip |
| GSAP skills jako nadrzędny workflow | Web interactivity nie jest kontraktem filmu | Wybrane zalecenia timeline/cleanup jako wiedza; review owner conflicts |
| GSAP jako „MIT, więc bezwarunkowo można” | Inna licencja engine i instrukcji | Zakres produktu vs pinned terms przed dependency |
| Pixi ticker lub requestAnimationFrame jako zegar eksportu | Zależy od czasu wykonania i stanu | evaluateFrame od integer frame; shuffle test |
| Three setTime jako gwarancja deterministycznej fizyki | Dotyczy miksera animacji, nie dowolnej historii | Bake/replay; reverse seek fixture |
| HyperFrames distributed dla każdego rational FPS | Badany backend distributed ma węższą listę | Lokalny render albo jawnie unsupported; decoded rate test |
| Bezpośrednie użycie nadchodzących Remotion v5 terms dla v4 | Strona określa przyszłe wejście w życie | Pinned license aktualnego wdrożenia |
| „Świeższy commit = szybszy/stabilniejszy” | Brak benchmarków i regresji w tym research | Porównanie tej samej sceny przy tym samym quality target |
| Dowolny demo pack / marketplace preset | Niezweryfikowane prawa, materiały i hidden dependencies | Własna scena syntetyczna lub zatwierdzony asset manifest |
| Unknown FrameMotion/FrameCut standalone repositories | Brak podanych adresów; nazwa produktu nie identyfikuje źródła | Zachować obecny publiczny FrameCut w Studio; ponowny audyt po wskazaniu URL |
| Nowe native fields v1 bez migracji | Rzeczywisty strict validator odrzuca nieznane pola | Sidecar **proponowany**, później versioned migration |
| Blender source build do zwykłego renderu | Zbędny koszt wobec istniejącej aplikacji | Skrypt w kompatybilnej aplikacji; bez instalacji podczas research |

## 6. Kolejność wykorzystania

**DERIVED:** P0 — potwierdzić native handshake i zachować kontrakty Studio. P1 — kwalifikować jeden obecny renderer HTML albo Remotion wspólnym fixture: exact copy, transform, alpha, rational time, audio cue, memory/resume. P2 — dodać Pixi/Three/Blender tylko przy konkretnym wymaganiu wizualnym; Motion Canvas dla explainera, GSAP dla organizacji animacji. Wszystkie wyjścia trafiają do obecnej kontroli jakości i ownera delivery.

Wspólny fixture powinien być krótki, mieć znaną liczbę klatek, polskie znaki, lokalne assety i akceptowane referencje. Powinien wykryć brak funkcji, a nie tylko uruchomić renderer. Testy oraz ewentualna implementacja pozostają przyszłym zadaniem; ten katalog nie jest zgodą na instalację, zakup, upload ani publikację.

