# DR-03 — nowe zasoby motion dla FrameCore
**Data: 2026-11-11. Badanie wykonane; integracje i testy wykonawcze: NOT_RUN.** Raport dla Claude jako głównego architekta, bez deklaracji architektonicznej akceptacji.

Największa możliwa korzyść to małe moduły proceduralne, wąskie adaptery istniejących rendererów i wybrane rodziny assetów. Baseline jest już rozbudowany: posiada kontrolę klatek, Lottie/Pixi/D3/Three, eksport Canvas i osobne werdykty jakości. Kolejny pełny silnik lub ogólny katalog efektów miałby duże nakładanie się z istniejącymi narzędziami. To wniosek **DERIVED** z odczytanych źródeł, nie wynik benchmarku. [Baseline i dowody](BASELINE.md)

## Zakres i wynik katalogu
Zebrano **30 kandydatów**: 12 modułów wykonawczych, 9 pozycji wiedzy i 9 kolekcji/assetów. **12 pogłębionych analiz** obejmuje R01/R03/R04/R06/R09, K01/K03/K06/K07 i A01/A03/A06. Katalog zawiera 9 NEW, 15 KNOWN_NEW_CAPABILITY, 4 ALREADY_COVERED, 1 DUPLICATE/FORK i 1 BASELINE_UNKNOWN. Zatem 30 pozycji nie oznacza 30 nowych możliwości.

Rejestr zawiera **220 rekordów źródeł / 205 różnych URL**. Wlicza manifesty, kod, metadane, źródła baseline i jawnie nieudane odczyty; nie oznacza 220 przeczytanych pełnych dokumentów ani niezależnych potwierdzeń. Zakres odczytu zapisano przy każdym rekordzie. [SOURCES.json](SOURCES.json) · [Metoda i etykiety](METHODOLOGY.md)

Wyniki użytkowe:
- [CATALOG.csv](CATALOG.csv) i [CATALOG.json](CATALOG.json): pola porównawcze i źródła.
- [CARDS.md](CARDS.md): kompletne karty wszystkich 30 pozycji.
- [DEEP_DIVES.md](DEEP_DIVES.md): kod/manifesty/prawa oraz karty adaptacji wiedzy.
- [RANKINGS.md](RANKINGS.md): oddzielnie nowa użyteczność, assety i wiedza.
- [TEST_PLAN.md](TEST_PLAN.md): 12 rodzajów prób, wszystkie NOT_RUN.
- [TIME_ADAPTER.md](TIME_ADAPTER.md): interakcja → czas/seek → render.
- [IMPLEMENTATION_HANDOFF.md](IMPLEMENTATION_HANDOFF.md): P0/P1/P2 i materiał do decyzji Claude.
- [REJECTIONS.md](REJECTIONS.md): duplikaty, nakładanie się i REFERENCE_ONLY.

## Baseline: co już istnieje
Przypięto Studio **4611c9c4ed44579b8a2c0224c9276d955fccd8d6** (2026-11-11; manifest 1.174.1), Toolbox **adc8094f8e087889e4337c99dd0d267ae1b11a51** (2026-11-07; 1.12.0) i Open Assets **889471fcdbc2216ddc465715eff0e82784d5b8ee** (2026-11-06; 0.5.0). To wersje źródłowe. Installed version i działanie w tej sesji nie były testowane. [Pełne zestawienie](BASELINE.md)

Toolbox ma 27 narzędzi plus indeks, m.in. GL transitions, PixelFX, Animate, motion-designer, GSAP/Three skills, motion-launch-videos, Manim, papercut, stickman-kino i cutaway. Sam review w katalogu nie oznacza aktywnej pozycji: istnieją też usunięte wpisy. [Przypięty manifest](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/.claude-plugin/marketplace.json)

useAnimations i LottieFiles Generative Icons pozostają znane z wcześniejszych **raportowanych** prób. Aktualny zapis repo jest documentation-only i nie dodaje dependencies/entries/runtime. Nie odczytano oryginalnych mediów tych prób. Source/CLI/catalog versions są odrębne; reported alpha/seek/repeatability wyników nie wolno rozciągać na całą bibliotekę ani na tę sesję. [Sekcja 14 handovera](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/docs/handover-creme-de-la-creme-2026-11-09.md)

Repozytorium i API **FrameMotion pozostają Unknown**. Studio koordynuje produkcję; Toolbox odpowiada za katalog i adaptery, Open Assets za media/proweniencję, FrameCut za montaż. Proponowany właściciel nowego adaptera motion wymaga decyzji Claude. Badanie nie zmienia tych granic.

## Najistotniejsze ustalenia
**1. Parametr time lub seed nie wystarcza do filmu z losowym seek.** EffectPass w postprocessing kumuluje material.time, a Pixi GlitchFilter używa Math.random dla części geometrii mimo uSeed. Najpierw whitelist prostych efektów, a potem pełny model RNG/history albo bake. R06 simplex-noise ma mniejszy zakres: PRNG dostarczany przy tworzeniu funkcji, następnie noise zależny od współrzędnych. Propozycja okresowego pola z modulo frame jest DERIVED. [EffectPass](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/passes/EffectPass.js) · [GlitchFilter](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/glitch/GlitchFilter.ts) · [simplex source](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/simplex-noise.ts)

**2. Tekst potrzebuje kontraktu przygotowania.** Troika sync callback działa w gałęzi wymagającej synchronizacji; bezwarunkowe oczekiwanie na taki callback przy każdej niezmienionej klatce może zawiesić adapter. Grapheme segmentation i negative font cases są użytecznymi dodatkami do obecnego font readiness. Nie zastępują shaping, glyph coverage ani przeglądu polskiego tekstu. [Troika Text.js](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/Text.js) · [UAX29 rev49](https://unicode.org/reports/tr29/tr29-49.html) · [W3C FontFaceSet.check](https://www.w3.org/TR/2023/WD-css-font-loading-3-20230406/#font-face-set-check)

**3. Automatyczny screenshot może ukryć badany problem.** Playwright screenshot assertion domyślnie wyłącza animacje. K03 proponuje explicit clock/settled i capture policy oraz celową scenę negatywną z uciekającym zegarem. Nie jest to zarzut wobec Playwright ani dowód wad obecnego Studio: to warunek prawidłowego przyszłego fixture. [Przypięty matcher](https://github.com/microsoft/playwright/blob/3b438229c6a2ccdbe2d3572755935892203d83c3/packages/playwright/src/matchers/toMatchSnapshot.ts)

**4. Rive wymaga kwalifikacji konkretnego runtime i assetu.** Cookbook i przypięte typy różnią się opisem advance/advanceAndApply. State-machine replay ze stałym krokiem jest propozycją, nie dowiedzionym arbitrary seek. Layer Masks i inne funkcje muszą odpowiadać rendererowi. K06/A05 pozostają P2. [Cookbook](https://github.com/rive-app/rive-docs/blob/047f52be339575f86eb0710a5512e2c600e14313/runtimes/web/low-level-api-usage.mdx) · [Runtime types](https://github.com/rive-app/rive-wasm/blob/b61517a5bdcdcce54c4b5f50e86bac7e11fadecc/js/src/rive_advanced.mjs.d.ts)

**5. Gotowy asset nie oznacza gotowego interchange.** Meteocons source/release/site mają różne wersje; gotowe outputs nie są tym samym co przypięty source commit. DAEDAL deklaruje MP4 na czerni, co nie jest kanałem alpha. Quaternius rozdziela darmowy Standard od płatnego source .blend. Każdy wariant potrzebuje praw i własnego hasha pliku przed użyciem. Szczegółowe primary źródła i Unknown: [karty assetów](agents/assets/CARDS.md).

**6. Licencja kodu nie obejmuje automatycznie wszystkich materiałów.** R02 ma ISC w manifest i MIT w LICENSE; R12 ma mieszane licencje test fonts. R09 jest MPL-2.0 i wymaga odrębnego rozważenia dystrybucji kodu/binariów. Poly Haven i ambientCG różnie opisują prawa do previews. Raport rozdziela rendered-film use, source redistribution, code, media, fonts, models i examples. [R02 manifest](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/package.json) · [R02 LICENSE](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/LICENSE) · [R12 fonts](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/test/fonts/LICENSE)

## Pokrycie kategorii i uczciwe luki
| Kategoria | Trafne delty lub baseline | Pozostała luka |
|---|---|---|
| Kinetic typography / reveals / layout | R03/R12, K01/K02/K08; baseline GSAP/SplitText | Shaping/ligatures/emoji/fonts wymagają realnego testu; brak gotowego nowego kompletnego text engine |
| Shape/path/stroke/masks/mattes | R01/R02; baseline MorphSVG/DrawSVG/Lottie | Compound paths/holes ograniczają flubber; track matte zgodność zależna od renderera |
| Transitions/particles/trails/generative | R06/R08, A02, R11 comparator; baseline GL transitions/PixelFX | Symulacje z pełnym deterministic seek niepotwierdzone; R11 nie wnosi dowiedzionej przewagi |
| Shaders/displacement/lighting/postprocessing | R04/R05/R06, A07/A08 baseline | Temporal history, WebGL/WebGPU parity, HDR i GPU cost NOT_RUN |
| Glitch/CRT/VHS/pixel/dithering/ASCII/halftone | R05 CRT; baseline PixelFX i shader transitions | Nie znaleziono w shortlist dobrze kwalifikowanej nowej paczki pełnego VHS/ASCII/halftone; jawna luka, nie dopełniamy nazwami |
| 2.5D/3D/geometry/physics/camera | R03, A03/A04; baseline Anatomy/Cutaway/Three; R07 comparator | Cloth/fluid/live physics i camera rigs bez nowej, wiarygodnie zakwalifikowanej pozycji; VDB to baked asset |
| UI/product/diagram/chart/explainer | A01/A05, R01; baseline D3/Animate/Manim/motion-launch | Asset-family advantage vs model-authored geometry niemierzone |
| Audio reactive/beat/onset/captions | K04 oraz K01; baseline Earshot/captions | Nie wykonywano analizy/odsłuchu; real-time analyser nie jest offline export contract |
| Alpha/compositing/blur/grain/glow/export | K07/R09/R10, R04/R05, A06 | A06 bez deklarowanej alfy; ActionVFX terms niedostępne; brak nowego positive alpha-overlay testu |

## Zgodność z silnikami: droga, nie deklaracja działania
| Host | Proponowana droga | Status |
|---|---|---|
| Remotion | Pure frame props; Three modules przez istniejącą integrację, Lottie konkretnym rendererem | ADAPTER/DOCUMENTED; integracja NOT_RUN |
| HyperFrames/GSAP/HTML | Paused timeline, input events jako dane, master time zamiast scroll/RAF | DERIVED na baseline; NOT_RUN |
| SVG/Canvas | Interpolacja geometry do statycznego stanu; R09 tylko static SVG rasterization | CODE_INSPECTED; import/export NOT_RUN |
| PixiJS | Existing manual app.render; wybrany filtr z kontrolą time/RNG/padding | CODE_INSPECTED + DERIVED; NOT_RUN |
| Three.js/WebGL | R03/R04; pełne uniforms/state z klatki, history effects osobno | CODE_INSPECTED; headless/GPU NOT_RUN |
| Blender | A03 retarget lub A04 VDB → jawnie wyrenderowany clip/EXR | DOCUMENTED asset route/DERIVED adapter; NOT_RUN |
| FFmpeg | Encoding/decoding już gotowych klatek; K07 diagnostics per dostępny build | CODE_INSPECTED/DOCUMENTED; lokalna obsługa NOT_RUN |

Nie zakładamy dostępności tych silników w aktualnym środowisku. PNG RGBA, opaque MP4, alpha WebM/ProRes i EXR mają różne wymagania; konkretnego eksportu nie potwierdza sama nazwa kontenera. Metadane nie dowodzą wyglądu, brzmienia ani jakości szwu.

## Zalecana kolejność dalszych decyzji
**P0:** exact-copy graphemes/font negative fixtures, prawidłowy capture QA, deklaracja modelu czasu, rozdzielone prawa i tożsamość assetu, mały spec seeded noise. **P1:** bounded text/shader/shape/asset pilot i alpha/renderer qualification. **P2:** stateful Rive, symulacje/VDB/retarget, kosztowne albo nadal niejasne ścieżki. Szczegóły, owner i acceptance zawiera [handoff](IMPLEMENTATION_HANDOFF.md).

Toolbox wymaga udokumentowanej konkretnej poprawy przed admission. Żadna nowa integracja nie otrzymała takiego dowodu w tym researchu. [Toolbox rules](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/CLAUDE.md)

## Weryfikacja i ograniczenia
Badanie wykonały trzy specjalizacje collaboration w rozłącznych plikach; częściowe wyniki po przerwaniu odtworzono. Świeży recenzent niezależnie sprawdzał dokumenty i primary claims. Jego wynik to **PASS_RESEARCH_ARTIFACTS_AFTER_CORRECTIONS** po 17 celowanych sprawdzeniach źródeł; wszystkie trzy uwagi rozstrzygnięto. Szczegóły są w [REVIEW.md](review/REVIEW.md) i [RESOLUTION.md](review/RESOLUTION.md). Lokalny check `python3 verify_artifacts.py` zakończył się **PASS / exit 0**; zakres opisuje [VERIFICATION.md](VERIFICATION.md). Hipson: **T-0006**, końcowy status i świeży wynik checku znajdują się w ledgerze.

Kontrola strukturalna potwierdza kompletność i spójność artefaktów, hash promptu i odwołania; nie jest testem produktu. Nie wykonano instalacji, uruchomienia pobranego kodu, pobrań binarnych assetów, renderów, oglądu mediów ani odsłuchu, płatnych usług, prywatnych uploadów, push/deploy/publikacji. Claude CLI nie uruchamiano po wcześniej zgłoszonym OAuth401 zgodnie z wyjątkiem dla tego badania.

Nie potwierdzono installed versions, pełnej zgodności rendererów, performance/memory, jakości alfy/seam ani zmierzonej oszczędności produkcji. Rozstrzygnięte są jedynie wskazane kwestie dokumentacyjne/kodowe; wykonanie pozostaje **NOT_RUN**.

