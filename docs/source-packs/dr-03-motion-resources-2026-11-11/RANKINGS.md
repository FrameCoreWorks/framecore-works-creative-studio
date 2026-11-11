# DR-03 — trzy osobne rankingi
**DERIVED**, 2026-11-11. To kolejność kwalifikacji i prób, nie wynik benchmarku ani akceptacja produkcyjna. Dowody/commity/prawa dla każdego ID: CATALOG.json i CARDS.md. Ocena „kontrola” opisuje czytelność drogi z inspekcji, nie zaliczony render. Jakość wizualna wszystkich kandydatów pozostaje NOT_RUN.

## 1. Nowa użyteczność modułów wykonawczych
| Miejsce | Kandydat / nowa wartość | Kontrola czasu | Prawa i koszt integracji — DERIVED | Decyzja |
|---|---|---|---|---|
| 1 | R06 simplex-noise: mały seeded scalar field dla tła/displacement/trails, bez kolejnego silnika | Dobra droga: PRNG w init, parametry funkcją klatki; loop z modulo frame | MIT kod; 0.5–1.5 dnia helper+fixture | P0 projekt małej metody; potem test |
| 2 | R03 Troika: SDF text mesh i readiness dla Three | Async layout trzeba przygotować i cache; nie Promise(sync) każdą klatkę | MIT kod, fonty osobno; 1–3 dni | P1 lokalne fonty/PL/timeout, wcześniej P0 spec readiness |
| 3 | R04 postprocessing: whitelist bloom/outline, ograniczone dodatkowe efekty | render(delta) kumuluje time; per-effect adapter | Zlib kod, media osobno; 2–4 dni | P1 tylko efekty bez historii |
| 4 | R01 flubber: lekki geometry-only morph zamkniętych konturów | Interpolator przyjmuje progress; wielokonturowe glyph/logo ograniczone | MIT; 0.5–2 dni | P1 przy realnej potrzebie bez GSAP; baseline MorphSVG pozostaje |
| 5 | R12 opentype.js: glif jako edytowalna geometria | Host nadaje czas; shaping i ligatury oddzielne | MIT kod, mieszane font fixtures; 1–3 dni | P1 deformacja glifów; nie prosty text reveal |
| 6 | R05 pixi-filters: CRT z jawnym time/seed | Tylko wąski profil; glitch ma niezależne Math.random | MIT; 1–3 dni | P1 CRT; glitch HOLD |
| 7 | R09 resvg-js: CPU SVG→PNG bez pełnego browser capture | Każda klatka musi być statycznie materializowanym SVG | MPL-2.0, alpha prerelease/native dependencies; 2–5 dni | P1 kwalifikacja, produkcja HOLD; nie proponować HEAD jako stabilnego |
| 8 | R02 svg-path-properties: path metrics w Node | Geometria bez własnego zegara | ISC w package vs MIT LICENSE; 0.5–2 dni plus wyjaśnienie praw | HOLD redystrybucji do wyjaśnienia, wąski pilot dopiero później |

R10 pixelmatch jest uzupełnieniem **istniejącego QA**, nie nową możliwością motion. R08 three.quarks pozostaje P2 do pełnego seed/replay/bake; R07 Zdog jest ALREADY_COVERED, R11 MeshLine to DUPLICATE/FORK. Nie dodajemy ich dla liczby.

Istotne źródła rankingu: [simplex implementation](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/simplex-noise.ts), [Troika Text](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/Text.js), [EffectPass](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/passes/EffectPass.js), [GlitchFilter](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/glitch/GlitchFilter.ts). Same source inspections nie ustalają jakości.

## 2. Gotowe assety — priorytet pozyskania do pilota
| Miejsce | Kandydat | Dlaczego może oszczędzić pracę | Najważniejszy warunek |
|---|---|---|---|
| 1 | A01 Meteocons | Spójna, specjalistyczna rodzina weather SVG/Lottie | Rozdzielić source/release/site version, hash konkretnego pliku, renderer feature QA; reported seam issue |
| 2 | A02 Kenney Particle Pack | Tekstury zamiast rysowania każdego sprite; CC0 | Statyczne tekstury nie są potwierdzonym flipbookiem; alpha/inventory/decode Unknown |
| 3 | A06 DAEDAL Bokeh & Particles | Gotowe MP4 do prostego compositingu, CC0 | Czarne tło nie jest kanałem alpha; 35,525,100 B przekracza domyślny cap 32 MiB wskazany w source review |
| 4 | A03 Quaternius Universal Animation Library 2 | Ruch humanoida/rig i root-motion zamiast nowej symulacji postaci | Retarget/clip FPS/loop do inspekcji; source .blend jest płatnym wariantem, nie kupiono |
| 5 | A05 Rive Vehicle Loader | Konkretny CC BY 4.0 asset do kwalifikacji interakcji → timeline | Prawa konkretnego itemu, credit/zmiany; renderer/state machine gate; nie whole-gallery clearance |
| 6 | A04 JangaFX Tornado Looping | Gotowa symulacja VDB zastępuje kosztowny bake od zera | 1.7 GB, fps/grids Unknown, Blender/volume render; P2 on-demand, nie bundle |

A07 Poly Haven Studio Small 09 i A08 ambientCG Metal046B pozostają użytecznymi fixtures **ALREADY_COVERED**, nie nowymi providerami. A09 ActionVFX jest **REFERENCE_ONLY** z nieodczytanymi terms; nie trafia do rankingu użytkowego. Parametry assetów są danymi autorów/metadanymi, nie własnymi pomiarami ani oceną seam/alfa.

## 3. Wiedza do adaptacji w istniejących właścicielach
| Miejsce | Kandydat | Konkretna delta | Forma i koszt — DERIVED |
|---|---|---|---|
| 1 | K01 + K02 | Pełne graphemes, exact copy, negative font fixtures; check() true nie dowodzi właściwego glyph | SKILL_ADAPTATION, 0.5–1.5 dnia |
| 2 | K03 | Playwright default screenshot może wyłączyć badany ruch; explicit capture + celowy live-clock negative | SKILL_ADAPTATION w obecnym QA, 1–2 dni |
| 3 | K07 | Oddzielić alpha presence/association/decoded evidence; undetermined nie znaczy premultiplied | KNOWLEDGE_ONLY + fixture, 0.5–1 dnia |
| 4 | K05 | Per-asset/per-renderer Lottie feature matrix zamiast valid JSON = visually correct | SKILL_ADAPTATION, 1–2 dni |
| 5 | K04 | Onset time różny od backtracked slice point; jawne mapowanie sample→frame | KNOWLEDGE_ONLY, 0.5–1.5 dnia |
| 6 | K08 | Seek callbacks i side effects nie są tym samym co stan timeline | KNOWLEDGE_ONLY, 0.5–1 dnia |
| 7 | K06 | Rive low-level API drift; linear animation i state-machine replay osobno | ADAPTER/P2, 3–5 dni plus asset qualification |

K09 Remotion flicker cookbook jest **ALREADY_COVERED** i pełni rolę kontroli negatywnej nowości. R10 comparator policy warto dołączyć do K03, gdy obecny diff helper nie pokrywa wymogu; nie instalować tylko dla nowej nazwy.

Szacunki nie sumują się automatycznie: wspólne fixtures i adaptery współdzielą pracę. Cały ranking wymaga sprawdzenia przy konkretnym briefie i API FrameMotion. Konkretny wynik może odrzucić wysoko sklasyfikowaną pozycję.

